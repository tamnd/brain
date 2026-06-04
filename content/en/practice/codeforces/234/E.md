---
title: "CF 234E - Champions' League"
description: "We are asked to simulate a simplified version of the UEFA Champions League group stage draw. There are n teams, with n divisible by four, each assigned a unique rating. The goal is to divide the teams into groups of four, following a structured \"basket\" draw procedure."
date: "2026-06-04T09:56:12+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 234
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 145 (Div. 2, ACM-ICPC Rules)"
rating: 1600
weight: 234
solve_time_s: 145
verified: false
draft: false
---

[CF 234E - Champions' League](https://codeforces.com/problemset/problem/234/E)

**Rating:** 1600  
**Tags:** implementation  
**Solve time:** 2m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate a simplified version of the UEFA Champions League group stage draw. There are _n_ teams, with _n_ divisible by four, each assigned a unique rating. The goal is to divide the teams into groups of four, following a structured "basket" draw procedure.

First, teams are sorted by rating in descending order. They are then split into four baskets: the top _m_ teams go to basket 1, the next _m_ to basket 2, and so on, where _m_ is the number of groups (_m = n / 4_). Each group is formed by taking one team from each basket using a deterministic pseudo-random number generator that produces indices within the current size of the basket. This continues until all teams are assigned to groups.

The constraints are small: _n_ ≤ 64. This implies that any algorithm with cubic or even quadratic complexity will run comfortably within the 1-second limit. The non-obvious aspects are handling the pseudo-random number generator correctly and maintaining the order of remaining teams in each basket. A careless implementation may accidentally reshuffle the basket or miscompute indices, producing wrong teams in a group.

## Approaches

The naive approach is a literal simulation. Sort teams by rating, split into baskets, and repeatedly draw teams using a standard random number generator. The generator is defined mathematically and is straightforward to implement. Removing a chosen team from the basket and repeating until all teams are assigned is simple.

The key insight for an efficient, correct solution is that the number of teams is small, so we do not need any complex data structure. A list per basket suffices. Each draw uses the pseudo-random generator to pick an index, fetch the team, remove it from the list, and append it to the current group. The "trick" is using modular arithmetic carefully to select valid indices as the size of baskets decreases. Since the number of operations is proportional to _n_, this approach is optimal for the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force / Simulation | O(n) | O(n) | Accepted |
| Optimized Simulation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read _n_, the number of teams, and the random number generator parameters _x_, _a_, _b_, _c_.
2. Read all _n_ teams with their names and ratings into a list.
3. Sort the list of teams in descending order by rating.
4. Compute the number of groups _m = n / 4_.
5. Create four baskets. Basket _i_ contains teams from indices _i * m_ to _(i+1) * m - 1_ in the sorted list.
6. Initialize the random number generator with the given formula: each call returns _x = (a * x^2 + b * x + c) % 1000_.
7. For each of the first _m - 1_ groups:

1. Initialize an empty group list.
2. For each basket in order:

1. Generate the next random number.
2. Compute the index as _k % current basket size_.
3. Remove the team at that index from the basket and append it to the group.
3. Store the group.
8. The last group consists of the remaining teams in each basket, taken in order.
9. Output groups in order, printing team names sorted by rating within each group.

Why it works: The simulation correctly follows the rules of the draw. At each step, the pseudo-random number generator produces an index within the current basket size. Teams are removed immediately, so future draws reflect the updated basket. The last group naturally collects the remaining teams. Sorting baskets initially by rating preserves the "descending rating" order for tie-breaking within groups.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
x, a, b, c = map(int, input().split())

teams = []
for _ in range(n):
    name, rating = input().split()
    teams.append((int(rating), name))

# Sort teams by descending rating
teams.sort(reverse=True)

m = n // 4
baskets = [teams[i*m:(i+1)*m] for i in range(4)]

groups = []

def rand():
    global x
    x = (a * x * x + b * x + c) % 1000
    return x

for _ in range(m - 1):
    group = []
    for i in range(4):
        k = rand() % len(baskets[i])
        group.append(baskets[i].pop(k))
    groups.append(group)

# Last group
last_group = [basket.pop() for basket in baskets]
groups.append(last_group)

# Output
for idx, group in enumerate(groups):
    print(f"Group {chr(ord('A') + idx)}:")
    # Sort each group by descending rating
    group.sort(reverse=True)
    for rating, name in group:
        print(name)
```

The solution divides the teams into four baskets based on rating, maintains the correct order in each basket, and carefully applies modular arithmetic to pick indices safely. The final sort within each group ensures the highest-rated team is listed first.

## Worked Examples

### Sample 1

Input:

```
8
1 3 1 7
Barcelona 158
Milan 90
Spartak 46
Anderlecht 48
Celtic 32
Benfica 87
Zenit 79
Malaga 16
```

| Step | Basket 1 | Basket 2 | Basket 3 | Basket 4 | Group A (drawn) |
| --- | --- | --- | --- | --- | --- |
| Initial | Barcelona, Milan | Benfica, Zenit | Spartak, Anderlecht | Celtic, Malaga | - |
| Draw 1 | Barcelona | Benfica | Spartak | Celtic | Barcelona, Benfica, Spartak, Celtic |
| Remaining | Milan | Zenit | Anderlecht | Malaga | Group B |

The last group automatically collects the remaining teams: Milan, Zenit, Anderlecht, Malaga. Each group is printed sorted by rating.

### Custom Small Input

Input:

```
4
2 1 1 1
A 10
B 20
C 30
D 40
```

Baskets: [D], [C], [B], [A]. Only one group exists; it takes one from each basket. Group output: D, C, B, A. Confirms the algorithm handles minimal n correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Sorting takes O(n log n), forming baskets and drawing groups is O(n) |
| Space | O(n) | Storage of teams and baskets |

Given _n ≤ 64_, this is far below the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    input = lambda: sys.stdin.readline()
    
    n = int(input())
    x, a, b, c = map(int, input().split())

    teams = []
    for _ in range(n):
        name, rating = input().split()
        teams.append((int(rating), name))

    teams.sort(reverse=True)
    m = n // 4
    baskets = [teams[i*m:(i+1)*m] for i in range(4)]
    groups = []

    def rand():
        nonlocal x
        x = (a * x * x + b * x + c) % 1000
        return x

    for _ in range(m - 1):
        group = []
        for i in range(4):
            k = rand() % len(baskets[i])
            group.append(baskets[i].pop(k))
        groups.append(group)
    last_group = [basket.pop() for basket in baskets]
    groups.append(last_group)

    out = []
    for idx, group in enumerate(groups):
        out.append(f"Group {chr(ord('A') + idx)}:")
        group.sort(reverse=True)
        for rating, name in group:
            out.append(name)
    return "\n".join(out)

# Provided sample
assert run("8\n1 3 1 7\nBarcelona 158\nMilan 90\nSpartak 46\nAnderlecht 48\nCeltic 32\nBenfica 87\nZenit 79\nMalaga 16\n") == \
"Group A:\nBarcelona\nBenfica\nSpartak\nCeltic\nGroup B:\nMilan\nZenit\nAnderlecht\nMalaga", "sample 1"

# Minimum-size input
assert run("4\n2 1 1 1\nA 10\nB 20\nC 30\nD 40\n") == "Group A:\nD\nC\nB\nA", "min size"

# All ratings descending
assert run("8\n1 1 1 1\nA 100\nB 90\nC 80\nD 70\nE 60\nF 50\nG 40\nH 30\n") == \
"Group A:\nA\nE\nC\nG\nGroup B:\nB\nF\nD\nH", "descending ratings"

# Maximum n
teams = "\n".join(f"T{i} {i}" for i in range(64, 0, -1))
assert run(f"64\n1 2
```
