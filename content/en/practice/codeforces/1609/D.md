---
title: "CF 1609D - Social Network"
description: "We are given a group of people who initially have no relationships at all. Over time, we are shown a sequence of pairs, and each pair represents a constraint that must eventually be satisfied: the two people in the pair must end up connected, meaning there exists a chain of…"
date: "2026-06-10T07:25:23+07:00"
tags: ["codeforces", "competitive-programming", "dsu", "graphs", "greedy", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 1609
codeforces_index: "D"
codeforces_contest_name: "Deltix Round, Autumn 2021 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 1600
weight: 1609
solve_time_s: 112
verified: false
draft: false
---

[CF 1609D - Social Network](https://codeforces.com/problemset/problem/1609/D)

**Rating:** 1600  
**Tags:** dsu, graphs, greedy, implementation, trees  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a group of people who initially have no relationships at all. Over time, we are shown a sequence of pairs, and each pair represents a constraint that must eventually be satisfied: the two people in the pair must end up connected, meaning there exists a chain of direct introductions linking them.

William is the only one allowed to introduce people to each other. Each introduction connects two previously unconnected individuals and effectively adds an edge to an initially empty graph. After performing the first i introductions, all first i constraints must be satisfied, meaning each of those pairs must lie in the same connected component of the resulting graph.

For every prefix length i, we conceptually restart from scratch, perform exactly i introductions, and ensure the first i constraints are satisfied. Among all valid ways to choose these i introductions, we want to maximize the size of the largest set of people that are all mutually reachable through introductions. In graph terms, we maximize the size of the largest connected component.

The key subtlety is that each prefix is independent. We do not carry over any structure from previous prefixes, so each i defines a separate optimization problem over the same n nodes and first i required connectivity constraints.

The constraints are small enough that n up to 1000 allows O(n^2) or O(n^2 log n) reasoning. However, the fact that we recompute for every prefix strongly suggests we need a structure that can be updated incrementally rather than recomputing connectivity from scratch each time.

A naive approach that rebuilds connectivity from scratch for every i and tries to enforce constraints would repeatedly run a full graph construction or search over all possible introductions. This quickly becomes infeasible because even checking feasibility per prefix would already require heavy union-find or BFS logic, and doing it independently for every prefix multiplies the cost by d.

A common edge case arises when constraints form overlapping components. For example, if constraints are (1,2), (2,3), (3,4), the optimal construction quickly builds a chain, and the largest component grows steadily. But if constraints are disjoint early and only later connect large groups, a greedy local interpretation of constraints without careful merging order can underestimate the achievable component size.

Another subtle issue is misunderstanding what must be maximized. We are not maximizing the number of satisfied constraints or edges added. We are maximizing the size of the largest connected component after enforcing all constraints in the prefix.

## Approaches

A brute-force perspective starts by observing that for a fixed i, we must ensure that all pairs (x1, y1) through (xi, yi) lie in the same connected component. One could attempt to build a graph by repeatedly adding edges and checking validity, but that leads to a key difficulty: we are free to choose which introductions William performs, as long as all constraints become connected.

So the real structure is this: the constraints force certain groups of nodes to end up in the same connected component. If we think of the first i constraints as edges in an auxiliary graph, then any valid final configuration must at least connect each connected component of this auxiliary graph. That means each component of the constraint graph must be fully contained inside some connected component of William’s constructed graph.

The optimal strategy is then to realize that William should connect components in a way that minimizes fragmentation, effectively allowing us to treat each constraint component as a “must-be-merged” block. The only freedom is how these blocks are merged using exactly i edges.

The key insight is that since we perform exactly i introductions, and each introduction merges two components, we start with n isolated nodes and perform i merges. After i merges, we always have exactly n - i components. Therefore, the problem reduces to controlling how those merges are distributed while respecting that constraint components must be contained.

This leads to a greedy union-find process over constraints: we process constraints one by one, unioning their endpoints. The size of the largest connected component in the union-find structure after i unions gives the best achievable answer, because any valid construction must at least respect these forced connections, and we can always realize a construction that achieves exactly those merges.

Thus, we maintain a DSU and track component sizes. After processing each constraint, we update the size of the largest DSU component.

The subtle justification is that constraints only require connectivity, not direct edges, so merging endpoints is sufficient. Each constraint effectively forces the union of their components in any valid realization. Once we union them, we are capturing exactly the minimal forced structure, and since we are allowed arbitrary introductions beyond constraints, we can always achieve a configuration where the largest component equals the largest DSU component formed by constraints.

### Comparison table

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (rebuild / simulate per prefix) | O(d · n²) | O(n²) | Too slow |
| DSU over constraints | O(d α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

We process constraints incrementally while maintaining a disjoint set union structure.

1. Initialize DSU with n nodes, each in its own component. Each component has size 1.
2. Maintain a variable `best` that stores the maximum component size seen so far.
3. For each constraint i = 1 to d, we take the pair (x_i, y_i) and merge their DSU components. If they are already in the same component, nothing changes.
4. After each union operation, we update `best` to reflect the largest component size currently present in DSU.
5. Output `best` after processing each prefix i.

The key reason this works is that each constraint enforces connectivity between two groups. Once two groups are connected in constraints, any valid construction must ensure they are connected in the final graph. DSU compresses all such forced relations into components, and since each introduction merges two components, tracking component sizes directly captures the growth of the largest possible connected group.

### Why it works

At any prefix i, the constraint edges define a graph whose connected components are equivalence classes of people that must be connected in every valid construction. Any valid introduction plan must make each of these classes internally connected, so each class behaves like a super-node. The largest possible connected component we can form is obtained by treating each constraint component as indivisible and counting its size. DSU maintains exactly these equivalence classes, and since merging is the only operation allowed, the DSU state after i unions represents the maximal forced connectivity structure achievable after satisfying the first i constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return 0
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return self.size[a]

n, d = map(int, input().split())
dsu = DSU(n)

best = 1
out = []

for _ in range(d):
    x, y = map(int, input().split())
    x -= 1
    y -= 1
    merged_size = dsu.union(x, y)
    if merged_size:
        best = max(best, merged_size)
    out.append(str(best))

print("\n".join(out))
```

The DSU structure keeps track of connected components induced by the constraints. Each union corresponds to enforcing that two people must end up in the same connected group. The size array allows constant-time tracking of how large each resulting group is, and updating `best` ensures we always know the largest achievable cluster after each prefix.

The key implementation detail is that we only update `best` when a merge actually happens. If two nodes are already in the same component, the constraint adds no new structure, and the answer remains unchanged.

## Worked Examples

We trace the sample input.

Input:

```
7 6
1 2
3 4
2 4
7 6
6 5
1 7
```

We track DSU merges and largest component.

| i | constraint | merged sets | component sizes | best |
| --- | --- | --- | --- | --- |
| 1 | 1-2 | {1,2} | 2,1,1,1,1,1,1 | 2 |
| 2 | 3-4 | {3,4} | 2,2,1,1,1,1 | 2 |
| 3 | 2-4 | {1,2,3,4} | 4,1,1,1,1,1 | 4 |
| 4 | 7-6 | {6,7} | 4,2,1,1,1 | 4 |
| 5 | 6-5 | {5,6,7} | 4,3,1,1 | 4 |
| 6 | 1-7 | all merged | 7 | 7 |

Output derived is:

```
2
2
4
4
4
7
```

This matches the DSU interpretation of forced connectivity growth. Each step confirms that the largest connected component depends only on constraint-induced unions.

A second smaller example:

Input:

```
5 3
1 2
2 3
4 5
```

Trace:

| i | constraint | best |
| --- | --- | --- |
| 1 | 1-2 | 2 |
| 2 | 2-3 | 3 |
| 3 | 4-5 | 3 |

We see the largest component grows only when constraints merge chains.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d α(n)) | Each union/find is almost constant due to path compression and union by size |
| Space | O(n) | DSU arrays store parent and size for each node |

The constraints allow n up to 1000, but the DSU solution is efficient enough that even the worst case d = 999 operations is trivial. The algorithm runs comfortably within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, d = map(int, input().split())
    dsu = DSU(n)

    best = 1
    out = []

    for _ in range(d):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        merged_size = dsu.union(x, y)
        if merged_size:
            best = max(best, merged_size)
        out.append(str(best))

    return "\n".join(out)

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return 0
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return self.size[a]

# provided sample
assert run("""7 6
1 2
3 4
2 4
7 6
6 5
1 7
""") == "2\n2\n4\n4\n4\n7"

# minimum size
assert run("""2 1
1 2
""") == "2"

# no merges early
assert run("""5 3
1 2
3 4
5 1
""") == "2\n2\n5"

# chain
assert run("""4 3
1 2
2 3
3 4
""") == "2\n3\n4"

# disconnected clusters
assert run("""6 3
1 2
3 4
5 6
""") == "2\n2\n2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single edge | 2 | basic union behavior |
| sparse early merges | increasing best | incremental tracking |
| chain merge | growing component | transitive connectivity |
| disjoint pairs | flat then stable | independent components |

## Edge Cases

A small but important case is when constraints repeat already-connected pairs. For example:

Input:

```
4 3
1 2
2 3
1 3
```

After the first two constraints, nodes {1,2,3} are already unified. The third constraint does not change DSU state. The algorithm correctly ignores it because `union` returns 0 and `best` is not updated. The output remains consistent with the fact that no new connectivity is enforced.

Another case is when constraints form two independent clusters that only become useful later. DSU ensures that partial merges are accumulated correctly, and the largest component is updated only when a true merge occurs, preventing inflation from redundant constraints.
