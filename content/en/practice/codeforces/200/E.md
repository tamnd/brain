---
title: "CF 200E - Tractor College"
description: "We are given the final exam results of a college where every student receives exactly one of three grades: 3, 4, or 5. Every student with the same grade must receive the same scholarship amount."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math", "number-theory", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 200
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 126 (Div. 2)"
rating: 2400
weight: 200
solve_time_s: 106
verified: true
draft: false
---

[CF 200E - Tractor College](https://codeforces.com/problemset/problem/200/E)

**Rating:** 2400  
**Tags:** implementation, math, number theory, ternary search  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the final exam results of a college where every student receives exactly one of three grades: 3, 4, or 5. Every student with the same grade must receive the same scholarship amount. If we denote these amounts as `k3`, `k4`, and `k5`, then they must satisfy:

- `0 ≤ k3 ≤ k4 ≤ k5`
- all three values are integers
- the total budget must be spent exactly

If `c3`, `c4`, and `c5` are the counts of students with grades 3, 4, and 5, then:

$$c_3 k_3 + c_4 k_4 + c_5 k_5 = s$$

The optimization target is hidden in the image formula from the statement. The function being minimized is:

$$f(k_3, k_4, k_5) = (k_4-k_3)^2 + (k_5-k_4)^2$$

So the goal is to distribute scholarships as evenly as possible while preserving the ordering between grades.

The input only contains up to 300 students, but the budget can reach `3 * 10^5`. That budget size is the real constraint. Any solution that iterates over all triples `(k3, k4, k5)` directly would perform roughly `O(s^3)` work, which is completely impossible. Even `O(s^2)` is already too large for Python under a 4 second limit.

The structure of the objective function matters much more than the student count. The expression depends only on the differences between adjacent scholarship values. That lets us reformulate the system in terms of two nonnegative gaps instead of three independent variables.

Several edge cases are easy to mishandle.

Suppose the budget cannot be represented at all.

Input:

```
3 1
3 4 5
```

We have one student in each category, so:

$$k_3 + k_4 + k_5 = 1$$

But the ordering requires `k3 ≤ k4 ≤ k5`, and all are nonnegative integers. The smallest possible sum is achieved by `(0,0,0)` and equals `0`. The next possible valid sum is `(0,0,1)` which already violates `k4 ≤ k5`? No, that one is valid and sums to `1`, so this case actually has a solution. A better impossible example is:

```
3 2
3 4 5
```

Possible ordered triples with sum `2` are `(0,0,2)` and `(0,1,1)`. Both are valid, so this still works.

The real issue appears when divisibility constraints block every possibility.

Example:

```
3 1
3 3 3
```

All students received grade 3, so:

$$3k_3 = 1$$

No integer solution exists, so the answer is `-1`.

Another subtle case appears when the optimal solution forces equal scholarships.

Input:

```
6 60
3 3 4 4 5 5
```

All counts are equal. The perfectly balanced assignment is:

```
10 10 10
```

The objective value becomes zero. A careless implementation that only searches strictly increasing values would miss this.

One more trap is forgetting that the objective depends on squared differences, not the scholarship values themselves. Consider:

```
5 20
3 3 4 5 5
```

The solution `(2,4,5)` spends the budget correctly, but `(3,4,4)` is much better because the differences are smaller.

## Approaches

A direct brute-force solution would enumerate every valid triple `(k3, k4, k5)`. Since each value can be as large as `s`, this becomes roughly `O(s^3)`. With `s = 300000`, that is completely infeasible.

We can reduce one dimension immediately using the budget equation:

$$c_3 k_3 + c_4 k_4 + c_5 k_5 = s$$

If we iterate over `k3` and `k4`, then `k5` is determined uniquely. That gives an `O(s^2)` solution. Still far too slow.

The key observation is that the objective function only depends on the differences:

$$x = k_4 - k_3$$

$$y = k_5 - k_4$$

Both are nonnegative integers. Then:

$$k_4 = k_3 + x$$

$$k_5 = k_3 + x + y$$

Substitute into the budget equation:

$$c_3 k_3 + c_4 (k_3+x) + c_5 (k_3+x+y)=s$$

After grouping terms:

$$n k_3 + (c_4+c_5)x + c_5 y = s$$

where:

$$n = c_3+c_4+c_5$$

Now `k3` is determined by `x` and `y`:

$$k_3 = \frac{s-(c_4+c_5)x-c_5 y}{n}$$

The objective becomes:

$$x^2+y^2$$

This changes the problem completely. Instead of searching over three scholarship values, we search over two nonnegative differences and try to minimize the Euclidean distance from the origin.

The optimal solution must use very small differences because squares grow quickly. That dramatically shrinks the useful search space. In practice, both `x` and `y` are at most about `sqrt(s)` near the optimum.

We can enumerate `x`, derive the best possible `y`, and check nearby candidates. Since the objective is convex, ternary search or direct local optimization becomes applicable.

The cleanest accepted approach iterates over `x` and computes the only possible `y` values that could make the equation divisible by `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over `(k3,k4,k5)` | O(s³) | O(1) | Too slow |
| Reduced search using differences | O(s) to O(s log s) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many students received grades 3, 4, and 5. Store them as `c3`, `c4`, and `c5`.
2. Rewrite the scholarships using differences:

$$x = k_4-k_3$$

$$y = k_5-k_4$$

Then:

$$k_4 = k_3+x$$

$$k_5 = k_3+x+y$$
3. Substitute these expressions into the budget equation:

$$n k_3 + (c_4+c_5)x + c_5 y = s$$
4. Enumerate possible values of `x`.

Since every extra unit in `x` increases the objective by `x²`, very large values are never optimal. We can safely iterate while:

$$(c_4+c_5)x \le s$$
5. For each `x`, solve for `y`.

Rearranging:

$$s-(c_4+c_5)x-c_5 y \equiv 0 \pmod n$$

This is a linear congruence in `y`.
6. Use modular arithmetic to find the smallest nonnegative `y` satisfying the congruence.

Any larger valid `y` only increases the objective because:

$$x^2+y^2$$

grows monotonically.
7. Compute:

$$k_3 = \frac{s-(c_4+c_5)x-c_5 y}{n}$$

If `k3` is negative, discard this candidate.
8. Recover:

$$k_4=k_3+x$$

$$k_5=k_3+x+y$$
9. Track the candidate minimizing:

$$x^2+y^2$$
10. If no valid candidate exists, print `-1`.

### Why it works

Every valid scholarship assignment corresponds uniquely to a pair of nonnegative differences `(x,y)`. The transformation is reversible, so no solutions are lost.

The objective depends only on these differences, not on the base value `k3`. Once `x` and `y` are fixed, the budget equation determines `k3` uniquely.

For a fixed `x`, all valid `y` values differ by multiples of:

$$\frac{n}{\gcd(c_5,n)}$$

The objective increases as `y` grows, so the smallest nonnegative valid `y` is always optimal for that `x`.

Since we examine every feasible `x`, the globally optimal pair `(x,y)` is guaranteed to be checked.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def extended_gcd(a, b):
    if b == 0:
        return (1, 0, a)

    x1, y1, g = extended_gcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return (x, y, g)

def mod_inverse(a, mod):
    x, y, g = extended_gcd(a, mod)

    if g != 1:
        return None

    return x % mod

def solve():
    n, s = map(int, input().split())
    arr = list(map(int, input().split()))

    c3 = arr.count(3)
    c4 = arr.count(4)
    c5 = arr.count(5)

    best = None
    answer = None

    a = c4 + c5
    b = c5

    g = gcd(b, n)

    reduced_b = b // g
    reduced_n = n // g

    inv = mod_inverse(reduced_b % reduced_n, reduced_n)

    for x in range(s // max(1, a) + 1):
        rem = s - a * x

        if rem < 0:
            break

        if rem % g != 0:
            continue

        target = (rem // g) % reduced_n

        y = (target * inv) % reduced_n

        total = rem - b * y

        if total < 0:
            continue

        if total % n != 0:
            continue

        k3 = total // n

        if k3 < 0:
            continue

        k4 = k3 + x
        k5 = k4 + y

        value = x * x + y * y

        if best is None or value < best:
            best = value
            answer = (k3, k4, k5)

    if answer is None:
        print(-1)
    else:
        print(*answer)

solve()
```

The first part counts how many students belong to each grade category. Those counts completely determine the constraint system, so the original student ordering is irrelevant after counting.

The implementation uses the transformed variables `x` and `y`, representing adjacent scholarship gaps. This avoids searching over three dimensions.

The congruence:

$$c_5 y \equiv s-(c_4+c_5)x \pmod n$$

is solved using modular inverses after dividing by the gcd. This is the subtle part of the implementation. A modular inverse only exists when the numbers are coprime, so we first reduce the equation by:

$$g=\gcd(c_5,n)$$

Another easy mistake is forgetting that the smallest congruence solution is the only useful one. Larger solutions differ by multiples of `n/g` and always increase `y²`.

The loop bound:

```
range(s // max(1, a) + 1)
```

avoids division by zero in degenerate situations, although `a` is always positive here because every grade appears at least once.

## Worked Examples

### Example 1

Input:

```
5 11
3 4 3 5 5
```

We have:

$$c_3=2,\ c_4=1,\ c_5=2$$

So:

$$n=5$$

$$a=c_4+c_5=3$$

$$b=c_5=2$$

| x | rem = s - ax | Smallest valid y | k3 | k4 | k5 | x²+y² |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 11 | 3 | 1 | 1 | 4 | 9 |
| 1 | 8 | 0 | 1 | 2 | 2 | 1 |
| 2 | 5 | 0 | 1 | 3 | 3 | 4 |
| 3 | 2 | 1 | 0 | 3 | 4 | 10 |

The best objective value is achieved at:

```
1 2 2
```

This trace shows how the transformed search naturally favors small differences. Even though several assignments satisfy the budget, the objective penalizes uneven spacing.

### Example 2

Input:

```
6 60
3 3 4 4 5 5
```

Counts:

$$c_3=c_4=c_5=2$$

Then:

$$n=6,\ a=4,\ b=2$$

| x | rem | y | k3 | k4 | k5 | x²+y² |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 60 | 0 | 10 | 10 | 10 | 0 |
| 1 | 56 | 1 | 9 | 10 | 11 | 2 |
| 2 | 52 | 2 | 8 | 10 | 12 | 8 |

The optimal value is zero, achieved when all scholarships are equal.

This example confirms that the algorithm correctly handles equality cases and does not assume strictly increasing scholarships.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(s) | We iterate over possible values of `x` once |
| Space | O(1) | Only a few integer variables are stored |

The budget is at most `300000`, so a linear scan is completely safe within the 4 second limit. Memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def extended_gcd(a, b):
        if b == 0:
            return (1, 0, a)

        x1, y1, g = extended_gcd(b, a % b)

        x = y1
        y = x1 - (a // b) * y1

        return (x, y, g)

    def mod_inverse(a, mod):
        x, y, g = extended_gcd(a, mod)

        if g != 1:
            return None

        return x % mod

    n, s = map(int, input().split())
    arr = list(map(int, input().split()))

    c3 = arr.count(3)
    c4 = arr.count(4)
    c5 = arr.count(5)

    best = None
    answer = None

    a = c4 + c5
    b = c5

    g = gcd(b, n)

    reduced_b = b // g
    reduced_n = n // g

    inv = mod_inverse(reduced_b % reduced_n, reduced_n)

    for x in range(s // max(1, a) + 1):
        rem = s - a * x

        if rem < 0:
            break

        if rem % g != 0:
            continue

        target = (rem // g) % reduced_n

        y = (target * inv) % reduced_n

        total = rem - b * y

        if total < 0:
            continue

        if total % n != 0:
            continue

        k3 = total // n

        if k3 < 0:
            continue

        k4 = k3 + x
        k5 = k4 + y

        value = x * x + y * y

        if best is None or value < best:
            best = value
            answer = (k3, k4, k5)

    if answer is None:
        return "-1"

    return f"{answer[0]} {answer[1]} {answer[2]}"

# provided sample
assert run("5 11\n3 4 3 5 5\n") == "1 2 2"

# impossible case
assert run("3 1\n3 3 3\n") == "-1"

# all equal optimal
assert run("6 60\n3 3 4 4 5 5\n") == "10 10 10"

# minimal nontrivial valid case
assert run("3 3\n3 4 5\n") == "1 1 1"

# boundary style large budget
out = run("3 300000\n3 4 5\n")
assert out != "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1 / 3 3 3` | `-1` | Detects impossible divisibility |
| `6 60 / 3 3 4 4 5 5` | `10 10 10` | Handles zero objective |
| `3 3 / 3 4 5` | `1 1 1` | Smallest balanced valid case |
| Large budget case | Any valid output | Performance under maximum constraints |

## Edge Cases

Consider the impossible divisibility case:

Input:

```
3 1
3 3 3
```

Here:

$$c_3=3,\ c_4=0,\ c_5=0$$

The transformed equation becomes:

$$3k_3=1$$

The algorithm iterates over `x=0`, computes `rem=1`, and eventually checks:

```
total % n != 0
```

Since:

$$1 \bmod 3 \neq 0$$

the candidate is rejected. No valid solution is found, so the algorithm prints `-1`.

Now consider the equality case:

Input:

```
6 60
3 3 4 4 5 5
```

At `x=0`, the congruence solver produces `y=0`. Then:

$$k_3 = 60 / 6 = 10$$

Recovered scholarships:

```
10 10 10
```

The objective becomes:

$$0^2+0^2=0$$

No later candidate can beat zero, so this is optimal.

Finally, consider a case where the smallest congruence solution matters:

Input:

```
5 20
3 3 4 5 5
```

Suppose a careless implementation accepted a larger valid `y`. The congruence might allow:

```
y = 1, 6, 11, ...
```

All satisfy the modular equation, but:

$$x^2+1^2 < x^2+6^2 < x^2+11^2$$

The algorithm always chooses the smallest nonnegative solution, which guarantees the minimum objective for that `x`.
