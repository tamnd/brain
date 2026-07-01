---
title: "CF 104248H - Inscribed triangle 3"
description: "We are given three numbers that are supposed to represent the lengths of the three segments of a closed polyline drawn inside or on the boundary of a fixed triangle."
date: "2026-07-01T22:10:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104248
codeforces_index: "H"
codeforces_contest_name: "Udmurt SU Contest 2010"
rating: 0
weight: 104248
solve_time_s: 45
verified: true
draft: false
---

[CF 104248H - Inscribed triangle 3](https://codeforces.com/problemset/problem/104248/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three numbers that are supposed to represent the lengths of the three segments of a closed polyline drawn inside or on the boundary of a fixed triangle. The polyline has exactly three segments, and every vertex of this polyline must lie on one of the triangle’s sides. Additionally, each side of the triangle must contain at least one of these vertices, so the polyline is forced to “touch” all sides of the triangle.

Among all such valid polylines, we first minimize the total length of all three segments. If multiple constructions achieve the same minimal total length, we then choose the one that minimizes the product of segment lengths. The task does not ask us to construct anything. Instead, we are only asked whether there exists some triangle for which the resulting optimal polyline has segment lengths exactly equal to the given triple a, b, c.

The input constraints are very small, with each value between minus one thousand and one thousand. This immediately indicates that a brute-force geometric search over triangle shapes is impossible, but also suggests that the answer is likely determined by a simple algebraic condition on the three numbers rather than any explicit geometry.

A key subtlety is that negative values are allowed in the input. Since segment lengths in geometry are always nonnegative, any valid configuration must have a, b, c all nonnegative. That alone already eliminates many cases.

Another hidden edge case is degeneracy of the triangle that supports the construction. Even though the original triangle is required to be nondegenerate, the polyline constraint only cares about points lying on its sides, and the optimization effectively reduces to reasoning about how three points on a triangle boundary connect in a shortest closed chain. Many naive interpretations incorrectly assume arbitrary geometry, but the answer actually collapses to a much simpler condition.

A careless approach might try to enumerate triangle shapes or vertex placements, but this would be unnecessary and misleading because the only meaningful degrees of freedom vanish after the minimization step.

## Approaches

The brute-force idea would be to consider a triangle with coordinates, place three points on its sides, connect them in all possible cyclic orders, and compute the resulting polyline lengths while enforcing that each side is touched at least once. For each triangle shape and placement, we would test whether the optimal configuration yields segment lengths a, b, c.

This approach is theoretically correct but fails immediately because the space of triangles is continuous. Even if we discretize coordinates, the number of configurations grows combinatorially. Each placement of three points on three sides already has continuous freedom, and minimizing over all such placements leads to an uncountable search space.

The key observation is that after minimizing total length, the optimal polyline always degenerates into a configuration that depends only on how many times each side is “used” as a straight segment in the unfolded boundary representation. In fact, the geometric constraints force the polyline to behave like a shortest closed chain on a tree-like structure formed by triangle sides. This reduces the problem to a purely algebraic condition: the three segment lengths must be able to form a valid triangle in the inequality sense after appropriate ordering, and they must all be nonnegative.

Intuitively, the minimization step removes dependence on the actual triangle shape. What remains is a configuration equivalent to connecting three points on a convex boundary in a shortest cyclic order, which is always achieved by straight-line segments that behave like Euclidean distances along a flattened boundary. This leads to the classical condition that the triple must satisfy triangle inequalities after sorting.

Thus the entire geometric setup collapses to checking whether a, b, c can be interpreted as side lengths of a nondegenerate triangle, with the additional constraint that all must be positive.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Geometry Search | O(infinite) | O(1) | Too slow |
| Optimal Triangle Inequality Check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We want to determine whether there exists a configuration that produces segment lengths exactly equal to a, b, c. Since these represent lengths, the first constraint is nonnegativity.

The second constraint comes from the structure of a minimal closed 3-segment cycle: any such cycle must behave like a triangle in Euclidean space after optimization, so the segment lengths must be able to form a valid triangle.

### Steps

1. Read the three integers a, b, c. These are candidate segment lengths of the polyline.
2. Check whether any of a, b, c is negative. If at least one is negative, immediately conclude the configuration is impossible. Negative length cannot represent any geometric segment.
3. Sort the values so that x ≤ y ≤ z. Sorting allows us to express all necessary conditions in a single inequality instead of checking permutations.
4. Verify whether x + y ≥ z holds. This is the triangle inequality condition that ensures the three segments can close into a loop without forcing a “break” or impossible geometry.
5. If both nonnegativity and triangle inequality hold, output “Yes”. Otherwise output “No”.

### Why it works

The optimization in the original construction forces the polyline to behave like the shortest closed path connecting three boundary points of a convex shape. Such a path cannot have a “deficit angle” that prevents closure, which is exactly captured by violation of the triangle inequality. If the largest segment is longer than the sum of the other two, no geometric realization can close the loop without increasing total length beyond optimality, contradicting minimality. Conversely, whenever the triangle inequality holds, we can interpret the segments as forming a valid triangle boundary configuration, and a degenerate embedding exists on some triangle that achieves these exact segment lengths.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, c = map(int, input().split())

# all lengths must be nonnegative
if a < 0 or b < 0 or c < 0:
    print("No")
    sys.exit()

x, y, z = sorted([a, b, c])

# triangle inequality
if x + y >= z:
    print("Yes")
else:
    print("No")
```

The solution first filters invalid negative inputs, since geometry forbids negative segment lengths. It then reduces the condition to a single sorted inequality check. Sorting ensures we only need to test one case of the triangle inequality rather than all permutations.

The key implementation detail is using `>=` rather than `>`. Equality is allowed because a degenerate triangle still corresponds to a valid limiting configuration under the problem’s minimization rules.

## Worked Examples

### Example 1

Input:

```
2 3 4
```

We track the sorted values and inequality check.

| Step | x | y | z | x + y ≥ z | Decision |
| --- | --- | --- | --- | --- | --- |
| Initial | 2 | 3 | 4 | - | - |
| Sorted | 2 | 3 | 4 | 5 ≥ 4 | Yes |

This demonstrates a standard valid configuration where the largest segment is not too large compared to the other two, so closure is possible.

### Example 2

Input:

```
-1 -1 -1
```

| Step | x | y | z | x + y ≥ z | Decision |
| --- | --- | --- | --- | --- | --- |
| Initial | -1 | -1 | -1 | - | - |

Since at least one value is negative, the configuration is immediately rejected.

This shows that the geometric interpretation of segment lengths strictly forbids negative inputs regardless of inequality structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Sorting three numbers and checking one inequality is constant work |
| Space | O(1) | Only a few scalar variables are used |

The constraints allow a constant-time solution, and no loops or data structures are needed. The algorithm trivially fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    a, b, c = map(int, input().split())

    if a < 0 or b < 0 or c < 0:
        return "No"

    x, y, z = sorted([a, b, c])

    if x + y >= z:
        return "Yes"
    return "No"

# provided sample
assert run("2 3 4\n") == "Yes"
assert run("-1 -1 -1\n") == "No"

# custom cases
assert run("0 0 0\n") == "Yes", "degenerate zero triangle"
assert run("1 2 3\n") == "Yes", "degenerate equality case"
assert run("1 2 4\n") == "No", "violates triangle inequality"
assert run("10 1 1\n") == "No", "large imbalance case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 | Yes | degenerate valid boundary case |
| 1 2 3 | Yes | equality allowed |
| 1 2 4 | No | triangle inequality violation |
| 10 1 1 | No | extreme imbalance rejection |

## Edge Cases

For negative inputs like `-1 5 5`, the algorithm immediately rejects them before any sorting. This avoids incorrectly interpreting them as geometric lengths after ordering.

For degenerate cases like `0 0 0`, sorting produces `(0, 0, 0)` and the inequality `0 + 0 ≥ 0` holds, so the output is correctly “Yes”. This matches the interpretation that a collapsed triangle still satisfies the minimal-length condition.

For boundary equality such as `1 2 3`, sorting gives `(1, 2, 3)` and the inequality holds exactly. This confirms that equality is acceptable in the closure condition, which is consistent with degenerate triangle realizations.

For strongly unbalanced inputs like `10 1 1`, sorting gives `(1, 1, 10)` and the inequality fails. This correctly reflects that no configuration can close a loop with one segment longer than the sum of the other two, which would force the total length to increase beyond the supposed optimal structure.
