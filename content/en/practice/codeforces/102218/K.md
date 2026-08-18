---
title: "CF 102218K - K-th Missing Digit"
description: "We have two positive integers, (A) and (B), but their lengths can be enormous. Their product (A times B) is given as a decimal string with exactly one digit replaced by ."
date: "2026-08-18T12:50:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "K"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 109
verified: false
draft: false
---

[CF 102218K - K-th Missing Digit](https://codeforces.com/problemset/problem/102218/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We have two positive integers, (A) and (B), but their lengths can be enormous. Their product (A \times B) is given as a decimal string with exactly one digit replaced by `*`. The missing digit is guaranteed to be one of (1,\ldots,9), so we need to recover that single digit without necessarily constructing the potentially huge product.

The first line gives the lengths of (A), (B), and the product representation. The next two lines contain the decimal representations of (A) and (B), and the final line contains the product with one unknown digit. The length bounds are the key detail. (A) and (B) may each contain almost one million digits, so treating them as ordinary machine integers is impossible. Even arbitrary-precision multiplication of two million-digit numbers would be far beyond what this problem needs.

The useful operation must consequently be linear in the number of input digits. Scanning each string once is feasible, while actually multiplying (A) and (B) would require at least quadratic work with ordinary digit multiplication. The product itself can also have nearly two million digits, so storing or recomputing it through general big-integer arithmetic is unnecessary.

There are several edge cases that can break a careless implementation. The first is when the missing digit is `9`. For example,

```
1 1 2
3
3
2*
```

The product is `9`, so the answer is `9`. A solution that only considers digits `1` through `8`, or interprets a remainder of zero as digit `0`, would fail.

The second edge case is when the missing digit occurs at the beginning of the product. For example,

```
2 2 3
10
10
*00
```

The product is `100`, so the answer is `1`. The position of `*` does not matter to the method because every decimal position contributes its digit to the same modulo-9 value.

The third case is a missing digit at the end, as in the first sample. The representation `2*` means that the product is `24`, not merely that some intermediate arithmetic has to be performed. Since the missing digit contributes exactly its own value modulo 9, its location also does not affect the calculation.

## Approaches

A direct brute-force idea would be to replace `*` by each possible nonzero digit from `1` to `9`, then check which completed string is equal to (A\times B). This is logically correct because exactly one candidate represents the real product. The problem is that checking the candidates requires dealing with multiplication of numbers containing up to nearly one million digits. With ordinary long multiplication, one multiplication can require (O(ab)) digit operations, where (a) and (b) are the lengths of (A) and (B). Trying nine candidates therefore costs (O(9ab)=O(ab)), which is on the order of (10^{12}) elementary digit operations near the largest lengths. That is completely impractical.

The key observation is that decimal numbers have a simple relationship with their digit sums modulo 9. For every decimal integer (X),

[
X \equiv \text{sum of digits of }X \pmod 9.
]

The same congruence also respects multiplication, so

[
A\times B \equiv (A\bmod 9)(B\bmod 9)\pmod 9.
]

We can compute (A\bmod9) and (B\bmod9) by scanning their digits. We can also compute the sum modulo 9 of all known digits in the product. If the missing digit is (d), then

[
d+\text{known digit sum}
\equiv A\times B
\pmod9.
]

Thus

[
d\equiv (A\bmod9)(B\bmod9)-\text{known digit sum}\pmod9.
]

There is one small ambiguity because the residues modulo 9 are (0,\ldots,8), while the answer is guaranteed to be (1,\ldots,9). The digit `9` has residue `0`, so whenever the computed residue is zero, the answer must be `9`. Every other residue directly identifies the missing digit.

The brute-force approach works because testing all nine digits exhausts every possible answer, but it fails because it requires huge-number multiplication. The observation that only the product modulo 9 matters reduces the entire problem to three linear scans of the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(9ab)) with ordinary multiplication | (O(a+b)) plus product storage | Too slow |
| Optimal | (O(a+b+p)) | (O(a+b+p)) for the input strings | Accepted |

## Algorithm Walkthrough

1. Read the lengths and the three decimal strings. The length values are not needed for the mathematics, because the strings themselves tell us exactly which digits must be processed.
2. Compute (A\bmod9) by scanning every digit of (A). For each character, convert it to its numeric value and update the remainder with

[
r=(10r+d)\bmod9.
]

Since (10\equiv1\pmod9), this is equivalent to simply adding all digits modulo 9.
3. Compute (B\bmod9) in the same way. No conversion to a Python integer is attempted, because these strings may contain hundreds of thousands of digits.
4. Scan the product string (P) and add every digit except `*` modulo 9. The unknown digit is deliberately excluded because it is the value we are solving for.
5. Let the missing digit be (d). The completed product must satisfy

[
d+\text{known}\equiv (A\bmod9)(B\bmod9)\pmod9.
]

Rearranging gives

[
d\equiv (A\bmod9)(B\bmod9)-\text{known}\pmod9.
]
6. Normalize the result into the range (0,\ldots,8). If it is nonzero, print it directly. If it is zero, print `9`, because the problem guarantees that the missing digit is nonzero and `9` is the only nonzero decimal digit congruent to zero modulo 9.

### Why it works

The invariant is that every processed decimal string is represented by its exact value modulo 9. Decimal notation preserves this residue because (10\equiv1\pmod9). Consequently, after scanning (A) and (B), their stored residues are exactly (A\bmod9) and (B\bmod9). After scanning the known product digits, the stored sum is exactly the contribution of every known digit modulo 9. The actual product has residue ((A\bmod9)(B\bmod9)), so the only missing contribution must be the missing digit (d). The resulting congruence determines (d) uniquely among (1,\ldots,9), since those nine digits have distinct residues modulo 9.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mod9(s):
    r = 0
    for ch in s:
        if ch != '\n':
            r = (r + ord(ch) - ord('0')) % 9
    return r

def solve():
    a, b, p = map(int, input().split())
    A = input().strip()
    B = input().strip()
    P = input().strip()

    ra = mod9(A)
    rb = mod9(B)

    known = 0
    for ch in P:
        if ch != '*':
            known = (known + ord(ch) - ord('0')) % 9

    missing = (ra * rb - known) % 9

    if missing == 0:
        missing = 9

    print(missing)

if __name__ == "__main__":
    solve()
```

The `mod9` function implements the first two algorithm steps. It scans a decimal string and accumulates its digit sum modulo 9. Using `ord(ch) - ord('0')` avoids any integer conversion of the entire string and processes each character in constant time.

The product string is handled separately because it contains `*`. Every ordinary digit contributes to the known part of the product's digit sum, while `*` is skipped. There is no need to remember its position.

The expression `(ra * rb - known) % 9` is Python-safe even when the subtraction is negative, because Python's modulo operation returns a value in the range (0,\ldots,8). The final conversion from `0` to `9` handles the only residue that corresponds to two decimal digits, `0` and `9`. Since `0` is forbidden by the input guarantee, `9` is the only valid answer.

There is also no integer-overflow issue in this implementation. The only arithmetic performed on values derived from the huge input strings is modulo 9, so the intermediate values remain tiny.

## Worked Examples

### Sample 1

The input is

```
1 1 2
3
8
2*
```

The scan states are:

| Stage | (A\bmod9) | (B\bmod9) | Known product sum mod 9 | Missing residue |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | 0 |
| After `A = 3` | 3 | 0 | 0 | 0 |
| After `B = 8` | 3 | 8 | 0 | 0 |
| After product digit `2` | 3 | 8 | 2 | 22 mod 9 = 4 |

The product residue is (3\times8=24\equiv6\pmod9). The known digit contributes `2`, so the missing digit must satisfy (2+d\equiv6\pmod9), giving (d=4). The completed product is `24`.

### Sample 2

The input is

```
2 2 3
10
10
*00
```

The scan proceeds as follows:

| Stage | (A\bmod9) | (B\bmod9) | Known product sum mod 9 | Missing residue |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | 0 |
| After `A = 10` | 1 | 0 | 0 | 0 |
| After `B = 10` | 1 | 1 | 0 | 0 |
| After product `0` | 1 | 1 | 0 | 1 |
| After product `0` | 1 | 1 | 0 | 1 |

The product residue is (1\times1=1). Both known product digits are zero, so the missing digit has residue 1 and is consequently `1`. The completed product is `100`.

This example also demonstrates that a leading `*` needs no special handling. Its position is irrelevant because the digit-sum property treats every decimal position uniformly modulo 9.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(a+b+p)) | Each digit of (A), (B), and (P) is scanned once. |
| Space | (O(a+b+p)) | The three input strings are stored; the algorithm itself uses (O(1)) additional space. |

With (a) and (b) potentially close to one million, linear processing is the appropriate target. The algorithm performs only a few arithmetic operations per input character and never constructs the enormous product, so its running time and memory usage are both proportional to the input size.

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
    for ch in A:
        ra = (ra + ord(ch) - ord('0')) % 9

    rb = 0
    for ch in B:
        rb = (rb + ord(ch) - ord('0')) % 9

    known = 0
    for ch in P:
        if ch != '*':
            known = (known + ord(ch) - ord('0')) % 9

    answer = (ra * rb - known) % 9
    if answer == 0:
        answer = 9

    print(answer)

def run(inp: str) -> str:
    global_input = sys.stdin
    global_output = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    result = sys.stdout.getvalue().strip()

    sys.stdin = global_input
    sys.stdout = global_output
    return result

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
3
3
*
""") == "9", "minimum-size input and missing 9"

assert run("""1 1 2
9
9
8*
""") == "1", "boundary residue calculation"

assert run("""3 3 6
111
111
12321*
""") == "9", "all-equal values and missing 9"

assert run("""5 5 10
99999
99999
999980000*
""") == "1", "large digit strings and trailing missing digit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 3 / 3 / *` | `9` | Smallest possible input and the special residue-zero case |
| `1 1 2 / 9 / 9 / 8*` | `1` | Arithmetic near a modulo-9 boundary |
| `3 3 6 / 111 / 111 / 12321*` | `9` | Repeated digits and the answer `9` |
| `5 5 10 / 99999 / 99999 / 999980000*` | `1` | Longer strings and a missing digit at the end |

The final custom case uses `99999^2=9999800001`, so the given representation `999980000*` requires the trailing digit `1`. It also confirms that the algorithm does not rely on the missing digit appearing near the beginning of the product.

## Edge Cases

A missing digit of `9` is the most important modulo-specific edge case. Consider

```
1 1 1
3
3
*
```

The product is `9`. We calculate (3\times3\equiv0\pmod9), while the known product digit sum is zero because there are no known digits. The computed missing residue is therefore zero. The algorithm converts that residue to `9`, rather than incorrectly printing `0`.

A missing digit at the beginning requires no separate branch. For

```
2 2 3
10
10
*00
```

we have (10\bmod9=1) for both operands. The product therefore has residue 1. The known digits contribute zero, so the missing digit has residue 1 and the algorithm prints `1`. The same calculation works regardless of whether `*` is the first, middle, or last character.

A missing digit at the end is handled identically. For

```
1 1 2
3
8
2*
```

the product residue is (3\times8\equiv6\pmod9), while the known digit contributes 2. The missing digit is (6-2\equiv4\pmod9), so the output is `4`. There is no off-by-one issue involving the final character because the algorithm only distinguishes `*` from ordinary digits.

Finally, the huge-input case is handled without converting the numbers to native integers. If (A) contains 999,999 digits, the code still performs only 999,999 small additions and modulo operations. The product is never constructed, so the algorithm remains linear even when the actual multiplication would be far too expensive.
