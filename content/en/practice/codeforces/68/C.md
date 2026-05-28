---
title: "CF 68C - Synchrophasotron"
description: "We have a directed acyclic graph on vertices 1...n. For every pair i < j, there is exactly one directed edge from i to j. Each pipe has three parameters. It must carry between l and h units of flow inclusive, even if we do not want to use that pipe."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 68
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 62"
rating: 2200
weight: 68
solve_time_s: 423
verified: true
draft: false
---

[CF 68C - Synchrophasotron](https://codeforces.com/problemset/problem/68/C)

**Rating:** 2200  
**Tags:** brute force  
**Solve time:** 7m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a directed acyclic graph on vertices `1...n`. For every pair `i < j`, there is exactly one directed edge from `i` to `j`.

Each pipe has three parameters. It must carry between `l` and `h` units of flow inclusive, even if we do not want to use that pipe. If the actual flow through the pipe is positive, we pay an activation cost `a` plus the square of the flow. If the flow is zero, we pay nothing.

Fuel enters node `1` and leaves through node `n`. Every intermediate node must conserve flow, incoming equals outgoing. All flows are integers.

Among all feasible flow assignments, we first want to minimize the total amount reaching node `n`. Among all solutions with that minimum total flow, we want the maximum possible total cost.

The graph is tiny. `n ≤ 6`, so the number of edges is at most `15`. Every edge capacity is at most `5`. This changes the character of the problem completely. We are not looking for a sophisticated polynomial optimization algorithm. The search space is small enough that brute force over edge flows becomes realistic.

Still, naive brute force over all assignments is too large. Every edge can take values `0...5`, so in the worst case there are `6^15 ≈ 4.7e11` assignments. Even with aggressive pruning, that is hopeless.

The small capacities are the real key. The total amount of flow moving through the network can never become large. Since only edges leaving node `1` create flow and each such edge has capacity at most `5`, the total flow into the whole graph is at most `5 * (n-1) ≤ 25`.

That means we can think in terms of node balances instead of independent edge choices.

There are several subtle edge cases.

The first one is that lower bounds apply even to inactive edges. Consider:

```
3
1 2 0 2 0
2 3 3 5 0
1 3 0 5 0
```

Edge `2 -> 3` must carry at least `3`, so node `2` must receive at least `3`. But edge `1 -> 2` can carry at most `2`. The correct answer is:

```
-1 -1
```

A careless implementation that only checks capacities on used edges would incorrectly accept the network.

Another trap is the zero-flow solution. Example:

```
2
1 2 0 5 3
```

We may send zero units through the only edge. Since the edge is inactive, the cost is also zero. The correct output is:

```
0 0
```

If we always add activation cost whenever an edge exists, we get the wrong answer.

The cost function also behaves in a non-intuitive way. Since we maximize sum of squares, splitting flow across several edges can increase the total because each activated edge contributes its own activation bonus. Example:

```
4
1 2 0 2 5
1 3 0 2 5
1 4 0 2 0
2 3 0 2 5
2 4 0 2 5
3 4 0 2 5
```

Suppose the minimum feasible total flow is `2`. Sending both units along one path gives fewer activated edges than splitting the units across different paths. The optimal answer prefers activating more edges when possible.

A final subtlety is that lower bounds can force circulation-like behavior inside the DAG. Since the graph only goes from smaller to larger vertices, cycles are impossible, but intermediate vertices can still be forced to relay mandatory flow because of outgoing lower bounds.

## Approaches

The most direct brute force is to assign a value to every edge independently. For each edge we try every integer flow between `0` and `h`, reject assignments violating lower bounds or flow conservation, then compute the total flow and cost.

This is correct because every feasible solution corresponds to exactly one assignment of edge values.

The problem is the size of the search space. With `15` edges and `6` choices per edge, we get roughly `4.7e11` states. Even if each state took one CPU instruction, it would still be impossible.

The graph structure gives us a better way to think about the problem.

For every vertex except `1` and `n`, flow conservation determines the total outgoing flow once we know the incoming flow. Since capacities are tiny, the total amount entering any node is also tiny.

This suggests dynamic programming over vertices and balances.

Process vertices from left to right. When we reach vertex `v`, all incoming edges into `v` are already fixed because they come from smaller vertices. Their sum determines exactly how much outgoing flow must leave `v`.

Now we only need to distribute that required amount among edges `v -> u` where `u > v`, respecting lower and upper bounds.

The number of possible distributions is small. A vertex has at most `5` outgoing edges and each edge carries at most `5`. The total outgoing flow is at most `25`. Enumerating all distributions becomes feasible.

The crucial observation is that once we process vertices in order, no future decision can change the balance of an already processed vertex. That turns a global feasibility problem into a local transition problem.

We keep DP states describing how much incoming flow each future vertex has accumulated so far. When processing vertex `v`, we know its current incoming amount from the state. We enumerate all valid outgoing assignments and update future balances.

The total state space stays manageable because there are only `5` future vertices and each balance is at most `25`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all edge assignments | $O(6^{15})$ | $O(15)$ | Too slow |
| DP over vertex balances | Roughly $O(\text{states} \times \text{transitions})$ with fewer than a few million operations | $O(\text{states})$ | Accepted |

## Algorithm Walkthrough

1. Read all edges and store their lower bound `l`, upper bound `h`, and activation cost `a`.
2. Define a DP state after processing vertices `1...v-1`.

The state stores, for every future vertex `u ≥ v`, how much incoming flow has already been assigned to `u`.

Since edges only go forward, future decisions cannot modify balances of earlier vertices.
3. Start with all balances equal to zero before processing any vertex.
4. When processing vertex `v`, determine the amount of flow that must leave it.

For `v = 1`, this amount is unrestricted because node `1` is the source. Its outgoing total becomes whatever we assign.

For intermediate vertices, outgoing flow must equal the incoming flow already accumulated for that vertex in the state.
5. Enumerate every possible assignment for outgoing edges `v -> u`.

Each edge flow must lie in `[l, h]`.

For intermediate vertices, the sum of assigned outgoing flows must equal the required outgoing amount.

For vertex `1`, any total is allowed because it is the source.
6. For each assignment, compute:

- the added cost,
- the additional incoming flow contributed to future vertices,
- the total flow eventually reaching node `n`.
7. Update the DP state for the next vertex.

If two ways reach the same state with the same final total flow, keep the larger cost.
8. After processing all vertices, examine states where node `n` has accumulated some flow.

The amount entering node `n` is exactly the total delivered to the synchrophasotron.
9. Choose the smallest feasible total flow. Among those, choose the maximum cost.

### Why it works

The invariant is that after processing vertices `1...v-1`, the DP state exactly records all flow already forced into vertices `v...n`.

Because the graph is acyclic and edges always go forward, future decisions cannot alter balances of processed vertices. Every feasible global flow corresponds to one sequence of local outgoing assignments during the DP, and every sequence generated by the DP satisfies all conservation and capacity constraints.

The DP explores all feasible distributions of outgoing flow at every vertex. Since transitions preserve exact balances and capacities, no invalid solution survives. Since every valid solution can be reconstructed vertex by vertex, no feasible solution is missed.

## Python Solution

```python
import sys
from collections import defaultdict
from itertools import product

input = sys.stdin.readline

def solve():
    n = int(input())

    l = [[0] * n for _ in range(n)]
    h = [[0] * n for _ in range(n)]
    a = [[0] * n for _ in range(n)]

    for _ in range(n * (n - 1) // 2):
        s, f, lo, hi, cost = map(int, input().split())
        s -= 1
        f -= 1

        l[s][f] = lo
        h[s][f] = hi
        a[s][f] = cost

    # state:
    # tuple of accumulated incoming flow for every vertex
    # dp[state] = maximum cost

    start = tuple([0] * n)
    dp = {start: 0}

    for v in range(n - 1):
        ndp = dict()

        targets = list(range(v + 1, n))

        ranges = [range(l[v][u], h[v][u] + 1) for u in targets]

        for state, cur_cost in dp.items():

            required = state[v]

            for flows in product(*ranges):

                total_out = sum(flows)

                # conservation for intermediate vertices
                if v != 0 and total_out != required:
                    continue

                new_state = list(state)

                add_cost = 0

                for idx, u in enumerate(targets):
                    f = flows[idx]
                    new_state[u] += f

                    if f > 0:
                        add_cost += a[v][u] + f * f

                new_state = tuple(new_state)

                value = cur_cost + add_cost

                if new_state not in ndp or ndp[new_state] < value:
                    ndp[new_state] = value

        dp = ndp

    best_flow = None
    best_cost = -1

    for state, cost in dp.items():
        flow = state[n - 1]

        if best_flow is None or flow < best_flow:
            best_flow = flow
            best_cost = cost
        elif flow == best_flow:
            best_cost = max(best_cost, cost)

    if best_flow is None:
        print("-1 -1")
    else:
        print(best_flow, best_cost)

solve()
```

The core idea in the implementation is that `state[i]` stores how much incoming flow vertex `i` has already accumulated from processed vertices.

When processing vertex `v`, all incoming edges into `v` are already fixed because every such edge originates from a smaller vertex. That means `state[v]` is the exact amount that must leave `v` if `v` is an intermediate vertex.

The transition enumerates all possible outgoing assignments using `itertools.product`. This works because each edge capacity is at most `5` and there are at most `5` outgoing edges.

The condition

```
if v != 0 and total_out != required:
```

implements flow conservation. Vertex `1` is excluded because it is the source and may inject arbitrary flow.

Another subtle point is the activation cost:

```
if f > 0:
    add_cost += a[v][u] + f * f
```

We only pay the fixed activation cost if the edge actually carries positive flow.

The DP stores only the maximum achievable cost for each state. If two different constructions produce the same accumulated balances, future possibilities become identical, so keeping the larger cost dominates the smaller one.

## Worked Examples

### Example 1

Input:

```
2
1 2 1 2 3
```

Processing vertex `1`:

| State before | Chosen flow | New state | Added cost |
| --- | --- | --- | --- |
| (0,0) | 1 | (0,1) | 4 |
| (0,0) | 2 | (0,2) | 7 |

Final states:

| Final flow to node 2 | Cost |
| --- | --- |
| 1 | 4 |
| 2 | 7 |

The minimum feasible delivered flow is `1`, and among those states the maximum cost is `4`.

Output:

```
1 4
```

This trace shows how the source vertex is treated differently. It is allowed to generate arbitrary outgoing flow within edge capacities.

### Example 2

Input:

```
3
1 2 0 2 0
1 3 0 5 0
2 3 3 5 0
```

Processing vertex `1`:

| Flow 1->2 | Flow 1->3 | State after |
| --- | --- | --- |
| 0 | 0 | (0,0,0) |
| 1 | 0 | (0,1,0) |
| 2 | 0 | (0,2,0) |
| ... | ... | ... |

Now process vertex `2`.

If state is `(0,0,0)`, required outgoing flow is `0`, but edge `2->3` must carry at least `3`.

| Required outgoing | Allowed edge flow | Valid? |
| --- | --- | --- |
| 0 | 3..5 | No |
| 1 | 3..5 | No |
| 2 | 3..5 | No |

No state survives.

Output:

```
-1 -1
```

This demonstrates how lower bounds can force infeasibility even though every individual edge looks locally valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Roughly $O(S \cdot T)$ | `S` is the number of reachable balance states, `T` is the number of outgoing flow combinations |
| Space | $O(S)$ | DP stores one value per reachable state |

In practice, the limits are tiny. There are at most `15` edges and every edge capacity is at most `5`. The number of reachable states stays comfortably small, and the solution easily fits within the `3s` limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict
from itertools import product

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())

    l = [[0] * n for _ in range(n)]
    h = [[0] * n for _ in range(n)]
    a = [[0] * n for _ in range(n)]

    for _ in range(n * (n - 1) // 2):
        s, f, lo, hi, cost = map(int, input().split())
        s -= 1
        f -= 1

        l[s][f] = lo
        h[s][f] = hi
        a[s][f] = cost

    start = tuple([0] * n)
    dp = {start: 0}

    for v in range(n - 1):
        ndp = dict()

        targets = list(range(v + 1, n))
        ranges = [range(l[v][u], h[v][u] + 1) for u in targets]

        for state, cur_cost in dp.items():

            required = state[v]

            for flows in product(*ranges):

                total_out = sum(flows)

                if v != 0 and total_out != required:
                    continue

                new_state = list(state)

                add_cost = 0

                for idx, u in enumerate(targets):
                    f = flows[idx]
                    new_state[u] += f

                    if f > 0:
                        add_cost += a[v][u] + f * f

                new_state = tuple(new_state)

                value = cur_cost + add_cost

                if new_state not in ndp or ndp[new_state] < value:
                    ndp[new_state] = value

        dp = ndp

    best_flow = None
    best_cost = -1

    for state, cost in dp.items():
        flow = state[n - 1]

        if best_flow is None or flow < best_flow:
            best_flow = flow
            best_cost = cost
        elif flow == best_flow:
            best_cost = max(best_cost, cost)

    if best_flow is None:
        return "-1 -1"

    return f"{best_flow} {best_cost}"

# provided sample
assert run(
"""2
1 2 1 2 3
"""
) == "1 4", "sample 1"

# zero-flow solution
assert run(
"""2
1 2 0 5 3
"""
) == "0 0", "zero flow"

# impossible because of lower bounds
assert run(
"""3
1 2 0 2 0
1 3 0 5 0
2 3 3 5 0
"""
) == "-1 -1", "infeasible network"

# forcing relay through intermediate node
assert run(
"""3
1 2 2 2 1
1 3 0 0 0
2 3 2 2 1
"""
) == "2 10", "exact forced flow"

# activation-cost maximization
assert run(
"""3
1 2 0 1 5
1 3 0 2 0
2 3 0 1 5
"""
) == "0 0", "minimum flow dominates cost"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge with lower bound 1 | `1 4` | Basic correctness |
| Edge with lower bound 0 | `0 0` | Proper handling of inactive edges |
| Impossible relay constraint | `-1 -1` | Lower bounds causing infeasibility |
| Exact forced flow through path | `2 10` | Flow conservation correctness |
| Competing high-cost routes | `0 0` | Lexicographic optimization, minimize flow first |

## Edge Cases

Consider the infeasible relay case again:

```
3
1 2 0 2 0
1 3 0 5 0
2 3 3 5 0
```

After processing node `1`, the maximum incoming flow node `2` can accumulate is `2`.

When processing node `2`, conservation requires outgoing flow equal to incoming flow. But edge `2 -> 3` has lower bound `3`, so every transition requires at least `3` outgoing units. No state survives. The DP naturally eliminates all impossible configurations and returns `-1 -1`.

Now consider the zero-flow case:

```
2
1 2 0 5 3
```

The DP enumerates flows `0...5` on the only edge. Flow `0` is valid because it satisfies the lower bound. Since the edge is inactive, no activation cost is added. The final answer becomes `0 0`.

A common mistake is adding activation cost whenever an edge exists rather than only when its flow is positive.

Finally, consider a case where maximizing cost prefers activating more edges:

```
4
1 2 0 1 5
1 3 0 1 5
1 4 0 2 0
2 4 0 1 5
3 4 0 1 5
2 3 0 0 0
```

Suppose we want total delivered flow `2`.

One possibility is sending both units directly `1 -> 4`, cost `4`.

Another possibility is splitting:

`1 -> 2 = 1`,

`2 -> 4 = 1`,

`1 -> 3 = 1`,

`3 -> 4 = 1`.

This activates four expensive edges, giving cost:

```
(5+1) + (5+1) + (5+1) + (5+1) = 24
```

The DP keeps the larger cost among states with equal balances, so it correctly prefers the split configuration.
