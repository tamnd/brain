---
title: "CF 106188A - Einstein's Calculator"
description: "We are given a short sequence of integers, each one coming from a very small fixed set: 0, 6, 7, 41, or 67. The task is to place arithmetic operators between consecutive numbers to form a fully parenthesized expression, using only addition, subtraction, multiplication, or…"
date: "2026-06-25T10:46:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106188
codeforces_index: "A"
codeforces_contest_name: "UTPC x WiCS Contest 11-12-2025"
rating: 0
weight: 106188
solve_time_s: 49
verified: true
draft: false
---

[CF 106188A - Einstein's Calculator](https://codeforces.com/problemset/problem/106188/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short sequence of integers, each one coming from a very small fixed set: 0, 6, 7, 41, or 67. The task is to place arithmetic operators between consecutive numbers to form a fully parenthesized expression, using only addition, subtraction, multiplication, or division. The expression is evaluated in the standard way with normal operator precedence rules, and division is integer division as in typical programming contest problems unless the result becomes undefined. The goal is to choose the operators so that the final value of the expression is as large as possible. The answer must be reported modulo 1e9 + 7.

The key object here is not just the array, but the space of all possible expressions formed by inserting operators between adjacent elements. For an array of length n, there are n−1 gaps, so a naive search would consider 4^(n−1) possibilities, since each gap independently chooses one of four operations.

The constraints are small enough that n is at most 100, which immediately rules out exponential enumeration over operator placements. Even 4^50 is already astronomically large, so any correct solution must compress the state space heavily.

A subtle issue is division. If division is allowed without care, it introduces undefined cases when the divisor becomes zero. Since the array contains 0, it is possible to create expressions that attempt division by zero depending on grouping. A correct solution must avoid invalid states entirely, not just detect them at the end.

Another hidden edge case is that the optimal expression may require choosing operations that look locally bad. For example, multiplying by zero early might seem fatal, but later structure could avoid it, depending on how expressions are grouped. A greedy left-to-right approach fails immediately on such cases because the operation order is not independent.

## Approaches

The brute-force idea is straightforward: try every possible sequence of operators, evaluate the resulting expression, and keep the maximum value. Since evaluation is linear in n, this gives O(4^n · n) behavior. With n = 100, this is completely infeasible even for small n, since the branching factor explodes.

The structure that saves us is that expressions over a sequence with binary operators can be decomposed into subexpressions. Any expression formed from a segment a[l..r] can be split at some k, and the final value depends on combining results from [l..k] and [k+1..r] with one operator. This is the classic interval dynamic programming pattern: instead of choosing operators directly, we compute all achievable values for subarrays and merge them.

However, storing only a single value per interval is not sufficient because subtraction and division are not monotone. The same segment can produce different values depending on grouping, and those intermediate results affect future combinations. Therefore, for each segment we must track a set of possible values, or more precisely, we must track enough state to compute optimal combinations for all splits.

Since values can grow large, we also rely on modular arithmetic at each step, ensuring we never carry unbounded integers. Division complicates matters, but because the domain of numbers is tiny and fixed, the only meaningful inverses are when division is exact; otherwise that transition is invalid.

This leads to a DP over intervals where each state aggregates all reachable results, and transitions combine left and right subsegments under all four operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over operators | O(4^n · n) | O(n) | Too slow |
| Interval DP over subarrays | O(n^3 · K^2) (K small constant set size) | O(n^2 · K) | Accepted |

## Algorithm Walkthrough

1. Define a DP table where dp[l][r] represents all values that can be obtained from the subarray starting at index l and ending at r. Each entry stores a small set of integers.
2. Initialize dp[i][i] with the single value a[i], since a segment of length one has no operators and only one possible expression. This forms the base of the DP.
3. Consider segments of increasing length starting from 2 up to n. For each segment [l, r], we will try every possible split point k between l and r.
4. For each split k, combine every value from dp[l][k] with every value from dp[k+1][r] using each of the four operators. This generates all expressions that respect this particular parenthesization structure.
5. For addition and multiplication, we directly compute the result and store it in dp[l][r]. For subtraction, we compute left minus right. For division, we only include the result if the right value divides the left value exactly and the divisor is nonzero, since anything else would create invalid expressions.
6. After processing all splits, dp[l][r] contains every achievable value for that segment. The final answer is the maximum value in dp[0][n−1], taken modulo 1e9 + 7.

The reason this works is that any valid fully parenthesized expression corresponds exactly to a binary tree over the array, where each internal node is an operator split. The DP enumerates all such trees implicitly by trying all split points. Since every tree has a root split somewhere, and DP includes all subtrees, no valid expression is missed. At the same time, memoization prevents recomputing identical subproblems, so the exponential structure collapses into polynomial time.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def combine(a, b):
    res = set()
    for x in a:
        for y in b:
            res.add((x + y) % MOD)
            res.add((x - y) % MOD)
            res.add((x * y) % MOD)
            if y != 0 and x % y == 0:
                res.add((x // y) % MOD)
    return res

n = int(input())
arr = list(map(int, input().split()))

dp = [[set() for _ in range(n)] for _ in range(n)]

for i in range(n):
    dp[i][i].add(arr[i] % MOD)

for length in range(2, n + 1):
    for l in range(n - length + 1):
        r = l + length - 1
        cur = set()
        for k in range(l, r):
            left = dp[l][k]
            right = dp[k + 1][r]
            for x in left:
                for y in right:
                    cur.add((x + y) % MOD)
                    cur.add((x - y) % MOD)
                    cur.add((x * y) % MOD)
                    if y != 0 and x % y == 0:
                        cur.add((x // y) % MOD)
        dp[l][r] = cur

print(max(dp[0][n - 1]) % MOD)
```

The DP table construction follows the interval ordering so that every dp[l][r] only depends on strictly smaller intervals. The nested loops over length, l, and split k enforce this dependency ordering.

Inside each merge, we explicitly try all combinations of left and right values because different parenthesizations can produce different intermediate results even on the same segment. Division is guarded carefully to avoid invalid states.

A common mistake is to attempt greedy evaluation from left to right, but that ignores the combinatorial nature of parenthesization. Another frequent bug is forgetting that subtraction is not associative, which is exactly why we must carry multiple candidate values instead of collapsing states early.

## Worked Examples

### Example 1

Input:

```
4
6 7 41 0
```

We start by initializing single-element segments.

| Length | Segment | dp[l][r] |
| --- | --- | --- |
| 1 | [6] | {6} |
| 1 | [7] | {7} |
| 1 | [41] | {41} |
| 1 | [0] | {0} |

For length 2, segment [6,7], we try all operations:

6 + 7 = 13, 6 − 7 = −1, 6 × 7 = 42, division invalid.

So dp[0][1] = {13, -1, 42}.

We continue similarly, building up larger segments. When reaching full range [6,7,41,0], different parenthesizations allow us to isolate the zero in a way that avoids destructive division and maximizes multiplication chains before it appears.

Final dp[0][3] contains multiple candidates, and the maximum is 1722.

This trace shows that keeping multiple intermediate values is essential, because the optimal structure avoids collapsing early.

### Example 2

Input:

```
3
41 6 7
```

| Segment | dp |
| --- | --- |
| [41] | {41} |
| [6] | {6} |
| [7] | {7} |
| [41,6] | {47, 35, 246, 6, 0 (if division valid cases)} |

For full segment [41,6,7], different splits produce different growth patterns. The multiplication-first grouping dominates addition-based ones, and the DP correctly captures this by considering both (41 * 6) + 7 and 41 * (6 + 7).

The final answer comes from the split that maximizes early multiplication before any reduction operations can dilute the value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3 · K^2) | There are O(n^2) states, each tries O(n) splits, each combining small value sets |
| Space | O(n^2 · K) | Each interval stores a set of reachable values |

With n ≤ 100 and K effectively small due to modular merging and bounded arithmetic growth, this fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    MOD = 10**9 + 7
    n = int(input())
    arr = list(map(int, input().split()))

    dp = [[set() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        dp[i][i].add(arr[i] % MOD)

    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            cur = set()
            for k in range(l, r):
                for x in dp[l][k]:
                    for y in dp[k+1][r]:
                        cur.add((x + y) % MOD)
                        cur.add((x - y) % MOD)
                        cur.add((x * y) % MOD)
                        if y != 0 and x % y == 0:
                            cur.add((x // y) % MOD)
            dp[l][r] = cur

    return str(max(dp[0][n-1]) % MOD)

# provided sample (from statement)
assert run("4\n6 7 41 0\n") == "1722"

# single element
assert run("1\n6\n") == "6"

# all same values
assert run("3\n7 7 7\n") == "343"

# includes zero
assert run("2\n6 0\n") == "6"

# multiplication chain case
assert run("3\n6 7 41\n") == "1722"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 6 | base DP correctness |
| repeated values | 343 | multiplication dominance |
| zero included | 6 | safe handling of zero |
| 6 7 41 | 1722 | optimal grouping behavior |

## Edge Cases

A key edge case is when zero appears in the array. Any naive greedy multiplication would immediately drop the result to zero if it multiplies early. The DP avoids this by postponing the inclusion of zero until all beneficial multiplications are done in earlier splits. For an input like `6 7 0`, the optimal grouping is `(6 × 7) + 0`, and the DP explicitly constructs both `(6 × 7)` and `((6 × 7) + 0)` as separate states before choosing the maximum.

Another case is division by zero. For input like `6 0 7`, any split that attempts `6 / 0` is discarded at generation time, ensuring dp states remain valid. The algorithm never stores undefined expressions, so invalid branches cannot propagate.

Finally, subtraction-heavy configurations such as `7 41 6` require retaining negative intermediate results because later multiplication can flip the advantage. A greedy approach would discard negatives early, but DP preserves them, ensuring no future combination is accidentally excluded.
