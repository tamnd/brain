---
title: "CF 105862B - Fair and Square"
description: "The problem asks us to take a rectangular grid with height n and width m, make several identical copies of it, and attach those copies without rotating them. The final combined shape must be a square. We need the smallest number of copies needed to achieve that."
date: "2026-06-25T14:33:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105862
codeforces_index: "B"
codeforces_contest_name: "ACPC Kickoff 2025"
rating: 0
weight: 105862
solve_time_s: 37
verified: true
draft: false
---

[CF 105862B - Fair and Square](https://codeforces.com/problemset/problem/105862/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to take a rectangular grid with height `n` and width `m`, make several identical copies of it, and attach those copies without rotating them. The final combined shape must be a square. We need the smallest number of copies needed to achieve that. The original problem is from Codeforces and has up to `10^5` test cases with dimensions as large as `10^9`.

The input describes many independent rectangles. For each rectangle, the output is the minimum count of these rectangles that can be tiled into a larger square while preserving each rectangle's orientation. The copies are arranged in a grid-like way, so if we place `a` copies vertically and `b` copies horizontally, the final dimensions become `(a * n) × (b * m)`. For this to be a square, those two values must be equal.

The large bounds immediately rule out simulation. The side lengths can be one billion, so trying possible square sizes or repeatedly adding rectangles would be impossible. With `10^5` test cases, we need an approach that does only a small constant amount of arithmetic per test case.

The main edge case is when the rectangle is already a square. For input `1 1`, the answer is `1`. A careless approach that searches for a larger arrangement might incorrectly return a larger number, but using one copy already satisfies the condition.

Another edge case is when one side divides the other. For input:

```
1
2 4
```

the correct output is:

```
2
```

Two copies of a `2 × 4` rectangle can be placed side by side to create a `2 × 8` rectangle, but that is not square. Instead, placing them one above another gives a `4 × 4` square. An approach that only checks horizontal placements would fail.

A more subtle case is when the dimensions are unrelated. For input:

```
1
2 3
```

the answer is:

```
6
```

The smallest square has side length `6`. We need three copies in one direction and two in the other, giving `6` rectangles. A solution that only computes the area ratio misses the actual tiling requirement.

## Approaches

A straightforward approach is to try possible numbers of copies. Suppose we place `x` copies vertically and `y` copies horizontally. The final rectangle has dimensions `x * n` and `y * m`, so we need to find the smallest `x * y` such that:

```
x * n = y * m
```

The brute force idea would try values of `x` and `y` until the equality holds. This is correct because every possible arrangement is represented by some pair `(x, y)`. However, with dimensions up to `10^9`, even iterating over a small fraction of possible values is too slow. Across many test cases the number of operations would explode.

The key observation is that we do not actually care about the arrangement itself, only the smallest square side length that both rectangle dimensions can divide. The final square side length must be a common multiple of `n` and `m`. The smallest possible side is their least common multiple.

If the final square has side length `L`, then the number of copies along the height is `L / n` and along the width is `L / m`. The total number of rectangles is:

```
(L / n) * (L / m)
```

For the smallest possible `L`, we choose:

```
L = lcm(n, m)
```

Using the relationship:

```
lcm(n, m) = n / gcd(n, m) * m
```

the number of copies becomes:

```
(n / gcd(n, m)) * (m / gcd(n, m))
```

which simplifies to:

```
n * m / gcd(n, m)^2
```

This gives the answer directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(minimum square side) | O(1) | Too slow |
| Optimal | O(log(min(n, m))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the rectangle dimensions `n` and `m`.

We only need these two values because every possible final arrangement depends on how many copies are placed in each direction.
2. Compute `g = gcd(n, m)`.

The greatest common divisor tells us how much the two dimensions already share. Removing this shared factor leaves the smallest incompatible parts that determine the number of copies needed.
3. Compute the number of copies on the two axes.

The number of copies vertically is `m / g`, and the number horizontally is `n / g`. Multiplying them gives the total number of rectangles.

The reason this works is that the smallest square side is the least common multiple. The two axes must scale until the dimensions meet at that value.
4. Output:

```
(n / g) * (m / g)
```

This is the minimum possible count.

Why it works: every valid construction creates a square whose side length is a common multiple of `n` and `m`. The smallest such length is the least common multiple, so any other square construction must use at least as many copies. The formula uses that smallest side length, meaning it achieves the minimum.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        g = gcd(n, m)
        ans.append(str((n // g) * (m // g)))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The code reads all test cases and processes each rectangle independently. The `gcd` function is enough because the entire problem reduces to finding the least common multiple relationship.

The expression is written as:

```
(n // g) * (m // g)
```

instead of:

```
n * m // (g * g)
```

because dividing first keeps intermediate values smaller. Python integers do not overflow, but this form also mirrors the mathematical reasoning more clearly.

The only possible mistake is using the greatest common divisor incorrectly. The shared part must be removed from both dimensions before multiplying, because that shared part represents progress both vertically and horizontally.

## Worked Examples

For the rectangle `2 × 3`:

| Step | n | m | gcd | copies |
| --- | --- | --- | --- | --- |
| Initial | 2 | 3 | 1 | 6 |
| Final | 2 | 3 | 1 | 2 × 3 |

The gcd is `1`, meaning there is no shared factor. The smallest square side is `6`, requiring three copies along one direction and two along the other, for a total of `6`.

For the rectangle `6 × 8`:

| Step | n | m | gcd | copies |
| --- | --- | --- | --- | --- |
| Initial | 6 | 8 | 2 | 6 |
| Final | 6 | 8 | 2 | 3 × 4 |

The common factor `2` reduces the problem to `3 × 4`. The smallest square side is `24`, so we need `4` rectangles in one direction and `3` in the other.

These traces show the invariant: after dividing both sides by the gcd, the remaining factors represent the exact scaling required to reach the first common square size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(min(n, m))) | Euclid's algorithm computes the gcd efficiently |
| Space | O(1) | Only a few integer variables are stored |

The solution performs one gcd computation per test case. Since the number of test cases can be large, a constant-time arithmetic solution per case is required, and this easily fits the limits.

## Test Cases

```python
import sys
import io
from math import gcd

def solution(data):
    input = io.StringIO(data).readline
    t = int(input())
    res = []
    for _ in range(t):
        n, m = map(int, input().split())
        g = gcd(n, m)
        res.append(str((n // g) * (m // g)))
    return "\n".join(res)

def run(inp: str) -> str:
    return solution(inp)

assert run("""2
2 3
1 1
""") == """6
1""", "samples"

assert run("""1
2 4
""") == "2", "dividing side"

assert run("""1
999999999 1000000000
""") == "999999999000000000", "large values"

assert run("""3
5 5
10 20
7 11
""") == """1
2
77""", "basic cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3` | `6` | Coprime dimensions |
| `2 4` | `2` | One dimension divides the other |
| `999999999 1000000000` | `999999999000000000` | Very large bounds |
| Equal sides such as `5 5` | `1` | Already a square |

## Edge Cases

For the already-square case:

```
1
5 5
```

the gcd is `5`. The formula becomes:

```
(5 / 5) * (5 / 5) = 1
```

Only one rectangle is needed, which is correct.

For a divisible side:

```
1
3 12
```

the gcd is `3`. The answer is:

```
(3 / 3) * (12 / 3) = 4
```

The final square side is `12`, formed by placing four `3 × 12` rectangles stacked vertically.

For coprime sides:

```
1
4 7
```

the gcd is `1`, so the answer is:

```
4 * 7 = 28
```

The square side must be `28`, requiring seven copies along one axis and four along the other. Since no smaller common multiple exists, no smaller arrangement can work.
