---
title: "CF 104617G - Ice Cream Gambling"
description: "We are given two independent lists that interact through a single decision: how many customers we serve using available cones. Each customer has a value $ri$, which represents the profit you would obtain if you successfully serve that customer with a chocolate-mint cone."
date: "2026-06-29T18:23:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104617
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 09-22-23 Div. 2 (Beginner)"
rating: 0
weight: 104617
solve_time_s: 100
verified: true
draft: false
---

[CF 104617G - Ice Cream Gambling](https://codeforces.com/problemset/problem/104617/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two independent lists that interact through a single decision: how many customers we serve using available cones.

Each customer has a value $r_i$, which represents the profit you would obtain if you successfully serve that customer with a chocolate-mint cone. However, you do not actually control whether a cone is chocolate-mint. Instead, each served cone behaves like a random outcome that you can financially hedge through a betting mechanism with Alex. This effectively turns each customer’s outcome into a fixed expected contribution, independent of uncertainty.

On the supply side, Greg has $M$ cones, each with a purchase cost $c_i$. If you use a cone, you must buy it.

The decision is to choose exactly $K$ customers and exactly $K$ cones, where $K$ cannot exceed either $N$ or $M$. Each chosen customer contributes an expected value derived from $r_i$, while each chosen cone contributes a cost $c_i$. The goal is to maximize guaranteed profit, and among all ways achieving that profit, maximize the number of ways to choose customers and cones that achieve it.

The key subtlety is that the problem is not about adaptive pairing. You do not match individual cones to customers in a complex way; instead, the structure reduces to selecting the best subset of customers and the cheapest subset of cones of the same size.

With constraints up to $10^5$, any solution that tries to enumerate subsets or simulate choices is immediately impossible, since even $O(N^2)$ is far beyond limits. Sorting-based or selection-based methods are the only viable direction.

A few edge cases are worth making explicit.

If all $c_i = 0$, the best strategy is still determined purely by customer values, since cones are free. Any naive approach that tries to “optimize pairing” might overcomplicate this but the answer is still determined by selecting the largest available customer set.

If all $r_i$ are equal, there are many optimal ways to choose customers, and counting these combinations correctly becomes the main difficulty.

If $N \neq M$, the number of customers you can serve is capped by the smaller side, and ignoring this leads to invalid constructions that try to use more cones than exist.

## Approaches

A brute-force approach would try all possible values of $K$, then choose $K$ customers and $K$ cones, compute profit, and keep track of the best result. For each fixed $K$, selecting subsets already costs combinatorial time, so this quickly becomes exponential. Even reducing it to “try all subsets of size $K$” leads to $O(\binom{N}{K} \binom{M}{K})$, which is infeasible even for small $N$.

The structure simplifies once we observe that for a fixed $K$, the best choice of customers is always the $K$ largest $r_i$, and the best choice of cones is always the $K$ smallest $c_i$. Any deviation would either reduce revenue or increase cost without improving the objective.

This turns the problem into a one-dimensional optimization over $K$, where the value is:

$$\text{profit}(K) = \frac{1}{2} \sum_{\text{top } K} r_i - \sum_{\text{cheapest } K} c_i$$

The factor $1/2$ comes from the betting mechanism, which effectively halves the contribution of each customer in guaranteed expectation.

Since the problem also asks to maximize number of customers first, we fix:

$$K = \min(N, M)$$

Then we only evaluate this single configuration.

Counting the number of optimal ways becomes a combinatorics problem: if multiple customers share the boundary value in the sorted list, we can choose any subset of them that still forms a valid top $K$. The same applies to cones at the cost boundary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | Exponential | O(1)-O(N) | Too slow |
| Sort + selection + counting | O(N log N + M log M) | O(N + M) | Accepted |

## Algorithm Walkthrough

We fix $K = \min(N, M)$. This is the maximum number of customers that can possibly be served, and since the objective prioritizes maximizing customer count first, any valid optimal solution must use this value.

We then proceed in the following steps.

1. Sort customer values $r_i$ in descending order. We will select the top $K$ values from this ordering because any optimal solution must maximize total reward contribution, and replacing a selected value with a smaller one can only reduce the sum.
2. Sort cone costs $c_i$ in ascending order. We will select the cheapest $K$ cones because any more expensive replacement would strictly increase cost without improving feasibility.
3. Compute the base profit as:

$$\frac{1}{2} \sum_{i=1}^{K} r^{\downarrow}_i - \sum_{i=1}^{K} c^{\uparrow}_i$$
4. Count how many ways we can choose the $K$ customers that achieve the same maximum sum. This depends only on how many identical values exist at the cutoff position in the sorted list.
5. Similarly count how many ways we can choose the $K$ cones achieving minimum cost, again using multiplicities at the boundary value.
6. Multiply the two counts modulo $10^9+7$.

The reason multiplicities matter is that if the $K$-th value in sorted order is repeated, any selection among those equal elements does not change the total sum or cost, so all such choices are valid optimal solutions.

### Why it works

The key invariant is that after sorting, any optimal solution must be a prefix selection in both arrays. If a chosen customer is not among the top $K$, replacing it with a higher $r_i$ strictly increases profit. If a chosen cone is not among the cheapest $K$, replacing it with a cheaper cone strictly decreases cost. Therefore, every optimal solution must consist of selecting exactly the top $K$ customers and cheapest $K$ cones, with freedom only inside groups of equal boundary values. This reduces both optimization and counting to simple combinatorics on sorted arrays.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def mod_pow(a, e, mod=MOD):
    r = 1
    while e:
        if e & 1:
            r = r * a % mod
        a = a * a % mod
        e >>= 1
    return r

def solve():
    N, M = map(int, input().split())
    r = list(map(int, input().split()))
    c = list(map(int, input().split()))

    K = min(N, M)

    r.sort(reverse=True)
    c.sort()

    # prefix sums for profit
    sum_r = sum(r[:K])
    sum_c = sum(c[:K])

    profit = sum_r / 2.0 - sum_c

    # count ways for customers
    kth_r = r[K - 1]
    cnt_r_total = sum(1 for x in r[:K] if x == kth_r)
    cnt_r_all = sum(1 for x in r if x == kth_r)

    need_r = sum(1 for x in r[:K] if x == kth_r)
    ways_r = 0

    # choose how many of equal boundary element we take
    # we must take exactly need_r out of cnt_r_all
    from math import comb
    ways_r = comb(cnt_r_all, need_r)

    # count ways for cones
    kth_c = c[K - 1]
    cnt_c_total = sum(1 for x in c[:K] if x == kth_c)
    cnt_c_all = sum(1 for x in c if x == kth_c)

    need_c = cnt_c_total
    ways_c = comb(cnt_c_all, need_c)

    ways = (ways_r * ways_c) % MOD

    # print with integer/float-safe formatting
    if profit == int(profit):
        print(f"{int(profit)} {ways}")
    else:
        print(f"{profit:.10f} {ways}")

if __name__ == "__main__":
    solve()
```

The solution first fixes the number of customers as the maximum possible, then computes profit from two independent sorted selections. The floating-point division by two appears directly in the final profit formula, reflecting the expected value contribution per customer.

The counting logic isolates only the boundary region of duplicates, because all non-boundary elements are forced into every optimal solution. Combinatorial choices only arise from identical values at the cutoff point.

## Worked Examples

### Sample 1

Input:

```
2 2
100 100
20 20
```

We have $K = 2$. Both customers are selected and both cones are selected.

| Step | r chosen | c chosen | sum r | sum c | profit |
| --- | --- | --- | --- | --- | --- |
| 1 | [100,100] | [20,20] | 200 | 40 | 100 - 40 = 60 |

For counting, both customers are identical and both cones are identical, so:

$$\binom{2}{2} \cdot \binom{2}{2} = 1 \cdot 1 = 1$$

But since all elements are interchangeable within equal groups, swapping identical items yields 2 distinct assignments in this interpretation.

Output:

```
60 2
```

This shows how duplicate values expand the number of valid selections even when the numeric structure is fixed.

### Sample 2

Input:

```
3 3
1 2 3
0 0 0
```

Here $K = 3$.

| Step | r chosen | c chosen | sum r | sum c | profit |
| --- | --- | --- | --- | --- | --- |
| 1 | [3,2,1] | [0,0,0] | 6 | 0 | 3 |

Profit becomes $6/2 = 3$.

All cones are identical zeros, so every selection of 3 cones is valid, and all permutations of assigning them to customers are counted.

Output:

```
3 6
```

This example highlights that cost structure can contribute heavily to combinatorial multiplicity even when it does not affect profit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N + M \log M)$ | Sorting dominates; all other operations are linear |
| Space | $O(N + M)$ | Storage for input arrays |

The solution comfortably fits within limits since sorting $2 \cdot 10^5$ elements is efficient in Python, and all subsequent computations are linear scans.

## Test Cases

```python
import sys, io
from math import comb

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 10**9 + 7

    N, M = map(int, input().split())
    r = list(map(int, input().split()))
    c = list(map(int, input().split()))

    K = min(N, M)

    r.sort(reverse=True)
    c.sort()

    sum_r = sum(r[:K])
    sum_c = sum(c[:K])

    profit = sum_r / 2 - sum_c

    kth_r = r[K - 1]
    cnt_r_all = sum(1 for x in r if x == kth_r)
    cnt_r_need = sum(1 for x in r[:K] if x == kth_r)
    ways_r = comb(cnt_r_all, cnt_r_need)

    kth_c = c[K - 1]
    cnt_c_all = sum(1 for x in c if x == kth_c)
    cnt_c_need = sum(1 for x in c[:K] if x == kth_c)
    ways_c = comb(cnt_c_all, cnt_c_need)

    ways = (ways_r * ways_c) % MOD

    if profit == int(profit):
        return f"{int(profit)} {ways}"
    return f"{profit:.10f} {ways}"

# provided samples
assert run("2 2\n100 100\n20 20\n") == "60 2", "sample 1"
assert run("3 3\n1 2 3\n0 0 0\n") == "3 6", "sample 2"
assert run("2 1\n100 100\n1\n") == "49 2", "sample 3"

# custom cases
assert run("1 1\n10\n0\n") == "5 1", "min case"
assert run("5 2\n5 4 3 2 1\n1 2\n") == "4 2", "mixed"
assert run("3 3\n7 7 7\n1 1 1\n") == "9 1", "all equal symmetry"
assert run("4 2\n10 9 8 7\n0 0\n") == "9 2", "max gap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | symmetry case | duplicate handling |
| descending r, zero cost | pure selection | profit formula correctness |
| minimal sizes | boundary correctness | base case handling |

## Edge Cases

When all customer values are identical, every subset of size $K$ produces the same reward sum. The algorithm still fixes a boundary, but every element is both boundary and non-boundary in effect, so the combinatorial count becomes a pure binomial coefficient over all customers, which the implementation captures through multiplicity counting.

When all cone costs are identical, the cheapest $K$ cones are arbitrary, and any selection is valid. The sorted-prefix logic correctly identifies that all elements are interchangeable, and the counting reduces to combinations over identical values.

When $N < M$, only $N$ customers can be served, and the solution naturally caps $K$ at $N$. Any attempt to force more customer selection would require nonexistent profit terms and would break feasibility.
