---
title: "CF 1651B - Prove Him Wrong"
description: "We need to construct an array of length n such that applying the given operation to any pair of positions never decreases the total sum of the array. Suppose we choose two values x and y."
date: "2026-06-10T03:48:49+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1651
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 124 (Rated for Div. 2)"
rating: 800
weight: 1651
solve_time_s: 130
verified: true
draft: false
---

[CF 1651B - Prove Him Wrong](https://codeforces.com/problemset/problem/1651/B)

**Rating:** 800  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to construct an array of length `n` such that applying the given operation to any pair of positions never decreases the total sum of the array.

Suppose we choose two values `x` and `y`. The operation replaces both numbers with `|x-y|`.

Before the operation, these two positions contribute

$$x+y$$

to the total sum.

After the operation, they contribute

$$2|x-y|.$$

For the sum to never decrease, we need

$$2|x-y| \ge x+y$$

for every pair of elements in the array.

The input contains several test cases. For each test case we are given only the desired array length `n`. We must either construct a valid array whose elements lie between `1` and `10^9`, or prove that no such array exists.

The constraints are tiny. There are at most 100 test cases and `n` is at most 1000. Any construction running in linear time per test case is more than enough. The real challenge is discovering the mathematical pattern that makes every pair satisfy the required inequality while keeping all values within the allowed range.

A few edge cases deserve attention.

Consider `n = 2`. The array `[1, 2]` is valid because

$$2|2-1| = 2,\qquad 1+2 = 3.$$

Actually this decreases the sum, so it is not valid. A careless solution might assume any increasing sequence works. We need much larger gaps between consecutive values.

Consider `n = 3` and array `[1, 2, 4]`. For pair `(2,4)`,

$$2|4-2| = 4 < 6.$$

The sum decreases, so powers of two are not sufficient.

Consider large `n`. Even if we find a rapidly growing sequence, all values must remain at most `10^9`. A construction that grows too quickly may exceed the limit before reaching length `n`, making some values illegal.

## Approaches

A brute-force viewpoint is to think directly about the condition for every pair. Given an array, we could check all pairs `(i,j)` and verify whether

$$2|a_i-a_j| \ge a_i+a_j.$$

For an array of length `n`, this requires examining `O(n^2)` pairs.

The real problem is not verification but construction. We need a family of arrays that automatically satisfies the inequality for every pair.

Assume two elements satisfy `x < y`. Then

$$|x-y| = y-x.$$

Substituting into the inequality gives

$$2(y-x)\ge x+y.$$

Rearranging,

$$y \ge 3x.$$

This is the key observation. Every pair must satisfy the condition, and for a sorted array it is enough that every larger element is at least three times the smaller one.

A natural construction is

$$1,\ 3,\ 9,\ 27,\dots$$

where each element is three times the previous one.

For any pair with indices `i < j`,

$$a_j = 3^{j-i}a_i \ge 3a_i,$$

so the derived condition holds automatically.

Now we only need to check how many such values fit under `10^9`.

$$3^{19}=1162261467>10^9,$$

while

$$3^{18}=387420489<10^9.$$

Starting from `1`, we can use at most 19 numbers:

$$3^0,3^1,\dots,3^{18}.$$

Hence a valid array exists only when `n \le 19`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force verification of a candidate | O(n²) | O(1) | Not a construction |
| Powers of 3 construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n`.
2. If `n > 19`, print `NO`.

No valid powers-of-three construction fits inside the limit `10^9`, and the official solution relies on the fact that no larger valid construction is possible within the allowed bounds.
3. Otherwise print `YES`.
4. Generate the sequence

$$1,3,9,27,\dots$$

by repeatedly multiplying the current value by `3`.
5. Output the first `n` values.

The reason this construction works is that every later element is at least three times every earlier element. That is exactly the condition obtained from the inequality governing whether the sum decreases.

### Why it works

Take any two elements of the constructed array and assume `x < y`.

Because the array is powers of three, every larger element is at least three times the smaller one:

$$y \ge 3x.$$

Rearranging gives

$$y-x \ge \frac{x+y}{2}.$$

Multiplying by two,

$$2(y-x)\ge x+y.$$

Since `y>x`, we have `|x-y|=y-x`, so

$$2|x-y|\ge x+y.$$

The contribution of those two positions after the operation is at least their contribution before the operation. Since all other positions remain unchanged, the total sum never decreases.

The largest generated value is `3^{18}=387420489`, which satisfies the bound `10^9`. The next power exceeds the limit, so length 19 is the maximum possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())

    if n > 19:
        print("NO")
        continue

    print("YES")

    cur = 1
    ans = []

    for _ in range(n):
        ans.append(cur)
        cur *= 3

    print(*ans)
```

The program follows the construction directly.

The first decision is whether `n` exceeds 19. If it does, we immediately print `NO`.

For feasible lengths, we build the sequence iteratively. Starting from `1`, each new value is obtained by multiplying the previous one by `3`. This avoids any concerns about floating-point arithmetic or exponentiation errors.

All arithmetic easily fits in Python integers. Even the largest generated value is below `10^9`, so there are no overflow concerns.

## Worked Examples

### Example 1

Input:

```
1
3
```

| Step | Current Value | Generated Array |
| --- | --- | --- |
| Start | 1 | [] |
| Add first element | 1 | [1] |
| Multiply by 3 | 3 | [1] |
| Add second element | 3 | [1, 3] |
| Multiply by 3 | 9 | [1, 3] |
| Add third element | 9 | [1, 3, 9] |

Output:

```
YES
1 3 9
```

Checking the pairs:

$$(1,3),\quad (1,9),\quad (3,9)$$

Every larger value is at least three times the smaller one, so the sum never decreases.

### Example 2

Input:

```
1
20
```

| Step | n | Decision |
| --- | --- | --- |
| Read test case | 20 | Compare with 19 |
| Check limit | 20 > 19 | Impossible |
| Output | - | NO |

Output:

```
NO
```

This trace demonstrates the value-bound restriction. A twentieth power-of-three term would exceed `10^9`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Generate and print `n` numbers |
| Space | O(n) | Store the constructed array |

Since `n ≤ 1000` and at most 100 test cases exist, this complexity is far below the available limits. The actual accepted construction never generates more than 19 values.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        if n > 19:
            out.append("NO")
            continue

        out.append("YES")

        cur = 1
        arr = []
        for _ in range(n):
            arr.append(str(cur))
            cur *= 3

        out.append(" ".join(arr))

    return "\n".join(out) + "\n"

# sample-style tests
assert run("1\n2\n") == "YES\n1 3\n"

# minimum valid size
assert run("1\n2\n") == "YES\n1 3\n"

# largest valid size
out = run("1\n19\n")
assert out.startswith("YES\n")

# first impossible size
assert run("1\n20\n") == "NO\n"

# multiple test cases
assert run("3\n2\n19\n20\n").startswith("YES\n1 3\nYES\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n2\n` | `YES` with two values | Minimum allowed length |
| `1\n19\n` | `YES` | Largest constructible array |
| `1\n20\n` | `NO` | Boundary where values exceed `10^9` |
| `3\n2\n19\n20\n` | Mixed answers | Multiple test case handling |

## Edge Cases

Consider:

```
1
2
```

The algorithm outputs:

```
YES
1 3
```

For the only pair,

$$2|3-1| = 4,$$

while the original contribution is

$$1+3 = 4.$$

The sum stays unchanged, which is allowed.

Consider:

```
1
19
```

The generated array ends with

$$3^{18}=387420489.$$

Every element is within the allowed range. For any pair, the larger value is at least three times the smaller one, so the required inequality holds.

Consider:

```
1
20
```

The next power would be

$$3^{19}=1162261467,$$

which exceeds `10^9`. The algorithm correctly prints `NO` instead of producing an invalid array.

Consider a pair deep inside the sequence, such as `81` and `2187`.

Since

$$2187 = 27 \cdot 81,$$

we have

$$2187 \ge 3 \cdot 81.$$

Thus

$$2(2187-81)=4212,$$

and

$$2187+81=2268.$$

The new contribution is larger than the old one, confirming the invariant used in the proof.
