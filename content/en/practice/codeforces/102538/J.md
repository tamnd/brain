---
title: "CF 102538J - Just Counting"
description: "We have an undirected graph. Every edge must receive one value from the set of residues modulo five, meaning the possible values are 0, 1, 2, 3, 4. A labeling is valid when every vertex has incident edge values whose sum is divisible by five."
date: "2026-08-03T21:05:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102538
codeforces_index: "J"
codeforces_contest_name: "300iq Contest 3"
rating: 0
weight: 102538
solve_time_s: 75
verified: true
draft: false
---

[CF 102538J - Just Counting](https://codeforces.com/problemset/problem/102538/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected graph. Every edge must receive one value from the set of residues modulo five, meaning the possible values are `0, 1, 2, 3, 4`. A labeling is valid when every vertex has incident edge values whose sum is divisible by five.

The task is to count how many valid edge labelings exist. The answer is printed modulo `998244353`.

The input consists of several graph instances. Each instance gives the number of vertices and edges, followed by the pairs of vertices connected by every edge. The graph can be disconnected, so each connected component must be handled independently.

The constraints make a linear or almost linear solution necessary. The total number of vertices and edges across all test cases is bounded, so a traversal of the graph is affordable. Any approach that tries to enumerate assignments has no chance because each edge has five choices, giving `5^m` possibilities. Even moderately sized graphs make this astronomically large.

The main hidden difficulty is understanding the number of independent constraints. A common mistake is to assume that every vertex condition removes one degree of freedom. That is false because the vertex equations are not always independent. A tree and an odd cycle behave differently, and disconnected components multiply their contributions.

For example, a single isolated vertex has no edges.

```
1 0
```

There is only one empty assignment, so the answer is `1`. A solution that assumes every connected component contributes a cycle degree of freedom would incorrectly add something here.

A triangle is another important case.

```
3 3
1 2
2 3
3 1
```

The answer is `1`. The three vertex equations are independent over modulo five because the cycle is odd. Treating every cycle as adding one free variable would incorrectly produce `5`.

A square shows the opposite behavior.

```
4 4
1 2
2 3
3 4
4 1
```

The answer is `5`. The alternating assignment around an even cycle creates one free variable. A method that only checks whether the graph contains a cycle, without checking whether it is odd or even, would miss this.

## Approaches

A direct solution would try every possible assignment of values to edges and test the vertex sums. This is correct because every possible labeling is examined, and only valid ones are counted. However, with `m` edges this requires `5^m` assignments. For a graph with hundreds of thousands of edges this is impossible.

The useful observation comes from viewing the problem as a linear system over the field modulo five. Each edge is a variable. Each vertex gives an equation requiring the sum of adjacent edge variables to be zero. If there are `m` variables and the system has rank `r`, the number of solutions is:

`5^(m-r)`

The entire problem becomes finding the rank of the incidence-like matrix of the graph.

For a connected component with `n` vertices, the rank depends only on whether the component is bipartite. If the component is bipartite, the vertex equations have one dependency, so the rank is `n-1`. If the component is not bipartite, the odd cycle removes that dependency and the rank becomes `n`.

The brute-force method works because the equations completely describe the valid assignments, but fails because it ignores the structure of the linear system. The observation that only the rank matters lets us replace exponential enumeration with graph traversal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(5^m · (n+m)) | O(n+m) | Too slow |
| Optimal | O(n+m) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list of the graph. Each edge is stored in both directions because later we need to traverse connected components and test bipartiteness.
2. Run a breadth-first search or depth-first search from every unvisited vertex. During the traversal, assign each vertex one of two colors. If an edge connects two vertices with the same color, the component is not bipartite.
3. Count the number of vertices and edges inside the current connected component. If the component is bipartite, add `vertices - 1` to the total rank. Otherwise, add `vertices` to the total rank.

The reason the edge count does not need to be used directly is that every component contributes according to its number of vertices and its parity structure. The number of edges only appears later in the exponent.

1. After processing all components, compute the answer as:

`5^(total_edges - total_rank)`

using modular exponentiation.

Why it works:

The graph equations form a linear system over modulo five. The number of solutions to a homogeneous linear system with `m` variables and rank `r` is exactly `5^(m-r)`, because every free variable can independently take one of five values.

For a connected bipartite component, the sum of all vertex equations with alternating signs cancels every edge, creating one dependency. The rank is therefore one less than the number of vertices. For a non-bipartite component, an odd cycle prevents that dependency, so the rank equals the number of vertices. Summing these ranks over connected components gives the rank of the full system, which makes the final exponent correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    t = int(next(it))
    ans = []

    for _ in range(t):
        n = int(next(it))
        m = int(next(it))

        g = [[] for _ in range(n)]
        for _ in range(m):
            a = int(next(it)) - 1
            b = int(next(it)) - 1
            g[a].append(b)
            g[b].append(a)

        color = [-1] * n
        rank = 0

        for start in range(n):
            if color[start] != -1:
                continue

            color[start] = 0
            stack = [start]
            vertices = 0
            bipartite = True

            while stack:
                v = stack.pop()
                vertices += 1

                for u in g[v]:
                    if color[u] == -1:
                        color[u] = color[v] ^ 1
                        stack.append(u)
                    elif color[u] == color[v]:
                        bipartite = False

            if bipartite:
                rank += vertices - 1
            else:
                rank += vertices

        ans.append(str(pow(5, m - rank, MOD)))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The adjacency list construction corresponds to the first algorithm step. Every edge appears twice, but this only affects traversal time, not the mathematical count.

The DFS stack maintains the current connected component. The array `color` stores the two-coloring attempt. When a previously visited neighbor has the same color, the component contains an odd cycle, so it is not bipartite.

The variable `rank` stores the total rank contribution of all components. The final call to `pow` uses Python's modular exponentiation, which avoids constructing the enormous value `5^(m-rank)` directly.

There are no overflow concerns because Python integers are arbitrary precision and the modular exponentiation keeps intermediate values controlled. The exponent is never negative because the rank of the system cannot exceed the number of edge variables.

## Worked Examples

For the triangle:

```
3 3
1 2
2 3
3 1
```

The traversal behaves as follows.

| Current component | Vertices found | Bipartite | Rank contribution | Exponent |
| --- | --- | --- | --- | --- |
| triangle | 3 | no | 3 | 3 - 3 = 0 |

The triangle has an odd cycle, so there is no free variable. The answer is `5^0 = 1`.

For the square:

```
4 4
1 2
2 3
3 4
4 1
```

The traversal gives:

| Current component | Vertices found | Bipartite | Rank contribution | Exponent |
| --- | --- | --- | --- | --- |
| square | 4 | yes | 3 | 4 - 3 = 1 |

The even cycle creates one degree of freedom. The answer is `5^1 = 5`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n+m) | Every vertex and edge is visited a constant number of times |
| Space | O(n+m) | The adjacency list and traversal arrays store the graph |

The total input size is bounded, so a linear traversal easily fits within the intended limits. The solution avoids any dependence on the number of possible edge assignments.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 998244353

def solution(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    res = []

    for _ in range(t):
        n, m = map(int, input().split())
        g = [[] for _ in range(n)]

        for _ in range(m):
            a, b = map(int, input().split())
            a -= 1
            b -= 1
            g[a].append(b)
            g[b].append(a)

        color = [-1] * n
        rank = 0

        for i in range(n):
            if color[i] != -1:
                continue

            stack = [i]
            color[i] = 0
            cnt = 0
            ok = True

            while stack:
                v = stack.pop()
                cnt += 1
                for u in g[v]:
                    if color[u] == -1:
                        color[u] = color[v] ^ 1
                        stack.append(u)
                    elif color[u] == color[v]:
                        ok = False

            rank += cnt - 1 if ok else cnt

        res.append(str(pow(5, m - rank, MOD)))

    return "\n".join(res)

assert solution("""3
1 0
3 3
1 2
2 3
3 1
4 4
1 2
2 3
3 4
4 1
""") == """1
1
5""", "samples"

assert solution("""1
2 0
""") == "1", "isolated vertices"

assert solution("""1
5 4
1 2
2 3
3 4
4 5
""") == "1", "tree"

assert solution("""1
6 6
1 2
2 3
3 4
4 5
5 6
6 1
""") == "5", "even cycle"

assert solution("""1
5 5
1 2
2 3
3 4
4 5
5 1
""") == "1", "odd cycle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex with no edges | `1` | Empty assignment handling |
| A tree | `1` | Bipartite component with no cycles |
| An even cycle | `5` | One free variable from an even cycle |
| An odd cycle | `1` | Full rank in a non-bipartite component |

## Edge Cases

For an isolated vertex:

```
1 0
```

The component contains one vertex and no edges. It is bipartite, so its rank contribution is `1-1=0`. The exponent is `0-0=0`, giving `1`. The algorithm does not incorrectly remove a degree of freedom that does not exist.

For a tree:

```
5 4
1 2
2 3
3 4
4 5
```

The graph is bipartite. The component rank is `5-1=4`, matching the number of edges. The exponent is zero, so every edge value is forced and only the all-zero assignment remains.

For an odd cycle:

```
3 3
1 2
2 3
3 1
```

The coloring attempt detects a conflict when the last edge joins two equally colored vertices. The component rank becomes `3` instead of `2`. The exponent becomes zero, which correctly gives only one valid assignment.

For an even cycle:

```
4 4
1 2
2 3
3 4
4 1
```

The coloring succeeds. The rank contribution is `3`, leaving one free edge variable. The exponent is one, so the component contributes five solutions. The algorithm captures the extra freedom without explicitly constructing the cycle.
