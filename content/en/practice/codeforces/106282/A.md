---
title: "CF 106282A - \u0421\u043e\u0432\u0443\u043d\u044c\u044f \u0438 \u0441\u043e\u043b\u0435\u043d\u0438\u044f"
description: "The problem describes a simple situation: there are n mushrooms that need to be placed equally into k jars. If n is not divisible by k, some more mushrooms must be collected."
date: "2026-06-25T07:39:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106282
codeforces_index: "A"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 (\u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435) 9 \u043a\u043b\u0430\u0441\u0441, \u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c, 2025"
rating: 0
weight: 106282
solve_time_s: 28
verified: true
draft: false
---

[CF 106282A - \u0421\u043e\u0432\u0443\u043d\u044c\u044f \u0438 \u0441\u043e\u043b\u0435\u043d\u0438\u044f](https://codeforces.com/problemset/problem/106282/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes a simple situation: there are `n` mushrooms that need to be placed equally into `k` jars. If `n` is not divisible by `k`, some more mushrooms must be collected. The goal is to find the smallest number of additional mushrooms needed so that the total number of mushrooms can be split evenly among all jars.

The input contains two integers. The first is the current number of mushrooms, and the second is the number of jars. The output is the minimum number of extra mushrooms required.

The constraints allow both values to be as large as `10^9`. That immediately rules out trying to simulate adding mushrooms one by one, because in the worst case the answer itself can be close to `10^9`. Even a loop with hundreds of millions of iterations would be too slow. The solution needs to use constant-time arithmetic.

The main edge cases come from handling numbers that are already divisible and from correctly interpreting the remainder.

Consider `n = 8` and `k = 4`. The correct output is `0`, because eight mushrooms already fill four jars equally. A careless solution that always adds `k - n % k` would still work here, but if implemented incorrectly with a special case missing, it could return `4`.

Another case is when the number of mushrooms is smaller than the number of jars. For example:

```
n = 3
k = 5
```

The correct output is `2`, because after collecting two more mushrooms there will be five mushrooms, one for each jar. A solution that only checks whether `n / k` is already positive might incorrectly conclude that no distribution is possible.

A final boundary case is when the remainder is close to `k`. For example:

```
n = 17
k = 10
```

The correct output is `3`, because `17 + 3 = 20`, which is the first multiple of ten after seventeen. Forgetting that we need to reach the next multiple, not just remove the remainder, leads to wrong answers.

# Approaches

The straightforward approach is to repeatedly add one mushroom until the total becomes divisible by `k`. This works because every valid answer must be some number of additions that moves `n` to a multiple of `k`. If we try `0`, then `1`, then `2`, and so on, the first successful value is guaranteed to be minimal.

The problem is that the answer can be very large. Suppose `n = 1` and `k = 10^9`. A simulation would require almost one billion iterations before reaching a valid total. That is far beyond what a program can do in a typical contest time limit.

The key observation is that divisibility depends only on the remainder after division by `k`. If `n % k = r`, then `n` is already `r` mushrooms away from the previous multiple of `k`. To reach the next multiple, we need to add `k - r` mushrooms. The only exception is when `r = 0`, because the number is already valid and we need to add nothing.

The entire problem reduces to computing the remainder and converting it into the distance to the next multiple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) in the worst case | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

# Algorithm Walkthrough

1. Read the current number of mushrooms `n` and the number of jars `k`.
2. Compute `n % k`, which tells us how many mushrooms remain after making as many complete groups of `k` as possible.
3. If the remainder is zero, output `0` because the mushrooms can already be distributed equally.
4. Otherwise, output `k - (n % k)`, because that is exactly the number of mushrooms needed to move from the current remainder to the next multiple of `k`.

Why it works: every number divisible by `k` is a multiple of `k`. Starting from `n`, the closest larger multiple of `k` is obtained by increasing the remainder to `k`. If the remainder is already zero, the closest valid multiple is the number itself. Since we move to the nearest possible multiple, the number of added mushrooms is minimal.

# Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
k = int(input())

rem = n % k

if rem == 0:
    print(0)
else:
    print(k - rem)
```

The first two lines read the two values from input. There are no multiple test cases, so the program directly processes these numbers.

The remainder calculation is the core of the solution. Python integers can handle values much larger than `10^9`, so there is no overflow concern.

The `rem == 0` condition is necessary because `k - rem` would give `k` in that situation, but the correct answer is zero. This is the only special case needed.

# Worked Examples

### Example 1

Input:

```
3
4
```

| Step | n | k | n % k | Answer |
| --- | --- | --- | --- | --- |
| Read values | 3 | 4 | - | - |
| Compute remainder | 3 | 4 | 3 | - |
| Add mushrooms to next multiple | 3 | 4 | 3 | 1 |

The three mushrooms leave a remainder of three when grouped into jars of size four. One more mushroom creates four mushrooms, which can be placed one per jar.

### Example 2

Input:

```
7
5
```

| Step | n | k | n % k | Answer |
| --- | --- | --- | --- | --- |
| Read values | 7 | 5 | - | - |
| Compute remainder | 7 | 5 | 2 | - |
| Add mushrooms to next multiple | 7 | 5 | 2 | 3 |

Seven mushrooms leave a remainder of two after taking out groups of five. Adding three mushrooms creates ten mushrooms, which can be split into two mushrooms per jar.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only one division and a few arithmetic operations are performed. |
| Space | O(1) | The algorithm stores only a few integer variables. |

The constraints allow values up to `10^9`, and the algorithm does not depend on the size of the answer. It easily fits within the time and memory limits.

# Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    n = int(input())
    k = int(input())

    rem = n % k
    ans = 0 if rem == 0 else k - rem

    sys.stdin = old_stdin
    return str(ans) + "\n"

# provided samples
assert solve("3\n4\n") == "1\n", "sample 1"
assert solve("7\n5\n") == "3\n", "sample 2"

# custom cases
assert solve("8\n4\n") == "0\n", "already divisible"
assert solve("1\n1000000000\n") == "999999999\n", "large gap"
assert solve("1000000000\n1000000000\n") == "0\n", "maximum equal values"
assert solve("17\n10\n") == "3\n", "next multiple boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `8 / 4` | `0` | Handles numbers already divisible by the jar count |
| `1 / 1000000000` | `999999999` | Handles the largest possible addition count |
| `1000000000 / 1000000000` | `0` | Checks maximum values and exact division |
| `17 / 10` | `3` | Checks moving to the next multiple correctly |

# Edge Cases

For `n = 8` and `k = 4`, the algorithm computes `8 % 4 = 0`. Since the remainder is zero, it immediately returns `0`. No extra mushrooms are requested because the distribution is already possible.

For `n = 3` and `k = 5`, the algorithm computes `3 % 5 = 3`. The next multiple of five is five, so it calculates `5 - 3 = 2`. After adding two mushrooms, there are five mushrooms and each jar receives one.

For `n = 17` and `k = 10`, the algorithm computes `17 % 10 = 7`. The next multiple of ten is twenty, which is three away. The answer `3` confirms that the algorithm always moves forward to the nearest valid total rather than simply using the current remainder.
