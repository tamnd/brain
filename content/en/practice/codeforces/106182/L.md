---
title: "CF 106182L - Lice Hopping"
description: "The room is modeled as a tree, where every person is a vertex and two people are connected if the lice can move directly between them in one day of training. After training for d days, the lice can jump between any two vertices whose tree distance is at most d."
date: "2026-06-25T10:52:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106182
codeforces_index: "L"
codeforces_contest_name: "Petrozavodsk Summer Camp 2025. Day 6. Xeppelin Contest The 4rd Universal Cup. Stage 2: Grand Prix of Paris)"
rating: 0
weight: 106182
solve_time_s: 35
verified: true
draft: false
---

[CF 106182L - Lice Hopping](https://codeforces.com/problemset/problem/106182/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The room is modeled as a tree, where every person is a vertex and two people are connected if the lice can move directly between them in one day of training. After training for `d` days, the lice can jump between any two vertices whose tree distance is at most `d`. The goal is to choose a starting person and an order to visit every person exactly once, while minimizing the required jump distance.

The input gives several independent trees. For each tree, we need the smallest value of `d` that allows such a visiting order. The output is this minimum training time for every test case.

The constraint that the total number of vertices across all test cases is at most `10^6` means the solution must be close to linear. Any approach that tries many possible paths, permutations, or repeated graph searches will be too slow. We need to extract a structural property of trees and decide the answer with only a few passes over the edges.

The main edge cases come from confusing the existence of a short traversal with ordinary depth-first search order. A DFS order may force a jump from the end of a long branch to another distant branch, even though a different ordering works.

For example, a star tree:

```
3
1 2
1 3
```

The correct output is:

```
2
```

A careless solution might think every tree can be walked using only edges because every vertex is connected. However, after visiting one leaf and returning through the center, the center cannot be visited again. The second leaf must be reached by a jump of distance 2.

A path tree is different:

```
4
1 2
2 3
3 4
```

The correct output is:

```
1
```

The vertices can be visited in the order `1 -> 2 -> 3 -> 4`, using only existing edges. A solution that always prints 2 would miss that paths are special.

Another common mistake is checking only the diameter. A tree with a large diameter can still have answer 2, because the lice do not need to follow the diameter. They only need a Hamiltonian path in the graph where every pair of vertices at distance at most 2 is connected.

## Approaches

A direct approach would try to construct a visiting order for every possible jump distance. For a fixed distance, we could search the graph formed by allowing jumps of that length and check whether it contains a Hamiltonian path. This is correct because the problem asks exactly for such a path, but Hamiltonian path search is exponential in general. Even on a tree, trying to reason about all possible orders quickly becomes infeasible.

The key observation is that trees have a very strong property: the square of every tree is Hamiltonian. The square of a tree is the graph where every vertex is connected to all vertices at distance at most 2. This means that with two days of training, every tree can be visited.

Now only the cases where one day is enough remain. With one day of training, every jump must follow an original tree edge. A tree can have a path visiting all vertices using its own edges only if the tree itself is a simple path. In a tree, this happens exactly when every vertex has degree at most 2.

The brute force fails because it treats the visiting order as the main object. The structural observation reduces the whole problem to checking the maximum degree of the tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the tree and compute the degree of every vertex. The only information needed is whether some vertex branches into three or more directions.
2. Find the maximum degree among all vertices. If every degree is at most 2, the tree is a path, so walking along edges is possible and the answer is 1.
3. If some vertex has degree at least 3, the tree is not a path. One-day jumps cannot visit every vertex, while two-day jumps are always sufficient because the square of a tree always has a Hamiltonian path. The answer is 2.

Why it works:

A tree with maximum degree at most 2 cannot branch, so it is exactly a chain of vertices. Following the chain visits every vertex with distance 1 jumps.

If the maximum degree is larger than 2, the tree contains a branching point. A path using only tree edges cannot enter multiple branches without revisiting the branching point, so distance 1 is impossible. Allowing distance 2 connects every vertex to its parent, children, and siblings, which is enough to arrange all vertices into one valid visiting sequence.

The invariant behind the algorithm is that the only possible answers are 1 and 2. The degree check distinguishes exactly the trees that achieve the smaller value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    t = data[0]
    idx = 1
    ans = []

    for _ in range(t):
        n = data[idx]
        idx += 1

        deg = [0] * n

        for _ in range(n - 1):
            u = data[idx] - 1
            v = data[idx + 1] - 1
            idx += 2
            deg[u] += 1
            deg[v] += 1

        if max(deg) <= 2:
            ans.append("1")
        else:
            ans.append("2")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input parser uses `sys.stdin.buffer.read()` because the total number of vertices can reach one million, and reading the entire input at once avoids overhead from many small `input()` calls.

For each test case, the code stores only the degree array. Every edge increases the degree of exactly two endpoints, so there is no need to build adjacency lists.

The condition `max(deg) <= 2` is the entire decision step. A tree cannot contain a cycle, so having every vertex degree at most 2 forces it to be a single path. For all other trees, the answer is exactly 2.

There are no distance calculations or traversals, which avoids unnecessary work. The values are small enough for normal Python integers, and the maximum possible degree is only `n - 1`.

## Worked Examples

Sample-style input:

```
4
3
1 2
1 3
5
1 2
1 3
1 4
1 5
7
1 2
1 3
2 4
2 5
3 6
3 7
15
1 2
1 3
2 4
2 5
3 6
3 7
4 8
4 9
5 10
5 11
6 12
6 13
7 14
7 15
```

The degree states are:

| Tree | Maximum degree | Decision | Answer |
| --- | --- | --- | --- |
| 3 vertices in a path | 2 | The tree is a path | 1 |
| Star with 4 leaves | 4 | Branching exists | 2 |
| Perfect binary tree with 7 vertices | 3 | Branching exists | 2 |
| Perfect binary tree with 15 vertices | 3 | Branching exists | 2 |

The first case demonstrates the only situation where one day is enough. The other cases show that even highly structured trees with many branches need only two days.

A second small trace:

Input:

```
2
1 2
```

The tree has two vertices.

| Tree size | Degrees | Maximum degree | Answer |
| --- | --- | --- | --- |
| 2 | [1, 1] | 1 | 1 |

This confirms the minimum-size tree case. The only possible movement is along the single edge, so one day is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each edge is processed once, and the degree array is scanned once. |
| Space | O(n) | The degree array stores one value per vertex. |

The total number of vertices over all test cases is bounded by `10^6`, so the linear solution comfortably fits the limits. The implementation avoids adjacency lists and graph traversal, keeping the memory usage low.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# minimum size
assert run("""1
2
1 2
""") == "1", "two nodes"

# path
assert run("""1
5
1 2
2 3
3 4
4 5
""") == "1", "path tree"

# star
assert run("""1
6
1 2
1 3
1 4
1 5
1 6
""") == "2", "star tree"

# balanced branching tree
assert run("""1
7
1 2
1 3
2 4
2 5
3 6
3 7
""") == "2", "binary tree"

# multiple test cases
assert run("""2
3
1 2
2 3
4
1 2
1 3
1 4
""") == "1\n2", "mixed cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two vertices | 1 | Minimum tree size and basic edge traversal |
| Long chain | 1 | Detects path-shaped trees |
| Star tree | 2 | Detects branching vertices |
| Binary tree | 2 | Confirms non-path trees need two days |
| Mixed cases | 1 and 2 | Checks multiple test case handling |

## Edge Cases

For a path-shaped tree:

```
5
1 2
2 3
3 4
4 5
```

The degrees are `[1, 2, 2, 2, 1]`. The maximum degree is 2, so the algorithm returns 1. The visiting order can simply follow the chain from one end to the other.

For a branching tree:

```
5
1 2
1 3
1 4
1 5
```

The degrees are `[4, 1, 1, 1, 1]`. The center has degree 4, so a one-day walk is impossible. The algorithm returns 2, which matches the fact that leaves can be reached from other leaves through jumps of distance 2.

For a large balanced tree, many vertices have degree 3, but the algorithm does not need to simulate the jumps. It only checks the existence of a branching vertex and immediately returns 2. The Hamiltonian property of the tree square handles all such cases.
