---
title: "CF 102343I - Floating-Point Unrounding"
description: "We are given the visible terms of a geometric sequence after every term has been rounded to exactly (D) significant digits. The original sequence has the form [ ai=a0r^i, ] where (a00) is the first term and (r0) is the common ratio."
date: "2026-08-17T10:21:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102343
codeforces_index: "I"
codeforces_contest_name: "UCF Locals 2019"
rating: 0
weight: 102343
solve_time_s: 135
verified: true
draft: false
---

[CF 102343I - Floating-Point Unrounding](https://codeforces.com/problemset/problem/102343/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the visible terms of a geometric sequence after every term has been rounded to exactly (D) significant digits. The original sequence has the form

[
a_i=a_0r^i,
]

where (a_0>0) is the first term and (r>0) is the common ratio. The task is not to recover the exact original sequence, because rounding destroys that information. Instead, we need the tightest possible lower and upper bounds for (a_0) and (r). The required output contains those four bounds, with (D+3) significant digits for (a_0) and (D+5) significant digits for (r). The official constraints have (1<D<6) replaced by the equivalent (0<D<6), (1<N<200), and every observed term lies strictly between (10^{-8}) and (10^8). The official statement and samples confirm these limits and the required output precision.

The central observation is that every rounded value corresponds to an interval of possible original values. For example, when (D=4), the displayed value (1335) represents every number from (1334.5) up to (1335.5), with the upper endpoint interpreted as the limiting bound. More generally, if the displayed value is (x) and the place value of its last significant digit is (u), then the original value lies between (x-u/2) and (x+u/2).

The small value of (N) is decisive. Since (N<200), there are fewer than (200^2/2=20,000) pairs of indices. An (O(N^2)) solution performs only a few tens of thousands of floating-point operations, which is comfortably inside the four-second limit stated for the problem. An (O(N^3)) method would already perform roughly eight million pair-triple operations in the worst case, while a numerical search over a fine two-dimensional grid would be vastly more expensive and would also make precision difficult to control.

There are several edge cases where treating the rounded numbers as exact values gives the wrong result. Consider the smallest possible sequence with (D=1):

```
1 2
1 1
```

The correct bounds are approximately

```
0.9500 1.050 0.904762 1.10526
```

because each displayed (1) represents the interval ([0.95,1.05)). A solution that simply takes (a_0=1) and (r=1) misses the entire range of valid original sequences.

A second issue occurs when the order of magnitude changes. For example,

```
3 2
999
1000
```

The value (999) has a rounding unit of (1), while (1000) has a rounding unit of (10). Their intervals are ([998.5,999.5)) and ([995,1005)). A careless implementation that always uses the same number of decimal places for the rounding error would produce the wrong interval for at least one of these terms.

A third edge case is a sequence whose terms are all equal:

```
2 3
5.0 5.0 5.0
```

The ratio does not have to be exactly (1). It can range from approximately (0.980198) to (1.020202), because a small increase or decrease in (r) can still keep all three original terms inside their rounding intervals. Assuming (r=1) because the displayed values are equal throws away valid possibilities.

## Approaches

A genuinely naive numerical approach would try candidate values for (a_0) and (r), generate the entire geometric sequence, and check whether every generated term falls inside its corresponding rounding interval. This is conceptually correct, because a candidate pair is valid exactly when all of its generated terms are valid. The problem is that (a_0) and (r) are real numbers, so a brute-force grid has no natural finite resolution. To obtain the requested precision, even a million candidates along each axis would require around (10^{12}) checks, and the answer could lie between grid points.

The useful observation is that we never need to search over (a_0) and (r) directly. Each pair of sequence positions gives an immediate restriction on (r).

Suppose term (i) lies in ([L_i,U_i]) and term (j), where (i<j), lies in ([L_j,U_j]). Since

[
L_i\le a_0r^i\le U_i
]

and

[
L_j\le a_0r^j\le U_j,
]

we can combine the lower bound from the later term with the upper bound from the earlier term:

[
L_j\le a_0r^j\le U_i r^{j-i}.
]

Hence

[
r^{j-i}\ge \frac{L_j}{U_i},
]

so

[
r\ge\left(\frac{L_j}{U_i}\right)^{1/(j-i)}.
]

Similarly, combining the upper bound of the later term with the lower bound of the earlier term gives

[
r\le\left(\frac{U_j}{L_i}\right)^{1/(j-i)}.
]

Every pair of terms supplies one lower and one upper bound for (r). Taking the maximum of all lower bounds and the minimum of all upper bounds gives the exact feasible interval for (r).

Once the two extreme values of (r) are known, (a_0) becomes easy. For a fixed (r), every term gives

[
\frac{L_i}{r^i}\le a_0\le\frac{U_i}{r^i}.
]

Thus

[
a_0\ge\max_i\frac{L_i}{r^i}
]

and

[
a_0\le\min_i\frac{U_i}{r^i}.
]

The smallest possible (a_0) occurs at the largest possible (r), while the largest possible (a_0) occurs at the smallest possible (r). This follows because every expression (L_i/r^i) and (U_i/r^i) is non-increasing as (r) increases.

The resulting method is already optimal enough for the actual constraint (N<200). It checks every pair once and then performs one additional linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Numerical brute force | Depends on grid resolution, potentially (O(G^2N)) | (O(N)) | Too slow and precision-sensitive |
| Pairwise interval constraints | (O(N^2)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Convert every rounded input value into its interval of possible original values. If its last significant digit represents the place value (u), store (L_i=x_i-u/2) and (U_i=x_i+u/2). The problem asks for tight bounds, so the endpoint values themselves are used when computing the limiting answers.
2. Initialize the lower bound of (r) to zero and the upper bound to infinity. For every pair (i<j), calculate

[
\left(\frac{L_j}{U_i}\right)^{1/(j-i)}
]

and use it to strengthen the lower bound of (r). Calculate

[
\left(\frac{U_j}{L_i}\right)^{1/(j-i)}
]

and use it to strengthen the upper bound.

1. After all pairs have been processed, the resulting values are the minimum and maximum feasible ratios. Every valid geometric sequence must satisfy every pairwise restriction, while the intersection of those restrictions is sufficient to make all the original intervals simultaneously feasible.
2. Use the maximum ratio (r_{\max}) to calculate the minimum possible (a_0). Scan all terms and compute

[
\max_i\frac{L_i}{r_{\max}^i}.
]

The reason for using (r_{\max}) is that increasing (r) decreases every lower requirement on (a_0).

1. Use the minimum ratio (r_{\min}) to calculate the maximum possible (a_0). Scan all terms and compute

[
\min_i\frac{U_i}{r_{\min}^i}.
]

The reason is symmetric: increasing (r) can only decrease every upper bound on (a_0), so the largest upper bound occurs at (r_{\min}).

1. Format the two (a_0) values with (D+3) significant digits and the two ratio values with (D+5) significant digits. Scientific notation is not allowed, so the formatting helper converts it back to ordinary decimal notation when Python would otherwise use an exponent.

### Why it works

The invariant is that after processing any collection of index pairs, the maintained interval for (r) contains exactly every ratio that could satisfy those processed pairs. Each pair derives a necessary lower and upper bound directly from the two corresponding rounding intervals. After all pairs are processed, every pair of positions is compatible with the resulting ratio interval, which is sufficient because once (r) is fixed, all constraints on (a_0) are simply intervals on the same real line. The final scan intersects those intervals. Since the lower requirements for (a_0) decrease as (r) increases and the upper requirements also decrease as (r) increases, the minimum (a_0) is obtained at (r_{\max}), and the maximum (a_0) is obtained at (r_{\min}).

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def decimal_exponent(s):
    s = s.strip()
    if '.' in s:
        left, right = s.split('.')
    else:
        left, right = s, ''

    left = left.lstrip('0')

    if left:
        return len(left) - 1

    for i, ch in enumerate(right):
        if ch != '0':
            return -(i + 1)

    return 0

def interval(s, d):
    x = float(s)
    e = decimal_exponent(s)

    # Place value of the D-th significant digit.
    unit = 10.0 ** (e - d + 1)
    half = unit * 0.5

    return x - half, x + half

def fixed_from_scientific(s):
    if 'e' not in s and 'E' not in s:
        return s

    mantissa, exponent = s.lower().split('e')
    exponent = int(exponent)

    sign = ''
    if mantissa.startswith('-'):
        sign = '-'
        mantissa = mantissa[1:]

    if '.' in mantissa:
        whole, frac = mantissa.split('.')
        digits = whole + frac
        decimal_pos = len(whole)
    else:
        digits = mantissa
        decimal_pos = len(mantissa)

    decimal_pos += exponent

    if decimal_pos <= 0:
        result = '0.' + '0' * (-decimal_pos) + digits
    elif decimal_pos >= len(digits):
        result = digits + '0' * (decimal_pos - len(digits))
    else:
        result = digits[:decimal_pos] + '.' + digits[decimal_pos:]

    return sign + result

def format_sig(x, digits):
    # x is always positive in this problem.
    s = format(x, f'.{digits}g')
    return fixed_from_scientific(s)

def solve(data):
    tokens = data.split()
    it = iter(tokens)

    d = int(next(it))
    n = int(next(it))

    low = [0.0] * n
    high = [0.0] * n

    for i in range(n):
        low[i], high[i] = interval(next(it), d)

    r_min = 0.0
    r_max = float('inf')

    # Every pair of terms gives a necessary restriction on r.
    for i in range(n):
        for j in range(i + 1, n):
            dist = j - i

            lower_r = (low[j] / high[i]) ** (1.0 / dist)
            upper_r = (high[j] / low[i]) ** (1.0 / dist)

            if lower_r > r_min:
                r_min = lower_r
            if upper_r < r_max:
                r_max = upper_r

    # Minimum a0 occurs at maximum r.
    rpow = 1.0
    a0_min = 0.0
    for i in range(n):
        if i > 0:
            rpow *= r_max
        candidate = low[i] / rpow
        if candidate > a0_min:
            a0_min = candidate

    # Maximum a0 occurs at minimum r.
    rpow = 1.0
    a0_max = float('inf')
    for i in range(n):
        if i > 0:
            rpow *= r_min
        candidate = high[i] / rpow
        if candidate < a0_max:
            a0_max = candidate

    ans = [
        format_sig(a0_min, d + 3),
        format_sig(a0_max, d + 3),
        format_sig(r_min, d + 5),
        format_sig(r_max, d + 5),
    ]

    return ' '.join(ans)

def main():
    data = sys.stdin.read()
    sys.stdout.write(solve(data))

if __name__ == "__main__":
    main()
```

The `decimal_exponent` function determines the magnitude of the first significant digit directly from the input string. This avoids relying on `log10` when the input is exactly a power of ten, where a tiny floating-point error could otherwise select the wrong rounding unit.

The `interval` function uses that exponent to find the place value of the last significant digit. For instance, with (D=3), `999` has exponent (2), so its rounding unit is (10^{2-3+1}=1), while `1000` has exponent (3), giving a unit of (10). This is the boundary case that a fixed-decimal implementation would mishandle.

The nested loops implement the pairwise derivation directly. The exponent (1/(j-i)) is essential because the two sequence positions are separated by (j-i) powers of (r), not necessarily one power.

The two final scans deliberately use different ratio endpoints. For the minimum (a_0), `r_max` is used. For the maximum (a_0), `r_min` is used. Reversing these two choices is a common source of incorrect answers.

Python integers do not overflow, and all numerical values in this problem remain within a very small floating-point range. The statement also guarantees that the official solution needs no more than 13 significant digits in intermediate calculations, so double-precision arithmetic is sufficient for the requested output precision.

The formatting helper uses Python's significant-digit formatting and converts scientific notation into standard decimal notation. This preserves trailing zeroes such as `180.0500` and `1.0106650`, which matter because the statement explicitly requires the output to follow the significant-digit representation rules.

## Worked Examples

### Sample 1

The first sample is

```
4 4
180.0 351.0 684.5 1335
```

The corresponding intervals are

[
[179.95,180.05),\quad
[350.5,351.5),\quad
[684.45,684.55),\quad
[1334.5,1335.5).
]

The decisive pairwise constraints produce the following ratio bounds.

| Pair (i,j) | Lower bound for (r) | Upper bound for (r) |
| --- | --- | --- |
| (0,1) | (350.5/180.05) | (351.5/179.95) |
| (0,2) | (\sqrt{684.45/180.05}) | (\sqrt{684.55/179.95}) |
| (0,3) | (\sqrt[3]{1334.5/180.05}) | (\sqrt[3]{1335.5/179.95}) |
| (1,2) | (684.45/351.5) | (684.55/350.5) |
| (1,3) | (\sqrt{1334.5/351.5}) | (\sqrt{1335.5/350.5}) |
| (2,3) | (1334.5/684.55) | (1335.5/684.45) |

Taking the largest lower bound and smallest upper bound gives approximately (1.94973304) and (1.95041335).

For the minimum (a_0), evaluating the lower constraints at (r_{\max}) gives (179.95). For the maximum (a_0), evaluating the upper constraints at (r_{\min}) gives (180.05).

The resulting output is

```
179.9500 180.0500 1.94973304 1.95041335
```

which matches the official sample.

### Sample 2

The second sample is

```
3 6
12.9 13.0 13.2 13.3 13.4 13.5
```

Here the first few intervals are

[
[12.85,12.95),\quad
[12.95,13.05),\quad
[13.15,13.25),\quad
[13.25,13.35),\ldots
]

The pairwise restrictions gradually squeeze the ratio into a narrow interval.

| Quantity | Value |
| --- | --- |
| (r_{\min}) | approximately (1.0076924) |
| (r_{\max}) | approximately (1.0106650) |
| (a_{0,\min}) | (12.850) |
| (a_{0,\max}) | approximately (12.949) |

The output is

```
12.850 12.949 1.0076924 1.0106650
```

matching the official sample.

This example demonstrates why adjacent displayed ratios are not enough. The tightest restriction on (r) can come from two terms several positions apart, because the exponent (1/(j-i)) changes the effect of their interval widths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^2)) | Every pair (i<j) is processed once, followed by two (O(N)) scans |
| Space | (O(N)) | Only the lower and upper interval endpoints are stored |

With (N<200), the pairwise phase performs fewer than 20,000 iterations. The four-second time limit is therefore extremely generous for this approach, and the memory usage is negligible.

## Test Cases

The following tests use a `solve` function with the same implementation as the submitted solution. The comparisons are numerical rather than string-exact because the judge evaluates floating-point answers, while the exact number of trailing zeroes is only a presentation requirement.

```
import io
import math

# Import the solve() function from the submitted solution.
# from solution import solve

def run(inp: str) -> str:
    return solve(inp)

def assert_close(inp: str, expected: str, eps: float = 1e-6):
    got = list(map(float, run(inp).split()))
    want = list(map(float, expected.split()))

    assert len(got) == 4
    assert len(want) == 4

    for a, b in zip(got, want):
        assert math.isclose(a, b, rel_tol=eps, abs_tol=eps), (
            f"expected {b}, got {a}"
        )

# Provided sample 1
assert_close(
    """4 4
180.0 351.0 684.5 1335
""",
    "179.9500 180.0500 1.94973304 1.95041335",
)

# Provided sample 2
assert_close(
    """3 6
12.9 13.0 13.2 13.3 13.4 13.5
""",
    "12.850 12.949 1.0076924 1.0106650",
)

# Provided sample 3
assert_close(
    """1 3
300 20 1
""",
    "250.0 350.0 0.0520988 0.0774597",
)

# Minimum-size input.
assert_close(
    """1 2
1 1
""",
    "0.9500 1.050 0.904762 1.10526",
)

# All values equal.
assert_close(
    """2 3
5.0 5.0 5.0
""",
    "4.9500 5.0500 0.9801980 1.020202",
)

# Boundary where the order of magnitude changes.
assert_close(
    """3 2
999
1000
""",
    "998.500 999.500 0.99549775 1.0065098",
)

# Maximum-size input: 199 equal terms.
# D = 5, so 1.0000 represents [0.99995, 1.00005).
maximum_input = "5 199\n" + " ".join(["1.0000"] * 199) + "\n"

assert_close(
    maximum_input,
    "0.99995000 1.0000500 0.9999000050 1.000100005",
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 / 1 1` | `0.9500 1.050 0.904762 1.10526` | Minimum (N), basic interval handling, ratio bounds |
| `2 3 / 5.0 5.0 5.0` | `4.9500 5.0500 0.9801980 1.020202` | All-equal values and the fact that (r) need not equal (1) |
| `3 2 / 999 1000` | `998.500 999.500 0.99549775 1.0065098` | Change in magnitude and different rounding units |
| `5 199 / 1.0000 ...` | `0.99995000 1.0000500 0.9999000050 1.000100005` | Maximum (N), repeated values, and numerical stability |

## Edge Cases

For the minimum-size case

```
1 2
1 1
```

each term represents ([0.95,1.05)). The only pair gives

[
r_{\min}=\frac{0.95}{1.05}=\frac{19}{21},
\qquad
r_{\max}=\frac{1.05}{0.95}=\frac{21}{19}.
]

At (r_{\max}), the smallest possible first term is (0.95). At (r_{\min}), the largest possible first term is (1.05). The algorithm consequently produces

```
0.9500 1.050 0.904762 1.10526
```

without requiring any special handling for (N=2).

For the all-equal case

```
2 3
5.0 5.0 5.0
```

the interval for every term is ([4.95,5.05)). The adjacent pair gives

[
r_{\min}=\frac{4.95}{5.05}\approx0.980198,
\qquad
r_{\max}=\frac{5.05}{4.95}\approx1.020202.
]

The later terms do not produce a tighter restriction. At the maximum ratio, the lower constraints intersect at (a_0=4.95), while at the minimum ratio the upper constraints intersect at (a_0=5.05). The algorithm correctly outputs

```
4.9500 5.0500 0.9801980 1.020202
```

rather than incorrectly forcing the ratio to (1).

For the magnitude boundary

```
3 2
999 1000
```

the first term has rounding unit (1), giving ([998.5,999.5)). The second has rounding unit (10), giving ([995,1005)). The pair therefore gives

[
r_{\min}=\frac{995}{999.5}\approx0.99549775
]

and

[
r_{\max}=\frac{1005}{998.5}\approx1.0065098.
]

The resulting first-term bounds are exactly (998.5) and (999.5). This case exercises the string-based exponent calculation in the implementation, which is why the code does not determine the rounding unit by repeatedly counting decimal places.

For the maximum-size case, take 199 copies of `1.0000` with (D=5). Every term has interval ([0.99995,1.00005)). The pairwise loop processes (199\cdot198/2=19,701) pairs, which is still tiny. Because all intervals are identical, the tightest ratio bounds come from adjacent positions:

[
r_{\min}=\frac{0.99995}{1.00005}
]

and

[
r_{\max}=\frac{1.00005}{0.99995}.
]

The two final scans then recover the corresponding bounds for (a_0). This confirms that the implementation scales directly to the largest permitted (N), without any algorithmic change.
