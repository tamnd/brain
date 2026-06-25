---
title: "CF 105910A - SCUPC"
description: "We have three binary strings of the same length. At each position, we look at the three bits and count that position if at least two of the bits are 1. We are allowed to pick exactly one of the three strings and rotate it cyclically to the left any number of times."
date: "2026-06-25T14:03:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105910
codeforces_index: "A"
codeforces_contest_name: "The 23rd Sichuan University Programming Contest"
rating: 0
weight: 105910
solve_time_s: 62
verified: true
draft: false
---

[CF 105910A - SCUPC](https://codeforces.com/problemset/problem/105910/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three binary strings of the same length. At each position, we look at the three bits and count that position if at least two of the bits are `1`.

We are allowed to pick exactly one of the three strings and rotate it cyclically to the left any number of times. The other two strings stay fixed. After choosing the best string to rotate and the best rotation amount, we want the largest possible number of positions where at least two of the three bits are `1`. The contest statement gives multiple test cases, and the sum of all string lengths is at most $10^5$.

The total length bound is the key observation. Any solution that tries all $n$ rotations and evaluates all $n$ positions for each rotation would require $O(n^2)$ work per test case, which becomes far too large when $n$ reaches $10^5$. We need something around $O(n \log n)$.

A subtle point is that rotating different strings produces different optimization problems. A solution that only considers rotating the third string can miss the optimum.

Consider:

```
n = 3
s1 = 110
s2 = 001
s3 = 001
```

Rotating `s3` is not equivalent to rotating `s1`. The best answer must be taken over all three choices.

Another easy mistake is to optimize only pairwise overlaps. The objective is not the number of positions where all three strings have `1`, but the number of positions where at least two strings have `1`.

For example:

```
s1 = 10
s2 = 10
s3 = 01
```

The first position already contributes because two strings contain `1`, even though the third string contains `0`.

## Approaches

A direct brute-force solution is straightforward. Choose which string to rotate. Try all $n$ cyclic shifts. For each shift, scan all $n$ positions and count how many positions contain at least two ones.

The brute-force method is correct because it explicitly checks every valid configuration. Its running time is $O(3n^2)$, which is effectively $O(n^2)$. With $n = 10^5$, that means around $10^{10}$ operations, far beyond the limit.

To find a faster approach, we need to rewrite the scoring function.

Assume we rotate the third string. Let

$$a_i=s_{1,i}, \quad b_i=s_{2,i}, \quad c_i=s_{3,i}.$$

For binary values, the indicator that at least two bits are equal to `1` can be written as

$$[a_i+b_i+c_i\ge2]
=
a_ib_i+a_ic_i+b_ic_i-2a_ib_ic_i.$$

Summing over all positions gives

$$\text{score}
=
\sum a_ib_i
+
\sum a_ic_i
+
\sum b_ic_i
-
2\sum a_ib_ic_i.$$

The first term does not depend on the rotation.

Now define

$$d_i=a_i+b_i-2a_ib_i.$$

Checking all four possibilities of $(a_i,b_i)$:

| $a_i$ | $b_i$ | $d_i$ |
| --- | --- | --- |
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

So $d_i = a_i \oplus b_i$.

The score becomes

$$\sum a_ib_i + \sum d_i \cdot c_i.$$

After rotation, only the second term changes. The problem reduces to:

Find the maximum cyclic overlap between a binary string $d=a\oplus b$ and the rotated string $c$.

This is a classic cyclic cross-correlation problem. All shift values can be computed simultaneously with one FFT convolution.

We repeat the same computation for the three possible choices of the rotated string and take the maximum answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal FFT | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Computing the value when the third string is rotated

1. Let `a`, `b`, and `c` be the three binary arrays.
2. Compute

$$\text{base}=\sum a_i b_i.$$

This part never changes under rotations of `c`.
3. Compute

$$d_i=a_i\oplus b_i.$$

The score for any shift becomes

$$\text{base} + \sum d_i \cdot c_{i+\text{shift}}.$$
4. Build `cc = c + c`, the doubled array of length `2n`.

Every cyclic shift of `c` appears as a contiguous length-`n` segment inside `cc`.
5. Reverse `cc` and convolve it with `d` using FFT.
6. Extract the $n$ correlation values corresponding to the $n$ cyclic shifts.
7. Let `best_corr` be the maximum extracted correlation.
8. The best score for rotating `c` is

$$\text{base} + \text{best\_corr}.$$

### Considering all choices

1. Rotate `s1`, keep `s2` and `s3` fixed.
2. Rotate `s2`, keep `s1` and `s3` fixed.
3. Rotate `s3`, keep `s1` and `s2` fixed.
4. Output the maximum of the three results.

### Why it works

For a fixed choice of rotated string, the identity

$$[a+b+c\ge2]
=
ab+ac+bc-2abc$$

is exact for every binary triple. After regrouping terms, the entire score becomes

$$\sum ab + \sum (a\oplus b)c.$$

The first sum is constant. The second sum is exactly a cyclic correlation between two binary arrays. FFT computes every shift's correlation simultaneously, so the largest correlation corresponds to the best rotation. Evaluating all three choices of rotated string guarantees that the global optimum is found.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def fft(a, invert):
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
        ang = 2.0 * math.pi / length
        if not invert:
            ang = -ang

        wlen = complex(math.cos(ang), math.sin(ang))

        for i in range(0, n, length):
            w = 1 + 0j
            half = length // 2

            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w

                a[j] = u + v
                a[j + half] = u - v

                w *= wlen

        length <<= 1

    if invert:
        for i in range(n):
            a[i] /= n

def convolution(a, b):
    n = 1
    need = len(a) + len(b) - 1

    while n < need:
        n <<= 1

    fa = [complex(x, 0) for x in a] + [0j] * (n - len(a))
    fb = [complex(x, 0) for x in b] + [0j] * (n - len(b))

    fft(fa, False)
    fft(fb, False)

    for i in range(n):
        fa[i] *= fb[i]

    fft(fa, True)

    return [int(round(x.real)) for x in fa[:need]]

def solve_one(x, y, rot):
    n = len(x)

    base = 0
    d = [0] * n

    for i in range(n):
        a = x[i]
        b = y[i]

        if a and b:
            base += 1

        d[i] = a ^ b

    doubled = rot + rot

    conv = convolution(d, doubled[::-1])

    best = 0

    for shift in range(n):
        idx = n - 1 + (n - 1 - shift)
        best = max(best, conv[idx])

    return base + best

def main():
    t = int(input())

    ans = []

    for _ in range(t):
        n = int(input())

        s1 = [int(c) for c in input().strip()]
        s2 = [int(c) for c in input().strip()]
        s3 = [int(c) for c in input().strip()]

        res = 0

        res = max(res, solve_one(s2, s3, s1))
        res = max(res, solve_one(s1, s3, s2))
        res = max(res, solve_one(s1, s2, s3))

        ans.append(str(res))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()
```

The function `solve_one` assumes one particular string is allowed to rotate. The other two strings are transformed into a constant part and an XOR array. After that, the problem becomes a cyclic correlation query.

The doubled array `rot + rot` is the standard trick for cyclic shifts. Every rotation appears as a length-`n` window inside this doubled sequence.

The convolution uses FFT to compute all correlations simultaneously. Since FFT works with floating point values, the resulting coefficients are rounded to the nearest integer.

The index extraction is the part most likely to cause mistakes. The convolution of `d` and `reverse(rot + rot)` produces all alignments. The coefficient

$$n-1+(n-1-\text{shift})$$

corresponds exactly to the cyclic shift we need.

## Worked Examples

### Example 1

```
n = 10
s1 = 0000001000
s2 = 0000000110
s3 = 0000000001
```

Rotate `s3`.

| Position | s1 | s2 | XOR(s1,s2) |
| --- | --- | --- | --- |
| 6 | 1 | 0 | 1 |
| 7 | 0 | 1 | 1 |
| 8 | 0 | 1 | 1 |

The XOR array contains three isolated ones. Rotating `s3` can align its single `1` with exactly one of them.

| Shift | Correlation |
| --- | --- |
| Best shift | 1 |

`base = 0`, so the answer becomes `1`.

This example shows that when only one string contributes a single `1`, the best possible result is determined entirely by the XOR positions.

### Example 2

```
n = 10
s1 = 0000001000
s2 = 0000010000
s3 = 0000001100
```

For the choice of rotating `s3`:

| Position | s1 | s2 | XOR |
| --- | --- | --- | --- |
| 5 | 0 | 1 | 1 |
| 6 | 1 | 0 | 1 |

| Shift | Correlation |
| --- | --- |
| Best shift | 2 |

`base = 0`, so the answer is `2`.

This demonstrates that FFT is finding the maximum overlap between the XOR pattern and the rotated string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Three FFT-based correlations per test case |
| Space | $O(n)$ | FFT arrays and temporary buffers |

Since the sum of all string lengths is at most $10^5$, the total FFT workload remains comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    from solution import main

    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    main()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided samples
assert run(
"""3
10
0000001000
0000000110
0000000001
10
0000001000
0000010000
0000001100
10
0000000111
0000000011
0001000000
"""
) == "1\n2\n3"

# minimum size
assert run(
"""1
1
0
0
0
"""
) == "0"

# all equal
assert run(
"""1
5
11111
11111
11111
"""
) == "5"

# single useful rotation
assert run(
"""1
4
1000
0000
0001
"""
) == "1"

# boundary alignment
assert run(
"""1
4
1000
0100
0010
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single position, all zeros | 0 | Minimum size |
| Three all-one strings | 5 | Already optimal |
| One rotating match | 1 | Cyclic shift handling |
| Ones near opposite ends | 1 | Wrap-around correctness |

## Edge Cases

Consider:

```
n = 1
s1 = 0
s2 = 0
s3 = 0
```

No rotation changes anything. The XOR array is `[0]`, the correlation is `0`, and the answer remains `0`.

Consider:

```
n = 4
s1 = 1000
s2 = 0000
s3 = 0001
```

The XOR array is `[1,0,0,0]`. Rotating `s3` by one step moves its `1` into the first position, producing correlation `1`. The algorithm finds this through the cyclic correlation extracted from the convolution.

Consider:

```
n = 5
s1 = 11111
s2 = 11111
s3 = 00000
```

Here `base = 5` because every position already contains two ones. The XOR array is all zeros, so every correlation is zero. The algorithm returns `5`, correctly recognizing that no rotation can improve or damage the score.

These cases cover minimum length, wrap-around alignment, and situations where the answer is already fixed before any rotation is applied.
