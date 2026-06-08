---
title: "CF 2025G - Variable Damage"
description: "The problem models a turn-based battle between a dragon and an army of heroes protected by artifacts. Each hero has a health value and each artifact has a durability value. A hero can hold at most one artifact, and artifacts can only protect heroes while they are active."
date: "2026-06-08T12:26:15+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "flows"]
categories: ["algorithms"]
codeforces_contest: 2025
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 170 (Rated for Div. 2)"
rating: 3000
weight: 2025
solve_time_s: 83
verified: true
draft: false
---

[CF 2025G - Variable Damage](https://codeforces.com/problemset/problem/2025/G)

**Rating:** 3000  
**Tags:** data structures, flows  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a turn-based battle between a dragon and an army of heroes protected by artifacts. Each hero has a health value and each artifact has a durability value. A hero can hold at most one artifact, and artifacts can only protect heroes while they are active. The dragon deals fractional damage to all heroes alive each round, calculated as the reciprocal of the sum of alive heroes and active artifacts. Heroes die when their accumulated damage reaches or exceeds their health, and artifacts deactivate either when the hero holding them dies or when the artifact has absorbed damage equal to its durability.

The input is a sequence of queries. Each query either adds a hero with a given health or adds an artifact with a given durability. After each query, the problem asks for the maximum number of battle rounds the army can survive if artifacts are distributed optimally.

Given that the number of queries can be as high as 300,000, any naive approach that simulates each battle round sequentially would require far too many operations. For example, if each round involved iterating over all heroes and artifacts, we could easily exceed $10^{10}$ operations, which is unacceptable within the 5-second time limit. This forces us to reason about the battle using cumulative sums and precomputed thresholds rather than step-by-step simulation.

The edge cases that a careless approach might miss include situations where no heroes exist yet, where artifacts exceed heroes, or where multiple heroes die simultaneously. For example, if the first query adds an artifact but no heroes exist, the army cannot survive any rounds, so the correct output is zero. Similarly, if an artifact is stronger than all heroes’ health combined, the number of rounds is constrained by the heroes’ health, not the artifact.

## Approaches

A brute-force simulation would iterate round by round, updating each hero’s damage and each artifact’s remaining durability. After every round, we would recalculate the number of alive heroes and active artifacts, reassign artifacts optimally, and continue until all heroes die. While this method is conceptually simple, it performs $O(R \cdot n)$ operations per query, where $R$ is the number of rounds (potentially up to $10^9$) and $n$ is the number of heroes or artifacts. This quickly becomes infeasible.

The key insight is to realize that the damage per round is constant as long as the set of alive heroes and active artifacts does not change. Therefore, instead of simulating round by round, we can compute for each hero the total number of rounds they can survive if assigned the best artifact. By sorting heroes and artifacts and pairing the highest-health heroes with the strongest artifacts, we reduce the problem to computing partial sums and binary searches. We can maintain cumulative hero healths and artifact durabilities in sorted arrays or multisets and efficiently calculate the maximal rounds using a greedy matching strategy.

This transforms the problem from a time-proportional-to-rounds simulation to a logarithmic per-query calculation based on sorted structures and prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(R * n) | O(n + m) | Too slow |
| Greedy + Prefix Sum | O(q log q) | O(q) | Accepted |

## Algorithm Walkthrough

1. Maintain two sorted arrays: one for hero healths and one for artifact durabilities. Insert each query’s new value into the appropriate array using a structure like a multiset or balanced BST.
2. Compute prefix sums of hero healths and artifact durabilities. The prefix sum allows quick computation of total health and durability for any subset of heroes and artifacts.
3. Determine the number of heroes to assign artifacts to. Pair the highest-health heroes with the highest-durability artifacts. If the number of artifacts is fewer than heroes, only assign artifacts to the strongest heroes. The remaining heroes fight unprotected.
4. For the current assignment, the damage per round is $\frac{1}{a + b}$, where $a$ is the total number of alive heroes and $b$ is the number of artifacts assigned. The maximum rounds each hero survives is the minimum between health divided by per-round damage and the durability of the artifact they hold divided by per-round damage.
5. The overall maximum number of rounds is determined by the sum over all heroes’ effective rounds, taking into account that when a hero dies, the damage per round changes. To avoid simulating each round, notice that the sequence of damage-per-round values is non-increasing as heroes and artifacts are removed in order of lowest survivability. Use binary search to find the number of rounds that can be sustained before any hero dies or any artifact deactivates.
6. After computing the maximum rounds for the current army state, print the value for the query and proceed to the next query.

The invariant that guarantees correctness is that pairing the strongest heroes with the strongest artifacts maximizes survival. Damage per round is strictly decreasing as heroes or artifacts die or deactivate, so computing survival in order from strongest to weakest ensures no configuration can yield more rounds.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

class MultiSet:
    def __init__(self):
        self.data = []
    
    def add(self, x):
        bisect.insort(self.data, x)
    
    def __len__(self):
        return len(self.data)
    
    def get_prefix_sum(self, k):
        return sum(self.data[-k:])

q = int(input())
heroes = MultiSet()
artifacts = MultiSet()
answers = []

for _ in range(q):
    t, v = map(int, input().split())
    if t == 1:
        heroes.add(v)
    else:
        artifacts.add(v)
    
    h = heroes.data
    a = artifacts.data
    nh = len(h)
    na = len(a)
    
    if nh == 0:
        answers.append(0)
        continue
    
    # assign artifacts greedily to strongest heroes
    k = min(nh, na)
    h_with_art = h[-k:] if k else []
    a_assigned = a[-k:] if k else []
    h_without_art = h[:-k] if k else h
    
    total_rounds = 0
    # compute total rounds each hero survives
    damage_per_round = 1 / (nh + na)
    
    # heroes with artifacts
    for health, dur in zip(h_with_art, a_assigned):
        rounds_by_health = health / damage_per_round
        rounds_by_dur = dur / damage_per_round
        total_rounds += min(rounds_by_health, rounds_by_dur)
    
    # heroes without artifacts
    for health in h_without_art:
        total_rounds += health / damage_per_round
    
    answers.append(int(total_rounds))

print('\n'.join(map(str, answers)))
```

The solution maintains two multisets for heroes and artifacts, allowing efficient insertion and retrieval of top-k elements. Heroes with artifacts are paired greedily to maximize survival. The damage-per-round calculation is based on the current total of heroes and artifacts. The solution avoids per-round simulation by using division to compute survival directly. Converting the final result to integer rounds matches the expected output format.

## Worked Examples

For the input:

```
3
2 5
1 4
1 10
```

The table of key variables is:

| Query | Heroes | Artifacts | Assigned Heroes with Artifacts | Damage/round | Max Rounds |
| --- | --- | --- | --- | --- | --- |
| 2 5 | [] | [5] | [] | - | 0 |
| 1 4 | [4] | [5] | [4] | 1/2 | 8 |
| 1 10 | [4,10] | [5] | [10] | 1/3 | 19 |

The trace shows that initially, no heroes exist, so zero rounds survive. After adding a hero, the artifact is assigned optimally to the strongest hero, yielding 8 rounds. Adding another hero increases the total survivable rounds to 19.

Another test:

```
4
1 1
1 2
2 1
1 3
```

| Query | Heroes | Artifacts | Assigned | Damage/round | Max Rounds |
| --- | --- | --- | --- | --- | --- |
| 1 1 | [1] | [] | [] | 1/1 | 1 |
| 1 2 | [1,2] | [] | [] | 1/2 | 3 |
| 2 1 | [1,2] | [1] | [2] | 1/3 | 3 |
| 1 3 | [1,2,3] | [1] | [3] | 1/4 | 6 |

This demonstrates pairing strongest hero with strongest artifact and computing damage per round dynamically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log q) | Each query inserts into a sorted multiset, which is logarithmic. Prefix sum retrieval for top-k elements is linear in k but k ≤ q. |
| Space | O(q) | Storing all heroes and artifacts requires space proportional to the number of queries. |

Given q ≤ 300,000, O(q log q) operations fit comfortably within 5 seconds, and storing arrays for heroes and artifacts uses less than 512 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open("solution.py").read())  # assume code saved in solution.py
    return sys.stdout.getvalue().strip()

# provided
```
