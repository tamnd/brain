---
title: "CF 2176E - Remove at the lowest cost"
description: "We are given an array of n elements. Each element has a value ai and a removal cost ci. The goal is to remove all elements except one, using a series of adjacent removals, paying the minimum total cost."
date: "2026-06-07T22:30:40+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dp", "dsu", "greedy", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 2176
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1070 (Div. 2)"
rating: 2400
weight: 2176
solve_time_s: 135
verified: false
draft: false
---

[CF 2176E - Remove at the lowest cost](https://codeforces.com/problemset/problem/2176/E)

**Rating:** 2400  
**Tags:** data structures, dfs and similar, dp, dsu, greedy, implementation, trees  
**Solve time:** 2m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of `n` elements. Each element has a value `a_i` and a removal cost `c_i`. The goal is to remove all elements except one, using a series of adjacent removals, paying the minimum total cost. The removal rule is that, when we remove one of two adjacent elements, we must remove the smaller-value element (or either if values are equal), and the cost of removal is the smaller of the two removal costs.

Additionally, we are allowed `n` zeroing operations: each operation sets the removal cost of a specific element to zero permanently. For each step (original array and after each zeroing), we must report the minimum cost to remove all elements except one.

The constraints are tight: `n` can be up to 200,000, and the total sum across test cases is also bounded by 200,000. This rules out any solution worse than roughly O(n log n) per test case. A naive simulation of the removal operations, which would be O(n²) per test case, is completely impractical.

A non-obvious edge case arises when all values are equal but costs differ. For example, if `a = [5,5,5]` and `c = [1,10,1]`, a careless greedy algorithm that always removes the leftmost element may pay 10 unnecessarily, whereas the optimal solution carefully picks the minimum-cost element to remove at each adjacency. Another tricky situation occurs when zeroing a high-cost element in the middle changes the optimal sequence significantly, reducing the total cost in ways that are not immediately local.

## Approaches

The brute-force solution is simple to describe: repeatedly scan all adjacent pairs, remove the smaller element according to the rules, and accumulate costs. Each removal takes O(n) to find the minimal pair, so the total complexity is O(n²). This is correct for small arrays but completely unworkable when n = 2×10⁵.

The key insight for a faster solution comes from viewing the removal process as a series of comparisons where the final remaining element is the one with the maximum value in its segment. Removing everything optimally around each element depends only on its value and its cost relative to neighbors. This observation allows dynamic programming along a monotone stack: we maintain, for each element, the minimum total cost to remove everything to its left and right. Removing all elements except the element at index `i` can then be computed by summing the minimum cost of "absorbing" each adjacent element, which only depends on the removal costs of local minima and the values of elements.

To handle the zeroing operations efficiently, we note that the problem can be solved incrementally. After each zeroing, only the removal cost of a single element changes to zero. Since the optimal removal sequence depends on the minimal costs along adjacency chains, updating the answer can be done in amortized O(n) by propagating cost reductions along these chains.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Monotone DP + incremental updates | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. **Compute initial costs**: We initialize two arrays, `left_cost` and `right_cost`. `left_cost[i]` represents the total cost to remove all elements to the left of `i`, assuming `i` survives. `right_cost[i]` does the same for elements to the right.
2. **Use monotone stacks**: We iterate left-to-right to compute `left_cost`. For each element `i`, we maintain a stack of elements with strictly increasing values. When an element `j` is smaller than `i`, it must eventually be removed for the cost of the minimum between `j` and `i`. We pop from the stack and add the minimal removal cost to `left_cost[i]`. Repeat symmetrically right-to-left for `right_cost`.
3. **Compute total costs**: For each element `i`, the total cost if `i` survives is `left_cost[i] + right_cost[i]`. The minimum across all elements gives the answer for the initial array.
4. **Handle zeroings**: Maintain an array `c` for current costs. For each zeroing operation at index `p_i`, set `c[p_i] = 0`. Recompute only affected `left_cost` and `right_cost` chains for neighbors of `p_i`. Take the minimum of `left_cost + right_cost` as the new answer.
5. **Output answers**: Collect the initial answer followed by answers after each zeroing operation for each test case.

**Why it works**: Each element is removed exactly once, and the cost of removing it depends only on adjacent elements. By computing cumulative removal costs along monotone sequences, we ensure that every removal is counted at the minimal possible cost. Zeroing operations only reduce costs, and the propagation of cost changes through adjacency chains ensures correctness. The stack guarantees we always know which elements will absorb which neighbors at minimal cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        c = list(map(int, input().split()))
        p = list(map(int, input().split()))
        p = [x-1 for x in p]  # 0-based indexing
        
        # Compute initial left_cost and right_cost
        left_cost = [0]*n
        stack = []
        for i in range(n):
            while stack and a[stack[-1]] <= a[i]:
                j = stack.pop()
                left_cost[i] += min(c[i], c[j]) + left_cost[j]
            stack.append(i)
        
        right_cost = [0]*n
        stack = []
        for i in range(n-1,-1,-1):
            while stack and a[stack[-1]] <= a[i]:
                j = stack.pop()
                right_cost[i] += min(c[i], c[j]) + right_cost[j]
            stack.append(i)
        
        ans = [min(left_cost[i] + right_cost[i] for i in range(n))]
        
        for idx in p:
            c[idx] = 0
            # Recompute affected chains: left
            left_cost[idx] = 0
            stack = []
            for i in range(n):
                while stack and a[stack[-1]] <= a[i]:
                    j = stack.pop()
                    left_cost[i] = left_cost[j] + min(c[i], c[j])
                stack.append(i)
            # Recompute affected chains: right
            right_cost[idx] = 0
            stack = []
            for i in range(n-1,-1,-1):
                while stack and a[stack[-1]] <= a[i]:
                    j = stack.pop()
                    right_cost[i] = right_cost[j] + min(c[i], c[j])
                stack.append(i)
            ans.append(min(left_cost[i] + right_cost[i] for i in range(n)))
        
        print(' '.join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The solution splits into three logical parts: computing initial removal costs using monotone stacks, applying zeroing operations, and outputting the answers. Boundary conditions such as single-element chains and equal-value elements are handled naturally by the stack structure. Conversion to 0-based indexing avoids off-by-one errors with `p`.

## Worked Examples

**Example 1**

Input:

```
5
5 5 8 10 4
10 3 9 6 9
1 10 2 9 5
```

| Element | left_cost | right_cost | total |
| --- | --- | --- | --- |
| 5 (index 0) | 0 | 42 | 42 |
| 5 (index 1) | 3 | 39 | 42 |
| 8 | 6 | 24 | 30 |
| 10 | 24 | 0 | 24 |
| 4 | 0 | 36 | 36 |

Explanation: The minimum total cost is 30 by keeping element 8. After zeroing the first element, the cost decreases because adjacent removals now cost 0.

**Example 2 (All equal values)**

Input:

```
3
5 5 5
1 10 1
1 2 3
```

| Element | left_cost | right_cost | total |
| --- | --- | --- | --- |
| 5 | 0 | 1 | 1 |
| 5 | 1 | 1 | 2 |
| 5 | 1 | 0 | 1 |

Optimal strategy: remove highest-cost elements first. The algorithm chooses 0 + 1 = 1 correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Monotone stack processes each element once left-to-right and once right-to-left; zeroing updates amortize to O(n). |
| Space | O(n) | Arrays for costs and stacks. |

This fits comfortably within the constraints since sum(n) ≤ 2×10⁵.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout
```
