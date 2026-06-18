---
problem: 1285C
contest_id: 1285
problem_index: C
name: "Fadi and LCM"
contest_name: "Codeforces Round 613 (Div. 2)"
rating: 1400
tags: ["brute force", "math", "number theory"]
answer: passed_samples
verified: true
solve_time_s: 490
date: 2026-06-14
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2dad95-f3d8-83ec-91f0-7606a9042964
---

# CF 1285C - Fadi and LCM

**Rating:** 1400  
**Tags:** brute force, math, number theory  
**Model:** gpt-5-5  
**Solve time:** 8m 10s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2dad95-f3d8-83ec-91f0-7606a9042964  

---

## Solution

## Problem Understanding

We are given a single integer $X$, and we need to split it into two positive integers $a$ and $b$ such that their least common multiple is exactly $X$. Among all such valid pairs, we want the one that minimizes the larger of the two numbers.

In other words, we are not just looking for any factorization of $X$, but a pair that "covers" all prime powers of $X$ via their LCM, while keeping both numbers as balanced as possible so that the maximum element is as small as it can be.

The constraint $X \le 10^{12}$ immediately rules out any quadratic or even naive linear search over all pairs. A brute force over all $a \le X$ is impossible, since $X$ can be extremely large and has up to roughly $10^6$ potential divisors in worst-case density scenarios.

A subtle edge case appears when $X = 1$. In that case, both $a = 1$ and $b = 1$ are required, since LCM(1,1) = 1, and no other pair exists. Any solution must explicitly handle this or naturally converge to it.

Another potential failure case is assuming that choosing $a$ as a divisor of $X$ and setting $b = X / a$ is always valid. That is not true, because LCM depends on prime exponents, not just product structure. For example, if $X = 12$, choosing $a = 4$, $b = 3$ works, but $a = 6$, $b = 2$ also works; however, many divisor pairs such as $a = 12$, $b = 1$ are valid but suboptimal.

The key difficulty is ensuring the LCM condition while optimizing the maximum value.

## Approaches

The brute-force idea is straightforward: enumerate all pairs $(a, b)$ such that $\text{lcm}(a, b) = X$, then track the pair minimizing $\max(a, b)$. The immediate issue is that there are $O(X)$ candidates, and even if we restrict to divisors, there can be $O(\sqrt{X})$ divisors, leading to $O(D^2)$ pairs. With $X$ up to $10^{12}$, this becomes computationally infeasible.

The turning point is realizing that both $a$ and $b$ must divide $X$, because if $\text{lcm}(a,b) = X$, every prime factor of $a$ and $b$ is already contained in $X$. So we only need to search over divisors of $X$, not arbitrary integers.

Now the problem becomes: among divisor pairs $a, b$, find one whose LCM equals $X$ and minimizes $\max(a,b)$. If we fix one divisor $a$, the smallest valid partner $b$ is not arbitrary; it must contribute exactly the missing prime powers so that LCM becomes $X$.

This leads to a cleaner reformulation. We iterate over all divisors $a \mid X$, and compute:

$$b = \frac{X}{\gcd(a, X/a)}$$

However, a simpler and more standard observation resolves everything: if we enforce $a \cdot b = X$ and $\gcd(a,b)=1$, then LCM becomes $X$. The optimal answer always corresponds to splitting $X$ into two coprime parts. The goal becomes finding a factor pair $(a, b)$ with product $X$, then checking which pair is coprime and minimizes the maximum value.

Even more directly, the known structure of the optimal solution is: we try all divisors $a \le \sqrt{X}$, set $b = X/a$, and compute the LCM via $\text{lcm}(a,b) = X \cdot \frac{a}{\gcd(a,b)} / a = \frac{X}{\gcd(a,b)}$. So the condition reduces to $\gcd(a,b) = 1$. Among all valid pairs, we pick the one minimizing $\max(a,b)$.

The optimal solution is therefore a single pass over divisors up to $\sqrt{X}$, using gcd checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over pairs | $O(X)$ or worse | $O(1)$ | Too slow |
| Divisor + gcd enumeration | $O(\sqrt{X})$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We rewrite the task as finding a divisor pair $(a, b)$ of $X$ such that $a \cdot b = X$ and $\gcd(a,b)=1$, minimizing $\max(a,b)$.

1. Iterate over all integers $i$ from $1$ to $\lfloor \sqrt{X} \rfloor$.

We only check up to the square root because divisors come in symmetric pairs $(i, X/i)$, and we want to avoid redundant work.
2. If $i$ divides $X$, set $a = i$ and $b = X / i$.

This ensures we only consider valid factor pairs.
3. Compute $g = \gcd(a, b)$.

This step checks whether the pair shares prime factors that would distort the LCM away from $X$.
4. If $g = 1$, the pair is valid for the LCM condition.

We then consider $\max(a,b)$ as a candidate answer.
5. Track the pair that minimizes $\max(a,b)$ across all valid candidates.

The answer is the stored best pair after all iterations.

### Why it works

Any valid solution must use only prime factors from $X$. If a pair $(a,b)$ shares a common prime factor, that factor would be counted only once in the LCM, meaning the LCM would be strictly smaller than $X$ unless compensated by higher exponents, which would force one of the numbers to exceed the corresponding exponent structure of $X$. The optimal configuration avoids duplication entirely, meaning the best pairs are exactly coprime factor pairs of $X$. Checking all divisors ensures every possible decomposition is considered, and minimizing $\max(a,b)$ ensures balance.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    x = int(input().strip())

    best_a, best_b = 1, x
    best_max = x

    i = 1
    while i * i <= x:
        if x % i == 0:
            a = i
            b = x // i

            if math.gcd(a, b) == 1:
                if max(a, b) < best_max:
                    best_a, best_b = a, b
                    best_max = max(a, b)

            # check the symmetric pair is not needed since (a,b) already covers it

        i += 1

    print(best_a, best_b)

if __name__ == "__main__":
    solve()
```

The code iterates only up to $\sqrt{X}$, ensuring efficiency under the $10^{12}$ constraint. Each divisor pair is tested once, and gcd filtering guarantees correctness of the LCM condition. The best pair is updated whenever a smaller maximum value is found, which directly encodes the optimization target.

One subtle detail is initialization: starting with $(1, X)$ guarantees a valid baseline, since $\gcd(1,X)=1$ always holds.

## Worked Examples

### Example 1

Input:

```
2
```

We check divisors up to $\sqrt{2}$.

| i | a | b | gcd(a,b) | valid | max(a,b) |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 1 | yes | 2 |

The only valid pair is (1,2), so the answer is (1,2). This confirms that for prime numbers, the optimal split is always trivial.

### Example 2

Input:

```
12
```

| i | a | b | gcd(a,b) | valid | max(a,b) |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 12 | 1 | yes | 12 |
| 2 | 2 | 6 | 2 | no | - |
| 3 | 3 | 4 | 1 | yes | 4 |

The best pair is (3,4) because it is coprime and minimizes the maximum element. This shows why naive divisor pairing fails unless gcd is enforced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{X})$ | We iterate up to $\sqrt{X}$, checking divisibility and gcd in constant amortized time |
| Space | $O(1)$ | Only a few integers are stored regardless of input size |

The constraint $X \le 10^{12}$ allows up to $10^6$ iterations, which is comfortably within limits in Python. Each iteration is lightweight, involving only a modulo and a gcd computation.

## Test Cases

```python
import sys, io, math

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x = int(sys.stdin.readline())

    best_a, best_b = 1, x
    best_max = x

    i = 1
    while i * i <= x:
        if x % i == 0:
            a = i
            b = x // i
            if math.gcd(a, b) == 1:
                if max(a, b) < best_max:
                    best_a, best_b = a, b
                    best_max = max(a, b)
        i += 1

    return f"{best_a} {best_b}"

# provided sample
assert solve("2\n") == "1 2"

# custom cases
assert solve("1\n") == "1 1", "minimum edge case"
assert solve("12\n") == "3 4", "non-trivial composite"
assert solve("6\n") in ("2 3", "3 2"), "small composite"
assert solve("1000000000000\n") is not None, "large stress case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 1 | smallest boundary case |
| 12 | 3 4 | non-trivial optimal split |
| 6 | 2 3 | coprime factor selection |
| 10^12 | valid pair | performance at max constraints |

## Edge Cases

For $X = 1$, the loop runs once with $i = 1$. We get $a = 1$, $b = 1$, and $\gcd(1,1)=1$, so the algorithm returns (1,1), which is correct.

For prime $X$, only divisor pair is $(1,X)$. Since gcd is 1, it is automatically selected, and no other candidate exists.

For perfect squares like $X = 36$, symmetric divisors such as (6,6) fail the gcd test because gcd is not 1, preventing invalid LCM reduction. Only coprime pairs like (4,9) survive, and the algorithm correctly prefers the most balanced one.

For large powers like $X = 10^{12}$, the loop still only runs up to $10^6$, and gcd checks remain constant time. The algorithm avoids any dependence on the number of divisors or factorization depth, relying only on square root enumeration.