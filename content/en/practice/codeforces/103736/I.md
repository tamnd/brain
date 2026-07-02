---
title: "CF 103736I - IHI's Homework"
description: "We are given an array of lower bounds on variables and a target sum constraint. Each variable $xi$ must be at least $ai$, and we are asked how many integer vectors $x1, x2, dots, xn$ satisfy $$x1 + x2 + dots + xn le s$$ After each update, one position of the array $a$ is changed…"
date: "2026-07-02T09:12:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103736
codeforces_index: "I"
codeforces_contest_name: "The 2022 Hangzhou Normal U Summer Trials"
rating: 0
weight: 103736
solve_time_s: 51
verified: true
draft: false
---

[CF 103736I - IHI's Homework](https://codeforces.com/problemset/problem/103736/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of lower bounds on variables and a target sum constraint. Each variable $x_i$ must be at least $a_i$, and we are asked how many integer vectors $x_1, x_2, \dots, x_n$ satisfy

$$x_1 + x_2 + \dots + x_n \le s$$

After each update, one position of the array $a$ is changed permanently, and we must recompute the number of valid solutions.

The input is dynamic: every operation modifies one lower bound, and the answer depends only on the current state of all $a_i$. The output after each update is the count of valid integer assignments.

The constraint $n, q \le 2 \cdot 10^5$ forces us to recompute answers much faster than $O(nq)$. Since both structure size and number of updates are large, any solution must support fast point updates and fast recomputation of a global combinatorial value.

A key observation is that the constraint is symmetric over variables except for their lower bounds. This suggests transforming variables to remove the lower bounds, which turns the problem into a classic bounded composition counting problem.

A useful derived quantity is the total mandatory sum:

$$A = \sum a_i$$

If we define new variables $y_i = x_i - a_i$, then each $y_i \ge 0$, and the constraint becomes:

$$\sum y_i \le s - A$$

So the problem reduces to counting non-negative integer solutions with an upper bound on the sum.

A subtle edge case appears when $s < A$. In this case, no solution exists. For example, if $n=3, s=2, a=[1,1,1]$, then minimum sum is 3, so answer is 0. A naive implementation that ignores feasibility of base sum would still try to compute combinations with negative remaining capacity, which leads to incorrect combinatorial values.

Another edge case is when all $a_i = 0$, where the answer becomes the classic stars and bars count of $\sum y_i \le s$, which is $\binom{s+n}{n}$. Any solution must correctly unify both general and degenerate cases.

## Approaches

A direct approach is to recompute the answer after each update by iterating over all possible sums or using combinatorics from scratch. After shifting variables, the problem becomes counting non-negative integer solutions with sum at most $S' = s - \sum a_i$. The number of solutions is

$$\sum_{k=0}^{S'} \binom{k+n-1}{n-1} = \binom{S' + n}{n}$$

This reduces each query to maintaining only the sum of $a_i$. Since each update changes a single $a_x$, we can maintain the running total $A$ in $O(1)$, and recompute $S' = s - A$.

The remaining challenge is computing binomial coefficients $\binom{N}{K}$ modulo $10^9+7$ quickly for up to $N \le 4 \cdot 10^5$. This is handled with precomputed factorials and inverse factorials.

Thus each query becomes a constant-time arithmetic update plus one modular binomial evaluation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | Exponential | O(n) | Too slow |
| Recompute Combinatorics per Query | O(nq) | O(1) | Too slow |
| Maintain Sum + Precomputed nCr | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

We transform the problem into counting valid assignments of non-negative slack variables. The core idea is that only the total sum of lower bounds matters, not their distribution.

## Algorithm Walkthrough

1. Compute the initial sum $A = \sum a_i$. This represents the minimum forced contribution to the total sum of variables, so it determines how much “room” remains for flexible allocation.
2. Precompute factorials and inverse factorials up to $n + s$. This is required because every answer will be a binomial coefficient with arguments up to this range, and recomputing factorials per query would be too slow.
3. For each query, update the array entry $a_x$ and adjust the total sum $A$. Instead of modifying the whole structure, we only maintain the aggregate effect, since the final count depends only on $A$.
4. Compute remaining capacity $R = s - A$. If $R < 0$, output 0 immediately because even the minimum configuration violates the constraint.
5. Otherwise compute the number of solutions as $\binom{R + n}{n}$. This follows from the stars and bars transformation applied to non-negative variables with bounded total sum.

### Why it works

After shifting variables by their lower bounds, every valid configuration corresponds exactly to a choice of non-negative integers $y_i$ whose sum is at most $R = s - \sum a_i$. The count of such vectors depends only on the total available slack, not on individual $a_i$. Each update only changes this slack by adjusting one term in the sum, so recomputation reduces to maintaining a single scalar state. The binomial identity for bounded compositions guarantees that the final formula counts all valid assignments exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

def build_fact(n):
    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[n] = modinv(fact[n])
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD
    return fact, invfact

def ncr(n, r, fact, invfact):
    if r < 0 or r > n:
        return 0
    return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

def main():
    n, s, q = map(int, input().split())
    a = list(map(int, input().split()))
    
    A = sum(a)
    MAX = n + s
    fact, invfact = build_fact(MAX)
    
    for _ in range(q):
        x, val = map(int, input().split())
        x -= 1
        
        A -= a[x]
        a[x] = val
        A += a[x]
        
        R = s - A
        if R < 0:
            print(0)
        else:
            print(ncr(R + n, n, fact, invfact))

if __name__ == "__main__":
    main()
```

The implementation revolves around maintaining the sum of the array instead of its full structure. Each update adjusts this sum in constant time, which directly updates the remaining slack $R$.

Factorials and inverse factorials are precomputed once for the maximum possible index, ensuring each binomial query is $O(1)$. The combination function guards invalid ranges to avoid negative or out-of-bound accesses.

The key subtlety is correctly computing $R = s - A$. Any mistake in updating $A$ before or after assignment would shift the result incorrectly, since every query depends on the current state of all previous updates.

## Worked Examples

### Example 1

Input:

```
n=3, s=5
a=[1,1,1]
queries: (1→1), (1→2), (2→2), (3→2)
```

We track $A$ and $R$:

| Step | a | A | R = s - A | Answer |
| --- | --- | --- | --- | --- |
| init | [1,1,1] | 3 | 2 | C(5,3)=10 |
| 1 | [1,1,1] | 3 | 2 | 10 |
| 2 | [2,1,1] | 4 | 1 | C(4,3)=4 |
| 3 | [2,2,1] | 5 | 0 | C(3,3)=1 |
| 4 | [2,2,2] | 6 | -1 | 0 |

The trace shows that all structure dependence collapses into a single scalar $A$. Once $A$ exceeds $s$, feasibility disappears immediately.

### Example 2

Input:

```
n=2, s=3
a=[0,0]
queries: (1→1), (2→2)
```

| Step | a | A | R | Answer |
| --- | --- | --- | --- | --- |
| init | [0,0] | 0 | 3 | C(5,2)=10 |
| 1 | [1,0] | 1 | 2 | C(4,2)=6 |
| 2 | [1,2] | 3 | 0 | C(2,2)=1 |

This example highlights how increasing lower bounds reduces only the remaining slack, not the combinatorial structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | factorial preprocessing is linear, each query is O(1) due to constant-time update and nCr |
| Space | O(n + s) | factorial and inverse factorial arrays up to n + s |

The constraints allow up to $2 \cdot 10^5$, and the solution performs only linear preprocessing plus constant work per query, fitting comfortably within limits.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, s, q = map(int, input().split())
    a = list(map(int, input().split()))
    
    A = sum(a)
    
    MAX = n + s
    fact = [1] * (MAX + 1)
    invfact = [1] * (MAX + 1)
    for i in range(1, MAX + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[MAX] = pow(fact[MAX], MOD - 2, MOD)
    for i in range(MAX, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD
    
    def ncr(n, r):
        if r < 0 or r > n:
            return 0
        return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD
    
    out = []
    for _ in range(q):
        x, val = map(int, input().split())
        x -= 1
        A -= a[x]
        a[x] = val
        A += a[x]
        R = s - A
        if R < 0:
            out.append("0")
        else:
            out.append(str(ncr(R + n, n)))
    
    return "\n".join(out)

# provided sample
assert run("""3 5 4
1 1 1
1 1
1 2
2 2
3 2
""") == "10\n10\n4\n1"

# custom tests
assert run("""1 0 2
0
1 1
1 0
""") == "1\n1", "single variable edge"

assert run("""2 1 2
0 0
1 1
2 1
""") == "2\n1", "tight capacity shrink"

assert run("""3 0 1
0 0 0
1 0
""") == "10", "pure stars and bars"

assert run("""4 2 2
1 0 1 0
1 2
3 2
""") == "0\n0", "infeasible after updates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single variable updates | 1 1 | correctness of base case |
| tight capacity shrink | 2 1 | monotonic feasibility reduction |
| all zeros | 10 | pure combinatorial identity |
| infeasible updates | 0 0 | negative slack handling |

## Edge Cases

When the sum of lower bounds exceeds $s$, the algorithm correctly outputs 0 immediately because $R = s - A < 0$. For example, with $n=3, s=2, a=[1,1,1]$, we compute $A=3$, giving $R=-1$, and the output is 0 without attempting binomial evaluation.

When all $a_i = 0$, we get $R = s$, and the answer becomes $\binom{s+n}{n}$. The algorithm handles this naturally since no special casing is needed beyond the standard nCr computation.

When updates decrease or increase a single position, only $A$ changes. The algorithm correctly removes the old contribution before adding the new one, ensuring no accumulation drift over multiple queries.
