---
title: "CF 304A - Pythagorean Theorem II"
description: "We need to count how many integer-sided right triangles exist such that all three sides are at most n. A right triangle with sides (a, b, c) satisfies the Pythagorean equation: $a^2+b^2=c^2$$a$$b$$c = sqrt{a^2 + b^2} approx 21.21$$a^2 + b^2 = c^2 approx 225.00 + 225.00 = 450."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 304
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 183 (Div. 2)"
rating: 1200
weight: 304
solve_time_s: 120
verified: true
draft: false
---

[CF 304A - Pythagorean Theorem II](https://codeforces.com/problemset/problem/304/A)

**Rating:** 1200  
**Tags:** brute force, math  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We need to count how many integer-sided right triangles exist such that all three sides are at most `n`.

A right triangle with sides `(a, b, c)` satisfies the Pythagorean equation:

$a^2+b^2=c^2$$a$$b$$c = \sqrt{a^2 + b^2} \approx 21.21$$a^2 + b^2 = c^2 \approx 225.00 + 225.00 = 450.00$Adjusting a and b updates the triangle and the derived value of c.abc

The problem restricts the order of the sides:

```
1 ≤ a ≤ b ≤ c ≤ n
```

The ordering matters because triangles like `(3,4,5)` and `(4,3,5)` should be treated as the same triangle. The condition `a ≤ b` removes duplicates automatically.

The input contains a single integer `n`. The output is the number of valid triples `(a, b, c)` satisfying the equation and the ordering constraints.

The upper bound is only `10^4`. That immediately changes the nature of the problem. Even an `O(n^2)` algorithm performs around `10^8` simple operations in the worst case if implemented carefully in Python, which is still borderline but often acceptable with lightweight arithmetic. An `O(n^3)` solution is completely impossible because it would require roughly `10^12` iterations.

The main challenge is avoiding unnecessary enumeration of triples.

A subtle edge case appears when duplicate triangles are counted accidentally.

For example:

Input:

```
5
```

The only valid triangle is `(3,4,5)`.

The correct answer is:

```
1
```

A careless brute-force that loops over all ordered pairs `(a,b)` without enforcing `a ≤ b` would count both `(3,4,5)` and `(4,3,5)` and incorrectly print `2`.

Another easy mistake is forgetting that `c` must also be at most `n`.

For example:

Input:

```
10
```

The pair `(6,8)` produces `c = 10`, which is valid.

But `(8,15)` produces `c = 17`, which must not be counted even though it satisfies the equation.

A third pitfall comes from floating point precision. Some implementations compute:

```
c = int(math.sqrt(a*a + b*b))
```

and then check whether the equation holds. Floating point rounding can occasionally produce incorrect values for larger numbers. The safe approach is to verify explicitly that:

```
c * c == a * a + b * b
```

before counting the triangle.

## Approaches

The most direct brute-force solution tries every possible triple `(a,b,c)`.

We loop through all values:

```
1 ≤ a ≤ b ≤ c ≤ n
```

and check whether:

$a^2+b^2=c^2$$a$$b$$c = \sqrt{a^2 + b^2} \approx 21.21$$a^2 + b^2 = c^2 \approx 225.00 + 225.00 = 450.00$Adjusting a and b updates the triangle and the derived value of c.abc

This works because the definition of a valid triangle is checked exactly. Nothing is missed and nothing invalid is counted.

The problem is the number of iterations. There are roughly:

$n^3$

possible triples. With `n = 10^4`, that becomes about `10^12` checks, far beyond the time limit.

The key observation is that once `a` and `b` are fixed, the value of `c` is completely determined.

From the equation:

$c=\sqrt{a^2+b^2}$$a$$b$$c = \sqrt{a^2 + b^2} \approx 21.21$$a^2 + b^2 = c^2 \approx 225.00 + 225.00 = 450.00$Adjusting a and b updates the triangle and the derived value of c.abc

So instead of iterating over three variables, we only iterate over `(a,b)` and test whether the resulting square root is an integer.

This reduces the search space from cubic to quadratic.

For every pair `(a,b)` with `a ≤ b`, we compute:

```
s = a*a + b*b
c = int(sqrt(s))
```

If `c*c == s` and `c ≤ n`, then we found one valid triangle.

The quadratic approach succeeds because the constraint `n ≤ 10^4` allows about `5 × 10^7` lightweight iterations in optimized Python.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Optimal | O(n²) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Initialize `answer = 0`.
3. Iterate `a` from `1` to `n`.

This chooses the first leg of the triangle.
4. Iterate `b` from `a` to `n`.

Starting from `a` guarantees `a ≤ b`, so every triangle is counted exactly once.
5. Compute:

```
s = a*a + b*b
```

This is the square of the hypotenuse.
6. Compute:

```
c = int(s ** 0.5)
```

We only need to check whether `s` is a perfect square.
7. Verify both conditions:

```
c * c == s
c <= n
```

The first condition confirms that `c` is an integer.

The second ensures the triangle respects the problem bounds.
8. If both conditions hold, increment the answer.
9. Print the final answer.

### Why it works

The algorithm examines every possible ordered pair `(a,b)` satisfying `1 ≤ a ≤ b ≤ n`.

For each pair, there is exactly one possible value of `c` that could satisfy the Pythagorean equation. The algorithm computes that candidate and checks whether it is a valid integer within bounds.

Every valid triangle appears exactly once because the loop enforces `a ≤ b`. No invalid triangle can be counted because the equality:

$a^2+b^2=c^2$$a$$b$$c = \sqrt{a^2 + b^2} \approx 21.21$$a^2 + b^2 = c^2 \approx 225.00 + 225.00 = 450.00$Adjusting a and b updates the triangle and the derived value of c.abc

is checked directly.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

answer = 0

for a in range(1, n + 1):
    for b in range(a, n + 1):
        s = a * a + b * b
        c = int(s ** 0.5)

        if c <= n and c * c == s:
            answer += 1

print(answer)
```

The outer loop chooses the first leg `a`. The inner loop starts from `a` instead of `1`, which removes duplicate orderings automatically.

The variable `s` stores:

$a^2+b^2$

The code computes the integer square root candidate `c` using floating point square root and integer conversion. The crucial detail is the validation step:

```
c * c == s
```

Without this check, rounding errors could incorrectly classify non-squares as squares.

The condition:

```
c <= n
```

prevents counting triangles whose hypotenuse exceeds the limit.

No extra arrays or data structures are required, so the memory usage stays constant.

## Worked Examples

### Example 1

Input:

```
5
```

| a | b | s = a²+b² | c | Valid? | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 1 | No | 0 |
| 1 | 2 | 5 | 2 | No | 0 |
| 1 | 3 | 10 | 3 | No | 0 |
| 1 | 4 | 17 | 4 | No | 0 |
| 1 | 5 | 26 | 5 | No | 0 |
| 2 | 2 | 8 | 2 | No | 0 |
| 2 | 3 | 13 | 3 | No | 0 |
| 2 | 4 | 20 | 4 | No | 0 |
| 2 | 5 | 29 | 5 | No | 0 |
| 3 | 4 | 25 | 5 | Yes | 1 |

The only valid triple is `(3,4,5)`. The ordering condition avoids counting `(4,3,5)` separately.

### Example 2

Input:

```
10
```

| a | b | s | c | Valid? | Answer |
| --- | --- | --- | --- | --- | --- |
| 3 | 4 | 25 | 5 | Yes | 1 |
| 6 | 8 | 100 | 10 | Yes | 2 |
| Remaining pairs | - | - | - | No | 2 |

The valid triangles are `(3,4,5)` and `(6,8,10)`.

This example demonstrates that multiple scaled versions of a primitive Pythagorean triple are counted separately as long as all sides remain within the limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Two nested loops over `a` and `b` |
| Space | O(1) | Only a few integer variables are stored |

With `n = 10^4`, the algorithm performs roughly fifty million iterations in the worst case. Each iteration only does a few arithmetic operations, which fits comfortably within the limits in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    answer = 0

    for a in range(1, n + 1):
        for b in range(a, n + 1):
            s = a * a + b * b
            c = int(s ** 0.5)

            if c <= n and c * c == s:
                answer += 1

    print(answer)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout
    return out.getvalue()

# provided sample
assert run("5\n") == "1\n", "sample 1"

# minimum input
assert run("1\n") == "0\n", "no triangle possible"

# first valid triangle appears
assert run("3\n") == "0\n", "3-4-5 not fully included"

# exact boundary inclusion
assert run("5\n") == "1\n", "3-4-5 counted"

# multiple triples
assert run("10\n") == "2\n", "3-4-5 and 6-8-10"

# larger case
assert run("25\n") == "8\n", "multiple primitive and scaled triples"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Minimum boundary |
| `3` | `0` | Hypotenuse exceeds limit |
| `5` | `1` | First valid Pythagorean triple |
| `10` | `2` | Multiple valid triples |
| `25` | `8` | Larger search space and scaling behavior |

## Edge Cases

Consider the smallest possible input:

```
1
```

The loops only test `(1,1)`.

The algorithm computes:

```
1² + 1² = 2
```

Since `2` is not a perfect square, no triangle is counted. The output becomes:

```
0
```

This confirms the algorithm correctly handles cases where no valid triangle exists.

Now consider the duplicate-counting issue:

```
5
```

A naive implementation that loops independently over all `a` and `b` would count both:

```
(3,4,5)
(4,3,5)
```

The current algorithm avoids this because the inner loop starts from `b = a`. Once `(3,4)` is processed, `(4,3)` never appears.

Finally, consider a case where the hypotenuse exceeds the limit:

```
10
```

The pair `(8,15)` satisfies the Pythagorean equation because:

$8^2+15^2=17^2$

But `17 > 10`, so the condition:

```
c <= n
```

rejects it correctly. Without that check, the algorithm would overcount invalid triangles.
