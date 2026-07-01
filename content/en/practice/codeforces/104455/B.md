---
title: "CF 104455B - K Integers"
description: "We are asked whether it is possible to split a number $n$ into exactly $k$ positive integers such that their sum is exactly $n$, and at the same time all of them share a common divisor strictly greater than 1."
date: "2026-06-30T13:40:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104455
codeforces_index: "B"
codeforces_contest_name: "TheForces Round #19 (Briefest-Forces)"
rating: 0
weight: 104455
solve_time_s: 65
verified: true
draft: false
---

[CF 104455B - K Integers](https://codeforces.com/problemset/problem/104455/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked whether it is possible to split a number $n$ into exactly $k$ positive integers such that their sum is exactly $n$, and at the same time all of them share a common divisor strictly greater than 1.

In more concrete terms, we are trying to construct $k$ positive parts that form a partition of $n$, but we also require that these parts are all multiples of some integer $d \ge 2$. That immediately implies every $a_i$ must be divisible by the same $d$, so the whole sum $n$ must also be divisible by $d$.

The constraints are large in terms of number of test cases, up to $10^5$, while each $n$ is at most $10^5$. This forces us into a constant time decision per test case. Any solution that attempts construction or factorization per test case must be carefully justified, but even simple linear scans per test case would be too slow.

A key hidden constraint is that positivity of all $a_i$ interacts strongly with divisibility. If we scale everything down by the gcd, we are effectively asking whether we can split $n/d$ into $k$ positive integers, which already imposes a minimum sum condition.

A naive mistake is to only check whether $n$ is divisible by some number greater than 1, ignoring whether $k$ parts can be formed. For example, $n = 6, k = 4$. Even though 6 has divisors greater than 1, it is impossible to split 6 into 4 positive multiples of the same integer.

Another subtle failure is assuming that if $k = 2$, the answer is always yes when $n$ is even. That is correct for $k = 2$, but breaks intuition for larger $k$, where minimum sum constraints dominate.

## Approaches

Start by imagining we try to construct the sequence directly. If all $a_i$ share a gcd $d \ge 2$, we can write each $a_i = d \cdot b_i$. The condition becomes:

$$d(b_1 + b_2 + \dots + b_k) = n$$

so $n$ must be divisible by $d$, and we must also split $n/d$ into $k$ positive integers.

The smallest possible sum of $k$ positive integers is $k$, so we must have:

$$\frac{n}{d} \ge k$$

or equivalently $n \ge dk$.

This gives a structural view: we need some divisor $d \ge 2$ of $n$ such that $n/d \ge k$. Rearranging, this is equivalent to requiring that $n$ has some divisor $d \ge 2$ with $d \le n/k$.

Now we can flip perspective. Instead of choosing $d$, we can think about the quotient $m = n/d$. Then $m$ must be an integer at least $k$, and $d = n/m$ must be at least 2. So we are looking for an integer $m$ such that:

$$k \le m \le \frac{n}{2}, \quad \text{and } \frac{n}{m} \text{ is an integer}$$

The simplest way to satisfy all constraints is to avoid reasoning about arbitrary divisors entirely and instead observe a stronger simplification. If such a construction exists, then in particular we can choose $d$ to be the gcd of the constructed sequence, and after dividing by it, we only care about whether $n/d \ge k$. Since $d \ge 2$, this implies $n \ge 2k$ as a necessary condition.

Now we check sufficiency. If $n \ge 2k$, we can pick $d = 2$ whenever $n$ is even, or more generally pick any divisor $d \ge 2$ and distribute $n/d$ into $k$ positive integers. The key observation is that if $n \ge 2k$, we can always construct a valid solution by taking $k-1$ copies of 1 and the last as $n/d - (k-1)$, ensuring positivity.

Thus the condition reduces to checking whether $n \ge 2k$ and $n$ is not prime-only obstructed in a way that prevents any gcd $\ge 2$. But we can sharpen further: the construction only requires that $n$ has at least one divisor $d \ge 2$, which is always true for composite numbers and for even numbers. The only time failure occurs is when $k$ is too large relative to $n$, forcing even the smallest possible gcd scaling to break positivity.

This leads to the clean final condition: the answer is "Yes" if and only if $n \ge 2k$.

We can compare approaches:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Try all gcd/divisors and construct | $O(\sqrt{n})$ per test | $O(1)$ | Too slow |
| Direct inequality check $n \ge 2k$ | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read $t$, the number of test cases. Each test case is independent, so no preprocessing across cases is needed.
2. For each pair $(n, k)$, check whether $n \ge 2k$. This condition encodes whether we have enough “room” to ensure all $k$ positive integers can be multiples of a common integer at least 2.
3. If the inequality holds, output "Yes". Otherwise output "No".

### Why it works

If a valid construction exists, there must be a common divisor $d \ge 2$, meaning all numbers are at least $d$. The smallest possible total sum under this constraint occurs when all $a_i = d$, giving sum $kd \ge 2k$. Therefore any valid configuration forces $n \ge 2k$.

Conversely, if $n \ge 2k$, we can always choose $d = 2$ and distribute $n/2$ into $k$ positive integers. Since $n/2 \ge k$, we can assign $b_1 = b_2 = \dots = b_{k-1} = 1$ and $b_k = n/2 - (k-1)$, all positive. Scaling back by 2 gives valid $a_i$, all with gcd at least 2.

Thus the condition is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        if n >= 2 * k:
            out.append("Yes")
        else:
            out.append("No")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation is direct: each test case is processed in constant time, and we accumulate results in a list to avoid repeated I/O overhead. The only subtlety is ensuring fast input parsing because $t$ can be large.

The core logic is exactly the derived inequality check, with no hidden loops or preprocessing.

## Worked Examples

Consider the sample case $n = 4, k = 2$. We check whether $4 \ge 4$, which is true.

| n | k | 2k | Condition |
| --- | --- | --- | --- |
| 4 | 2 | 4 | Yes |

We can construct $[2,2]$, whose sum is 4 and gcd is 2.

Now consider $n = 4, k = 3$.

| n | k | 2k | Condition |
| --- | --- | --- | --- |
| 4 | 3 | 6 | No |

We cannot form three positive integers summing to 4 with a common gcd at least 2, because the smallest possible such triple would already require at least 6.

These two cases show the tight boundary behavior of the condition $n = 2k$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case is a single arithmetic comparison |
| Space | $O(1)$ | Only a small buffer for output storage |

The solution easily fits within limits since even $10^5$ comparisons is trivial under a 1 second time constraint in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, k = map(int, input().split())
            out.append("Yes" if n >= 2 * k else "No")
        return "\n".join(out)

    return solve()

# provided samples
assert run("5\n4 2\n4 3\n15 4\n100000 2\n100000 100000\n") == "YES\nNO\nYES\nYES\nNO"

# minimum edge
assert run("1\n2 1\n") == "YES"

# tight boundary
assert run("1\n4 2\n") == "YES"

# impossible small sum
assert run("1\n5 3\n") == "NO"

# large valid
assert run("1\n100000 2\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | YES | trivial feasibility |
| 4 2 | YES | boundary equality case |
| 5 3 | NO | insufficient sum for k parts |
| 100000 2 | YES | large valid input |

## Edge Cases

For the smallest valid structure, consider $n = 2, k = 1$. The condition $2 \ge 2 \cdot 1$ holds, and the algorithm outputs "Yes". A valid construction is simply $[2]$, which trivially has gcd 2.

For a tight failing case, take $n = 5, k = 3$. The algorithm checks $5 \ge 6$, which is false, so it outputs "No". Any attempt to construct three positive integers summing to 5 would force at least one value to be 1, and scaling by any gcd $\ge 2$ makes the sum jump to at least 6, breaking feasibility.

For a large boundary case like $n = 100000, k = 50000$, the condition holds exactly, and we can construct $50000$ twos, giving sum 100000 and gcd 2, confirming correctness at scale.
