---
title: "CF 102694A - Circumference of a Tree"
description: "The tree is treated like a geometric object where the diameter is the longest path between any two nodes. The problem defines an unusual version of circumference: instead of the real value of pi, we use pi = 3."
date: "2026-08-01T23:22:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102694
codeforces_index: "A"
codeforces_contest_name: "AlgorithmsThread Tree Basics Contest"
rating: 0
weight: 102694
solve_time_s: 59
verified: true
draft: false
---

[CF 102694A - Circumference of a Tree](https://codeforces.com/problemset/problem/102694/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The tree is treated like a geometric object where the diameter is the longest path between any two nodes. The problem defines an unusual version of circumference: instead of the real value of pi, we use pi = 3. Since circumference is normally diameter multiplied by pi, the required answer is three times the diameter of the tree. The input describes an undirected tree with `n` vertices and `n - 1` edges, and the output is the circumference value under this modified definition.

The main task is not to simulate any geometry. It is to find the longest distance between two vertices in a tree. The constraint allows up to `3 * 10^5` vertices, so an algorithm that explores the tree a constant number of times is required. An approach that tries every pair of vertices would need about `n^2 / 2` pairs, which becomes around `4.5 * 10^10` checks for the largest input and is far beyond what a one second limit can support.

The edge cases come from the structure of trees. A single vertex has no edges, so its diameter is zero and the answer must also be zero. For example:

```
Input:
1

Output:
0
```

A careless implementation that assumes there is always at least one edge may fail while building the adjacency list or while running a search from a nonexistent neighbor.

A tree with two vertices has diameter one, not two. For example:

```
Input:
2
1 2

Output:
3
```

The longest path contains one edge, so the circumference is `1 * 3`. A common mistake is counting vertices instead of edges and producing `6`.

A star-shaped tree is another useful case. For example:

```
Input:
5
1 2
1 3
1 4
1 5

Output:
6
```

The longest path goes from one leaf through the center to another leaf, containing two edges. An implementation that only checks the deepest child from one arbitrary root can incorrectly return one instead of two.

## Approaches

A direct solution would calculate the distance between every pair of vertices and keep the maximum. For each starting vertex, we could run a DFS or BFS to find distances to every other vertex. This is correct because the diameter is exactly the maximum distance among all pairs. However, doing this from every vertex costs `O(n^2)` time. With `n = 300000`, this would require tens of billions of operations.

The useful property of trees is that the diameter can be found using only two traversals. Pick any starting vertex and find the farthest vertex from it. That vertex is guaranteed to be one endpoint of a diameter. Then start another traversal from that endpoint. The farthest distance found in the second traversal is the diameter length.

The reason this works comes from the shape of paths in trees. Every pair of vertices has exactly one path between them. If we start from an arbitrary point, moving as far as possible takes us toward an extreme end of the tree. The second search from that extreme end reaches the opposite extreme, giving the longest possible path.

After finding the diameter in number of edges, the final answer is simply `diameter * 3` because the problem defines pi as 3.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the tree. Each edge connects two vertices, so both directions must be stored because the tree is undirected.
2. Run a DFS or BFS from any vertex, such as vertex `1`, and record distances from that vertex. Find the vertex with the largest distance.

The first traversal does not need to start from a special vertex. The farthest vertex it finds is enough to begin the real diameter search.

1. Run a second DFS or BFS from the vertex found in the previous step. Again record distances and take the maximum distance reached.

This maximum distance is the diameter of the tree measured in edges.

1. Multiply the diameter by `3` and print the result.

The reason the algorithm is correct is that a tree has a unique path between every pair of vertices. The first traversal reaches a leaf on one side of a longest path. Starting from that endpoint, the second traversal must reach the opposite endpoint of the longest path, so the maximum distance found is exactly the diameter. Since every valid diameter path has been considered through this endpoint, no larger distance can exist.

## Python Solution

```python
import sys
input = sys.stdin.readline

def farthest(start, graph):
    stack = [(start, -1, 0)]
    best_node = start
    best_dist = 0

    while stack:
        node, parent, dist = stack.pop()

        if dist > best_dist:
            best_dist = dist
            best_node = node

        for nxt in graph[node]:
            if nxt != parent:
                stack.append((nxt, node, dist + 1))

    return best_node, best_dist

def solve():
    n = int(input())

    graph = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)

    if n == 1:
        print(0)
        return

    endpoint, _ = farthest(1, graph)
    _, diameter = farthest(endpoint, graph)

    print(diameter * 3)

if __name__ == "__main__":
    solve()
```

The adjacency list stores the tree in `O(n)` memory, which is necessary because every edge must be visited. The helper function `farthest` performs an iterative DFS. Using an explicit stack avoids Python recursion depth problems on a tree that can be a chain of length `300000`.

The first call to `farthest` only identifies a good starting endpoint for the diameter search. Its returned distance is ignored because it is not necessarily the final diameter. The second call starts from that endpoint and its returned distance is the actual diameter.

The multiplication is performed after the diameter is found. The diameter counts edges, so a path with `k` edges has circumference `3k`. There is no integer overflow concern in Python because integers grow automatically.

## Worked Examples

### Example 1

Input:

```
1
```

The tree contains only one vertex.

| Step | Start node | Farthest node | Diameter | Answer |
| --- | --- | --- | --- | --- |
| Initial tree | 1 | 1 | 0 | 0 |

The example confirms the isolated vertex case. There is no path between different vertices, so the diameter is zero.

### Example 2

Input:

```
5
4 2
1 4
5 4
3 4
```

The tree is a star centered at vertex `4`.

| Step | Start node | Farthest node | Maximum distance |
| --- | --- | --- | --- |
| First traversal | 1 | 2 | 2 |
| Second traversal | 2 | 1 | 2 |

The second traversal finds a diameter of two edges. Multiplying by three gives the required circumference of six.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The tree is traversed twice, and every edge is processed a constant number of times. |
| Space | O(n) | The adjacency list and DFS stack contain at most a linear number of elements. |

The maximum input size is `300000` vertices, so a linear algorithm is required. Two tree traversals are small enough to fit comfortably within the limits.

## Test Cases

```python
import sys
import io

def solve(data):
    sys.stdin = io.StringIO(data)
    input = sys.stdin.readline

    n = int(input())
    graph = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)

    def farthest(start):
        stack = [(start, -1, 0)]
        node = start
        dist = 0

        while stack:
            cur, parent, d = stack.pop()
            if d > dist:
                node = cur
                dist = d
            for nxt in graph[cur]:
                if nxt != parent:
                    stack.append((nxt, cur, d + 1))
        return node, dist

    if n == 1:
        return "0"

    a, _ = farthest(1)
    _, d = farthest(a)
    return str(d * 3)

assert solve("1\n") == "0", "single vertex"

assert solve("""3
3 2
2 1
""") == "6", "sample 2"

assert solve("""5
4 2
1 4
5 4
3 4
""") == "6", "sample 3"

assert solve("""2
1 2
""") == "3", "two vertices"

assert solve("""5
1 2
1 3
1 4
1 5
""") == "6", "star tree"

assert solve("""6
1 2
2 3
3 4
4 5
5 6
""") == "15", "long chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | 0 | Handles the smallest possible tree |
| Two vertices | 3 | Confirms diameter counts edges, not vertices |
| Star tree | 6 | Checks branching structures |
| Long chain | 15 | Checks a maximum-depth style tree |
| Sample cases | 6 | Confirms standard examples |

## Edge Cases

For the one-vertex tree:

```
Input:
1
```

The algorithm skips the traversals and directly returns zero. Without this condition, code that assumes a second endpoint exists may access invalid data.

For a two-vertex tree:

```
Input:
2
1 2
```

The first traversal finds the other vertex at distance one. The second traversal also finds a maximum distance of one, so the answer is `1 * 3 = 3`. This confirms that distances are measured by edges.

For a star tree:

```
Input:
5
1 2
1 3
1 4
1 5
```

Starting from vertex `1`, the farthest nodes are leaves at distance one. Starting from one of those leaves, the second traversal reaches another leaf at distance two. The algorithm correctly finds the path through the center instead of only considering direct children.
