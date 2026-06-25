---
title: "CF 106160C - Coherency"
description: "Each model is represented by a circle on a very large board. The input gives the center coordinates of the circle and its diameter. Two models are considered directly connected when the distance between the edges of their bases is at most two inches."
date: "2026-06-25T11:11:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106160
codeforces_index: "C"
codeforces_contest_name: "2025 Benelux Algorithm Programming Contest (BAPC 25)"
rating: 0
weight: 106160
solve_time_s: 56
verified: true
draft: false
---

[CF 106160C - Coherency](https://codeforces.com/problemset/problem/106160/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

Each model is represented by a circle on a very large board. The input gives the center coordinates of the circle and its diameter.

Two models are considered directly connected when the distance between the edges of their bases is at most two inches. Since all coordinates and diameters are given in millimeters, two inches equals 50.8 mm.

If we build a graph where every model is a vertex and every directly connected pair is an edge, then a collection is coherent when two conditions hold.

First, the graph must be connected. Every model must be reachable from every other model through a chain of direct connections.

Second, when the unit contains at least seven models, every model must have degree at least two. A model that is connected to only one neighbor is not sufficient.

The input size is the main challenge. There can be up to 200,000 models. A naive check of every pair would require roughly

$$\frac{200000 \cdot 199999}{2} \approx 2 \cdot 10^{10}$$

distance computations, which is completely impossible.

The key geometric observation is that bases are small. The largest diameter is only 160 mm, so the largest possible connection distance between centers is

$$80 + 80 + 50.8 = 210.8 \text{ mm}.$$

No edge can ever connect models whose centers are farther apart than 210.8 mm.

This bounded interaction radius is what makes a spatial partitioning solution possible.

A subtle edge case appears when two models are exactly at the allowed distance. For example:

```
2
13 13 25
88 13 25
```

The center distance is 75 mm. The radii sum is 25 mm. The gap between bases is exactly 50 mm, which is within 50.8 mm, so the answer is `yes`.

A strict `<` comparison would incorrectly reject such cases.

Another important case is a connected graph with seven or more models where one vertex has degree one.

```
7
...
```

Even though the graph is connected, the answer must be `no` because the degree requirement becomes active once the unit size reaches seven.

A third source of mistakes is floating point precision. The threshold involves 50.8 mm. Comparing floating point distances directly can lead to borderline errors. The safest approach is to convert the condition into an integer comparison using squared distances.

## Approaches

The brute-force solution is straightforward. For every pair of models, compute whether they are directly connected. Whenever an edge exists, add it to the graph, update degrees, and merge the endpoints in a DSU. After all pairs are processed, verify connectivity and the degree condition.

This works because the definition of coherency is literally a graph property. The problem is the number of pairs. With 200,000 models, the pair count is about twenty billion, which is far beyond the time limit.

The reason we can do better is that edges are extremely local. Regardless of where a model is on the 100 km board, it can only connect to models whose centers are within 210.8 mm.

That suggests dividing the plane into square cells. If the cell side length is greater than the maximum possible connection radius, then any model can only connect to models in its own cell or one of the eight neighboring cells.

Using a cell size of 211 mm is enough because every possible edge has length at most 210.8 mm.

Now each model only needs to be compared against a small number of nearby models. Because bases never overlap, there is a lower bound on how close centers can be. Inside a constant-sized neighborhood, only a constant number of models can exist. The total number of comparisons becomes linear in practice and in the geometric packing argument.

Whenever a valid edge is found, we update the degree counts and merge the endpoints in a DSU. After processing all nearby pairs, we check whether all models belong to one component and whether every degree is at least two when $n \ge 7$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n α(n)) expected / geometric linear | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all models and store their coordinates and diameters.
2. Create a DSU with one node per model.
3. Choose a grid cell size of 211 mm. This is slightly larger than the maximum possible center-to-center connection distance.
4. Process models one by one. For a model at `(x, y)`, compute its cell coordinates:

$$(x // 211,\; y // 211)$$
5. Before inserting the model into the grid, inspect the nine cells consisting of its own cell and the eight neighboring cells.

Any model farther away than that cannot possibly be connected because the cell size already exceeds the maximum edge length.
6. For every previously stored model found in those cells, test whether an edge exists.

Let the diameters be `d1` and `d2`.

The connection condition is

$$\text{center distance}
\le
\frac{d_1+d_2}{2}+50.8$$

To avoid floating point arithmetic, rewrite it as

$$100 \cdot \text{dist}^2
\le
(5(d_1+d_2)+508)^2$$
7. Whenever the condition holds, increase both degrees and merge the two vertices in the DSU.
8. Insert the current model into its grid cell.
9. After all models are processed, verify that every model belongs to the same DSU component.
10. If `n >= 7`, verify that every degree is at least two.
11. Output `"yes"` if both checks pass, otherwise output `"no"`.

### Why it works

The grid never misses an edge. Every valid edge has length at most 210.8 mm, while each cell has side length 211 mm. Two points whose cells differ by more than one in either coordinate must be farther apart than 211 mm in at least one axis, making an edge impossible.

Every actual edge is tested exactly once when the later endpoint is processed. Whenever an edge exists according to the problem definition, the algorithm adds it to the DSU and updates the degree counts.

The DSU therefore represents exactly the connected components of the coherence graph, and the degree array contains exactly the graph degrees. The final checks are precisely the two conditions from the definition of a coherent unit.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

CELL = 211

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return

        if self.sz[a] < self.sz[b]:
            a, b = b, a

        self.p[b] = a
        self.sz[a] += self.sz[b]

def solve():
    n = int(input())

    models = []
    for _ in range(n):
        x, y, d = map(int, input().split())
        models.append((x, y, d))

    dsu = DSU(n)
    deg = [0] * n

    grid = defaultdict(list)

    for i, (x, y, d) in enumerate(models):
        cx = x // CELL
        cy = y // CELL

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                cell = (cx + dx, cy + dy)

                for j in grid.get(cell, []):
                    x2, y2, d2 = models[j]

                    dist2 = (x - x2) * (x - x2) + (y - y2) * (y - y2)

                    rhs = 5 * (d + d2) + 508

                    if 100 * dist2 <= rhs * rhs:
                        deg[i] += 1
                        deg[j] += 1
                        dsu.union(i, j)

        grid[(cx, cy)].append(i)

    root = dsu.find(0)

    for i in range(1, n):
        if dsu.find(i) != root:
            print("no")
            return

    if n >= 7:
        for d in deg:
            if d < 2:
                print("no")
                return

    print("yes")

solve()
```

The DSU tracks connectivity without explicitly storing the graph. Every discovered edge immediately merges its endpoints.

The geometric search is handled by the hash grid. A model is compared only with models already inserted into neighboring cells, which avoids duplicate checks.

The distance comparison is entirely integer-based. The expression

```
rhs = 5 * (d + d2) + 508
```

comes from multiplying the threshold by ten:

$$10 \cdot \left(\frac{d_1+d_2}{2}+50.8\right)
=
5(d_1+d_2)+508$$

Squaring both sides produces an exact integer comparison with no precision issues.

The connectivity check uses a single representative root. If any vertex belongs to a different DSU component, the graph is disconnected.

The degree condition is checked only when `n >= 7`, matching the problem statement exactly.

## Worked Examples

### Example 1

Input:

```
2
13 13 25
88 13 25
```

| i | Position | Degree Changes | Components |
| --- | --- | --- | --- |
| 0 | (13,13) | none | {0} |
| 1 | (88,13) | deg[0]++, deg[1]++ | {0,1} |

Final degrees:

| Vertex | Degree |
| --- | --- |
| 0 | 1 |
| 1 | 1 |

The graph is connected. Since `n < 7`, the degree rule does not apply. The answer is `yes`.

### Example 2

Input:

```
7
1066 910 130
1007 1032 130
875 1062 130
770 978 130
770 843 130
875 758 130
1007 788 130
```

| Vertex | Degree After Processing |
| --- | --- |
| 0 | 2 |
| 1 | 2 |
| 2 | 2 |
| 3 | 2 |
| 4 | 2 |
| 5 | 2 |
| 6 | 2 |

All vertices form a single cycle-like structure. The graph is connected and every degree is at least two. The answer is `yes`.

This example demonstrates why the degree condition is separate from connectivity. A connected graph alone would not be enough when seven or more models are present.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n α(n)) expected | Each model only interacts with nearby models in a constant-sized neighborhood |
| Space | O(n) | DSU, degree array, and grid storage |

The board is enormous, but the interaction radius is tiny and bounded. Spatial hashing keeps the number of distance checks proportional to the number of models, making the solution easily fast enough for 200,000 inputs.

## Test Cases

```python
# helper: run solution on input string, return output string
import io
import sys
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    CELL = 211

    class DSU:
        def __init__(self, n):
            self.p = list(range(n))
            self.sz = [1] * n

        def find(self, x):
            while self.p[x] != x:
                self.p[x] = self.p[self.p[x]]
                x = self.p[x]
            return x

        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)
            if a == b:
                return
            if self.sz[a] < self.sz[b]:
                a, b = b, a
            self.p[b] = a
            self.sz[a] += self.sz[b]

    n = int(input())
    models = [tuple(map(int, input().split())) for _ in range(n)]

    dsu = DSU(n)
    deg = [0] * n
    grid = defaultdict(list)

    for i, (x, y, d) in enumerate(models):
        cx = x // CELL
        cy = y // CELL

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in grid.get((cx + dx, cy + dy), []):
                    x2, y2, d2 = models[j]
                    dist2 = (x - x2) ** 2 + (y - y2) ** 2
                    rhs = 5 * (d + d2) + 508
                    if 100 * dist2 <= rhs * rhs:
                        deg[i] += 1
                        deg[j] += 1
                        dsu.union(i, j)

        grid[(cx, cy)].append(i)

    root = dsu.find(0)

    ok = True
    for i in range(n):
        if dsu.find(i) != root:
            ok = False

    if ok and n >= 7:
        ok = all(d >= 2 for d in deg)

    return ("yes\n" if ok else "no\n")

# provided samples
assert run("2\n13 13 25\n88 13 25\n") == "yes\n"
assert run("2\n13 13 25\n89 13 25\n") == "no\n"

# custom cases
assert run("2\n0 0 25\n1000 0 25\n") == "no\n"
assert run("3\n0 0 25\n50 0 25\n100 0 25\n") == "yes\n"
assert run("7\n0 0 25\n50 0 25\n100 0 25\n150 0 25\n200 0 25\n250 0 25\n300 0 25\n") == "no\n"
assert run("7\n100 0 130\n62 78 130\n-22 97 130\n-90 43 130\n-90 -43 130\n-22 -97 130\n62 -78 130\n") == "yes\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two far apart models | no | Disconnected graph |
| Three models in a chain | yes | Connectivity through intermediate vertices |
| Seven-model path | no | Degree condition activates |
| Seven-model cycle | yes | Connected and every degree at least two |

## Edge Cases

Consider two models exactly at the allowed threshold:

```
2
13 13 25
88 13 25
```

The center distance is 75. The threshold is

$$12.5 + 12.5 + 50.8 = 75.8.$$

The integer comparison accepts the edge because it uses `<=`, not `<`. The graph is connected, so the answer is `yes`.

Now consider a connected chain of seven models:

```
7
0 0 25
50 0 25
100 0 25
150 0 25
200 0 25
250 0 25
300 0 25
```

The graph is connected, but the endpoints have degree one. After edge processing, the degree array begins and ends with `1`. Since `n >= 7`, the algorithm rejects the unit and prints `no`.

Finally, consider a case near the floating point boundary. The algorithm never computes square roots and never stores 50.8 as a floating point threshold. It checks

$$100 \cdot \text{dist}^2
\le
(5(d_1+d_2)+508)^2$$

using integers only, so no rounding error can incorrectly change the result.
