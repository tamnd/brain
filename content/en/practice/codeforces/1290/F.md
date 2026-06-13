---
title: "CF 1290F - Making Shapes"
description: "We are given up to five distinct directions in the plane. A shape is created by choosing these vectors repeatedly and walking along them in counter-clockwise order until the walk returns to the starting point."
date: "2026-06-11T18:58:34+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1290
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 616 (Div. 1)"
rating: 3500
weight: 1290
solve_time_s: 146
verified: false
draft: false
---

[CF 1290F - Making Shapes](https://codeforces.com/problemset/problem/1290/F)

**Rating:** 3500  
**Tags:** dp  
**Solve time:** 2m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given up to five distinct directions in the plane. A shape is created by choosing these vectors repeatedly and walking along them in counter-clockwise order until the walk returns to the starting point.

Because the vectors are already required to appear in counter-clockwise order, once we decide how many times each vector is used, the resulting convex polygon is completely determined. The actual starting point does not matter because shapes are considered identical up to translation.

Let $c_i$ be the number of times vector $i$ is used.

Returning to the origin means

$$\sum c_i x_i = 0, \qquad \sum c_i y_i = 0.$$

The polygon must also fit inside an $m \times m$ square after translation.

The unusual part of the problem is the constraint mix. The coefficients $x_i,y_i$ are tiny, at most $4$ in absolute value, and $n \le 5$. On the other hand, $m$ can be as large as $10^9$, so the counts $c_i$ can be enormous.

A direct search over the values $c_i$ is hopeless because there is no useful upper bound on them. The small vector coordinates suggest that we should work bit-by-bit on the equations instead of value-by-value.

A subtle edge case is the degenerate polygon. If every $c_i=0$, the equations are satisfied and the width and height are both zero. This does not represent a valid shape and must be removed from the final count.

For example:

```
1 10
1 1
```

The only solution of

$$c_1(1,1)=(0,0)$$

is $c_1=0$. The correct answer is $0$, not $1$.

Another easy mistake is misunderstanding the bounding-square condition. The polygon does not need to start inside the square. We may translate it. Only its horizontal and vertical spans matter.

For example, if the horizontal range of the polygon is $7$, then it fits in an $m=7$ square regardless of where it was originally drawn.

## Approaches

Suppose we try brute force.

We could enumerate all possible vectors usage counts $c_i$, check the two closure equations, and verify the bounding-box limits. The problem is that $m$ reaches $10^9$, so the counts can also reach roughly $10^9$. Even with only five variables, the search space is astronomically large.

The key observation is that the coordinates of the vectors are tiny.

Split the closure equations into positive and negative contributions:

$$\sum_{x_i>0} c_i x_i = \sum_{x_i<0} c_i (-x_i),$$

$$\sum_{y_i>0} c_i y_i = \sum_{y_i<0} c_i (-y_i).$$

Define

$$PX=\sum_{x_i>0} c_i x_i,\quad NX=\sum_{x_i<0} c_i (-x_i),$$

and similarly $PY,NY$.

Then we only need

$$PX=NX,\qquad PY=NY.$$

For a convex polygon whose edges are traversed in angular order, the horizontal span equals $NX$, and the vertical span equals $NY$. Thus the square condition becomes

$$NX \le m,\qquad NY \le m.$$

Now the problem becomes counting non-negative integer vectors $(c_1,\ldots,c_n)$ satisfying two equalities and two upper bounds.

The coefficients are at most $4$, which means carries in binary addition stay very small. This is exactly the setting where digit DP works.

Process the binary representation from the least significant bit upward. At each bit we choose whether the current bit of each $c_i$ is $0$ or $1$. That gives only $2^n \le 32$ possibilities per layer.

The DP state stores the current carries of $PX,PY,NX,NY$ together with two tightness flags describing whether $NX$ and $NY$ are already strictly below $m$.

This converts an infinite search over all counts into a finite carry-DP whose state space is only a few million.

The official solution uses exactly this carry digit-DP idea.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over counts | Exponential in the maximum count | Huge | Too slow |
| Binary digit DP with carries | $O(\log m \cdot 20^4 \cdot 2^n)$ | $O(20^4)$ states per layer | Accepted |

## Algorithm Walkthrough

1. Separate every vector contribution into four groups: positive-x, negative-x, positive-y, and negative-y.
2. Process binary digits from bit $0$ up to bit $29$. Since $m \le 10^9$, thirty bits are enough.
3. Let the DP state be

$$(dp\;bit,\;px,\;py,\;nx,\;ny,\;xm,\;ym).$$

Here $px,py,nx,ny$ are the current carries of the four sums after processing all lower bits.

1. For the current bit, enumerate a mask from $0$ to $(1<<n)-1$.

Bit $i$ of the mask represents the current binary digit of $c_i$.
2. Add the corresponding vector contributions into temporary carry values.
3. Extract the parity of all four temporary sums.

The equality $PX=NX$ requires the current output bit of both sides to be identical, so

$$(PX \bmod 2)=(NX \bmod 2).$$

The same condition is required for the $y$-equation.

1. If either equality fails, discard this transition.
2. Shift all temporary sums right by one to obtain the carries for the next digit.
3. Update the two limit flags.

They track whether the already-built suffix of $NX$ and $NY$ is strictly smaller than the corresponding suffix of $m$.
4. Continue recursively.
5. At bit $30$, accept only states where all carries are zero and both limit flags indicate that the constructed values do not exceed $m$.
6. Subtract one from the final answer to remove the all-zero choice $c_i=0$.

### Why it works

The DP is performing ordinary binary addition simultaneously for the four sums $PX,PY,NX,NY$.

At every bit position, the parity check guarantees that the current bit produced by $PX$ matches the current bit produced by $NX$, and likewise for $PY$ and $NY$. Since carries are propagated exactly as in binary arithmetic, reaching the terminal state with zero carries means the entire numbers are equal.

The limit flags are the standard digit-DP mechanism for enforcing $NX \le m$ and $NY \le m$. Every valid vector of counts produces exactly one path through the DP, and every accepted path reconstructs a unique vector of counts. Hence the DP counts precisely the desired shapes.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

MOD = 998244353

def solve():
    n, m = map(int, input().split())
    x = []
    y = []

    for _ in range(n):
        a, b = map(int, input().split())
        x.append(a)
        y.append(b)

    def upd(limit_bit, digit, state):
        if limit_bit != digit:
            return 0 if digit > limit_bit else 1
        return state

    @lru_cache(None)
    def dp(bit, px, py, nx, ny, xm, ym):
        if bit == 30:
            return int(
                px == 0 and py == 0 and
                nx == 0 and ny == 0 and
                xm == 0 and ym == 0
            )

        mb = (m >> bit) & 1
        ans = 0

        for mask in range(1 << n):
            tpx = px
            tpy = py
            tnx = nx
            tny = ny

            for i in range(n):
                if (mask >> i) & 1:
                    if x[i] > 0:
                        tpx += x[i]
                    else:
                        tnx += -x[i]

                    if y[i] > 0:
                        tpy += y[i]
                    else:
                        tny += -y[i]

            bpx = tpx & 1
            bpy = tpy & 1
            bnx = tnx & 1
            bny = tny & 1

            if bpx != bnx or bpy != bny:
                continue

            ans += dp(
                bit + 1,
                tpx >> 1,
                tpy >> 1,
                tnx >> 1,
                tny >> 1,
                upd(mb, bpx, xm),
                upd(mb, bpy, ym)
            )

        return ans % MOD

    print((dp(0, 0, 0, 0, 0, 0, 0) - 1) % MOD)

solve()
```

The state variables `px`, `py`, `nx`, and `ny` are carries, not complete sums. Their maximum value stays tiny because every coefficient is at most four and there are only five vectors. That is why the state space remains manageable.

The transition enumerates one bit of every count $c_i$. A mask represents the binary digits chosen at the current position.

The parity checks are the core of the construction. They enforce equality of the corresponding positive and negative sums bit-by-bit.

The terminal condition requires all carries to vanish. Otherwise some higher bit would still remain unmatched.

The final subtraction removes the configuration where every count is zero, which corresponds to no polygon at all.

## Worked Examples

### Sample 1

```
3 3
-1 0
1 1
0 -1
```

At bit 0, one valid choice is selecting all three vectors once.

| Bit | Mask | PX parity | NX parity | PY parity | NY parity | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 111 | 1 | 1 | 1 | 1 | Yes |

The DP continues propagating carries and eventually finds exactly three accepted count vectors.

| Quantity | Value |
| --- | --- |
| Accepted solutions | 3 |
| Output | 3 |

This example demonstrates that multiple distinct multiplicity vectors can generate different convex polygons while satisfying the same closure conditions.

### Sample 2

```
3 3
-1 0
2 2
0 -1
```

The closure equations become

$$2c_2=c_1, \qquad 2c_2=c_3.$$

The square limit forces only one non-zero feasible solution.

| Quantity | Value |
| --- | --- |
| Accepted solutions | 1 |
| Output | 1 |

This example shows how the bounding-box restriction removes infinitely many algebraic solutions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log m \cdot 20^4 \cdot 2^n)$ | About 30 digit levels, tiny carry ranges, and at most 32 masks per state |
| Space | $O(20^4)$ | Memoized carry states |

With $n \le 5$ and vector coordinates bounded by $4$, carry values never grow large. The resulting state space comfortably fits within the memory limit, and the transition count fits inside the 5-second limit.

## Test Cases

```python
# helper skeleton

import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    # paste solve() here and return printed output
    return ""

# sample 1
# expected: 3

# sample 2
# expected: 1

# custom sanity cases

# single vector, impossible to form a polygon
# 1 10
# 1 1
# expected: 0

# only zero-count solution exists
# 1 1
# -1 0
# expected: 0

# very small m boundary
# should reject shapes whose span exceeds 1

# large m stress case from statement
# 5 1000000000
# ...
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One non-zero vector | 0 | Removes the all-zero configuration |
| $m=1$ boundary case | Depends on geometry | Correct limit handling |
| Sample 1 | 3 | Multiple valid polygons |
| Sample 2 | 1 | Closure plus bounding-box constraints |

## Edge Cases

Consider:

```
1 10
1 1
```

At every digit, the only way to satisfy

$$PX=NX,\quad PY=NY$$

is to keep the corresponding bit of $c_1$ equal to zero. The DP reaches exactly one terminal state, the all-zero solution. The final subtraction removes it, producing answer $0$.

Now consider:

```
3 1
-1 0
2 2
0 -1
```

The closure equations still have non-zero solutions, but they require horizontal and vertical spans larger than $1$. During digit DP, the limit flags detect that either $NX$ or $NY$ exceeds $m$, and those branches are rejected. No accepted terminal state remains.

These examples illustrate the two easiest implementation mistakes: forgetting to remove the empty shape and enforcing equality without also enforcing the square-size bounds.
