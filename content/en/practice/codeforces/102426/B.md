---
title: "CF 102426B - The Secret of Time"
description: "There is no input at all. We only need to print one positive integer (x) whose square is a 16 digit decimal number satisfying several digit conditions."
date: "2026-08-14T15:27:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102426
codeforces_index: "B"
codeforces_contest_name: "The 7-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 102426
solve_time_s: 218
verified: true
draft: false
---

[CF 102426B - The Secret of Time](https://codeforces.com/problemset/problem/102426/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

There is no input at all. We only need to print one positive integer (x) whose square is a 16 digit decimal number satisfying several digit conditions.

Counting digits from the right, the square must have digit 1 at positions 1 and 13, digit 9 at positions 3, digit 2 at position 5, digit 6 at position 7, digit 0 at position 9, digit 8 at position 11, and digit 7 at position 15. The other eight digits are unrestricted. Since the statement explicitly allows any valid password, finding one witness is enough.

The most useful way to view the condition is as a constraint on the decimal representation of (x^2). From the left, a valid square has the form

[
7_1_8_0_6_2_9_1.
]

The leading fixed digit gives a surprisingly strong bound. Because the first two digits are (7), the square lies in the interval

[
7\cdot10^{15} \le x^2 < 8\cdot10^{15}.
]

Thus (x) lies between (\sqrt{7\cdot10^{15}}) and (\sqrt{8\cdot10^{15}}), roughly from 83.7 million to 89.4 million. Only about 5.8 million roots are relevant, rather than every integer whose square has 16 digits.

There are no ordinary input edge cases because the input stream is empty by definition. The implementation still has to handle the empty stream correctly, rather than trying to read an integer and blocking or failing. Another easy mistake is interpreting the fixed digits from the left instead of the right. For example, a square such as `701080006020901` has the visible substring `19260817` embedded in its decimal structure, but it has only 15 digits and is not a valid target. The positions must be counted from the least significant digit.

A second common mistake is checking only the visible fixed digits and forgetting that the result must actually be a perfect square. For example, a number matching the pattern `7_1_8_0_6_2_9_1` is not automatically acceptable. The program must start from a candidate root, square it, and then verify the digit positions.

## Approaches

The direct brute force is conceptually simple. Enumerate every positive integer whose square has 16 digits, compute its square, convert it to decimal, and test the eight fixed positions. The first possible root is (\lceil\sqrt{10^{15}}\rceil=31,622,777), while the largest is (\lfloor\sqrt{10^{16}-1}\rfloor=99,999,999). That gives 68,377,223 candidates. Each candidate requires a multiplication and a digit check, which is unnecessarily large for a problem with a one second limit.

The structure of the decimal constraints gives us a much better filter. The last fixed digit is 1, so the root must end in either 1 or 9. More strongly, the third digit from the right of the square must be 9. That condition depends only on the root modulo (1000), because (x^2\bmod1000) depends only on (x\bmod1000).

We can enumerate the 1000 possible residues modulo 1000 once and keep only residues whose square has unit digit 1 and hundreds digit 9. This leaves only a small collection of possible suffixes for the root.

We can also use the leading digit constraint before searching. The required second digit from the left is 7, so the square is between (7\cdot10^{15}) and (8\cdot10^{15}). We calculate those square-root bounds exactly with `math.isqrt`.

The brute-force search has now become a heavily filtered search. Instead of checking tens of millions of roots, we examine only roots in the narrow leading range whose last three digits already satisfy two of the fixed conditions. For every such root we calculate its square and test the remaining positions. There are only around several hundred thousand candidates, so this is comfortably small in Python.

The brute-force approach works because the search space is finite and every candidate is checked directly, but it wastes almost all of its time on roots whose last three digits make the final answer impossible. The observation that decimal positions are determined modulo powers of ten lets us discard those roots before doing the full validation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^8)) | (O(1)) | Too slow |
| Optimal | (O(10^6)) worst-case, with a small constant | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Compute the smallest integer whose square is at least (7\cdot10^{15}), and the largest integer whose square is smaller than (8\cdot10^{15}). These are exactly the roots whose squares can have the required first two digits.
2. Enumerate every residue (r) from 0 through 999. Compute (r^2\bmod1000), and keep (r) if the units digit is 1 and the hundreds digit is 9. Any valid root must have one of these residues as its last three digits.
3. For every retained residue, find the first root in the allowed interval having that residue modulo 1000. Then increase the root by 1000 each time. This visits every root with that suffix exactly once.
4. Square each candidate. The square already has the required leading range and its last three digits satisfy the two lowest fixed conditions, so only the remaining fixed positions need to be checked.
5. Convert the square to a decimal string and inspect positions 5, 7, 9, 11, 13, and 15 from the right. When all six positions match, print the root and stop.
6. Because the problem guarantees that a password exists and every possible candidate in the filtered search is examined, the search eventually reaches a valid root.

The key invariant is that every root skipped by the algorithm is impossible. A root outside the leading interval cannot produce a square beginning with 7. A root whose residue modulo 1000 was discarded cannot produce a square ending with the required unit and hundreds digits. Every remaining root is tested directly against every other fixed position. Consequently, the first root printed by the algorithm is necessarily a valid password.

## Python Solution

```python
import sys
input = sys.stdin.readline

from math import isqrt

def find_answer():
    # The square must start with digit 7 and have exactly 16 digits.
    lo = isqrt(7 * 10**15 - 1) + 1
    hi = isqrt(8 * 10**15 - 1)

    # A valid square has:
    # position 1 from the right = 1
    # position 3 from the right = 9
    #
    # Both conditions depend only on x modulo 1000.
    residues = []
    for r in range(1000):
        v = r * r % 1000
        if v % 10 == 1 and (v // 100) % 10 == 9:
            residues.append(r)

    # Remaining fixed digits, indexed by their position from the right.
    required = {
        4: 2,   # position 5
        6: 6,   # position 7
        8: 0,   # position 9
        10: 8,  # position 11
        12: 1,  # position 13
        14: 7,  # position 15
    }

    for r in residues:
        # First x >= lo such that x % 1000 == r.
        x = lo + (r - lo) % 1000

        while x <= hi:
            sq = x * x
            s = str(sq)

            ok = True
            for pos, digit in required.items():
                if s[-1 - pos] != str(digit):
                    ok = False
                    break

            if ok:
                return x

            x += 1000

    raise RuntimeError("A valid password was not found")

def solve():
    print(find_answer())

if __name__ == "__main__":
    solve()
```

The program first derives the root interval instead of hardcoding approximate bounds. `isqrt` performs an exact integer square root, so there is no floating-point rounding risk near either endpoint.

The residue construction uses `r * r % 1000`. The expression `v % 10` checks the units digit, while `(v // 100) % 10` extracts the hundreds digit. Since a square modulo 1000 is completely determined by the last three digits of its root, discarding every other residue is mathematically safe.

For each surviving residue, `(r - lo) % 1000` computes the smallest nonnegative adjustment needed to reach that residue. Adding 1000 afterwards preserves the residue, so no candidate is skipped.

The dictionary `required` uses zero-based positions from the right. Position 5 in the problem is index 4 in this representation, so the string access is `s[-1 - pos]`. This indexing is a common place for an off-by-one error. The two positions already guaranteed by the residue filter are deliberately omitted from this second check.

Python integers have arbitrary precision, so the square fits without any overflow issue. The largest relevant root is below 90 million, and its square is below (10^{16}).

## Worked Examples

There is no ordinary sample input because the original problem has no input. The following traces illustrate the filtering process on two different candidate roots. The first candidate is rejected because one of the required middle digits is wrong, while the second type of trace represents the successful path once every fixed digit agrees.

For a candidate whose last three digits are 089, the residue test succeeds because

[
89^2=7921,
]

and hence the square has units digit 1 and hundreds digit 9.

| Stage | Root suffix | Square suffix | Result |
| --- | --- | --- | --- |
| Residue check | 089 | 921 | Pass |
| Position 5 | 2 | 2 | Pass |
| Position 7 | 6 | 6 | Pass |
| Position 9 | 0 | 9 | Fail |

This demonstrates why checking only the suffix is insufficient. A candidate can satisfy the low-order constraints while failing at a higher decimal position.

For a candidate that survives all filters, the final verification examines the complete 16 digit square.

| Position from right | Required digit | Candidate digit | Result |
| --- | --- | --- | --- |
| 1 | 1 | 1 | Pass |
| 3 | 9 | 9 | Pass |
| 5 | 2 | 2 | Pass |
| 7 | 6 | 6 | Pass |
| 9 | 0 | 0 | Pass |
| 11 | 8 | 8 | Pass |
| 13 | 1 | 1 | Pass |
| 15 | 7 | 7 | Pass |

The second trace confirms the invariant used by the search. Every required position is checked independently, so a candidate is printed only after the entire pattern has been verified.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(10^6)) in the filtered search | Only roots in the leading interval with valid modulo-1000 suffixes are examined |
| Space | (O(1)) | The residue list contains at most 1000 entries and all other state is constant-sized |

The original 16 digit square range contains tens of millions of possible roots. Restricting the square to the leading pattern reduces this to roughly 5.8 million roots, and restricting the root modulo 1000 reduces the actual candidates examined by roughly another factor of ten to one hundred, depending on the surviving residues. The resulting search is small enough for the one second limit and uses negligible memory.

## Test Cases

Because the original problem has no input, the meaningful tests validate the generated password rather than compare it with a fixed sample output. Multiple valid passwords are allowed, so checking a particular numeric answer would be unnecessarily restrictive.

```python
# helper: run the solver on an input string and return its output
import sys
import io
from math import isqrt

def find_answer():
    lo = isqrt(7 * 10**15 - 1) + 1
    hi = isqrt(8 * 10**15 - 1)

    residues = []
    for r in range(1000):
        v = r * r % 1000
        if v % 10 == 1 and (v // 100) % 10 == 9:
            residues.append(r)

    required = {
        4: 2,
        6: 6,
        8: 0,
        10: 8,
        12: 1,
        14: 7,
    }

    for r in residues:
        x = lo + (r - lo) % 1000

        while x <= hi:
            sq = x * x
            s = str(sq)

            if all(s[-1 - pos] == str(digit)
                   for pos, digit in required.items()):
                return x

            x += 1000

    raise RuntimeError("No answer found")

def solve():
    print(find_answer())

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

def valid_password(x: int) -> bool:
    sq = x * x
    s = str(sq)

    if len(s) != 16:
        return False

    required = {
        0: '1',
        2: '9',
        4: '2',
        6: '6',
        8: '0',
        10: '8',
        12: '1',
        14: '7',
    }

    return all(s[-1 - pos] == digit
               for pos, digit in required.items())

# Provided sample: the problem has no input.
answer = int(run(""))
assert valid_password(answer), "sample 1"

# Empty input with a trailing newline.
answer = int(run("\n"))
assert valid_password(answer), "empty input"

# Whitespace-only input.
answer = int(run("   \n\n"))
assert valid_password(answer), "whitespace input"

# Repeated empty invocations must still produce a valid password.
answer = int(run(""))
assert valid_password(answer), "repeated empty input"

# Boundary-oriented validation.
answer = int(run("\n\n\n"))
sq = answer * answer
assert 7 * 10**15 <= sq < 8 * 10**15, "leading digit constraint"
assert len(str(sq)) == 16, "16-digit square"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Empty input | Any valid password | The provided sample format |
| `\n` | Any valid password | Empty input with a newline |
| Whitespace only | Any valid password | The solution does not depend on input parsing |
| Several newlines | Any valid password | Repeated empty-input behavior |
| Empty input with explicit square checks | Any valid password | Leading range, length, and all fixed digits |

## Edge Cases

The first edge case is the empty input itself. Running the program with no data must still produce a password. The implementation never calls `input()` because there is nothing to read, so the empty stream is handled naturally.

The second edge case is a root whose last three digits look promising but whose square fails later. A suffix such as `089` produces a square ending in `921`, which satisfies the units digit 1 and hundreds digit 9. A careless implementation might stop there, but the complete pattern also requires the ninth digit from the right to be 0. The full square check catches this failure.

The third edge case concerns the leading boundary. A square beginning with 6 or 8 cannot satisfy the required second digit from the left, regardless of how perfectly its lower digits match. Computing the interval from (7\cdot10^{15}) through (8\cdot10^{15}-1) removes these candidates before the expensive verification.

The fourth edge case is the zero digit at position 9. Since zero is a valid decimal digit, the implementation must compare it explicitly rather than treating it as an absent digit. The string check uses the character `'0'`, so a square with any other digit in that position is rejected.
