---
title: "CF 102760K - Sewing Graph"
description: "The cloth contains $N$ points in the plane. A sewing sequence is a list of point indices. Consecutive points in this list define segments, and the side of the cloth on which a segment is drawn depends on whether its position in the sequence is odd or even."
date: "2026-07-28T23:59:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102760
codeforces_index: "K"
codeforces_contest_name: "2020 KAIST 10th ICPC Mock Contest (XXI Open Cup. Grand Prix of Korea. Division 2)"
rating: 0
weight: 102760
solve_time_s: 87
verified: true
draft: false
---

[CF 102760K - Sewing Graph](https://codeforces.com/problemset/problem/102760/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

The cloth contains $N$ points in the plane. A sewing sequence is a list of point indices. Consecutive points in this list define segments, and the side of the cloth on which a segment is drawn depends on whether its position in the sequence is odd or even. The odd-positioned segments form the pattern on the front side, and the even-positioned segments form the pattern on the back side.

A valid pattern requires that the segments on each side connect all points and do not cross except at shared endpoints. The goal is not to minimize the total length of thread or the geometric distance traveled. The only thing being minimized is the number of points written in the sewing sequence.

Each side needs to contain a connected graph over $N$ vertices. Any connected graph on $N$ vertices has at least $N-1$ edges, so the front side requires at least $N-1$ sewing segments and the back side requires at least $N-1$ sewing segments. Since a sequence of length $k$ creates exactly $k-1$ segments, we immediately get the lower bound

$$k-1 \geq 2(N-1)$$

which means

$$k \geq 2N-1.$$

The constraints allow $N$ up to $1000$, but this lower bound tells us something stronger: we do not need a complicated geometric algorithm. We only need to find any valid construction using exactly $2N-1$ points in the sequence.

A few cases can break naive thinking. For $N=2$, the sequence cannot simply contain the two vertices once because one side would receive no edge. For the input

```
2
1 1
2 2
```

the correct output length is $3$, for example:

```
3
1 2 1
```

The front side gets edge $1-2$, and the back side gets the same geometric edge on the other side of the cloth.

Another common mistake is trying to use a non-planar structure. A sequence such as

```
1 2 3 4 1
```

does not automatically produce a valid pattern because arbitrary segments between points may intersect. The construction needs a graph where crossings are impossible by design.

The final edge case is a large number of points that are not in convex position. For example:

```
4
1 1
10 10
5 5
8 2
```

Connecting arbitrary pairs may create intersections, but connecting every point directly to one fixed point always works because all segments meet only at that center point.

## Approaches

A direct approach would be to search for two non-crossing spanning trees and then find an alternating walk that uses all their edges. This is difficult because the trees have geometric restrictions, and the interaction between the two sides of the cloth makes the construction unnecessarily complicated.

The lower bound gives a clue. If we achieve a sequence of length exactly $2N-1$, then every side receives exactly $N-1$ edges. Both sides must then be trees. We only need to find one planar tree whose edges can be used twice, once on each side.

A star graph solves this immediately. Choose point $1$ as the center and connect it to every other point. This graph is always planar because all edges share the same endpoint. Now perform a depth-first traversal of this star tree. The traversal starts at the center, visits a leaf, returns to the center, visits the next leaf, and so on.

The resulting sequence is:

$$1,2,1,3,1,4,1,\ldots,N,1$$

Every edge of the star appears once between odd positions and once between even positions. The front side receives the outward trips, and the back side receives the return trips. Both sides contain the same spanning tree, which is allowed because the two sides of the cloth are independent.

The brute force idea fails because it tries to discover a valid planar structure. The observation that a star is always planar removes all geometric difficulty and reduces the problem to outputting a fixed pattern.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $N$ if searching over sequences | Large | Too slow |
| Optimal | O($N$) | O($N$) | Accepted |

## Algorithm Walkthrough

1. Choose point $1$ as the center of a star-shaped spanning tree. Every other point will be connected directly to this point. This guarantees that no two edges on the same side can intersect except at the center.
2. Start the sewing sequence with point $1$. This represents standing at the center before making any stitch.
3. For every point from $2$ to $N$, append the point and then append point $1$ again. Each pair of moves goes from the center to a leaf and back.
4. Output the length of the sequence, which is exactly $2N-1$, followed by the generated sequence.

Why it works:

The generated sequence is an Euler walk of the star tree where every edge is traversed twice. The first traversal of every edge always appears on one side of the cloth, and the return traversal always appears on the other side. Since each side receives every edge of the star exactly once, both sides form connected planar spanning trees. The lower bound already proved that no shorter sequence can exist, so this construction is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    for _ in range(n):
        input()

    ans = [1]
    for i in range(2, n + 1):
        ans.append(i)
        ans.append(1)

    print(len(ans))
    print(*ans)

if __name__ == "__main__":
    solve()
```

The input coordinates are irrelevant after we realize that a star centered at any point is always a valid planar graph. The code still reads all coordinates because they are part of the input format.

The sequence construction starts with vertex `1`. For every other vertex, the code adds the trip from the center to that vertex and then immediately returns to the center. This creates exactly two appearances of each star edge, one for each side of the cloth.

The final sequence length is `1 + 2(N-1)`, which equals `2N-1`. No index manipulation beyond iterating from `2` to `N` is needed, so there are no boundary issues.

## Worked Examples

For the input:

```
5
1 1
2 4
3 2
4 5
5 3
```

the generated sequence is:

```
1 2 1 3 1 4 1 5 1
```

| Step | Added point | Current sequence | Front edge added | Back edge added |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | None | None |
| 2 | 2 | 1 2 | 1-2 | None |
| 3 | 1 | 1 2 1 | None | 2-1 |
| 4 | 3 | 1 2 1 3 | 1-3 | None |
| 5 | 1 | 1 2 1 3 1 | None | 3-1 |
| 6 | 4 | 1 2 1 3 1 4 | 1-4 | None |
| 7 | 1 | 1 2 1 3 1 4 1 | None | 4-1 |
| 8 | 5 | 1 2 1 3 1 4 1 5 | 1-5 | None |
| 9 | 1 | 1 2 1 3 1 4 1 5 1 | None | 5-1 |

The table shows that each side receives all four edges of the star. The example also demonstrates that the repeated center point is intentional.

For the input:

```
3
10 10
20 1
5 7
```

the sequence becomes:

```
1 2 1 3 1
```

| Step | Added point | Current sequence | Front edge added | Back edge added |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | None | None |
| 2 | 2 | 1 2 | 1-2 | None |
| 3 | 1 | 1 2 1 | None | 2-1 |
| 4 | 3 | 1 2 1 3 | 1-3 | None |
| 5 | 1 | 1 2 1 3 1 | None | 3-1 |

Both sides contain the tree connecting all three points, even though the geometric arrangement of the points is arbitrary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O($N$) | Each point is read once and appended to the answer once. |
| Space | O($N$) | The output sequence contains $2N-1$ indices. |

The maximum $N$ is small enough that a linear construction easily fits within the limits. The algorithm does not perform any geometry calculations, so the runtime is dominated by input and output.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# provided sample style
out = run("""5
1 1
2 4
3 2
4 5
5 3
""").split()

assert out[0] == "9", "sample 1 length"

# minimum size
out = run("""2
1 1
2 2
""").split()

assert out[0] == "3", "minimum size"

# all points arbitrary
out = run("""4
100 100
1 50
20 30
90 5
""").split()

assert out[0] == "7", "four points"

# larger case
out = run("""6
1 1
2 2
3 3
4 4
5 5
6 6
""").split()

assert out[0] == "11", "six points"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 points from the sample | 9 | The optimal length formula $2N-1$ |
| 2 points | 3 | The smallest valid sequence |
| Arbitrary coordinates | 7 | Coordinates do not affect the construction |
| 6 points on a line | 11 | Collinear points and larger input |

## Edge Cases

For two points, the lower bound gives $2N-1=3$. The algorithm creates:

```
1 2 1
```

The front side has the edge $1-2$, and the back side has the same edge drawn on the other side. The two points are connected on both sides, so the construction is valid.

For points arranged in a way where many arbitrary segments would cross, the algorithm still succeeds. Consider:

```
4
1 1
10 10
5 5
8 2
```

The output sequence is:

```
1 2 1 3 1 4 1
```

The only segments created are between point 1 and another point. Since all segments share point 1, intersections can only happen at that endpoint.

For large $N$, the algorithm continues the same pattern:

```
1 2 1 3 1 4 1 ... N 1
```

Every new point contributes exactly two positions and exactly one edge to each side. The invariant remains that both sides contain the same star spanning tree, so connectivity and planarity are preserved.
