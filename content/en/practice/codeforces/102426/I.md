---
title: "CF 102426I - Integer Factorization"
description: "We are given two integers a and b generated from two unknown primes p and q: [ a=(pq)oplus(p+q), ] [ b=(pq)oplus(p-q). ] The task is to recover the original ordered pair (p, q)."
date: "2026-08-12T19:30:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102426
codeforces_index: "I"
codeforces_contest_name: "The 7-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 102426
solve_time_s: 330
verified: true
draft: false
---

[CF 102426I - Integer Factorization](https://codeforces.com/problemset/problem/102426/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers `a` and `b` generated from two unknown primes `p` and `q`:

[
a=(pq)\oplus(p+q),
]

[
b=(pq)\oplus(p-q).
]

The task is to recover the original ordered pair `(p, q)`. The order matters because the second expression contains `p-q`, so swapping the two primes generally changes `b`.

The challenge is that `pq` itself is not given. Ordinary integer factorization methods cannot be applied directly because there is no known product to factor. The only information we have is two XOR expressions involving the product, sum, and difference.

The input contains up to 3000 independent test cases. Each `a` and `b` fits in a signed 64-bit integer. That makes algorithms depending on enumerating values up to `2^63` completely impossible. Even a linear scan over all possible prime values would already require billions or trillions of operations, while trying all pairs would be astronomically worse.

There are several edge cases that a direct implementation must handle correctly. First, `p` can be smaller than `q`, so `p-q` is negative. For example, with `p=2,q=3`,

[
pq=6,\quad p+q=5,\quad p-q=-1,
]

so

[
a=6\oplus5=3,
]

and under the usual two's-complement interpretation,

[
b=6\oplus(-1)=-7.
]

Thus the input

```
3 -7
```

has output

```
2 3
```

A solution that assumes `p-q` is nonnegative will fail here.

The second edge case is `p=q`. The only way two primes can be equal is for both to be the same prime. For `p=q=2`,

[
a=4\oplus4=0,\qquad b=4\oplus0=4,
]

so

```
0 4
```

must produce

```
2 2
```

A careless implementation that assumes the two primes are distinct can reject this valid case.

There is also a subtle input-format issue in the statement as reproduced here. The formal input description contains `T`, while the displayed sample contains only the pair `1279 1201`. The implementation below accepts both forms, so it works with the formal judge format and with the displayed sample format.

## Approaches

The most direct approach would be to guess `p` and `q`, calculate

[
(pq)\oplus(p+q)
]

and

[
(pq)\oplus(p-q),
]

and compare them with `a` and `b`. Since the relevant values are potentially 64-bit integers, this would require an enormous search space. If we allow both primes to range over 64-bit values, checking all pairs takes on the order of (2^{128}) candidates. Even restricting the search to values around the square root of a possible product is impossible because the product itself is not known.

The useful observation is that XOR, addition, subtraction, and multiplication are all compatible with taking a number modulo a power of two. The lowest `k` bits of `p*q` depend only on the lowest `k` bits of `p` and `q`. The same is true for `p+q` and `p-q`. Consequently, the lowest `k` bits of both outputs depend only on the lowest `k` bits of the two unknown primes.

This gives us a completely different way to search. Instead of guessing the entire 64-bit primes at once, reconstruct them from the least significant bit upwards.

Suppose we already know `k` low bits of a possible pair `(p,q)`. For the next bit, there are only four possibilities:

[
(p_k,q_k)\in{0,1}\times{0,1}.
]

We append each of those four possibilities and calculate the two expressions modulo (2^{k+1}). If either expression disagrees with the corresponding low bits of `a` or `b`, that candidate can never become the real solution, because higher bits cannot change lower bits of ordinary addition, subtraction, multiplication, or XOR.

The brute-force search therefore changes from guessing an enormous integer pair to maintaining a very small set of valid low-bit prefixes. Each level creates four times as many prefixes, but the two output constraints eliminate roughly three quarters of them. This is the same bit-by-bit reconstruction idea used in the official solution of the closely related 2018 USTC RSA problem.

For a 64-bit instance, only 64 levels are needed. At each level we perform a constant amount of arithmetic for each surviving candidate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^{128})) | (O(1)) | Too slow |
| Optimal | (O(64C)), expected (O(64)) | (O(C)) | Accepted |

Here `C` is the maximum number of surviving bit prefixes. The two independent XOR equations keep `C` very small in practice, giving effectively linear work in the number of bits.

## Algorithm Walkthrough

1. Start with the only possible zero-bit prefixes, `(p,q)=(0,0)`. No bits of either prime have been chosen yet.
2. Process the bits from least significant to most significant. At bit position `k`, every surviving pair has already been verified modulo (2^k).
3. For every surviving pair, try all four choices for the next bits of `p` and `q`. If the current prefix is `(x,y)`, the four extensions are

[
(x,y),\quad
(x+2^k,y),\quad
(x,y+2^k),\quad
(x+2^k,y+2^k).
]

1. For each extension, compute

[
f_1(x,y)=(xy)\oplus(x+y)
]

and

[
f_2(x,y)=(xy)\oplus(x-y).
]

Only their lowest `k+1` bits matter at this stage. Use the mask

[
2^{k+1}-1
]

to discard all higher bits.

1. Keep the extension only if

[
f_1(x,y)\bmod 2^{k+1}=a\bmod 2^{k+1}
]

and

[
f_2(x,y)\bmod 2^{k+1}=b\bmod 2^{k+1}.
]

This pruning is valid because operations on integers cannot make higher bits alter already determined lower bits.

1. After enough bits have been reconstructed, check each surviving candidate using the complete expressions rather than only their masked versions. When

[
f_1(p,q)=a
]

and

[
f_2(p,q)=b,
]

we have recovered the required ordered pair.

1. We use 64 reconstruction bits. The given outputs are signed 64-bit values, and the corresponding prime factors are within the range needed by the problem. Python's arbitrary-precision integers also let us evaluate the final product without overflow.

Why it works

The invariant is that after processing bit `k`, every surviving candidate `(x,y)` has exactly the same lowest `k` bits as some possible solution `(p,q)`, and every discarded candidate cannot possibly have those same output bits. The reason is that the low `k` bits of multiplication, addition, subtraction, and XOR depend only on the low `k` bits of their operands. Hence a candidate rejected at level `k` can never be repaired by choosing different higher bits. Conversely, the real `(p,q)` passes every level because its prefixes produce exactly the corresponding prefixes of `a` and `b`. After all relevant bits have been processed, the actual pair remains, and the final exact check removes any remaining prefix that does not represent the complete solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(a, b):
    def f1(x, y):
        return (x * y) ^ (x + y)

    def f2(x, y):
        return (x * y) ^ (x - y)

    candidates = {(0, 0)}

    for bit in range(64):
        mask = (1 << (bit + 1)) - 1
        target_a = a & mask
        target_b = b & mask

        next_candidates = set()

        for x, y in candidates:
            add = 1 << bit

            for bx in (0, 1):
                xx = x + bx * add

                for by in (0, 1):
                    yy = y + by * add

                    if (f1(xx, yy) & mask) != target_a:
                        continue

                    if (f2(xx, yy) & mask) != target_b:
                        continue

                    next_candidates.add((xx, yy))

        candidates = next_candidates

        # A complete solution may be smaller than 2^(bit+1).
        for x, y in candidates:
            if f1(x, y) == a and f2(x, y) == b:
                return x, y

        if not candidates:
            break

    # The problem guarantees a unique solution.
    for x, y in candidates:
        if f1(x, y) == a and f2(x, y) == b:
            return x, y

    raise ValueError("No solution found")

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    # The formal statement has T, while the displayed sample omits it.
    if len(data) >= 3 and len(data) == 1 + 2 * data[0]:
        t = data[0]
        values = data[1:]
    else:
        t = len(data) // 2
        values = data

    out = []

    for i in range(t):
        a = values[2 * i]
        b = values[2 * i + 1]
        p, q = solve_case(a, b)
        out.append(f"{p} {q}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The two helper functions directly encode the two expressions from the problem. Keeping them separate makes the bit-prefix condition easy to read and avoids accidentally using the wrong sign in the second expression.

`mask = (1 << (bit + 1)) - 1` keeps exactly the bits that have been reconstructed so far. The comparison with `a & mask` and `b & mask` is the central pruning operation.

The nested loops over `bx` and `by` generate all four possible assignments for the next bit. A common mistake is to modify the existing candidate in place. Each of the four possibilities must instead be treated as an independent candidate.

The code deliberately does not use fixed-width integer arithmetic. Python integers can represent the product `x*y` exactly, even when it is much larger than a signed 64-bit integer. This matters during the final verification because the product can occupy more bits than either input.

Negative values of `b` also require care. Python's bitwise operations on negative integers use an infinite two's-complement representation, which gives the same low bits as a fixed-width signed integer. Since every intermediate comparison is masked with `mask`, the relevant low bits are exactly the ones required by the problem.

The exact comparison is performed after every level as well as after the main loop. If the true primes are small, their higher bits are simply zero, so the full expressions can already match before all 64 levels have been processed.

## Worked Examples

### Sample 1

For the sample,

```
a = 1279
b = 1201
```

and the answer is `39 31`.

The binary prefixes of the real pair can be followed from the least significant bit upwards.

| Bit processed | Mask | `p` prefix | `q` prefix | `a & mask` | `b & mask` |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 | 1 |
| 1 | 3 | 3 | 3 | 3 | 1 |
| 2 | 7 | 7 | 7 | 7 | 1 |
| 3 | 15 | 7 | 15 | 15 | 1 |
| 4 | 31 | 7 | 31 | 31 | 17 |
| 5 | 63 | 39 | 31 | 63 | 49 |

At every row, the true prefixes satisfy both output constraints. For example, after six bits the complete values are already `39` and `31`, so the exact expressions give

[
39\cdot31=1209,
]

[
39+31=70,
]

[
39-31=8,
]

and hence

[
1209\oplus70=1279,
]

[
1209\oplus8=1201.
]

The trace demonstrates the central invariant: once a low bit is incompatible with either output, no higher bit can fix it.

### Custom Example 2

Take

```
a = 3
b = -7
```

The expected answer is `2 3`.

| Bit processed | Mask | `p` prefix | `q` prefix | `a & mask` | `b & mask` |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 1 | 1 |
| 1 | 3 | 2 | 3 | 3 | 1 |

The full values are `p=2` and `q=3`. We get

[
pq=6,\quad p+q=5,\quad p-q=-1,
]

so

[
6\oplus5=3
]

and

[
6\oplus(-1)=-7.
]

This example specifically exercises the signed XOR case. The candidate filtering only needs the low bits, where Python's negative integer representation behaves consistently with two's-complement arithmetic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(64C)), expected (O(64)) | Each of 64 bit positions extends every surviving candidate in four ways and checks two expressions. |
| Space | (O(C)) | Only the current and next candidate sets are stored. |

The key parameter is `C`, the number of prefixes surviving at one level. Each candidate has four possible extensions, while the two output bits provide two independent binary constraints. The expected surviving count stays small rather than growing exponentially. With only 64 relevant bits and at most 3000 test cases, this is easily practical in Python.

The memory usage is also tiny because the algorithm never stores a large search tree. It retains only the current frontier of valid prefixes.

## Test Cases

```python
import sys
import io

def solve_case(a, b):
    def f1(x, y):
        return (x * y) ^ (x + y)

    def f2(x, y):
        return (x * y) ^ (x - y)

    candidates = {(0, 0)}

    for bit in range(64):
        mask = (1 << (bit + 1)) - 1
        target_a = a & mask
        target_b = b & mask
        next_candidates = set()
        add = 1 << bit

        for x, y in candidates:
            for bx in (0, 1):
                xx = x + bx * add
                for by in (0, 1):
                    yy = y + by * add

                    if (f1(xx, yy) & mask) != target_a:
                        continue
                    if (f2(xx, yy) & mask) != target_b:
                        continue

                    next_candidates.add((xx, yy))

        candidates = next_candidates

        for x, y in candidates:
            if f1(x, y) == a and f2(x, y) == b:
                return x, y

    for x, y in candidates:
        if f1(x, y) == a and f2(x, y) == b:
            return x, y

    raise ValueError("No solution")

def run(inp: str) -> str:
    data = list(map(int, inp.split()))

    if len(data) >= 3 and len(data) == 1 + 2 * data[0]:
        t = data[0]
        data = data[1:]
    else:
        t = len(data) // 2

    ans = []
    for i in range(t):
        p, q = solve_case(data[2 * i], data[2 * i + 1])
        ans.append(f"{p} {q}")

    return "\n".join(ans)

# Provided sample, as displayed in the statement.
assert run("1279 1201") == "39 31", "sample 1"

# Same sample using the formal T-based input format.
assert run("1\n1279 1201\n") == "39 31", "sample 1 with T"

# Minimum prime pair, including negative p-q.
assert run("3 -7") == "2 3", "minimum-size ordered pair"

# Equal primes.
assert run("0 4") == "2 2", "equal primes"

# Reversed small primes.
assert run("3 7") == "3 2", "reversed ordered pair"

# A larger boundary-style case.
assert run("2147483647 2147483651") == "2147483647 2", "large prime boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 -7` | `2 3` | Handles negative `p-q` and signed XOR. |
| `0 4` | `2 2` | Handles equal primes and zero difference. |
| `3 7` | `3 2` | Confirms that the order of `p` and `q` is preserved. |
| `2147483647 2147483651` | `2147483647 2` | Exercises a large 31-bit prime and many reconstruction levels. |

## Edge Cases

The negative difference case is handled without a special branch. For

```
3 -7
```

the correct pair is `(2,3)`. At the low-bit level, `-7` has the same low bits as its two's-complement representation, and masking with `1`, `3`, `7`, and so on extracts exactly the bits that must match. After reconstructing `2` and `3`, Python evaluates `6 ^ -1` as `-7`, so the final exact check succeeds.

The equal-prime case is

```
0 4
```

with answer `(2,2)`. The algorithm does not assume `p-q` is nonzero. Its second expression simply becomes `4 ^ 0`, which is `4`. The two-bit reconstruction reaches `(2,2)`, and the exact check accepts it.

The reversed-order case is

```
3 7
```

with answer `(3,2)`. Although the product and sum are unchanged if the primes are swapped, the difference changes from `1` to `-1`. Thus the second equation distinguishes the two orientations. The algorithm reconstructs the ordered pair because it always treats the bits of `p` and `q` separately.

The large boundary case is

```
2147483647 2147483651
```

with answer `(2147483647,2)`. Here

[
pq=4294967294,
]

[
p+q=2147483649,
]

[
p-q=2147483645.
]

The first XOR is

[
4294967294\oplus2147483649=2147483647,
]

while the second is

[
4294967294\oplus2147483645=2147483651.
]

The factors require 31 reconstruction bits, so this case checks that the implementation does not accidentally stop after a small fixed number of iterations or confuse the number of processed bits with the magnitude of `a` or `b`.

The central lesson is that the problem looks like integer factorization only at first glance. The actual structure is a constraint system over binary prefixes. Once the two XOR equations are viewed modulo increasing powers of two, the unknown primes can be reconstructed one bit at a time, avoiding any general-purpose factorization algorithm.
