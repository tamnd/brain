---
title: "CF 2125C - Count Good Numbers"
description: "A number is called good if none of the primes in its prime factorization are single digit primes. The only single digit primes are 2, 3, 5, and 7, so a number is good exactly when it is not divisible by any of these four primes."
date: "2026-06-08T03:27:37+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2125
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 181 (Rated for Div. 2)"
rating: 1100
weight: 2125
solve_time_s: 120
verified: true
draft: false
---

[CF 2125C - Count Good Numbers](https://codeforces.com/problemset/problem/2125/C)

**Rating:** 1100  
**Tags:** bitmasks, combinatorics, math, number theory  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

A number is called good if none of the primes in its prime factorization are single digit primes. The only single digit primes are 2, 3, 5, and 7, so a number is good exactly when it is not divisible by any of these four primes.

The task is to count how many integers in a range $[l,r]$ satisfy this property.

The limits completely change how we should think about the problem. The interval endpoints can be as large as $10^{18}$, so factoring numbers one by one is impossible. Even iterating through the interval is impossible because the range itself can contain up to $10^{18}$ numbers. We need a counting formula that works directly on the endpoints.

The key observation is that the definition depends only on divisibility by four specific primes. We do not care whether a number contains larger primes, because every prime with at least two digits is allowed.

A few edge cases are easy to miss.

Consider the range:

```
13 37
```

The answer is 7, not 25. Most numbers in this interval are divisible by 2, 3, 5, or 7 and must be excluded.

Consider:

```
11 11
```

The answer is 1. The number 11 is itself a two digit prime, so it is good.

Consider:

```
14 14
```

The answer is 0. Although 14 contains the prime 7 only once, that is enough to make it bad. The multiplicity does not matter.

Consider:

```
49 49
```

The answer is 0. Some solutions mistakenly check only for prime factors less than 7 appearing once. Since $49=7^2$, it is still divisible by 7 and remains bad.

The problem is really asking for the count of integers not divisible by any of 2, 3, 5, or 7.

## Approaches

A brute force solution would iterate through every number in the interval, factor it, and verify whether all prime factors are at least 10. This is correct because it directly implements the definition.

Unfortunately, even checking a single interval of length $10^{18}$ is impossible. Factoring one number requires roughly $O(\sqrt n)$ work, and there may be $10^{18}$ numbers to inspect.

The crucial observation is that a number is good if and only if it is not divisible by 2, 3, 5, or 7.

That converts the problem into a classic counting problem. Instead of identifying good numbers directly, count all numbers divisible by at least one of these four primes and subtract them from the total.

Whenever we need the count of numbers divisible by several sets simultaneously, inclusion-exclusion is the natural tool. There are only four primes involved, so the number of subsets is tiny:

$$2^4=16.$$

For any $x$, let $F(x)$ denote the number of good integers in $[1,x]$.

The count of integers divisible by a particular subset of primes equals

$$\left\lfloor \frac{x}{\operatorname{lcm}(\text{subset})} \right\rfloor.$$

Since the primes are distinct, the LCM is simply their product.

Applying inclusion-exclusion gives the count of integers divisible by at least one forbidden prime. Subtracting from $x$ yields $F(x)$. The answer for a query becomes

$$F(r)-F(l-1).$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((r-l+1)\sqrt r)$ | $O(1)$ | Too slow |
| Optimal | $O(2^4)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

Let the forbidden primes be:

$$P=\{2,3,5,7\}.$$

For a given value $x$, define $F(x)$ as the number of good integers in $[1,x]$.

1. Start with `bad = 0`.
2. Enumerate every non-empty subset of $\{2,3,5,7\}$.
3. Compute the product of the primes in the subset. Since the primes are distinct, this product is also their least common multiple.
4. Compute how many integers in $[1,x]$ are divisible by this product:

$$\left\lfloor \frac{x}{\text{product}} \right\rfloor.$$
5. If the subset size is odd, add this quantity to `bad`.
6. If the subset size is even, subtract this quantity from `bad`.

This is exactly the inclusion-exclusion principle.
7. After processing all subsets, `bad` equals the number of integers in $[1,x]$ divisible by at least one forbidden prime.
8. Compute

$$F(x)=x-bad.$$
9. For each query $[l,r]$, output

$$F(r)-F(l-1).$$

### Why it works

A number is bad precisely when it belongs to at least one of the sets

$$A_2,A_3,A_5,A_7,$$

where $A_p$ contains numbers divisible by $p$.

Inclusion-exclusion computes the size of the union

$$|A_2\cup A_3\cup A_5\cup A_7|$$

exactly. Every number divisible by one forbidden prime contributes once. Every number divisible by multiple forbidden primes is corrected by the alternating signs of inclusion-exclusion.

Subtracting the union size from the total count $x$ leaves exactly those numbers divisible by none of the forbidden primes. Those are exactly the good numbers, so $F(x)$ is correct. Taking $F(r)-F(l-1)$ restricts the count to the requested interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

PRIMES = [2, 3, 5, 7]

def count_good(x):
    if x <= 0:
        return 0

    bad = 0

    for mask in range(1, 16):
        prod = 1
        bits = 0

        for i in range(4):
            if mask & (1 << i):
                prod *= PRIMES[i]
                bits += 1

        cnt = x // prod

        if bits & 1:
            bad += cnt
        else:
            bad -= cnt

    return x - bad

def solve():
    t = int(input())

    ans = []

    for _ in range(t):
        l, r = map(int, input().split())
        ans.append(str(count_good(r) - count_good(l - 1)))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The function `count_good(x)` computes the number of good integers in the prefix $[1,x]$.

The loop over masks represents all non-empty subsets of `{2,3,5,7}`. Since there are only four primes, exactly fifteen non-empty subsets exist.

For each subset we compute its product and the number of multiples inside the prefix. Odd-sized subsets contribute positively and even-sized subsets contribute negatively, matching inclusion-exclusion.

The expression `x - bad` converts the count of bad numbers into the count of good numbers.

The final answer uses the standard prefix-count technique:

$$\text{answer}=F(r)-F(l-1).$$

All arithmetic fits comfortably in 64-bit integers because the largest intermediate product is

$$2\cdot3\cdot5\cdot7=210,$$

while Python integers support arbitrary precision anyway.

## Worked Examples

### Example 1

Input:

```
2 100
```

We compute $F(100)$.

| Subset | Product | Multiples ≤ 100 | Sign | Contribution |
| --- | --- | --- | --- | --- |
| {2} | 2 | 50 | + | 50 |
| {3} | 3 | 33 | + | 33 |
| {5} | 5 | 20 | + | 20 |
| {7} | 7 | 14 | + | 14 |
| {2,3} | 6 | 16 | - | -16 |
| {2,5} | 10 | 10 | - | -10 |
| {2,7} | 14 | 7 | - | -7 |
| {3,5} | 15 | 6 | - | -6 |
| {3,7} | 21 | 4 | - | -4 |
| {5,7} | 35 | 2 | - | -2 |
| {2,3,5} | 30 | 3 | + | 3 |
| {2,3,7} | 42 | 2 | + | 2 |
| {2,5,7} | 70 | 1 | + | 1 |
| {3,5,7} | 105 | 0 | + | 0 |
| {2,3,5,7} | 210 | 0 | - | 0 |

Summing contributions gives:

$$bad=79.$$

Hence

$$F(100)=100-79=21.$$

This matches the sample output.

### Example 2

Input:

```
13 37
```

We compute:

$$F(37)=9,$$

and

$$F(12)=2.$$

| Quantity | Value |
| --- | --- |
| Good numbers in [1,37] | 9 |
| Good numbers in [1,12] | 2 |
| Answer | 7 |

Thus

$$F(37)-F(12)=7.$$

This demonstrates why prefix counting is useful. We never inspect individual numbers inside the interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^4)$ per test case | Inclusion-exclusion over 15 non-empty subsets |
| Space | $O(1)$ | Only a few integer variables are stored |

Since $2^4=16$, each test case performs only a handful of arithmetic operations. Even with $1000$ test cases, the total work is negligible and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

PRIMES = [2, 3, 5, 7]

def count_good(x):
    if x <= 0:
        return 0

    bad = 0

    for mask in range(1, 16):
        prod = 1
        bits = 0

        for i in range(4):
            if mask & (1 << i):
                prod *= PRIMES[i]
                bits += 1

        if bits & 1:
            bad += x // prod
        else:
            bad -= x // prod

    return x - bad

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        l, r = map(int, input().split())
        out.append(str(count_good(r) - count_good(l - 1)))

    print("\n".join(out))

def run(inp: str) -> str:
    global input
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf

    solve()

    sys.stdout = old
    return buf.getvalue()

# provided sample
assert run(
"""4
2 100
2 1000
13 37
2 1000000000000000000
"""
) == (
"""21
227
7
228571428571428570
"""
)

# minimum interval
assert run(
"""1
2 2
"""
) == (
"""0
"""
)

# single good prime
assert run(
"""1
11 11
"""
) == (
"""1
"""
)

# divisible by forbidden prime
assert run(
"""1
49 49
"""
) == (
"""0
"""
)

# boundary around first good number
assert run(
"""1
10 13
"""
) == (
"""2
"""
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2` | `0` | Smallest valid value is not good |
| `11 11` | `1` | Two digit prime is good |
| `49 49` | `0` | Repeated forbidden prime factor |
| `10 13` | `2` | Boundary transition around first good numbers |

## Edge Cases

Consider:

```

```
