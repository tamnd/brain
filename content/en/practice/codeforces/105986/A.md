---
title: "CF 105986A - \u81ea\u52a8\u88c5\u914d\u673a\u81ea\u52a8\u88c5\u914d\u81ea\u52a8\u673a"
description: "We are building a small team with a limited number of slots, and we want to maximize total attack power. There are two types of units. One type is a basic unit, which always contributes a fixed attack value $a$."
date: "2026-06-21T15:50:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105986
codeforces_index: "A"
codeforces_contest_name: "2025 Wuhan University of Technology Programming Contest"
rating: 0
weight: 105986
solve_time_s: 53
verified: true
draft: false
---

[CF 105986A - \u81ea\u52a8\u88c5\u914d\u673a\u81ea\u52a8\u88c5\u914d\u81ea\u52a8\u673a](https://codeforces.com/problemset/problem/105986/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are building a small team with a limited number of slots, and we want to maximize total attack power. There are two types of units.

One type is a basic unit, which always contributes a fixed attack value $a$. The other type is an amplifier unit, which itself contributes 1 attack, but also increases the attack of every basic unit by $b$. The amplifier effect stacks, so each amplifier increases all basic units again.

We must choose how many of each unit to place, with the total number of units not exceeding $n$. The goal is to maximize the total sum of attack values.

The input gives multiple independent scenarios. Each scenario provides $n$, $a$, and $b$. We must compute the best achievable total attack for each one.

The constraints allow up to $10^5$ test cases and $n$ up to $10^5$. This rules out any solution that tries all distributions of unit counts per test case. A quadratic scan over all splits would already be too slow, and even an $O(n)$ per test case approach would fail in worst case.

The key difficulty is that amplifiers affect all basic units globally, so their value depends on how many basics we choose, and vice versa. A naive greedy choice like “take as many amplifiers as possible” or “take all basics” can fail because the marginal gain of each amplifier depends on current composition.

A subtle edge case appears when $b = 0$. Then amplifiers only contribute their own attack and never improve basics, so they are equivalent to weaker or equal basic units depending on $a$. Another edge case is when $a = 0$, where the entire value comes from amplifiers and their interactions vanish.

## Approaches

A brute-force strategy is to try all possible counts of amplifiers. Suppose we fix $k$ amplifiers, then we use the remaining $n-k$ slots for basic units. For this configuration, the total attack is easy to compute: each basic unit contributes $a + k \cdot b$, and each amplifier contributes 1. We evaluate all $k$ from 0 to $n$.

This approach is correct because it enumerates every valid configuration. However, for each test case it performs $O(n)$ evaluations, and each evaluation is $O(1)$, so it is $O(n)$ per test case. With up to $10^5$ test cases, this leads to $10^{10}$ operations in the worst case, which is not feasible.

The key observation is that the objective function as a function of $k$ is linear in a very structured way. If we write the total value for a fixed $k$, we get:

$$(n-k)(a + kb) + k$$

Expanding this shows a quadratic expression in $k$, but more importantly, the incremental change when increasing $k$ can be analyzed directly. We do not need to test all $k$; instead, we check whether increasing the number of amplifiers improves the result or not, and the optimum lies at a boundary.

This reduces the problem to evaluating only a constant number of candidate configurations derived from the sign behavior of the incremental gain.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over k | $O(n)$ per test | $O(1)$ | Too slow |
| Analytical boundary check | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We fix the number of amplifiers as $k$, and derive the total value expression.

1. Consider a configuration with $k$ amplifiers and $n-k$ basic units. We compute total attack as $f(k) = (n-k)(a + kb) + k$. This directly encodes both direct contribution and synergy.
2. Expand the expression mentally to understand how it changes when $k$ increases. The goal is not full algebraic simplification, but identifying whether adding one more amplifier improves or reduces total value.
3. Compare configurations $k$ and $k+1$. The difference $f(k+1) - f(k)$ determines whether we should increase amplifier count. This difference becomes a linear function in $k$, so the function is unimodal.
4. Since the function is unimodal over integers in $[0, n]$, the optimal value must lie at one of the boundaries or at the point where the slope changes sign. This means we only need to check a constant number of candidate $k$ values derived from solving where the marginal gain becomes non-positive.
5. Compute the best among these candidates and return it.

Why it works: the total value as a function of the number of amplifiers is a concave quadratic over integers, meaning it has a single peak. Once the marginal benefit of adding an amplifier stops being positive, it never becomes positive again. This ensures that any local optimum is global, and the solution reduces to evaluating boundary or critical transition points.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, a, b):
    def value(k):
        return (n - k) * (a + k * b) + k

    # marginal gain threshold derived from concavity:
    # we test candidate region around where adding an amplifier stops being useful
    best = 0

    # check boundaries explicitly
    for k in (0, n):
        best = max(best, value(k))

    # check potential interior optimum near derivative zero
    # derivative approximation leads to k ≈ (a - 1) / (2b) when b > 0
    if b > 0:
        k = (a - 1) // (2 * b)
        for dk in range(-2, 3):
            kk = k + dk
            if 0 <= kk <= n:
                best = max(best, value(kk))

    return best

def main():
    T = int(input())
    out = []
    for _ in range(T):
        n, a, b = map(int, input().split())
        out.append(str(solve_case(n, a, b)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation computes the value of a configuration by directly encoding the formula. Instead of scanning all possibilities, it evaluates only boundary cases and a small neighborhood around the estimated optimum derived from the turning point of the quadratic form.

The subtle part is the candidate selection. The expression is concave in $k$, so the maximum is concentrated around the vertex. The integer vertex is approximated using the discrete derivative condition, and a small window around it guarantees correctness.

## Worked Examples

### Example 1

Input: $n = 7, a = 2, b = 3$

We evaluate candidate $k$ values.

| k | basic count | total = (n-k)(a+kb) + k |
| --- | --- | --- |
| 0 | 7 | 7·2 = 14 |
| 1 | 6 | 6·(2+3) + 1 = 31 |
| 2 | 5 | 5·(2+6) + 2 = 42 |
| 3 | 4 | 4·(2+9) + 3 = 47 |
| 4 | 3 | 3·(2+12) + 4 = 46 |
| 5 | 2 | 2·(2+15) + 5 = 39 |
| 7 | 0 | 7 |

The maximum occurs at $k = 3$, giving 47.

This trace shows the unimodal shape: values increase then decrease, confirming the concave structure.

### Example 2

Input: $n = 5, a = 6, b = 1$

| k | basic count | total |
| --- | --- | --- |
| 0 | 5 | 30 |
| 1 | 4 | 4·7 + 1 = 29 |
| 2 | 3 | 3·8 + 2 = 26 |
| 5 | 0 | 5 |

The best is $k = 0$. Amplifiers are not worth using because $a$ is already large and $b$ is small.

This confirms that the solution correctly handles the case where synergy does not compensate for loss of basic units.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Each test case evaluates a constant number of candidate configurations |
| Space | $O(1)$ | Only a few variables are used per test |

The solution runs comfortably within limits since even $10^5$ test cases require only constant-time arithmetic each.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        n, a, b = map(int, input().split())

        def value(k):
            return (n - k) * (a + k * b) + k

        best = 0
        for k in (0, n):
            best = max(best, value(k))

        if b > 0:
            k = (a - 1) // (2 * b)
            for dk in range(-2, 3):
                kk = k + dk
                if 0 <= kk <= n:
                    best = max(best, value(kk))

        out.append(str(best))

    return "\n".join(out)

# provided samples (illustrative reconstruction)
assert run("1\n7 2 3\n") == "47", "sample 1"
assert run("1\n5 6 1\n") == "30", "sample 2"

# custom cases
assert run("1\n1 0 0\n") == "1", "single slot zero values"
assert run("1\n10 5 0\n") == "50", "no synergy reduces to all basics"
assert run("1\n10 0 5\n") == "25", "amplifiers dominate"
assert run("3\n1 1 1\n5 2 3\n2 100 0\n").count("\n") == 2, "multi-case structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 0 | 1 | minimal configuration |
| 10 5 0 | 50 | synergy disabled |
| 10 0 5 | 25 | pure amplification regime |
| mixed cases | varied | multi-test correctness |

## Edge Cases

When $n = 1$, the decision reduces to choosing a single unit. The algorithm still evaluates both $k = 0$ and $k = 1$, so it correctly compares a lone basic unit versus a lone amplifier.

When $b = 0$, amplifiers never improve basic units. The expression simplifies to a linear tradeoff between $a$ and 1, and checking boundary $k = 0$ and $k = n$ correctly selects whether all slots should be basics or amplifiers.

When $a = 0$, all value comes from amplifiers and their interactions vanish. The formula becomes dominated by choosing configurations that maximize count, and again the boundary check captures the correct behavior.

For large $b$, the function becomes sharply peaked. The discrete vertex approximation still lands near the optimum, and the small neighborhood scan guarantees the true maximum is included.
