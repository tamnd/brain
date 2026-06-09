---
title: "CF 1798C - Candy Store"
description: "Each candy type has two numbers attached to it. There are $ai$ candies of that type in stock, and each candy costs $bi$ coins. For every type, we must choose a pack size $di$."
date: "2026-06-09T09:53:34+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1798
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 860 (Div. 2)"
rating: 1700
weight: 1798
solve_time_s: 272
verified: true
draft: false
---

[CF 1798C - Candy Store](https://codeforces.com/problemset/problem/1798/C)

**Rating:** 1700  
**Tags:** greedy, math, number theory  
**Solve time:** 4m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

Each candy type has two numbers attached to it. There are $a_i$ candies of that type in stock, and each candy costs $b_i$ coins.

For every type, we must choose a pack size $d_i$. The only restriction is that the entire stock must be partitioned into equal packs, so $d_i$ must divide $a_i$.

The price of one pack becomes

$$c_i = b_i \cdot d_i.$$

After choosing all pack sizes, we obtain a sequence of pack prices

$$c_1,c_2,\dots,c_n.$$

A single price tag can cover a contiguous block if every pack in that block has exactly the same price. The goal is to choose the pack sizes so that the number of required contiguous equal-price blocks is as small as possible.

The length of all test cases combined is at most $2 \cdot 10^5$. That immediately rules out any approach that tries to search over divisors or perform expensive pairwise checks inside every segment. We need something close to linear or $O(n \log C)$, where $C$ is the size of the numbers involved.

The subtle part is that we are not directly choosing the final pack prices. Each price must have the form $b_i \cdot d_i$, and $d_i$ must divide $a_i$.

A common mistake is to think only about pairwise compatibility. For example:

```
(a,b):
(6,2)
(10,3)
(15,5)
```

The first two types may share one valid pack price, and the last two may share another, but there may be no single price that works for all three simultaneously. The condition must be checked for the entire segment at once.

Another easy mistake is to work with the divisors $d_i$ directly. The actual constraint is about the common pack price $X$, not about making the $d_i$ equal.

For example:

```
a=6, b=2
a=10, b=3
```

The common price $X=6$ works because

$$d_1 = 6/2 = 3,\qquad d_2 = 6/3 = 2.$$

The pack sizes are different, but the pack prices match.

## Approaches

A brute-force view is to consider every possible segment and ask whether all candy types inside that segment can share a common pack price. If a segment is valid, it can be represented by one price tag.

The problem is that even checking one segment naively is expensive. Every candy type contributes divisibility constraints, and there are $O(n^2)$ segments. With $n$ up to $2 \cdot 10^5$, this is completely infeasible.

The key observation comes from rewriting the condition for a common pack price.

Suppose a segment uses a common price $X$.

Since

$$X = b_i \cdot d_i,$$

we know $X$ must be divisible by $b_i$.

Also,

$$d_i = \frac{X}{b_i}$$

must divide $a_i$. Multiplying both sides by $b_i$,

$$X \mid (a_i b_i).$$

So every candy type imposes two conditions:

$$b_i \mid X,$$

and

$$X \mid a_i b_i.$$

For an entire segment, $X$ must be:

1. A multiple of every $b_i$.
2. A divisor of every $a_i b_i$.

The smallest number satisfying the first requirement is

$$L = \operatorname{lcm}(b_i).$$

The largest number satisfying the second requirement is

$$G = \gcd(a_i b_i).$$

A valid $X$ exists exactly when some multiple of $L$ divides $G$. That happens precisely when

$$L \mid G.$$

This transforms the problem into maintaining, for a growing segment:

$$L = \operatorname{lcm}(b_i),$$

and

$$G = \gcd(a_i b_i).$$

A segment is valid if and only if

$$G \bmod L = 0.$$

Now the solution becomes greedy. Extend the current segment as long as the condition remains true. The moment it becomes false, no larger segment starting at the same position can ever become valid again, because adding more elements can only decrease the gcd and increase the lcm. We must start a new segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ or worse | $O(1)$ | Too slow |
| Optimal Greedy + GCD/LCM | $O(n \log C)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Start a new segment with the first candy type.
2. Maintain two values for the current segment:

$$G = \gcd(a_i b_i)$$

over the segment, and

$$L = \operatorname{lcm}(b_i)$$

over the segment.
3. When a new candy type arrives, compute:

$$G'=\gcd(G, a_i b_i),$$

$$L'=\operatorname{lcm}(L,b_i).$$
4. Check whether

$$G' \bmod L' = 0.$$

If this holds, the enlarged segment is still feasible, so replace $G,L$ by $G',L'$.
5. If the condition fails, no common pack price exists for the enlarged segment. Finish the current segment, increment the answer, and start a new segment containing only the current candy type.
6. Continue until all candy types are processed.
7. The number of segments formed by this greedy process is the minimum number of required price tags.

### Why it works

For a segment, a common pack price exists if and only if the segment's lcm of $b_i$ divides the segment's gcd of $a_i b_i$.

When we extend a segment, the gcd can only stay the same or decrease, while the lcm can only stay the same or increase. Once the divisibility condition fails, adding more elements cannot repair it. The left side can only become larger and the right side can only become smaller.

That monotonicity makes the greedy strategy optimal. Every segment is extended as far as possible. Any solution must start a new price tag at the first position where the condition becomes impossible, so the greedy partition uses the minimum possible number of segments.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def lcm(a, b):
    return a // gcd(a, b) * b

t = int(input())

for _ in range(t):
    n = int(input())

    ans = 1
    g = 0
    l = 1

    for _ in range(n):
        a, b = map(int, input().split())

        ng = gcd(g, a * b) if g else a * b
        nl = lcm(l, b)

        if ng % nl == 0:
            g = ng
            l = nl
        else:
            ans += 1
            g = a * b
            l = b

    print(ans)
```

The implementation mirrors the mathematical condition directly.

The variable `g` stores the gcd of all values $a_i b_i$ in the current segment. The variable `l` stores the lcm of all $b_i$ values in the current segment.

For each new candy type we tentatively extend the segment. If the divisibility condition still holds, we keep the extension. Otherwise we start a fresh segment beginning with the current candy type.

One implementation detail is that `g` is initialized as zero. Since

$$\gcd(0,x)=x,$$

this lets the first element initialize the segment naturally.

Another detail is the lcm computation:

```
a // gcd(a, b) * b
```

The division is performed before multiplication to avoid unnecessary growth of intermediate values.

## Worked Examples

### Example 1

Input segment:

```
(20,3)
(6,2)
(14,5)
(20,7)
```

| Step | a·b | Current G | Current L | Valid? |
| --- | --- | --- | --- | --- |
| Start | 60 | 60 | 3 | Yes |
| Add (6,2) | 12 | gcd(60,12)=12 | lcm(3,2)=6 | 12 % 6 = 0 |
| Add (14,5) | 70 | gcd(12,70)=2 | lcm(6,5)=30 | 2 % 30 ≠ 0 |
| New segment | 70 | 70 | 5 | Yes |
| Add (20,7) | 140 | gcd(70,140)=70 | lcm(5,7)=35 | 70 % 35 = 0 |

The array splits into two segments, so the answer is 2.

This example shows why the algorithm cuts exactly when the divisibility condition breaks.

### Example 2

Input segment:

```
(444,5)
(2002,10)
(2020,2)
```

| Step | a·b | Current G | Current L | Valid? |
| --- | --- | --- | --- | --- |
| Start | 2220 | 2220 | 5 | Yes |
| Add | 20020 | 20 | 10 | 20 % 10 = 0 |
| Add | 4040 | 20 | 10 | 20 % 10 = 0 |

The entire array remains one valid segment, so only one price tag is needed.

This example demonstrates that the common price does not need to be explicitly constructed. The gcd/lcm condition alone is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log C)$ | Each step performs a constant number of gcd operations |
| Space | $O(1)$ | Only a few integers are maintained |

Here $C$ is the magnitude of the stored numbers. Since the total number of candy types across all test cases is at most $2 \cdot 10^5$, this complexity easily fits within the limits.

## Test Cases

```python
import sys
import io
from math import gcd

def solve():
    input = sys.stdin.readline

    def lcm(a, b):
        return a // gcd(a, b) * b

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        ans = 1
        g = 0
        l = 1

        for _ in range(n):
            a, b = map(int, input().split())

            ng = gcd(g, a * b) if g else a * b
            nl = lcm(l, b)

            if ng % nl == 0:
                g = ng
                l = nl
            else:
                ans += 1
                g = a * b
                l = b

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out.strip()

# provided sample
assert run(
"""5
4
20 3
6 2
14 5
20 7
3
444 5
2002 10
2020 2
5
7 7
6 5
15 2
10 3
7 7
5
10 1
11 5
5 1
2 2
8 2
6
7 12
12 3
5 3
9 12
9 3
1000000000 10000
"""
) == """2
1
3
2
5"""

# minimum size
assert run(
"""1
2
1 1
1 1
"""
) == "1"

# every item forced into its own segment
assert run(
"""1
3
2 2
3 3
5 5
"""
) == "3"

# all can stay together
assert run(
"""1
3
10 2
15 2
20 2
"""
) == "1"

# boundary style case with large values
assert run(
"""1
2
1000000000 10000
1000000000 10000
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two identical types | 1 | Minimum-size valid segment |
| `(2,2),(3,3),(5,5)` | 3 | Every extension fails immediately |
| Three types with same `b` | 1 | Entire array forms one segment |
| Maximum-value style case | 1 | Large-number gcd/lcm handling |

## Edge Cases

Consider a segment consisting entirely of one candy type:

```
1
2
10 7
20 3
```

The first candy type always forms a valid segment by itself because choosing $d_1=1$ gives a valid pack price. The algorithm starts with `G=a_1b_1` and `L=b_1`, and clearly `G % L = 0`.

Now consider a case where the lcm grows too quickly:

```
1
3
2 2
3 3
5 5
```

After the first two types,

$$G=\gcd(4,9)=1,$$

$$L=\operatorname{lcm}(2,3)=6.$$

Since $1 \not\equiv 0 \pmod 6$, the segment must be split. Any larger segment would only decrease the gcd further and increase the lcm further, so the failure is permanent.

Finally, consider a case where the common price exists even though the pack sizes differ:

```
1
2
6 2
10 3
```

We have

$$G=\gcd(12,30)=6,$$

$$L=\operatorname{lcm}(2,3)=6.$$

Because $6 \bmod 6 = 0$, the segment is valid. A common pack price is $X=6$, giving pack sizes $3$ and $2$. This confirms that equality of pack sizes is irrelevant; only equality of pack prices matters.
