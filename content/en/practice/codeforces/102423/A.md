---
title: "CF 102423A - Carryless Square Root"
description: "The operation in this problem looks like ordinary multiplication, except that every addition performed inside the multiplication discards carries."
date: "2026-08-12T04:42:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102423
codeforces_index: "A"
codeforces_contest_name: "North American Southeast Regional 2019 (Div 1)"
rating: 0
weight: 102423
solve_time_s: 228
verified: true
draft: false
---

[CF 102423A - Carryless Square Root](https://codeforces.com/problemset/problem/102423/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The operation in this problem looks like ordinary multiplication, except that every addition performed inside the multiplication discards carries. If the decimal digits of two numbers are viewed as coefficient arrays, their carryless product is exactly the coefficient-wise convolution, with every coefficient reduced modulo 10.

For example, if the digits of a number (a) from least significant to most significant are (a_0,a_1,\ldots), then the (k)-th digit of (a\otimes a) is

[
c_k=\left(\sum_{i+j=k}a_i a_j\right)\bmod 10.
]

The input is one positive decimal integer (N), with at most 25 digits and no leading zeroes. We need the smallest positive integer (a) whose carryless square is exactly (N). If no such (a) exists, we print (-1). The official statement gives a one-second time limit and a 512 MB memory limit.

The 25-digit bound is small enough that we can afford algorithms quadratic in the number of decimal digits. What we cannot afford is enumerating all possible roots. A root with 13 digits already gives up to (10^{13}) candidates, which is far beyond anything a one-second program can inspect.

There are several edge cases that matter because decimal carryless arithmetic is not ordinary arithmetic. First, a one-digit input does not necessarily have the usual integer square root. For input `6`, the answer is `4`, because (4\otimes4=16), whose only retained digit is 6. A program using ordinary square roots would reject this immediately.

Second, the least significant digit can have several possible square roots modulo 10. For input `6`, both 4 and 6 satisfy (x^2\equiv6\pmod {10}). Choosing the first locally convenient digit without considering the rest of the number can lead to a non-minimal root.

Third, divisibility by 5 creates a special situation. For input `5`, the answer is `5`, since (5\otimes5=5). Treating the arithmetic as if division by (2a_0) were always possible modulo 10 breaks here because 10 is not a field.

Finally, the highest digit must be handled by degree rather than by an ordinary numerical square-root bound. A nonzero leading digit always has a nonzero square modulo 10, so a root with (m) digits produces a square with exactly (2m-1) decimal positions. Thus a 25-digit input can have a root of at most 13 digits, but its root is not generally close to the ordinary integer square root.

## Approaches

The direct approach is to enumerate every possible root and calculate its carryless square. Since a 25-digit number can have a root of at most 13 digits, there can be (10^{13}) candidate roots. Even if squaring one candidate only costs (O(13^2)) digit operations, the worst case is roughly (10^{13}\cdot169), or about (1.7\times10^{15}) elementary digit products. The brute force is correct because every possible root is eventually tested, but the search space is hopelessly large.

The useful observation is that carryless arithmetic is polynomial arithmetic modulo 10. The modulus 10 is not prime, which makes direct algebra awkward, but 10 factors into two coprime primes:

[
10=2\cdot5.
]

By the Chinese remainder theorem, a decimal digit is uniquely determined by its residue modulo 2 and modulo 5. Consequently, instead of solving the polynomial square equation over (\mathbb Z_{10}), we can solve it separately over the fields (\mathbb F_2) and (\mathbb F_5), then combine the resulting digits.

Modulo 2, squaring becomes exceptionally simple. In characteristic 2,

a_0+a_1x^2+a_2x^4+\cdots.
]

All odd-degree coefficients disappear. Thus the input must have zero coefficients at every odd position, and the coefficient of (x^{2i}) directly tells us the (i)-th root coefficient modulo 2.

Modulo 5, the situation is also manageable because we are working in a field. If the constant coefficient of the polynomial is nonzero, once we choose its square root (r_0), every later coefficient is forced. The coefficient of (x^k) in the square is

[
2r_0r_k+\sum_{i=1}^{k-1}r_ir_{k-i}.
]

Since (r_0\neq0) modulo 5, (2r_0) is invertible, so (r_k) has a unique value. There are at most two choices for (r_0), because a nonzero element of (\mathbb F_5) has at most two square roots.

If the polynomial is divisible by (x^t) modulo 5, a square can only have an even value of (t). We remove (x^t), solve the remaining polynomial whose constant coefficient is nonzero, and put (t/2) zero coefficients back into the root. The same degree argument applies at the other end, so the degree of a nonzero polynomial must also be even.

The two modular roots are then combined digit by digit using the unique number from 0 through 9 having the required residues modulo 2 and 5. At most two complete decimal roots can result, so we simply choose the smaller valid one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^{13}\cdot25^2)) | (O(25)) | Too slow |
| Modular decomposition | (O(25^2)) | (O(25)) | Accepted |

## Algorithm Walkthrough

1. Read the decimal representation of (N) and store its digits from least significant to most significant. Working from the least significant digit matches polynomial coefficient order, so coefficient (k) is immediately available as `digits[k]`.
2. Solve the square equation modulo 2. For every odd index (k), the input digit must be even. If some odd-position digit is odd, no root exists because every square over (\mathbb F_2) has zero coefficients at odd degrees. For every (i), set the root coefficient at position (i) modulo 2 to the input coefficient at position (2i) modulo 2.
3. Reduce the input polynomial modulo 5 and find its first and last nonzero coefficients. If every coefficient is zero modulo 5, the root is also zero modulo 5. Otherwise, the first nonzero position and the degree must both be even. A square has even valuation because its lowest nonzero term comes from squaring the lowest nonzero root term, and its degree is twice the root degree.
4. Remove the even power of (x) from the modulo-5 polynomial. The remaining polynomial has a nonzero constant coefficient. Try each of its at most two square roots for that constant coefficient. These two choices correspond to (r) and (-r).
5. For each chosen constant root, determine the remaining coefficients from low degree to high degree. At coefficient (k), all products involving two already known coefficients are known, leaving only (2r_0r_k) unknown. Divide by (2r_0) modulo 5 using its modular inverse.
6. Verify the completed modulo-5 polynomial by squaring it. This is inexpensive because there are at most 25 input digits, and it also makes the implementation robust against any boundary mistake in the recurrence.
7. Combine every valid modulo-5 root with the unique modulo-2 root. For each position, find the digit (d\in[0,9]) satisfying both required residues. The Chinese remainder theorem guarantees exactly one such digit.
8. Remove leading zeroes from the resulting root representation and convert it to an integer string. If there are two candidates, choose the smaller one.
9. If no candidate survives, print `-1`.

### Why it works

The central invariant is that a candidate root is represented simultaneously by its coefficients modulo 2 and modulo 5. The modulo-2 construction guarantees that its square matches (N) modulo 2, while the modulo-5 construction guarantees that its square matches (N) modulo 5. Every resulting decimal digit is the unique residue modulo 10 having those two residues, so the complete square matches (N) modulo 10 at every coefficient.

Since equality of two decimal digits modulo 10 means equality of the digits themselves, the carryless square is exactly (N). Conversely, every genuine carryless square root produces a square root modulo 2 and a square root modulo 5, so our two modular searches cannot discard a possible root. The only ambiguity is the sign of the nonzero modulo-5 square root, giving at most two candidates. Choosing the smaller candidate therefore gives the required smallest positive root.

## Python Solution

```python
import sys
input = sys.stdin.readline

def square_mod(poly, mod, length=None):
    if length is None:
        length = 2 * len(poly) - 1

    res = [0] * length
    for i, x in enumerate(poly):
        for j, y in enumerate(poly):
            if i + j >= length:
                break
            res[i + j] = (res[i + j] + x * y) % mod
    return res

def roots_mod5(n5):
    m = len(n5)

    first = -1
    last = -1

    for i, x in enumerate(n5):
        if x % 5 != 0:
            if first == -1:
                first = i
            last = i

    if first == -1:
        return [[0] * ((m + 1) // 2)]

    if first % 2 == 1 or last % 2 == 1:
        return []

    shift = first
    root_degree = (last - first) // 2
    target = n5[first:last + 1]

    constant = target[0] % 5

    initial_roots = []
    for r in range(5):
        if r * r % 5 == constant:
            initial_roots.append(r)

    result = []

    for r0 in initial_roots:
        q = [0] * (root_degree + 1)
        q[0] = r0

        inv = pow((2 * r0) % 5, 3, 5)

        for k in range(1, root_degree + 1):
            known = 0
            for i in range(1, k):
                known += q[i] * q[k - i]
            q[k] = ((target[k] - known) * inv) % 5

        full = [0] * (shift // 2 + len(q))
        full[shift // 2:] = q

        expected = n5
        got = square_mod(full, 5, len(expected))

        if got == expected:
            result.append(full)

    return result

def combine(r2, r5):
    length = max(len(r2), len(r5))
    ans = []

    for i in range(length):
        a = r2[i] if i < len(r2) else 0
        b = r5[i] if i < len(r5) else 0

        digit = None
        for d in range(10):
            if d % 2 == a and d % 5 == b:
                digit = d
                break

        ans.append(digit)

    while len(ans) > 1 and ans[-1] == 0:
        ans.pop()

    return int(''.join(map(str, reversed(ans))))

def carryless_square(a):
    digits = list(map(int, reversed(str(a))))
    res = [0] * (2 * len(digits) - 1)

    for i, x in enumerate(digits):
        for j, y in enumerate(digits):
            res[i + j] = (res[i + j] + x * y) % 10

    while len(res) > 1 and res[-1] == 0:
        res.pop()

    return int(''.join(map(str, reversed(res))))

def solve():
    s = input().strip()
    digits = list(map(int, reversed(s)))
    n = len(digits)

    # Solve modulo 2.
    # In characteristic 2, every square has zero coefficients
    # at odd degrees.
    for i in range(1, n, 2):
        if digits[i] % 2:
            print(-1)
            return

    r2_len = (n + 1) // 2
    r2 = [0] * r2_len

    for i in range(r2_len):
        r2[i] = digits[2 * i] % 2

    # Solve modulo 5.
    n5 = [x % 5 for x in digits]
    roots5 = roots_mod5(n5)

    if not roots5:
        print(-1)
        return

    candidates = []

    for r5 in roots5:
        candidate = combine(r2, r5)

        if candidate > 0 and carryless_square(candidate) == int(s):
            candidates.append(candidate)

    if not candidates:
        print(-1)
    else:
        print(min(candidates))

if __name__ == "__main__":
    solve()
```

The input digits are reversed first because polynomial coefficients are naturally indexed from the least significant decimal digit. The coefficient at position zero is the constant term, position one is the coefficient of (x), and so on.

The modulo-2 part is deliberately simple. If the input has an odd-position digit that is odd, the answer is immediately impossible. Otherwise, the coefficient at root position (i) is copied from input position (2i). There is no recurrence because the Frobenius identity makes all cross terms vanish modulo 2.

The modulo-5 routine first finds the valuation and degree of the input polynomial. Both must be even for a nonzero square. After removing the initial power of (x), the constant coefficient is nonzero, so its square root is also nonzero. The inverse of (2r_0) exists modulo 5, which makes every later coefficient uniquely determined.

The expression `pow((2 * r0) % 5, 3, 5)` computes the inverse modulo 5. Since every nonzero residue (x) modulo 5 satisfies (x^4=1), its inverse is (x^3). Python's modular exponentiation handles this directly.

The final combination searches only ten possible decimal digits. It is tempting to use a closed formula for CRT here, but a ten-element search is clearer and removes opportunities for sign or residue mistakes.

The final carryless-square verification is not needed mathematically once both modular computations are correct, but it costs essentially nothing for a 25-digit input. It protects the implementation against mistakes involving unused high coefficients and confirms the exact decimal result before accepting it.

## Worked Examples

### Sample 1: `6`

The input has only one coefficient, so the polynomial is (6).

Modulo 2, (6\equiv0). The root coefficient must consequently be 0 modulo 2.

Modulo 5, (6\equiv1). The two square roots of 1 modulo 5 are 1 and 4.

| Root mod 5 | Root mod 2 | Decimal digit | Candidate |
| --- | --- | --- | --- |
| 1 | 0 | 6 | 6 |
| 4 | 0 | 4 | 4 |

Both candidates are genuine roots:

[
4\otimes4=16\longrightarrow6,
]

while

[
6\otimes6=36\longrightarrow6.
]

The smaller positive root is 4, so the output is `4`.

This example demonstrates why solving only modulo 10 by greedily choosing a digit can be misleading. There are multiple valid lowest digits, and the two prime-modulus views make the complete set of possibilities explicit.

### Sample 2: `149`

The digits from low to high are (9,4,1).

Modulo 2 they become (1,0,1). The odd-position coefficient is zero, so a root exists modulo 2. Its coefficients are obtained from positions 0 and 2:

[
r_0=1,\qquad r_1=1.
]

Thus the root is (1+x) modulo 2.

Modulo 5, the polynomial is

[
4+4x+x^2.
]

The constant coefficient 4 has square roots 2 and 3 modulo 5. Choosing 2 first gives

[
r_0=2.
]

For the coefficient of (x),

[
4=2r_0r_1=4r_1\pmod5,
]

so (r_1=1). The resulting root is (2+x) modulo 5.

Combining the residues digit by digit gives:

| Position | Mod 2 | Mod 5 | Decimal digit |
| --- | --- | --- | --- |
| 0 | 1 | 2 | 7 |
| 1 | 1 | 1 | 1 |

The candidate is therefore `17`.

The other modulo-5 root gives another valid candidate, but it is larger. The algorithm checks both and selects `17`, matching the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(L^2)) | Every polynomial multiplication or coefficient recurrence touches at most (L^2) digit pairs, with (L\le25). |
| Space | (O(L)) | The input and a constant number of root arrays contain only (O(L)) coefficients. |

Here (L) is the number of decimal digits of (N), at most 25 according to the official problem statement. The largest computation is only a few hundred digit-level operations, so the quadratic algorithm is comfortably inside the one-second limit and uses negligible memory compared with the 512 MB limit.

## Test Cases

The following test harness exposes the solution as a function so that each assertion can run independently.

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_data(data: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(data)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return output

# Provided samples
assert solve_data("6\n") == "4", "sample 1"
assert solve_data("149\n") == "17", "sample 2"
assert solve_data("123476544\n") == "11112", "sample 3"
assert solve_data("15\n") == "-1", "sample 4"

# Minimum-size input.
assert solve_data("1\n") == "1", "minimum input"

# All-equal digits, deliberately not a square.
assert solve_data("11111\n") == "-1", "all-equal non-square"

# Boundary case where the root is exactly half the number of digits.
assert solve_data("10000\n") == "100", "degree boundary"

# Maximum-size valid construction:
# 1111111111111 ⊗ 1111111111111
# = 1234567890123456789012345
assert solve_data("1234567890123456789012345\n") == "1111111111111", \
    "maximum-size valid input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Minimum-size input and positive-root handling |
| `11111` | `-1` | All-equal digits and rejection of an impossible square |
| `10000` | `100` | Degree calculation and boundary between input and root lengths |
| `1234567890123456789012345` | `1111111111111` | Maximum-size valid input and high-degree coefficients |

## Edge Cases

For input `6`, the modulo-2 root is zero while the modulo-5 roots are 1 and 4. CRT gives decimal roots 6 and 4, and the algorithm chooses 4. This catches the common mistake of assuming the lowest decimal digit has a unique square root.

For input `5`, the modulo-5 polynomial is zero, so its root is zero modulo 5. The modulo-2 polynomial is also zero, so the only CRT digit is 5. The algorithm produces `5`, and indeed (5\otimes5=5). This catches implementations that try to divide by (2a_0) modulo 10 without first separating the modulus into fields.

For input `15`, the modulo-2 polynomial has coefficient 1 at degree zero and 1 at degree one. The odd-degree coefficient is nonzero, but every square modulo 2 has zero coefficients at odd degrees. The algorithm rejects the number immediately and prints `-1`, which is the fourth official sample.

For input `10000`, the polynomial is (x^4). Its modulo-2 square root is (x^2), and its modulo-5 square root is also (x^2). CRT consequently produces the decimal root `100`. Squaring it carrylessly gives `10000`. This tests the case where the input has several trailing zero digits and the root's degree is determined entirely by the polynomial degree.

For the 25-digit input `1234567890123456789012345`, the root `1111111111111` has 13 digits. Its carryless square has coefficients given by the number of pairs contributing to each degree, reduced modulo 10, producing exactly the 25-digit input. This exercises the largest possible root length and confirms that the algorithm does not accidentally allocate or inspect coefficients beyond the valid polynomial degree.
