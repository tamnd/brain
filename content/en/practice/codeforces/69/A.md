---
title: "CF 69A - Young Physicist"
description: "We are given several force vectors acting on a body in three-dimensional space. Each vector has three components: its effect along the x-axis, y-axis, and z-axis. A body is in equilibrium only if the total force acting on it is zero in every direction."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 69
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 63 (Div. 2)"
rating: 1000
weight: 69
solve_time_s: 103
verified: true
draft: false
---

[CF 69A - Young Physicist](https://codeforces.com/problemset/problem/69/A)

**Rating:** 1000  
**Tags:** implementation, math  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several force vectors acting on a body in three-dimensional space. Each vector has three components: its effect along the x-axis, y-axis, and z-axis.

A body is in equilibrium only if the total force acting on it is zero in every direction. That means:

- the sum of all x-components must be 0
- the sum of all y-components must be 0
- the sum of all z-components must be 0

The task is simply to read all vectors, add their coordinates independently, and check whether all three totals are zero. If they are, print `"YES"`. Otherwise, print `"NO"`.

The constraints are very small. At most 100 vectors are given, and each coordinate is between -100 and 100. Even an inefficient solution would easily fit inside the limits. The largest possible absolute sum along one axis is only 100 × 100 = 10000, so ordinary integer arithmetic is completely safe.

The main challenge is not performance, but translating the physics condition correctly into code. A common mistake is checking whether each vector individually equals `(0,0,0)`. That is not required. Nonzero vectors can cancel each other out.

For example:

```
2
1 2 3
-1 -2 -3
```

The correct output is:

```
YES
```

The total force is `(0,0,0)` even though neither vector is zero.

Another subtle case is when only one axis balances.

```
3
1 0 0
-1 5 0
0 -3 0
```

The x-axis sums to zero, but the y-axis sums to 2. The correct output is:

```
NO
```

A careless implementation that checks only one coordinate would fail here.

There is also the minimum-size case:

```
1
0 0 0
```

The correct output is:

```
YES
```

With only one vector, equilibrium happens only if that vector itself is zero.

## Approaches

The most direct approach is brute force. We can try to compute the total force by examining every vector and adding its coordinates into running sums. After processing all vectors, we check whether the final sums are all zero.

This already works efficiently because the input size is tiny. We perform exactly three additions per vector, so even in the worst case we do only around 300 arithmetic operations.

The key observation is that equilibrium depends only on the combined effect of all forces, not on their order or individual magnitudes. Vector addition is associative and commutative, so we never need to store the vectors after processing them. We only need three running totals.

That reduces the problem to maintaining:

```
sum_x
sum_y
sum_z
```

As we read each vector `(x, y, z)`, we update these totals. At the end:

- if all three sums are zero, the body is balanced
- otherwise, some net force remains, so the body will move

Even though the brute-force and optimal approaches look similar here, the important optimization is recognizing that we only need constant extra memory and a single pass through the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`, the number of force vectors.
2. Initialize three variables:

`sum_x = 0`, `sum_y = 0`, and `sum_z = 0`.

These variables represent the total force accumulated along each axis.
3. Repeat `n` times:

- Read one vector `(x, y, z)`.
- Add `x` to `sum_x`.
- Add `y` to `sum_y`.
- Add `z` to `sum_z`.

Each vector contributes independently to the net force along every axis.
4. After processing all vectors, check whether all three sums equal zero.

The body is in equilibrium only if there is no remaining force in any direction.
5. Print `"YES"` if all sums are zero. Otherwise print `"NO"`.

### Why it works

The algorithm maintains the invariant that after processing the first `i` vectors, the variables `sum_x`, `sum_y`, and `sum_z` equal the total force contributed by those `i` vectors along each axis.

Vector addition works component-wise, so the overall net force is:

$$\left(\sum x_i,\ \sum y_i,\ \sum z_i\right)$$

A body is in equilibrium exactly when this resulting vector equals `(0,0,0)`. Since the algorithm computes these sums correctly, the final check always produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

sum_x = 0
sum_y = 0
sum_z = 0

for _ in range(n):
    x, y, z = map(int, input().split())

    sum_x += x
    sum_y += y
    sum_z += z

if sum_x == 0 and sum_y == 0 and sum_z == 0:
    print("YES")
else:
    print("NO")
```

The program begins by reading the number of vectors. Three accumulator variables are initialized to track the total force along each axis.

Inside the loop, each vector is read and immediately added into the running totals. The vectors never need to be stored because only the cumulative sums matter.

The final condition checks all three coordinates simultaneously. This is important because equilibrium requires the entire vector sum to be zero, not just one coordinate.

Integer overflow is not a concern in Python, but even in fixed-width languages the limits are small enough to fit comfortably inside standard integer types.

The implementation also avoids unnecessary data structures. Using constant memory keeps the solution simple and directly aligned with the mathematical definition of equilibrium.

## Worked Examples

### Example 1

Input:

```
3
4 1 7
-2 4 -1
1 -5 -3
```

| Step | Vector | sum_x | sum_y | sum_z |
| --- | --- | --- | --- | --- |
| Start | - | 0 | 0 | 0 |
| 1 | (4, 1, 7) | 4 | 1 | 7 |
| 2 | (-2, 4, -1) | 2 | 5 | 6 |
| 3 | (1, -5, -3) | 3 | 0 | 3 |

Final vector sum is `(3,0,3)`, which is not zero. The body still experiences a net force, so the correct output is:

```
NO
```

This example demonstrates that even if one axis balances perfectly, the other axes must also balance.

### Example 2

Input:

```
3
3 -1 7
-5 2 -4
2 -1 -3
```

| Step | Vector | sum_x | sum_y | sum_z |
| --- | --- | --- | --- | --- |
| Start | - | 0 | 0 | 0 |
| 1 | (3, -1, 7) | 3 | -1 | 7 |
| 2 | (-5, 2, -4) | -2 | 1 | 3 |
| 3 | (2, -1, -3) | 0 | 0 | 0 |

All three totals become zero after processing every vector.

The correct output is:

```
YES
```

This trace confirms the invariant that the running sums always represent the net force from all vectors processed so far.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each vector is processed once |
| Space | O(1) | Only three accumulator variables are stored |

With at most 100 vectors, the program runs almost instantly. The memory usage is constant because the algorithm never stores the full list of vectors.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())

    sx = sy = sz = 0

    for _ in range(n):
        x, y, z = map(int, input().split())
        sx += x
        sy += y
        sz += z

    if sx == 0 and sy == 0 and sz == 0:
        print("YES")
    else:
        print("NO")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run(
"""3
4 1 7
-2 4 -1
1 -5 -3
"""
) == "NO\n", "sample 1"

# minimum-size equilibrium
assert run(
"""1
0 0 0
"""
) == "YES\n", "single zero vector"

# minimum-size non-equilibrium
assert run(
"""1
5 -3 2
"""
) == "NO\n", "single nonzero vector"

# vectors cancel each other
assert run(
"""2
1 2 3
-1 -2 -3
"""
) == "YES\n", "perfect cancellation"

# only one axis unbalanced
assert run(
"""3
1 0 0
-1 5 0
0 -3 0
"""
) == "NO\n", "y-axis remains nonzero"

# boundary values
assert run(
"""2
100 100 100
-100 -100 -100
"""
) == "YES\n", "boundary coordinate values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single `(0,0,0)` vector | YES | Minimum-size equilibrium case |
| Single nonzero vector | NO | Minimum-size non-equilibrium |
| Two opposite vectors | YES | Cancellation across all axes |
| One axis remains nonzero | NO | All three coordinates must balance |
| Boundary coordinate values | YES | Correct handling of extreme inputs |

## Edge Cases

Consider the case where vectors cancel each other even though none of them is zero.

Input:

```
2
1 2 3
-1 -2 -3
```

Execution trace:

- After first vector: `(1,2,3)`
- After second vector: `(0,0,0)`

The algorithm prints `"YES"` because the total force becomes zero. This confirms that equilibrium depends on the sum of vectors, not on individual vectors.

Now consider a case where only one coordinate remains nonzero.

Input:

```
3
1 0 0
-1 5 0
0 -3 0
```

Execution trace:

- After first vector: `(1,0,0)`
- After second vector: `(0,5,0)`
- After third vector: `(0,2,0)`

The x-axis balances, but the y-axis total is still `2`. The algorithm correctly prints `"NO"` because equilibrium requires every coordinate sum to be zero simultaneously.

Finally, consider the smallest valid input.

Input:

```
1
0 0 0
```

Execution trace:

- After processing the only vector: `(0,0,0)`

The algorithm prints `"YES"` immediately. This confirms correct handling of the lower constraint boundary.
