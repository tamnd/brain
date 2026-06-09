---
title: "CF 1913E - Matrix Problem"
description: "We start with a binary matrix. Every cell currently contains either 0 or 1, and we are allowed to change any cell to either value. Changing a cell counts as one operation. The final matrix must satisfy two independent requirements."
date: "2026-06-08T20:11:10+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1913
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 160 (Rated for Div. 2)"
rating: 2400
weight: 1913
solve_time_s: 168
verified: true
draft: false
---

[CF 1913E - Matrix Problem](https://codeforces.com/problemset/problem/1913/E)

**Rating:** 2400  
**Tags:** flows, graphs  
**Solve time:** 2m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a binary matrix. Every cell currently contains either 0 or 1, and we are allowed to change any cell to either value. Changing a cell counts as one operation.

The final matrix must satisfy two independent requirements. For every row, the number of ones must match a prescribed row sum. For every column, the number of ones must match a prescribed column sum.

Among all matrices satisfying those row and column requirements, we need the one requiring the fewest cell changes from the original matrix.

The matrix dimensions are at most 50 × 50, so there are at most 2500 cells. That is small enough for graph algorithms on a few thousand vertices and edges, but completely rules out enumerating possible matrices. A binary matrix with 2500 cells has $2^{2500}$ possible configurations.

Before thinking about optimization, there is a basic feasibility condition. The total number of ones demanded by the rows must equal the total number of ones demanded by the columns. If

$$\sum A_i \ne \sum B_j,$$

then no matrix can satisfy both sets of constraints simultaneously.

Several edge cases are easy to miss.

Consider

```
2 2
0 0
0 0
2 0
1 1
```

The row sums require two ones in the first row and zero in the second. The column sums require one one in each column. The total demand is 2 in both directions, so a solution exists.

A careless solution that only checks row requirements or only checks column requirements could incorrectly reject this case.

Another important case is when the original matrix already satisfies everything:

```
2 2
1 0
0 1
1 1
1 1
```

The answer is 0. Any algorithm that tries to greedily move ones around without accounting for existing placements may perform unnecessary modifications.

The impossible case must also be detected immediately:

```
2 2
0 0
0 0
2 2
1 1
```

Rows demand four ones while columns demand only two. No matrix can satisfy both requirements, so the correct answer is -1.

The most subtle issue is that minimizing changes is not the same as constructing any feasible matrix. Different feasible matrices can require different numbers of edits. The optimization objective must be built directly into the model.

## Approaches

A brute-force solution would try every binary matrix of size $n \times m$, check whether its row sums and column sums match the targets, and among all valid matrices compute the smallest Hamming distance from the original matrix.

This is correct because it explicitly examines every candidate final matrix. Unfortunately, even a 10 × 10 matrix already has $2^{100}$ possibilities. With up to 2500 cells, brute force is completely hopeless.

The key observation is that the constraints describe a bipartite structure.

Every row decides where its required ones go. Every column receives a required number of ones. If we think of putting a one into cell $(i,j)$ as selecting an edge between row $i$ and column $j$, then:

- Row $i$ must participate in exactly $A_i$ selected edges.
- Column $j$ must participate in exactly $B_j$ selected edges.

This is exactly a flow problem.

Now consider the objective. Suppose cell $(i,j)$ currently contains 1.

If we keep it as 1, the cost is 0.

If we change it to 0, the cost is 1.

Similarly, if a cell currently contains 0:

- Keeping it 0 costs 0.
- Changing it to 1 costs 1.

Instead of minimizing modifications directly, it is easier to maximize how many cells remain unchanged.

For a chosen final matrix $x$,

$$\text{changes} = nm - \text{unchanged cells}.$$

So we want the feasible matrix that preserves the maximum number of original values.

This turns the problem into a minimum-cost flow formulation.

For every cell:

- Choosing final value 1 sends one unit of flow through that row-column pair.
- The edge cost reflects whether this choice preserves or changes the original cell.

Using costs

$$\text{cost}(1)= \begin{cases} 0 & a_{ij}=1\\ 1 & a_{ij}=0 \end{cases}$$

counts the cost of creating the final matrix's ones.

However, cells that end up as 0 may also contribute modification costs. To capture the total edit count cleanly, we shift the objective.

Let every original 1 contribute a constant cost of 1 initially. Then:

- If an original 1 remains 1, we gain 1.
- If an original 0 becomes 1, we pay 1.

This leads to edge weights

$$w_{ij}= \begin{cases} 1 & a_{ij}=1\\ -1 & a_{ij}=0 \end{cases}$$

and we seek the feasible matrix maximizing total weight.

After obtaining the maximum weight $W$,

$$\text{answer} = (\#\text{original ones}) - W.$$

The resulting optimization is a maximum-cost bipartite flow, equivalently a minimum-cost flow after negating edge costs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{nm})$ | $O(1)$ | Too slow |
| Optimal Min-Cost Flow | $O(V^2E)$ or better for this size | $O(E)$ | Accepted |

## Algorithm Walkthrough

1. Read the matrix and compute the number of original ones, denoted by `ones`.
2. Check whether

$$\sum A_i = \sum B_j.$$

If not, print `-1` because no matrix can satisfy both sets of requirements.
3. Build a flow network.

Create a source `S`, a node for each row, a node for each column, and a sink `T`.
4. Add edges from `S` to each row node with capacity `A_i` and cost `0`.

This forces exactly `A_i` units of flow to leave row `i`, corresponding to exactly `A_i` ones in that row.
5. Add edges from each column node to `T` with capacity `B_j` and cost `0`.

This forces exactly `B_j` units of flow into column `j`.
6. For every cell `(i,j)`, add an edge from row `i` to column `j` with capacity `1`.

Its cost is:

$$-1 \quad \text{if } a_{ij}=1$$

$$+1 \quad \text{if } a_{ij}=0$$

We negate the weights because standard min-cost flow minimizes cost.
7. Send exactly

$$F=\sum A_i$$

units of flow from source to sink.

If the network cannot send this amount, no feasible matrix exists and the answer is `-1`.
8. Let `cost` be the minimum total cost found.

Since costs were negated,

$$W=-cost.$$
9. Output

$$\text{ones}-W.$$

### Why it works

Every unit of flow corresponds to selecting exactly one matrix cell whose final value is 1. Capacity one on row-column edges guarantees a cell is chosen at most once. Source-row capacities enforce row sums, and column-sink capacities enforce column sums.

For an original 1, selecting that cell contributes weight +1. For an original 0, selecting that cell contributes weight -1. The total weight equals

$$(\text{original 1s kept}) - (\text{original 0s turned into 1}).$$

If the original matrix contains `ones` ones, then

$$\text{changes} = (\text{original 1s removed}) + (\text{original 0s added}) = \text{ones}-W.$$

Thus maximizing weight is exactly equivalent to minimizing the number of modified cells. The min-cost flow algorithm finds the optimal feasible flow, so the resulting edit count is minimal.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

class Edge:
    __slots__ = ("to", "rev", "cap", "cost")

    def __init__(self, to, rev, cap, cost):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost

class MinCostFlow:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap, cost):
        fwd = Edge(to, len(self.g[to]), cap, cost)
        rev = Edge(fr, len(self.g[fr]), 0, -cost)
        self.g[fr].append(fwd)
        self.g[to].append(rev)

    def min_cost_flow(self, s, t, need):
        n = self.n
        pot = [0] * n
        flow = 0
        cost = 0

        INF = 10**18

        while flow < need:
            dist = [INF] * n
            parent_v = [-1] * n
            parent_e = [-1] * n

            dist[s] = 0
            pq = [(0, s)]

            while pq:
                d, v = heapq.heappop(pq)
                if d != dist[v]:
                    continue

                for i, e in enumerate(self.g[v]):
                    if e.cap <= 0:
                        continue

                    nd = d + e.cost + pot[v] - pot[e.to]
                    if nd < dist[e.to]:
                        dist[e.to] = nd
                        parent_v[e.to] = v
                        parent_e[e.to] = i
                        heapq.heappush(pq, (nd, e.to))

            if dist[t] == INF:
                return None

            for v in range(n):
                if dist[v] < INF:
                    pot[v] += dist[v]

            add = need - flow
            v = t

            while v != s:
                pv = parent_v[v]
                pe = parent_e[v]
                add = min(add, self.g[pv][pe].cap)
                v = pv

            v = t
            while v != s:
                pv = parent_v[v]
                pe = parent_e[v]
                e = self.g[pv][pe]

                e.cap -= add
                self.g[v][e.rev].cap += add

                v = pv

            flow += add
            cost += add * pot[t]

        return cost

def solve():
    n, m = map(int, input().split())

    a = [list(map(int, input().split())) for _ in range(n)]
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    if sum(A) != sum(B):
        print(-1)
        return

    original_ones = sum(sum(row) for row in a)

    S = 0
    row_start = 1
    col_start = row_start + n
    T = col_start + m
    N = T + 1

    mcf = MinCostFlow(N)

    for i in range(n):
        mcf.add_edge(S, row_start + i, A[i], 0)

    for j in range(m):
        mcf.add_edge(col_start + j, T, B[j], 0)

    for i in range(n):
        for j in range(m):
            cost = -1 if a[i][j] == 1 else 1
            mcf.add_edge(row_start + i, col_start + j, 1, cost)

    required_flow = sum(A)

    cost = mcf.min_cost_flow(S, T, required_flow)

    if cost is None:
        print(-1)
        return

    max_weight = -cost
    answer = original_ones - max_weight
    print(answer)

if __name__ == "__main__":
    solve()
```

The network contains one node per row and one node per column. A unit of flow through a row-column edge means that the corresponding cell is assigned value 1 in the final matrix.

The row capacities and column capacities encode the required row and column sums exactly. Since every cell edge has capacity 1, no cell can contribute more than one selected one.

The subtle part is the cost assignment. An original one receives cost `-1`, while an original zero receives cost `+1`. The min-cost flow algorithm minimizes total cost, which is equivalent to maximizing the weight described in the proof. After the flow is computed, the final formula converts that maximum weight back into the number of edits.

The implementation uses successive shortest augmenting paths with Johnson potentials. Negative edge costs appear only on forward cell edges, but there are no negative cycles. Potentials make all reduced costs nonnegative, allowing Dijkstra's algorithm to be used efficiently.

## Worked Examples

### Example 1

Input:

```
3 3
0 0 0
0 0 0
0 0 0
1 1 1
1 1 1
```

The original matrix contains zero ones.

Required flow is 3.

| Chosen Cells | Weight Contribution | Total Weight |
| --- | --- | --- |
| (1,1) | -1 | -1 |
| (2,2) | -1 | -2 |
| (3,3) | -1 | -3 |

All selected cells come from original zeros.

| Quantity | Value |
| --- | --- |
| Original ones | 0 |
| Max weight | -3 |
| Answer | 3 |

Output:

```
3
```

The trace shows that every required one must be created from a zero, producing exactly three edits.

### Example 2

```
2 2
1 0
0 1
1 1
1 1
```

The matrix already satisfies the targets.

| Chosen Cells | Weight Contribution | Running Weight |
| --- | --- | --- |
| (1,1) | +1 | 1 |
| (2,2) | +1 | 2 |

| Quantity | Value |
| --- | --- |
| Original ones | 2 |
| Max weight | 2 |
| Answer | 0 |

Output:

```
0
```

The flow chooses exactly the cells that are already ones, preserving every original value and requiring no edits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(V^2E)$ | Successive shortest augmenting path min-cost flow |
| Space | $O(E)$ | Graph storage |

For this problem,

$$V = n + m + 2 \le 102$$

and

$$E = nm + n + m \le 2600.$$

These values are very small for a min-cost flow implementation, so the solution comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    pass

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue()

# sample 1
assert run(
"""3 3
0 0 0
0 0 0
0 0 0
1 1 1
1 1 1
"""
) == "3\n"

# already valid matrix
assert run(
"""2 2
1 0
0 1
1 1
1 1
"""
) == "0\n"

# impossible totals
assert run(
"""2 2
0 0
0 0
2 2
1 1
"""
) == "-1\n"

# all ones already
assert run(
"""2 2
1 1
1 1
2 2
2 2
"""
) == "0\n"

# minimum dimensions
assert run(
"""2 2
0 0
0 0
1 0
1 0
"""
) == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 3 | Creating all required ones |
| Already valid matrix | 0 | No unnecessary edits |
| Mismatched totals | -1 | Feasibility check |
| All ones already | 0 | Preserving existing structure |
| 2×2 boundary case | 1 | Smallest valid dimensions |

## Edge Cases

Consider the impossible-total case:

```
2 2
0 0
0 0
2 2
1 1
```

The row requirements sum to 4, while the column requirements sum to 2. Before any flow computation starts, the algorithm detects the mismatch and returns `-1`. No feasible matrix can exist because every one contributes simultaneously to one row count and one column count.

Consider a matrix already satisfying all requirements:

```
2 2
1 0
0 1
1 1
1 1
```

The flow demand is 2. The cheapest edges are exactly the two cells already containing ones, each with cost `-1`. The algorithm sends flow through those cells, obtains total cost `-2`, computes weight `2`, and returns `2 - 2 = 0`.

Consider a case where multiple feasible matrices exist:

```
2 2
1 0
0 0
1 1
1 1
```

Two final matrices satisfy the row and column sums. One keeps the existing one and changes only one additional cell. Another discards the existing one and creates two new ones. The flow objective prefers the first configuration because keeping an original one contributes positive weight. The resulting answer is the true minimum edit count, not merely any feasible count.

These examples illustrate why feasibility and optimization must be handled together, which is exactly what the min-cost flow formulation accomplishes.
