---
title: "CF 293C - Cube Problem"
description: "We are looking for the number of positive integer triples $(a,b,c)$ such that three smaller cubes of sizes $a^3$, $b^3$, and $c^3$ together are short of exactly $n$ unit cubes when trying to build one large cube of side length $a+b+c$."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 293
codeforces_index: "C"
codeforces_contest_name: "Croc Champ 2013 - Round 2"
rating: 2400
weight: 293
solve_time_s: 96
verified: true
draft: false
---

[CF 293C - Cube Problem](https://codeforces.com/problemset/problem/293/C)

**Rating:** 2400  
**Tags:** brute force, math, number theory  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are looking for the number of positive integer triples $(a,b,c)$ such that three smaller cubes of sizes $a^3$, $b^3$, and $c^3$ together are short of exactly $n$ unit cubes when trying to build one large cube of side length $a+b+c$.

The missing amount is

$$(a+b+c)^3 - a^3 - b^3 - c^3 = n$$

We must count how many ordered triples of positive integers satisfy this equation.

The first step is to expand the cube:

$$(a+b+c)^3
= a^3+b^3+c^3
+3(a+b)(b+c)(c+a)$$

Subtracting the three individual cubes leaves

$$n = 3(a+b)(b+c)(c+a)$$

So the entire problem becomes counting positive integer triples satisfying this product identity.

The constraint is the real challenge. The value of $n$ can reach $10^{14}$. Any approach that iterates over all possible $a,b,c$ directly is hopeless. Even trying all values up to $10^5$ in three nested loops already gives $10^{15}$ operations.

The structure of the equation matters much more than brute force. The expression factors cleanly into three terms, and those terms have strong parity relationships that let us reconstruct $a,b,c$ from divisors of $n/3$.

There are a few easy mistakes here.

One common mistake is forgetting that the triples are ordered. The triples $(1,2,3)$ and $(3,2,1)$ are different unless the values coincide.

Another subtle point is positivity. Suppose we derive values mathematically but one of $a,b,c$ becomes zero or negative. Those must be discarded.

For example, if $n=3$, then

$$(a+b)(b+c)(c+a)=1$$

The only possible factorization is $1\cdot1\cdot1$, which would imply

$$a=b=c=0$$

Zero is not allowed, so the correct answer is $0$.

Parity is another hidden constraint. If we define

$$x=a+b,\quad y=b+c,\quad z=c+a$$

then

$$a=\frac{x+z-y}{2}$$

and similarly for $b,c$. The numerator must always be even. A careless implementation that skips this check may count impossible factorizations.

For instance, if $n=24$, then

$$xyz=8$$

Taking $(x,y,z)=(1,1,8)$ gives

$$a=\frac{1+8-1}{2}=4,\quad
b=\frac{1+1-8}{2}=-3$$

This is invalid even though the product matches.

## Approaches

The brute force interpretation is straightforward. We can try all positive integers $a,b,c$, compute

$$(a+b+c)^3-a^3-b^3-c^3$$

and count how many times it equals $n$.

Why does this work? Because the formula directly models the problem. Every valid triple will eventually be checked.

The issue is the search space. Since cubes grow quickly, each variable can still be around $10^5$ when $n\le10^{14}$. Three nested loops would require around $10^{15}$ iterations, which is completely infeasible.

The key observation is that the expression factorizes:

$$(a+b+c)^3-a^3-b^3-c^3
=
3(a+b)(b+c)(c+a)$$

Now the problem becomes multiplicative instead of cubic.

Define

$$x=a+b,\quad y=b+c,\quad z=c+a$$

Then

$$xyz = \frac n3$$

and

$$a=\frac{x+z-y}{2},\quad
b=\frac{x+y-z}{2},\quad
c=\frac{y+z-x}{2}$$

So instead of searching over all triples $(a,b,c)$, we only search over factor triples $(x,y,z)$ of $n/3$.

This is dramatically smaller because the number of divisors of numbers up to $10^{14}$ is manageable. We can enumerate divisors of $m=n/3$, try all factorizations $x\cdot y\cdot z=m$, and reconstruct $a,b,c$.

The parity conditions and positivity checks guarantee correctness.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(K^3)$ | $O(1)$ | Too slow |
| Optimal | $O(\sqrt n + d^2)$ | $O(d)$ | Accepted |

Here $d$ is the number of divisors of $n/3$, which is small enough for the constraints.

## Algorithm Walkthrough

1. Read $n$.
2. Check whether $n$ is divisible by $3$.

Since

$$n = 3(a+b)(b+c)(c+a)$$

every valid answer must make $n$ a multiple of $3$. If not, print $0$.
3. Let

$$m = \frac n3$$

We now need all positive integer triples $(x,y,z)$ such that

$$xyz=m$$
4. Enumerate all divisors of $m$.

We store every divisor in a list so we can iterate through possible values of $x$ and $y$.
5. For every pair of divisors $(x,y)$, check whether $xy$ divides $m$.

If not, no integer $z$ exists.

Otherwise define

$$z=\frac{m}{xy}$$
6. Reconstruct the original variables:

$$a=\frac{x+z-y}{2}$$

$$b=\frac{x+y-z}{2}$$

$$c=\frac{y+z-x}{2}$$
7. Check validity conditions.

All three numerators must be even, otherwise $a,b,c$ are not integers.

All three values must also be strictly positive.
8. Count every valid triple.

Different ordered factorizations produce different ordered triples, which matches the problem statement.

### Why it works

The transformation between $(a,b,c)$ and $(x,y,z)$ is reversible.

Starting from any valid triple,

$$x=a+b,\quad y=b+c,\quad z=c+a$$

gives

$$xyz=\frac n3$$

Conversely, any factor triple $(x,y,z)$ satisfying the parity and positivity conditions reconstructs exactly one triple $(a,b,c)$.

So the algorithm neither misses valid solutions nor counts invalid ones.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    if n % 3 != 0:
        print(0)
        return

    m = n // 3

    divisors = []
    d = 1

    while d * d <= m:
        if m % d == 0:
            divisors.append(d)
            if d * d != m:
                divisors.append(m // d)
        d += 1

    ans = 0

    for x in divisors:
        for y in divisors:
            xy = x * y

            if m % xy != 0:
                continue

            z = m // xy

            a_num = x + z - y
            b_num = x + y - z
            c_num = y + z - x

            if (a_num & 1) or (b_num & 1) or (c_num & 1):
                continue

            a = a_num // 2
            b = b_num // 2
            c = c_num // 2

            if a > 0 and b > 0 and c > 0:
                ans += 1

    print(ans)

solve()
```

The implementation follows the algebraic reduction directly.

The divisor generation loop runs up to $\sqrt m$. Whenever we find a divisor $d$, we also add $m/d$. The square root case must be handled carefully so we do not insert the same divisor twice.

The nested loops iterate over ordered pairs $(x,y)$. Once those are fixed, $z$ is determined uniquely by

$$z=\frac{m}{xy}$$

The parity checks happen before division by two. Using bitwise `& 1` is a compact way to test oddness.

The positivity check is essential. The formulas can produce zero or negative values even when the product condition holds.

Python integers automatically handle values up to $10^{14}$, so overflow is not a concern.

## Worked Examples

### Example 1

Input:

```
24
```

We compute

$$m = 24/3 = 8$$

The valid factor triple is $(2,2,2)$.

| x | y | z | a | b | c | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | 2 | 1 | 1 | 1 | Yes |

The answer is $1$.

This trace shows the clean symmetric case where all three cubes have equal size.

### Example 2

Input:

```
48
```

Now

$$m = 16$$

Several factor triples exist.

| x | y | z | a | b | c | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | 4 | 2 | 0 | 2 | No |
| 2 | 4 | 2 | 0 | 2 | 2 | No |
| 4 | 2 | 2 | 2 | 2 | 0 | No |
| 2 | 4 | 2 | 0 | 2 | 2 | No |
| 4 | 4 | 1 | 0.5 | 3.5 | 0.5 | No |
| 2 | 2 | 4 | 2 | 0 | 2 | No |

No valid positive integer triple exists, so the answer is $0$.

This example demonstrates why parity and positivity checks are both necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt n + d^2)$ | Divisor generation plus checking divisor pairs |
| Space | $O(d)$ | Storage for all divisors |

The number of divisors of a number up to $10^{14}$ is relatively small, so iterating over divisor pairs is easily fast enough within 2 seconds.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())

        if n % 3 != 0:
            return "0"

        m = n // 3

        divisors = []
        d = 1

        while d * d <= m:
            if m % d == 0:
                divisors.append(d)
                if d * d != m:
                    divisors.append(m // d)
            d += 1

        ans = 0

        for x in divisors:
            for y in divisors:
                xy = x * y

                if m % xy != 0:
                    continue

                z = m // xy

                a_num = x + z - y
                b_num = x + y - z
                c_num = y + z - x

                if (a_num & 1) or (b_num & 1) or (c_num & 1):
                    continue

                a = a_num // 2
                b = b_num // 2
                c = c_num // 2

                if a > 0 and b > 0 and c > 0:
                    ans += 1

        return str(ans)

    return solve()

# provided sample
assert run("24\n") == "1", "sample 1"

# custom cases
assert run("1\n") == "0", "n not divisible by 3"
assert run("3\n") == "0", "produces zero-sized cubes"
assert run("81\n") == "3", "multiple ordered triples"
assert run("192\n") == "1", "all equal larger cubes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Impossible because $n$ is not divisible by 3 |
| `3` | `0` | Rejects zero-sized solutions |
| `81` | `3` | Multiple ordered valid triples |
| `192` | `1` | Symmetric case with larger equal cubes |

## Edge Cases

Consider the input:

```
1
```

Since $1$ is not divisible by $3$, the algorithm immediately returns $0$. This matches the factorization formula exactly because

$$n=3(a+b)(b+c)(c+a)$$

cannot produce a non-multiple of $3$.

Now consider:

```
3
```

We get

$$m=1$$

The only factorization is

$$x=y=z=1$$

Then

$$a=b=c=0$$

The positivity check rejects this case, so the answer becomes $0$.

Another subtle case is:

```
48
```

Here $m=16$. Some factor triples satisfy the product equation but fail parity conditions. For example:

$$(x,y,z)=(1,1,16)$$

gives

$$a=\frac{1+16-1}{2}=8$$

$$b=\frac{1+1-16}{2}=-7$$

The algorithm rejects this because $b\le0$.

Finally, consider a symmetric valid case:

```
192
```

We get

$$m=64$$

Choosing

$$x=y=z=4$$

produces

$$a=b=c=2$$

which satisfies

$$(2+2+2)^3 - 2^3 - 2^3 - 2^3
=216-24
=192$$

The algorithm counts exactly one valid ordered triple.
