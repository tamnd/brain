---
title: "CF 102535K - Kim Possible and the Mooks"
description: "The line of enemies can be viewed as an array of length n. Each position is either an active enemy, written as MOOK, or an inactive enemy, written as MEEK. Kim always starts from the left end and walks until she reaches the first active enemy."
date: "2026-08-05T15:23:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102535
codeforces_index: "K"
codeforces_contest_name: "2020 UP ACM Algolympics Elimination Round"
rating: 0
weight: 102535
solve_time_s: 71
verified: true
draft: false
---

[CF 102535K - Kim Possible and the Mooks](https://codeforces.com/problemset/problem/102535/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

The line of enemies can be viewed as an array of length `n`. Each position is either an active enemy, written as `MOOK`, or an inactive enemy, written as `MEEK`. Kim always starts from the left end and walks until she reaches the first active enemy. Defeating that enemy costs one minute, after which that position becomes inactive and every inactive position before it becomes active again.

The task is to calculate the total number of minutes until every position becomes `MEEK`.

The constraints are small in terms of `n`, with `n` at most 50, but there can be many test cases, up to 10,000. A simulation that takes time proportional to the number of operations can still be dangerous because the number of operations can grow exponentially with `n`. A 50 position line can represent values around `2^50`, so any approach that literally performs every fight cannot finish. The solution must find a mathematical pattern instead of simulating the battles.

The tricky cases come from the fact that the line does not simply lose one enemy after every fight. For example, an already inactive position can become active again.

Consider:

```
1
MOOK
```

The answer is `1`. A solution that only counts the initial number of `MOOK` positions would work here, but it fails on larger cases because enemies can return.

Another example is:

```
3
MOOK
MEEK
MEEK
```

The answer is also `1`. After defeating the first position, there are no active enemies left. A careless simulation that expects every original `MEEK` to require some work would overcount.

A more revealing example is:

```
3
MEEK
MOOK
MEEK
```

The answer is `2`. The first fight changes the line to:

```
MOOK
MEEK
MEEK
```

The second fight finishes it. The middle enemy caused the enemy at the front to reappear, which is the central behavior of the problem.

## Approaches

A direct solution would keep the current array, find the first `MOOK`, change it into a `MEEK`, turn all previous `MEEK` positions into `MOOK`, and repeat until the array contains only `MEEK`. This exactly follows the process, so it is correct.

The problem is the number of repetitions. The process is actually counting down through a binary number, so the number of fights can be as large as `2^n - 1`. With `n = 50`, the worst case would require more than one quadrillion operations. Even a very efficient simulation cannot handle that.

The useful observation is that each position behaves exactly like a binary digit. Let `MOOK` represent `1` and `MEEK` represent `0`. The first position is the least significant bit. When Kim defeats the first `MOOK`, she finds the first `1` bit and changes it to `0`, while all earlier `0` bits become `1`. This is exactly how subtracting one from a binary number works.

For example, the state

```
MOOK
MEEK
MOOK
```

represents binary digits `101` when read with the left side as the least significant bit. Its value is:

```
1 * 2^0 + 0 * 2^1 + 1 * 2^2 = 5
```

The process performs five fights before reaching zero.

The entire problem reduces to converting the initial arrangement into a binary number where the leftmost position has weight `2^0`, then outputting that value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the line from left to right and treat every `MOOK` as a binary digit `1` and every `MEEK` as a binary digit `0`.

The leftmost enemy is the least significant bit because it is the first position Kim can defeat.
2. Maintain the current binary value while scanning the line. For the position at index `i`, add `2^i` if it contains a `MOOK`.

Each active enemy contributes exactly the number of fights represented by its binary weight.
3. Print the accumulated value.

The value can reach `2^50 - 1`, which fits comfortably inside Python's integer type.

Why it works:

The invariant is that the current enemy line represents the number of fights still required before the process ends. A single fight performs the exact transformation of subtracting one from the binary representation, where the leftmost position is the least significant bit. Since the process stops when the binary number reaches zero, the starting binary value is exactly the number of fights needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        value = 0

        for i in range(n):
            s = input().strip()
            if s == "MOOK":
                value += 1 << i

        ans.append(str(value))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The program processes each test case independently. The variable `value` stores the binary number represented by the line.

The shift operation `1 << i` creates the weight of the position. Since the first input line has index `0` in the code, the first enemy contributes `2^0`, matching the process where the first enemy is the first one Kim can reach.

The solution never simulates fights, so it avoids the exponential number of state changes. Python integers also avoid overflow issues because the largest possible value is below `2^50`.

## Worked Examples

For the sample case:

```
MOOK
MEEK
MEEK
```

the binary value is calculated as follows:

| Index | State | Contribution | Current value |
| --- | --- | --- | --- |
| 0 | MOOK | 2^0 = 1 | 1 |
| 1 | MEEK | 0 | 1 |
| 2 | MEEK | 0 | 1 |

The answer is `1`. This confirms the case where the first enemy is already the only required fight.

For:

```
MOOK
MEEK
MEEK
MOOK
MEEK
MOOK
MEEK
```

the contributions are:

| Index | State | Contribution | Current value |
| --- | --- | --- | --- |
| 0 | MOOK | 1 | 1 |
| 1 | MEEK | 0 | 1 |
| 2 | MEEK | 0 | 1 |
| 3 | MOOK | 8 | 9 |
| 4 | MEEK | 0 | 9 |
| 5 | MOOK | 32 | 41 |
| 6 | MEEK | 0 | 41 |

The output is `41`. The trace shows that separated groups of enemies are not independent, because each position contributes a binary weight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Every enemy position is read once |
| Space | O(1) | Only the accumulated answer is stored |

The total work is at most 500,000 position reads across all test cases, which easily fits the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

def solve():
    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        value = 0
        for i in range(n):
            if input().strip() == "MOOK":
                value += 1 << i
        ans.append(str(value))

    print("\n".join(ans))

assert run("""3
1
MOOK
3
MOOK
MEEK
MEEK
7
MOOK
MEEK
MEEK
MOOK
MEEK
MOOK
MEEK
""") == "1\n1\n41\n"

assert run("""1
1
MEEK
""") == "0\n"

assert run("""1
4
MOOK
MOOK
MOOK
MOOK
""") == "15\n"

assert run("""1
3
MEEK
MOOK
MEEK
""") == "2\n"

assert run("""1
50
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
MOOK
""") == str((1 << 50) - 1) + "\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single `MEEK` | `0` | Already finished state |
| Four `MOOK` values | `15` | All bits set and binary conversion |
| `MEEK, MOOK, MEEK` | `2` | A nonzero middle bit |
| Fifty `MOOK` values | `2^50 - 1` | Maximum size and large integer handling |

## Edge Cases

For the input:

```
1
MOOK
```

the algorithm assigns the only position a weight of `2^0`, giving `1`. This matches the single fight needed.

For the input:

```
3
MOOK
MEEK
MEEK
```

the algorithm ignores the inactive positions and returns `1`. The process ends immediately after the first defeat because no higher binary bits are set.

For the input:

```
3
MEEK
MOOK
MEEK
```

the second position contributes `2^1`, giving `2`. The first fight activates the first position, and the second fight removes it. This confirms that initially inactive positions are not simply empty space, they are binary digits with value zero.

For the maximum case where all 50 positions are `MOOK`, the answer is:

```
1 + 2 + 4 + ... + 2^49 = 2^50 - 1
```

The algorithm handles this directly without performing any of the individual fights.
