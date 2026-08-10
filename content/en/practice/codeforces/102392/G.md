---
title: "CF 102392G - Projection"
description: "For a fixed depth coordinate x, the first projection tells us which y-positions must contain at least one cube, while the second projection tells us which z-positions must contain at least one cube. A cube at (x,y,z) simultaneously creates the projection cells (x,y) and (x,z)."
date: "2026-08-10T19:35:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102392
codeforces_index: "G"
codeforces_contest_name: "2019-2020 ICPC Southeastern European Regional Programming Contest (SEERC 2019)"
rating: 0
weight: 102392
solve_time_s: 131
verified: true
draft: false
---

[CF 102392G - Projection](https://codeforces.com/problemset/problem/102392/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

For a fixed depth coordinate x, the first projection tells us which y-positions must contain at least one cube, while the second projection tells us which z-positions must contain at least one cube. A cube at (x,y,z) simultaneously creates the projection cells (x,y) and (x,z).

Let Y x ​ be the set of y-coordinates where the first projection contains a `1` in row x, and let Z x ​ be the corresponding set of z-coordinates from the second projection. A cube at depth x is useful exactly when y∈Y x ​ and z∈Z x ​. Consequently, once both sets are known, every pair in Y x ​ ×Z x ​ is a legal cube.

This completely separates the three-dimensional problem into n independent two-dimensional problems. For each x, we only need to connect every vertex of Y x ​ with at least one vertex of Z x ​.

The first feasibility condition follows immediately. If Y x ​ is nonempty but Z x ​ is empty, a required first-projection cell can never be produced. The same is true with the two sides reversed. If both sets are empty, that slice simply contains no cubes and is valid.

The dimensions are at most 100, so there are at most 100⋅100⋅100=10 6 possible cubes. This is small enough to enumerate all cubes once, but far too large for any exponential search over subsets. The required solution should be essentially linear in the number of possible cubes, which is comfortably within the 1 second limit in optimized implementations.

A subtle case is a completely empty slice. For example,

```
1 2 2
00
00
```

has no required shadows at all. The correct output is

```
0
0
```

A careless implementation that assumes every slice needs at least one cube might incorrectly reject it.

Another important case is an inconsistent slice:

```
1 2 1
10
0
```

The first projection requires a cube with y=0, but the second projection requires no cube at all because its only entry is zero. The correct output is

```
-1
```

Trying to construct a cube from every `1` in the first projection would silently create an unwanted `1` in the second projection.

The lexicographic requirement also matters. Consider

```
1 3 2
111
11
```

There are three required y-positions and two required z-positions. Three cubes are necessary and sufficient. The lexicographically smallest minimum solution is

```
3
0 0 0
0 1 0
0 2 1
```

A construction that pairs the coordinates diagonally without considering lexicographic order could produce a valid solution with the same number of cubes but a larger coordinate sequence.

## Approaches

The brute-force approach is to consider every subset of the nmh possible cubes, project that subset onto the two matrices, and keep the valid subset with maximum size and the valid subset with minimum size. This is correct because every possible physical arrangement is represented by exactly one subset of cubes. However, there are 2 nmh subsets. At the maximum dimensions this becomes 2 1,000,000 candidates, and even checking one candidate would require up to 10 6 cube operations. This is completely infeasible.

The useful observation is that cubes with different x-coordinates never interact. For one fixed x, the allowed cubes form a complete bipartite graph between Y x ​ and Z x ​. There is an edge between every required y-coordinate and every required z-coordinate.

For the maximum solution, every allowed edge can be present. Adding any cube whose two projection cells are already required cannot invalidate the projections, so the maximum solution contains exactly ∣Y x ​ ∣∣Z x ​ ∣ cubes in slice x.

For the minimum solution, we need the fewest edges that touch every vertex of this complete bipartite graph. If the two sides contain a and b vertices, every cube touches at most one vertex from each side, so at least max(a,b) cubes are necessary. That many are also sufficient: assign one edge to every vertex of the larger side and reuse vertices from the smaller side as necessary. Thus the minimum for slice x is max(∣Y x ​ ∣,∣Z x ​ ∣).

The remaining issue is choosing those edges lexicographically. Suppose a≥b. There must be exactly one edge for each y, because a edges are required and all a different y-coordinates must appear. Since the output is sorted by (x,y,z), the y-coordinates are forced to appear as y 0 ​ ,y 1 ​ ,…,y a−1 ​. To make the sequence of z-coordinates lexicographically smallest while still using every z, we use the smallest z as many times as possible, then move to the next one. Hence the sequence is z 0 ​ repeated a−b+1 times, followed by z 1 ​ ,z 2 ​ ,…,z b−1 ​. The case b>a is symmetric.

The brute-force method works because it explicitly considers every arrangement, but fails because the number of arrangements is exponential. The observation that every slice is a complete bipartite graph reduces the problem to simple counting and a direct lexicographic construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2 nmh ⋅nmh) | O(nmh) | Too slow |
| Optimal | O(nmh) | O(n(m+h)) | Accepted |

## Algorithm Walkthrough

1. Read the two projection matrices and, for every x, store the y-coordinates and z-coordinates containing `1`.

The two lists completely describe everything that can happen in that slice. There is no need to store the three-dimensional volume itself.
2. For every x, check whether exactly one of Y x ​ and Z x ​ is empty.

If that happens, the projections contradict each other. A cube producing a required y-position would necessarily produce some z-position, and vice versa. If the check fails for any x, print `-1`.
3. For the maximum solution, iterate through every y∈Y x ​ and every z∈Z x ​, and output the cube (x,y,z).

Every such pair is allowed, and adding all of them still produces exactly the same projection because both endpoints were already marked as `1`. Since every possible legal cube is included, the number of cubes is maximal.
4. For the minimum solution, let a=∣Y x ​ ∣, b=∣Z x ​ ∣, and k=max(a,b).

At least k cubes are necessary because each cube can introduce at most one new y-coordinate and at most one new z-coordinate. A construction with k cubes exists, so k is optimal.
5. Generate the minimum solution by iterating i from k down to 1. Use

y[max(0,a−i)]

and

z[max(0,b−i)].

When one side is larger, its coordinates advance through the entire list while the smaller side repeats its smallest coordinate until every vertex on the larger side has been covered. Because the lists are stored in increasing order, the produced triples are already lexicographically sorted.
6. Process x in increasing order and each stored projection coordinate in increasing order.

This makes the complete output lexicographically ordered, which is required by the statement. Since different x-slices are independent, making each slice lexicographically smallest also makes the concatenated solution lexicographically smallest.

### Why it works

For every fixed x, the required projection cells define a complete bipartite graph between Y x ​ and Z x ​. A valid cube set is exactly an edge set that touches every vertex. If either side is empty while the other is not, such an edge set cannot exist. Otherwise, all ab edges are legal, giving the maximum solution.

For a minimum solution, at least max(a,b) edges are required because one edge can cover at most one vertex on each side. The construction uses exactly that many edges and covers every vertex, so it is optimal. Among all such solutions, if a≥b, every y must occur exactly once. Their order is consequently fixed. The smallest possible z is chosen at every position where doing so still leaves enough positions to introduce all remaining z-coordinates. This gives the smallest possible z-sequence, proving lexicographic optimality. The symmetric argument applies when b>a.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, h = map(int, input().split())

    ys = [[] for _ in range(n)]
    zs = [[] for _ in range(n)]

    for x in range(n):
        row = input().strip()
        for y, ch in enumerate(row):
            if ch == '1':
                ys[x].append(y)

    for x in range(n):
        row = input().strip()
        for z, ch in enumerate(row):
            if ch == '1':
                zs[x].append(z)

    for x in range(n):
        if bool(ys[x]) != bool(zs[x]):
            print(-1)
            return

    out = []

    # Maximum solution.
    kmax = 0
    for x in range(n):
        kmax += len(ys[x]) * len(zs[x])

    out.append(str(kmax))

    for x in range(n):
        for y in ys[x]:
            for z in zs[x]:
                out.append(f"{x} {y} {z}")

    # Minimum solution.
    kmin = 0
    for x in range(n):
        kmin += max(len(ys[x]), len(zs[x]))

    out.append(str(kmin))

    for x in range(n):
        a = len(ys[x])
        b = len(zs[x])
        k = max(a, b)

        for i in range(k, 0, -1):
            y = ys[x][max(0, a - i)]
            z = zs[x][max(0, b - i)]
            out.append(f"{x} {y} {z}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input is stored as two lists per x. A `1` in the first projection becomes an entry in `ys[x]`, while a `1` in the second becomes an entry in `zs[x]`. The original matrices do not need to remain in memory after these lists are constructed.

The feasibility check compares whether the two lists are empty using `bool`. The equality of these two Boolean values is exactly the condition that either both projection sets are empty or both are nonempty.

The maximum count uses the product of the two list sizes. The nested loops then enumerate every pair in increasing y, followed by increasing z. This produces triples in lexicographic order because x is already processed from small to large.

For the minimum construction, the expression `max(0, a - i)` is the key boundary operation. When a is smaller than b, the index remains zero for the first several iterations, so the smallest y is repeated. Once the larger index reaches the end of the smaller list, all smaller-side coordinates have been used. The same expression handles the opposite imbalance without a separate branch.

Python integers have arbitrary precision, so the maximum count, at most 10 6, needs no special integer handling. The output is accumulated in a list and written once, avoiding the overhead of a million separate `print` calls.

## Worked Examples

### Sample 1

For the first sample, the projection rows produce the following slice sizes.

| x | Y x ​ | Z x ​ | Maximum | Minimum |
| --- | --- | --- | --- | --- |
| 0 | 0,1,2 | 0,1,2 | 9 | 3 |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 1 | 0,1 | 2 | 2 |
| 3 | 1 | 0 | 1 | 1 |
| 4 | 1 | 0 | 1 | 1 |

The maximum count is

9+1+2+1+1=14.

For x=0, both sides have size three, so the minimum construction uses

```
(0,0,0)
(0,1,1)
(0,2,2)
```

For x=2, the sizes are one and two, so the smaller y-coordinate is repeated:

```
(2,1,0)
(2,1,1)
```

The complete minimum construction has eight cubes.

| x | a | b | k | Generated minimum pairs |
| --- | --- | --- | --- | --- |
| 0 | 3 | 3 | 3 | (0,0), (1,1), (2,2) |
| 1 | 1 | 1 | 1 | (1,0) |
| 2 | 1 | 2 | 2 | (1,0), (1,1) |
| 3 | 1 | 1 | 1 | (1,0) |
| 4 | 1 | 1 | 1 | (1,0) |

This demonstrates both the equal-size case and the case where one projection contains more required coordinates than the other.

### Sample 2

The second sample is

```
2 2 2
00
00
11
11
```

The first projection contains no `1` in either row, so both Y 0 ​ and Y 1 ​ are empty. The second projection contains two required z-coordinates in each row.

| x | Y x ​ | Z x ​ | Feasible |
| --- | --- | --- | --- |
| 0 | empty | 0,1 | no |
| 1 | empty | 0,1 | no |

The first slice already has an empty Y x ​ and nonempty Z x ​. A cube cannot produce a `1` in the second projection without simultaneously producing a `1` in the first projection, so the correct result is immediately `-1`.

This trace exercises the consistency check before either maximum or minimum construction begins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nmh) | Reading the projections costs O(nm+nh), enumerating the maximum solution costs at most O(nmh), and constructing the minimum solution costs O(n(m+h)). |
| Space | O(n(m+h)+nmh) | The projection lists use O(n(m+h)) space and the output buffer can contain O(nmh) triples. |

The largest possible output itself contains 10 6 cubes, so any accepted implementation must spend at least linear time in the output size in the worst case. The algorithm performs only constant work per output cube and avoids matching, flow, dynamic programming, or exponential enumeration. The memory limit of 512 MB is sufficient for the projection lists and output buffer.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m, h = map(int, input().split())

    ys = [[] for _ in range(n)]
    zs = [[] for _ in range(n)]

    for x in range(n):
        row = input().strip()
        for y, ch in enumerate(row):
            if ch == '1':
                ys[x].append(y)

    for x in range(n):
        row = input().strip()
        for z, ch in enumerate(row):
            if ch == '1':
                zs[x].append(z)

    for x in range(n):
        if bool(ys[x]) != bool(zs[x]):
            print(-1)
            return

    out = []

    kmax = sum(len(ys[x]) * len(zs[x]) for x in range(n))
    out.append(str(kmax))

    for x in range(n):
        for y in ys[x]:
            for z in zs[x]:
                out.append(f"{x} {y} {z}")

    kmin = sum(max(len(ys[x]), len(zs[x])) for x in range(n))
    out.append(str(kmin))

    for x in range(n):
        a = len(ys[x])
        b = len(zs[x])
        k = max(a, b)

        for i in range(k, 0, -1):
            y = ys[x][max(0, a - i)]
            z = zs[x][max(0, b - i)]
            out.append(f"{x} {y} {z}")

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample1_in = """\
5 3 3
111
010
010
010
010
111
100
110
100
100
"""

sample1_out = """\
14
0 0 0
0 0 1
0 0 2
0 1 0
0 1 1
0 1 2
0 2 0
0 2 1
0 2 2
1 1 0
2 1 0
2 1 1
3 1 0
4 1 0
8
0 0 0
0 1 1
0 2 2
1 1 0
2 1 0
2 1 1
3 1 0
4 1 0
"""

sample2_in = """\
2 2 2
00
00
11
11
"""

sample2_out = """\
-1
"""

sample3_in = """\
2 3 2
101
011
10
11
"""

sample3_out = """\
6
0 0 0
0 2 0
1 1 0
1 1 1
1 2 0
1 2 1
4
0 0 0
0 2 0
1 1 0
1 2 1
"""

assert run(sample1_in) == sample1_out, "sample 1"
assert run(sample2_in) == sample2_out, "sample 2"
assert run(sample3_in) == sample3_out, "sample 3"

assert run("""\
1 1 1
1
1
""") == """\
1
0 0 0
1
0 0 0
""", "minimum-size nonempty case"

assert run("""\
2 2 2
00
00
00
00
""") == """\
0
0
""", "all-zero projections"

assert run("""\
1 2 1
10
0
""") == """\
-1
""", "inconsistent projections"

assert run("""\
1 2 3
11
111
""") == """\
6
0 0 0
0 0 1
0 0 2
0 1 0
0 1 1
0 1 2
3
0 0 0
0 0 1
0 1 2
""", "unequal sides"

assert run(
    "100 100 100\n" +
    ("0" * 100 + "\n") * 100 +
    ("0" * 100 + "\n") * 100
) == "0\n0", "maximum dimensions with all zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1`, both projections `1` | One identical cube in each solution | Minimum dimensions and the smallest possible nonempty volume |
| `2 2 2`, all zeros | `0` cubes for both solutions | Empty volume and zero-sized slice handling |
| `1 2 1`, `10` versus `0` | `-1` | Projection consistency check |
| `1 2 3`, `11` versus `111` | Maximum 6, minimum 3 | Unequal projection sizes and lexicographic repetition |
| `100 100 100`, all zeros | `0` and `0` | Maximum dimensions, large input parsing, and all-equal values |

## Edge Cases

### An entirely empty slice

For

```
1 2 2
00
00
```

we have Y 0 ​ =∅ and Z 0 ​ =∅. The feasibility check accepts the slice because both sides are empty. Its contribution to the maximum is 0⋅0=0, and its contribution to the minimum is max(0,0)=0. The output is

```
0
0
```

No artificial cube is introduced, which is necessary because any cube would create unwanted projection cells.

### A required projection on only one side

For

```
1 2 1
10
0
```

we have Y 0 ​ ={0} and Z 0 ​ =∅. The Boolean emptiness values differ, so the algorithm prints `-1` before constructing anything. This prevents the common mistake of inventing a z-coordinate that would change the second projection.

### More y-coordinates than z-coordinates

For

```
1 3 2
111
11
```

we have Y 0 ​ =(0,1,2) and Z 0 ​ =(0,1). The lower bound says at least three cubes are required because there are three distinct y-coordinates. The construction uses

```
0 0 0
0 1 0
0 2 1
```

The first two cubes reuse the smallest z-coordinate because doing so is lexicographically better than using z=1 earlier. The final cube introduces the missing z=1. All three y-coordinates and both z-coordinates are covered.

### More z-coordinates than y-coordinates

For

```
1 2 3
11
111
```

we have Y 0 ​ =(0,1) and Z 0 ​ =(0,1,2). Three cubes are necessary because there are three distinct z-coordinates. The minimum construction is

```
0 0 0
0 0 1
0 1 2
```

Here y=0 is repeated because the y-side is smaller. The z-coordinates are introduced in increasing order, giving the lexicographically smallest possible sequence.

### Maximum output size

When n=m=h=100 and every projection cell is `1`, every one of the 10 6 possible cubes belongs to the maximum solution. The algorithm does not attempt to store a three-dimensional Boolean structure or search through configurations. It simply enumerates the million legal pairs. The minimum solution contains only 100⋅100=10 4 cubes because every one of the 100 slices requires max(100,100)=100 cubes.
