---
title: "CF 1809B - Points on Plane"
description: "We want to place n chips on integer lattice points of the plane. The cost of a chip at (x, y) is its Manhattan distance from the origin, The chips must satisfy one geometric restriction: every pair of chips must be more than 1 unit apart in Euclidean distance."
date: "2026-06-09T08:50:45+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1809
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 145 (Rated for Div. 2)"
rating: 1000
weight: 1809
solve_time_s: 83
verified: true
draft: false
---

[CF 1809B - Points on Plane](https://codeforces.com/problemset/problem/1809/B)

**Rating:** 1000  
**Tags:** binary search, greedy, math  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We want to place `n` chips on integer lattice points of the plane. The cost of a chip at `(x, y)` is its Manhattan distance from the origin, `|x| + |y|`. The cost of the whole arrangement is the largest chip cost among all placed chips.

The chips must satisfy one geometric restriction: every pair of chips must be more than `1` unit apart in Euclidean distance.

The task is to find the smallest possible maximum cost that allows placing exactly `n` chips.

The input contains up to `10^4` test cases, and each `n` can be as large as `10^18`. Such a huge value immediately rules out any approach that explicitly constructs points or iterates up to `n`. Even an `O(√n)` algorithm would be too slow for the largest inputs. We need something around `O(log n)` per test case.

The key challenge is understanding how many lattice points can fit inside a given cost limit.

A subtle edge case is `n = 1`.

Input:

```
1
1
```

Output:

```
0
```

One chip can be placed at the origin, so the answer is `0`. A solution that assumes the minimum cost is at least `1` would fail.

Another important boundary is when `n` is exactly a perfect square.

Input:

```
1
9
```

Output:

```
3
```

The answer is not `2`, because a cost limit of `2` contains only `3² = 9` valid positions? This observation is actually the entire solution. Getting the counting formula wrong by one causes incorrect answers around perfect squares.

A final source of bugs is handling values near `10^18`.

Input:

```
1
1000000000000000000
```

The answer is `1000000000`. Any implementation using floating-point square roots risks precision errors near this range. Integer arithmetic is safer.

## Approaches

A brute-force mindset starts by fixing some maximum allowed cost `k` and counting how many lattice points satisfy `|x| + |y| ≤ k`. The set forms a diamond around the origin.

Without considering the distance restriction, the number of lattice points in that diamond is

$$1 + 2k(k+1).$$

One could then try increasing `k` until enough points exist.

The problem is that the distance restriction changes everything. Two neighboring lattice points such as `(0,0)` and `(1,0)` are exactly distance `1` apart, which is forbidden. We cannot use all points in the diamond.

The crucial observation is that the distance condition becomes very simple on the integer grid. Since coordinates are integers, the only way for two distinct lattice points to have distance at most `1` is if they differ by exactly one unit horizontally or vertically.

That suggests selecting points of only one parity. Consider all lattice points where `x + y` is even. Any two such points differ by an even value in `x + y`, so they can never be horizontal or vertical neighbors. Their Euclidean distance is always greater than `1`.

Now look at the diamond `|x| + |y| ≤ k`. Among its lattice points, exactly

$$(k+1)^2$$

have even parity.

Even better, this is optimal. The lattice graph formed by horizontal and vertical adjacencies is bipartite, split by parity. Every admissible set is an independent set in this graph, and one parity class already achieves the maximum possible size.

So with cost limit `k`, we can place exactly `(k+1)^2` chips.

The problem is now reduced to finding the smallest `k` such that

$$(k+1)^2 \ge n.$$

Since `n` can be as large as `10^{18}`, we can solve this with binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k²) or worse | O(1) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For a candidate cost limit `k`, compute how many chips can be placed:

$$(k+1)^2$$

This comes from taking all lattice points of one parity inside the diamond.
2. Observe that larger `k` always allows at least as many chips as smaller `k`.

The function `(k+1)^2` is monotonic, which makes binary search applicable.
3. Binary search the smallest `k` such that:

$$(k+1)^2 \ge n$$
4. Initialize `low = 0` and `high = 10^9`.

Since `n ≤ 10^{18}`, the answer never exceeds `10^9 - 1`.
5. During the search, let `mid = (low + high) // 2`.
6. If `(mid + 1)^2 ≥ n`, keep the left half by setting `high = mid`.

This means `mid` is already sufficient, but there may be a smaller valid answer.
7. Otherwise set `low = mid + 1`.

This means `mid` cannot accommodate enough chips.
8. When `low == high`, output that value.

### Why it works

For every cost limit `k`, the largest valid set of lattice points inside `|x| + |y| ≤ k` has size `(k+1)^2`. One parity class achieves this size, and no larger independent set exists because the lattice adjacency graph inside the diamond is bipartite, with the larger side containing exactly `(k+1)^2` vertices.

Thus a cost limit `k` is feasible if and only if `(k+1)^2 ≥ n`. Binary search finds the smallest feasible `k`, which is exactly the minimum possible cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())

    lo, hi = 0, 10**9

    while lo < hi:
        mid = (lo + hi) // 2

        if (mid + 1) * (mid + 1) >= n:
            hi = mid
        else:
            lo = mid + 1

    print(lo)
```

The solution revolves around the monotonic predicate

$$(k+1)^2 \ge n.$$

For any fixed `k`, this tells us whether the diamond of radius `k` can contain enough valid chip positions.

The binary search maintains the invariant that the answer always lies inside `[lo, hi]`. Whenever `mid` is feasible, we keep searching to the left because we want the minimum cost. Whenever `mid` is infeasible, every smaller value is also infeasible, so we move right.

All arithmetic is performed using integers. This avoids precision issues that can appear when using floating-point square roots near `10^18`.

The upper bound `10^9` is sufficient because

$$(10^9)^2 = 10^{18}.$$

So an answer larger than `10^9` is never needed.

## Worked Examples

### Example 1

Input:

```
n = 5
```

| Step | lo | hi | mid | (mid+1)² | Feasible? |
| --- | --- | --- | --- | --- | --- |
| Initial | 0 | 1000000000 | 500000000 | huge | Yes |
| ... | ... | ... | ... | ... | ... |
| Near end | 0 | 3 | 1 | 4 | No |
| Next | 2 | 3 | 2 | 9 | Yes |
| Final | 2 | 2 | - | - | Answer |

Output:

```
2
```

A cost limit of `1` allows only `4` chips, while a cost limit of `2` allows `9`. The minimum feasible value is `2`.

### Example 2

Input:

```
n = 975461057789971042
```

| Step | lo | hi | mid | Check |
| --- | --- | --- | --- | --- |
| Initial | 0 | 1000000000 | 500000000 | Too small |
| ... | ... | ... | ... | ... |
| Final | 987654321 | 987654321 | - | Answer |

Output:

```
987654321
```

Indeed,

$$(987654321+1)^2
=
987654322^2
=
975461057789971684$$

which is at least `975461057789971042`, while one less cost is insufficient.

This trace demonstrates that the method handles values close to `10^18` entirely with integer arithmetic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Binary search on the answer |
| Space | O(1) | Only a few integer variables are stored |

Since `log2(10^18)` is about `60`, each test case performs only a small number of iterations. With at most `10^4` test cases, the total work easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())

        lo, hi = 0, 10**9

        while lo < hi:
            mid = (lo + hi) // 2

            if (mid + 1) * (mid + 1) >= n:
                hi = mid
            else:
                lo = mid + 1

        ans.append(str(lo))

    print("\n".join(ans))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out.getvalue()

# provided sample
assert run(
"""4
1
3
5
975461057789971042
"""
) == """0
1
2
987654321
"""

# minimum size
assert run(
"""1
1
"""
) == """0
"""

# perfect square boundary
assert run(
"""1
9
"""
) == """2
"""

# just above perfect square
assert run(
"""1
10
"""
) == """3
"""

# maximum value
assert run(
"""1
1000000000000000000
"""
) == """999999999
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n = 1` | `0` | Smallest possible answer |
| `n = 9` | `2` | Exact perfect-square boundary |
| `n = 10` | `3` | Off-by-one after a boundary |
| `n = 10^18` | `999999999` | Largest input size |

## Edge Cases

Consider the smallest input:

```
1
1
```

The search checks whether `(k+1)^2 ≥ 1`. Already at `k = 0`, the condition holds because `1² = 1`. The algorithm returns `0`, corresponding to placing the chip at `(0,0)`.

Now consider a perfect square:

```
1
9
```

The algorithm searches for the smallest `k` with `(k+1)^2 ≥ 9`. For `k = 1`, we get `4`, which is insufficient. For `k = 2`, we get `9`, which is exactly enough. The answer is `2`. This confirms that equality must be treated as feasible.

Finally, consider:

```
1
10
```

For `k = 2`, we still have only `9` available positions. The next value gives `(3+1)^2 = 16`, making `k = 3` the answer. This is the classic off-by-one case that catches incorrect binary-search conditions.

For the maximum range:

```
1
1000000000000000000
```

The condition becomes `(k+1)^2 ≥ 10^18`. The smallest valid value is `k = 999999999`, since `(10^9)^2 = 10^18`. Integer arithmetic handles this safely, avoiding any floating-point rounding issues.
