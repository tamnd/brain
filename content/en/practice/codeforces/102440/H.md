---
title: "CF 102440H - Policeman from Rublevka"
description: "We have an integer array (a1,dots,an), where each element describes the difficulty of one solved crime. Lesha wants to remove one existing element (ap) and insert two new integer values (q) and (r). The resulting array has (n+1) elements."
date: "2026-08-09T13:34:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102440
codeforces_index: "H"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Junior"
rating: 0
weight: 102440
solve_time_s: 415
verified: true
draft: false
---

[CF 102440H - Policeman from Rublevka](https://codeforces.com/problemset/problem/102440/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an integer array (a_1,\dots,a_n), where each element describes the difficulty of one solved crime. Lesha wants to remove one existing element (a_p) and insert two new integer values (q) and (r). The resulting array has (n+1) elements.

The checker does not compare the arrays directly. It only compares their arithmetic mean and variance. We need to find an index (p) and two integers (q,r) such that both statistics remain exactly the same. If no such modification exists, we print `Impossible`.

Let

[
S=\sum_{i=1}^n a_i
]

and

[
Q=\sum_{i=1}^n a_i^2.
]

The original mean is (m=S/n), and the variance can be rewritten as

[
D=\frac{Q}{n}-m^2.
]

This form is much more useful than expanding every ((a_i-m)^2), because it reduces the problem to preserving the first two power sums.

The array contains up to (10^5) elements, so an algorithm that examines a quadratic number of pairs is not viable. With a roughly one-second contest limit, the intended solution needs to be linear or close to linear. The values themselves are bounded by (10^5), but the sum of up to (10^5) such values can reach (10^{10}), and the sum of squares can reach (10^{15}). Python integers handle these values safely, while fixed-width languages need 64-bit integers.

There are several edge cases that a careless implementation can miss. If (n=1), the only element can always be replaced by two copies of itself. For example, for `1 / 5`, the correct answer is `Possible`, with removal of the first element and insertion of `5 5`. A method that assumes the array has at least two elements may incorrectly reject it.

A second issue is a non-integer mean. Consider

```
2
0 1
```

The original mean is (1/2). After the operation there are three integers, so their sum is an integer and their mean cannot be (1/2), because three times (1/2) is not an integer. Thus the answer is `Impossible`. A solution using floating point and approximate comparisons can easily obscure this exact impossibility.

A third issue is that preserving the mean alone is insufficient. For

```
3
0 0 6
```

the mean is (2), but simply choosing two integers whose sum compensates for a removed element does not guarantee the variance will survive. The second moment must also be preserved.

Finally, even when the discriminant is a perfect square, its parity matters. If (q+r=s) and (q-r=d), then

[
q=\frac{s+d}{2},\qquad r=\frac{s-d}{2}.
]

Both values are integers only when (s) and (d) have the same parity. Checking only whether the discriminant is a square is not enough.

## Approaches

A direct brute-force approach could try every position (p), remove (a_p), and then enumerate possible values for one of the new elements. Once (p) and (q) are fixed, the required value of (r) is determined by the mean, so each candidate can be checked by recomputing the two statistics. The idea is correct because every possible replacement is eventually considered.

The problem is the number of candidates. The original values have magnitude at most (10^5), while the replacement values can be somewhat larger because the new array has one additional element. Even restricting the search to a safe interval around (10^5) would leave on the order of (10^5) candidates for each of (10^5) positions, or about (10^{10}) checks. Recomputing statistics inside that loop would make it even worse.

The brute-force works because the statistics impose strong algebraic restrictions, but it fails because it does not exploit them early enough. The key observation is that equality of the mean immediately fixes the sum (q+r), while equality of the variance, together with the equal mean, fixes (q^2+r^2). Once both the sum and sum of squares are known, (q) and (r) are the two roots of a quadratic equation. There is no need to search for them.

Suppose we remove (x=a_p). Let the original mean be (m), and let

[
T=\frac{Q}{n}.
]

Preserving the mean gives

[
\frac{S-x+q+r}{n+1}=m.
]

Since (S=nm), this simplifies to

[
q+r=x+m.
]

Because (x,q,r) are integers, this already tells us that (m) must be an integer. If the original mean is not an integer, the answer is immediately impossible.

Preserving the variance is equivalent to preserving the second raw moment (Q/n), because the means are already equal. Hence

[
\frac{Q-x^2+q^2+r^2}{n+1}=\frac{Q}{n},
]

which gives

[
q^2+r^2=x^2+\frac{Q}{n}.
]

So (Q) must also be divisible by (n), because the left side and (x^2) are integers.

Now let

[
s=q+r=x+m.
]

Using

[
(q-r)^2=2(q^2+r^2)-(q+r)^2,
]

we obtain

2\left(x^2+\frac Qn\right)-(x+m)^2.
]

For every possible removed element (x), this value can be calculated in constant time. If it is non-negative and a perfect square (d^2), and (d) has the same parity as (x+m), then

[
q=\frac{x+m+d}{2},
\qquad
r=\frac{x+m-d}{2}
]

are integers and form a valid replacement.

Thus the entire problem becomes a single scan through the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n\cdot V)), about (10^{10}) candidates in the worst case | (O(1)) | Too slow |
| Optimal | (O(n)) | (O(n)) for the input array | Accepted |

## Algorithm Walkthrough

1. Read the array and compute

[
S=\sum a_i,\qquad Q=\sum a_i^2.
]

These two quantities are sufficient because the mean and variance can both be expressed through the first two power sums.

1. Check whether (S) is divisible by (n). If it is not, print `Impossible`.

The reason is especially simple. The replacement values are integers, so (q+r) is an integer. From preservation of the mean,

[
q+r=x+\frac Sn.
]

Since (x) is an integer, (S/n) must also be an integer.

1. Set

[
m=\frac Sn.
]

Then check whether (Q) is divisible by (n). If not, print `Impossible`.

For any removed (x),

[
q^2+r^2=x^2+\frac Qn.
]

The left side and (x^2) are integers, so (Q/n) must be an integer.

1. Set

[
T=\frac Qn.
]

Scan every array element (x=a_i) as a possible element to remove.

1. For the current (x), calculate

[
s=x+m
]

and

[
d^2=2(x^2+T)-s^2.
]

The value (s) is forced by the mean. The value (d^2) is forced by the second moment.

1. If (d^2<0), this (x) cannot be removed. Otherwise compute the integer square root (d=\lfloor\sqrt{d^2}\rfloor) and check whether (d^2=d\cdot d).

A negative discriminant means no real values (q,r) exist. A non-square discriminant means the two roots are not separated by an integer difference.

1. Check that (s) and (d) have the same parity.

If they do not, the formulas

[
q=\frac{s+d}{2},\qquad r=\frac{s-d}{2}
]

would produce half-integers, which are forbidden.

1. Construct

[
q=\frac{s+d}{2},\qquad r=\frac{s-d}{2}
]

and output the index (i+1), followed by (q,r).

The order of (q) and (r) does not matter, since they contribute symmetrically to both required statistics.

1. If the scan finishes without finding a valid element, print `Impossible`.

### Why it works

For every candidate (x), the algorithm derives the only possible sum (q+r) from equality of the means and the only possible value of (q^2+r^2) from equality of the second moments. Consequently, any valid pair (q,r) must satisfy the computed value of ((q-r)^2). The square and parity checks are exactly the conditions required for two integers with that sum and difference to exist. Thus every pair produced by the algorithm preserves both the mean and the variance. Conversely, any valid replacement must pass all of these checks, so scanning every possible removed element guarantees that a valid solution is found whenever one exists.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    total = sum(a)
    squares = sum(x * x for x in a)

    # The new mean is the old mean.
    # Since q + r and a[p] are integers, total / n must be integer.
    if total % n != 0:
        print("Impossible")
        return

    mean = total // n

    # q^2 + r^2 = a[p]^2 + squares / n,
    # so squares / n must also be integer.
    if squares % n != 0:
        print("Impossible")
        return

    second_moment = squares // n

    for i, x in enumerate(a):
        s = x + mean

        # d^2 = (q-r)^2
        d2 = 2 * (x * x + second_moment) - s * s

        if d2 < 0:
            continue

        d = math.isqrt(d2)

        if d * d != d2:
            continue

        if (s - d) % 2 != 0:
            continue

        q = (s + d) // 2
        r = (s - d) // 2

        print("Possible")
        print(i + 1, q, r)
        return

    print("Impossible")

if __name__ == "__main__":
    solve()
```

The first two sums are computed once. The variable `total` represents the first power sum, while `squares` represents the second power sum. Both can be large, so the calculation is done with Python integers rather than floating point.

The divisibility checks deliberately happen before the main loop. If `total % n != 0`, no removed element can work because every candidate requires (q+r=x+m). If `squares % n != 0`, no candidate can work because (q^2+r^2=x^2+Q/n).

Inside the loop, `s` is the forced value of (q+r). The expression `d2` is the forced value of ((q-r)^2). Using `math.isqrt` avoids floating-point precision problems when checking whether a potentially large integer is a perfect square.

The parity test uses `(s - d) % 2`. Checking either `s-d` or `s+d` is sufficient because they have the same parity. Once the check succeeds, integer division produces the two required replacement values.

The output index is `i + 1`, because Python arrays are zero-indexed while the problem numbers crimes starting from one.

## Worked Examples

### Sample 1

The input is

```
11
-5 -4 -3 -2 -1 0 1 2 3 4 5
```

The important global values are

[
S=0,\qquad Q=110,
]

so

[
m=0,\qquad T=10.
]

The scan behaves as follows.

| Index | (x) | (s=x+m) | (d^2) | Result |
| --- | --- | --- | --- | --- |
| 1 | -5 | -5 | 45 | Not a square |
| 2 | -4 | -4 | 36 | Valid, (d=6) |

For (x=-4),

[
q+r=-4
]

and

[
q-r=6.
]

Hence

[
q=1,\qquad r=-5.
]

The resulting array is obtained by replacing (-4) with (1,-5). Its sum is still (0), and its sum of squares becomes

[
110-16+1+25=120.
]

There are now (12) elements, so the second moment is (120/12=10), exactly the original value.

The output is therefore

```
Possible
2 1 -5
```

This trace demonstrates the central invariant: after removing (x), both the new sum and the new sum of squares are completely determined.

### Constructed Example 2

Consider

```
1
5
```

Here

[
S=5,\qquad Q=25,
]

so

[
m=5,\qquad T=25.
]

There is only one possible element to remove.

| Index | (x) | (s=x+m) | (d^2) | (d) | (q,r) |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 10 | 0 | 0 | 5, 5 |

The resulting array is `[5, 5]`. Its mean remains (5), and its variance remains zero.

The output can be

```
Possible
1 5 5
```

This case exercises the minimum value of (n) and confirms that the discriminant is allowed to be zero. The two inserted values can be identical.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | The sums are computed in one pass and every array element is tested once. |
| Space | (O(n)) | The input array is stored so that the selected crime value and its index can be inspected. |

For (n\le 10^5), the algorithm performs only a constant amount of integer arithmetic per element. There is no nested search over replacement values and no floating-point computation, so it comfortably fits the intended limits.

## Test Cases

The output of a valid solution is not unique, so the tests below validate the semantic conditions rather than requiring one exact valid triple. The helper reconstructs the resulting array and checks that its mean and variance match the original exactly.

```python
import sys
import io
import math

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    total = sum(a)
    squares = sum(x * x for x in a)

    if total % n != 0 or squares % n != 0:
        ans = "Impossible\n"
        sys.stdin = old_stdin
        return ans

    mean = total // n
    second_moment = squares // n

    for i, x in enumerate(a):
        s = x + mean
        d2 = 2 * (x * x + second_moment) - s * s

        if d2 < 0:
            continue

        d = math.isqrt(d2)

        if d * d != d2:
            continue

        if (s - d) % 2 != 0:
            continue

        q = (s + d) // 2
        r = (s - d) // 2

        ans = f"Possible\n{i + 1} {q} {r}\n"
        sys.stdin = old_stdin
        return ans

    sys.stdin = old_stdin
    return "Impossible\n"

def validate(inp: str, out: str) -> bool:
    lines = out.strip().splitlines()

    n, *rest = inp.strip().splitlines()
    n = int(n)
    a = list(map(int, rest[0].split()))

    if lines[0] == "Impossible":
        # Independently check whether any solution exists by using
        # the same necessary-and-sufficient conditions.
        total = sum(a)
        squares = sum(x * x for x in a)

        if total % n != 0 or squares % n != 0:
            return True

        mean = total // n
        second_moment = squares // n

        for x in a:
            s = x + mean
            d2 = 2 * (x * x + second_moment) - s * s

            if d2 < 0:
                continue

            d = math.isqrt(d2)

            if d * d == d2 and (s - d) % 2 == 0:
                return False

        return True

    if lines[0] != "Possible" or len(lines) != 2:
        return False

    p, q, r = map(int, lines[1].split())

    if not (1 <= p <= n):
        return False

    b = a[:p - 1] + [q, r] + a[p:]

    old_sum = sum(a)
    new_sum = sum(b)

    old_sq = sum(x * x for x in a)
    new_sq = sum(x * x for x in b)

    return (
        new_sum * n == old_sum * (n + 1)
        and new_sq * n == old_sq * (n + 1)
    )

# Provided sample
sample1 = """\
11
-5 -4 -3 -2 -1 0 1 2 3 4 5
"""
out = run(sample1)
assert validate(sample1, out), "sample 1"

# Minimum-size input
case2 = """\
1
5
"""
out = run(case2)
assert validate(case2, out), "minimum-size case"

# All values equal
case3 = """\
5
7 7 7 7 7
"""
out = run(case3)
assert validate(case3, out), "all-equal case"

# Non-integer mean, immediately impossible
case4 = """\
2
0 1
"""
out = run(case4)
assert out.strip() == "Impossible", "non-integer mean"

# Large boundary values
case5 = """\
100000
""" + " ".join(["100000"] * 100000) + "\n"
out = run(case5)
assert validate(case5, out), "maximum-size boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `11` followed by `-5 ... 5` | `Possible` with any valid triple | Provided sample and discriminant derivation |
| `1 / 5` | `Possible` | Minimum (n), zero discriminant |
| Five copies of `7` | `Possible` | All-equal values |
| `2 / 0 1` | `Impossible` | Non-integer original mean |
| (10^5) copies of `100000` | `Possible` | Maximum input size, large sums and squares |

The validator intentionally avoids comparing the exact output triple. This problem asks for any valid replacement, so two different answers can both be correct.

## Edge Cases

For the minimum-size input

```
1
5
```

the algorithm computes (m=5) and (T=25). For the only possible removed value (x=5),

[
s=10
]

and

[
d^2=2(25+25)-100=0.
]

Thus (d=0), and both inserted values are (5). The output is `Possible`, as required.

For a non-integer mean such as

```
2
0 1
```

we have (S=1) and (n=2), so (S\bmod n=1). The algorithm immediately prints `Impossible`. This is stronger than a floating-point comparison because it proves that no integer (q+r) can satisfy the required mean.

For an all-equal array such as

```
5
7 7 7 7 7
```

we have (m=7) and (T=49). Removing any (x=7) gives (s=14) and (d^2=0). The algorithm inserts (7,7), preserving a variance of zero.

The perfect-square check is another critical boundary. In the sample, removing (-4) gives (d^2=36), so (d=6) and the roots are integers. If a candidate instead produced (d^2=35), the two roots would not be integral even though the discriminant is positive. The algorithm rejects it because `isqrt(35)` is (5), and (5^2\ne35).

Parity is a separate condition. Suppose the calculated values were (s=5) and (d=2). The quadratic roots would be

[
\frac{5+2}{2}=\frac72,\qquad
\frac{5-2}{2}=\frac32,
]

so no integer replacement exists. The algorithm rejects this candidate because (s-d=3) is odd.

The largest values also remain safe. With (10^5) elements each equal to (10^5),

[
S=10^{10}
]

and

[
Q=10^{15}.
]

Both fit comfortably in Python's arbitrary-precision integers. More importantly, the algorithm never constructs the full variance as a floating-point number, so there is no precision loss when comparing two theoretically equal statistics.
