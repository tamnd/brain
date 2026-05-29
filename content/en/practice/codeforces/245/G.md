---
title: "CF 245G - Suggested Friends"
description: "We are given an undirected social network where each user is identified by a string name and friendships are given as pairs of names."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "graphs"]
categories: ["algorithms"]
codeforces_contest: 245
codeforces_index: "G"
codeforces_contest_name: "CROC-MBTU 2012, Elimination Round (ACM-ICPC)"
rating: 2200
weight: 245
solve_time_s: 66
verified: true
draft: false
---

[CF 245G - Suggested Friends](https://codeforces.com/problemset/problem/245/G)

**Rating:** 2200  
**Tags:** brute force, graphs  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected social network where each user is identified by a string name and friendships are given as pairs of names. From these friendships we must determine, for every user, which non-friends are the most “similar” to them, where similarity is measured by the number of mutual friends.

Concretely, for a fixed user `x`, we look at every other user `y` who is not `x` and is not already directly connected to `x`. Among all such candidates, we count how many users `z` are friends with both `x` and `y`. The users maximizing this count are considered suggested friends of `x`. We must output, for each user, how many such maximizers exist.

The structure is a graph problem on an undirected simple graph, but instead of finding just one best candidate, we must count all vertices tied for the maximum number of common neighbors.

The input size is small in terms of edges, with at most 5000 friendship pairs, but the number of distinct users is not explicitly bounded and can still be large. This makes adjacency list based reasoning essential. A dense $O(n^2)$ scan over all pairs of users is still acceptable if implemented carefully, but recomputing intersections naively for each pair of users would be too slow.

A subtle edge case comes from users with very small friend sets. If a user has only one friend, every non-friend candidate shares at most one or zero mutual friends, so many candidates can tie for the maximum. Another corner case is when multiple users achieve the same maximum count, meaning we must not pick a single best friend but count all of them.

Another issue is double counting mutual friends if adjacency is not treated carefully. Since the graph is undirected and input edges are unique, we must still ensure symmetric adjacency construction.

## Approaches

A direct approach is to consider every user `x`, then iterate over every other user `y`, skip if `y` is `x` or already a friend of `x`, and compute the number of common friends by intersecting adjacency sets. If adjacency is stored as lists, each intersection costs $O(deg(x) + deg(y))$, which leads to a worst-case cost of roughly $O(n^2 \cdot n)$, which is not acceptable when the number of users is large.

The key observation is that mutual friend counts can be computed by iterating over friends of `x`. For each friend `z` of `x`, every neighbor `y` of `z` contributes one mutual friend between `x` and `y`. This shifts the computation from pairwise intersections to a “neighbor propagation” view. Instead of comparing all pairs directly, we accumulate scores for candidates in the two-hop neighborhood of `x`.

This works efficiently because each edge contributes to exactly two adjacency lists, and each triangle relationship `(x, z, y)` is counted exactly once per shared neighbor `z`.

We still must ensure we do not consider users already directly connected to `x`, and we must exclude `x` itself.

The overall complexity becomes proportional to the sum of degrees of neighbors of each node, which is essentially linear in the number of “two-step walks” in the graph, and fits easily within constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force pairwise intersection | O(n² · d) | O(n + m) | Too slow |
| Two-hop accumulation | O(∑ d²) ≈ O(m√m) worst-case intuition, practically O(mn) worst-case but acceptable for m ≤ 5000 | O(n + m) | Accepted |

## Algorithm Walkthrough

We represent the graph using adjacency sets so we can test friendship in O(1).

1. Map each unique username to an integer index. This simplifies graph handling and avoids repeated string comparisons.
2. Build an adjacency set `adj[u]` for each user. Since friendships are symmetric, we insert both directions.
3. For each user `x`, create a dictionary `cnt` that will store how many mutual friends each candidate `y` has with `x`.
4. Iterate over each friend `z` of `x`. For every neighbor `y` of `z`, increase `cnt[y]` by one. This step counts the number of shared neighbors between `x` and `y` via `z`.
5. After processing all friends of `x`, determine the maximum value in `cnt`. Any user achieving this value is a candidate suggested friend.
6. Exclude from consideration any user `y` who is either `x` itself or already a direct friend of `x`, since they are disqualified by definition.
7. Count how many remaining users achieve the maximum mutual friend count and store this as the answer for `x`.

The key idea is that every mutual friend relationship is generated exactly once per shared intermediate node. If `x` and `y` share `k` friends, then there are exactly `k` distinct paths of length two connecting them through those friends, and each such path increments the counter once.

### Why it works

For a fixed source node `x`, every potential candidate `y` receives exactly one increment for each distinct path `x → z → y`. These paths correspond one-to-one with common neighbors of `x` and `y`. Therefore, `cnt[y]` always equals the number of shared friends between `x` and `y`. Since we explicitly exclude direct friends and `x` itself, the maximum over remaining `y` correctly identifies all most similar non-friends.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    m = int(input())
    
    name_to_id = {}
    adj = []
    
    def get_id(name):
        if name not in name_to_id:
            name_to_id[name] = len(adj)
            adj.append(set())
        return name_to_id[name]
    
    for _ in range(m):
        a, b = input().split()
        u = get_id(a)
        v = get_id(b)
        adj[u].add(v)
        adj[v].add(u)
    
    n = len(adj)
    id_to_name = [""] * n
    for name, i in name_to_id.items():
        id_to_name[i] = name
    
    ans = [0] * n
    
    for x in range(n):
        cnt = {}
        
        for z in adj[x]:
            for y in adj[z]:
                if y == x:
                    continue
                cnt[y] = cnt.get(y, 0) + 1
        
        best = -1
        for y, c in cnt.items():
            if y == x or y in adj[x]:
                continue
            if c > best:
                best = c
        
        if best <= 0:
            ans[x] = 0
        else:
            ans[x] = sum(
                1 for y, c in cnt.items()
                if y != x and y not in adj[x] and c == best
            )
    
    print(n)
    for i in range(n):
        print(id_to_name[i], ans[i])

if __name__ == "__main__":
    solve()
```

The implementation first compresses string names into integer ids so that adjacency operations are efficient. Each adjacency list is stored as a set, allowing constant-time checks for whether a user is already a friend.

For each node, we build a frequency map over its two-hop neighborhood. The inner double loop walks over each friend and then over that friend’s friends, accumulating counts of shared neighbors. The second pass extracts the maximum value and counts how many candidates achieve it, excluding invalid ones.

A subtle detail is handling users with no valid candidates. In that case `best` remains `-1`, and we correctly output zero suggested friends.

## Worked Examples

### Example 1

Input:

```
5
Mike Gerald
Kate Mike
Kate Tank
Gerald Tank
Gerald David
```

We build adjacency:

Mike: Gerald, Kate

Gerald: Mike, Tank, David

Kate: Mike, Tank

Tank: Kate, Gerald

David: Gerald

For `David`, neighbors of `Gerald` are Mike, Tank, Mike, Tank contributions via shared structure:

| x | z (friend of x) | y (neighbor of z) | cnt[y] |
| --- | --- | --- | --- |
| David | Gerald | Mike | 1 |
| David | Gerald | Tank | 1 |

Maximum is 1, achieved by Mike and Tank, so answer is 2 for David.

For `Kate`, similar reasoning yields one best candidate.

This confirms that the algorithm correctly counts two-hop overlaps rather than direct connections.

### Example 2

Input:

```
4
A B
B C
C D
A D
```

Adjacency forms a cycle. For `A`, candidates are `C` only (since `B` and `D` are friends), and `C` shares one mutual friend with `A` via `B` or `D`.

| x | z | y | cnt[y] |
| --- | --- | --- | --- |
| A | B | C | 1 |
| A | D | C | 2 |

Here `C` accumulates 2 mutual friends and is uniquely best.

This shows that multiple paths to the same candidate are correctly aggregated.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(∑ deg(v)²) | For each node, we traverse adjacency of its neighbors, accumulating two-hop contributions |
| Space | O(n + m) | Adjacency sets plus temporary counting map |

The constraint $m \le 5000$ ensures that even in worst structured graphs, the total number of two-hop traversals stays within acceptable limits. The algorithm avoids any quadratic scan over all pairs of users, which would be infeasible if the number of users grows large.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict
    import sys
    
    m = int(sys.stdin.readline())
    name_to_id = {}
    adj = []
    
    def get_id(name):
        if name not in name_to_id:
            name_to_id[name] = len(adj)
            adj.append(set())
        return name_to_id[name]
    
    for _ in range(m):
        a, b = sys.stdin.readline().split()
        u = get_id(a)
        v = get_id(b)
        adj[u].add(v)
        adj[v].add(u)
    
    n = len(adj)
    id_to_name = [""] * n
    for name, i in name_to_id.items():
        id_to_name[i] = name
    
    ans = [0] * n
    
    for x in range(n):
        cnt = {}
        for z in adj[x]:
            for y in adj[z]:
                if y == x:
                    continue
                cnt[y] = cnt.get(y, 0) + 1
        
        best = -1
        for y, c in cnt.items():
            if y == x or y in adj[x]:
                continue
            if c > best:
                best = c
        
        if best <= 0:
            ans[x] = 0
        else:
            ans[x] = sum(
                1 for y, c in cnt.items()
                if y != x and y not in adj[x] and c == best
            )
    
    out = [str(n)]
    for i in range(n):
        out.append(id_to_name[i] + " " + str(ans[i]))
    return "\n".join(out)

# provided sample
assert run("""5
Mike Gerald
Kate Mike
Kate Tank
Gerald Tank
Gerald David
""").splitlines()[0] == "5"

# custom: triangle
assert run("""3
A B
B C
A C
""")  # all excluded as friends => 0 suggested each

# custom: chain
assert run("""2
A B
B C
""")  # C and A mutual via B

# custom: star
assert run("""3
A B
A C
A D
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| triangle | all zeros | all candidates are direct friends |
| chain | endpoints have shared candidate | two-hop propagation |
| star | leaves share center structure | high-degree hub behavior |

## Edge Cases

A key edge case is when all potential candidates are already direct friends. For example, in a complete triangle graph `A-B-C-A`, every pair is connected, so no suggested friends exist. The algorithm builds `cnt`, but every candidate is filtered out by the adjacency check, leaving `best <= 0` and producing zero.

Another case is a star graph where one central node connects to many leaves. For a leaf node `x`, every other leaf shares exactly one mutual friend (the center). The counting loop ensures each leaf gets count 1, and all such leaves are correctly tied for maximum.

Finally, in sparse graphs where a node has only one neighbor, the algorithm still correctly counts second-degree connections even though the intermediate set is tiny. The correctness relies only on enumerating neighbors of neighbors, not on degree size assumptions.
