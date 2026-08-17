---
title: "CF 102192F - Boolean 3-Array"
description: "A Boolean 3-array is an (mtimes ntimes p) box whose cells contain either zero or one. We may permute the slices independently along each of the three dimensions, and we may toggle any complete slice along any dimension."
date: "2026-08-18T02:04:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102192
codeforces_index: "F"
codeforces_contest_name: "2018 Chinese Multi-University Training, Nanjing U Contest"
rating: 0
weight: 102192
solve_time_s: 273
verified: true
draft: false
---

[CF 102192F - Boolean 3-Array](https://codeforces.com/problemset/problem/102192/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

A Boolean 3-array is an (m\times n\times p) box whose cells contain either zero or one. We may permute the slices independently along each of the three dimensions, and we may toggle any complete slice along any dimension. Two arrays belong to the same class if one can be changed into the other using these operations. The task is to count how many such classes exist, because from every class we can choose at most one representative.

The official input has up to 300 test cases, and every dimension is at most 13. The small dimension bound is the central clue. A direct enumeration of the (2^{mnp}) arrays is already impossible at (13\times13\times13), where there are exactly (2^{2197}) arrays. The permutation groups are also too large to enumerate individually. We need to count orbits without constructing them.

There are several easy cases that expose mistakes in a naive implementation. For `1 1 1`, the single cell can be toggled, so the two possible arrays are equivalent and the answer is `1`. For `1 1 2`, each of the two layers can be toggled independently, so all four arrays are equivalent and the answer is again `1`. A program that only considers permutations would incorrectly return two classes for this case.

A slightly less trivial boundary case is `1 2 2`. After the first dimension disappears, the structure is a (2\times2) binary matrix. Row and column toggles change two cells at a time, so the parity of the four cells is invariant. Both parities occur, giving answer `2`. A careless argument saying that arbitrary slice flips can always clear the whole array misses this invariant.

The official statement confirms the bounds (m,n,p\le13), the 2 second limit, and the sample outputs `1`, `9`, and `723` for `1 1 1`, `2 2 2`, and `2 3 4`.

## Approaches

The brute-force approach would enumerate every one of the (2^{mnp}) arrays and assign each array to an equivalence class by trying the allowed operations. This is correct because the operations generate exactly the equivalence relation from the statement. At the largest size there are (2^{2197}) arrays, roughly (10^{661}), so even merely reading all possible arrays is impossible. Pairwise comparison would require exactly (\binom{2^{2197}}2) comparisons in the worst case.

The useful observation is that the operations form a finite group action on the set of Boolean arrays. The number of equivalence classes is consequently given by Burnside's lemma: average, over all group elements, the number of arrays fixed by that element.

A group element consists of a permutation of the first dimension, a permutation of the second dimension, a permutation of the third dimension, and a collection of slice toggles. Instead of handling individual permutations, we group permutations by cycle type. A permutation of size at most 13 has very few possible cycle types, only 101 at size 13.

Fix three permutations. Consider one cycle of length (a), one of length (b), and one of length (c). Their product action on the corresponding block of cells has

[
\frac{abc}{\operatorname{lcm}(a,b,c)}
]

cell orbits. Consequently, if the three permutations have cycle lists (A,B,C), the total number of cell orbits is

\sum_{a\in A}\sum_{b\in B}\sum_{c\in C}
\frac{abc}{\operatorname{lcm}(a,b,c)}.
]

The harder part is counting which slice-toggle choices allow a fixed array to exist. This becomes a linear system over (\mathbb F_2). For each permutation cycle, only the parity of the toggles on that cycle matters. The number of actual toggle assignments corresponding to a chosen cycle parity is already absorbed into the total dimension of this system.

For a cell orbit coming from cycle lengths (a,b,c), let (L=\operatorname{lcm}(a,b,c)). The corresponding consistency equation contains the parity of the (a)-cycle exactly (L/a) times. Modulo two, this coefficient is one precisely when (L/a) is odd. That happens exactly when the cycle (a) has the largest power of two dividing its length among (a,b,c).

This means the linear algebra does not depend on the complete cycle lengths. It only depends on their 2-adic valuations. At a fixed valuation (v), let (x,y,z) be the numbers of cycles of exact valuation (v) in the three permutations. Constraints at this valuation are independent of all other valuations. If all three dimensions have usable cycles up to valuation (v), the rank contributed at this level is (x+y+z-2) when all three have cycles of valuation (v), (x+y-1) when exactly two dimensions do, and the number of cycles when only one dimension does.

The two pieces now combine cleanly. For a fixed triple of permutation cycle types, the sum of fixed arrays over all slice-toggle choices is

[
2^{m+n+p-r}\cdot 2^{Q},
]

where (r) is the rank of the parity constraints and (Q) is the number of cell orbits.

The brute-force approach works because it explicitly represents every orbit. It fails because there are astronomically many arrays. Burnside lets us count all those orbits at once, while cycle types compress the permutation space from factorially many permutations to at most 101 partitions per dimension.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^{mnp})) or worse | (O(2^{mnp})) | Too slow |
| Burnside with cycle types | (O(P(m)P(n)P(p)\cdot 13)) per distinct dimension triple | (O(P(13)^2\cdot13)) auxiliary | Accepted |

Here (P(k)) denotes the number of integer partitions of (k), with (P(13)=101). Since the answer is symmetric in the three dimensions, the implementation sorts every dimension triple before caching it. There are only (\binom{15}{3}=455) possible sorted triples.

## Algorithm Walkthrough

1. Generate every integer partition of every number from 1 through 13. For each partition, store its cycle lengths, the number of permutations having that cycle type, and how many cycles have each 2-adic valuation.

A partition such as (1+1+2) represents permutations containing two fixed points and one 2-cycle. Its multiplicity is

[
\frac{3!}{1^2,2^1,2!,1!}=3.
]
2. For every pair of cycle types that is needed, precompute

\sum_{a,b}
\text{cnt}_A[a]\text{cnt}_B[b]
\frac{abc}{\operatorname{lcm}(a,b,c)}
]

for every possible third cycle length (c).

Once this vector is known, the total number of cell orbits for a third cycle type is just

[
Q=\sum_c \text{cnt}_C[c]S[c].
]

This avoids repeatedly evaluating gcd and lcm operations inside the innermost loop.
3. For a triple of cycle types, compute the rank of the toggle consistency equations independently for valuations (v=0,1,2,3). No cycle length at most 13 has a larger 2-adic valuation than 3.

At valuation (v), first check whether each dimension contains at least one cycle of valuation at most (v). Otherwise no cell orbit can have (v) as its maximum valuation. If the level is active, count how many dimensions have at least one cycle of exact valuation (v), and add the corresponding rank contribution.
4. For each permutation cycle-type triple, multiply its three permutation multiplicities by

[
2^{m+n+p-r+Q}.
]

The exponent (m+n+p-r) counts all slice-toggle assignments satisfying the parity constraints, while (Q) counts the binary choices for the cells in the resulting cell orbits.
5. Sum these contributions over all cycle-type triples.
6. Divide the Burnside sum by

[
m!,n!,p!,2^{m+n+p}.
]

There is a small subtlety here. The slice toggles have a two-dimensional kernel: toggling every slice in two dimensions produces no change. Thus the actual toggle group has size (2^{m+n+p-2}). Our calculation deliberately sums over all (2^{m+n+p}) toggle descriptions, so every actual group element appears four times. The same factor of four appears in the numerator, which is why dividing by (2^{m+n+p}) is exactly correct.
7. Sort the three dimensions before evaluating the answer and cache the result. The operations treat the three axes symmetrically, so this does not change the answer and avoids repeating work across permutations of the same dimensions.

### Why it works

For every group element, Burnside requires its exact number of fixed arrays. The permutation part splits the cells into independent orbits. An array fixed by the element must be constant up to the prescribed toggle parity along every such orbit, giving (2^Q) choices once the toggle parities are consistent.

The consistency conditions depend on a cycle only through the parity of its slice toggles. The coefficient of that parity is odd exactly for cycles whose 2-adic valuation reaches the maximum valuation in the corresponding triple. Hence all constraints with the same maximum valuation form a separate linear system, and its rank is the complete bipartite or tripartite parity rank described above.

Thus every permutation triple contributes exactly the value used by the algorithm. Summing over all permutations through their cycle-type multiplicities gives the complete Burnside numerator, and the final division gives exactly the number of equivalence classes.

## Python Solution

```python
import sys
from math import gcd
from functools import lru_cache

input = sys.stdin.readline

MOD = 998244353
MAXN = 13
MAXCELLS = MAXN * MAXN * MAXN

fact = [1] * (MAXN + 1)
for i in range(1, MAXN + 1):
    fact[i] = fact[i - 1] * i % MOD

invfact = [1] * (MAXN + 1)
invfact[MAXN] = pow(fact[MAXN], MOD - 2, MOD)
for i in range(MAXN, 0, -1):
    invfact[i - 1] = invfact[i] * i % MOD

pow2 = [1] * (MAXCELLS + 1)
for i in range(1, MAXCELLS + 1):
    pow2[i] = pow2[i - 1] * 2 % MOD

invpow2 = [1] * (MAXCELLS + 1)
inv2 = (MOD + 1) // 2
for i in range(1, MAXCELLS + 1):
    invpow2[i] = invpow2[i - 1] * inv2 % MOD

def v2(x):
    return (x & -x).bit_length() - 1

# orbit3[a][b][c] is the number of cell orbits produced
# by one a-cycle, one b-cycle and one c-cycle.
orbit3 = [[[0] * (MAXN + 1) for _ in range(MAXN + 1)]
          for _ in range(MAXN + 1)]

for a in range(1, MAXN + 1):
    for b in range(1, MAXN + 1):
        ab = a * b // gcd(a, b)
        for c in range(1, MAXN + 1):
            l = ab * c // gcd(ab, c)
            orbit3[a][b][c] = a * b * c // l

class CycleType:
    __slots__ = ("n", "parts", "cnt", "vcnt", "weight", "cum")

    def __init__(self, n, parts, cnt):
        self.n = n
        self.parts = parts
        self.cnt = cnt

        vcnt = [0] * 4
        for length, number in cnt.items():
            vcnt[v2(length)] += number
        self.vcnt = tuple(vcnt)

        denom = 1
        for length, number in cnt.items():
            for _ in range(number):
                denom *= length
            denom *= fact[number]
        self.weight = fact[n] * pow(denom, MOD - 2, MOD) % MOD

        s = 0
        cum = []
        for x in vcnt:
            s += x
            cum.append(s)
        self.cum = tuple(cum)

def make_cycle_types(n):
    result = []

    def dfs(rem, last, parts):
        if rem == 0:
            cnt = {}
            for x in parts:
                cnt[x] = cnt.get(x, 0) + 1
            result.append(CycleType(n, tuple(parts), cnt))
            return

        for x in range(last, rem + 1):
            parts.append(x)
            dfs(rem - x, x, parts)
            parts.pop()

    dfs(n, 1, [])
    return result

types = [None] * (MAXN + 1)
for n in range(1, MAXN + 1):
    types[n] = make_cycle_types(n)

pair_orbit_cache = {}

def get_pair_orbits(A, B):
    key = (id(A), id(B))
    if key in pair_orbit_cache:
        return pair_orbit_cache[key]

    s = [0] * (MAXN + 1)

    for a in A.parts:
        ca = A.cnt[a]
        for b in B.parts:
            cb = B.cnt[b]
            mul = ca * cb
            row = orbit3[a][b]
            for c in range(1, MAXN + 1):
                s[c] += mul * row[c]

    pair_orbit_cache[key] = tuple(s)
    return pair_orbit_cache[key]

def rank_of(A, B, C):
    rank = 0

    for v in range(4):
        av = A.vcnt[v]
        bv = B.vcnt[v]
        cv = C.vcnt[v]

        if av == 0 and bv == 0 and cv == 0:
            continue

        # Every dimension must have some cycle of valuation <= v,
        # otherwise v cannot be the maximum valuation of a cell orbit.
        if A.cum[v] == 0 or B.cum[v] == 0 or C.cum[v] == 0:
            continue

        active_dimensions = (av > 0) + (bv > 0) + (cv > 0)
        total = av + bv + cv

        rank += total - active_dimensions + 1

    return rank

@lru_cache(maxsize=None)
def solve_dimension(n, m, p):
    n, m, p = sorted((n, m, p))

    total = 0

    for A in types[n]:
        wa = A.weight

        for B in types[m]:
            wb = B.weight
            s = get_pair_orbits(A, B)
            wab = wa * wb % MOD

            for C in types[p]:
                q = 0
                for c in C.parts:
                    q += C.cnt[c] * s[c]

                r = rank_of(A, B, C)

                contribution = pow2[n + m + p - r + q]
                contribution = contribution * wab % MOD
                contribution = contribution * C.weight % MOD

                total += contribution

    total %= MOD

    denominator_inverse = (
        invfact[n]
        * invfact[m]
        % MOD
        * invfact[p]
        % MOD
        * invpow2[n + m + p]
        % MOD
    )

    return total * denominator_inverse % MOD

def main():
    T = int(input())
    out = []

    for _ in range(T):
        n, m, p = map(int, input().split())
        out.append(str(solve_dimension(n, m, p)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The factorial arrays handle the multiplicity of permutation cycle types. For a cycle type with (c_l) cycles of length (l), its multiplicity is

[
\frac{n!}{\prod_l l^{c_l}c_l!}.
]

The `CycleType` object stores exactly the information needed by Burnside: its cycle lengths, their multiplicities, its permutation weight, and the number of cycles at each 2-adic valuation.

The `orbit3` table removes gcd and lcm work from the innermost enumeration. Its value is the number of orbits inside the product of three individual permutation cycles, which is the product of their sizes divided by the lcm of those sizes.

`get_pair_orbits` then combines two cycle types into a compact vector. Once this vector has been computed, selecting the third cycle type requires only a short weighted sum.

`rank_of` deliberately works with cumulative valuation counts. A valuation level can contribute constraints only when every dimension has at least one cycle whose valuation is no larger than that level. The expression `total - active_dimensions + 1` gives the rank of a complete one, two, or three-partite parity system.

Python integers do not overflow, but every combinatorial value is reduced modulo `998244353` after multiplication. The exponent of `pow2` is at most (mnp+m+n+p), well within the precomputed range.

The final inverse factor contains `invpow2[n+m+p]`, not `invpow2[n+m+p-2]`. The code enumerates all slice-toggle descriptions, including the four descriptions that represent the identity in the toggle subgroup. That fourfold redundancy is intentional and cancels against the corresponding factor in the Burnside numerator.

## Worked Examples

### Sample 1: `1 1 1`

There is only one cycle type in every dimension, namely a single cycle of length 1.

| Dimension | Cycle type | Permutation weight | 2-adic counts |
| --- | --- | --- | --- |
| 1 | `[1]` | 1 | (v_2=0:1) |
| 1 | `[1]` | 1 | (v_2=0:1) |
| 1 | `[1]` | 1 | (v_2=0:1) |

The single cell is one cell orbit, so (Q=1). At valuation zero all three dimensions participate, giving rank (1+1+1-2=1).

| Quantity | Value |
| --- | --- |
| (m+n+p) | 3 |
| (Q) | 1 |
| rank | 1 |
| fixed-array sum | (2^{3-1+1}=8) |
| denominator | (2^3=8) |
| answer | 1 |

The result is `1`, because the two possible single-cell arrays differ only by a toggle.

### Sample 2: `2 2 2`

For size 2, the two permutation cycle types are `[1,1]` and `[2]`, each with multiplicity 1.

| First dimension | Second dimension | Third dimension | Main effect |
| --- | --- | --- | --- |
| `[1,1]` | `[1,1]` | `[1,1]` | All cycles have valuation 0 |
| `[1,1]` | `[1,1]` | `[2]` | The third dimension has the larger valuation |
| `[1,1]` | `[2]` | `[1,1]` | The second dimension has the larger valuation |
| `[1,1]` | `[2]` | `[2]` | The two 2-cycles share the largest valuation |
| `[2]` | `[1,1]` | `[1,1]` | Symmetric to the second row |
| `[2]` | `[1,1]` | `[2]` | Symmetric to the fourth row |
| `[2]` | `[2]` | `[1,1]` | Symmetric to the fourth row |
| `[2]` | `[2]` | `[2]` | All three dimensions have valuation 1 |

The algorithm evaluates these eight cycle-type triples, multiplies each fixed-array count by its permutation multiplicity, and divides their sum by

[
2^{6}(2!)^3.
]

The resulting number of orbits is `9`, matching the official sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(P(n)P(m)P(p)\cdot13)) per uncached dimension triple | Each cycle-type triple needs a short orbit sum and four valuation levels |
| Space | (O(P(13)^2\cdot13)) | Cached pair orbit vectors plus all partition data |

Since (P(13)=101), even the largest individual case has at most (101^3) cycle-type triples. Sorting the dimensions makes the answer symmetric and caching prevents repeated work for identical dimension triples. The constraints are deliberately small enough that integer partitions replace the impossible enumeration of permutations and arrays.

## Test Cases

```python
# This test harness uses the solve_dimension function from the solution above.

def run(inp: str) -> str:
    data = list(map(int, inp.split()))
    t = data[0]
    pos = 1
    ans = []

    for _ in range(t):
        n, m, p = data[pos], data[pos + 1], data[pos + 2]
        pos += 3
        ans.append(str(solve_dimension(n, m, p)))

    return "\n".join(ans)

# Official samples
assert run("""1
1 1 1
""") == "1", "sample 1"

assert run("""1
2 2 2
""") == "9", "sample 2"

assert run("""1
2 3 4
""") == "723", "sample 3"

# Minimum size
assert run("""1
1 1 1
""") == "1", "minimum dimensions"

# Maximum allowed dimension, with the other two dimensions minimal.
# Every layer can be toggled independently, so all arrays are equivalent.
assert run("""1
1 1 13
""") == "1", "maximum single dimension"

# Boundary case where the answer is not 1.
# This exposes the invariant given by the parity of all four cells.
assert run("""1
1 2 2
""") == "2", "2x2 matrix parity"

# Another one-dimensional boundary case.
assert run("""1
1 1 2
""") == "1", "independent layer toggles"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | Minimum-size array and complete toggle equivalence |
| `1 1 13` | `1` | Maximum dimension bound and independent layer toggles |
| `1 2 2` | `2` | Non-trivial parity invariant when one dimension is 1 |
| `1 1 2` | `1` | Independent toggling of individual layers |
| `2 2 2` | `9` | Interaction between permutations, toggles, and 2-adic ranks |

## Edge Cases

For `1 1 1`, the algorithm has one cycle type in every dimension. Its cell-orbit count is (1), its parity rank is (1), and the Burnside numerator is (2^{3-1+1}=8). The denominator is also 8, so the result is exactly `1`.

For `1 1 2`, the first two dimensions contain one 1-cycle and the third dimension has either two 1-cycles or one 2-cycle. The toggle operations on the two individual layers already connect all four binary arrays. The Burnside calculation gives one orbit, so the answer is `1`. This case catches implementations that treat the layer permutation as the only operation.

For `1 2 2`, the two non-trivial dimensions form a binary (2\times2) matrix. Toggling one row or one column changes exactly two cells, so the parity of the total number of ones cannot change. Permuting rows or columns also preserves this parity. Both parity values occur, and every matrix of a fixed parity is equivalent under the allowed operations, giving exactly two classes. The cycle-type calculation produces `2`.

For the maximum allowed single dimension, `1 1 13`, every one of the 13 layers can be toggled independently. Starting from any binary vector, toggle exactly the layers containing one, obtaining the all-zero array. Hence every array is equivalent to every other one and the answer remains `1`. The algorithm handles this without a special case because the Burnside rank automatically accounts for all independent slice toggles.

The case `2 2 2` is the useful sanity check for the full machinery. It contains both odd-length cycles and even-length cycles, so the distinction between 2-adic valuations matters. Using only the number of cycles, without tracking whether their lengths are odd or even, gives the wrong fixed-array counts. The valuation-based rank calculation is precisely what separates these cases and produces the correct answer `9`.
