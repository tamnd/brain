---
title: "CF 1328A - Divisibility Problem"
description: "Each test case contains two positive integers. We may only perform one kind of operation: increase the first number by one."
date: "2026-06-11T16:26:34+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1328
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 629 (Div. 3)"
rating: 800
weight: 1328
solve_time_s: 325
verified: false
draft: false
---

[CF 1328A - Divisibility Problem](https://codeforces.com/problemset/problem/1328/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 5m 25s  
**Verified:** no  

## Solution
## Problem Understanding

Each test case contains two positive integers. We may only perform one kind of operation: increase the first number by one. The goal is to reach the nearest value greater than or equal to the current one that is divisible by the second number, while using as few increments as possible.

The input starts with the number of test cases, then each pair of numbers is processed independently. For every pair, we must output how many increments are required before the first number becomes a multiple of the second.

The number of test cases reaches $10^4$, while both numbers can be as large as $10^9$. These limits are small enough for constant-time work per test case, but they rule out any approach that repeatedly adds one until divisibility is achieved. In the worst case, the answer itself can be enormous, so a simulation could require hundreds of millions or even billions of iterations.

Several edge cases deserve attention.

When the first number is already divisible by the second, the answer is zero.

Input:

```
1
92 46
```

Output:

```
0
```

A careless formula such as `b - (a % b)` produces `46`, which is incorrect because no moves are needed.

Another tricky situation appears when the divisor is larger than the current value.

Input:

```
1
123 456
```

Output:

```
333
```

The next multiple of 456 is 456 itself, so we need $456-123=333$ increments.

A very small example can also expose off-by-one errors.

Input:

```
1
10 4
```

Output:

```
2
```

Since $10 \bmod 4 = 2$, two more increments are needed to reach 12. Using an incorrect expression such as `b - a % b - 1` would give 1 instead of 2.

## Approaches

The most straightforward strategy is to repeatedly increase the number by one and stop as soon as it becomes divisible by the divisor. This method is correct because every operation is forced, and stopping at the first divisible value gives the minimum number of moves.

The problem with this approach is its running time. Suppose $a=1$ and $b=10^9$. We would perform $999\,999\,999$ increments before reaching the first multiple of $10^9$. Such a simulation is far too slow.

The key observation is that divisibility depends only on the remainder when dividing by $b$. If the remainder is $r$, then exactly $b-r$ more units are needed to reach the next multiple. The only exception occurs when $r=0$, because the number is already divisible and no operations are required.

The brute-force works because it eventually reaches the next multiple, but fails when the gap is huge. The observation that the remainder already tells us how far we are from that multiple reduces the problem to a few arithmetic operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases and process each pair independently because the cases do not interact.
2. Compute the remainder `a % b`. This tells us how far the current value is from the nearest lower multiple of `b`.
3. If the remainder is zero, output zero because the current value is already divisible.
4. Otherwise, output `b - remainder`. This quantity is exactly the distance from the current value to the next multiple of `b`.

### Why it works

For any integer $a$, we may write

$$a = kb + r,$$

where $0 \le r < b$. If $r=0$, then $a$ itself is a multiple of $b$. Otherwise, the next multiple is

$$(k+1)b = kb + b.$$

The difference between these two values is

$$(k+1)b-a = b-r.$$

No smaller number of increments can work because every intermediate value still has a nonzero remainder. Hence the algorithm always produces the minimum number of moves.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    a, b = map(int, input().split())
    rem = a % b

    if rem == 0:
        print(0)
    else:
        print(b - rem)
```

The program first reads the number of test cases and handles each pair separately.

For every pair, it computes the remainder after dividing `a` by `b`. This remainder determines how far the number is from the previous multiple. If the remainder is zero, the answer is immediately zero.

Otherwise, the distance to the next multiple equals `b - rem`.

The only subtle point is the divisible case. Writing only `b - (a % b)` gives the wrong answer when `a % b` is zero, because it would output `b` instead of `0`. Handling that case separately avoids the off-by-one error.

## Worked Examples

### Example 1

Input:

```
10 4
```

| a | b | a % b | Answer |
| --- | --- | --- | --- |
| 10 | 4 | 2 | 2 |

The remainder is 2, so two increments bring the number to 12, which is divisible by 4. This example shows the normal case where the current value lies between two multiples.

### Example 2

Input:

```
123 456
```

| a | b | a % b | Answer |
| --- | --- | --- | --- |
| 123 | 456 | 123 | 333 |

Since the divisor exceeds the current value, the first reachable multiple is 456 itself. The algorithm correctly computes $456-123=333$.

### Example 3

Input:

```
92 46
```

| a | b | a % b | Answer |
| --- | --- | --- | --- |
| 92 | 46 | 0 | 0 |

This example exercises the special case where the number is already divisible. The answer remains zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations are performed |
| Space | O(1) | No extra data structures are used |

Since there are at most $10^4$ test cases, the total running time is linear in the number of cases. Constant work per case easily fits within the one-second limit, and the memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())

    for _ in range(t):
        a, b = map(int, input().split())
        rem = a % b

        if rem == 0:
            print(0)
        else:
            print(b - rem)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run(
"""5
10 4
13 9
100 13
123 456
92 46
"""
) == """2
5
4
333
0
""", "sample 1"

# minimum values
assert run(
"""1
1 1
"""
) == """0
""", "minimum values"

# maximum values
assert run(
"""1
1000000000 1000000000
"""
) == """0
""", "maximum equal values"

# divisor larger than number
assert run(
"""1
1 1000000000
"""
) == """999999999
""", "large gap"

# off-by-one check
assert run(
"""1
10 4
"""
) == """2
""", "remainder case"

# already divisible
assert run(
"""1
81 9
"""
) == """0
""", "exact multiple"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | Smallest possible values |
| `1000000000 1000000000` | `0` | Maximum equal values |
| `1 1000000000` | `999999999` | Very large answer |
| `10 4` | `2` | Typical remainder case |
| `81 9` | `0` | Already divisible numbers |

## Edge Cases

Consider the case where the number is already divisible.

Input:

```
1
92 46
```

The algorithm computes `92 % 46 = 0`. Since the remainder is zero, it immediately outputs 0. No increments are required, and the special case prevents returning 46 by mistake.

Now consider a divisor larger than the current value.

Input:

```
1
123 456
```

The remainder equals 123. The algorithm computes `456 - 123 = 333`, which means increasing 123 exactly 333 times reaches 456. Any smaller number of increments produces a value below 456 and cannot be divisible by 456.

Finally, consider a case that can expose off-by-one mistakes.

Input:

```
1
10 4
```

The remainder is 2. The algorithm returns `4 - 2 = 2`, meaning the sequence becomes 11 and then 12. After two operations, divisibility is achieved. One operation is insufficient because 11 is not divisible by 4.
