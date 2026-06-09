---
title: "CF 2020C - Bitwise Balancing"
description: "We are given three non-negative integers b, c, and d. We must construct a non-negative integer a such that $$(a mid b) - (a & c) = d$$ where The task is not to optimize some value of a. Any valid a is acceptable. If no such value exists, we print -1."
date: "2026-06-08T12:47:39+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "hashing", "implementation", "math", "schedules", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 2020
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 976 (Div. 2) and Divide By Zero 9.0"
rating: 1400
weight: 2020
solve_time_s: 130
verified: false
draft: false
---

[CF 2020C - Bitwise Balancing](https://codeforces.com/problemset/problem/2020/C)

**Rating:** 1400  
**Tags:** bitmasks, hashing, implementation, math, schedules, ternary search  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given three non-negative integers `b`, `c`, and `d`. We must construct a non-negative integer `a` such that

$$(a \mid b) - (a \& c) = d$$

where `|` is bitwise OR and `&` is bitwise AND.

The task is not to optimize some value of `a`. Any valid `a` is acceptable. If no such value exists, we print `-1`.

The first observation comes from the size of the numbers. Each value can be as large as $10^{18}$, which means up to about 60 binary bits are relevant. There can be as many as $10^5$ test cases, so a solution that spends even a few thousand operations per test case is fine, but anything depending on the magnitude of the numbers themselves is impossible.

A brute-force search over possible values of `a` is immediately ruled out. The allowed range reaches $2^{61}$, which is roughly $2.3 \times 10^{18}$.

The tricky part is the subtraction. Many bitwise problems can be solved independently bit by bit, but subtraction normally introduces borrows between neighboring bits. A careless solution that treats every bit independently without considering borrows would be incorrect in general.

The key edge cases come from combinations of bits that force contradictions.

Consider:

```
b = 0, c = 0, d = 1
```

Then the equation becomes

$$a - 0 = 1$$

so the answer is `a = 1`.

A solution that does not correctly reconstruct bits of `a` would miss this trivial case.

Another important case is:

```
b = 1, c = 0, d = 0
```

For bit 0, `(a|1)` is always `1`, while `(a&0)` is always `0`. The left side is always at least `1`, so no solution exists. The correct output is `-1`.

A third source of bugs is forgetting that subtraction may generate a borrow.

For example:

```
b = 0, c = 1, d = 1
```

If we choose `a = 1`, then

(1|0) - (1&1) = 1 - 1 = 0

not `1`.

The relationship between bits depends on the borrow entering the current position, so we must explicitly track it.

## Approaches

The most direct idea is brute force. Try every possible value of `a`, evaluate

$$(a|b)-(a\&c)$$

and check whether it equals `d`.

This is obviously correct because it examines every candidate. The problem is the search space. `a` may be as large as $2^{61}$, so the worst case requires more than $2 \times 10^{18}$ evaluations. Even at a billion operations per second, that would take decades.

The structure of the expression suggests a bitwise approach. Both OR and AND operate independently on each bit. The only operation coupling different bit positions is the subtraction.

Let

$$X = a|b$$

and

$$Y = a\&c$$

The equation becomes

$$X - Y = d.$$

When performing binary subtraction, the only information that flows from one bit to the next is the borrow. That means we can process bits from least significant to most significant while maintaining a single state: the incoming borrow.

For each bit position we know:

- bit of `b`
- bit of `c`
- bit of `d`
- current borrow

The unknown is the bit of `a`.

Trying both possibilities (`0` or `1`) is enough. For each choice we can compute the corresponding bits of `X` and `Y`, perform one step of binary subtraction, and check whether the produced bit matches the target bit in `d`.

This turns the problem into a tiny dynamic process with only two borrow states, `0` and `1`. Since we process at most 61 bits, the work per test case is constant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{61})$ | $O(1)$ | Too slow |
| Optimal | $O(61)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Initialize `a = 0` and `borrow = 0`.
2. Process bit positions from `0` through `60`.
3. Extract the current bits:

$$b_i,\ c_i,\ d_i$$

from `b`, `c`, and `d`.
4. Try both possible values for the current bit of `a`, namely `0` and `1`.
5. For a candidate bit `a_i`, compute:

$$x_i = a_i \mid b_i$$

and

$$y_i = a_i \& c_i$$
6. Simulate one step of binary subtraction:

$$x_i - y_i - borrow$$

If the value is non-negative, the resulting bit is that value and the next borrow is `0`.

Otherwise add `2` to the value and set the next borrow to `1`.
7. Check whether the resulting bit equals `d_i`.

If it matches, this choice of `a_i` is consistent with the equation. Store the bit in the answer, update the borrow, and continue to the next position.
8. If neither `a_i = 0` nor `a_i = 1` produces the required bit, no solution exists. Output `-1`.
9. After all bits are processed, verify that the final borrow is zero. A remaining borrow would mean the subtraction result does not equal `d`.
10. Output the constructed value of `a`.

### Why it works

At every bit position, binary subtraction depends only on three values: the current bit of the minuend, the current bit of the subtrahend, and the borrow entering that position.

The algorithm explicitly enumerates the only two possibilities for the unknown bit `a_i`. Whenever a choice reproduces the required bit of `d`, it preserves the possibility of a valid global solution because all information needed by higher bits is summarized by the outgoing borrow.

The borrow acts as the complete state of the subtraction process. Since every processed bit matches the corresponding bit of `d`, and the final borrow is zero, the reconstructed number satisfies

$$(a|b)-(a\&c)=d.$$

If at some position no choice of `a_i` can produce the required bit, then no valid continuation exists, so reporting `-1` is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        b, c, d = map(int, input().split())

        a = 0
        borrow = 0
        ok = True

        for i in range(61):
            bi = (b >> i) & 1
            ci = (c >> i) & 1
            di = (d >> i) & 1

            found = False

            for ai in (0, 1):
                xi = ai | bi
                yi = ai & ci

                cur = xi - yi - borrow

                if cur >= 0:
                    bit = cur
                    nb = 0
                else:
                    bit = cur + 2
                    nb = 1

                if bit == di:
                    found = True
                    borrow = nb

                    if ai:
                        a |= (1 << i)

                    break

            if not found:
                ok = False
                break

        if borrow:
            ok = False

        ans.append(str(a if ok else -1))

    sys.stdout.write("\n".join(ans))

solve()
```

The solution follows the subtraction process exactly.

The variable `borrow` stores the borrow entering the current bit. For every bit position we test both possible values of `a_i`.

The expressions

```
xi = ai | bi
yi = ai & ci
```

represent the corresponding bits of `(a|b)` and `(a&c)`.

The subtraction step is performed exactly as binary arithmetic does it. If the local value becomes negative, we borrow from the next bit, add `2` to the current position, and record an outgoing borrow of `1`.

A subtle point is the processing range. The problem guarantees that a valid answer lies within `[0, 2^61]`, so checking bits `0..60` is sufficient. All inputs are below `2^60`, and any borrow propagation that would require a higher bit is detected by the final `borrow` check.

Another subtle detail is that we immediately commit to the first valid choice. For every state `(bit position, incoming borrow)` there is at most one continuation needed. The borrow completely summarizes all previous decisions, so no additional backtracking is required.

## Worked Examples

### Example 1

Input:

```
b = 2
c = 2
d = 2
```

Binary representations:

```
b = 10
c = 10
d = 10
```

| Bit | bi | ci | di | Borrow In | Chosen ai | Borrow Out |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 |

The constructed answer is:

```
a = 0
```

Checking:

$$(0|2)-(0\&2)=2-0=2$$

This example shows that choosing `a_i = 0` can already satisfy the equation without needing any set bits in `a`.

### Example 2

Input:

```
b = 10
c = 2
d = 14
```

Binary:

```
b = 1010
c = 0010
d = 1110
```

| Bit | bi | ci | di | Borrow In | Chosen ai | Borrow Out |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 1 | 0 | 1 | 0 |
| 3 | 1 | 0 | 1 | 0 | 1 | 0 |

The constructed value is:

```
a = 1100₂ = 12
```

Verification:

$$(12|10)=14$$

$$(12\&2)=0$$

$$14-0=14$$

This trace demonstrates how the algorithm reconstructs the answer one bit at a time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(61)$ | Each of 61 bits tries at most two values |
| Space | $O(1)$ | Only a few integer variables are stored |

Since 61 is a constant, the running time is effectively linear in the number of test cases. Even with $10^5$ test cases, the total work is only a few million elementary operations, which easily fits within the limits.

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
        b, c, d = map(int, input().split())

        a = 0
        borrow = 0
        ok = True

        for i in range(61):
            bi = (b >> i) & 1
            ci = (c >> i) & 1
            di = (d >> i) & 1

            found = False

            for ai in (0, 1):
                xi = ai | bi
                yi = ai & ci

                cur = xi - yi - borrow

                if cur >= 0:
                    bit = cur
                    nb = 0
                else:
                    bit = cur + 2
                    nb = 1

                if bit == di:
                    found = True
                    borrow = nb

                    if ai:
                        a |= (1 << i)

                    break

            if not found:
                ok = False
                break

        if borrow:
            ok = False

        out.append(str(a if ok else -1))

    return "\n".join(out)

# provided samples
assert run("3\n2 2 2\n4 2 6\n10 2 14\n") == "0\n-1\n12"

# minimum values
assert run("1\n0 0 0\n") == "0"

# simple solvable case
assert run("1\n0 0 1\n") == "1"

# impossible case
assert run("1\n1 0 0\n") == "-1"

# large boundary value
assert run(f"1\n{(1<<60)-1} 0 {(1<<60)-1}\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0` | `0` | Smallest possible values |
| `0 0 1` | `1` | Reconstruction of a single set bit |
| `1 0 0` | `-1` | Detecting impossible configurations |
| `(2^60-1) 0 (2^60-1)` | `0` | Correct handling of very large values |
| Sample input | Sample output | General correctness |

## Edge Cases

Consider:

```
1
1 0 0
`
```

At bit 0 we have:

```
bi = 1
c
```
