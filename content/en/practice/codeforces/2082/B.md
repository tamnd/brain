---
title: "CF 2082B - Floor or Ceil"
description: "We start with an integer value and must perform two kinds of halving operations a fixed number of times. One operation replaces the current value with the floor of half the value. The other replaces it with the ceiling of half the value."
date: "2026-06-09T03:46:20+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2082
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1010 (Div. 2, Unrated)"
rating: 1600
weight: 2082
solve_time_s: 156
verified: false
draft: false
---

[CF 2082B - Floor or Ceil](https://codeforces.com/problemset/problem/2082/B)

**Rating:** 1600  
**Tags:** brute force, greedy  
**Solve time:** 2m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We start with an integer value and must perform two kinds of halving operations a fixed number of times.

One operation replaces the current value with the floor of half the value. The other replaces it with the ceiling of half the value. We must use the floor operation exactly `n` times and the ceiling operation exactly `m` times, but we may choose their order. The task is to find the smallest and largest final value that can be obtained.

The first thing to notice is that both operations behave identically on even numbers:

$$\left\lfloor \frac{x}{2} \right\rfloor = \left\lceil \frac{x}{2} \right\rceil = \frac{x}{2}$$

The only interesting situation occurs when `x` is odd:

$$\left\lfloor \frac{x}{2} \right\rfloor = \frac{x-1}{2}$$

$$\left\lceil \frac{x}{2} \right\rceil = \frac{x+1}{2}$$

On odd values, the floor operation produces a result that is exactly one smaller than the ceiling operation.

The constraints are the real challenge. The values `x`, `n`, and `m` can all be as large as `10^9`, and there are up to `10^4` test cases. Any approach that tries to simulate all `n + m` operations is impossible because a single test case could require two billion operations.

The key observation is that every operation roughly halves the current value. Since `x ≤ 10^9`, after about 30 halvings the value becomes `0` or `1`. Once we reach that point, the remaining operations can be handled analytically. This means the actual amount of work per test case can be reduced to a tiny constant.

Several edge cases are easy to mishandle.

Consider:

```
x = 1, n = 1, m = 100
```

The minimum possible answer is `0`. Applying the floor operation at any time turns `1` into `0`, and after that all operations keep it at `0`. A careless implementation that stops when it reaches `1` would incorrectly return `1`.

Consider:

```
x = 1, n = 0, m = 100
```

The answer is `1`. Ceiling of `1/2` is still `1`, so the value never changes.

Consider:

```
x = 0, n = 10^9, m = 10^9
```

The answer is `0 0`. Both operations leave zero unchanged forever.

These terminal states must be handled separately.

## Approaches

A brute-force solution would try every possible ordering of the operations. Even for small values of `n + m`, the number of possible orders is enormous:

$$\binom{n+m}{n}$$

This grows exponentially and becomes hopeless almost immediately.

A more reasonable brute-force would simulate a chosen order. That still fails because `n + m` may be as large as `2 \cdot 10^9`.

The structure of the operations gives us a much stronger observation. Every operation halves the current value. Starting from at most `10^9`, after roughly 30 steps the value is already reduced to `0` or `1`. From then on, further operations are trivial.

The remaining question is how to choose the order optimally.

When the current value is odd, floor produces a smaller result than ceiling. If we are trying to minimize the final answer, we would like to spend a floor operation on odd numbers whenever possible. If we are trying to maximize the final answer, we would like to spend a ceiling operation on odd numbers whenever possible.

Even numbers are different because both operations give exactly the same next value. Since the result is identical, we should use those moments to consume the operation type that is less useful later.

For minimization, floor operations are valuable because they help on odd numbers. On even numbers we should consume ceiling operations first and save floor operations for future odd values.

For maximization, ceiling operations are valuable because they help on odd numbers. On even numbers we should consume floor operations first and save ceiling operations for future odd values.

This greedy strategy completely determines the optimal sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(log x) | O(1) | Accepted |

## Algorithm Walkthrough

To compute the minimum answer:

1. While `x > 1` and there are still operations remaining, inspect the parity of `x`.
2. If `x` is odd and a floor operation is available, use it.

This gives the smallest possible next value.
3. If `x` is odd and no floor operation remains, use a ceiling operation.
4. If `x` is even, both operations lead to the same next value.

Use a ceiling operation if one exists, because ceiling operations are less useful than floor operations on future odd values.
5. Continue until either all operations are used or `x` becomes `0` or `1`.
6. If `x = 0`, the answer is `0`.
7. If `x = 1`, the answer is `0` if any floor operation remains, otherwise `1`.

To compute the maximum answer:

1. While `x > 1` and operations remain, inspect the parity.
2. If `x` is odd and a ceiling operation is available, use it.

This gives the largest possible next value.
3. If `x` is odd and no ceiling operation remains, use a floor operation.
4. If `x` is even, use a floor operation if possible.

Floor operations are harmless on even values, so we preserve ceiling operations for future odd values.
5. Continue until either all operations are used or `x` becomes `0` or `1`.
6. If `x = 0`, the answer is `0`.
7. If `x = 1`, the answer is `1` only when no floor operations remain. Otherwise some floor must eventually be applied, making the result `0`.

### Why it works

The crucial property is that floor and ceiling differ only on odd numbers.

For the minimum answer, every floor operation used on an odd value decreases the current value by one more than a ceiling operation would. Since all future operations are monotone functions of the current value, having a smaller value now can never hurt a minimization objective. Floor operations are therefore most valuable on odd states, and ceiling operations should be spent on even states whenever possible.

The maximization argument is symmetric. Ceiling operations are most valuable on odd states because they keep the value one larger. Using floor operations on even states preserves those valuable ceiling operations for later.

Since each greedy choice preserves the more useful operation type for the next odd encounter, no alternative ordering can produce a better final result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def get_minimum(x, n, m):
    while x > 1 and (n > 0 or m > 0):
        if x & 1:
            if n > 0:
                x //= 2
                n -= 1
            else:
                x = (x + 1) // 2
                m -= 1
        else:
            if m > 0:
                x //= 2
                m -= 1
            else:
                x //= 2
                n -= 1

    if x == 0:
        return 0
    if x == 1:
        return 0 if n > 0 else 1
    return x

def get_maximum(x, n, m):
    while x > 1 and (n > 0 or m > 0):
        if x & 1:
            if m > 0:
                x = (x + 1) // 2
                m -= 1
            else:
                x //= 2
                n -= 1
        else:
            if n > 0:
                x //= 2
                n -= 1
            else:
                x //= 2
                m -= 1

    if x == 0:
        return 0
    if x == 1:
        return 1 if n == 0 else 0
    return x

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        x, n, m = map(int, input().split())
        mn = get_minimum(x, n, m)
        mx = get_maximum(x, n, m)
        ans.append(f"{mn} {mx}")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The two helper functions implement the two greedy strategies independently.

The loops run only while `x > 1`. Every iteration halves the value, so the number of iterations is at most about 31 for the given constraints. Even when `n` and `m` are one billion, we never simulate anywhere near that many operations.

The terminal handling is the subtle part. Once `x` becomes `1`, the remaining operations matter. A remaining floor operation eventually turns `1` into `0`. Ceiling operations alone leave `1` unchanged. This is why the final logic depends only on whether any floor operations are still available.

No overflow issues exist because the value only decreases.

## Worked Examples

### Example 1

Input:

```
12 1 2
```

Minimum computation:

| x | n | m | Action |
| --- | --- | --- | --- |
| 12 | 1 | 2 | even, use ceil |
| 6 | 1 | 1 | even, use ceil |
| 3 | 1 | 0 | odd, use floor |
| 1 | 0 | 0 | stop |

Result: `1`.

Maximum computation:

| x | n | m | Action |
| --- | --- | --- | --- |
| 12 | 1 | 2 | even, use floor |
| 6 | 0 | 2 | even, use ceil |
| 3 | 0 | 1 | odd, use ceil |
| 2 | 0 | 0 | stop |

Result: `2`.

This example shows why consuming the less valuable operation type on even numbers matters.

### Example 2

Input:

```
706636307 0 3
```

Both minimum and maximum behave identically because only ceiling operations exist.

| x | n | m | Action |
| --- | --- | --- | --- |
| 706636307 | 0 | 3 | odd, ceil |
| 353318154 | 0 | 2 | even, ceil |
| 176659077 | 0 | 1 | odd, ceil |
| 88329539 | 0 | 0 | stop |

Result:

```
88329539 88329539
```

This demonstrates that when only one operation type remains, the ordering question disappears.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log x) | Each step halves the current value |
| Space | O(1) | Only a few variables are stored |

Since `x ≤ 10^9`, `log2(x)` is at most about 30. With at most `10^4` test cases, the total work is only a few hundred thousand operations, comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    def get_minimum(x, n, m):
        while x > 1 and (n > 0 or m > 0):
            if x & 1:
                if n:
                    x //= 2
                    n -= 1
                else:
                    x = (x + 1) // 2
                    m -= 1
            else:
                if m:
                    x //= 2
                    m -= 1
                else:
                    x //= 2
                    n -= 1

        if x == 0:
            return 0
        if x == 1:
            return 0 if n > 0 else 1
        return x

    def get_maximum(x, n, m):
        while x > 1 and (n > 0 or m > 0):
            if x & 1:
                if m:
                    x = (x + 1) // 2
                    m -= 1
                else:
                    x //= 2
                    n -= 1
            else:
                if n:
                    x //= 2
                    n -= 1
                else:
                    x //= 2
                    m -= 1

        if x == 0:
            return 0
        if x == 1:
            return 1 if n == 0 else 0
        return x

    t = int(input())
    out = []
    for _ in range(t):
        x, n, m = map(int, input().split())
        out.append(f"{get_minimum(x,n,m)} {get_maximum(x,n,m)}")
    print("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    res = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return res

# provided sample
assert run(
"""5
12 1 2
12 1 1
12 0 0
12 1000000000 1000000000
706636307 0 3
"""
) == "\n".join([
"1 2",
"3 3",
"12 12",
"0 0",
"88329539 88329539"
])

# custom cases
assert run("1\n0 100 100\n") == "0 0", "zero stays zero"
assert run("1\n1 1 100\n") == "0 0", "remaining floor kills one"
assert run("1\n1 0 100\n") == "1 1", "only ceilings keep one"
assert run("1\n3 1 0\n") == "1 1", "single odd floor"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 100 100` | `0 0` | Zero is an absorbing state |
| `1 1 100` | `0 0` | Any remaining floor eventually reaches zero |
| `1 0 100` | `1 1` | Ceilings alone never change one |
| `3 1 0` | `1 1` | Basic odd floor behavior |

## Edge Cases

Consider:

```
1
1 1 100
```

The simulation immediately reaches the terminal state `x = 1`. The minimum logic checks whether any floor operation remains. Since `n = 1`, the answer becomes `0`. The maximum logic reaches the same conclusion because a floor must eventually be used. The output is:

```
0 0
```

Consider:

```
1
1 0 100
```

No floor operations exist. Ceiling of `1/2` is still `1`, so every remaining operation leaves the value unchanged. Both answers are:

```
1 1
```

Consider:

```
1
0 1000000000 1000000000
```

The algorithm never enters the main loop because `x = 0`. The terminal check returns `0` immediately. The output is:

```
0 0
```

Consider:

```
1
12 1000000000 1000000000
```

The value reaches `0` after only a handful of halvings. The algorithm does not attempt to simulate billions of operations. Once `x = 0`, the answer is fixed at `0`, which is exactly the behavior required for the largest constraints.
