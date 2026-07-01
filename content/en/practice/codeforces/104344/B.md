---
title: "CF 104344B - Triplas pitag\u00f3ricas"
description: "We are given two integers $m$ and $n$, with $1 le n < m le 10^4$. From these two values, we must construct a triple of integers using a fixed algebraic recipe and print the result in a specific order. The construction is not arbitrary."
date: "2026-07-01T18:27:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104344
codeforces_index: "B"
codeforces_contest_name: "Maratona dos Bixes 2023 - UNICAMP"
rating: 0
weight: 104344
solve_time_s: 81
verified: true
draft: false
---

[CF 104344B - Triplas pitag\u00f3ricas](https://codeforces.com/problemset/problem/104344/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers $m$ and $n$, with $1 \le n < m \le 10^4$. From these two values, we must construct a triple of integers using a fixed algebraic recipe and print the result in a specific order.

The construction is not arbitrary. It follows a deterministic mapping from the pair $(m, n)$ into three values:

$a = m^2 - n^2$,

$b = 2mn$,

$c = m^2 + n^2$.

The output is simply these three computed values in this exact order.

Even though the statement references geometric intuition, the task itself is purely arithmetic. The only real requirement is correct evaluation and ordering.

The constraints are extremely small. Even the largest value, $m^2$, is at most $10^8$, so all computations comfortably fit inside 32-bit integers. This means there is no need for modular arithmetic, big integers, or optimizations beyond direct computation.

A common failure mode here is reordering the triple. The expression defines a specific order, and swapping values still produces a valid Pythagorean triple but an invalid answer for this problem. For example, with input $m=3, n=2$, correct output is $5\ 12\ 13$, while $12\ 5\ 13$ is incorrect even though it satisfies the same identity.

Another subtle issue is assuming any permutation is acceptable because all permutations satisfy $a^2 + b^2 = c^2$. That property is irrelevant here since the problem fixes the order explicitly.

## Approaches

A brute-force interpretation would ignore the closed-form formula and try to “discover” a valid Pythagorean triple matching the given structure. One might attempt to enumerate candidate integers $a, b, c$ derived from $m, n$ or even search for triples satisfying $a^2 + b^2 = c^2$ near the magnitude of $m^2$. Such an approach is unnecessary and inefficient because the problem does not ask for discovery, only evaluation of a known formula.

If we attempted a naive search over possible triples up to magnitude $O(m^2)$, the worst case would involve checking up to $O(m^4)$ combinations in the naive 3-loop space, which is far beyond the limit even for $m = 10^4$. Even reducing to a single loop over $c$ would still require checking many decompositions, which is wasted work because the structure is already fully determined.

The key observation is that the formula given is complete. It directly constructs the triple without ambiguity. Each of $a$, $b$, and $c$ depends only on $m$ and $n$, so the entire problem reduces to evaluating three arithmetic expressions.

This removes any combinatorial or search component. There is no decision-making step, only computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force search for triples | $O(m^4)$ or worse | $O(1)$ | Too slow |
| Direct formula evaluation | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read integers $m$ and $n$. These define the parameter pair that uniquely determines the triple.
2. Compute $m^2$ once, since it is used in all expressions. This avoids redundant multiplication and keeps the computation clean.
3. Compute $a = m^2 - n^2$. This corresponds to the difference of squares structure, which ensures $a$ is positive because $m > n$.
4. Compute $b = 2mn$. This is the cross term that scales linearly with both parameters.
5. Compute $c = m^2 + n^2$. This is the sum of squares and will always be the largest value among the three.
6. Output $a, b, c$ in this exact order.

### Why it works

The construction is the classical Euclidean parameterization of Pythagorean triples. Algebraically, substituting the expressions shows that

$(m^2 - n^2)^2 + (2mn)^2 = (m^2 + n^2)^2$,

because both sides expand to $m^4 + 2m^2n^2 + n^4$. This identity guarantees that the produced triple always satisfies the Pythagorean condition.

The ordering is fixed by the definition itself, not by size. Even though $c$ is always the largest value, $a$ and $b$ are not ordered relative to each other, so swapping them would still preserve correctness mathematically but violate the output specification.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    m, n = map(int, input().split())

    m2 = m * m
    n2 = n * n

    a = m2 - n2
    b = 2 * m * n
    c = m2 + n2

    print(a, b, c)

if __name__ == "__main__":
    main()
```

The implementation directly follows the formula. Precomputing $m^2$ and $n^2$ avoids recomputation and keeps the code readable. The multiplication $2mn$ is computed explicitly to avoid any ambiguity in operator precedence, even though Python handles it correctly.

All values are computed using integer arithmetic, and Python’s integer type easily accommodates the maximum possible values.

## Worked Examples

### Example 1

Input:

```
2 1
```

| Step | m | n | m² | n² | a = m²−n² | b = 2mn | c = m²+n² |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Init | 2 | 1 | 4 | 1 | - | - | - |
| Compute | 2 | 1 | 4 | 1 | 3 | 4 | 5 |

Output:

```
3 4 5
```

This case confirms that the smallest valid Pythagorean triple is generated correctly. It also shows that $a$ can be smaller than $b$, reinforcing that ordering is not based on magnitude.

### Example 2

Input:

```
3 2
```

| Step | m | n | m² | n² | a = m²−n² | b = 2mn | c = m²+n² |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Init | 3 | 2 | 9 | 4 | - | - | - |
| Compute | 3 | 2 | 9 | 4 | 5 | 12 | 13 |

Output:

```
5 12 13
```

This trace highlights how the cross term $2mn$ grows faster than the difference term. It also confirms that $c$ is always the largest component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a constant number of arithmetic operations are performed regardless of input size |
| Space | $O(1)$ | Only a few integer variables are stored |

The computation involves at most a handful of multiplications and additions, so it is far below the limits even for large numbers. Memory usage is constant and negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    m, n = map(int, input().split())
    a = m*m - n*n
    b = 2*m*n
    c = m*m + n*n
    return f"{a} {b} {c}"

# provided samples
assert run("2 1\n") == "3 4 5"
assert run("3 2\n") == "5 12 13"

# custom cases
assert run("4 1\n") == "15 8 17"
assert run("5 3\n") == "16 30 34"
assert run("10 9\n") == "19 180 181"
assert run("100 1\n") == "9999 200 10001"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 1 | 15 8 17 | non-small triple, checks ordering |
| 5 3 | 16 30 34 | general correctness for mid values |
| 10 9 | 19 180 181 | edge case with close m and n |
| 100 1 | 9999 200 10001 | large difference scale |

## Edge Cases

A key edge case is when $n$ is very close to $m$, for example $m=10, n=9$. The computation yields:

$a = 100 - 81 = 19$,

$b = 180$,

$c = 181$.

Even though $a$ is small, it remains positive because the strict inequality $m > n$ guarantees $m^2 - n^2 > 0$. The algorithm naturally handles this without special checks.

Another case is when $n = 1$ and $m$ is large, such as $m=100$. Here $a$ becomes $9999$, which is still comfortably within bounds, while $b$ remains linear in $m$. The computation does not overflow in Python, and even in fixed-width integer languages it remains safe under 32-bit limits.

A third scenario is the smallest valid input $m=2, n=1$. This produces the base triple $3, 4, 5$, confirming that the formula is well-defined at the lower bound and does not require special handling for small values.
