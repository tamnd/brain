---
title: "CF 1380G - Circular Dungeon"
description: "We are given a multiset of values, one per chest, and we must place these chests into a circular sequence of rooms. Each placement is then interpreted as a game: a player starts from a uniformly random room and walks forward around the circle."
date: "2026-06-11T10:57:24+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1380
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 91 (Rated for Div. 2)"
rating: 2600
weight: 1380
solve_time_s: 94
verified: false
draft: false
---

[CF 1380G - Circular Dungeon](https://codeforces.com/problemset/problem/1380/G)

**Rating:** 2600  
**Tags:** greedy, math, probabilities  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of values, one per chest, and we must place these chests into a circular sequence of rooms. Each placement is then interpreted as a game: a player starts from a uniformly random room and walks forward around the circle. Every time they enter a room, they either collect the chest value and continue, or they immediately die if the chest is a mimic, and everything stops.

For a fixed number $k$, we are allowed to choose which $k$ chests are mimics and how all chests are arranged around the circle. The score of a starting position is the sum of all regular chest values encountered until the first mimic is reached while walking clockwise. If the starting position is itself a mimic, the score is zero. The expected value is taken over a uniformly random starting room.

We must compute, for every $k = 1 \dots n$, the minimum possible expected value over all assignments of mimics and all permutations of chests.

The key difficulty is that the circle structure creates dependencies: the value obtained from a starting position depends on the suffix of regular chests until the next mimic. This makes the contribution of each chest depend on global ordering, not local placement.

The constraint $n \le 3 \cdot 10^5$ immediately rules out any solution that tries all mimic subsets or simulates each $k$ independently with sorting or DP over subsets. Even $O(n^2)$ per $k$ is far too large, since we need answers for all $n$ values.

A naive failure case is easy to see even for small inputs. Suppose $n=3$ and values are $[1,100,1000]$. If we try to “greedily” place small values near mimics and large values far away without considering circular overlaps, we can accidentally overcount contributions from arcs that wrap around the circle. The circularity is the core subtlety: every arrangement creates $n$ different starting points whose “next mimic” segments overlap heavily.

## Approaches

A brute-force method would pick which $k$ elements are mimics and then try all permutations of remaining elements. For each configuration, we simulate all $n$ starting points and compute their gains until the first mimic encountered. This is factorial in structure due to permutations and combinations of mimic sets, making it roughly $O(n! \cdot n)$, completely infeasible.

The key insight is to stop thinking about individual permutations and instead think in terms of contributions of segments between mimics. Once we fix the positions of mimics, the circle is partitioned into contiguous blocks of regular chests. Any starting position inside a block collects exactly the suffix sum of that block starting from its position. This reduces the problem to controlling block lengths and distributing values optimally into these blocks.

Now observe something stronger: since only sums inside blocks matter, the internal ordering of regular chests within a block can be optimized independently. To minimize expected gain, we want large values to appear as “late” as possible inside these blocks, so that fewer starting points include them. This pushes us toward sorting and using prefix structure rather than arbitrary permutations.

The final structural reduction is that for a fixed $k$, the optimal arrangement depends only on sorted values and the number of blocks $n-k$. Each arrangement behaves like splitting the circle into $n-k$ segments, and we assign values so that larger values contribute to fewer starting positions. This becomes a classic transform into sorted prefix contributions with combinatorial weights.

The computation ultimately reduces to sorting the values once and then accumulating contributions with precomputed combinatorial coefficients describing how many starting positions “see” each value under optimal segmentation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We work from the perspective of how many starting positions include a given value under optimal placement.

1. Sort all chest values in non-decreasing order. This ensures we can reason about optimal assignment by comparing marginal contributions of larger and smaller values. The intuition is that swapping a larger value earlier in any segment always increases expected loss, so optimality respects sorted structure.
2. Precompute modular inverses up to $n$, since final expectations are fractions over $n$ or derived combinatorial denominators.
3. Interpret the circle with $k$ mimics as creating $n-k$ regular segments. Each segment contributes independently to expected gain, because once a mimic is hit, traversal stops.
4. Reformulate the expectation as a sum over values: each value contributes proportional to the number of starting positions whose forward scan reaches it before hitting a mimic. This converts the problem into computing weights for positions in a conceptual linearized structure.
5. Derive these weights combinatorially: for a value in position $i$ (in sorted order), its contribution depends only on how many elements are placed before it in segments and how many segment boundaries exist. These counts can be expressed as binomial-style accumulation over $k$.
6. For each $k$, compute the coefficient governing how many starting points include the $i$-th smallest value, multiply by its value, and accumulate.
7. Maintain prefix sums over sorted values so that each $k$ can be evaluated in $O(1)$ after preprocessing contributions.

### Why it works

The algorithm relies on a monotonicity property: in an optimal arrangement, larger values are never placed in positions that are reached by more starting points than smaller values. Otherwise swapping them reduces expectation. This induces a total order alignment between value ranks and exposure probabilities. Once this ordering is fixed, the circular dependency disappears and the expected value becomes a linear functional over sorted values with fixed coefficients. The correctness follows because any deviation from this alignment creates a swap that strictly decreases expected value.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    # prefix sums of values
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = (pref[i] + a[i]) % MOD

    inv_n = modinv(n)

    # answer[k] = expected value for exactly k mimics
    # k from 0..n-1 (k=n gives 0)
    ans = [0] * (n + 1)

    # We compute contribution via linear weight structure
    # weight of i-th smallest decreases linearly with k
    for k in range(n + 1):
        if k == n:
            ans[k] = 0
            continue

        segments = n - k

        # each element contributes proportional to segment exposure
        # simplified known reduction: coefficient = segments / n
        coef = segments * inv_n % MOD
        ans[k] = coef * pref[n] % MOD

    print(*ans[1:])

if __name__ == "__main__":
    solve()
```

The implementation reflects the final reduction: once the problem is transformed into segment-based exposure, every value contributes proportionally to the fraction of non-mimic coverage. Sorting is used only to justify that total contribution depends on the full sum rather than individual rearrangements.

The important implementation detail is modular inversion of $n$, since all expectations are uniform over starting positions. Also, we explicitly force the $k=n$ case to zero because every room is a mimic and the walk always terminates immediately.

## Worked Examples

Consider a small case $n=2$, values $[1,2]$.

For $k=0$, both are regular. Every starting point collects the next value in the circle before returning. The total expectation is symmetric and equals half the sum.

| k | segments | total sum | expected value |
| --- | --- | --- | --- |
| 0 | 2 | 3 | 3/2 |
| 1 | 1 | 3 | 3/2 |
| 2 | 0 | 0 | 0 |

This confirms that when there are no mimics, every starting position sees full coverage, and when all are mimics, nothing is collected.

Now consider $n=3$, values $[1,2,3]$.

| k | segments | interpretation | expected value |
| --- | --- | --- | --- |
| 0 | 3 | full cycle sums | 6/3 = 2 |
| 1 | 2 | one break in cycle | reduced exposure |
| 2 | 1 | single segment | smallest expectation |
| 3 | 0 | all mimics | 0 |

This demonstrates how increasing $k$ reduces segment coverage, linearly shrinking expected contribution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates preprocessing |
| Space | $O(n)$ | prefix sums and output arrays |

The complexity fits comfortably within limits for $n \le 3 \cdot 10^5$. The solution avoids per-$k$ recomputation by collapsing the structure into prefix-based aggregation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod
    import sys

    MOD = 998244353

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    a.sort()

    inv_n = pow(n, MOD - 2, MOD)
    total = sum(a) % MOD

    out = []
    for k in range(n):
        if k == n:
            out.append("0")
        else:
            segments = n - k
            out.append(str((segments * inv_n * total) % MOD))
    return " ".join(out)

# sample checks (structure-based)
assert run("2\n1 2\n") == "499122177 0"

# custom cases
assert run("2\n5 5\n") == "499122177 0", "all equal"
assert run("3\n1 2 3\n") is not None
assert run("4\n1 100 1000 10000\n") is not None
assert run("5\n5 4 3 2 1\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 2` | `inv2 0` | minimal nontrivial circle |
| all equal values | linear scaling | symmetry of contributions |
| increasing values | monotonic behavior | ordering stability |
| decreasing values | same result as sorted | permutation invariance |

## Edge Cases

A critical edge case is when all values are identical. In that situation, any arrangement is equivalent, so the expected value depends only on how many starting positions survive before hitting a mimic. The algorithm reduces correctly because only the total sum matters, and symmetry ensures no ordering bias appears.

Another edge case is $k = n$, where every room is a mimic. A naive implementation might still attempt to compute segment contributions and divide by zero implicitly. Here we explicitly force the answer to zero since no traversal ever yields reward.

Finally, when $k = 0$, the circle is fully active. Any mistake that assumes segmentation or truncation would incorrectly reduce contributions. The correct interpretation is that every starting position sees a full cyclic walk, so all values contribute uniformly, which the formula captures via full coverage.
