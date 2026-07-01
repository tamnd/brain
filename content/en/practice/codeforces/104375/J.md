---
title: "CF 104375J - Jumping Reaction"
description: "We are given an array of integers where each value represents a “jumping energy” of a substance. When two substances with energies $a$ and $b$ are mixed, they contribute an energy of $ab$."
date: "2026-07-01T17:31:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104375
codeforces_index: "J"
codeforces_contest_name: "2023 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 104375
solve_time_s: 74
verified: true
draft: false
---

[CF 104375J - Jumping Reaction](https://codeforces.com/problemset/problem/104375/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers where each value represents a “jumping energy” of a substance. When two substances with energies $a$ and $b$ are mixed, they contribute an energy of $ab$. When more than two substances are mixed together, the total energy is defined as the sum of all pairwise products among the chosen elements.

So for any query range $[L, R]$, we take the subarray $A_L, A_{L+1}, \dots, A_R$ and compute:

$$\sum_{L \le i < j \le R} A_i A_j$$

Each query asks for this value modulo $10^9 + 7$, and there can be up to $10^6$ queries over an array of size up to $10^6$.

A direct reading suggests we need to repeatedly compute a function over many subarrays, and the function depends on all pairwise interactions inside the subarray.

The key constraint implication is that both $N$ and $Q$ are large enough that any solution doing even $O(R-L)$ per query is too slow. A per-query quadratic approach is completely impossible since a single worst-case query would already be $O(10^{12})$ operations.

A slightly less naive approach is still insufficient: even $O(N)$ per query leads to $10^{12}$ total operations.

The only acceptable target is roughly $O((N+Q)\log N)$ or $O(N+Q)$.

A subtle issue appears in naive formulations: recomputing pair sums independently per query leads to repeated work that is not reusable unless we restructure the expression.

## Approaches

A brute-force approach directly follows the definition. For each query $[L, R]$, we iterate over all pairs $i < j$ and accumulate $A_i A_j$. This is correct because it exactly matches the definition of the energy as sum of pairwise products. However, for a range of length $k$, this requires $k(k-1)/2$ multiplications. In the worst case $k = N = 10^6$, so a single query already becomes infeasible.

Even if we try to improve it by fixing one endpoint and summing over the other, each query remains linear in the range size, which still leads to worst-case quadratic total complexity.

The key observation is that the pairwise sum has a standard algebraic identity. If we define:

$$S = \sum A_i, \quad S_2 = \sum A_i^2$$

then:

$$\left(\sum A_i\right)^2 = \sum A_i^2 + 2\sum_{i<j} A_iA_j$$

Rearranging gives:

$$\sum_{i<j} A_iA_j = \frac{S^2 - S_2}{2}$$

This transforms the problem from “sum over all pairs” into a problem of computing two prefix sums: sum of elements and sum of squares. Once those are available, each query becomes O(1).

We precompute prefix sums:

$$P[i] = \sum_{k=1}^{i} A_k,\quad Q[i] = \sum_{k=1}^{i} A_k^2$$

Then for a query $[L, R]$:

$$S = P[R] - P[L-1], \quad S_2 = Q[R] - Q[L-1]$$

and answer is:

$$(S^2 - S_2) \cdot inv2 \bmod (10^9+7)$$

The division by 2 requires modular inverse of 2.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NQ) | O(1) | Too slow |
| Prefix sums + identity | O(N + Q) | O(N) | Accepted |

## Algorithm Walkthrough

1. Precompute prefix sums of values and prefix sums of squares over the array.

This allows any segment sum or squared-sum to be computed in constant time.
2. For each index $i$, store:

$P[i] = P[i-1] + A[i]$ and $Q[i] = Q[i-1] + A[i]^2$.

The reason we square values in advance is that the final formula depends on both linear and quadratic aggregates.
3. Precompute the modular inverse of 2 under $10^9+7$.

This is necessary because pair counting introduces a division by 2 that must be handled in modular arithmetic.
4. For each query $[L, R]$, compute:

$S = P[R] - P[L-1]$ and $S_2 = Q[R] - Q[L-1]$, normalized modulo.

These represent the sum and sum of squares of the chosen segment.
5. Convert the segment into the pair-sum using:

$(S^2 - S_2) / 2$.

This step relies on the algebraic identity that expands the square of a sum.
6. Output the result modulo $10^9+7$.

### Why it works

The correctness comes from expanding the square of a sum over a multiset. Every product $A_iA_j$ with $i \ne j$ appears exactly twice in $S^2$, once as $A_iA_j$ and once as $A_jA_i$. Subtracting $\sum A_i^2$ removes diagonal terms, leaving exactly twice the desired pairwise sum. Dividing by two corrects the overcounting, ensuring each unordered pair contributes exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
INV2 = (MOD + 1) // 2

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    pref2 = [0] * (n + 1)

    for i in range(1, n + 1):
        x = a[i - 1] % MOD
        pref[i] = (pref[i - 1] + x) % MOD
        pref2[i] = (pref2[i - 1] + x * x) % MOD

    out = []

    for _ in range(q):
        l, r = map(int, input().split())
        s = (pref[r] - pref[l - 1]) % MOD
        s2 = (pref2[r] - pref2[l - 1]) % MOD

        ans = (s * s - s2) % MOD
        ans = (ans * INV2) % MOD
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The prefix arrays `pref` and `pref2` store cumulative sums and cumulative squared sums respectively, both taken modulo $10^9+7$. Each query reduces to constant time arithmetic on these precomputed values.

The multiplication `s * s` is safe under modulo arithmetic because all operations are already reduced modulo MOD. The subtraction is also normalized to avoid negative values. The inverse of 2 is precomputed once since MOD is prime.

## Worked Examples

### Example 1

Input:

```
5 3
1 2 3 4 5
1 2
1 5
3 5
```

We build prefix sums:

| i | A[i] | P[i] | Q[i] |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 3 | 5 |
| 3 | 3 | 6 | 14 |
| 4 | 4 | 10 | 30 |
| 5 | 5 | 15 | 55 |

For query $[1,2]$, $S=3$, $S_2=5$.

Answer $= (9 - 5)/2 = 2$.

For $[1,5]$, $S=15$, $S_2=55$.

Answer $= (225 - 55)/2 = 85$.

For $[3,5]$, $S=12$, $S_2=50$.

Answer $= (144 - 50)/2 = 47$.

This confirms the identity consistently transforms pair sums into prefix computations.

### Example 2

Input:

```
10 2
3 1 5 2 3 1 5 6 1 1
7 10
2 3
```

Prefix reasoning:

For $[7,10]$: values are $5,6,1,1$.

Sum $S=13$, squares $S_2=25 + 36 + 1 + 1 = 63$.

Answer $= (169 - 63)/2 = 53$.

For $[2,3]$: values are $1,5$.

Sum $S=6$, squares $S_2=26$.

Answer $= (36 - 26)/2 = 5$.

This demonstrates that even disjoint distributions and mixed magnitudes behave uniformly under the same transformation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + Q) | One pass to build prefix sums and constant work per query |
| Space | O(N) | Two prefix arrays of size N |

The constraints require linear preprocessing and constant-time queries since both $N$ and $Q$ are up to $10^6$. Any approach with logarithmic or linear per query cost would exceed time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""5 3
1 2 3 4 5
1 2
1 5
3 5
""") == """2
85
47"""

assert run("""10 2
3 1 5 2 3 1 5 6 1 1
7 10
2 3
""") == """53
5"""

# custom cases

# minimum size ranges
assert run("""2 1
1 1
1 2
""") == "1"

# all equal values
assert run("""5 2
2 2 2 2 2
1 5
2 4
""") == """20
12"""

# single-element queries
assert run("""6 3
1 2 3 4 5 6
3 3
1 1
6 6
""") == """0
0
0"""

# increasing sequence stress
assert run("""4 2
1 2 3 4
1 4
2 4
""") == """35
26"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single-element ranges | 0 | ensures diagonal terms are excluded correctly |
| all equal values | consistent quadratic growth | verifies symmetry and scaling |
| full range vs subrange | 35 / 26 | checks prefix correctness and slicing |

## Edge Cases

A key edge case is when the range has only one element. For input like:

```
1 1
7
1 1
```

the correct answer is 0 because there are no pairs. The algorithm handles this because $S^2 = S_2$, so subtraction yields zero before division.

Another case is large uniform arrays where naive implementations risk overflow or slowdowns due to repeated multiplication. For example, all values being $10^6$ leads to large intermediate sums, but modular arithmetic keeps values bounded and prefix computation remains stable.

A final subtle case is when subtraction produces a negative intermediate result in modular arithmetic. The implementation fixes this by taking modulo after every subtraction, ensuring correctness even when $P[L-1]$ or $Q[L-1]$ is larger than the corresponding prefix at $R$.
