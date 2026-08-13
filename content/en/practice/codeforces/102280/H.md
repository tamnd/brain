---
title: "CF 102280H - \u0417\u0430\u0434\u0430\u0447\u0430 \u0428\u0443\u043c\u0430\u0445\u0435\u0440\u0430"
description: "We are given two prime numbers, (p) and (q), and need to decide whether [ (p+1)^q ] is a perfect square. The numbers can contain up to (1000) decimal digits, so they are far beyond ordinary machine integer types."
date: "2026-08-13T09:51:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102280
codeforces_index: "H"
codeforces_contest_name: "2010, \u0422\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0430 \u0421\u0413\u0410\u0423 aka \u041a\u043e\u043d\u0442\u0435\u0441\u0442 \u043f\u0440\u043e \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u043a\u0438"
rating: 0
weight: 102280
solve_time_s: 169
verified: true
draft: false
---

[CF 102280H - \u0417\u0430\u0434\u0430\u0447\u0430 \u0428\u0443\u043c\u0430\u0445\u0435\u0440\u0430](https://codeforces.com/problemset/problem/102280/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two prime numbers, (p) and (q), and need to decide whether

[
(p+1)^q
]

is a perfect square. The numbers can contain up to (1000) decimal digits, so they are far beyond ordinary machine integer types. The required output is `YES` when the expression is the square of a natural number, and `NO` otherwise.

The decisive property is the exponent (q). Since (q) is prime, it is either (2) or an odd prime. When (q=2), the expression is simply ((p+1)^2), which is always a perfect square. When (q) is odd, raising a number to the (q)-th power does not change whether every prime exponent in its factorization is even. Thus ((p+1)^q) is a square exactly when (p+1) itself is a square.

The remaining question is much simpler because (p) is also prime. Suppose (p+1=k^2). Then

[
p=k^2-1=(k-1)(k+1).
]

Since (p) is prime, this product can only have one factor equal to (1). Hence (k-1=1), giving (k=2) and (p=3). So for every odd prime (q), the answer is `YES` exactly when (p=3).

The huge upper bound of (10^{1000}) changes the implementation strategy completely. We cannot convert the inputs to 64-bit integers, and constructing ((p+1)^q) is hopeless because its number of digits would itself be enormous. Even a generic perfect-square test on that value would require manipulating an astronomically large integer. The mathematical reduction lets us avoid all arithmetic involving the huge power. We only need to compare the decimal input strings with `2` and `3`, which takes time proportional to the input length.

There are a few boundary cases that can fool an implementation based only on the statement's algebra. For example, with

```
3
2
```

the answer is `YES`, because ((3+1)^2=16). A solution that checks whether (p+1) is a square first would incorrectly reject this case, since the special exponent (q=2) makes every base work.

For

```
2
3
```

the answer is `NO`. Here (q) is odd, so (p+1=3) would itself have to be a square, which it is not. A solution that treats every odd exponent as producing a square would fail here.

For

```
3
3
```

the answer is `YES`, because (p+1=4) is a square and an odd power of a square remains a square. This case verifies the second branch of the characterization.

The statement says that the inputs are prime, so values such as `0` and `1` are outside the valid mathematical domain despite appearing in the numeric bounds. The solution relies on the primality condition and does not need to handle such values as valid test cases.

## Approaches

A direct approach would construct ((p+1)^q) and test whether the result is a square. This is correct mathematically, but it completely ignores the structure of the problem. With inputs having up to (1000) digits, (q) can be on the order of (10^{1000}). Even conceptually performing (q) multiplications is about (10^{1000}) operations, and the resulting number has an astronomical number of digits. Such an approach is not merely too slow for the (0.5) second limit, it is infeasible.

A slightly less direct brute-force method could try to determine whether (p+1) is a square by enumerating possible roots. In the worst case (p) is around (10^{1000}), so the root is around (10^{500}), giving roughly (10^{500}) candidates. That is equally impossible.

The useful observation is that the exponent is prime. Every prime is either (2) or odd. The case (q=2) immediately gives a square. For odd (q), consider the prime factorization of (p+1). If a prime factor occurs with exponent (e), it occurs in ((p+1)^q) with exponent (eq). Since (q) is odd, (eq) is even exactly when (e) is even. Consequently, the power is a square exactly when (p+1) is already a square.

Now use the fact that (p) is prime. If (p+1=k^2), then (p=(k-1)(k+1)). A prime cannot be represented as a product of two integers greater than (1), so (k-1=1), which forces (p=3).

The entire problem has therefore collapsed to two string comparisons. If (q=2), print `YES`. Otherwise, because (q) is an odd prime, print `YES` exactly when (p=3).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(q)) multiplications, with an enormous result size | Astronomical | Too slow |
| Optimal | (O( | p | + | q | )) | (O( | p | + | q | )) | Accepted |

## Algorithm Walkthrough

1. Read (p) and (q) as strings rather than converting them to ordinary integers. Their values may contain (1000) digits, while the algorithm only needs to compare them with the small constants (2) and (3).
2. Check whether (q=2). If it is, output `YES` immediately because
[
(p+1)^2
]
is a square for every possible (p).
3. If (q\neq2), then (q) is an odd prime. For an odd exponent, ((p+1)^q) is a square exactly when (p+1) is a square.
4. Suppose (p+1=k^2). Since (p) is prime,
[
p=k^2-1=(k-1)(k+1).
]
The only possible prime value occurs at (k=2), giving (p=3).
5. Check whether (p=3). If so, output `YES`; otherwise output `NO`.

The key invariant is that after the first branch, (q) is known to be odd, so the square status of ((p+1)^q) is exactly the square status of (p+1). The primality of (p) then reduces that condition to the single possibility (p=3). Every possible valid input belongs to one of these two branches, so no other case can produce `YES`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    p = input().strip()
    q = input().strip()

    if q == "2" or p == "3":
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The input is kept as strings because converting a thousand-digit value to a machine integer is unnecessary for this solution. Python can handle arbitrarily large integers as well, but using strings makes the intended complexity explicit and avoids any multiplication or exponentiation.

The first comparison handles the exceptional prime exponent (2). No condition on (p) is needed there, since the entire expression has the form (x^2).

If that comparison fails, (q) is an odd prime by the problem's guarantee. In that situation the only possible value of (p) leading to a square is (3), so the second comparison is sufficient.

There are no overflow concerns because the program never evaluates (p+1), never computes a power, and never constructs a square root. The largest operation is comparing two strings whose lengths are at most (1000).

## Worked Examples

The statement's extracted sample section does not preserve the actual input values, but the intended two basic cases can be represented by the following valid examples.

### Example 1

Consider

```
3
2
```

The execution is:

| Step | (p) | (q) | Decision | Output |
| --- | --- | --- | --- | --- |
| 1 | 3 | 2 | (q=2) | `YES` |

The algorithm stops at the first branch. Indeed, the expression is (4^2=16), so the result is a perfect square. This example demonstrates why checking only whether (p+1) is a square is insufficient as a general strategy.

### Example 2

Consider

```
2
3
```

The execution is:

| Step | (p) | (q) | Decision | Output |
| --- | --- | --- | --- | --- |
| 1 | 2 | 3 | (q\neq2) | continue |
| 2 | 2 | 3 | (p\neq3) | `NO` |

Since (q=3) is odd, the base (p+1=3) would have to be a square. It is not, so the answer is `NO`.

For another useful trace, consider

```
3
3
```

Here the first comparison fails because (q\neq2), but the second succeeds because (p=3). The underlying expression is (4^3=64=8^2), confirming that the odd-exponent branch is also correct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O( | p | + | q | )) | Reading and comparing the two decimal strings dominates the work. |
| Space | (O( | p | + | q | )) | The input strings occupy space proportional to their lengths. |

Both inputs have at most (1000) digits, so the algorithm performs only a tiny amount of work relative to the limits. In particular, it never constructs the potentially enormous value ((p+1)^q), which is the reason the solution comfortably fits the (0.5) second and (64) MB limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    p = input().strip()
    q = input().strip()

    if q == "2" or p == "3":
        print("YES")
    else:
        print("NO")

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

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided-sample-style cases
assert run("3\n2\n") == "YES", "q = 2 always gives a square"
assert run("2\n3\n") == "NO", "odd q requires p + 1 to be a square"

# Minimum valid prime values
assert run("2\n2\n") == "YES", "both primes are 2"

# The unique p producing a square for odd q
assert run("3\n3\n") == "YES", "p = 3 works for every odd prime q"

# Large decimal inputs, q is odd and p is not 3
assert run("99999999999999999999999999999999999999999999999999\n3\n") == "NO", \
    "large p must not trigger big-integer arithmetic"

# Large q with q = 2 represented exactly by its small decimal form
assert run("99999999999999999999999999999999999999999999999999\n2\n") == "YES", \
    "q = 2 works for every prime p"
```

The helper above temporarily replaces standard input and output so that the same `solve` function can be tested repeatedly. The first two assertions cover the two fundamental branches. The third checks the smallest valid prime (p) and (q). The fourth verifies the special value (p=3) for an odd exponent. The last two checks demonstrate that the algorithm does not attempt to perform arithmetic on thousand-digit values.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 2` | `YES` | Special exponent (q=2) |
| `2 3` | `NO` | Smallest (p) with an odd exponent |
| `2 2` | `YES` | Minimum valid prime values |
| `3 3` | `YES` | Unique (p=3) case for odd (q) |
| Large (p), `q=3` | `NO` | Large input without big-integer arithmetic |
| Large (p), `q=2` | `YES` | (q=2) branch with a huge (p) |

## Edge Cases

The first non-obvious case is (q=2). For input

```
2
2
```

the algorithm immediately sees `q == "2"` and prints `YES`. The expression is (3^2=9). More generally, this branch accepts every valid prime (p), so it must be checked before applying the odd-exponent argument.

The second case is (p=2) with an odd prime exponent:

```
2
3
```

Here (q) is odd and (p+1=3). The algorithm skips the (q=2) branch, then checks `p == "3"`, which is false, and prints `NO`. Algebraically, (3^3=27), which is not a square.

The third case is the unique positive case for odd (q):

```
3
3
```

The first comparison fails, but `p == "3"` succeeds. The algorithm prints `YES`. Indeed, (p+1=4=2^2), and (4^3=64=8^2).

The final edge case concerns the enormous numeric bounds. Suppose (p) has (1000) digits and (q=2). The program does not calculate (p+1) or ((p+1)^2). It only compares the string `q` with `"2"`, so it can immediately return `YES`. Likewise, for an enormous prime (p) and an odd (q), it only checks whether the complete input string for (p) is exactly `"3"`. This avoids the overflow, memory growth, and running time that a direct computation of the expression would cause.
