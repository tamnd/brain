---
title: "CF 70A - Cookies"
description: "We have a square box of size 2^n × 2^n. Inside this box, we repeatedly place special triangular cookies. A cookie of size k occupies the upper triangular part of a k × k square, including the main diagonal."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 70
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 64"
rating: 1300
weight: 70
solve_time_s: 106
verified: true
draft: false
---

[CF 70A - Cookies](https://codeforces.com/problemset/problem/70/A)

**Rating:** 1300  
**Tags:** math  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a square box of size `2^n × 2^n`. Inside this box, we repeatedly place special triangular cookies.

A cookie of size `k` occupies the upper triangular part of a `k × k` square, including the main diagonal. Its area is:

$$1 + 2 + 3 + \dots + k = \frac{k(k+1)}{2}$$

The cookies cannot be rotated, so every cookie always points in the same direction.

The packing process is greedy. At every step, we choose the largest cookie that can still fit somewhere in the remaining empty space, place it, and continue until no cookie of size at least `2` can be placed anymore. Cookies of size `1` do not exist.

The task is to compute how many unit cells stay empty after this process finishes. Since the number grows quickly, the answer must be printed modulo `10^6 + 3`.

The constraint is small, `n ≤ 1000`, but the actual board size is `2^n × 2^n`, which becomes astronomically large. For example, when `n = 1000`, the side length itself has more than 300 decimal digits. Any approach that tries to construct the board explicitly is impossible. Even storing one row would already be infeasible.

This immediately tells us the solution must come from identifying a mathematical pattern.

A subtle edge case appears at `n = 0`. The board size becomes `1 × 1`, but cookies of size `1` do not exist. The box remains completely empty.

Input:

```
0
```

Correct output:

```
1
```

A careless implementation that assumes every board can fit at least one cookie would incorrectly print `0`.

Another easy mistake is misunderstanding the greedy process. The packing is not arbitrary. The largest possible cookie is always chosen first. For example, for `n = 1`, the board is `2 × 2`. A size-2 cookie fits exactly once and covers 3 cells, leaving 1 empty cell.

Input:

```
1
```

Correct output:

```
1
```

If someone incorrectly assumes smaller cookies may also be used afterward, they might try to fill the remaining cell with a nonexistent size-1 cookie.

The final trap is integer overflow in languages with fixed-width integers. The board area is:

$$(2^n)^2 = 4^n$$

For `n = 1000`, this number is enormous. The modulo must be applied during exponentiation instead of after constructing the full value.

## Approaches

The most direct approach is to simulate the packing process on the grid itself. We could represent the `2^n × 2^n` board, repeatedly search for the largest cookie that fits, place it, and continue until no placement remains.

This works for tiny values of `n`. For example, when `n = 3`, the board is only `8 × 8`, so brute force is manageable. The issue is that the side length doubles with every increment of `n`. At `n = 20`, the board already contains more than one trillion cells. Even iterating over the grid once becomes impossible.

The brute-force idea fails because it treats the board as arbitrary geometry, while the actual process has a very rigid recursive structure.

The key observation is that the greedy packing creates a perfect recursive decomposition.

Start with a `2^n × 2^n` board. The largest cookie that fits is exactly size `2^n`. That cookie occupies the entire upper triangular half of the board.

What remains uncovered is another triangular region in the lower-right half. After shifting coordinates, that remaining region has exactly the same shape as the original problem for size `2^{n-1}`.

This means the number of empty cells follows a recurrence.

Let `f(n)` be the number of uncovered cells for a board of size `2^n × 2^n`.

The largest cookie covers:

$$\frac{2^n(2^n+1)}{2}$$

The total board area is:

$$4^n$$

The uncovered region after placing the largest cookie becomes another instance of the same problem with parameter `n-1`.

Experimenting with small values reveals:

$$f(0)=1$$

$$f(1)=1$$

$$f(2)=3$$

$$f(3)=9$$

This is a geometric progression:

$$f(n)=3^{n-1} \quad \text{for } n \ge 1$$

The recurrence can also be derived formally:

$$f(n)=3f(n-1)$$

Each recursive subdivision creates three copies of the previous uncovered pattern.

Once the pattern is identified, the problem reduces to modular exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in board size | Exponential in board size | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Handle the special case `n = 0`.

The board is `1 × 1`, and no cookie can be placed because the minimum cookie size is `2`. The single cell remains empty, so the answer is `1`.
3. For `n ≥ 1`, use the derived formula:

$$f(n)=3^{n-1}$$

This follows from the recursive structure of the uncovered regions after each largest-cookie placement.

1. Compute the power modulo `10^6 + 3`.

Python's built-in `pow(base, exp, mod)` performs fast binary exponentiation in logarithmic time.
2. Print the result.

### Why it works

The greedy process always places the largest possible cookie first, which is a cookie of size `2^n`. After placing it, the remaining uncovered area splits into smaller regions that reproduce the same geometric structure as the original problem.

Each recursive level produces exactly three independent copies of the previous uncovered configuration. Because the base case contains one uncovered cell, the number of uncovered cells triples at every level:

$$f(n)=3f(n-1)$$

Solving this recurrence gives:

$$f(n)=3^{n-1}$$

for all `n ≥ 1`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**6 + 3

n = int(input())

if n == 0:
    print(1)
else:
    print(pow(3, n - 1, MOD))
```

The implementation is intentionally short because the difficult part of the problem is discovering the recurrence, not coding it.

The first branch handles the only exceptional case. When `n = 0`, the board is too small to place any cookie, so the answer is exactly one empty cell.

For all larger values, the solution uses the closed-form recurrence:

$$f(n)=3^{n-1}$$

The built-in `pow` function with three arguments computes modular exponentiation efficiently using repeated squaring. This avoids constructing enormous intermediate numbers such as `3^999`.

An easy off-by-one mistake is using `3^n` instead of `3^{n-1}`. Checking small values immediately exposes the issue:

For `n = 1`, the answer must be `1`, not `3`.

## Worked Examples

### Example 1

Input:

```
3
```

The algorithm computes:

| Variable | Value |
| --- | --- |
| n | 3 |
| exponent | 2 |
| result | 9 |

Output:

```
9
```

This demonstrates the recursive tripling pattern:

$$f(3)=3^2=9$$

The uncovered regions after each level form three copies of the previous configuration.

### Example 2

Input:

```
1
```

| Variable | Value |
| --- | --- |
| n | 1 |
| exponent | 0 |
| result | 1 |

Output:

```
1
```

The board is `2 × 2`. A single size-2 cookie covers three cells, leaving exactly one uncovered cell.

### Example 3

Input:

```
0
```

| Variable | Value |
| --- | --- |
| n | 0 |
| special case triggered | yes |
| result | 1 |

Output:

```
1
```

This trace confirms the boundary condition where no cookie can be placed at all.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Fast modular exponentiation |
| Space | O(1) | Only a few integer variables are stored |

Even though the board size grows exponentially, the solution never constructs the board. The algorithm only computes one modular power, so it easily fits within the limits for `n = 1000`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 10**6 + 3

def solve():
    input = sys.stdin.readline

    n = int(input())

    if n == 0:
        print(1)
    else:
        print(pow(3, n - 1, MOD))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("3\n") == "9\n", "sample 1"

# minimum size
assert run("0\n") == "1\n", "n = 0"

# smallest non-trivial board
assert run("1\n") == "1\n", "single size-2 cookie"

# small recursive case
assert run("2\n") == "3\n", "tripling starts"

# larger value
assert run("5\n") == "81\n", "3^(5-1)"

# maximum boundary style test
expected = str(pow(3, 999, MOD)) + "\n"
assert run("1000\n") == expected, "large exponent modulo"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1` | No cookie fits |
| `1` | `1` | Smallest valid cookie placement |
| `2` | `3` | First recursive expansion |
| `5` | `81` | Correct exponent formula |
| `1000` | `pow(3,999,MOD)` | Large modular exponentiation |

## Edge Cases

The first important edge case is the smallest possible board.

Input:

```
0
```

The board size is:

$$2^0 = 1$$

So the board contains exactly one cell. Since cookies of size `1` do not exist, nothing can be placed.

The algorithm immediately triggers the special-case branch and prints:

```
1
```

Without this branch, the formula `3^{n-1}` would incorrectly require computing `3^{-1}`.

The second edge case is the first board where placement becomes possible.

Input:

```
1
```

The board size is `2 × 2`. The greedy process places one size-2 cookie:

$$\frac{2(2+1)}{2}=3$$

Three cells are covered and one remains empty.

The algorithm computes:

$$3^{1-1}=3^0=1$$

which matches the actual configuration.

The final important edge case is very large `n`.

Input:

```
1000
```

The board side length becomes `2^{1000}`, which is far beyond explicit computation. The algorithm never constructs the board or any huge arrays. It only evaluates:

$$3^{999} \bmod (10^6+3)$$

using logarithmic-time exponentiation, so it remains fast and memory-efficient.
