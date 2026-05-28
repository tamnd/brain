---
title: "CF 39D - Cubical Planet"
description: "We are given two vertices of a unit cube. Each vertex is described by three coordinates, and every coordinate is either 0 or 1. Since each coordinate can only take two values, these coordinates represent the eight corners of the cube. Two flies stand on two different vertices."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 39
codeforces_index: "D"
codeforces_contest_name: "School Team Contest 1 (Winter Computer School 2010/11)"
rating: 1100
weight: 39
solve_time_s: 87
verified: true
draft: false
---

[CF 39D - Cubical Planet](https://codeforces.com/problemset/problem/39/D)

**Rating:** 1100  
**Tags:** math  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two vertices of a unit cube. Each vertex is described by three coordinates, and every coordinate is either `0` or `1`. Since each coordinate can only take two values, these coordinates represent the eight corners of the cube.

Two flies stand on two different vertices. They can see each other if both vertices belong to at least one common face of the cube. The task is to print `"YES"` when such a face exists, otherwise print `"NO"`.

The input size is tiny. We only read six integers total, so performance is irrelevant here. Even a brute-force geometric check over all cube faces would run instantly. The challenge is recognizing the geometric property hidden in the coordinates.

The key observation is how cube faces are represented in coordinates. Every face fixes exactly one coordinate. For example, the face `x = 0` contains all vertices whose first coordinate is `0`. Two vertices lie on the same face if they share at least one coordinate value in the same position.

There are a couple of easy-to-miss cases.

Consider opposite vertices:

```
0 0 0
1 1 1
```

The correct answer is `"NO"`. These vertices do not share any face because every coordinate differs. A careless approach that checks only Euclidean distance or edge connectivity could fail here.

Now consider vertices connected only diagonally across a face:

```
0 0 0
0 1 1
```

The correct answer is `"YES"`. These vertices are not adjacent by an edge, but they still belong to the face `x = 0`. A wrong solution might assume that only neighboring vertices can see each other.

Another subtle case is when exactly one coordinate matches:

```
1 0 1
1 1 0
```

The answer is still `"YES"` because both points belong to the face `x = 1`.

## Approaches

A brute-force solution would explicitly model the six faces of the cube. Each face contains four vertices. We could generate all cube vertices, group them by faces, then check whether both given vertices appear together in any face.

That approach is correct because the definition of visibility is exactly “sharing a face”. The cube has only six faces, so even a literal simulation would take constant time.

The geometry becomes much simpler once we describe faces using coordinates. Every cube face fixes one coordinate:

```
x = 0
x = 1
y = 0
y = 1
z = 0
z = 1
```

Two vertices lie on the same face precisely when at least one coordinate matches in the same position. If the first coordinates are equal, both vertices belong to either `x = 0` or `x = 1`. The same logic applies to `y` and `z`.

This removes all geometry from the implementation. We only need to compare the coordinates pairwise.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the coordinates of the first vertex into `(x1, y1, z1)`.
2. Read the coordinates of the second vertex into `(x2, y2, z2)`.
3. Compare corresponding coordinates.

If `x1 == x2`, both vertices lie on the same `x` face.

If `y1 == y2`, both vertices lie on the same `y` face.

If `z1 == z2`, both vertices lie on the same `z` face.
4. If at least one comparison matches, print `"YES"`.
5. Otherwise print `"NO"`.

### Why it works

Every face of a cube is defined by fixing one coordinate. For example, all vertices on the face `z = 1` have third coordinate equal to `1`.

If two vertices share any coordinate value in the same position, they both belong to the corresponding face. Conversely, if all three coordinates differ, then one vertex is at the opposite corner of the cube from the other, and no face contains both points.

The algorithm checks exactly this condition, so it is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

x1, y1, z1 = map(int, input().split())
x2, y2, z2 = map(int, input().split())

if x1 == x2 or y1 == y2 or z1 == z2:
    print("YES")
else:
    print("NO")
```

The program reads two triples of coordinates and compares each coordinate independently.

The condition uses logical `or` because sharing even one coordinate is enough to place both vertices on a common face.

A common mistake is requiring two matching coordinates. That would only detect vertices connected by an edge and would incorrectly reject face diagonals such as `(0,0,0)` and `(0,1,1)`.

Another possible mistake is checking adjacency by Manhattan distance. Visibility is broader than adjacency, so that approach misses valid cases.

## Worked Examples

### Example 1

Input:

```
0 0 0
0 1 0
```

| x1 | y1 | z1 | x2 | y2 | z2 | Matching coordinates | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 1 | 0 | x and z | YES |

The vertices share both `x = 0` and `z = 0`, so they clearly lie on common faces.

### Example 2

Input:

```
0 0 0
1 1 1
```

| x1 | y1 | z1 | x2 | y2 | z2 | Matching coordinates | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 1 | 1 | none | NO |

All coordinates differ. These are opposite cube corners, so no face contains both vertices.

This example confirms the key invariant: at least one coordinate must match.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only three coordinate comparisons are performed |
| Space | O(1) | The algorithm stores a fixed number of integers |

The running time and memory usage are both constant, far below the problem limits. The program finishes instantly even on the slowest environments.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    x1, y1, z1 = map(int, input().split())
    x2, y2, z2 = map(int, input().split())

    if x1 == x2 or y1 == y2 or z1 == z2:
        print("YES")
    else:
        print("NO")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run("0 0 0\n0 1 0\n") == "YES\n", "sample 1"

# opposite corners
assert run("0 0 0\n1 1 1\n") == "NO\n", "opposite vertices"

# face diagonal
assert run("0 0 0\n0 1 1\n") == "YES\n", "same face but not adjacent"

# exactly one coordinate equal
assert run("1 0 1\n1 1 0\n") == "YES\n", "single matching coordinate"

# another opposite pair
assert run("1 0 0\n0 1 1\n") == "NO\n", "all coordinates different"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0 / 1 1 1` | `NO` | Opposite cube corners |
| `0 0 0 / 0 1 1` | `YES` | Face diagonal visibility |
| `1 0 1 / 1 1 0` | `YES` | Exactly one matching coordinate |
| `1 0 0 / 0 1 1` | `NO` | No shared face |

## Edge Cases

Consider opposite vertices:

```
0 0 0
1 1 1
```

The algorithm compares coordinates one by one:

```
0 == 1 → false
0 == 1 → false
0 == 1 → false
```

No coordinate matches, so the program prints `"NO"`. This correctly identifies that opposite corners never share a face.

Now consider a face diagonal:

```
0 0 0
0 1 1
```

The first coordinates match:

```
0 == 0 → true
```

The algorithm immediately knows both vertices belong to the face `x = 0`, so it prints `"YES"`.

Finally, consider a case with only one shared coordinate:

```
1 0 1
1 1 0
```

The comparison results are:

```
1 == 1 → true
0 == 1 → false
1 == 0 → false
```

At least one coordinate matches, which is enough for visibility. The output is `"YES"`.

These cases show why the condition “at least one equal coordinate” exactly matches the geometry of cube faces.
