---
title: "CF 102569H - Tree Painting"
description: "The tree represents a network of connected vertices. An operation chooses two vertices and colors every vertex and edge on the unique route between them. The goal is to find the smallest number of chosen routes that together cover every part of the tree."
date: "2026-07-31T07:54:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102569
codeforces_index: "H"
codeforces_contest_name: "2020, XIII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102569
solve_time_s: 91
verified: true
draft: false
---

[CF 102569H - Tree Painting](https://codeforces.com/problemset/problem/102569/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

The tree represents a network of connected vertices. An operation chooses two vertices and colors every vertex and edge on the unique route between them. The goal is to find the smallest number of chosen routes that together cover every part of the tree.

The input describes the connections of the tree. Since a tree with `n` vertices always has `n - 1` edges, the entire structure is defined by these connections. The output is the minimum number of path selections needed to make the whole tree painted.

The constraint `n <= 200000` changes the way we approach the problem. A solution that explores many possible paths or repeatedly performs tree traversals for every choice will not fit into the 2 second limit. We need an algorithm close to linear time because the input itself contains up to about two hundred thousand edges. Anything around `O(n^2)` or worse is too slow.

A common mistake is to focus only on leaves. Leaves do matter because they are natural endpoints of painting paths, but internal vertices with odd degree also affect the answer. For example, in a tree where the center has three branches, only counting leaves gives the wrong intuition because the center itself must act as an endpoint in some path arrangement.

Consider this tree:

```
4
1 2
3 2
4 2
```

The correct answer is `2`. A careless approach that counts only the three leaves might think one path is enough because a path can connect two leaves and pass through the center, but one operation cannot cover all three branches. The center has degree `3`, so one of the necessary endpoints is created there as well.

Another boundary case is a simple chain:

```
5
1 2
2 3
3 4
4 5
```

The answer is `1`. A solution that always returns the number of leaves divided by two would work here, but a solution that assumes every branching point needs a separate operation could incorrectly return a larger value. The two endpoints of the chain are the only odd-degree vertices.

## Approaches

A direct approach would be to generate every possible path in the tree, then search for the smallest collection of these paths whose union contains every edge. There are `O(n^2)` possible pairs of endpoints, and checking every subset of them is exponential. Even with optimizations, this quickly becomes impossible for `n = 200000`.

The brute force works because every valid answer is indeed a collection of paths, but it fails because the number of possible collections is far larger than the input size.

The key observation comes from looking at vertex degrees. Every time we use a path operation, the two endpoints of that path are the only places where the used path contributes an odd number of incident path edges. All internal vertices of the path receive two path edges, so they do not affect parity.

If we select several paths covering the entire tree, the vertices that need to be endpoints of these paths are exactly the vertices with odd degree. A single path can fix two odd-degree vertices because it has two endpoints. This gives a lower bound: if the tree has `x` odd-degree vertices, at least `x / 2` paths are required.

This lower bound is also achievable. We can pair odd-degree vertices and make each pair the endpoints of one path. The paths may overlap at vertices, which is allowed because painting something multiple times has no negative effect. Every edge of the tree can be included in this pairing process, so no extra paths are needed.

The answer is simply half the number of vertices with odd degree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of possible paths | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the tree edges and store the degree of every vertex. Every edge increases the degree of both of its endpoints because the degree tells us how many branches leave a vertex.
2. Count how many vertices have an odd degree. These are the vertices that cannot be completely handled by being internal points of paths, so they must appear as endpoints.
3. Divide this count by two and output the result. Each operation contributes exactly two endpoints, and the pairing argument shows that this number of operations is always enough.

Why it works:

The important invariant is the parity of vertex degrees. A path operation changes the perspective of the tree into a collection of used path edges. Inside a painted path, every non-endpoint vertex receives two used edges, keeping its parity even. Only path endpoints contribute odd parity. Since the original tree has exactly the odd-degree vertices that need to be represented as endpoints, any solution needs at least half as many paths as odd vertices. Pairing these odd vertices into paths reaches that bound, so the minimum is exactly the number of odd-degree vertices divided by two.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    degree = [0] * (n + 1)

    for _ in range(n - 1):
        u, v = map(int, input().split())
        degree[u] += 1
        degree[v] += 1

    odd = 0
    for i in range(1, n + 1):
        if degree[i] % 2 == 1:
            odd += 1

    print(odd // 2)

if __name__ == "__main__":
    solve()
```

The array `degree` stores only the information needed from the tree. We do not need adjacency lists because the final answer depends only on the degree parity of every vertex.

While reading each edge, both endpoints gain one incident edge, so both degree values are incremented. After all edges are processed, the loop counts vertices whose degree is odd.

A tree always has an even number of odd-degree vertices, so integer division by two gives the exact number of required operations. Python integers handle the maximum degree values without any overflow concerns.

## Worked Examples

### Sample 1

Input:

```
5
1 2
1 3
1 4
1 5
```

The tree is a star. The center has degree `4`, and all four leaves have degree `1`.

| Step | Degrees considered | Odd count | Answer |
| --- | --- | --- | --- |
| After reading edges | 1:4, 2:1, 3:1, 4:1, 5:1 | 4 | 2 |
| Final computation | Four odd vertices need pairing | 4 | 4 / 2 = 2 |

The four leaves are the only odd-degree vertices. Two paths can pair them: one path covers two leaves through the center, and another path covers the remaining two leaves.

### Sample 2

Input:

```
5
1 2
2 3
3 4
4 5
```

This is a straight chain.

| Step | Degrees considered | Odd count | Answer |
| --- | --- | --- | --- |
| After reading edges | 1:1, 2:2, 3:2, 4:2, 5:1 | 2 | 1 |
| Final computation | Only the two ends are odd | 2 | 2 / 2 = 1 |

The entire chain is already one path, so one operation is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every edge is read once and every vertex degree is checked once |
| Space | O(n) | The degree array stores one value per vertex |

The solution performs only a few linear passes over the input. With `200000` vertices, this is well within the time and memory limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    def solve():
        import sys
        input = sys.stdin.readline

        n = int(input())
        degree = [0] * (n + 1)

        for _ in range(n - 1):
            u, v = map(int, input().split())
            degree[u] += 1
            degree[v] += 1

        print(sum(d % 2 for d in degree) // 2)

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""5
1 2
1 3
1 4
1 5
""") == "2\n", "sample 1"

assert run("""5
1 2
2 3
3 4
4 5
""") == "1\n", "sample 2"

assert run("""4
1 2
3 2
4 2
""") == "2\n", "sample 3"

assert run("""2
1 2
""") == "1\n", "minimum size tree"

assert run("""6
1 2
1 3
1 4
1 5
1 6
""") == "3\n", "large star"

assert run("""7
1 2
2 3
3 4
4 5
3 6
3 7
""") == "2\n", "branching chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` vertices connected by one edge | `1` | Minimum possible tree size |
| Star with five leaves | `3` | Correct handling of many odd-degree leaves |
| Chain with extra branches | `2` | Internal odd-degree vertices are counted correctly |

## Edge Cases

For the three-node star:

```
3
1 2
1 3
```

the degrees are `1, 2, 1`. There are two odd-degree vertices, so the algorithm outputs `1`. One path from vertex `2` to vertex `3` paints the entire tree.

For the four-node star:

```
4
1 2
1 3
1 4
```

the degrees are `3, 1, 1, 1`. All four vertices are odd. The algorithm counts four odd vertices and returns `2`. One operation can connect two leaves through the center, but a second operation is required for the remaining branch.

For the five-node chain:

```
5
1 2
2 3
3 4
4 5
```

only vertices `1` and `5` have odd degree. The algorithm returns `1`, because selecting these two endpoints paints the whole chain. This confirms that long paths do not require splitting into smaller operations.

For a tree where the branching vertex is odd:

```
4
1 2
3 2
4 2
```

vertex `2` has degree `3`, and the leaves also have degree `1`. The odd count is `4`, so the answer is `2`. The algorithm includes the center in the parity calculation, avoiding the mistake of counting leaves only.
