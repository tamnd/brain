---
title: "CF 1717A - Madoka and Strange Thoughts"
description: "For each test case we are given a number n. We consider every ordered pair (a, b) such that both numbers lie between 1 and n. Among those pairs, we want to count how many satisfy $$frac{operatorname{lcm}(a,b)}{gcd(a,b)} le 3."
date: "2026-06-09T19:46:29+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1717
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 818 (Div. 2)"
rating: 800
weight: 1717
solve_time_s: 57
verified: true
draft: false
---

[CF 1717A - Madoka and Strange Thoughts](https://codeforces.com/problemset/problem/1717/A)

**Rating:** 800  
**Tags:** math, number theory  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case we are given a number `n`. We consider every ordered pair `(a, b)` such that both numbers lie between `1` and `n`. Among those pairs, we want to count how many satisfy

$$\frac{\operatorname{lcm}(a,b)}{\gcd(a,b)} \le 3.$$

The answer is the number of ordered pairs with this property.

The limits are very revealing. There can be up to `10^4` test cases, and each `n` can be as large as `10^8`. Any approach that iterates over all pairs immediately becomes impossible, since one test case alone would contain `10^16` pairs. Even an `O(n)` solution per test case would perform about `10^{12}` operations in the worst case across all tests, which is too much. The target complexity is constant time per test case.

There are a few edge cases that deserve attention.

For `n = 1`, the only pair is `(1,1)`, so the answer is `1`. A formula that accidentally assumes the existence of numbers greater than `1` would fail here.

For example:

```
1
1
```

The correct output is

```
1
```

For `n = 2`, every ordered pair works:

```
(1,1), (1,2), (2,1), (2,2)
```

so the answer is `4`. A careless derivation that forgets ordered pairs and counts only unordered pairs would produce `3`.

For example:

```
1
2
```

The correct output is

```
4
```

Another common mistake is to assume that only equal numbers are valid. For `n = 3`, pairs `(1,3)` and `(3,1)` also satisfy the condition because

$$\frac{\operatorname{lcm}(1,3)}{\gcd(1,3)}=3.$$

The correct answer is `7`.

Input:

```
1
3
```

Output:

```

```

## Approaches

The most direct solution examines every ordered pair `(a,b)`, computes `gcd(a,b)` and `lcm(a,b)`, and checks whether their ratio is at most `3`. Since there are `n²` pairs, this requires up to `10^16` checks when `n = 10^8`, which is hopeless.

The brute force works because it literally follows the definition, but it ignores the arithmetic structure hidden inside the ratio.

Suppose

$$g=\gcd(a,b).$$

We may write

$$a=gx,\qquad b=gy,$$

where `gcd(x,y)=1`.

Since

$$\operatorname{lcm}(a,b)=gxy,$$

the ratio becomes

$$\frac{\operatorname{lcm}(a,b)}{\gcd(a,b)}
=xy.$$

Now the problem becomes much simpler. We need coprime positive integers `x` and `y` whose product is at most `3`.

The possibilities are extremely limited.

When `xy=1`, we have

```
(x,y)=(1,1)
```

When `xy=2`, the coprime pairs are

```
(1,2), (2,1)
```

When `xy=3`, the coprime pairs are

```
(1,3), (3,1)
```

No larger product is allowed.

Multiplying these pairs by `g` gives:

```
(g,g)
(g,2g)
(2g,g)
(g,3g)
(3g,g)
```

The value of `g` must keep both numbers at most `n`.

Equal pairs contribute `n`.

Pairs `(g,2g)` and `(2g,g)` exist for every `g ≤ n/2`, contributing `2⌊n/2⌋`.

Pairs `(g,3g)` and `(3g,g)` exist for every `g ≤ n/3`, contributing `2⌊n/3⌋`.

Hence

$$\boxed{n+2\left\lfloor\frac n2\right\rfloor+2\left\lfloor\frac n3\right\rfloor}$$

which is constant time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the value of `n`.
2. Count all pairs with equal numbers. There are exactly `n` such pairs because `(g,g)` is valid for every `1 ≤ g ≤ n`.
3. Count pairs of the form `(g,2g)` and `(2g,g)`. The value `g` can range from `1` to `⌊n/2⌋`, so these contribute `2⌊n/2⌋`.
4. Count pairs of the form `(g,3g)` and `(3g,g)`. Here `g` ranges from `1` to `⌊n/3⌋`, contributing `2⌊n/3⌋`.
5. Add the three contributions and print the result.

### Why it works

After dividing both numbers by their gcd, the remaining numbers are coprime. The ratio `lcm/gcd` becomes the product of those coprime numbers. Since that product must not exceed `3`, only the normalized pairs `(1,1)`, `(1,2)`, `(2,1)`, `(1,3)`, and `(3,1)` are possible. Every valid pair is obtained uniquely by multiplying one of these normalized pairs by some positive integer `g`. The counting formula covers all such choices exactly once, so the algorithm cannot miss a pair or count one twice.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    ans = n + 2 * (n // 2) + 2 * (n // 3)
    print(ans)
```

The program processes each test case independently. Integer division is used because only complete multiples fit inside the range `[1, n]`.

The term `n` counts equal pairs. The term `2 * (n // 2)` counts both `(g,2g)` and `(2g,g)`, while `2 * (n // 3)` counts `(g,3g)` and `(3g,g)`.

Using integer arithmetic avoids precision issues. Python integers automatically handle the largest possible answer, which is `266666666` when `n = 10^8`.

The order of operations is straightforward because the three categories are disjoint. No pair belongs to more than one category.

## Worked Examples

### Example 1: n = 3

| Step | Value |
| --- | --- |
| Equal pairs | 3 |
| Pairs with ratio 2 | 2 |
| Pairs with ratio 3 | 2 |
| Total | 7 |

The valid pairs are

```
(1,1)
(2,2)
(3,3)
(1,2)
(2,1)
(1,3)
(3,1)
```

This example shows that unequal numbers can also satisfy the condition.

### Example 2: n = 5

| Step | Value |
| --- | --- |
| Equal pairs | 5 |
| Pairs with ratio 2 | 4 |
| Pairs w |  |
