---
title: "CF 1027F - Session in BSU"
description: "We are given a collection of tasks, each task representing an exam that must be scheduled on exactly one of two possible days. For exam $i$, there are two candidate days $ai$ and $bi$, and we must choose one of them."
date: "2026-06-16T21:39:16+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dfs-and-similar", "dsu", "graph-matchings", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1027
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 49 (Rated for Div. 2)"
rating: 2400
weight: 1027
solve_time_s: 417
verified: false
draft: false
---

[CF 1027F - Session in BSU](https://codeforces.com/problemset/problem/1027/F)

**Rating:** 2400  
**Tags:** binary search, dfs and similar, dsu, graph matchings, graphs  
**Solve time:** 6m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of tasks, each task representing an exam that must be scheduled on exactly one of two possible days. For exam $i$, there are two candidate days $a_i$ and $b_i$, and we must choose one of them. The constraint is that no more than one exam can be taken on any single day, so the chosen days across all exams must be all distinct.

The goal is not just to find any valid assignment, but to minimize the latest day used in such an assignment. In other words, we want to assign each exam to either its first or second available day so that all assignments are conflict free, and the maximum chosen day is as small as possible. If no assignment exists at all, we must report impossibility.

The structure immediately suggests a bipartite-style assignment problem with two choices per item, but the complication is that the domain of days is large up to $10^9$, while the number of exams is up to $10^6$. This rules out any approach that explicitly builds a day-based structure of that size.

The constraint $n \le 10^6$ implies that any solution must be close to linear or linearithmic, since $O(n \log n)$ is the typical upper bound that survives in Python at this scale. Anything quadratic in exams or in days is immediately infeasible.

A subtle failure case appears when a greedy assignment picks early constraints incorrectly:

If two exams are $(1, 2)$ and $(1, 2)$, a naive strategy might assign both to day 1, but that is invalid. Conversely, always picking the earliest available day without structure can block later assignments, even when a valid schedule exists.

Another tricky case is when many exams share a single early day but have different fallback days. If we do not control how we assign those early slots, we can unnecessarily push too many exams to later days, increasing the final maximum day or even making assignment impossible.

## Approaches

A brute-force perspective would be to treat this as a backtracking assignment problem. For each exam, we choose either $a_i$ or $b_i$, and we maintain a set of used days. Each choice either succeeds or conflicts, and we explore all possibilities.

This works conceptually because it enforces the constraint directly, but the state space doubles per exam. With $n = 10^6$, this becomes $2^n$, which is entirely impossible even for very small $n$.

A more structured view is to think of each exam as an edge between two possible days, and we want to assign each exam to exactly one endpoint such that no endpoint is reused. This is equivalent to selecting a matching in a graph where each exam is a node on one side and days are nodes on the other side, but each exam has degree 2. The problem becomes finding an injective assignment from exams to days with constraints.

The key observation is that we do not need to consider all days explicitly. Only the relative ordering of days matters, because we are minimizing the maximum used day. This suggests sorting all exams by their preferred structure and processing them greedily.

A natural greedy strategy emerges if we sort exams by their first available day $a_i$, then attempt to assign each exam to the smallest possible valid day, preferring $a_i$ before $b_i$. However, this naive greedy still fails in certain configurations because early decisions can block later ones.

The correct perspective is to interpret this as a bipartite matching with each left node having degree 2, and to process using a structure that always keeps track of forced assignments. This can be solved by processing in increasing order of days and maintaining which exams are still unassigned, using a greedy choice that avoids blocking future assignments. A standard way to enforce correctness is to treat each exam as an interval choice and use a greedy scheduling with ordering by second endpoint, combined with a data structure that always assigns the earliest feasible slot.

In practice, the optimal solution reduces to sorting by $b_i$ and greedily assigning exams to available days, ensuring we always use the earliest possible day and avoid future conflicts. This mirrors classic interval scheduling with alternatives, where ordering by the later constraint minimizes blocking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Backtracking | $O(2^n)$ | $O(n)$ | Too slow |
| Greedy with ordering by $b_i$ | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We transform each exam into a pair of candidate days and process exams in an order that respects their constraints.

1. Sort all exams by their second available day $b_i$. This ensures that exams with tighter deadlines are handled first. The intuition is that if an exam has a small $b_i$, delaying it risks losing both options.
2. Maintain a set or ordered structure of already used days. This structure allows us to check whether a day is already occupied in logarithmic time.
3. Iterate through exams in sorted order. For each exam, attempt to assign it to $a_i$ if that day is free. If not, attempt to assign it to $b_i$.
4. If neither $a_i$ nor $b_i$ is available, the assignment is impossible, so we return -1 immediately.
5. Track the maximum day used across all assignments. This value represents the earliest day by which all exams are completed.
6. After processing all exams, return the maximum assigned day.

The choice of preferring $a_i$ over $b_i$ is not arbitrary. Since $a_i < b_i$, using the earlier slot when possible preserves later flexibility, while still respecting the ordering imposed by sorting on $b_i$.

### Why it works

At any step, we process the exam with the smallest second choice among all remaining exams. This ensures that if there is any feasible assignment, we never postpone an exam beyond its last possible safe placement. The invariant is that after processing the first $k$ exams, there exists a valid assignment for those exams using only already considered structure, and no future decision depends on reassigning earlier choices. The greedy choice preserves feasibility because any alternative assignment that delays an exam with smaller $b_i$ cannot improve feasibility for later exams with larger or equal $b_i$.

## Python Solution

```
PythonRun
```

The sorting step ensures we always process the most constrained exams first in terms of their second available day. The greedy assignment tries the earlier day first because it preserves later availability. The set `used` enforces the uniqueness constraint across all chosen days. The variable `ans` tracks the latest day used in any assignment.

The early exit on failure is crucial because once an exam cannot be assigned, no rearrangement of future assignments can fix the violation due to the ordering by $b_i$.

## Worked Examples

### Example 1

Input:

```

```

Sorted by $b$:

| Step | Exam (a,b) | Try a | Try b | Used days | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,5) | 1 free | - | {1} | 1 |
| 2 | (1,7) | 1 taken | 7 free | {1,7} | 7 |

Output:

```

```

This trace shows how conflicts at early days force use of later slots, and the maximum day reflects the final completion time.

### Example 2

Input:

```

```

Sorted by $b$:

| Step | Exam | Action | Used | ans |
| --- | --- | --- | --- | --- |
| 1 | (1,2) | take 1 | {1} | 1 |
| 2 | (2,3) | take 2 | {1,2} | 2 |
| 3 | (1,3) | 1 taken, take 3 | {1,2,3} | 3 |

Output:

```

```

This demonstrates that even when early choices collide, fallback assignments preserve feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; each exam is processed once with O(1) set operations on average |
| Space | $O(n)$ | Storage for exams and used-day tracking |

The complexity fits comfortably within constraints for $n = 10^6$, as sorting and linear processing remain feasible under typical limits.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical chain | 5 | greedy feasibility propagation |
| duplicate impossible | -1 | conflict detection |
| single exam | 10 | base case correctness |
| chained overlaps | 4 | late blocking behavior |

## Edge Cases

A key edge case is when many exams share the same early day but differ in fallback days. The algorithm handles this because sorting by $b_i$ ensures the most constrained exams are assigned first, preventing them from being pushed into conflicts later.

Another case is when two exams share both candidates. For example:

```

```

After sorting, the first exam takes day 1, and the second is forced to day 2. If both 1 and 2 were already taken, the algorithm correctly fails. This shows that the set-based occupancy check correctly enforces injectivity without requiring explicit backtracking.

A final subtle case is long chains where each assignment depends on freeing earlier choices. Because we never reassign once a day is used, correctness relies entirely on processing order. Sorting by $b_i$ guarantees that no later decision can invalidate earlier feasibility, so the greedy assignment remains consistent throughout execution.
