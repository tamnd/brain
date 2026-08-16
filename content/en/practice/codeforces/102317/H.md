---
title: "CF 102317H - Count the Dividing Pairs"
description: "We have a list of up to (p) integers, and every ordered pair of positions ((i,j)) is a candidate. The pair is counted when (Ai) is a proper divisor of (Aj), meaning (Aj) is an integer multiple of (Ai), but the two values are not equal."
date: "2026-08-16T19:02:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102317
codeforces_index: "H"
codeforces_contest_name: "UCF Locals 2016"
rating: 0
weight: 102317
solve_time_s: 449
verified: true
draft: false
---

[CF 102317H - Count the Dividing Pairs](https://codeforces.com/problemset/problem/102317/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a list of up to (p) integers, and every ordered pair of positions ((i,j)) is a candidate. The pair is counted when (A_i) is a proper divisor of (A_j), meaning (A_j) is an integer multiple of (A_i), but the two values are not equal. Equal values never form a proper dividing pair, even when the value occurs several times. The input values range from (0) to (10^7), while (p) can reach (10^6). The official statement also gives a special rule for zero: zero divides nothing, while every nonzero integer is a proper divisor of zero.

The output is the number of ordered index pairs satisfying that condition. Multiplicity matters, so if the value (2) appears three times and (6) appears twice, those occurrences contribute (3\cdot2=6) pairs with divisor (2) and dividend (6). The official format is `Test case #t: m`, followed by a blank line.

The main constraint changes the shape of the solution. With (p=10^6), checking every ordered pair would require (10^{12}) divisibility tests in the worst case, which is far beyond a five-second limit. The values are bounded by only (10^7), though, and that bounded value range is exactly what lets us replace pair enumeration with a multiples sieve. The contest gives five seconds and 256 MB, so the intended approach needs to exploit the value bound rather than the number of pairs.

There are several edge cases that can silently break an otherwise reasonable implementation.

Consider

```
1
2
1 1
```

The answer is `0`. Although (1) divides (1), a proper divisor must be different from the number it divides. A solution that checks only `N % D == 0` would incorrectly count both ordered pairs.

Consider

```
1
2
0 5
```

The answer is `1`, because ((5,0)) is a proper dividing pair. The pair ((0,5)) is not valid because zero is not a divisor of any number. A solution that simply tests `N % D == 0` cannot even evaluate the zero-divisor case safely.

Consider

```
1
4
1 2 2 4
```

The answer is `5`. The two copies of (2) are distinct elements, so each can serve as the divisor of (4), giving two pairs. The value (1) divides both copies of (2) and (4), giving three more. Treating the input as a set instead of a multiset would lose those multiplicities.

## Approaches

The direct approach is to inspect every ordered pair of positions. For each pair ((i,j)), we check whether (A_i) is nonzero, whether (A_i\neq A_j), and whether (A_j) is divisible by (A_i). This is correct because it applies the definition directly to every possible pair. The problem is the (O(p^2)) number of checks. At (p=10^6), the worst case contains (10^{12}) ordered pairs, so even a very cheap divisibility test cannot make this approach viable.

The useful observation is that the condition depends only on the values, not on the positions. Suppose a positive value (d) occurs (freq[d]) times. Every positive multiple (2d,3d,\ldots) that occurs in the input can be its dividend. If (m) is such a multiple, then every occurrence of (d) pairs with every occurrence of (m), contributing

[
freq[d]\cdot freq[m].
]

We can count these contributions by fixing the divisor value (d) and walking through its multiples. The value (d) itself is deliberately skipped, because equality is forbidden.

Zero can be handled separately. Every positive input value is a proper divisor of zero, so if `zero_count` is the number of zeros and `positive_count` is the number of positive elements, zero contributes exactly

[
positive_count\cdot zero_count.
]

Zero itself contributes nothing as a divisor.

The brute-force method works because it explicitly considers every pair, but fails because there are too many pairs. The observation that all possible dividends of a fixed positive divisor are its multiples lets us aggregate equal values first and enumerate divisibility relationships over the bounded value domain.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(p^2)) | (O(1)) besides input | Too slow |
| Multiples Sieve | (O(M\log M)) in the full value range, with (M\le10^7) | (O(M)) | Accepted |

Here (M) is the largest value actually appearing in the test case. Since (p\le10^6), at most (10^6) distinct positive values can actually occur, so the number of visited multiples is often substantially smaller than the theoretical (M\log M) bound.

## Algorithm Walkthrough

1. Read the (p) values and find the largest value (M). We only need frequency information up to (M), so allocating space up to the fixed upper bound (10^7) is unnecessary when the actual maximum is smaller.
2. Build a frequency array `freq`, where `freq[x]` is the number of occurrences of value (x). An array is preferable to a dictionary because the algorithm repeatedly accesses frequencies at exact multiples, and the value range is bounded.
3. Count zeros separately. A zero can never be the divisor in a valid pair, but every positive value can be the divisor of every zero.
4. Initialize the answer with `positive_count * zero_count`. This accounts for every pair whose dividend is zero and whose divisor is positive.
5. For every positive value (d) that occurs in the input, walk through `2*d, 3*d, ...` while the multiple is at most (M). These are exactly the positive values that (d) divides and that are different from (d).
6. For every multiple (m), add `freq[d] * freq[m]` to the answer. The first factor chooses an occurrence of the divisor, and the second chooses an occurrence of the dividend. Starting from `2*d` rather than `d` automatically excludes equal values.
7. Print the accumulated answer in the required test-case format and add the required blank line.

The key invariant is that after processing a divisor value (d), every valid pair whose divisor value is (d) and whose dividend is positive has been counted exactly once. It is counted when the outer loop reaches (d), because every positive divisible value appears in the multiples loop, and the product of the two frequencies counts every combination of their occurrences. No pair with equal values is counted because the multiples loop starts at (2d), and no pair involving zero as a divisor is counted because the outer loop starts at (1). The separate zero contribution accounts for every remaining valid pair involving zero.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve_case(a):
    n = len(a)
    mx = max(a)

    zero_count = 0
    for x in a:
        if x == 0:
            zero_count += 1

    positive_count = n - zero_count

    # An unsigned 32-bit integer is enough because n <= 10^6.
    freq = array('I', [0]) * (mx + 1)

    for x in a:
        freq[x] += 1

    # Every positive number is a proper divisor of zero.
    ans = positive_count * zero_count

    # For each divisor d, inspect only its proper positive multiples.
    for d in range(1, mx + 1):
        cd = freq[d]
        if cd == 0:
            continue

        for m in range(d + d, mx + 1, d):
            cm = freq[m]
            if cm:
                ans += cd * cm

    return ans

def main():
    t = int(input())
    out = []

    for tc in range(1, t + 1):
        p = int(input())

        a = []
        while len(a) < p:
            a.extend(map(int, input().split()))

        ans = solve_case(a)
        out.append(f"Test case #{tc}: {ans}")
        out.append("")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The `solve_case` function first determines the actual maximum value, which keeps the frequency array as small as possible. With a maximum of (10^7), an unsigned 32-bit entry is sufficient because every frequency is at most (10^6). The `array` module avoids the much larger memory cost of storing millions of Python integer objects.

The zero contribution is calculated before the multiples loop. If there are `positive_count` positive elements and `zero_count` zeros, every positive element can occupy the divisor position while every zero can occupy the dividend position, producing their Cartesian product.

The main loop begins at `d + d`. This single boundary choice handles the proper-divisor restriction without needing a separate equality check. Starting at `d` and adding `freq[d] * freq[d]` would be wrong because equal values are not proper dividing pairs.

The multiplication uses Python integers, so there is no overflow problem. In a language with fixed-width integers, a 64-bit type is necessary because the number of valid ordered pairs can be on the order of (p^2), which can reach (10^{12}).

The input reader allows the (p) values to span multiple physical lines even though the official format presents them as one line. This makes the parser robust without changing the algorithm.

## Worked Examples

The official problem archive describes the sample section, but the extracted statement available through the contest archive does not expose the sample input and output values themselves. The following two examples are consequently constructed to show the important cases directly.

Consider

```
1
4
1 2 2 4
```

The frequency state is `freq[1] = 1`, `freq[2] = 2`, and `freq[4] = 1`. There are no zeros.

| Divisor `d` | `freq[d]` | Multiples visited | Added contribution | Running answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2, 4 | (1\cdot2 + 1\cdot1 = 3) | 3 |
| 2 | 2 | 4 | (2\cdot1 = 2) | 5 |
| 4 | 1 | none | 0 | 5 |

The three pairs contributed by divisor (1) are the two occurrences of (2) and the one occurrence of (4). The two occurrences of (2) each divide the occurrence of (4), giving two more. The final output is `Test case #1: 5`.

Now consider

```
1
3
0 5 10
```

There is one zero and two positive values. The zero contribution is already (2), because both (5) and (10) are proper divisors of zero.

| Divisor `d` | `freq[d]` | Multiples visited | Added contribution | Running answer |
| --- | --- | --- | --- | --- |
| 1 | 0 | none | 0 | 2 |
| 5 | 1 | 10 | (1\cdot1 = 1) | 3 |
| 10 | 1 | none | 0 | 3 |

The final answer is `3`. The three pairs are ((5,0)), ((10,0)), and ((5,10)). The zero never appears as a divisor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(M\log M)) worst case | For divisor (d), at most (M/d-1) multiples are inspected, and the harmonic sum is (O(M\log M)). |
| Space | (O(M)) | The frequency array stores one 32-bit count for every value from (0) through (M). |

The maximum value is (10^7), while the number of input elements is at most (10^6). The bounded value range makes the multiples sieve feasible, whereas (O(p^2)) pair enumeration would require up to (10^{12}) checks. The contest memory limit is 256 MB, and the Python implementation uses a compact 32-bit frequency array rather than a Python list of integer objects.

## Test Cases

```python
# helper: run the solution on an input string
import io
import sys
from array import array

def solve_case(a):
    n = len(a)
    mx = max(a)

    zero_count = 0
    for x in a:
        if x == 0:
            zero_count += 1

    positive_count = n - zero_count

    freq = array('I', [0]) * (mx + 1)

    for x in a:
        freq[x] += 1

    ans = positive_count * zero_count

    for d in range(1, mx + 1):
        cd = freq[d]
        if cd == 0:
            continue

        for m in range(d + d, mx + 1, d):
            cm = freq[m]
            if cm:
                ans += cd * cm

    return ans

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)

        t = int(sys.stdin.readline())
        out = []

        for tc in range(1, t + 1):
            p = int(sys.stdin.readline())

            a = []
            while len(a) < p:
                a.extend(map(int, sys.stdin.readline().split()))

            out.append(f"Test case #{tc}: {solve_case(a)}")
            out.append("")

        return "\n".join(out)
    finally:
        sys.stdin = old_stdin

# Minimum-size input. 1 divides 0, so there is one valid pair.
assert run("1\n2\n0 1\n") == "Test case #1: 1\n", "minimum size"

# All values equal. Divisibility alone is not enough because equal values
# cannot form proper dividing pairs.
assert run("1\n4\n7 7 7 7\n") == "Test case #1: 0\n", "all equal"

# Duplicates must be counted by occurrence.
# 1 divides both 2s and 4: 3 pairs.
# Each of the two 2s divides 4: 2 pairs.
assert run("1\n4\n1 2 2 4\n") == "Test case #1: 5\n", "duplicates"

# Zero boundary case.
# 5 and 10 divide 0, and 5 divides 10.
assert run("1\n3\n0 5 10\n") == "Test case #1: 3\n", "zero handling"

# Maximum value boundary.
# Two copies of 10^7 are both proper divisors of zero.
assert run("1\n3\n10000000 10000000 0\n") == "Test case #1: 2\n", "maximum value"

# Maximum-size input, with all values equal.
# There are 10^6 equal values, but none can divide another properly.
max_n = 10**6
max_input = "1\n" + str(max_n) + "\n" + ("1 " * max_n)
assert run(max_input) == "Test case #1: 0\n", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 0 1` | `Test case #1: 1` | Minimum size and the special zero rule |
| `4 / 7 7 7 7` | `Test case #1: 0` | Equal values must not be counted |
| `4 / 1 2 2 4` | `Test case #1: 5` | Duplicate occurrences contribute independently |
| `3 / 0 5 10` | `Test case #1: 3` | Zero as a dividend and ordinary divisibility |
| `3 / 10000000 10000000 0` | `Test case #1: 2` | Maximum value boundary and duplicate maximum values |
| (10^6) copies of `1` | `Test case #1: 0` | Maximum input size and the fact that (p), not the number of distinct values, controls multiplicity |

## Edge Cases

For equal values, consider

```
1
2
1 1
```

The frequency array contains `freq[1] = 2`. The outer loop reaches (d=1), but its multiples loop starts at (2), so there are no positive multiples to inspect. The zero count is also zero, leaving the answer at zero. This directly enforces the strict condition (D\neq N).

For zero as a divisor, consider

```
1
2
0 5
```

The positive count is one and the zero count is one, so the initial answer is (1\cdot1=1). The multiples loop never processes (d=0), correctly avoiding the invalid idea that zero divides another value. The result is `Test case #1: 1`.

For zero as a dividend, consider

```
1
3
0 5 10
```

The initial zero contribution is (2), accounting for ((5,0)) and ((10,0)). The divisor (5) then finds (10) as a proper positive multiple and adds one more pair. The result is three. This case demonstrates why zero cannot simply be ignored.

For duplicates, consider

```
1
4
1 2 2 4
```

When (d=1), `freq[1]` is one, `freq[2]` is two, and `freq[4]` is one, so the contribution is three. When (d=2), its frequency is two and the frequency of its proper multiple (4) is one, so two more pairs are added. The answer is five. The algorithm works with frequencies precisely because every occurrence of the divisor can pair with every occurrence of the dividend.

For the largest possible value, consider

```
1
3
10000000 10000000 0
```

The two copies of (10^7) are both proper divisors of zero, contributing two pairs. Since there is no larger positive multiple within the allowed value range, the multiples loop for (10^7) performs no iterations. Equal copies of (10^7) are not counted. The result is `Test case #1: 2`.

For the maximum input size, one useful stress case is one million copies of the same value:

```
1
1000000
1 1 1 1 ...
```

There are no zeros, and the only distinct divisor value is (1). Its multiples begin at (2), whose frequency is zero, so the answer remains zero. More generally, this case demonstrates why the algorithm depends on the number of distinct values for its actual multiples work, while still correctly preserving the multiplicity of all one million input elements.
