---
title: "CF 102437A - \u0411\u043b\u044d\u043a \\& \u0423\u0430\u0439\u0442"
description: "There are (n) cities arranged around a circle and one capital in the middle. The only possible roads are the (n) circular roads between consecutive outer cities and the (n) spokes from the capital to the outer cities. Some roads may be absent."
date: "2026-08-09T00:18:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102437
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102437
solve_time_s: 334
verified: true
draft: false
---

[CF 102437A - \u0411\u043b\u044d\u043a \\& \u0423\u0430\u0439\u0442](https://codeforces.com/problemset/problem/102437/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (n) cities arranged around a circle and one capital in the middle. The only possible roads are the (n) circular roads between consecutive outer cities and the (n) spokes from the capital to the outer cities. Some roads may be absent. Every existing road is controlled either by White or by Black.

We need to count spanning trees of this graph according to how many White-controlled roads they contain. If a tree has exactly (k) White roads, it contributes to the coefficient (a_k). Since a spanning tree on (n+1) vertices always has exactly (n) edges, (k) ranges from (0) to (n).

The useful way to think about the input is as two cyclic arrays. The string (s) describes the circular edges, where (s_i) is the edge from city (i) to city (i+1), with (n+1) interpreted as city (1). The string (t) describes the spokes, where (t_i) is the edge from the capital to city (i). A character `W` gives that edge weight (x), a character `B` gives it weight (1), and `-` gives it weight (0).

Then the required answer is simply the coefficient sequence of the spanning-tree generating polynomial

[
F(x)=\sum_T x^{#W(T)}.
]

The constraint (n\le 50000) rules out anything quadratic in (n). Even an (O(n^2)) dynamic program would require around (2.5\cdot 10^9) basic operations at the upper bound. The answer itself has (n+1) coefficients, so an (O(n\log^2 n)) or similar polynomial-time approach is appropriate. The modulus (998244353) is particularly convenient because it supports efficient NTT polynomial multiplication.

There are several boundary cases where a superficially correct counting argument fails. If every spoke is absent, for example

```
3
WWW
---
```

the circular cities form a cycle but the capital is isolated, so there are no spanning trees and the answer is `0 0 0 0`. A method that counts forests on the outer cycle without explicitly enforcing connectivity to the capital would incorrectly count them.

If all roads are Black,

```
3
BBB
BBB
```

the graph is (K_4), so there are (16) spanning trees and all contain zero White roads. The answer is `16 0 0 0`. This is a useful check because the constant coefficient must survive all the polynomial manipulations.

If all roads are White,

```
3
WWW
WWW
```

the same graph has (16) spanning trees, but every tree contains exactly three White edges. The answer is `0 0 0 16`. This catches mistakes where the polynomial degree is interpreted as the number of Black edges instead.

The cyclic boundary also matters. For

```
4
---W
BBBB
```

the only circular road is the edge from city (4) back to city (1). There is one tree consisting of all four Black spokes, and two more trees that use the White circular edge and omit either the spoke to city (1) or the spoke to city (4). Thus the answer is `1 2 0 0 0`. Treating the circular array as a path would miss these two trees.

## Approaches

A direct brute-force solution can enumerate every subset of the existing roads, check whether it contains exactly (n) edges, and then test whether those edges form a spanning tree. There are at most (2n) possible roads, so enumerating all subsets already gives (2^{2n}=4^n) possibilities. Checking connectivity for every subset costs another (O(n)), giving (O(n4^n)) time in the simplest implementation. Even using the fact that a tree has exactly (n) edges only changes this to roughly

[
O\left(n\binom{2n}{n}\right),
]

which is still exponential. The brute force is correct because every spanning tree is exactly one enumerated edge subset, but it becomes useless long before (n=50000).

The structure of this graph gives us a much stronger description of a spanning tree. Look only at the selected circular edges. They form either a collection of paths, or the entire circle. If at least one circular edge is missing, the selected circular edges split the outer vertices into several path components. Every such component must contain exactly one selected spoke to the capital. If it contained no spoke, that component would remain disconnected from the capital. If it contained two or more spokes, the two spokes together with the path between their endpoints would create a cycle.

This observation converts the graph problem into a local sequence problem. While walking around the circle, we only need to remember whether the current outer component has already received its unique spoke. That is a two-state automaton.

The cyclic nature of the graph means that instead of running this automaton from an arbitrarily chosen starting state, we multiply its (2\times2) transition matrices and take their trace. The trace forces the state after the last edge to equal the state before the first edge, exactly what is required when the sequence wraps around.

Each matrix entry is a polynomial in (x). We therefore have to multiply (n) small matrices whose entries are polynomials of increasing degree. Ordinary polynomial multiplication would again become quadratic, so the final ingredient is NTT convolution. A divide-and-conquer product tree multiplies the matrices in (O(\log n)) levels, while each level performs a total amount of polynomial multiplication bounded by (O(n\log n)). The complete complexity is (O(n\log^2 n)).

The matrix product itself can be performed with seven polynomial multiplications using the Strassen (2\times2) formula instead of the usual eight. This is only an implementation optimization, but it matters for a Python implementation because polynomial convolution dominates the running time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n4^n)) | (O(n)) | Too slow |
| Optimal | (O(n\log^2 n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Treat every existing road as a polynomial weight. A White road gets weight (x), a Black road gets weight (1), and an absent road gets weight (0). The product of the weights of a selected edge set is then exactly (x^k), where (k) is its number of White edges.
2. For every outer city (i), let (q_i) be the weight of its spoke, and let (r_i) be the weight of the circular edge from (i) to (i+1).

While processing city (i), maintain a state (0) or (1). State (0) means that the current circular component has not yet selected a spoke, while state (1) means that it already has its unique spoke.
3. Consider first the case where the circular edge (i) is absent. The current component ends at city (i), so it must contain exactly one spoke. From state (0), we must select the spoke, contributing (q_i), and move to state (0) for the next component. From state (1), we must not select another spoke, contributing (1), and again move to state (0).

Its transition matrix is

[
A_i=
\begin{pmatrix}
q_i&0\
1&0
\end{pmatrix}.
]
4. Now consider the case where circular edge (i) is selected. It contributes (r_i). If the current component has state (0), we may either omit the spoke and remain in state (0), or select the spoke and move to state (1). If the component already has state (1), we cannot select another spoke, so it stays in state (1).

The transition matrix before multiplying by the edge weight is

[
B_i=
\begin{pmatrix}
1&q_i\
0&1
\end{pmatrix}.
]

Including the circular edge weight gives (r_iB_i).
5. We may choose either state of the circular edge, so the complete transition matrix is

\begin{pmatrix}
q_i+r_i&q_ir_i\
1&r_i
\end{pmatrix}.
]

Every valid local choice is represented exactly once in this matrix.
6. Multiply all matrices in circular order:

[
P=M_1M_2\cdots M_n.
]

Taking (\operatorname{tr}(P)) forces the automaton to finish in the same state in which it started. If at least one circular edge is absent, that gives exactly the condition that every circular component contains one spoke.
7. There is one exceptional configuration that the trace counts but which is not a spanning tree. If every circular edge is selected, the outer vertices form one complete cycle. The automaton has two possible cyclic states, state (0) everywhere and state (1) everywhere, and both produce a contribution equal to

[
\prod_i r_i.
]

No spoke is selected in either configuration, so the capital is disconnected. Thus we must subtract

[
2\prod_i r_i.
]

If any circular edge is absent, this product is zero and there is nothing to subtract.
8. The resulting polynomial has degree at most (n), because every spanning tree has exactly (n) edges. During polynomial multiplication we can discard coefficients above degree (n), since they can never affect the final answer.
9. Multiplying the (n) polynomial matrices sequentially would still create (O(n^2)) work. Instead, build a balanced divide-and-conquer product tree. A segment of matrices is represented by its product, and two adjacent segment products are multiplied when their recursive calls return.
10. Polynomial multiplication is performed by NTT under (998244353). For very small polynomials, ordinary (O(ab)) multiplication is faster than constructing NTT arrays, so the implementation uses a small naive-multiplication threshold.
11. Finally, take the trace of the complete matrix, subtract the exceptional all-circular-edge contribution, and print coefficients (0) through (n).

The invariant behind the construction is that, whenever a circular edge is processed, the matrix state records exactly whether the currently open circular component already contains its one permitted spoke. A transition through an absent circular edge is allowed only when that component has exactly one spoke, while a selected circular edge merely extends the component without allowing a second spoke. Consequently, every cyclic state sequence counted by the trace corresponds to a collection of circular paths with exactly one spoke per component. Such a collection has exactly (n) edges and is connected, hence is a spanning tree. The only trace configurations outside this correspondence are the two zero-spoke states when every circular edge is selected, and those are removed explicitly.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
ROOT = 3
NAIVE_LIMIT = 32

LIMIT = 0
root_cache = {}
inv_root_cache = {}

def cut(p):
    if len(p) > LIMIT + 1:
        p = p[:LIMIT + 1]
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p

def padd(a, b):
    n = max(len(a), len(b))
    c = [0] * n
    la = len(a)
    lb = len(b)
    for i in range(n):
        x = a[i] if i < la else 0
        y = b[i] if i < lb else 0
        z = x + y
        if z >= MOD:
            z -= MOD
        c[i] = z
    return cut(c)

def psub(a, b):
    n = max(len(a), len(b))
    c = [0] * n
    la = len(a)
    lb = len(b)
    for i in range(n):
        x = a[i] if i < la else 0
        y = b[i] if i < lb else 0
        z = x - y
        if z < 0:
            z += MOD
        c[i] = z
    return cut(c)

def lincomb(items):
    n = 1
    for p, _ in items:
        if len(p) > n:
            n = len(p)

    c = [0] * n
    for p, sign in items:
        if sign == 1:
            for i, x in enumerate(p):
                c[i] += x
        else:
            for i, x in enumerate(p):
                c[i] -= x

    for i in range(n):
        c[i] %= MOD

    return cut(c)

def ntt(a, invert):
    n = len(a)

    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        if invert:
            wlen = inv_root_cache.get(length)
            if wlen is None:
                wlen = pow(ROOT, (MOD - 1) // length, MOD)
                wlen = pow(wlen, MOD - 2, MOD)
                inv_root_cache[length] = wlen
        else:
            wlen = root_cache.get(length)
            if wlen is None:
                wlen = pow(ROOT, (MOD - 1) // length, MOD)
                root_cache[length] = wlen

        half = length >> 1

        for start in range(0, n, length):
            w = 1
            end = start + half
            j = start
            while j < end:
                u = a[j]
                v = a[j + half] * w % MOD

                x = u + v
                if x >= MOD:
                    x -= MOD

                y = u - v
                if y < 0:
                    y += MOD

                a[j] = x
                a[j + half] = y
                w = w * wlen % MOD
                j += 1

        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def convolution(a, b):
    if not a or not b:
        return [0]

    if a == [0] or b == [0]:
        return [0]

    la = len(a)
    lb = len(b)

    if min(la, lb) <= NAIVE_LIMIT or la * lb <= 4096:
        res = [0] * (min(la + lb - 1, LIMIT + 1))

        for i, x in enumerate(a):
            if x == 0:
                continue
            max_j = min(lb, LIMIT + 1 - i)
            for j in range(max_j):
                res[i + j] = (res[i + j] + x * b[j]) % MOD

        return cut(res)

    need = min(la + lb - 1, LIMIT + 1)

    size = 1
    while size < la + lb - 1:
        size <<= 1

    fa = a + [0] * (size - la)
    fb = b + [0] * (size - lb)

    ntt(fa, False)
    ntt(fb, False)

    for i in range(size):
        fa[i] = fa[i] * fb[i] % MOD

    ntt(fa, True)

    return cut(fa[:need])

def matrix_add(a, b):
    return (
        padd(a[0], b[0]),
        padd(a[1], b[1]),
        padd(a[2], b[2]),
        padd(a[3], b[3]),
    )

def matrix_product(a, b):
    """
    a = [[a0, a1],
         [a2, a3]]

    b = [[b0, b1],
         [b2, b3]]

    Polynomial Strassen multiplication.
    """

    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b

    p1 = convolution(padd(a0, a3), padd(b0, b3))
    p2 = convolution(padd(a2, a3), b0)
    p3 = convolution(a0, psub(b1, b3))
    p4 = convolution(a3, psub(b2, b0))
    p5 = convolution(padd(a0, a1), b3)
    p6 = convolution(psub(a2, a0), padd(b0, b1))
    p7 = convolution(psub(a1, a3), padd(b2, b3))

    c0 = lincomb([
        (p1, 1),
        (p4, 1),
        (p5, -1),
        (p7, 1),
    ])

    c1 = lincomb([
        (p3, 1),
        (p5, 1),
    ])

    c2 = lincomb([
        (p2, 1),
        (p4, 1),
    ])

    c3 = lincomb([
        (p1, 1),
        (p3, 1),
        (p2, -1),
        (p6, 1),
    ])

    return c0, c1, c2, c3

def make_poly(v):
    if v == 0:
        return [0]
    if v == 1:
        return [1]
    return [0, 1]

def build_product(s, t, left, right):
    if right - left == 1:
        q = make_poly(1 if t[left] == 'B' else 0 if t[left] == '-' else 2)
        r = make_poly(1 if s[left] == 'B' else 0 if s[left] == '-' else 2)

        # The encoding above used 2 for W temporarily.
        # Replace it by the polynomial x.
        if t[left] == 'W':
            q = [0, 1]
        if s[left] == 'W':
            r = [0, 1]

        qr = convolution(q, r)
        qr = cut(qr)

        return (
            padd(q, r),
            qr,
            [1],
            r,
        )

    mid = (left + right) >> 1

    a = build_product(s, t, left, mid)
    b = build_product(s, t, mid, right)

    return matrix_product(a, b)

def solve_case(n, s, t):
    global LIMIT
    LIMIT = n

    # M_i =
    #
    # [ q_i + r_i, q_i r_i ]
    # [     1,       r_i   ]

    product = build_product(s, t, 0, n)

    answer = product[0][:]
    if len(product[3]) > len(answer):
        answer += [0] * (len(product[3]) - len(answer))

    for i, x in enumerate(product[3]):
        answer[i] = (answer[i] + x) % MOD

    # The trace is product[0] + product[3].
    # If every circular edge is present, it contains two
    # invalid zero-spoke cyclic states.
    if '-' not in s:
        white_rim = s.count('W')
        if white_rim >= len(answer):
            answer += [0] * (white_rim + 1 - len(answer))
        answer[white_rim] = (answer[white_rim] - 2) % MOD

    if len(answer) < n + 1:
        answer += [0] * (n + 1 - len(answer))

    answer = answer[:n + 1]

    return ' '.join(map(str, answer))

def main():
    n = int(input())
    s = input().strip()
    t = input().strip()
    print(solve_case(n, s, t))

if __name__ == "__main__":
    main()
```

The implementation represents a (2\times2) polynomial matrix by a tuple of four polynomials in row-major order. At a leaf, `q` is the spoke weight and `r` is the circular-edge weight, so the matrix is exactly

[
\begin{pmatrix}
q+r&qr\
1&r
\end{pmatrix}.
]

The small conversion in `build_product` deliberately keeps absent edges as the zero polynomial, Black edges as the constant polynomial (1), and White edges as (x).

The recursive function `build_product` preserves the original circular order. It first computes the product of the left half and the right half, then multiplies those two matrices. No commutation of matrices is performed, which is necessary because matrix multiplication itself is not commutative.

The polynomial operations always truncate at degree (n). This is safe because every desired spanning-tree term has exactly (n) edges, so coefficients of higher degree can never influence the requested answer.

The matrix multiplication uses the seven-product Strassen identity. For polynomials, each scalar multiplication in that identity is replaced by a convolution. This reduces eight NTT convolutions to seven per matrix merge.

The `convolution` function switches to ordinary multiplication for small inputs. This matters because an NTT has a relatively large constant factor, while a polynomial of a few dozen coefficients is cheaper to multiply directly.

The subtraction of (2\prod r_i) is implemented without another polynomial multiplication. Since each (r_i) is either (0), (1), or (x), their product is zero if any circular edge is absent. Otherwise it is simply (x^c), where (c) is the number of White circular edges.

Python integers do not overflow, so there is no separate overflow concern. Every arithmetic result that enters a polynomial is reduced modulo (998244353). The NTT length never approaches the modulus limitation because the largest required transform is comfortably below the supported power of two.

## Worked Examples

### Sample 1

The input is

```
3
---
WBW
```

Every circular edge is absent, so (r_i=0). The spoke weights are (q_1=x), (q_2=1), and (q_3=x).

The individual transition matrices are

[
M_1=
\begin{pmatrix}
x&0\
1&0
\end{pmatrix},
\quad
M_2=
\begin{pmatrix}
1&0\
1&0
\end{pmatrix},
\quad
M_3=
\begin{pmatrix}
x&0\
1&0
\end{pmatrix}.
]

The product states evolve as follows.

| Step | Matrix product | Trace |
| --- | --- | --- |
| Start | (M_1) | (x) |
| After city 2 | (M_1M_2) | (x) |
| After city 3 | (M_1M_2M_3) | (x^2) |

There are no circular edges, so the exceptional all-circular-edge correction is zero. The final polynomial is (x^2), giving

```
0 0 1 0
```

This demonstrates that the polynomial exponent counts White edges directly. The only possible spanning tree consists of all three spokes, two of which are White.

### Sample 2

The input is

```
3
WWW
BBB
```

Every circular edge has weight (x), while every spoke has weight (1). All three transition matrices are therefore

[
M=
\begin{pmatrix}
1+x&x\
1&x
\end{pmatrix}.
]

The successive products are

| Step | Polynomial matrix |
| --- | --- |
| (M) | (\begin{pmatrix}1+x&x\1&x\end{pmatrix}) |
| (M^2) | (\begin{pmatrix}1+3x+x^2&x+2x^2\1+2x&x+x^2\end{pmatrix}) |
| (M^3) | (\begin{pmatrix}1+4x+5x^2+x^3&x+3x^2+2x^3\1+3x&x+3x^2+x^3\end{pmatrix}) |

The trace is

[
1+6x+9x^2+2x^3.
]

All circular edges are present, so the two invalid zero-spoke states contribute (2x^3). Removing them gives

[
1+6x+9x^2.
]

Thus the answer is

```
1 6 9 0
```

The correction is the key part of this example. Without it, the coefficient of (x^3) would incorrectly be (2).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log^2 n)) | The divide-and-conquer matrix product has (O(\log n)) levels, and each level performs a total (O(n\log n)) amount of NTT convolution work |
| Space | (O(n)) | Each recursive product stores (O(n)) polynomial coefficients, and the largest NTT buffers are also (O(n)) |

The largest instance has (50000) outer cities, so a quadratic algorithm would already require billions of operations. The product-tree approach reduces the polynomial work to near-linear complexity apart from logarithmic factors. The modulus (998244353) allows all required convolutions to be performed exactly with NTT.

## Test Cases

The following test harness uses the same `solve_case` function as the submitted solution. The maximum-size tests use the known total number of spanning trees of an unweighted wheel. For the wheel with (n) outer vertices this total is (L_{2n}-2), where (L_0=2), (L_1=1), and (L_i=L_{i-1}+L_{i-2}).

```python
# helper: run solution on input string, return output string
import io
import sys

def run(inp: str) -> str:
    data = inp.strip().splitlines()
    n = int(data[0])
    s = data[1].strip()
    t = data[2].strip()
    return solve_case(n, s, t)

# Provided samples
assert run("""3
---
WBW
""") == "0 0 1 0", "sample 1"

assert run("""3
WWW
BBB
""") == "1 6 9 0", "sample 2"

assert run("""5
BWB-B
WB-W-
""") == "0 2 6 3 0 0", "sample 3"

# Minimum-size graph, all roads Black.
assert run("""3
BBB
BBB
""") == "16 0 0 0", "all black, K4"

# Minimum-size graph, all roads White.
assert run("""3
WWW
WWW
""") == "0 0 0 16", "all white, K4"

# No spokes, so the capital is isolated.
assert run("""3
WWW
---
""") == "0 0 0 0", "isolated capital"

# Only the wrap-around circular edge exists and is White.
assert run("""4
---W
BBBB
""") == "1 2 0 0 0", "wrap-around edge"

# Maximum-size all-Black instance.
n = 50000
s = "B" * n
t = "B" * n

lucas0, lucas1 = 2, 1
for _ in range(2 * n):
    lucas0, lucas1 = lucas1, (lucas0 + lucas1) % MOD

total = (lucas1 - 2) % MOD
expected = " ".join([str(total)] + ["0"] * n)

assert run(f"{n}\n{s}\n{t}\n") == expected, "maximum-size all black"

# Maximum-size all-White instance.
s = "W" * n
t = "W" * n
expected = " ".join(["0"] * n + [str(total)])

assert run(f"{n}\n{s}\n{t}\n") == expected, "maximum-size all white"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / BBB / BBB` | `16 0 0 0` | Minimum size and all-Black weighting |
| `3 / WWW / WWW` | `0 0 0 16` | All-White weighting and highest degree |
| `3 / WWW / ---` | `0 0 0 0` | Disconnected capital |
| `4 / ---W / BBBB` | `1 2 0 0 0` | Circular wrap-around edge and boundary indexing |
| (n=50000), all `B` | (L_{100000}-2) at coefficient zero | Maximum-size input and NTT path |
| (n=50000), all `W` | (L_{100000}-2) at coefficient (50000) | Maximum degree and all-White boundary |

## Edge Cases

When the capital has no incident edges, the algorithm automatically gives zero. Every transition has (q_i=0), so a circular component can never close with a selected spoke. If the circular graph is still present, the trace may describe circular configurations, but the required one-spoke-per-component condition eliminates them. For `3 / WWW / ---`, every coefficient is zero.

When every road is Black, every road weight is (1). For (n=3), the graph is (K_4), and the transition product produces the full spanning-tree count. The correction subtracts the two invalid all-circular-edge states, leaving (16) at degree zero. Thus the answer is `16 0 0 0`.

When every road is White, every selected edge contributes one factor of (x). Every spanning tree has exactly (n) edges, so all valid terms must have degree (n). For (n=3), the polynomial is (16x^3), producing `0 0 0 16`. This is also a useful check that truncating degrees above (n) cannot remove a valid answer.

If one circular edge is missing, the exceptional correction disappears because (\prod_i r_i=0). For example, with

```
4
---W
BBBB
```

the only circular edge is the wrap-around edge (4\leftrightarrow1). The all-spoke tree contributes one term of degree zero. Selecting the White circular edge creates a path between cities (4) and (1), so exactly one of their two spokes must be removed. There are two such trees, both with one White edge. The result is `1 2 0 0 0`.

The case where all circular edges exist is the subtle cyclic boundary case. The trace has two artificial configurations because the automaton can remain forever in state (0), or forever in state (1), without ever closing a component. Both correspond to selecting every circular edge and no spokes. They are not spanning trees because the capital is isolated, so subtracting exactly (2\prod_i r_i) is necessary. The subtraction also handles mixed Black and White circular edges correctly, since the product carries the appropriate power of (x).

Finally, absent edges must be represented by the zero polynomial rather than simply skipped. Their presence changes the connectivity structure, not just the weight of a selected edge. The transition matrix incorporates this by making every transition that selects an absent road contribute zero, while still allowing the automaton to close the current component when that road is omitted.
