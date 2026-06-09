---
title: "CF 1907E - Good Triples"
description: "We need to count ordered triples of non-negative integers $(a,b,c)$ whose sum is exactly $n$. The unusual part is the digit-sum condition: $$text{digsum}(a)+text{digsum}(b)+text{digsum}(c)=text{digsum}(n).$$ A triple is counted only if both conditions hold."
date: "2026-06-08T20:38:52+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1907
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 913 (Div. 3)"
rating: 1600
weight: 1907
solve_time_s: 115
verified: true
draft: false
---

[CF 1907E - Good Triples](https://codeforces.com/problemset/problem/1907/E)

**Rating:** 1600  
**Tags:** brute force, combinatorics, number theory  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to count ordered triples of non-negative integers $(a,b,c)$ whose sum is exactly $n$. The unusual part is the digit-sum condition:

$$\text{digsum}(a)+\text{digsum}(b)+\text{digsum}(c)=\text{digsum}(n).$$

A triple is counted only if both conditions hold. Since order matters, $(1,2,3)$ and $(3,2,1)$ are different triples.

The value of $n$ can be as large as $10^7$, and there can be $10^4$ test cases. Any algorithm that iterates over possible values of $a$, $b$, and $c$ is immediately impossible. Even iterating over all pairs $(a,b)$ would require around $10^{14}$ operations in the worst case.

The key constraint is not the size of $n$, but the fact that $n$ has at most 8 decimal digits. This strongly suggests that the answer depends on the decimal representation digit by digit rather than on the numeric value itself.

There are a few edge cases that can easily mislead a naive solution.

For $n=0$, the only valid triple is $(0,0,0)$. The answer is $1$. A formula that assumes every digit contributes multiple possibilities would incorrectly return a larger value.

For $n=10$, the valid triples are not all solutions of $a+b+c=10$. For example, $(5,5,0)$ has digit sums $5+5+0=10$, while $\text{digsum}(10)=1$, so it is invalid. Carry operations matter.

For $n=10000000$, most digits are zero. A careless digit DP might accidentally allow carries between positions and count many extra configurations. The correct answer is only $3$, corresponding to placing the entire value in exactly one of the three numbers.

## Approaches

A brute-force solution would enumerate all triples $(a,b,c)$ with $a+b+c=n$, then check the digit-sum condition. Since $c$ is determined by $a$ and $b$, this requires roughly

$$\sum_{a=0}^{n}(n-a+1)=O(n^2)$$

states.

For $n=10^7$, that is around $10^{14}$ iterations, completely infeasible.

The crucial observation comes from a standard property of decimal addition. Whenever a carry occurs, the sum of digit sums decreases by a multiple of $9$.

For any non-negative integers,

$$\text{digsum}(x)+\text{digsum}(y)-\text{digsum}(x+y)$$

equals $9$ times the number of carries produced during the addition.

Applying this repeatedly,

$$\text{digsum}(a)+\text{digsum}(b)+\text{digsum}(c)-\text{digsum}(n)$$

is $9$ times the total number of carries occurring while adding the three numbers.

Our condition requires this difference to be exactly zero. Since carries can only make the left side larger, the only possibility is that **no carry occurs anywhere**.

That completely changes the problem. Instead of thinking about numbers, we think about digits.

Suppose a digit of $n$ is $d$. Since no carry is allowed, the corresponding digits $x,y,z$ of $a,b,c$ must satisfy

$$x+y+z=d.$$

Different digit positions become independent. The number of valid triples is simply the product of the number of digit triples for each digit of $n$.

For a fixed digit $d$, we need the number of non-negative solutions of

$$x+y+z=d.$$

Since $d\le 9$, the digit bounds $x,y,z\le 9$ are automatically satisfied.

By stars and bars,

$$\#(x+y+z=d)=\binom{d+2}{2}.$$

Each digit contributes independently, so the final answer is

$$\prod_{\text{digits } d \text{ of } n} \binom{d+2}{2}.$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(\text{digits}(n))$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Precompute the values

$$f[d]=\binom{d+2}{2}$$

for digits $d=0$ through $9$.
2. For each test case, convert $n$ to its decimal representation.
3. Initialize the answer as $1$.
4. Process every digit $d$ of $n$.
5. Multiply the answer by $f[d]$.

This counts all digit triples $(x,y,z)$ whose sum equals $d$ at that position.
6. After all digits are processed, output the product.

### Why it works

The digit-sum condition is equivalent to saying that no carry occurs during the addition $a+b+c=n$. If even one carry appears, the quantity

$$\text{digsum}(a)+\text{digsum}(b)+\text{digsum}(c)$$

becomes strictly larger than $\text{digsum}(n)$ by a multiple of $9$.

When there are no carries, each decimal position is independent. At a digit position where $n$ contains digit $d$, the digits chosen for $a$, $b$, and $c$ only need to satisfy $x+y+z=d$. The number of such triples is $\binom{d+2}{2}$. Since choices at different positions do not interact, the multiplication principle gives the product over all digits. Thus every valid triple is counted exactly once, and every counted configuration produces a valid triple.

## Python Solution

```python
import sys
input = sys.stdin.readline

# f[d] = C(d + 2, 2)
ways = [(d + 2) * (d + 1) // 2 for d in range(10)]

t = int(input())

for _ in range(t):
    n = input().strip()

    ans = 1
    for ch in n:
        ans *= ways[ord(ch) - ord('0')]

    print(ans)
```

The array `ways` stores the number of non-negative solutions of $x+y+z=d$ for every digit $d$. Since $d\le 9$, the stars-and-bars formula directly applies.

For each test case we read the number as a string. This avoids repeatedly extracting digits with division and naturally handles values up to $10^7$.

The answer starts at $1$. Each digit contributes an independent multiplicative factor, so we multiply by `ways[d]` for every digit.

Python integers automatically expand to arbitrary size, which is useful because answers such as the one for $9999999$ exceed 32-bit and 64-bit limits.

## Worked Examples

### Example 1: $n=11$

Digits are $1$ and $1$.

For digit $1$,

$$\binom{1+2}{2}=3.$$

| Digit | Contribution | Running Answer |
| --- | --- | --- |
| 1 | 3 | 3 |
| 1 | 3 | 9 |

Final answer: $9$.

These correspond exactly to choosing, independently at each digit position, one of the three possibilities:

$$(1,0,0),\ (0,1,0),\ (0,0,1).$$

### Example 2: $n=3141$

| Digit | Contribution $\binom{d+2}{2}$ | Running Answer |
| --- | --- | --- |
| 3 | 10 | 10 |
| 1 | 3 | 30 |
| 4 | 15 | 450 |
| 1 | 3 | 1350 |

Final answer: $1350$.

This example demonstrates the independence of digit positions. The total count is simply the product of the counts for each digit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\text{digits}(n))$ | One multiplication per decimal digit |
| Space | $O(1)$ | Only a small fixed-size lookup table |

Since $n \le 10^7$, each test case contains at most 8 digits. Even with $10^4$ test cases, the total work is only around $8 \times 10^4$ digit operations, comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    ways = [(d + 2) * (d + 1) // 2 for d in range(10)]

    t = int(input())
    out = []

    for _ in range(t):
        n = input().strip()
        ans = 1
        for ch in n:
            ans *= ways[int(ch)]
        out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run(
"""12
11
0
1
2
3
4
5
3141
999
2718
9999999
10000000
"""
) == (
"""9
1
3
6
10
15
21
1350
166375
29160
1522435234375
3"""
), "sample"

# minimum value
assert run(
"""1
0
"""
) == "1", "only (0,0,0)"

# single digit maximum
assert run(
"""1
9
"""
) == "55", "C(11,2)"

# power of ten
assert run(
"""1
1000
"""
) == "3", "only one nonzero digit"

# all digits equal to 9
assert run(
"""1
999
"""
) == "166375", "55^3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1` | Smallest possible value |
| `9` | `55` | Largest single-digit contribution |
| `1000` | `3` | Many zero digits, carry handling |
| `999` | `166375` | Large multiplicative answer |

## Edge Cases

Consider the input:

```
1
0
```

The algorithm processes the single digit $0$. Its contribution is

$$\binom{2}{2}=1.$$

The final answer is $1$, corresponding to the unique triple $(0,0,0)$.

Consider the input:

```
1
10
```

The digits are $1$ and $0$. Their contributions are $3$ and $1$.

$$3 \times 1 = 3.$$

The valid triples are exactly $(10,0,0)$, $(0,10,0)$, and $(0,0,10)$. Any triple such as $(5,5,0)$ creates a carry in the units place and violates the digit-sum condition. The algorithm excludes it automatically because it only counts no-carry digit assignments.

Consider the input:

```
1
10000000
```

The digit contributions are

$$3 \times 1 \times 1 \times 1 \times 1 \times 1 \times 1 \times 1 = 3.$$

Only one number may contain the leading $1$, while the other two must be zero. The algorithm correctly returns $3$.

Consider the input:

```
1
9999999
```

Every digit contributes

$$\binom{11}{2}=55.$$

The answer becomes

$$55^7=1522435234375.$$

This checks that the implementation handles very large answers correctly and relies on Python's arbitrary-precision integers rather than fixed-width arithmetic.
