---
title: "CF 471D - MUH and Cube Walls"
description: "We have two walls represented by sequences of tower heights. The bears' wall contains n towers, while Horace's wall contains w towers. Horace is allowed to shift his entire wall vertically by any amount."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 471
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 269 (Div. 2)"
rating: 1800
weight: 471
solve_time_s: 118
verified: true
draft: false
---

[CF 471D - MUH and Cube Walls](https://codeforces.com/problemset/problem/471/D)

**Rating:** 1800  
**Tags:** string suffix structures, strings  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two walls represented by sequences of tower heights.

The bears' wall contains `n` towers, while Horace's wall contains `w` towers. Horace is allowed to shift his entire wall vertically by any amount. Every tower in his wall must be shifted by the same value, but that value may be positive, negative, or zero.

For a segment of length `w` in the bears' wall, we want to know whether Horace can choose some vertical shift so that his wall exactly matches that segment. The task is to count how many such segments exist.

The key detail is that Horace may add the same constant to every tower in his wall. This means absolute heights do not matter. Only the differences between consecutive towers matter.

The constraints reach `2 · 10^5` elements. Any algorithm that compares every length-`w` segment against the pattern directly would require roughly `n · w` operations, which can reach about `4 · 10^10`, far beyond what fits into a 2-second limit. We need something close to linear time.

Several edge cases are easy to miss.

Consider:

```
n = 5, w = 1
a = [10, 20, 30, 40, 50]
b = [7]
```

Every single tower can match a one-tower wall because Horace may shift his wall by any amount. The correct answer is `5`.

A solution based only on difference arrays would produce empty difference sequences and might incorrectly return `0` unless this case is handled separately.

Another example:

```
a = [5, 8, 11]
b = [1, 4]
```

The segment `[5,8]` matches after adding `4` to every element of `b`, and `[8,11]` also matches after adding `7`.

The answer is `2`, even though no heights are equal directly.

A third example shows why consecutive differences are enough:

```
a = [100, 103, 106]
b = [1, 4, 7]
```

Differences are:

```
a: [3, 3]
b: [3, 3]
```

The walls match after adding `99` to every element of `b`.

## Approaches

A brute-force solution examines every length-`w` segment of the bears' wall. For each segment, compute the shift needed to align the first tower, then verify that every remaining tower matches after applying that shift.

This is correct because a valid match must use a single constant shift. The problem appears when we analyze the cost. There are approximately `n` candidate segments, and each comparison may inspect up to `w` towers. The worst-case complexity is `O(nw)`, which becomes about `4 · 10^10` operations when both arrays have length `2 · 10^5`.

The crucial observation is that adding a constant to every tower preserves consecutive differences.

Suppose Horace's wall is:

```
b1, b2, b3, ...
```

and we add some value `c`:

```
b1+c, b2+c, b3+c, ...
```

Then:

```
(b2+c) - (b1+c) = b2-b1
```

and similarly for every adjacent pair.

A segment matches Horace's wall after some shift if and only if their difference arrays are identical.

Let:

```
DA[i] = a[i+1] - a[i]
DB[i] = b[i+1] - b[i]
```

A match of the original walls corresponds exactly to an occurrence of `DB` inside `DA`.

Now the problem becomes a classic string matching problem on integer sequences. We need to count how many times pattern `DB` occurs in text `DA`.

The Knuth-Morris-Pratt algorithm finds all occurrences of a pattern in linear time. Since the difference arrays have lengths `n-1` and `w-1`, the total complexity becomes `O(n+w)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nw) | O(1) | Too slow |
| Optimal (Differences + KMP) | O(n+w) | O(n+w) | Accepted |

## Algorithm Walkthrough

1. Read the two height arrays.
2. Handle the special case `w = 1`.

Any single tower can match a one-tower elephant wall after choosing an appropriate vertical shift. The answer is simply `n`.
3. Build the difference array of the bears' wall.

For every adjacent pair, store:

```
a[i+1] - a[i]
```

Two matching walls must have identical consecutive differences.
4. Build the difference array of Horace's wall in the same way.
5. Compute the KMP prefix-function for the pattern difference array.

The prefix-function stores, for every position, the length of the longest proper prefix that is also a suffix. KMP uses this information to avoid rechecking values after mismatches.
6. Run KMP matching on the bears' difference array.

Whenever the matched pattern length reaches `len(DB)`, one occurrence has been found.
7. Count all occurrences and print the result.

### Why it works

Two walls differ only by a vertical shift if there exists a constant `c` such that every corresponding tower differs by exactly `c`.

If such a constant exists, every adjacent difference is identical, so the difference arrays match.

Conversely, if the difference arrays match, then after aligning the first tower of Horace's wall with the first tower of the segment, all remaining towers are forced to match because every consecutive change is the same. Thus matching difference arrays are both necessary and sufficient.

KMP finds every occurrence of the pattern difference array inside the text difference array, so every valid segment is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def prefix_function(pattern):
    pi = [0] * len(pattern)

    for i in range(1, len(pattern)):
        j = pi[i - 1]

        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]

        if pattern[i] == pattern[j]:
            j += 1

        pi[i] = j

    return pi

def solve():
    n, w = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    if w == 1:
        print(n)
        return

    text = [a[i + 1] - a[i] for i in range(n - 1)]
    pattern = [b[i + 1] - b[i] for i in range(w - 1)]

    pi = prefix_function(pattern)

    j = 0
    ans = 0

    for x in text:
        while j > 0 and x != pattern[j]:
            j = pi[j - 1]

        if x == pattern[j]:
            j += 1

        if j == len(pattern):
            ans += 1
            j = pi[j - 1]

    print(ans)

solve()
```

The first important choice is handling `w = 1` immediately. The difference array of a one-element wall is empty, and trying to run KMP on an empty pattern complicates the implementation unnecessarily. Every position is valid, so the answer is simply `n`.

The next step converts both walls into difference arrays. This transformation removes the irrelevant absolute heights and keeps exactly the information preserved under vertical shifts.

The prefix-function is the standard KMP preprocessing phase. It records how much of the pattern remains matched after a mismatch, allowing the scan to stay linear.

During the matching phase, `j` always represents the current matched prefix length. When `j` reaches the full pattern length, one occurrence has been found. Resetting `j` to `pi[j-1]` allows overlapping matches to be counted correctly.

All arithmetic fits comfortably in Python integers. Differences may be negative, but KMP works on arbitrary integer sequences exactly as it works on strings.

## Worked Examples

### Sample 1

Input:

```
13 5
2 4 5 5 4 3 2 2 2 3 3 2 1
3 4 4 3 2
```

Difference arrays:

```
DA = [2,1,0,-1,-1,-1,0,0,1,0,-1,-1]
DB = [1,0,-1,-1]
```

| Text Position | Value | Matched Length After Processing | Occurrence Found |
| --- | --- | --- | --- |
| 0 | 2 | 0 | No |
| 1 | 1 | 1 | No |
| 2 | 0 | 2 | No |
| 3 | -1 | 3 | No |
| 4 | -1 | 4 | Yes |
| 5 | -1 | 0 | No |
| 6 | 0 | 0 | No |
| 7 | 0 | 0 | No |
| 8 | 1 | 1 | No |
| 9 | 0 | 2 | No |
| 10 | -1 | 3 | No |
| 11 | -1 | 4 | Yes |

Total occurrences: `2`.

This trace shows exactly what we wanted. The pattern difference sequence appears twice inside the bears' difference sequence, so there are two valid wall segments.

### Example 2

Input:

```
3 2
5 8 11
1 4
```

Difference arrays:

```
DA = [3,3]
DB = [3]
```

| Text Position | Value | Matched Length After Processing | Occurrence Found |
| --- | --- | --- | --- |
| 0 | 3 | 1 | Yes |
| 1 | 3 | 1 | Yes |

Answer: `2`.

Both length-2 segments match after choosing different vertical shifts. This example demonstrates that absolute heights are irrelevant once the difference pattern matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + w) | Building difference arrays, computing prefix-function, and KMP scan are all linear |
| Space | O(n + w) | Stores the difference arrays and prefix-function |

With `n, w ≤ 2 · 10^5`, a linear-time algorithm performs only a few hundred thousand operations and comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def prefix_function(pattern):
        pi = [0] * len(pattern)

        for i in range(1, len(pattern)):
            j = pi[i - 1]

            while j > 0 and pattern[i] != pattern[j]:
                j = pi[j - 1]

            if pattern[i] == pattern[j]:
                j += 1

            pi[i] = j

        return pi

    n, w = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    if w == 1:
        return str(n)

    text = [a[i + 1] - a[i] for i in range(n - 1)]
    pattern = [b[i + 1] - b[i] for i in range(w - 1)]

    pi = prefix_function(pattern)

    ans = 0
    j = 0

    for x in text:
        while j > 0 and x != pattern[j]:
            j = pi[j - 1]

        if x == pattern[j]:
            j += 1

        if j == len(pattern):
            ans += 1
            j = pi[j - 1]

    return str(ans)

# provided sample
assert run(
"""13 5
2 4 5 5 4 3 2 2 2 3 3 2 1
3 4 4 3 2
"""
) == "2", "sample 1"

# minimum size
assert run(
"""1 1
5
10
"""
) == "1", "single tower"

# w = 1
assert run(
"""5 1
10 20 30 40 50
7
"""
) == "5", "every position matches"

# all equal values
assert run(
"""5 3
7 7 7 7 7
2 2 2
"""
) == "3", "all zero differences"

# off-by-one boundary
assert run(
"""4 4
10 11 13 16
1 2 4 7
"""
) == "1", "whole array matches"

# no match
assert run(
"""5 3
1 2 3 4 5
1 3 6
"""
) == "0", "pattern absent"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, w=1` | `1` | Smallest legal input |
| `w=1` | `n` | Special-case handling |
| All equal heights | `3` | Zero-difference patterns |
| `n=w` matching arrays | `1` | Whole-array match boundary |
| No occurrence | `0` | Correct rejection |

## Edge Cases

Consider the one-tower pattern:

```
5 1
10 20 30 40 50
7
```

The algorithm immediately triggers the `w == 1` branch and returns `5`. Every tower can become height `7` after choosing an appropriate shift, so every position is valid.

Now consider a case where matching requires a large shift:

```
3 3
100 103 106
1 4 7
```

Difference arrays are:

```
DA = [3,3]
DB = [3,3]
```

KMP finds one occurrence. The algorithm never uses the actual shift value `99`, because matching differences already proves that such a shift exists.

Finally, consider repeated values:

```
5 3
7 7 7 7 7
2 2 2
```

Difference arrays become:

```
DA = [0,0,0,0]
DB = [0,0]
```

KMP finds occurrences starting at positions `0`, `1`, and `2`, producing answer `3`. Overlapping matches are counted correctly because after every full match, KMP falls back using the prefix-function instead of restarting from zero.
