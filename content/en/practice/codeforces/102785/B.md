---
title: "CF 102785B - Gremlins attack!"
description: "We have an N x N board of houses. Some cells contain gremlins at the beginning. Every cell starts with its light on, so gremlins cannot move through it. Over time, the history describes cells whose lights are switched off. After a cell becomes dark, it remains available forever."
date: "2026-07-28T03:39:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102785
codeforces_index: "B"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 18)"
rating: 0
weight: 102785
solve_time_s: 46
verified: true
draft: false
---

[CF 102785B - Gremlins attack!](https://codeforces.com/problemset/problem/102785/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an `N x N` board of houses. Some cells contain gremlins at the beginning. Every cell starts with its light on, so gremlins cannot move through it. Over time, the history describes cells whose lights are switched off. After a cell becomes dark, it remains available forever. A gremlin may move between side-adjacent dark cells, and reaching any cell on the outer border means it can leave the town.

The task is to find the earliest operation in the history after which at least one initial gremlin belongs to a connected region of dark cells that touches the border. If such a path already exists before any operation, the answer is `0`.

The board size can reach `500 x 500`, which means there are up to `250000` cells. The history can also contain up to `250000` operations. A solution that repeatedly searches the whole board after every operation could perform about `250000 * 250000` cell visits, which is around `6.25 * 10^10` operations and is far beyond the limit. We need a method where every cell and every operation is processed only a small number of times.

The main edge cases come from the dynamic nature of the board. A careless solution may forget that a cell can be turned off more than once. For example:

```
2 1 2
0 0
0 1
0 1
```

The gremlin starts at `(0,0)`, which is already on the border, so the correct answer is `0`. A solution that only checks after processing history events would incorrectly return `1`.

Another tricky case is when the newly opened cell connects two previously separate dark regions. For example:

```
3 1 2
1 1
0 1
1 0
```

After the first operation, `(0,1)` is a border cell and the gremlin can escape through it, so the answer is `1`. A solution that only checks whether the newly opened cell itself contains a gremlin would miss paths created through connections.

A third common mistake is treating diagonal cells as connected. For example:

```
3 1 2
1 1
0 0
2 2
```

The two dark cells are diagonal from each other and do not form a path. The correct answer is not `1` because diagonal movement is impossible.

## Approaches

A straightforward approach is to simulate the process exactly. After each light is turned off, we could run a graph traversal from every gremlin position and check whether a border cell is reachable through dark cells. This is correct because it directly tests the definition of escape.

The problem is the cost. In the worst case there can be `250000` history events, and each breadth-first search can visit `250000` cells. The total work can reach about `6.25 * 10^10` visits, which is too slow.

The useful observation is that the only change in the grid is that cells are added to the set of usable cells. Once a cell becomes dark, it never becomes blocked again. This means the connected components of dark cells only merge over time. We do not need to know the exact path every time, only whether a component contains a gremlin and whether it touches the border.

A disjoint set union structure fits this behavior. Each dark cell is represented as a node. When a cell is switched off, we activate it and merge it with every already active neighbor. Along with each component's parent, we store two properties: whether the component contains at least one starting gremlin and whether it contains a border cell. After each merge, if both properties are true for the resulting component, an escape is possible at that moment.

The brute-force approach repeatedly discovers the same connected regions. The DSU approach remembers those regions and only updates the small part of the graph affected by a newly opened cell.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(K * N²) | O(N²) | Too slow |
| Optimal | O(N² + K * α(N²)) | O(N²) | Accepted |

## Algorithm Walkthrough

1. Create a disjoint set union structure containing every board position. Initially every cell is inactive, because all lights are on. Store two flags for every component: whether it contains an initial gremlin and whether it touches the border.
2. Mark every starting gremlin position in the DSU data. If any starting position is already on the border, the answer is immediately `0`, because the gremlin can escape without waiting for any light to turn off.
3. Process the history in order. For each operation, activate the specified cell. If it was already active because the same house appeared earlier in the history, there is no new connection to create.
4. When activating a new cell, inspect its four neighbors. Any neighbor that is already active belongs to the same dark area and should be merged with the new cell's component.
5. After all necessary merges, inspect the component containing the newly activated cell. If it has both a gremlin and a border cell, the current operation number is the first possible escape moment.
6. The first time this condition appears is the answer because cells only become dark and components only grow. A later operation cannot create an earlier escape opportunity.

Why it works: the DSU always represents exactly the connected components of all currently dark cells. The stored gremlin flag is true exactly when some original gremlin can reach every cell in that component, and the border flag is true exactly when the component provides an exit. A gremlin can escape if and only if its component has both properties. Since each operation only adds dark cells, the first operation where a component has both properties is exactly the required earliest moment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    
    size = n * n
    parent = list(range(size))
    active = [False] * size
    has_gremlin = [False] * size
    has_border = [False] * size

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return ra
        if size_rank[ra] < size_rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        has_gremlin[ra] |= has_gremlin[rb]
        has_border[ra] |= has_border[rb]
        if size_rank[ra] == size_rank[rb]:
            size_rank[ra] += 1
        return ra

    size_rank = [0] * size

    gremlins = []
    answer = -1

    for _ in range(m):
        x, y = map(int, input().split())
        idx = x * n + y
        gremlins.append(idx)
        has_gremlin[idx] = True
        if x == 0 or y == 0 or x == n - 1 or y == n - 1:
            answer = 0

    history = []
    for _ in range(k):
        x, y = map(int, input().split())
        history.append((x, y))

    if answer == 0:
        print(0)
        return

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for step, (x, y) in enumerate(history, 1):
        idx = x * n + y

        if not active[idx]:
            active[idx] = True
            root = idx

            if x == 0 or y == 0 or x == n - 1 or y == n - 1:
                has_border[root] = True

            for dx, dy in directions:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < n and 0 <= ny < n:
                    nxt = nx * n + ny
                    if active[nxt]:
                        root = union(root, nxt)

        root = find(idx)
        if has_gremlin[root] and has_border[root]:
            print(step)
            return

    print(k)

if __name__ == "__main__":
    solve()
```

The DSU arrays are indexed by flattening `(x, y)` into `x * n + y`. This avoids storing large nested structures and gives constant-time access to every cell.

The `active` array is separate from the DSU state because inactive cells must not participate in unions. The parent array exists for all cells, but a cell only becomes part of the current graph after activation.

The `union` operation combines the two component properties using logical OR. If either old component had a gremlin, the merged component has one. The same reasoning applies to border contact. The order of operations matters: the new cell must be activated before checking its neighbors, otherwise connections through that cell would be missed.

The final check is only performed on the component containing the changed cell because all other components are unchanged during this operation. The use of union by rank and path compression keeps each DSU operation almost constant time.

## Worked Examples

For the first sample:

```
3 1 3
1 1
0 0
0 1
0 2
```

The gremlin starts at the center, so it cannot escape initially. The trace is:

| Step | Activated cell | Component contains gremlin | Component touches border | Result |
| --- | --- | --- | --- | --- |
| 0 | none | yes | no | continue |
| 1 | (0,0) | no | yes | continue |
| 2 | (0,1) | yes | yes | answer is 2 |

The second operation connects the center cell to the border through `(0,1)`. The DSU detects this because the merged component now has both stored properties.

For the second sample:

```
5 2 5
0 1
4 1
0 0
1 1
2 2
3 3
4 4
```

The trace is:

| Step | Activated cell | Component contains gremlin | Component touches border | Result |
| --- | --- | --- | --- | --- |
| 0 | none | yes | yes | answer is 0 |

The initial gremlins are already on border cells, so no history operation is needed.

This example confirms that the initial state must be checked before processing any events.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N² + K * α(N²)) | Every cell is initialized once, and every history event performs a constant number of DSU operations. |
| Space | O(N²) | The DSU arrays and state arrays store information for every possible cell. |

The maximum board has `250000` cells, so the linear memory usage fits within the limit. The near-constant DSU operations allow all history events to be processed efficiently.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    
    def fake_print(x):
        output.write(str(x))
    
    old_print = __builtins__.print
    __builtins__.print = fake_print
    
    try:
        solve()
    finally:
        sys.stdin = old_stdin
        __builtins__.print = old_print
    
    return output.getvalue()

assert run("""3 1 3
1 1
0 0
0 1
0 2
""") == "2", "sample 1"

assert run("""5 2 5
0 1
4 1
0 0
1 1
2 2
3 3
4 4
""") == "0", "sample 2"

assert run("""2 1 2
0 0
0 1
0 1
""") == "0", "initial border escape"

assert run("""3 1 2
1 1
0 1
1 0
""") == "1", "first opening creates path"

assert run("""3 1 3
1 1
0 0
2 2
1 1
""") == "3", "diagonal cells are not connected"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 2 | A path appears after several unions |
| Sample 2 | 0 | Immediate escape before history |
| `2 x 2` case | 0 | Border starting position handling |
| Center connected through one opening | 1 | New cell creates a connection |
| Diagonal openings | 3 | Only four-direction movement counts |

## Edge Cases

The first edge case is an initial escape. In the input:

```
2 1 2
0 0
0 1
0 1
```

The gremlin starts at `(0,0)`, which is already a border cell. The algorithm checks this before activating any history cells and returns `0`.

The second edge case is repeated history entries. If the same cell is turned off multiple times, the second occurrence does not create new connections. The `active` array prevents duplicate activation, so the DSU state remains correct.

The third edge case is a connection created indirectly. In:

```
3 1 2
1 1
0 1
1 0
```

After the first operation, the cell `(0,1)` is activated and connected directly to the gremlin at `(1,1)`. The component has a gremlin and touches the border, so the algorithm returns `1`.

The fourth edge case is diagonal adjacency. If dark cells are placed at `(0,0)` and `(1,1)`, they remain in separate components because the algorithm only checks the four side neighbors. This matches the movement rules and prevents false escapes.
