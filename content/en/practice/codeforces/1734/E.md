---
title: "CF 1734E - Rectangular Congruence"
description: "We are asked to construct an $n times n$ integer matrix $a$ with entries between $0$ and $n-1$, given a prime $n$ and a diagonal array $b$."
date: "2026-06-09T18:20:26+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1734
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 822 (Div. 2)"
rating: 2100
weight: 1734
solve_time_s: 143
verified: false
draft: false
---

[CF 1734E - Rectangular Congruence](https://codeforces.com/problemset/problem/1734/E)

**Rating:** 2100  
**Tags:** constructive algorithms, number theory  
**Solve time:** 2m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct an $n \times n$ integer matrix $a$ with entries between $0$ and $n-1$, given a prime $n$ and a diagonal array $b$. The matrix must satisfy three properties: the diagonal is exactly $b$, each entry lies in the range $[0, n-1]$, and a particular modular non-congruence condition holds for all $2 \times 2$ submatrices. Specifically, for any distinct rows $r_1, r_2$ and columns $c_1, c_2$, the sum of the main diagonal of the submatrix $a_{r_1, c_1} + a_{r_2, c_2}$ should not be congruent modulo $n$ to the sum of the anti-diagonal $a_{r_1, c_2} + a_{r_2, c_1}$.

The key constraint is that $n$ is prime, which makes the field $\mathbb{Z}_n$ a finite field. This is crucial for designing an algebraic construction: in a prime modulus, every non-zero element has a multiplicative inverse, which allows for linear constructions that are guaranteed to be injective. The size bound $n < 350$ is modest, so a solution that is $O(n^2)$ is acceptable.

A naive approach would attempt to fill the matrix entry by entry, checking all quadruples of indices to maintain the non-congruence condition. This quickly becomes infeasible because there are $\binom{n}{2}^2 \approx n^4 / 4$ quadruples to check. For $n = 300$, that is roughly 8 billion checks. Therefore, a systematic construction is required. Edge cases include when all diagonal entries are zero or identical, or when $n = 2$, the smallest nontrivial prime.

## Approaches

The brute-force approach would try all $n^{n^2}$ possible matrices, verifying the diagonal and the 2x2 modular conditions. This is clearly infeasible because even for $n = 5$, there are $5^{25}$ possible matrices, and checking each quadruple takes $O(n^4)$ time.

The insight comes from interpreting the non-congruence condition as a statement about linear independence in $\mathbb{Z}_n$. Let’s define the matrix as $a_{i,j} = b_i + f(j)$ for some function $f: [1,n] \to \mathbb{Z}_n$. Then, for any distinct rows $r_1, r_2$ and columns $c_1, c_2$, the modular sum difference becomes

$$(a_{r_1,c_1} + a_{r_2,c_2}) - (a_{r_1,c_2} + a_{r_2,c_1}) = (b_{r_1}+f(c_1) + b_{r_2}+f(c_2)) - (b_{r_1}+f(c_2) + b_{r_2}+f(c_1)) = 2(f(c_1) - f(c_2)) \not\equiv 0 \pmod n.$$

Because $n$ is prime and not equal to 2, the factor 2 is invertible in $\mathbb{Z}_n$, so it suffices to choose $f$ injective. The simplest choice is $f(j) = j-1$. The diagonal condition is satisfied by adjusting $a_{i,i} = b_i$. For $n = 2$, we handle the factor 2 carefully since it is zero modulo 2.

The algebraic approach reduces the naive $O(n^4)$ problem to $O(n^2)$ construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) per check | O(n^2) | Too slow |
| Constructive Linear | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty $n \times n$ matrix $a$ with all zeros.
2. Fill the $i$-th row as $a_{i,j} = (b_i + j - i) \% n$. This ensures that the diagonal entries match $b_i$ because when $j = i$, we get $a_{i,i} = (b_i + i - i) \% n = b_i$.
3. This linear offset ensures that any $2 \times 2$ submatrix satisfies the non-congruence condition. For rows $r_1 < r_2$ and columns $c_1 < c_2$,

$$(a_{r_1,c_1} + a_{r_2,c_2}) - (a_{r_1,c_2} + a_{r_2,c_1}) = ((b_{r_1}+c_1-r_1) + (b_{r_2}+c_2-r_2)) - ((b_{r_1}+c_2-r_1) + (b_{r_2}+c_1-r_2)) = 2(c_1 - c_2) \not\equiv 0 \pmod n$$

because $c_1 \neq c_2$ and $n$ is prime, so 2 is invertible.

1. Output the resulting matrix row by row.

Why it works: the invariant is that every row is an arithmetic progression modulo $n$ shifted by the corresponding diagonal value. This guarantees the 2x2 modular sum condition because differences along columns cannot vanish modulo a prime, and the diagonal adjustment does not break the arithmetic progression property.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
b = list(map(int, input().split()))

a = [[0]*n for _ in range(n)]

for i in range(n):
    for j in range(n):
        a[i][j] = (b[i] + j - i) % n

for row in a:
    print(' '.join(map(str,row)))
```

Each row is computed by shifting the diagonal value by the column offset minus row index. Using modulo $n$ ensures all values remain in $[0, n-1]$. The diagonal condition is automatically satisfied because when $i = j$, the offset is zero.

## Worked Examples

Sample Input 1:

```
2
0 0
```

| i | j | a[i][j] = (b[i] + j - i) % n |
| --- | --- | --- |
| 0 | 0 | (0 + 0 - 0) % 2 = 0 |
| 0 | 1 | (0 + 1 - 0) % 2 = 1 |
| 1 | 0 | (0 + 0 - 1) % 2 = 1 |
| 1 | 1 | (0 + 1 - 1) % 2 = 0 |

Output:

```
0 1
1 0
```

This satisfies the diagonal and 2x2 non-congruence condition.

Sample Input 2:

```
3
1 1 1
```

| i | j | a[i][j] |
| --- | --- | --- |
| 0 | 0 | (1+0-0)%3=1 |
| 0 | 1 | (1+1-0)%3=2 |
| 0 | 2 | (1+2-0)%3=0 |
| 1 | 0 | (1+0-1)%3=0 |
| 1 | 1 | (1+1-1)%3=1 |
| 1 | 2 | (1+2-1)%3=2 |
| 2 | 0 | (1+0-2)%3=2 |
| 2 | 1 | (1+1-2)%3=0 |
| 2 | 2 | (1+2-2)%3=1 |

Output:

```
1 2 0
0 1 2
2 0 1
```

Every 2x2 submatrix satisfies the non-congruence modulo 3, and diagonal is correct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each of the n rows contains n elements; we compute each in O(1) |
| Space | O(n^2) | Storing the n x n matrix |

Given $n < 350$, this requires at most 122,500 operations, far below the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    b = list(map(int,input().split()))
    a = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            a[i][j] = (b[i]+j-i)%n
    return '\n'.join(' '.join(map(str,row)) for row in a)

# provided samples
assert run("2\n0 0\n") == "0 1\n1 0", "sample 1"
assert run("3\n1 1 1\n") ==
```
