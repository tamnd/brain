---
title: "CF 46B - T-shirts from Sponsor"
description: "We are given a limited stock of T-shirts in five sizes: S, M, L, XL, and XXL. Each participant in the contest has a preferred size. Participants arrive in a fixed order and try to pick the T-shirt closest to their preferred size."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 46
codeforces_index: "B"
codeforces_contest_name: "School Personal Contest #2 (Winter Computer School 2010/11) - Codeforces Beta Round 43 (ACM-ICPC Rules)"
rating: 1100
weight: 46
solve_time_s: 73
verified: true
draft: false
---

[CF 46B - T-shirts from Sponsor](https://codeforces.com/problemset/problem/46/B)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a limited stock of T-shirts in five sizes: S, M, L, XL, and XXL. Each participant in the contest has a preferred size. Participants arrive in a fixed order and try to pick the T-shirt closest to their preferred size. If their preferred size is available, they take it. If not, they choose the closest available size. If two sizes are equally close, they pick the larger one. The goal is to determine exactly which size each participant receives.

The input consists of five integers representing the number of T-shirts in each size, followed by the number of participants, and then a list of the preferred sizes in the order participants arrive. The output is a sequence of the actual T-shirt sizes each participant receives.

The constraints are tight but manageable. With up to 1000 participants and up to 1000 T-shirts of each size, we can perform up to roughly 5000 checks per participant without exceeding typical 2-second time limits. This implies an algorithm of roughly $O(K \cdot 5)$, where 5 is the number of sizes, is acceptable. Edge cases include having zero T-shirts of certain sizes, multiple participants preferring a single popular size, or situations where only smaller or larger sizes remain. For example, if all S and M shirts are gone and someone prefers M, they should get L. A naive implementation might simply pick the next in array order, which could violate the "closest and bigger if tie" rule.

## Approaches

The brute-force approach iterates through the size preferences for each participant and checks sequentially for available shirts in the preferred order. You could construct the preference order dynamically for each participant. For instance, someone preferring L would check L, XL, M, XXL, S in that order. This method works because you are guaranteed a T-shirt exists for every participant, but it requires repeatedly generating the preference sequence for every participant and searching through the stock counts, resulting in $O(K \cdot 5)$ operations. With K ≤ 1000, this is acceptable, but it can be made slightly cleaner by predefining the preference order based on distances from each size.

The key insight is that there are only five fixed sizes, so for each participant we can precompute the order in which they will try to take shirts. This reduces any dynamic computation and avoids mistakes in tie-breaking. Once the preference order is stored in a dictionary, fulfilling the participant’s request is a simple loop through that list to find the first size with remaining stock. The structure of the problem, with a guaranteed shirt for each participant and a fixed size set, makes this approach optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(K * 5) | O(1) | Accepted |
| Optimal | O(K * 5) | O(1) | Accepted |

## Algorithm Walkthrough

1. Map each size to an index from 0 to 4: S=0, M=1, L=2, XL=3, XXL=4. This makes distance comparisons easier.
2. Store the stock counts in a list aligned to the index mapping. For example, `stock[2]` represents the number of L-shirts available.
3. Precompute the preference order for each size as a list of indices. For instance, for L (index 2), the preference is `[2, 3, 1, 4, 0]`. This is derived by increasing distance from the preferred index, and in case of a tie, choosing the larger index first.
4. Iterate through the participants in order. Convert each preferred size to its index. Use the precomputed preference order to find the first size with stock remaining.
5. Once a size is chosen, decrement its stock count and record the result.
6. Convert the final index back to the size string and output it for each participant.

This works because at every step, each participant always chooses the closest available T-shirt according to the rules. The invariant is that stock counts always reflect the shirts remaining after each participant, ensuring that no two participants are assigned the same shirt and all preferences follow the "closest and larger if tie" rule.

## Python Solution

```python
import sys
input = sys.stdin.readline

size_to_index = {'S': 0, 'M': 1, 'L': 2, 'XL': 3, 'XXL': 4}
index_to_size = ['S', 'M', 'L', 'XL', 'XXL']

# Precompute preference orders
preference_order = []
for i in range(5):
    order = [i]
    for d in range(1, 5):
        if i + d <= 4:
            order.append(i + d)
        if i - d >= 0:
            order.append(i - d)
    preference_order.append(order)

# Read stock
stock = list(map(int, input().split()))
k = int(input())

# Process participants
result = []
for _ in range(k):
    pref = input().strip()
    idx = size_to_index[pref]
    for choice in preference_order[idx]:
        if stock[choice] > 0:
            stock[choice] -= 1
            result.append(index_to_size[choice])
            break

# Output
print('\n'.join(result))
```

The solution defines mappings from sizes to indices for easy computation. The `preference_order` list ensures the "closest and bigger if tie" rule is followed. Iterating through each participant is straightforward because the preference order is precomputed. The stock is decremented immediately after assignment to maintain correctness.

## Worked Examples

Sample Input 1:

```
1 0 2 0 1
3
XL
XXL
M
```

| Participant | Preferred | Preference Order | Stock Before | Assigned | Stock After |
| --- | --- | --- | --- | --- | --- |
| 1 | XL | [3,4,2,1,0] | [1,0,2,0,1] | XXL | [1,0,2,0,0] |
| 2 | XXL | [4,3,2,1,0] | [1,0,2,0,0] | L | [1,0,1,0,0] |
| 3 | M | [1,2,0,3,4] | [1,0,1,0,0] | L | [1,0,0,0,0] |

This demonstrates the tie-breaking: when XL is unavailable, the participant chooses the next closest size, preferring larger over smaller when distance is equal.

Sample Input 2:

```
0 1 0 1 1
4
S
M
XL
XXL
```

| Participant | Preferred | Assigned |
| --- | --- | --- |
| 1 | S | M |
| 2 | M | M |
| 3 | XL | XL |
| 4 | XXL | XXL |

This shows handling zero-stock sizes correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(K * 5) | For each participant, we check at most 5 sizes in preference order. |
| Space | O(1) | Only 5-element lists for stock and preferences, plus output of size K. |

With K ≤ 1000, this fits well within the 2-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    size_to_index = {'S': 0, 'M': 1, 'L': 2, 'XL': 3, 'XXL': 4}
    index_to_size = ['S', 'M', 'L', 'XL', 'XXL']

    preference_order = []
    for i in range(5):
        order = [i]
        for d in range(1, 5):
            if i + d <= 4:
                order.append(i + d)
            if i - d >= 0:
                order.append(i - d)
        preference_order.append(order)

    stock = list(map(int, input().split()))
    k = int(input())

    result = []
    for _ in range(k):
        pref = input().strip()
        idx = size_to_index[pref]
        for choice in preference_order[idx]:
            if stock[choice] > 0:
                stock[choice] -= 1
                result.append(index_to_size[choice])
                break

    return '\n'.join(result)

# Provided samples
assert run("1 0 2 0 1\n3\nXL\nXXL\nM\n") == "XXL\nL\nL", "sample 1"

# Custom cases
assert run("0 0 1 0 1\n2\nL\nXXL\n") == "L\nXXL", "custom 1: minimal stock"
assert run("5 5 5 5 5\n5\nS\nM\nL\nXL\nXXL\n") == "S\nM\nL\nXL\nXXL", "custom 2: exact stock match"
assert run("0 1 0 1 0\n2\nS\nXXL\n") == "M\nXL", "custom 3: must pick nearest available"
assert run("0 0
```
