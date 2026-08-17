---
title: "CF 102253D - Division Game"
description: "We have (k) identical piles, each initially containing the same huge integer (n). The piles are arranged cyclically. Round (1) operates pile (0), round (2) operates pile (1), and so on, wrapping around after pile (k-1)."
date: "2026-08-17T21:25:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102253
codeforces_index: "D"
codeforces_contest_name: "2017 Chinese Multi-University Training, BeihangU Contest"
rating: 0
weight: 102253
solve_time_s: 193
verified: true
draft: false
---

[CF 102253D - Division Game](https://codeforces.com/problemset/problem/102253/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (k) identical piles, each initially containing the same huge integer (n). The piles are arranged cyclically. Round (1) operates pile (0), round (2) operates pile (1), and so on, wrapping around after pile (k-1).

An operation replaces the current value (x) in a pile by a proper divisor (d) of (x), so (1 \le d < x). The game stops immediately when some pile becomes (1). For every pile (i), we need the number of complete operation sequences whose first pile to reach (1), and hence last changed pile, is (i).

The integer (n) itself can be far too large to construct. Instead, its prime factorization is given as

[
n=\prod_{j=1}^{m}p_j^{e_j}.
]

The primes themselves are almost irrelevant to the combinatorics. What matters is the exponent vector ((e_1,\ldots,e_m)), because replacing a number by a divisor simply decreases each prime exponent independently.

Let

[
w=\sum_{j=1}^{m}e_j.
]

Every operation decreases at least one exponent by at least one, so a single pile can be operated at most (w) times. Since (w\le 10^5), a solution whose main loop is linear or (O(w\log w)) is realistic. A quadratic algorithm with (10^{10}) operations at the upper bound is completely ruled out. The fact that only a few test cases have (w\ge 10^4) is especially useful for an NTT-based implementation, because the expensive transforms are needed only for the genuinely large cases. The official solution uses exactly this reduction and an NTT under the given modulus.

There are several boundary cases where a superficial simulation or an incorrectly indexed formula gives the wrong answer. For example, with

```
1 1
2 2
```

we have (n=4) and one pile. There are exactly two chains, (4\to1) and (4\to2\to1), so the answer is `Case #1: 2`. A simulation that only considers the shortest chain misses the second possibility.

With

```
1 2
2 1
```

we have two piles and (n=2). Pile (0) can immediately become (1), giving one valid sequence. If pile (1) is supposed to be last, pile (0) must first be changed without becoming (1), which is impossible. The answer is `Case #1: 1 0`. Treating the piles symmetrically would incorrectly give the same answer for both.

A second subtle case is when several prime exponents can be decreased in the same operation. For (n=6=2^1 3^1), one operation can change (6) directly to (1), or it can remove only one prime factor and leave (2) or (3). A method that counts chains for each prime independently and then multiplies them misses the requirement that every operation must decrease at least one exponent, while allowing several exponents to decrease together.

Finally, the term corresponding to zero previous operations must be handled correctly. We define (f(0)=0), because a positive number cannot become (1) in zero operations. At the other boundary, (f(w+1)=0), because (w+1) operations cannot occur on one pile. These two artificial boundary values make the final summation clean and prevent off-by-one errors.

## Approaches

A direct approach would simulate every possible divisor choice for every pile. This is correct because every legal operation is exactly a transition from one divisor to a smaller proper divisor. The problem is the number of chains. Consider the particularly simple input (n=2^w). A chain from (2^w) to (1) is determined by which of the intermediate exponents (1,2,\ldots,w-1) occur. Every subset gives one strictly decreasing chain, so there are exactly (2^{w-1}) chains for just one pile. With (w=10^5), that is (2^{99999}) possibilities. Brute force is already impossible before considering multiple piles.

The key observation is to forget the actual prime values and describe one pile entirely by its exponent vector. Suppose a pile is changed exactly (x) times before reaching (1). Let (d_{r,j}) be how much exponent (e_r) is removed during operation (j). Then

[
\sum_{j=1}^{x}d_{r,j}=e_r
]

for every prime (r), and every operation must actually change the pile, so

[
\sum_{r=1}^{m}d_{r,j}>0
]

for every operation (j).

Thus (f(x)), the number of ways for one pile to become (1) in exactly (x) operations, is precisely the number of such matrices (d). This turns a divisor-chain problem into a restricted composition problem. This is the central combinatorial transformation used by the official solution.

If we temporarily ignore the requirement that every operation must remove something, each exponent (e_r) can be distributed among (x) operations in

[
\binom{e_r+x-1}{x-1}
]

ways. Multiplying over all prime factors gives

[
g(x)=\prod_{r=1}^{m}\binom{e_r+x-1}{x-1}.
]

Now some of the (x) operations may receive nothing at all. Inclusion-exclusion over the empty operations gives

[
f(x)=\sum_{y=0}^{x}(-1)^{x-y}\binom{x}{y}g(y).
]

Computing this formula independently for every (x) would again be quadratic. The useful part is that the binomial coefficient separates:

[
\binom{x}{y}=\frac{x!}{y!(x-y)!}.
]

Hence

\sum_{y=0}^{x}
\frac{(-1)^{x-y}}{(x-y)!}
\frac{g(y)}{y!}.
]

This is an ordinary convolution. Define

[
A_t=\frac{(-1)^t}{t!},
\qquad
B_y=\frac{g(y)}{y!}.
]

Then

[
\frac{f(x)}{x!}=(A*B)_x.
]

The modulus is particularly convenient:

[
985661441=235\cdot2^{22}+1,
]

and (3) is a primitive root, so powers of two up to (2^{22}) support NTT. The largest required convolution has length at most about (2w), which fits inside (2^{18}) when (w\le10^5).

We still need to connect (f) back to the circular sequence of piles. Suppose pile (i), using zero-based indexing, is the one that becomes (1), and suppose this happens on its (x)-th operation. Every pile before (i) has already been operated (x) times and must still contain more than one stone. The number of such histories is (f(x+1)), because any valid history of (x) operations that ends above (1) has exactly one possible next operation, namely changing that remaining value to (1). The final pile has (x) operations and contributes (f(x)). Every pile after (i) has only (x-1) operations and also contributes (f(x)). Thus

\sum_{x=0}^{w}
f(x+1)^i f(x)^{k-i}.
]

This is (O(wk)), which is small because (k\le10). The same formula appears in the official derivation, with one-based pile indices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^w)) or worse over all piles | Exponential | Too slow |
| Optimal | (O(wm+w\log w+wk)) | (O(w)) | Accepted |

## Algorithm Walkthrough

1. Read all test cases and store only the exponents (e_1,\ldots,e_m) and (k). The prime values never participate in the counting, because divisor operations are completely determined by exponent decreases.
2. Compute (w=\sum e_i). No pile can be operated more than (w) times, since every legal operation decreases the total exponent sum by at least one.
3. Precompute factorials and inverse factorials modulo (985661441) up to the largest (w) among all test cases. Since (w<985661441), every integer up to (w) has a modular inverse.
4. Build (g(x)) for (1\le x\le w), where

[
g(x)=\prod_r\binom{e_r+x-1}{x-1}.
]

Set (g(0)=0), because positive exponents cannot be distributed among zero operations. Starting from (g(1)=1), each factor satisfies

\binom{e+x-1}{x-1}\frac{e+x}{x}.
]

Thus each step from (g(x)) to (g(x+1)) needs only (m) modular multiplications instead of recomputing binomial coefficients from scratch.

1. Construct the two convolution arrays

[
A_t=\frac{(-1)^t}{t!},
\qquad
B_t=\frac{g(t)}{t!}.
]

The convolution coefficient at position (x) is exactly (f(x)/x!).

1. Multiply these two arrays with NTT. The required transform size is the smallest power of two at least (2(w+1)-1). The given modulus has a sufficiently large power of two in (p-1), so the transform is exact modular arithmetic rather than floating-point FFT.
2. Recover

[
f(x)=(A*B)_x x!
]

for (0\le x\le w). Append (f(w+1)=0). This value is zero because a pile cannot require more than (w) operations to reach (1).

1. For every pile (i), compute

\sum_{x=0}^{w}
f(x+1)^i f(x)^{k-i}.
]

The exponent (i) corresponds to the piles that occur before the final pile in the cyclic order. The remaining (k-i) factors correspond to the final pile and the piles after it.

1. Output the (k) answers modulo (985661441). The resulting sequence is asymmetric in general because the round order is fixed, even though all piles start with the same value.

Why it works: the invariant behind the entire solution is that a legal chain of divisor operations is equivalent to a matrix of exponent decreases whose row sums equal the original exponents and whose columns are all nonzero. The function (g) counts all matrices with the correct row sums, and inclusion-exclusion removes exactly those matrices containing an empty column. Thus (f(x)) counts exactly the legal (x)-operation chains to (1). For a fixed final pile and fixed (x), the cyclic schedule determines exactly how many operations every other pile has received, and the (f(x+1)) versus (f(x)) factors count precisely the histories that have not yet reached (1). Summing over every possible (x) counts every valid game exactly once, at the moment its first pile becomes (1).

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 985661441
ROOT = 3
NAIVE_LIMIT = 256

FACT = []
IFACT = []

def ntt(a, invert):
    n = len(a)

    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        wlen = pow(ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)

        half = length >> 1
        for start in range(0, n, length):
            w = 1
            end = start + half
            for i in range(start, end):
                u = a[i]
                v = a[i + half] * w % MOD

                x = u + v
                if x >= MOD:
                    x -= MOD

                y = u - v
                if y < 0:
                    y += MOD

                a[i] = x
                a[i + half] = y
                w = w * wlen % MOD

        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def convolution(a, b):
    need = len(a) + len(b) - 1

    if min(len(a), len(b)) <= NAIVE_LIMIT:
        res = [0] * need
        for i, x in enumerate(a):
            if x == 0:
                continue
            for j, y in enumerate(b):
                if y:
                    res[i + j] = (res[i + j] + x * y) % MOD
        return res

    size = 1
    while size < need:
        size <<= 1

    a += [0] * (size - len(a))
    b += [0] * (size - len(b))

    ntt(a, False)
    ntt(b, False)

    for i in range(size):
        a[i] = a[i] * b[i] % MOD

    ntt(a, True)
    return a[:need]

def build_f(exps):
    w = sum(exps)

    g = [0] * (w + 1)
    g[1] = 1

    for x in range(1, w):
        inv_x = FACT[x - 1] * IFACT[x] % MOD
        ratio = 1

        for e in exps:
            ratio = ratio * (e + x) % MOD
            ratio = ratio * inv_x % MOD

        g[x + 1] = g[x] * ratio % MOD

    a = [0] * (w + 1)
    b = [0] * (w + 1)

    for x in range(w + 1):
        inv_fact = IFACT[x]
        a[x] = inv_fact if x % 2 == 0 else MOD - inv_fact
        b[x] = g[x] * inv_fact % MOD

    c = convolution(a, b)

    f = [0] * (w + 2)
    for x in range(w + 1):
        f[x] = c[x] * FACT[x] % MOD

    f[w + 1] = 0
    return f

def solve():
    global FACT, IFACT

    cases = []
    max_w = 0

    while True:
        line = input()
        if not line:
            break
        if not line.strip():
            continue

        m, k = map(int, line.split())
        exps = []

        for _ in range(m):
            _, e = map(int, input().split())
            exps.append(e)

        w = sum(exps)
        max_w = max(max_w, w)
        cases.append((exps, k))

    if not cases:
        return

    FACT = [1] * (max_w + 1)
    for i in range(1, max_w + 1):
        FACT[i] = FACT[i - 1] * i % MOD

    IFACT = [1] * (max_w + 1)
    IFACT[max_w] = pow(FACT[max_w], MOD - 2, MOD)
    for i in range(max_w, 0, -1):
        IFACT[i - 1] = IFACT[i] * i % MOD

    out = []

    for case_id, (exps, k) in enumerate(cases, 1):
        w = sum(exps)
        f = build_f(exps)

        ans = [0] * k

        for x in range(w + 1):
            left = f[x + 1]
            right = f[x]

            powers_left = [1] * k
            powers_right = [1] * (k + 1)

            for j in range(1, k):
                powers_left[j] = powers_left[j - 1] * left % MOD

            for j in range(1, k + 1):
                powers_right[j] = powers_right[j - 1] * right % MOD

            for i in range(k):
                ans[i] += powers_left[i] * powers_right[k - i] % MOD
                if ans[i] >= MOD:
                    ans[i] -= MOD

        out.append(
            "Case #{}: {}".format(case_id, " ".join(map(str, ans)))
        )

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input phase stores the exponent lists first so factorials can be precomputed only once, using the maximum (w) across all test cases. This matters because there can be around 200 cases, and repeatedly rebuilding factorial arrays would add unnecessary work.

The recurrence for (g) avoids factorials with arguments as large as (e_i+x-1). For each exponent, the transition from (x) to (x+1) multiplies by ((e_i+x)/x). The inverse of (x) is obtained as `FACT[x - 1] * IFACT[x]`. The denominator must be applied once for every exponent, which is why the inverse appears inside the loop over `exps`.

The two arrays `a` and `b` implement the normalized convolution directly. `a[x]` is ((-1)^x/x!), while `b[x]` is (g(x)/x!). After convolution, multiplying coefficient (x) by `FACT[x]` recovers (f(x)).

The NTT uses primitive root (3), which is valid for this modulus. The modulus has the form (235\cdot2^{22}+1), so every transform length needed by the problem divides the available power of two.

The final loop deliberately runs through (x=w). At (x=w), `f[x + 1]` is the explicitly appended zero. For pile (0), its exponent is zero, so the corresponding (0^0) is interpreted by the modular power array as (1), which is exactly what the formula requires. For every other pile, the same term vanishes because a positive power of `f[w + 1]` occurs.

The implementation uses a quadratic convolution only for very small arrays. Once the polynomial becomes large, NTT is used. This does not change the asymptotic complexity and avoids paying NTT's larger constant factor on tiny test cases.

## Worked Examples

### Sample 1

The first sample case is

```
1 1
2 2
```

so (n=2^2=4), (k=1), and (w=2).

For one prime exponent (e=2), the unrestricted distribution counts are

[
g(1)=1,\qquad g(2)=\binom31=3.
]

Inclusion-exclusion gives

[
f(1)=1,
]

and

[
f(2)=g(2)-2g(1)=3-2=1.
]

There cannot be three nonempty operations when the total exponent sum is only two, so (f(3)=0).

| (x) | (f(x)) | (f(x+1)) | Contribution to pile 0 |
| --- | --- | --- | --- |
| 0 | 0 | 1 | (1^0 0^1=0) |
| 1 | 1 | 1 | (1^0 1^1=1) |
| 2 | 1 | 0 | (0^0 1^1=1) |

The two contributions correspond exactly to (4\to1) and (4\to2\to1). The result is `Case #1: 2`, matching the sample output.

### Sample 2

The second sample case is

```
2 1
2 1
3 1
```

so (n=2\cdot3=6), (k=1), and (w=2).

There are two exponent rows, each containing one unit. For one operation both units must be placed in the same operation, giving (f(1)=1). For two operations, each exponent must be assigned to a different operation, giving two possibilities, so (f(2)=2).

| (x) | (f(x)) | (f(x+1)) | Contribution |
| --- | --- | --- | --- |
| 0 | 0 | 1 | (0) |
| 1 | 1 | 2 | (1) |
| 2 | 2 | 0 | (2\cdot0^0=2) |

The two length-two chains are (6\to2\to1) and (6\to3\to1), while (6\to1) gives the length-one chain. The total is (3), producing `Case #2: 3`.

The second trace also demonstrates why different prime exponents may be removed in the same operation. The two exponent units are not forced to behave as independent chains.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(wm+w\log w+wk)) | (g(x)) takes (O(wm)), the NTT convolution takes (O(w\log w)), and all pile answers take (O(wk)) |
| Space | (O(w)) | Factorials, convolution arrays, and (f) all have linear size |

The largest (w) is (10^5), while (m,k\le10). The NTT length is the next power of two above (2w+1), at most (2^{18}). The modulus supports this transform size because its (2)-adic factor is (2^{22}). The special restriction that only five cases can have (w\ge10^4) keeps the expensive large transforms under control. The resulting complexity matches the intended solution.

## Test Cases

The following tests assume the solution above is saved as `solution.py`. The helper replaces standard input and captures standard output, so the same `solve()` function used by the judge is tested.

```python
# helper: run solution on input string, return output string
import sys
import io
from solution import solve

MOD = 985661441

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    try:
        solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    return output.getvalue()

# Provided samples
sample = """\
1 1
2 2
2 1
3 1
5 1
1 2
2 3
2 2
2 4
5 4
"""

expected_sample = """\
Case #1: 2
Case #2: 3
Case #3: 6 4
Case #4: 1499980 1281085
"""

assert run(sample) == expected_sample, "provided samples"

# Custom 1: minimum exponent, many piles.
# n = 2, k = 10. Only pile 0 can become 1.
inp = """\
1 10
2 1
"""

expected = "Case #1: 1 " + " ".join(["0"] * 9) + "\n"
assert run(inp) == expected, "prime n with many piles"

# Custom 2: boundary between one and two operations.
# n = 4, k = 2.
# f(1) = 1, f(2) = 1, so answers are [2, 1].
inp = """\
1 2
2 2
"""

assert run(inp) == "Case #1: 2 1\n", "two-pile boundary case"

# Custom 3: equal exponents on distinct primes.
# n = 2^2 * 3^2 = 36, k = 2.
# f(1), f(2), f(3), f(4) = 1, 7, 12, 6.
# Answers are 230 and 163.
inp = """\
2 2
2 2
3 2
"""

assert run(inp) == "Case #1: 230 163\n", "equal exponent case"

# Custom 4: maximum allowed exponent sum.
# n = 2^100000, k = 1.
# For one prime, every chain is a strictly decreasing sequence of
# exponents, so there are 2^99999 chains.
inp = """\
1 1
2 100000
"""

expected = f"Case #1: {pow(2, 99999, MOD)}\n"
assert run(inp) == expected, "maximum-size exponent case"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 10 / 2 1` | `Case #1: 1 0 0 0 0 0 0 0 0 0` | Minimum exponent, cyclic ordering, and the fact that the first pile is special |
| `1 2 / 2 2` | `Case #1: 2 1` | The (x=0) and (x=w) boundaries and pile-index orientation |
| `2 2 / 2 2 / 3 2` | `Case #1: 230 163` | Multiple prime factors with equal exponents and simultaneous exponent decreases |
| `1 1 / 2 100000` | `Case #1: 2^99999 mod 985661441` | Maximum (w), large factorials, NTT, and the exponential number of underlying chains |

## Edge Cases

For the two-pile prime case

```
1 2
2 1
```

we have (w=1), (f(0)=0), (f(1)=1), and (f(2)=0). For pile (0), the term with (x=1) is

[
f(2)^0f(1)^2=1,
]

so its answer is (1). For pile (1), every term contains a positive power of (f(2)=0), so its answer is (0). The algorithm outputs `Case #1: 1 0`. This catches the most common indexing mistake, where the cyclic order is accidentally treated as symmetric.

For

```
1 2
2 2
```

we have (n=4) and (w=2). The legal chains are (4\to1) and (4\to2\to1), so (f(1)=f(2)=1). For pile (0),

[
f(1)^2+f(2)^2=2,
]

while for pile (1),

[
f(2)f(1)=1.
]

The algorithm produces `Case #1: 2 1`. The (f(w+1)=0) boundary eliminates all impossible longer histories.

For

```
2 2
2 1
3 1
```

the exponent matrix for two operations has two rows and two columns. Each row contains one unit, and both columns must be nonempty, so the two rows must be assigned to different columns. There are exactly two possibilities, giving (f(2)=2). The resulting pile answers are `Case #1: 5 2`. This is the case that exposes why a single operation may reduce several different prime exponents at once.

For the maximum-size case

```
1 1
2 100000
```

there is only one exponent. A valid chain is simply a strictly decreasing sequence from exponent (100000) to exponent (0). Every subset of the (99999) intermediate exponents determines one chain, so the answer is

[
2^{99999}\pmod{985661441}.
]

The implementation never constructs (2^{100000}), never enumerates the chains, and never constructs the original integer (n). It only processes the exponent sum (w=100000), which is exactly the information needed by the combinatorial formulation.
