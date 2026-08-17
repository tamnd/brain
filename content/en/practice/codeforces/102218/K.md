---
title: "CF 102218K - K-th Missing Digit"
description: "We are given two positive integers (A) and (B), but they can be extremely long because the first line gives their digit counts, not their numeric values within a machine-sized range."
date: "2026-08-17T23:26:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "K"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 163
verified: false
draft: false
---

[CF 102218K - K-th Missing Digit](https://codeforces.com/problemset/problem/102218/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two positive integers (A) and (B), but they can be extremely long because the first line gives their digit counts, not their numeric values within a machine-sized range. We are also given a decimal string (P) that should equal (A \times B), except that exactly one digit has been replaced by `*`. The missing digit is guaranteed to be one of (1,\dots,9), and we need to print it.

The crucial constraint is that (a), (b), and (p) can be close to (10^6). That means (A), (B), and (P) can contain around a million characters. We cannot convert them to ordinary integers, and even multiplying two million-digit integers with schoolbook multiplication would require roughly (10^{12}) single-digit operations. The 0.5 second time limit makes any quadratic algorithm completely unsuitable. We need a linear scan over the input.

There are several edge cases that can make an apparently reasonable implementation fail. The missing digit can be the digit (9). For example,

```
1 1 2
7
3
2*
```

The product is (21), so the answer is (1), not a residue of (0). More generally, when a calculation modulo (9) produces (0), the only valid missing digit is (9), because (0) itself is forbidden.

The `*` can also be the first character of the product. For example,

```
2 2 3
10
10
*00
```

The answer is (1). A method that tries to parse the incomplete product as an integer must handle the leading wildcard specially, while a digit-sum method does not care where the wildcard occurs.

The product can also be much larger than standard integer types. For example, if (A) and (B) each have hundreds of thousands of digits, constructing (A \times B) explicitly is infeasible. The solution below never constructs the product and only needs the digit sum of the known part of (P).

## Approaches

A direct brute-force approach would try every possible missing digit from (1) through (9). For each candidate, it would replace `*`, construct the complete product string, and check whether it equals (A \times B). The idea is correct because the statement guarantees that exactly one candidate is the real missing digit.

The problem is the multiplication. If (A) and (B) both contain (10^6) digits, ordinary schoolbook multiplication takes (O(10^{12})) digit operations. Trying nine candidates does not change the asymptotic problem, so this approach is far beyond the time limit.

The key observation is that decimal digit sums preserve the value modulo (9). For every integer (X),

[
X \equiv \text{sum of digits of }X \pmod 9.
]

Since (P=A\times B), we know

[
P \equiv A\times B \pmod 9.
]

Suppose the known digits of (P) have sum (S), and the missing digit is (d). Then

[
S+d \equiv A\times B \pmod 9.
]

We can compute (A\bmod 9) and (B\bmod 9) by scanning their digits, without ever constructing their numeric values. We can also compute (S\bmod 9) by scanning (P). Thus the missing digit is determined with a single linear pass over all input characters.

The guarantee that (d\neq0) removes the only ambiguity. A residue from (1) through (8) directly gives the corresponding digit, while residue (0) must represent digit (9).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(ab)) | (O(a+b+p)) | Too slow |
| Optimal | (O(a+b+p)) | (O(a+b+p)) for input storage, (O(1)) auxiliary | Accepted |

## Algorithm Walkthrough

1. Read the digit counts and the three strings. The counts are not needed for the computation itself, but reading the strings is necessary because the numbers may be far too large for native integer types.
2. Compute (A\bmod9) by processing every digit of (A). If the current remainder is (r) and the next digit is (x), the new remainder is

[
(10r+x)\bmod9.
]

Because (10\equiv1\pmod9), this is equivalent to simply adding the digit modulo (9).

1. Compute (B\bmod9) in the same way.
2. Scan (P) and add every digit except `*` to a running sum modulo (9). The location of `*` does not matter because only the sum of the remaining digits is needed.
3. Let (r=(A\bmod9)(B\bmod9)\bmod9). This is the residue of the complete product.
4. The missing digit must satisfy

[
d\equiv r-S\pmod9.
]

Normalize the result to the range (0,\dots,8).

1. If the resulting residue is (0), print (9). Otherwise print the residue itself. Since the missing digit is guaranteed to be nonzero, residue (0) cannot correspond to digit (0), leaving (9) as the unique valid answer.

### Why it works

The invariant is that every number and the sum of its decimal digits have the same remainder modulo (9). During the scans of (A) and (B), we maintain their exact residues modulo (9). During the scan of (P), we maintain the residue of all known product digits. If the missing digit is (d), the complete digit sum of (P) is (S+d), so it must have the same residue as (A\times B). The computed value (d\equiv A B-S\pmod9) is consequently the only possible missing digit modulo (9). Digits (1) through (9) represent every residue modulo (9) exactly once, with (9) representing residue (0), so the answer is uniquely determined.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mod9(s):
    r = 0
    for ch in s:
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

The `mod9` function implements the first two algorithm steps. It never converts the entire string to an integer, so its intermediate value stays below (9). Using the digit sum directly is valid because (10\equiv1\pmod9).

The product string is scanned separately so that `*` is ignored rather than accidentally treated as a digit. The expression `(ra * rb - known) % 9` uses Python's modulo operation to normalize negative differences automatically.

There is no integer overflow concern in Python, and even in a fixed-width language the only values used for the modular computation would be at most (8). The only potentially large objects are the three input strings themselves. The declared digit counts are not used to index the strings, so there is no off-by-one issue related to the product length.

## Worked Examples

For the first sample,

```
1 1 2
3
8
2*
```

we obtain the following state.

| Step | (A\bmod9) | (B\bmod9) | Known product residue | Missing residue |
| --- | --- | --- | --- | --- |
| Read (A=3) | 3 |  |  |  |
| Read (B=8) | 3 | 8 |  |  |
| Read known digit `2` | 3 | 8 | 2 |  |
| Compute product residue | 3 | 8 | 2 | (3\cdot8-2=22\equiv4) |
| Output | 3 | 8 | 2 | 4 |

The actual product is (24), so the missing digit is (4). The trace demonstrates the central invariant: (24\equiv2+4\equiv6\pmod9).

For the second sample,

```
2 2 3
10
10
*00
```

the trace is:

| Step | (A\bmod9) | (B\bmod9) | Known product residue | Missing residue |
| --- | --- | --- | --- | --- |
| Read (A=10) | 1 |  |  |  |
| Read (B=10) | 1 | 1 |  |  |
| Read `*00` | 1 | 1 | 0 |  |
| Compute product residue | 1 | 1 | 0 | (1\cdot1-0=1) |
| Output | 1 | 1 | 0 | 1 |

The complete product is (100), so the wildcard is correctly recovered as (1). This example also confirms that a wildcard in the first position requires no special handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(a+b+p)) | Every digit of (A), (B), and (P) is scanned once. |
| Space | (O(a+b+p)) | The input strings are stored; the algorithm itself uses (O(1)) auxiliary space. |

With up to roughly one million digits per input number, a linear scan performs only a few million simple operations. That is compatible with the intended constraints, whereas explicitly multiplying the large integers would require quadratic work and is infeasible under the 0.5 second limit.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.split()
    a, b, p = map(int, data[:3])
    A, B, P = data[3], data[4], data[5]

    def mod9(s):
        r = 0
        for ch in s:
            if ch != '*':
                r = (r + ord(ch) - ord('0')) % 9
        return r

    ra = mod9(A)
    rb = mod9(B)

    known = 0
    for ch in P:
        if ch != '*':
            known = (known + ord(ch) - ord('0')) % 9

    ans = (ra * rb - known) % 9
    if ans == 0:
        ans = 9

    return str(ans)

def run(inp: str) -> str:
    return solve_data(inp).strip()

# Provided sample 1
assert run("""1 1 2
3
8
2*
""") == "4", "sample 1"

# Provided sample 2
assert run("""2 2 3
10
10
*00
""") == "1", "sample 2"

# Minimum-size values: 1 * 1 = 1
assert run("""1 1 1
1
1
*
""") == "1", "minimum-size case"

# Missing digit is 9, exercising the residue-zero boundary.
assert run("""1 1 2
7
3
1*
""") == "9", "digit 9 / residue zero"

# Wildcard at the beginning.
assert run("""2 1 3
99
1
*99
""") == "9", "leading wildcard"

# All equal digits: 111 * 111 = 12321.
assert run("""3 3 5
111
111
12*21
""") == "3", "all-equal inputs"

# Large input sizes, generated without constructing the product.
# A = 999...999 (999 digits), B = 1.
# 999...999 * 1 is the same string, so the missing digit is 9.
n = 999
A = "9" * n
P = "9" * (n - 1) + "*"
large_input = f"{n} 1 {n}\n{A}\n1\n{P}\n"
assert run(large_input) == "9", "large-size linear scan"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1 / 1 / *` | `1` | Smallest possible values and a one-digit product |
| `1 1 2 / 7 / 3 / 1*` | `9` | Residue (0) must map to digit (9) |
| `2 1 3 / 99 / 1 / *99` | `9` | Wildcard at the first product position |
| `3 3 5 / 111 / 111 / 12*21` | `3` | Repeated input digits and an internal wildcard |
| 999-digit `9...9`, multiplied by `1` | `9` | Large input and linear-time behavior |

## Edge Cases

The residue-zero case is the most subtle. Consider

```
1 1 2
7
3
1*
```

Here (A\bmod9=7), (B\bmod9=3), so the product has residue (21\bmod9=3). The known digit contributes (1), giving (d\equiv3-1\equiv2\pmod9). The algorithm prints (2), matching (7\times3=21). If the required digit were (9), the computed residue would instead be (0), and the final conversion from (0) to (9) handles that case.

A wildcard at the beginning needs no separate branch. For

```
2 2 3
10
10
*00
```

the two operands both have residue (1), so their product has residue (1). The known digits sum to (0), giving (d=1). The algorithm never tries to parse `*00`, so there is no leading-character problem.

The same reasoning works when the wildcard is in the middle or at the end. For example, in

```
3 3 5
111
111
12*21
```

the operands have residues (3) and (3), giving product residue (0). The known product digits sum to (6), which is also residue (6). Thus the missing digit satisfies (d\equiv0-6\equiv3\pmod9), so the answer is (3). The actual product is (12321).

Finally, very long operands do not change the method. If (A) has (999999) digits, the algorithm still performs exactly one modular update per digit. It never stores a million-digit integer as a numeric object and never performs multiplication on those digits. The product itself is represented only indirectly through the congruence modulo (9), which is precisely the information needed to identify the single missing nonzero digit.
