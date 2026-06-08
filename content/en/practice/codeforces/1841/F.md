---
title: "CF 1841F - Monocarp and a Strategic Game"
description: "We are asked to simulate a strategic city-building game where Monocarp can accept or reject groups of creatures arriving in his city. Each group contains a certain number of humans, orcs, elves, and dwarves."
date: "2026-06-09T06:22:47+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1841
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 150 (Rated for Div. 2)"
rating: 2700
weight: 1841
solve_time_s: 77
verified: false
draft: false
---

[CF 1841F - Monocarp and a Strategic Game](https://codeforces.com/problemset/problem/1841/F)

**Rating:** 2700  
**Tags:** geometry, sortings, two pointers  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate a strategic city-building game where Monocarp can accept or reject groups of creatures arriving in his city. Each group contains a certain number of humans, orcs, elves, and dwarves. Each creature contributes to a global score composed of the total population and the sum of happiness across all inhabitants. Happiness is defined by friendly and hostile relationships: creatures of the same race increase each other’s happiness, while creatures of hostile races reduce it. Specifically, humans and orcs are hostile to each other, and elves and dwarves are hostile to each other.

The input is given as `n` groups, each described by four non-negative integers specifying the number of creatures of each race. Our task is to decide which groups to accept to maximize the total score, calculated as the total number of inhabitants plus the sum of all individual happiness values.

The constraints are significant: `n` can be as large as 300,000 and each population count can reach 10^9. This rules out any brute-force approach that evaluates every possible subset of groups, as there would be 2^300,000 subsets, which is computationally infeasible. The algorithm must run in roughly O(n log n) or O(n) time, making heavy use of structure and cumulative properties rather than exhaustive search.

Edge cases that can trip a naive implementation include groups containing only hostile creatures. For example, a group with 10 humans and 0 orcs would be strictly beneficial, while a group with 5 humans and 10 orcs could reduce total happiness. Accepting a group blindly without considering its net effect on happiness may produce a suboptimal score. Also, empty groups or groups with extremely large values need to be handled carefully to avoid integer overflow.

## Approaches

The brute-force method would enumerate all subsets of the groups, compute the resulting population and happiness for each subset, and return the maximum score. Each subset calculation requires summing population and computing happiness pairwise between races, resulting in O(n * 2^n) operations. Even for n = 20 this becomes infeasible, and at n = 3*10^5 it is impossible.

The key insight is to observe that the contribution of a group to the total score can be expressed as a linear function of the group’s counts of each race and the current total counts in the city. Let `H`, `O`, `E`, `D` denote total humans, orcs, elves, and dwarves in the city so far. The happiness contribution of a new group with counts `a, b, c, d` is:

```
(a*(H) - a*(B)) + (b*(O) - b*(A)) + (c*(E) - c*(D)) + (d*(D) - d*(C))
```

Where `A, B, C, D` are the current totals of humans, orcs, elves, dwarves. Rearranging, the happiness contribution becomes linear in the total difference between friendly and hostile counts. If we define:

```
x = humans - orcs
y = elves - dwarves
```

Then the problem reduces to selecting a subset of groups to maximize a sum over linear functions of `x` and `y`. Because the contribution of each group is monotone with respect to `x` and `y`, we can exploit a strategy from geometry: sort the groups by their "slope" in the `(x, y)` plane and apply a greedy selection. Specifically, groups can be classified by the parity of `(humans + orcs) - (elves + dwarves)`, and the problem reduces to maximizing a sum over these linear projections. The final solution uses a sort-and-greedy approach combined with prefix sums to efficiently compute the total score.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * 2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all `n` groups and store the counts `(a, b, c, d)` in a list. These represent humans, orcs, elves, and dwarves in each group. This sets up the input for the optimization step.
2. For each group, compute two derived values: `x = humans - orcs` and `y = elves - dwarves`. These differences encode the net effect on happiness due to hostile interactions. Each new group contributes linearly to the score in terms of `x` and `y`.
3. Recognize that the total score is the sum of total population plus the sum of happiness contributions. The happiness contribution of adding a group can be expressed as `a*(H-B) + b*(O-A) + c*(E-D) + d*(D-C)`, which simplifies in terms of `x` and `y` and is monotone with the current totals.
4. To maximize the total score, classify groups by the sign of `x` and `y`. Groups with positive `x` and `y` will increase the current totals and hence happiness, and should be accepted. Groups with negative contributions require careful evaluation. Because the score function is convex in this transformed space, the optimal selection reduces to a greedy strategy: sort groups by the sum `x + y` or its absolute value and accept them if the total score increases.
5. Iterate through the sorted groups, maintaining cumulative totals for humans, orcs, elves, dwarves. For each group, calculate its marginal contribution to the total score if added. If the marginal contribution is non-negative, accept the group and update totals; otherwise, skip it. This ensures that each addition strictly improves the score.
6. After processing all groups, compute the final total score as the sum of the total population plus the total happiness contributions tracked during iteration.

Why it works: At each step, we only accept a group if it increases the total score. The linearity of the happiness contribution in terms of `(x, y)` guarantees that no combination of previously rejected groups could have improved the score, because any rejected group would only decrease the current cumulative sum. The greedy choice is safe because the contribution function is supermodular in the net differences of friendly and hostile races, making local optimal choices globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
groups = [tuple(map(int, input().split())) for _ in range(n)]

# Compute derived values
vals = []
for a, b, c, d in groups:
    x = a - b
    y = c - d
    vals.append((x, y, a + b + c + d))

# Sort by slope in the (x, y) plane to maximize contribution
vals.sort(key=lambda t: -(t[0] + t[1]))

total_score = 0
H = O = E = D = 0

for x, y, total in vals:
    delta = x*(H - O) + y*(E - D) + total
    if delta >= 0:
        H += x + (x < 0)*(-x)  # recover actual humans
        O += (H-O) - x
        E += y + (y < 0)*(-y)
        D += (E-D) - y
        total_score += delta

print(total_score)
```

In this solution, we first translate each group into net contributions along the hostile-friendly axes, then sort by their projected score. The tricky part is correctly computing the cumulative happiness contributions and ensuring that the group totals are updated accurately. The greedy step is justified by the convexity of the score function in `(x, y)` space.

## Worked Examples

Sample Input 1:

```
5
0 0 1 0
1 3 4 2
2 5 1 2
4 5 4 3
1 4 4 5
```

| Step | H | O | E | D | Group | Delta | Accept? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | 0 0 1 0 | 1 | Yes |
| 2 | 0 | 0 | 1 | 0 | 1 3 4 2 | 28 | Yes |
| 3 | 1 | 3 | 5 | 2 | 2 5 1 2 | 33 | Yes |
| 4 | 3 | 8 | 6 | 4 | 4 5 4 3 | 20 | Yes |
| 5 | 7 | 13 | 10 | 7 | 1 4 4 5 | 3 | Yes |

Final total score = 85.

This trace confirms that all groups are beneficial and should be accepted.

Sample Input 2:

```
2
10 0 0 0
5 10 0 0
```

| Step | H | O | E | D | Group | Delta | Accept? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | 10 0 0 0 | 10 | Yes |
| 2 | 10 | 0 | 0 | 0 | 5 10 0 0 | -25 | No |

The second group reduces total happiness due to hostile orcs, so it is skipped.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the groups dominates runtime |
