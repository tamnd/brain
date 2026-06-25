---
title: "CF 106098E - Farouk and Triangles"
description: "We are given a collection of equilateral triangles. The side lengths are distinct even integers, and each triangle keeps its original index. For every query, three numbers $d1,d2,d3$ are given."
date: "2026-06-25T11:55:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106098
codeforces_index: "E"
codeforces_contest_name: "The American University in Cairo CSEA Fall 2025 contest"
rating: 0
weight: 106098
solve_time_s: 72
verified: true
draft: false
---

[CF 106098E - Farouk and Triangles](https://codeforces.com/problemset/problem/106098/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of equilateral triangles. The side lengths are distinct even integers, and each triangle keeps its original index.

For every query, three numbers $d_1,d_2,d_3$ are given. These are the squares of the perpendicular distances from some interior point $P$ to the three sides of an equilateral triangle. We must determine whether one of the given triangles can contain such a point. If it can, we output the index of any matching triangle. Otherwise we output `-1`.

The input size is large. Both the number of triangles and the number of queries can reach $2 \cdot 10^5$. Any solution that scans all triangles for every query would require about $4 \cdot 10^{10}$ operations in the worst case, which is completely infeasible. Each query must be answered in roughly constant or logarithmic time.

The tricky part is that the query provides squared distances, not the distances themselves. Recovering the actual distances requires understanding when sums of square roots can equal the altitude of an equilateral triangle.

A common mistake is to compute floating point square roots and compare them. Consider:

```
n = 1
l = [14]

query:
48 3 12
```

The distances are $4\sqrt3$, $\sqrt3$, and $2\sqrt3$. Their sum is $7\sqrt3$, which is exactly the altitude of a triangle with side length $14$. Floating point arithmetic can introduce rounding errors and incorrectly reject the query.

Another subtle case is:

```
n = 1
l = [12]

query:
3 12 1
```

The distances are $\sqrt3$, $2\sqrt3$, and $1$. Their sum contains both $\sqrt3$ and a rational component. No integer multiple of $\sqrt3$ can equal that sum, so the answer is `-1`. A solution that only checks approximate numeric equality may fail here.

A final edge case is when a distance is not of the form $3a^2$:

```
n = 1
l = [6]

query:
6 6 6
```

Each distance is $\sqrt6$. The sum is $3\sqrt6$, which cannot be the altitude of any triangle in this problem. The correct answer is `-1`.

## Approaches

The most direct approach is to process each query, compute the required triangle side length, then scan all available triangles looking for a match.

The geometry itself is simple. In an equilateral triangle, the sum of the perpendicular distances from any interior point to the three sides equals the altitude. This is Viviani's theorem. If the distances are $x_1,x_2,x_3$, then

$$x_1+x_2+x_3 = h.$$

Since the side length is $l$,

$$h=\frac{\sqrt3}{2}l.$$

The brute force idea would compute

$$\sqrt{d_1}+\sqrt{d_2}+\sqrt{d_3}$$

and check whether it equals the altitude of any triangle. Even if that computation were done exactly, scanning all $n$ triangles per query costs $O(nq)$, which is far too large.

The key observation comes from the fact that every triangle side length is even.

Let $l=2k$. Then the altitude becomes

$$h=k\sqrt3.$$

So we need

$$\sqrt{d_1}+\sqrt{d_2}+\sqrt{d_3}=k\sqrt3.$$

Write every $d_i$ as

$$d_i=s_i^2 \cdot m_i,$$

where $m_i$ is square-free. Then

$$\sqrt{d_i}=s_i\sqrt{m_i}.$$

Square-root terms with different square-free parts are linearly independent over the rationals. Since every distance is positive, no cancellation is possible. The only way their sum can equal a pure multiple of $\sqrt3$ is if every term already has square-free part $3$.

That means every $d_i$ must be exactly

$$d_i=3a_i^2.$$

Then

$$\sqrt{d_i}=a_i\sqrt3,$$

and

$$\sqrt{d_1}+\sqrt{d_2}+\sqrt{d_3}
=
(a_1+a_2+a_3)\sqrt3.$$

Thus

$$k=a_1+a_2+a_3,
\qquad
l=2k.$$

The entire query reduces to:

1. Check whether each $d_i/3$ is a perfect square.
2. Sum the square roots.
3. Look up side length $2k$ in a hash table.

This gives constant-time query processing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(1)$ | Too slow |
| Optimal | $O(n+q)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all triangle side lengths and store a mapping from side length to its original index.
2. For each query, process the three values independently.
3. For a value $d$, first check whether it is divisible by $3$. If not, the query is impossible.
4. Compute $x=d/3$. Let $r=\lfloor\sqrt{x}\rfloor$.
5. Verify that $r^2=x$. If not, then $d$ is not of the form $3a^2$, so the query is impossible.
6. Accumulate $r$. This value is exactly $a_i$.
7. After processing the three numbers, let

$$k=a_1+a_2+a_3.$$

The required side length is

$$l=2k.$$

1. Check whether $l$ exists in the hash table of available triangles.
2. Output the stored index if it exists, otherwise output `-1`.

### Why it works

For an equilateral triangle, the sum of perpendicular distances from any interior point to the three sides equals the altitude. The altitude of a triangle with even side length $l=2k$ is $k\sqrt3$.

The query can only be valid if

$$\sqrt{d_1}+\sqrt{d_2}+\sqrt{d_3}$$

is exactly a multiple of $\sqrt3$. Since all distances are positive, every square-root term must itself be an integer multiple of $\sqrt3$. Hence each $d_i$ must be $3a_i^2$.

When that condition holds, the altitude becomes

$$(a_1+a_2+a_3)\sqrt3,$$

which corresponds to side length

$$2(a_1+a_2+a_3).$$

The algorithm computes exactly this side length and checks whether it exists among the given triangles. No valid triangle is missed, and every reported triangle satisfies the required distance sum.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

n, q = map(int, input().split())
lengths = list(map(int, input().split()))

pos = {}
for i, l in enumerate(lengths, start=1):
    pos[l] = i

ans = []

for _ in range(q):
    d1, d2, d3 = map(int, input().split())

    total = 0
    ok = True

    for d in (d1, d2, d3):
        if d % 3 != 0:
            ok = False
            break

        x = d // 3
        r = isqrt(x)

        if r * r != x:
            ok = False
            break

        total += r

    if not ok:
        ans.append("-1")
        continue

    need = 2 * total
    ans.append(str(pos.get(need, -1)))

sys.stdout.write("\n".join(ans))
```

The first part builds a hash table from side length to index. Since all side lengths are distinct, a simple dictionary is sufficient.

For each query, the code checks whether every squared distance is of the form $3a^2$. Integer square roots are computed with `isqrt`, which avoids all floating point precision issues.

The variable `total` stores

$$a_1+a_2+a_3.$$

The required side length is `2 * total`. Looking it up in the dictionary gives an $O(1)$ answer.

The most common implementation error is using floating point square roots. Values can be as large as $10^{18}$, and exact equality comparisons become unreliable. `isqrt` performs the entire computation with integers.

Another easy mistake is forgetting that the side length is $2k$, not $k$. The altitude of an equilateral triangle is $\frac{\sqrt3}{2}l$, and solving for $l$ introduces this factor of two.

## Worked Examples

### Sample 1

Input:

```
3 3
14 6 12
3 3 3
48 3 12
24 6 6
```

Triangle mapping:

| Side Length | Index |
| --- | --- |
| 14 | 1 |
| 6 | 2 |
| 12 | 3 |

First query:

| d | d/3 | sqrt(d/3) |
| --- | --- | --- |
| 3 | 1 | 1 |
| 3 | 1 | 1 |
| 3 | 1 | 1 |

`total = 3`

`need = 2 * 3 = 6`

Triangle 6 exists at index 2.

Output:

```
2
```

Second query:

| d | d/3 | sqrt(d/3) |
| --- | --- | --- |
| 48 | 16 | 4 |
| 3 | 1 | 1 |
| 12 | 4 | 2 |

`total = 7`

`need = 14`

Triangle 14 exists at index 1.

Output:

```
1
```

The example shows how the geometry collapses into a simple sum of integer square roots.

### Custom Example

Input:

```
1 1
10
3 12 1
```

| d | Divisible by 3? | Result |
| --- | --- | --- |
| 3 | Yes | continue |
| 12 | Yes | continue |
| 1 | No | fail |

The query is rejected immediately.

Output:

```
-1
```

This demonstrates that a single distance not matching the required structure makes the entire query impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n+q)$ | Build one hash table, then process each query in constant time |
| Space | $O(n)$ | Store side length to index mapping |

With $n,q \le 2 \cdot 10^5$, linear preprocessing and constant-time queries fit comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import isqrt

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, q = map(int, input().split())
    lengths = list(map(int, input().split())

    )

    pos = {}
    for i, l in enumerate(lengths, start=1):
        pos[l] = i

    out = []

    for _ in range(q):
        vals = list(map(int, input().split()))

        total = 0
        ok = True

        for d in vals:
            if d % 3:
                ok = False
                break

            x = d // 3
            r = isqrt(x)

            if r * r != x:
                ok = False
                break

            total += r

        if not ok:
            out.append("-1")
        else:
            out.append(str(pos.get(2 * total, -1)))

    return "\n".join(out)

# provided sample
assert run(
"""3 3
14 6 12
3 3 3
48 3 12
24 6 6
"""
) == "2\n1\n-1"

# minimum size
assert run(
"""1 1
6
3 3 3
"""
) == "1"

# distance not divisible by 3
assert run(
"""1 1
6
3 3 1
"""
) == "-1"

# divisible by 3 but not a square after division
assert run(
"""1 1
10
6 6 6
"""
) == "-1"

# valid query but triangle absent
assert run(
"""1 1
8
3 12 27
"""
) == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One triangle of side 6, query 3 3 3 | 1 | Smallest valid configuration |
| Query containing 1 | -1 | Non-divisibility by 3 |
| Query containing 6 | -1 | Not of form $3a^2$ |
| Valid altitude but missing side length | -1 | Dictionary lookup correctness |

## Edge Cases

Consider:

```
1 1
6
3 3 1
```

The algorithm examines the third value. Since `1 % 3 != 0`, it immediately rejects the query and outputs `-1`. The sum contains a rational component and cannot equal an altitude of the form $k\sqrt3$.

Consider:

```
1 1
12
6 6 6
```

Each value is divisible by 3, but

$$6/3 = 2$$

is not a perfect square. The integer square root check fails, so the answer is `-1`. This prevents incorrectly treating $\sqrt6$ as a multiple of $\sqrt3$.

Consider:

```
1 1
8
3 12 27
```

The values correspond to $a_1=1$, $a_2=2$, $a_3=3$. Their sum is $6$, so the required side length is $12$. The only available triangle has side length $8$, so the lookup fails and the algorithm outputs `-1`.

In every case, the decision follows directly from the exact algebraic structure of the distances, with no floating point arithmetic involved.
