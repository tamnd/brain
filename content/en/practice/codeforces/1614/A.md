---
title: "CF 1614A - Divan and a Store"
description: "Divan wants to buy chocolate bars under three constraints: he only considers bars within a price range [l, r], and he cannot exceed his total budget k."
date: "2026-06-10T06:46:43+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1614
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 757 (Div. 2)"
rating: 800
weight: 1614
solve_time_s: 77
verified: true
draft: false
---

[CF 1614A - Divan and a Store](https://codeforces.com/problemset/problem/1614/A)

**Rating:** 800  
**Tags:** brute force, constructive algorithms, greedy  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

Divan wants to buy chocolate bars under three constraints: he only considers bars within a price range [l, r], and he cannot exceed his total budget k. We are given the prices of n chocolate bars, and for each test case, we need to compute the maximum number of bars he can buy without violating these constraints.

The input provides multiple test cases, each with the number of bars, the lower and upper acceptable prices, Divan's total budget, and the array of chocolate prices. The output for each test case is a single integer representing the maximum count of chocolates Divan can purchase.

The constraints imply that n is at most 100, and prices as well as the budget can be up to 10^9. The small size of n tells us that any approach with complexity roughly O(n log n) or even O(n^2) is acceptable for a single test case. However, since t, the number of test cases, can reach 100, a naive O(n^2) approach could require up to 10^6 operations in the worst case, which is still acceptable given the generous 1-second time limit. What matters more is careful handling of price filtering and the budget constraint.

Non-obvious edge cases include situations where all chocolate bars are too cheap or too expensive, or when the budget is smaller than even the cheapest acceptable bar. For example, if l = 10, r = 20, k = 5, and the prices are [12, 15], the correct answer is 0, since Divan cannot afford any bar. A careless solution might incorrectly pick the cheapest acceptable bar without checking the budget.

Another edge case arises when multiple bars have the same price, potentially filling the budget exactly. For instance, if k = 10 and prices = [5, 5, 5], Divan can buy only two bars, not three. Forgetting to accumulate the cost carefully can lead to overcounting.

## Approaches

A brute-force solution would enumerate all subsets of acceptable chocolate bars and check which subsets fit within the budget. For n = 100, this results in 2^100 subsets, which is astronomically too large. Clearly, this approach is infeasible.

The key observation is that we do not care which combination of bars we pick beyond their price. To maximize the number of bars, we should always pick the cheapest bars first, because buying cheaper bars allows us to include more within the same budget. This reduces the problem to a sorting and greedy selection task: filter bars by price, sort the remaining bars in ascending order, and then iterate through them, accumulating their cost until the budget is exceeded. This approach is both correct and efficient given n ≤ 100.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all subsets) | O(2^n) | O(n) | Too slow |
| Filter + Sort + Greedy | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases t. Loop over each test case.
2. For a test case, read n, l, r, k, and the array of prices a.
3. Filter the array a to keep only prices between l and r inclusive. This ensures we consider only chocolates Divan likes.
4. Sort the filtered array in ascending order. Sorting guarantees we consider cheaper bars first, which maximizes the number of bars we can buy under budget k.
5. Initialize a counter for the number of chocolates bought and a variable for the remaining budget. Iterate through the sorted prices.
6. For each price p, check if p is less than or equal to the remaining budget. If so, subtract p from the budget and increment the counter. If p exceeds the remaining budget, stop iterating because adding any further bars (all more expensive) would exceed the budget.
7. After processing all bars, output the counter as the answer for the test case.

Why it works: At every step, we maintain the invariant that we have spent the minimum possible amount on the maximum number of bars. Because the array is sorted in ascending order, skipping a bar because it exceeds the remaining budget guarantees that no further bar can be included. This greedy approach ensures the maximum number of chocolates is selected without exceeding the budget.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, l, r, k = map(int, input().split())
    prices = list(map(int, input().split()))
    
    # Keep only acceptable chocolates
    valid_prices = [p for p in prices if l <= p <= r]
    
    # Sort ascending to prioritize cheaper chocolates
    valid_prices.sort()
    
    count = 0
    remaining_budget = k
    for price in valid_prices:
        if price <= remaining_budget:
            remaining_budget -= price
            count += 1
        else:
            break
    
    print(count)
```

The code reads all test cases efficiently. Filtering ensures we do not consider unacceptable prices, sorting allows the greedy choice of cheaper bars, and the iteration accumulates chocolates until the budget runs out. Sorting and filtering are straightforward but require attention to the boundaries of l and r inclusive. The iteration must stop as soon as the budget is insufficient, which is a common off-by-one source of errors.

## Worked Examples

### Sample 1

Input:

```
3 1 100 100
50 100 50
```

| Variable | Value after filtering | Value after sorting | Counter progression |
| --- | --- | --- | --- |
| valid_prices | [50, 100, 50] | [50, 50, 100] | count = 0, remaining = 100 |
| Step 1 | p = 50 | - | count = 1, remaining = 50 |
| Step 2 | p = 50 | - | count = 2, remaining = 0 |
| Step 3 | p = 100 | - | exceeds budget, stop |

Output: 2. This confirms the greedy choice of cheapest bars first maximizes count.

### Sample 2

Input:

```
6 3 5 10
1 2 3 4 5 6
```

Filtered valid_prices = [3, 4, 5], sorted ascending = [3, 4, 5]. Iteration:

| Step | Price | Remaining | Count |
| --- | --- | --- | --- |
| 1 | 3 | 10-3=7 | 1 |
| 2 | 4 | 7-4=3 | 2 |
| 3 | 5 | 3 < 5, stop | 2 |

Output: 2. Confirms stopping correctly when the next bar exceeds remaining budget.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n log n) | Filtering is O(n), sorting O(n log n), iterating O(n). For t test cases, multiply by t. |
| Space | O(n) | Storing the filtered list of valid prices. |

With n ≤ 100 and t ≤ 100, t*n log n is at most 100 * 100 * log 100 ≈ 66,000 operations, well within the 1s limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    # Solution code
    t = int(input())
    for _ in range(t):
        n, l, r, k = map(int, input().split())
        prices = list(map(int, input().split()))
        valid_prices = [p for p in prices if l <= p <= r]
        valid_prices.sort()
        count = 0
        remaining_budget = k
        for price in valid_prices:
            if price <= remaining_budget:
                remaining_budget -= price
                count += 1
            else:
                break
        print(count)
    
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("8\n3 1 100 100\n50 100 50\n6 3 5 10\n1 2 3 4 5 6\n6 3 5 21\n1 2 3 4 5 6\n10 50 69 100\n20 30 40 77 1 1 12 4 70 10000\n3 50 80 30\n20 60 70\n10 2 7 100\n2 2 2 2 2 7 7 7 7 7\n4 1000000000 1000000000 1000000000\n1000000000 1000000000 1000000000 1000000000\n1 1 1 1\n1") == "2\n2\n3\n0\n0\n10\n1\n1", "samples"

# Custom edge cases
assert run("1\n5 10 20 5\n12 15 18 19 20") == "0", "budget too small for any"
assert run("1\n5 10 20 50\n12 15 18 19 20") == "4", "maximum bars under budget"
assert run("1\n3 5 5 10\n5 5 5") == "2", "all equal prices, exact budget use"
assert run("1\n1 1 1000000000 1000000000\n100000
```
