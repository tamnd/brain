---
title: "CF 102365E - Exciting Acts"
description: "We have an array a[1..N] describing the excitement of the scenes in chronological order. We must cut this array into exactly K non-empty contiguous parts."
date: "2026-08-12T23:54:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102365
codeforces_index: "E"
codeforces_contest_name: "UBC Programming Contest 2019 (UBCPC 2019)"
rating: 0
weight: 102365
solve_time_s: 183
verified: true
draft: false
---

[CF 102365E - Exciting Acts](https://codeforces.com/problemset/problem/102365/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array `a[1..N]` describing the excitement of the scenes in chronological order. We must cut this array into exactly `K` non-empty contiguous parts. The value contributed by a part is the maximum array value inside that part, and the objective is to maximize the sum of those `K` maxima. The official constraints are `1 <= K <= N <= 2000` and `1 <= a[i] <= 1000`.

The first bound, `N <= 2000`, is large enough that trying every pair of cut positions inside every DP state is too expensive. A standard partition DP has `K * N` states, and each state can have up to `N` possible previous cut positions, giving `O(KN^2)`, which reaches about `8 * 10^9` transitions when `N = K = 2000`. That is far beyond what a one-second limit can support. We need to exploit the special way a segment's maximum changes when its right endpoint moves.

There are several boundary cases that can quietly break a careless implementation. If `K = 1`, there is only one segment, so the answer is simply the maximum of the whole array. For example, `N = 2, K = 1, a = [3, 1]` gives `3`, not `4`, because the two scenes belong to the same act.

If `K = N`, every segment must contain exactly one element. For example, `N = 3, K = 3, a = [2, 7, 4]` gives `13`. A DP that accidentally permits an empty segment can produce an invalid transition and overcount.

Equal values also need careful handling. For `N = 4, K = 2, a = [5, 5, 1, 5]`, the answer is `10`. When a new value equals the current segment maximum, the corresponding candidates can be treated as one monotonic-stack group because their maximum does not change. Using the wrong strictness in the stack condition can split equal maxima into unnecessary groups, although the final value remains correct only if the associated candidate states are handled consistently.

## Approaches

The direct dynamic programming formulation is straightforward. Let `dp[k][i]` be the maximum excitement obtainable by partitioning the first `i` elements into exactly `k` non-empty acts. If the last act begins immediately after position `j`, then its contribution is `max(a[j+1..i])`, so

`dp[k][i] = max(dp[k-1][j] + max(a[j+1..i]))`

over all valid `j`.

This recurrence is correct because every valid partition has a unique position immediately before its last act. Once that position is fixed, the first `j` elements form an optimal solution with `k-1` acts, while the final interval contributes its maximum.

A brute-force implementation can maintain the maximum while moving `j` backwards, so each DP state takes `O(N)` time instead of recomputing every interval maximum from scratch. There are `O(KN)` states, giving `O(KN^2)` total work. With `N = K = 2000`, this is about `8 * 10^9` candidate transitions, which is too slow.

The key observation is that the expensive part of the transition is not `dp[k-1][j]`. It is the changing value of `max(a[j+1..i])` as `i` moves to the right.

Fix one DP layer `k` and suppose we are processing the right endpoint `i`. For every possible start `j`, consider the candidate

`dp[k-1][j] + max(a[j+1..i])`.

As `i` increases by one, all these interval maxima either stay unchanged or become the new value `a[i]`. More specifically, if several starts currently have a segment maximum no larger than `a[i]`, all of those starts now have the same new maximum `a[i]`. They can be merged into one group.

A monotonic stack naturally represents these groups. The stack stores decreasing segment-maximum values. Along with each maximum, we store the largest `dp[k-1][j]` among all starts belonging to that group. The best candidate represented by the group is then simply

`group_maximum + largest_previous_dp`.

When a new `a[i]` arrives, groups whose maximum is at most `a[i]` are popped and merged. Since `a[i]` is at least as large as their previous maxima, their candidate values do not decrease after the merge. This gives another important simplification: we do not need a segment tree or heap to maintain the global maximum. If the old global optimum belonged to a popped group, the merged group contains that same candidate and possibly improves it. If it belonged to a group that was not popped, it remains unchanged. We can consequently maintain the answer for the current DP state with a single scalar.

The stack is monotonic, and every group is pushed once and popped at most once during one DP layer. Thus one DP layer takes `O(N)`, giving an `O(KN)` algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | `O(KN^2)` | `O(N)` with rolling DP | Too slow |
| Monotonic Stack DP | `O(KN)` | `O(N)` | Accepted |

## Algorithm Walkthrough

1. Define `prev[i]` as the best score for partitioning the first `i` elements into the previous number of acts. Initially, for zero acts, only `prev[0] = 0` is valid. Every other state is impossible.
2. Process the number of acts from `1` through `K`. For the current layer, create `cur`, where `cur[i]` will eventually represent the best score for partitioning the first `i` elements into the current number of acts.
3. For a fixed right endpoint `i`, consider every possible start `j` of the final act. Its candidate value is `prev[j] + max(a[j+1..i])`. Instead of storing every candidate separately, group starts whose current interval maximum is equal.
4. Store those groups in a stack whose maximum values are strictly decreasing from bottom to top. Each stack entry contains a maximum value `mx` and the largest `prev[j]` among all starts represented by that group. The best candidate in that group is `mx + best_prev`.
5. When processing `a[i]`, begin with the new possible final-act start `j = i-1`. Its interval consists only of `a[i]`, so its segment maximum is `a[i]` and its base value is `prev[i-1]`.
6. Pop every stack group whose maximum is at most `a[i]`. All starts in those groups now have `a[i]` as their new interval maximum. Merge their `best_prev` values with `prev[i-1]`, then create one group with maximum `a[i]`.

The condition uses `<=` rather than `<` because equal maxima have the same effect on every candidate. Combining them keeps the stack compact without losing any possible optimum.
7. The best candidate of the newly created group is `a[i] + best_prev`. Update the global best for `cur[i]` with this value. Groups that were not popped keep exactly the same candidate values, so the previous global best remains valid.
8. Only endpoints with enough elements for the requested number of acts are processed. For `k` acts, the first possible endpoint is `i = k`, because every act must contain at least one element. After completing the layer, replace `prev` by `cur`.
9. After processing all `K` layers, `prev[N]` is the maximum possible excitement for the entire array divided into exactly `K` acts.

The invariant is that immediately before computing `cur[i]`, every possible start `j` for the final act is represented by exactly one stack group. Within that group, all such starts have the same value of `max(a[j+1..i])`, so retaining only the largest `prev[j]` is sufficient. When `a[i]` is added, precisely the groups with maximum at most `a[i]` change, and all of them change to the same maximum `a[i]`, which is exactly what the pop-and-merge operation performs. Since untouched groups preserve their candidates and the merged group preserves or improves every candidate it absorbs, the maintained global maximum is exactly `cur[i]`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    neg = -10**18

    # prev[i] = best value for first i elements using the previous
    # number of acts.
    prev = [neg] * (n + 1)
    prev[0] = 0

    for acts in range(1, k + 1):
        cur = [neg] * (n + 1)

        # Each entry is [current maximum, best prev[j]]
        # for all starts j represented by this group.
        stack = []

        best = neg

        for i in range(acts, n + 1):
            x = a[i - 1]

            best_prev = prev[i - 1]

            while stack and stack[-1][0] <= x:
                _, group_best = stack.pop()
                if group_best > best_prev:
                    best_prev = group_best

            stack.append((x, best_prev))

            candidate = x + best_prev
            if candidate > best:
                best = candidate

            cur[i] = best

        prev = cur

    print(prev[n])

if __name__ == "__main__":
    solve()
```

The outer loop constructs one DP layer for each possible number of acts. `prev` contains the answers for `acts - 1` acts, while `cur` is filled for `acts` acts. Keeping only two layers is enough because the recurrence refers exclusively to the previous number of acts.

Inside a layer, `stack` stores pairs `(maximum, best_previous_value)`. The second component is the maximum `prev[j]` over all starting positions currently sharing the first component as their segment maximum. No other information about those starts can affect the transition.

The line `while stack and stack[-1][0] <= x` is the core of the optimization. Every popped group has a previous maximum no larger than `x`, so after extending the right endpoint to the current position, its maximum becomes `x`. Its best `prev[j]` can consequently be merged into the new group.

The variable `best` stores the maximum candidate among all groups seen for the current endpoint. It does not need to be recomputed after popping groups. If the old optimum was in an unpopped group, it is unchanged. If it was in a popped group, that group's candidate is replaced by a candidate in the merged group that is at least as large.

The lower bound `i = acts` prevents impossible states where fewer than `acts` elements are being divided into `acts` non-empty segments. Python integers do not overflow, and the theoretical answer is at most `K * 1000 <= 2,000,000`.

## Worked Examples

For Sample 1,

```
2 1
3 1
```

There is only one act, so the DP layer needs to find the maximum of the entire prefix.

| `i` | `a[i]` | Stack after update | `best` | `cur[i]` |
| --- | --- | --- | --- | --- |
| 1 | 3 | `(3, 0)` | 3 | 3 |
| 2 | 1 | `(3, 0), (1, -inf)` | 3 | 3 |

At `i = 2`, the new value `1` does not replace the existing maximum `3`, so the best one-act partition remains `3`. The output is `3`.

For Sample 2,

```
2 2
3 100
```

The first DP layer represents one act. At the end of that layer, the prefix answers are `3` and `100`. The second layer then considers only `i = 2`, because two acts require at least two elements.

| `i` | `a[i]` | Stack after update | `best` | `cur[i]` |
| --- | --- | --- | --- | --- |
| 2 | 100 | `(100, 3)` | 103 | 103 |

The only possible partition is `[3] | [100]`, whose score is `3 + 100 = 103`. The trace also demonstrates why `prev[i-1]` is the correct base value for the newly started final act.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(KN)` | Each DP layer processes every endpoint once, and every stack entry is pushed and popped at most once. |
| Space | `O(N)` | Two DP arrays and one monotonic stack each contain at most `N + 1` entries. |

With `N <= 2000` and `K <= 2000`, the algorithm performs on the order of four million main DP iterations, plus a linear number of stack operations per layer. This fits comfortably within the intended asymptotic requirements, whereas the quadratic transition over previous cut positions would reach billions of operations.

## Test Cases

```python
import sys
import io

def solution(data: str) -> str:
    it = iter(data.split())
    n = int(next(it))
    k = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    neg = -10**18
    prev = [neg] * (n + 1)
    prev[0] = 0

    for acts in range(1, k + 1):
        cur = [neg] * (n + 1)
        stack = []
        best = neg

        for i in range(acts, n + 1):
            x = a[i - 1]
            best_prev = prev[i - 1]

            while stack and stack[-1][0] <= x:
                _, group_best = stack.pop()
                if group_best > best_prev:
                    best_prev = group_best

            stack.append((x, best_prev))

            candidate = x + best_prev
            if candidate > best:
                best = candidate

            cur[i] = best

        prev = cur

    return str(prev[n])

def run(inp: str) -> str:
    return solution(inp).strip()

# Provided samples
assert run("2 1\n3 1\n") == "3", "sample 1"
assert run("2 2\n3 100\n") == "103", "sample 2"

# Minimum-size input
assert run("1 1\n7\n") == "7", "single element"

# K = N, every element must form its own act
assert run("5 5\n1 9 3 7 2\n") == "22", "K equals N"

# All values equal
assert run("5 3\n4 4 4 4 4\n") == "12", "all equal"

# Case where the best cut is not near an obvious local maximum
assert run("4 2\n1 10 2 9\n") == "19", "best two-act partition"

# Maximum-size case, also checks repeated equal values
n = 2000
k = 2000
inp = f"{n} {k}\n" + " ".join(["1000"] * n) + "\n"
assert run(inp) == "2000000", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 7` | `7` | Minimum `N` and `K`, with exactly one non-empty segment |
| `5 5 / 1 9 3 7 2` | `22` | Boundary case `K = N`, where every segment has length one |
| `5 3 / 4 4 4 4 4` | `12` | Equal values and the `<=` stack merge condition |
| `4 2 / 1 10 2 9` | `19` | Choosing the optimal cut rather than greedily cutting at local maxima |
| `2000 2000 / 1000 ... 1000` | `2000000` | Maximum `N`, maximum `K`, and maximum excitement value |

## Edge Cases

When `K = 1`, the algorithm runs only one DP layer. For the input

```
2 1
3 1
```

the first position creates the group `(3, 0)`. At the second position, `1` is smaller than `3`, so it creates another group, but the global best remains `3`. The final answer is `3`, exactly the maximum of the entire array.

When `K = N`, every act must contain exactly one element. Consider

```
3 3
2 7 4
```

The first layer produces the best one-act prefix values `2, 7, 7`. The second layer starts at `i = 2`, giving `2 + 7 = 9`, and eventually reaches the correct prefix values for two acts. The third layer can only finish at `i = 3`, where the final single-element act contributes `4`, producing `2 + 7 + 4 = 13`.

Equal values exercise the stack merging rule. For

```
4 2
5 5 1 5
```

when the second `5` arrives, the existing group with maximum `5` is popped because its maximum is equal to the new value. Both starts now have the same segment maximum, so merging them loses no information. Later, the final `5` similarly merges all groups whose current maximum is at most `5`. The optimal score is `10`.

A case such as

```
4 2
1 10 2 9
```

shows why the DP must preserve multiple possible starting positions. Cutting after the first element gives `1 + 10 = 11`, while cutting after the third element gives `10 + 9 = 19`. The monotonic stack keeps the candidates for both possibilities until the right endpoint determines which one is better, so the algorithm returns `19`.

The maximum-size input contains `2000` elements and may require `2000` acts. With all values equal to `1000`, every act contributes exactly `1000`, so the answer is `2,000,000`. The stack operations remain linear per DP layer even in this highly repetitive case, giving the required `O(KN)` running time.
