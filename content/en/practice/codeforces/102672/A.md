---
title: "CF 102672A - Wooden Castle"
description: "The lock is a tree whose vertices are painted in two colors. A move can either repaint one vertex or remove an entire connected region whose vertices all currently have the same color. The task is to find the minimum number of moves needed until no vertices remain."
date: "2026-08-01T23:42:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102672
codeforces_index: "A"
codeforces_contest_name: "Selection of tasks from Internet olympiads season 2019-20"
rating: 0
weight: 102672
solve_time_s: 75
verified: true
draft: false
---

[CF 102672A - Wooden Castle](https://codeforces.com/problemset/problem/102672/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
# Problem Understanding

The lock is a tree whose vertices are painted in two colors. A move can either repaint one vertex or remove an entire connected region whose vertices all currently have the same color. The task is to find the minimum number of moves needed until no vertices remain. The input gives the number of vertices, the initial binary coloring, and the tree edges. The output is the smallest possible number of operations.

The key detail is that the tree structure is not asking us to simulate deletions. The number of vertices can reach 200,000, so any approach that tries many possible deletion orders or maintains the tree after every operation will not fit. A solution must be close to linear time, because even a quadratic algorithm would already require around 40 billion operations at the largest size.

There are two natural strategies. We can delete every initial monochromatic component separately, or we can spend operations repainting vertices so that many components merge and disappear together. The challenge is recognizing that no complicated combination of partial repainting and partial deletion can beat the best of these two ideas.

Consider a tree with four vertices shaped like a star:

```
4
1000
1 2
1 3
1 4
```

There are four monochromatic components initially, so deleting components one by one takes four moves. However, repainting the center makes the whole tree white and one final deletion removes everything, giving an answer of two. A solution that only counts components fails here.

Another important case is when all vertices already have the same color. For example:

```
3
000
1 2
2 3
```

The answer is one, because the entire tree is already a single removable component. A formula that always adds one repaint before deleting would incorrectly return two.

The opposite extreme is also important. For a single vertex:

```
1
1
```

The answer is one. There is no need to repaint, but the vertex still has to be removed by a deletion operation.

# Approaches

A direct brute force approach would try to decide which components to delete first and which vertices to repaint. For every possible state of the tree, it could try every available operation and use recursion with memoization. This is correct because it explores every possible sequence, but the number of states grows exponentially with the number of vertices. Even small trees create too many possible colorings and remaining vertex sets, so this approach is unusable.

A simpler brute force idea is to repeatedly count current monochromatic components and try every possible repaint. This still fails because after each repaint the number of possible choices remains large. With 200,000 vertices, even checking every possible single vertex repaint is already too expensive.

The important observation is that a repaint only helps by reducing the number of different colored groups. There are only two colors, so if we decide to make the entire tree one color, the cheapest choice is repainting every vertex of the less frequent color and then deleting the tree once. This costs:

```
min(number of white vertices, number of black vertices) + 1
```

The other option is to do no repainting at all. Then every initial monochromatic connected component must eventually be deleted, so the cost equals the number of such components.

The surprising part is that mixing the two strategies cannot improve the answer. If we repaint fewer vertices than the minority color count, some vertices of both colors remain. The remaining differently colored regions still require separate deletions, and the total cannot beat simply deleting all initial components. If we repaint enough vertices to remove one color completely, we are already paying at least the cost of making the whole tree monochromatic.

The solution is thus reduced to counting two values in one traversal: the number of monochromatic components and the number of vertices of each color.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(n) | Accepted |

# Algorithm Walkthrough

1. Count how many vertices have each color. This gives the cost of the strategy where we erase one color from the tree, repaint the other color, and perform one final deletion.
2. Traverse the tree once and count monochromatic connected components. Start a traversal from every unvisited vertex. All reachable vertices with the same color belong to the same component.
3. Compute the two possible answers. The first is the number of monochromatic components. The second is the number of vertices of the less common color plus one final deletion operation.
4. Output the smaller of these two values because every optimal sequence is covered by one of these two cases.

Why it works:

Every deletion operation removes one monochromatic connected component of the current tree. If we never eliminate a color completely, the remaining color boundary forces us to pay at least the same cost as handling the original components. The only way to avoid those component boundaries is to repaint enough vertices so that the whole tree becomes one color. The cheapest such transformation repaints all vertices of the smaller color class. After that, one deletion removes everything. Since every optimal solution must either keep both colors or remove one color entirely, the minimum of these two costs is always achievable and cannot be improved.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    count0 = s.count('0')
    count1 = n - count0

    components = 0
    visited = [False] * n

    for i in range(n):
        if not visited[i]:
            components += 1
            color = s[i]
            stack = [i]
            visited[i] = True

            while stack:
                v = stack.pop()
                for u in graph[v]:
                    if not visited[u] and s[u] == color:
                        visited[u] = True
                        stack.append(u)

    repaint_strategy = min(count0, count1) + 1
    print(min(components, repaint_strategy))

if __name__ == "__main__":
    solve()
```

The first part of the code builds the tree using adjacency lists. A tree has exactly `n - 1` edges, so storing each edge twice gives linear memory usage.

The color counts are enough to evaluate the full repaint strategy. We never need to know which particular vertices are repainted because only the total number of vertices of each color matters.

The DFS counts monochromatic components. When a new unvisited vertex is found, it starts exactly one component traversal. The DFS only follows edges to vertices with the same color, so vertices of the opposite color naturally split the tree into different components.

There are no off by one issues in the component count because every vertex is visited exactly once, and each traversal start corresponds to one component. Python integers also handle the maximum counts without any overflow concerns.

# Worked Examples

## Example 1

Input:

```
4
1000
1 2
1 3
1 4
```

The center is black and the leaves are white.

| Step | Current vertex | Component color | Components counted |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 0 | 2 |
| 3 | 3 | 0 | 3 |
| 4 | 4 | 0 | 4 |

The component strategy costs 4. There is one black vertex and three white vertices, so repainting the smaller color costs `1 + 1 = 2`. The answer is 2.

## Example 2

Input:

```
5
01010
1 2
2 3
3 4
4 5
```

The path alternates colors.

| Step | Current vertex | Component color | Components counted |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 1 |
| 2 | 2 | 1 | 2 |
| 3 | 3 | 0 | 3 |
| 4 | 4 | 1 | 4 |
| 5 | 5 | 0 | 5 |

There are five components. The smaller color appears twice, so the repaint strategy costs `2 + 1 = 3`. The algorithm chooses 3, meaning repaint the two black vertices and delete the resulting white tree.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every vertex and edge is processed once during the traversal. |
| Space | O(n) | The adjacency list, visited array, and DFS stack store linear information. |

The input size can reach 200,000 vertices, and the algorithm performs only a constant amount of work per vertex and edge. It fits comfortably within the required limits.

# Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    data = sys.stdin.readline
    n = int(data())
    s = data().strip()

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, data().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    count0 = s.count("0")
    count1 = n - count0

    visited = [False] * n
    components = 0

    for i in range(n):
        if not visited[i]:
            components += 1
            color = s[i]
            stack = [i]
            visited[i] = True
            while stack:
                v = stack.pop()
                for u in graph[v]:
                    if not visited[u] and s[u] == color:
                        visited[u] = True
                        stack.append(u)

    ans = min(components, min(count0, count1) + 1)

    sys.stdin = old_stdin
    return str(ans) + "\n"

assert run("""4
1000
1 2
1 3
1 4
""") == "2\n", "sample 1"

assert run("""1
0
""") == "1\n", "single vertex"

assert run("""3
000
1 2
2 3
""") == "1\n", "already one component"

assert run("""5
01010
1 2
2 3
3 4
4 5
""") == "3\n", "alternating path"

assert run("""6
111111
1 2
2 3
3 4
4 5
5 6
""") == "1\n", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 / 1000` star tree | 2 | Repainting one color can beat deleting components. |
| Single vertex | 1 | Minimum size boundary condition. |
| All zero tree | 1 | Already monochromatic tree. |
| Alternating path | 3 | Many components where repainting is better. |
| All one color | 1 | Equal value handling. |

# Edge Cases

For the star shaped tree:

```
4
1000
1 2
1 3
1 4
```

The algorithm counts four monochromatic components. It also counts one black vertex and three white vertices, producing a repaint strategy of two operations. The minimum is two, matching the sequence of repainting the center and deleting the whole tree.

For a fully monochromatic tree:

```
3
000
1 2
2 3
```

The traversal finds one component. The repaint strategy would cost four because there are no black vertices to repaint and the formula becomes `0 + 1 = 1`. The answer remains one because the tree can immediately be deleted.

For the smallest possible input:

```
1
1
```

The traversal creates exactly one component. The repaint strategy also gives one, so the final answer is one. The algorithm does not accidentally return zero because deletion is always required to remove the final vertex.
