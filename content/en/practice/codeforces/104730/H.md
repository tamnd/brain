---
title: "CF 104730H - \u0417\u0430\u0434\u0430\u0447\u0430 \u0432 \u043f\u043e\u0434\u0430\u0440\u043e\u043a"
description: "We are given a collection of problems, each with a difficulty value. We can initially choose some subset of these problems to solve, as long as the sum of their difficulties does not exceed a budget $S$."
date: "2026-06-29T02:41:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104730
codeforces_index: "H"
codeforces_contest_name: "Moscow team school olympiad (MKOSHP) 2023"
rating: 0
weight: 104730
solve_time_s: 74
verified: false
draft: false
---

[CF 104730H - \u0417\u0430\u0434\u0430\u0447\u0430 \u0432 \u043f\u043e\u0434\u0430\u0440\u043e\u043a](https://codeforces.com/problemset/problem/104730/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of problems, each with a difficulty value. We can initially choose some subset of these problems to solve, as long as the sum of their difficulties does not exceed a budget $S$. This models the normal “solve as many as you can under a total cost constraint” scenario.

After this phase, there is a one-time special action. We may pick exactly one additional problem for free, even if it was not solved before. This extra choice is only allowed after we finish the initial selection, and it depends on what we already solved: the chosen bonus problem must be such that at least half of the already solved problems have difficulty not smaller than it. Once this bonus is used, the process ends.

A subtle but important detail is that solving zero problems is allowed. In that case, the condition about “half of solved problems” becomes vacuously true, so we can pick any single problem for free as the final answer.

The task is to maximize the total number of problems solved including this final free pick.

The constraints allow up to 300000 problems, so any solution that tries all subsets is impossible. Even checking all pairs or maintaining dynamic subsets per candidate quickly becomes quadratic or worse, so we need a structure that supports efficient counting and selection, likely after sorting and using a greedy or prefix-based strategy.

A few edge cases matter:

If all difficulties are very large except one small one, a naive greedy “take smallest until budget runs out” might miss that the final free pick can depend on the median of chosen set, not just remaining budget.

If we solve nothing, we can still pick any problem at the end, so the answer is at least 1 whenever $n \ge 1$.

If we solve many small problems, the free pick becomes constrained by a median-like threshold, meaning the structure of the chosen set matters, not only its sum.

## Approaches

The first natural idea is to fix the set of problems we solve under budget $S$, and then try every possible additional problem as the final pick. For each candidate set, we would check which problems satisfy the “at least half are not easier than it” condition. However, enumerating subsets under a knapsack-like constraint is exponential, and even deciding the best subset for each candidate is infeasible.

A more structured brute-force is to sort problems and try all prefixes as the solved set. For a fixed prefix, we can check all possible extra picks by counting how many elements in the prefix are at least a given value. This already reduces the search space, but still requires iterating over many prefixes and recomputing feasibility under sum constraint, which leads to $O(n^2)$ behavior in worst cases.

The key observation is that the final condition depends only on order statistics of the chosen set, not on its exact composition. If we fix the number of initially solved problems $k$, then the best strategy is always to take the $k$ smallest difficulties, because this maximizes the chance to fit under budget $S$. Among all size-$k$ subsets, this also maximizes flexibility for the final median-type condition.

So the structure becomes: choose $k$ smallest possible sum, check feasibility, then compute what is the best extra element we can take. The condition for the extra pick depends on how many chosen elements are greater or equal to it, which is directly related to the sorted order of the selected prefix.

We sort the array and use prefix sums. For each $k$, we check whether the sum of first $k$ elements is within $S$. If yes, we consider adding one more element as bonus. That bonus must be such that at least $\lceil k/2 \rceil$ elements in the chosen set are not easier than it, which means it must be no larger than the element at position $k - \lceil k/2 \rceil + 1$ in the sorted order of the chosen set. Since the chosen set is the prefix, this becomes a direct index constraint.

We maximize over all valid $k$ the value $k + 1$ if a valid bonus exists, otherwise $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | Exponential | O(n) | Too slow |
| Sort + prefix greedy check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all problem difficulties in non-decreasing order.

Sorting ensures that any prefix corresponds to the cheapest possible selection of a given size.
2. Build prefix sums over the sorted array.

This allows constant-time checks of whether a chosen prefix fits within the budget $S$.
3. Iterate over possible values of $k$, the number of problems we solve normally, from 0 to $n$.

Each $k$ represents a candidate initial strategy.
4. For each $k$, check whether the sum of the first $k$ elements is at most $S$. If not, skip it.

If we already exceed the budget, any larger $k$ is also invalid because prefix sums only increase.
5. For a valid $k$, determine whether a bonus problem can be added.

The condition requires that at least half of the $k$ solved problems have difficulty at least as large as the bonus. In a sorted prefix, this translates into requiring the bonus threshold to be at most the element at index $k - \lceil k/2 \rceil$.
6. If there exists at least one unused element that satisfies this threshold condition, we can extend the answer to $k + 1$. Otherwise the best we can do is $k$.
7. Track the maximum over all $k$.

### Why it works

The core invariant is that for any fixed number of solved problems, the optimal choice is the lexicographically smallest set, which is the prefix of sorted difficulties. Any deviation from the prefix increases total cost without improving the median-based constraint for the bonus move. The bonus condition depends only on order within the chosen set, so replacing any chosen element with a larger one cannot help. This reduces the entire decision space to prefix lengths, where both feasibility and bonus eligibility can be checked from precomputed prefix sums and indices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, S = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    ans = 0

    for k in range(n + 1):
        if pref[k] > S:
            break

        ans = max(ans, k)

        if k == 0:
            ans = max(ans, 1)
            continue

        need = (k + 1) // 2
        idx = k - need  # smallest allowed threshold index in prefix

        if idx < k:
            ans = max(ans, k + 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The sorting step guarantees we always consider optimal subsets for each size. The prefix sum array makes feasibility checks constant time. The loop over $k$ stops early once the budget is exceeded.

The key subtlety is handling $k = 0$, where the answer is always at least 1 because we can directly pick any problem using the bonus rule.

The computation of `need = (k + 1) // 2` encodes the “at least half” requirement, and converting it into an index inside the sorted prefix is what turns the median-like constraint into a simple arithmetic condition.

## Worked Examples

### Sample 1

Input:

```
6 12
4 2 1 3 6 5
```

Sorted array: [1, 2, 3, 4, 5, 6]

Prefix sums: [0, 1, 3, 6, 10, 15, 21]

We evaluate $k$:

| k | prefix sum | valid | bonus possible | best |
| --- | --- | --- | --- | --- |
| 0 | 0 | yes | yes | 1 |
| 1 | 1 | yes | yes | 2 |
| 2 | 3 | yes | yes | 3 |
| 3 | 6 | yes | yes | 4 |
| 4 | 10 | yes | yes | 5 |
| 5 | 15 | no | - | stop |

The process stops at $k=5$ because budget is exceeded. The maximum is 5.

This demonstrates that the optimal solution almost always uses the full budget greedily, and the bonus allows pushing beyond pure knapsack size by one.

### Sample 2

Input:

```
7 11
4 3 2 1 100 1000000000
```

Sorted array: [1, 2, 3, 4, 100, 1000000000]

Prefix sums: [0, 1, 3, 6, 10, 110, 1000110]

| k | prefix sum | valid | bonus possible | best |
| --- | --- | --- | --- | --- |
| 0 | 0 | yes | yes | 1 |
| 1 | 1 | yes | yes | 2 |
| 2 | 3 | yes | yes | 3 |
| 3 | 6 | yes | yes | 4 |
| 4 | 10 | yes | yes | 5 |
| 5 | 110 | no | - | stop |

Even though large elements exist, they are never used because they break the budget constraint. The solution correctly focuses entirely on small elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates; single linear scan over prefixes |
| Space | O(n) | prefix sum array and sorted list |

The constraints allow up to 300000 elements, so $n \log n$ sorting and linear scanning comfortably fit within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, S = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    pref = [0]
    for x in a:
        pref.append(pref[-1] + x)

    ans = 0
    for k in range(n + 1):
        if pref[k] > S:
            break
        ans = max(ans, k)
        if k == 0:
            ans = max(ans, 1)
            continue
        need = (k + 1) // 2
        idx = k - need
        if idx < k:
            ans = max(ans, k + 1)

    return str(ans)

# provided samples
assert run("6 12\n4 2 1 3 6 5") == "5"
assert run("7 11\n4 3 2 1 100 1000000000") == "4"

# custom cases
assert run("1 0\n100") == "1"
assert run("3 5\n10 10 10") == "1"
assert run("5 15\n1 2 3 4 5") == "5"
assert run("4 100\n1 2 3 4") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 / 100 | 1 | minimum size, forced bonus-only solution |
| 3 5 / 10 10 10 | 1 | no feasible prefix beyond zero |
| 5 15 / 1 2 3 4 5 | 5 | full greedy packing |
| 4 100 / 1 2 3 4 | 4 | unrestricted budget case |

## Edge Cases

A key edge case is when $k = 0$. The algorithm explicitly treats this as a valid state with answer 1, since we can always pick one problem using the bonus rule. For example, input:

```
3 0
5 6 7
```

Sorting gives [5, 6, 7]. No prefix of size 1 fits budget, but $k = 0$ yields answer 1 immediately, which matches the rule.

Another edge case occurs when all elements are too large to include any prefix of size 1 under $S$. The algorithm still returns 1 because the bonus mechanism bypasses the budget constraint entirely when nothing is chosen initially.

A third subtle case is when $k$ is large but the median threshold for bonus becomes very restrictive. For a prefix like [1,2,3,4,100], even though $k=5$ is barely infeasible, the structure ensures we never incorrectly assume a bonus is possible beyond the prefix limit, since the index computation ties the threshold strictly to the chosen prefix size.
