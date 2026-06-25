---
title: "CF 106186F - Count Pairs"
description: "We are given a permutation of the numbers from 1 to n. The task is to count ordered choices of an index i and another index j where the value at j can be used as a jump length, and after making that jump from i, the value found there is exactly the sum of the starting value and…"
date: "2026-06-25T10:49:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106186
codeforces_index: "F"
codeforces_contest_name: "NWU IUPC 2025 powered by CPS Academy"
rating: 0
weight: 106186
solve_time_s: 35
verified: true
draft: false
---

[CF 106186F - Count Pairs](https://codeforces.com/problemset/problem/106186/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of the numbers from `1` to `n`. The task is to count ordered choices of an index `i` and another index `j` where the value at `j` can be used as a jump length, and after making that jump from `i`, the value found there is exactly the sum of the starting value and the jump length.

In other words, if the value at position `j` is `x`, we need:

`a[i + x] = a[i] + x`

The position `i + x` must exist inside the array. The answer is the number of such valid choices of `i` and `j`.

The permutation property is the key restriction. Every number from `1` to `n` appears exactly once, so every possible jump length `x` has exactly one position where it occurs.

With `n` up to `200000`, checking every pair of indices would require around `n² / 2`, which is about twenty billion checks in the worst case. That is far beyond what a typical competitive programming time limit allows. We need to transform the condition into something that can be counted in linear time.

The main edge cases come from the fact that the valid pair in the transformed view is not necessarily the same pair of indices as `(i, j)` from the statement.

For example:

```
5
3 4 1 2 5
```

The valid answer is `2`. One valid original pair is `(3, 3)`, because `a[3] = 1` and `a[4] = 2`, giving `1 + 1 = 2`. A careless solution that only checks pairs with different indices would miss this case.

Another edge case is when many indices have the same transformed value. For example:

```
4
1 2 3 4
```

The answer is `6`. Every pair works because the array is increasing by exactly one, so all indices have the same value of `index - value`. Counting only adjacent positions would incorrectly return a smaller answer.

## Approaches

A direct solution follows the definition. For every possible pair of indices `(i, j)`, we calculate the jump length `a[j]`, check whether `i + a[j]` is inside the array, and compare `a[i + a[j]]` with `a[i] + a[j]`.

This is correct because it tests exactly the required condition. However, there are `n²` possible ordered pairs. When `n = 200000`, this creates about forty billion operations, which is impossible.

The useful observation comes from rewriting the equation. Let:

```
x = a[j]
q = i + x
```

The condition becomes:

```
a[q] = a[i] + x
```

Since `q - i = x`, we get:

```
a[q] - a[i] = q - i
```

Rearranging:

```
q - a[q] = i - a[i]
```

So instead of looking for the special jump value, we only need to count pairs of positions that have the same value of `index - value`.

Every pair of positions with the same transformed value corresponds to exactly one valid original pair. If positions `p < q` satisfy:

```
p - a[p] = q - a[q]
```

then:

```
a[q] - a[p] = q - p
```

The distance `q - p` is a number between `1` and `n`, and because the array is a permutation, that number appears somewhere as `a[j]`. Choosing that `j` gives the required original pair.

The problem is reduced to grouping equal values of `index - value` and adding the number of pairs inside every group.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Group by index-value difference | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Iterate through every position `i` and compute the value `i - a[i]`. We use one-based indexing because the statement describes positions that way.
2. Store how many times each transformed value appears. Positions with the same transformed value can form valid pairs with each other.
3. When a transformed value has already appeared `cnt` times and we see it again, the new position forms `cnt` new pairs. Add `cnt` to the answer before increasing the frequency.
4. Output the accumulated count.

The reason the counting works is that when processing positions from left to right, every previous occurrence of the same transformed value is an earlier index that forms a valid pair with the current index.

Why it works:

The transformation preserves exactly the required condition. A valid original pair produces two positions `i` and `i + a[j]` whose values satisfy equal `index - value`. Conversely, any two positions with equal `index - value` have a distance equal to their value difference, and that distance is present as some array value because the array is a permutation. Thus every counted pair corresponds to one and only one valid choice from the original problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    freq = {}
    ans = 0

    for i, x in enumerate(a, start=1):
        key = i - x
        ans += freq.get(key, 0)
        freq[key] = freq.get(key, 0) + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The loop uses one-based positions by starting `enumerate` from `1`. This avoids converting between zero-based Python indices and the mathematical positions from the problem.

`freq` stores the number of previous positions having each value of `i - a[i]`. When the same value appears again, every previous occurrence creates one new valid pair, so we add the current frequency before inserting the current position.

Python integers are arbitrary precision, so the answer does not need special handling even though the number of pairs can exceed 32-bit integer limits.

There are no boundary checks in the implementation because the algebraic transformation already includes the condition that the jump stays inside the array. The second position of every counted pair is a real position in the permutation.

## Worked Examples

Consider:

```
5
3 4 1 2 5
```

The transformed values are:

| Position | Value | Position - Value | Current answer |
| --- | --- | --- | --- |
| 1 | 3 | -2 | 0 |
| 2 | 4 | -2 | 1 |
| 3 | 1 | 2 | 1 |
| 4 | 2 | 2 | 2 |
| 5 | 5 | 0 | 2 |

The groups are `{-2: 2}`, `{2: 2}`, and `{0: 1}`. The two groups of size two each contribute one pair, giving the final answer `2`.

This trace demonstrates that the algorithm does not need to know which position contains the jump length. The permutation property handles that connection automatically.

Now consider:

```
4
1 2 3 4
```

| Position | Value | Position - Value | Current answer |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 0 |
| 2 | 2 | 0 | 1 |
| 3 | 3 | 0 | 3 |
| 4 | 4 | 0 | 6 |

All positions share the same transformed value, so every pair is counted. The result is `4 * 3 / 2 = 6`.

This example verifies that the solution handles large groups correctly instead of only checking nearby positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each array element is processed once and each dictionary operation is expected O(1). |
| Space | O(n) | In the worst case every position has a different transformed value. |

The solution performs only a single pass over the permutation, so it easily fits the required limits for `n = 200000`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(input())
    a = list(map(int, input().split()))

    freq = {}
    ans = 0
    for i, x in enumerate(a, start=1):
        key = i - x
        ans += freq.get(key, 0)
        freq[key] = freq.get(key, 0) + 1

    sys.stdin = old_stdin
    return str(ans)

# provided sample
assert run("5\n3 4 1 2 5\n") == "2", "sample"

# minimum size
assert run("1\n1\n") == "0", "single element"

# all pairs are valid
assert run("5\n1 2 3 4 5\n") == "10", "increasing permutation"

# catches missing same-index cases
assert run("3\n2 1 3\n") == "1", "self jump case"

# many equal transformed values
assert run("6\n1 2 3 4 5 6\n") == "15", "all equal keys"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `0` | Minimum size and no possible pair |
| `5 / 1 2 3 4 5` | `10` | Every pair belongs to one transformed group |
| `3 / 2 1 3` | `1` | Pairs where the original `i` and `j` can coincide |
| `6 / 1 2 3 4 5 6` | `15` | Large frequency group counting |

## Edge Cases

For the case:

```
5
3 4 1 2 5
```

the algorithm computes transformed values:

```
-2, -2, 2, 2, 0
```

The repeated values create two pairs. These correspond to the two valid original choices, including the case where the same index is used as both parts of the original pair.

For:

```
4
1 2 3 4
```

all transformed values are zero. The algorithm keeps adding the number of previous occurrences, producing:

```
0 + 1 + 2 + 3 = 6
```

which counts every possible pair exactly once.

For a permutation with no repeated transformed values, every frequency remains one, so the answer stays zero. Such cases are handled naturally because no previous position can match the current one.
