---
title: "CF 103708J - Jeffrey's ambition"
description: "The problem gives a set of wealthy individuals and a set of companies. Each person has a list of companies they are willing to buy, and each company can be assigned to at most one person."
date: "2026-07-02T09:32:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103708
codeforces_index: "J"
codeforces_contest_name: "2022 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 103708
solve_time_s: 50
verified: true
draft: false
---

[CF 103708J - Jeffrey's ambition](https://codeforces.com/problemset/problem/103708/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives a set of wealthy individuals and a set of companies. Each person has a list of companies they are willing to buy, and each company can be assigned to at most one person. Some people may have no allowed companies at all, and some companies may appear in multiple lists.

The council must assign companies to people so that every assignment respects the lists, meaning a person can only receive a company they explicitly listed. After all assignments are made, some companies may remain unassigned. The goal is to choose assignments in a way that minimizes the number of unassigned companies.

In graph terms, this is a bipartite matching problem between people and companies, where we want to maximize the number of matched companies, since every matched company removes one from the “unassigned” count.

The constraints are large enough that both the number of people and companies can be up to 10,000, and the total number of preferences across all people is up to 100,000. This rules out any approach that tries to enumerate all matchings or repeatedly simulate greedy reassignment in a naive way. Any solution needs to behave close to linear or near-linear in the number of edges.

A subtle edge case appears when some people have an empty list. For example, if a person has no allowed companies, they contribute nothing to the matching but still exist in the input. Another edge case occurs when multiple people want the same single company, for instance two people both list only company 1. A naive greedy assignment that processes people in input order can easily assign the company to a suboptimal person and block a better overall matching.

For example, consider two people both interested in the same two companies, but structured asymmetrically:

Input:

```
2 2
2 1 2
1 1
```

If we assign person 1 to company 1 immediately, person 2 becomes impossible to satisfy, but a better assignment is person 1 to company 2, person 2 to company 1, achieving zero unassigned companies. This shows that local greedy decisions can fail.

## Approaches

A brute-force strategy would try to explore all possible assignments of companies to people while respecting preferences. Each person could choose among multiple companies, and we would recursively assign or skip companies, backtracking when conflicts arise. This quickly becomes exponential because each company shared by multiple people creates branching decisions, and in the worst case where every person wants many companies, the number of states grows as a factorial-type search over matchings.

The key observation is that we are not actually trying to assign people optimally for their benefit, but rather to maximize the number of matched companies. This transforms the problem into finding a maximum bipartite matching between people and companies. Each successful match reduces the count of unassigned companies by one, so maximizing matches is equivalent to minimizing leftovers.

This structure allows us to use classical matching techniques. Since edges are unweighted and the graph is bipartite, we can apply a standard DFS-based augmenting path approach (Kuhn’s algorithm). The idea is to iterate over people and try to assign each one to a company, possibly rearranging previous assignments if that allows a better overall matching. When a company is already taken, we attempt to “push” its current owner to another acceptable company recursively, freeing it for the current person. This local reassignment mechanism is exactly what fixes the failure cases of greedy assignment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search over assignments | Exponential | O(N + M) | Too slow |
| Kuhn’s DFS augmenting path matching | O(N·E) worst-case, ~O(E√V) typical | O(N + M + E) | Accepted |

## Algorithm Walkthrough

We model people on the left side and companies on the right side of a bipartite graph. An edge connects a person to each company in their preference list.

1. Build adjacency lists where each person stores all companies they are willing to buy. This representation allows efficient traversal of all possible matches for a person.
2. Maintain an array `match_to_company` that records which person currently owns each company. Initially, all companies are unassigned, so this array is empty.
3. Define a depth-first search function that tries to assign a company to a given person. The function explores all companies in that person’s list.
4. For each company, check whether it is currently unassigned. If it is free, assign it immediately to the current person and return success, because we have increased the matching size without conflict.
5. If the company is already assigned to another person, attempt to reassign that existing person to a different company by recursively calling the DFS on that person. If that recursive call succeeds, it means we have found an alternative placement, so we can safely take the company for the current person.
6. Repeat this process for all people. Each time a new assignment is made, it potentially triggers a chain of reassignments that preserves feasibility while increasing total matches.
7. After processing all people, count how many companies remain unassigned. The answer is the total number of companies minus the number of matched companies.

The key idea behind the correctness is that every time we reassign a company, we preserve a valid matching while possibly freeing space for another assignment. The DFS guarantees that if a better configuration exists reachable through local swaps along alternating paths, it will be found.

## Why it works

At any point in the algorithm, the set of assigned companies forms a valid matching. The DFS search explores alternating paths between free and occupied companies. Each successful recursive reassignment corresponds to following an alternating path that ends at a free company, which allows the entire path to be flipped. This maintains the invariant that no company is assigned to more than one person while monotonically increasing the number of assigned companies whenever possible. Since each successful DFS either assigns a previously unassigned company or reconfigures a chain to free one, the total number of matches is maximal when no further augmenting path exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    
    for i in range(n):
        data = list(map(int, input().split()))
        k = data[0]
        if k > 0:
            g[i] = data[1:]

    match = [-1] * (m + 1)
    vis = None

    def dfs(u):
        for v in g[u]:
            if vis[v]:
                continue
            vis[v] = True
            if match[v] == -1 or dfs(match[v]):
                match[v] = u
                return True
        return False

    for i in range(n):
        vis = [False] * (m + 1)
        dfs(i)

    matched = sum(1 for x in match if x != -1)
    print(m - matched)

if __name__ == "__main__":
    solve()
```

The adjacency list stores each person's allowed companies directly, so the DFS can enumerate only valid transitions. The `match` array is indexed by company and stores the current assigned person.

The visited array is recreated for each DFS attempt to prevent cycling within a single augmenting search, which is necessary because the graph is dynamic in terms of exploration but static in structure. Resetting `vis` per outer iteration ensures that each attempt explores a fresh search tree.

The final subtraction `m - matched` converts maximum matching size into the number of unassigned companies, which is the required output.

## Worked Examples

### Example 1

Input:

```
5 6
2 1 2
0
1 3
1 4
2 1 5
```

We track only key match changes.

| Person | Preferences | DFS outcome | match state (company → person) |
| --- | --- | --- | --- |
| 0 | 1,2 | assigns 1 | 1→0 |
| 1 | none | no change | 1→0 |
| 2 | 3 | assigns 3 | 1→0, 3→2 |
| 3 | 4 | assigns 4 | 1→0, 3→2, 4→3 |
| 4 | 1,5 | 1 occupied, 5 free | 1→0, 3→2, 4→3, 5→4 |

Matched companies = 4, so answer = 6 − 4 = 2.

This trace shows how DFS avoids blocking future assignments by only committing to a company when it either is free or can be freed through reassignment.

### Example 2

Input:

```
5 5
1 1
1 2
1 3
1 4
1 5
```

| Person | Preferences | DFS outcome | match state |
| --- | --- | --- | --- |
| 0 | 1 | assign 1 | 1→0 |
| 1 | 2 | assign 2 | 1→0, 2→1 |
| 2 | 3 | assign 3 | 1→0, 2→1, 3→2 |
| 3 | 4 | assign 4 | 1→0, 2→1, 3→2, 4→3 |
| 4 | 5 | assign 5 | 1→0, 2→1, 3→2, 4→3, 5→4 |

Matched companies = 5, answer = 0.

This case confirms the algorithm achieves full matching when the graph is already perfectly structured.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N·E) worst-case | Each DFS may traverse edges multiple times during augmentation chains |
| Space | O(N + M + E) | adjacency list plus match arrays and recursion state |

The total number of edges is bounded by 100,000, and both N and M are at most 10,000, which makes this approach fast enough in practice under typical Codeforces constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n, m = map(int, inp.split()[0:2])  # dummy to silence lint
    # re-run solution
    input_data = inp
    sys.stdin = io.StringIO(input_data)

    def solve():
        n, m = map(int, input().split())
        g = [[] for _ in range(n)]
        for i in range(n):
            data = list(map(int, input().split()))
            k = data[0]
            if k > 0:
                g[i] = data[1:]

        match = [-1] * (m + 1)

        def dfs(u, vis):
            for v in g[u]:
                if vis[v]:
                    continue
                vis[v] = True
                if match[v] == -1 or dfs(match[v], vis):
                    match[v] = u
                    return True
            return False

        for i in range(n):
            dfs(i, [False] * (m + 1))

        return str(m - sum(1 for x in match if x != -1))

    return solve()

# provided samples
assert run("""5 6
2 1 2
0
1 3
1 4
2 1 5
""") == "2"

assert run("""5 5
1 1
1 2
1 3
1 4
1 5
""") == "0"

# custom tests
assert run("""1 3
2 1 2
""") == "2", "single person"

assert run("""3 3
1 1
1 1
1 1
""") == "2", "conflict single target"

assert run("""2 2
1 1
1 2
""") == "0", "perfect matching"

assert run("""2 3
0
0
""") == "3", "no assignments"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single person | 2 | basic assignment |
| all want same company | 2 | conflict handling |
| perfect matching | 0 | optimal full assignment |
| no assignments | 3 | empty preference handling |

## Edge Cases

A key edge case is when multiple people list the same single company. In that situation, a naive greedy approach assigns the first person and blocks others, but the DFS-based matching ensures only one final assignment remains and correctly counts the rest as unassigned.

Another edge case is people with empty preference lists. These nodes do not participate in any matching attempt, and the DFS naturally skips them without affecting correctness. The algorithm still counts unassigned companies properly because matching size depends only on successful assignments.

A final edge case arises when preference lists are large and highly overlapping, creating long augmenting paths. The recursive DFS handles these chains correctly by repeatedly reassigning along alternating paths until a free company is reached, ensuring no locally optimal but globally suboptimal configuration remains.
