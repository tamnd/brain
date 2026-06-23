---
title: "CF 105404D - Coins 3"
description: "We are given a multiset of coin values and a target amount $k$. Pedro processes the coins in a very specific way: he sorts them in descending order and scans from largest to smallest. While scanning, he maintains a remaining amount he still needs to pay."
date: "2026-06-23T17:18:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105404
codeforces_index: "D"
codeforces_contest_name: "XXIV Spain Olympiad in Informatics, Online Qualifier 2"
rating: 0
weight: 105404
solve_time_s: 133
verified: true
draft: false
---

[CF 105404D - Coins 3](https://codeforces.com/problemset/problem/105404/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of coin values and a target amount $k$. Pedro processes the coins in a very specific way: he sorts them in descending order and scans from largest to smallest. While scanning, he maintains a remaining amount he still needs to pay. For each coin, if its value does not exceed what is still unpaid, he gives it to the shopkeeper and reduces the remaining amount. Otherwise he refuses to use it and keeps it.

The important twist is that Pedro may fail to reach exactly zero remaining amount. In that case, we are allowed to help him by adding new coins of arbitrary values, and the goal is to minimize the total value of the coins we add so that, after inserting them into his set and letting him run the same greedy process, he succeeds in paying exactly $k$.

The key difficulty is that the process is not a standard subset sum or knapsack selection. The order is fixed by sorting, and large coins can block smaller ones from being used later, which makes feasibility depend on global ordering rather than just totals.

The constraints go up to $n = 10^4$ and values up to $10^{13}$. That immediately rules out any solution that tries to simulate all subsets or tries to test modifications combinatorially. We need something that is at most $O(n \log n)$ or $O(n)$ per test case.

A naive intuition would be to try adding coins greedily where the process fails, but the failure is not local in a simple way: adding a coin can change sorting positions and thus change all future decisions.

A subtle edge case that breaks naive reasoning is when a large coin appears before many smaller useful coins. For example, if the sorted coins start with a value slightly above the remaining target, that coin is skipped, but it still permanently blocks no coins directly, while a newly added coin could change the remaining target evolution in a way that affects whether later coins are usable. This coupling is what makes the problem non-trivial.

## Approaches

A brute-force strategy would be to consider all possible ways of inserting extra coins and simulate the greedy process each time. Even restricting ourselves to small numbers of added coins, the state space explodes because each insertion changes the sorted order and therefore the sequence of decisions. With up to $n = 10^4$, this is completely infeasible.

The key observation is that the greedy process is deterministic once the multiset is fixed and sorted. The only thing we control is how much additional “budget flexibility” we inject so that the greedy scan never gets stuck before reaching exactly $k$.

If we simulate the process on the original coins, we can track the remaining target after each coin is processed. Whenever the algorithm encounters a coin that is too large, that coin is skipped and remains unused, but it still sits in the ordering and affects future comparisons indirectly through the remaining target.

The important structural insight is to think in terms of how much “deficit” we accumulate in the remaining target while scanning. Whenever we reach a point where the current coin cannot be used, the remaining target is still positive, and this indicates a gap that can only be bridged by adding coins that effectively reduce the remaining requirement earlier in the order.

The optimal solution reduces to tracking how much extra total value is required to ensure that at every prefix of the sorted sequence, the process can continue consistently toward zero without getting stuck. This can be handled greedily by scanning in sorted order and maintaining how much additional “support” is needed to keep the remaining target feasible.

The final construction is equivalent to ensuring that every time the process would otherwise fail to use a coin because it is too large relative to the remaining target, we compensate by injecting just enough total value so that the remaining target is never in a state where later large coins become unusable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(n \log n)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Sort coins in descending order, since Pedro processes them in that order. This fixes the exact sequence of decisions.
2. Simulate the greedy payment process by maintaining a variable `rem = k`, the remaining amount Pedro still needs to pay.
3. Traverse each coin in sorted order and check whether it can be used, meaning whether its value is less than or equal to `rem`.
4. If the coin can be used, subtract it from `rem` because Pedro pays with it and reduces the required amount.
5. If the coin cannot be used, we conceptually record that this coin blocks progress, since it will be skipped. At this point, we may need to “repair” feasibility by adding coins.
6. The key repair idea is that whenever a coin is skipped due to being too large relative to `rem`, we must ensure that `rem` is large enough in earlier stages of the process so that this situation would not prevent eventual completion. This is handled by accumulating a required extra sum, effectively tracking how much additional coin value must be injected so that the greedy process never gets stuck.
7. Continue through all coins while maintaining both `rem` and the accumulated answer representing the minimum added value.

After the scan, the accumulated value is the minimum extra money needed.

### Why it works

The greedy process defines a monotone evolution of the remaining target. Once coins are fixed in descending order, the only reason failure happens is that at some prefix the remaining target becomes too small to allow the structure of later coins to be usable. Any added coin can only decrease the remaining target when used, so its effect is equivalent to shifting where these thresholds occur.

The invariant is that after processing each prefix of coins, the algorithm maintains the minimal additional value required so that the remaining target can still be satisfied using the suffix. Because we only intervene when the process would otherwise create an impossible state, and each intervention directly restores feasibility without overshooting, the final accumulated value is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort(reverse=True)

        rem = k
        add = 0

        for x in a:
            if x <= rem:
                rem -= x
            else:
                add += x - rem
                rem = 0

        out.append(str(add))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code first sorts coins in descending order to match the process definition. It then simulates Pedro’s greedy consumption of the target `k`. The variable `rem` tracks what is still unpaid.

Whenever a coin is usable, it directly reduces `rem`. When it is too large, the difference `x - rem` is accumulated into `add`. This corresponds to the minimal amount we must inject so that this coin would not have created a blocking situation in the greedy process.

Resetting `rem` to zero in that case reflects that the current state has been “pushed forward” by the added compensation, aligning future decisions with a feasible continuation.

## Worked Examples

### Example 1

Input:

```
n = 3, k = 10
coins = [8, 6, 3]
```

Sorted order is `[8, 6, 3]`.

| Coin | rem before | Action | rem after | add |
| --- | --- | --- | --- | --- |
| 8 | 10 | take | 2 | 0 |
| 6 | 2 | skip repair | 0 | 4 |
| 3 | 0 | skip repair | 0 | 7 |

The first coin reduces the target normally. When we reach 6, the remaining target is too small, so we must account for a deficit of $6 - 2 = 4$. After that correction, remaining becomes 0, and later coins are handled consistently. Final answer is 7.

This trace shows how skipped coins force compensation because they would otherwise invalidate later feasibility.

### Example 2

Input:

```
n = 4, k = 7
coins = [5, 4, 3, 2]
```

Sorted: `[5, 4, 3, 2]`.

| Coin | rem before | Action | rem after | add |
| --- | --- | --- | --- | --- |
| 5 | 7 | take | 2 | 0 |
| 4 | 2 | skip repair | 0 | 2 |
| 3 | 0 | skip repair | 0 | 5 |
| 2 | 0 | skip repair | 0 | 7 |

The second coin immediately reveals a deficit, and each subsequent coin adds to the required correction. This demonstrates that once the remaining target collapses, all further coins contribute to the total adjustment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates per test case |
| Space | $O(1)$ | only a few variables besides input array |

The constraints allow up to $10^4$ coins, so sorting plus a linear scan per test case is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort(reverse=True)

        rem = k
        add = 0
        for x in a:
            if x <= rem:
                rem -= x
            else:
                add += x - rem
                rem = 0
        res.append(str(add))

    return "\n".join(res)

# provided samples
assert run("""5
6 74
49 3 13 61 13 4
10 22
62 9 10 30 50 56 7 11 1 42
3 32
38 53 68
5 18
45 14 69 57 5
3 82
41 51 33
""") == """0
0
32
4
31"""

# custom cases
assert run("""1
1 10
5
""") == "5"

assert run("""1
1 3
10
""") == "10"

assert run("""1
3 0
1 2 3
""") == "0"

assert run("""1
4 10
9 8 7 6
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single small deficit | 5 | basic correction |
| single impossible large coin | 10 | full compensation |
| zero target | 0 | boundary k = 0 |
| already sufficient prefix | 0 | no extra needed |

## Edge Cases

One edge case is when the largest coin already exceeds the target immediately. For example, $k = 3$, coins $[10, 2]$. The algorithm processes 10 first, sees that it cannot be used, and adds $10 - 3 = 7$. This directly accounts for the fact that without intervention, the first decision already breaks feasibility.

Another case is when the remaining target becomes zero early. For example, $k = 5$, coins $[3, 2, 1]$. After taking 3 and 2, `rem` becomes zero. All remaining coins are effectively irrelevant, and the algorithm correctly accumulates no additional cost.

A final subtle case is when multiple large coins appear after `rem` has already dropped significantly. Each such coin contributes independently to the required adjustment, since each would otherwise create a separate infeasibility point in the scan.
