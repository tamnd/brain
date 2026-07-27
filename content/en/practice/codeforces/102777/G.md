---
title: "CF 102777G - \u0422\u043e\u0432\u0430\u0440\u0438\u0449 \u043c\u0430\u0439\u043e\u0440"
description: "The input describes a network of criminals. Each criminal is a vertex of an undirected graph, and each documented connection is an edge between two vertices. A criminal community is a connected group of criminals, but a single isolated criminal does not count as a community."
date: "2026-07-27T20:35:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102777
codeforces_index: "G"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102777
solve_time_s: 65
verified: true
draft: false
---

[CF 102777G - \u0422\u043e\u0432\u0430\u0440\u0438\u0449 \u043c\u0430\u0439\u043e\u0440](https://codeforces.com/problemset/problem/102777/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes a network of criminals. Each criminal is a vertex of an undirected graph, and each documented connection is an edge between two vertices. A criminal community is a connected group of criminals, but a single isolated criminal does not count as a community. The task is to determine how many connected components of the graph contain at least two vertices.

The first line gives the number of criminals and the number of recorded connections. The following pairs describe which criminals are directly connected. Connections can form chains, so two criminals belong to the same community even if there is no direct edge between them, as long as there is a path through other criminals. The output is the number of such non-trivial connected components.

The number of criminals is at most 100, and the number of connections can be as large as the square of the number of criminals. With these limits, even simple graph traversal methods are easily fast enough. A solution with time complexity around O(N + M) is much more than sufficient. More expensive approaches that repeatedly search all paths between all pairs of criminals are unnecessary and would perform much more work than the structure of the problem requires.

Several cases require care. A graph containing no real community should produce zero, even if vertices exist.

For example:

```
3 0
```

The answer is:

```
0
```

A careless implementation that counts every vertex as a component would incorrectly return 3.

A connected pair of criminals must count as one community.

Example:

```
2 1
0 1
```

The answer is:

```
1
```

An implementation that only looks for vertices with many edges might miss this, because each criminal has only one connection.

A self-connection does not turn an isolated criminal into a community.

Example:

```
3 1
1 1
```

The answer is:

```
0
```

The vertex has a loop, but the connected component still contains only one criminal. A solution that counts every component containing an edge would produce the wrong result.

## Approaches

A direct brute-force idea is to start from every criminal and search for all criminals reachable from it. After finding the reachable set, we could check whether its size is greater than one and count it as a community. To avoid counting the same community several times, we would need to keep track of which criminals have already been processed.

Without that optimization, the same component would be explored repeatedly. In the worst case, a dense graph with 100 criminals can have around 10,000 connections. Running a full traversal from every vertex would perform about O(N(N + M)) operations, which is around one million operations here. It would still pass for these constraints, but it ignores the simpler structure of the task.

The key observation is that a community is exactly a connected component of an undirected graph. We do not need to find paths between specific pairs of criminals. We only need to discover every connected region once and check its size.

A graph traversal such as depth-first search or breadth-first search naturally does this. Starting from an unvisited criminal, the traversal visits everyone in the same component. After the traversal finishes, we know the component size. If that size is at least two, it contributes one star.

The brute-force works because reachability can be discovered by graph traversal, but it fails conceptually because it repeats the same work. The observation that every criminal belongs to exactly one connected component lets us process each vertex and edge only once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N(N + M)) | O(N) | Works here, but unnecessary |
| Optimal | O(N + M) | O(N + M) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the graph. For every connection between two different criminals, store each endpoint in the other's list because the graph is undirected. A self-loop can be stored or ignored, since a component of size one never contributes to the answer.
2. Create an array that records whether each criminal has already been visited. Initially every criminal is unvisited because no connected component has been explored.
3. Iterate through all criminals. When an unvisited criminal is found, start a DFS from it and count how many vertices are reached. The traversal marks every criminal in this connected component, so later iterations will skip the same community.
4. After the DFS finishes, check the size of the discovered component. If it contains at least two criminals, increase the answer by one. A single visited vertex is only an isolated criminal, not a community.
5. Print the final number of counted components.

Why it works:

The invariant during the algorithm is that every completed DFS traversal represents exactly one connected component. DFS only moves along existing edges, so it cannot leave that component. At the same time, every vertex reachable through a path is eventually visited, so no member of the component is missed. Since every vertex starts one DFS only when it has not been seen before, every connected component is counted exactly once. The final size check removes single-vertex components, matching the definition of a criminal community.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        x, y = map(int, input().split())
        if x != y:
            graph[x].append(y)
            graph[y].append(x)

    visited = [False] * n
    answer = 0

    for start in range(n):
        if visited[start]:
            continue

        stack = [start]
        visited[start] = True
        size = 0

        while stack:
            v = stack.pop()
            size += 1

            for to in graph[v]:
                if not visited[to]:
                    visited[to] = True
                    stack.append(to)

        if size > 1:
            answer += 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The graph is stored as an adjacency list because traversal only needs to know which criminals are directly connected. Storing a full adjacency matrix would also fit the constraints, but it would use more memory and would make the solution less directly connected to the graph traversal idea.

The iterative DFS uses a stack instead of recursion. Python recursion depth can become a problem on long chains in larger graph tasks, so the explicit stack avoids that limitation.

The variable `size` counts vertices in the current connected component. It is checked only after the traversal ends because the algorithm must know the entire component size before deciding whether it represents a community.

Ignoring self-loops when building the graph is safe. A self-loop never creates another vertex in the component, and the only question that matters is whether the component size exceeds one.

## Worked Examples

### Sample 1

Input:

```
10 4
1 2
1 3
0 2
0 1
```

Trace:

| Step | Current vertex | Visited vertices | Current component size | Answer |
| --- | --- | --- | --- | --- |
| Start DFS at 0 | 0 | {0} | 0 | 0 |
| Visit neighbor 1 | 1 | {0,1} | 1 | 0 |
| Visit neighbor 3 | 3 | {0,1,3} | 2 | 0 |
| Visit neighbor 2 | 2 | {0,1,2,3} | 3 | 0 |
| Finish component |  | {0,1,2,3} | 4 | 1 |
| Check remaining vertices |  | {0,1,2,3} visited |  | 1 |

The four connected criminals form one component. The remaining six criminals are isolated, so they do not increase the count.

### Custom Example 2

Input:

```
5 2
0 1
3 4
```

Trace:

| Step | Current vertex | Visited vertices | Current component size | Answer |
| --- | --- | --- | --- | --- |
| Start DFS at 0 | 0 | {0} | 0 | 0 |
| Visit 1 | 1 | {0,1} | 1 | 0 |
| Finish component |  | {0,1} | 2 | 1 |
| Start DFS at 2 | 2 | {2} | 1 | 1 |
| Finish component |  | {2} | 1 | 1 |
| Start DFS at 3 | 3 | {3} | 0 | 1 |
| Visit 4 | 4 | {3,4} | 1 | 1 |
| Finish component |  | {3,4} | 2 | 2 |

This example shows that isolated criminals are ignored while multiple separate communities are counted independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | Every criminal is visited once and every stored edge is examined once. |
| Space | O(N + M) | The adjacency list stores the graph, and the traversal arrays store O(N) additional data. |

The largest graph has only 100 vertices, so the linear traversal easily fits within the time limit. The memory usage is also far below the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    graph = [[] for _ in range(n)]

    for _ in range(m):
        x, y = map(int, input().split())
        if x != y:
            graph[x].append(y)
            graph[y].append(x)

    visited = [False] * n
    ans = 0

    for i in range(n):
        if not visited[i]:
            stack = [i]
            visited[i] = True
            size = 0

            while stack:
                v = stack.pop()
                size += 1
                for u in graph[v]:
                    if not visited[u]:
                        visited[u] = True
                        stack.append(u)

            if size > 1:
                ans += 1

    return str(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        return solve()
    finally:
        sys.stdin = old_stdin

assert run("""10 4
1 2
1 3
0 2
0 1
""") == "1", "sample 1"

assert run("""5 2
0 1
3 4
""") == "2", "two communities"

assert run("""1 0
""") == "0", "minimum isolated graph"

assert run("""4 4
0 1
1 2
2 3
3 0
""") == "1", "cycle community"

assert run("""5 3
0 0
2 2
3 4
""") == "1", "self loops and one real community"

assert run("""100 99
""" + "\n".join(f"{i} {i+1}" for i in range(99)) + "\n") == "1", "maximum chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample graph | 1 | Original example with one non-trivial component |
| Two disconnected pairs | 2 | Multiple communities are counted separately |
| One isolated criminal | 0 | Single vertices are ignored |
| Four-cycle | 1 | A larger connected structure is counted once |
| Self-loops with one pair | 1 | Loops do not create fake communities |
| Chain of 100 criminals | 1 | Large connected component and traversal depth |

## Edge Cases

An input with only isolated criminals:

```
3 0
```

starts a DFS from each vertex, but every traversal visits exactly one vertex. The size check rejects all three components, leaving the answer as 0. The algorithm handles this because connectivity and community size are checked separately.

A connected pair:

```
2 1
0 1
```

causes the first DFS to visit both vertices. The component size becomes 2, so the answer increases to 1. The algorithm does not require a component to have many edges, only multiple vertices.

A self-loop:

```
3 1
1 1
```

does not create a valid community. The graph representation ignores the loop, and the DFS from vertex 1 still has size 1. The answer remains 0 because a single criminal cannot form a community.

A graph with several disconnected groups:

```
6 3
0 1
1 2
4 5
```

is processed as three components. The first has size 3 and contributes one star, the second is isolated and contributes nothing, and the third has size 2 and contributes one more star. The final answer is 2. This confirms that the traversal counts components independently rather than counting vertices or edges.
