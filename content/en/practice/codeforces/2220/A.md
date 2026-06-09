---
title: "CF 2220A - Blocked"
description: "We are given two nonnegative integers (x) and (y). We must construct two new nonnegative integers (p) and (q) such that no bit is set in both numbers simultaneously, that is, [ p ,&, q = 0."
date: "2026-06-09T04:58:25+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2220
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1093 (Div. 2)"
rating: 0
weight: 2220
solve_time_s: 164
verified: false
draft: false
---

[CF 2220A - Blocked](https://codeforces.com/problemset/problem/2220/A)

**Rating:** -  
**Tags:** greedy, sortings  
**Solve time:** 2m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two nonnegative integers \(x\) and \(y\). We must construct two new nonnegative integers \(p\) and \(q\) such that no bit is set in both numbers simultaneously, that is,

$$
p \,\&\, q = 0.
$$

Among all such pairs, we want to minimize

$$
|x-p| + |y-q|.
$$

The output is not the minimum value itself. We must output one optimal pair \((p,q)\).

The numbers are smaller than \(2^{30}\), but there are up to \(10^4\) test cases. Any approach that searches over candidate values of \(p\) or \(q\) is immediately impossible. Even exploring all values within a small neighborhood of \(x\) and \(y\) would not work.

The condition \(p \,\&\, q = 0\) is bitwise. The objective function is numeric. This combination is a strong signal that the solution should process bits from most significant to least significant while tracking how the constructed numbers compare to \(x\) and \(y\).

A subtle edge case occurs when both \(x\) and \(y\) contain the same high bit. For example:

```
x = 4
y = 4
```

The pair \((4,4)\) is forbidden because \(4 \& 4 = 4\). A greedy strategy that keeps every matching bit would fail. One optimal answer is \((4,3)\), with cost \(1\).

Another tricky case is

```
x = 1
y = 1
```

The best answer is not \((1,0)\) or \((0,1)\), both of which have cost \(1\). The sample outputs \((2,1)\), which also has cost \(1\). Optimal solutions are not unique, so the algorithm must optimize the cost, not attempt to reproduce a specific answer.

## Approaches

A brute force search would enumerate all pairs \((p,q)\) satisfying \(p \& q = 0\), compute

$$
|x-p| + |y-q|,
$$

and keep the best one.

Even if we restricted ourselves to numbers below \(2^{31}\), there would be roughly \(2^{62}\) candidate pairs. This is completely infeasible.

The key observation is that both the constraint and the objective can be handled bit by bit.

Suppose we are constructing \(p\) and \(q\) from the most significant bit downward. At any point, only three comparison states are possible for \(p\) relative to \(x\):

$$
p < x,\quad p = x,\quad p > x.
$$

The same is true for \(q\) relative to \(y\).

Therefore the entire future only depends on two ternary states, giving

$$
3 \times 3 = 9
$$

possible comparison states.

Once the relation between \(p\) and \(x\) has already been determined, lower bits contribute linearly to \(|p-x|\). The same holds for \(q\) and \(y\). This allows a digit-DP style solution over binary digits.

We process bits from 30 down to 0. At each bit we choose one of the three allowed assignments:

$$
(p_b,q_b)\in\{(0,0),(0,1),(1,0)\},
$$

because \((1,1)\) would violate \(p \& q = 0\).

The DP keeps the minimum possible cost for every comparison state and stores transitions for reconstruction.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---:|---:|---|
| Brute Force | \(O(2^{62})\) | \(O(1)\) | Too slow |
| Bit DP | \(O(31 \cdot 9 \cdot 3)\) | \(O(31 \cdot 9)\) | Accepted |

## Algorithm Walkthrough

1. Process bits from 30 down to 0.

2. Maintain a state \((s_x,s_y)\), where each component belongs to \(\{-1,0,1\}\).

   Here

   $$
   s_x =
   \begin{cases}
   -1 & p < x,\\
   0 & p = x,\\
   1 & p > x,
   \end{cases}
   $$

   considering only the already processed higher bits.

   The definition of \(s_y\) is analogous.

3. For each state, try the three valid bit assignments

   $$
   (0,0),\ (0,1),\ (1,0).
   $$

4. Update the comparison state for \(p\) versus \(x\).

   If \(s_x=0\), the current bit may establish the relation for the first time.

   If \(s_x\neq0\), the relation never changes again.

5. Add the contribution of the current bit to \(|p-x|\).

   Let

   $$
   d_x = p_b - x_b.
   $$

   If \(s_x=1\), the sign of \(p-x\) is already known to be positive, so this bit contributes

   $$
   d_x \cdot 2^b.
   $$

   If \(s_x=-1\), it contributes

   $$
   -d_x \cdot 2^b.
   $$

   If \(s_x=0\), then a first difference contributes exactly

   $$
   2^b.
   $$

6. Do the same for \(q\) versus \(y\).

7. Keep the transition yielding the minimum cost.

8. After the last bit, choose the state with minimum total cost and reconstruct \(p\) and \(q\) from the stored parents.

### Why it works

The most significant bit where \(p\) and \(x\) differ determines whether \(p>x\) or \(p<x\). Once that bit is fixed, every lower bit contributes with a known sign to the absolute difference. The DP state stores exactly this sign information.

Since every valid assignment of bits corresponds to a unique path through the DP, and every path accumulates precisely the value

$$
|p-x|+|y-q|,
$$

the DP examines all feasible pairs \((p,q)\) satisfying \(p\&q=0\) and selects one with minimum cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

BITS = 31
INF = 10**18

def solve_case(x, y):
    dp = [[INF] * 9 for _ in range(BITS + 1)]
    parent = [[None] * 9 for _ in range(BITS + 1)]

    start = 4  # (sx, sy) = (0, 0)
    dp[0][start] = 0

    def idx(sx, sy):
        return (sx + 1) * 3 + (sy + 1)

    def decode(v):
        return v // 3 - 1, v % 3 - 1

    for pos in range(BITS):
        b = 30 - pos
        w = 1 << b

        xb = (x >> b) & 1
        yb = (y >> b) & 1

        for st in range(9):
            cur = dp[pos][st]
            if cur == INF:
                continue

            sx, sy = decode(st)

            for pb, qb in ((0, 0), (0, 1), (1, 0)):
                # x side
                dx = pb - xb

                if sx == 0:
                    if dx == 0:
                        nsx = 0
                        addx = 0
                    elif dx > 0:
                        nsx = 1
                        addx = w
                    else:
                        nsx = -1
                        addx = w
                elif sx == 1:
                    nsx = 1
                    addx = dx * w
                else:
                    nsx = -1
                    addx = -dx * w

                # y side
                dy = qb - yb

                if sy == 0:
                    if dy == 0:
                        nsy = 0
                        addy = 0
                    elif dy > 0:
                        nsy = 1
                        addy = w
                    else:
                        nsy = -1
                        addy = w
                elif sy == 1:
                    nsy = 1
                    addy = dy * w
                else:
                    nsy = -1
                    addy = -dy * w

                nst = idx(nsx, nsy)
                nv = cur + addx + addy

                if nv < dp[pos + 1][nst]:
                    dp[pos + 1][nst] = nv
                    parent[pos + 1][nst] = (st, pb, qb)

    best_state = min(range(9), key=lambda s: dp[BITS][s])

    p = 0
    q = 0
    st = best_state

    for pos in range(BITS, 0, -1):
        prev, pb, qb = parent[pos][st]
        b = 30 - (pos - 1)

        p |= pb << b
        q |= qb << b

        st = prev

    return p, q

def main():
    t = int(input())
    ans = []

    for _ in range(t):
        x, y = map(int, input().split())
        p, q = solve_case(x, y)
        ans.append(f"{p} {q}")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()
```

The DP table contains 31 layers, one per bit position. Each layer has only 9 states. For every state we try exactly three transitions because the pair \((1,1)\) is forbidden.

The contribution formulas are the subtle part. When the comparison state is already known, lower bits affect the signed difference directly. When the current bit creates the first difference, that bit contributes exactly its weight because it becomes the leading differing bit.

The reconstruction phase walks backward through the stored parents and rebuilds the chosen bits of \(p\) and \(q\).

## Worked Examples

### Example 1

Input:

```
x = 4
y = 4
```

Binary representations:

$$
x=y=100_2.
$$

At bit 2, choosing \((1,1)\) is forbidden.

| Bit | x bit | y bit | Chosen (p,q) bit |
|---|---:|---:|---:|
| 2 | 1 | 1 | (1,0) |
| 1 | 0 | 0 | (0,1) |
| 0 | 0 | 0 | (0,1) |

This reconstructs

$$
p=100_2=4,\qquad q=011_2=3.
$$

The cost is

$$
|4-4|+|4-3|=1.
$$

The example shows how a shared high bit is split between the two numbers.

### Example 2

Input:

```
x = 3
y = 6
```

Binary:

$$
x=011_2,\qquad y=110_2.
$$

One optimal reconstruction is:

| Bit | x bit | y bit | Chosen (p,q) bit |
|---|---:|---:|---:|
| 2 | 0 | 1 | (0,1) |
| 1 | 1 | 1 | (1,0) |
| 0 | 1 | 0 | (1,0) |

This yields

$$
p=3,\qquad q=4.
$$

The cost is

$$
|3-3|+|6-4|=2.
$$

The sample output uses \(q=8\), which has the same optimal cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---:|---|
| Time | \(O(31 \cdot 9 \cdot 3)\) | 31 bits, 9 states, 3 transitions |
| Space | \(O(31 \cdot 9)\) | DP and parent tables |

The total work per test case is only a few hundred operations. With \(10^4\) test cases, the solution easily fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    BITS = 31
    INF = 10**18

    def solve_case(x, y):
        dp = [[INF] * 9 for _ in range(BITS + 1)]
        parent = [[None] * 9 for _ in range(BITS + 1)]

        dp[0][4] = 0

        def idx(sx, sy):
            return (sx + 1) * 3 + (sy + 1)

        def decode(v):
            return v // 3 - 1, v % 3 - 1

        for pos in range(BITS):
            b = 30 - pos
            w = 1 << b

            xb = (x >> b) & 1
            yb = (y >> b) & 1

            for st in range(9):
                cur = dp[pos][st]
                if cur == INF:
                    continue

                sx, sy = decode(st)

                for pb, qb in ((0, 0), (0, 1), (1, 0)):
                    dx = pb - xb
                    dy = qb - yb

                    if sx == 0:
                        if dx == 0:
                            nsx, addx = 0, 0
                        elif dx > 0:
                            nsx, addx = 1, w
                        else:
                            nsx, addx = -1, w
                    elif sx == 1:
                        nsx, addx = 1, dx * w
                    else:
                        nsx, addx = -1, -dx * w

                    if sy == 0:
                        if dy == 0:
                            nsy, addy = 0, 0
                        elif dy > 0:
                            nsy, addy = 1, w
                        else:
                            nsy, addy = -1, w
                    elif sy == 1:
                        nsy, addy = 1, dy * w
                    else:
                        nsy, addy = -1, -dy * w

                    nst = idx(nsx, nsy)
                    nv = cur + addx + addy

                    if nv < dp[pos + 1][nst]:
                        dp[pos + 1][nst] = nv
                        parent[pos + 1][nst] = (st, pb, qb)

        best = min(range(9), key=lambda s: dp[BITS][s])

        p = q = 0
        st = best

        for pos in range(BITS, 0, -1):
            prev, pb, qb = parent[pos][st]
            b = 30 - (pos - 1)
            p |= pb << b
            q |= qb << b
            st = prev

        return f"{p} {q}"

    t = int(input())
    return "\n".join(
        solve_case(*map(int, input().split()))
        for _ in range(t)
    )

# sample input, output may differ because multiple answers exist

# minimum values
out = run("1\n0 0\n")
p, q = map(int, out.split())
assert (p & q) == 0

# equal numbers
out = run("1\n4 4\n")
p, q = map(int, out.split())
assert (p & q) == 0

# boundary
out = run("1\n1073741823 1073741822\n")
p, q = map(int, out.split())
assert (p & q) == 0

# asymmetric
out = run("1\n0 123456\n")
p, q = map(int, out.split())
assert (p & q) == 0
```

| Test input | Expected output | What it validates |
|---|---|---|
| `0 0` | Any valid optimal pair | Smallest possible values |
| `4 4` | Any optimal pair with AND zero | Shared highest bit |
| `1073741823 1073741822` | Any optimal pair | Largest inputs |
| `0 123456` | Any optimal pair | One number already zero |

## Edge Cases

When both numbers are zero, the DP remains in the equality state for every bit and reconstructs \((0,0)\). The cost is zero, which is clearly optimal.

When both numbers share a large bit, such as

```
4 4
```

the bit assignment \((1,1)\) is forbidden. The DP evaluates both possibilities, giving the bit to \(p\) or giving it to \(q\), then optimally adjusts lower bits. This avoids the common mistake of keeping both numbers unchanged.

For

```
1073741823 1073741822
```

every bit below bit 30 is active in at least one number. A local greedy choice can easily create a larger error later. The DP keeps all comparison states simultaneously, so it never commits to a suboptimal high-bit decision.
