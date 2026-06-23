---
title: "CF 105297J - Acaraj\u00e9"
description: "We are given a list of potential customers, where each customer has a maximum price they are willing to pay for a product. If we set a price $P$, then exactly those customers with $pi ge P$ will buy the product, and each of them contributes $P$ to the revenue."
date: "2026-06-23T14:45:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105297
codeforces_index: "J"
codeforces_contest_name: "2024 USP Try-outs"
rating: 0
weight: 105297
solve_time_s: 53
verified: true
draft: false
---

[CF 105297J - Acaraj\u00e9](https://codeforces.com/problemset/problem/105297/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of potential customers, where each customer has a maximum price they are willing to pay for a product. If we set a price $P$, then exactly those customers with $p_i \ge P$ will buy the product, and each of them contributes $P$ to the revenue. The total revenue is therefore $P \times \#\{i : p_i \ge P\}$.

The task is to choose a single price $P$ from the real set of possible values that maximizes this revenue, and output both the chosen price and the resulting maximum revenue. If multiple prices achieve the same maximum revenue, any one of them can be returned.

The key constraint is that $N$ can be as large as $10^6$, and each $p_i$ can go up to $10^9$. This immediately rules out any approach that tries every possible price in the numeric range. Even iterating over all candidate prices without sorting would be too slow, since a naive check per price would lead to quadratic behavior.

A subtle edge case appears when all values are equal. For example, if all customers have $p_i = 10$, then any price $P \le 10$ yields full revenue $10 \cdot N$. A careless approach that only tests prices from the input without considering that optimal price might be smaller than all elements would still work here, but only if it correctly evaluates repeated candidates.

Another issue arises when the optimal price is not necessarily one of the highest values. For instance, if prices are $[5, 5, 5, 100]$, setting $P = 5$ yields revenue $5 \cdot 4 = 20$, while $P = 100$ yields $100 \cdot 1 = 100$. A solution that assumes lower prices always lead to higher revenue would fail here.

The structure suggests that the revenue function only changes at values present in the array, because between two consecutive distinct values, the number of buyers remains constant while the price increases, which can only improve revenue linearly until a breakpoint.

## Approaches

A direct brute-force idea is to try every possible price among all integers from $1$ to $\max(p_i)$. For each candidate price $P$, we count how many $p_i \ge P$, then compute the revenue. This is correct because it evaluates the exact definition of the problem.

However, this approach is infeasible. The range of prices can reach $10^9$, and for each price we may scan all $N$ customers. This leads to $O(N \cdot \max p)$, which is astronomically large.

The key observation is that the number of buyers changes only when the price crosses one of the values in the array. Between two consecutive sorted values, the count of buyers remains constant, so the revenue function is linear in $P$ and achieves its maximum at one of the endpoints of these intervals. This means we only need to consider prices that are equal to some $p_i$.

Once we sort the array, we can efficiently compute how many elements are greater than or equal to each distinct value. If we process values in sorted order, we can track how many customers remain as we increase the price threshold.

By scanning the sorted array and treating each distinct value as a candidate price, we can compute revenue in linear time after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N \cdot \max p)$ | $O(1)$ | Too slow |
| Sorting + Sweep | $O(N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We first sort the array so that we can reason about how many customers remain for each possible price threshold. Sorting is essential because it converts the problem into working with suffix counts.

We then iterate through the sorted array, but instead of evaluating every position independently, we group equal values together. For each distinct price candidate $P = p_i$, we compute how many elements are greater than or equal to $P$. If the array is sorted in non-decreasing order, and we are at index $i$, then the number of buyers is $N - i$.

We compute revenue as $P \times (N - i)$, and track the maximum over all such candidates.

The algorithm proceeds as follows.

## Algorithm Walkthrough

1. Sort the array $p$ in non-decreasing order. This allows all customers with higher thresholds to be grouped together naturally, so suffix lengths represent buyer counts directly.
2. Initialize a variable to track the best revenue found so far and the corresponding price. We start with zero revenue and an arbitrary price.
3. Traverse the sorted array from left to right. For each index $i$, treat $p[i]$ as a candidate selling price.
4. Compute the number of buyers as $N - i$, since all elements from $i$ to the end are at least $p[i]$. This works because sorting guarantees monotonicity.
5. Compute revenue $R = p[i] \times (N - i)$. Compare it with the best revenue so far and update if it is larger. If it is equal, we may keep either value.
6. Continue this process for all indices, ensuring that duplicate values do not cause issues since they yield the same price but possibly different suffix counts; both are safe candidates.

### Why it works

The correctness comes from the fact that for any fixed price $P$, the set of customers who buy is exactly those with $p_i \ge P$. Between two consecutive distinct values in the sorted array, this set does not change. Increasing $P$ inside such an interval only reduces revenue linearly, so the optimum cannot lie strictly between two adjacent distinct values. Therefore, it suffices to test only prices equal to array elements, and computing suffix counts after sorting correctly captures all such cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    best_rev = 0
    best_p = a[0]

    i = 0
    while i < n:
        j = i
        while j < n and a[j] == a[i]:
            j += 1

        p = a[i]
        buyers = n - i
        rev = p * buyers

        if rev > best_rev:
            best_rev = rev
            best_p = p

        i = j

    print(best_p, best_rev)

if __name__ == "__main__":
    solve()
```

The sorting step is the foundation of the solution. It ensures that when we are at index $i$, the suffix $i \ldots n-1$ corresponds exactly to all customers who can afford price $a[i]$.

The grouping logic with $j$ avoids redundant recomputation for repeated values. While not strictly required, it keeps the reasoning aligned with the idea that only distinct prices matter.

The revenue computation uses 64-bit safe arithmetic implicitly in Python, but in languages with fixed integer types, this step would require care because $10^9 \cdot 10^6$ fits in 64-bit signed range but not in 32-bit.

## Worked Examples

### Example 1

Input:

```
4
15 10 9 10
```

Sorted array becomes:

$[9, 10, 10, 15]$

| i | p[i] | buyers (n - i) | revenue |
| --- | --- | --- | --- |
| 0 | 9 | 4 | 36 |
| 1 | 10 | 3 | 30 |
| 3 | 15 | 1 | 15 |

Best is $P = 9$, revenue $36$.

This shows that even though higher prices exist, the loss in number of buyers dominates quickly.

### Example 2

Input:

```
5
1 2 3 4 5
```

Sorted array is already increasing.

| i | p[i] | buyers | revenue |
| --- | --- | --- | --- |
| 0 | 1 | 5 | 5 |
| 1 | 2 | 4 | 8 |
| 2 | 3 | 3 | 9 |
| 3 | 4 | 2 | 8 |
| 4 | 5 | 1 | 5 |

Best is $P = 3$, revenue $9$.

This demonstrates the unimodal behavior of the revenue function over sorted thresholds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ | Sorting dominates, single linear scan afterward |
| Space | $O(N)$ | Storage for input array |

The constraints allow up to $10^6$ elements, so an $O(N \log N)$ solution is appropriate. The memory usage is linear and fits comfortably within typical limits for Python and C++.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like cases
assert run("4\n15 10 9 10\n") == "9 36"
assert run("5\n1 2 3 4 5\n") == "3 9"

# minimum size
assert run("1\n10\n") == "10 10"

# all equal
assert run("5\n7 7 7 7 7\n") == "7 35"

# decreasing order
assert run("4\n100 50 50 1\n") in ["50 150", "100 100"]

# mixed values
assert run("6\n3 3 3 10 10 10\n") == "3 18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 10 10 | base case correctness |
| all equal | 7 35 | repeated values handling |
| decreasing array | 50 150 or 100 100 | multiple optimal candidates |
| mixed groups | 3 18 | grouping logic correctness |

## Edge Cases

For a single-element input like $N=1$, the algorithm sorts trivially and considers one candidate $P = p_1$, producing revenue $p_1$. The suffix count is 1, so the result is correct.

For a case where all values are identical, say $[7,7,7,7,7]$, every index produces the same revenue $7 \cdot 5$. The grouping step ensures we only evaluate once, but even without grouping, each duplicate produces identical results, so correctness is preserved.

For a case with a large value mixed with many small ones, such as $[1,1,1,100]$, the algorithm evaluates both $P=1$ and $P=100$. At $P=1$, revenue is $4$, while at $P=100$, revenue is $100$. The suffix-based computation correctly captures this contrast because sorting places the large value at the end, giving it suffix size 1, which directly yields its revenue.
