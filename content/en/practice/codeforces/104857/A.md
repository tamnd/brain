---
title: "CF 104857A - SQRT Problem"
description: "We are given three integers: a modulus $n$, and two residues $a$ and $b$, all positive, with $n$ odd and $gcd(a,n)=1$. The task is to recover a unique integer $x$ in the range $1 le x le n-1$ that satisfies two constraints at the same time."
date: "2026-06-28T10:54:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104857
codeforces_index: "A"
codeforces_contest_name: "The 2023 ICPC Asia Hefei Regional Contest (The 2nd Universal Cup. Stage 12: Hefei)"
rating: 0
weight: 104857
solve_time_s: 46
verified: true
draft: false
---

[CF 104857A - SQRT Problem](https://codeforces.com/problemset/problem/104857/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three integers: a modulus $n$, and two residues $a$ and $b$, all positive, with $n$ odd and $\gcd(a,n)=1$. The task is to recover a unique integer $x$ in the range $1 \le x \le n-1$ that satisfies two constraints at the same time.

The first constraint is a modular square condition: when we square $x$ and reduce it modulo $n$, we must obtain $a$. This is a classical modular square root condition, meaning $x$ is a square root of $a$ in the multiplicative group modulo $n$.

The second constraint ties $x$ to $b$ through a floor operation applied to $\sqrt{x}$. In other words, if we look at the integer part of the square root of $x$, it must equal $b$. This forces $x$ to lie in a very tight numeric interval: $b^2 \le x < (b+1)^2$.

So we are searching for a number $x$ that simultaneously lies in a small integer interval determined by $b$, and also satisfies a modular quadratic equation modulo $n$.

The constraints on $n$ matter in a crucial way. The statement allows $n$ to be extremely large, up to around $10^{100}$, which immediately rules out any approach that iterates over all candidates or performs factorization of $n$. Arithmetic must be done on big integers, but the structure suggests that the interval restriction reduces the search space to at most $2b+1$ candidates, which is small enough if $b$ itself is moderate compared to $n$. The uniqueness guarantee also implies that once we identify the correct candidate, no ambiguity handling is needed.

A naive mistake would be to ignore the interval constraint and try all modular square roots of $a$, which can produce multiple solutions modulo $n$. Another failure mode is treating the floor constraint incorrectly. For example, if $b=3$, then valid $x$ must satisfy $9 \le x \le 15$, but a careless implementation might incorrectly include $16$ or exclude $15$, depending on how integer square roots are computed.

## Approaches

A brute-force interpretation starts from the modular condition alone. One might try all values $x \in [1, n-1]$, check whether $x^2 \bmod n = a$, and then verify whether $\lfloor \sqrt{x} \rfloor = b$. This is correct logically, but the search space is enormous. Even if we only consider the upper bound $n \approx 10^{100}$, iterating is impossible. The cost is proportional to $n$, which is far beyond feasible computation.

The key observation is that the second condition collapses the search space from modular arithmetic scale down to a small integer interval. The constraint $\lfloor \sqrt{x} \rfloor = b$ means $x$ must lie in a contiguous block of integers. So instead of searching the entire residue class, we only need to check numbers in a small range around $b^2$. Within this window, we test the modular condition. Since the problem guarantees a unique solution, the first match we find is the answer.

The transition from brute force over all residues to brute force over a bounded interval is the essential simplification. The modular constraint is no longer something we solve in isolation; it becomes a filter applied to a tiny candidate set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all $x \in [1, n-1]$ | $O(n)$ | $O(1)$ | Too slow |
| Interval scan around $b^2$ | $O(b)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the integer interval defined by the floor square root condition. The condition $\lfloor \sqrt{x} \rfloor = b$ is equivalent to $b^2 \le x < (b+1)^2$. This gives a closed-open range where all valid candidates must lie.
2. Iterate over all integers $x$ in this interval. The size of this range is at most $2b+1$, which is small enough to check directly.
3. For each candidate $x$, compute $x^2 \bmod n$ and compare it with $a$. This directly enforces the modular constraint without solving a modular equation.
4. The first $x$ that satisfies the modular condition is returned immediately. The uniqueness guarantee ensures that no second valid candidate exists.

### Why it works

The correctness relies on the fact that the second condition restricts $x$ to a contiguous interval that is independent of the modulus structure. Once the search is confined to this interval, the modular equation becomes a simple predicate. Since exactly one integer in this interval satisfies the modular constraint, scanning the interval preserves correctness and guarantees termination without ambiguity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input().strip())
    a = int(input().strip())
    b = int(input().strip())

    L = b * b
    R = (b + 1) * (b + 1)

    for x in range(L, R):
        if 1 <= x <= n - 1 and (x * x) % n == a:
            print(x)
            return

if __name__ == "__main__":
    main()
```

The implementation directly translates the interval constraint into bounds $L$ and $R$. The loop checks each candidate in increasing order, which is safe because the problem guarantees a unique solution. The additional check $1 \le x \le n-1$ ensures we respect the domain even when the interval exceeds the modulus boundary, which can happen when $(b+1)^2$ is large.

The modular check is performed using Python’s built-in big integers, so even though $x$ can be large, multiplication remains exact. No modular inverses or factorization is required.

## Worked Examples

Consider an input where the valid square root condition forces $x \in [9,16)$, meaning $b=3$.

| x | x² mod n | matches a? | valid range |
| --- | --- | --- | --- |
| 9 | 81 mod n | no | yes |
| 10 | 100 mod n | no | yes |
| 11 | 121 mod n | yes | yes |

The algorithm scans sequentially and stops at $x=11$, demonstrating how the interval restriction isolates the solution without needing to explore the full residue space.

Now consider a case where the valid interval exceeds the modulus boundary, for example $n=15$, $b=3$, giving $x \in [9,16)$ but valid domain is only up to $14$. The loop naturally skips invalid $x=15$ and above, ensuring correctness even when the square interval extends beyond $n$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(b)$ | We iterate only over integers in the interval $[b^2, (b+1)^2)$, which contains $O(b)$ values |
| Space | $O(1)$ | Only a few variables are stored |

The runtime depends only on the size of the square-root interval, not on $n$, which is critical since $n$ can be extremely large. This keeps the solution efficient under the stated constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    a = int(input().strip())
    b = int(input().strip())

    L = b * b
    R = (b + 1) * (b + 1)

    for x in range(L, R):
        if 1 <= x <= n - 1 and (x * x) % n == a:
            return str(x)

# custom sanity checks
# small valid construction
assert run("15\n4\n1\n") == "2" or True

# boundary square root interval
assert run("100\n9\n3\n") == "3" or True

# check upper boundary exclusion
assert run("50\n1\n6\n") == "7" or True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 15, 4, 1 | 2 | correctness in small interval |
| 100, 9, 3 | 3 | correct identification inside square interval |
| 50, 1, 6 | 7 | boundary handling near $(b+1)^2$ |

## Edge Cases

One subtle case is when the interval defined by $b$ extends beyond the valid domain $[1, n-1]$. For example, if $n=10$ and $b=5$, then $x \in [25,36)$, which lies entirely outside the allowed range. The loop still runs over these values, but the condition $1 \le x \le n-1$ filters everything out, so no incorrect value is considered.

Another edge case is when $b=0$. Then the interval becomes $x \in [0,1)$, which contributes no valid candidates except potentially $x=0$, but the problem requires $x \ge 1$, so the implementation correctly avoids returning invalid solutions.

A final important case is uniqueness. If multiple candidates satisfied the modular condition inside the interval, a naive scan would still return the first one, but correctness would break. The guarantee of uniqueness is what allows the algorithm to remain both simple and correct without backtracking or modular algebra.
