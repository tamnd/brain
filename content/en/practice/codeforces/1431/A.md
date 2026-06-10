---
title: "CF 1431A - Selling Hamburgers"
description: "We are asked to find the optimal price for selling hamburgers to a set of customers, each with a specific amount of money. Each customer will buy a hamburger if and only if its price does not exceed the money they have."
date: "2026-06-11T05:05:11+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 1431
codeforces_index: "A"
codeforces_contest_name: "Kotlin Heroes 5: ICPC Round"
rating: 800
weight: 1431
solve_time_s: 77
verified: true
draft: false
---

[CF 1431A - Selling Hamburgers](https://codeforces.com/problemset/problem/1431/A)

**Rating:** 800  
**Tags:** *special  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find the optimal price for selling hamburgers to a set of customers, each with a specific amount of money. Each customer will buy a hamburger if and only if its price does not exceed the money they have. The goal is to maximize the total coins collected by the cafeteria. Conceptually, we are choosing a price $m$, and the revenue is $m$ times the number of customers whose money is at least $m$.

The inputs are multiple test cases. Each test case consists of the number of customers $n$ and an array $a$ of their available coins. Each $a_i$ can be as large as $10^{12}$, but $n$ is only up to 100. The low $n$ allows us to consider algorithms that scale with $n^2$ or even $n \log n$ comfortably. However, the potentially huge coin values mean that any approach relying on iterating through all possible prices up to $10^{12}$ is infeasible.

Edge cases arise when all customers have the same coins, when one customer has far more money than the rest, or when multiple customers can afford a very high price but setting it slightly lower would increase total revenue. For instance, if all customers have 1 coin, setting the price higher than 1 earns nothing. If customers have coins `[1, 1000000000000]`, the optimal price is not the maximum, because selling at 1 would allow two hamburgers to be sold instead of only one at the maximum.

## Approaches

The brute-force method is to consider every integer price from 1 up to the maximum customer coin and compute the revenue for each. For each price, we would iterate over all customers to count how many would buy at that price and multiply by the price. This is correct because it exhaustively tests all possibilities, but it is far too slow. Even for $n = 100$, if the largest coin is $10^{12}$, iterating over all prices is infeasible.

The key observation that allows optimization is that the only candidate prices that could yield maximum revenue are the prices equal to some customer’s coin. This is because increasing the price beyond any customer’s coins immediately reduces the number of buyers without increasing the price above a buyer’s limit, and any price between two customers’ coins does not change the set of buyers. Therefore, we only need to consider prices $m \in a$.

Once we sort the array of coins, we can compute revenue for each candidate price efficiently. If we consider price $a[i]$ in a sorted array, the number of customers who can pay at least $a[i]$ is $n - i$. The revenue is simply $a[i] \cdot (n - i)$. Iterating over this sorted array yields the maximum revenue in $O(n \log n)$ time due to sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * max(a_i)) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$ and the array of customer coins $a$. Reading all inputs first is standard practice for competitive programming and ensures consistent I/O handling.
2. Sort the array $a$ in non-decreasing order. Sorting ensures that for each price $a[i]$, the number of buyers who can afford it is $n - i$.
3. Initialize a variable to track the maximum revenue, $\text{max\_revenue} = 0$.
4. Iterate through the sorted array with index $i$. For each coin $a[i]$, calculate the potential revenue as $\text{revenue} = a[i] \cdot (n - i)$.
5. Update $\text{max\_revenue}$ if the calculated revenue is greater than the current maximum.
6. After processing all candidate prices, output $\text{max\_revenue}$.

Why it works: the invariant is that the revenue for any price not equal to a customer coin cannot exceed the revenue at some customer coin. Sorting guarantees that $n - i$ correctly counts the number of buyers, so each revenue computation considers all possible valid subsets of buyers for the given price.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    max_revenue = 0
    for i in range(n):
        revenue = a[i] * (n - i)
        if revenue > max_revenue:
            max_revenue = revenue
    print(max_revenue)
```

The code first reads the number of test cases. Sorting the coins array ensures we can efficiently calculate the number of customers who can pay a given price. Iterating through the sorted array, we compute the revenue as price times the number of buyers. Updating the maximum revenue at each step guarantees we track the best achievable revenue. Off-by-one errors are avoided by carefully using $n - i$, which counts all buyers from index $i$ to the end.

## Worked Examples

### Sample 1

Input coins: `[1, 1, 1]`. Sorted: `[1, 1, 1]`.

| i | a[i] | n-i | revenue |
| --- | --- | --- | --- |
| 0 | 1 | 3 | 3 |
| 1 | 1 | 2 | 2 |
| 2 | 1 | 1 | 1 |

The maximum revenue is 3.

### Sample 2

Input coins: `[4, 1, 1]`. Sorted: `[1, 1, 4]`.

| i | a[i] | n-i | revenue |
| --- | --- | --- | --- |
| 0 | 1 | 3 | 3 |
| 1 | 1 | 2 | 2 |
| 2 | 4 | 1 | 4 |

The maximum revenue is 4. Here, choosing the highest coin yields the optimal revenue because fewer customers buy, but the higher price compensates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates. Iteration over the array is linear. |
| Space | O(n) | We store the array of coins for each test case. |

Given $n \le 100$ and $t \le 100$, the solution handles up to 10,000 elements overall efficiently. Large coin values do not affect the iteration count since we do not enumerate all possible prices.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        max_revenue = 0
        for i in range(n):
            revenue = a[i] * (n - i)
            if revenue > max_revenue:
                max_revenue = revenue
        print(max_revenue)
    return output.getvalue().strip()

# Provided samples
assert run("6\n3\n1 1 1\n3\n4 1 1\n3\n2 4 2\n8\n1 2 3 4 5 6 7 8\n1\n1000000000000\n3\n1000000000000 999999999999 1\n") == "3\n4\n6\n20\n1000000000000\n1999999999998"

# Custom cases
assert run("1\n1\n1\n") == "1", "single customer"
assert run("1\n5\n5 5 5 5 5\n") == "25", "all equal coins"
assert run("1\n3\n1 1000000000000 2\n") == "2000000000000", "two high-value buyers"
assert run("1\n4\n1 2 3 4\n") == "8", "incremental coins"
assert run("1\n2\n1 1000000000000\n") == "1000000000000", "high discrepancy"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1\n` | `1` | Minimum-size input |
| `1\n5\n5 5 5 5 5\n` | `25` | All-equal coins, optimal price equals coin value |
| `1\n3\n1 1000000000000 2\n` | `2000000000000` | Multiple buyers, ensure maximum revenue chosen |
| `1\n4\n1 2 3 4\n` | `8` | Incremental coins, check intermediate price selection |
| `1\n2\n1 1000000000000\n` | `1000000000000` | Large discrepancy, single expensive buyer dominates |

## Edge Cases

For a single customer with a huge coin, the algorithm correctly selects that coin as the price. Input: `[1000000000000
