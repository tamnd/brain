---
title: "CF 106153C - \u742a\u9732\u8bfa\u653e\u51b0\u5757"
description: "We are given a rectangular board of size $n times m$. We also have rectangular blocks of size $a times b$. The task is to determine how many such blocks can be placed on the board if they are aligned to the grid and cannot overlap, and crucially, they cannot be rotated."
date: "2026-06-19T19:20:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106153
codeforces_index: "C"
codeforces_contest_name: "HNNU Freshman Competition Round 2"
rating: 0
weight: 106153
solve_time_s: 54
verified: true
draft: false
---

[CF 106153C - \u742a\u9732\u8bfa\u653e\u51b0\u5757](https://codeforces.com/problemset/problem/106153/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular board of size $n \times m$. We also have rectangular blocks of size $a \times b$. The task is to determine how many such blocks can be placed on the board if they are aligned to the grid and cannot overlap, and crucially, they cannot be rotated.

The interpretation is straightforward: we tile the board starting from the top-left corner, placing each block in a fixed orientation of width $a$ and height $b$. The question reduces to how many full blocks fit along the vertical dimension and how many fit along the horizontal dimension, and then combining these two counts.

The input consists of multiple test cases, each giving four integers representing the board dimensions and the block dimensions. For each test case, we output a single integer representing the maximum number of blocks that fit.

The constraints are small enough that each test case must be handled in constant time. Even if there are up to $10^5$ test cases, any solution that does more than a few arithmetic operations per case would be too slow. This immediately rules out any simulation over the grid or any attempt to place blocks one by one.

A subtle mistake people sometimes make in this type of problem is assuming rotation is allowed. If rotation were allowed, we would need to consider both $(a, b)$ and $(b, a)$ placements and take the better result. Another mistake is trying to account for partial overlaps or greedy packing strategies, which are unnecessary here because the grid structure makes the solution purely arithmetic.

An edge case worth highlighting is when either $a > n$ or $b > m$. In that case, no block fits at all, and the answer should be zero. For example, if $n = 3, m = 3, a = 5, b = 1$, then no vertical placement is possible, so the output must be $0$, even though horizontal space exists.

## Approaches

The most direct way to think about the problem is to simulate placing blocks. We could iterate over all possible top-left positions in the grid and check whether a block fits. This would involve checking up to $n \cdot m$ positions per test case, and each check would involve constant-time validation. This leads to $O(nm)$ per test case, which is already unnecessary but still conceptually manageable.

However, this simulation ignores the structure of the problem. Once we observe that blocks are fixed rectangles aligned to the grid, we see that placement is independent along rows and columns. Along the vertical direction, we can only fit $\lfloor n / a \rfloor$ full blocks stacked. Along the horizontal direction, we can only fit $\lfloor m / b \rfloor$ blocks side by side. Every valid placement in one direction combines independently with placements in the other direction, so the total count is their product.

This reduces the problem from a geometric packing task into two integer divisions and a multiplication. The key structural insight is that because there is no rotation and no partial placement allowed, the grid decomposes into independent strips.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force placement simulation | $O(nm)$ per test case | $O(1)$ | Too slow |
| Direct arithmetic decomposition | $O(1)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Each test case is independent, so we can process them separately without storing any state.
2. For each test case, read four integers $n, m, a, b$, representing the board dimensions and block dimensions. The goal is to compute how many full $a \times b$ rectangles fit into the $n \times m$ rectangle.
3. Compute how many blocks fit vertically using integer division $n // a$. This represents how many full rows of height $a$ can be stacked without exceeding the board height.
4. Compute how many blocks fit horizontally using integer division $m // b$. This represents how many full columns of width $b$ can be placed across the board.
5. Multiply these two values to obtain the total number of blocks. This works because every vertical slot can independently combine with every horizontal slot to form a valid placement region.
6. Output the result for the test case.

### Why it works

The crucial property is separability of dimensions. Since every block must occupy a contiguous $a \times b$ region and cannot rotate, every valid placement corresponds uniquely to choosing a vertical index among $\lfloor n / a \rfloor$ possibilities and a horizontal index among $\lfloor m / b \rfloor$ possibilities. There is no interaction between these choices, and no leftover region can partially contribute to another block. This creates a Cartesian product structure of valid placements, which guarantees the correctness of multiplying the two integer quotients.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, a, b = map(int, input().split())
    print((n // a) * (m // b))

t = int(input())
for _ in range(t):
    solve()
```

The solution reads each test case and directly applies integer division to compute how many full segments fit in each dimension. The multiplication step is safe because the values involved are small enough to fit comfortably within Python integers.

A common pitfall is forgetting integer division and using floating-point division, which would introduce precision issues. Another mistake is attempting to round up instead of down; only full blocks count, so floor division is essential.

The order of operations does not matter here because multiplication is commutative, but keeping the structure as two separate divisions improves clarity and reduces the risk of mixing dimensions.

## Worked Examples

### Example 1

Input:

```
1
6 8 2 3
```

| Step | Vertical (n//a) | Horizontal (m//b) | Result |
| --- | --- | --- | --- |
| Start | 6 | 8 | - |
| After vertical division | 3 | 8 | - |
| After horizontal division | 3 | 2 | - |
| Final | 3 | 2 | 6 |

Here, the board can be split into 3 full rows of height 2, and each row contains 2 full columns of width 3. The product gives 6 blocks.

This demonstrates how the decomposition into independent dimensions naturally forms a grid of valid placements.

### Example 2

Input:

```
1
5 5 6 2
```

| Step | Vertical (n//a) | Horizontal (m//b) | Result |
| --- | --- | --- | --- |
| Start | 5 | 5 | - |
| After vertical division | 0 | 5 | - |
| After horizontal division | 0 | 2 | - |
| Final | 0 | 2 | 0 |

Since the block height exceeds the board height, no vertical placement is possible. Even though horizontal space exists, it does not matter, and the final answer is zero.

This confirms the correct handling of infeasible dimensions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case requires a constant number of arithmetic operations |
| Space | $O(1)$ | No additional data structures are used beyond input variables |

The solution comfortably fits within typical limits for competitive programming, even when the number of test cases is large, since each case is solved in constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        n, m, a, b = map(int, input().split())
        return (n // a) * (m // b)

    t = int(input())
    out = []
    for _ in range(t):
        out.append(str(solve()))
    return "\n".join(out)

# provided sample-style tests
assert run("1\n6 8 2 3\n") == "6"
assert run("1\n5 5 6 2\n") == "0"

# custom cases
assert run("1\n1 1 1 1\n") == "1", "minimum valid case"
assert run("1\n10 10 3 3\n") == "9", "perfect tiling"
assert run("1\n9 9 10 2\n") == "0", "height too large"
assert run("1\n7 5 2 3\n") == "3", "mixed leftover space"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 with 1×1 block | 1 | minimal valid tiling |
| 10×10 with 3×3 block | 9 | clean full grid packing |
| 9×9 with 10×2 block | 0 | block larger than board dimension |
| 7×5 with 2×3 block | 3 | partial remainders do not count |

## Edge Cases

When $a > n$, the vertical quotient becomes zero immediately, and the algorithm outputs zero regardless of width. For example, input `n=4, m=10, a=5, b=2` produces `(4//5)*(10//2) = 0*5 = 0`, matching the fact that no block can be placed.

When $b > m$, the same symmetry applies horizontally. Even if vertical stacking is possible, the lack of horizontal fit forces the result to zero.

When both dimensions divide evenly, such as `n=8, m=6, a=2, b=3`, the computation becomes `(8//2)*(6//3) = 4*2 = 8`, which corresponds exactly to a full grid partition with no leftover space.
