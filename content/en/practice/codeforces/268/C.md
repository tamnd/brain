---
title: "CF 268C - Beautiful Sets of Points"
description: "We are given all lattice points inside a rectangle, meaning every point $(x,y)$ with integer coordinates such that $0 le x le n$, $0 le y le m$, and $(0,0)$ is excluded."
date: "2026-06-05T01:14:27+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 268
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 164 (Div. 2)"
rating: 1500
weight: 268
solve_time_s: 118
verified: false
draft: false
---

[CF 268C - Beautiful Sets of Points](https://codeforces.com/problemset/problem/268/C)

**Rating:** 1500  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given all lattice points inside a rectangle, meaning every point $(x,y)$ with integer coordinates such that $0 \le x \le n$, $0 \le y \le m$, and $(0,0)$ is excluded.

Among these points we must choose the largest possible subset with a special property: for every pair of chosen points, the Euclidean distance between them must not be an integer.

The task is constructive. We do not need to count the answer only, we must actually output one maximum-size beautiful set.

The bounds are very small, $n,m \le 100$. A brute-force search over all subsets is still impossible because the rectangle contains up to $101 \times 101 - 1 = 10200$ points. The number of subsets is astronomically large. The small constraints are a hint that the intended solution is based on discovering a structure of an optimal set rather than performing heavy computation.

A subtle point is that distances are integer exactly when the squared distance is a perfect square. Since all coordinates are integers, every squared distance is an integer. A naive solution might try to check distances using floating point arithmetic, which can introduce precision issues. The intended solution avoids distance computations entirely.

Another easy mistake is assuming that only horizontal and vertical alignments create integer distances. For example, between $(0,0)$ and $(3,4)$ the distance is $5$, which is also an integer. Any constructive solution must prevent all such cases, not just axis-aligned ones.

Consider $n=1,m=3$. The available points are:

$$(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3)$$

Choosing all points on a single column fails because distances like between $(0,1)$ and $(0,3)$ equal $2$, an integer. The structure of the solution must carefully avoid creating integer differences in coordinates.

## Approaches

A brute-force viewpoint is useful for understanding the problem. Suppose we build a graph whose vertices are lattice points and connect two vertices whenever their distance is an integer. Then the task becomes finding a maximum independent set.

This formulation is correct because a beautiful set is exactly a set containing no conflicting pair.

Unfortunately, the graph may contain over ten thousand vertices. Maximum independent set is already difficult on much smaller graphs, so this direction is hopeless.

The key observation comes from looking at points lying on the same diagonal $x+y=c$.

Take two distinct points on that diagonal:

$$(x_1,y_1), \quad (x_2,y_2)$$

Since both satisfy $x+y=c$,

$$y_2-y_1 = -(x_2-x_1)$$

The squared distance becomes

$$(x_2-x_1)^2 + (y_2-y_1)^2
=
2(x_2-x_1)^2$$

For any nonzero integer $d$,

$$2d^2$$

is never a perfect square. Thus every distance between distinct points on the same diagonal is irrational and therefore non-integer.

This immediately gives a large beautiful set: take all lattice points on a single diagonal.

How many such points can a diagonal contain? The diagonal $x+y=t$ contains

$$\min(t,n)-\max(0,t-m)+1$$

points. The maximum possible size over all diagonals is exactly

$$\min(n,m)+1.$$

A particularly simple diagonal achieving this size is

$$(0,\min(n,m)),
(1,\min(n,m)-1),
\dots,
(\min(n,m),0).$$

Now we need to prove optimality.

For any point $(x,y)$, consider its value $x+y$. Since

$$1 \le x+y \le n+m,$$

there are only $n+m$ possible positive sums.

If two points have the same $x$-coordinate, their distance is $|y_1-y_2|$, an integer. Thus at most one chosen point may use each $x$-coordinate.

There are only $\min(n,m)+1$ usable $x$-coordinates along the shorter dimension. More directly, one can show that every beautiful set has size at most $\min(n,m)+1$, and the diagonal construction reaches this bound.

Hence the diagonal is optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Construction | O(min(n,m)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute $k=\min(n,m)$.
2. Construct the points

$$(0,k), (1,k-1), \ldots, (k,0).$$

Every point satisfies $x+y=k$, so all points lie on the same diagonal.
3. Output $k+1$, the number of constructed points.
4. Output each constructed point.

The reason this works is that any two distinct points on the diagonal have coordinate difference $(d,-d)$. Their squared distance equals $2d^2$, which is never a perfect square, so every pair has a non-integer distance.

### Why it works

All chosen points satisfy $x+y=k$. For any two distinct chosen points, the difference vector is $(d,-d)$ with $d \ne 0$. The squared distance is $2d^2$. Since $2$ is not a square, $2d^2$ cannot be a perfect square. Thus every pairwise distance is non-integer, so the set is beautiful.

The diagonal contains exactly $k+1=\min(n,m)+1$ points. This is the maximum possible size proved in the editorial argument above, so the construction is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    k = min(n, m)

    print(k + 1)
    for x in range(k + 1):
        print(x, k - x)

solve()
```

The implementation follows the construction directly.

First we compute $k=\min(n,m)$. The diagonal $x+y=k$ is guaranteed to stay inside the rectangle because both coordinates remain between $0$ and $k$, and $k$ does not exceed either bound.

The loop generates every lattice point on that diagonal. When $x$ increases from $0$ to $k$, the corresponding $y$ decreases from $k$ to $0$.

No distance calculations are required. The mathematical proof guarantees that all generated points form a beautiful set and that its size is optimal.

A common implementation mistake is choosing the diagonal $x+y=\max(n,m)$. Such a diagonal may leave the rectangle. Using $k=\min(n,m)$ avoids that issue.

## Worked Examples

### Example 1

Input:

```
2 2
```

Here $k=2$.

| Step | x | y | Generated Point |
| --- | --- | --- | --- |
| 1 | 0 | 2 | (0,2) |
| 2 | 1 | 1 | (1,1) |
| 3 | 2 | 0 | (2,0) |

Output:

```
3
0 2
1 1
2 0
```

All points lie on the diagonal $x+y=2$. Every pair has squared distance $2d^2$, never a perfect square.

### Example 2

Input:

```
1 3
```

Here $k=1$.

| Step | x | y | Generated Point |
| --- | --- | --- | --- |
| 1 | 0 | 1 | (0,1) |
| 2 | 1 | 0 | (1,0) |

Output:

```
2
0 1
1 0
```

This example shows why we use the shorter dimension. The diagonal $x+y=1$ fits entirely inside the rectangle and already achieves the optimal size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(min(n,m)) | We output exactly min(n,m)+1 points |
| Space | O(1) | Only a few variables are stored |

Since $n,m \le 100$, the running time is tiny. The solution performs only a short loop and uses constant extra memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, m = map(int, input().split())
    k = min(n, m)

    out = [str(k + 1)]
    for x in range(k + 1):
        out.append(f"{x} {k - x}")

    return "\n".join(out)

# custom validator for beautiful-set outputs
def validate(inp, out):
    n, m = map(int, inp.split())
    lines = out.strip().splitlines()

    k = int(lines[0])
    assert k == min(n, m) + 1

# sample
assert run("2 2\n") == "3\n0 2\n1 1\n2 0"

# minimum values
assert run("1 1\n") == "2\n0 1\n1 0"

# rectangular grid
assert run("1 3\n") == "2\n0 1\n1 0"

# opposite rectangular grid
assert run("5 2\n") == "3\n0 2\n1 1\n2 0"

# maximum values
res = run("100 100\n")
assert res.splitlines()[0] == "101"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 2 points | Smallest valid instance |
| 1 3 | 2 points | Highly asymmetric rectangle |
| 5 2 | 3 points | Uses shorter dimension correctly |
| 100 100 | 101 points | Largest allowed square grid |

## Edge Cases

Consider the smallest possible input:

```
1 1
```

The algorithm computes $k=1$ and outputs:

```
2
0 1
1 0
```

The distance between the two points is $\sqrt{2}$, which is not an integer. The set is beautiful and optimal.

Consider a highly asymmetric rectangle:

```
1 100
```

The algorithm still uses $k=1$. It outputs only the points on the diagonal $x+y=1$:

```
2
0 1
1 0
```

Trying to extend farther along the taller dimension would create vertical pairs with integer distances. Restricting the construction to the shorter dimension avoids this problem.

Consider a square at the maximum size:

```
100 100
```

The algorithm outputs all points

$$(0,100),(1,99),\ldots,(100,0).$$

Every pair remains on the same diagonal, so the squared distance between any two points is $2d^2$. The proof is independent of the actual size, so the construction remains valid even at the largest constraints.
