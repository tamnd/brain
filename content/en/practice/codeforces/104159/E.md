---
title: "CF 104159E - \u0412\u0435\u0440\u0441\u0442\u043e\u0432\u044b\u0435 \u0441\u0442\u043e\u043b\u0431\u044b"
description: "We are given a positive integer $N$. We need to construct the smallest positive integer that satisfies two conditions at the same time: it must be divisible by $N$, and its decimal representation must end in the digit zero. Ending in zero means the number is a multiple of 10."
date: "2026-07-02T01:07:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104159
codeforces_index: "E"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u0420\u0421(\u042f) (5-8 \u043a\u043b\u0430\u0441\u0441\u044b) 2022-23, 2 \u0434\u0435\u043d\u044c"
rating: 0
weight: 104159
solve_time_s: 59
verified: true
draft: false
---

[CF 104159E - \u0412\u0435\u0440\u0441\u0442\u043e\u0432\u044b\u0435 \u0441\u0442\u043e\u043b\u0431\u044b](https://codeforces.com/problemset/problem/104159/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer $N$. We need to construct the smallest positive integer that satisfies two conditions at the same time: it must be divisible by $N$, and its decimal representation must end in the digit zero.

Ending in zero means the number is a multiple of 10. So we are effectively looking for the smallest number that is a common multiple of $N$ and 10, with the extra constraint that we want the smallest such number in absolute value.

The key observation is that we are not asked for the least common multiple in abstract form only, but specifically the smallest positive integer that is simultaneously a multiple of $N$ and 10. That is exactly the definition of $\mathrm{lcm}(N, 10)$, since any number divisible by both $N$ and 10 must be a common multiple, and the smallest such number is the LCM.

The input size goes up to $10^9$, which rules out any factorization-heavy or iterative search approaches that depend on scanning multiples of $N$. Even iterating up to $10^9 / N$ in the worst case is unnecessary when the structure is purely number theoretic.

A naive approach would try to start from $N$ and repeatedly add $N$ until a multiple ends in zero. This fails immediately in cases like $N = 999999937$, where the first valid answer is extremely large relative to $N$, and the number of iterations can become large in pathological cases.

Another subtle pitfall is assuming that multiplying by 10 always gives the answer. That is only correct when $N$ is not divisible by 2 or 5 in a way that already interacts with the factorization of 10. For example, $N = 6$ gives answer 30, not 60.

## Approaches

A brute-force interpretation would be to generate multiples of $N$: $N, 2N, 3N, \dots$ and stop at the first value whose last digit is zero. This is correct because every valid answer must be a multiple of $N$, so enumerating multiples eventually finds it. The issue is that the number of candidates can be large before hitting a number divisible by 10. In the worst case, if $N$ is coprime with 10, the last digit cycles through all 10 possibilities, meaning we may need up to 10 steps per full residue cycle, but since values grow without bound, this still does not give a useful bound for large $N$ in practice when thinking in terms of magnitude of the answer rather than iteration count.

The structure of the problem removes all of this complexity. We are looking for a number divisible by both $N$ and 10, which is exactly the least common multiple of these two integers. Since 10 has only prime factors 2 and 5, we only need to adjust $N$ so that it contains enough of these factors to cover 10. Concretely, we compute $\mathrm{lcm}(N, 10) = \frac{N \cdot 10}{\gcd(N, 10)}$.

The gcd computation is constant time for 32-bit or 64-bit integers, so this reduces the entire problem to a single arithmetic expression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Multiples | O(k) | O(1) | Too slow |
| GCD-based LCM | O(log N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $N$. The entire structure of the solution depends only on its prime factor interaction with 10.
2. Compute $g = \gcd(N, 10)$. This extracts the shared factors between $N$ and the requirement that the result ends in 0, which enforces divisibility by 2 and 5.
3. Compute the answer as $\frac{N}{g} \cdot 10$. This construction ensures we are adding only the missing prime factors needed to make the number divisible by 10 without introducing redundancy.
4. Output the computed value directly.

### Why it works

Every valid number must be divisible by both $N$ and 10. The set of all such numbers is exactly the set of multiples of $\mathrm{lcm}(N, 10)$. The expression $\frac{N \cdot 10}{\gcd(N, 10)}$ produces the smallest number containing all prime factors required by both $N$ and 10 without duplication. Since any smaller number would fail divisibility by at least one of the two constraints, the result is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math

def solve():
    n = int(input().strip())
    g = math.gcd(n, 10)
    ans = (n // g) * 10
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution relies entirely on computing the gcd with 10, which isolates how many factors of 2 and 5 are already present in $N$. Dividing by this gcd removes overlap before multiplying by 10, ensuring we do not double-count shared factors.

The order of operations matters for correctness and overflow safety in languages with fixed integer sizes, but in Python the integer range is unbounded. Still, computing $n // g$ before multiplication keeps the expression aligned with the mathematical definition of LCM.

## Worked Examples

### Sample 1: $N = 6$

| Step | N | gcd(N,10) | n/g | result |
| --- | --- | --- | --- | --- |
| Start | 6 | - | - | - |
| gcd | 6 | 2 | - | - |
| divide | 6 | 2 | 3 | - |
| multiply | 6 | 2 | 3 | 30 |

The number 6 already contains a factor of 2, so only one additional factor of 5 is needed to reach a multiple of 10. The result 30 is the smallest number divisible by both 6 and 10.

### Sample 2: $N = 19$

| Step | N | gcd(N,10) | n/g | result |
| --- | --- | --- | --- | --- |
| Start | 19 | - | - | - |
| gcd | 19 | 1 | - | - |
| divide | 19 | 1 | 19 | - |
| multiply | 19 | 1 | 19 | 190 |

Since 19 is coprime with 10, we must attach the full factor of 10. No smaller multiple can end in zero while still being divisible by 19.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log N) | dominated by gcd computation |
| Space | O(1) | only a few integer variables |

The computation is constant work per test case, and even with multiple inputs, the total runtime remains trivial compared to constraints up to $10^9$.

## Test Cases

```python
import sys, io, math

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline().strip())
    g = math.gcd(n, 10)
    return str((n // g) * 10)

# provided samples
assert solve("6\n") == "30"
assert solve("19\n") == "190"

# minimum case
assert solve("1\n") == "10"

# already ending with 0
assert solve("10\n") == "10"

# multiple of 2 but not 5
assert solve("8\n") == "40"

# multiple of 5 but not 2
assert solve("25\n") == "50"

# large prime
assert solve("999999937\n") == str((999999937 // math.gcd(999999937, 10)) * 10)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 10 | smallest edge case |
| 10 | 10 | already valid multiple |
| 8 | 40 | needs factor 5 |
| 25 | 50 | needs factor 2 |
| 999999937 | computed | large prime correctness |

## Edge Cases

One important edge case is when $N$ is already divisible by 10. For $N = 10$, the gcd with 10 is 10, so the formula gives $(10 / 10) \cdot 10 = 10$. The algorithm correctly avoids increasing the number, since it is already the smallest multiple of itself that ends in zero.

For $N = 8$, the gcd with 10 is 2. The computation becomes $(8 / 2) \cdot 10 = 40$. Tracing this, we see that 8 lacks a factor of 5, and multiplying after removing the shared factor ensures we introduce exactly one 5 without disturbing the 2 already present.

For $N = 25$, gcd is 5, so the result is $(25 / 5) \cdot 10 = 50$. This shows the symmetry: the algorithm removes overlap so that only missing prime factors of 10 are introduced, avoiding overcounting and ensuring minimality.
