---
title: "CF 102263L - Burgers"
description: "The infinite board is periodic. Every (n times m) block contains the same values, so only the position inside one block matters. Let the zero-based local row and column be (x) and (y). The burger value at that position is [ f(x,y)=xm+y+1."
date: "2026-08-17T20:10:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102263
codeforces_index: "L"
codeforces_contest_name: "ArabellaCPC 2019"
rating: 0
weight: 102263
solve_time_s: 137
verified: true
draft: false
---

[CF 102263L - Burgers](https://codeforces.com/problemset/problem/102263/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

The infinite board is periodic. Every (n \times m) block contains the same values, so only the position inside one block matters. Let the zero-based local row and column be (x) and (y). The burger value at that position is

[
f(x,y)=xm+y+1.
]

After eating, the player moves by (r) rows and (c) columns. Since we only care about the position inside the repeated block, the sequence of states is

[
(x+kr)\bmod n,\qquad (y+kc)\bmod m.
]

The player stops immediately before eating a burger whose value has already appeared. Because every value from (1) through (nm) occurs at exactly one local position, two states have the same deliciousness exactly when both their row and column residues are equal. Thus the process stops when the pair of residues repeats.

For the row coordinate, the number of distinct positions visited is

[
p_n=\frac{n}{\gcd(n,r)}.
]

For the column coordinate it is

[
p_m=\frac{m}{\gcd(m,c)}.
]

The complete pair repeats after

[
L=\operatorname{lcm}(p_n,p_m)
]

moves. The player eats exactly (L) burgers.

The constraints are much too large for simulation. Both dimensions can reach (2\cdot10^9), so there can be up to (4\cdot10^{18}) positions in one period. The official problem limit is only 0.5 seconds, so even an (O(nm)) method is impossible, let alone iterating through a complete trajectory from every starting cell. The solution must reduce the trajectory to a few gcd, lcm, and arithmetic-sum computations.

There are several easy traps. For `1 1 1 1`, the only burger has value (1), the first burger is eaten and the next state has the same value, so the answer is `1`. A solution that assumes the player always eats at least two burgers would be off by one.

For `1 4 1 2`, the columns visited from any starting column have the same parity. The best trajectory visits columns with values (2) and (4), giving (2+4=6). A careless solution that assumes a step of (2) eventually visits all four columns would incorrectly use the sum (1+2+3+4=10). The correct sample output is `6`.

For `4 3 2 1`, the row step has (\gcd(4,2)=2), so only two rows belong to any row cycle. A solution that treats the row step as if it were coprime to (n) would include values from all four rows. The correct answer is `48`.

Finally, when (r=n) or (c=m), the corresponding coordinate does not change at all. For example, with `3 2 3 2`, the same cell is reached after every move, so the optimal starting cell is simply the bottom-right cell, whose value is (6). The answer is `6`.

## Approaches

The direct approach is to choose every possible starting position, simulate the jumps until a previously eaten value occurs, and keep the largest sum. For one starting position this takes (L) iterations, where

[
L=\operatorname{lcm}\left(\frac n{\gcd(n,r)},\frac m{\gcd(m,c)}\right).
]

There are (nm) possible local starting positions, so the brute-force operation count is

[
O(nmL).
]

In the worst case the two reduced periods can be coprime, giving (L) close to (nm). With both dimensions near (2\cdot10^9), this can approach ((nm)^2), around (1.6\cdot10^{37}) trajectory steps. The brute-force method is correct because it literally follows the process, but its dependence on the period makes it unusable.

The useful observation is that the row and column coordinates evolve independently. For one dimension of size (q) with step (d), let

[
g=\gcd(q,d),\qquad p=\frac qg.
]

Starting from a residue (s), the visited residues are exactly

[
s,\ s+g,\ s+2g,\ldots,s+(p-1)g
]

after reducing them modulo (q). In other words, a trajectory visits one complete residue class modulo (g). Every starting point with the same residue modulo (g) produces the same set of positions.

The sum of that residue class is

[
p s+g\frac{p(p-1)}2.
]

The coefficient of (s) is positive, so the largest sum comes from (s=g-1). Thus the maximum one-period sum for this dimension is

[
S(q,d)=p(g-1)+g\frac{p(p-1)}2.
]

The row and column cycles can have different periods, so a row cycle is repeated (L/p_n) times during the complete two-dimensional trajectory, and a column cycle is repeated (L/p_m) times.

The burger value is (xm+y+1), so the total contribution splits into a row part, a column part, and one constant (1) for every eaten burger. This separation lets us maximize the best row cycle and best column cycle independently. The corresponding starting row and starting column can simply be combined into one starting cell.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nmL)) | (O(1)) | Too slow |
| Optimal | (O(\log(\max(n,m)))) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Compute (g_n=\gcd(n,r)) and (p_n=n/g_n). The row coordinate returns to its starting value after exactly (p_n) jumps, because (p_n r) is the smallest positive multiple of (n).
2. Compute (g_m=\gcd(m,c)) and (p_m=m/g_m) in the same way for columns. The full local cell repeats after

[
L=\operatorname{lcm}(p_n,p_m).
]

This is the number of burgers eaten before the next burger would have a previously seen value.

1. For the row dimension, calculate

[
S_n=p_n(g_n-1)+g_n\frac{p_n(p_n-1)}2.
]

This is the maximum sum of the zero-based row indices during one row cycle. The best starting row belongs to the residue class (g_n-1\pmod {g_n}).

1. For the column dimension, calculate

[
S_m=p_m(g_m-1)+g_m\frac{p_m(p_m-1)}2.
]

This is the corresponding maximum sum of zero-based column indices during one column cycle.

1. A row cycle of length (p_n) occurs (L/p_n) times during the complete trajectory. Hence the total row-index sum is

[
S_n\frac{L}{p_n}.
]

Similarly, the total column-index sum is

[
S_m\frac{L}{p_m}.
]

1. Convert those coordinate sums into burger deliciousness. Every row index contributes a factor of (m), every column index contributes directly, and every eaten burger contributes (1). The answer is

[
mS_n\frac{L}{p_n}
+
S_m\frac{L}{p_m}
+
L.
]

Take this expression modulo (10^9+7).

Why it works: every trajectory is an orbit of the translation ((x,y)\mapsto(x+r,y+c)) on the finite torus (\mathbb Z_n\times\mathbb Z_m). Its length is (L), so exactly one complete orbit is eaten. In each coordinate, the orbit consists of one residue class modulo the corresponding gcd, and the maximum sum of such a class is obtained by choosing its largest residue. Since the burger value is the sum of an independent row term, an independent column term, and a constant, maximizing the two coordinate sums independently also maximizes the complete trajectory sum. The formula consequently evaluates the best possible starting cell.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

MOD = 10**9 + 7

def cycle_info(q, d):
    g = gcd(q, d)
    p = q // g

    # Maximum sum of residues in one cycle.
    # The best residue class starts at g - 1:
    # (g - 1), (2g - 1), ..., (pg - 1)
    s = p * (g - 1) + g * p * (p - 1) // 2
    return g, p, s

def solve():
    n, m, r, c = map(int, input().split())

    _, pn, row_sum = cycle_info(n, r)
    _, pm, col_sum = cycle_info(m, c)

    # lcm(pn, pm)
    L = pn // gcd(pn, pm) * pm

    row_repetitions = L // pn
    col_repetitions = L // pm

    answer = 0
    answer += (m % MOD) * (row_sum % MOD) % MOD
    answer %= MOD
    answer = answer * (row_repetitions % MOD) % MOD

    answer += (col_sum % MOD) * (col_repetitions % MOD) % MOD
    answer += L % MOD

    print(answer % MOD)

if __name__ == "__main__":
    solve()
```

The `cycle_info` function implements the one-dimensional mathematical reduction. `g` identifies which residue classes are preserved by the jump, while `p` is the number of positions in one such class. The arithmetic progression starts at (g-1) because that gives the largest possible sum.

The complete period is the lcm of the row and column periods. The expression `pn // gcd(pn, pm) * pm` computes it without constructing any trajectory.

The row contribution needs both the row-cycle sum and the number of times that cycle occurs inside the combined period. The factor `m` converts a zero-based row index into its contribution to the burger value. The column contribution needs no additional dimension factor.

Python integers have arbitrary precision, so the intermediate products are safe even though the complete period can be around (4\cdot10^{18}). The code still reduces products modulo (10^9+7) as it goes, which keeps the arithmetic compact and directly reflects the required output.

The use of zero-based coordinates is deliberate. With row (x) and column (y), the burger value is exactly (mx+y+1). Using one-based coordinates would require an additional adjustment in every arithmetic progression and is an easy source of off-by-one errors.

## Worked Examples

For Sample 1, the input is `3 3 1 1`. Both dimensions have gcd (1), so every coordinate is visited completely.

| Dimension | (g) | Period (p) | Best cycle sum | Repetitions |
| --- | --- | --- | --- | --- |
| Row | 1 | 3 | 3 | 1 |
| Column | 1 | 3 | 3 | 1 |

The complete period is (L=3). The row contribution is (3\cdot3=9), the column contribution is (3), and the constant contribution is (3). The total is (9+3+3=15), matching the sample.

For Sample 2, the input is `1 4 1 2`. The row dimension has only one position. For columns, (\gcd(4,2)=2), so each trajectory visits one of the two parity classes.

| Dimension | (g) | Period (p) | Best cycle sum | Repetitions |
| --- | --- | --- | --- | --- |
| Row | 1 | 1 | 0 | 2 |
| Column | 2 | 2 | 4 | 1 |

The complete period is (L=2). The best column class contains zero-based columns (1) and (3), corresponding to burger values (2) and (4). The answer is (0+4+2=6). This demonstrates why the gcd matters: the jump does not visit every column.

For Sample 3, the input is `2000000000 1 1 1`. The column contribution is zero because there is only one column. The row period is (2\cdot10^9), and the best row cycle contains every row. The answer is

[
\frac{2000000000\cdot1999999999}{2}+2000000000.
]

Modulo (10^9+7), this is `91`, as in the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\log(\max(n,m)))) | Two gcd computations and constant-time arithmetic |
| Space | (O(1)) | Only a fixed number of integer variables are stored |

The dimensions can be (2\cdot10^9), but the algorithm never iterates over rows, columns, cells, or trajectory positions. Euclid's algorithm finishes in logarithmic time, so the solution easily fits the 0.5 second limit and uses constant memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import gcd

MOD = 10**9 + 7

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        n, m, r, c = map(int, sys.stdin.readline().split())

        def cycle_sum(q, d):
            g = gcd(q, d)
            p = q // g
            s = p * (g - 1) + g * p * (p - 1) // 2
            return p, s

        pn, row_sum = cycle_sum(n, r)
        pm, col_sum = cycle_sum(m, c)

        L = pn // gcd(pn, pm) * pm

        ans = (
            (m % MOD) * (row_sum % MOD) % MOD
            * (L // pn)
            + (col_sum % MOD) * (L // pm)
            + L
        ) % MOD

        return str(ans)
    finally:
        sys.stdin = old_stdin
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

# Provided samples
assert solve_io("3 3 1 1\n") == "15", "sample 1"
assert solve_io("1 4 1 2\n") == "6", "sample 2"
assert solve_io("2000000000 1 1 1\n") == "91", "sample 3"

# Minimum size, only one burger and one-step repetition
assert solve_io("1 1 1 1\n") == "1", "minimum-size case"

# All burgers in the trajectory have the same local value
assert solve_io("1 2 1 2\n") == "2", "all-equal trajectory"

# Boundary case r = n and c = m, so the same cell is reached immediately
assert solve_io("3 2 3 2\n") == "6", "zero movement modulo dimensions"

# Partial gcd cycles in both dimensions
assert solve_io("4 3 2 1\n") == "48", "non-coprime row step"

# Maximum-size dimensions
assert solve_io("2000000000 2000000000 1 1\n") == "999998628", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `1` | Minimum dimensions and period one |
| `1 2 1 2` | `2` | A coordinate whose jump is exactly its dimension |
| `3 2 3 2` | `6` | Both jumps equal their corresponding dimensions |
| `4 3 2 1` | `48` | Non-coprime row step and repeated row cycles |
| `2000000000 2000000000 1 1` | `999998628` | Maximum dimensions and large modular arithmetic |

## Edge Cases

For `1 1 1 1`, we have (g_n=g_m=1), (p_n=p_m=1), and (L=1). The row and column sums are both zero because their zero-based coordinates are always zero. The formula gives (0+0+1=1), so exactly one burger is eaten.

For `1 4 1 2`, the column gcd is (2), giving (p_m=2). The best residue class is (1\pmod2), containing zero-based columns (1) and (3). Their sum is (4), and the trajectory has length (2). The result is (4+2=6). The algorithm never assumes that a non-coprime step visits the whole dimension.

For `3 2 3 2`, both jumps are equal to their dimensions. We get (p_n=p_m=1), hence (L=1). The best row residue is (2), the best column residue is (1), and the only eaten burger has value (2\cdot2+1+1=6). The next position has exactly the same deliciousness, so the player wakes immediately. The formula produces (6).

For `4 3 2 1`, the row cycle has (g_n=2) and (p_n=2). Its best zero-based rows are (1) and (3), whose sum is (4). The complete period is (L=\operatorname{lcm}(2,3)=6), so each row position occurs three times and each column position occurs twice. The row contribution is (3\cdot4\cdot3=36), the column contribution is (3\cdot2=6), and the constant contribution is (6). The final answer is (36+6+6=48).

For `2000000000 2000000000 1 1`, both dimensions have period (2\cdot10^9), so the complete trajectory contains (2\cdot10^9) burgers. The one-dimensional maximum sum is (2000000000\cdot1999999999/2) for each coordinate. The calculation is performed using modular multiplication, so no iteration over the enormous trajectory is necessary, and the final result is `999998628`.
