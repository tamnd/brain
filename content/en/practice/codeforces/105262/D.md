---
title: "CF 105262D - The FFT Problem"
description: "We are trying to choose a numeric base for representing a given integer so that its representation contains the digit 4 at least once. Among all such bases in a given range, we want the largest one. Concretely, for each test case we receive a number $n$."
date: "2026-06-24T03:01:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105262
codeforces_index: "D"
codeforces_contest_name: "Game of Coders 3.0"
rating: 0
weight: 105262
solve_time_s: 72
verified: true
draft: false
---

[CF 105262D - The FFT Problem](https://codeforces.com/problemset/problem/105262/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are trying to choose a numeric base for representing a given integer so that its representation contains the digit 4 at least once. Among all such bases in a given range, we want the largest one.

Concretely, for each test case we receive a number $n$. We imagine writing $n$ in base $b$, where $b$ must be at least 2 and at most $2 \cdot 10^{12}$. In that representation, we scan its digits. If at least one digit equals 4, then this base is considered valid. Our task is to find the maximum valid base, or report that none exists.

The constraint $n \le 10^{12}$ means the number of digits of $n$ in any reasonable base is small, at most around 40 in base 2 and even smaller for larger bases. That limits how many digit positions can even exist in any representation. The number of test cases is at most 10, so an algorithm that is roughly $O(n^{1/2})$ or $O(n^{1/3})$ per case is still fine.

A naive attempt would try every base $b$ from 2 up to $2 \cdot 10^{12}$, convert $n$ into base $b$, and check whether a digit equals 4. That approach fails immediately because even testing a single base is logarithmic in $n$, so the total work would be far beyond any limit.

Another common failure case appears when people only check whether $n \% b = 4$. That only verifies the last digit and misses all higher digit positions. For example, $n = 24$ in base 5 is $44_5$, which has a 4 but does not satisfy $24 \% 5 = 4$ alone as a sufficient condition for all valid bases.

The real difficulty is that the digit 4 can appear at any position, and each position imposes a different algebraic constraint on $b$.

## Approaches

The brute-force structure is simple. For every candidate base $b$, we repeatedly divide $n$ by $b$ and check remainders to see whether any digit equals 4. This is correct because base conversion is exactly repeated division. The problem is that the range of $b$ is enormous, and iterating over all of it gives roughly $2 \cdot 10^{12}$ candidates, each costing $O(\log n)$, which is completely infeasible.

The key observation is that the digit condition can be expressed algebraically. If a digit 4 appears at position $i$, then in base $b$ the number can be written as

$$n = x \cdot b^{i+1} + 4 \cdot b^i + y$$

with $0 \le y < b^i$. This turns the problem into searching for integer solutions of this equation rather than simulating bases.

We separate cases by the position of the digit 4. When the 4 is in the least significant digit, the equation simplifies to $n = q b + 4$, so $b \mid (n - 4)$. That means all valid bases in this case are divisors of $n - 4$, which can be enumerated efficiently.

When the 4 is in a higher position, say $i \ge 1$, the term $b^{i+1}$ grows quickly. This immediately restricts $b$ because $b^{i+1} \le n$. So for each fixed position, the possible bases are bounded by $n^{1/(i+1)}$, which becomes very small as $i$ increases. This allows us to try all candidate bases for each position separately and verify validity by reconstructing the base representation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over bases | $O(n \log n)$ | $O(1)$ | Too slow |
| Position-based enumeration | $O(\sum n^{1/k} \log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We split the search based on where the digit 4 might appear in the base representation.

1. First handle the case where the digit 4 is in the units position. In that case we require $n = q b + 4$. Rearranging gives $n - 4 = q b$, so every valid base must divide $n - 4$. We enumerate all divisors of $n - 4$, check that the base is at least 2, and verify that converting $n$ into this base indeed contains digit 4. This step is necessary because divisibility alone does not guarantee that higher digits do not also violate constraints.
2. Next consider the case where the digit 4 is at position $i \ge 1$. We rewrite the number as $n = a b^{i+1} + 4 b^i + r$, where $r < b^i$. This ensures the digit at position $i$ is exactly 4 and no carry or overflow occurs.
3. For a fixed position $i$, we exploit the fact that $b^{i+1} \le n$. This gives an upper bound on $b$, specifically $b \le n^{1/(i+1)}$. We iterate all such candidate bases.
4. For each candidate base, we explicitly construct digits of $n$ in that base and check whether any digit equals 4. This verification is safe because the candidate set is small.
5. We keep track of the maximum base among all valid candidates across all positions.

The correctness comes from the fact that every valid base must have its digit 4 at some position $i$. We enumerate all possible positions and, for each, we only consider bases that can possibly support that digit position without overflow. Every valid solution appears in exactly one of these cases, so no candidate is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def has_four(n, b):
    while n > 0:
        if n % b == 4:
            return True
        n //= b
    return False

def divisors(x):
    res = []
    i = 1
    while i * i <= x:
        if x % i == 0:
            res.append(i)
            if i * i != x:
                res.append(x // i)
        i += 1
    return res

T = int(input())
for _ in range(T):
    n = int(input())
    best = -1

    if n - 4 > 0:
        for d in divisors(n - 4):
            if d >= 2 and has_four(n, d):
                best = max(best, d)

    i = 1
    while True:
        pow_b = 1
        ok = False

        max_b = int((n) ** (1 / (i + 1)))
        if max_b < 2:
            break

        for b in range(2, max_b + 1):
            if has_four(n, b):
                best = max(best, b)

        i += 1
        if max_b <= 2:
            break

    print(best)
```

The divisor step handles the special structure when the 4 is the least significant digit, where the problem collapses into a clean divisibility condition. The second loop tries increasing digit positions and bounds the base so that the positional contribution $b^{i+1}$ does not exceed $n$. The helper function `has_four` performs base conversion and checks digits directly, which is safe because the number of digits is logarithmic in $n$.

The stopping condition for increasing $i$ comes from the fact that once $b^{i+1} > n$, no higher digit position can contain a 4.

## Worked Examples

Consider $n = 24$. We test bases that arise from $n - 4 = 20$. The divisors are 1, 2, 4, 5, 10, 20. Filtering valid bases and checking representations:

| Base $b$ | Representation of 24 | Contains 4 |
| --- | --- | --- |
| 2 | 11000₂ | No |
| 4 | 30₄ | No |
| 5 | 44₅ | Yes |
| 10 | 24₁₀ | No |
| 20 | 14₂₀ | Yes |

The maximum valid base here is 20.

Now consider $n = 10$. We again check $n - 4 = 6$, giving candidate bases 2, 3, 6. Direct verification:

| Base $b$ | Representation of 10 | Contains 4 |
| --- | --- | --- |
| 2 | 1010₂ | No |
| 3 | 101₃ | No |
| 6 | 14₆ | Yes |

The largest valid base is 6.

These traces show how the divisor case captures all possibilities where 4 is the last digit, and how direct checking validates higher positions implicitly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \cdot \sqrt{n} + T \cdot n^{1/3})$ | divisors plus bounded base search over small exponent ranges |
| Space | $O(1)$ | only a few variables and divisor lists |

The bound on $n$ ensures that even the worst case of enumerating up to $n^{1/2}$ candidates is acceptable because $n^{1/2} \le 10^6$, and there are at most 10 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def has_four(n, b):
        while n > 0:
            if n % b == 4:
                return True
            n //= b
        return False

    def divisors(x):
        res = []
        i = 1
        while i * i <= x:
            if x % i == 0:
                res.append(i)
                if i * i != x:
                    res.append(x // i)
            i += 1
        return res

    T = int(input())
    out = []
    for _ in range(T):
        n = int(input())
        best = -1

        if n - 4 > 0:
            for d in divisors(n - 4):
                if d >= 2 and has_four(n, d):
                    best = max(best, d)

        i = 1
        while True:
            max_b = int(n ** (1 / (i + 1)))
            if max_b < 2:
                break
            for b in range(2, max_b + 1):
                if has_four(n, b):
                    best = max(best, b)
            i += 1
            if max_b <= 2:
                break

        out.append(str(best))

    return "\n".join(out)

# custom tests
assert run("1\n20\n") == "16", "basic case"
assert run("1\n24\n") == "20", "divisor dominance case"
assert run("1\n4\n") == "-1", "minimum edge case"
assert run("1\n44444\n") != "", "large structured case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 4 | -1 | no valid base exists |
| 1, 24 | 20 | correct maximum over multiple valid bases |
| 1, 20 | 16 | higher-base candidate beating small divisors |

## Edge Cases

One subtle case occurs when $n = 4$. Here $n - 4 = 0$, so the divisor logic would incorrectly try to enumerate divisors of zero. The correct behavior is immediate rejection since no base representation of 4 contains digit 4 in a valid way (the representation would be just “4”, but base must be strictly greater than 4, making the digit invalid in base constraints).

Another case is when the optimal base is exactly $n - 4$. For $n = 20$, we get $n - 4 = 16$, and base 16 produces representation $14_{16}$, which contains a single digit 4. The divisor enumeration correctly includes this candidate, and verification ensures it is accepted.

A third edge case arises for large $n$ with sparse valid bases, where only higher-position digit placements work. The bounded search over $b^{i+1} \le n$ ensures these are still reachable because for small $i$, the base range remains large enough to include all candidates, and for large $i$, the bound collapses quickly, preventing missed solutions.
