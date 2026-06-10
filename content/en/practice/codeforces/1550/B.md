---
title: "CF 1550B - Maximum Cost Deletion"
description: "We are given a binary string and repeatedly remove substrings that consist of only one character type. Every deletion of a substring of length l gives a l + b points. The string shrinks after each operation because the remaining parts are concatenated together."
date: "2026-06-10T13:27:42+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1550
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 111 (Rated for Div. 2)"
rating: 1000
weight: 1550
solve_time_s: 219
verified: true
draft: false
---

[CF 1550B - Maximum Cost Deletion](https://codeforces.com/problemset/problem/1550/B)

**Rating:** 1000  
**Tags:** greedy, math  
**Solve time:** 3m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string and repeatedly remove substrings that consist of only one character type. Every deletion of a substring of length `l` gives `a * l + b` points. The string shrinks after each operation because the remaining parts are concatenated together.

The goal is not to find a sequence of deletions, but to compute the maximum possible total score after the entire string has been erased.

The first thing to notice is that every character is deleted exactly once. No matter how we choose the operations, the sum of all deleted lengths is always `n`. Because of that, the contribution from `a` is fixed:

`a * n`

The only part affected by our choices is how many deletion operations we perform. If we perform `k` deletions, the total score becomes:

`a * n + b * k`

This observation completely changes the problem. We no longer care about the exact lengths of deleted substrings. We only care about maximizing or minimizing the number of operations, depending on the sign of `b`.

The constraints are very small. The string length is at most 100, and there are at most 2000 test cases. Even fairly inefficient solutions would fit comfortably. Still, the intended solution is a simple greedy observation running in linear time per test case.

A few edge cases are easy to mishandle if we focus only on deletions instead of the score formula.

Consider:

```
n = 5
a = 3
b = 4
s = 11111
```

A careless solution might delete the whole string in one operation and score `15 + 4 = 19`. The correct answer is `5 * (3 + 4) = 35`, because when `b > 0`, every extra operation gives additional points, so deleting one character at a time is optimal.

Consider:

```
n = 6
a = 1
b = -5
s = 000000
```

Deleting one character at a time gives six operations and incurs the negative bonus six times. The optimal strategy is deleting the whole string at once, giving:

```
1 * 6 + (-5) = 1
```

Another subtle case is an alternating string:

```
n = 5
a = 0
b = -1
s = 01010
```

At first glance it seems we are forced to perform five deletions because there are five runs. In reality, after deleting all occurrences of one character type, the remaining characters merge into one block. The optimal answer comes from the run-count formula discussed later and equals `-3`, not `-5`.

## Approaches

A brute-force approach would try all possible valid deletions and recursively explore the resulting strings. This is correct because every legal sequence of operations is examined. Unfortunately, the number of possible deletion sequences grows exponentially. Even for strings of length 100, the search space is astronomically large and completely infeasible.

The key observation is that the total contribution from lengths is fixed. Every character contributes exactly `a` once, regardless of the deletion order. The entire optimization problem reduces to choosing the number of operations.

The score can be rewritten as:

```
a * n + b * k
```

where `k` is the number of deletions.

If `b >= 0`, every additional deletion increases the score. The best strategy is to maximize `k`. Since every single character is itself a valid monochromatic substring, we can delete characters one by one and achieve:

```
k = n
```

The interesting case is `b < 0`. Now every operation costs points, so we want as few deletions as possible.

Let the string consist of `runs` maximal blocks of equal characters.

For a binary string, we can always delete all runs of one character type first. After that, all remaining runs merge together into a single run and can be removed in one final operation.

If there are `runs` blocks, then one character appears in at most `runs / 2` blocks. We choose the character with fewer blocks.

The minimum possible number of operations becomes:

```
floor(runs / 2) + 1
```

A well-known equivalent formula is:

```
max(count_0_runs, count_1_runs)
```

Since:

```
max(count_0_runs, count_1_runs)
= floor(runs / 2) + 1
```

for any binary string.

Once we know the optimal number of operations, computing the answer is immediate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `a`, `b`, and the binary string.
2. If `b >= 0`, return:

```
n * (a + b)
```

This corresponds to deleting each character separately, giving exactly `n` operations.
3. If `b < 0`, count the number of runs in the string.

A run starts at position `0` and whenever `s[i] != s[i-1]`.
4. Compute:

```
operations = runs // 2 + 1
```

This is the minimum achievable number of deletions for a binary string.
5. Return:

```
a * n + b * operations
```

After counting runs, the answer follows directly from the score formula.

### Why it works

The total deleted length over the entire process is always `n`, so every strategy earns exactly `a * n` points from the length term. The only variable part is `b` multiplied by the number of operations.

When `b >= 0`, increasing the number of operations always improves the score. Deleting one character at a time achieves the maximum possible value `k = n`.

When `b < 0`, fewer operations are better. In a binary string, deleting all runs of the less frequent character first causes the remaining runs to merge into one block. If there are `runs` total blocks, the less frequent character occupies `floor(runs / 2)` runs. Those runs are removed individually, and the merged remainder is removed once more, giving `floor(runs / 2) + 1` operations. No strategy can do better, so this is the minimum possible number of deletions.

Since the algorithm always uses the optimal value of `k`, it always produces the maximum score.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, a, b = map(int, input().split())
    s = input().strip()

    if b >= 0:
        print(n * (a + b))
    else:
        runs = 1
        for i in range(1, n):
            if s[i] != s[i - 1]:
                runs += 1

        operations = runs // 2 + 1
        print(a * n + b * operations)
```

The first branch handles the easy case where every extra deletion is beneficial. Since deleting individual characters is always allowed, the optimal number of operations is exactly `n`.

The second branch counts runs. A run boundary occurs whenever adjacent characters differ. Starting from one run and counting transitions avoids off-by-one mistakes.

After obtaining the number of runs, we apply the formula `runs // 2 + 1` for the minimum possible deletions. The final score is then computed directly from `a * n + b * operations`.

No special handling is needed for strings of length one. The run counter correctly remains equal to one, producing one operation.

## Worked Examples

### Example 1

Input:

```
n = 5
a = -2
b = 5
s = 11001
```

Since `b > 0`, we immediately use the first case.

| Variable | Value |
| --- | --- |
| n | 5 |
| a | -2 |
| b | 5 |
| Strategy | maximize operations |
| Operations | 5 |
| Answer | 5 × (-2 + 5) = 15 |

This example demonstrates that when `b` is positive, the string structure does not matter at all. Only the length matters.

### Example 2

Input:

```
n = 6
a = 1
b = -4
s = 100111
```

Count runs.

| Position | Character | Run Count |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 0 | 2 |
| 2 | 0 | 2 |
| 3 | 1 | 3 |
| 4 | 1 | 3 |
| 5 | 1 | 3 |

Now compute the answer.

| Variable | Value |
| --- | --- |
| runs | 3 |
| operations | 3 // 2 + 1 = 2 |
| a × n | 6 |
| b × operations | -8 |
| Answer | -2 |

This trace shows the key greedy idea. Even though the string contains three runs, only two deletions are necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One scan of the string to count runs |
| Space | O(1) | Only a few variables are stored |

With `n ≤ 100` and at most `2000` test cases, the solution performs only a few hundred thousand character comparisons in total. It is comfortably within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, a, b = map(int, input().split())
        s = input().strip()

        if b >= 0:
            ans.append(str(n * (a + b)))
        else:
            runs = 1
            for i in range(1, n):
                if s[i] != s[i - 1]:
                    runs += 1
            ans.append(str(a * n + b * (runs // 2 + 1)))

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue()

# provided samples
assert run(
"""3
3 2 0
000
5 -2 5
11001
6 1 -4
100111
"""
) == "6\n15\n-2"

# minimum size
assert run(
"""1
1 3 -2
0
"""
) == "1"

# all equal, negative b
assert run(
"""1
6 1 -5
000000
"""
) == "1"

# alternating pattern
assert run(
"""1
5 0 -1
01010
"""
) == "-3"

# maximum operations beneficial
assert run(
"""1
4 -1 10
1010
"""
) == "36"

# length 100, all same
assert run(
"""1
100 1 -100
""" + "0" * 100 + "\n"
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, s=0, a=3, b=-2` | `1` | Minimum-size string |
| `000000, b<0` | `1` | Single run, one deletion |
| `01010, b=-1` | `-3` | Alternating runs and run formula |
| `1010, b>0` | `36` | Positive bonus, maximize operations |
| Length 100 all zeros | `0` | Largest length with one run |

## Edge Cases

### Single-character string

Input:

```
1
1 3 -2
0
```

The string has one run.

```
runs = 1
operations = 1 // 2 + 1 = 1
answer = 3 * 1 + (-2) * 1 = 1
```

The algorithm correctly handles the smallest possible input without requiring any special case.

### All characters equal

Input:

```
1
6 1 -5
000000
```

There is exactly one run.

```
runs = 1
operations = 1
answer = 6 - 5 = 1
```

A naive strategy that deletes characters individually would perform six operations and lose extra points. The formula correctly identifies that one deletion is optimal.

### Alternating string

Input:

```
1
5 0 -1
01010
```

Run counting gives:

```
runs = 5
operations = 5 // 2 + 1 = 3
answer = -3
```

Although there are five runs initially, deleting all runs of one character type first allows the remaining runs to merge. This is exactly the scenario where many incorrect solutions overestimate the minimum number of operations.

### Positive bonus with one run

Input:

```
1
5 2 3
11111
```

Since `b > 0`, the algorithm ignores run structure and computes:

```
answer = 5 * (2 + 3) = 25
```

Deleting one character at a time yields five operations, which is better than deleting the whole string at once. The positive-bonus branch captures this behavior automatically.
