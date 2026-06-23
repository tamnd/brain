---
title: "CF 105381L - The Bag of Forgotten Coins"
description: "We are given a sequence of coins laid out in a line, where coin k has a fixed value v[k]. We are allowed to pick a subset of these coins, but there is a strict restriction: we cannot pick two coins whose indices differ by exactly one."
date: "2026-06-23T16:09:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105381
codeforces_index: "L"
codeforces_contest_name: "National Yang Ming Chiao Tung University 2024 Team Selection Programming Contest"
rating: 0
weight: 105381
solve_time_s: 60
verified: true
draft: false
---

[CF 105381L - The Bag of Forgotten Coins](https://codeforces.com/problemset/problem/105381/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of coins laid out in a line, where coin `k` has a fixed value `v[k]`. We are allowed to pick a subset of these coins, but there is a strict restriction: we cannot pick two coins whose indices differ by exactly one. In other words, if we pick coin `i`, then coins `i-1` and `i+1` become forbidden.

The task is to select a subset of indices that respects this restriction and maximizes the sum of chosen values. We are not required to pick any coin, so choosing nothing is always a valid option.

The input size goes up to one million coins, which immediately rules out any exponential enumeration of subsets. Even quadratic solutions that try to consider all pairs or recompute subproblems inefficiently will not pass. The solution must process the array in linear time with constant work per position.

A subtle point is that values can be negative. This creates cases where taking a coin is harmful, and the optimal strategy may skip many or even all coins. For example, if the input is `[-5, -2, -8]`, the correct answer is `0`, not `-2` or any negative sum, because selecting nothing is allowed and better than taking any negative contribution.

Another edge case comes from alternating signs. For input `[10, -1, 10]`, greedily taking positives does not violate adjacency, but for `[10, 5, 10]`, picking both 10s is optimal while skipping the middle entirely. This shows that local choice based only on immediate value is insufficient.

## Approaches

A direct approach would be to try all subsets of indices and check whether any two chosen indices are adjacent. For each valid subset, we compute its sum and keep the maximum. This is correct because it explores the entire search space, but the number of subsets is `2^n`, which is infeasible even for `n = 40`, let alone `10^6`.

We can improve by noticing the structure of the constraint. Each position only conflicts with its immediate neighbors, which means decisions form a chain. At index `i`, we only need to know whether we took `i-1` or skipped it. This reduces the global combinatorial explosion into a local recurrence.

At position `i`, there are only two meaningful choices: either we do not take coin `i`, in which case we carry forward the best solution up to `i-1`, or we take coin `i`, in which case we must have skipped `i-1`, and we add `v[i]` to the best solution up to `i-2`. This creates a simple dynamic programming transition over a line.

The brute force works because it explicitly explores all subsets, but fails because the number of subsets grows exponentially. The observation that each state depends only on the previous two positions lets us compress the state space into a linear recurrence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | O(2^n) | O(n) | Too slow |
| Dynamic Programming | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the array from left to right, maintaining the best achievable sum up to each prefix while respecting the adjacency restriction.

1. We define `dp[i]` as the maximum sum we can obtain using coins from index `1` to `i`. This interpretation ensures we only consider valid prefixes at each step.
2. For each position `i`, we decide between skipping or taking coin `i`. If we skip it, the best value remains `dp[i-1]`. This corresponds to carrying forward the optimal solution without change.
3. If we take coin `i`, we are forced to exclude `i-1`, so the best we can build is `dp[i-2] + v[i]`. This is the key constraint propagation step, where the adjacency rule directly reduces the available history.
4. We set `dp[i] = max(dp[i-1], dp[i-2] + v[i])`. This guarantees we preserve the best valid option at every prefix without needing to remember the full subset structure.
5. To avoid storing the entire array, we keep only the last two states. We maintain `prev2 = dp[i-2]` and `prev1 = dp[i-1]`, updating them iteratively as we move forward.

### Why it works

At every index `i`, any valid selection over the first `i` elements must fall into exactly one of two categories: either it does not include `i`, or it includes `i`. If it does not include `i`, its value is bounded by `dp[i-1]`. If it includes `i`, then it cannot include `i-1`, so the remainder of the selection is a valid solution on the first `i-2` elements. These two cases are disjoint and exhaustive, which guarantees that taking their maximum produces the optimal solution for prefix `i`. This inductive structure ensures correctness over the entire array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    v = list(map(int, input().split()))
    
    if n == 0:
        print(0)
        return

    prev2 = 0
    prev1 = 0

    for i in range(n):
        take = prev2 + v[i]
        skip = prev1
        cur = take if take > skip else skip
        prev2 = prev1
        prev1 = cur

    print(prev1)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the recurrence directly. The variable `prev1` always holds the best result up to the previous index, while `prev2` stores the result two steps back. The update order is crucial: `prev2` must be updated after computing `cur`, otherwise the recurrence would accidentally reuse overwritten state.

The initialization with zeros implicitly handles negative values correctly. Since we allow selecting nothing, starting from zero ensures that we never force a negative contribution.

## Worked Examples

Consider the input `v = [3, 2, 5]`.

We track `prev2`, `prev1`, and `cur`:

| i | v[i] | take = prev2 + v[i] | skip = prev1 | cur |
| --- | --- | --- | --- | --- |
| 0 | 3 | 3 | 0 | 3 |
| 1 | 2 | 2 | 3 | 3 |
| 2 | 5 | 8 | 3 | 8 |

The final answer is `8`, achieved by picking indices `1` and `3`. This shows how skipping an intermediate element enables a larger later gain.

Now consider `v = [4, -1, 2, 10]`.

| i | v[i] | take | skip | cur |
| --- | --- | --- | --- | --- |
| 0 | 4 | 4 | 0 | 4 |
| 1 | -1 | -1 | 4 | 4 |
| 2 | 2 | 6 | 4 | 6 |
| 3 | 10 | 14 | 6 | 14 |

This trace shows how negative values naturally get avoided unless they enable a better future combination.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each coin contributes a constant amount of work in the recurrence |
| Space | O(1) | Only two rolling states are stored regardless of input size |

The linear scan is necessary because each position depends only on its immediate neighbors, and there is no structure that allows skipping indices safely. With `n` up to one million, a single pass solution fits comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# minimum size
assert run("1\n5\n") == "5"

# all negative values
assert run("3\n-5 -2 -8\n") == "0"

# increasing values
assert run("4\n1 2 3 4\n") == "6"

# alternating high values
assert run("5\n10 1 10 1 10\n") == "30"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 5 | base case handling |
| all negatives | 0 | empty selection optimality |
| increasing | 6 | skipping middle elements |
| alternating highs | 30 | optimal non-adjacent accumulation |

## Edge Cases

For a single coin like `n = 1, v = [7]`, the algorithm sets `prev1 = 7` after the first iteration, directly selecting the only available option. The recurrence naturally reduces to a single comparison between taking and skipping, where skipping yields zero and taking yields seven.

For all-negative input like `[-3, -1, -2]`, the rolling state ensures that every `take` value is negative while `skip` carries forward zero. At each step, the maximum keeps the result at zero, correctly modeling the option of selecting no coins at all.
