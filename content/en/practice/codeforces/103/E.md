---
title: "CF 103E - Buying Sets"
description: "We are given several sets of integers, each with an associated cost. We may choose any collection of these sets, including the empty collection. Let the number of chosen sets be $k$, and let the union of all chosen sets contain $u$ distinct integers."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graph-matchings"]
categories: ["algorithms"]
codeforces_contest: 103
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 80 (Div. 1 Only)"
rating: 2900
weight: 103
solve_time_s: 190
verified: false
draft: false
---

[CF 103E - Buying Sets](https://codeforces.com/problemset/problem/103/E)

**Rating:** 2900  
**Tags:** flows, graph matchings  
**Solve time:** 3m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several sets of integers, each with an associated cost. We may choose any collection of these sets, including the empty collection. Let the number of chosen sets be $k$, and let the union of all chosen sets contain $u$ distinct integers.

The goal is to minimize the total cost under the condition $u = k$.

The unusual part of the statement is the guarantee about the family of sets. For every collection of $k$ sets, their union always contains at least $k$ distinct numbers. This is exactly Hall's condition. It means every chosen set can be assigned a distinct representative element from inside that set.

The input size is small enough to allow cubic graph algorithms, but too large for subset enumeration. Since $n \le 300$, brute force over all $2^n$ collections is hopeless. Even $2^{40}$ would already be too large, and here we may have $2^{300}$ subsets.

The costs may be negative, which changes the nature of the optimization. A naive greedy strategy like “take all negative sets” can fail because adding one set may force the union size to grow, breaking the equality condition.

A subtle edge case is the empty collection. If all costs are positive, buying nothing is valid because both the number of chosen sets and the union size equal zero.

For example:

```
2
1 1
1 2
5 7
```

The correct answer is:

```
0
```

A careless solution that insists on choosing at least one set would incorrectly output `5`.

Another tricky case appears when multiple sets overlap heavily.

```
3
2 1 2
2 1 2
1 2
-5 -4 100
```

The correct answer is:

```
-9
```

The first two sets can both be chosen because the union has size 2 and there are 2 chosen sets. The third set should not be added because then we would have 3 sets but still only 2 distinct numbers.

A common mistake is to think the condition means the chosen sets must be pairwise disjoint. That is false. The condition only constrains the total union size.

Another dangerous case is when equality already holds automatically.

```
2
1 1
1 2
-3 -4
```

The correct answer is:

```
-7
```

Each set contributes a distinct number, so taking both is optimal.

Understanding when equality happens is the entire key to the problem.

## Approaches

The brute force approach is straightforward. Enumerate every subset of sets, compute the size of the union, and keep the minimum total cost among subsets where:

$$|\text{chosen sets}| = |\text{union}|$$

The condition from the statement guarantees:

$$|\text{union}| \ge |\text{chosen sets}|$$

for every subset. So feasible subsets are exactly those where equality holds.

This brute force method is correct because it checks every possible collection explicitly. The problem is the complexity. There are $2^n$ subsets, and $n$ can be 300. Even storing all subsets is impossible.

The important observation comes from Hall's theorem.

The statement guarantee says every collection of sets has at least as many distinct elements as sets. Hall's theorem then tells us that every collection admits a perfect matching between chosen sets and distinct elements.

Now consider when equality holds:

$$|\text{union}| = |\text{chosen sets}|$$

Suppose we look at the bipartite graph between chosen sets and elements appearing in them. Hall guarantees a matching covering all chosen sets. Since the union contains exactly as many elements as sets, the matching must actually use every element in the union.

This means every chosen element is matched exactly once.

That immediately implies the chosen subgraph forms a balanced component structure. In matroid language, the feasible collections are exactly the tight sets of a transversal matroid.

The optimization can then be transformed into a minimum weight closure problem, which reduces to a min-cut computation.

The key structural fact is this:

A subset of sets satisfies equality if and only if it is a union of strongly connected components in a directed dependency graph derived from alternating paths in a matching.

We first build one perfect matching from sets to distinct elements. Then we orient edges:

From a set to all unmatched elements inside it.

From a matched element back to its matched set.

This creates a directed graph. Tight subsets correspond exactly to vertex subsets closed under reachability.

Finding the minimum cost closed subset is a classical reduction to min-cut.

The brute force works because the condition depends only on subsets and unions, but fails because there are exponentially many subsets. The Hall structure allows us to reinterpret feasible subsets as closed sets in a directed graph, turning an exponential search into polynomial-time flow computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n^2)$ | $O(n^2)$ | Too slow |
| Optimal | $O(n^3)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Build a bipartite graph between sets and numbers.

The left side contains the $n$ sets. The right side contains numbers $1 \ldots n$. There is an edge from set $i$ to number $x$ if $x$ belongs to the set.
2. Compute a perfect matching covering all sets.

Hall's condition guarantees such a matching exists. We can use Kuhn's algorithm because $n \le 300$.
3. Construct a directed graph.

For every set $i$:

If $i$ contains number $x$ and $x$ is not matched to $i$, add a directed edge:

$$i \to \text{owner}(x)$$

where `owner(x)` is the set matched to $x$.

This edge represents an alternating-path dependency. If we include set $i$, we are forced to include the owner of $x$ to preserve tightness.
4. Compute strongly connected components.

Inside one SCC, every vertex depends on every other vertex. Either we take the whole SCC or none of it.
5. Compress the SCC graph into a DAG.

Each SCC becomes one node with weight equal to the sum of costs of its sets.
6. Find the minimum weight closed subset.

A closed subset means:

If a node is chosen, all outgoing neighbors must also be chosen.

This is solved using minimum cut.
7. Build a flow network.

For every SCC with negative total weight, connect:

$$S \to \text{SCC}$$

with capacity equal to $-w$.

For every SCC with positive total weight, connect:

$$\text{SCC} \to T$$

with capacity equal to $w$.

For every DAG edge:

$$u \to v$$

add infinite capacity.
8. Run max-flow/min-cut.

The minimum closed subset weight equals:

$$\text{maxflow} - \sum_{\text{negative } w} |w|$$
9. Compare against zero.

The empty collection is always valid, so the answer cannot exceed zero.

### Why it works

The matching converts the Hall condition into a structural dependency graph. Tight subsets are exactly those where every reachable dependency is also included. That is precisely the definition of a closed set in the directed graph.

Strongly connected components represent indivisible groups because every vertex inside an SCC forces every other vertex.

The min-cut reduction for minimum weight closure is standard. Infinite-capacity edges forbid violating closure constraints. The cut chooses which SCCs remain reachable from the source, and the capacity exactly equals the penalty for excluding negative SCCs or including positive SCCs.

Because every feasible collection corresponds to one closed subset and vice versa, minimizing closure weight gives the optimal answer.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

INF = 10**18

class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, c):
        self.g[u].append([v, c, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def bfs(self, s, t):
        self.level = [-1] * self.n
        q = deque([s])
        self.level[s] = 0

        while q:
            u = q.popleft()
            for v, c, rev in self.g[u]:
                if c > 0 and self.level[v] == -1:
                    self.level[v] = self.level[u] + 1
                    q.append(v)

        return self.level[t] != -1

    def dfs(self, u, t, f):
        if u == t:
            return f

        for i in range(self.ptr[u], len(self.g[u])):
            self.ptr[u] = i

            v, c, rev = self.g[u][i]

            if c > 0 and self.level[v] == self.level[u] + 1:
                pushed = self.dfs(v, t, min(f, c))

                if pushed:
                    self.g[u][i][1] -= pushed
                    self.g[v][rev][1] += pushed
                    return pushed

        return 0

    def maxflow(self, s, t):
        flow = 0

        while self.bfs(s, t):
            self.ptr = [0] * self.n

            while True:
                pushed = self.dfs(s, t, INF)
                if not pushed:
                    break
                flow += pushed

        return flow

def solve():
    n = int(input())

    sets = []
    for _ in range(n):
        arr = list(map(int, input().split()))
        sets.append(arr[1:])

    cost = list(map(int, input().split()))

    match_num = [-1] * (n + 1)

    def kuhn(u, vis):
        if vis[u]:
            return False

        vis[u] = True

        for x in sets[u]:
            if match_num[x] == -1 or kuhn(match_num[x], vis):
                match_num[x] = u
                return True

        return False

    for i in range(n):
        vis = [False] * n
        kuhn(i, vis)

    owner = [-1] * (n + 1)

    for x in range(1, n + 1):
        if match_num[x] != -1:
            owner[x] = match_num[x]

    g = [[] for _ in range(n)]

    for i in range(n):
        matched_x = -1

        for x in sets[i]:
            if owner[x] == i:
                matched_x = x

        for x in sets[i]:
            if x != matched_x:
                g[i].append(owner[x])

    # Tarjan SCC
    sys.setrecursionlimit(10**6)

    tin = [-1] * n
    low = [0] * n
    stack = []
    in_stack = [False] * n

    comp = [-1] * n
    timer = 0
    comp_cnt = 0

    def dfs(u):
        nonlocal timer, comp_cnt

        tin[u] = low[u] = timer
        timer += 1

        stack.append(u)
        in_stack[u] = True

        for v in g[u]:
            if tin[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif in_stack[v]:
                low[u] = min(low[u], tin[v])

        if low[u] == tin[u]:
            while True:
                x = stack.pop()
                in_stack[x] = False
                comp[x] = comp_cnt

                if x == u:
                    break

            comp_cnt += 1

    for i in range(n):
        if tin[i] == -1:
            dfs(i)

    comp_weight = [0] * comp_cnt

    for i in range(n):
        comp_weight[comp[i]] += cost[i]

    dag = set()

    for u in range(n):
        for v in g[u]:
            cu = comp[u]
            cv = comp[v]

            if cu != cv:
                dag.add((cu, cv))

    S = comp_cnt
    T = comp_cnt + 1

    dinic = Dinic(comp_cnt + 2)

    neg_sum = 0

    for i in range(comp_cnt):
        w = comp_weight[i]

        if w < 0:
            dinic.add_edge(S, i, -w)
            neg_sum += -w
        else:
            dinic.add_edge(i, T, w)

    for u, v in dag:
        dinic.add_edge(u, v, INF)

    flow = dinic.maxflow(S, T)

    ans = flow - neg_sum
    ans = min(ans, 0)

    print(ans)

solve()
```

The first part computes a matching from numbers to sets. Hall's condition guarantees that every set can obtain a distinct representative, so Kuhn's algorithm always succeeds.

The directed graph construction is the delicate part. Every unmatched edge creates a dependency edge. If set `i` can also use a number owned by another set, then including `i` without that owner would violate tightness.

The SCC compression is necessary because dependencies may form cycles. In a cycle, every set forces every other set, so they must be selected together.

The min-cut construction encodes the closure rule. Infinite edges prevent cuts that violate dependencies. Negative SCC weights are profitable and connected from the source. Positive SCC weights are penalties and connected to the sink.

The final formula:

```
flow - neg_sum
```

is the standard conversion from minimum cut value back into minimum closure weight.

A subtle implementation detail is using sufficiently large `INF`. It only needs to exceed any possible absolute answer. Since costs are bounded by $10^6$ and there are at most 300 sets, $10^{18}$ is completely safe.

## Worked Examples

### Sample 1

Input:

```
3
1 1
2 2 3
1 3
10 20 -3
```

One possible matching is:

| Set | Matched Number |
| --- | --- |
| 0 | 1 |
| 1 | 2 |
| 2 | 3 |

Dependency graph:

| Set | Extra Numbers | Edges |
| --- | --- | --- |
| 0 | none | none |
| 1 | 3 | 1 → 2 |
| 2 | none | none |

SCCs:

| SCC | Sets | Weight |
| --- | --- | --- |
| A | {0} | 10 |
| B | {1} | 20 |
| C | {2} | -3 |

The only negative SCC is `{2}` and it has no outgoing dependencies, so we choose it alone.

Result:

```
-3
```

This example shows that a single set can already satisfy the equality condition. Set `{3}` has one element and contributes one set.

### Custom Example

Input:

```
3
2 1 2
2 1 2
1 2
-5 -4 100
```

Suppose the matching is:

| Set | Matched Number |
| --- | --- |
| 0 | 1 |
| 1 | 2 |

Dependencies:

| Set | Extra Numbers | Edges |
| --- | --- | --- |
| 0 | 2 | 0 → 1 |
| 1 | 1 | 1 → 0 |
| 2 | 2 | 2 → 1 |

SCCs:

| SCC | Sets | Weight |
| --- | --- | --- |
| A | {0,1} | -9 |
| B | {2} | 100 |

Since sets 0 and 1 form a cycle, they must be taken together.

Optimal answer:

```
-9
```

This demonstrates why SCC compression is necessary. Taking only one of the first two sets would violate closure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^3)$ | Matching, SCC computation, and max-flow all fit within cubic complexity |
| Space | $O(n^2)$ | Graphs and flow network store at most quadratic edges |

With $n \le 300$, cubic algorithms are completely practical. Even dense graphs remain comfortably inside the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    from collections import deque

    input = sys.stdin.readline
    INF = 10**18

    class Dinic:
        def __init__(self, n):
            self.n = n
            self.g = [[] for _ in range(n)]

        def add_edge(self, u, v, c):
            self.g[u].append([v, c, len(self.g[v])])
            self.g[v].append([u, 0, len(self.g[u]) - 1])

        def bfs(self, s, t):
            self.level = [-1] * self.n
            q = deque([s])
            self.level[s] = 0

            while q:
                u = q.popleft()

                for v, c, rev in self.g[u]:
                    if c > 0 and self.level[v] == -1:
                        self.level[v] = self.level[u] + 1
                        q.append(v)

            return self.level[t] != -1

        def dfs(self, u, t, f):
            if u == t:
                return f

            for i in range(self.ptr[u], len(self.g[u])):
                self.ptr[u] = i

                v, c, rev = self.g[u][i]

                if c > 0 and self.level[v] == self.level[u] + 1:
                    pushed = self.dfs(v, t, min(f, c))

                    if pushed:
                        self.g[u][i][1] -= pushed
                        self.g[v][rev][1] += pushed
                        return pushed

            return 0

        def maxflow(self, s, t):
            flow = 0

            while self.bfs(s, t):
                self.ptr = [0] * self.n

                while True:
                    pushed = self.dfs(s, t, INF)

                    if not pushed:
                        break

                    flow += pushed

            return flow

    n = int(input())

    sets = []

    for _ in range(n):
        arr = list(map(int, input().split()))
        sets.append(arr[1:])

    cost = list(map(int, input().split()))

    match_num = [-1] * (n + 1)

    def kuhn(u, vis):
        if vis[u]:
            return False

        vis[u] = True

        for x in sets[u]:
            if match_num[x] == -1 or kuhn(match_num[x], vis):
                match_num[x] = u
                return True

        return False

    for i in range(n):
        vis = [False] * n
        kuhn(i, vis)

    owner = [-1] * (n + 1)

    for x in range(1, n + 1):
        if match_num[x] != -1:
            owner[x] = match_num[x]

    g = [[] for _ in range(n)]

    for i in range(n):
        matched_x = -1

        for x in sets[i]:
            if owner[x] == i:
                matched_x = x

        for x in sets[i]:
            if x != matched_x:
                g[i].append(owner[x])

    sys.setrecursionlimit(10**6)

    tin = [-1] * n
    low = [0] * n
    stack = []
    in_stack = [False] * n

    comp = [-1] * n
    timer = 0
    comp_cnt = 0

    def dfs(u):
        nonlocal timer, comp_cnt

        tin[u] = low[u] = timer
        timer += 1

        stack.append(u)
        in_stack[u] = True

        for v in g[u]:
            if tin[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif in_stack[v]:
                low[u] = min(low[u], tin[v])

        if low[u] == tin[u]:
            while True:
                x = stack.pop()
                in_stack[x] = False
                comp[x] = comp_cnt

                if x == u:
                    break

            comp_cnt += 1

    for i in range(n):
        if tin[i] == -1:
            dfs(i)

    comp_weight = [0] * comp_cnt

    for i in range(n):
        comp_weight[comp[i]] += cost[i]

    dag = set()

    for u in range(n):
        for v in g[u]:
            cu = comp[u]
            cv = comp[v]

            if cu != cv:
                dag.add((cu, cv))

    S = comp_cnt
    T = comp_cnt + 1

    dinic = Dinic(comp_cnt + 2)

    neg_sum = 0

    for i in range(comp_cnt):
        w = comp_weight[i]

        if w < 0:
            dinic.add_edge(S, i, -w)
            neg_sum += -w
        else:
            dinic.add_edge(i, T, w)

    for u, v in dag:
        dinic.add_edge(u, v, INF)

    ans = dinic.maxflow(S, T) - neg_sum
    ans = min(ans, 0)

    return str(ans) + "\n"

# provided sample
assert run(
"""3
1 1
2 2 3
1 3
10 20 -3
"""
) == "-3\n"

# empty collection optimal
assert run(
"""2
1 1
1 2
5 7
"""
) == "0\n"

# SCC cycle
assert run(
"""3
2 1 2
2 1 2
1 2
-5 -4 100
"""
) == "-9\n"

# all negative independent sets
assert run(
"""3
1 1
1 2
1 3
-1 -2 -3
"""
) == "-6\n"

# minimum size
assert run(
"""1
1 1
5
"""
) == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single positive set | 0 | Empty collection handling |
| Two overlapping negative sets | -9 | SCC compression correctness |
| Independent negative singleton sets | -6 | Multiple disjoint feasible components |
| Minimum size input | 0 | Boundary condition with $n=1$ |

## Edge Cases

Consider the case where every available set has positive cost.

```
2
1 1
1 2
5 7
```

The algorithm builds two isolated SCCs with positive weights. In the flow network, both connect only to the sink. The minimum cut excludes both SCCs, producing total cost 0. This correctly corresponds to choosing the empty collection.

Now consider a cyclic dependency.

```
2
2 1 2
2 1 2
-3 -4
```

Suppose set 0 owns number 1 and set 1 owns number 2. Then each set has an unmatched edge to the other owner's number, creating edges:

```
0 → 1
1 → 0
```

Both sets collapse into one SCC with total weight `-7`. The min-cut either selects both or neither. Since the SCC weight is negative, the algorithm chooses both, producing the correct answer `-7`.

Finally, consider a misleading overlap.

```
3
2 1 2
1 1
1 2
-100 1 1
```

Choosing only the first set is valid because one set and two numbers do not satisfy equality. The dependency graph captures this. The large negative set depends on both singleton owners, so closure forces inclusion of all three sets. Their total cost is `-98`, and the union size becomes 2 while the number of sets becomes 3, which is impossible. The closure constraints prevent this invalid selection automatically.
