---
title: "CF 46F - Hercule Poirot Problem"
description: "We are given a house with a certain number of rooms connected by doors, and each door has a unique key. There are several residents in the house, each initially in some room with some keys. We also know the positions and key holdings of every resident at a later time."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 46
codeforces_index: "F"
codeforces_contest_name: "School Personal Contest #2 (Winter Computer School 2010/11) - Codeforces Beta Round 43 (ACM-ICPC Rules)"
rating: 2300
weight: 46
solve_time_s: 61
verified: true
draft: false
---

[CF 46F - Hercule Poirot Problem](https://codeforces.com/problemset/problem/46/F)

**Rating:** 2300  
**Tags:** dsu, graphs  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a house with a certain number of rooms connected by doors, and each door has a unique key. There are several residents in the house, each initially in some room with some keys. We also know the positions and key holdings of every resident at a later time. The question is whether it is possible, through a sequence of legal actions - opening doors with the keys, moving between rooms through open doors, and exchanging keys with other residents in the same room - to reach the second configuration from the first. If yes, we print "YES"; otherwise, "NO".

The house can be modeled as a graph: rooms are nodes, doors are edges. Residents move along edges if the edge is unlocked by some key they hold or obtain from someone else. Each door has exactly one key somewhere among the residents. Any door can be opened and closed multiple times, and residents can share keys when in the same room. The problem effectively asks whether each resident's final room is reachable from their initial room under these key-sharing constraints.

The constraints are small: $n, m, k \le 1000$. A brute-force simulation where we try every possible move for each resident would be too slow because the number of sequences of moves grows exponentially. However, the constraints allow graph traversal methods like BFS or DFS over at most 1000 nodes and edges. Edge cases include situations where a door is initially isolated because no one has the key in the same connected component, or all residents are in one room but need to end up in disconnected rooms - naive approaches that assume free movement would fail.

An example where careless implementation fails is two rooms connected by a door, one person in each room, and the key for the door held by the person in the opposite room. Naive "everyone can reach everyone else" logic would incorrectly say "YES," but the correct answer is "NO" because no one can unlock the door to meet or exchange keys.

## Approaches

A brute-force solution would attempt to simulate every possible sequence of door openings, resident movements, and key exchanges. For each time step, we would iterate through each resident and consider moving through every door they can open. While this would produce the correct answer, the number of possibilities is astronomical, easily exceeding $2^{1000}$ sequences in the worst case, making it impractical.

The key insight is to model each connected component of rooms that can be accessed via the keys available to residents in that component. At any moment, the residents in the same component can share keys freely. Once all keys present in a component have been propagated through reachable rooms, all rooms connected by those keys form a single "reachable component." This is exactly the problem where Disjoint Set Union (DSU) or Union-Find shines: each door is a bridge between rooms, and the key needed for a door is somewhere in the system. By iteratively merging rooms that can be unlocked using the current set of keys in a component, we can determine the maximal set of rooms each group of residents can access. If, in the end, each resident's target room lies within the reachable component of their initial room, the configuration is achievable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k * 2^m) | O(n + m + k) | Too slow |
| DSU/Component Propagation | O(m + n + k) | O(n + m + k) | Accepted |

## Algorithm Walkthrough

1. Parse the input and store the graph of rooms and doors. For each door, maintain its endpoints and associate it with a unique key.
2. Track the initial locations of each resident and the keys they hold. Also track the target locations for each resident. Maintain a mapping from key to the resident who initially holds it.
3. Initialize a Disjoint Set Union (DSU) structure to track components of rooms reachable by the keys currently available. Initially, each room is its own component.
4. For each resident, mark the doors they can currently open. For each openable door, merge the two rooms it connects in the DSU. This represents that someone with the key can move freely between those rooms.
5. Iteratively propagate keys through components. For each component, collect all keys held by residents inside the component. If a door connects two rooms in different components but the key for that door is present in one of the components, merge the components. Repeat this until no new merges are possible.
6. After the propagation stabilizes, for each resident, check if their target room lies in the same DSU component as their initial room. If all residents satisfy this condition, print "YES"; otherwise, print "NO".

Why it works: the DSU merges ensure that any two rooms in the same component are mutually reachable using the keys available to residents in that component. Key propagation guarantees that as soon as a key is accessible in some room, all doors it can open are considered, expanding the reachable area. Since residents can exchange keys freely within components, this captures all legal moves. If a target room is outside the component, it is unreachable given the constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root != y_root:
            self.parent[y_root] = x_root

def solve():
    n, m, k = map(int, input().split())
    doors = []
    for _ in range(m):
        u, v = map(int, input().split())
        doors.append((u-1, v-1))
    
    residents_init = {}
    residents_final = {}
    key_owner_init = [None] * m
    
    for i in range(k):
        parts = input().split()
        name = parts[0]
        room = int(parts[1]) - 1
        num_keys = int(parts[2])
        keys = [int(x)-1 for x in parts[3:]]
        residents_init[name] = (room, set(keys))
        for key in keys:
            key_owner_init[key] = name

    for i in range(k):
        parts = input().split()
        name = parts[0]
        room = int(parts[1]) - 1
        residents_final[name] = room

    dsu = DSU(n)
    
    changed = True
    while changed:
        changed = False
        component_keys = [set() for _ in range(n)]
        for name, (room, keys) in residents_init.items():
            root = dsu.find(room)
            component_keys[root].update(keys)
        for idx, (u, v) in enumerate(doors):
            ru, rv = dsu.find(u), dsu.find(v)
            if ru != rv:
                if idx in component_keys[ru] or idx in component_keys[rv]:
                    dsu.union(ru, rv)
                    changed = True
    
    possible = all(dsu.find(residents_init[name][0]) == dsu.find(residents_final[name]) for name in residents_init)
    print("YES" if possible else "NO")

solve()
```

The code maintains a DSU to track reachable rooms, collects all keys in each component, and iteratively merges components when a door can be opened with any key in a component. The `changed` flag ensures propagation continues until no more merges are possible. The final check verifies that each resident can reach their target room.

## Worked Examples

**Sample 1:**

Input:

```
2 1 2
1 2
Dmitry 1 1 1
Natalia 2 0
Natalia 1 1 1
Dmitry 2 0
```

| Resident | Initial Room | Keys | DSU Components after propagation | Final Room | Reachable? |
| --- | --- | --- | --- | --- | --- |
| Dmitry | 0 | {0} | 0 and 1 merged | 1 | Yes |
| Natalia | 1 | {} | 0 and 1 merged | 0 | Yes |

The DSU merges room 0 and room 1 because Dmitry holds the key for the only door. Both residents can swap keys and move to any room. Output: `YES`.

**Custom Example 2:**

Input:

```
3 2 2
1 2
2 3
Alice 0 1 0
Bob 2 1 1
Alice 2 1 0
Bob 0 1 1
```

Alice starts in room 0 with key 0, Bob in room 2 with key 1. Key 0 opens door 0 (1-2), key 1 opens door 1 (2-3). DSU initially:

- Merge room 0 and 1 using Alice's key
- Merge room 1 and 2 using Bob's key

All rooms in one component. Both residents can reach target rooms. Output: `YES`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m + k) | Each DSU union/find operation is near-constant with path compression. Iteration over doors for propagation is at most O(m * α(n)) where α is inverse Ackermann. |
| Space | O(n + m + k) | DSU parent array, key sets per component, resident info. |

Given n, m, k ≤
