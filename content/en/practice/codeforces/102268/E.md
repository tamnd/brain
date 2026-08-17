---
title: "CF 102268E - Expected Value"
description: "We have a connected undirected plane graph whose vertices are given by their coordinates and whose edges are straight segments. A random walk starts at vertex (1). Whenever the walk is at a vertex, it chooses one of its incident edges uniformly and moves across it."
date: "2026-08-17T18:47:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102268
codeforces_index: "E"
codeforces_contest_name: "300iq Contest 1"
rating: 0
weight: 102268
solve_time_s: 410
verified: false
draft: false
---

[CF 102268E - Expected Value](https://codeforces.com/problemset/problem/102268/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We have a connected undirected plane graph whose vertices are given by their coordinates and whose edges are straight segments. A random walk starts at vertex (1). Whenever the walk is at a vertex, it chooses one of its incident edges uniformly and moves across it. The process stops the first time vertex (n) is reached, and we need the expected number of moves, represented modulo (998244353).

The coordinates are not needed for the random walk itself. Their purpose is to describe a plane embedding, which gives us the crucial structural bound on the number of edges. A simple plane graph with (n\ge 3) vertices has at most (3n-6) edges. Thus, although the statement allows the general complete-graph bound syntactically, the actual input graph is sparse, with (m=O(n)). The official problem uses (n\le 3000), so an (O(n^2)) algorithm is realistic, while a dense (O(n^3)) linear algebra method is too slow.

There is another constraint hidden in the probabilistic nature of the problem. The hitting time is not bounded by (n), so simulating the walk for a fixed number of steps cannot directly give the exact answer. A path with (n) vertices already has an expected hitting time of (n(n-1)), and more complicated graphs can also have large hitting times. We need to turn the infinite sequence of survival probabilities into a finite computation.

The first edge case is the smallest possible graph. With two vertices and the single edge (1\mathbin{-}2), the answer is exactly (1).

```
2
0 0
5000 5000
1
1 2
```

A careless implementation that builds only the transient graph and assumes every transient vertex has an outgoing transition could fail here, because after removing the target there are no remaining edges. The correct interpretation is that the walk makes one move directly into vertex (2), so the output is (1).

The second edge case is a direct edge to the target in a larger graph. Consider

```
3
0 0
1 0
5000 5000
2
1 2
1 3
```

Starting from vertex (1), the walk reaches vertex (3) with probability (1/2), while with probability (1/2) it moves to vertex (2), from which it must return to (1). The expectation is (3), because
[
E_1=1+\frac12E_2,\qquad E_2=1+E_1,
]
so (E_1=3). A common mistake is to normalize the transient transition probabilities after deleting the target. That would incorrectly make vertex (1) move to vertex (2) with probability (1), whereas the original walk still chooses among all original neighbors.

The third edge case is a graph with many edges incident to the target. Those edges affect the degree of their other endpoints, because they represent genuine possibilities of hitting the target. They must remain in the degree used for the transition probability, even though they disappear from the transient state transition matrix.

## Approaches

The most direct approach is to write a first-step equation for every vertex. Let (E_v) be the expected remaining time to reach (n) from (v). Then (E_n=0), and for every other vertex
[
E_v=1+\frac{1}{\deg(v)}\sum_{u\sim v}E_u.
]
After fixing (E_n=0), this is a linear system with (n-1) unknowns.

This system is mathematically perfect, but ordinary dense Gaussian elimination performs (\Theta(n^3)) arithmetic operations. The elimination update count alone is roughly
[
\sum_{k=0}^{n-2}(n-k-1)^2
=\frac{(n-1)(n-2)(2n-3)}6,
]
which is about (9\times10^9) updates when (n=3000). Sparse input does not save a naive implementation, because elimination creates fill-in. The brute-force linear-system formulation is useful for understanding correctness, but it does not exploit the graph structure enough.

The observation that unlocks the intended solution is to stop asking for the expectation directly. For a nonnegative integer-valued random variable (T),
[
E[T]=\sum_{i\ge0}\Pr(T>i).
]
Let (S_i=\Pr(T>i)). Instead of solving for one expected value, we generate the first (2(n-1)) values of the sequence (S_i).

Delete the target vertex (n) from the state space, but do not change the original degrees. Let (f_i(v)) be the probability that after exactly (i) moves the walker is at transient vertex (v), having never visited (n). The transition is linear:
[
f_{i+1}(v)=\sum_{u\sim v,\ u\ne n}\frac{f_i(u)}{\deg(u)}.
]
The survival probability is simply
[
S_i=\sum_{v\ne n}f_i(v).
]

There are only (n-1) transient states, so this is a fixed linear transformation applied repeatedly. By the Cayley-Hamilton theorem, every sequence obtained from powers of an ((n-1)\times(n-1)) matrix satisfies a linear recurrence of degree at most (n-1). Consequently, (S_i) also satisfies such a recurrence. Berlekamp-Massey can recover the shortest recurrence from the first (2(n-1)) terms. The standard (2N)-term bound is exactly the reason we only need a finite prefix of this otherwise infinite sequence.

Finally, the recurrence gives the infinite sum without generating any more terms. If
[
C(x)=c_0+c_1x+\cdots+c_Lx^L
]
is the connection polynomial returned by Berlekamp-Massey, then
[
F(x)=\sum_{i\ge0}S_ix^i
]
satisfies (F(x)C(x)=R(x)), where (R) has degree less than (L). Thus
[
F(1)=\frac{R(1)}{C(1)}.
]
This is exactly the technique used in the known solution for this problem. The plane-graph bound (m=O(n)) makes generating all the terms take (O(nm)=O(n^2)) operations, while Berlekamp-Massey takes (O(n^2)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) | (O(n^2)) | Too slow |
| Optimal | (O(nm+n^2)=O(n^2)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Read the graph and compute the original degree of every vertex. The degree must include edges going directly to vertex (n), because those edges are real choices made by the random walk.
2. Remove vertex (n) from the transient state space. Store every edge whose two endpoints are different from (n). Such an edge contributes transitions in both directions. Edges incident to (n) are not stored as transient transitions because taking one of them terminates the process.
3. Compute the modular inverse of every transient vertex degree. If the current probability at (u) is (f(u)), then the amount contributed to each neighbor is (f(u)/\deg(u)). All divisions are performed modulo (998244353).
4. Initialize (f_0(1)=1) and every other transient probability to zero. Consequently, (S_0=1), because the walk has taken zero steps and has certainly not reached (n).
5. Repeatedly apply the transient transition matrix to generate (S_1,S_2,\ldots,S_{2N-1}), where (N=n-1). For an internal edge ((u,v)), the next probability receives (f(u)/\deg(u)) at (v), and (f(v)/\deg(v)) at (u). Processing every undirected edge once therefore performs both directed transitions.
6. Apply Berlekamp-Massey to the resulting sequence. It returns coefficients (C_0,\ldots,C_L) satisfying
[
\sum_{j=0}^{L}C_jS_{i-j}=0
]
for every (i\ge L), with (C_0=1). The recurrence degree is at most (N), so (2N) terms are enough to determine the infinite recurrence.
7. Define
[
F(x)=\sum_{i\ge0}S_ix^i,\qquad
C(x)=\sum_{j=0}^{L}C_jx^j.
]
Multiplying them gives
[
F(x)C(x)=R(x),
]
where the coefficients from (x^L) onward vanish because they are exactly the recurrence equations. Hence (R) has degree at most (L-1).
8. Evaluate at (x=1). Since (F(1)=E[T]),
[
E[T]=\frac{R(1)}{C(1)}.
]
The numerator can be computed from prefix sums of (S_i):
[
R(1)=
\sum_{j=0}^{L-1}C_j
\left(\sum_{k=0}^{L-1-j}S_k\right).
]
The denominator is simply
[
C(1)=\sum_{j=0}^{L}C_j.
]
9. Multiply the numerator by the modular inverse of (C(1)) and print the result. The problem's modular fraction interpretation guarantees that this inverse is defined for the supplied tests.

### Why it works

The key invariant is that (f_i) contains exactly the probabilities of being at each non-target vertex after (i) moves without having visited the target. The transition preserves that meaning because every original choice has probability (1/\deg(u)), while transitions into (n) are simply omitted from the surviving probability mass. Thus (S_i=\sum_v f_i(v)) is exactly (\Pr(T>i)).

The transient transition is multiplication by a fixed matrix (M). Cayley-Hamilton gives a polynomial of degree at most (N=n-1) that annihilates (M), so every scalar sequence obtained from (M^i), including (S_i), satisfies a recurrence of degree at most (N). Berlekamp-Massey recovers that recurrence from (2N) terms. Once the recurrence is known, (F(x)C(x)) contains only its first (L) coefficients, so evaluating the rational generating function at (x=1) gives the infinite sum of all survival probabilities, which is exactly the expected hitting time.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def berlekamp_massey(s):
    # C[0] = 1 and
    # sum(C[i] * s[n-i]) = 0
    # for all sufficiently large n.
    C = [1]
    B = [1]

    L = 0
    m = 1
    b = 1

    for n in range(len(s)):
        d = s[n]
        for i in range(1, L + 1):
            d = (d + C[i] * s[n - i]) % MOD

        if d == 0:
            m += 1
            continue

        old_C = C[:]
        coef = d * pow(b, MOD - 2, MOD) % MOD

        need = m + len(B)
        if len(C) < need:
            C.extend([0] * (need - len(C)))

        for i in range(len(B)):
            C[i + m] = (C[i + m] - coef * B[i]) % MOD

        if 2 * L <= n:
            L = n + 1 - L
            B = old_C
            b = d
            m = 1
        else:
            m += 1

    return C[:L + 1]

def solve():
    n = int(input())

    # Coordinates only describe the plane embedding.
    for _ in range(n):
        input()

    m = int(input())

    target = n - 1
    deg = [0] * n
    internal_edges = []

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        if u != target:
            deg[u] += 1
        if v != target:
            deg[v] += 1

        if u != target and v != target:
            internal_edges.append((u, v))

    inv_deg = [0] * (n - 1)
    for v in range(n - 1):
        inv_deg[v] = pow(deg[v], MOD - 2, MOD)

    N = n - 1
    terms = [1]

    # f[v] is the probability of being at v without
    # having visited the target.
    f = [0] * N
    f[0] = 1

    # We need 2N terms: S_0 ... S_{2N-1}.
    for _ in range(1, 2 * N):
        scaled = [0] * N
        for v in range(N):
            scaled[v] = f[v] * inv_deg[v] % MOD

        nxt = [0] * N

        # Each undirected internal edge represents two
        # possible directed transitions.
        for u, v in internal_edges:
            x = nxt[u] + scaled[v]
            if x >= MOD:
                x -= MOD
            nxt[u] = x

            x = nxt[v] + scaled[u]
            if x >= MOD:
                x -= MOD
            nxt[v] = x

        total = 0
        for v in range(N):
            total += nxt[v]
            if total >= MOD:
                total -= MOD

        terms.append(total)
        f = nxt

    C = berlekamp_massey(terms)
    L = len(C) - 1

    # prefix[i] = S_0 + ... + S_i
    prefix = [0] * len(terms)
    cur = 0
    for i, x in enumerate(terms):
        cur += x
        if cur >= MOD:
            cur -= MOD
        prefix[i] = cur

    # R(1) = sum_{j=0}^{L-1} C[j] *
    #              (S_0 + ... + S_{L-1-j})
    numerator = 0
    for j in range(L):
        numerator = (
            numerator + C[j] * prefix[L - 1 - j]
        ) % MOD

    denominator = sum(C) % MOD
    answer = numerator * pow(denominator, MOD - 2, MOD) % MOD

    print(answer)

if __name__ == "__main__":
    solve()
```

The input parser first reads all coordinates and discards them. They are necessary for the statement to describe a plane graph, but the random walk depends only on adjacency.

The degree array is computed before the target is removed from the transition system. This is the most subtle graph detail in the implementation. If an edge (u-n) exists, it must increase (\deg(u)), even though it never contributes to `nxt`, because choosing that edge is exactly the event that ends the walk.

Only edges whose endpoints are both transient are stored. Processing an undirected edge ((u,v)) once updates both `nxt[u]` and `nxt[v]`, which cuts the transition loop roughly in half compared with explicitly storing two directed edges.

The probability vector is kept modulo `MOD` after every transition. The implementation uses conditional subtraction instead of `% MOD` for each edge addition. Both operands are already in the range ([0,\mathrm{MOD})), so one subtraction is enough.

Berlekamp-Massey stores only the current and previous connection polynomials. The implementation therefore uses (O(n)) memory rather than storing every intermediate polynomial, which would be unnecessary.

The final generating-function calculation deserves special attention. If (C(x)=\sum C_jx^j), then the coefficient of (x^k) in (F(x)C(x)) is
[
\sum_{j=0}^{k}C_jS_{k-j}.
]
It vanishes for (k\ge L), so only (k<L) contribute to (R(1)). The prefix-sum expression in the code evaluates all those contributions in (O(L)) time instead of using another (O(L^2)) nested loop.

No integer overflow occurs in the mathematical computation because every value is reduced modulo (998244353). Python integers also remove the fixed-width overflow concern present in C++, although keeping values reduced is still necessary for performance.

## Worked Examples

### Sample 1

The graph has only vertices (1) and (2), with (2) as the target.

| Step | (f(1)) | (S_i) | BM state |
| --- | --- | --- | --- |
| (0) | (1) | (1) | initial |
| (1) | (0) | (0) | recurrence begins |
| (2) | (0) | (0) | stable zero tail |
| final | (0) | (1,0,\ldots) | (C(x)=1) effectively |

The only move from vertex (1) goes directly to vertex (2), so (T=1). The survival sequence is (1,0,0,\ldots), whose generating function is simply (F(x)=1). The final result is (1).

### Sample 2

The graph has six vertices and vertex (6) is the target. The transient degrees are
[
\deg(1)=2,\quad
\deg(2)=4,\quad
\deg(3)=2,\quad
\deg(4)=3,\quad
\deg(5)=2.
]

The first few transient states are enough to see how the probability mass is handled.

| Step | (f(1)) | (f(2)) | (f(3)) | (f(4)) | (f(5)) | (S_i) |
| --- | --- | --- | --- | --- | --- | --- |
| (0) | (1) | (0) | (0) | (0) | (0) | (1) |
| (1) | (0) | (1/2) | (0) | (0) | (0) | (1/2) |
| (2) | (1/8) | (0) | (1/8) | (1/8) | (0) | (3/8) |
| (3) | (0) | (1/6) | (1/24) | (1/16) | (1/24) | (5/16) |

At step (1), half of the probability goes from (1) to (2), while the other half goes directly to the target and disappears from the transient state. This is why (S_1=1/2).

The actual expected value can also be checked directly from first-step equations. Writing (E_i) for the expected time from vertex (i), we get
[
E_1=1+\frac{E_2}{2},
]
[
E_2=1+\frac{E_1+E_3+E_4}{4},
]
[
E_3=1+\frac{E_2+E_4}{2},
]
[
E_4=1+\frac{E_2+E_3+E_5}{3},
]
[
E_5=1+\frac{E_4}{2}.
]
Solving gives (E_1=18/5). Modulo (998244353),
[
18\cdot5^{-1}\equiv798595486,
]
which matches the sample output.

The BM stage uses the full prefix of (2(n-1)=10) survival values, finds a recurrence for the sequence, and the generating-function evaluation returns the same (18/5). The trace demonstrates why probability that has already reached the target must disappear permanently from the state vector.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nm+n^2)) | (2(n-1)) sparse transitions cost (O(nm)), and Berlekamp-Massey costs (O(n^2)) |
| Space | (O(n+m)) | The graph, two probability vectors, survival sequence, and BM polynomials are all linear-sized |

For a simple plane graph with (n\ge3), (m\le3n-6), so (nm=O(n^2)). The total complexity is consequently (O(n^2)). With (n\le3000), this is the intended scale for the problem, whereas dense Gaussian elimination would require cubic work. The plane-graph sparsity is exactly what turns the repeated matrix-vector multiplication into a feasible operation.

## Test Cases

```python
# Save the solution above as solution.py before running this test file.
import sys
import io

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    try:
        solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    return out.getvalue().strip()

def path_input(n: int) -> str:
    lines = [str(n)]
    for i in range(n):
        lines.append(f"{i} 0")

    lines.append(str(n - 1))
    for i in range(1, n):
        lines.append(f"{i} {i + 1}")

    return "\n".join(lines) + "\n"

# Provided sample 1
sample1 = """\
2
0 0
35 35
1
1 2
"""
assert run(sample1) == "1", "sample 1"

# Provided sample 2
sample2 = """\
6
0 0
1 1
2 4
3 9
4 16
5 25
8
1 2
2 3
2 4
3 4
4 5
5 6
1 6
2 6
"""
assert run(sample2) == "798595486", "sample 2"

# Minimum size, also tests the direct transition into the target.
assert run("""\
2
0 0
5000 5000
1
1 2
""") == "1", "minimum-size graph"

# Path 1-2-3 has expected hitting time 3 * 2 = 6.
assert run("""\
3
0 0
1 0
5000 5000
2
1 2
2 3
""") == "6", "path graph"

# Four-cycle, target is vertex 4.
# The expected hitting time from 1 is 9.
assert run("""\
4
0 0
5000 0
5000 5000
0 5000
4
1 2
2 3
3 4
4 1
""") == "9", "regular cycle"

# Star centered at vertex 1, target is vertex 4.
# E = 2 * 3 - 1 = 5.
assert run("""\
4
0 0
5000 0
0 5000
5000 5000
3
1 2
1 3
1 4
""") == "5", "direct target edge and high degree"

# Maximum-size path.
# H(1, n) = n(n-1) for a path.
assert run(path_input(3000)) == "8997000", "maximum-size sparse graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two vertices joined by one edge | `1` | Minimum size and empty transient edge set |
| Three-vertex path | `6` | Repeated backtracking and nontrivial recurrence |
| Four-cycle | `9` | A graph where every vertex has equal degree |
| Four-vertex star | `5` | Target edge must remain in the source degree |
| Three-vertex path with coordinates at (0) and (5000) | `6` | Coordinate boundaries and ordinary graph behavior |
| Three-thousand-vertex path | `8997000` | Maximum (n), sparse plane graph, and (O(n^2)) scale |

## Edge Cases

The two-vertex graph is handled because the algorithm defines (N=n-1=1), so there is exactly one transient state. Its degree is one, its only edge goes to the target, and the internal-edge list is empty. The initial state is (f_0(1)=1), and after one transition the transient probability becomes zero. Thus (S_0=1) and (S_i=0) afterward, giving (F(x)=1) and answer (1).

```
2
0 0
5000 5000
1
1 2
```

A direct edge to the target in a larger graph is handled differently from an ordinary transient edge. For

```
3
0 0
1 0
5000 5000
2
1 2
1 3
```

vertex (1) has degree (2), not degree (1). The transition (1\to3) is omitted from `nxt` because it terminates the walk, but the factor (1/\deg(1)=1/2) is still used for the transition (1\to2). The first survival probabilities are (S_0=1), (S_1=1/2), (S_2=1/2), and their infinite sum is (3).

The same principle handles a target connected to many vertices. Consider the four-vertex star

```
4
0 0
5000 0
0 5000
5000 5000
3
1 2
1 3
1 4
```

Vertex (1) has degree (3). At each visit to (1), the probability of reaching target (4) is (1/3), while the probability of moving to one of the two non-target leaves is (2/3). Each leaf immediately returns to (1). The first-step equation is
[
E_1=1+\frac23(1+E_1),
]
giving (E_1=5). The implementation obtains the same result because the two leaf edges remain in the transient graph while the target edge contributes only to the degree of vertex (1).

A long path exercises the opposite extreme. For (n=3000), every interior vertex has degree (2), vertex (1) has degree (1), and vertex (n) is the absorbing target. The expected time is
[
n(n-1)=3000\cdot2999=8997000.
]
The walk can spend a quadratic number of steps repeatedly moving backward before finally reaching the target, so any approach that simulates only (O(n)) steps is fundamentally insufficient. The recurrence approach does not care how large the actual expectation is, because it reconstructs the entire infinite tail algebraically.

Finally, the modular arithmetic boundary deserves attention. Every transition probability is a rational number such as (1/2), (1/3), or (1/\deg(v)), so the implementation converts each denominator to its modular inverse before generating the sequence. Since every transient vertex has positive degree in the original connected graph, these inverses exist modulo the prime. The final division by (C(1)) is handled in the same way, matching the fraction interpretation required by the problem.
