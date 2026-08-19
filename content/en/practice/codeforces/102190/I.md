---
title: "CF 102190I - standard input/output"
description: "We have (n) points and an (n times n) distance matrix. Some entries already contain their final values, while every (-1) represents a distance that we are free to choose."
date: "2026-08-20T00:44:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102190
codeforces_index: "I"
codeforces_contest_name: "2019 ECNU Campus Invitational Contest"
rating: 0
weight: 102190
solve_time_s: 133
verified: true
draft: false
---

[CF 102190I - standard input/output](https://codeforces.com/problemset/problem/102190/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (n) points and an (n \times n) distance matrix. Some entries already contain their final values, while every (-1) represents a distance that we are free to choose. The final matrix must satisfy the four required properties: every diagonal entry is zero, every distance is non-negative, the matrix is symmetric, and every direct distance obeys the triangle inequality.

The restriction on existing entries is strict. If the input says (d(i,j)=7), the answer must also contain (7) at that position. An unknown entry, on the other hand, can take any value from (0) through (10^9). The statement allows zero between distinct points, so this is a pseudometric rather than the stricter convention where distinct points must have positive distance.

The largest matrix has (500^2=250000) entries, and the sum of (n) over all test cases is at most (500). This makes an (O(n^3)) algorithm the natural target. At (n=500), cubic work is about (125) million elementary iterations, while (O(n^4)) or worse would become unnecessarily expensive. The small total sum of (n) also prevents many large test cases from multiplying the cubic cost.

There are several cases where a simple fill strategy can silently fail. A known diagonal value such as

```
2
1 -1
-1 0
```

must produce `NO`, because the first point is required to have distance zero from itself. A careless algorithm that only processes off-diagonal entries might overlook this contradiction.

Symmetry can also be violated directly. For example,

```
2
0 3
4 0
```

is impossible because the two representations of the same distance disagree. Filling only the (-1) entries would not repair this, since neither existing value may be changed.

A more subtle contradiction comes from a shorter known path. Consider

```
3
0 5 2
5 0 2
2 2 0
```

The direct distance between points (1) and (2) is fixed at (5), but the route (1 \rightarrow 3 \rightarrow 2) has length (4). Any metric must satisfy (d(1,2)\le4), so the fixed value (5) makes the instance impossible. Checking only triangles that are explicitly present in the input is not enough for larger paths of this kind.

Finally, the known-distance graph can be disconnected. For example,

```
3
0 2 -1
2 0 -1
-1 -1 0
```

is perfectly completable. The first two points form one component and the third point forms another. We can choose a sufficiently large distance between the components. A solution that assumes every pair has a finite shortest path would incorrectly reject this case.

The official contest sample contains four test cases, including the disconnected and partially specified situations described above.

## Approaches

A brute-force approach would treat every unknown distance as a variable and try possible values until a complete metric is found. Even after exploiting symmetry, an (n=500) instance can have

[
\frac{500\cdot499}{2}=124750
]

unknown unordered pairs. Since an output value can be any integer from (0) to (10^9), exhaustive enumeration has

[
(10^9+1)^{124750}
]

possible assignments in the worst case. Checking each candidate would itself require at least (O(n^3)) work to verify all triangle inequalities. This is not merely too slow, it is computationally infeasible.

The brute-force idea does contain the right conceptual starting point: every known distance can be regarded as a constraint that must remain unchanged. The key is to stop thinking of the missing entries as independent variables.

Treat every known distance as an undirected weighted edge. Once this graph is built, any valid metric must satisfy

[
d(u,v)\le d(u,x_1)+d(x_1,x_2)+\cdots+d(x_k,v)
]

for every path between (u) and (v). Consequently, a fixed edge of weight (w) can survive only if there is no known path between its endpoints whose total weight is smaller than (w).

The shortest-path metric of the known graph gives exactly the strongest distances forced by the existing constraints. If a fixed edge is longer than its shortest known path, the instance is impossible. If no fixed edge becomes shorter, the shortest-path distances themselves are a valid completion inside every connected component.

This is precisely what Floyd-Warshall computes. Initialize the matrix with the known distances and infinity for missing entries, then compute all-pairs shortest paths. Afterward, every known distance must equal the corresponding shortest-path distance.

Disconnected components require one final detail. There is no path between two different components, so their distances remain infinity after Floyd-Warshall. We can replace every such infinity by (10^9). Choosing one common sufficiently large value between components preserves the triangle inequality and stays within the required output range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (\Theta((10^9+1)^{\Theta(n^2)})) candidates | (O(n^2)) | Too slow |
| Optimal | (O(n^3)) | (O(n^2)) | Accepted |

## Algorithm Walkthrough

1. Read the matrix and remember which entries were originally fixed. Set the working diagonal to zero only if the input diagonal is already zero. If a known diagonal entry is anything else, reject immediately because no metric can change it.
2. Check every pair (i,j) for symmetry. If both (d(i,j)) and (d(j,i)) are known, they must be equal. If only one direction is known, copy that value to the other direction in the working matrix. This is valid because the missing entry has no restriction yet, while symmetry forces it to equal the known one.
3. Interpret every known off-diagonal distance as an undirected weighted edge. Initialize missing distances to `INF`, where `INF` is much larger than every possible finite shortest-path distance.
4. Run Floyd-Warshall. For every intermediate vertex (k), try to improve every pair (i,j) through (k) using

[
d(i,j)=\min(d(i,j),d(i,k)+d(k,j)).
]

The resulting matrix contains the shortest path using only distances that were already known.

1. Check every originally fixed distance against the shortest-path matrix. If an original value (w) has become smaller than (w), the fixed edge is longer than a forced path and no completion can exist. Reject the test case.
2. Replace every remaining `INF` entry by (10^9). These are exactly the pairs lying in different connected components of the known-distance graph. A large common value can safely connect different components because every finite internal distance is much smaller than (10^9).
3. Output the resulting matrix. Every finite entry produced by Floyd-Warshall is a shortest-path distance, while every cross-component entry is the common large value. The diagonal remains zero.

**Why it works.** The central invariant is that after Floyd-Warshall, every finite value (d(i,j)) is the minimum length of a path formed entirely from originally known distances. Any valid completion must satisfy the triangle inequality along every such path, so it must have (d(i,j)) no larger than that shortest-path value. At the same time, if an originally fixed edge has exactly its shortest-path value, keeping that value is compatible with every known path. Thus a fixed value smaller than every known path is safe, while a fixed value larger than some known path is impossible. Once all fixed entries survive this test, the shortest-path distances satisfy the triangle inequality by construction. Different connected components have no constraints between them, and assigning (10^9) to every cross-component pair creates valid triangle inequalities because all internal finite distances are below (10^9).

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**15
BIG = 10**9

def solve_case(a):
    n = len(a)

    # Build a symmetric working matrix.
    dist = [[INF] * n for _ in range(n)]
    fixed = []

    for i in range(n):
        if a[i][i] != -1 and a[i][i] != 0:
            return None

        dist[i][i] = 0

    for i in range(n):
        for j in range(i + 1, n):
            x = a[i][j]
            y = a[j][i]

            if x != -1 and y != -1:
                if x != y:
                    return None
                w = x
                fixed.append((i, j, w))
                dist[i][j] = w
                dist[j][i] = w
            elif x != -1:
                fixed.append((i, j, x))
                dist[i][j] = x
                dist[j][i] = x
            elif y != -1:
                fixed.append((i, j, y))
                dist[i][j] = y
                dist[j][i] = y

    # Floyd-Warshall.
    rng = range(n)
    for k in rng:
        dk = dist[k]
        for i in rng:
            di = dist[i]
            dik = di[k]
            if dik == INF:
                continue

            for j in rng:
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd

    # Every fixed edge must still have exactly its original value.
    for u, v, w in fixed:
        if dist[u][v] != w:
            return None

    # Connect different components with one sufficiently large value.
    for i in rng:
        di = dist[i]
        for j in rng:
            if di[j] == INF:
                di[j] = BIG

    return dist

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = [list(map(int, input().split())) for _ in range(n)]

        ans = solve_case(a)

        if ans is None:
            out.append("NO")
            continue

        out.append("YES")
        for row in ans:
            out.append(" ".join(map(str, row)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first construction phase deliberately separates the original matrix from the working matrix. The `fixed` list records every known unordered pair, so later we can distinguish an edge that was allowed to change from one that was required to stay unchanged.

The symmetry check is performed before Floyd-Warshall. If only one side of a pair is known, copying it to the other side is not modifying a fixed value. It is simply assigning the missing value that symmetry forces. If both sides are present and differ, there is no possible answer.

The diagonal receives special handling because there is no reason to put a self-loop into the graph. A known zero is consistent with every metric, while any other known diagonal value immediately makes the instance impossible.

`INF` is deliberately much larger than the output limit. A connected component containing at most 500 vertices has a simple path with at most 499 edges, and each original edge is at most 1000, so any finite shortest path is at most (499000). The chosen `INF` is therefore safely unreachable by legitimate distances. Python integers also have arbitrary precision, so there is no overflow issue.

The Floyd-Warshall loop skips a row when `dist[i][k]` is infinite. This matters for disconnected graphs, where many pairs can remain unreachable throughout the computation. The local variables `dk` and `di` also avoid repeated indexing of the two-dimensional list.

After Floyd-Warshall, checking only the input's known entries is sufficient. Unknown entries are allowed to take the shortest-path values, so they impose no additional restriction. If a fixed edge has been reduced, the reduction represents a known path that violates the required triangle inequalities.

Finally, all unreachable pairs are assigned `BIG`. The value is exactly (10^9), which is permitted by the output bound. It is larger than every possible finite distance generated from the original constraints, so cross-component distances cannot introduce a new shorter route that would alter a fixed internal distance.

## Worked Examples

### Sample 1

The first sample is already a complete metric:

```
3
0 3 3
3 0 3
3 3 0
```

The key state during Floyd-Warshall is unchanged.

| Intermediate (k) | (d(1,2)) | (d(1,3)) | (d(2,3)) | Result |
| --- | --- | --- | --- | --- |
| Initial | 3 | 3 | 3 | All fixed |
| 1 | 3 | 3 | 3 | No improvement |
| 2 | 3 | 3 | 3 | No improvement |
| 3 | 3 | 3 | 3 | No improvement |

Every fixed value equals its shortest-path distance, so the answer is `YES` followed by the same matrix.

This example demonstrates that Floyd-Warshall is not trying to change fixed entries arbitrarily. It only reveals whether another collection of fixed edges would force them to become smaller.

### Sample 2

The second sample is

```
3
0 0 0
0 0 -1
0 -1 0
```

The missing pair is forced to zero by symmetry and the known zero distances.

| Stage | (d(1,2)) | (d(1,3)) | (d(2,3)) | State |
| --- | --- | --- | --- | --- |
| Input | 0 | 0 | -1 | One direction is missing |
| Symmetry completion | 0 | 0 | 0 | Missing value becomes 0 |
| (k=1) | 0 | 0 | 0 | No improvement |
| (k=2) | 0 | 0 | 0 | No improvement |
| (k=3) | 0 | 0 | 0 | No improvement |

The final matrix is all zeros.

This case exercises the non-standard part of the statement: distinct points are allowed to have distance zero. An implementation that assumes strict positivity for distinct points would reject a valid input.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^3)) | Floyd-Warshall examines all triples of vertices |
| Space | (O(n^2)) | The distance matrix and original fixed-edge information occupy quadratic space |

With (n\le500), the cubic bound is the intended scale for this problem, and the total sum of (n) across test cases is also at most 500. The matrix requires only (250000) distance values at maximum, so quadratic memory usage is easily manageable.

## Test Cases

The output of a constructive problem does not have to be unique, so a robust test harness should validate the returned matrix rather than compare every `YES` case to one exact matrix. The small official samples happen to match the deterministic construction below.

```python
import sys
import io

INF = 10**15
BIG = 10**9

def solve_case(a):
    n = len(a)
    dist = [[INF] * n for _ in range(n)]
    fixed = []

    for i in range(n):
        if a[i][i] != -1 and a[i][i] != 0:
            return None
        dist[i][i] = 0

    for i in range(n):
        for j in range(i + 1, n):
            x = a[i][j]
            y = a[j][i]

            if x != -1 and y != -1:
                if x != y:
                    return None
                fixed.append((i, j, x))
                dist[i][j] = x
                dist[j][i] = x
            elif x != -1:
                fixed.append((i, j, x))
                dist[i][j] = x
                dist[j][i] = x
            elif y != -1:
                fixed.append((i, j, y))
                dist[i][j] = y
                dist[j][i] = y

    for k in range(n):
        dk = dist[k]
        for i in range(n):
            di = dist[i]
            dik = di[k]
            if dik == INF:
                continue
            for j in range(n):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd

    for u, v, w in fixed:
        if dist[u][v] != w:
            return None

    for i in range(n):
        for j in range(n):
            if dist[i][j] == INF:
                dist[i][j] = BIG

    return dist

def solve(inp):
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = [list(map(int, input().split())) for _ in range(n)]
        ans = solve_case(a)

        if ans is None:
            out.append("NO")
        else:
            out.append("YES")
            for row in ans:
                out.append(" ".join(map(str, row)))

    sys.stdin = old_stdin
    return "\n".join(out)

def parse_output(s):
    return s.strip().splitlines()

def assert_valid_case(a, output_lines, pos):
    n = len(a)

    assert output_lines[pos] == "YES"
    pos += 1

    b = []
    for _ in range(n):
        row = list(map(int, output_lines[pos].split()))
        assert len(row) == n
        b.append(row)
        pos += 1

    for i in range(n):
        assert b[i][i] == 0
        for j in range(n):
            assert 0 <= b[i][j] <= BIG
            assert b[i][j] == b[j][i]
            if a[i][j] != -1:
                assert b[i][j] == a[i][j]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                assert b[i][j] <= b[i][k] + b[k][j]

    return pos

# Official sample
sample = """\
4
3
0 3 3
3 0 3
3 3 0
3
0 0 0
0 0 -1
0 -1 0
3
5 6 7
-1 -1 -1
-1 -1 -1
3
-1 3 5
-1 -1 3
-1 -1 -1
"""

expected_sample = """\
YES
0 3 3
3 0 3
3 3 0
YES
0 0 0
0 0 0
0 0 0
NO
YES
0 3 5
3 0 3
5 3 0
"""

assert solve(sample) == expected_sample.strip(), "official sample"

# Minimum-size valid input.
case_min = """\
1
2
0 1000
1000 0
"""
assert solve(case_min) == """\
YES
0 1000
1000 0
""".strip(), "minimum size and maximum fixed distance"

# All distances equal to zero, including distinct points.
case_zero = """\
1
4
0 0 -1 0
0 0 0 -1
-1 0 0 0
0 -1 0 0
"""
assert solve(case_zero) == """\
YES
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
""".strip(), "all-zero pseudometric"

# A longer known path contradicts a fixed direct edge.
case_shorter_path = """\
1
3
0 5 2
5 0 2
2 2 0
"""
assert solve(case_shorter_path).strip() == "NO", "fixed edge is longer than a known path"

# Asymmetric fixed values.
case_asymmetric = """\
1
2
0 3
4 0
"""
assert solve(case_asymmetric).strip() == "NO", "symmetry contradiction"

# Maximum-size case, all distances initially unknown.
n = 500
rows = []
for i in range(n):
    row = [-1] * n
    row[i] = 0
    rows.append(row)

max_input = "1\n500\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"
max_output = solve(max_input)
max_lines = parse_output(max_output)

assert max_lines[0] == "YES"
assert len(max_lines) == 501

for i in range(500):
    row = list(map(int, max_lines[i + 1].split()))
    assert len(row) == 500
    assert row[i] == 0
    for j in range(500):
        if i != j:
            assert row[j] == BIG
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` points with distance `1000` | The fixed matrix | Minimum size and the largest allowed input distance |
| Four points with all distances zero | All-zero matrix | Zero distances between distinct points |
| Three points with edges `2, 2, 5` | `NO` | Detection of a shorter multi-edge path |
| Two points with `3` in one direction and `4` in the other | `NO` | Symmetry validation |
| (500\times500) matrix with only zero diagonals | `YES`, zero diagonal and (10^9) elsewhere | Maximum size and disconnected components |

## Edge Cases

A non-zero fixed diagonal is rejected before graph processing. For the input

```
1
2
1 -1
-1 0
```

the first diagonal entry is `1`, so `solve_case` immediately returns `None`. The output is `NO`. No shortest-path calculation can make this valid because the diagonal is a direct metric axiom.

An asymmetric pair is handled before Floyd-Warshall. With

```
1
2
0 3
4 0
```

the pair ((1,2)) has two fixed values, `3` and `4`. The construction detects `x != y` and rejects the case. A tempting alternative would be to overwrite one side with the other, but that would violate the requirement that fixed input values cannot be modified.

The shorter-path contradiction is detected by the all-pairs shortest-path phase. For

```
1
3
0 5 2
5 0 2
2 2 0
```

the initial edge (1\leftrightarrow2) has weight `5`. Once vertex (3) is considered as an intermediate vertex, Floyd-Warshall obtains

[
d(1,2)=\min(5,2+2)=4.
]

The original fixed value was `5`, so the final validation fails and the answer is `NO`. The same argument works for a path containing many edges, which is why checking only directly visible triangles is insufficient.

A partially specified symmetric pair is filled from the known side. In

```
1
3
0 3 -1
-1 0 4
-1 -1 0
```

the entries (d(1,2)) and (d(2,1)) become `3`, while (d(2,3)) and (d(3,2)) become `4`. The remaining pair can be chosen as `7`, which is the shortest-path value through vertex (2). The algorithm naturally discovers this through Floyd-Warshall.

Disconnected components are completed after shortest paths are computed. For

```
1
3
0 2 -1
2 0 -1
-1 -1 0
```

vertices (1) and (2) have distance `2`, while vertex (3) has no known connection to them. Floyd-Warshall leaves the cross-component entries at `INF`, and the final phase changes those entries to (10^9). The resulting matrix is

```
0 2 1000000000
2 0 1000000000
1000000000 1000000000 0
```

Every triangle involving two cross-component distances is valid, and the internal distance `2` is far smaller than (10^9+10^9).

Finally, an input with every off-diagonal entry equal to zero is valid under this problem's definition. For example,

```
1
3
0 0 0
0 0 0
0 0 0
```

passes unchanged. The implementation never inserts a positivity requirement for distinct vertices, matching the actual condition used by the problem.
