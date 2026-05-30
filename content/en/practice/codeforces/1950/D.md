---
title: "CF 1950D - Product of Binary Decimals"
description: "We are given up to 50,000 independent queries. For each query, a number n is provided, where 1 ≤ n ≤ 100000. A number is called a binary decimal if every digit in its usual decimal representation is either 0 or 1. Examples include 1, 10, 11, 101, and 1001."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "implementation", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1950
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 937 (Div. 4)"
rating: 1100
weight: 1950
solve_time_s: 77
verified: true
draft: false
---

[CF 1950D - Product of Binary Decimals](https://codeforces.com/problemset/problem/1950/D)

**Rating:** 1100  
**Tags:** brute force, dp, implementation, number theory  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given up to 50,000 independent queries. For each query, a number `n` is provided, where `1 ≤ n ≤ 100000`.

A number is called a binary decimal if every digit in its usual decimal representation is either `0` or `1`. Examples include `1`, `10`, `11`, `101`, and `1001`.

The task is to determine whether `n` can be written as a product of one or more binary decimals. Repetition is allowed, so something like `121 = 11 × 11` is valid.

The most important observation from the constraints is that `n` never exceeds `100000`. Although there are many test cases, the universe of possible values is very small. Instead of solving each query from scratch, we can preprocess all numbers up to `100000` once and answer every test case in constant time.

A few edge cases deserve attention.

Consider:

```
1
1
```

The correct answer is `YES`. The number `1` is itself a binary decimal. A solution that only tries to factor numbers into smaller binary decimals could accidentally reject it.

Consider:

```
1
100000
```

The correct answer is `YES`, because every digit is either `0` or `1`, so the number itself is already a valid product consisting of one factor.

Consider:

```
1
99
```

The correct answer is `NO`. Although `99 = 9 × 11`, the factor `9` is not a binary decimal. A careless implementation that only checks whether some divisor is binary-decimal and recursively ignores the remaining factor's validity would produce the wrong answer.

Another subtle case is:

```
1
121
```

The answer is `YES`, even though `121` itself is not a binary decimal. It equals `11 × 11`, so we must consider products of binary decimals, not just numbers whose own digits are `0` and `1`.

## Approaches

A direct brute-force idea is to recursively factor every number. For a given `n`, enumerate all binary decimals not exceeding `n`, try dividing by each one, and recursively check the quotient.

This is correct because every valid representation can be viewed as repeatedly removing one binary-decimal factor at a time. The problem is repetition. With up to 50,000 test cases, many numbers are checked again and again. Recursive exploration also revisits the same states through different factorization orders.

The key observation comes from the very small limit, `n ≤ 100000`.

How many binary decimals are there up to `100000`? A six-digit number whose digits are restricted to `{0,1}` has at most `2^6 = 64` possibilities. After excluding invalid values such as leading-zero forms and numbers exceeding `100000`, only a few dozen remain.

This turns the problem into a reachability question.

Start from `1`, which is certainly representable. If a number `x` is representable, then `x × b` is also representable for every binary decimal `b`, provided the product does not exceed `100000`.

We can build every representable number up to `100000` using a simple dynamic process. Once preprocessing finishes, answering a query is just checking whether `n` was reached.

This is essentially a graph where each number points to `number × binary_decimal`. Since there are only `100000` states and only a few dozen binary-decimal multipliers, the entire reachable set can be computed once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in factorization depth | O(depth) | Too slow |
| Optimal | O(MAX × B) preprocessing, O(1) per query | O(MAX) | Accepted |

Here `MAX = 100000` and `B` is the number of binary decimals up to `100000`, which is only a few dozen.

## Algorithm Walkthrough

1. Generate every binary decimal not exceeding `100000`.

A number is a binary decimal if each decimal digit is either `0` or `1`. Since the limit is small, we can simply test every number from `1` to `100000`.
2. Create a boolean array `reachable` of size `100001`.

`reachable[x]` will mean that `x` can be expressed as a product of binary decimals.
3. Mark `reachable[1] = True`.

The number `1` is itself a binary decimal, so it is a valid starting state.
4. Iterate through all numbers from `1` to `100000`.

Whenever `reachable[x]` is true, treat `x` as a known valid product.
5. For every binary decimal `b`, compute `x × b`.

If the product does not exceed `100000`, mark it reachable.

This mirrors the definition of the problem. Multiplying a valid product by another binary decimal produces another valid product.
6. After preprocessing, answer each test case by printing `YES` if `reachable[n]` is true and `NO` otherwise.

### Why it works

The proof follows directly from closure under multiplication.

Initially, `reachable[1]` is true. Every time the algorithm marks a new number, it does so by multiplying an already representable number by a binary decimal. Thus every marked number is genuinely representable.

For the other direction, suppose a number `n` can be written as a product of binary decimals:

```
n = b1 × b2 × ... × bk
```

Starting from `1`, the preprocessing can multiply by `b1`, then by `b2`, and so on. Each intermediate product is marked reachable, so eventually `n` is marked as well.

The set produced by the algorithm is exactly the set of numbers representable as products of binary decimals.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 100000

def is_binary_decimal(x):
    while x:
        d = x % 10
        if d != 0 and d != 1:
            return False
        x //= 10
    return True

binary_decimals = []
for x in range(1, MAXN + 1):
    if is_binary_decimal(x):
        binary_decimals.append(x)

reachable = [False] * (MAXN + 1)
reachable[1] = True

for x in range(1, MAXN + 1):
    if not reachable[x]:
        continue

    for b in binary_decimals:
        y = x * b
        if y > MAXN:
            break
        reachable[y] = True

t = int(input())
ans = []

for _ in range(t):
    n = int(input())
    ans.append("YES" if reachable[n] else "NO")

sys.stdout.write("\n".join(ans))
```

The first part generates all binary decimals up to `100000`. Since the limit is tiny, checking each number digit-by-digit is completely affordable.

The `reachable` array stores the preprocessing result. We begin from `1` and repeatedly multiply by every binary decimal. Because numbers are processed in increasing order, every reachable value eventually propagates its reachability to larger products.

A useful implementation detail is the `break` inside the multiplication loop. The list of binary decimals is sorted. Once `x * b` exceeds `100000`, every later multiplier will also exceed the limit, so continuing would be wasted work.

No special handling is needed for `1`. Since it is both the starting state and a binary decimal, the preprocessing naturally handles it.

## Worked Examples

### Example 1

Input:

```
121
```

Relevant preprocessing trace:

| Current x | Binary decimal used | Product y | reachable[y] |
| --- | --- | --- | --- |
| 1 | 11 | 11 | True |
| 11 | 11 | 121 | True |

After preprocessing:

| Query n | reachable[n] | Output |
| --- | --- | --- |
| 121 | True | YES |

This demonstrates that a number does not need to be a binary decimal itself. It is enough that it can be built by multiplying binary-decimal factors.

### Example 2

Input:

```
99
```

Relevant reachable values near 99:

| Number | Reachable? |
| --- | --- |
| 11 | True |
| 22 | True |
| 55 | True |
| 99 | False |

Query phase:

| Query n | reachable[n] | Output |
| --- | --- | --- |
| 99 | False | NO |

This demonstrates that having a binary-decimal divisor is not sufficient. Every factor in the product decomposition must ultimately be binary-decimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MAX × B + t) | Preprocessing visits every reachable state and tries all binary-decimal multipliers |
| Space | O(MAX) | The reachability array stores one boolean per number |

With `MAX = 100000` and only a few dozen binary decimals, preprocessing is easily fast enough. Each query is answered in constant time, which is ideal for as many as 50,000 test cases.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MAXN = 100000

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def is_binary_decimal(x):
        while x:
            d = x % 10
            if d != 0 and d != 1:
                return False
            x //= 10
        return True

    binary_decimals = [
        x for x in range(1, MAXN + 1)
        if is_binary_decimal(x)
    ]

    reachable = [False] * (MAXN + 1)
    reachable[1] = True

    for x in range(1, MAXN + 1):
        if not reachable[x]:
            continue
        for b in binary_decimals:
            y = x * b
            if y > MAXN:
                break
            reachable[y] = True

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        out.append("YES" if reachable[n] else "NO")

    return "\n".join(out)

# provided sample
assert run(
"""11
121
1
14641
12221
10110
100000
99
112
2024
12421
1001
"""
) == """YES
YES
YES
YES
YES
YES
NO
NO
NO
NO
YES"""

# minimum value
assert run(
"""1
1
"""
) == "YES"

# binary decimal itself
assert run(
"""1
10101
"""
) == "YES"

# non-representable small number
assert run(
"""1
2
"""
) == "NO"

# boundary value
assert run(
"""1
100000
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `YES` | Base case and starting state |
| `10101` | `YES` | A number that is already a binary decimal |
| `2` | `NO` | Small non-representable value |
| `100000` | `YES` | Upper boundary of the allowed range |

## Edge Cases

Consider the input:

```
1
1
```

The preprocessing starts with `reachable[1] = True`. Since `1` is already representable, the query immediately returns `YES`. This handles the smallest possible input correctly.

Consider:

```
1
100000
```

The number itself is a binary decimal because its digits are only `1` and `0`. During preprocessing, multiplying `1` by `100000` marks `reachable[100000] = True`. The answer is `YES`.

Consider:

```
1
121
```

The algorithm first marks `11` reachable from `1`, then marks `121 = 11 × 11`. The number is not a binary decimal, but it belongs to the closure of binary-decimal multiplication, so the output is `YES`.

Consider:

```
1
99
```

No sequence of binary-decimal multiplications produces `99`. Since it is never marked in the reachability table, the query returns `NO`. This avoids the common mistake of accepting numbers merely because they have one binary-decimal divisor.
