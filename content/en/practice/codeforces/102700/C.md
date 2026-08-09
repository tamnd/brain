---
title: "CF 102700C - Cipher count"
description: "The key observation is that two different key strings do not necessarily represent two different Vigenère ciphers. If a key is itself a repetition of a shorter string, extending either key periodically produces exactly the same sequence of shifts."
date: "2026-08-10T05:50:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102700
codeforces_index: "C"
codeforces_contest_name: "2020 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102700
solve_time_s: 501
verified: true
draft: false
---

[CF 102700C - Cipher count](https://codeforces.com/problemset/problem/102700/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

The key observation is that two different key strings do not necessarily represent two different Vigenère ciphers. If a key is itself a repetition of a shorter string, extending either key periodically produces exactly the same sequence of shifts.

For example, over a binary alphabet, the keys `0`, `00`, `000`, and so on all generate the same infinite shift sequence. Likewise, `01` and `0101` are equivalent because both generate `010101...`. The attacker only needs to try one representative from each such equivalence class.

Every nonempty string can be written uniquely as repetitions of a shortest string. That shortest string is called its primitive root. A string is primitive when it cannot itself be written as a repetition of a shorter string. Thus, the problem is equivalent to counting all primitive strings whose lengths are at most `k`.

For an alphabet of size `a`, there are `a^n` strings of length `n`. Let `P(n)` be the number of primitive strings of length `n`. Every string of length `n` has a unique primitive root whose length divides `n`, so

[
a^n = \sum_{d\mid n} P(d).
]

Möbius inversion gives

[
P(n)=\sum_{d\mid n}\mu(d)a^{n/d},
]

where `μ` is the Möbius function. This standard primitive-word formula follows directly from the unique primitive-root decomposition.

The required answer is

[
\sum_{n=1}^{k}P(n).
]

The alphabet size is at most `10^3`, while the maximum key length is `5 * 10^6`. The important constraint is the latter. Any algorithm involving all possible keys is exponential in `k`, and even an `O(k log k)` divisor enumeration is unnecessarily expensive. A linear-time sieve followed by a linear scan is the appropriate target.

There are several edge cases that can easily break a careless implementation. For `a = 1` and `k = 3`, the only possible key at every length is a string of identical symbols, so every key represents the same cipher and the answer is `1`. For `a = 2` and `k = 2`, the four possible keys are `0`, `1`, `00`, and `11` at lengths up to two, but `00` has primitive root `0` and `11` has primitive root `1`, so the answer is `4`, not `4` plus some additional repeated-key classes. For `a = 2` and `k = 3`, the primitive counts are `P(1)=2`, `P(2)=2`, and `P(3)=6`, giving answer `10`. A solution that simply sums `2^n` would incorrectly count repeated keys several times.

The official statement gives the same constraints and sample behavior, including the fact that keys such as `00` and `11` need not both be tried separately.

## Approaches

A direct approach would generate every possible key of every length from `1` through `k`. There are

[
a+a^2+\cdots+a^k
]

such keys. For each key, we could find its shortest period and count it only if it is primitive. This is correct because exactly one representative from every cipher-equivalence class is primitive.

The problem is the number of candidates. When `a >= 2`, the total is `Θ(a^k)`, already exponential. At the maximum values `a=1000` and `k=5*10^6`, the number of length-`k` candidates alone is `1000^{5,000,000}=10^{15,000,000}`. If we also explicitly inspect up to `k` positions to test periodicity, the work becomes `Θ(k a^k)`. Enumeration itself is already impossible, so optimizing the period test cannot rescue this approach.

The useful observation is that we never need to construct a key. We only need the number of primitive strings of each length. The primitive-root decomposition gives a clean divisor identity,

[
a^n=\sum_{d\mid n}P(d).
]

Möbius inversion converts this into a formula for `P(n)`. Computing that formula independently for every `n` would still require enumerating divisors. The second observation removes that cost.

Start with

\sum_{n=1}^{k}\sum_{d\mid n}\mu(d)a^{n/d}.
]

Write `n = d x`. Then `d x <= k`, so

[
\sum_{x=1}^{k}a^x
\sum_{d=1}^{\lfloor k/x\rfloor}\mu(d).
]

Define the prefix Möbius sum

[
M(t)=\sum_{d=1}^{t}\mu(d).
]

The entire answer becomes

[
\boxed{
\sum_{x=1}^{k}a^x M\left(\left\lfloor\frac{k}{x}\right\rfloor\right)
}.
]

Now every term is obtained in constant time once the Möbius prefix sums are known. We can generate all Möbius values with a linear Euler sieve, build their prefix sums, and then evaluate the formula in one more linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `Θ(k a^k)` if periodicity is checked directly | `O(k)` per candidate | Too slow |
| Optimal | `O(k)` | `O(k)` | Accepted |

## Algorithm Walkthrough

1. Read the alphabet size `a` and maximum key length `k`. If `a=1`, immediately return `1`, because every possible key consists of the same symbol and has the same primitive root.
2. Compute the Möbius function `μ(1), μ(2), ..., μ(k)` with a linear Euler sieve. The sieve keeps the smallest prime factor of each number and constructs `μ` at the same time. A prime gets Möbius value `-1`. If a number receives a prime factor that is already present in its factorization, its Möbius value becomes `0`. Otherwise the sign is flipped.
3. Convert the Möbius array into its prefix sums. After this transformation, the value stored at position `t` is

[
M(t)=\mu(1)+\mu(2)+\cdots+\mu(t).
]

The original Möbius values are no longer needed, so the same storage used for the sieve can be reused for these prefix sums.

1. Maintain `power = a^x mod MOD` while iterating `x` from `1` to `k`. For the current `x`, add

[
a^x M\left(\left\lfloor\frac{k}{x}\right\rfloor\right)
]

to the answer. The prefix sum is indexed by `k // x` because that is exactly the range of possible divisors `d` after substituting `n = d x`.

1. Update `power` by multiplying it by `a` modulo `10^9+7`. After the final iteration, print the accumulated answer modulo `10^9+7`.

### Why it works

Every nonempty key has a unique primitive root. Two keys produce the same periodic sequence of shifts exactly when they have the same primitive root, so the number of keys that the attacker must try is precisely the number of primitive strings of lengths at most `k`.

For length `n`, every string is a repetition of a unique primitive string whose length divides `n`. Thus `a^n = Σ_{d|n} P(d)`, and Möbius inversion gives `P(n) = Σ_{d|n} μ(d)a^{n/d}`.

Summing over all `n <= k` and exchanging the order of summation gives

\sum_{x=1}^{k}a^xM(\lfloor k/x\rfloor).
]

The algorithm evaluates exactly this expression, so every primitive-root class contributes once and only once.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    a, k = map(int, input().split())

    # With a one-letter alphabet, every key is a repetition
    # of the same one-character primitive root.
    if a == 1:
        print(1)
        return

    # lp[x] = smallest prime factor of x.
    # Using a compact integer array keeps memory usage small.
    lp = array('I', [0]) * (k + 1)

    # mu[x] is stored as -1, 0, or 1.
    mu = array('b', [0]) * (k + 1)
    mu[1] = 1

    primes = array('I')

    # Linear Euler sieve for the Möbius function.
    for i in range(2, k + 1):
        if lp[i] == 0:
            lp[i] = i
            primes.append(i)
            mu[i] = -1

        li = lp[i]

        for p in primes:
            x = i * p
            if x > k:
                break

            lp[x] = p

            if p == li:
                mu[x] = 0
                break
            else:
                mu[x] = -mu[i]

    # lp is no longer needed as a smallest-prime-factor array.
    # Reuse it to store Mertens prefix sums:
    # lp[i] = mu(1) + ... + mu(i).
    prefix = 0
    for i in range(1, k + 1):
        prefix += mu[i]
        lp[i] = prefix

    del mu
    del primes

    ans = 0
    power = a % MOD

    # ans = sum_{x=1}^k a^x * M(floor(k/x)).
    for x in range(1, k + 1):
        ans = (ans + power * lp[k // x]) % MOD
        power = (power * a) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The Euler sieve is the implementation of Step 2. `lp` records the smallest prime factor, while `mu` stores only three possible values, so a signed byte array is enough for the Möbius function.

The condition `p == li` is the key part of the sieve. If `p` is already the smallest prime factor of `i`, then `i*p` contains a squared prime factor, so its Möbius value is zero. Otherwise, multiplying by a new prime changes the sign of the Möbius value.

After the sieve, `lp` is no longer needed for factorization. Reusing it for the Mertens prefix sums avoids allocating another large array. This matters because `k` can reach five million.

The final loop does not compute `P(x)` individually. Instead, it directly evaluates the transformed sum

[
a^xM(\lfloor k/x\rfloor).
]

`power` always contains `a^x mod MOD` at the beginning of the iteration for `x`. Updating it after adding the current term avoids an off-by-one error. Python integers do not overflow, but reducing after each multiplication keeps the intermediate values small and the implementation efficient.

The special case `a=1` is also more than a micro-optimization. It makes the maximum-length test immediate, because there is only one possible key at every length and all of them have the same primitive root.

## Worked Examples

### Sample 1: `a = 26, k = 1`

Only keys of length one are allowed. Every one-character key is primitive, so the answer must be `26`.

For `k=1`, the Möbius values and prefix sums are:

| `x` | `μ(x)` | `M(x)` | `a^x` | `k // x` | Added term |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 26 | 1 | 26 |

The final answer is `26`.

This confirms that the transformation does not lose the simplest case. The formula reduces to `a^1 * M(1) = a`.

### Sample 2: `a = 2, k = 2`

There are four raw keys: `0`, `1`, `00`, and `11`. The first two are primitive. The last two are repetitions of the first two, so there are still four keys to try according to the problem's representative-key interpretation, because the primitive strings of lengths at most two are `0`, `1`, `01`, and `10`.

The relevant Möbius values are

[
\mu(1)=1,\qquad \mu(2)=-1,
]

so the prefix sums are

[
M(1)=1,\qquad M(2)=0.
]

The transformed sum is:

| `x` | `μ(x)` | `M(x)` | `a^x` | `k // x` | `M(k // x)` | Added term |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | 2 | 0 | 0 |
| 2 | -1 | 0 | 4 | 1 | 1 | 4 |

The answer is `4`.

The zero contribution for `x=1` reflects the cancellation caused by length-two repetitions. The four remaining representatives are exactly the four primitive strings of lengths one and two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(k)` | The Euler sieve performs linear work, followed by two linear scans. |
| Space | `O(k)` | The smallest-prime-factor array, Möbius values, and prime list all have linear size. |

With `k <= 5 * 10^6`, linear complexity is appropriate. The implementation uses compact `array` storage rather than Python's much larger general-purpose integer lists for the sieve data, keeping the memory usage comfortably below the `512 MB` limit.

## Test Cases

```python
import io
import sys
from array import array

MOD = 1_000_000_007

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    a, k = map(int, sys.stdin.readline().split())

    if a == 1:
        print(1)
    else:
        lp = array('I', [0]) * (k + 1)
        mu = array('b', [0]) * (k + 1)
        mu[1] = 1
        primes = array('I')

        for i in range(2, k + 1):
            if lp[i] == 0:
                lp[i] = i
                primes.append(i)
                mu[i] = -1

            li = lp[i]

            for p in primes:
                x = i * p
                if x > k:
                    break

                lp[x] = p

                if p == li:
                    mu[x] = 0
                    break
                mu[x] = -mu[i]

        s = 0
        for i in range(1, k + 1):
            s += mu[i]
            lp[i] = s

        ans = 0
        power = a % MOD

        for x in range(1, k + 1):
            ans = (ans + power * lp[k // x]) % MOD
            power = power * a % MOD

        print(ans)

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("26 1\n") == "26\n", "sample 1"
assert run("2 2\n") == "4\n", "sample 2"
assert run("1 3\n") == "1\n", "sample 3"

assert run("1 1\n") == "1\n", "minimum alphabet and key length"
assert run("2 3\n") == "10\n", "primitive lengths 1, 2, and 3"
assert run("1000 1\n") == "1000\n", "maximum alphabet at key length 1"
assert run("1 5000000\n") == "1\n", "maximum key length with one-letter alphabet"
assert run("2 4\n") == "22\n", "length-four divisor boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum values and the one-symbol alphabet case |
| `2 3` | `10` | Several primitive lengths and a prime key length |
| `1000 1` | `1000` | Maximum alphabet size and `k=1` boundary |
| `1 5000000` | `1` | Maximum `k` and the special `a=1` case |
| `2 4` | `22` | Composite length with nontrivial divisors |

## Edge Cases

For `a=1` and `k=3`, the only possible keys are the one-symbol string, its two-symbol repetition, and its three-symbol repetition. Every one has the same primitive root. The implementation returns `1` immediately, avoiding unnecessary sieve work.

For `a=2` and `k=2`, the primitive strings are `0`, `1`, `01`, and `10`. The strings `00` and `11` are not new primitive roots because they are repetitions of `0` and `1`. The Möbius calculation gives `P(1)=2` and `P(2)=4-2=2`, so the total is `4`.

For `a=2` and `k=3`, the length-one contribution is `2`. At length two, the two nonprimitive strings are `00` and `11`, leaving `2` primitive strings. At length three, the only proper divisor is one, so `P(3)=2^3-2=6`. The answer is `2+2+6=10`. This case catches implementations that accidentally exclude primitive strings at prime lengths.

For `a=2` and `k=4`, the length-four strings include repetitions of length-one and length-two roots. The formula gives

[
P(4)=2^4-2^2=12,
]

because `μ(4)=0` and `μ(2)=-1`. The total is

# 2+2+6+12

1. 

]

This catches divisor-boundary mistakes involving a square factor, where the Möbius value must be zero.

Finally, for `a=1` and `k=5,000,000`, the answer remains `1`. This is both a mathematical edge case and a practical stress case. A solution that constructs or sieves all lengths unnecessarily can waste substantial time, while the special case finishes immediately.
