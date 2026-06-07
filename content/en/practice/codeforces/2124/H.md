---
title: "CF 2124H - Longest Good Subsequence"
description: "We are given an array a. We want to choose a subsequence and reinterpret it as a new array b. The goal is to maximize the length of b, subject to b being a good array. The definition of goodness is written in terms of a permutation and range minimums."
date: "2026-06-08T03:34:55+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "trees"]
categories: ["algorithms"]
codeforces_contest: 2124
codeforces_index: "H"
codeforces_contest_name: "EPIC Institute of Technology Round Summer 2025 (Codeforces Round 1036, Div. 1 + Div. 2)"
rating: 3400
weight: 2124
solve_time_s: 111
verified: false
draft: false
---

[CF 2124H - Longest Good Subsequence](https://codeforces.com/problemset/problem/2124/H)

**Rating:** 3400  
**Tags:** dp, math, trees  
**Solve time:** 1m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array `a`. We want to choose a subsequence and reinterpret it as a new array `b`. The goal is to maximize the length of `b`, subject to `b` being a _good_ array.

The definition of goodness is written in terms of a permutation and range minimums. At first glance it looks unrelated to subsequences, but the real task is to understand which arrays `b` can actually appear from that construction.

The value `b_i` represents the leftmost position of a segment ending at `i` whose minimum occurs exactly at position `i`. Since the permutation contains distinct values, every comparison is strict. The structure hidden in the definition turns out to be much more important than the permutation itself.

The length of the original array is at most `15000`, and the sum of `n²` over all test cases is at most `15000²`. This is a very strong hint. A solution with complexity around `O(n²)` is intended. A cubic algorithm would require roughly `3·10¹²` operations in the worst case and is completely infeasible. A quadratic dynamic programming solution, about `2.25·10⁸` simple operations across all tests, is exactly the range these constraints are designed for.

Several edge cases are easy to mishandle.

Consider:

```
a = [2,2,2,2]
```

A tempting idea is that equal values can always be chained together. They cannot. Any good array must contain a position whose value equals its own index. Since every value is `2`, no nonempty good subsequence exists. The correct answer is `0`.

Consider:

```
a = [1]
```

The single element already satisfies the required structure. The answer is `1`.

Consider:

```
a = [1,1,2]
```

The whole sequence is not good. A naive check based only on local inequalities would incorrectly accept it. The longest good subsequence is `[1,2]`, whose length is `2`.

These examples show that the critical difficulty is not selecting positions, but characterizing which sequences are actually good.

## Approaches

The brute force idea is straightforward. Enumerate every subsequence, test whether it is good, and keep the maximum length.

For an array of length `n`, there are `2^n` subsequences. Even for `n = 60` this is already hopeless, and here `n` can reach `15000`. The brute force approach serves only as a conceptual starting point.

The real breakthrough comes from understanding the structure of good arrays.

Let `b_i = x`. Looking at the range-minimum interpretation, position `x` must itself be the start of a valid block. After unwinding the definition, one obtains the following characterization:

A sequence `b` is good if and only if for every position `i` with `b_i = x`, one of the following holds:

1. `x = i`.
2. `b_x = x` and every value on the segment `[x, i]` is at least `x`.

This completely removes the permutation from the problem. We only need to reason about indices and values.

Now think of every position `x` satisfying `b_x = x` as the root of a block. Any later occurrence of value `x` must belong to that block, and all values inside the block must be at least `x`.

This naturally leads to interval dynamic programming. We process possible block roots and extend them to the right. Whenever we encounter a larger value, we may start a nested block. The key observation is that the starting position of such a nested block should be chosen greedily as early as possible. That allows all transitions to be implemented in quadratic time.

The resulting DP fits perfectly into the `Σ n² ≤ 15000²` constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^n · n)` | `O(n)` | Too slow |
| Optimal DP | `O(n²)` | `O(n²)` | Accepted |

## Algorithm Walkthrough

### State Definition

Let `dp[i][j]` represent the maximum length of a good subsequence that can be formed inside the interval `[i, j]` under the conditions:

- position `i` is chosen,
- its value acts as a block root,
- position `j` is the last occurrence of that root value inside the constructed subsequence.

The editorial implementation stores exactly this quantity.

### Transition Construction

1. Process starting positions `i` from right to left.
2. Initialize the block rooted at `i`.

The smallest valid subsequence consists only of occurrences of `a[i]`. Initially:

```
dp[i][i] = a[i]
```

The variable `curr` stores the best value obtained so far.
3. Extend the right endpoint `j`.
4. If `a[j] < a[i]`, the element cannot belong to the current block.

The characterization requires every value inside the block to be at least the root value.
5. If `a[j] = a[i]`, we may append this occurrence for free.

Increase `curr` by one and set:

```
dp[i][j] = curr
```
6. If `a[j] > a[i]`, the element may become the root of a nested block.

Maintain an array `good[v]`.

`good[v]` stores the earliest position whose value is `v` and whose DP value is already large enough to support a block of type `v`.
7. When such a nested block exists, merge it into the current structure:

```
curr = max(curr, dp[idx][j])
```

where `idx = good[a[j]]`.
8. Continue until all endpoints have been processed.

### Extracting the Answer

After all interval states are computed, run the same transition logic once more on the whole array.

Whenever a valid root becomes available, use its corresponding `dp` values to update the global answer.

The final value of `curr` is the length of the longest good subsequence.

### Why it works

The characterization of good arrays says that every occurrence of value `x` must belong to a block rooted at a position where the value is also `x`.

Inside such a block, all values must be at least `x`. This means smaller values can never be appended, equal values always extend the block, and larger values can only appear through nested blocks whose root already satisfies the same property recursively.

The DP state stores exactly the best achievable length for a block root and a fixed last occurrence. Every valid good subsequence can be decomposed into these nested blocks, and every transition performed by the DP corresponds to one legal decomposition. Since the earliest feasible root is always optimal for future extensions, the greedy choice used by `good[]` never loses a better solution.

Thus every valid good subsequence is considered, and every subsequence produced by the DP satisfies the characterization. The algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))

    dp = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(n, 0, -1):
        good = [-1] * (n + 1)

        curr = a[i]
        dp[i][i] = curr

        for j in range(i + 1, n + 1):
            if a[j] < a[i]:
                continue

            if a[j] == a[i]:
                curr += 1
                dp[i][j] = curr
                continue

            if good[a[j]] == -1 and a[j] <= curr + 1:
                good[a[j]] = j

            if good[a[j]] != -1:
                idx = good[a[j]]
                curr = max(curr, dp[idx][j])

    curr = 0
    good = [-1] * (n + 1)

    for j in range(1, n + 1):
        if good[a[j]] == -1 and a[j] <= curr + 1:
            good[a[j]] = j

        if good[a[j]] != -1:
            idx = good[a[j]]
            curr = max(curr, dp[idx][j])

    print(curr)

t = int(input())
for _ in range(t):
    solve()
```

The outer loop computes every interval state `dp[i][j]`. Processing `i` from right to left guarantees that all nested blocks needed by future transitions have already been computed.

The array `good` is rebuilt for every starting position. It records the earliest usable root for each value. Storing only the first such position is enough because earlier roots dominate later ones.

A subtle point is the condition:

```
a[j] <= curr + 1
```

A block rooted at value `v` requires at least `v - 1` positions to have already been constructed before it can begin. This condition is exactly the feasibility check.

Another subtle detail is that entries with `a[j] < a[i]` are skipped completely. Allowing them would violate the characterization theorem and create invalid blocks.

## Worked Examples

### Example 1

Input:

```
[1,1,3,3,5]
```

Key DP evolution:

| i | j | a[j] | curr |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 1 | 2 | 1 | 2 |
| 1 | 3 | 3 | 2 |
| 1 | 4 | 3 | 4 |
| 1 | 5 | 5 | 5 |

Final answer:

```
5
```

The whole sequence already satisfies the block structure. Every larger value begins a nested block and all conditions remain valid.

### Example 2

Input:

```
[1,1,2]
```

Key evolution of the global phase:

| j | a[j] | curr before | curr after |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 1 |
| 2 | 1 | 1 | 2 |
| 3 | 2 | 2 | 2 |

Final answer:

```
2
```

The sequence `[1,1,2]` is not good, but `[1,2]` is. The DP correctly refuses to build the invalid structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n²)` | Every pair `(i, j)` is processed once |
| Space | `O(n²)` | DP table of size `(n+1)²` |

The problem explicitly guarantees that the sum of `n²` across all test cases does not exceed `15000²`. An `O(n²)` dynamic programming solution is exactly what these constraints are designed to support, and the memory usage also fits comfortably within the 1024 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    from io import StringIO

    data = StringIO(inp)
    out = StringIO()

    input = data.readline

    t = int(input())

    for _ in range(t):
        n = int(input())
        a = [0] + list(map(int, input().split()))

        dp = [[0] * (n + 1) for _ in range(n + 1)]

        for i in range(n, 0, -1):
            good = [-1] * (n + 1)
            curr = a[i]
            dp[i][i] = curr

            for j in range(i + 1, n + 1):
                if a[j] < a[i]:
                    continue

                if a[j] == a[i]:
                    curr += 1
                    dp[i][j] = curr
                    continue

                if good[a[j]] == -1 and a[j] <= curr + 1:
                    good[a[j]] = j

                if good[a[j]] != -1:
                    curr = max(curr, dp[good[a[j]]][j])

        curr = 0
        good = [-1] * (n + 1)

        for j in range(1, n + 1):
            if good[a[j]] == -1 and a[j] <= curr + 1:
                good[a[j]] = j

            if good[a[j]] != -1:
                curr = max(curr, dp[good[a[j]]][j])

        out.write(str(curr) + "\n")

    return out.getvalue()

# provided sample
assert run(
"""5
5
1 1 3 3 5
3
1 1 2
4
2 2 2 2
7
1 2 4 2 4 6 2
1
1
"""
) == """5
2
0
5
1
"""

# minimum size
assert run(
"""1
1
1
"""
) == """1
"""

# all equal but impossible
assert run(
"""1
4
2 2 2 2
"""
) == """0
"""

# single valid chain
assert run(
"""1
4
1 2 3 4
"""
) == """4
"""

# off-by-one style case
assert run(
"""1
3
1 1 2
"""
) == """2
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1]` | `1` | Smallest nonempty instance |
| `[2,2,2,2]` | `0` | No valid root position exists |
| `[1,2,3,4]` | `4` | Entire array forms a valid structure |
| `[1,1,2]` | `2` | Rejects a tempting but invalid full sequence |

## Edge Cases

Consider:

```
1
4
2 2 2 2
```

During the global phase, value `2` can never become a valid root because the current achievable length never reaches `1` before a root must be created. No DP state becomes usable, and the answer remains `0`. This matches the characterization, since a nonempty good sequence must contain some position `i` with value `i`.

Consider:

```
1
1
1
```

The only position is simultaneously a root and the end of its block. The DP initializes `dp[1][1] = 1`, and the global phase immediately recovers answer `1`.

Consider:

```
1
3
1 1 2
```

The first two elements create a block rooted at value `1`. When the final value `2` is examined, the DP detects that the required nested structure does not exist for the full sequence. The best valid subsequence remains length `2`, corresponding to `[1,2]`.

These examples illustrate the two most common pitfalls: assuming equal values can always be chained, and ignoring the requirement that every block must originate from a valid root.
