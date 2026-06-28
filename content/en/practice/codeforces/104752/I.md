---
title: "CF 104752I - Inspecting the Scores"
description: "Each game consists of a sequence of $N$ matches. The score starts at 1, and every match either multiplies the current score by $A$, multiplies it by $B$, or leaves it unchanged if nobody solves the problem. The key point is that we are not choosing a single sequence."
date: "2026-06-29T01:25:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104752
codeforces_index: "I"
codeforces_contest_name: "Concurso de programaci\u00f3n ANIEI 2023"
rating: 0
weight: 104752
solve_time_s: 69
verified: false
draft: false
---

[CF 104752I - Inspecting the Scores](https://codeforces.com/problemset/problem/104752/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** no  

## Solution
## Problem Understanding

Each game consists of a sequence of $N$ matches. The score starts at 1, and every match either multiplies the current score by $A$, multiplies it by $B$, or leaves it unchanged if nobody solves the problem.

The key point is that we are not choosing a single sequence. We must consider every possible way the matches could be resolved independently: each match has three possibilities, but two of them affect the score. Two games are considered different if at least one match was solved by a different person.

For each such full sequence of outcomes, we compute the final score and then sum these scores over all possible sequences.

The input gives multiple test cases, each with $N$, $A$, and $B$. We must output the sum of scores over all valid outcome sequences modulo $10^9 + 7$.

The constraints allow up to $10^5$ test cases and $N$ up to $1000$. This immediately rules out any solution that tries to enumerate outcomes, since even for a single test case there are $3^N$ possibilities. The solution must instead aggregate contributions per position or use a closed-form combinatorial structure.

A subtle edge case appears when $A = B = 1$. In that case every sequence produces score 1, so the answer is exactly the number of sequences, which is $3^N$. Any derivation that divides by $A - B$ or assumes invertibility without checking will fail here. Another edge case is $A = B \neq 1$, where symmetry collapses the structure and naive formulas with cancellation again break.

## Approaches

A brute-force interpretation treats each match as independently choosing among three outcomes: Franco solves, Rafa solves, or nobody solves. For a fixed sequence, the score is the product of contributions along the sequence. This leads directly to $3^N$ sequences, each requiring $O(N)$ multiplication to evaluate, which is far beyond feasible even for $N = 30$.

The key observation is that multiplication distributes over independent choices. Instead of thinking about full sequences, we can think about each match contributing a factor that is independent across all sequences. For each match, we are effectively summing contributions over three choices: multiply by $A$, multiply by $B$, or multiply by 1.

This means that when expanding all sequences, the total sum factorizes. Each position contributes a multiplicative factor equal to the sum of its local contributions across all choices, and since choices are independent across positions, the global answer becomes a power of that local sum.

At each match, the possible contributions to the total sum are:

- 1 if nobody solves,
- $A$ if Franco solves,
- $B$ if Rafa solves.

So each position contributes a factor $1 + A + B$. Since all positions are independent, the total sum over all sequences is:

$$(1 + A + B)^N.$$

This reduces the entire problem to fast modular exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(3^N \cdot N)$ | $O(1)$ | Too slow |
| Optimal | $O(T \log N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

### Optimal computation via modular exponentiation

1. For each test case, read $N$, $A$, and $B$. The entire structure of the problem depends only on these values through the expression $1 + A + B$.
2. Compute the base value $x = (1 + A + B) \bmod (10^9 + 7)$. This represents the total contribution of a single match after summing over all possible outcomes.
3. Compute $x^N \bmod (10^9 + 7)$ using binary exponentiation. This step aggregates the independent contributions of all matches.
4. Output the result.

Binary exponentiation is necessary because direct multiplication $N$ times is too slow for large $N$ and repeated across $10^5$ test cases.

### Why it works

Each match contributes independently to every full game configuration. When summing over all configurations, we are effectively expanding a product of identical sums:

$$\prod_{i=1}^{N} (1 + A + B).$$

Because there is no interaction between positions, no term depends on decisions at other positions. This independence guarantees that multiplication across positions correctly reconstructs the full combinatorial expansion without overcounting or missing any sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modexp(a, e):
    res = 1
    while e:
        if e & 1:
            res = (res * a) % MOD
        a = (a * a) % MOD
        e >>= 1
    return res

t = int(input())
for _ in range(t):
    n, a, b = map(int, input().split())
    base = (1 + a + b) % MOD
    print(modexp(base, n))
```

The core idea is the reduction of the entire combinatorial process into a single power computation. The function `modexp` implements binary exponentiation, ensuring logarithmic time per test case.

A common pitfall is forgetting the neutral “no solve” outcome, which contributes the $1$ in the base. Missing it leads to computing $(A + B)^N$, which undercounts all sequences where a match is skipped.

## Worked Examples

### Sample 1: $N = 1, A = 6, B = 9$

| Step | Base $1 + A + B$ | Result |
| --- | --- | --- |
| Compute base | $1 + 6 + 9 = 16$ | 16 |
| Power | $16^1$ | 16 |

This confirms that for a single match, all three outcomes are directly summed.

### Sample 2: $N = 2, A = 8, B = 4$

| Step | Base | Power computation |
| --- | --- | --- |
| Compute base | $1 + 8 + 4 = 13$ | 13 |
| First expansion | $13^2 = 169$ | 169 |

This shows how two independent matches multiply their identical contribution structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \log N)$ | Each test case requires binary exponentiation over $N$ |
| Space | $O(1)$ | Only a few variables are used per test case |

The constraints allow up to $10^5$ test cases, and $N \le 1000$, so $\log N$ is at most around 10. This ensures the solution easily runs within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    MOD = 10**9 + 7

    def modexp(a, e):
        res = 1
        while e:
            if e & 1:
                res = (res * a) % MOD
            a = (a * a) % MOD
            e >>= 1
        return res

    t = int(sys.stdin.readline())
    for _ in range(t):
        n, a, b = map(int, sys.stdin.readline().split())
        base = (1 + a + b) % MOD
        output.append(str(modexp(base, n)))

    return "\n".join(output)

# provided samples
assert run("1\n1 6 9\n") == "16", "sample 1"
assert run("1\n2 8 4\n") == "169", "sample 2"

# custom cases
assert run("1\n1 0 0\n") == "1", "only neutral outcome"
assert run("1\n3 1 1\n") == "27", "symmetric small case"
assert run("2\n1 2 3\n1 5 7\n") == "6\n13", "multiple independent cases"
assert run("1\n1000 1 1\n") == str(pow(3, 1000, 10**9+7)), "large exponent check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $1\ 0\ 0$ | 1 | Only no-op outcomes |
| $3\ 1\ 1$ | 27 | Uniform branching |
| two cases | 6 / 13 | Multiple test handling |
| $1000\ 1\ 1$ | $3^{1000}$ | Large exponent correctness |

## Edge Cases

When $A = 0$ and $B = 0$, only the “no solve” outcome contributes. The base becomes 1, so the answer is $1^N = 1$. The algorithm handles this directly through the base computation.

When $A = B = 1$, every match contributes equally, and the base becomes 3. The answer is $3^N$, matching the number of all possible outcome sequences. Any approach that simplifies symmetry incorrectly might accidentally collapse this to 1 or $2^N$, but the exponentiation formulation preserves correctness.

When $A$ and $B$ are large, modular reduction happens only at the base computation and during exponentiation steps. Since all arithmetic is modular throughout, overflow is avoided and intermediate values remain bounded.
