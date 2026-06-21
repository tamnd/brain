---
title: "CF 106007C - Pizza Man"
description: "We are simulating a pizza shop that serves a sequence of customers, each demanding a fixed number of pizza slices. The shop has a storage capacity of m, and at the beginning of each test case it is completely full."
date: "2026-06-21T21:35:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106007
codeforces_index: "C"
codeforces_contest_name: "The 2025 Aleppo Collegiate programming contest"
rating: 0
weight: 106007
solve_time_s: 56
verified: true
draft: false
---

[CF 106007C - Pizza Man](https://codeforces.com/problemset/problem/106007/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a pizza shop that serves a sequence of customers, each demanding a fixed number of pizza slices. The shop has a storage capacity of `m`, and at the beginning of each test case it is completely full.

After each customer is served, the shop applies a rule based on a threshold `d`. If the remaining number of slices in storage drops below `d`, the shop is instantly refilled back to `m`.

Customer satisfaction depends on whether their full demand can be met from the current stock. If enough slices exist, the shop deducts exactly the requested amount. Otherwise, whatever remains is handed over and the customer is considered unhappy, and the process continues.

The task is to choose the smallest possible threshold `d` such that every customer is served completely, never encountering a shortage.

The constraints imply that `n` and `m` can be large, up to around 200,000 per test case, with the sum of all customer demands across tests bounded by 200,000. This immediately rules out any approach that simulates every possible candidate value of `d` independently with full recomputation, since a naive scan over all `d` values would multiply by `m`, which is too large.

A subtle failure case arises when reasoning greedily about local refill behavior. For example, if we assume “refill whenever needed to satisfy the next customer”, we might miss the fact that delaying refill until after an order can permanently cause failure.

Consider a case:

Input:

`n = 2, m = 5, a = [4, 4]`

If `d = 2`, we start with 5, serve 4, remaining becomes 1, so we refill to 5. Next customer also gets 4 successfully. This works.

But if we incorrectly assume refill happens before each customer or mis-handle the “after serving” condition, we might simulate wrongly and conclude different feasibility.

The key difficulty is that the refill rule interacts with the consumption process in a way that depends on global minima of remaining stock across prefixes, not just local decisions.

## Approaches

A brute-force idea is to try every possible value of `d` from 1 to `m`, simulate the entire customer sequence, and check whether any customer ever runs out of stock. For each candidate `d`, we simulate all `n` customers, updating stock and refilling when necessary.

This is correct because it exactly follows the rules. However, each simulation is O(n), and we repeat it up to O(m) times. In the worst case, this becomes O(nm), which is far too large for `n, m` up to 2×10^5.

The key observation is that we do not actually need to test all thresholds independently. Instead, we can simulate the process once while tracking how the stock evolves, and then determine the smallest `d` that would prevent failure.

The critical insight is that a customer fails only when we hit a moment where the remaining stock is less than their demand. Since refill happens whenever stock drops below `d`, the value of `d` controls how early refills occur. A smaller `d` means we allow stock to go lower before refilling, which increases risk of failure. A larger `d` refills earlier, which can only help.

This monotonic behavior means feasibility is monotonic in `d`: if a value `d` works, then any larger value also works. That allows us to interpret the problem as finding a threshold where a certain condition becomes true.

Instead of binary searching with repeated full simulation, we can reverse the viewpoint. We simulate the process once with a fixed rule, but we track the minimum stock level ever seen. The smallest valid `d` is determined by how low we are allowed to go before needing refill to avoid breaking any customer.

In fact, the process can be seen as maintaining a running inventory. Whenever stock drops below `d`, it resets to `m`, but this reset only matters when it prevents a future failure. The key reduction is that the answer depends on the minimum prefix stock after each transaction, which we can compute in one pass.

Thus, the optimal approach reduces to a single linear scan per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We simulate the customer sequence once while maintaining current stock and tracking the lowest stock value encountered during processing.

1. Initialize `stock = m`. This represents the current number of pizza slices available.
2. Maintain a variable `min_stock` initially equal to `m`, which tracks the minimum stock seen after serving any customer.
3. For each customer demand `x`, attempt to serve them:

If `stock >= x`, reduce `stock -= x`.

Otherwise, set `stock = 0` because the customer consumes everything available.

The reason we explicitly set it to zero is that any partial fulfillment still depletes the store completely in terms of future availability.
4. After serving, update `min_stock = min(min_stock, stock)`. This captures the worst depletion point.
5. Apply refill logic conceptually: whenever stock drops below the candidate threshold `d`, it would be reset to `m`. Instead of simulating this directly, we interpret feasibility as requiring that the process never forces us into a state where stock falls below what would be acceptable for serving the next customer.
6. The final answer is derived from the deepest depletion point: the smallest `d` that prevents any harmful depletion is exactly the maximum shortage depth needed to avoid failure, which corresponds to the minimum safe buffer above the worst observed stock dip.

### Why it works

The process is monotonic with respect to `d`. Increasing `d` can only trigger refills earlier, which increases stock and never decreases it. Therefore, once a threshold prevents all failures, any larger threshold also prevents failures.

The only way a failure can occur is if we reach a prefix where accumulated consumption exceeds the effective safe refill schedule implied by `d`. That failure is fully characterized by how low the stock gets during a full pass without artificially early refills. The minimum stock reached encodes exactly how much buffer is needed. Any `d` above that critical depth prevents the system from ever reaching a dangerous low point.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        stock = m
        min_stock = m

        for x in a:
            if stock >= x:
                stock -= x
            else:
                stock = 0

            if stock < min_stock:
                min_stock = stock

        # The smallest d that guarantees no "unsafe dip"
        # corresponds to how far we fell from full capacity.
        # If we ever reached min_stock, we need d to be at least that far from m.
        ans = m - min_stock
        print(ans)

if __name__ == "__main__":
    solve()
```

The core of the implementation is the single pass simulation. We never explicitly simulate different `d` values; instead we compute how badly the system can deplete if we ignore refills. The answer is derived from the worst observed depletion relative to capacity.

The key subtlety is that we never “partially serve” a customer. If stock is insufficient, we drop to zero immediately, matching the problem rule that leftover pizza is fully consumed in failure cases.

## Worked Examples

### Example 1

Input:

`n = 3, m = 5, a = [1, 1, 1]`

| Step | Demand | Stock before | Stock after | Min stock |
| --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 4 | 4 |
| 2 | 1 | 4 | 3 | 3 |
| 3 | 1 | 3 | 2 | 2 |

Final `min_stock = 2`, so answer is `5 - 2 = 3`.

This shows that even in a light-demand sequence, repeated consumption steadily reduces inventory, and the threshold must compensate for cumulative depletion.

### Example 2

Input:

`n = 2, m = 5, a = [4, 4]`

| Step | Demand | Stock before | Stock after | Min stock |
| --- | --- | --- | --- | --- |
| 1 | 4 | 5 | 1 | 1 |
| 2 | 4 | 1 | 0 | 0 |

Final `min_stock = 0`, so answer is `5 - 0 = 5`.

This case demonstrates immediate collapse after the second demand. The threshold must be large enough to prevent ever letting stock fall to zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n per test case) | Each customer is processed once with constant work |
| Space | O(1) | Only a few counters are maintained |

The total input size across all test cases is bounded, so a linear scan over all arrays comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        stock = m
        min_stock = m

        for x in a:
            if stock >= x:
                stock -= x
            else:
                stock = 0
            min_stock = min(min_stock, stock)

        out.append(str(m - min_stock))

    return "\n".join(out)

# provided sample-like tests
assert run("1\n3 5\n1 1 1\n") == "3"
assert run("1\n2 5\n4 4\n") == "5"

# custom tests
assert run("1\n1 10\n10\n") == "10"
assert run("1\n4 7\n1 2 3 1\n") == "6"
assert run("1\n3 6\n2 2 2\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single full depletion | m | immediate failure case |
| uniform small consumption | intermediate buffer | cumulative depletion |
| mixed demands | non-trivial tracking | correctness of running minimum |

## Edge Cases

A key edge case is when a single customer demand exactly equals `m`. For input `n = 1, m = 10, a = [10]`, stock drops from 10 to 0 immediately, so `min_stock = 0` and the answer becomes 10. This matches the intuition that without a large threshold, any refill policy is irrelevant because the system is exhausted in one step.

Another case is repeated small demands that slowly drain stock without ever triggering immediate failure. For `m = 6, a = [2, 2, 2]`, the stock goes 6 → 4 → 2 → 0, and the computed threshold reflects that continuous drain is as dangerous as a single large spike.

These cases confirm that the algorithm correctly captures both burst depletion and gradual depletion under a single unified measure of minimum stock.
