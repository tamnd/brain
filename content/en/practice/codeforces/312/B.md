---
title: "CF 312B - Archer"
description: "Two archers shoot at a target alternately. SmallR shoots first and hits with probability $a/b$ on each shot. Zanoes hits with probability $c/d$ on each shot. As soon as someone lands the first hit of the match, the game ends and that player wins."
date: "2026-06-06T00:51:43+07:00"
tags: ["codeforces", "competitive-programming", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 312
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 185 (Div. 2)"
rating: 1300
weight: 312
solve_time_s: 104
verified: true
draft: false
---

[CF 312B - Archer](https://codeforces.com/problemset/problem/312/B)

**Rating:** 1300  
**Tags:** math, probabilities  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

Two archers shoot at a target alternately. SmallR shoots first and hits with probability $a/b$ on each shot. Zanoes hits with probability $c/d$ on each shot. As soon as someone lands the first hit of the match, the game ends and that player wins.

The input consists of four integers $a, b, c, d$, which define the two hit probabilities:

$$p=\frac{a}{b}, \qquad q=\frac{c}{d}$$

We must compute the probability that SmallR eventually wins.

The constraints are tiny. The input contains only four integers, and the answer is a single probability. There is no large data structure, no graph, and no repeated queries. The challenge is entirely mathematical. Any solution that derives a closed-form expression runs in constant time.

The main difficulty is recognizing that the game can, in principle, continue forever. A naive simulation cannot enumerate all possible sequences because there are infinitely many rounds. The probability must instead be expressed as an infinite series or solved through a recurrence.

A common mistake is to consider only the first round. For example:

```
1 2 1 2
```

SmallR hits immediately with probability $1/2$, but he can also miss, Zanoes can miss, and then SmallR gets another chance. The correct answer is $2/3$, not $1/2$.

Another subtle case occurs when both players have very small hit probabilities:

```
1 1000 1 1000
```

The match may last many rounds, but the total winning probability is still well-defined. Any approach that truncates the process after a fixed number of rounds risks losing noticeable probability mass.

A third source of errors is forgetting that SmallR shoots first. Consider:

```
1 1 1 1
```

Both players never miss. SmallR shoots before Zanoes, so he wins with probability $1$, not $1/2$.

## Approaches

The most direct approach is to enumerate all ways SmallR can win.

He can win immediately on his first shot. He can also win after both players miss once, then hit on his second attempt. He can win after both players miss twice, then hit on his third attempt, and so on.

This produces an infinite sum:

$$p + (1-p)(1-q)p + ((1-p)(1-q))^2 p + \cdots$$

Every term corresponds to a specific number of complete failed rounds before SmallR finally lands the first hit.

The brute-force version would literally evaluate many terms of this series. It is mathematically correct because each term represents a disjoint winning scenario. The problem is that the series is infinite. Truncating after $k$ terms introduces approximation error, and choosing a sufficiently large $k$ is unnecessary.

The key observation is that the series is geometric.

Let

$$r=(1-p)(1-q).$$

Then the probability becomes

$$p + rp + r^2p + r^3p + \cdots.$$

This is exactly the geometric series

$$p \sum_{i=0}^{\infty} r^i.$$

Since $0 \le r < 1$, its sum is

$$\frac{p}{1-r}.$$

Substituting back:

$$\boxed{
\frac{p}{1-(1-p)(1-q)}
}$$

This closed-form expression gives the answer in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (sum many terms) | O(k) | O(1) | Approximate only |
| Optimal (geometric series) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four integers $a, b, c, d$.
2. Compute SmallR's hit probability:

$$p=\frac{a}{b}.$$
3. Compute Zanoes's hit probability:

$$q=\frac{c}{d}.$$
4. Compute the probability that an entire round fails, meaning both players miss:

$$r=(1-p)(1-q).$$

After such a round, the game returns to exactly the same state as at the beginning.
5. Use the geometric-series formula:

$$\text{answer}
=
\frac{p}{1-r}.$$
6. Print the result with sufficient precision.

### Why it works

Let $W$ denote the probability that SmallR wins from the start of a round.

SmallR can win immediately with probability $p$.

If SmallR misses and Zanoes also misses, which happens with probability $(1-p)(1-q)$, the game returns to the original state. From that point onward the probability that SmallR eventually wins is again $W$.

Thus

$$W=p+(1-p)(1-q)W.$$

Solving for $W$:

$$W\bigl(1-(1-p)(1-q)\bigr)=p,$$

$$W=
\frac{p}{1-(1-p)(1-q)}.$$

The algorithm computes exactly this quantity, so it must return the correct winning probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, c, d = map(int, input().split())

p = a / b
q = c / d

ans = p / (1.0 - (1.0 - p) * (1.0 - q))

print(f"{ans:.12f}")
```

The program first converts the fractions into floating-point probabilities. It then computes the probability that both players miss in a complete round.

The formula

$$\frac{p}{1-(1-p)(1-q)}$$

is applied directly. Python's double-precision floating point is more than sufficient for the required $10^{-6}$ accuracy.

Printing twelve digits after the decimal point comfortably satisfies the error tolerance.

## Worked Examples

### Example 1

Input:

```
1 2 1 2
```

Here

$$p=\frac12,\qquad q=\frac12.$$

| Variable | Value |
| --- | --- |
| $p$ | 0.5 |
| $q$ | 0.5 |
| $r=(1-p)(1-q)$ | 0.25 |
| Answer $=p/(1-r)$ | 0.666666666667 |

The result is $2/3$. SmallR benefits from shooting first, so the answer is greater than $1/2$.

### Example 2

Input:

```
1 1 1 1
```

| Variable | Value |
| --- | --- |
| $p$ | 1 |
| $q$ | 1 |
| $r=(1-p)(1-q)$ | 0 |
| Answer $=p/(1-r)$ | 1 |

SmallR never misses. Since he shoots before Zanoes, the match ends immediately with SmallR's victory.

This example confirms that the formula correctly handles probabilities equal to one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed |
| Space | O(1) | No additional data structures are used |

The running time does not depend on the values of the input numbers. The solution performs a handful of floating-point computations and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    a, b, c, d = map(int, input().split())
    p = a / b
    q = c / d
    ans = p / (1.0 - (1.0 - p) * (1.0 - q))

    return f"{ans:.12f}"

# provided sample
assert run("1 2 1 2\n") == "0.666666666667"

# SmallR always hits
assert run("1 1 1 2\n") == "1.000000000000"

# Zanoes always hits if he gets a turn
assert run("1 2 1 1\n") == "0.500000000000"

# Equal small probabilities
out = float(run("1 1000 1 1000\n"))
expected = (1 / 1000) / (1 - (999 / 1000) * (999 / 1000))
assert abs(out - expected) < 1e-12

# Both always hit
assert run("1 1 1 1\n") == "1.000000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 1 2` | `0.666666666667` | Official sample |
| `1 1 1 2` | `1.000000000000` | SmallR wins immediately |
| `1 2 1 1` | `0.500000000000` | Zanoes never misses once his turn arrives |
| `1 1000 1 1000` | Computed value | Long expected game, geometric formula |
| `1 1 1 1` | `1.000000000000` | Both perfect, shooting order matters |

## Edge Cases

### SmallR always hits

Input:

```
1 1 1 2
```

We have $p=1$ and $q=1/2$.

The algorithm computes

$$r=(1-1)\left(1-\frac12\right)=0,$$

$$\text{answer}=\frac{1}{1-0}=1.$$

SmallR hits before Zanoes ever gets a shot, so probability $1$ is correct.

### Both players have tiny hit probabilities

Input:

```
1 1000 1 1000
```

The probability of a failed round is

$$r=\frac{999}{1000}\cdot\frac{999}{1000}=0.998001.$$

The game often lasts many rounds, but the formula sums all possibilities at once:

$$\text{answer}
=
\frac{0.001}{1-0.998001}
\approx 0.500250125.$$

No truncation is needed, so no probability mass is lost.

### Both always hit

Input:

```
1 1 1 1
```

The algorithm gives

$$r=0,
\qquad
\text{answer}=1.$$

A careless solution might assume symmetry and return $1/2$. The formula correctly incorporates the fact that SmallR shoots first and wins immediately.
