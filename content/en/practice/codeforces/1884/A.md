---
title: "CF 1884A - Simple Design"
description: "For each test case, we are given a starting number x and an integer k. A number is considered beautiful if the sum of its decimal digits is divisible by k. The task is to find the smallest integer y such that y ≥ x and the digit sum of y is divisible by k."
date: "2026-06-08T22:22:58+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1884
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 904 (Div. 2)"
rating: 800
weight: 1884
solve_time_s: 104
verified: true
draft: false
---

[CF 1884A - Simple Design](https://codeforces.com/problemset/problem/1884/A)

**Rating:** 800  
**Tags:** brute force, greedy, math  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we are given a starting number `x` and an integer `k`. A number is considered beautiful if the sum of its decimal digits is divisible by `k`.

The task is to find the smallest integer `y` such that `y ≥ x` and the digit sum of `y` is divisible by `k`.

The constraints are surprisingly small from an algorithmic perspective. The value of `x` can reach `10^9`, but `k` is at most `10`. The number of test cases can be as large as `10^4`, so the solution for a single test case should be extremely cheap.

The key observation from the constraints is that digit sums are small. Even for numbers around `10^9`, the digit sum is at most `9 × 10 = 90`. Since `k ≤ 10`, we do not need to search very far before finding a valid answer. This makes a direct search practical.

One easy mistake is assuming the answer must be strictly larger than `x`. Consider:

```
x = 777, k = 3
```

The digit sum is `7 + 7 + 7 = 21`, which is already divisible by `3`. The correct answer is:

```
777
```

Another common mistake is checking divisibility of the number itself instead of its digit sum. For example:

```
x = 17, k = 8
```

The number `17` is not divisible by `8`, but its digit sum is `1 + 7 = 8`, which is divisible by `8`. The correct answer is:

```
17
```

A third subtle case occurs when several consecutive numbers fail before the first valid one appears.

```
x = 1, k = 10
```

Digit sums are:

```
1 -> 1
2 -> 2
...
18 -> 9
19 -> 10
```

The answer is:

```
19
```

A careless implementation that only checks a few nearby numbers could miss the first valid candidate.

## Approaches

The most direct approach is to start from `x` and repeatedly test numbers one by one.

For a candidate number `cur`, compute its digit sum. If that sum is divisible by `k`, we have found the smallest valid answer because we checked numbers in increasing order. Otherwise, increment `cur` and continue.

Brute force is correct because every number greater than or equal to `x` is examined in order, and the first beautiful number encountered must be the smallest possible answer.

Normally, linear searching over integers would be dangerous. If the gap between valid answers could be very large, the worst-case running time would become unacceptable.

The crucial observation is that `k ≤ 10`. The digit sum changes frequently, and among any reasonably small range of numbers we will encounter a digit sum divisible by any value from `1` to `10`. In practice, the search never travels far. This is exactly the intended solution for the problem.

Computing a digit sum takes only a few operations because the numbers have at most ten digits. Even with `10^4` test cases, the total work is tiny.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search | O(g · d) | O(1) | Accepted |
| Optimal (same observation) | O(g · d) | O(1) | Accepted |

Here `g` is the number of checked candidates until the answer is found, and `d` is the number of digits. Since `k ≤ 10`, `g` remains very small.

## Algorithm Walkthrough

1. Read `x` and `k`.
2. Set `cur = x`.
3. Compute the sum of digits of `cur`.
4. If the digit sum is divisible by `k`, output `cur` and stop processing this test case.
5. Otherwise increase `cur` by one.
6. Repeat from step 3.

The search proceeds in increasing numerical order. The first valid number encountered is automatically the smallest valid answer.

### Why it works

At every iteration, all integers from `x` through `cur - 1` have already been checked and rejected because their digit sums are not divisible by `k`.

When the algorithm stops at some value `cur`, its digit sum is divisible by `k`. Since every smaller number greater than or equal to `x` was already examined and found invalid, no smaller valid answer exists. Thus `cur` is exactly the smallest beautiful number not less than `x`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def digit_sum(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s

t = int(input())

for _ in range(t):
    x, k = map(int, input().split())

    cur = x
    while True:
        if digit_sum(cur) % k == 0:
            print(cur)
            break
        cur += 1
```

The helper function computes the digit sum using repeated modulo and division operations. This avoids converting the number to a string, although either method would be fast enough.

For each test case, the program starts at `x` and checks candidates one by one. The loop terminates as soon as a digit sum divisible by `k` is found.

A subtle boundary condition is when `x` itself is already beautiful. The algorithm handles this naturally because `cur` starts at `x`, so the first check includes the starting number.

There are no overflow concerns because Python integers are unbounded, and the problem values are already very small by competitive programming standards.

## Worked Examples

### Example 1

Input:

```
x = 10, k = 8
```

| Current Number | Digit Sum | Digit Sum % 8 | Action |
| --- | --- | --- | --- |
| 10 | 1 | 1 | Continue |
| 11 | 2 | 2 | Continue |
| 12 | 3 | 3 | Continue |
| 13 | 4 | 4 | Continue |
| 14 | 5 | 5 | Continue |
| 15 | 6 | 6 | Continue |
| 16 | 7 | 7 | Continue |
| 17 | 8 | 0 | Stop |

Output:

```
17
```

This example shows that the number itself is irrelevant. Only the digit sum matters.

### Example 2

Input:

```
x = 1235, k = 10
```

| Current Number | Digit Sum | Digit Sum % 10 | Action |
| --- | --- | --- | --- |
| 1235 | 11 | 1 | Continue |
| 1236 | 12 | 2 | Continue |
| 1237 | 13 | 3 | Continue |
| 1238 | 14 | 4 | Continue |
| 1239 | 15 | 5 | Continue |
| 1240 | 7 | 7 | Continue |
| 1241 | 8 | 8 | Continue |
| 1242 | 9 | 9 | Continue |
| 1243 | 10 | 0 | Stop |

Output:

```
1243
```

This trace demonstrates why checking numbers sequentially is necessary. Carry operations can dramatically change the digit sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(g · d) | `g` candidates checked, `d` digits per digit-sum computation |
| Space | O(1) | Only a few integer variables are stored |

The numbers contain at most ten digits, so `d` is effectively constant. The search distance `g` is also very small because `k ≤ 10`. Even with `10^4` test cases, the solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    def digit_sum(n):
        s = 0
        while n:
            s += n % 10
            n //= 10
        return s

    t = int(input())
    ans = []

    for _ in range(t):
        x, k = map(int, input().split())
        cur = x

        while True:
            if digit_sum(cur) % k == 0:
                ans.append(str(cur))
                break
            cur += 1

    print("\n".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue()

# provided sample
assert run(
"""6
1 5
10 8
37 9
777 3
1235 10
1 10
"""
) == """5
17
45
777
1243
19
"""

# minimum values
assert run(
"""1
1 1
"""
) == """1
"""

# already beautiful
assert run(
"""1
999999999 9
"""
) == """999999999
"""

# carry changes digit sum drastically
assert run(
"""1
19 10
"""
) == """19
"""

# near upper bound
assert run(
"""1
1000000000 10
"""
) == """1000000009
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Smallest possible input |
| `999999999 9` | `999999999` | Answer can equal the starting value |
| `19 10` | `19` | Exact divisibility at the starting number |
| `1000000000 10` | `1000000009` | Large values and repeated searching |

## Edge Cases

Consider:

```
1
777 3
```

The algorithm begins with `cur = 777`. The digit sum is `21`, and `21 % 3 = 0`. The loop stops immediately and outputs:

```
777
```

This confirms that the answer may be exactly `x`.

Consider:

```
1
17 8
```

The digit sum is `1 + 7 = 8`. Since `8 % 8 = 0`, the algorithm outputs:

```
17
```

This demonstrates that the property depends on the digit sum, not on divisibility of the number itself.

Consider:

```
1
1 10
```

The algorithm checks numbers sequentially:

```
1, 2, 3, ..., 18, 19
```

The first digit sum divisible by `10` occurs at `19`, whose digit sum is `10`. The output is:

```
19
```

This case shows why the search must continue until a valid digit sum is found, even when many consecutive numbers fail.
