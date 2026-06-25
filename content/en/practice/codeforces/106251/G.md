---
title: "CF 106251G - Busy Beaver's Faulty Machine"
description: "We are given a positive integer $X$ written in base $B$ as a sequence of digits. The task is to determine whether there exist two positive integers $Y$ and $Z$ such that: $$X + Y = Z$$ and the base-$B$ representations of $Y$ and $Z$ contain exactly the same multiset of digits."
date: "2026-06-25T07:22:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106251
codeforces_index: "G"
codeforces_contest_name: "MITIT Winter 2025-26 Beginner Round"
rating: 0
weight: 106251
solve_time_s: 56
verified: true
draft: false
---

[CF 106251G - Busy Beaver's Faulty Machine](https://codeforces.com/problemset/problem/106251/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer $X$ written in base $B$ as a sequence of digits.

The task is to determine whether there exist two positive integers $Y$ and $Z$ such that:

$$X + Y = Z$$

and the base-$B$ representations of $Y$ and $Z$ contain exactly the same multiset of digits. The order of digits may differ, but every digit must appear the same number of times in both numbers.

If such numbers exist, we must output one valid pair. Otherwise, we output `NO`.

The input size is large. A single number may contain up to $10^5$ digits, and the total number of digits across all test cases is at most $2 \cdot 10^5$. Any solution that tries to convert the whole value into a built-in integer type is impossible. We need an algorithm that works directly on the base-$B$ digit representation and runs in linear time.

The most important observation comes from digit sums. Any two numbers with the same multiset of digits have exactly the same digit sum. In base $B$,

$$N \equiv \text{sum of digits of } N \pmod{B-1}.$$

Since $Y$ and $Z$ use the same digits,

$$Y \equiv Z \pmod{B-1}.$$

Using $Z-Y=X$,

$$X \equiv 0 \pmod{B-1}.$$

This is a necessary condition.

A careless implementation might stop here and only test divisibility. The harder part is proving that this condition is also sufficient and constructing a valid answer.

Consider a small example in base $10$:

```
X = 36
```

The digit sum is $3+6=9$, so $X$ is divisible by $9$. A valid answer is

```
Y = 105
Z = 150
```

Both use the digits `{1,0,5}`, and

$$150 - 105 = 45 \neq 36.$$

Having the same digits is not enough. The construction must produce exactly the required difference.

Another edge case is when $X$ has only one digit.

```
B = 2
X = 1
```

Since $B-1=1$, every number is divisible by $B-1$. A solution must still exist. Any approach that assumes the quotient has multiple digits would fail here.

A third subtle case is when the quotient contains leading zeros after division. For example,

```
B = 10
X = 18
```

Then $X/(B-1)=2$. The quotient representation is simply `[2]`, not `[0,2]`. Long division must remove leading zeros correctly.

## Approaches

The brute-force idea is to generate candidate digit multisets, build all permutations for $Y$ and $Z$, and check whether $Z-Y=X$. This works only for extremely tiny inputs because the number of permutations grows factorially with the number of digits. Even a length of 20 already makes the search completely infeasible.

The key observation is modular arithmetic.

Because $Y$ and $Z$ contain the same digits, they have the same digit sum. In base $B$, every number is congruent to its digit sum modulo $B-1$. Hence

$$Y \equiv Z \pmod{B-1}.$$

Since $X=Z-Y$,

$$X \equiv 0 \pmod{B-1}.$$

This immediately gives a necessary condition.

The surprising part is that it is also sufficient.

Let

$$K=\frac{X}{B-1}.$$

Suppose the base-$B$ digits of $K$ are

$$d_1,d_2,\ldots,d_m.$$

Construct

$$Y = (1,0,d_1,d_2,\ldots,d_m)_B$$

and

$$Z = (1,d_1,d_2,\ldots,d_m,0)_B.$$

The two numbers clearly contain exactly the same digits: both contain one digit `1`, one digit `0`, and all digits of $K$.

Numerically,

$$Y = 1\cdot B^{m+1}+K,$$

$$Z = 1\cdot B^{m+1}+B\cdot K.$$

Subtracting,

$$Z-Y=(B-1)K=X.$$

So every $X$ divisible by $B-1$ admits a solution.

The entire problem reduces to:

1. Check whether $X$ is divisible by $B-1$.
2. If not, output `NO`.
3. Otherwise compute $K=X/(B-1)$ using long division on the digit array.
4. Output the construction above.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read the base-$B$ digits of $X$.
2. Compute the digit sum modulo $B-1$.

Since $B \equiv 1 \pmod{B-1}$, a number is divisible by $B-1$ exactly when its digit sum is divisible by $B-1$.
3. If the remainder is nonzero, output `NO`.

No valid pair can exist because any two numbers with the same digit multiset are congruent modulo $B-1$.
4. Divide the digit array of $X$ by $B-1$ using standard long division in base $B$.

Maintain a remainder. For each digit, update

$$cur = remainder \cdot B + digit,$$

emit

$$cur // (B-1),$$

and keep

$$cur \bmod (B-1).$$
5. Remove leading zero digits from the quotient. The remaining digits are the base-$B$ representation of $K$.
6. Let the quotient digits be $d_1,\ldots,d_m$.
7. Output

$$Y=(1,0,d_1,\ldots,d_m)$$

and

$$Z=(1,d_1,\ldots,d_m,0).$$

### Why it works

The divisibility test is necessary because equal digit multisets imply equal digit sums, and numbers are congruent to their digit sums modulo $B-1$. Hence every valid $X$ must satisfy $X \equiv 0 \pmod{B-1}$.

When this condition holds, we define $K=X/(B-1)$. The construction places the same digits into $Y$ and $Z$, merely changing their positions. Their leading digit is always `1`, so neither number has leading zeros.

The numerical difference is

$$(1\cdot B^{m+1}+BK) - (1\cdot B^{m+1}+K)
= (B-1)K
= X.$$

Thus the construction satisfies both required properties, proving sufficiency.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
out = []

for _ in range(t):
    n, b = map(int, input().split())
    a = list(map(int, input().split()))

    mod = b - 1

    if sum(a) % mod != 0:
        out.append("NO")
        continue

    # Long division: X / (B - 1)
    q = []
    rem = 0

    for digit in a:
        cur = rem * b + digit
        q.append(cur // mod)
        rem = cur % mod

    idx = 0
    while idx < len(q) - 1 and q[idx] == 0:
        idx += 1
    q = q[idx:]

    m = len(q) + 2

    y = [1, 0] + q
    z = [1] + q + [0]

    out.append("YES")
    out.append(str(m))
    out.append(" ".join(map(str, y)))
    out.append(" ".join(map(str, z)))

sys.stdout.write("\n".join(out))
```

The first part checks divisibility by $B-1$ using the digit-sum rule. This avoids ever reconstructing the enormous value of $X$.

The long-division section computes $K=X/(B-1)$ directly from the digit array. Every intermediate value is at most

$$(B-2)\cdot B + (B-1) < B^2,$$

which easily fits in standard integers.

After division, leading zeros are removed. This is important because the quotient must be represented in canonical form.

The final construction is exactly the proof. The two arrays contain the same digits, neither starts with zero, and their difference equals $X$.

## Worked Examples

### Example 1

Input:

```
N = 2, B = 10
X = [3, 6]
```

Digit sum is $9$, divisible by $9$.

Long division by $9$:

| Position | Digit | Current Value | Quotient Digit | Remainder |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 0 | 3 |
| 2 | 6 | 36 | 4 | 0 |

So $K=[4]$.

Construction:

| Variable | Digits |
| --- | --- |
| Y | [1, 0, 4] |
| Z | [1, 4, 0] |

Numerically,

$$140 - 104 = 36.$$

This demonstrates the core construction.

### Example 2

Input:

```
N = 4, B = 5
X = [1, 4, 3, 4]
```

Digit sum:

$$1+4+3+4=12.$$

Since $12 \equiv 0 \pmod 4$, a solution exists.

Long division by $4$:

| Position | Digit | Current Value | Quotient Digit | Remainder |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 1 |
| 2 | 4 | 9 | 2 | 1 |
| 3 | 3 | 8 | 2 | 0 |
| 4 | 4 | 4 | 1 | 0 |

Quotient digits are `[2, 2, 1]`.

Construction:

| Variable | Digits |
| --- | --- |
| Y | [1, 0, 2, 2, 1] |
| Z | [1, 2, 2, 1, 0] |

The two numbers use exactly the same digits, and their difference is the original $X$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | One divisibility scan and one long-division scan |
| Space | O(N) | Stores the quotient digits and output |
|  |  |  |

The total number of processed digits across all test cases is at most $2 \cdot 10^5$, so linear complexity easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, b = map(int, input().split())
        a = list(map(int, input().split()))

        mod = b - 1

        if sum(a) % mod != 0:
            out.append("NO")
            continue

        q = []
        rem = 0

        for digit in a:
            cur = rem * b + digit
            q.append(cur // mod)
            rem = cur % mod

        idx = 0
        while idx < len(q) - 1 and q[idx] == 0:
            idx += 1
        q = q[idx:]

        m = len(q) + 2
        y = [1, 0] + q
        z = [1] + q + [0]

        out.append("YES")
        out.append(str(m))
        out.append(" ".join(map(str, y)))
        out.append(" ".join(map(str, z)))

    return "\n".join(out)

# sample NO case
assert run(
"""1
5 12
4 8 8 3 1
"""
) == "NO"

# base 2, minimum length
assert run(
"""1
1 2
1
"""
).startswith("YES")

# divisible by B-1
assert run(
"""1
2 10
3 6
"""
).startswith("YES")

# not divisible
assert run(
"""1
1 10
5
"""
) == "NO"

# all digits zero except leading digit
assert run(
"""1
3 10
9 0 0
"""
).startswith("YES")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 12 / 4 8 8 3 1` | `NO` | Fails divisibility condition |
| `1 2 / 1` | `YES` | Smallest possible size |
| `2 10 / 3 6` | `YES` | Basic constructive case |
| `1 10 / 5` | `NO` | Non-divisible single digit |
| `3 10 / 9 0 0` | `YES` | Quotient with leading zeros after division |

## Edge Cases

Consider:

```
1
1 10
5
```

The digit sum is $5$. Since $5 \not\equiv 0 \pmod 9$, the algorithm immediately outputs `NO`. Any valid pair would require $X\equiv0\pmod9$, so rejection is correct.

Consider:

```
1
1 2
1
```

Here $B-1=1$. Every integer is divisible by $1$. Long division gives $K=1$. The construction produces

```
Y = [1,0,1]
Z = [1,1,0]
```

and

$$110_2 - 101_2 = 1.$$

The smallest possible input is handled naturally.

Consider:

```
1
2 10
1 8
```

We have $18/9=2$. Long division initially generates quotient digits `[0,2]`. The leading zero is removed, leaving `[2]`. The construction then uses the canonical representation of $K$, preventing accidental leading zeros in the output.
