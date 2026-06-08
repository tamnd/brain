---
title: "CF 2033F - Kosuke's Sloth"
description: "For a fixed integer $k$, look at the Fibonacci sequence and mark every position whose Fibonacci value is divisible by $k$. For example, when $k=2$: $$1,1,mathbf{2},3,5,mathbf{8},13,21,mathbf{34},dots$$ The marked positions are $3,6,9,dots$."
date: "2026-06-08T11:44:10+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2033
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 981 (Div. 3)"
rating: 1800
weight: 2033
solve_time_s: 121
verified: true
draft: false
---

[CF 2033F - Kosuke's Sloth](https://codeforces.com/problemset/problem/2033/F)

**Rating:** 1800  
**Tags:** brute force, math, number theory  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

For a fixed integer $k$, look at the Fibonacci sequence and mark every position whose Fibonacci value is divisible by $k$.

For example, when $k=2$:

$$1,1,\mathbf{2},3,5,\mathbf{8},13,21,\mathbf{34},\dots$$

The marked positions are $3,6,9,\dots$.

Define $G(n,k)$ as the position of the $n$-th marked Fibonacci number. We are given $n$ and $k$, and must compute $G(n,k)$ modulo $10^9+7$.

The main difficulty is that $n$ can be as large as $10^{18}$. We cannot generate Fibonacci numbers or count divisible terms one by one. Even an $O(n)$ algorithm is completely impossible.

The other important constraint is $k \le 10^5$, and the sum of all $k$ values across test cases is at most $10^6$. This strongly suggests that we should spend roughly $O(k)$ work per test case and exploit some structure that depends only on $k$.

A subtle edge case appears when $k=1$. Every Fibonacci number is divisible by $1$, so the marked positions are simply $1,2,3,\dots$. Thus $G(n,1)=n$. Any solution that assumes divisibility events are sparse may fail here.

For example:

```
Input:
1
5 1
```

The correct answer is:

```
5
```

Another easy mistake is to search for the $n$-th divisible Fibonacci number directly. Consider:

```
Input:
1
1000000000000000000 2
```

The answer exists at an index around $3 \times 10^{18}$. Simulating positions one by one is hopeless.

A third pitfall is forgetting that the final answer is required modulo $10^9+7$. The actual index $G(n,k)$ may be far larger than 64-bit limits when $n$ is huge. The modulo must be applied using modular arithmetic instead of constructing the full value.

## Approaches

The most direct idea is to generate Fibonacci numbers modulo $k$, check whether each term is divisible by $k$, and count how many such positions have appeared. As soon as the count reaches $n$, we output the current index.

This is correct because divisibility by $k$ depends only on the Fibonacci value modulo $k$. The problem is that $n$ can be $10^{18}$, so we might need to process around $10^{18}$ positions. That is many orders of magnitude beyond what is possible.

The key observation is that Fibonacci numbers modulo $k$ are periodic. The sequence

$$(F_i \bmod k)$$

is called the Pisano sequence. Since each state is determined by the pair

$$(F_i \bmod k,\; F_{i+1} \bmod k),$$

there are only $k^2$ possible states. Eventually a state repeats, and once a state repeats, the entire sequence repeats.

In fact, the Fibonacci sequence modulo $k$ always returns to the starting pair $(0,1)$. The length of this cycle is the Pisano period.

Inside one period, the positions where $F_i \equiv 0 \pmod k$ form a repeating pattern. Let the first such position be $z$. A classical property of Fibonacci sequences says that every index divisible by $z$ also gives a multiple of $k$, and no smaller positive index does. Consequently, all divisible positions are

$$z,\;2z,\;3z,\dots$$

The $n$-th divisible Fibonacci number is therefore located at position

$$n \cdot z.$$

The entire problem reduces to finding the smallest positive index $z$ such that

$$F_z \equiv 0 \pmod k.$$

Since the Pisano period for $k \le 10^5$ is at most $6k$, we can find this index by simulating Fibonacci numbers modulo $k$ until the first zero appears.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(G(n,k))$ | $O(1)$ | Too slow |
| Optimal | $O(k)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Let `MOD = 1_000_000_007`.
2. For a test case $(n,k)$, generate Fibonacci numbers modulo $k$.
3. Start with the pair $(1,1)$, corresponding to $F_1$ and $F_2$.
4. Repeatedly compute the next Fibonacci residue modulo $k$, while tracking its index.
5. The first index $z$ where the residue becomes zero is the smallest positive index satisfying $F_z \equiv 0 \pmod k$.

This index is often called the rank of apparition of $k$.
6. Every Fibonacci number divisible by $k$ occurs at an index that is a multiple of $z$.
7. The $n$-th divisible Fibonacci number is therefore at index $n \cdot z$.
8. Output

$$(n \bmod MOD)\cdot(z \bmod MOD)\bmod MOD.$$

### Why it works

Let $z$ be the smallest positive index with $F_z \equiv 0 \pmod k$.

A standard Fibonacci divisibility property states that

$$\gcd(F_a,F_b)=F_{\gcd(a,b)}.$$

Using this fact, one can show that if $F_m$ is divisible by $k$, then $z$ divides $m$. Otherwise $F_{\gcd(z,m)}$ would also be divisible by $k$, contradicting the minimality of $z$.

Conversely, Fibonacci numbers satisfy

$$F_z \mid F_{tz}$$

for every positive integer $t$. Since $F_z$ is already divisible by $k$, every $F_{tz}$ is divisible by $k$ as well.

Thus the divisible positions are exactly

$$z,2z,3z,\dots$$

and the $n$-th such position is $nz$. The algorithm finds $z$ and computes this value modulo $10^9+7$.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def first_zero_index(k):
    if k == 1:
        return 1

    a, b = 1 % k, 1 % k
    idx = 2

    while True:
        a, b = b, (a + b) % k
        idx += 1

        if b == 0:
            return idx

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, k = map(int, input().split())

        z = first_zero_index(k)
        ans.append(str((n % MOD) * (z % MOD) % MOD))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The function `first_zero_index` searches for the first Fibonacci index whose value is divisible by `k`. The variables `a` and `b` always represent two consecutive Fibonacci residues modulo `k`.

The index starts at `2` because `a` and `b` initially correspond to `F1` and `F2`. After each transition, `b` becomes the next Fibonacci value, so when `b == 0`, the current value of `idx` is exactly the desired index.

The special case `k == 1` is handled separately because every Fibonacci number is divisible by `1`, making the answer index equal to `1`.

The final multiplication uses modular arithmetic immediately. Since `n` may be as large as `10^18`, computing modulo first keeps all values small and avoids unnecessary large integers.

## Worked Examples

### Example 1

Input:

```
3 2
```

We search for the first Fibonacci number divisible by `2`.

| Index | Fibonacci mod 2 |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 0 |

We find:

| Variable | Value |
| --- | --- |
| n | 3 |
| z | 3 |
| Answer | 3 × 3 = 9 |

Output:

```
9
```

This demonstrates the fundamental pattern. Once index `3` is found, all divisible positions are multiples of `3`.

### Example 2

Input:

```
100 1
```

Since every Fibonacci number is divisible by `1`:

| Variable | Value |
| --- | --- |
| z | 1 |
| n | 100 |
| Answer | 100 |

Output:

```
100
```

This exercises the special case where the first divisible position occurs immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k)$ per test case | The first zero appears within the Pisano cycle, whose length is at most $6k$ |
| Space | $O(1)$ | Only a few integers are stored |

The sum of all $k$ values is at most $10^6$, so the total amount of Fibonacci simulation across all test cases is linear in the input size. This comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 1000000007

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def first_zero_index(k):
        if k == 1:
            return 1

        a, b = 1 % k, 1 % k
        idx = 2

        while True:
            a, b = b, (a + b) % k
            idx += 1
            if b == 0:
                return idx

    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())
        z = first_zero_index(k)
        out.append(str((n % MOD) * (z % MOD) % MOD))

    return "\n".join(out)

# provided samples
assert run(
"""3
3 2
100 1
1000000000000 1377
"""
) == """9
100
999244007"""

# minimum values
assert run(
"""1
1 1
"""
) == "1"

# first divisible position for k=2 is 3
assert run(
"""1
1 2
"""
) == "3"

# second divisible position for k=2 is 6
assert run(
"""1
2 2
"""
) == "6"

# large n with easy k
assert run(
"""1
1000000000000000000 1
"""
) == str(1000000000000000000 % MOD)
```

### Custom Test Summary

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Smallest possible input |
| `1 2` | `3` | First divisible Fibonacci position |
| `2 2` | `6` | Multiples of the first zero index |
| `10^18 1` | `10^18 mod MOD` | Huge `n`, special case `k=1` |

## Edge Cases

Consider:

```
1
5 1
```

Every Fibonacci number is divisible by `1`. The algorithm immediately returns `z = 1`. The answer becomes `5 × 1 = 5`. No sequence generation is required.

Consider:

```
1
1 2
```

The Fibonacci sequence modulo `2` is:

```
1, 1, 0, 1, 1, 0, ...
```

The first zero occurs at index `3`, so `z = 3`. The answer is `1 × 3 = 3`. This verifies that the first divisible Fibonacci number is not necessarily at index `1`.

Consider:

```
1
1000000000000000000 2
```

The same `z = 3` is found. The algorithm computes

$$(10^{18} \bmod 10^9+7)\cdot 3 \bmod 10^9+7$$

without ever constructing the enormous index $3 \times 10^{18}$. This is exactly why modular arithmetic is applied at the end.
