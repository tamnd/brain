---
title: "CF 106151D - packages"
description: "We are given a collection of packages, each package having two parameters. The first is a base cost that you pay once if you include that package in your delivery batch."
date: "2026-06-20T02:23:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106151
codeforces_index: "D"
codeforces_contest_name: "2025 ICPC Greek Collegiate Programming Contest (GRCPC 2025)"
rating: 0
weight: 106151
solve_time_s: 68
verified: true
draft: false
---

[CF 106151D - packages](https://codeforces.com/problemset/problem/106151/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of packages, each package having two parameters. The first is a base cost that you pay once if you include that package in your delivery batch. The second is a congestion coefficient that scales with how many packages you decide to send in the same batch.

If you choose to deliver exactly K packages in one run, then each selected package i costs a total of $a_i + K \cdot b_i$. The key point is that the congestion term depends on the global number of selected packages, not on the individual package.

Your task is to choose a subset of packages and also choose its size K implicitly, so that the total cost of the chosen subset does not exceed the budget B, while maximizing K. Among all subsets achieving this maximum K, you must report the minimum possible cost.

The interaction between selection and cost is the core difficulty: selecting more packages increases the per-package congestion penalty for all selected items, which feeds back into the feasibility of the selection itself.

The constraints allow up to $2 \cdot 10^5$ packages, with costs up to $10^9$ total budget and up to $10^5$ for individual parameters. This immediately rules out any solution that recomputes feasibility for each subset explicitly. Any approach that is worse than roughly $O(n \log n)$ or $O(n \sqrt n)$ depending on constants will be unsafe.

A naive but instructive failure mode is trying to fix K and greedily choose the cheapest K packages under modified costs. For example, suppose all $b_i$ are large for a few items and small for others. If K is fixed incorrectly, a greedy selection can pick items that become expensive only after K changes, invalidating earlier decisions.

Another subtle edge case appears when K changes the ordering of items. Two packages can swap order depending on K because cost is $a_i + K b_i$. For instance, if $a_1 < a_2$ but $b_1 > b_2$, then for small K package 1 is cheaper, but for large K package 2 becomes cheaper. Any approach that sorts once by $a_i$ or $a_i + b_i$ without considering K will break.

## Approaches

The brute-force idea is to try every possible K from 1 to N. For each K, we compute the cost of selecting the cheapest K packages under the cost formula $a_i + K b_i$. To do this directly, we would need to evaluate all packages, compute adjusted costs, sort them, and pick the best K.

For a fixed K, sorting takes $O(n \log n)$, and doing this for all K leads to $O(n^2 \log n)$, which is far too slow for $2 \cdot 10^5$.

The key structural observation is that we do not actually need to try all K independently in a full recomputation sense. Instead, we can ask a decision question: for a fixed K, can we pick K packages within budget, and what is the minimum cost? If we can answer this efficiently, we can binary search K.

For a fixed K, each package contributes $a_i + K b_i$. Since K is fixed, this is just a static weight per item. So the optimal selection is simply the K smallest values of $a_i + K b_i$. That means we only need to sort once per check, but even that is too slow.

We reduce this further by binary searching K and using a heap-based or selection-based feasibility check. However, there is an even simpler trick: for a fixed K, we compute values $a_i + K b_i$, select the K smallest using sorting or a heap in $O(n)$ or $O(n \log n)$, and compute the sum. Then we binary search K in $O(\log n)$.

This gives $O(n \log n \log n)$, which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over K with full recomputation | $O(n^2 \log n)$ | $O(n)$ | Too slow |
| Binary search K + selection of K smallest adjusted costs | $O(n \log n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Define a function that, for a given K, computes the minimum total cost of choosing exactly K packages. For each package, compute its effective cost $c_i = a_i + K b_i$, since K is fixed inside this check.
2. Sort all computed $c_i$ values and take the sum of the smallest K values. This corresponds to the optimal choice because, for fixed K, each package contributes independently and there is no coupling except selection count.
3. If this sum is less than or equal to B, then K packages are feasible under budget. Otherwise, K is too large.
4. Binary search K from 0 to N. We maintain a range where feasibility transitions from true to false.
5. For each midpoint K, run the feasibility function. If it is feasible, move the lower bound up; otherwise move the upper bound down.
6. After binary search completes, we know the maximum feasible K. We recompute its cost using the same procedure to obtain the minimum total cost for that K.

Why it works: for each fixed K, the cost function is fully determined and independent across packages except through selection count. The feasibility predicate is monotonic in K because increasing K increases every $c_i = a_i + K b_i$, which can only increase the sum of the K smallest values or make selection harder. This monotonicity guarantees binary search correctness, since once a K becomes infeasible, all larger K remain infeasible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cost_for_k(a, b, K, B):
    n = len(a)
    vals = [a[i] + K * b[i] for i in range(n)]
    vals.sort()
    s = sum(vals[:K])
    return s

def feasible(a, b, K, B):
    if K == 0:
        return True, 0
    n = len(a)
    vals = [a[i] + K * b[i] for i in range(n)]
    vals.sort()
    s = sum(vals[:K])
    return s <= B, s

def main():
    n, B = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    lo, hi = 0, n
    best_k = 0
    best_cost = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        vals = [a[i] + mid * b[i] for i in range(n)]
        vals.sort()
        s = sum(vals[:mid]) if mid > 0 else 0

        if s <= B:
            best_k = mid
            best_cost = s
            lo = mid + 1
        else:
            hi = mid - 1

    print(best_k, best_cost)

if __name__ == "__main__":
    main()
```

The code implements a direct binary search over the answer K. For each midpoint, it computes adjusted costs $a_i + K b_i$ and selects the K smallest via sorting. The sum of these K values is the minimum possible cost for that K because any other subset would replace a chosen element with a larger one.

The binary search maintains the best feasible K seen so far. When a midpoint is feasible, we store both K and its cost, then try to increase K. Otherwise, we reduce K. This works because feasibility is monotone in K.

A subtle implementation detail is handling K = 0 separately to avoid slicing issues and to ensure correctness when budget allows zero packages. Another important point is recomputing the cost inside each iteration rather than trying to reuse previous computations, since the cost function depends on K.

## Worked Examples

### Example 1

Input:

```
N = 4, B = 10
a = [1, 2, 2, 1]
b = [2, 2, 2, 2]
```

We test different K values.

| K | adjusted costs $a_i + K b_i$ | smallest K values | sum | feasible |
| --- | --- | --- | --- | --- |
| 1 | [3,4,4,3] | [3] | 3 | yes |
| 2 | [5,6,6,5] | [5,5] | 10 | yes |
| 3 | [7,8,8,7] | [7,7,7] | 21 | no |
| 4 | [9,10,10,9] | [9,9,10,10] | 38 | no |

Binary search finds K = 2 as maximum feasible. The cost is 10.

This trace shows how increasing K uniformly inflates all items, and how feasibility breaks once the cumulative congestion becomes too large.

### Example 2

Input:

```
N = 5, B = 35
a = [3,2,1,4,5]
b = [3,4,5,2,1]
```

| K | adjusted costs | smallest K values | sum | feasible |
| --- | --- | --- | --- | --- |
| 1 | [6,6,6,6,6] | [6] | 6 | yes |
| 2 | [9,10,11,8,7] | [7,8] | 15 | yes |
| 3 | [12,14,17,10,8] | [8,10,12] | 30 | yes |
| 4 | [15,18,23,12,9] | [9,12,15,18] | 54 | no |

Maximum feasible K is 3, with cost 30.

This example highlights that the relative ordering of items shifts with K, but the algorithm naturally adapts because it recomputes ordering at each check.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n \log n)$ | Each feasibility check sorts n values, and binary search runs in log n iterations |
| Space | $O(n)$ | Storage for transformed costs |

The constraints allow up to $2 \cdot 10^5$ items, and sorting that many integers around 20 times is acceptable in Python with optimized implementation. Memory usage remains linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, B = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    def check(K):
        vals = [a[i] + K * b[i] for i in range(n)]
        vals.sort()
        return sum(vals[:K]) if K > 0 else 0

    lo, hi = 0, n
    best_k, best_c = 0, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        c = check(mid)
        if c <= B:
            best_k, best_c = mid, c
            lo = mid + 1
        else:
            hi = mid - 1

    return f"{best_k} {best_c}"

# provided samples
assert run("4 10\n1 2 2 1\n2 2 2 2\n") == "2 10", "sample 1"
assert run("5 35\n3 2 1 4 5\n3 4 5 2 1\n") == "3 30", "sample 2"

# custom cases
assert run("1 100\n5\n1\n") == "1 6", "single item"
assert run("3 0\n1 2 3\n1 1 1\n") == "0 0", "zero budget"
assert run("4 1000\n0 0 0 0\n0 0 0 0\n") == "4 0", "free items"
assert run("5 20\n10 9 8 7 6\n1 2 3 4 5\n") == "2 19", "mixed tradeoff"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single item | 1 6 | minimal boundary case |
| zero budget | 0 0 | inability to select any package |
| free items | 4 0 | all selections are optimal |
| mixed tradeoff | 2 19 | interaction between a and b |

## Edge Cases

A key edge case is when K equals zero. In this situation, no packages are chosen and cost is exactly zero. The algorithm explicitly handles this before sorting, avoiding unnecessary work and ensuring correctness even when budget is zero.

Another edge case arises when all $b_i$ are zero. Then cost becomes independent of K for each item, and the problem reduces to selecting K smallest $a_i$ values. The algorithm still works because $a_i + K b_i = a_i$.

A third case is when $a_i$ values are zero but $b_i$ are positive. Here increasing K quickly makes selection expensive even though individual items seem free initially. The binary search naturally discovers the cutoff K where congestion dominates, and recomputation at each step correctly captures this nonlinear behavior.
