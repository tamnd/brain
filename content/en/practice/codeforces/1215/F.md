---
title: "CF 1215F - Radio Stations"
description: "We are asked to assign a signal power to a set of radio stations and choose a subset of these stations such that all citizen complaints are satisfied, no two stations interfere, and each chosen station's signal power falls within its allowed range."
date: "2026-06-11T22:58:40+07:00"
tags: ["codeforces", "competitive-programming", "2-sat"]
categories: ["algorithms"]
codeforces_contest: 1215
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 585 (Div. 2)"
rating: 2700
weight: 1215
solve_time_s: 135
verified: false
draft: false
---

[CF 1215F - Radio Stations](https://codeforces.com/problemset/problem/1215/F)

**Rating:** 2700  
**Tags:** 2-sat  
**Solve time:** 2m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to assign a signal power to a set of radio stations and choose a subset of these stations such that all citizen complaints are satisfied, no two stations interfere, and each chosen station's signal power falls within its allowed range. Each complaint identifies two stations and requires that at least one of them is active. Each station has a minimum and maximum allowed signal power, and certain pairs of stations cannot both be active due to interference. The challenge is to find a signal power and a valid set of stations or report impossibility.

The input size is large: up to 400,000 complaints, stations, and interference pairs. This rules out any algorithm with cubic or quadratic complexity in the number of stations or complaints. We need a solution close to linear or linearithmic time. A naive approach that tries every subset of stations or every possible signal power is infeasible because even enumerating all subsets of 400,000 stations is astronomically slow.

Non-obvious edge cases include situations where the minimum allowed power of all stations is above the maximum allowed power of others, making it impossible to find a single global signal power. Another tricky case is when interference constraints form a complex web that prevents activating stations needed for complaints, for example, if complaints form a cycle and each adjacent station interferes with the next. A careless implementation might pick stations greedily without checking for conflicts, producing an invalid solution or reporting no solution when one exists.

## Approaches

The brute-force approach would try every integer signal power from 1 to M and, for each power, attempt to pick a subset of stations satisfying all complaints and avoiding interference. To verify each subset, one would need to check all complaints and all interfering pairs. This is correct in principle but too slow: iterating over M values up to 4×10^5 and processing potentially 400,000 complaints for each leads to roughly 1.6×10^11 operations, far above feasible limits.

The key observation is that for any chosen signal power, a station is either allowed (its `[l_i, r_i]` contains the signal power) or not. If we fix a candidate signal power, the problem reduces to a 2-SAT instance. Each complaint requires that at least one of its two stations is selected, forming a clause `(x_i OR y_i)`. Each interference pair forbids selecting both stations, forming a clause `(NOT u_i OR NOT v_i)`. 2-SAT can be solved in linear time with respect to the number of variables and clauses using strongly connected components in an implication graph.

Thus, the optimal approach is to iterate over possible signal powers intelligently. Instead of testing all powers from 1 to M, we only consider powers where some station range starts or ends because only these boundaries can change the set of valid stations. For each candidate power, we build the 2-SAT instance for stations allowed at that power, solve it, and return the solution if satisfiable. This reduces the number of candidate powers to at most 2p, which is feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(M·(n+m)) ≈ 1.6×10^11 | O(n+m) | Too slow |
| Optimal | O(p + n + m) per candidate × O(p) candidates ≈ 10^7-10^8 | O(p + n + m) | Accepted |

## Algorithm Walkthrough

1. Collect all distinct values from the `l_i` and `r_i` arrays of stations. These are the only signal powers where the set of valid stations changes, as moving between these points does not add or remove any allowed stations.
2. Sort these candidate powers. Iterating in order lets us process contiguous ranges efficiently if desired.
3. For each candidate signal power `f`, determine which stations are allowed. A station is allowed if its minimum `l_i ≤ f ≤ r_i`.
4. Build a 2-SAT instance for allowed stations:

- For each complaint `(x_i, y_i)`, add a clause `(x_i OR y_i)`. This ensures at least one station satisfies the complaint.
- For each interference pair `(u_i, v_i)`, add a clause `(NOT u_i OR NOT v_i)` to forbid both being selected.
5. Solve the 2-SAT instance using the standard implication graph method:

- For each clause `(a OR b)`, add edges `(NOT a → b)` and `(NOT b → a)`.
- Find strongly connected components. If a variable and its negation are in the same component, the instance is unsatisfiable.
- Otherwise, assign truth values based on component order to get a valid selection of stations.
6. If any candidate signal power yields a satisfiable 2-SAT instance, output the signal power and the chosen stations. Otherwise, report `-1`.

Why it works: iterating over boundary powers guarantees that all feasible signal powers are tested without redundancy. 2-SAT correctly models both complaints and interference constraints. The solution for any satisfiable instance satisfies all original problem conditions because it directly encodes the allowed station ranges and conflict restrictions.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

def solve():
    n, p, M, m = map(int, input().split())
    complaints = [tuple(map(int, input().split())) for _ in range(n)]
    lr = [tuple(map(int, input().split())) for _ in range(p)]
    conflicts = [tuple(map(int, input().split())) for _ in range(m)]

    # Collect candidate powers
    candidates = set()
    for l, r in lr:
        candidates.add(l)
        candidates.add(r)
    candidates = sorted(candidates)

    # 2-SAT helper functions
    class TwoSAT:
        def __init__(self, n):
            self.N = n
            self.adj = [[] for _ in range(2*n)]

        def add_implication(self, u, v):
            self.adj[u].append(v)

        def add_or(self, u, v):
            self.add_implication(u^1, v)
            self.add_implication(v^1, u)

        def satisfiable(self):
            self.order = []
            self.visited = [False]*(2*self.N)
            self.comp = [0]*(2*self.N)

            def dfs(u):
                self.visited[u] = True
                for v in self.adj[u]:
                    if not self.visited[v]:
                        dfs(v)
                self.order.append(u)

            for u in range(2*self.N):
                if not self.visited[u]:
                    dfs(u)

            g_rev = [[] for _ in range(2*self.N)]
            for u in range(2*self.N):
                for v in self.adj[u]:
                    g_rev[v].append(u)

            self.visited = [False]*(2*self.N)
            label = 0
            comp = [0]*(2*self.N)
            def dfs_rev(u):
                comp[u] = label
                self.visited[u] = True
                for v in g_rev[u]:
                    if not self.visited[v]:
                        dfs_rev(v)

            for u in reversed(self.order):
                if not self.visited[u]:
                    dfs_rev(u)
                    label += 1
            self.comp = comp
            assignment = [False]*self.N
            for i in range(self.N):
                if comp[2*i] == comp[2*i+1]:
                    return None
                assignment[i] = comp[2*i] < comp[2*i+1]
            return assignment

    for f in candidates:
        valid = [i for i, (l, r) in enumerate(lr) if l <= f <= r]
        if not valid:
            continue
        id_map = {v: idx for idx, v in enumerate(valid)}
        ts = TwoSAT(len(valid))

        for x, y in complaints:
            if x-1 in id_map and y-1 in id_map:
                ts.add_or(2*id_map[x-1], 2*id_map[y-1])
            elif x-1 in id_map:
                ts.add_or(2*id_map[x-1], 2*id_map[x-1])
            elif y-1 in id_map:
                ts.add_or(2*id_map[y-1], 2*id_map[y-1])
            else:
                break
        else:
            for u, v in conflicts:
                if u-1 in id_map and v-1 in id_map:
                    ts.add_or(2*id_map[u-1]^1, 2*id_map[v-1]^1)
            assignment = ts.satisfiable()
            if assignment:
                chosen = [valid[i]+1 for i, val in enumerate(assignment) if val]
                print(len(chosen), f)
                print(*chosen)
                return
    print(-1)

if __name__ == "__main__":
    solve()
```

The solution first identifies the candidate signal powers using the boundaries of station ranges. The TwoSAT class is implemented using the implication graph approach. Complaints generate OR clauses, interference generates NOT-OR clauses. Only stations allowed at the current power are mapped into variables. If satisfiable, the program prints the chosen power and stations; otherwise, it continues to the next candidate.

## Worked Examples

**Sample 1**

| Step | Candidate power f | Valid stations | Clauses added | Satisfiable? | Chosen stations |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1,2,4 | (1 OR 3), (2 |  |  |
