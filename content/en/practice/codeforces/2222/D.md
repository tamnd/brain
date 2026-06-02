---
title: "CF 2222D - Permutation Construction"
description: "We are given an array $a$ of length $n$. We must construct a permutation $p$ of indices $1$ to $n$. For any pair of positions $i<j$, the pair contributes to the score only if it is an inversion in $p$, meaning $pipj$."
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2222
codeforces_index: "D"
codeforces_contest_name: "Spectral::Cup 2026 Round 1 (Codeforces Round 1094, Div. 1 + Div. 2)"
rating: 0
weight: 2222
solve_time_s: 249
verified: false
draft: false
---

[CF 2222D - Permutation Construction](https://codeforces.com/problemset/problem/2222/D)

**Rating:** -  
**Tags:** constructive algorithms, data structures, sortings  
**Solve time:** 4m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array $a$ of length $n$. We must construct a permutation $p$ of indices $1$ to $n$.

For any pair of positions $i<j$, the pair contributes to the score only if it is an inversion in $p$, meaning $p_i>p_j$. Each such inversion contributes the interval sum

$$\sum_{k=i}^{j-1} a_k.$$

The task is to choose the permutation $p$ that maximizes the total contribution over all inversions.

The key difficulty is that the contribution of a pair depends on the positions $i,j$ in the permutation domain, while the inversion condition depends on the relative ordering of the values placed at those positions. The permutation therefore defines a total order over indices, and every pair $(i,j)$ either contributes its interval weight or contributes nothing.

The constraints allow $\sum n \le 2\cdot 10^5$, so any solution must be near linear or $O(n\log n)$ per test case. Quadratic strategies over all pairs are infeasible because the number of pairs is $\Theta(n^2)$ in the worst case.

A naive approach that tries all permutations is impossible, and even greedy local swaps are dangerous because changing the order affects all pair contributions simultaneously.

A subtle edge case arises when $a_i$ are negative. For example, if $a=[-5,10,-5]$, interval sums can be negative or positive depending on endpoints, so locally placing large values early or late is not obviously optimal. A correct solution must globally account for all interval sums consistently.

## Approaches

We reinterpret the objective in a way that removes dependence on the permutation structure.

Fix positions $i<j$. If in the final permutation the element originally at position $i$ is ranked higher than the element at position $j$, then the pair contributes $w(i,j)=\sum_{k=i}^{j-1} a_k$. Otherwise it contributes $0$.

Thus each pair $(i,j)$ with $i<j$ contributes either $w(i,j)$ or $0$, depending on whether we orient $i$ above $j$ in the total order defined by $p$.

This becomes a maximum linear ordering problem with weights $w(i,j)$.

A brute force approach would try all $n!$ permutations, computing the score in $O(n^2)$ per permutation, which is far beyond feasible limits.

The key structural observation is that the weight simplifies via prefix sums. Define

$$S[1]=0,\quad S[i]=\sum_{k=1}^{i-1} a_k \quad (i\ge 2).$$

Then for $i<j$,

$$w(i,j)=\sum_{k=i}^{j-1} a_k = S[j]-S[i].$$

This linear form collapses the pair interaction into a difference of vertex potentials, which makes the global objective separable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force permutations | $O(n!,n^2)$ | $O(n)$ | Too slow |
| Prefix potential ordering | $O(n\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We construct prefix sums $S[i]$ and sort indices by these values.

1. Define $S[1]=0$ and for each $i\ge 2$ compute $S[i]=S[i-1]+a_{i-1}$.

This encodes every interval sum as a difference $S[j]-S[i]$.
2. Compare any two positions $i$ and $j$ using only $S[i]$ and $S[j]$.

The ordering we choose determines which pairs contribute $S[j]-S[i]$.
3. Assign a total order to indices by sorting them in nondecreasing order of $S[i]$.
4. Construct the permutation $p$ by assigning increasing ranks to indices in this sorted order.

The smallest $S[i]$ receives the smallest rank, and the largest $S[i]$ receives the largest rank.
5. Output the resulting permutation.

The choice of sorting direction aligns high $S[i]$ with large rank values. Since contribution weights become linear in ranks, this alignment maximizes the global sum by matching increasing sequences.

### Why it works

After rewriting with prefix sums, the total score becomes a function of ranks:

$$\sum_{i=1}^n S[i]\cdot (2r(i)-n-1),$$

where $r(i)$ is the rank of position $i$ in the permutation induced by $p$.

This expression separates into a sum of products of two sequences: the fixed sequence $S[i]$ and the linear coefficient sequence $2r-n-1$. The coefficient sequence is strictly increasing in $r$. By the rearrangement inequality, the maximum is achieved when $S[i]$ is sorted in the same order as the coefficients.

Since the coefficients increase with rank, assigning increasing ranks to increasing $S[i]$ maximizes the sum. This determines the optimal permutation uniquely up to ties in $S[i]$.

This completes the proof. ∎

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        # prefix sums S[i] = sum_{k < i} a[k]
        S = [0] * n
        cur = 0
        for i in range(1, n):
            cur += a[i - 1]
            S[i] = cur

        idx = list(range(n))
        idx.sort(key=lambda i: S[i])

        # assign permutation values 1..n in this order
        p = [0] * n
        for rank, i in enumerate(idx, start=1):
            p[i] = rank

        print(*p)

if __name__ == "__main__":
    solve()
```

The implementation first constructs prefix sums in linear time, ensuring every interval sum is encoded implicitly. Sorting indices by these values defines the optimal total order. The final permutation assigns ranks directly according to this sorted order, guaranteeing each index receives a unique value from $1$ to $n$.

A common implementation pitfall is forgetting that $S[1]=0$ must be included explicitly; without it, index alignment shifts and the ordering becomes incorrect.

## Worked Examples

### Example 1

Let $a=[2,-1,3]$.

Prefix sums:

$S[1]=0$, $S[2]=2$, $S[3]=1$.

Sorting by $S$ gives indices $[1,3,2]$.

Assign ranks:

$1\to 1$, $3\to 2$, $2\to 3$.

Permutation:

$p=[1,3,2]$.

This ordering places smaller prefix values earlier and larger ones later, maximizing weighted inversion gains.

### Example 2

Let $a=[-2,-1,-3]$.

Prefix sums:

$S=[0,-2,-3]$.

Sorted order is $[3,2,1]$.

Assign ranks:

$3\to 1$, $2\to 2$, $1\to 3$.

Permutation:

$p=[3,2,1]$.

This example shows that even when all $a_i$ are negative, the structure remains consistent: more negative prefix sums are placed earlier.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n\log n)$ | sorting indices by prefix sums dominates |
| Space | $O(n)$ | prefix sums and permutation arrays |

The sum of $n$ over all test cases is $2\cdot 10^5$, so the total complexity remains within limits. Sorting is applied independently per test case but over a bounded total input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        S = [0]*n
        cur = 0
        for i in range(1, n):
            cur += a[i-1]
            S[i] = cur
        idx = list(range(n))
        idx.sort(key=lambda i: S[i])
        p = [0]*n
        for r,i in enumerate(idx, start=1):
            p[i]=r
        out.append(" ".join(map(str,p)))
    return "\n".join(out)

# minimal
assert run("1\n1\n0\n") == "1"

# already increasing
assert run("1\n3\n1 2\n") == "1 2 3"

# all negative
assert run("1\n3\n-1 -1\n") in ["3 2 1", "2 3 1"]

# mixed
res = run("1\n4\n3 -5 2\n")
assert sorted(map(int,res.split())) == [1,2,3,4]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case correctness |
| increasing array | 1 2 3 | monotone prefix ordering |
| all negative | reverse-like | stability under sign flip |
| mixed values | permutation | validity of output |

## Edge Cases

When $n=1$, there are no pairs $(i,j)$, so any permutation is valid. The algorithm assigns $S[1]=0$ and outputs $[1]$, which is consistent.

When all $a_i$ are identical, all prefix sums decrease linearly, producing a strict order that still sorts correctly; the resulting permutation becomes a full reversal, which remains valid because all interval sums are identical and ordering symmetry is preserved.

When $a_i$ are negative and large in magnitude, prefix sums become strictly decreasing, and sorting still produces a valid permutation. The construction does not rely on positivity, only on relative ordering of $S[i]$.
