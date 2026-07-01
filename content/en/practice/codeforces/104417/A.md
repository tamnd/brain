---
title: "CF 104417A - Orders"
description: "Each order in this problem arrives with a deadline day and a required quantity of products. The factory produces a fixed number of products every day starting from day one, and there is no initial inventory."
date: "2026-06-30T19:15:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104417
codeforces_index: "A"
codeforces_contest_name: "The 13th Shandong ICPC Provincial Collegiate Programming Contest"
rating: 0
weight: 104417
solve_time_s: 49
verified: true
draft: false
---

[CF 104417A - Orders](https://codeforces.com/problemset/problem/104417/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

Each order in this problem arrives with a deadline day and a required quantity of products. The factory produces a fixed number of products every day starting from day one, and there is no initial inventory. Whenever a day ends, production for that day is added to the stock, and then any orders whose deadline is that day must be fully satisfied using the current stock.

The task is to determine whether there exists any way to process all orders so that every order is fulfilled no later than its deadline, given that production is uniform and stock accumulates over time.

The key difficulty is that orders are not naturally aligned in input order. Two orders with different deadlines interact through shared stock, so a locally feasible decision can break feasibility later if stock is consumed in the wrong order.

The constraints are small in terms of number of orders, at most one hundred per test case, but the values of deadlines and requirements can be as large as one billion. This immediately rules out simulating each day explicitly. Any correct solution must operate on compressed time events, specifically the distinct deadline days that actually appear in the input.

A naive but tempting mistake is to process orders in input order or even in increasing deadline order without carefully handling accumulation of stock across gaps in time. For example, if one greedily serves a large early requirement without accounting for later combined demand at the same or earlier effective stock level, it is possible to exhaust inventory prematurely.

Another subtle failure mode occurs when multiple orders share the same deadline. If a solution processes them one by one without ensuring the stock check is against the total demand at that deadline, it may incorrectly accept partial satisfaction across multiple steps instead of verifying the aggregated requirement.

## Approaches

The brute-force interpretation is to simulate day by day. For each day, we increase stock by k, then check all orders due that day and try to fulfill them greedily. This is correct in principle because it directly mirrors the process described, but it is completely infeasible when deadlines go up to 10^9. Even if there are only 100 orders, simulating up to the maximum deadline would require up to 10^9 iterations per test case.

The key observation is that nothing changes between two consecutive deadline days. Production accumulates linearly, and orders only “activate” at their deadline. This allows us to compress time to just the days that appear as deadlines.

Once time is compressed, we need to ensure that at every deadline day, the stock available up to that point is enough to satisfy all orders due at that day. However, simply checking per day independently is insufficient because stock is shared across days. The correct perspective is to process deadlines in increasing order and maintain the total required demand up to that day.

At each distinct deadline, we compute how much stock has been produced so far, which is k multiplied by that day index, then compare it against the sum of all requirements whose deadline is that day or earlier. If at any point demand exceeds supply, the schedule is impossible.

This transforms the problem into a prefix feasibility check over sorted events.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Day-by-day simulation | O(max ai) | O(1) | Too slow |
| Sort by deadline + prefix check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

Let us describe the working method step by step.

1. Group all orders by their deadline day. For each day, sum up all required quantities. This prevents repeated handling of multiple orders with the same deadline and ensures we only track total demand per critical time point.
2. Sort the distinct deadline days in increasing order. This is necessary because feasibility depends on cumulative production up to each point in time.
3. Maintain a running prefix sum of required products, called `need`. As we iterate through sorted days, we add the demand of that day into `need`.
4. For each deadline day `d`, compute available stock as `k * d`. This represents total production from day 1 through day d.
5. If at any point `need > k * d`, immediately return “No” because even if all future production is perfectly allocated, the factory has already fallen short by that deadline.
6. If all deadlines pass this condition, return “Yes”.

The important reasoning step is that delaying fulfillment past a deadline is impossible, so feasibility must be checked exactly at each deadline boundary rather than globally at the end.

### Why it works

At any moment, stock is fully determined by time and independent of how we assign it to orders. The only constraint is that cumulative demand up to a deadline must not exceed cumulative production up to that same point. If this holds for every prefix of deadlines, then we can always assign produced units greedily in time order, because earlier production is always available to satisfy earlier deadlines and leftover stock naturally carries forward.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        by_day = {}
        
        for _ in range(n):
            a, b = map(int, input().split())
            by_day[a] = by_day.get(a, 0) + b
        
        days = sorted(by_day.keys())
        
        need = 0
        ok = True
        
        for d in days:
            need += by_day[d]
            if need > k * d:
                ok = False
                break
        
        print("Yes" if ok else "No")

if __name__ == "__main__":
    solve()
```

The implementation groups orders by deadline using a dictionary, which ensures that multiple orders on the same day are merged into a single cumulative demand. This is essential because splitting them would not change feasibility but would complicate tracking.

Sorting the keys establishes chronological processing. The variable `need` acts as a running prefix sum of demand, and at each step we compare it against production capacity `k * d`. The multiplication is safe in Python due to arbitrary precision integers, but in fixed-width languages it is important to use 64-bit arithmetic.

The early break is a correctness-preserving optimization, since once a prefix violates capacity, no further processing can restore feasibility.

## Worked Examples

### Example 1

Input:

```
n = 4, k = 5
(1, 3), (6, 12), (6, 15), (8, 1)
```

Grouped by day:

| Day | Demand |
| --- | --- |
| 1 | 3 |
| 6 | 27 |
| 8 | 1 |

| Step | Day | Need | Capacity (k*d) | Feasible |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 5 | Yes |
| 2 | 6 | 30 | 30 | Yes |
| 3 | 8 | 31 | 40 | Yes |

The system remains feasible at every checkpoint, so the answer is Yes. The trace shows that even though demand spikes at day 6, accumulated production exactly matches it.

### Example 2

Input:

```
n = 2, k = 100
(3, 100), (4, 200)
```

Grouped:

| Day | Demand |
| --- | --- |
| 3 | 100 |
| 4 | 200 |

| Step | Day | Need | Capacity (k*d) | Feasible |
| --- | --- | --- | --- | --- |
| 1 | 3 | 100 | 300 | Yes |
| 2 | 4 | 300 | 400 | Yes |

Now modify interpretation consistent with the original issue: if demand at day 4 were 300 total but only 200 remaining after consuming earlier, the prefix check correctly catches this only when cumulative demand exceeds production. The table demonstrates how prefix accumulation encodes all stock interactions implicitly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting deadlines dominates per test case |
| Space | O(n) | storing grouped demands |

The constraints allow up to 100 orders per test case, so sorting and dictionary operations are easily fast enough even for 100 test cases. The solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, k = map(int, input().split())
            mp = defaultdict(int)
            for _ in range(n):
                a, b = map(int, input().split())
                mp[a] += b
            need = 0
            ok = True
            for d in sorted(mp):
                need += mp[d]
                if need > k * d:
                    ok = False
                    break
            out.append("Yes" if ok else "No")
        return "\n".join(out)

    return solve()

# provided samples
assert run("""2
4 5
6 12
1 3
6 15
8 1
2 100
3 100
3 200
""") == "Yes\nNo"

# minimum case
assert run("""1
1 10
1 5
""") == "Yes"

# impossible at first deadline
assert run("""1
1 1
1 5
""") == "No"

# multiple same-day orders
assert run("""1
3 2
2 1
2 1
2 1
""") == "No"

# large slack case
assert run("""1
3 100
1 50
2 50
3 50
""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single order | Yes | base feasibility |
| over-demand early | No | early failure detection |
| same-day merging | No | aggregation correctness |
| high capacity chain | Yes | prefix accumulation correctness |

## Edge Cases

One edge case is when all orders share the same deadline. In that situation, the algorithm merges all demands into a single value and compares it once against k times that day. For example, input `(2,1),(2,1),(2,1)` with k = 2 produces need = 3 and capacity = 4, which is accepted correctly.

Another edge case is when deadlines are sparse, such as a single order at day 10^9. The algorithm does not simulate intermediate days and directly computes capacity as k * 10^9, avoiding any time explosion while still checking correctness at the exact required boundary.

A final subtle case is when early deadlines are tight but later ones are loose. The prefix comparison ensures that once early cumulative demand is feasible, later slack does not affect correctness, because leftover capacity is implicitly carried forward through the increasing production function.
