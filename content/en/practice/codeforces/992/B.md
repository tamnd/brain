---
title: "CF 992B - Nastya Studies Informatics"
description: "We are given four integers $l, r, x, y$. The task is to count ordered pairs $(a, b)$ such that both numbers lie inside the interval $[l, r]$, and their greatest common divisor is exactly $x$ while their least common multiple is exactly $y$."
date: "2026-06-17T00:20:47+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 992
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 489 (Div. 2)"
rating: 1600
weight: 992
solve_time_s: 77
verified: true
draft: false
---

[CF 992B - Nastya Studies Informatics](https://codeforces.com/problemset/problem/992/B)

**Rating:** 1600  
**Tags:** math, number theory  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four integers $l, r, x, y$. The task is to count ordered pairs $(a, b)$ such that both numbers lie inside the interval $[l, r]$, and their greatest common divisor is exactly $x$ while their least common multiple is exactly $y$.

Instead of thinking in terms of arbitrary integers, it helps to view the condition as a very rigid structural constraint on how $a$ and $b$ are built. The GCD forces both numbers to share a common base factor, while the LCM forces their combined prime structure to exactly match $y$. So we are not searching freely inside the interval, but rather searching for pairs that must align perfectly with a fixed arithmetic pattern.

The bounds $l, r \le 10^9$ rule out any approach that iterates over all candidate pairs. Even iterating over a single variable is borderline if done per test without structure. The solution must reduce the search space to something dependent on divisors or factorizations of $y$, not on the interval size.

A key edge situation arises when $y$ is not divisible by $x$. In that case, no pair can exist because the GCD must divide the LCM, and any valid pair must satisfy $x \mid y$. Another subtle case is when even after satisfying divisibility, one of the transformed variables falls outside the allowed interval after normalization.

For example, if $l = 1, r = 2, x = 2, y = 3$, there is no pair because $x$ does not divide $y$, even though both bounds are small enough that brute force might still try candidates.

## Approaches

A direct approach tries all pairs $(a, b)$ in the range $[l, r]$ and checks whether their GCD is $x$ and LCM is $y$. This is correct but has a worst case of $(r-l+1)^2$ checks. With $r$ up to $10^9$, even a reduced interval can still be far too large to enumerate.

The key observation is to remove the GCD constraint first by normalizing both numbers. If we set $a = x \cdot A$ and $b = x \cdot B$, then $\gcd(A, B) = 1$. This transformation isolates the common factor and reduces the problem to counting coprime pairs.

Substituting into the LCM condition, we get:

$$\text{lcm}(a, b) = x \cdot A \cdot B = y$$

which implies:

$$A \cdot B = \frac{y}{x} = k$$

So the entire problem reduces to counting ordered factor pairs $(A, B)$ such that $A \cdot B = k$, $\gcd(A, B) = 1$, and both $xA, xB$ lie in $[l, r]$.

This gives a clean structure: we only need to enumerate divisors of $k$, and for each divisor $A$, define $B = k / A$, then check coprimality and interval constraints.

The brute force fails because it searches in a 2D space of size $O(r^2)$, while the transformed problem only depends on divisor structure, which is $O(\sqrt{k})$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((r-l+1)^2)$ | $O(1)$ | Too slow |
| Optimal | $O(\sqrt{y/x})$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. First check whether $y$ is divisible by $x$. If not, the answer is immediately zero because no scaling of a GCD can produce a non-multiple LCM. This avoids unnecessary work.
2. Compute $k = y / x$. We now reinterpret the problem in terms of factor pairs of $k$, where each valid pair corresponds to $(A, B)$.
3. Iterate over all integers $A$ such that $A \cdot A \le k$. Each such $A$ represents a potential divisor of $k$, and we can compute $B = k / A$ when $A$ divides $k$.
4. For each divisor $A$, check whether $k \bmod A = 0$. If not, skip it since it cannot form a valid pair.
5. Let $B = k / A$. Check whether $\gcd(A, B) = 1$. This condition ensures that the original numbers $xA$ and $xB$ have GCD exactly $x$, not larger.
6. Convert back to the original domain by verifying bounds: $l \le xA \le r$ and $l \le xB \le r$.
7. If all conditions hold, count the ordered pairs. If $A \ne B$, both $(A, B)$ and $(B, A)$ are valid, so add 2. If $A = B$, add 1.

### Why it works

Any valid pair $(a, b)$ must share a greatest common divisor $x$, so dividing both numbers by $x$ produces integers $A$ and $B$ that are coprime. The LCM condition forces their product to be exactly $y/x$, so every valid pair corresponds bijectively to a coprime factorization of $k$. The bounds only filter which of these factorizations actually lie inside the interval. Since every step preserves equivalence in both directions, no valid pair is lost and no invalid pair is introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def solve():
    l, r, x, y = map(int, input().split())
    
    if y % x != 0:
        print(0)
        return
    
    k = y // x
    ans = 0
    
    for a in range(1, int(math.isqrt(k)) + 1):
        if k % a != 0:
            continue
        b = k // a
        
        if math.gcd(a, b) != 1:
            continue
        
        A = x * a
        B = x * b
        
        if l <= A <= r and l <= B <= r:
            if a == b:
                ans += 1
            else:
                ans += 2
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code begins by validating the necessary divisibility condition between $x$ and $y$. Without it, the transformed equation $A \cdot B = k$ would not even be integral, so the search space collapses immediately.

The loop over divisors uses $\sqrt{k}$ because every divisor pair is encountered exactly once through $a$ and $k/a$. The gcd check enforces that no extra common factor remains after removing $x$, which is essential for correctness of the reverse transformation.

The boundary check is applied after reconstructing the original values $a = xA$ and $b = xB$, since the constraints are defined in the original domain rather than the normalized one.

## Worked Examples

### Example 1

Input:

```
1 2 1 2
```

Here $k = 2$. Divisors are (1, 2).

| A | B | gcd(A,B) | xA | xB | valid |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 1 | 2 | yes |
| 2 | 1 | 1 | 2 | 1 | yes |

Both pairs are inside bounds, so answer is 2.

This confirms that ordering is preserved and both symmetric configurations are counted.

### Example 2

Input:

```
1 12 3 12
```

Here $k = 4$. Divisors are (1,4), (2,2), (4,1).

| A | B | gcd(A,B) | xA | xB | valid |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 3 | 12 | yes |
| 2 | 2 | 2 | 6 | 6 | no |
| 4 | 1 | 1 | 12 | 3 | yes |

Answer is 2 valid ordered pairs.

This example shows how the coprimality condition eliminates diagonal factorizations where shared factors remain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{y/x})$ | We enumerate divisors of $k = y/x$, and each check is constant time |
| Space | $O(1)$ | Only a few integers are stored regardless of input size |

The divisor bound ensures the solution comfortably fits within 1 second even when $y$ is up to $10^9$, since the loop runs at most about $3 \times 10^4$ iterations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    l, r, x, y = map(int, sys.stdin.readline().split())
    
    if y % x != 0:
        return "0\n"
    
    k = y // x
    ans = 0
    
    for a in range(1, int(math.isqrt(k)) + 1):
        if k % a != 0:
            continue
        b = k // a
        if math.gcd(a, b) != 1:
            continue
        A = x * a
        B = x * b
        if l <= A <= r and l <= B <= r:
            ans += 1 if a == b else 2
    
    return str(ans) + "\n"

# provided samples
assert run("1 2 1 2\n") == "2\n", "sample 1"

# custom cases
assert run("1 1 1 1\n") == "1\n", "single point"
assert run("1 10 2 20\n") == "2\n", "simple factor pairs"
assert run("1 100 3 12\n") == "2\n", "multiple divisors with gcd filtering"
assert run("1 100 5 7\n") == "0\n", "impossible case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 1 | minimal boundary case |
| 1 10 2 20 | 2 | basic valid factor pairs |
| 1 100 3 12 | 2 | gcd filtering correctness |
| 1 100 5 7 | 0 | invalid divisibility case |

## Edge Cases

One important edge case is when $y$ is not divisible by $x$. For example, with input $l=1, r=100, x=4, y=6$, the transformation would require $A \cdot B = 1.5$, which is impossible. The algorithm immediately returns zero before attempting any divisor search.

Another edge case is when $A = B$, meaning $k$ is a perfect square. In that situation, only one ordering exists instead of two. For example, $x=2, y=8$ gives $k=4$, and the pair $A=B=2$ produces exactly one valid configuration.

A third case is boundary clipping: even if a factor pair is valid in normalized form, scaling by $x$ can push it outside $[l, r]$. For instance, $l=10, r=12, x=3, y=12$ produces normalized pair $(1,4)$, but $3\cdot4=12$ is valid while $3\cdot1=3$ is not, so only one direction survives after bounds filtering.
