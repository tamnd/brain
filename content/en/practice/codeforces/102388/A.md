---
title: "CF 102388A - Strange Base"
description: "We need to print the unique base-(phi) representation of a positive integer (n), where (phi=(1+sqrt5)/2). A digit is either (0) or (1), and two neighboring positions may not both contain (1)."
date: "2026-08-14T13:47:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102388
codeforces_index: "A"
codeforces_contest_name: "SUFE ICPC Team Formation Test"
rating: 0
weight: 102388
solve_time_s: 242
verified: false
draft: false
---

[CF 102388A - Strange Base](https://codeforces.com/problemset/problem/102388/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We need to print the unique base-(\phi) representation of a positive integer (n), where (\phi=(1+\sqrt5)/2). A digit is either (0) or (1), and two neighboring positions may not both contain (1). Unlike an ordinary positional system, powers with negative exponents are allowed, so the decimal point may be followed by several digits.

For example, (2) cannot be represented using only non-negative powers. The largest usable power is (\phi), but (\phi) is smaller than (2), and the exact correction is (\phi^{-2}):

[
2=\phi+\phi^{-2},
]

so the answer is `10.01`.

The largest input is only (10^5), and there are at most (10) test cases. This rules out algorithms that enumerate a large number of possible digit strings. The useful representation has only (O(\log n)) relevant positions, so an algorithm that processes each possible exponent once is easily fast enough for the one-second limit.

There are three edge cases that a straightforward implementation can mishandle. For (n=1), the answer is simply `1`, with no fractional part. An implementation that always prints a decimal point would produce a different string. For (n=2), the answer is `10.01`, so restricting the search to non-negative powers cannot work. For (n=3), the answer is `100.01`, and the fractional digit is again necessary. Finally, floating-point subtraction can leave a tiny nonzero remainder after the true remainder is zero, causing a careless implementation to emit spurious trailing digits.

The last issue is especially relevant here because (\phi) is irrational. We will avoid floating-point arithmetic completely.

## Approaches

A brute-force approach can enumerate every binary digit string satisfying the no-adjacent-ones condition, evaluate its value, and look for the string representing (n). This is correct because the problem guarantees that the required representation exists and is unique. The problem is the number of candidates. The maximum positive exponent for (n\le100000) is (25), while the required fractional part can extend to about (26) positions, giving roughly (50) relevant positions. Even before considering the fixed leading and trailing digits, the number of binary strings of length (50) with no adjacent ones is (F_{52}=32,951,280,099). Evaluating those candidates is far beyond the time limit.

The useful observation is that this representation has the same greedy structure as ordinary positional systems, despite the base being irrational. Suppose the current positive remainder is (r), and choose the largest exponent (k) satisfying

[
\phi^k\le r.
]

After subtracting (\phi^k), the new remainder satisfies

[
r-\phi^k<\phi^{k+1}-\phi^k=\phi^{k-1}.
]

Consequently, the next digit at position (k-1) must be zero. This is exactly the restriction required by the canonical representation. We can keep taking the largest power that fits until the remainder becomes zero.

The brute force works because it searches all possible valid digit strings. It fails because there are exponentially many of them. The greedy observation lets us make a single decision at every exponent instead, reducing the problem to (O(\log n)) positions.

The remaining difficulty is comparison. We cannot safely store (\phi^k) as a floating-point number and repeatedly subtract it, because eventually the remainder can be extremely small. Instead, every power of (\phi) can be written exactly as

[
\phi^k=a+b\phi
]

for integers (a,b). The identity

[
\phi^2=\phi+1
]

lets us update these integer pairs exactly. We can also compare two such expressions using only integer arithmetic, because the sign of (a+b\phi) can be determined by comparing integers after substituting (\phi=(1+\sqrt5)/2).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential, (\Theta(F_L)) candidates for (L) positions | (O(L)) | Too slow |
| Optimal greedy | (O(\log n)) exponent positions | (O(\log n)) | Accepted |

## Algorithm Walkthrough

1. Represent every power of (\phi) as an integer pair ((a,b)) meaning (a+b\phi). Start with (\phi^0=1), represented by ((1,0)). Multiplying (a+b\phi) by (\phi) gives
[
(a+b\phi)\phi=b+(a+b)\phi,
]
so increasing the exponent changes ((a,b)) into ((b,a+b)).

For negative powers, divide by (\phi). Since (\phi^{-1}=\phi-1), multiplying by (\phi^{-1}) changes ((a,b)) into ((b-a,a)). Thus all required powers can be generated using integers only.
2. Find the largest exponent (q) for which (\phi^q\le n). Since (n\le100000), (q) is at most (25). The greedy representation must start at this position because using any larger power would already exceed the number.
3. Set the current remainder to (n), represented by the pair ((n,0)). Then inspect exponents from (q) downward.
4. At exponent (k), test whether the current remainder is at least (\phi^k). If it is, put digit (1) at position (k) and subtract the corresponding pair from the remainder. Otherwise put digit (0).

Choosing the largest fitting power is the greedy decision. If (\phi^k\le r<\phi^{k+1}), then after subtraction the new remainder is smaller than (\phi^{k-1}), so the immediately following position cannot be selected.
5. Continue through the negative exponents until the remainder becomes exactly the zero pair. For (n\le100000), going down to exponent (-30) is more than enough. A short bound explains why. If the smallest fractional exponent is (-m), its fractional tail is positive and smaller than
[
\phi^{-m}+\phi^{-m-2}+\phi^{-m-4}+\cdots=\phi^{1-m}.
]
The tail is a nonzero algebraic integer (A+B\phi), so its norm (A^2+AB-B^2) is a nonzero integer. Its conjugate has absolute value less than (n+3<100003), so the tail is larger than (1/100003). If (m\ge27), then (\phi^{1-m}=\phi^{-26}<1/100003), a contradiction. Thus exponent (-26) is already sufficient.
6. Convert the selected digits into a string. Positions from (q) through (0) form the integer part. If a negative position was used, place a decimal point after position (0), then append positions (-1,-2,\ldots,p). Leading and trailing unnecessary zeroes are omitted.

**Why it works.** At every iteration, the remainder is exactly the value still missing from the answer. We select (\phi^k) precisely when it does not exceed that remainder, so the new remainder remains nonnegative. Because the previous remainder is smaller than (\phi^{k+1}), subtracting (\phi^k) leaves less than (\phi^{k-1}), which forbids the next exponent from being selected. Thus every generated digit is valid and no adjacent digits are (1). When the remainder reaches zero, the selected powers sum exactly to (n). The problem states that a valid representation with these restrictions is unique, so the greedy representation is the required one.

## Python Solution

```python
import sys
input = sys.stdin.readline

MIN_K = -30
MAX_K = 30

def nonnegative(a, b):
    """Return whether a + b*phi >= 0, using integer arithmetic only."""
    if b == 0:
        return a >= 0

    if b > 0:
        if a >= 0:
            return True

        # a + b*phi >= 0
        # b*sqrt(5) >= -2*a - b
        c = -a
        d = 2 * c - b

        if d <= 0:
            return True

        return 5 * b * b >= d * d

    # b < 0
    c = -b

    if a < 0:
        return False

    # a >= c*phi
    # 2*a - c >= c*sqrt(5)
    d = 2 * a - c

    if d < 0:
        return False

    return d * d >= 5 * c * c

def build_powers():
    powers = {0: (1, 0)}

    # Positive exponents.
    a, b = 1, 0
    for k in range(1, MAX_K + 1):
        a, b = b, a + b
        powers[k] = (a, b)

    # Negative exponents.
    a, b = 1, 0
    for k in range(-1, MIN_K - 1, -1):
        a, b = b - a, a
        powers[k] = (a, b)

    return powers

powers = build_powers()

def encode(n):
    # Find the largest q with phi^q <= n.
    q = 0
    for k in range(MAX_K, -1, -1):
        a, b = powers[k]
        if nonnegative(n - a, -b):
            q = k
            break

    rem_a, rem_b = n, 0
    digits = {}

    for k in range(q, MIN_K - 1, -1):
        a, b = powers[k]

        if nonnegative(rem_a - a, rem_b - b):
            digits[k] = '1'
            rem_a -= a
            rem_b -= b

            if rem_a == 0 and rem_b == 0:
                last = k
                break
        else:
            digits[k] = '0'
    else:
        raise AssertionError("The guaranteed finite representation was not found")

    if last >= 0:
        left = ''.join(digits[k] for k in range(q, 0, -1))
        left += digits[0]

        if last >= 0:
            return left

    left = ''.join(digits[k] for k in range(q, -1, -1))
    right = ''.join(digits[k] for k in range(-1, last - 1, -1))

    return left + '.' + right

def main():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        out.append(encode(n))

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    main()
```

The `powers` dictionary stores exact algebraic values. For example, exponent (2) is `(1, 1)` because (\phi^2=1+\phi), while exponent (-2) is `(2, -1)` because (\phi^{-2}=2-\phi).

The `nonnegative` function is the key numerical detail. For (a+b\phi), write

[
2(a+b\phi)=(2a+b)+b\sqrt5.
]

If the two terms already have the same sign, the answer is immediate. Otherwise, both sides are nonnegative and we can square them, replacing an irrational comparison by an integer comparison involving (5b^2). There is no rounding anywhere in the conversion.

The positive and negative power generation use the two transformations derived from (\phi^2=\phi+1). Python integers have arbitrary precision, so there is no overflow concern.

The loop goes downward because the greedy rule requires the largest usable exponent first. Once a power is selected, the remainder is updated immediately before considering the next position. This ordering is what gives the no-adjacent-ones property.

The formatting code treats exponent (0) as the last digit before the decimal point. If the representation has no negative exponent, no decimal point is printed, which handles (n=1) correctly.

## Worked Examples

### Example 1: (n=2)

The largest power not exceeding (2) is (\phi^1). The relevant exact values are (\phi^1=\phi), (\phi^0=1), (\phi^{-1}=\phi-1), and (\phi^{-2}=2-\phi).

| Exponent (k) | Current remainder | Compare | Digit | New remainder |
| --- | --- | --- | --- | --- |
| 1 | (2) | (2\ge\phi) | 1 | (2-\phi=\phi^{-2}) |
| 0 | (2-\phi) | (2-\phi<1) | 0 | (2-\phi) |
| -1 | (2-\phi) | (2-\phi<\phi^{-1}) | 0 | (2-\phi) |
| -2 | (2-\phi) | (2-\phi=\phi^{-2}) | 1 | (0) |

The digits are `10.01`. The trace demonstrates why fractional powers are necessary even for a small integer. It also shows the advantage of exact arithmetic: after the final subtraction the remainder is literally the integer pair `(0, 0)`, not a floating-point approximation of zero.

### Example 2: (n=4)

The largest usable power is (\phi^2), because (\phi^2=1+\phi<4) while (\phi^3>4).

| Exponent (k) | Current remainder | Compare | Digit | New remainder |
| --- | --- | --- | --- | --- |
| 2 | (4) | (4\ge\phi^2) | 1 | (4-\phi^2=3-\phi) |
| 1 | (3-\phi) | (3-\phi<\phi) | 0 | (3-\phi) |
| 0 | (3-\phi) | (3-\phi\ge1) | 1 | (2-\phi=\phi^{-2}) |
| -1 | (2-\phi) | (2-\phi<\phi^{-1}) | 0 | (2-\phi) |
| -2 | (2-\phi) | (2-\phi=\phi^{-2}) | 1 | (0) |

The resulting representation is `101.01`. After selecting exponent (2), the next exponent (1) is automatically impossible. After selecting exponent (0), exponent (-1) is again impossible. This is the greedy invariant appearing directly in the trace.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\log n)) | There are (O(\log n)) relevant positive and negative exponent positions, and every position is processed once. |
| Space | (O(\log n)) | The power table and digit array contain only (O(\log n)) entries. |

For (n\le100000), the largest positive exponent is only (25), and the fractional part needs fewer than (30) positions. With at most (10) test cases, the algorithm performs only a few hundred integer operations per input file. It is comfortably inside both the one-second time limit and the 256 MB memory limit.

## Test Cases

```python
import sys
import io

MIN_K = -30
MAX_K = 30

def nonnegative(a, b):
    if b == 0:
        return a >= 0

    if b > 0:
        if a >= 0:
            return True

        c = -a
        d = 2 * c - b

        if d <= 0:
            return True

        return 5 * b * b >= d * d

    c = -b

    if a < 0:
        return False

    d = 2 * a - c

    if d < 0:
        return False

    return d * d >= 5 * c * c

def build_powers():
    powers = {0: (1, 0)}

    a, b = 1, 0
    for k in range(1, MAX_K + 1):
        a, b = b, a + b
        powers[k] = (a, b)

    a, b = 1, 0
    for k in range(-1, MIN_K - 1, -1):
        a, b = b - a, a
        powers[k] = (a, b)

    return powers

powers = build_powers()

def encode(n):
    q = 0

    for k in range(MAX_K, -1, -1):
        a, b = powers[k]
        if nonnegative(n - a, -b):
            q = k
            break

    rem_a, rem_b = n, 0
    digits = {}

    for k in range(q, MIN_K - 1, -1):
        a, b = powers[k]

        if nonnegative(rem_a - a, rem_b - b):
            digits[k] = '1'
            rem_a -= a
            rem_b -= b

            if rem_a == 0 and rem_b == 0:
                last = k
                break
        else:
            digits[k] = '0'
    else:
        raise AssertionError("representation did not terminate")

    left = ''.join(digits[k] for k in range(q, -1, -1))

    if last >= 0:
        return left

    right = ''.join(digits[k] for k in range(-1, last - 1, -1))
    return left + '.' + right

def solve_data(inp):
    data = list(map(int, inp.split()))
    t = data[0]

    ans = []
    for i in range(1, t + 1):
        ans.append(encode(data[i]))

    return '\n'.join(ans) + '\n'

def run(inp: str) -> str:
    return solve_data(inp)

sample = """\
5
1
2
3
100000
123
"""

expected_sample = """\
1
10.01
100.01
101010001010100000100000.101000101000000010000001
10000000000.0000000001
"""

assert run(sample) == expected_sample, "sample"

assert run("""\
1
1
""") == "1\n", "minimum input"

assert run("""\
3
2
3
4
""") == """\
10.01
100.01
101.01
""", "small boundary cases"

assert run("""\
3
5
5
5
""") == """\
1000.1001
1000.1001
1000.1001
""", "repeated equal values"

assert run("""\
1
100000
""") == "101010001010100000100000.101000101000000010000001\n", "maximum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Minimum input and omission of an unnecessary decimal point |
| `2`, `3`, `4` | `10.01`, `100.01`, `101.01` | Fractional powers and greedy boundary decisions |
| `5`, `5`, `5` | `1000.1001` three times | Multiple test cases with identical values |
| `100000` | `101010001010100000100000.101000101000000010000001` | Maximum input and the full range of positive and negative positions |

## Edge Cases

For (n=1), the input is

```
1
```

The largest usable power is (\phi^0=1). The first greedy step selects it, leaving the exact remainder zero. No negative exponent is visited, so the output is simply `1`. A formatter that blindly inserts `.` would incorrectly produce something such as `1.`.

For (n=2), the input is

```
2
```

The first selected power is (\phi^1), leaving (2-\phi=\phi^{-2}). Neither (\phi^0) nor (\phi^{-1}) fits, and (\phi^{-2}) fits exactly. The digits are `10.01`. This catches implementations that assume every integer has a representation using only non-negative powers.

For (n=3), the input is

```
3
```

The first selected power is (\phi^2), leaving (3-\phi^2=2-\phi=\phi^{-2}). Thus the result is `100.01`. The same fractional correction appears as for (2), but the integer part has shifted one position to the left. This is a useful check for exponent indexing around the decimal point.

For (n=4), the input is

```
4
```

The greedy choices are (\phi^2), then (1), then (\phi^{-2}). The powers (\phi^1) and (\phi^{-1}) are rejected because they would exceed the current remainder. The result is `101.01`. This case catches an off-by-one error in the greedy comparison and verifies that selected digits never become adjacent.

For (n=100000), the representation reaches both many positive and many negative positions. The exact pair arithmetic continues to work without any special handling for the tiny fractional powers. The remainder eventually becomes exactly `(0, 0)`, producing the sample output without relying on an epsilon or floating-point rounding.
