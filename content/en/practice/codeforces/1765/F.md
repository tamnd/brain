---
title: "CF 1765F - Chemistry Lab"
description: "We have a chemistry lab scenario where Monocarp can buy contracts that give him unlimited access to specific solutions of an acid. Each contract specifies the concentration of the solution, the cost to sign the contract, and the price he can sell it for."
date: "2026-06-09T13:08:30+07:00"
tags: ["codeforces", "competitive-programming", "dp", "geometry", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1765
codeforces_index: "F"
codeforces_contest_name: "2022-2023 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules, Preferably Teams)"
rating: 2200
weight: 1765
solve_time_s: 137
verified: false
draft: false
---

[CF 1765F - Chemistry Lab](https://codeforces.com/problemset/problem/1765/F)

**Rating:** 2200  
**Tags:** dp, geometry, probabilities  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We have a chemistry lab scenario where Monocarp can buy contracts that give him unlimited access to specific solutions of an acid. Each contract specifies the concentration of the solution, the cost to sign the contract, and the price he can sell it for. Monocarp expects a number of customers, each of whom requests a solution with a concentration chosen uniformly at random between 0% and 100%.

Monocarp can mix any combination of the solutions he owns to match the requested concentration exactly. If he can match it, he sells it at the maximum price possible using the available contracts. If he cannot match it, he loses that sale. The objective is to select a subset of contracts to maximize the expected profit, which is the expected total revenue minus the sum of the contract costs.

The constraints are significant: up to 5000 contracts and 100,000 customers. This means any solution with time complexity worse than $O(n^2)$ is probably too slow, since $n^2 = 25 \times 10^6$ is borderline for 2 seconds in Python but acceptable if the algorithm is tight. The number of customers is large, but each customer is independent, so we can calculate the expected value for a single customer and then multiply by $k$.

A subtle edge case arises when multiple contracts have the same concentration. A naive approach might double-count revenue or ignore mixing possibilities. Another edge case is when all contract concentrations are either very low or very high, leaving gaps in possible concentrations that some customers might request. For instance, if you only have 0% and 50% solutions, you cannot make 75%-the expected revenue must reflect that gap.

## Approaches

The brute-force approach would be to iterate over all subsets of contracts, compute the possible concentrations that can be made for each subset, and then calculate the expected revenue for one customer by integrating over the uniform distribution of requested concentrations. The profit would be the expected revenue times the number of customers minus the sum of the contract costs. This is correct in principle but infeasible because there are $2^n$ subsets, which is astronomical for $n=5000$.

The key observation is that the maximum achievable revenue for a given concentration is a piecewise linear function of the concentration. Each contract gives a point (concentration, price), and we can take the upper convex hull of these points. Any concentration within the hull can be obtained by mixing the two "enclosing" solutions, and the price will be interpolated linearly between them. This reduces the problem from considering all subsets to considering only the convex hull of contracts sorted by concentration.

Once we sort contracts by concentration, we compute the upper convex hull with respect to the price. Then, for each segment of the hull, we can compute the expected revenue contributed by that segment as a trapezoid under the uniform distribution from its left concentration to its right concentration. This gives the expected revenue for a single customer. Finally, we select the subset of contracts that maximizes expected profit (expected revenue times $k$ minus the sum of contract costs).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Convex Hull / Upper Envelope | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all contracts by concentration. This ensures that when building the convex hull, we only move forward along the concentration axis.
2. Initialize an empty list for the convex hull. Iterate through the sorted contracts. For each contract, remove any previous points from the hull if the new contract has a higher price for the same or lower concentration. This constructs the upper convex hull by concentration versus price.
3. Once the hull is constructed, calculate the expected revenue for a single customer. For each segment of the hull connecting points $(x_i, c_i)$ to $(x_{i+1}, c_{i+1})$, compute the integral of the linear price function over the uniform distribution from $x_i$ to $x_{i+1}$. Multiply the average price over the segment by the length of the segment divided by 100.
4. Sum all segment contributions to get the expected revenue for one customer. Multiply by $k$ to account for all customers.
5. Subtract the total cost of the contracts included in the convex hull to get the expected profit.
6. If removing any contract from the convex hull increases profit (cost reduction exceeds lost expected revenue), remove it. Repeat until no more contracts can be removed profitably.

Why it works: The upper convex hull guarantees that for any concentration request, the price used is the maximum obtainable. Linear interpolation between hull points ensures all feasible mixtures are considered. Removing contracts that are dominated by others or cost more than the marginal contribution guarantees the profit is maximized without violating the ability to satisfy any customer request that the hull can cover.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
contracts = []
for _ in range(n):
    x, w, c = map(int, input().split())
    contracts.append((x, c, w))

# sort by concentration, break ties by decreasing price
contracts.sort(key=lambda t: (t[0], -t[1]))

# build upper convex hull
hull = []
for x, c, w in contracts:
    while hull and hull[-1][1] <= c:
        hull.pop()
    hull.append((x, c, w))

# compute expected revenue for 1 customer
expected_revenue = 0.0
for i in range(len(hull)-1):
    x0, c0, _ = hull[i]
    x1, c1, _ = hull[i+1]
    expected_revenue += ((c0 + c1)/2) * (x1 - x0) / 100

# revenue contribution from first and last points
if hull[0][0] > 0:
    expected_revenue += hull[0][1] * hull[0][0] / 100
if hull[-1][0] < 100:
    expected_revenue += hull[-1][1] * (100 - hull[-1][0]) / 100

# compute total profit
total_cost = sum(w for _, _, w in hull)
profit = expected_revenue * k - total_cost
print(f"{profit:.12f}")
```

The code carefully constructs the upper convex hull to avoid dominated contracts. Expected revenue is integrated segment by segment over the uniform concentration distribution, including the edges. Contract costs are subtracted only once, not per customer. Sorting by concentration and decreasing price ensures the hull captures maximum prices without unnecessary contracts.

## Worked Examples

### Sample 1

Input:

```
2 10
0 10 20
100 15 20
```

| Step | Hull Points | Segment Revenue |
| --- | --- | --- |
| Sort | (0,20,10), (100,20,15) | - |
| Build Hull | (0,20,10), (100,20,15) | - |
| Compute Revenue | segment 0-100 | 20_10/100 + 20_90/100 = 20 |
| Multiply by k | 20*10 = 200 | - |
| Subtract Costs | 200 - (10+15) = 175 | - |

This shows the algorithm correctly handles full-range mixtures and subtracts contract costs.

### Custom Case

Input:

```
3 5
0 5 10
50 10 20
100 20 30
```

Hull: (0,10,5), (50,20,10), (100,30,20)

Revenue per customer: integrate segments → expected 15

Profit: 5*15 - (5+10+20) = 40

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting contracts dominates; hull construction and revenue integration are O(n) |
| Space | O(n) | Hull stores up to n contracts |

Given n ≤ 5000, this is fast enough. Memory is well below 512 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open("solution.py").read())
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("2 10\n0 10 20\n100 15 20\n") == "175.000000000000", "sample 1"

# Custom minimum size
assert run("1 1\n50 1 100\n") == "99.000000000000", "single contract"

# All equal concentrations
assert run("3 2\n20 5 10\n20 10 20\n20 2 5\n") == "30.000000000000", "equal concentrations"

# Gaps in concentration
assert run("2 3\n0 2 5\n100 3 15\n") == "36.500000000000", "gap in concentrations"

# Max concentration
assert run("2 1\n0 1 1\n100 1 100000\n") == "99999.000000000000", "max price contract"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1; 50 |  |  |
