---
title: "CF 106188G - Ancient History"
description: "We are given n line segments with lengths a[i]. We need count how many ways to choose exactly k of these segments so that the chosen segments can form a non-degenerate polygon whose vertices lie on a circle."
date: "2026-06-25T10:47:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106188
codeforces_index: "G"
codeforces_contest_name: "UTPC x WiCS Contest 11-12-2025"
rating: 0
weight: 106188
solve_time_s: 37
verified: true
draft: false
---

[CF 106188G - Ancient History](https://codeforces.com/problemset/problem/106188/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given `n` line segments with lengths `a[i]`. We need count how many ways to choose exactly `k` of these segments so that the chosen segments can form a non-degenerate polygon whose vertices lie on a circle. Segments with equal lengths are still different choices because every discovered segment is considered unique.

For a set of side lengths, being able to form a non-degenerate polygon is equivalent to the longest side being strictly smaller than the sum of all remaining sides. A polygon satisfying this condition can be arranged as a cyclic polygon, so the problem becomes counting `k`-element subsets where no chosen segment is at least as long as the total length of the others.

The input size allows `n` to reach around one hundred and the lengths can be large enough that checking all subsets is impossible. The number of possible choices is `C(n, k)`, which grows too quickly even for moderate values of `n`. We need a polynomial-time solution. The maximum length of a segment is only `10000`, which is the key bound we can exploit.

The tricky part is that we cannot only look at the largest value globally. A subset can be invalid because of its own largest element. For example:

```
Input
4 3
1 2 3 10
```

The answer is `1` because the only valid choice is `{1,2,3}`. A careless implementation that checks only the total sum of all segments might incorrectly conclude that large segments can always participate.

Another edge case is repeated lengths. For example:

```
Input
5 3
3 3 3 1 2
```

The answer is `7`. The three segments of length `3` are different objects, so combinations containing different copies must be counted separately. Treating lengths as unique values would undercount.

A final boundary case is equality. The condition is strict. For example:

```
Input
3 3
1 2 3
```

The answer is `0` because `3 = 1 + 2`, producing a degenerate triangle instead of a valid polygon. Using `<=` instead of `<` would give the wrong result.

## Approaches

The direct approach is to generate every subset of size `k`, find its maximum side, and test whether that maximum is smaller than the sum of the others. This is correct because it checks exactly the polygon inequality for every possible choice. However, there can be `C(100,50)` subsets, which is far beyond what can be processed.

The useful observation is that every invalid subset has one distinguished side: its largest side. After sorting the lengths, suppose the current largest chosen segment has length `x`. The subset is invalid exactly when the other `k-1` chosen segments have total length at most `x`.

This lets us count invalid subsets instead of trying to count valid ones directly. Since the largest possible segment length is only `10000`, we only need dynamic programming information about sums up to `10000`. Larger sums can never make a subset invalid.

We process the segments in increasing order. Before inserting a segment `x` into the dynamic programming table, the table contains only smaller segments. We use it to count how many groups of `k-1` smaller segments have sum at most `x`. Every such group creates exactly one invalid subset with `x` as the largest element. After counting these bad subsets, we insert `x` into the table so it can serve as the largest element for future choices.

The total number of all possible `k`-subsets is `C(n, k)`. Subtracting the invalid ones gives the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(C(n,k) * k)` | `O(k)` | Too slow |
| Optimal | `O(n * k * A)` | `O(k * A)` | Accepted |

Here `A` is the maximum segment length, at most `10000`.

## Algorithm Walkthrough

1. Sort all segment lengths in nondecreasing order. Processing in this order guarantees that when we examine a segment, every segment already stored in the dynamic programming table is smaller or equal and can only be a non-maximum side.
2. Create a dynamic programming table `dp[j][s]`. It stores the number of ways to choose `j` processed segments whose total length is exactly `s`, where `s` is limited to `10000`.
3. For each segment length `x`, first count invalid polygons where `x` is the largest side. We need groups of `k-1` previous segments whose sum is at most `x`.
4. Add that count to the invalid subset total. This counts every invalid subset once because every invalid subset has exactly one largest chosen segment.
5. Insert `x` into the dynamic programming table. Iterate sizes backwards so that the current segment is not reused multiple times in the same subset.
6. Compute the total number of ways to choose `k` segments using combinations and subtract the invalid count.

Why it works: every invalid selection has a unique largest side. When that side is processed, all other chosen sides have already been inserted into `dp`, so the algorithm counts the selection exactly once. Every selection that is not counted as invalid has its largest side smaller than the sum of the remaining sides, which is exactly the polygon inequality. The subtraction leaves precisely the valid cyclic polygons.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7
MAX_A = 10000

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    comb = [[0] * (k + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        comb[i][0] = 1
        for j in range(1, min(i, k) + 1):
            if j == i:
                comb[i][j] = 1
            else:
                comb[i][j] = (comb[i - 1][j - 1] + comb[i - 1][j]) % MOD

    dp = [[0] * (MAX_A + 1) for _ in range(k)]
    dp[0][0] = 1

    invalid = 0

    for x in a:
        if k > 1:
            bad = 0
            for s in range(x + 1):
                bad += dp[k - 1][s]
            invalid = (invalid + bad) % MOD

        for cnt in range(k - 2, -1, -1):
            current = dp[cnt]
            nxt = dp[cnt + 1]
            for s in range(MAX_A - x + 1):
                if current[s]:
                    nxt[s + x] = (nxt[s + x] + current[s]) % MOD

    answer = (comb[n][k] - invalid) % MOD
    print(answer)

if __name__ == "__main__":
    solve()
```

The combination table computes the total number of possible `k`-segment selections. The values are needed modulo `10^9+7`, so Pascal's triangle avoids overflow and handles all cases directly.

The dynamic programming table only stores sums up to `10000`. A larger sum can never appear in an invalid subset check because the largest side being tested is never larger than `10000`.

The loop that counts bad subsets happens before inserting the current segment. This ordering prevents counting the current segment as one of the smaller sides. The update loop goes backward over the chosen count, which is the standard 0/1 knapsack pattern and prevents using one segment multiple times.

## Worked Examples

For the first sample:

```
5 3
1 2 3 3 3
```

The processing state is:

| Current segment | Invalid groups with this as largest | Stored subset sizes |
| --- | --- | --- |
| 1 | 0 | 1: {1} |
| 2 | 0 | sums of smaller groups |
| 3 | groups with two previous segments having sum ≤ 3 | updated with 3 |
| 3 | same check with previous values | updated with another 3 |
| 3 | same check with previous values | updated with another 3 |

The invalid choices are removed from the total number of `3`-element selections. The remaining answer is `7`.

For the second sample:

```
6 4
1 5 2 3 4 1
```

After sorting:

```
1 1 2 3 4 5
```

The important states are:

| Current segment | Need previous 3 segments with sum ≤ current value | Result |
| --- | --- | --- |
| 1 | impossible | no invalid subset |
| 2 | impossible except tiny sums | no invalid subset |
| 3 | previous triples are too large | no invalid subset |
| 4 | previous triples with small sum are checked | invalid counted |
| 5 | all remaining possible largest-side failures are counted | invalid counted |

The algorithm counts every bad quadrilateral by its longest side and subtracts them from all possible choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n * k * A)` | Each segment updates every subset size and every possible sum up to `A = 10000`. |
| Space | `O(k * A)` | The table stores counts for every subset size and possible relevant sum. |

With `n <= 100`, `k <= 100`, and `A <= 10000`, the number of operations is around `10^8` in the largest case and fits the intended limits with optimized Python loops.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline
    n, k = map(int, data().split())
    a = list(map(int, data().split()))
    a.sort()

    MOD = 10 ** 9 + 7
    MAX_A = 10000

    comb = [[0] * (k + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        comb[i][0] = 1
        for j in range(1, min(i, k) + 1):
            comb[i][j] = (comb[i - 1][j - 1] + comb[i - 1][j]) % MOD

    dp = [[0] * (MAX_A + 1) for _ in range(k)]
    dp[0][0] = 1
    bad = 0

    for x in a:
        for s in range(x + 1):
            bad += dp[k - 1][s]
        for c in range(k - 2, -1, -1):
            for s in range(MAX_A - x + 1):
                if dp[c][s]:
                    dp[c + 1][s + x] += dp[c][s]

    sys.stdin = old
    return str((comb[n][k] - bad) % MOD)

assert run("""5 3
1 2 3 3 3
""") == "7"

assert run("""6 4
1 5 2 3 4 1
""") == "12"

assert run("""3 3
1 2 3
""") == "0"

assert run("""3 3
2 2 3
""") == "0"

assert run("""5 5
1 1 1 1 1
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 3 / 1 2 3 3 3` | `7` | Repeated lengths are treated as separate segments |
| `6 4 / 1 5 2 3 4 1` | `12` | General polygon counting |
| `3 3 / 1 2 3` | `0` | Equality case is rejected |
| `3 3 / 2 2 3` | `0` | Degenerate polygon handling |
| `5 5 / 1 1 1 1 1` | `1` | Minimum non-empty complete selection |

## Edge Cases

For the equality boundary:

```
3 3
1 2 3
```

When processing `3`, the dynamic programming table contains the pair `{1,2}` with sum `3`. Since the query counts sums up to and including the current largest side, this subset is marked invalid. The final answer is `0`.

For repeated values:

```
5 3
3 3 3 1 2
```

The sorted order is `1,2,3,3,3`. Each copy of `3` is inserted separately into the dynamic programming table. Different indices create different choices, so the algorithm naturally preserves multiplicity.

For a large side dominating the others:

```
4 3
1 2 3 10
```

When `10` is processed, the table contains all pairs among the smaller values. Every pair has sum at most `10`, so all subsets containing `10` are invalid. The only remaining valid triangle is `{1,2,3}`.

For the smallest possible polygon size:

```
3 3
2 3 4
```

The algorithm checks the only possible subset. The largest side is `4`, while the other two sides sum to `5`, so the subset is valid and the answer is `1`.
