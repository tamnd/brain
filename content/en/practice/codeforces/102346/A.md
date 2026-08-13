---
title: "CF 102346A - Artwork"
description: "The room is the rectangle with corners (0, 0) and (M, N). The thief needs a continuous path from the lower-left corner to the upper-right corner while staying strictly outside every sensor's detection disk."
date: "2026-08-14T05:19:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102346
codeforces_index: "A"
codeforces_contest_name: "2019-2020 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102346
solve_time_s: 78
verified: true
draft: false
---

[CF 102346A - Artwork](https://codeforces.com/problemset/problem/102346/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The room is the rectangle with corners `(0, 0)` and `(M, N)`. The thief needs a continuous path from the lower-left corner to the upper-right corner while staying strictly outside every sensor's detection disk.

Each sensor `(x, y, s)` can be viewed geometrically as a closed circle of radius `s` centered at `(x, y)`. The question is not about finding an actual path. The useful question is whether the collection of forbidden disks can form a continuous wall that separates the two required corners.

With `K <= 1000`, checking every pair of sensors is feasible because there are only `K(K-1)/2`, at most about `500,000`, pairs. A quadratic algorithm is consequently practical. A cubic approach would already be around `10^9` operations at the upper bound and is far too slow for a one-second contest limit. The room dimensions can reach `10^4` and sensor radii can also reach `10^4`, so coordinate values themselves do not make a grid simulation attractive. In fact, a grid over the room could contain around `10^8` positions, which is both unnecessary and much larger than the number of sensors.

There are two boundary details that are easy to mishandle. First, touching counts as blocking because the thief must remain at a distance strictly greater than the sensor sensitivity. For example, two sensors that are exactly tangent must be treated as connected:

```
10 10 2
3 5 2
7 5 2
```

The two disks touch at `(5, 5)` and form a wall from the left side to the right side. The correct answer is `N`. Using a strict `<` comparison would incorrectly report `S`.

Second, a sensor can reach a room boundary even though its center is strictly inside the room. For example:

```
10 10 1
5 5 5
```

The disk touches all four sides, so it completely separates the lower-left and upper-right corners. The correct answer is `N`. A careless implementation that only checks whether sensor centers lie on boundaries would miss the obstruction.

The four relevant boundary pairs are also easy to mix up. A connected obstacle touching the top and left sides blocks the lower-left corner from the rest of the room. A component touching the bottom and right sides blocks the upper-right corner. A component touching top and bottom separates the two vertical sides, while a component touching left and right separates the two horizontal sides. Thus the blocking condition is exactly that one connected sensor component touches at least one side from `{top, left}` and at least one side from `{bottom, right}`.

## Approaches

A direct geometric approach would try to construct the free-space region and search for a path through it. One possibility is to discretize the room into a fine grid and run BFS, marking every grid point covered by a sensor. This is conceptually straightforward, and it would work on a tiny room, but the room may be `10^4` by `10^4`. Even one cell per meter would give `10^8` cells, while the input contains only `1000` sensors. The discretization also introduces awkward precision questions because the actual obstacles are circles rather than unit squares.

The useful observation is that a path becomes impossible only when the forbidden circles form a continuous barrier. Two sensors belong to the same barrier precisely when their disks intersect or touch. For sensors `i` and `j`, this happens when

`(xi - xj)^2 + (yi - yj)^2 <= (si + sj)^2`.

We can consequently forget the exact shape of the overlapping region after establishing connectivity. Make every sensor a graph vertex, and connect two vertices whenever their disks intersect or touch. Every connected component of this graph represents one connected forbidden region.

The brute-force graph construction checks every pair of sensors, which is only `O(K^2)`. After the graph is built, DFS visits every vertex and edge once. For each component, we record which room boundaries its circles touch. If the component connects one boundary from `{top, left}` to one from `{bottom, right}`, it forms a separator between `(0, 0)` and `(M, N)`, so the answer is `N`. If no component does this, the free space contains a route between the two corners, so the answer is `S`.

The same idea can be implemented with a disjoint-set union structure instead of DFS. For this problem, DFS is simple enough and makes the connected-component interpretation explicit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Grid simulation | Potentially `O(MN)` or worse | `O(MN)` | Too large |
| Brute-force path geometry | Potentially much worse than quadratic | Large | Too slow |
| Sensor intersection graph + DFS | `O(K^2)` | `O(K^2)` with an explicit graph | Accepted |
| Sensor intersection graph + DSU | `O(K^2 α(K))` | `O(K)` | Accepted |

## Algorithm Walkthrough

1. Store every sensor as `(x, y, s)`. Treat its detection area as a closed disk, because distance exactly equal to `s` is also detected.
2. For every pair of sensors, compute the squared distance between their centers and compare it with the squared sum of their radii. If

`dx² + dy² <= (si + sj)²`,

connect the two sensors in the graph. Squared distances avoid floating-point arithmetic completely, and the largest intermediate values are easily handled by Python integers.
3. Run DFS from every unvisited sensor. During the DFS, collect the room boundaries touched by every sensor in that connected component. A sensor touches the left boundary when `x - s <= 0`, the right boundary when `x + s >= M`, the bottom boundary when `y - s <= 0`, and the top boundary when `y + s >= N`.
4. After finishing one connected component, test whether it touches at least one boundary in `{top, left}` and at least one boundary in `{bottom, right}`. If so, the component is a continuous wall separating the entrance corner from the painting corner, so immediately output `N`.
5. If every connected component fails that test, output `S`. No forbidden component separates the two corners, so a continuous path through the remaining part of the room exists.

Why it works: the invariant is that every DFS component represents exactly one connected union of sensor disks. Whenever two disks touch, the thief cannot pass through their contact point because equality is forbidden, so merging touching disks preserves the topology relevant to path existence. A connected forbidden set joining top to bottom or left to right separates the two opposite sides of the rectangle, and joining top to left or bottom to right cuts off one of the two target corners. Conversely, if no component connects one side of `{top, left}` with one side of `{bottom, right}`, there is no connected obstacle wall capable of separating the two diagonal corners. The algorithm checks exactly these possible separators.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    M, N, K = map(int, input().split())
    sensors = [tuple(map(int, input().split())) for _ in range(K)]

    graph = [[] for _ in range(K)]

    for i in range(K):
        x1, y1, r1 = sensors[i]
        for j in range(i + 1, K):
            x2, y2, r2 = sensors[j]

            dx = x1 - x2
            dy = y1 - y2
            sr = r1 + r2

            if dx * dx + dy * dy <= sr * sr:
                graph[i].append(j)
                graph[j].append(i)

    visited = [False] * K

    for start in range(K):
        if visited[start]:
            continue

        stack = [start]
        visited[start] = True

        top = False
        right = False
        bottom = False
        left = False

        while stack:
            u = stack.pop()
            x, y, r = sensors[u]

            if y + r >= N:
                top = True
            if x + r >= M:
                right = True
            if y - r <= 0:
                bottom = True
            if x - r <= 0:
                left = True

            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)

        if (top or left) and (bottom or right):
            print("N")
            return

    print("S")

if __name__ == "__main__":
    solve()
```

The first nested loop constructs the intersection graph. There is no square root because comparing squared distances gives exactly the same result and avoids floating-point boundary errors. The `<=` comparison is deliberate: two detection disks that are tangent leave no legal path through their touching point.

The DFS uses an explicit stack rather than recursive DFS. With `K = 1000`, Python recursion would probably be sufficient after increasing the recursion limit, but an iterative traversal avoids depending on recursion depth and makes the implementation more robust.

Each sensor contributes four independent boundary tests. The inequalities are also inclusive because a disk that merely touches a room boundary participates in a blocking wall. For example, `x - r == 0` means the sensor reaches the left boundary and must be counted.

The component is rejected when `(top or left) and (bottom or right)` is true. This compact expression represents the four separating pairs: top-bottom, top-right, left-bottom, and left-right after considering the corner orientation used by the coordinate system. With `top` paired with `left` as one group and `bottom` paired with `right` as the other, it is equivalent to checking the four possible barriers that separate the two diagonal corners.

The input has only one test case, so `solve()` is called once. Python's arbitrary-precision integers also remove any overflow concern from the squared coordinate and radius calculations.

## Worked Examples

### Sample 1

The input is:

```
10 22 2
4 6 5
6 16 5
```

The two sensors have center distance squared

`(4 - 6)^2 + (6 - 16)^2 = 104`.

Their combined radius is `10`, so the combined-radius square is `100`. Since `104 > 100`, the disks do not touch and form two separate components.

| Component | Sensors | Top | Right | Bottom | Left | Blocking? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `(4,6,5)` | No | No | No | Yes | No |
| 2 | `(6,16,5)` | No | No | No | No | No |

No component connects two separating boundaries, so the thief can get from the entrance to the painting.

The output is `S`.

### Sample 2

The input is:

```
10 10 2
3 7 4
5 4 4
```

The squared distance between the sensor centers is

`(3 - 5)^2 + (7 - 4)^2 = 13`.

The squared sum of their radii is `8² = 64`, so the two detection disks overlap and become one connected component.

| Component | Sensors | Top | Right | Bottom | Left | Blocking? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | both sensors | Yes | Yes | Yes | Yes | Yes |

The component reaches all four boundaries. In particular, it connects a boundary from the first group to a boundary from the second group, creating a complete barrier between the two target corners.

The output is `N`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(K^2)` | Every pair of sensors is tested once, and DFS processes every graph edge once. |
| Space | `O(K^2)` | In the worst case every pair of sensors intersects, so the graph contains `O(K^2)` edges. |

With `K <= 1000`, there are at most `499,500` sensor pairs. That is small enough for a quadratic solution, while the room dimensions never need to be expanded into a grid. The graph and its traversal are comfortably within the intended constraints.

## Test Cases

The following test harness uses the same `solve()` logic through a function that accepts a string. The custom cases include the minimum room size, a single sensor, tangent sensors, a sensor reaching the entrance corner, and a dense set of sensors.

```python
import sys
import io

def solve(inp: str) -> str:
    data = io.StringIO(inp)
    input_fn = data.readline

    M, N, K = map(int, input_fn().split())
    sensors = [tuple(map(int, input_fn().split())) for _ in range(K)]

    graph = [[] for _ in range(K)]

    for i in range(K):
        x1, y1, r1 = sensors[i]
        for j in range(i + 1, K):
            x2, y2, r2 = sensors[j]

            dx = x1 - x2
            dy = y1 - y2
            sr = r1 + r2

            if dx * dx + dy * dy <= sr * sr:
                graph[i].append(j)
                graph[j].append(i)

    visited = [False] * K

    for start in range(K):
        if visited[start]:
            continue

        stack = [start]
        visited[start] = True

        top = right = bottom = left = False

        while stack:
            u = stack.pop()
            x, y, r = sensors[u]

            top |= y + r >= N
            right |= x + r >= M
            bottom |= y - r <= 0
            left |= x - r <= 0

            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)

        if (top or left) and (bottom or right):
            return "N\n"

    return "S\n"

assert solve("""10 22 2
4 6 5
6 16 5
""") == "S\n", "sample 1"

assert solve("""10 10 2
3 7 4
5 4 4
""") == "N\n", "sample 2"

assert solve("""100 100 3
40 50 30
5 90 50
90 10 5
""") == "S\n", "sample 3"

assert solve("""10 10 1
5 5 1
""") == "S\n", "minimum room, isolated sensor"

assert solve("""10 10 2
3 5 2
7 5 2
""") == "N\n", "tangent sensors form a left-right wall"

assert solve("""10 10 1
3 3 5
""") == "N\n", "sensor reaches the entrance corner"

assert solve("""10 10 1
5 5 5
""") == "N\n", "one disk reaches all four boundaries"

assert solve("""10 10 4
2 2 3
8 2 3
2 8 3
8 8 3
""") == "N\n", "four equal sensors create connected barriers"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `10 10 1 / 5 5 1` | `S` | Minimum room dimensions and an isolated obstacle |
| `10 10 2 / 3 5 2 / 7 5 2` | `N` | Exact tangency must count as an intersection |
| `10 10 1 / 3 3 5` | `N` | A large sensor can block the entrance corner |
| `10 10 1 / 5 5 5` | `N` | One component can touch every boundary |
| Four equal sensors at `(2,2)`, `(8,2)`, `(2,8)`, `(8,8)` | `N` | Equal radii, multiple connections, and component merging |

## Edge Cases

A tangent pair is the most common numerical boundary mistake. Consider:

```
10 10 2
3 5 2
7 5 2
```

The centers are four meters apart and the radii sum to four, so the comparison is `16 <= 16`. The disks are connected exactly at one point. That contact is enough to block a path through the point because the thief must stay strictly farther than the sensor sensitivity. The graph puts both sensors in one component, and the component touches the left and right boundaries. The algorithm outputs `N`.

A large sensor can reach a corner even though every sensor center is strictly inside the room. For:

```
10 10 1
3 3 5
```

the distance from the sensor center to `(0,0)` is `sqrt(18)`, which is less than `5`. The entrance itself lies inside the detection disk, so there is no legal starting point at the entrance. The boundary checks also show that the disk reaches both the left and bottom sides. The algorithm's separator logic handles connected boundary barriers, while the geometric interpretation makes clear why this is a blocked entrance case.

A sensor touching a boundary exactly must be counted. For example:

```
10 10 1
5 5 5
```

gives `x-r = 0`, `x+r = 10`, `y-r = 0`, and `y+r = 10`. The component touches every side, so the condition `(top or left) and (bottom or right)` is true and the answer is `N`. Replacing any of the boundary comparisons with a strict inequality would incorrectly miss this case.

Finally, several sensors may not individually form a wall but can form one after transitive merging. Suppose sensor A touches B, B touches C, and C touches a room boundary. A is connected to that boundary even if A itself is far from it. DFS captures this because all three sensors belong to the same connected component. The component records every boundary reached by any of its members, which is exactly the information needed to decide whether the entire chain blocks the room.
