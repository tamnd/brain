---
title: "CF 102375G - \u0415\u0441\u0442\u044c \u043b\u0438 \u0434\u0435\u043b\u0438\u0442\u0435\u043b\u044c?"
description: "We are given a nonempty decimal string without leading zeroes. The digits are not necessarily a decimal representation of the number we care about. Instead, we may choose a base (B), and then interpret exactly the same digit sequence in base (B)."
date: "2026-08-15T07:12:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "G"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 517
verified: false
draft: false
---

[CF 102375G - \u0415\u0441\u0442\u044c \u043b\u0438 \u0434\u0435\u043b\u0438\u0442\u0435\u043b\u044c?](https://codeforces.com/problemset/problem/102375/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a nonempty decimal string without leading zeroes. The digits are not necessarily a decimal representation of the number we care about. Instead, we may choose a base (B), and then interpret exactly the same digit sequence in base (B). If the digits are (a_0,a_1,\ldots,a_{n-1}), the resulting value is

[
D=a_0B^{n-1}+a_1B^{n-2}+\cdots+a_{n-1}.
]

The base must be at least one more than every digit appearing in the string. We need to find a base (2\le B\le10^9) and a proper divisor (X), with (2\le X<D) and (X\le10^9). If no such pair exists, we print (-1). The original contest statement gives (n\le3\cdot10^6), a 2 second limit, and 512 MiB of memory.

The length is the key constraint. With up to three million digits, anything quadratic in the length is impossible, and even algorithms that repeatedly manipulate the whole string many times are undesirable. We want a constant number of linear passes, ideally just one pass to collect a few properties of the digits. The numerical value (D) itself can have millions of digits, so constructing it as an integer is completely unnecessary and would be impossible in ordinary fixed-width arithmetic.

There are several small cases where a tempting construction fails. For input `1`, the represented number is always (1), regardless of the base, so it has no proper divisor and the answer is correctly `-1`. For input `2`, the value is always (2), so choosing (X=2) is invalid because (X<D) is required. The same problem occurs for the one-digit primes `3`, `5`, and `7`. In contrast, input `4` is already composite, so `10 2` works because the represented value is (4) and its proper divisor (2) is valid.

Another boundary case is `10`. Its digit sum is (1), so the construction based directly on the digit sum cannot use (X=1). A valid answer is `4 2`: the string `10` in base (4) represents (4), which is divisible by (2). The same special construction works for every string of the form `100...0` having at least two digits.

## Approaches

A direct approach would try bases starting from the smallest legal base and, for each base, somehow determine whether the resulting number is composite. One could even try every possible divisor (X) from (2) through (10^9), evaluating the represented number modulo (X). That is correct because finding any (X) with zero remainder immediately gives the required certificate, but the search space contains up to (10^9) bases and (10^9) candidate divisors, giving (10^{18}) divisor checks in the worst case. Computing a residue from the whole three-million-character string for every candidate would make the approach even worse.

The brute force works because the only property we need is divisibility. The crucial observation is that we control the base itself. Suppose we choose

[
B=X+1.
]

Then (B\equiv1\pmod X), so every power of (B) is also congruent to (1\pmod X). Consequently,

[
D
=\sum a_iB^{n-1-i}
\equiv\sum a_i
\pmod X.
]

The represented number modulo (X) is simply the sum of the decimal digits modulo (X). This lets us choose (X) rather than search for it.

Let (S) be the sum of all digits. If (S\ge2), choose

[
X=S,\qquad B=S+1.
]

Then (D\equiv S\equiv0\pmod X). Since the largest digit is at most (S), the base (S+1) is legal. Also, (S\le9n\le27\cdot10^6), so both (B) and (X) are far below (10^9).

For a string with at least two digits, (D>X) as well. Its leading digit is positive, so (D\ge B=S+1>X). Thus the divisor is proper.

The only case not covered by (S\ge2) is (S=1). Because the first digit is nonzero, the string must be `1` or `100...0`. The one-character case is the value (1), so no answer exists. If there are at least two characters, choose (B=4) and (X=2). The string represents (4^{n-1}), which is divisible by (2), and its value is at least (4), so (2) is a proper divisor.

For a one-digit input with value (d>1), changing the base has no effect at all. We simply need to check whether (d) is composite. Since (d\le9), this can be handled directly by looking for a divisor from (2) through (\sqrt d).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^{18}n)) in the direct search | (O(1)) apart from input | Too slow |
| Optimal | (O(n)) | (O(n)) for the input string | Accepted |

## Algorithm Walkthrough

1. Read the digit string and compute its digit sum (S). We only need the sum, because choosing a base congruent to (1) modulo (S) turns the entire positional representation into that digit sum modulo (S).
2. If the string has length one, handle the value directly. For `1`, there is no valid divisor. For `2`, `3`, `5`, and `7`, the number is prime. For `4`, `6`, `8`, and `9`, choose base (10) and a proper divisor of the digit.
3. If the string has at least two digits and (S=1), the string is necessarily `100...0`. Choose (B=4) and (X=2). The represented value is (4^{n-1}), so it is divisible by (2), and because (n\ge2), its value is at least (4).
4. If the string has at least two digits and (S\ge2), choose (X=S) and (B=S+1). Since every digit is at most (S), all digits are valid in base (B).
5. The choice in the previous step gives (B\equiv1\pmod X). Hence (B^k\equiv1\pmod X) for every (k), and the represented number satisfies
[
D\equiv S\equiv0\pmod X.
]
Because the first digit is positive and there are at least two digits, (D\ge B=S+1>X), so (X) is a proper divisor.
6. Print the constructed pair. Since (S\le9\cdot3\cdot10^6=27\cdot10^6), both (S) and (S+1) satisfy the (10^9) bound.

The invariant behind the construction is the congruence (B\equiv1\pmod X). Once that holds, the positional representation loses all dependence on the powers of (B) modulo (X), leaving exactly the sum of its digits. Choosing (X) equal to that sum makes the represented number divisible by (X). The only situation where this divisor would be (1) is (S=1), and that case is handled separately.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    if n == 1:
        d = ord(s[0]) - ord('0')

        if d < 4:
            print(-1)
            return

        for x in range(2, int(d ** 0.5) + 1):
            if d % x == 0:
                print(10, x)
                return

        print(-1)
        return

    digit_sum = sum(ord(c) - ord('0') for c in s)

    if digit_sum == 1:
        print(4, 2)
        return

    x = digit_sum
    b = x + 1

    print(b, x)

if __name__ == "__main__":
    solve()
```

The first branch handles one-digit strings because the base cannot change their numerical value. For a one-digit number (d), a valid divisor exists exactly when (d) is composite. Testing divisors only up to (\sqrt d) is more than enough, although the values are so small that even a hardcoded check would work.

For longer strings, the code computes the digit sum in one pass. Python integers can store this sum comfortably because its maximum is only (27\cdot10^6).

When the sum is (1), the absence of any other nonzero digit follows from the nonnegative digits and the fact that the first digit is already (1). The base (4), divisor (2) construction then works without ever constructing (D).

For a sum of at least (2), the code sets `x = digit_sum` and `b = x + 1`. There is no need to evaluate the huge number represented by the string. The divisibility proof operates entirely modulo (x).

There is also no overflow issue in Python. More importantly, the implementation never creates (B^{n-1}) or (D), which would be the wrong implementation strategy even in a language with arbitrary-precision integers because (D) can contain millions of digits.

## Worked Examples

For Sample 1, the input is `1`.

| Variable | Value |
| --- | --- |
| `s` | `1` |
| `n` | `1` |
| `d` | `1` |
| Result | `-1` |

The only value represented by a one-digit `1` is (1), independent of the base. It has no divisor (X>1), so the algorithm correctly rejects it.

For Sample 2, the input is `4`.

| Variable | Value |
| --- | --- |
| `s` | `4` |
| `n` | `1` |
| `d` | `4` |
| Tested divisor | `2` |
| Result | `10 2` |

The represented value is (4) in every base. The divisor (2) is proper, and base (10) is legal because the digit `4` is valid in decimal notation. Thus the output is valid.

For completeness, Sample 3 illustrates the main construction. Its digit sum is (1+9=10), so the algorithm chooses (X=10) and (B=11). The value is

[
D=1\cdot11+9=20,
]

and (20) is divisible by (10). The output `11 10` is different from the sample output `11 2`, but both are valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | The only operation depending on the input length is the digit-sum pass. |
| Space | (O(n)) | The input string itself occupies (O(n)) memory; the algorithm uses (O(1)) additional space. |

With (n\le3\cdot10^6), a single pass over three million characters is easily within the intended scale of the problem. The algorithm performs no factorization of a huge number and never constructs the value represented by the digit string. The official statement specifies a 2 second time limit and 512 MiB memory limit, and this linear scan is designed for those constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    s = input().strip()
    n = len(s)

    if n == 1:
        d = ord(s[0]) - ord('0')

        if d < 4:
            print(-1)
            return

        for x in range(2, int(d ** 0.5) + 1):
            if d % x == 0:
                print(10, x)
                return

        print(-1)
        return

    digit_sum = sum(ord(c) - ord('0') for c in s)

    if digit_sum == 1:
        print(4, 2)
        return

    x = digit_sum
    b = x + 1
    print(b, x)

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue() if False else ""
    finally:
        sys.stdin = old_stdin
        input = old_input

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

# Provided samples.
assert run("1\n") == "-1", "sample 1"
assert run("4\n") == "10 2", "sample 2"

# Sample 3 has many valid answers. This implementation returns 11 10.
assert run("19\n") == "11 10", "sample 3"

# Custom: one-digit prime.
assert run("7\n") == "-1", "one-digit prime"

# Custom: one-digit composite.
assert run("9\n") == "10 3", "one-digit composite"

# Custom: digit sum is exactly one, with two digits.
assert run("10\n") == "4 2", "sum-one boundary"

# Custom: all digits equal.
assert run("999\n") == "28 27", "all equal digits"

# Custom: maximum length.
assert run("1" * 3_000_000 + "\n") == "3000001 3000000", "maximum length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7` | `-1` | One-digit prime cannot be made composite by changing the base. |
| `9` | `10 3` | One-digit composite handling and divisor search. |
| `10` | `4 2` | The special (S=1) construction and the strict (X<D) condition. |
| `999` | `28 27` | Large digit sum and the (B=S+1) construction. |
| `111...111` with 3,000,000 digits | `3000001 3000000` | Maximum input length and the (10^9) bounds. |

The test helper has to capture standard output because the competitive-programming solution writes directly to `stdout`. The sample with `19` deliberately checks the output produced by this particular implementation, since the task accepts any valid pair rather than requiring the sample pair.

## Edge Cases

For input `1`, the algorithm enters the one-digit branch immediately. Its value is (1), so the loop looking for a divisor is not even needed, and the answer is `-1`. This catches the most basic mistake, which would be to choose (X) equal to the digit itself without checking (X>1).

For input `2`, the same one-digit branch recognizes that the number is not composite and prints `-1`. Choosing `B=3, X=2` would look superficially attractive, but the represented number is still (2), so (X=D), violating the strict inequality.

For input `4`, the algorithm finds (2) as a divisor and prints `10 2`. The represented value remains (4), so the result satisfies (2<D). This demonstrates why one-digit inputs need to be treated separately instead of applying the digit-sum construction mechanically.

For input `10`, the digit sum is (1), which cannot be used as a divisor because divisors must be at least (2). Since the string has two digits and sum (1), it must be exactly `10`. The special branch chooses (B=4), giving (D=4), and (X=2). Here (2\mid4) and (2<4), so the construction is valid.

For input `1000`, the same reasoning gives (B=4), (X=2). The represented number is (4^3=64), which is divisible by (2). A careless implementation that assumes the digit sum is always at least (2) would instead try to output (X=1), which is forbidden.

For an input such as `11`, the digit sum is (2), so the algorithm chooses (B=3) and (X=2). The represented value is (1\cdot3+1=4), and (4\equiv0\pmod2). The strict inequality (X<D) also holds. This is the smallest nontrivial example of the general construction.

For the maximum-length input consisting of three million `9` digits, the digit sum is (27,000,000). The algorithm outputs (B=27,000,001) and (X=27,000,000). Both are much smaller than (10^9), and (B) is certainly larger than every digit. The represented value is congruent to the digit sum modulo (X), so it is divisible by (X), while its length guarantees that it is much larger than (X). The algorithm never constructs this enormous value, which is the central reason the solution remains linear in the input size.
