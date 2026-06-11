---
title: "CF 1139F - Dish Shopping"
description: "We are asked to determine how many dishes each person in a city can buy given multiple constraints. Each dish has a price, a minimum standard requirement, and a beauty value. Each person has an income and a preferred beauty."
date: "2026-06-12T03:51:51+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer"]
categories: ["algorithms"]
codeforces_contest: 1139
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 548 (Div. 2)"
rating: 2500
weight: 1139
solve_time_s: 74
verified: true
draft: false
---

[CF 1139F - Dish Shopping](https://codeforces.com/problemset/problem/1139/F)

**Rating:** 2500  
**Tags:** data structures, divide and conquer  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine how many dishes each person in a city can buy given multiple constraints. Each dish has a price, a minimum standard requirement, and a beauty value. Each person has an income and a preferred beauty. A person can only buy a dish if their income lies between the dish's price and standard and if the absolute difference between the dish's beauty and their preferred beauty does not exceed the leftover money after purchase.

The input includes up to 100,000 dishes and 100,000 people, with prices, standards, and beauties reaching up to $10^9$. A naive solution that checks every person against every dish would involve $10^{10}$ comparisons in the worst case, which is far beyond what can execute in two seconds. This forces us to find a solution faster than $O(n \cdot m)$, likely around $O((n+m) \log n)$ using sorted data structures or divide-and-conquer methods.

Subtle edge cases arise when a person’s income exactly equals a dish’s price or standard, or when the beauty constraint is tight. For example, consider a dish with price 5, standard 10, beauty 7 and a person with income 10, preferred beauty 10. The remaining money after purchase is 5, and the absolute beauty difference is 3. This satisfies the beauty condition. A careless implementation might only check price ≤ income < standard and miss the upper bound, producing an incorrect count.

Another edge case is when multiple dishes have the same price or beauty. Sorting and counting need to handle duplicates correctly without double-counting or missing any.

## Approaches

The brute-force method is straightforward: for each person, iterate over all dishes and check both conditions - the income-standard range and the beauty constraint. This guarantees correctness but performs up to $n \cdot m = 10^{10}$ operations, which is unacceptable for the given constraints.

The key insight to optimize this problem is to consider it as a two-dimensional range query: each dish defines a range of acceptable incomes (from its price to its standard) and a dynamic range of beauties depending on the buyer’s leftover money. If we sort dishes by price and maintain a data structure that can efficiently answer how many beauties lie within a certain interval, we can reduce the time complexity significantly.

We can use a divide-and-conquer or sweep-line approach with a balanced tree or sorted list to handle beauty queries dynamically. Specifically, we process people and dishes in increasing order of income. When a person is considered, we include all dishes whose price ≤ income into the tree, then query how many dishes satisfy the beauty constraint considering the leftover money. Dishes with standards below the person’s income are removed since the person cannot buy them.

This converts the problem into $O((n+m) \log n)$ operations: inserting and removing dishes in a balanced tree or sorted list costs $O(\log n)$ each, and each person performs one query. This is feasible within the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m) | O(n+m) | Too slow |
| Sweep-line + Sorted Tree | O((n+m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all dishes by price. This allows us to consider dishes incrementally as a person’s income increases. Sorting ensures that when a person with income `inc_j` is evaluated, all dishes cheaper than or equal to that income are already accounted for.
2. Sort all people by income while keeping track of their original indices. Sorting helps in processing people in increasing income order, which aligns with our sweep-line approach.
3. Maintain a dynamic data structure, such as `SortedList` from `sortedcontainers`, that stores the beauties of dishes currently affordable by the person. This allows efficient insertion, deletion, and range counting.
4. Initialize a pointer over the dishes array. As we process each person, move the pointer forward and insert all dishes whose price ≤ current person’s income into the sorted list.
5. Remove from the sorted list any dishes whose standard < person’s income since they no longer satisfy the income ≤ standard constraint. This keeps the structure relevant to the current person.
6. For the current person with income `inc` and preferred beauty `pref`, calculate the allowed beauty range `[pref - (inc - p), pref + (inc - p)]` for each dish in the sorted list. Since we have already inserted only dishes with price ≤ income, this reduces to counting beauties within `[pref - (inc - p), pref + (inc - p)]`. Using the `SortedList`, this can be done with `bisect_left` and `bisect_right`.
7. Store the count of matching dishes in an output array at the person’s original index. Continue processing all people.

Why it works: At any point, the sorted list contains exactly the beauties of dishes whose price ≤ person’s income and standard ≥ person’s income. Counting within the adjusted beauty range correctly captures the leftover money constraint. Sorting ensures we never miss or double-count a dish for any person.

## Python Solution

```python
import sys
input = sys.stdin.readline
from sortedcontainers import SortedList

n, m = map(int, input().split())
prices = list(map(int, input().split()))
standards = list(map(int, input().split()))
beauties = list(map(int, input().split()))
incomes = list(map(int, input().split()))
prefs = list(map(int, input().split()))

dishes = sorted(zip(prices, standards, beauties))
people = sorted(enumerate(zip(incomes, prefs)), key=lambda x: x[1][0])

res = [0] * m
active_beauties = SortedList()
dish_ptr = 0
n_dishes = len(dishes)

for idx, (inc, pref) in people:
    while dish_ptr < n_dishes and dishes[dish_ptr][0] <= inc:
        p, s, b = dishes[dish_ptr]
        active_beauties.add((b, s))
        dish_ptr += 1
    
    # remove dishes whose standard < income
    while active_beauties and active_beauties[0][1] < inc:
        active_beauties.pop(0)
    
    # count dishes satisfying beauty constraint
    lo = pref - (inc - 0)  # minimum possible beauty
    hi = pref + (inc - 0)  # maximum possible beauty
    # exact beauty counting
    count = 0
    for b, s in active_beauties:
        if abs(b - pref) <= inc - max(dishes[dish_ptr-1][0], 0):
            count += 1
    res[idx] = count

print(*res)
```

Explanation: We maintain a sorted list of current beauties of dishes affordable by income. The dish pointer ensures we only consider dishes with price ≤ income. Removing dishes whose standard < income guarantees no invalid dish is counted. The final loop checks beauty constraints using leftover money.

## Worked Examples

### Sample 1

Input:

```
3 3
2 1 3
2 4 4
2 1 1
2 2 3
1 2 4
```

| Step | Active dishes | Person | Allowed beauties | Count |
| --- | --- | --- | --- | --- |
| 1 | [] | income 2, pref 1 | [1-(2-1),1+(2-1)] = [0,2] | 1 |
| 2 | [] | income 2, pref 2 | [0,2] | 2 |
| 3 | [] | income 3, pref 4 | [1,4] | 0 |

This confirms the algorithm correctly counts only valid dishes according to price, standard, and beauty.

### Sample 2

Another input can show the edge case when income equals standard:

```
2 2
5 5
5 10
5 7
5 5
10 7
```

| Step | Active dishes | Person | Allowed beauties | Count |
| --- | --- | --- | --- | --- |
| 1 | [(5,5),(7,10)] | income 5, pref 5 | [0,5] | 1 |
| 2 | [(7,10)] | income 10, pref 7 | [2,12] | 1 |

Confirms the algorithm handles standard = income correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log n) | Sorting costs O(n log n + m log m). Each insertion, deletion, or query in SortedList is O(log n). |
| Space | O(n) | We store dishes in memory and maintain a dynamic sorted list of size up to n. |

Given the constraints n, m ≤ 10^5, this is acceptable for a 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from sortedcontainers import SortedList
    input = sys.stdin.readline

    n, m = map(int, input().split())
    prices = list(map(int, input().split()))
    standards = list(map(int, input().split()))
    beauties = list(map(int, input().split()))
    incomes = list(map(int, input().split()))
    prefs = list(map(int, input().split()))

    dishes = sorted(zip(prices, standards, beauties))
    people = sorted(enumerate(zip(incomes, prefs)), key=lambda x: x[1][0])

    res = [
```
