---
title: "CF 104820A - \u0414\u043e\u0433\u043e\u043d\u044f\u043b\u043a\u0438"
description: "Two players start on a number line: Alice is at position $a$, Bob is at position $b$, with $a < b$. Each second Alice moves to the right by a fixed integer speed $c$, and Bob moves to the right by a fixed integer speed $d$."
date: "2026-06-28T12:54:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104820
codeforces_index: "A"
codeforces_contest_name: "\u0420\u0421\u041e-\u0410\u043b\u0430\u043d\u0438\u044f 2018-2023. \u0418\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0435"
rating: 0
weight: 104820
solve_time_s: 68
verified: true
draft: false
---

[CF 104820A - \u0414\u043e\u0433\u043e\u043d\u044f\u043b\u043a\u0438](https://codeforces.com/problemset/problem/104820/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

Two players start on a number line: Alice is at position $a$, Bob is at position $b$, with $a < b$. Each second Alice moves to the right by a fixed integer speed $c$, and Bob moves to the right by a fixed integer speed $d$. Bob’s speed $d$ is known, but Alice has forgotten her own speed $c$. What she remembers is that her speed was chosen so that at some integer time $t \ge 0$, both players occupy exactly the same position.

The task is not to reconstruct a single valid speed, but to count how many integer values of $c$ make such a meeting possible.

The condition for a meeting is that there exists an integer $t \ge 0$ such that

$$a + ct = b + dt.$$

Rearranging gives

$$(c - d)t = b - a.$$

So the difference $b-a$ must be divisible by $c-d$, and the sign of $c-d$ determines whether Alice can ever catch up or whether she is already faster.

The constraints allow $a, b, d$ up to $10^{12}$, so any approach that iterates over all possible $c$ is immediately impossible. Even iterating up to $b-a$ would be infeasible when the gap is large.

A subtle edge case is when Alice is already slower than Bob. If $c \le d$, then $c-d \le 0$, and Alice can only meet Bob if they start at the same point, which is explicitly forbidden since $a < b$. So valid solutions must satisfy $c > d$, reducing the search space to positive offsets above $d$.

Another important detail is that the meeting time $t$ must be an integer. This converts the problem into a divisibility condition on $b-a$, and invalidates any reasoning that only considers real-valued time.

## Approaches

A direct way to think about the problem is to try all possible integer speeds $c$ and check whether there exists an integer $t$ satisfying the equation

$$a + ct = b + dt.$$

For a fixed $c$, we compute the difference $b-a$ and check whether it can be expressed as $t(c-d)$ for some integer $t \ge 0$. This is equivalent to checking whether $c-d$ divides $b-a$. However, iterating over all $c$ up to $10^{12}$ is too slow, since each check is constant time but the range is enormous.

The key observation is that the problem depends only on the difference between speeds, not on their absolute values. Let $k = c - d$. Then $k$ must be a positive integer such that $k \mid (b-a)$. Once $k$ is fixed, we recover $c = d + k$. This transforms the problem into counting positive divisors of $b-a$.

So instead of searching over speeds, we count divisors of a single number, which is at most $10^{12}$. Counting divisors can be done in $O(\sqrt{n})$ by checking pairs of factors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over $c$ | $O(b-a)$ | $O(1)$ | Too slow |
| Divisor enumeration | $O(\sqrt{b-a})$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

Let $n = b - a$.

1. Compute the distance $n = b - a$. This isolates the only quantity that determines whether a meeting is possible.
2. Initialize an answer counter to zero. This will count valid speed differences $k$.
3. Iterate over all integers $i$ from $1$ to $\lfloor \sqrt{n} \rfloor$. Each $i$ is treated as a potential divisor candidate of $n$.
4. If $i$ divides $n$, then $i$ contributes a valid value for $k$, and also $n/i$ contributes another value unless they are equal. The reason is that every divisor corresponds to a valid speed difference $k = c-d$, and each such $k$ defines exactly one valid $c$.
5. Count all such divisors carefully, ensuring that when $i^2 = n$, the divisor is only counted once.
6. Output the total count.

### Why it works

The equation $a + ct = b + dt$ reduces to $(c-d)t = n$, so $c-d$ must be a positive divisor of $n$. Conversely, every positive divisor $k$ of $n$ yields a valid solution by choosing $t = n/k$ and $c = d + k$, which is always a positive integer. This establishes a one-to-one correspondence between valid speeds $c$ and positive divisors of $b-a$, so counting valid $c$ is exactly counting divisors of $b-a$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, d = map(int, input().split())
    n = b - a

    ans = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            ans += 1
            if i * i != n:
                ans += 1
        i += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first compresses the problem into computing $n = b-a$. It then counts divisors of $n$ using the standard square-root method. Each divisor corresponds to a valid choice of $c$, because $c = d + k$ and $k$ is any divisor of $n$. The loop carefully handles the perfect-square case to avoid double counting.

A subtle implementation point is that $d$ never appears in the divisor counting logic. It only shifts the final value of $c$, but does not affect how many valid $k$ exist.

## Worked Examples

### Sample 1

Input:

```
1 2 3
```

Here $n = 1$.

| i | n % i == 0 | divisor(s) added | ans |
| --- | --- | --- | --- |
| 1 | yes | 1 | 1 |

The only divisor of 1 is 1, meaning $k=1$, so $c = d + 1 = 4$ is the only valid speed.

This confirms that even when the distance is minimal, the method correctly counts exactly one valid configuration.

### Sample 2

Input:

```
1 11 12
```

Here $n = 10$.

| i | divisors found | ans |
| --- | --- | --- |
| 1 | 1, 10 | 2 |
| 2 | 2, 5 | 4 |
| 3 | none | 4 |

Final answer is 4.

This shows that multiple divisor pairs contribute independently, and each divisor corresponds to a distinct valid speed difference $k$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{b-a})$ | We test divisors only up to the square root of the distance |
| Space | $O(1)$ | Only a few integer variables are used |

The distance $b-a$ can be as large as $10^{12}$, so $\sqrt{b-a} \le 10^6$. This fits comfortably within typical time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b, d = map(int, input().split())
    n = b - a

    ans = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            ans += 1
            if i * i != n:
                ans += 1
        i += 1

    return str(ans)

# provided samples
assert run("1 2 3\n") == "1"
assert run("1 11 12\n") == "4"
assert run("11 54 65\n") == "2"

# custom cases
assert run("1 2 1\n") == "1", "small gap"
assert run("1 1000000000000 1\n") == str(len([i for i in range(1, int((999999999999)**0.5)+1) if (999999999999)%i==0])*2 - (1 if int((999999999999)**0.5)**2 == 999999999999 else 0)), "large composite"
assert run("5 6 100\n") == "1", "minimal distance"
assert run("10 11 2\n") == "1", "single divisor"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 1 | 1 | smallest non-zero gap |
| 1 10^12 1 | computed | large value stress test |
| 5 6 100 | 1 | minimal distance edge case |
| 10 11 2 | 1 | correctness when d is irrelevant |

## Edge Cases

When $b-a = 1$, the algorithm only checks $i = 1$, finds exactly one divisor, and returns 1. This corresponds to the only possible speed difference $k = 1$, which yields a valid meeting time $t = 1$.

When $b-a$ is a perfect square, such as $n = 36$, the loop reaches $i = 6$. The divisor $6$ should only be counted once, and the condition `if i * i != n` ensures correctness by avoiding double counting.

When $n$ is prime, only $1$ and $n$ are counted. The loop correctly identifies exactly two divisors, reflecting exactly two valid speed differences and therefore two valid values of $c$.
