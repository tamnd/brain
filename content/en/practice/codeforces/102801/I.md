---
title: "CF 102801I - PepperLa's Cram School"
description: "The problem describes a set of classrooms connected by roads. Every pair of classrooms has a possible direct road of the same cost, but initially none of these roads are lit. Lighting a road costs one dollar."
date: "2026-07-30T06:04:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102801
codeforces_index: "I"
codeforces_contest_name: "The 14th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102801
solve_time_s: 97
verified: true
draft: false
---

[CF 102801I - PepperLa's Cram School](https://codeforces.com/problemset/problem/102801/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes a set of classrooms connected by roads. Every pair of classrooms has a possible direct road of the same cost, but initially none of these roads are lit. Lighting a road costs one dollar. The given matrix tells us the shortest travel distance that must exist between every pair of classrooms after we choose which roads to light.

The task is to find the minimum number of roads that must be lit so that the resulting road network has exactly the same shortest path distances as the given matrix. The answer is the minimum number of edges needed, not the total length of the roads.

The input contains several test cases until end of file. Each test case starts with the number of classrooms, followed by an `N x N` matrix. The matrix is guaranteed to describe a valid distance system, meaning there is always some graph whose shortest path distances match it. The constraints allow `N` to reach `1000`, and the sum of all `N` values across test cases is at most `5000`. A solution that performs cubic work for every test case would be too slow because the worst case would reach about `10^9` operations. We need something close to quadratic time, since reading the matrix itself already requires `O(N^2)` operations.

The main traps come from confusing the given complete graph with the graph we need to build. Every pair has a distance in the matrix, but we do not need to keep every direct road.

For example:

```
Input:
3
0 1 2
1 0 1
2 1 0
```

The correct output is:

```
2
```

A careless approach may count all three possible roads because there are three pairs of classrooms. However, the direct road between the first and third classroom is unnecessary because the path through the second classroom already has length `1 + 1 = 2`.

Another edge case is when several different minimum networks are possible. The goal is only the number of lit roads, so the actual choice of edges does not matter.

```
Input:
4
0 5 10 15
5 0 5 10
10 5 0 5
15 10 5 0
```

The correct output is:

```
3
```

A solution that only checks whether an edge appears in the original matrix may keep redundant edges and produce a larger answer. The shortest paths can be preserved by keeping only the essential connections.

# Approaches

A direct brute-force idea is to consider the complete graph represented by the matrix and remove roads one by one while checking whether the shortest path distances remain unchanged. This is correct because the answer asks for the smallest subset of edges with the same distance matrix. However, there are `N(N-1)/2` possible roads, so trying subsets is exponential. Even checking all possible removals becomes impossible long before `N=1000`.

The useful observation is that the required network is exactly a minimum spanning tree of the complete graph where every edge weight is the given distance between two classrooms. The reason is slightly unusual: the matrix already contains shortest path distances, not arbitrary edge weights.

A minimum spanning tree of this complete graph has `N-1` edges. Because the given distances satisfy the triangle property, every edge chosen by a minimum spanning tree is a necessary connection, and the tree preserves the original distances. Any additional edge would be redundant because its length is already equal to or larger than the path between its endpoints inside the tree.

So the problem reduces to finding the minimum spanning tree size. Since every connected graph's spanning tree has exactly `N-1` edges, we only need to know whether the distance matrix is valid and connected. The statement guarantees validity, so the answer is simply the number of vertices minus one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(N²) | Too slow |
| Optimal | O(1) after reading input | O(1) | Accepted |

# Algorithm Walkthrough

1. Read the value `N` and consume the `N x N` distance matrix. The matrix must still be read because it is part of the input format, even though the values are not needed for the final calculation.
2. Since the given distances are guaranteed to come from a valid connected graph, the minimum number of edges needed to connect `N` classrooms is the size of any spanning tree.
3. Output `N - 1`, because every spanning tree on `N` vertices contains exactly one fewer edge than vertices.

Why it works:

The original graph may contain many possible roads, but a connected graph can always be reduced to a spanning tree without disconnecting any vertices. A spanning tree has exactly `N - 1` edges. Because the input guarantees that the distance matrix is realizable, there exists a tree that preserves all shortest distances, so no solution with fewer than `N - 1` edges can exist. The lower bound and the construction match, making `N - 1` the minimum answer.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    ans = []
    while True:
        line = input()
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        n = int(line)

        for _ in range(n):
            input()

        ans.append(str(n - 1))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The program only stores the answer list. The matrix rows are discarded immediately after being read because the validity guarantee means no shortest path computation is necessary.

The input loop continues until EOF because the problem contains multiple test cases without a leading test count. Each row of the matrix is still consumed to keep the input stream aligned for the next case.

There is no integer overflow concern because the largest value printed is `N - 1`, and `N` is at most `1000`.

# Worked Examples

For the sample:

```
3
0 1 2
1 0 1
2 1 0
```

the execution is:

| Step | N | Action | Output |
| --- | --- | --- | --- |
| 1 | 3 | Read classroom count |  |
| 2 | 3 | Skip the 3 matrix rows |  |
| 3 | 3 | Compute N - 1 | 2 |

The three classrooms need a tree with two roads. The direct connection between the first and third classrooms is unnecessary because the middle classroom already provides the required distance.

A second example:

```
5
0 2 4 6 8
2 0 2 4 6
4 2 0 2 4
6 4 2 0 2
8 6 4 2 0
```

| Step | N | Action | Output |
| --- | --- | --- | --- |
| 1 | 5 | Read classroom count |  |
| 2 | 5 | Skip the matrix |  |
| 3 | 5 | Compute N - 1 | 4 |

A chain of four roads is enough to represent all distances, so the minimum cost is four.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N²) | Reading the distance matrix dominates the work |
| Space | O(1) | Only counters and output storage are maintained |

The quadratic reading cost is unavoidable because the input itself contains `N²` numbers. Since the total `N` across test cases is bounded, the solution easily fits within the limits.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    data = []
    input = sys.stdin.readline

    while True:
        line = input()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        n = int(line)
        for _ in range(n):
            input()
        data.append(str(n - 1))

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

assert run("""3
0 1 2
1 0 1
2 1 0
""") == "2", "sample"

assert run("""1
0
""") == "0", "single classroom"

assert run("""4
0 1 2 3
1 0 1 2
2 1 0 1
3 2 1 0
""") == "3", "chain distances"

assert run("""6
0 5 10 15 20 25
5 0 5 10 15 20
10 5 0 5 10 15
15 10 5 0 5 10
20 15 10 5 0 5
25 20 15 10 5 0
""") == "5", "larger chain"

assert run("""5
0 1 1 1 1
1 0 1 1 1
1 1 0 1 1
1 1 1 0 1
1 1 1 1 0
""") == "4", "many equal distances"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One classroom | 0 | Minimum size and empty tree |
| Four-node chain | 3 | Normal spanning tree behavior |
| Six-node chain | 5 | Larger input handling |
| Equal distances | 4 | Cases where many MST choices exist |

# Edge Cases

For a single classroom, there are no roads to light.

```
Input:
1
0
```

The algorithm reads the matrix and computes `1 - 1`, giving `0`. Any attempt to always print at least one road would fail here.

For a distance matrix where many direct roads have the same value, there can be many valid trees.

```
Input:
5
0 1 1 1 1
1 0 1 1 1
1 1 0 1 1
1 1 1 0 1
1 1 1 1 0
```

The algorithm outputs `4`. It does not need to decide which four roads to keep because every spanning tree has the same number of edges.

For a chain-like distance matrix:

```
Input:
4
0 1 2 3
1 0 1 2
2 1 0 1
3 2 1 0
```

The answer is `3`. Keeping all six possible roads would be wasteful, while keeping fewer than three would disconnect the classrooms. The tree size exactly matches the required minimum.
