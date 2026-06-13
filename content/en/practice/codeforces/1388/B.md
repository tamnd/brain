---
title: "CF 1388B - Captain Flint and a Long Voyage"
description: "We need to construct an $n$-digit decimal number $x$. Take every digit of $x$, write its binary representation without leading zeroes, and concatenate those binary strings. The resulting binary string is called $k$. After that, the last $n$ bits of $k$ are removed."
date: "2026-06-11T10:34:36+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1388
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 660 (Div. 2)"
rating: 1000
weight: 1388
solve_time_s: 132
verified: true
draft: false
---

[CF 1388B - Captain Flint and a Long Voyage](https://codeforces.com/problemset/problem/1388/B)

**Rating:** 1000  
**Tags:** greedy, math  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to construct an $n$-digit decimal number $x$.

Take every digit of $x$, write its binary representation without leading zeroes, and concatenate those binary strings. The resulting binary string is called $k$.

After that, the last $n$ bits of $k$ are removed. The remaining prefix is interpreted as a binary number $r$.

Our goal is to choose $x$ so that $r$ is as large as possible. If several different $x$ produce the same maximum $r$, we must output the smallest such $x$.

The input consists only of the length $n$. We never need to reconstruct $k$ explicitly for large values. The sum of all $n$ across test cases is at most $2 \cdot 10^5$, so any solution that processes each test case in linear time is easily fast enough. Anything exponential in $n$, or anything that attempts to search over all $n$-digit numbers, is completely impossible.

The tricky part is understanding what removing the last $n$ bits actually means. The value of $r$ depends only on the prefix of the concatenated binary string that survives the truncation. Since binary numbers are compared lexicographically by length and then by bits, we want that surviving prefix to be as large as possible.

Several edge cases are easy to misunderstand.

For $n=1$, the answer is not $9$. If $x=9$, then $k=1001$. Removing the last bit leaves $100$. If $x=8$, then $k=1000$, and removing the last bit leaves $100$ as well. Both give the same maximum $r$, but $8$ is smaller, so the correct answer is:

```
Input:
1

Output:
8
```

Another subtle case is $n=2$. A naive idea might be to maximize every digit and output $99$. Then:

$$k = 1001\,1001$$

Removing the last two bits leaves $100110$.

For $98$:

$$k = 1001\,1000$$

Removing the last two bits also leaves $100110$.

Since both achieve the same maximum $r$, we must choose the smaller number, namely $98$.

A final pitfall is assuming that only the last digit matters. For $n=3$, the answer is $998$, not $989$. The placement of the digits determines which bits survive after truncation, and the optimal structure turns out to require several trailing 8s.

## Approaches

The brute-force idea is straightforward. Enumerate every $n$-digit number $x$, build the binary string $k$, remove its last $n$ bits, compute $r$, and keep the best candidate.

This is correct because it checks every possibility. Unfortunately, even for $n=10$, there are $9 \cdot 10^9$ candidates. The actual constraints allow $n$ up to $10^5$, so exhaustive search is not remotely feasible.

To find the pattern, we need to understand how $r$ is formed.

Digits $8$ and $9$ are special because they have the longest binary representations among decimal digits:

$$8 = 1000,\qquad 9 = 1001.$$

Both contribute four bits. Every other digit contributes at most three bits.

The length of the surviving prefix $r$ is

$$|k| - n.$$

To maximize a binary number, the first priority is maximizing its length. Since each digit contributes at most four bits, we should make every digit contribute four bits whenever possible. That means every digit should be either $8$ or $9$.

Now all candidates have the same total binary length $4n$, so every resulting $r$ has length $3n$. The comparison becomes lexicographic.

Observe that the binary strings of $8$ and $9$ differ only in the last bit:

$$1000,\qquad 1001.$$

The last $n$ bits of the concatenation are discarded. Any bit that falls entirely inside the removed suffix has no effect on $r$.

Suppose we place an $8$ near the end. Its last bit is $0$ instead of the $1$ provided by a $9$. If that differing bit is removed anyway, changing a $9$ to an $8$ does not affect $r$, while making $x$ smaller.

The optimal strategy is therefore:

1. Use only digits $8$ and $9$.
2. Keep as many leading digits as possible equal to $9$, because their differing bits survive inside $r$.
3. Replace the largest possible suffix by $8$, because the differing bits of those digits lie inside the discarded portion.

How many trailing digits can be changed to $8$?

Each digit contributes four bits. The discarded suffix has length $n$. A digit's distinguishing bit is its fourth bit. We can safely hide that bit inside the removed suffix for exactly

$$\left\lceil \frac{n}{4} \right\rceil$$

digits at the end.

Thus the answer is:

$$\underbrace{99\ldots9}_{n-\lceil n/4\rceil} \underbrace{88\ldots8}_{\lceil n/4\rceil}.$$

This is the well-known Codeforces solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $n$ | Exponential | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read $n$.
2. Compute

$$m = \left\lceil \frac{n}{4} \right\rceil.$$

This is the number of trailing digits that can be changed from $9$ to $8$ without affecting the maximum value of $r$.

1. The first $n-m$ positions should be digit $9$.

These digits contribute bits that remain inside the surviving prefix, so making them $9$ gives the lexicographically largest possible $r$.
2. The last $m$ positions should be digit $8$.

Their distinguishing bits lie inside the discarded suffix, so replacing $9$ by $8$ keeps $r$ unchanged while making $x$ smaller.
3. Output the resulting string.

### Why it works

Any digit other than $8$ or $9$ contributes fewer than four bits, reducing the total length of $k$. Since $r$ has length $|k|-n$, this immediately produces a shorter binary number and cannot be optimal.

After restricting ourselves to digits $8$ and $9$, every digit contributes exactly four bits. The only difference between them is the final bit of their binary representation. The last $n$ bits of the concatenation are discarded, so the distinguishing bits of the final $\lceil n/4\rceil$ digits never appear in $r$. Those digits may be changed from $9$ to $8$ without affecting $r$.

Any earlier digit still influences $r$. Changing such a digit from $9$ to $8$ replaces a surviving bit $1$ by $0$, making $r$ smaller. Hence all earlier positions must remain $9$.

Among all numbers producing the maximum possible $r$, this construction minimizes $x$ because it replaces every possible trailing $9$ by $8$.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
ans = []

for _ in range(t):
    n = int(input())
    eights = (n + 3) // 4
    nines = n - eights
    ans.append("9" * nines + "8" * eights)

print("\n".join(ans))
```

The implementation directly follows the mathematical characterization.

The expression `(n + 3) // 4` computes $\lceil n/4 \rceil$ using integer arithmetic. This is the only non-trivial detail.

The first part of the answer contains `n - eights` copies of `'9'`. The second part contains `eights` copies of `'8'`.

No binary strings are constructed. The solution only builds the final decimal answer, which is why it remains linear in the output size.

A common mistake is using `n // 4` instead of ceiling division. For example, when `n = 1`, floor division gives `0`, producing `"9"` instead of the correct answer `"8"`.

## Worked Examples

### Example 1

Input:

```
n = 1
```

| Step | Value |
| --- | --- |
| n | 1 |
| eights | (1 + 3) // 4 = 1 |
| nines | 0 |
| answer | 8 |

Output:

```
8
```

This example shows why ceiling division is required. The entire digit belongs to the removable region, so the smallest optimal choice is `8`.

### Example 2

Input:

```
n = 3
```

| Step | Value |
| --- | --- |
| n | 3 |
| eights | (3 + 3) // 4 = 1 |
| nines | 2 |
| answer | 998 |

Output:

```
998
```

This is the sample from the statement. Only the final digit can be changed to `8` without reducing the optimal value of $r$.

### Example 3

Input:

```
n = 7
```

| Step | Value |
| --- | --- |
| n | 7 |
| eights | (7 + 3) // 4 = 2 |
| nines | 5 |
| answer | 9999988 |

Output:

```
9999988
```

This example illustrates that the suffix of `8`s grows every four positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Constructing the output string requires $n$ characters |
| Space | $O(n)$ | The produced answer itself contains $n$ characters |

The sum of all $n$ values is at most $2 \cdot 10^5$, so the total amount of work across all test cases is linear in the total output size. This is comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        eights = (n + 3) // 4
        ans.append("9" * (n - eights) + "8" * eights)

    return "\n".join(ans)

# provided sample
assert run("2\n1\n3\n") == "8\n998", "sample"

# minimum size
assert run("1\n1\n") == "8", "n = 1"

# boundary around multiple of four
assert run("1\n4\n") == "9998", "exact multiple of four"

# just after multiple of four
assert run("1\n5\n") == "99988", "ceiling division"

# larger case
assert run("1\n8\n") == "99999988", "two trailing eights"

# maximum style stress case
n = 100000
expected = "9" * 75000 + "8" * 25000
assert run(f"1\n{n}\n") == expected, "maximum length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1` | `8` | Smallest possible input |
| `n=4` | `9998` | Exact multiple of four |
| `n=5` | `99988` | Correct ceiling division |
| `n=8` | `99999988` | Two trailing eights |
| `n=100000` | 75000 nines followed by 25000 eights | Maximum constraint |

## Edge Cases

Consider the smallest input:

```
1
1
```

The algorithm computes:

$$\left\lceil \frac{1}{4} \right\rceil = 1.$$

So the answer is `8`. Using floor division would incorrectly produce `9`. The construction handles this boundary correctly.

Consider:

```
1
4
```

The algorithm computes:

$$\left\lceil \frac{4}{4} \right\rceil = 1.$$

The output is:

```
9998
```

Only the final digit belongs to the removable region. Any earlier replacement by `8` would reduce the resulting value of $r$.

Consider:

```
1
5
```

The algorithm computes:

$$\left\lceil \frac{5}{4} \right\rceil = 2.$$

The output is:

```
99988
```

This case catches the most common off-by-one error. Using floor division would produce only one trailing `8`, which is not the minimum valid answer among all optimal constructions.

Finally, for a very large value such as:

```
1
100000
```

the algorithm never builds binary representations and never performs any expensive computation. It simply outputs 75,000 nines followed by 25,000 eights, remaining linear in the output size.
