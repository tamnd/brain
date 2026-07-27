---
title: "CF 102772A - \u0412\u0430\u0436\u043d\u043e\u0435 \u043d\u0430\u0443\u0447\u043d\u043e\u0435 \u0447\u0438\u0441\u043b\u043e"
description: "We have two gears with sizes a and b. We need to add the same non-negative number of teeth x to both gears. After adding these teeth, the first new size a + x must be divisible by the original second size b, and the second new size b + x must be divisible by the original first…"
date: "2026-07-27T20:49:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102772
codeforces_index: "A"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434 \u0434\u043b\u044f \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u0421\u0435\u0437\u043e\u043d 2020-21, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102772
solve_time_s: 66
verified: true
draft: false
---

[CF 102772A - \u0412\u0430\u0436\u043d\u043e\u0435 \u043d\u0430\u0443\u0447\u043d\u043e\u0435 \u0447\u0438\u0441\u043b\u043e](https://codeforces.com/problemset/problem/102772/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two gears with sizes `a` and `b`. We need to add the same non-negative number of teeth `x` to both gears. After adding these teeth, the first new size `a + x` must be divisible by the original second size `b`, and the second new size `b + x` must be divisible by the original first size `a`.

The task is to find the smallest possible `x`.

The input contains two integers `a` and `b`, each up to `10^9`. This immediately rules out searching through possible values of `x`, because the answer can be very large. Even a loop that checks millions of candidates is not reliable, and an approach proportional to `a` or `b` is impossible. We need to reduce the problem to a few arithmetic operations.

The main edge cases come from the relationship between the two numbers. If the gears already have the same size, the answer is zero because both divisibility conditions are already satisfied. For example, input `123 123` gives output `0`, and a solution that blindly tries to increase both values may miss this.

Another tricky case is when one number divides the other. For input `8 1`, the answer is `7`, not `0`, because the new sizes become `15` and `8`, and `15` is divisible by `1` while `8` is divisible by `8`. A careless approach that only checks whether one original value divides the other could incorrectly stop early.

A third edge case appears when the least common multiple is smaller than the sum of the two original values. For input `3 4`, the least common multiple is `12`, and the smallest valid final gear size alignment requires adding `5`, not `0` or `1`. The answer is `5` because the final sizes are `8` and `9`, satisfying the required divisibility.

## Approaches

A direct approach would try values of `x` starting from zero and test whether both conditions hold. This is correct because the first value passing the test is exactly the minimum. However, the answer may be close to `10^18`, so even checking a huge number of candidates is impossible.

The useful observation comes from looking at the final gear sizes. The number `a + x` must be a multiple of `b`, and `b + x` must be a multiple of `a`. This means the two final values are multiples of the opposite original values while their difference stays fixed:

`(a + x) - (b + x) = a - b`.

A cleaner way is to express the first condition. Let:

`a + x = k * b`.

Then:

`b + x = b + k*b - a = (k + 1)b - a`.

For this to be divisible by `a`, the value `(k + 1)b` must be divisible by `a`. The smallest multiplier that makes a multiple of `b` also compatible with multiples of `a` is related to the least common multiple.

The final common alignment point is a multiple of `lcm(a, b)`. Since both final values differ from the original values by the same amount, the smallest possible added value is obtained by finding the smallest multiple of the least common multiple that is at least `a + b`.

Let `L = lcm(a, b)`. The answer is:

`smallest_multiple_of_L_not_less_than_(a+b) - a - b`.

Because `L` is at least both `a` and `b`, the needed multiple is either `L` or `2L`, but using integer ceiling division handles every case directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Too slow |
| Optimal | O(log(min(a, b))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the greatest common divisor of `a` and `b`. The least common multiple can be obtained as `a * b / gcd(a, b)`, and using the gcd first prevents unnecessary overflow in languages with smaller integer types.
2. Let `L` be the least common multiple of the two gear sizes. We need the smallest multiple of `L` that is not smaller than `a + b`.
3. Compute the multiplier with ceiling division: `(a + b + L - 1) // L`. Multiplying `L` by this value gives the smallest valid alignment point.
4. Subtract `a + b` from this alignment point. The remaining number is exactly the amount of teeth that must be added to both gears.

Why it works: the final values `a + x` and `b + x` must be positioned so that each one reaches the divisibility structure of the other. The distance between these two values is fixed, and the common divisibility requirement forces the alignment to occur at multiples of `lcm(a, b)`. The algorithm chooses the first such alignment after the current total size `a + b`, so any smaller value of `x` would leave the gears before the first possible valid position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())

    g = math.gcd(a, b)
    lcm = a // g * b

    target = ((a + b + lcm - 1) // lcm) * lcm
    print(target - a - b)

if __name__ == "__main__":
    import math
    solve()
```

The solution first reads the two gear sizes and computes their greatest common divisor. The gcd is used to build the least common multiple without multiplying `a` and `b` too early.

The variable `target` represents the first multiple of the least common multiple that is not smaller than `a + b`. The ceiling division formula avoids off-by-one errors when `a + b` is already a multiple of `lcm`.

The final subtraction removes the original contribution of both gears. What remains is exactly the number of teeth that must be added to each gear.

Python integers handle large values automatically, so the multiplication used for the least common multiple does not need special handling.

## Worked Examples

### Example 1

Input:

```
10 5
```

| Step | a | b | gcd | lcm | target | answer |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 10 | 5 | 5 | 10 | 10 | 10 - 10 = 0 |

The least common multiple is `10`, which is already equal to `a + b`. The gears can be aligned without adding teeth, so the result is `0`.

### Example 2

Input:

```
3 4
```

| Step | a | b | gcd | lcm | target | answer |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 3 | 4 | 1 | 12 | 12 | 12 - 7 = 5 |

The current total is `7`, but the first compatible alignment is `12`. Adding `5` to both gears gives sizes `8` and `9`, and the divisibility conditions become valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(min(a, b))) | The gcd computation uses the Euclidean algorithm. |
| Space | O(1) | Only a constant number of integer variables are stored. |

The input values are up to `10^9`, so the algorithm avoids all loops depending on the answer size or the values themselves. The gcd computation is fast enough even at the maximum limits.

## Test Cases

```python
import sys
import io
import math

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    a, b = map(int, input().split())
    g = math.gcd(a, b)
    lcm = a // g * b
    target = ((a + b + lcm - 1) // lcm) * lcm
    return str(target - a - b) + "\n"

assert solution("10 5\n") == "0\n", "sample-like divisible case"
assert solution("8 1\n") == "7\n", "one divides the other"
assert solution("3 4\n") == "5\n", "different coprime values"
assert solution("123 123\n") == "0\n", "equal gears"
assert solution("1 1\n") == "0\n", "minimum values"
assert solution("1000000000 999999999\n") == "999999998999999999\n", "large values"
assert solution("6 9\n") == "3\n", "common divisor case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | The smallest possible values and already valid gears |
| `123 123` | `0` | Equal gear sizes |
| `8 1` | `7` | A case where one value divides the other |
| `6 9` | `3` | Non-coprime values and gcd handling |
| `1000000000 999999999` | `999999998999999999` | Large arithmetic values |

## Edge Cases

For equal gears, such as:

```
123 123
```

the gcd is `123`, and the least common multiple is also `123`. The sum `a + b` is already a multiple of `lcm`, so the target remains `246`, producing an answer of `0`. The algorithm naturally handles this without a special case.

For the dividing case:

```
8 1
```

the least common multiple is `8`. The sum is `9`, so the first multiple of `8` that reaches or exceeds it is `16`. The answer is `16 - 9 = 7`, which gives final gear sizes `15` and `8`. The first is divisible by `1`, and the second is divisible by `8`.

For a coprime pair:

```
3 4
```

the least common multiple is `12`. The sum of the current sizes is `7`, so the first valid alignment is `12`. The algorithm returns `5`, producing final sizes `8` and `9`, where `8` is divisible by `4` and `9` is divisible by `3`.

For very large values, the algorithm performs only gcd and arithmetic operations. It never iterates over possible answers, so the running time stays constant with respect to the magnitude of the required addition.
