---
title: "CF 1475B - New Year's Number"
description: "We are given a number $n$, and we want to know whether it can be built by adding together some number of 2020s and some number of 2021s."
date: "2026-06-11T00:08:36+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1475
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 697 (Div. 3)"
rating: 900
weight: 1475
solve_time_s: 221
verified: true
draft: false
---

[CF 1475B - New Year's Number](https://codeforces.com/problemset/problem/1475/B)

**Rating:** 900  
**Tags:** brute force, dp, math  
**Solve time:** 3m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number $n$, and we want to know whether it can be built by adding together some number of 2020s and some number of 2021s.

If we choose $a$ copies of 2020 and $b$ copies of 2021, then the resulting value is

$$2020a + 2021b$$

The task is simply to determine whether there exist non-negative integers $a$ and $b$ that produce the given $n$.

The input contains up to $10^4$ test cases. Each value of $n$ is at most $10^6$. Since there can be many test cases, we want an algorithm that is essentially constant time per query. An approach that performs only a few arithmetic operations for each test case is ideal.

A few edge cases are easy to miss.

Consider:

```
1
2020
```

The correct answer is:

```
YES
```

because one copy of 2020 is allowed. A solution that mistakenly requires both numbers to appear at least once would fail.

Consider:

```
1
2019
```

The correct answer is:

```
NO
```

because every usable number is at least 2020. Any positive combination must be at least 2020.

Consider:

```
1
2021
```

The correct answer is:

```
YES
```

because a single 2021 is valid.

A more subtle case is:

```
1
4040
```

The correct answer is:

```
YES
```

since $4040 = 2020 + 2020$. A careless solution that only checks divisibility by 2021 would incorrectly reject it.

The key challenge is finding a mathematical characterization that avoids searching through many combinations.

## Approaches

The most direct approach is brute force. We can try every possible number of 2021s. Suppose we choose $b$ copies of 2021. The remaining value is

$$n - 2021b$$

If that remainder is non-negative and divisible by 2020, then we have found a valid representation.

This method is correct because every possible representation corresponds to exactly one value of $b$, and we check all of them.

The problem is efficiency. For $n = 10^6$, the number of possible values of $b$ is roughly

$$\frac{10^6}{2021} \approx 495.$$

Even that is actually small enough for this problem, so the brute force solution would pass. But there is a cleaner observation that reduces the whole question to a few arithmetic operations.

Rewrite the expression:

$$n = 2020a + 2021b$$

Since $2021 = 2020 + 1$,

$$n = 2020a + (2020+1)b$$

$$n = 2020(a+b) + b$$

Let

$$k = a+b.$$

Then

$$n = 2020k + b.$$

When dividing $n$ by 2020:

$$n = 2020 \left\lfloor \frac{n}{2020} \right\rfloor + (n \bmod 2020).$$

Comparing with the previous form, we see that $b$ must equal the remainder.

The remainder is fixed:

$$b = n \bmod 2020.$$

The quotient is:

$$k = \left\lfloor \frac{n}{2020} \right\rfloor.$$

Since $a = k-b$, we need

$$k \ge b.$$

Substituting the quotient and remainder gives a very simple condition:

$$\left\lfloor \frac{n}{2020} \right\rfloor \ge n \bmod 2020.$$

If this inequality holds, the answer is YES. Otherwise, the answer is NO.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n/2020)$ per test case | $O(1)$ | Accepted |
| Optimal | $O(1)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the value $n$.
2. Compute the quotient:

$$q = n // 2020$$

This represents the maximum possible value of $a+b$.
3. Compute the remainder:

$$r = n \% 2020$$

Any valid representation must use exactly $r$ copies of 2021.
4. Check whether

$$q \ge r.$$

If true, then we can choose $b=r$ and $a=q-r$, both non-negative.
5. Output `"YES"` when the inequality holds, otherwise output `"NO"`.

### Why it works

Every representation can be written as

$$n = 2020(a+b) + b.$$

The remainder after division by 2020 is uniquely determined, so any valid representation must have

$$b = n \bmod 2020.$$

The quotient gives

$$a+b = n // 2020.$$

For a valid solution, $a$ must be non-negative:

$$a = (n // 2020) - (n \bmod 2020) \ge 0.$$

This condition is both necessary and sufficient. If it holds, we can explicitly construct $a$ and $b$. If it fails, no non-negative choice of $a$ exists. Thus the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        q = n // 2020
        r = n % 2020

        if q >= r:
            ans.append("YES")
        else:
            ans.append("NO")

    sys.stdout.write("\n".join(ans))

solve()
```

The implementation follows the mathematical derivation directly.

The quotient `q` represents the total number of terms if every 2021 is viewed as a 2020 plus an extra 1. The remainder `r` represents how many of those extra 1s are needed, which is exactly the number of 2021s.

The only condition to verify is whether enough total terms exist to accommodate those `r` copies of 2021. That is exactly the check `q >= r`.

There are no overflow concerns because the largest value of `n` is only $10^6$, far below Python's integer limits. The implementation performs only integer division, modulo, and a comparison for each test case.

## Worked Examples

### Example 1

Input:

```
4041
```

| n | q = n // 2020 | r = n % 2020 | q ≥ r | Answer |
| --- | --- | --- | --- | --- |
| 4041 | 2 | 1 | Yes | YES |

Here $r=1$, so exactly one copy of 2021 must be used. Since $q=2$, we have enough total terms. The construction is $2020 + 2021$.

### Example 2

Input:

```
8079
```

| n | q = n // 2020 | r = n % 2020 | q ≥ r | Answer |
| --- | --- | --- | --- | --- |
| 8079 | 3 | 2019 | No | NO |

The remainder is 2019, which would require 2019 copies of 2021. But the quotient is only 3, meaning $a+b=3$. Those two facts cannot both be true, so no representation exists.

This example demonstrates the key invariant. The remainder fixes the required number of 2021s, and if that number exceeds the total available terms, the representation is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ per test case | One division, one modulo, one comparison |
| Space | $O(1)$ | Only a few variables are stored |

With at most $10^4$ test cases, the total work is only a few tens of thousands of arithmetic operations. This is comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        q = n // 2020
        r = n % 2020
        ans.append("YES" if q >= r else "NO")

    return "\n".join(ans)

# provided sample
assert run(
"""5
1
4041
4042
8081
8079
"""
) == (
"""NO
YES
YES
YES
NO"""
), "sample 1"

# minimum value
assert run(
"""1
1
"""
) == "NO", "smallest possible n"

# exact 2020
assert run(
"""1
2020
"""
) == "YES", "single 2020"

# exact 2021
assert run(
"""1
2021
"""
) == "YES", "single 2021"

# boundary near first achievable range
assert run(
"""2
2019
2022
"""
) == (
"""NO
NO"""
), "boundary values"

# maximum constraint
assert run(
"""1
1000000
"""
) == "YES", "largest n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `NO` | Values below 2020 are impossible |
| `2020` | `YES` | Single 2020 works |
| `2021` | `YES` | Single 2021 works |
| `2019`, `2022` | `NO`, `NO` | Boundary behavior around the first valid numbers |
| `1000000` | `YES` | Large input near the constraint limit |

## Edge Cases

Consider:

```
1
2019
```

The algorithm computes:

| q | r |
| --- | --- |
| 0 | 2019 |

Since $0 < 2019$, the answer is NO. This is correct because every available building block is at least 2020.

Consider:

```
1
2020
```

The algorithm computes:

| q | r |
| --- | --- |
| 1 | 0 |

Since $1 \ge 0$, the answer is YES. The resulting construction is one copy of 2020 and zero copies of 2021.

Consider:

```
1
2021
```

The algorithm computes:

| q | r |
| --- | --- |
| 1 | 1 |

Since $1 \ge 1$, the answer is YES. Here $a=0$ and $b=1$, giving exactly 2021.

Consider:

```
1
4040
```

The algorithm computes:

| q | r |
| --- | --- |
| 2 | 0 |

Since $2 \ge 0$, the answer is YES. The construction is $2020 + 2020$. This case confirms that using only one of the two allowed numbers is perfectly valid.

Consider:

```
1
8079
```

The algorithm computes:

| q | r |
| --- | --- |
| 3 | 2019 |

Since $3 < 2019$, the answer is NO. The remainder forces far more copies of 2021 than the quotient allows, making any representation impossible.
