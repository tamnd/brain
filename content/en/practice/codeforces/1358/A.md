---
problem: 1358A
contest_id: 1358
problem_index: A
name: "Park Lighting"
contest_name: "Codeforces Round 645 (Div. 2)"
rating: 800
tags: ["greedy", "math"]
answer: passed_samples
verified: true
solve_time_s: 190
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e389b-22c4-83ec-a133-59a777b0e455
---

# CF 1358A - Park Lighting

**Rating:** 800  
**Tags:** greedy, math  
**Model:** gpt-5-3-mini  
**Solve time:** 3m 10s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e389b-22c4-83ec-a133-59a777b0e455  

---

## Solution

## Problem Understanding

We are given a rectangular grid of size $n \times m$, where each cell represents a square plot in a park. The grid is surrounded by streets, and there are also streets between every pair of adjacent cells horizontally and vertically. Lanterns can be placed on these street segments, and each lantern illuminates the two cells adjacent to the street where it is placed. If the lantern is on the outer boundary of the grid, it only lights a single cell because there is only one adjacent square.

The task is to determine the minimum number of lanterns needed so that every cell in the grid is illuminated by at least one lantern.

The constraints allow up to $10^4$ test cases, and each grid dimension can be as large as $10^4$. This immediately rules out any per-cell simulation or construction of the grid. Any solution must work in constant time per test case, since even $O(nm)$ per test case would explode to $10^8$ operations per test in the worst case.

A subtle edge case appears when one or both dimensions are very small. In a $1 \times 1$ grid, a single lantern is needed. In a $1 \times m$ or $n \times 1$ strip, each lantern covers up to two cells, but boundary behavior reduces efficiency, and a naive pairing argument must be carefully applied. For example, in $1 \times 3$, the answer is 2, not 1, because one lantern covers at most two adjacent cells and the third remains uncovered.

## Approaches

A brute-force approach would simulate placing lanterns and marking illuminated cells, possibly trying all placements or greedily filling uncovered cells. One might imagine iterating over each street segment and placing lanterns until all cells are lit. This would require maintaining a grid of coverage and repeatedly scanning for uncovered cells, leading to at least $O(nm)$ work per test case, and likely worse if we attempt any search or optimization over placements.

This fails because the grid can be extremely large and the number of test cases is also large. The structure of the problem is highly regular: every lantern always covers exactly two adjacent cells unless it is on the boundary. This means coverage is essentially about pairing cells efficiently.

The key observation is that we want to cover all $n \times m$ cells using objects that each cover up to 2 cells. If we ignore boundaries for a moment, we would need roughly $\lceil \frac{nm}{2} \rceil$ lanterns. However, because lanterns are constrained to edges of the grid, we cannot freely pair arbitrary cells, but the grid structure still allows an optimal construction that achieves exactly $\left\lceil \frac{n \cdot m}{2} \right\rceil$.

This is not obvious at first glance, but the grid can be decomposed into disjoint adjacent pairs in a checkerboard-like fashion. Each lantern effectively covers an edge of the grid graph, and the grid graph is bipartite with a perfect or near-perfect matching depending on parity. The minimum number of edges needed to cover all vertices corresponds to pairing all cells except possibly one, which appears only when $n \cdot m$ is odd.

So the problem reduces to counting how many pairs of cells we can form, which is exactly the ceiling of half the number of cells.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(nm)$ per test | $O(nm)$ | Too slow |
| Optimal Pairing Insight | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the integers $n$ and $m$. These define the total number of cells $n \cdot m$, which we want to cover using lanterns that each illuminate up to two cells.
2. Compute the total number of cells as $c = n \cdot m$. This is the core quantity because each lantern contributes at most two units of coverage.
3. If $c$ is even, return $c / 2$. Every cell can be perfectly paired with another cell, meaning each lantern covers exactly one pair.
4. If $c$ is odd, return $c / 2 + 1$. One cell remains unpaired, and it requires a dedicated lantern placement that ends up covering only one cell effectively.

The correctness hinges on the fact that the grid allows a full matching of adjacent cells in a checkerboard coloring. Adjacent cells always have opposite parity, so pairing is always structurally feasible across the grid.

## Why it works

The grid can be viewed as a bipartite graph where each cell is a node and edges connect orthogonal neighbors. Each lantern corresponds to selecting an edge, which covers its two endpoints. The goal is to select the minimum number of edges such that every node is incident to at least one chosen edge.

On a bipartite grid graph, it is always possible to find a matching that covers all vertices except possibly one when the total number of vertices is odd. This guarantees that the best achievable coverage pairs up all but at most one cell. Therefore the answer depends only on the parity of $n \cdot m$, giving $\lceil \frac{n \cdot m}{2} \rceil$.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    print((n * m + 1) // 2)
```

The implementation directly computes the number of cells and applies the ceiling division formula. The expression $(n * m + 1) // 2$ avoids floating point operations and correctly handles both even and odd cases.

The only subtle point is using integer arithmetic instead of division, which ensures correctness for large inputs and avoids precision issues.

## Worked Examples

We trace two cases: $1 \times 3$ and $3 \times 3$.

For $1 \times 3$, the total number of cells is 3.

| Step | n | m | n·m | Expression | Result |
| --- | --- | --- | --- | --- | --- |
| Compute | 1 | 3 | 3 | (3 + 1)//2 | 2 |

This shows that even though we might try to place one lantern covering two cells, one cell remains, requiring a second lantern.

For $3 \times 3$, the total number of cells is 9.

| Step | n | m | n·m | Expression | Result |
| --- | --- | --- | --- | --- | --- |
| Compute | 3 | 3 | 9 | (9 + 1)//2 | 5 |

This confirms that an odd-sized grid always leaves one uncovered cell in any perfect pairing scheme, requiring one additional lantern.

These traces confirm that the solution depends only on parity and not on geometry beyond the bipartite pairing structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ per test case | Only arithmetic operations are performed |
| Space | $O(1)$ | No auxiliary data structures are used |

The solution easily fits within constraints since even $10^4$ test cases require only $10^4$ constant-time computations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        out.append(str((n * m + 1) // 2))
    return "\n".join(out)

# provided samples
assert run("5\n1 1\n1 3\n2 2\n3 3\n5 3\n") == "1\n2\n2\n5\n8"

# minimum grid
assert run("1\n1 1\n") == "1"

# single row
assert run("1\n1 5\n") == "3"

# single column
assert run("1\n4 1\n") == "2"

# even grid
assert run("1\n2 4\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | smallest grid |
| 1 5 | 3 | single row pairing |
| 4 1 | 2 | single column pairing |
| 2 4 | 4 | even grid perfect pairing |

## Edge Cases

For a $1 \times 1$ grid, there is only one cell. The algorithm computes $(1 \cdot 1 + 1)//2 = 1$, which matches the fact that at least one lantern is needed even though it only lights a single cell.

For a $1 \times 3$ grid, the computation gives $(3 + 1)//2 = 2$. Conceptually, only one pair can be formed, leaving one cell uncovered, which forces a second lantern.

For a $2 \times 2$ grid, the computation gives $(4 + 1)//2 = 2$. The grid can be perfectly partitioned into two adjacent pairs, so every cell is covered with exactly two lanterns, confirming optimal pairing without waste.