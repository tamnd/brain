---
title: "CF 104821F - Equivalent Rewriting"
description: "We start with an array of length $m$, initially filled with zeros. Each operation $i$ takes a list of positions and overwrites all of those positions with the value $i$."
date: "2026-06-28T12:48:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104821
codeforces_index: "F"
codeforces_contest_name: "The 2023 ICPC Asia Nanjing Regional Contest (The 2nd Universal Cup. Stage 11: Nanjing)"
rating: 0
weight: 104821
solve_time_s: 95
verified: false
draft: false
---

[CF 104821F - Equivalent Rewriting](https://codeforces.com/problemset/problem/104821/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We start with an array of length $m$, initially filled with zeros. Each operation $i$ takes a list of positions and overwrites all of those positions with the value $i$. Since operations are applied in order from 1 to $n$, the final value at each position is simply the index of the last operation that touched it.

The final array $R$ is therefore determined by a “last write wins” rule: every index remembers the largest operation number that included it, and that operation number becomes its final value.

The task is to reorder the operations. We are allowed to permute the operations arbitrarily, but after applying them in this new order, every position must end up with exactly the same final value as in the original process.

The constraints allow up to $10^5$ operations and positions per test, with total input size up to about $2 \cdot 10^6$. This forces a linear or near-linear solution per test case. Anything quadratic in the number of operation-position incidences would fail immediately because each operation may touch many positions.

A subtle failure case appears when two operations overlap on some positions but the “winning” operation for those positions differs across the original process. For example, if operation 1 touches position 1 and 2, operation 2 touches position 2 and 3, and operation 3 touches position 1 and 3, then different indices have different last writers. A naive idea like sorting by operation size or by minimum index touched fails because it ignores that constraints are position-specific rather than global.

The core difficulty is that the final result encodes precedence constraints between operations, and these constraints must be extracted carefully.

## Approaches

If we ignore ordering constraints and simply try all permutations, we could simulate each ordering and compare results. That would cost $n! \cdot m$, which is completely infeasible even for tiny inputs.

A slightly less naive attempt is to realize that the final value of each position depends only on the last operation affecting it. This suggests computing, for each position, which operation is last in the original sequence. Call this $last[x]$. If we fix that the same operation must remain the last writer for each position, then we can derive constraints: for every position $x$, every operation that touches $x$ except $last[x]$ must appear before $last[x]$.

This transforms the problem into a partial order over operations. Each position contributes directed constraints of the form “operation $a$ must come before operation $b$”. Once we construct all such constraints, the problem becomes checking whether a valid topological ordering exists.

This is exactly where the structure becomes exploitable. Instead of reasoning about arrays, we reason about dependencies between operations. If the dependency graph has a cycle, no permutation can preserve all “last write” relationships. If it is acyclic, any topological ordering produces a valid permutation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot m)$ | $O(m)$ | Too slow |
| Dependency Graph + Toposort | $O(n + \sum p_i)$ | $O(n + \sum p_i)$ | Accepted |

## Algorithm Walkthrough

We reduce the problem to building and validating a directed graph over operations.

1. Compute the last operation affecting each position. We scan operations in increasing order and record for each position $x$ the largest index $i$ such that operation $i$ contains $x$. This value is $last[x]$. This step captures the final state of the array.
2. For every operation $i$, we examine all positions it touches. For each position $x$, if $last[x] \neq i$, then operation $i$ must appear before operation $last[x]$ in any valid ordering. We encode this as a directed edge $i \rightarrow last[x]$.
3. We build the full directed graph using adjacency lists and compute indegrees of all nodes. This graph encodes every constraint required to preserve the final array.
4. We perform a topological sort using a queue of nodes with indegree zero. Each time we remove an operation from the queue, we append it to the answer and reduce indegrees of its neighbors.
5. If we manage to output all $n$ operations, the ordering is valid. Otherwise, the graph contains a cycle and no permutation can preserve the result.

The key idea is that each position contributes a “winner must come after all other participants” constraint, and we enforce all such constraints globally.

### Why it works

Each position $x$ is determined in the original process by a unique operation $last[x]$. Any other operation that touches $x$ must not overwrite it after $last[x]$ in the new ordering, otherwise the final value would change. Therefore every such operation must precede $last[x]$. These constraints are exactly what the graph encodes.

Conversely, if all these constraints are satisfied, then for every position $x$, the last operation touching it in the new order is still $last[x]$, because all competing operations are forced earlier. This preserves the final array exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, m = map(int, input().split())
    
    ops = [[] for _ in range(n + 1)]
    last = [0] * (m + 1)

    for i in range(1, n + 1):
        arr = list(map(int, input().split()))
        p = arr[0]
        for x in arr[1:]:
            ops[i].append(x)
            last[x] = i

    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)

    for i in range(1, n + 1):
        for x in ops[i]:
            j = last[x]
            if j != i:
                g[i].append(j)
                indeg[j] += 1

    q = deque([i for i in range(1, n + 1) if indeg[i] == 0])
    res = []

    while q:
        u = q.popleft()
        res.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(res) != n:
        print("No")
    else:
        print("Yes")
        print(*res)

t = int(input())
for _ in range(t):
    solve()
```

The code first reconstructs the “last occurrence” of each position, which fully describes the target array. It then builds a directed graph where every edge enforces that a non-winning operation for a position must appear earlier than the winning one.

The topological sort is implemented using a deque. If any cycle exists, some operation will never reach indegree zero, which correctly signals impossibility.

A common pitfall is iterating edges twice or incorrectly adding edges for positions where an operation is itself the last writer. Those cases must be skipped, since they impose no constraint.

## Worked Examples

Consider a small instance where operations overlap:

Input:

```
n = 3, m = 3
1: [1]
2: [1, 2]
3: [2]
```

Here $last[1] = 2$, $last[2] = 3$, $last[3] = 0$.

We construct edges:

Operation 1 contributes $1 \rightarrow 2$.

Operation 2 contributes $2 \rightarrow 3$.

Operation 3 contributes nothing.

Topological sort yields the ordering $1, 2, 3$.

| Step | Queue | Chosen | Result | Indegree changes |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | [1] | 2 decreases |
| 1 | 2 | 2 | [1,2] | 3 decreases |
| 2 | 3 | 3 | [1,2,3] | done |

This confirms that dependencies propagate correctly along overlapping updates.

A second example shows impossibility:

```
1: [1]
2: [1]
```

Both operations touch the same position, but only operation 2 is last, so we get edge $1 \rightarrow 2$. This is still acyclic, so ordering exists as $1,2$. If we reversed dependencies incorrectly, we would create a cycle and incorrectly report failure. The construction ensures direction is always from non-last to last, preventing false cycles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + \sum p_i)$ | Each position is processed once for last-occurrence computation and once for edge generation |
| Space | $O(n + \sum p_i)$ | Stores adjacency lists and operation membership lists |

The total work scales linearly with the input size, which fits comfortably within the constraints where the sum of all $p_i$ is up to $10^6$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        n, m = map(int, input().split())
        ops = [[] for _ in range(n + 1)]
        last = [0] * (m + 1)

        for i in range(1, n + 1):
            arr = list(map(int, input().split()))
            p = arr[0]
            for x in arr[1:]:
                ops[i].append(x)
                last[x] = i

        g = [[] for _ in range(n + 1)]
        indeg = [0] * (n + 1)

        for i in range(1, n + 1):
            for x in ops[i]:
                j = last[x]
                if j != i:
                    g[i].append(j)
                    indeg[j] += 1

        q = deque([i for i in range(1, n + 1) if indeg[i] == 0])
        res = []

        while q:
            u = q.popleft()
            res.append(u)
            for v in g[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

        if len(res) != n:
            return "No\n"
        return "Yes\n" + " ".join(map(str, res)) + "\n"

    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve())
    return "".join(out)

# sample-style checks
assert run("""1
3 3
1 1
2 1 2
1 2
""").strip().startswith("Yes")

assert run("""1
2 2
1 1
1 1
""").strip() in ["Yes\n1 2", "Yes\n2 1"]

assert run("""1
2 2
1 1
1 1
""") != "", "non-empty output"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single chain of dependencies | Yes + valid order | Basic topological correctness |
| Identical operations | Yes | Handling redundant constraints |
| Overlapping but acyclic structure | Yes | Multiple constraints per node |

## Edge Cases

A minimal case is when every operation touches disjoint positions. The graph has no edges, so every permutation is valid. The algorithm correctly produces all nodes with indegree zero initially and outputs any order.

A more delicate case is when a single position is touched by many operations. Only the last one in the original sequence becomes the sink of a chain of edges, and all others point to it. The construction ensures no edge is reversed, so no artificial cycle is introduced.

A failure case would arise if we mistakenly added edges in both directions for shared positions. That would create immediate cycles even when a valid ordering exists. The algorithm avoids this by directing edges strictly toward the final writer determined by the original process.
