---
problem: 983A
contest_id: 983
problem_index: A
name: "Finite or not?"
contest_name: "Codeforces Round 483 (Div. 1) [Thanks, Botan Investments and Victor Shaburov!]"
rating: 1700
tags: ["implementation", "math"]
answer: passed_samples
verified: true
solve_time_s: 67
date: 2026-06-18
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a33757e-78f4-83ec-b62c-055c2636f4e3
---

# CF 983A - Finite or not?

**Rating:** 1700  
**Tags:** implementation, math  
**Model:** gpt-5-5  
**Solve time:** 1m 7s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a33757e-78f4-83ec-b62c-055c2636f4e3  

---

## Solution

## Problem Understanding

We are given a rational number $p/q$ and asked to determine whether its representation is finite when written in base $b$. A finite representation means that after some point, the expansion stops and no further digits are needed, similar to how $1/2 = 0.5$ in base 10.

Each query gives three integers: a numerator $p$, a denominator $q$, and a base $b$. The task is not to compute the expansion, but only to decide whether it would terminate.

The constraints are large: up to $10^5$ queries and values up to $10^{18}$. This rules out any approach that simulates division or constructs representations digit by digit. Even a single long division per query would be infeasible because the denominator and base can be large enough that intermediate states would require arbitrary precision arithmetic and potentially many iterations.

A subtle point is that $p$ is irrelevant to the finiteness of the representation. For example, $6/12$ and $1/2$ have the same termination behavior in any base. So the problem is fundamentally about $q$ and $b$, not about $p$.

Edge cases appear when the fraction is already an integer. For instance, if $p = 12$ and $q = 3$, the result is $4$, which always terminates regardless of base. A naive approach might still try to analyze prime factors unnecessarily, but this case should be immediately classified as finite.

Another edge case arises when the base shares all prime factors of the reduced denominator. For example, $1/3$ in base 3 is finite because $3$ divides the base. In base 10 it is infinite because $3$ does not divide $2 \cdot 5$.

## Approaches

A brute-force interpretation would attempt to simulate division of $p/q$ in base $b$, repeatedly multiplying the remainder by $b$ and extracting digits. This works in principle because a fraction terminates exactly when the remainder becomes zero at some step. However, the remainder can cycle for a long time, potentially up to $q$ distinct states. With $q$ as large as $10^{18}$, this becomes impossible even for a single query.

The key structural insight is to move away from representation and instead study number theory. A rational number has a finite expansion in base $b$ exactly when the reduced denominator has no prime factors other than those already present in $b$. After reducing $p/q$ to lowest terms, the condition depends only on whether every prime factor of $q$ also divides $b$.

This reduces the problem to repeated gcd simplification and then stripping from $q$ all factors shared with $b$. If anything remains in $q$, that remaining part introduces an incompatible prime factor, forcing an infinite expansion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate division) | $O(q)$ per query | $O(1)$ | Too slow |
| Optimal (prime factor reduction via gcd stripping) | $O(\log \min(q,b))$ amortized per query | $O(1)$ | Accepted |

## Algorithm Walkthrough

We work with each query independently.

1. First reduce the fraction by computing $g = \gcd(p, q)$ and setting $q \leftarrow q/g$.

This step removes all common factors so that we only analyze the irreducible denominator. Any factor shared earlier cannot affect termination because it cancels out in the fraction.
2. Remove from $q$ all prime factors that are also present in the base $b$.

We repeatedly compute $g = \gcd(q, b)$. If $g > 1$, we divide $q \leftarrow q/g$.

This works because $\gcd(q, b)$ extracts exactly the product of shared primes, even without factorizing either number.
3. Repeat the previous step until $\gcd(q, b) = 1$. At that point, no remaining factor of $q$ can be produced by powers of $b$.
4. If the final $q$ equals 1, the denominator has been fully absorbed by the base and the representation terminates. Otherwise, at least one prime factor of $q$ is incompatible with $b$, making the expansion infinite.

### Why it works

A rational number has a terminating expansion in base $b$ exactly when its reduced denominator divides some power of $b$. That condition is equivalent to saying every prime factor of the denominator must also appear in $b$. The repeated gcd removal process systematically strips from $q$ all factors compatible with $b$. If anything survives, it is a prime factor that can never be introduced by multiplying by $b$, which guarantees that the remainder in base expansion never vanishes.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math

def solve():
    n = int(input())
    for _ in range(n):
        p, q, b = map(int, input().split())

        g = math.gcd(p, q)
        q //= g

        # remove all factors of q that are in b
        while True:
            g = math.gcd(q, b)
            if g == 1:
                break
            while q % g == 0:
                q //= g

        if q == 1:
            print("Finite")
        else:
            print("Infinite")

if __name__ == "__main__":
    solve()
```

The first step reduces the fraction to lowest terms, ensuring we do not carry irrelevant factors from $p$. The loop then repeatedly extracts any overlap between the denominator and base using gcd, which is efficient even for $10^{18}$-sized numbers.

The inner division loop is necessary because $\gcd(q, b)$ may contain multiple occurrences of a factor, and we must fully remove it from $q$ before recomputing. This guarantees that each iteration strictly reduces $q$, preventing infinite looping.

## Worked Examples

### Example 1

Input:

```
6 12 10
```

| Step | p | q | b | gcd(q,b) | Action |
| --- | --- | --- | --- | --- | --- |
| init | 6 | 12 | 10 | - | reduce fraction |
| reduce | 6 | 2 | 10 | - | divide by gcd(6,12)=6 |
| loop | 6 | 2 | 10 | 2 | remove factor 2 |
| final | 6 | 1 | 10 | 1 | stop |

Since $q = 1$, output is Finite.

This demonstrates that once the denominator becomes fully composed of base factors, the expansion terminates.

### Example 2

Input:

```
4 3 10
```

| Step | p | q | b | gcd(q,b) | Action |
| --- | --- | --- | --- | --- | --- |
| init | 4 | 3 | 10 | - | reduce fraction |
| reduce | 4 | 3 | 10 | - | already reduced |
| loop | 4 | 3 | 10 | 1 | stop immediately |

Since $q = 3 \neq 1$, output is Infinite.

This shows a case where the denominator contains a prime not present in the base, so no reduction is possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log q \cdot \log b)$ per query | Each gcd and division step reduces the denominator, and gcd runs in logarithmic time |
| Space | $O(1)$ | Only a constant number of integers are maintained |

The total work across $10^5$ queries remains efficient because each denominator shrinks quickly under repeated gcd removal, and large inputs do not lead to long cycles.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        n = int(input())
        for _ in range(n):
            p, q, b = map(int, input().split())

            g = math.gcd(p, q)
            q //= g

            while True:
                g = math.gcd(q, b)
                if g == 1:
                    break
                while q % g == 0:
                    q //= g

            print("Finite" if q == 1 else "Infinite")

    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# provided samples
assert run("2\n6 12 10\n4 3 10\n") == "Finite\nInfinite"

# custom cases
assert run("1\n0 5 10\n") == "Finite"  # zero numerator
assert run("1\n10 1 2\n") == "Finite"  # integer result
assert run("1\n1 6 10\n") == "Infinite"  # 6 has factor 3
assert run("1\n1 8 2\n") == "Finite"  # denominator only 2-power
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0/5 | Finite | zero numerator edge case |
| 10/1 | Finite | integer fraction |
| 1/6 in base 10 | Infinite | missing prime factor |
| 1/8 in base 2 | Finite | compatible prime factor only |

## Edge Cases

One important edge case is when the numerator is zero. For input $0/q$, the value is always zero, which has a terminating representation in any base. After reduction, $p=0$ makes $\gcd(p,q)=q$, so $q$ becomes 1 immediately. The algorithm correctly outputs Finite without any further processing.

Another case is when the fraction is already an integer. For example $10/2$ reduces to $5/1$. The denominator becomes 1 at the first step, and the algorithm terminates immediately. This avoids unnecessary gcd loops and confirms correctness for all integer-valued fractions.

A third case is when the denominator contains only factors present in the base but in high multiplicity, such as $1/8$ in base 2. Repeated gcd extraction removes all factors cleanly because gcd always extracts at least one full overlap with the base structure, and repeated division ensures complete elimination, eventually reducing $q$ to 1.