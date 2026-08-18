---
title: "CF 102218K - K-th Missing Digit"
description: "We have two very large decimal integers, A and B, and a decimal string P that should equal their product. Exactly one digit of P has been replaced by . The missing digit is guaranteed to be from 1 through 9, so the task is to recover that digit."
date: "2026-08-18T22:50:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "K"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 251
verified: false
draft: false
---

[CF 102218K - K-th Missing Digit](https://codeforces.com/problemset/problem/102218/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We have two very large decimal integers, `A` and `B`, and a decimal string `P` that should equal their product. Exactly one digit of `P` has been replaced by `*`. The missing digit is guaranteed to be from `1` through `9`, so the task is to recover that digit.

The first three numbers, `a`, `b`, and `p`, are the digit counts of `A`, `B`, and `P`. They are not the numerical values of those integers. The two input integers can each contain almost one million digits, while the product can contain almost two million digits. The original problem has a 0.5 second time limit and 32 MB memory limit.

Those bounds immediately rule out treating `A` and `B` as ordinary machine integers. Even storing or multiplying million-digit values requires substantially more work than a constant-time arithmetic operation. The intended solution has to process the decimal strings directly and make only a constant amount of work per input digit, giving linear complexity in the total input size.

There are several cases where a careless solution can go wrong. If the missing character is the first digit, it must still be included in the arithmetic. For example,

```
1 1 2
3
8
2*
```

has product `24`, so the answer is `4`. A solution that accidentally skips the `*` position when computing the digit sum would use only the visible digit `2` and obtain the wrong residue.

The missing character can also be the last digit. For example,

```
1 1 2
7
8
5*
```

has product `56`, so the answer is `6`. Treating the star as a separator rather than as an unknown digit must still leave its contribution to the decimal digit sum to be recovered.

A particularly easy boundary case occurs when the required residue modulo 9 is zero. Since zero itself is forbidden, the correct missing digit is `9`, not `0`. For example,

```
1 1 1
9
1
*
```

has product `9`, so the answer is `9`.

## Approaches

A direct approach would be to try every possible missing digit from `1` through `9`, replace `*` with that digit, and check whether the resulting number is exactly `A * B`. The method is correct because one of the nine replacements is the real product, and the statement guarantees that the missing digit is nonzero.

The problem is the size of the numbers. In the largest case, `A` and `B` each have up to `999999` digits and `P` has almost two million digits. Constructing and multiplying the two enormous integers is far beyond ordinary fixed-width arithmetic. Even if we already had the product, checking all nine candidates by scanning the product would require up to `9p`, which is almost 18 million character checks in the largest input. The multiplication itself is much more expensive than that if implemented naively.

The key observation is that decimal numbers preserve their value modulo 9 through their digit sums. For every decimal integer `X`,

[
X \equiv \text{sum of the digits of }X \pmod 9.
]

Since

[
P=A\cdot B,
]

we consequently have

[
\operatorname{sumDigits}(P)
\equiv
\operatorname{sumDigits}(A)\operatorname{sumDigits}(B)
\pmod 9.
]

Every visible digit of `P` contributes a known amount to its digit sum. If the missing digit is `x`, then

(\text{digit sum of }A\bmod9)
(\text{digit sum of }B\bmod9)\bmod9.
]

Thus we only need to compute three small residues while reading the strings. No large integer multiplication is needed at all.

The missing digit is restricted to `1` through `9`. These nine digits have nine different residues modulo 9, so the required residue uniquely identifies the answer. In particular, residue `0` corresponds to digit `9`.

The brute-force idea works because only nine digits are possible, but it still treats the enormous product as a number that must be constructed or repeatedly checked. The observation that multiplication and decimal digit sums interact cleanly modulo 9 removes the large-number operation entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(p) plus huge-integer multiplication | O(p) | Too slow |
| Optimal | O(a + b + p) | O(a + b + p) for input strings | Accepted |

## Algorithm Walkthrough

1. Read the digit counts and the three strings. The counts are not needed for the computation, because the strings themselves tell us exactly which digits must be processed.
2. Compute the sum of the digits of `A` modulo 9. We only need the remainder, since the final equation is also modulo 9.
3. Compute the sum of the digits of `B` modulo 9 for the same reason.
4. Scan `P` and add every character other than `*` to a running digit sum modulo 9. The star contributes an unknown value, so leave it out for now.
5. Compute the required product residue

[
r=(A\bmod9)(B\bmod9)\bmod9.
]

1. Solve

[
(\text{visibleSum}+x)\bmod9=r.
]

The candidate `x` is the unique digit from `1` through `9` having that residue modulo 9. In code, this can be written as

[
x=(r-\text{visibleSum})\bmod9,
]

followed by changing `0` to `9`.

1. Print `x`. The uniqueness of the residue among the allowed digits means there is no need to construct the product or test multiple candidates.

### Why it works

The invariant is that every processed decimal string is represented only by its digit sum modulo 9, which is exactly the same residue as the integer represented by that string. For `A` and `B`, their residues can be multiplied to obtain the residue of their product. For `P`, all visible digits give a known residue and the missing digit contributes exactly `x`. The computed value of `x` makes the two residues equal, and because digits `1` through `9` represent every residue modulo 9 exactly once, that `x` is the only possible missing digit.

## Python Solution

```python
import sys
input = sys.stdin.readline

def digit_sum_mod9(s):
    total = 0
    for c in s:
        if c != '\n':
            total += ord(c) - ord('0')
    return total % 9

def solve():
    a, b, p = map(int, input().split())
    A = input().strip()
    B = input().strip()
    P = input().strip()

    ra = digit_sum_mod9(A)
    rb = digit_sum_mod9(B)

    visible = 0
    for c in P:
        if c != '*':
            visible += ord(c) - ord('0')
    visible %= 9

    required = (ra * rb) % 9
    answer = (required - visible) % 9

    if answer == 0:
        answer = 9

    print(answer)

if __name__ == "__main__":
    solve()
```

The helper `digit_sum_mod9` processes a decimal string character by character instead of converting it to an integer. That is necessary because the input integers can contain almost one million digits, far beyond normal machine integer sizes.

For `P`, the code skips only `*`. Every actual digit is included in the visible digit sum. The use of `ord(c) - ord('0')` avoids creating temporary integer objects through repeated conversions and keeps the computation simple.

The expression `(required - visible) % 9` gives a value from `0` through `8`. If it gives `1` through `8`, that value is already the corresponding missing digit. If it gives `0`, the missing digit must be `9`, because `0` is explicitly excluded by the problem.

There is no integer overflow issue because every running sum is reduced modulo 9 after each complete string, and even the unreduced `visible` sum is at most about 18 million. More importantly, the code never constructs `A * B`.

## Worked Examples

For Sample 1,

```
1 1 2
3
8
2*
```

the relevant state changes are:

| Variable | State |
| --- | --- |
| `ra = digitSum(A) mod 9` | 3 |
| `rb = digitSum(B) mod 9` | 8 |
| `required = ra * rb mod 9` | 6 |
| `visible = digitSum("2") mod 9` | 2 |
| `answer = (6 - 2) mod 9` | 4 |

The product must have digit sum congruent to `3 * 8 = 24`, which is `6` modulo 9. The visible digit contributes `2`, so the missing digit contributes `4`. The completed product is `24`, confirming the result.

For Sample 2,

```
2 2 3
10
10
*00
```

the state is:

| Variable | State |
| --- | --- |
| `ra = digitSum(A) mod 9` | 1 |
| `rb = digitSum(B) mod 9` | 1 |
| `required = ra * rb mod 9` | 1 |
| `visible = digitSum("00") mod 9` | 0 |
| `answer = (1 - 0) mod 9` | 1 |

The star is the first character, so this example also verifies that the missing position itself does not need special handling. The completed product is `100`, and the answer is `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(a + b + p) | Each input digit is processed once. |
| Space | O(a + b + p) | The input strings are stored, while the computation itself uses O(1) additional space. |

With `a` and `b` below one million and `p` below two million, the algorithm performs only a few million simple character operations. It never performs multiplication on the million-digit integers, so the running time scales linearly with the input size and the extra working memory is constant beyond the input strings.

The original contest uses a 0.5 second limit and 32 MB memory limit. The underlying algorithm is designed specifically to avoid large-number arithmetic, which is the essential requirement for those limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    a, b, p = map(int, input().split())
    A = input().strip()
    B = input().strip()
    P = input().strip()

    ra = 0
    for c in A:
        ra = (ra + ord(c) - 48) % 9

    rb = 0
    for c in B:
        rb = (rb + ord(c) - 48) % 9

    visible = 0
    for c in P:
        if c != '*':
            visible = (visible + ord(c) - 48) % 9

    answer = (ra * rb - visible) % 9
    if answer == 0:
        answer = 9

    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert run("""1 1 2
3
8
2*
""") == "4", "sample 1"

assert run("""2 2 3
10
10
*00
""") == "1", "sample 2"

assert run("""1 1 1
1
1
*
""") == "1", "minimum-size input"

assert run("""1 1 1
9
1
*
""") == "9", "residue zero must map to digit 9"

assert run("""1 1 2
7
8
5*
""") == "6", "missing digit at the end"

assert run("""2 2 3
11
11
1*1
""") == "2", "equal operands"

# Maximum-size valid construction:
# A = 1 followed by 999998 zeros
# B = 1 followed by 999998 zeros
# A * B = 1 followed by 1999996 zeros.
# The star replaces the leading 1.
n = 999999
A = "1" + "0" * (n - 1)
B = "1" + "0" * (n - 1)
P = "*" + "0" * (2 * n - 2)

max_case = f"{n} {n} {2 * n - 1}\n{A}\n{B}\n{P}\n"
assert run(max_case) == "1", "maximum-size input"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1 / 1 / *` | `1` | Smallest possible input and direct residue calculation |
| `1 1 1 / 9 / 1 / *` | `9` | The modulo 9 residue `0` must produce digit `9` |
| `1 1 2 / 7 / 8 / 5*` | `6` | Missing digit at the final position |
| `2 2 3 / 11 / 11 / 1*1` | `2` | Equal operands and an interior missing digit |
| Maximum-size powers of ten | `1` | Near-limit string lengths and leading missing digit |

## Edge Cases

The first edge case is a missing leading digit. For

```
2 2 3
10
10
*00
```

we get `A mod 9 = 1` and `B mod 9 = 1`, so the product must be `1` modulo 9. The visible part `00` contributes zero, giving `x = 1`. The algorithm never assumes that the star is somewhere after the first character, so it handles this naturally.

The second edge case is a missing final digit. For

```
1 1 2
7
8
5*
```

the product is `56`. The operand residues are `7` and `8`, giving `56 mod 9 = 2`. The visible digit `5` has residue `5`, so

[
x\equiv2-5\equiv6\pmod9.
]

The answer is `6`, and the completed string is `56`.

The third edge case is a required residue of zero. For

```
1 1 1
9
1
*
```

the product residue is `9 * 1 mod 9 = 0`, while the visible sum is zero. The arithmetic gives candidate `0`, but zero is not an allowed missing digit. The only allowed digit congruent to zero modulo 9 is `9`, so the algorithm converts the intermediate zero to `9`.

The fourth edge case is the maximum input size. Let both operands be `1` followed by `999998` zeros. Their product is `1` followed by `1999996` zeros. Replacing that first `1` by `*` gives a product string of length `1999997`. Both operand digit sums are `1`, and every visible product digit is zero, so the computed answer is immediately `1`. The algorithm processes the large strings once and never attempts to construct their product as an integer.
