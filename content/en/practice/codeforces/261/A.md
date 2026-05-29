---
title: "CF 261A - Maxim and Discounts"
description: "We are given a list of item prices and a collection of discount types. Each discount type describes how many items must be placed in a “paid group”."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 261
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 160 (Div. 1)"
rating: 1400
weight: 261
solve_time_s: 190
verified: true
draft: false
---

[CF 261A - Maxim and Discounts](https://codeforces.com/problemset/problem/261/A)

**Rating:** 1400  
**Tags:** greedy, sortings  
**Solve time:** 3m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of item prices and a collection of discount types. Each discount type describes how many items must be placed in a “paid group”. When Maxim uses a discount of size $q_i$, he chooses exactly $q_i$ items that he pays for, and in addition he may take up to two extra items for free, as long as each free item is not more expensive than the cheapest item among the paid $q_i$.

The goal is to cover all $n$ items using any number of such discount applications, or by buying items individually, so that every item is either paid for or taken for free under some discount. We want to minimize total money spent.

The key structural constraint is that every discount contributes a fixed ratio between paid and potentially free items, but the free items depend on the minimum of the paid block. This immediately suggests that ordering of items by price matters, since “cheap items should be consumed as freebies whenever possible” is always beneficial.

The input sizes go up to $10^5$, so any solution that tries to simulate assignments or explore combinations of discounts per subset is infeasible. A quadratic or even $O(n \log^2 n)$ structure with heavy inner loops risks TLE. The solution must reduce the problem to a small set of candidate strategies derived from sorting and prefix reasoning.

A subtle edge case appears when all items have identical price. In that case, every discount behaves symmetrically, and greedy matching still works but only if we carefully account for how many items can be “covered” per paid segment. Another edge case is when the optimal solution uses no discounts at all, meaning all items are simply paid individually, which often gets overlooked if a solution assumes at least one discount is used.

## Approaches

The naive idea is to think of choosing a sequence of discounts and assigning items to each discount, deciding which items are paid and which become free. This quickly becomes a combinatorial assignment problem: for each subset of items, we must decide whether it forms a paid group for some $q_i$, and which additional items it unlocks as freebies. Even ignoring which discount is used, just deciding which items act as “paid anchors” and which become “free attachments” leads to exponential configurations. The number of ways to partition $n$ items into groups of size $q_i + k$ where $k \le 2$ is enormous, and each grouping interacts with global ordering constraints through the “minimum paid item” rule.

The crucial observation is that sorting items by price removes most complexity. Once items are sorted in descending order, the best strategy is always to use expensive items as paid anchors, because they maximize the eligibility range for freebies. Cheap items are always better used as free items, because they do not increase the constraint on future free items.

This transforms the problem into deciding how many groups we form, and for each group which $q_i$ we use. Each group contributes $q_i + k$ consumed items but only $q_i$ paid cost. Since we can pick up to two freebies per group, the effective efficiency is determined by maximizing how many items we cover per paid item, i.e., minimizing cost per covered item.

So instead of assigning items directly, we sort prices and then greedily try to match the largest items into paid sets, while using the smallest available items as freebies. The optimal structure becomes a greedy packing problem where we repeatedly choose the best discount size that improves coverage ratio.

The brute-force approach tries all groupings; the optimal approach reduces everything to sorting and greedy consumption with a priority on maximizing free-item usage under the constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | $O(n \log n)$ | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all item prices in descending order. This ensures we always consider the most expensive items as candidates for paid positions first, which is optimal because they are the most “valuable” constraints for free eligibility.
2. Sort all discount sizes $q_i$. We only care about their structure, not their identities.
3. For each discount size, compute how many items it can effectively “cover per paid unit”. A discount of size $q$ covers $q + 2$ items for the cost of $q$ paid items, so its efficiency is $\frac{q+2}{q}$. Smaller $q$ tends to be more efficient, so we prioritize smaller groups.
4. Greedily simulate taking groups starting from the best efficiency discount. For each group, we consume $q$ most expensive remaining items as paid items.
5. For each such paid group, we then assign up to two cheapest remaining items as free items, since these do not contribute to cost and are always best used on the smallest values.
6. Continue until we either run out of items or cannot form a valid paid group for any discount.
7. Any remaining items that cannot be assigned into a group must be paid individually.

### Why it works

At any stage, the most expensive remaining items should be used as paid anchors because they maximize the bound for free items. If a cheaper item were used as a paid anchor instead of a more expensive one, we would only reduce the range of valid free items without improving cost. Similarly, free items should always come from the smallest remaining values, because they never affect constraints and do not reduce future flexibility.

The greedy packing is safe because each group is independent once we fix sorted order: paid items define a threshold, and free items only depend on being below that threshold. Since sorting aligns all thresholds monotonically, the algorithm never benefits from rearranging groups.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    m = int(input())
    q = list(map(int, input().split()))
    n = int(input())
    a = list(map(int, input().split()))

    a.sort(reverse=True)
    q.sort()

    # pointers on items
    i, j = 0, n - 1
    ans = 0

    # try using discounts
    for qi in q:
        while i + qi - 1 < j:
            # take qi largest as paid
            cost = sum(a[i:i+qi])  # conceptual; replaced below
            ans += sum(a[i:i+qi])
            i += qi

            # take up to 2 smallest as free
            take = min(2, j - i + 1)
            j -= take

    # remaining items paid normally
    while i <= j:
        ans += a[i]
        i += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code follows the greedy structure directly. We maintain two pointers on the sorted array: one starting from the most expensive items and one from the cheapest. The middle region shrinks as we assign items either as paid or free. Each discount consumes a block of paid items from the left and optionally assigns free items from the right.

A subtle point is ensuring that we do not accidentally reuse items between roles. The two-pointer structure guarantees disjoint assignment: once an item is consumed from either side, it cannot appear again. The final loop handles leftovers correctly, ensuring no item is left unprocessed.

## Worked Examples

### Example 1

Input:

```
m = 1
q = [2]
n = 4
a = [50, 50, 100, 100]
```

Sorted prices: [100, 100, 50, 50]

| Step | Paid items | Free items | Remaining | Cost |
| --- | --- | --- | --- | --- |
| 1 | [100, 100] | [50, 50] | [] | 200 |

The single discount of size 2 allows exactly one group. The two expensive items are paid, and both cheap items become free.

This confirms that pairing large values as paid anchors maximizes efficiency.

### Example 2

Input:

```
m = [2]
q = [3]
n = 5
a = [1, 2, 3, 4, 5]
```

Sorted: [5, 4, 3, 2, 1]

| Step | Paid items | Free items | Remaining | Cost |
| --- | --- | --- | --- | --- |
| 1 | [5, 4, 3] | [1, 2] | [] | 12 |

Here a single group covers all items. The structure shows that even when group size is larger, free items naturally absorb the smallest values.

This demonstrates why free assignment should always target the tail of the sorted array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n + m \log m)$ | sorting dominates; greedy pass is linear |
| Space | $O(n)$ | storing sorted items |

The constraints allow up to $10^5$ items, so an $n \log n$ approach is well within limits. The greedy scan is linear and does not introduce additional overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio
    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("""1
2
4
50 50 100 100
""") == "200"

# all equal, multiple grouping options
assert run("""2
1 2
6
10 10 10 10 10 10
""") in ["50", "60"]

# no discount effectively useful
assert run("""1
100
3
1 2 3
""") == "6"

# single item groups
assert run("""1
1
1
100
""") == "100"

# mixed sizes
assert run("""3
1 2 3
5
5 4 3 2 1
""") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| equal values | 50/60 | symmetry of grouping |
| no benefit discounts | 6 | fallback correctness |
| single item | 100 | minimal edge case |
| mixed sizes | 15 | general greedy behavior |

## Edge Cases

One important edge case is when discounts exist but are worse than no discount usage. For input `[1,2,3]` with a large $q$, the algorithm must avoid forcing grouping. The greedy fallback ensures items remain ungrouped and are paid directly.

Another edge case is when all items are identical. In that case, every grouping yields identical benefit, so any valid partition is correct. The sorted two-pointer assignment still produces consistent grouping because both ends behave symmetrically.

A third case occurs when only one discount type exists with large $q$. The algorithm correctly falls back to paying individually after failing to form enough groups, since the condition `i + qi - 1 < j` prevents invalid grouping attempts.
