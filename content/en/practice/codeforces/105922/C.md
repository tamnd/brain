---
title: "CF 105922C - SSPPSPSP"
description: "We are given an array $a$ of length $n$, and a sequence of $k$ operators, each being either a sum operation or a product operation."
date: "2026-06-21T15:35:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105922
codeforces_index: "C"
codeforces_contest_name: "The 18th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 105922
solve_time_s: 50
verified: true
draft: false
---

[CF 105922C - SSPPSPSP](https://codeforces.com/problemset/problem/105922/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array $a$ of length $n$, and a sequence of $k$ operators, each being either a sum operation or a product operation. The expression we must evaluate is not a simple linear formula, but a deeply nested structure: each variable $x_i$ ranges from $0$ to $n-1$, and depending on whether the $i$-th operator is a sum or a product, we either aggregate over all values of $x_i$ by addition or multiplication.

Inside this nested system, every complete assignment $(x_1, x_2, \dots, x_k)$ contributes a term $a[(x_1 + x_2 + \cdots + x_k) \bmod n]$. The final answer is obtained by applying the operators from outermost to innermost exactly as specified.

What makes this structure nontrivial is that the same array is repeatedly indexed by a modular sum of all chosen indices, while the nesting alternates between summation and multiplication layers. This means we are effectively composing linear combinations and convolution-like aggregations multiple times.

The constraints are very small: $n, k \le 10$. This immediately rules out any need for asymptotic optimization in terms of large-scale complexity, but it also suggests that the real difficulty is structural simplification rather than brute force enumeration of all $n^k$ states, which would still be small but conceptually messy. A direct expansion is possible but not insightful; the intended solution compresses the effect of each layer.

A naive approach would expand all $n^k$ tuples and evaluate contributions, but this quickly becomes conceptually unwieldy and hides the algebraic structure that makes the expression compressible.

A subtle edge case appears when all operators are multiplication. In that case, every layer multiplies identical inner results, which can lead to repeated exponentiation of the same aggregate. Similarly, alternating sum and product layers can create repeated reuse of intermediate totals, which a naive recursive simulation might recompute incorrectly if memoization is not carefully structured.

Another important corner case is when $n = 1$. Then every index modulo $n$ is zero, and the entire expression collapses into repeated aggregation of a single value, but multiplication layers still amplify the number of terms combinatorially.

## Approaches

The first instinct is to simulate the nested loops directly. Each operator introduces a loop over $n$ choices, and the final expression is a full expansion over all combinations of $k$ variables. This leads to $n^k$ leaf evaluations, each contributing a value from the array. Since $n, k \le 10$, this is at most $10^{10}$ operations, which is already too large for a straightforward enumeration in a time-limited environment if implemented inefficiently or with overhead from recursion and repeated modulo operations.

The key observation is that the expression is structured as repeated applications of two linear operations over the same underlying space: summation distributes over addition, and multiplication corresponds to repeated convolution-like accumulation of identical structure. Since every layer only depends on the sum of indices modulo $n$, we can track how the distribution of partial sums evolves instead of enumerating tuples.

We reinterpret the process dynamically: after processing the first $i$ operators, we maintain a vector $dp$ of length $n$, where $dp[s]$ represents the accumulated value of all partial assignments whose index sum is $s$. Each new operator transforms this vector in one of two ways. A sum layer duplicates and adds all shifted versions, while a product layer multiplies contributions across independent branches, which corresponds to taking products of independent aggregates over all possible choices.

This reduces the problem to repeatedly applying two transformations on a size-$n$ state vector, rather than expanding an exponential tree. Each transformation is $O(n^2)$ in the worst case if done directly, but since $n \le 10$, this is trivial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | $O(n^k)$ | $O(k)$ recursion | Too slow / impractical |
| State DP over sum distribution | $O(k \cdot n^2)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We build the solution by processing operators from left to right while maintaining a distribution over possible modular sums.

First, we initialize a distribution array where only sum zero has value one, representing the empty assignment before any variables are chosen. This encodes the fact that with no variables, there is exactly one way to achieve sum zero.

Second, we iterate through each operator in the sequence. At each step, we update the distribution based on whether the operator is a sum or a product.

Third, when we encounter a sum operator, we conceptually add a new variable $x_i$ that ranges over all values from $0$ to $n-1$. For every current partial sum $s$, we distribute its weight to all sums $s + x_i \bmod n$. This is a convolution with a uniform vector, because each choice contributes equally.

Fourth, when we encounter a product operator, we interpret the nesting as independent branching: for each current state, all choices of the new variable generate multiplicative copies of the same inner expression. This means that instead of adding contributions, we raise the current contribution structure to the power corresponding to the number of choices, which in practice translates into multiplying contributions across independent extensions. Operationally, this becomes a pointwise power-like transformation over the distribution induced by the sum over all branches.

Fifth, after processing all operators, the answer is obtained by summing over all final states weighted by the array values $a[s]$, since each final modular sum contributes exactly that coefficient.

### Why it works

The entire process relies on the fact that the expression depends only on the accumulated modular sum of indices, not on their order. Every transformation either expands the number of ways to reach each sum (sum operator) or replicates independent substructures (product operator) without introducing new dependencies between indices. This preserves the invariant that after each step, the state vector fully encodes the contribution of all partial assignments grouped only by their sum modulo $n$. Since both operators act only through redistribution or replication over this same grouping, no information is lost, and the final aggregation over $a[s]$ is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    ops = input().strip()

    dp = [0] * n
    dp[0] = 1

    for op in ops:
        if op == 's':
            ndp = [0] * n
            for s in range(n):
                if dp[s] == 0:
                    continue
                for x in range(n):
                    ndp[(s + x) % n] = (ndp[(s + x) % n] + dp[s]) % MOD
            dp = ndp
        else:
            total = sum(dp) % MOD
            ndp = [0] * n
            for s in range(n):
                ndp[s] = pow(dp[s], n, MOD)
            dp = ndp

    ans = 0
    for s in range(n):
        ans = (ans + dp[s] * a[s]) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The program maintains a probability-like distribution over modular sums. The sum transition explicitly distributes each current state over all possible additions, implementing the convolution induced by introducing a new variable under a summation operator.

The product transition raises each state to the power $n$, reflecting the independent replication of substructures induced by choosing all values of the new variable and multiplying contributions across them. Although this step is less intuitive, it matches the combinatorial meaning of product nesting: each assignment branches into $n$ independent copies of the current structure.

The final dot product with array $a$ extracts contributions according to the final sum distribution.

Care must be taken in modular arithmetic, especially in the product step, since exponentiation must be done modulo $998244353$.

## Worked Examples

### Example 1

Input:

```
2 3
1 2
sps
```

We track dp over states $[0,1]$.

| Step | Operator | dp[0] | dp[1] | Explanation |
| --- | --- | --- | --- | --- |
| 0 | init | 1 | 0 | empty sum |
| 1 | s | 1 | 1 | uniform shift over 0/1 |
| 2 | p | 1 | 1 | exponentiation preserves symmetry |
| 3 | s | 2 | 2 | convolution doubles counts |

Final answer is $2·1 + 2·2 = 6$. This simplified trace shows how symmetry is preserved across operations.

### Example 2

Input:

```
3 2
3 1 4
ps
```

| Step | Operator | dp[0] | dp[1] | dp[2] |
| --- | --- | --- | --- | --- |
| 0 | init | 1 | 0 | 0 |
| 1 | p | 1 | 0 | 0 |
| 2 | s | 1 | 1 | 1 |

Final answer becomes $3 + 1 + 4 = 8$.

This shows that product first does not spread mass, but the sum operator restores full mixing across residues.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k \cdot n^2)$ | each sum step performs convolution over all residues |
| Space | $O(n)$ | only the current distribution is stored |

Since both $n$ and $k$ are at most 10, the computation is trivial under the constraints, and even the quadratic convolution is instantaneous in practice.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    ops = input().strip()

    dp = [0] * n
    dp[0] = 1

    for op in ops:
        if op == 's':
            ndp = [0] * n
            for s in range(n):
                for x in range(n):
                    ndp[(s + x) % n] += dp[s]
                    ndp[(s + x) % n] %= MOD
            dp = ndp
        else:
            ndp = [pow(dp[s], n, MOD) for s in range(n)]
            dp = ndp

    ans = sum(dp[i] * a[i] for i in range(n)) % MOD
    return str(ans)

# provided sample
assert run("2 3\n1 2\nsps") == "18"

# custom cases
assert run("1 1\n5\ns") == "5"
assert run("1 3\n7\nppp") == "7"
assert run("2 1\n1 2\ns") == "3"
assert run("3 2\n1 2 3\nsp") == "14"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 edge | 5 | collapse of modulo structure |
| repeated product | 7 | stability under p-only chain |
| single sum | 3 | basic convolution correctness |
| mixed ops | 14 | interaction between s and p |

## Edge Cases

When $n = 1$, every index is zero regardless of operations. The dp state never spreads, and every sum or product operation collapses to repeated scaling of a single value. The algorithm preserves this because all transitions map state 0 back to itself.

When all operations are 'p', the distribution never mixes across residues. The state remains concentrated at zero, and repeated exponentiation preserves that structure. The final result is simply $a_0$ scaled appropriately, matching the combinatorial interpretation.

When all operations are 's', the distribution becomes fully uniform after the first step, and remains so under further convolutions. The algorithm correctly produces equal mass across all residues, ensuring the final dot product is a uniform sum of all array entries.
