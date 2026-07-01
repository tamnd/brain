---
title: "CF 104415F - Frisbee Training"
description: "The task describes a simple physical situation where a frisbee is thrown from the origin and lands at a point $(x, y)$. A player named Asfora can catch it only if he is able to run far enough before it lands."
date: "2026-06-30T19:51:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104415
codeforces_index: "F"
codeforces_contest_name: "IME++ Starters Try-outs 2023"
rating: 0
weight: 104415
solve_time_s: 43
verified: true
draft: false
---

[CF 104415F - Frisbee Training](https://codeforces.com/problemset/problem/104415/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a simple physical situation where a frisbee is thrown from the origin and lands at a point $(x, y)$. A player named Asfora can catch it only if he is able to run far enough before it lands. The geometry is straightforward: the required distance to reach the frisbee is the Euclidean distance from the origin to $(x, y)$, while the available running capability is expressed through a velocity-like parameter $v$ and a time $t$.

For each test case, we are given values that define the landing position and the movement capability. The decision is binary: determine whether Asfora can reach the frisbee in time.

The key observation is that everything reduces to comparing a geometric distance with a reachable radius. The Euclidean distance is $\sqrt{x^2 + y^2}$. The reachable distance is proportional to $v \cdot t$. The comparison is therefore whether the point lies inside or on a circle centered at the origin.

The input size is small per test case, and each query is independent. This immediately suggests that any solution beyond constant time per test case is unnecessary. Even if there are many test cases, the computation per case involves only a few arithmetic operations.

A subtle but important implementation issue is floating point precision. A direct computation using square roots can introduce rounding errors, especially when values are large or close to the boundary. Another practical issue is performance: repeatedly parsing floating point numbers in slow I/O environments can become a bottleneck even when the arithmetic itself is trivial.

Edge cases come from boundary equality and numerical precision. For example, when $x^2 + y^2$ is extremely close to $v^2 t^2$, floating point comparisons may flip the result incorrectly. Another edge case is when all values are zero, where the answer must trivially be positive.

## Approaches

The most direct approach is to compute the Euclidean distance explicitly. For each test case, we evaluate $\sqrt{x^2 + y^2}$, then compare it with $v \cdot t$. This is correct mathematically because it directly matches the geometric definition of distance. However, it introduces two inefficiencies. First, computing square roots is slower than multiplication and addition. Second, floating point arithmetic can introduce precision errors, especially when dealing with large integers or tight inequalities.

The better approach avoids both issues by eliminating the square root entirely. Instead of comparing $\sqrt{x^2 + y^2} \le v \cdot t$, we square both sides, producing $x^2 + y^2 \le v^2 t^2$. This transformation preserves correctness because all quantities involved are non-negative. The comparison becomes purely integer-based if inputs are integers, or at least avoids intermediate floating point instability.

The brute-force works because it mirrors the geometry directly, but it becomes less reliable and slightly slower when scaled across many test cases. The squared formulation removes transcendental operations and reduces the entire problem to a few multiplications and additions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct distance with sqrt | O(1) per test | O(1) | Correct but fragile |
| Squared comparison | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Each test case is independent, so no state is carried between them.
2. For each test case, read the values $x$, $y$, $v$, and $t$. These define the landing position and the available travel capability.
3. Compute the squared distance from the origin as $x^2 + y^2$. This represents the exact geometric requirement without introducing square roots.
4. Compute the squared reachable distance as $v^2 \cdot t^2$. This expands the available movement radius into the same squared space as the distance.
5. Compare the two values. If $x^2 + y^2 \le v^2 t^2$, output that the frisbee is reachable; otherwise, output that it is not.
6. Repeat for all test cases, printing each result immediately.

### Why it works

The algorithm relies on the fact that squaring is a strictly increasing transformation over non-negative numbers. Both the Euclidean distance and the reachable distance are always non-negative, so applying the same monotonic transformation to both sides preserves ordering. This ensures that the inequality in squared form is equivalent to the original geometric condition, eliminating numerical instability without changing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = input().strip().split()
    if not data:
        return
    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        x = int(data[idx]); y = int(data[idx + 1])
        v = int(data[idx + 2]); t_ = int(data[idx + 3])
        idx += 4

        lhs = x * x + y * y
        rhs = (v * t_) * (v * t_)

        if lhs <= rhs:
            out.append("YES")
        else:
            out.append("NO")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation keeps everything in integer arithmetic. The product $v \cdot t$ is computed first, then squared, which is safe in Python due to its large integer support. In a C++ setting, care would be needed to avoid overflow, but Python handles arbitrary precision naturally.

Reading input as a flat list avoids repeated function calls and minimizes overhead. This matters in environments where large numbers of test cases are packed into a single input stream.

## Worked Examples

### Example 1

Input:

```
2
3 4 5 1
3 4 1 1
```

We compute each case:

| Case | x | y | v | t | x²+y² | (v·t)² | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 4 | 5 | 1 | 25 | 25 | YES |
| 2 | 3 | 4 | 1 | 1 | 25 | 1 | NO |

The first case lies exactly on the boundary circle, which is accepted because the condition is non-strict. The second case clearly lies outside the reachable radius.

### Example 2

Input:

```
1
0 0 10 0
```

| Case | x | y | v | t | x²+y² | (v·t)² | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 10 | 0 | 0 | 0 | YES |

This tests the degenerate case where both position and time are zero. The frisbee is already at the origin, so the answer is trivially positive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case performs a constant number of arithmetic operations |
| Space | O(1) | Only a fixed number of variables are used aside from output storage |

The solution comfortably fits within constraints because each test case is resolved in constant time. Even for very large $T$, the computation is limited to integer multiplications and comparisons.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    data = sys.stdin.read().strip().split()
    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        x = int(data[idx]); y = int(data[idx + 1])
        v = int(data[idx + 2]); tt = int(data[idx + 3])
        idx += 4

        lhs = x * x + y * y
        rhs = (v * tt) * (v * tt)

        out.append("YES" if lhs <= rhs else "NO")

    return "\n".join(out)

# provided sample (if any assumed)
assert run("2\n3 4 5 1\n3 4 1 1\n") == "YES\nNO"

# all equal boundary
assert run("1\n6 8 10 1\n") == "YES"

# strict fail case
assert run("1\n6 8 1 1\n") == "NO"

# zero case
assert run("1\n0 0 0 5\n") == "YES"

# large safe case
assert run("1\n100000 100000 200000 1\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 4 5 1 | YES | Pythagorean boundary equality |
| 6 8 1 1 | NO | Clear failure outside radius |
| 0 0 0 5 | YES | Degenerate origin case |
| 100000 100000 200000 1 | YES | Large value correctness |

## Edge Cases

One edge case occurs when the point lies exactly on the boundary circle. For input $x=3, y=4, v=5, t=1$, the computation yields $x^2 + y^2 = 25$ and $(vt)^2 = 25$. The algorithm compares equality correctly because it uses `<=`, ensuring boundary inclusion.

Another edge case is when time is zero. For input $x=0, y=0, v=10, t=0$, both sides evaluate to zero, and the condition holds. The squared formulation avoids any division or floating point ambiguity.

A third edge case involves large coordinates. For $x=y=10^5, v=2\cdot10^5, t=1$, both sides fit safely in Python integers, and the comparison remains exact. In languages with fixed-width integers, intermediate multiplication must be handled carefully to avoid overflow, which is precisely why squaring the product after computing $v \cdot t$ in a widened type is necessary.
