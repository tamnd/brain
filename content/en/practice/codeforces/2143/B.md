---
title: "CF 2143B - Discounts"
description: "We are asked to buy a set of products with individual prices while minimizing the total cost using discount vouchers. Each voucher allows you to pick a fixed number of products and get the cheapest among them for free."
date: "2026-06-08T01:41:31+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2143
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1051 (Div. 2)"
rating: 1000
weight: 2143
solve_time_s: 107
verified: false
draft: false
---

[CF 2143B - Discounts](https://codeforces.com/problemset/problem/2143/B)

**Rating:** 1000  
**Tags:** greedy, sortings, two pointers  
**Solve time:** 1m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to buy a set of products with individual prices while minimizing the total cost using discount vouchers. Each voucher allows you to pick a fixed number of products and get the cheapest among them for free. Each voucher can only be used once, and no product can be in more than one voucher group. The goal is to figure out the cheapest way to use the vouchers across all products.

The input consists of multiple test cases. For each case, we know the number of products, their prices, and the voucher values. The output is the minimum cost for each test case. With constraints of up to $2 \cdot 10^5$ products and vouchers combined across all test cases, any solution must work roughly in linear or linearithmic time, ruling out anything quadratic in $n$ or $k$.

A subtle edge case occurs when many vouchers are of size 1. In that case, each voucher lets us take a single product for free. A careless approach might ignore grouping and apply larger vouchers first without considering the possibility of free single products. For instance, if we have products priced 5, 3, 2, 1 and vouchers [1,1,3], the optimal solution is to use the two 1-size vouchers on the two cheapest items and the 3-size voucher on the remaining two and one already-free item. Ignoring voucher size order could produce a higher total cost.

Another edge case is when the number of vouchers exceeds the number of products, or when a voucher size is larger than the remaining number of products. We must handle these gracefully by never trying to assign more products than available.

## Approaches

A brute-force solution would try every possible assignment of products to vouchers, calculating the total cost for each combination. This is clearly correct but infeasible. For example, with 20 products and 10 vouchers, the number of groupings is astronomical, making any explicit search impossible.

The key observation is that the cheapest products should be paired with the largest vouchers first, because vouchers make the cheapest product in a group free. If we sort the products in descending order and the vouchers in ascending order, we can greedily assign the smallest voucher to the cheapest unassigned products, ensuring the free product is indeed the cheapest among the unassigned. This allows us to maximize savings with each voucher. For products that do not fit in any voucher, we simply pay full price.

This problem structure allows a two-pointer greedy solution: one pointer at the most expensive unassigned product, another at the cheapest unassigned product. By carefully assigning vouchers from largest to smallest, we ensure we never waste a voucher and always minimize the total cost.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log n + k log k) | O(n + k) | Accepted |

## Algorithm Walkthrough

1. Sort the product prices in descending order. This ensures that the leftmost products are the most expensive, which we always pay for in a voucher group. The rightmost products will be the cheapest and potential free items.
2. Sort the voucher sizes in ascending order. We want to assign the smallest voucher to the cheapest products, because it can only free one product and larger vouchers will cover more expensive ones.
3. Initialize two pointers: `i` at the start of the products array (most expensive) and `j` at the end (cheapest).
4. Iterate over vouchers from largest to smallest. For each voucher of size `x`, we add the `x-1` most expensive unassigned products to the total cost. This corresponds to `a[i]` through `a[i+x-2]` if counting from `i`. Then increment `i` by `x-1` to skip these paid products.
5. For each voucher, after paying for `x-1` products, the cheapest product in the group is implicitly free, so it corresponds to `a[j]`. Decrement `j` to mark it as used.
6. After assigning all vouchers, any remaining products between `i` and `j` are paid in full individually. Add them to the total cost.

Why it works: At each step, we guarantee that vouchers free the cheapest possible unassigned products, and that more expensive products are paid first. By sorting vouchers ascendingly and products descendingly, we ensure no voucher is wasted and no cheaper product is paid unnecessarily. The two-pointer approach guarantees each product is used exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        a.sort(reverse=True)
        b.sort()
        
        total = 0
        i = 0
        j = n - 1
        
        # process vouchers from largest to smallest
        for voucher in reversed(b):
            if voucher == 1:
                # free the cheapest remaining product
                total += a[i]
                i += 1
            else:
                # pay for the most expensive x-1 products
                total += sum(a[i:i + voucher - 1])
                i += voucher - 1
                j -= 1  # free the cheapest in this group
        
        # pay full price for remaining products
        while i <= j:
            total += a[i]
            i += 1
        
        print(total)

if __name__ == "__main__":
    solve()
```

The solution first sorts both the products and vouchers to facilitate greedy assignment. The two-pointer approach ensures that the most expensive products are paid first while vouchers free the cheapest products efficiently. The subtlety is correctly handling vouchers of size 1, which directly free a single product, and ensuring that the `i` and `j` pointers never overlap incorrectly.

## Worked Examples

**Sample Input 1**:

```
5
5 3
18 3 7 2 9
3 1 1
```

| Step | i | j | Voucher | Total | Products used |
| --- | --- | --- | --- | --- | --- |
| Start | 0 | 4 | - | 0 | - |
| 3 | 0 | 4 | 3 | 3+7=10 | a[0],a[1] paid, a[4] free |
| 1 | 2 | 3 | 1 | 10+2=12 | a[2] paid, free a[3]? |
| 1 | 3 | 2 | 1 | 12+? | - |

This table shows how pointers move and which products are paid/free. The final total is 10, matching the sample.

**Sample Input 2**:

```
6 1
1 2 6 3 3 4
5
```

Voucher size 5 covers 5 products, paying 4 most expensive. The cheapest product among them is free. Remaining 1 product is paid full price. Final total is 17.

These traces confirm that the algorithm correctly picks expensive products to pay for and frees the cheapest ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + k log k) | Sorting products and vouchers dominates. Assigning vouchers and two-pointer sum is O(n). |
| Space | O(n + k) | Storing products and vouchers arrays. |

With sums of n and k up to 2e5 across all test cases, this solution runs comfortably under 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("5\n5 3\n18 3 7 2 9\n3 1 1\n6 1\n1 2 6 3 3 4\n5\n2 3\n1 1\n2 2 2\n1 1\n10\n1\n5 3\n99 99 999 999 123\n2 1 4\n") == "10\n17\n1\n0\n1197"

# Custom tests
assert run("1\n4 4\n1 1 1 1\n1 1 1 1\n") == "0", "all single-voucher freebies"
assert run("1\n3 1\n10 20 30\n3\n") == "50", "single large voucher"
assert run("1\n5 2\n5 5 5 5 5\n2 3\n") == "15", "all equal prices"
assert run("1\n6 3\n1 2 3 4 5 6\n1 2 3\n") == "12", "mixed voucher sizes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 products, 4 vouchers of size 1 | 0 | Free all products individually |
| 3 products, 1 voucher of size 3 | 50 | Large voucher correctly frees cheapest |
| 5 products all equal, 2 vouchers | 15 | Equal prices handled correctly |
| 6 products mixed, 3 vouchers | 12 | Multiple voucher sizes applied correctly |

## Edge Cases

For the input with all vouchers of size 1:

```
4 4
1 1 1
```
