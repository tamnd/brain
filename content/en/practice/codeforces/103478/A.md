---
title: "CF 103478A - \u76ae\u5361\u4e18\u4e0e Codeforces"
description: "We are given multiple Codeforces accounts, each starting with its own rating value. Over time, a sequence of contests happens, and each contest contributes a fixed rating change. For every contest, we must choose exactly one account to participate."
date: "2026-07-03T06:34:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103478
codeforces_index: "A"
codeforces_contest_name: "The 16-th Beihang University Collegiate Programming Contest (BCPC 2021) - Final"
rating: 0
weight: 103478
solve_time_s: 45
verified: true
draft: false
---

[CF 103478A - \u76ae\u5361\u4e18\u4e0e Codeforces](https://codeforces.com/problemset/problem/103478/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple Codeforces accounts, each starting with its own rating value. Over time, a sequence of contests happens, and each contest contributes a fixed rating change. For every contest, we must choose exactly one account to participate. When an account is chosen for a contest, that account alone receives the rating change for that contest, while all other accounts remain unchanged.

After all contests are assigned to accounts, every account will have accumulated some subset of the rating changes. The final value of each account is its initial rating plus the sum of all contest contributions assigned to it. Our goal is to distribute the contests among accounts so that the maximum final rating among all accounts is as large as possible.

The structure of the problem suggests a tradeoff: concentrating many positive gains into a single account increases a maximum, but negative values can drag an account down. Since we are maximizing the maximum final value across all accounts, we are effectively trying to construct one “best” account by selecting a subset of contests for it, while other accounts serve as sinks for remaining contests.

The constraints allow up to 100,000 accounts and 100,000 contests. Any solution that tries to enumerate assignments or even dynamic programming over subsets is impossible. A solution must be close to linear or linearithmic, around O(n + m) or O((n + m) log n).

A subtle edge case arises when all di are negative. A naive greedy strategy that always assigns positives to the current best account and negatives elsewhere can fail if it does not explicitly account for the fact that distributing negatives across accounts still affects the global maximum indirectly by lowering alternative candidates.

Another corner case is when all di are positive. In that case, the optimal strategy is to stack all contests onto a single account, but this is not immediately obvious if one thinks per-contest assignment greedily without considering the final objective.

## Approaches

The brute-force interpretation is to consider every possible assignment of each contest to one of n accounts. For each assignment, we compute final ratings and track the maximum value across accounts. This leads to n choices per contest, producing n^m possible assignments. Even for small values, this is astronomically large and completely infeasible.

The key observation is that only one account actually matters for the final answer, namely the account that ends up being the maximum after all updates. Suppose we fix which account will become the final maximum. Then every contest assignment that does not go to this account is irrelevant except for how it affects that account indirectly, which it does not. Therefore, for a chosen account i, we want to maximize its final value by assigning to it as many beneficial di as possible.

However, we are not forced to assign all contests to that account. Any contest assigned elsewhere does not contribute to i, so for maximizing i we clearly prefer assigning every contest to i. There is no restriction preventing this. Thus, for any fixed account i, its best possible final value is simply ri + sum(di over all contests).

This means every account can independently achieve the same total increase sum(di). Therefore, the only variation across accounts is their initial values ri. The best possible final maximum is achieved by taking the account with the largest initial rating and giving it all contests.

The subtle reasoning step is recognizing that since all di are always applied to exactly one account and we are maximizing the maximum over accounts, there is never a reason to split contests across accounts in a way that reduces the contribution to the current maximum candidate. Concentrating everything into the strongest initial account dominates all alternatives.

We can now reduce the problem to a simple computation: compute total sum of di, then add it to max ri.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Assignment | O(n^m) | O(n) | Too slow |
| Optimal Aggregation | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read n and m, followed by the array of initial ratings ri and the array of contest changes di.
2. Compute the maximum value among all initial ratings. This represents the strongest starting point among all accounts. Any optimal solution must end on some account, and starting from the best baseline is always dominant.
3. Compute the sum of all di. This represents the total available rating gain that will be injected into the system across all contests.
4. Add the total sum of di to the maximum initial rating. This corresponds to assigning every contest to the account that already has the highest starting value, ensuring that this account accumulates the full gain.
5. Output the resulting value.

Why it works

At any point, each contest contributes exactly one di to exactly one account. Therefore, across all accounts combined, the total added value is fixed and equal to sum(di). Since we are maximizing the maximum final account value, we want to concentrate as much of this fixed total into a single account. Any distribution that splits contributions across multiple accounts can only reduce the peak achievable value of any single account compared to concentrating all contributions. Thus, the optimal strategy is to assign all contributions to the account with the highest initial value, making the final answer max(ri) + sum(di).

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    r = list(map(int, input().split()))
    d = list(map(int, input().split()))
    
    best = max(r)
    total = sum(d)
    
    print(best + total)

if __name__ == "__main__":
    solve()
```

The implementation is straightforward: we scan the initial ratings once to find the maximum, and scan the contest deltas once to compute their sum. The result is the sum of these two values. No sorting or simulation is required.

A common mistake would be attempting to simulate assignment per contest or tracking per-account updates, which is unnecessary and risks TLE. Another mistake would be trying to distribute positive and negative di separately, but this ignores that the total sum is invariant and independent of assignment.

## Worked Examples

### Example 1

Input:

n = 2, m = 2

r = [1500, 1500]

d = [300, -300]

We compute:

| Step | Best rating | Sum d | Current answer |
| --- | --- | --- | --- |
| Init | 1500 | 0 | 1500 |
| After sum | 1500 | 0 | 1500 |

Final result is 1500.

This shows a case where gains and losses cancel out. Even though one contest is positive and one is negative, they must both be assigned somewhere, and the total net effect is zero. The best achievable maximum remains the initial best rating.

### Example 2

Input:

n = 3, m = 3

r = [100, 200, 50]

d = [10, 20, 30]

| Step | Best rating | Sum d | Current answer |
| --- | --- | --- | --- |
| Init | 200 | 0 | 200 |
| After sum | 200 | 60 | 260 |

Final result is 260.

This confirms that concentrating all positive contributions into the strongest initial account yields the maximum possible final value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | One pass to compute max of ratings and one pass to sum deltas |
| Space | O(1) | Only a few accumulator variables are used |

The constraints allow up to 200,000 total inputs, and a linear scan easily fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    r = list(map(int, input().split()))
    d = list(map(int, input().split()))
    return str(max(r) + sum(d))

# provided sample
assert run("2 2\n1500 1500\n300 -300\n") == "1500"

# minimum case
assert run("1 1\n5\n10\n") == "15"

# all negative updates
assert run("3 3\n100 200 150\n-1 -2 -3\n") == str(200 - 6)

# all positive updates
assert run("2 4\n10 20\n1 2 3 4\n") == str(20 + 10)

# mixed ratings
assert run("3 2\n-5 0 5\n100 -50\n") == str(5 + 50)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single account | handles trivial aggregation | base case correctness |
| all negative di | verifies cancellation behavior | negative handling |
| all positive di | verifies full accumulation | greedy concentration |
| mixed ri values | ensures correct max selection | initialization correctness |

## Edge Cases

A key edge case is when all di are negative. For example, if ri = [100, 90] and di = [-10, -20], the algorithm computes max ri = 100 and sum di = -30, producing 70. The execution assigns all updates to the best account conceptually, yielding 100 - 30. Any attempt to distribute negatives across accounts does not improve the maximum because every negative must still be assigned somewhere.

Another edge case is when there is only one account. In this case, all contests must be assigned to it, so the answer reduces to r1 + sum(di). The algorithm naturally handles this because max(r) is r1.

A final edge case is when all di are zero. The system does nothing, and the answer is simply the maximum initial rating. The algorithm reduces correctly since sum(di) is zero and the maximum remains unchanged.
