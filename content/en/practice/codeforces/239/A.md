---
title: "CF 239A - Two Bags of Potatoes"
description: "We know the second bag contains y potatoes. The first bag originally contained some positive number x, but that value was lost. The only remaining information is that the total number of potatoes, x + y, was divisible by k and did not exceed n."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 239
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 148 (Div. 2)"
rating: 1200
weight: 239
solve_time_s: 83
verified: true
draft: false
---

[CF 239A - Two Bags of Potatoes](https://codeforces.com/problemset/problem/239/A)

**Rating:** 1200  
**Tags:** greedy, implementation, math  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We know the second bag contains `y` potatoes. The first bag originally contained some positive number `x`, but that value was lost. The only remaining information is that the total number of potatoes, `x + y`, was divisible by `k` and did not exceed `n`.

The task is to print every possible value of `x` that satisfies those conditions, in increasing order.

The constraints immediately point toward a simple arithmetic solution. The values themselves can be as large as `10^9`, so iterating over every possible `x` from `1` to `n` would be too expensive in a general setting. At the same time, the condition `n / k ≤ 10^5` is very revealing. It means the number of multiples of `k` up to `n` is at most `100000`, so iterating through valid totals directly is completely safe.

The key observation is that we are not really searching for arbitrary numbers. We only care about totals divisible by `k`.

There are several easy-to-miss edge cases.

Suppose the total cannot be larger than the already known bag.

Input:

```
10 1 10
```

The total must be divisible by `1`, but also must satisfy `x + 10 ≤ 10`, which forces `x ≤ 0`. Since `x` must be positive, the correct answer is:

```
-1
```

A careless implementation might accidentally include `0`.

Another tricky case appears when the first valid multiple produces `x = 0`.

Input:

```
5 5 15
```

The multiples of `5` up to `15` are `5, 10, 15`.

For totals `5` and `10`, we get `x = 0` and `x = 5`. Only positive values are allowed, so the answer is:

```
5 10
```

If we forget to exclude zero, the output becomes incorrect.

One more subtle situation is when there are no multiples larger than `y`.

Input:

```
8 10 15
```

The only multiple of `10` not exceeding `15` is `10`, which gives `x = 2`. That is valid, so the answer is:

```
2
```

The condition is about the total, not about `x` itself being divisible by `k`. A common mistake is checking `x % k == 0`, which would incorrectly reject this case.

## Approaches

The brute-force approach is straightforward. We try every possible value of `x` from `1` to `n - y`. For each candidate, we check whether `(x + y) % k == 0`. Every valid value is added to the answer.

This works because the conditions are easy to verify independently. The issue is scale. In the worst case, `n` can reach `10^9`, so iterating through all candidates would require up to a billion checks, far beyond what is practical.

The structure of the divisibility condition gives a much better direction. Instead of guessing `x`, we can think about the total number of potatoes.

The total `x + y` must be a multiple of `k`. That means every valid total has the form:

$x+y=m\cdot k$

for some integer `m`.

So rather than iterating over all possible `x`, we iterate over all multiples of `k` up to `n`. For each multiple `t`, we compute:

$x=t-y$

If `x > 0`, then it is a valid answer.

The important difference is the number of candidates. There are only `n / k` multiples of `k` up to `n`, and the problem guarantees this quantity is at most `10^5`. That makes the optimized solution easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(n / k) | O(1) excluding output | Accepted |

## Algorithm Walkthrough

1. Read the integers `y`, `k`, and `n`.
2. Iterate through every multiple of `k` from `k` up to `n`.
3. For each multiple `t`, compute `x = t - y`.
4. Check whether `x` is positive.

The problem requires the first bag to contain at least one potato, so `x = 0` is invalid.
5. If `x > 0`, append it to the answer list.
6. After processing all multiples:

If the answer list is empty, print `-1`. Otherwise print all collected values separated by spaces.

### Why it works

Every valid configuration must satisfy two conditions:

$x+y\le n$

and

$(x+y)\bmod k=0$

The algorithm enumerates every multiple of `k` that does not exceed `n`. Each such multiple represents a possible total number of potatoes. Subtracting `y` gives the only corresponding value of `x`.

No valid answer can be missed because every valid total must appear among those multiples. No invalid answer can be included because we only accept positive `x`.

## Python Solution

```python
import sys
input = sys.stdin.readline

y, k, n = map(int, input().split())

ans = []

for total in range(k, n + 1, k):
    x = total - y
    if x > 0:
        ans.append(str(x))

if ans:
    print(" ".join(ans))
else:
    print(-1)
```

The loop iterates directly over multiples of `k`. This matches the mathematical structure of the problem and avoids checking irrelevant values.

The expression `range(k, n + 1, k)` generates:

```
k, 2k, 3k, ...
```

up to `n`.

For each total, we reconstruct the missing amount using:

```
x = total - y
```

The positivity check is crucial. Values where `x == 0` are invalid because the first bag originally contained at least one potato.

The solution stores answers as strings immediately, which makes the final printing step simple and efficient.

## Worked Examples

### Example 1

Input:

```
10 1 10
```

| total | x = total - y | Valid? | ans |
| --- | --- | --- | --- |
| 1 | -9 | No | [] |
| 2 | -8 | No | [] |
| 3 | -7 | No | [] |
| ... | ... | ... | [] |
| 10 | 0 | No | [] |

Final output:

```
-1
```

This example demonstrates the strict positivity requirement. Even though every total is divisible by `1`, no positive value of `x` exists.

### Example 2

Input:

```
5 3 20
```

| total | x = total - y | Valid? | ans |
| --- | --- | --- | --- |
| 3 | -2 | No | [] |
| 6 | 1 | Yes | [1] |
| 9 | 4 | Yes | [1, 4] |
| 12 | 7 | Yes | [1, 4, 7] |
| 15 | 10 | Yes | [1, 4, 7, 10] |
| 18 | 13 | Yes | [1, 4, 7, 10, 13] |

Final output:

```
1 4 7 10 13
```

This trace shows how each multiple of `k` corresponds to exactly one possible value of `x`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n / k) | We iterate through every multiple of `k` up to `n` |
| Space | O(1) excluding output | Only a few variables are used |

The constraint `n / k ≤ 10^5` guarantees the loop performs at most one hundred thousand iterations, which is trivial within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    y, k, n = map(int, input().split())

    ans = []

    for total in range(k, n + 1, k):
        x = total - y
        if x > 0:
            ans.append(str(x))

    if ans:
        print(" ".join(ans))
    else:
        print(-1)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("10 1 10\n") == "-1", "sample 1"

# custom cases
assert run("5 3 20\n") == "1 4 7 10 13", "basic valid sequence"

assert run("1 1 2\n") == "1", "minimum positive answer"

assert run("5 5 15\n") == "5 10", "exclude x = 0"

assert run("999999999 1000000000 1000000000\n") == "1", "large values"

assert run("8 10 15\n") == "2", "x itself need not be divisible by k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 3 20` | `1 4 7 10 13` | Standard progression of valid answers |
| `1 1 2` | `1` | Smallest non-trivial valid case |
| `5 5 15` | `5 10` | Ensures `x = 0` is excluded |
| `999999999 1000000000 1000000000` | `1` | Correct handling of large integers |
| `8 10 15` | `2` | Total must be divisible, not `x` |

## Edge Cases

Consider the case where no positive value of `x` exists.

Input:

```
10 1 10
```

The algorithm checks totals from `1` through `10`. Every computed value of `x = total - 10` is non-positive. Since the answer list remains empty, the algorithm prints:

```
-1
```

This correctly handles the situation where the known bag already uses the entire allowed total.

Now consider the boundary where the smallest multiple gives `x = 0`.

Input:

```
5 5 15
```

The examined totals are `5`, `10`, and `15`.

For `total = 5`:

```
x = 5 - 5 = 0
```

This is rejected because the first bag must contain at least one potato.

For the remaining totals:

```
x = 10 - 5 = 5
x = 15 - 5 = 10
```

Both are accepted, producing:

```
5 10
```

This confirms the strict `x > 0` condition is handled correctly.

Finally, consider a case where `x` itself is not divisible by `k`.

Input:

```
8 10 15
```

The only multiple of `10` not exceeding `15` is `10`.

The algorithm computes:

```
x = 10 - 8 = 2
```

Since `2 > 0`, it is printed.

The output is:

```
2
```

This verifies that divisibility applies to the total `x + y`, not to `x` individually.
