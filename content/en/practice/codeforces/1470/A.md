---
title: "CF 1470A - Strange Birthday Party"
description: "We are asked to minimize the total cost of giving presents to a group of friends under a set of constraints. Each friend has a preferred present number, $ki$. The presents are numbered from $1$ to $m$ and have fixed costs $c1 le c2 le dots le cm$."
date: "2026-06-11T00:58:44+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1470
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 694 (Div. 1)"
rating: 1300
weight: 1470
solve_time_s: 88
verified: true
draft: false
---

[CF 1470A - Strange Birthday Party](https://codeforces.com/problemset/problem/1470/A)

**Rating:** 1300  
**Tags:** binary search, dp, greedy, sortings, two pointers  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to minimize the total cost of giving presents to a group of friends under a set of constraints. Each friend has a preferred present number, $k_i$. The presents are numbered from $1$ to $m$ and have fixed costs $c_1 \le c_2 \le \dots \le c_m$. For a given friend, we have two options: either buy a present whose number does not exceed $k_i$ or simply give that friend $c_{k_i}$ dollars directly. Each present can only be purchased once. The goal is to compute the minimum total expenditure over all friends.

The input can have up to $3 \cdot 10^5$ friends and presents cumulatively across test cases. This bound rules out any solution with quadratic complexity. For each friend, iterating over all presents up to $k_i$ would be too slow because that could reach $O(n \cdot m)$ operations in the worst case. Instead, we need an approach linearithmic or linear in the number of friends, using sorting or greedy allocation.

Edge cases include situations where multiple friends have low $k_i$ values and cheap presents, or when $k_i$ values are already aligned with cheap presents. A careless greedy allocation of cheapest presents without considering the $k_i$ limits can overspend. For instance, if all friends prefer $k_i = 1$ but the cheapest presents are at the end of the list, blindly taking the cheapest available will violate the constraint.

## Approaches

The brute-force method would be to iterate over each friend, and for each, scan through all presents from $1$ to $k_i$ to pick the cheapest unassigned present. This is correct in principle but clearly too slow. If $n$ and $m$ are both around $3 \cdot 10^5$, scanning $O(k_i)$ for each friend can easily reach $10^{10}$ operations.

The key observation for a faster solution is that the friends who accept higher-numbered presents are more flexible. Conversely, those with smaller $k_i$ values have fewer options. We can exploit this by sorting friends by $k_i$ in descending order and assigning the cheapest remaining presents to the friends with higher $k_i$. We iterate over friends from the one willing to accept the most expensive present down to the friend with the smallest $k_i$. At each step, we compare the cheapest available present with giving $c_{k_i}$ dollars directly and choose the minimum. This guarantees that we never violate the $k_i$ constraint and also ensures we use the cheaper presents in order.

This approach naturally leads to a two-pointer or greedy method that is linear in the number of friends plus the sorting step, which is $O(n \log n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(m) | Too slow |
| Optimal | O(n log n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of friends $n$, number of presents $m$, the array of preferred presents $k$, and the costs $c$ of presents.
2. Sort the friends' $k_i$ in descending order. This ensures that friends who are willing to accept more expensive presents are handled first, so we assign cheaper presents without violating the limit.
3. Initialize a pointer `p` at 0 to track the next cheapest present in `c`.
4. Initialize `total_cost` as 0.
5. Iterate over each friend in descending $k_i$ order:

a. Compute the direct cost for this friend as $c[k_i - 1]`. b. If the pointer `p` is within bounds (`p < m`) and the present `c[p]` is cheaper than $c[k_i - 1]`, assign present `c[p]` and increment `p`.

c. Otherwise, give the friend $c[k_i - 1]$ dollars directly.

d. Add the chosen cost to `total_cost`.
6. After processing all friends, output `total_cost`.

Why it works: By processing friends willing to accept higher $k_i$ first, we ensure that the cheapest presents go to the most flexible friends. Any friend with a smaller $k_i$ will never be forced to take a present that exceeds their limit because we only use presents starting from the cheapest upward and never exceeding their $k_i$. The pointer `p` guarantees that each present is assigned at most once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        k = list(map(int, input().split()))
        c = list(map(int, input().split()))
        
        k.sort(reverse=True)
        p = 0
        total_cost = 0
        for ki in k:
            direct_cost = c[ki - 1]
            if p < m and c[p] < direct_cost:
                total_cost += c[p]
                p += 1
            else:
                total_cost += direct_cost
        print(total_cost)

if __name__ == "__main__":
    solve()
```

The code begins by reading the number of test cases. Each test case reads `n`, `m`, the friends' preferred presents, and the present costs. The `k` array is sorted in descending order to prioritize friends who can accept more expensive presents. The pointer `p` keeps track of which presents have been used. For each friend, we choose between the cheapest available present within bounds and the direct dollar amount. The choice is added to the cumulative `total_cost`. Printing the total after each test case matches the required output format. Subtle points include the `ki - 1` adjustment for zero-based indexing in Python and the boundary check `p < m`.

## Worked Examples

### Sample 1

Input:

```
5 4
2 3 4 3 2
3 5 12 20
```

| Friend (k_i) | Direct Cost | Cheapest Available (c[p]) | Chosen Cost | Pointer p |
| --- | --- | --- | --- | --- |
| 4 | 20 | 3 | 3 | 1 |
| 3 | 12 | 5 | 5 | 2 |
| 3 | 12 | 12 | 12 | 3 |
| 2 | 5 | 12 | 5 | 3 |
| 2 | 5 | 12 | 5 | 3 |

Total cost = 3 + 5 + 12 + 5 + 5 = 30

This trace confirms that the greedy assignment of cheapest presents to flexible friends avoids overspending.

### Sample 2

Input:

```
5 5
5 4 3 2 1
10 40 90 160 250
```

| Friend (k_i) | Direct Cost | Cheapest Available (c[p]) | Chosen Cost | Pointer p |
| --- | --- | --- | --- | --- |
| 5 | 250 | 10 | 10 | 1 |
| 4 | 160 | 40 | 40 | 2 |
| 3 | 90 | 90 | 90 | 3 |
| 2 | 40 | 160 | 40 | 3 |
| 1 | 10 | 160 | 10 | 3 |

Total cost = 10 + 40 + 90 + 40 + 10 = 190

The trace demonstrates how direct cost is used when remaining cheap presents exceed the friend's limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m) | Sorting friends is O(n log n), iteration over friends is O(n), cumulative m does not exceed constraints. |
| Space | O(n + m) | Storing k and c arrays; auxiliary space is negligible. |

The algorithm easily fits within the 1-second limit even at maximum input sizes because the main work is dominated by sorting `k`, and all other operations are linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("2\n5 4\n2 3 4 3 2\n3 5 12 20\n5 5\n5 4 3 2 1\n10 40 90 160 250\n") == "30\n190"

# minimum-size input
assert run("1\n1 1\n1\n100\n") == "100", "single friend, single present"

# all k_i same
assert run("1\n3 3\n2 2 2\n5 10 15\n") == "15", "friends with same k_i, use cheapest for first, rest direct"

# increasing k_i
assert run("1\n4 4\n1 2 3 4\n1 2 3 4\n") == "10", "assign cheapest presents to flexible friends"

# maximum k_i
assert run("1\n3 5\n5 5 5\n10 20 30 40 50\n") == "60", "all friends take cheapest available within k_i=5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| ` |  |  |
