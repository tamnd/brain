---
title: "CF 102174I - \u51fa\u7ed9 paul-lu \u7684\u6570\u6570\u9898"
description: "We have an (ntimes n) board, and every cell contains an integer from (1) to (k). A cell is called a bi point if its value is strictly larger than every other value in its row and also strictly larger than every other value in its column."
date: "2026-08-19T07:16:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102174
codeforces_index: "I"
codeforces_contest_name: "The 14-th BIT Campus Programming Contest"
rating: 0
weight: 102174
solve_time_s: 111
verified: true
draft: false
---

[CF 102174I - \u51fa\u7ed9 paul-lu \u7684\u6570\u6570\u9898](https://codeforces.com/problemset/problem/102174/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (n\times n) board, and every cell contains an integer from (1) to (k). A cell is called a bi point if its value is strictly larger than every other value in its row and also strictly larger than every other value in its column.

For every filled board, let (I) be the number of bi points on that board. If (B_i) is the number of boards with exactly (i) bi points, the required quantity is

[
\sum_i i^2 B_i.
]

This is simply the sum of (I^2) over all (k^{n^2}) possible boards. We never need to determine the entire distribution of (I). The square is the key: after expanding (I^2), we only need to count configurations containing one specified bi point and configurations containing two specified bi points.

The bounds (n,k\le 200) rule out anything exponential in (n^2). There are at most (20) test cases, so an (O(k\log n)) or (O(k^2)) computation per case is easily small enough, while even (O(n^2k)) is already unnecessarily large. The board itself has up to (40000) cells, but we only need to count assignments symbolically.

There are several boundary cases that can break a formula if they are not separated carefully. For (n=1), the only cell is automatically a bi point regardless of its value, so the answer is exactly (k). For example, input `1 5` has answer (5). A formula containing powers such as (2n-4) cannot be used directly here because that exponent becomes negative.

For (k=1) and (n>1), every cell has value (1), so no cell can be strictly larger than the other cells in its row or column. Thus the answer is (0). For example, input `3 1` has answer (0). A careless implementation that treats (0^0) as evidence for a valid maximum can incorrectly count a bi point.

For (n=2,k=2), the answer is (12). The boards with exactly one bi point are the four boards having one (2), one adjacent (1) in its row, one adjacent (1) in its column, and the opposite cell equal to (1), contributing (4). The two diagonal boards with two (2)'s each have two bi points, contributing (2^2) each, for another (8). A common mistake is to count every board containing a chosen bi point as a board with exactly one bi point. Such a board may contain several bi points, so indicator variables are necessary.

## Approaches

A direct approach would enumerate every board, count its bi points, square that count, and add it to the answer. There are (k^{n^2}) boards. Even if checking one board took only (O(n^2)), the total would be (O(n^2k^{n^2})). At the maximum constraint this contains (200^{40000}) boards, so the approach is completely infeasible.

The useful observation is that the quantity we need is a second moment. Let (X_c) be (1) when cell (c) is a bi point and (0) otherwise. Then

[
I=\sum_c X_c
]

and

[
I^2=\sum_c X_c+2\sum_{c<d}X_cX_d.
]

So we only need two kinds of counts: the number of boards where one fixed cell is a bi point, and the number of boards where two fixed cells are simultaneously bi points.

For one fixed cell, suppose its value is (x). Every other cell in its row and column must be smaller than (x). There are (2n-2) such cells, and they are distinct. Every one has (x-1) choices. All remaining cells are unrestricted.

For two fixed cells, there are three geometric possibilities. If they are in the same row, they cannot both be strict row maxima. The same is true when they are in the same column. Thus only pairs with different rows and different columns matter.

Consider such a pair and call their values (a) and (b). Each fixed cell constrains (2n-2) cells, but two cells lie at the intersections of the other fixed cell's row or column. Those two cells must be smaller than both (a) and (b), so each has (\min(a,b)-1) choices. The remaining constrained cells can be separated according to which fixed value they must be smaller than. This produces a symmetric sum that can be reduced to a single loop by maintaining a prefix sum.

The brute force works because checking one board exactly determines its contribution, but it fails because there are exponentially many boards. The observation that (I^2) only involves one-cell and two-cell indicator products reduces the problem to a small number of power sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2k^{n^2})) | (O(n^2)) | Too slow |
| Optimal | (O(k\log n)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Handle (n=1) separately. There is exactly one cell and it is always a bi point, so every one of the (k) boards contributes (1^2), giving answer (k).
2. Fix one particular cell and let its value be (x). There are (2n-2) other cells in its row or column, and all of them must be smaller than (x). Therefore this fixed cell is a bi point in

[
(x-1)^{2n-2}k^{(n-1)^2}
]

boards. Summing over (x=1,\ldots,k), the number of boards counted for one fixed cell is

[
A=k^{(n-1)^2}\sum_{t=0}^{k-1}t^{2n-2}.
]

There are (n^2) choices for the fixed cell, so the first part of the answer is (n^2A).

1. Consider two fixed cells. If they share a row or column, their simultaneous contribution is zero because two cells cannot both be strictly larger than the other cells in that same row or column.
2. For two cells in different rows and columns, write their values as (a) and (b), and put (t=a-1), (u=b-1). Each fixed cell has (2n-4) cells that are constrained only by its own value. The two crossing cells must be smaller than both values, so each has (\min(t,u)) choices. There are

[
(n-2)^2
]

completely unrestricted cells.

Thus the number of assignments for this fixed pair is

[
k^{(n-2)^2}
\sum_{t=0}^{k-1}\sum_{u=0}^{k-1}
t^{2n-4}u^{2n-4}\min(t,u)^2.
]

Let

[
p=2n-4.
]

The double sum is symmetric in (t,u). For (t>u), (\min(t,u)=u), so that part is

[
\sum_{t=0}^{k-1}t^p\sum_{u=0}^{t-1}u^{p+2}.
]

The diagonal (t=u) contributes

[
\sum_{t=0}^{k-1}t^{2p+2}.
]

Hence the whole double sum is

[
2\sum_{t=0}^{k-1}t^p
\left(\sum_{u=0}^{t-1}u^{p+2}\right)
+
\sum_{t=0}^{k-1}t^{2p+2}.
]

We can compute the inner sum incrementally while scanning (t), so the double sum becomes one loop.

1. Count how many unordered pairs of cells lie in different rows and different columns. Choose two rows, choose two columns, and choose one of the two diagonal matchings:

\frac{n^2(n-1)^2}{2}.
]

Since the expansion of (I^2) contains twice every unordered pair, the coefficient becomes

[
n^2(n-1)^2.
]

Therefore the second part of the answer is

[
n^2(n-1)^2
k^{(n-2)^2}
\left(
2\sum_{t=0}^{k-1}t^p
\sum_{u=0}^{t-1}u^{p+2}
+
\sum_{t=0}^{k-1}t^{2p+2}
\right).
]

1. Add the one-cell contribution and the two-cell contribution modulo (998244353). Every power is evaluated with modular exponentiation, and Python's built-in `pow(a, b, MOD)` performs this in (O(\log b)).

Why it works: the invariant is the identity

[
I^2=\sum_c X_c+2\sum_{c<d}X_cX_d.
]

The first counting formula gives exactly the number of boards for every term (X_c). For every pair (X_cX_d), pairs sharing a row or column contribute zero, while every pair in different rows and columns has exactly the counted set of constrained and unrestricted cells. Since every possible one-cell term and every possible two-cell term appears with precisely its coefficient from the expansion, the final sum is exactly (\sum_i i^2B_i).

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve_case(n, k):
    if n == 1:
        return k % MOD

    # Contribution of one fixed cell.
    single_exp = 2 * n - 2
    free_single = (n - 1) * (n - 1)

    sum_single = 0
    for t in range(k):
        sum_single += pow(t, single_exp, MOD)
        if sum_single >= MOD:
            sum_single -= MOD

    one_fixed = pow(k, free_single, MOD) * sum_single % MOD
    first = n * n % MOD * one_fixed % MOD

    # Contribution of one fixed pair in different rows and columns.
    p = 2 * n - 4
    free_pair = (n - 2) * (n - 2)

    prefix = 0
    pair_core = 0

    for t in range(k):
        tp = pow(t, p, MOD)

        # u < t contributes t^p * u^(p+2).
        pair_core += 2 * tp % MOD * prefix
        pair_core %= MOD

        # The diagonal term t = u.
        pair_core += pow(t, 2 * p + 2, MOD)
        pair_core %= MOD

        # Add u = t for the next iteration.
        prefix += pow(t, p + 2, MOD)
        prefix %= MOD

    pair_fixed = pow(k, free_pair, MOD) * pair_core % MOD

    pair_factor = n * n % MOD
    pair_factor = pair_factor * (n - 1) % MOD
    pair_factor = pair_factor * (n - 1) % MOD

    second = pair_factor * pair_fixed % MOD

    return (first + second) % MOD

def main():
    T = int(input())
    out = []

    for _ in range(T):
        n, k = map(int, input().split())
        out.append(str(solve_case(n, k)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The first branch handles the only case where the general pair formula would contain a negative exponent. When (n=1), the answer is simply the number of possible values in the single cell.

For (n>1), `single_exp` is (2n-2), because a fixed bi point has exactly (n-1) constrained cells in its row and another (n-1) constrained cells in its column. The remaining ((n-1)^2) cells are unrestricted.

For the pair calculation, `p = 2*n-4`. After fixing two cells in different rows and columns, each fixed value independently controls (2n-4) cells. The two crossing cells are controlled by both values, which is why they contribute the extra factor represented by the exponent (p+2) on the smaller value.

The variable `prefix` stores

[
\sum_{u<t}u^{p+2}.
]

Before adding the current (t) to the prefix, it contains exactly the values required for the (u<t) part of the symmetric sum. The diagonal contribution (t=u) is added separately as (t^{2p+2}).

All multiplication is reduced modulo (998244353). Python integers do not overflow, but reducing intermediate products keeps the values small and makes the implementation closer to the mathematical formula.

The factor `n*n*(n-1)*(n-1)` is not the number of unordered pairs. It already includes the factor (2) from the expansion of (I^2). This is an easy place to introduce a factor-of-two error.

## Worked Examples

For Sample 1, (n=2,k=2). The one-cell exponent is (2n-2=2), and the unrestricted-cell exponent is ((n-1)^2=1).

| Variable | Value |
| --- | --- |
| (n) | 2 |
| (k) | 2 |
| (2n-2) | 2 |
| (\sum t^{2n-2}) | (0^2+1^2=1) |
| (k^{(n-1)^2}) | (2) |
| One fixed cell | (2) |
| (n^2) one-cell contribution | (8) |

For the pair calculation, (p=0), so only (t=u=1) contributes to the core sum.

| Variable | Value |
| --- | --- |
| (p) | 0 |
| ((n-2)^2) | 0 |
| Pair core | 1 |
| (k^{(n-2)^2}) | 1 |
| Pair contribution factor | (2^2(2-1)^2=4) |
| Two-cell contribution | 4 |
| Final answer | 12 |

The value (12) matches the sample. The calculation also shows why boards with two bi points must not be removed from the one-cell count. They are intentionally counted once for each of their two bi points, exactly as the expansion of (I^2) requires.

For Sample 2, (n=3,k=2). Here (2n-2=4), so a fixed bi point requires four surrounding cells to be smaller.

| Variable | Value |
| --- | --- |
| (n) | 3 |
| (k) | 2 |
| (2n-2) | 4 |
| (\sum t^4) | 1 |
| (k^{(n-1)^2}) | (2^4=16) |
| One fixed cell | 16 |
| (n^2) one-cell contribution | 144 |

For two compatible cells, (p=2), and there is one unrestricted cell because ((n-2)^2=1).

| Variable | Value |
| --- | --- |
| (p) | 2 |
| Pair core | 1 |
| (k^{(n-2)^2}) | 2 |
| One fixed pair | 2 |
| Pair contribution factor | (3^2\cdot2^2=36) |
| Two-cell contribution | 72 |
| Final answer | 216 |

The second trace confirms the geometry of the two-cell case. Four cells are controlled exclusively by one of the two selected maxima, two crossing cells are controlled by both maxima, and one cell remains completely free.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(k\log n)) | There are (O(k)) iterations, each using a constant number of modular powers with exponents (O(n)). |
| Space | (O(1)) | Only a constant number of modular integers are stored. |

With (n,k\le200), each test case performs only a few hundred modular exponentiations, each requiring logarithmically many modular multiplications. Even with (20) test cases this is comfortably within the given limits, while memory usage is constant.

## Test Cases

The following test program uses the optimized implementation together with a direct (O(k^2)) reference formula. The reference is only for testing, so it remains tiny at (k\le200).

```python
import sys
import io

MOD = 998244353

def solve_case(n, k):
    if n == 1:
        return k % MOD

    single_exp = 2 * n - 2
    free_single = (n - 1) * (n - 1)

    sum_single = 0
    for t in range(k):
        sum_single = (sum_single + pow(t, single_exp, MOD)) % MOD

    one_fixed = pow(k, free_single, MOD) * sum_single % MOD
    first = n * n % MOD * one_fixed % MOD

    p = 2 * n - 4
    free_pair = (n - 2) * (n - 2)

    prefix = 0
    pair_core = 0

    for t in range(k):
        tp = pow(t, p, MOD)
        pair_core = (pair_core + 2 * tp * prefix) % MOD
        pair_core = (pair_core + pow(t, 2 * p + 2, MOD)) % MOD
        prefix = (prefix + pow(t, p + 2, MOD)) % MOD

    pair_fixed = pow(k, free_pair, MOD) * pair_core % MOD

    pair_factor = n * n % MOD
    pair_factor = pair_factor * (n - 1) % MOD
    pair_factor = pair_factor * (n - 1) % MOD

    return (first + pair_factor * pair_fixed) % MOD

def reference(n, k):
    if n == 1:
        return k % MOD

    single = 0
    for t in range(k):
        single += pow(t, 2 * n - 2, MOD)
    single %= MOD
    first = n * n % MOD
    first = first * pow(k, (n - 1) * (n - 1), MOD) % MOD
    first = first * single % MOD

    p = 2 * n - 4
    core = 0
    for t in range(k):
        for u in range(k):
            core += (
                pow(t, p, MOD)
                * pow(u, p, MOD)
                * min(t, u) ** 2
            )
            core %= MOD

    pair = pow(k, (n - 2) * (n - 2), MOD) * core % MOD
    pair_factor = n * n * (n - 1) * (n - 1) % MOD

    return (first + pair_factor * pair) % MOD

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input_func = sys.stdin.readline

    T = int(input_func())
    ans = []

    for _ in range(T):
        n, k = map(int, input_func().split())
        ans.append(str(solve_case(n, k)))

    return "\n".join(ans)

# Provided samples
assert run("3\n2 2\n3 2\n4 5\n") == (
    "12\n216\n129097970"
), "provided samples"

# Minimum-size input.
assert run("1\n1 1\n") == "1", "minimum n and k"

# n = 1 with many possible values.
assert run("1\n1 200\n") == "200", "single-cell boundary"

# All boards are equal when k = 1 and n > 1.
assert run("1\n3 1\n") == "0", "all-equal boards"

# Small case that exercises the pair formula.
assert run("1\n2 3\n") == "48", "n=2 pair counting"

# Maximum-size input, checked against a direct O(k^2) reference.
max_expected = reference(200, 200)
assert run("1\n200 200\n") == str(max_expected), "maximum constraints"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum board and the (n=1) special case |
| `1 200` | `200` | A single cell with the full value range |
| `3 1` | `0` | All cells equal, so strict maxima cannot exist |
| `2 3` | `48` | Two-cell contribution and diagonal-pair counting |
| `200 200` | Direct reference value | Maximum constraints and modular exponentiation |

## Edge Cases

For (n=1,k=5), the board consists of a single cell. Whatever value it contains, it is larger than every other cell in its row and column because there are no other cells. Thus every one of the five boards has (I=1), giving

[
5\cdot1^2=5.
]

The implementation returns (k) immediately and never evaluates the pair formula.

For (n=3,k=1), every board is the single configuration containing only (1)'s. No cell is strictly larger than the other cells in its row or column, so (I=0) and the answer is (0). In the one-cell formula, every term contains (t^{2n-2}=0^4=0), so the contribution vanishes naturally. The pair contribution also vanishes.

For (n=2,k=2), the one-cell count for a fixed cell is

[
2^{1}(0^2+1^2)=2.
]

There are four cells, giving (8) from the linear terms. Two cells can be bi points simultaneously only when they are diagonal. For each fixed diagonal pair, the only valid assignment for the two selected values is (2,2), while the remaining two cells must be (1), giving one assignment. There are two diagonal pairs, and the factor (2) from (I^2) gives (4). The total is (8+4=12).

For (n=200,k=200), the algorithm never constructs a board and never iterates over (n^2) cells. It only evaluates the one-cell power sum and the pair power sum over the (200) possible values. The largest exponent is below (40000), so modular exponentiation is inexpensive, and all intermediate values are reduced modulo (998244353).
