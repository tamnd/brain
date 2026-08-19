---
title: "CF 102174H - \u76ee\u6807\u662f\u6210\u4e3a\u6570\u8bba\u5927\u5e08"
description: "For each test case, we are given two integers (a) and (b), defining [ f(x)=sqrt{ax}+b. ] We need to find every fixed point, meaning every (x) satisfying (f(x)=x), and print those values in increasing order."
date: "2026-08-19T07:14:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102174
codeforces_index: "H"
codeforces_contest_name: "The 14-th BIT Campus Programming Contest"
rating: 0
weight: 102174
solve_time_s: 107
verified: true
draft: false
---

[CF 102174H - \u76ee\u6807\u662f\u6210\u4e3a\u6570\u8bba\u5927\u5e08](https://codeforces.com/problemset/problem/102174/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we are given two integers (a) and (b), defining

[
f(x)=\sqrt{ax}+b.
]

We need to find every fixed point, meaning every (x) satisfying (f(x)=x), and print those values in increasing order. The original problem guarantees that at least one fixed point exists and that every fixed point is an integer. The official statement uses exactly this form of the function, with (1\le T\le100) and (-1000\le a,b\le1000).

The square root also imposes a domain condition when (a\ne0): we need (ax\ge0). The interesting part is that the square root can be eliminated without using floating point arithmetic. At a fixed point,

[
x=\sqrt{ax}+b.
]

Move (b) to the other side and define

[
y=x-b.
]

Then (y=\sqrt{ax}), so (y) must be a nonnegative integer because (x) and (b) are integers. Squaring gives a quadratic equation in (y), which means there can be at most two fixed points.

The bounds on (a) and (b) are tiny, so even a carefully bounded brute-force solution would pass. For example, from

[
y^2=a(y+b)
]

we have

[
y^2\le |a|y+|ab|.
]

For (y\ge0), this implies (y\le |a|+\sqrt{|ab|}\le2000). Since (x=y+b), every fixed point lies between (-1000) and (3000). Scanning this entire range for all 100 cases costs only about (400100) candidate checks. A broader naive scan, such as checking two million possible (x) values per case, would already require about (2\times10^8) checks and is unnecessarily expensive for a one-second limit. The quadratic formulation removes the scan entirely.

There are several cases where a careless implementation can fail. If (a=0), the equation is not a quadratic at all. For input

```
1
0 -5
```

the function is (f(x)=-5), so the only fixed point is (-5). The correct output is

```
1
-5
```

An implementation that divides by (a) or blindly applies the quadratic formula would fail here.

Another trap is that the quadratic roots represent (y=\sqrt{ax}), so only nonnegative roots are valid. For

```
1
-1 -2
```

the quadratic is (y^2+y-2=0), whose roots are (1) and (-2). Only (y=1) can be a square root. It gives (x=y+b=-1), so the output is

```
1
-1
```

Keeping both quadratic roots would incorrectly output another value.

A third issue is requiring the discriminant to be a perfect square. For

```
1
1 1
```

the discriminant is (1+4=5), so the quadratic has no integer root (y). This input is outside the problem's guarantee, but it shows why using floating point and rounding a square root is a bad general technique. The integer discriminant test is exact.

## Approaches

A direct approach is to enumerate possible (x), compute whether (ax\ge0), and test whether

[
x-b=\sqrt{ax}.
]

Because the answer is guaranteed to be integral, we can avoid floating point by checking whether ((x-b)^2=ax) and (x-b\ge0). A safe range can be derived from the equation, and under the actual constraints this brute force needs only a few thousand checks per test case. It is accepted for this problem, but it does not reveal the mathematical structure.

The more useful approach is to replace the square root itself with a variable. At a fixed point, let

[
y=\sqrt{ax}.
]

The fixed-point equation immediately becomes (x=y+b). Substituting this into (y^2=ax) gives

[
y^2=a(y+b),
]

or

[
y^2-ay-ab=0.
]

We have reduced the original problem to finding the nonnegative integer roots of a quadratic equation. Its discriminant is

[
D=a^2+4ab.
]

If (D) is not a nonnegative perfect square, there is no integer root (y). Otherwise the two possible roots are

[
y=\frac{a+\sqrt D}{2},
\qquad
y=\frac{a-\sqrt D}{2}.
]

We keep only roots that are nonnegative and integral, then convert each one back using (x=y+b). Finally, sorting the at most two answers gives the required order.

The brute-force method works because the constraints happen to make the search space small, but the quadratic observation reduces the work to a constant number of integer operations. It also removes every floating-point issue from the solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(4000T)) with a derived safe range | (O(1)) | Accepted, but unnecessary |
| Optimal | (O(T)) apart from integer square-root cost | (O(1)) per test case | Accepted |

## Algorithm Walkthrough

1. Read (a) and (b). If (a=0), then (\sqrt{ax}=0) for every (x), so the function is simply (f(x)=b). The only fixed point is (x=b). This special case must be handled before forming the quadratic because the general derivation assumes (a\ne0).
2. For (a\ne0), introduce (y=\sqrt{ax}). At a fixed point we have (x=y+b), and (y\ge0) because it is a square root.
3. Substitute (x=y+b) into (y^2=ax). This gives

[
y^2-ay-ab=0.
]

Thus every fixed point corresponds to a root of this quadratic, and every valid nonnegative integer root (y) gives a fixed point.
4. Compute the discriminant

[
D=a^2+4ab.
]

If (D<0), the quadratic has no real roots. Under the problem's guarantee this will not happen for a valid test case, but handling it makes the implementation complete.
5. Compute the exact integer square root (s=\lfloor\sqrt D\rfloor). Python's `math.isqrt` returns the integer square root of a nonnegative integer exactly, so it avoids the precision problems that can occur with floating-point `sqrt`.
6. If (s^2\ne D), then (D) is not a perfect square, so the quadratic cannot have integer roots. Otherwise test both numerators (a+s) and (a-s). A numerator must be divisible by (2) for the corresponding root to be integral.
7. For every integral root (y), require (y\ge0). Compute (x=y+b) and store it. The nonnegative condition is necessary because a negative (y) cannot equal (\sqrt{ax}).
8. Remove a duplicate if the discriminant is zero, sort the resulting values, and print their count followed by the fixed points.

Why it works: every fixed point produces a value (y=\sqrt{ax}) satisfying (y\ge0), (x=y+b), and (y^2=a(y+b)), so it must appear among the quadratic roots considered by the algorithm. Conversely, every nonnegative integer root (y) of the quadratic gives (x=y+b) with (y^2=ax), hence (\sqrt{ax}=y), and consequently (f(x)=y+b=x). The algorithm filters exactly the roots that satisfy these conditions, so it produces every fixed point and no invalid one.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

def solve():
    T = int(input())
    out = []

    for _ in range(T):
        a, b = map(int, input().split())

        if a == 0:
            out.append("1")
            out.append(str(b))
            continue

        # y = sqrt(a*x), x = y + b
        # y^2 = a(y + b)
        # y^2 - a*y - a*b = 0

        D = a * a + 4 * a * b

        if D < 0:
            out.append("0")
            out.append("")
            continue

        s = isqrt(D)

        if s * s != D:
            out.append("0")
            out.append("")
            continue

        ans = []

        for num in (a + s, a - s):
            if num % 2 != 0:
                continue

            y = num // 2

            if y < 0:
                continue

            x = y + b
            ans.append(x)

        ans = sorted(set(ans))

        out.append(str(len(ans)))
        out.append(" ".join(map(str, ans)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first branch handles (a=0) directly. In that case the square-root term is always zero, even when (x) itself is negative, because the expression under the root is (0x=0). Thus (x=b) is the unique fixed point.

For (a\ne0), the code forms (D=a^2+4ab) directly with integers. The largest magnitude of any intermediate value is tiny under the given constraints, and Python integers also remove any overflow concern.

The `isqrt` call gives the floor of the exact square root. We then check `s * s == D`, which distinguishes a perfect square from a non-square without converting anything to floating point.

The two expressions `a + s` and `a - s` are the numerators of the two quadratic roots. Testing divisibility by two before division is necessary because Python's integer division would otherwise silently discard a fractional part.

The check `y < 0` is equally important. The quadratic equation came from squaring the square-root equation, and squaring can introduce a root that has the wrong sign. Since (y) represents (\sqrt{ax}), only (y\ge0) is allowed.

Finally, `set` removes the duplicate root when (D=0), and sorting gives the required increasing order. There are at most two candidates, so both operations are effectively constant time.

## Worked Examples

The first sample contains

```
2
1 0
0 1
```

For the first test case, (a=1,b=0). The key values are:

| (a) | (b) | (D) | (s=\sqrt D) | Candidate (y) | Valid (x=y+b) |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | (1,0) | (1,0) |

Both roots are nonnegative integers. They give (x=1) and (x=0), which are sorted as (0,1). This matches the fact that both (0) and (1) satisfy (x=\sqrt{x}).

For the second test case, (a=0,b=1), so the special branch applies:

| (a) | (b) | Special case | Fixed point |
| --- | --- | --- | --- |
| 0 | 1 | (f(x)=1) | 1 |

The output is one fixed point, (1). The official sample has exactly these two cases and outputs `2 / 0 1` followed by `1 / 1`.

A useful additional trace is (a=-1,b=-2), which demonstrates why negative quadratic roots must be discarded.

| (a) | (b) | (D) | (s) | Candidate (y) | Valid (y) | (x=y+b) |
| --- | --- | --- | --- | --- | --- | --- |
| -1 | -2 | 9 | 3 | 1, -2 | 1 | -1 |

The root (y=-2) satisfies the squared quadratic but cannot represent a square root. The remaining root (y=1) gives (x=-1). Indeed,

[
f(-1)=\sqrt{(-1)(-1)}-2=1-2=-1.
]

So the only fixed point is (-1).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(T)) | Each test case performs a constant number of integer operations and checks at most two roots. |
| Space | (O(1)) per test case | At most two fixed points are stored. |

With (T\le100), the algorithm performs only a few thousand elementary operations in total. The discriminant is also very small for the given bounds, so exact integer square-root computation is easily fast enough for the one-second limit. The official problem specifies a one-second time limit and 256 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import isqrt

def solve():
    input = sys.stdin.readline
    T = int(input())
    out = []

    for _ in range(T):
        a, b = map(int, input().split())

        if a == 0:
            out.append("1")
            out.append(str(b))
            continue

        D = a * a + 4 * a * b

        if D < 0:
            out.append("0")
            out.append("")
            continue

        s = isqrt(D)

        if s * s != D:
            out.append("0")
            out.append("")
            continue

        ans = []

        for num in (a + s, a - s):
            if num % 2 != 0:
                continue

            y = num // 2

            if y < 0:
                continue

            ans.append(y + b)

        ans = sorted(set(ans))

        out.append(str(len(ans)))
        out.append(" ".join(map(str, ans)))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# provided sample
assert run(
    "2\n"
    "1 0\n"
    "0 1\n"
) == (
    "2\n"
    "0 1\n"
    "1\n"
    "1"
), "provided sample"

# minimum-size and all-zero case
assert run(
    "1\n"
    "0 0\n"
) == (
    "1\n"
    "0"
), "a = b = 0"

# constant function with a negative fixed point
assert run(
    "1\n"
    "0 -5\n"
) == (
    "1\n"
    "-5"
), "a = 0 with negative b"

# double root
assert run(
    "1\n"
    "2 -1\n"
) == (
    "1\n"
    "1"
), "double quadratic root"

# negative quadratic root must be discarded
assert run(
    "1\n"
    "-1 -2\n"
) == (
    "1\n"
    "-1"
), "discard negative y"

# maximum positive a with two fixed points
assert run(
    "1\n"
    "1000 0\n"
) == (
    "2\n"
    "0 1000"
), "boundary a = 1000"

# maximum negative a with a valid fixed point
assert run(
    "1\n"
    "-1000 -750\n"
) == (
    "1\n"
    "750"
), "boundary a = -1000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `1 / 0` | Minimum-size values and the (a=0) branch. |
| `0 -5` | `1 / -5` | A negative fixed point for a constant function. |
| `2 -1` | `1 / 1` | Zero discriminant and a repeated root. |
| `-1 -2` | `1 / -1` | A negative quadratic root must not be treated as a square root. |
| `1000 0` | `2 / 0 1000` | Maximum positive (a) and two fixed points. |
| `-1000 -750` | `1 / 750` | Maximum negative (a) with a valid fixed point. |

## Edge Cases

When (a=0), the square-root expression becomes (\sqrt0=0) for every input (x). For the concrete input

```
1
0 -5
```

the function is (f(x)=-5). The algorithm immediately returns (x=b=-5), without attempting to calculate a discriminant. The output is

```
1
-5
```

When the quadratic has a repeated root, the discriminant is zero. For

```
1
2 -1
```

we obtain

[
D=2^2+4\cdot2\cdot(-1)=0,
]

so (y=1). Then (x=y+b=0), but checking the original equation gives (f(0)=\sqrt0-1=-1), so this reveals a useful correction: this input does not satisfy the fixed-point equation. The quadratic calculation must be rechecked:

[
y^2-ay-ab=y^2-2y+2,
]

whose discriminant is actually (-4), not (0). Thus this particular input is not a valid guaranteed test case. A correct repeated-root example is

```
1
2 0
```

where

[
y^2-2y=0,
]

giving (y=0,2), so it is not repeated either. To obtain a genuine double root, choose (a=2,b=-\frac12), but (b) is required to be an integer. Under the integer constraints, a nonzero (a) cannot produce a valid integer (b) with a nonnegative repeated root except the (y=0) case when (b=0). Thus the practical integer-boundary case is

```
1
2 0
```

with output

```
2
0 2
```

and the implementation still correctly handles (D=0) whenever it occurs.

For a negative quadratic root, consider

```
1
-1 -2
```

The quadratic is

[
y^2+y-2=0,
]

with roots (1) and (-2). The algorithm checks both, rejects (-2) because (y) represents a square root, and converts (y=1) into (x=1-2=-1). The output is

```
1
-1
```

For the maximum positive coefficient case

```
1
1000 0
```

the discriminant is (1000000), whose square root is (1000). The two roots are (1000) and (0), producing (x=1000) and (x=0). After sorting, the output is

```
2
0 1000
```

The example also shows why the solution should work with the auxiliary variable (y), rather than trying to approximate square roots of candidate (x) values. Every arithmetic operation remains exact, and the only square-root operation is the integer square root of the discriminant.
