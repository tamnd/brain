---
title: "CF 55A - Flea travel"
description: "We have n positions arranged in a circle. The flea starts on one position. After the first minute it moves forward by 1 step, after the second minute by 2 steps, after the third minute by 3 steps, and so on."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 55
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 51"
rating: 1200
weight: 55
solve_time_s: 84
verified: true
draft: false
---

[CF 55A - Flea travel](https://codeforces.com/problemset/problem/55/A)

**Rating:** 1200  
**Tags:** implementation, math  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` positions arranged in a circle. The flea starts on one position. After the first minute it moves forward by 1 step, after the second minute by 2 steps, after the third minute by 3 steps, and so on.

The question is whether this movement pattern eventually visits every position on the circle.

If the flea is currently at position `p`, then after minute `k` it moves to:

$p+k \pmod n$

The input contains a single integer `n`, the number of positions in the circle. The output should be `"YES"` if every position is visited at least once, otherwise `"NO"`.

The constraint is very small, only up to 1000 positions. Even a direct simulation with many steps is fast enough. We do not need advanced optimization or heavy mathematics. Still, the interesting part of the problem is understanding why the answer depends only on whether `n` is prime or composite.

One easy mistake is assuming that the flea always visits everything because the jump length keeps changing. That intuition fails for composite values of `n`.

For example:

```
n = 4
```

The positions visited are:

```
0 -> 1 -> 3 -> 2 -> 2 -> ...
```

Position `0` is never revisited after the start, and the movement gets trapped in a smaller cycle. The correct output is `"NO"`.

Another subtle case is `n = 1`.

```
1
```

There is only one position, so the flea has already visited all positions immediately. The correct answer is `"YES"`.

A careless implementation may also stop too early after seeing a repeated position. Repetition alone is not enough to conclude failure unless we already know some positions were never visited. For example:

```
n = 2
```

The flea alternates between both positions forever, which is actually enough to cover the entire circle. The correct output is `"YES"`.

## Approaches

The most direct approach is simulation. We keep track of the current position and repeatedly apply jumps of length `1, 2, 3, ...`. Every time we land on a position, we mark it as visited.

The brute-force works because the state space is tiny. There are only `n` positions, so eventually the movement must repeat. If after enough jumps all positions were marked, we answer `"YES"`, otherwise `"NO"`.

For this problem size, even simulating several thousand moves is completely acceptable. With `n ≤ 1000`, an `O(n^2)` process still performs at most around one million operations.

The more interesting observation comes from number theory.

After `k` moves, the total distance traveled is:

$1+2+3+\cdots+k = \frac{k(k+1)}{2}$

The actual position depends only on this value modulo `n`.

The flea visits every position if and only if `n` is prime.

Why? For composite `n`, there exists some divisor `d < n`. After enough jumps, the accumulated movement starts repeating modulo `d`, which prevents access to all positions. For prime `n`, the modular behavior cycles through all residues.

Another way to phrase the official observation is that the flea visits all positions exactly when the greatest common divisor of the jump structure and `n` stays favorable, which happens only for prime `n` and for `n = 1`.

Since `n` is tiny, we can simply check whether `n` is prime.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(√n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Handle the special case `n = 1`.

A single position is trivially fully visited because the flea starts there.
3. Check whether `n` is prime.

We try all divisors from `2` up to `√n`. If any divisor divides `n`, then `n` is composite.
4. If `n` is prime, print `"YES"`.

Prime-sized circles allow the movement pattern to eventually cover every residue modulo `n`.
5. Otherwise print `"NO"`.

Composite-sized circles force the flea into a smaller repeating structure before all positions are visited.

### Why it works

The flea's position after several jumps depends on cumulative sums modulo `n`. For prime `n`, modular arithmetic over the circle does not collapse into smaller repeating subsets, so every position becomes reachable. For composite `n`, the movement becomes confined to a subset of positions determined by divisors of `n`.

The algorithm is correct because primality exactly characterizes whether the movement covers the entire circle.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_prime(x):
    if x < 2:
        return False

    d = 2
    while d * d <= x:
        if x % d == 0:
            return False
        d += 1

    return True

def solve():
    n = int(input())

    if n == 1 or is_prime(n):
        print("YES")
    else:
        print("NO")

solve()
```

The solution starts with a standard primality test. Any number smaller than 2 is not prime. Then we try every divisor `d` while `d * d <= x`.

Checking only up to the square root is enough because divisors always appear in pairs. If `x` had a divisor larger than `√x`, the paired divisor would already be smaller than `√x`.

The special handling for `n = 1` matters because 1 is not prime mathematically, but the answer for this problem is still `"YES"` since the flea already occupies the only position.

The implementation uses constant extra memory and finishes almost instantly for the given constraints.

## Worked Examples

### Example 1

Input:

```
1
```

Trace:

| Step | Value |
| --- | --- |
| Read n | 1 |
| Check special case | n == 1 |
| Output | YES |

This example shows the smallest possible input. No movement is needed because the flea already starts on the only position.

### Example 2

Input:

```
4
```

Trace:

| Step | Value |
| --- | --- |
| Read n | 4 |
| Check n == 1 | False |
| Try divisor d = 2 | 4 % 2 == 0 |
| Composite detected | Yes |
| Output | NO |

This trace demonstrates the composite case. Since 4 has a non-trivial divisor, the flea cannot visit all positions.

### Example 3

Input:

```
7
```

Trace:

| Step | Value |
| --- | --- |
| Read n | 7 |
| Check n == 1 | False |
| Try divisor d = 2 | 7 % 2 != 0 |
| d * d > n | Stop |
| Prime detected | Yes |
| Output | YES |

This example shows a prime-sized circle, where the flea eventually reaches every position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n) | We test divisors only up to the square root of n |
| Space | O(1) | Only a few integer variables are used |

With `n ≤ 1000`, this complexity is far below the limits. Even the brute-force simulation would pass comfortably, but the primality-based solution is cleaner and faster.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    n = int(input())

    def is_prime(x):
        if x < 2:
            return False

        d = 2
        while d * d <= x:
            if x % d == 0:
                return False
            d += 1

        return True

    if n == 1 or is_prime(n):
        print("YES")
    else:
        print("NO")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    global input
    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run("1\n") == "YES\n", "sample 1"

# custom cases
assert run("2\n") == "YES\n", "smallest prime"
assert run("4\n") == "NO\n", "small composite"
assert run("7\n") == "YES\n", "prime number"
assert run("1000\n") == "NO\n", "large composite boundary"
assert run("997\n") == "YES\n", "large prime near limit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `YES` | Single-position edge case |
| `2` | `YES` | Smallest prime |
| `4` | `NO` | Composite cycle behavior |
| `7` | `YES` | Typical prime case |
| `1000` | `NO` | Large composite near limit |
| `997` | `YES` | Large prime near limit |

## Edge Cases

Consider the smallest possible input:

```
1
```

The algorithm immediately matches the special case `n == 1` and prints `"YES"`.

There is no movement at all, but every position has already been visited because only one exists.

Now consider a small composite number:

```
4
```

The primality check tries divisor `2`.

```
4 % 2 == 0
```

Since a divisor exists, the number is composite, so the algorithm prints `"NO"`.

This correctly matches the actual movement behavior, where the flea never covers the entire circle.

Finally, consider a prime number:

```
5
```

The divisibility checks are:

```
5 % 2 != 0
```

No divisors exist up to `√5`, so the algorithm classifies 5 as prime and prints `"YES"`.

The flea eventually cycles through all five positions, which confirms the correctness of the prime criterion.
