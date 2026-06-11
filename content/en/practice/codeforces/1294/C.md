---
title: "CF 1294C - Product of Three Numbers"
description: "For each test case, we are given a single integer n. We must determine whether n can be written as the product of three distinct integers a, b, and c, where each of them is at least 2. If such a decomposition exists, we print \"YES\" and one valid triple."
date: "2026-06-11T18:40:37+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1294
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 615 (Div. 3)"
rating: 1300
weight: 1294
solve_time_s: 143
verified: true
draft: false
---

[CF 1294C - Product of Three Numbers](https://codeforces.com/problemset/problem/1294/C)

**Rating:** 1300  
**Tags:** greedy, math, number theory  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we are given a single integer `n`. We must determine whether `n` can be written as the product of three **distinct** integers `a`, `b`, and `c`, where each of them is at least `2`.

If such a decomposition exists, we print `"YES"` and one valid triple. If no such triple exists, we print `"NO"`.

The input contains up to 100 test cases, and each value of `n` is at most `10^9`. A number this size can still be factorized by trial division up to `√n`, because `√(10^9) ≈ 31623`. Even if we perform this work for every test case, the total amount of computation remains comfortably within the time limit.

The main difficulty is not factorization itself. The challenge is finding three factors that are all different.

Consider `n = 64 = 2^6`. A decomposition exists:

```
64 = 2 × 4 × 8
```

All three factors are distinct and at least `2`.

Now consider `n = 32 = 2^5`.

Possible factorizations include:

```
32 = 2 × 2 × 8
32 = 2 × 4 × 4
```

Every decomposition repeats a factor, so the correct answer is `"NO"`.

Another subtle case is when `n` has exactly two distinct prime factors but one of them appears only once. For example:

```
n = 12 = 2^2 × 3
```

We can choose `2` and `3`, leaving `2` as the remaining factor. The factors become:

```
2, 3, 2
```

which are not distinct. A solution must reject this case.

A different example is:

```
n = 72 = 2^3 × 3^2
```

Choosing `2` and `3` leaves:

```
72 / (2 × 3) = 12
```

giving:

```
2, 3, 12
```

which is valid.

A careless implementation that merely finds any two divisors and uses the remainder as the third factor can accidentally produce duplicate values.

## Approaches

A brute-force solution would try all possible triples `(a, b, c)` such that `a × b × c = n`. One way is to iterate over all divisors for `a`, all divisors for `b`, and check whether the remaining quotient forms `c`.

Even if we restrict ourselves to divisors, this approach becomes impractical. The search space grows far too quickly, especially when performed for up to 100 test cases.

The key observation is that we do not need all factors. We only need **three distinct factors**.

Suppose we extract one non-trivial divisor `a` from `n`. After dividing by `a`, we obtain a smaller number. If we can extract a second divisor `b` that is different from `a`, then the remaining quotient automatically becomes:

```
c = n / (a × b)
```

The problem reduces to finding two distinct divisors while ensuring the final quotient is different from both.

Prime factorization makes this easy. We repeatedly search for the smallest divisor of the current number.

The first divisor found becomes `a`.

After removing `a`, we search again. The next divisor different from `a` becomes `b`.

Everything left is assigned to `c`.

If `c` is greater than `1` and distinct from both `a` and `b`, we have a valid answer. Otherwise no valid triple exists.

This works because any valid decomposition must ultimately come from the prime factors of `n`. Extracting factors greedily leaves as much factor mass as possible for the final number, making it easier to obtain three distinct values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) or worse | O(1) | Too slow |
| Optimal | O(√n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Store the original value of `n`.
2. Find the smallest divisor of `n` greater than `1`.

Let this divisor be `a`.
3. If no divisor exists, then `n` is prime.

A prime number cannot be written as a product of three integers greater than `1`, so print `"NO"`.
4. Divide `n` by `a`.
5. Search for another divisor of the reduced number.

The divisor must be different from `a`.
6. Let this divisor be `b`.
7. If no such divisor exists, print `"NO"`.
8. Compute

```
c = original_n / (a × b)
```
9. Check whether `c` is different from both `a` and `b`, and whether `c > 1`.
10. If all checks pass, print `"YES"` and the triple `(a, b, c)`. Otherwise print `"NO"`.

### Why it works

The algorithm extracts two distinct non-trivial factors from `n`. After removing them, every remaining prime factor is collected into `c`.

If a valid answer exists, then the prime factorization of `n` contains enough multiplicity and enough distinct prime factors to create three distinct numbers. Taking the first two factors greedily leaves the largest possible remainder for `c`, which maximizes the chance that `c` differs from the earlier choices.

Whenever the algorithm outputs a triple, the product is exactly `n` because:

```
c = n / (a × b)
```

and all three values are checked to be distinct and greater than `1`.

Whenever the algorithm fails, there is no way to construct three distinct factors. The remaining factorization structure is too small, causing one of the factors to repeat or become `1`.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    original = n

    a = -1
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            a = d
            n //= d
            break

    if a == -1:
        print("NO")
        continue

    b = -1
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0 and d != a:
            b = d
            n //= d
            break

    if b == -1:
        print("NO")
        continue

    c = original // (a * b)

    if c > 1 and c != a and c != b:
        print("YES")
        print(a, b, c)
    else:
        print("NO")
```

The first loop searches for the smallest divisor of the original number. This becomes `a`.

After dividing by `a`, the second loop searches for another divisor different from `a`. This becomes `b`.

The remaining quotient is computed from the original number rather than from the modified value of `n`. Either approach works, but using the original value makes the formula explicit and avoids mistakes when reasoning about the code.

The final distinctness check is essential. Without it, cases such as `12 = 2 × 3 × 2` would be incorrectly accepted.

All arithmetic fits comfortably inside Python integers, and there is no risk of overflow.

## Worked Examples

### Example 1

Input:

```
64
```

| Step | Current n | a | b | Action |
| --- | --- | --- | --- | --- |
| Start | 64 | - | - | Begin factorization |
| Find first divisor | 32 | 2 | - | Divide by 2 |
| Find second divisor | 8 | 2 | 4 | Divide by 4 |
| Compute c | 8 | 2 | 4 | c = 64 / (2×4) |

The resulting triple is:

```
2, 4, 8
```

All values are distinct and their product equals 64.

### Example 2

Input:

```
32
```

| Step | Current n | a | b | Action |
| --- | --- | --- | --- | --- |
| Start | 32 | - | - | Begin factorization |
| Find first divisor | 16 | 2 | - | Divide by 2 |
| Find second divisor | 4 | 2 | 4 | Divide by 4 |
| Compute c | 4 | 2 | 4 | c = 32 / (2×4) |

The candidate triple becomes:

```
2, 4, 4
```

Since `b = c`, the factors are not distinct, so the answer is `"NO"`.

This example shows why the final distinctness test cannot be skipped.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n) | Two trial-division scans up to the square root of the current value |
| Space | O(1) | Only a few integer variables are stored |

The largest possible input value is `10^9`, whose square root is about `31623`. Even with 100 test cases, this amount of work is easily handled within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        original = n

        a = -1
        for d in range(2, int(n ** 0.5) + 1):
            if n % d == 0:
                a = d
                n //= d
                break

        if a == -1:
            out.append("NO")
            continue

        b = -1
        for d in range(2, int(n ** 0.5) + 1):
            if n % d == 0 and d != a:
                b = d
                n //= d
                break

        if b == -1:
            out.append("NO")
            continue

        c = original // (a * b)

        if c > 1 and c != a and c != b:
            out.append("YES")
            out.append(f"{a} {b} {c}")
        else:
            out.append("NO")

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return result

# provided sample structure
out = run("5\n64\n32\n97\n2\n12345\n")
assert out.splitlines()[0] == "YES"
assert out.splitlines()[2] == "NO"
assert out.splitlines()[3] == "NO"
assert out.splitlines()[4] == "NO"

# prime number
assert run("1\n97\n").strip() == "NO"

# smallest input
assert run("1\n2\n").strip() == "NO"

# valid case with two prime factors
res = run("1\n72\n").splitlines()
assert res[0] == "YES"

# power of two that fails
assert run("1\n32\n").strip() == "NO"

# power of two that succeeds
res = run("1\n64\n").splitlines()
assert res[0] == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `97` | `NO` | Prime numbers cannot be decomposed |
| `2` | `NO` | Minimum input value |
| `72` | `YES` | Multiple prime factors with repeated powers |
| `32` | `NO` | Duplicate factor appears in every decomposition |
| `64` | `YES` | Large prime power can still produce three distinct factors |

## Edge Cases

Consider:

```
n = 12
```

The algorithm chooses:

```
a = 2
```

After division:

```
n = 6
```

The next distinct divisor is:

```
b = 3
```

The remainder becomes:

```
c = 12 / (2 × 3) = 2
```

Since `c = a`, the triple is not distinct. The algorithm correctly prints `"NO"`.

Consider:

```
n = 64
```

The factorization is:

```
64 = 2^6
```

The algorithm extracts:

```
a = 2
b = 4
c = 8
```

All three values are distinct, so it prints `"YES"`.

Consider:

```
n = 97
```

No divisor is found during the first search. Since 97 is prime, no decomposition into three integers greater than 1 exists. The algorithm immediately prints `"NO"`.

Consider:

```
n = 36
```

The algorithm finds:

```
a = 2
```

Then:

```
b = 3
```

Finally:

```
c = 36 / (2 × 3) = 6
```

The triple `(2, 3, 6)` is valid, and the algorithm prints `"YES"`. This case demonstrates how numbers with several prime factors naturally produce a valid decomposition.
