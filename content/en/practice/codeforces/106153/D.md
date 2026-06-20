---
title: "CF 106153D - \u742a\u9732\u8bfa\u7684\u65e0\u9650\u5faa\u73af\u5c0f\u6570"
description: "The task revolves around deciding whether a given fraction produces a terminating decimal or an infinite repeating decimal when written in base 10. Each test case gives an integer denominator, and we implicitly consider the fraction $frac{1}{n}$."
date: "2026-06-20T22:10:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106153
codeforces_index: "D"
codeforces_contest_name: "HNNU Freshman Competition Round 2"
rating: 0
weight: 106153
solve_time_s: 47
verified: true
draft: false
---

[CF 106153D - \u742a\u9732\u8bfa\u7684\u65e0\u9650\u5faa\u73af\u5c0f\u6570](https://codeforces.com/problemset/problem/106153/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

The task revolves around deciding whether a given fraction produces a terminating decimal or an infinite repeating decimal when written in base 10. Each test case gives an integer denominator, and we implicitly consider the fraction $\frac{1}{n}$. The goal is to determine whether its decimal expansion eventually stops or continues forever with a repeating cycle.

A decimal representation terminates exactly when the denominator, after being fully reduced with the numerator, contains no prime factors other than 2 and 5. This comes from the structure of base 10, since $10 = 2 \cdot 5$. Any factor of 2 or 5 can be absorbed into powers of 10, shifting digits in the decimal expansion until the fraction becomes an integer.

The input size allows many test cases and large values of $n$, which immediately rules out any simulation of decimal expansion or modular long division. Even repeated division by 10 or constructing digits would be far too slow if done directly for large numbers, especially when $n$ can be large enough that its factorization structure matters more than its magnitude.

A subtle edge case appears when $n = 1$. In this case the fraction is already an integer, so it clearly terminates. Another corner case is when $n$ is a power of 2 or 5, since these always terminate regardless of size. On the other side, even a single additional prime factor like 3 breaks termination completely, for example $n = 6$ produces $0.1666...$, which is infinite repeating even though it is small and simple.

A naive approach might try checking divisibility of large powers of 10 or testing up to some bound whether $10^k \equiv 0 \pmod{n}$. This fails because the required exponent can be extremely large, and without removing irrelevant factors first, the process becomes infeasible.

## Approaches

A brute-force idea is to directly simulate the decimal expansion of $\frac{1}{n}$ using long division. At each step, we multiply the remainder by 10 and take digits, checking whether the remainder becomes zero. If it ever becomes zero, the decimal terminates.

This approach is correct because long division exactly constructs the decimal representation. However, the worst case occurs when the fraction is repeating, in which case the remainder cycles through values modulo $n$. Since there are at most $n$ possible remainders, this simulation can take $O(n)$ steps per test case. With large inputs and multiple queries, this is too slow.

The key observation is that we do not need to simulate the process at all. The only reason a decimal terminates is that after canceling all factors of 2 and 5 from the denominator, nothing remains. This is because powers of 10 only introduce factors of 2 and 5, so any other prime factor can never be eliminated through multiplication by 10.

So instead of simulating division, we repeatedly remove all factors of 2 and 5 from $n$. If what remains is 1, the decimal terminates; otherwise it is infinite.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Long division simulation | $O(n)$ per test | $O(1)$ | Too slow |
| Factor stripping (2, 5) | $O(\log n)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We repeatedly divide the number by 2 and 5 while it is divisible by them. Once no more such factors exist, we check whether the result is 1.

1. Read the integer $n$ for the current test case. This represents the denominator of the fraction we are analyzing.
2. While $n$ is divisible by 2, divide it by 2. Each division removes one power of 2 from the factorization. This step is safe because powers of 2 are exactly those that can be absorbed into base 10.
3. While $n$ is divisible by 5, divide it by 5. This removes all factors compatible with base 10 scaling for the same reason as above.
4. After stripping these factors completely, check whether $n$ is equal to 1. If it is not, then some other prime factor remains, meaning it cannot be eliminated by multiplying powers of 10.
5. Output "NO" if $n = 1$, otherwise output "YES".

### Why it works

Any terminating decimal means there exists some power $10^k$ such that $\frac{1}{n} \cdot 10^k$ becomes an integer. Since $10^k = 2^k \cdot 5^k$, this implies all prime factors of $n$ must be contained in 2 and 5. Removing all factors of 2 and 5 from $n$ leaves 1 exactly when this condition holds, so the check is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    while n % 2 == 0:
        n //= 2
    while n % 5 == 0:
        n //= 5
    if n == 1:
        print("NO")
    else:
        print("YES")

def main():
    t = int(input())
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
```

The core of the implementation is the repeated factor stripping loop. The order of removing 2s and 5s does not matter because multiplication is commutative, and both loops reduce the number independently until no longer divisible.

The final check distinguishes between clean denominators composed only of 2s and 5s versus those that still contain other primes.

One subtle point is that the output convention in this problem is inverted from the usual statement: after normalization, a remaining value greater than 1 corresponds to an infinite decimal, which is labeled "YES" here.

## Worked Examples

Consider $n = 20$.

| Step | n | Action |
| --- | --- | --- |
| start | 20 | initial value |
| divide by 2 | 10 | remove one factor of 2 |
| divide by 2 | 5 | remove second factor of 2 |
| divide by 5 | 1 | remove factor of 5 |
| check | 1 | terminate |

Since the final value is 1, the output is "NO", meaning it does not have an infinite repeating component.

Now consider $n = 6$.

| Step | n | Action |
| --- | --- | --- |
| start | 6 | initial value |
| divide by 2 | 3 | remove factor 2 |
| stop 2-loop | 3 | not divisible by 2 |
| stop 5-loop | 3 | not divisible by 5 |
| check | 3 | final value |

Since the result is 3, the output is "YES", indicating an infinite repeating decimal.

These traces show that only primes outside {2, 5} survive the normalization process and fully determine the behavior.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \log n)$ | each test divides out powers of 2 and 5 |
| Space | $O(1)$ | only integer arithmetic is used |

The constraints allow this easily since each division quickly reduces the number, and even large values shrink rapidly due to repeated factor removal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        while n % 2 == 0:
            n //= 2
        while n % 5 == 0:
            n //= 5
        out.append("NO" if n == 1 else "YES")
    return "\n".join(out) + "\n"

# provided samples (illustrative)
assert run("2\n20\n6\n") == "NO\nYES\n"

# all ones
assert run("3\n1\n2\n5\n") == "NO\nNO\nNO\n"

# pure powers of 2 and 5
assert run("2\n32\n125\n") == "NO\nNO\n"

# mixed with other primes
assert run("3\n3\n7\n14\n") == "YES\nYES\nYES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 20, 6 | NO, YES | basic mixed behavior |
| 1, 2, 5 | NO, NO, NO | smallest terminating cases |
| 32, 125 | NO, NO | large pure powers of 2/5 |
| 3, 7, 14 | YES, YES, YES | non 2/5 primes always repeat |

## Edge Cases

For $n = 1$, the loops do nothing since it is not divisible by 2 or 5. The final value remains 1, so the algorithm correctly outputs "NO".

For $n = 8$, repeated division by 2 reduces it through 4, 2, and finally 1. The final state is clean, confirming termination.

For $n = 45$, we remove 5 twice to get 9, and 9 cannot be reduced further. Since 9 contains a factor 3, the algorithm correctly identifies it as infinite.

For each case, the key invariant holds: after stripping all factors of 2 and 5, the remaining number represents exactly the obstruction to writing the denominator as a power of 10 divisor.
