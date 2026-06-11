---
title: "CF 1141A - Game 23"
description: "We start with a number and want to reach a larger target number. The only allowed operation is multiplying the current value by 2 or by 3. The task is to determine how many operations are needed, or report that the transformation cannot be done."
date: "2026-06-12T03:41:05+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1141
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 547 (Div. 3)"
rating: 1000
weight: 1141
solve_time_s: 95
verified: true
draft: false
---

[CF 1141A - Game 23](https://codeforces.com/problemset/problem/1141/A)

**Rating:** 1000  
**Tags:** implementation, math  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a number and want to reach a larger target number. The only allowed operation is multiplying the current value by `2` or by `3`. The task is to determine how many operations are needed, or report that the transformation cannot be done.

A useful way to think about the process is to look at what changes between the starting value and the target value. Every move only introduces additional factors of `2` or `3`. Nothing else can ever appear. If the target contains any extra prime factor besides `2` and `3`, relative to the starting number, the transformation is impossible.

The numbers are at most `5 × 10^8`, which is small enough that repeated division by `2` and `3` is extremely cheap. Even in the worst case, a number below `5 × 10^8` contains fewer than thirty factors of `2` and fewer than twenty factors of `3`, so a simple loop is more than sufficient.

Several edge cases deserve attention.

Suppose the starting and target values are already equal.

Input:

```
10 10
```

Output:

```
0
```

No operations are needed. A solution that always performs at least one multiplication would fail here.

Suppose the target is not a multiple of the starting value.

Input:

```
48 72
```

Output:

```
-1
```

Since every operation only multiplies the current value, we can never decrease or remove factors. If `m` is not divisible by `n`, reaching it is impossible.

Suppose the ratio contains a prime factor other than `2` or `3`.

Input:

```
4 20
```

Output:

```
-1
```

The ratio is `20 / 4 = 5`. Multiplying by `2` and `3` can never create a factor of `5`.

## Approaches

A brute-force viewpoint is to treat each number as a state and repeatedly try multiplying by `2` and `3` until reaching the target. A breadth-first search would eventually find the answer because every edge represents one move.

The problem is that the numeric range is large. Even though the target is only `5 × 10^8`, exploring all reachable states is unnecessary work. The state graph grows exponentially with the number of moves, and a generic search is far more complicated than needed.

The key observation is that every valid sequence of operations multiplies the starting number by some combination of powers of `2` and `3`.

If

$$m = n \cdot 2^a \cdot 3^b,$$

then exactly `a + b` moves are required. Each multiplication by `2` contributes one factor of `2`, and each multiplication by `3` contributes one factor of `3`.

This immediately reduces the problem to analyzing the ratio

$$r = \frac{m}{n}.$$

If `m` is not divisible by `n`, there is no solution.

Otherwise, repeatedly divide `r` by `2` while possible and count how many times it happens. Then do the same for `3`. If anything remains besides `1`, the ratio contained some other prime factor, making the transformation impossible. If the remaining value is `1`, the answer is simply the total number of divisions performed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of moves | Exponential | Too slow |
| Optimal | O(log(m/n)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`.
2. Check whether `m` is divisible by `n`.

If not, output `-1` because multiplication can never remove factors already present in the target ratio.
3. Compute `r = m // n`.

This ratio represents everything that must be added through multiplications by `2` and `3`.
4. Initialize `moves = 0`.
5. While `r` is divisible by `2`, divide it by `2` and increment `moves`.

Each division corresponds to one multiplication by `2` in the forward process.
6. While `r` is divisible by `3`, divide it by `3` and increment `moves`.

Each division corresponds to one multiplication by `3`.
7. Check the remaining value of `r`.

If `r != 1`, some prime factor other than `2` or `3` remains, so output `-1`.
8. Otherwise output `moves`.

### Why it works

The ratio `m / n` captures exactly the multiplicative change needed to reach the target. Every allowed operation contributes one factor of either `2` or `3`, so any reachable ratio must have the form `2^a 3^b`.

The algorithm removes all factors of `2` and `3` from the ratio. If nothing remains, then the ratio is exactly `2^a 3^b`, and `a + b` operations are both necessary and sufficient. If some factor remains, it can never be created using the allowed operations, making the transformation impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    if m % n != 0:
        print(-1)
        return

    r = m // n
    moves = 0

    while r % 2 == 0:
        r //= 2
        moves += 1

    while r % 3 == 0:
        r //= 3
        moves += 1

    if r != 1:
        print(-1)
    else:
        print(moves)

solve()
```

The first check verifies that the target is a multiple of the starting value. Without this condition, integer division would hide impossible cases.

The variable `r` stores the ratio that still needs to be explained by allowed operations. Every time we divide by `2` or `3`, we count one corresponding move.

The final check is crucial. After removing all factors of `2` and `3`, the remaining value must be exactly `1`. If it is not, some forbidden prime factor remains. Missing this check would incorrectly accept cases such as `4 → 20`, where the ratio is `5`.

All arithmetic stays comfortably within Python integers, and the loops execute only logarithmically many times.

## Worked Examples

### Example 1

Input:

```
120 51840
```

The ratio is:

$$51840 / 120 = 432$$

| Step | r | moves |
| --- | --- | --- |
| Initial | 432 | 0 |
| Divide by 2 | 216 | 1 |
| Divide by 2 | 108 | 2 |
| Divide by 2 | 54 | 3 |
| Divide by 2 | 27 | 4 |
| Divide by 3 | 9 | 5 |
| Divide by 3 | 3 | 6 |
| Divide by 3 | 1 | 7 |

The remaining ratio becomes `1`, so the transformation is possible. The answer is `7`.

### Example 2

Input:

```
10 10
```

| Step | r | moves |
| --- | --- | --- |
| Initial | 1 | 0 |

Neither division loop runs. The ratio is already `1`, so the answer is `0`.

This example shows that equal numbers require no operations and are handled naturally by the algorithm.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(m/n)) | Each iteration removes a factor of 2 or 3 from the ratio |
| Space | O(1) | Only a few integer variables are used |

The ratio decreases by at least a factor of `2` or `3` on every loop iteration, so the total number of iterations is tiny. With values bounded by `5 × 10^8`, the running time is effectively instantaneous and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        n, m = map(int, input().split())

        if m % n != 0:
            print(-1)
            return

        r = m // n
        moves = 0

        while r % 2 == 0:
            r //= 2
            moves += 1

        while r % 3 == 0:
            r //= 3
            moves += 1

        print(moves if r == 1 else -1)

    solve()
    return sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""

# provided sample
assert run("120 51840\n").strip() == "7", "sample 1"

# custom cases
assert run("1 1\n").strip() == "0", "equal values"
assert run("48 72\n").strip() == "-1", "ratio contains forbidden factor"
assert run("4 20\n").strip() == "-1", "factor 5 remains"
assert run("1 268435456\n").strip() == "28", "large power of 2"
assert run("9 162\n").strip() == "2", "one factor 2 and one factor 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | No moves needed |
| `48 72` | `-1` | Ratio contains a forbidden factor |
| `4 20` | `-1` | Remaining factor after removing 2s and 3s |
| `1 268435456` | `28` | Large power of 2 |
| `9 162` | `2` | Mixed factors of 2 and 3 |

## Edge Cases

Consider the case where the numbers are already equal.

Input:

```
10 10
```

The ratio is `1`. Neither division loop executes. The algorithm reaches the final check with `r = 1` and outputs `0`. This correctly reflects that no operations are needed.

Consider a target that is not divisible by the starting value.

Input:

```
48 72
```

The first check computes `72 % 48`, which is not zero. The algorithm immediately outputs `-1`. Any sequence of multiplications preserves divisibility by the original value, so reaching `72` from `48` is impossible.

Consider a ratio containing another prime factor.

Input:

```
4 20
```

The ratio is `5`. It is not divisible by `2` or `3`, so neither loop runs. The remaining value is still `5`, not `1`, and the algorithm outputs `-1`. This correctly rejects transformations that would require introducing a factor other than `2` or `3`.
