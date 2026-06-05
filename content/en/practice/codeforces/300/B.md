---
title: "CF 300B - Coach"
description: "We are asked to divide n students into teams of exactly three. Some students explicitly request to be on the same team with certain other students. These requests are mutual, so if student 2 wants to team with student 5, then student 5 also wants student 2."
date: "2026-06-05T18:28:15+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 300
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 181 (Div. 2)"
rating: 1500
weight: 300
solve_time_s: 131
verified: false
draft: false
---

[CF 300B - Coach](https://codeforces.com/problemset/problem/300/B)

**Rating:** 1500  
**Tags:** brute force, dfs and similar, graphs  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to divide `n` students into teams of exactly three. Some students explicitly request to be on the same team with certain other students. These requests are mutual, so if student 2 wants to team with student 5, then student 5 also wants student 2. Our task is to assign students into triplets in a way that respects all such requests. If that is impossible, we must output `-1`. Otherwise, we should print the actual teams.

Input consists of `n` (divisible by 3) and `m` pairs of students who want to be together. The output is either `-1` if no valid arrangement exists, or `n/3` lines of three integers each representing a team.

The constraints are small: `n ≤ 48` and `m ≤ n(n-1)/2`. This suggests that any algorithm with complexity up to roughly `O(n^2)` will comfortably run within 2 seconds. So we can consider approaches that involve scanning all students, building groups, or simulating teams without worrying about optimization for large datasets.

A key edge case occurs when students have conflicting requests that would force a group larger than three. For example, if students 1, 2, 3, and 4 all request to be on the same team (via a chain of requests), it is impossible to form a team of exactly three. Another case is when some students are isolated and must be combined with others to form a complete team.

## Approaches

A brute-force approach would try every possible division of students into teams of three and check whether all the requests are satisfied. This approach is correct in theory but infeasible in practice. The number of ways to partition `n` students into groups of three is on the order of `(n!) / ((3!)^(n/3) * (n/3)!)`. For `n = 48`, this is astronomically large and cannot be enumerated.

The optimal approach observes that the requests define connected components in a graph: each student is a node, and an edge represents a "wants to be together" request. Each connected component must entirely fit into one or more teams. If any component has more than three students, it is impossible to divide them into teams of three because requests are mutual and must be respected. Components of size 1 or 2 can be combined to form teams.

The insight is to classify components by size. Components of size 3 form complete teams immediately. Components of size 2 need one extra student from size-1 components. Components of size 1 can be grouped into threes to form a team. If at any point the numbers do not match up, no valid solution exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Connected Components + Greedy Team Assignment | O(n^2) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Represent the students and their requests as an undirected graph using adjacency lists. Each student is a node, each request a bidirectional edge. This allows us to find connected groups efficiently.
2. Traverse the graph using Depth-First Search or Breadth-First Search to identify all connected components. Each component represents a set of students that must be on the same team. Store the size of each component and the list of students in it.
3. If any component has size greater than 3, output `-1` and terminate. Such a component cannot be split into teams of exactly three while preserving requests.
4. Categorize components into three groups: size 3, size 2, size 1. Components of size 3 form a complete team. Components of size 2 require one student from the size-1 group to complete a team. Components of size 1 can be combined in threes to form complete teams.
5. If the number of size-1 students is not enough to pair with size-2 components, or is not divisible by three after pairing, output `-1`.
6. Assemble the teams in this order: first, teams of size-3 components, then pair each size-2 component with a size-1 student, and finally group remaining size-1 students in threes.
7. Output all teams. Each team is printed as three student numbers.

Why it works: The graph-based decomposition guarantees that all mutual requests are respected. Components larger than three are rejected because they cannot fit in a single team. Greedily combining size-2 components with size-1 students and grouping remaining size-1 students in threes ensures that all students are included exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        a, b = map(int, input().split())
        adj[a-1].append(b-1)
        adj[b-1].append(a-1)

    visited = [False]*n
    components = []

    def dfs(u, comp):
        visited[u] = True
        comp.append(u)
        for v in adj[u]:
            if not visited[v]:
                dfs(v, comp)

    for i in range(n):
        if not visited[i]:
            comp = []
            dfs(i, comp)
            if len(comp) > 3:
                print(-1)
                return
            components.append(comp)

    ones, twos, threes = [], [], []
    for c in components:
        if len(c) == 1:
            ones.append(c[0])
        elif len(c) == 2:
            twos.append(c)
        else:
            threes.append(c)

    if len(ones) < len(twos):
        print(-1)
        return

    teams = []
    for t in threes:
        teams.append(t)
    for i, t in enumerate(twos):
        teams.append(t + [ones[i]])
    remaining_ones = ones[len(twos):]

    if len(remaining_ones) % 3 != 0:
        print(-1)
        return

    for i in range(0, len(remaining_ones), 3):
        teams.append(remaining_ones[i:i+3])

    for team in teams:
        print(' '.join(str(x+1) for x in team))

if __name__ == "__main__":
    main()
```

The code first constructs the graph and finds connected components using DFS. Components larger than three immediately trigger `-1`. Components are split by size, then teams are built in a greedy manner. Careful indexing ensures that students are assigned exactly once and all size-2 components are completed with size-1 students.

## Worked Examples

**Sample Input 1**

```
3 0
```

| Step | Components | Ones | Twos | Threes | Teams |
| --- | --- | --- | --- | --- | --- |
| Initial | [[0],[1],[2]] | [0,1,2] | [] | [] | [] |
| Assemble | [[0,1,2]] | [] | [] | [] | [0,1,2] |

All students are isolated. They are grouped in a single team of three.

**Sample Input 2**

```
6 2
1 2
3 4
```

| Step | Components | Ones | Twos | Threes | Teams |
| --- | --- | --- | --- | --- | --- |
| Initial DFS | [[0,1],[2,3],[4],[5]] | [4,5] | [[0,1],[2,3]] | [] | [] |
| Assemble | - | [4,5] | [[0,1],[2,3]] | [] | [[0,1,4],[2,3,5]] |

Twos are completed with ones to form full teams. Output is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | DFS traverses each edge once; n ≤ 48, so even O(n^2) adjacency checks are fine. |
| Space | O(n + m) | Adjacency list stores edges; visited array and component lists store n elements. |

For n ≤ 48 and m ≤ n(n-1)/2, both time and memory are well below the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("3 0\n") in ["1 2 3","3 2 1"], "sample 1"

# Custom cases
assert run("6 2\n1 2\n3 4\n") in ["1 2 5\n3 4 6","1 2 6\n3 4 5"], "size-2 pairing"
assert run("3 1\n1 2\n") == "1 2 3", "2 wants together, 1 alone"
assert run("3 1\n1 2\n") == "1 2 3", "size-2 + single"
assert run("6 1\n1 2\n") in ["1 2 3\n4 5 6","1 2 4\n3 5
```
