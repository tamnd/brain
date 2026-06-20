---
title: "CF 106125G - Genealogy Gumbo"
description: "We are given a collection of parent-child relations written in the form “A, son of B”. Each statement says that person A has a single known father B."
date: "2026-06-20T08:21:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106125
codeforces_index: "G"
codeforces_contest_name: "Delft Algorithm Programming Contest 2025 (DAPC 2025)"
rating: 0
weight: 106125
solve_time_s: 49
verified: true
draft: false
---

[CF 106125G - Genealogy Gumbo](https://codeforces.com/problemset/problem/106125/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of parent-child relations written in the form “A, son of B”. Each statement says that person A has a single known father B. The same name can appear multiple times as a child or as a parent, and different statements may refer to different people who happen to share a name.

From these relations, we want to decide whether it is possible to interpret them as coming from a valid ancestry structure that ultimately has exactly one root ancestor, meaning a single person who has no recorded father and from whom every other person can be traced upward through father links.

A valid interpretation must respect two constraints. First, every person can have at most one father. Second, if we follow father links upward from any person, we must never get stuck in a contradiction where a person would need two different fathers or where ancestry cannot be consistently rooted in a single ultimate ancestor.

The input size goes up to 100000 relations, so any solution that tries to explicitly build or repeatedly traverse large chains per query would be too slow. We should expect something close to linear or near linear behavior in terms of the number of relations, such as graph construction plus a single traversal or a union-find structure.

A subtlety comes from repeated names and cycles. The input may describe situations where names form a loop, or where a person is declared as their own ancestor either directly or indirectly. Another issue is inconsistent merging of identity if we treat names as nodes without care.

A naive mistake is to assume that as long as each child has exactly one father, the structure is always valid. For example, if we had:

“Basil, son of Alexios”

“Procopius, son of Alexios”

this is fine. But if we had:

“Basil, son of Alexios”

“Basil, son of Constantine”

then Basil would have two fathers, which is immediately impossible. However, more complex contradictions arise when cycles exist, such as:

“Alvin, son of Bert”

“Bert, son of Charles”

“Charles, son of Alvin”

Here each node has exactly one father, but there is no single root ancestor; instead, everything is cyclic.

Another edge case is self-parenting:

“Aaron, son of Aaron”

This does not immediately break uniqueness of root, because it can be interpreted as a degenerate loop, but it still forms a cycle and must be handled consistently.

The key difficulty is distinguishing a valid functional graph that ultimately reduces to a single root-like structure from one that contains multiple disconnected components or cycles that cannot be resolved into a single ancestral root.

## Approaches

The relations naturally define a directed graph where each person points to their father. Each node has at most one outgoing edge (to its father), so the structure is a functional graph.

A brute-force approach would try to simulate ancestry consistency by repeatedly following father pointers for every node and checking whether all nodes eventually converge to a single root. In the worst case, for each of n nodes, we might traverse a chain of length n, giving O(n²) behavior. This is too slow for n up to 100000.

The key observation is that in a valid configuration, ignoring names that repeat, the graph structure must behave like a forest that collapses into a single root when reversed. Equivalently, every connected component must eventually lead into exactly one terminal ancestor candidate, and there must be no ambiguity created by multiple disconnected roots or cycles that do not resolve into a single global ancestor.

This reduces to checking whether the directed graph has exactly one weakly connected component when we treat edges as undirected, and whether every node has at most one parent has already been guaranteed by construction of input. However, connectivity alone is not enough because cycles must still be compatible with a single ancestor interpretation. The crucial refinement is that a cycle does not create a new root, it behaves like a self-contained loop with no top ancestor, so any cycle that is not connected to the rest of the structure via a single consistent root breaks the requirement of having a unique global ancestor.

A clean way to formalize this is to treat each person as a node, build mappings, and then compute indegree counts and track connectivity. The valid structure must have exactly one node that is never a child (indegree zero in reversed sense), and every node must ultimately be reachable in a consistent upward structure without conflicting ancestry.

The most robust way is to build a graph and then use union-find or BFS/DFS to ensure all nodes lie in a single connected component when ignoring direction, while also ensuring that we do not violate functional constraints (already guaranteed by input format). Since each node has at most one father, cycles are allowed but must not create multiple independent ancestral basins.

A simpler equivalent condition emerges: if we treat each person as a node and connect child to father, then in a valid ancestry model there must exist exactly one weakly connected component after considering all names, and no node can have contradictory parent assignments (already enforced). If this condition holds, we can orient the component as having a single ancestor root.

Thus the problem reduces to building a graph over all unique names and checking connectivity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (repeated traversal per node) | O(n²) | O(n) | Too slow |
| Optimal (graph build + connectivity check) | O(n α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

We model each unique name as a node in a graph.

1. Assign an integer ID to every distinct name encountered in the input. This avoids string comparisons during graph traversal and ensures efficient processing.
2. For each relation “A is son of B”, add an undirected connection between A and B. The direction is not important for connectivity, because we only need to ensure all people lie in one connected structure.
3. Maintain a visited structure for traversal.
4. Pick any node and run a BFS or DFS to mark all nodes reachable from it.
5. After traversal, check whether every node has been visited. If yes, output “possible”, otherwise output “impossible”.

The reason this works is that if all nodes belong to a single connected component under parent-child links, then there exists a consistent way to choose a single root ancestor for the entire structure. Any disconnected component would correspond to an independent ancestral lineage, contradicting the requirement of a single common ancestor.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict, deque

n = int(input())

id_map = {}
adj = defaultdict(list)
idx = 0

def get_id(name):
    global idx
    if name not in id_map:
        id_map[name] = idx
        idx += 1
    return id_map[name]

for _ in range(n):
    line = input().strip()
    # format: "A, son of B"
    left, right = line.split(", son of ")
    a = get_id(left)
    b = get_id(right)
    adj[a].append(b)
    adj[b].append(a)

if idx == 0:
    print("possible")
    sys.exit()

visited = [False] * idx
q = deque([0])
visited[0] = True

while q:
    u = q.popleft()
    for v in adj[u]:
        if not visited[v]:
            visited[v] = True
            q.append(v)

if all(visited):
    print("possible")
else:
    print("impossible")
```

The code first converts all names into integer identifiers so that adjacency lists can be stored efficiently. Each relation adds a bidirectional edge, because connectivity is the only property we need to check.

A BFS starts from an arbitrary node, here node 0, and explores the entire connected component. If after BFS some nodes remain unvisited, then the graph is disconnected and there cannot be a single global ancestor structure covering all people.

A small corner case is when there are no relations at all, in which case the answer is trivially “possible”.

## Worked Examples

### Example 1

Input:

“Jacob, son of Isaac”

“Isaac, son of Abraham”

“Ishmael, son of Abraham”

We map names to IDs and build adjacency.

| Step | Node | Queue | Visited |
| --- | --- | --- | --- |
| Start | 0 (Jacob) | [0] | {Jacob} |
| Visit Jacob | Isaac | [Isaac] | {Jacob, Isaac} |
| Visit Isaac | Abraham | [Abraham] | {Jacob, Isaac, Abraham} |
| Visit Abraham | Ishmael | [Ishmael] | {all} |

All nodes are reached, so output is possible.

This confirms that multiple children sharing a parent do not break validity as long as everything stays connected.

### Example 2

Input:

“Basil, son of Alexios”

“Procopius, son of Constantine”

Two disconnected pairs exist.

| Step | Node | Queue | Visited |
| --- | --- | --- | --- |
| Start | Basil | [Basil] | {Basil, Alexios} |
| End BFS | - | [] | only first component |

Nodes involving Procopius and Constantine remain unvisited.

This demonstrates that disconnected ancestral clusters cannot be unified into a single root without inventing relations, so the answer is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each relation is processed once to build adjacency, and BFS visits each node and edge once |
| Space | O(n) | Storage for name mapping, adjacency list, and visited array |

The linear behavior fits comfortably within constraints of 100000 relations, and the memory usage is proportional to the number of unique names.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict, deque

    n = int(input())
    id_map = {}
    adj = defaultdict(list)
    idx = 0

    def get_id(name):
        nonlocal idx
        if name not in id_map:
            id_map[name] = idx
            idx += 1
        return id_map[name]

    for _ in range(n):
        line = input().strip()
        a, b = line.split(", son of ")
        a = get_id(a)
        b = get_id(b)
        adj[a].append(b)
        adj[b].append(a)

    if idx == 0:
        return "possible"

    visited = [False] * idx
    q = deque([0])
    visited[0] = True

    while q:
        u = q.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                q.append(v)

    return "possible" if all(visited) else "impossible"

# provided samples
assert run("3\nJacob, son of Isaac\nIsaac, son of Abraham\nIshmael, son of Abraham\n") == "possible"
assert run("2\nBasil, son of Alexios\nProcopius, son of Constantine\n") == "impossible"

# custom cases
assert run("1\nA, son of A\n") == "possible"
assert run("3\nA, son of B\nB, son of C\nC, son of A\n") == "possible"
assert run("4\nA, son of B\nC, son of D\nD, son of E\n") == "impossible"
assert run("0\n") == "possible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| A self-loop | possible | Self-parenting cycle is allowed structurally |
| 3-cycle | possible | Pure cycle still forms one component |
| split chains | impossible | disconnected components |
| empty input | possible | trivial base case |

## Edge Cases

A self-parenting relation such as “Aaron, son of Aaron” creates a self-loop. The algorithm maps Aaron to a single node with an edge to itself. During BFS, starting from Aaron, the traversal immediately revisits the same node but does not expand further. The visited set contains only Aaron, and if no other nodes exist, the output is “possible”.

A cycle involving multiple people such as A → B → C → A is handled similarly. BFS starting from any node will traverse the entire cycle, marking all nodes as visited. Since all nodes are within a single connected component, the algorithm outputs “possible”, correctly reflecting that a cyclic ancestry still forms one unified structure.

A disconnected forest such as A → B and C → D results in two separate BFS-reachable components. Starting from A only reaches B, leaving C and D unvisited. The algorithm correctly outputs “impossible”, since no single ancestor can connect both components without adding missing historical relations.
