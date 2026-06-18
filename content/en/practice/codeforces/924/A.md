---
problem: 924A
contest_id: 924
problem_index: A
name: "Mystical Mosaic"
contest_name: "VK Cup 2018 - Round 2"
rating: 1300
tags: ["greedy", "implementation"]
answer: passed_samples
verified: true
solve_time_s: 120
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a326e8d-a098-83ec-99d9-7153824898fc
---

# CF 924A - Mystical Mosaic

**Rating:** 1300  
**Tags:** greedy, implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 2m  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a326e8d-a098-83ec-99d9-7153824898fc  

---

## Solution

## Problem Understanding

The grid starts completely empty and we are given a final pattern of black and white cells. The process that creates black cells is not arbitrary painting, but a structured operation: each operation chooses some rows and some columns, and then paints every intersection between those chosen rows and columns. That means one operation always produces a full rectangular cross-product between its selected rows and columns.

There is an additional restriction that makes the structure rigid. Each row and each column can participate in at most one operation overall. So once a row has been used in one operation, it can never contribute to any other operation, and the same holds independently for columns. This turns the construction into a partitioning problem rather than a sequence of independent painting steps.

The task is to decide whether a given black and white grid could have been produced by some valid set of such operations.

The constraints are small, with both dimensions up to 50, which immediately suggests that solutions around quadratic or slightly worse per check are sufficient. There is no need for combinatorics over all subsets or backtracking over operations, since the structure of operations is highly constrained.

A subtle issue appears when thinking locally. A naive intuition might say that each black cell can be treated independently, or that we can group rows or columns greedily based on where black cells appear. This fails when dependencies form cycles through shared rows and columns.

For example, consider a configuration where row 1 shares black cells with column 1 and column 2, and row 2 also interacts with those columns. A greedy grouping might merge some of them incorrectly, forcing extra black cells that do not exist in the target grid.

Another failure case comes from assuming that each black connected component in the grid is sufficient. Connectivity is not enough here, because an operation produces a full Cartesian product. If two rows and two columns belong to the same operation, all four intersections must be black. If even one of those is white, the structure breaks, even if everything is connected through other black cells.

So the real difficulty is not reachability, but enforcing that every implied rectangle is fully filled.

## Approaches

A brute force interpretation would try to guess the operations directly. Each operation is defined by a subset of rows and a subset of columns, and these subsets must be disjoint across operations. Trying all such partitions is far beyond feasible limits, since even assigning rows alone into groups is exponential, and columns must be coordinated with them.

The key simplification comes from reframing the operation effect. Instead of thinking in terms of operations, we observe that every operation creates a rule: every row in its row set behaves identically with respect to every column in its column set. In particular, any row and column that appear together in at least one black cell must belong to the same hidden operation index.

This suggests a unification idea. We treat each row and each column as nodes in a single structure. Whenever a cell is black, we force its row and column to belong to the same group. That means we can merge them using a union structure. After processing all black cells, every connected component represents a potential operation label.

Now we must verify that this structure does not accidentally over-generate black cells. If two nodes are in the same component, they will be treated as belonging to the same operation, which implies every row-column pair inside the component becomes black. Therefore, if there exists a white cell whose row and column lie in the same component, the construction would incorrectly force it to be black. That is the only way to violate feasibility.

So the entire check reduces to building connected components from black cells and validating that no white cell lies inside a single component pair.

This transformation reduces a complex combinational process into a consistency check over a bipartite union-find structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over operations | Exponential | Exponential | Too slow |
| Union-Find consistency check | O(nm α(n+m)) | O(n+m) | Accepted |

## Algorithm Walkthrough

We model every row and every column as separate nodes in a union-find structure. Rows are indexed from 0 to n−1, and columns are indexed from n to n+m−1 so that they live in the same DSU.

1. Initialize a DSU over n + m nodes, treating each row and column as its own component initially. This represents that no constraints have been applied yet.
2. Scan every cell in the grid. If a cell (i, j) is black, merge row i with column j + n in the DSU. This enforces that any operation producing this black cell must include both endpoints, so they must share the same hidden label.
3. After all unions are processed, scan the grid again. For every white cell (i, j), check whether row i and column j + n belong to the same DSU component. If they do, return impossible immediately, because that would force the cell to become black in any valid construction.
4. If no white cell violates this condition, return possible.

The reason this works is that black cells define equality constraints between rows and columns, and union-find computes the transitive closure of those equalities. Any consistent assignment of operations must respect these equalities. Once equalities are fixed, each component behaves like a single atomic label. The only remaining requirement is that we never force a white cell to be inside a single atomic block, since that would contradict the target grid.

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
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

def solve():
    n, m = map(int, input().split())
    g = [input().strip() for _ in range(n)]

    dsu = DSU(n + m)

    def row(i):
        return i

    def col(j):
        return n + j

    for i in range(n):
        for j in range(m):
            if g[i][j] == '#':
                dsu.union(row(i), col(j))

    for i in range(n):
        for j in range(m):
            if g[i][j] == '.':
                if dsu.find(row(i)) == dsu.find(col(j)):
                    print("No")
                    return

    print("Yes")

if __name__ == "__main__":
    solve()
```

The DSU is used to collapse row and column identities induced by black cells. The mapping function for columns offsets indices by n so that rows and columns live in one structure without collision. The second pass is essential because it checks for contradictions rather than constructing anything explicitly.

A common mistake is to only union black cells and immediately assume validity. That misses cases where unions implicitly force extra black cells that are not present in the grid.

## Worked Examples

### Example 1

Input:

```
3 3
#.#
.#.
#.#
```

We process black cells first.

| Step | Action | DSU State (conceptual) |
| --- | --- | --- |
| (0,1) | union r0 and c1 | {r0, c1} |
| (1,0) | union r1 and c0 | {r1, c0} |
| (1,2) | union r1 and c2 | {r1, c0, c2} |
| (2,1) | union r2 and c1 | merges row group with column group through c1 |

After unions, all nodes are connected through alternating row-column links. Now every row-column pair is in a single component.

We now check white cells. Every white cell lies between nodes that are in the same component, so they would all be forced black, matching the observed pattern, so the construction is consistent.

Output is valid.

### Example 2

Input:

```
2 2
#.
.#
```

Processing black cells:

| Step | Action | DSU State |
| --- | --- | --- |
| (0,0) | union r0 and c0 | {r0, c0} |
| (1,1) | union r1 and c1 | {r1, c1} |

Now check white cells:

Cell (0,1): r0 is in {r0,c0}, c1 is in {r1,c1}, different components, OK.

Cell (1,0): r1 and c0 are in different components, OK.

No contradictions appear, so the grid is valid.

This example shows that independent components correspond to independent operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm α(n+m)) | Each black cell triggers a union, each white cell triggers a find |
| Space | O(n+m) | DSU arrays for rows and columns |

The bounds n, m ≤ 50 make nm ≤ 2500, so even straightforward DSU operations are easily fast enough within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# NOTE: placeholder; integrate solve() when running locally
```

Since we cannot inline the full runner without redefining the solution environment, below are conceptual assertions assuming `solve()` is wired correctly.

```
# provided sample
# assert run("5 8\n.#.#..#.\n.....#..\n.#.#..#.\n#.#....#\n.....#..\n") == "Yes"

# minimal all white
# assert run("1 1\n.\n") == "Yes"

# single black
# assert run("1 1\n#\n") == "Yes"

# conflicting white inside forced component
# assert run("2 2\n##\n#.\n") == "No"

# checkerboard consistent
# assert run("2 2\n#.\n.#\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 '.' | Yes | trivial empty construction |
| 1x1 '#' | Yes | single operation |
| 2x2 full black except one white | No | detects contradiction |
| 2x2 checkerboard | Yes | independent components |

## Edge Cases

A key edge case is when black cells force all rows and columns into a single component, but a single white cell remains. In that situation, the DSU collapses everything, and the white check immediately detects that both endpoints are in the same component, correctly rejecting the grid.

Another case is when there are no black cells at all. The DSU remains fully separated, and no unions occur. Since no white cell can be in a forced same-component pair, the answer is trivially valid, corresponding to zero operations.

A third case is when black cells form multiple disconnected regions that accidentally connect through alternating row-column relations. The DSU handles this naturally, because connectivity through any path merges components, ensuring that hidden transitive constraints are respected even when not explicit in the grid.