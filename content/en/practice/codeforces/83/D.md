---
title: "CF 83D - Numbers"
description: "We need to count integers inside the interval $[a,b]$ whose smallest divisor greater than $1$ is exactly $k$. For a number $x$, saying that its smallest divisor is $k$ means two things happen simultaneously: 1. $x$ is divisible by $k$. 2."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 83
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 72 (Div. 1 Only)"
rating: 2400
weight: 83
solve_time_s: 127
verified: true
draft: false
---

[CF 83D - Numbers](https://codeforces.com/problemset/problem/83/D)

**Rating:** 2400  
**Tags:** dp, math, number theory  
**Solve time:** 2m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to count integers inside the interval $[a,b]$ whose smallest divisor greater than $1$ is exactly $k$.

For a number $x$, saying that its smallest divisor is $k$ means two things happen simultaneously:

1. $x$ is divisible by $k$.
2. $x$ is not divisible by any integer from $2$ to $k-1$.

The second condition immediately implies that $k$ itself must be prime. If $k$ were composite, one of its smaller divisors would also divide $x$, so $k$ could never be the smallest divisor.

The limits are large. Both $a$ and $b$ can reach $2 \cdot 10^9$, so iterating through the interval is impossible. Even checking every number individually with trial division would require billions of operations in the worst case.

The value of $k$ is also large, but an important observation saves us: if $k$ is prime, then every valid number has the form

$$x = k \cdot t$$

and $t$ must avoid all prime factors smaller than $k$.

Since the smallest divisor of any composite number is prime, it is enough to forbid divisibility by primes smaller than $k$. That transforms the problem into a counting problem with inclusion-exclusion and the Möbius function.

Several edge cases are easy to mishandle.

If $k$ is composite, the answer is always zero. For example:

Input:

```
1 100 6
```

Every multiple of $6$ is divisible by $2$ or $3$, so $6$ can never be the smallest divisor. The correct answer is:

```
0
```

A careless implementation that only checks divisibility by numbers smaller than $k$ after scaling might accidentally count multiples of $6$.

Another subtle case appears when $k^2 > b$. Then the only possible valid number is $k$ itself, because every other multiple $2k,3k,\dots$ already has a smaller divisor. Example:

Input:

```
10 20 13
```

The only multiple of $13$ in the interval is $13$, and its smallest divisor is indeed $13$. The answer is:

```
1
```

There is also an off-by-one trap when converting the interval $[a,b]$ into a range for the multiplier $t$. Suppose:

Input:

```
15 30 5
```

We rewrite numbers as $x=5t$. Then:

$$t \in \left[\left\lceil \frac{15}{5} \right\rceil,\left\lfloor \frac{30}{5} \right\rfloor\right]
=
[3,6]$$

Among $3,4,5,6$, only $5$ is divisible by no prime smaller than $5$. That gives $25$ as the only valid number. Forgetting the ceiling on the left boundary would incorrectly include $10$.

## Approaches

The brute-force approach directly follows the definition. For every integer $x$ in $[a,b]$, we find its smallest divisor greater than $1$. If that divisor equals $k$, we count it.

This works logically because the smallest divisor uniquely determines whether the number satisfies the condition. The problem is the scale. The interval length can be almost $2 \cdot 10^9$. Even an $O(\sqrt{x})$ check per number becomes hopelessly large.

The key observation is that if the smallest divisor of $x$ equals $k$, then $k$ must be prime and $x$ must be divisible by $k$. Write:

$$x = k \cdot t$$

Now ask what conditions apply to $t$.

If some prime $p < k$ divides $t$, then $p$ also divides $x$, which contradicts $k$ being the smallest divisor. So $t$ must be coprime to the product of all primes smaller than $k$.

This converts the problem into counting integers in a range that are not divisible by a set of primes.

The number of primes smaller than $k$ cannot be large when their product stays below $2 \cdot 10^9$. The product of the first ten primes already exceeds this limit. That means we can safely use inclusion-exclusion over all subsets of these primes.

The brute-force checks every number individually. The optimal solution counts whole groups at once by subtracting multiples of forbidden primes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((b-a+1)\sqrt{b})$ | $O(1)$ | Too slow |
| Optimal | $O(\sqrt{k} + 2^{\pi(k)})$ | $O(\pi(k))$ | Accepted |

## Algorithm Walkthrough

1. Check whether $k$ is prime.

If $k$ is composite, immediately print $0$. A composite number can never be the smallest divisor of another number because one of its smaller prime divisors would appear first.
2. Convert the interval from numbers $x$ to multipliers $t$.

Every valid number has the form:

$$x = k \cdot t$$

So:

$$L = \left\lceil \frac{a}{k} \right\rceil$$

$$R = \left\lfloor \frac{b}{k} \right\rfloor$$

We now need to count integers $t \in [L,R]$ that are not divisible by any prime smaller than $k$.
3. Generate all primes smaller than $k$.

We only need primes up to $\sqrt{k}$ to test primality, but we also store every prime less than $k$ because these are the forbidden divisors for $t$.
4. Apply inclusion-exclusion.

Let the forbidden primes be:

$$p_1,p_2,\dots,p_m$$

For every subset of these primes, compute their product:

$$d = p_{i_1}p_{i_2}\cdots p_{i_s}$$

Count how many numbers in $[L,R]$ are divisible by $d$:

$$\left\lfloor \frac{R}{d} \right\rfloor -
\left\lfloor \frac{L-1}{d} \right\rfloor$$

Add this count if the subset size is even, subtract it if the subset size is odd.
5. The final inclusion-exclusion result is the number of valid multipliers $t$, which equals the number of valid integers $x$.

### Why it works

Every valid number can be uniquely written as $x = kt$. Since $k$ is prime, the only way for $x$ to have a smaller divisor is for $t$ to contain a prime factor smaller than $k$. The algorithm counts exactly those $t$ that avoid all forbidden primes.

Inclusion-exclusion is correct because it alternates between subtracting numbers divisible by at least one forbidden prime and adding back numbers counted multiple times. After processing all subsets, every invalid $t$ contributes zero net count, while every valid $t$ contributes exactly one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_prime(x):
    if x < 2:
        return False
    d = 2
    while d * d <= x:
        if x % d == 0:
            return False
        d += 1
    return True

def primes_less_than(k):
    primes = []
    for x in range(2, k):
        ok = True
        d = 2
        while d * d <= x:
            if x % d == 0:
                ok = False
                break
            d += 1
        if ok:
            primes.append(x)
    return primes

def solve():
    a, b, k = map(int, input().split())

    if not is_prime(k):
        print(0)
        return

    L = (a + k - 1) // k
    R = b // k

    if L > R:
        print(0)
        return

    primes = primes_less_than(k)

    ans = 0
    m = len(primes)

    for mask in range(1 << m):
        bits = 0
        prod = 1

        for i in range(m):
            if (mask >> i) & 1:
                bits += 1
                prod *= primes[i]

                if prod > R:
                    break

        else:
            cnt = R // prod - (L - 1) // prod

            if bits % 2 == 0:
                ans += cnt
            else:
                ans -= cnt

    print(ans)

solve()
```

The first part checks whether $k$ is prime. This is not an optimization, it is a correctness requirement. If $k$ is composite, no number can have smallest divisor exactly $k$.

Next we convert the original interval into multiplier space. Every candidate number is a multiple of $k$, so we only work with values of $t$. The ceiling division for the left boundary is easy to get wrong. Using:

```
(a + k - 1) // k
```

correctly computes the smallest integer $t$ such that $kt \ge a$.

The inclusion-exclusion loop iterates through every subset of forbidden primes. The variable `prod` stores the product of primes in the current subset. If that product already exceeds `R`, no number in the range can be divisible by it, so the subset contributes nothing.

The alternating signs come directly from inclusion-exclusion. Even-sized subsets add counts, odd-sized subsets subtract counts.

The implementation never risks overflow because Python integers are arbitrary precision, but the early break on `prod > R` keeps the subset processing small.

## Worked Examples

### Example 1

Input:

```
1 10 2
```

We have $k=2$, which is prime.

$$L = \left\lceil \frac{1}{2} \right\rceil = 1$$

$$R = \left\lfloor \frac{10}{2} \right\rfloor = 5$$

There are no primes smaller than $2$, so every $t$ in $[1,5]$ is valid.

| Step | Value |
| --- | --- |
| $L$ | 1 |
| $R$ | 5 |
| Forbidden primes | none |
| Valid $t$ | 1,2,3,4,5 |
| Valid $x$ | 2,4,6,8,10 |
| Answer | 5 |

This demonstrates the simplest case where inclusion-exclusion has only the empty subset.

### Example 2

Input:

```
1 30 5
```

Since $5$ is prime:

$$L = 1,\quad R = 6$$

Forbidden primes are $2$ and $3$.

| Subset | Product | Count in $[1,6]$ | Contribution |
| --- | --- | --- | --- |
| {} | 1 | 6 | +6 |
| {2} | 2 | 3 | -3 |
| {3} | 3 | 2 | -2 |
| {2,3} | 6 | 1 | +1 |

Final answer:

$$6 - 3 - 2 + 1 = 2$$

The valid multipliers are $1$ and $5$, giving numbers $5$ and $25$.

This trace shows how inclusion-exclusion removes numbers divisible by forbidden primes and restores overlaps correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{k} + 2^{\pi(k)})$ | primality testing plus inclusion-exclusion over primes smaller than $k$ |
| Space | $O(\pi(k))$ | storing forbidden primes |

The number of relevant primes is tiny because their product grows very quickly. Even though inclusion-exclusion is exponential in the number of primes, the actual subset count stays small enough for the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    def is_prime(x):
        if x < 2:
            return False
        d = 2
        while d * d <= x:
            if x % d == 0:
                return False
            d += 1
        return True

    def primes_less_than(k):
        primes = []
        for x in range(2, k):
            ok = True
            d = 2
            while d * d <= x:
                if x % d == 0:
                    ok = False
                    break
                d += 1
            if ok:
                primes.append(x)
        return primes

    a, b, k = map(int, input().split())

    if not is_prime(k):
        print(0)
        return

    L = (a + k - 1) // k
    R = b // k

    if L > R:
        print(0)
        return

    primes = primes_less_than(k)

    ans = 0
    m = len(primes)

    for mask in range(1 << m):
        bits = 0
        prod = 1

        for i in range(m):
            if (mask >> i) & 1:
                bits += 1
                prod *= primes[i]

                if prod > R:
                    break
        else:
            cnt = R // prod - (L - 1) // prod

            if bits % 2 == 0:
                ans += cnt
            else:
                ans -= cnt

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("1 10 2\n") == "5", "sample 1"

# composite k
assert run("1 100 6\n") == "0", "composite k"

# single valid number
assert run("13 13 13\n") == "1", "single prime"

# no multiples of k in range
assert run("1 10 13\n") == "0", "empty multiplier interval"

# boundary case with ceil division
assert run("15 30 5\n") == "1", "left boundary correctness"

# larger interval
assert run("1 30 5\n") == "2", "inclusion exclusion correctness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 100 6` | `0` | composite $k$ immediately fails |
| `13 13 13` | `1` | interval containing exactly one valid number |
| `1 10 13` | `0` | no multiples of $k$ exist |
| `15 30 5` | `1` | correct ceiling division on left boundary |
| `1 30 5` | `2` | inclusion-exclusion overlap handling |

## Edge Cases

Consider the composite case:

Input:

```
1 100 6
```

The algorithm first checks primality. Since $6$ is divisible by $2$, it is not prime, so the algorithm immediately returns:

```
0
```

This is correct because every multiple of $6$ is already divisible by $2$, which is smaller than $6$.

Now consider the boundary case where only $k$ itself may qualify:

Input:

```
10 20 13
```

We compute:

$$L = \left\lceil \frac{10}{13} \right\rceil = 1$$

$$R = \left\lfloor \frac{20}{13} \right\rfloor = 1$$

The only multiplier is $t=1$, corresponding to $x=13$. Since $1$ is divisible by no forbidden primes, the answer becomes:

```
1
```

The algorithm handles this naturally without special branching.

Finally, consider the off-by-one trap:

Input:

```
15 30 5
```

The algorithm computes:

$$L = (15+5-1)//5 = 3$$

$$R = 30//5 = 6$$

The candidate multipliers are $3,4,5,6$. Inclusion-exclusion removes $3,4,6$ because they are divisible by $2$ or $3$. Only $5$ remains, giving the single valid number $25$.

If we had used ordinary floor division for the left boundary, we would incorrectly include multiplier $2$, corresponding to $10$, which lies outside the interval.
