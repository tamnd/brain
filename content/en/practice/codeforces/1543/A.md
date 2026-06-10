---
title: "CF 1543A - Exciting Bets"
description: "We start with two non-negative integers, a and b. In one move we may either add 1 to both numbers or subtract 1 from both numbers, as long as both remain non-negative. After any number of moves, the excitement is defined as gcd(a, b)."
date: "2026-06-10T14:00:45+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1543
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 730 (Div. 2)"
rating: 900
weight: 1543
solve_time_s: 361
verified: false
draft: false
---

[CF 1543A - Exciting Bets](https://codeforces.com/problemset/problem/1543/A)

**Rating:** 900  
**Tags:** greedy, math, number theory  
**Solve time:** 6m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We start with two non-negative integers, `a` and `b`. In one move we may either add `1` to both numbers or subtract `1` from both numbers, as long as both remain non-negative. After any number of moves, the excitement is defined as `gcd(a, b)`.

The task is not to maximize the numbers themselves. We must find the largest possible value of `gcd(a, b)` that can ever be reached using these operations, and among all ways to reach that maximum value, report the minimum number of moves.

The constraint that immediately matters is that `a` and `b` can be as large as `10^18`. Any approach that simulates moves is impossible. Even moving one endpoint to zero could require up to `10^18` operations. Since there are up to `5000` test cases, we need a constant-time solution per test case.

The key difficulty is understanding how adding or subtracting the same amount to both numbers affects their greatest common divisor.

Several edge cases are easy to miss.

Consider `a = b = 4`.

The output is:

```
0 0
```

Since both numbers are always equal after every operation, we can make them arbitrarily large by repeatedly adding `1`. The excitement becomes `gcd(x, x) = x`, which has no upper bound. A solution that blindly computes `|a - b|` would return `0`, but the problem interprets this situation as infinite excitement.

Consider `a = 1, b = 2`.

The output is:

```
1 0
```

The difference is `1`, so every reachable pair has gcd at most `1`. Since the current gcd is already `1`, no move is needed. A careless solution might try to move toward zero and report a positive number of moves.

Consider `a = 3, b = 9`.

The output is:

```
6 3
```

The maximum possible excitement is not the current gcd, which is `3`. By decreasing both numbers three times we reach `(0, 6)`, whose gcd is `6`. Any solution that only examines the initial gcd misses the real optimum.

## Approaches

A brute-force idea is to try every possible number of moves. If we shift both numbers by some integer `k`, the reachable state is `(a+k, b+k)` as long as both values stay non-negative. For each reachable shift we could compute the gcd and keep the best answer.

This works conceptually because every sequence of operations is equivalent to adding the same integer `k` to both numbers. Unfortunately, `k` may range over values on the order of `10^18`, making such an approach hopelessly slow.

The turning point comes from looking at what never changes.

If we transform `(a, b)` into `(a+k, b+k)`, then

$$(a+k) - (b+k) = a-b$$

The difference remains constant.

Suppose some value `g` divides both final numbers. Then `g` must also divide their difference:

$$g \mid ((a+k)-(b+k))$$

which means

$$g \mid |a-b|$$

So no achievable gcd can exceed `|a-b|`.

The next question is whether `|a-b|` itself is achievable.

Let

$$d = |a-b|$$

Assume `a < b`. Then `b = a + d`.

If we decrease both numbers by exactly `a`, we reach

$$(0, d)$$

whose gcd equals `d`.

So the upper bound is attainable. The maximum excitement is exactly `|a-b|`.

Now we only need the minimum moves needed to reach a state where both numbers are multiples of `d`.

Let `m = min(a,b)`.

Any reachable pair has form `(a+k, b+k)`. We want one of them to become divisible by `d`. Since the difference is already a multiple of `d`, once one number is divisible by `d`, the other automatically is too.

We need the smallest distance from `m` to a multiple of `d`.

The nearest multiple can be reached either by moving downward or upward.

The downward distance is:

$$m \bmod d$$

The upward distance is:

$$d - (m \bmod d)$$

We choose the smaller one.

When `a = b`, the difference is zero, giving the special infinite-excitement case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | a-b | ) to O(10^18) |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `a` and `b`.
2. If `a == b`, output `0 0`.

When both numbers are equal, they remain equal forever. Repeatedly increasing both numbers makes the gcd arbitrarily large, so the maximum excitement is unbounded.
3. Compute

$$d = |a-b|$$

This value is the largest gcd that can ever be achieved because every reachable gcd must divide the invariant difference.
4. Let

$$m = \min(a,b)$$

We only need one number to become divisible by `d`. Then both numbers will be divisible by `d` because their difference is already a multiple of `d`.
5. Compute

$$r = m \bmod d$$

The distance to the nearest lower multiple of `d` is `r`.
6. The distance to the nearest higher multiple of `d` is `d-r`.
7. The minimum number of moves required is

$$\min(r, d-r)$$
8. Output `d` and the minimum move count.

### Why it works

The invariant is that the difference between the two numbers never changes. Any common divisor of the final pair must divide that fixed difference, so no achievable gcd can exceed `|a-b|`.

That bound is attainable. If the smaller number is reduced to zero, the pair becomes `(0, |a-b|)`, whose gcd equals `|a-b|`. Thus the maximum excitement is exactly `|a-b|`.

To achieve this maximum gcd, both numbers must be divisible by `|a-b|`. Since their difference already is, making either number divisible by `|a-b|` automatically makes the other divisible as well. The smallest number of moves is exactly the shortest distance from the smaller number to a multiple of `|a-b|`, which is `min(r, d-r)`.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    a, b = map(int, input().split())

    if a == b:
        print(0, 0)
        continue

    d = abs(a - b)
    r = min(a, b) % d

    print(d, min(r, d - r))
```

The first branch handles the special case where the numbers are equal. This must be checked before computing the remainder because `d` would be zero and division by zero is invalid.

For all other cases, `d = |a-b|` is the maximum achievable excitement. The remainder `r` tells us how far the smaller number is from the previous multiple of `d`. Moving upward to the next multiple costs `d-r` moves. The smaller of those two distances is the answer.

Python integers automatically handle values up to `10^18` and beyond, so there is no overflow risk.

## Worked Examples

### Example 1: `a = 8, b = 5`

| Variable | Value |
| --- | --- |
| `a` | 8 |
| `b` | 5 |
| `d = | a-b |
| `m = min(a,b)` | 5 |
| `r = m % d` | 2 |
| `d-r` | 1 |
| moves | 1 |

Output:

```
3 1
```

One move upward gives `(9, 6)`. Both numbers become divisible by `3`, so the gcd becomes `3`, which is the maximum possible value.

### Example 2: `a = 3, b = 9`

| Variable | Value |
| --- | --- |
| `a` | 3 |
| `b` | 9 |
| `d = | a-b |
| `m = min(a,b)` | 3 |
| `r = m % d` | 3 |
| `d-r` | 3 |
| moves | 3 |

Output:

```
6 3
```

Three downward moves produce `(0, 6)`. Three upward moves would produce `(6, 12)`. Both achieve gcd `6`, and three moves is optimal.

This example demonstrates that the maximum achievable gcd can be larger than the current gcd.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

With at most `5000` test cases, the total work is only a few thousand arithmetic computations. The solution comfortably fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())

    ans = []
    for _ in range(t):
        a, b = map(int, input().split())

        if a == b:
            ans.append("0 0")
            continue

        d = abs(a - b)
        r = min(a, b) % d
        ans.append(f"{d} {min(r, d - r)}")

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# provided sample
assert run(
"""4
8 5
1 2
4 4
3 9
"""
) == """3 1
1 0
0 0
6 3"""

# minimum values
assert run(
"""1
0 0
"""
) == """0 0"""

# difference equals 1
assert run(
"""1
1 2
"""
) == """1 0"""

# equal large values
assert run(
"""1
1000000000000000000 1000000000000000000
"""
) == """0 0"""

# large boundary values
assert run(
"""1
0 1000000000000000000
"""
) == """1000000000000000000 0"""

# off-by-one style case
assert run(
"""1
10 16
"""
) == """6 2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `0 0` | Infinite-excitement case at minimum values |
| `1 2` | `1 0` | Difference of one always gives gcd one |
| `10^18 10^18` | `0 0` | Equal large values |
| `0 10^18` | `10^18 0` | Already at maximum gcd |
| `10 16` | `6 2` | Correct nearest-multiple computation |

## Edge Cases

### Equal numbers

Input:

```
1
4 4
```

The algorithm first checks `a == b`. Since the condition is true, it immediately outputs:

```
0 0
```

This is correct because every reachable state has form `(4+k, 4+k)`, and the gcd equals `4+k`. By choosing arbitrarily large `k`, the excitement has no upper bound.

### Difference equal to one

Input:

```
1
1 2
```

We compute:

| Variable | Value |
| --- | --- |
| `d` | 1 |
| `m` | 1 |
| `r` | 0 |
| moves | 0 |

Output:

```
1 0
```

Every achievable gcd must divide the invariant difference `1`, so the maximum possible gcd is already fixed at `1`.

### One number already zero

Input:

```
1
0 6
```

We compute:

| Variable | Value |
| --- | --- |
| `d` | 6 |
| `m` | 0 |
| `r` | 0 |
| moves | 0 |

Output:

```
6 0
```

The pair already has gcd `6`, which equals the maximum achievable value `|0-6|`.

### Exactly midway between two multiples

Input:

```
1
3 9
```

We compute:

| Variable | Value |
| --- | --- |
| `d` | 6 |
| `r` | 3 |
| `d-r` | 3 |

Both directions require the same number of moves, so the answer is:

```
6 3
```

This verifies that taking `min(r, d-r)` correctly handles ties between moving upward and downward.
