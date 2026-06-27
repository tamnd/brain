---
title: "CF 105192B - Is this FFT?"
description: "We are given a single polynomial $c(x)$, described by its coefficients from degree 0 up to degree $l$. This polynomial is known to be the result of multiplying two other polynomials $a(x)$ and $b(x)$, but the original factors were lost."
date: "2026-06-27T04:11:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105192
codeforces_index: "B"
codeforces_contest_name: "Cupertino Informatics Tournament Online Mirror"
rating: 0
weight: 105192
solve_time_s: 78
verified: false
draft: false
---

[CF 105192B - Is this FFT?](https://codeforces.com/problemset/problem/105192/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a single polynomial $c(x)$, described by its coefficients from degree 0 up to degree $l$. This polynomial is known to be the result of multiplying two other polynomials $a(x)$ and $b(x)$, but the original factors were lost. The task is not to uniquely recover them, but to construct any pair of polynomials $a$ and $b$ whose convolution gives back exactly the given polynomial $c$.

The output format asks us to explicitly print the degree and coefficients of both reconstructed polynomials. There is no requirement for minimal degree, uniqueness, or any structural constraint beyond correctness of multiplication.

The constraints are large, with $l \le 10^5$, which immediately rules out any approach that tries to factor the polynomial meaningfully or solve systems of equations over coefficients. Any attempt to reconstruct a “real” factorization would involve convolution reasoning or algebraic decomposition, which is far heavier than needed. The key observation is that correctness only depends on the product matching $c$, not on how “interesting” the factors are.

The most dangerous edge case is assuming that both polynomials must be non-trivial or that some balanced split is required. For example, one might incorrectly try to split coefficients evenly or distribute degrees, but the problem never requires such constraints.

A simple case illustrates this:

Input:

```
2
6 5 1
```

The polynomial is $c(x) = 6 + 5x + x^2$. A tempting but unnecessary idea is to search for $(x+2)(x+3)$, but that is not required. Any valid factorization works.

The correct output could just as well be:

```
2
6 5 1
0
1
```

because multiplying by the constant polynomial $1$ preserves everything.

## Approaches

The naive interpretation is that we must recover two polynomials whose convolution equals the given one. If we attempted this directly, we would be solving for coefficients $a_i, b_j$ such that:

$$c_k = \sum_{i+j=k} a_i b_j$$

This is a nonlinear system of equations. Even for moderate $l$, trying to guess or solve such a system would explode combinatorially, since each coefficient introduces dependencies across many pairs.

A more structured attempt might involve fixing degrees $n$ and $m$, then trying to reconstruct coefficients iteratively. However, each step depends on previously chosen values in a way that quickly becomes underdetermined. There are infinitely many valid decompositions, and searching for one in a principled way is unnecessary.

The key simplification is recognizing that the problem does not require a non-trivial factorization. We are free to choose any valid pair. That immediately suggests a constant polynomial as one factor. If we set $b(x) = 1$, then:

$$a(x) \cdot 1 = a(x)$$

So choosing $a(x) = c(x)$ satisfies the requirement exactly.

This reduces the entire task to copying the input polynomial into one output polynomial and printing a constant polynomial $1$ as the second.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Factorization | Exponential | High | Too slow |
| Trivial Construction $a=c, b=1$ | $O(l)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

We construct a valid decomposition directly without performing any convolution or algebraic solving.

## Algorithm Walkthrough

1. Read the degree $l$ and the coefficients of $c(x)$. These coefficients will be reused directly as the coefficients of $a(x)$. This works because we plan to use a multiplicative identity polynomial for $b(x)$.
2. Set $a(x) = c(x)$. We do not modify the coefficients because any change would require compensating adjustments in $b(x)$, which is unnecessary complexity.
3. Construct $b(x) = 1$, which is a polynomial of degree 0 with a single coefficient equal to 1. This is chosen because it is the multiplicative identity under polynomial multiplication.
4. Output the degree and coefficients of $a(x)$.
5. Output degree 0 for $b(x)$, followed by coefficient 1.

### Why it works

Polynomial multiplication with a constant polynomial $1$ leaves every coefficient unchanged. Since convolution with $[1]$ does not mix or shift terms, the resulting polynomial is exactly the original one. This guarantees that the constructed pair always satisfies $a(x) \cdot b(x) = c(x)$, regardless of the input coefficients.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    l = int(input().strip())
    c = list(map(int, input().split()))
    
    # a(x) = c(x)
    print(l)
    print(*c)
    
    # b(x) = 1
    print(0)
    print(1)

if __name__ == "__main__":
    main()
```

The first part of the code reads the polynomial directly and prints it unchanged as $a(x)$. The second part constructs the identity polynomial $b(x)$. No computation beyond input/output handling is required, which is why this solution comfortably fits within constraints.

A subtle point is ensuring the formatting of degrees matches the definition: degree $l$ corresponds to $l+1$ coefficients, and degree 0 corresponds to a single coefficient. Mixing this up is the most common implementation error.

## Worked Examples

### Example 1

Input:

```
2
6 5 1
```

We interpret this as $c(x) = 6 + 5x + x^2$.

| Step | a(x) | b(x) | Comment |
| --- | --- | --- | --- |
| Read input | - | - | Store coefficients of $c$ |
| Assign a | [6, 5, 1] | - | Copy directly |
| Assign b | [6, 5, 1] | [1] | Identity polynomial |
| Output | [6, 5, 1] | [1] | Valid decomposition |

The output reconstructs $c(x)$ exactly because multiplying by 1 preserves all coefficients.

### Example 2

Input:

```
0
7
```

This corresponds to a constant polynomial $c(x) = 7$.

| Step | a(x) | b(x) | Comment |
| --- | --- | --- | --- |
| Read input | - | - | Single coefficient |
| Assign a | [7] | - | Copy |
| Assign b | [7] | [1] | Identity |
| Output | [7] | [1] | Valid |

This confirms that even the smallest possible polynomial is handled without special casing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(l)$ | We only read and print the coefficients once |
| Space | $O(1)$ extra | Input storage aside, no additional structures are used |

The constraints allow up to $10^5$ coefficients, and the solution only performs linear scanning and output, which is comfortably within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    l = int(input().strip())
    c = list(map(int, input().split()))

    out = []
    out.append(str(l))
    out.append(" ".join(map(str, c)))
    out.append("0")
    out.append("1")
    return "\n".join(out)

# provided sample
assert run("2\n6 5 1\n") == "2\n6 5 1\n0\n1"

# single constant polynomial
assert run("0\n7\n") == "0\n7\n0\n1"

# negative coefficients
assert run("1\n-3 4\n") == "1\n-3 4\n0\n1"

# larger case
assert run("3\n1 2 3 4\n") == "3\n1 2 3 4\n0\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| constant polynomial | identity behavior | smallest edge case |
| negative coefficients | sign preservation | no assumptions on positivity |
| small degree > 0 | general correctness | normal structure |
| larger array | scaling correctness | linear handling |

## Edge Cases

The constant polynomial case $l = 0$ is the only structurally different input. For input:

```
0
5
```

the algorithm sets $a(x) = [5]$ and $b(x) = [1]$. The convolution of a constant with 1 remains the same constant, so the output is valid without needing any special branching.

No matter how large or irregular the coefficient values are, the identity polynomial guarantees correctness without relying on any arithmetic beyond copying values.
