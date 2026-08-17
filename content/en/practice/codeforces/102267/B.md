---
title: "CF 102267B - Primes"
description: "We need to split the given prime number (n) into two prime numbers (a) and (b) such that [ a+b=n. ] Any valid pair is accepted, so there is no need to find a particular decomposition if several exist. If no such pair exists, we print (-1)."
date: "2026-08-17T19:13:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102267
codeforces_index: "B"
codeforces_contest_name: "The 2019 University of Jordan Collegiate Programming Contest"
rating: 0
weight: 102267
solve_time_s: 280
verified: false
draft: false
---

[CF 102267B - Primes](https://codeforces.com/problemset/problem/102267/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We need to split the given prime number (n) into two prime numbers (a) and (b) such that

[
a+b=n.
]

Any valid pair is accepted, so there is no need to find a particular decomposition if several exist. If no such pair exists, we print (-1).

The bound (n\le 10^7) is large enough that checking every possible pair and repeatedly testing numbers for primality is too expensive in a 1 second time limit. However, (10^7) is small enough that a single primality test by trial division is very cheap, because its square root is only about (3162). The main challenge is not the size of (n), but recognizing that the fact that (n) itself is prime dramatically restricts which pairs are possible.

There are three boundary situations that can easily cause mistakes. For (n=2), the smallest prime, the only way to write it as a sum of positive primes would require a prime smaller than (2), so the correct output is `-1`. For (n=3), the only possible use of the smallest prime is (2+1), but (1) is not prime, so the answer is also `-1`. A careless implementation that treats (1) as prime would incorrectly accept this case.

The parity of the numbers creates another common trap. For example, with (n=11), both primes cannot be odd because odd plus odd is even. The only possible pair is (2+9), but (9) is composite, so the correct output is `-1`. Trying arbitrary pairs without using parity may waste most of the available time.

## Approaches

A direct brute-force solution could try every possible (a) from (2) to (n-2), set (b=n-a), and test both numbers for primality. The method is correct because every possible decomposition has one of its primes in that range, so eventually every candidate pair is considered. If primality is checked by trial division, however, each test can require (O(\sqrt n)) divisions. In the worst case this gives (O(n\sqrt n)) work. At (n=10^7), that is on the order of (10^7\cdot3162\approx3.16\times10^{10}) trial divisions, far beyond what fits in one second.

The structure of the input gives us a much stronger observation. Every prime other than (2) is odd. Since (n) is prime, it is either (2) or an odd number. For an odd prime (n), a sum of two odd primes would be even, so a valid pair must contain (2). There is only one possible pair:

[
2+(n-2)=n.
]

The entire problem has therefore been reduced to checking whether (n-2) is prime. We do not need to search through candidates, build a sieve, or examine multiple pairs.

The brute-force method works because it explicitly explores all decompositions, but fails because it performs far more primality checks than necessary. The parity observation reduces the search space from (O(n)) candidate pairs to exactly one candidate pair. A single trial-division primality test is easily fast enough for the given limit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n\sqrt n)) | (O(1)) | Too slow |
| Optimal | (O(\sqrt n)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the prime number (n). If (n=2), immediately print `-1`, because two primes are each at least (2), so their sum is at least (4).
2. For an odd prime (n), use parity to conclude that one of the two required primes must be (2). The other value is forced to be (n-2), so there is no reason to try any other candidate.
3. Test whether (n-2) is prime using trial division. It is enough to test divisors up to (\sqrt{n-2}), because if a composite number has a factor larger than its square root, its corresponding factor must be smaller than the square root.
4. If (n-2) is prime, print `2 n-2`. Otherwise print `-1`, because every valid pair for an odd prime (n) would have to be exactly this pair.

### Why it works

For every odd prime (n), suppose (n=a+b) where both (a) and (b) are prime. If both were odd, their sum would be even, contradicting the fact that (n) is odd. Thus one of them must be the only even prime, (2). The other must consequently equal (n-2). The algorithm checks exactly this forced candidate and accepts it precisely when (n-2) is prime. For (n=2), no pair can exist because the minimum sum of two primes is (4). Hence every possible input is handled correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_prime(x):
    if x < 2:
        return False

    if x % 2 == 0:
        return x == 2

    d = 3
    while d * d <= x:
        if x % d == 0:
            return False
        d += 2

    return True

def solve():
    n = int(input())

    if n == 2:
        print(-1)
        return

    other = n - 2

    if is_prime(other):
        print(2, other)
    else:
        print(-1)

if __name__ == "__main__":
    solve()
```

The `is_prime` function first rejects values below (2), which handles the (n=3) case because then `other` equals (1). It also handles even numbers separately. After that, only odd divisors need to be considered, so the loop starts at (3) and increases by (2).

The condition `d * d <= x` is the standard boundary for trial division. Testing divisors beyond (\sqrt{x}) cannot discover a new factor without an already tested smaller complementary factor. Using multiplication instead of computing a floating-point square root also avoids precision concerns.

The main function handles (n=2) before forming the candidate. For every other valid input, `other = n - 2` is the only possible second prime. The program never performs unnecessary pair enumeration.

Python integers do not overflow here, and the largest multiplication in the primality test is only around (3162^2), so there is no numerical concern.

## Worked Examples

For the first sample, (n=5). Since (5) is odd, the only possible pair must contain (2), leaving (5-2=3).

| (n) | Candidate (n-2) | Divisor checks | Result |
| --- | --- | --- | --- |
| 5 | 3 | None needed beyond the even check | `2 3` |

The candidate (3) is prime, so the forced pair is valid. The trace demonstrates why no other pair needs to be considered.

For the second sample, (n=11). Again, parity forces one prime to be (2), leaving (9).

| (n) | Candidate (n-2) | Divisor checks | Result |
| --- | --- | --- | --- |
| 11 | 9 | (3\mid9) | `-1` |

The divisor (3) is found before the loop needs to continue. Since (9) is composite, the only possible pair fails, proving that no answer exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\sqrt n)) | Only one primality test is performed, checking odd divisors up to (\sqrt{n-2}). |
| Space | (O(1)) | The algorithm stores only a constant number of integers. |

With (n\le10^7), the primality test examines at most roughly (3162) possible divisor values, and in practice only about half of those are checked because even divisors are skipped. This is comfortably within the 1 second time limit and uses negligible memory compared with the 256 MB limit.

## Test Cases

```python
import sys
import io

def is_prime(x):
    if x < 2:
        return False

    if x % 2 == 0:
        return x == 2

    d = 3
    while d * d <= x:
        if x % d == 0:
            return False
        d += 2

    return True

def solve():
    n = int(input())
    if n == 2:
        print(-1)
        return

    other = n - 2
    if is_prime(other):
        print(2, other)
    else:
        print(-1)

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    output = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output

    try:
        solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

    return output.getvalue().strip()

assert run("5\n") == "2 3", "sample 1"
assert run("11\n") == "-1", "sample 2"

assert run("2\n") == "-1", "minimum prime"
assert run("3\n") == "-1", "n - 2 equals 1"
assert run("7\n") == "2 5", "smallest successful odd case"
assert run("9999991\n") == "-1", "maximum valid prime input"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | `-1` | Minimum input and the impossible equal-prime boundary |
| `3` | `-1` | Prevents treating (1) as prime |
| `7` | `2 5` | Small successful decomposition and correct (n-2) boundary |
| `9999991` | `-1` | Near the maximum input size and a large composite candidate |

The largest prime below (10^7) is (9,999,991), making it a valid maximum-size test input. Its forced candidate (9,999,989) is composite, with factors (223) and (44,843), so the expected answer is `-1`.

## Edge Cases

For `n = 2`, the algorithm enters the explicit boundary check and prints `-1`. The reason is stronger than simply saying that the candidate fails: two primes are at least (2) each, so their sum cannot be (2). A solution that blindly computes `n - 2` would obtain (0), which is not prime, but handling the case explicitly makes the reasoning clear.

For `n = 3`, the forced second value is (3-2=1). The primality function immediately returns `False` because values below (2) are not prime, so the program prints `-1`. This catches a common mistake where a custom primality test starts its divisor loop at (2) and accidentally treats (1) as prime because it finds no divisor.

For `n = 5`, the forced pair is (2+3). The primality test accepts (3), so the program prints `2 3`. This is the smallest valid input for which a decomposition exists and confirms that the candidate boundary is handled correctly.

For `n = 11`, the forced pair is (2+9). The primality test checks (3), finds that (9) is divisible by (3), and returns `False`. The program prints `-1`. Trying another pair cannot help, because two odd primes would sum to an even number, so (2+9) is the only possible structure.

For an equal-prime decomposition, suppose (a=b=p). Then (n=2p), which is even. Since the input (n) is prime, the only even possibility is (n=2), but (2) cannot equal (2p) for any prime (p). Thus no valid input can have the two output primes equal. The minimum theoretical equal-prime sum would be (2+2=4), but (4) is not an allowed input because it is not prime.

For the largest valid input (n=9,999,991), the algorithm still performs only one primality test, this time on (9,999,989). That candidate is divisible by (223), so the test stops as soon as that factor is found and the program outputs `-1`. The size of (n) does not change the fundamental strategy, because the number of candidate pairs remains exactly one.
