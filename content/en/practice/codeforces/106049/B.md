---
title: "CF 106049B - Kaosar and Segments"
description: "We have a regular polygon with vertices numbered from 1 to n in clockwise order. A segment may be drawn between vertices i and j only when the vertices are not adjacent on the polygon boundary and gcd(i, j) = 1."
date: "2026-06-25T12:34:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106049
codeforces_index: "B"
codeforces_contest_name: "TheForces Round #44 (DIV3.5-Forces)"
rating: 0
weight: 106049
solve_time_s: 42
verified: true
draft: false
---

[CF 106049B - Kaosar and Segments](https://codeforces.com/problemset/problem/106049/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a regular polygon with vertices numbered from `1` to `n` in clockwise order. A segment may be drawn between vertices `i` and `j` only when the vertices are not adjacent on the polygon boundary and `gcd(i, j) = 1`. The goal is to draw as many such segments as possible while keeping the drawing non-crossing. Segments are allowed to meet at endpoints, but two segments may not intersect in their interiors.

The input contains multiple test cases, each consisting of a single value `n`. For every test case we must output the maximum number of segments that can be added.

The largest value of `n` is `10^5`, and there can be up to `10^4` test cases. Any solution that performs per-vertex geometry or graph construction would be unnecessary. We need something close to constant time per test case.

A subtle point is that the coprimality condition looks important, which may tempt us into searching for a complicated graph structure. The key observation is that vertex `1` is coprime with every other vertex.

Consider `n = 3`.

```
3
```

There are no diagonals in a triangle, so the answer is `0`.

A careless solution that only checks the coprimality condition might incorrectly count segments involving vertex `1`, forgetting that adjacent vertices cannot be connected.

Consider `n = 4`.

The only diagonal is `(1,3)`, and it is valid because `gcd(1,3)=1`. The answer is `1`.

A solution that tries to count all coprime pairs would overcount because many valid pairs cannot coexist without crossings.

## Approaches

The brute-force way would be to generate every valid segment, then search for the largest non-crossing subset. Even constructing all candidate segments takes roughly `O(n²)` pairs, and finding the maximum compatible subset is much harder. With `n = 10^5`, this is completely infeasible.

The structure of polygons gives a much stronger fact. In any `n`-gon, the maximum possible number of non-crossing diagonals is `n - 3`. This happens in every triangulation.

So the question becomes: can we actually achieve `n - 3` using only allowed segments?

Yes.

Take every diagonal from vertex `1` to vertices `3, 4, ..., n-1`.

These segments form a fan triangulation. They never cross because they all share the same endpoint. Every such segment is valid:

`|1 - j| > 1` for `j = 3 ... n-1`, so the vertices are not adjacent.

`gcd(1, j) = 1` for every integer `j`.

The number of these diagonals is exactly:

$$(n-1) - 3 + 1 = n-3$$

Since no non-crossing configuration can contain more than `n-3` diagonals, and we have constructed exactly `n-3`, this is optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n²) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`.
2. Recall that any non-crossing set of diagonals in an `n`-gon contains at most `n - 3` diagonals.
3. Observe that every diagonal from vertex `1` to a vertex `j` with `3 ≤ j ≤ n-1` is allowed because `gcd(1, j) = 1`.
4. These diagonals form a fan, so none of them cross each other.
5. The number of such diagonals is exactly `n - 3`.
6. Output `n - 3`.

### Why it works

The upper bound comes from polygon triangulation theory: no non-crossing diagonal set can contain more than `n - 3` diagonals. Our construction uses exactly `n - 3` diagonals, all of which satisfy the problem's validity rules. Since we simultaneously achieve the global upper bound and satisfy all constraints, the answer must be `n - 3`.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    print(n - 3)
```

The implementation is extremely small because all of the work is done by the mathematical observation.

For each test case we output `n - 3`. No geometry, graph construction, or gcd computation is needed. The proof already guarantees that the fan centered at vertex `1` always exists and is optimal.

The only boundary condition is `n = 3`. In that case the formula gives `0`, which is correct because a triangle has no diagonals.

## Worked Examples

### Example 1

Input:

```
3
```

| n | Answer |
| --- | --- |
| 3 | 0 |

There are no diagonals in a triangle, so the maximum number of segments is `0`.

### Example 2

Input:

```
5
```

Fan construction uses the diagonals `(1,3)` and `(1,4)`.

| Step | Diagonal Added | Count |
| --- | --- | --- |
| 1 | (1,3) | 1 |
| 2 | (1,4) | 2 |

The final count is `2`, which equals `5 - 3`.

This example shows that the construction reaches the theoretical maximum number of non-crossing diagonals.

### Example 3

Input:

```
7
```

Fan construction uses `(1,3)`, `(1,4)`, `(1,5)`, `(1,6)`.

| Step | Diagonal Added | Count |
| --- | --- | --- |
| 1 | (1,3) | 1 |
| 2 | (1,4) | 2 |
| 3 | (1,5) | 3 |
| 4 | (1,6) | 4 |

The answer is `4 = 7 - 3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only one subtraction is performed |
| Space | O(1) | No auxiliary storage |

Even with `10^4` test cases, the running time is negligible. The solution easily fits within all limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        ans.append(str(n - 3))

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided samples
assert run("2\n3\n5\n") == "0\n2", "sample 1"

# custom cases
assert run("1\n3\n") == "0", "minimum polygon"
assert run("1\n4\n") == "1", "single diagonal"
assert run("1\n7\n") == "4", "general case"
assert run("1\n100000\n") == "99997", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | `0` | Smallest valid polygon |
| `4` | `1` | Exactly one diagonal exists |
| `7` | `4` | General fan construction |
| `100000` | `99997` | Maximum constraint |

## Edge Cases

For the smallest polygon:

```
1
3
```

The algorithm computes `3 - 3 = 0`.

A triangle has no diagonals, so there is nothing to draw. The output is correct.

For a quadrilateral:

```
1
4
```

The algorithm computes `4 - 3 = 1`.

The only possible non-crossing diagonal count is one. The fan construction gives `(1,3)`, which satisfies the coprimality condition.

For a larger polygon such as:

```
1
6
```

The algorithm outputs `3`.

The fan consists of `(1,3)`, `(1,4)`, and `(1,5)`. All are valid because every number is coprime with `1`, and they do not cross because they share a common endpoint. No solution can exceed `6 - 3 = 3`, so the answer is optimal.
