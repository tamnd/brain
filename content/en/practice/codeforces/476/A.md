---
title: "CF 476A - Dreamoon and Stairs"
description: "Dreamoon wants to reach the top of a staircase containing n steps. Every move can cover either 1 step or 2 steps. Among all possible ways to reach exactly step n, we need the number of moves used to be divisible by m. The task is not asking for the number of different sequences."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 476
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 272 (Div. 2)"
rating: 1000
weight: 476
solve_time_s: 92
verified: true
draft: false
---

[CF 476A - Dreamoon and Stairs](https://codeforces.com/problemset/problem/476/A)

**Rating:** 1000  
**Tags:** implementation, math  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

Dreamoon wants to reach the top of a staircase containing `n` steps. Every move can cover either 1 step or 2 steps. Among all possible ways to reach exactly step `n`, we need the number of moves used to be divisible by `m`.

The task is not asking for the number of different sequences. It asks for the smallest possible move count that is a multiple of `m` and still allows Dreamoon to reach exactly the top. If no such move count exists, we must print `-1`.

The constraints are very small. The staircase height is at most 10000 and `m` is at most 10. Even a simple linear scan over all possible move counts would be easily fast enough. There is no need for dynamic programming, graph search, or combinatorics.

The key observation comes from understanding which move counts are possible.

If every move is a 2-step move, the number of moves is as small as possible. That minimum is `ceil(n / 2)`.

If every move is a 1-step move, the number of moves is as large as possible. That maximum is `n`.

Every integer move count between these two values is achievable. Starting from all 2-step moves, replacing one 2-step move with two 1-step moves increases the move count by exactly 1 while keeping the total climbed distance unchanged.

There are a few edge cases that can easily cause mistakes.

Consider:

```
3 5
```

The minimum possible move count is `2` and the maximum is `3`. There is no multiple of `5` in that interval, so the answer is:

```
-1
```

A careless solution that simply rounds the minimum move count up to the next multiple of `m` would obtain `5`, which is impossible because five moves cannot climb exactly three steps.

Another important case is:

```
1 2
```

The only possible move count is `1`. Since `1` is not divisible by `2`, the correct answer is:

```
-1
```

A solution that assumes there is always an answer would fail here.

Finally:

```
10 2
```

The minimum possible move count is `5`. Since `6` is the first multiple of `2` that is at least `5`, the answer is:

```
6
```

The algorithm must search within the feasible interval rather than blindly taking either endpoint.

## Approaches

A brute-force approach is to enumerate every possible move count and check whether it can correspond to a valid climb. A move count `k` is feasible if `ceil(n/2) ≤ k ≤ n`. Among all feasible values, we choose the smallest one divisible by `m`.

For this problem, the interval contains at most 10000 values, so even a linear scan is perfectly acceptable.

The interesting part is recognizing why the feasible interval is exactly from `ceil(n/2)` to `n`.

The smallest number of moves occurs when we use as many 2-step moves as possible. That gives `ceil(n/2)` moves.

The largest number of moves occurs when every move is a 1-step move. That gives `n` moves.

Every value in between is reachable because replacing a single 2-step move by two 1-step moves increases the move count by exactly one without changing the total climbed distance.

Once this property is understood, the problem becomes very simple. We only need the smallest multiple of `m` that lies inside the interval `[ceil(n/2), n]`.

Instead of scanning the whole interval, we can directly compute the first multiple of `m` that is at least `ceil(n/2)`. If that multiple does not exceed `n`, it is the answer. Otherwise no valid move count exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the minimum possible number of moves.

This is `ceil(n / 2)`, which can be written as `(n + 1) // 2` using integer arithmetic.
2. Find the smallest multiple of `m` that is at least this minimum value.

Let `mn` be the minimum move count. The desired multiple is:

`((mn + m - 1) // m) * m`

This is the standard way to round a number up to the next multiple.
3. Check whether this multiple is still a feasible move count.

If the multiple is greater than `n`, it lies outside the achievable interval and no answer exists.
4. Print the multiple if it is feasible, otherwise print `-1`.

### Why it works

Every valid climb uses some number of 1-step moves and some number of 2-step moves. The move count can never be smaller than `ceil(n/2)` and can never exceed `n`.

Furthermore, every integer between those bounds is achievable. Starting from a minimum-move solution, each replacement of one 2-step move by two 1-step moves increases the move count by exactly one while preserving the total distance climbed.

Because all move counts in the interval are feasible, the problem reduces to finding the smallest multiple of `m` inside that interval. The algorithm computes exactly that value. If the first such multiple exceeds the upper bound `n`, then no valid multiple exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

mn = (n + 1) // 2
ans = ((mn + m - 1) // m) * m

if ans <= n:
    print(ans)
else:
    print(-1)
```

The first computation finds the minimum achievable move count. Using `(n + 1) // 2` avoids floating-point arithmetic and correctly implements the ceiling operation.

The next line rounds this minimum value upward to the nearest multiple of `m`. This directly gives the smallest candidate answer.

The final check is crucial. A multiple may exist above the feasible interval. For example, with `n = 3` and `m = 5`, the rounded value is `5`, but five moves cannot climb only three stairs. Comparing against `n` catches this situation and produces `-1`.

All calculations fit comfortably in standard integer types, and Python handles them naturally.

## Worked Examples

### Sample 1

Input:

```
10 2
```

| Variable | Value |
| --- | --- |
| n | 10 |
| m | 2 |
| mn = (n + 1) // 2 | 5 |
| First multiple of 2 ≥ 5 | 6 |
| Check 6 ≤ 10 | True |
| Answer | 6 |

The minimum possible move count is 5. Since 5 is not divisible by 2, we move to the next multiple, which is 6. It still lies within the feasible interval `[5, 10]`, so the answer is 6.

### Sample 2

Input:

```
3 5
```

| Variable | Value |
| --- | --- |
| n | 3 |
| m | 5 |
| mn = (n + 1) // 2 | 2 |
| First multiple of 5 ≥ 2 | 5 |
| Check 5 ≤ 3 | False |
| Answer | -1 |

The feasible move counts are only 2 and 3. Neither is divisible by 5. The first multiple of 5 is already outside the interval, so no valid answer exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a handful of arithmetic operations are performed |
| Space | O(1) | No extra data structures are used |

The solution performs constant-time arithmetic regardless of the value of `n`. It easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    n, m = map(int, input().split())

    mn = (n + 1) // 2
    ans = ((mn + m - 1) // m) * m

    print(ans if ans <= n else -1)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("10 2\n") == "6", "sample 1"

# sample-like impossible case
assert run("3 5\n") == "-1", "sample 2"

# minimum staircase
assert run("1 2\n") == "-1", "minimum size"

# exact multiple at lower bound
assert run("4 2\n") == "2", "lower bound already valid"

# answer requires rounding up
assert run("7 3\n") == "6", "round to next multiple"

# large boundary
assert run("10000 10\n") == "5000", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | `-1` | Smallest staircase, no valid multiple |
| `4 2` | `2` | Lower bound already divisible by `m` |
| `7 3` | `6` | Correct rounding to next multiple |
| `10000 10` | `5000` | Largest input size |
| `3 5` | `-1` | No multiple exists inside feasible interval |

## Edge Cases

Consider:

```
1 2
```

The algorithm computes:

`mn = (1 + 1) // 2 = 1`

The first multiple of 2 at least 1 is 2.

Since `2 > 1`, the value lies outside the feasible interval `[1, 1]`. The algorithm prints:

```
-1
```

which is correct.

Now consider:

```
3 5
```

The feasible move counts are only 2 and 3.

The algorithm computes:

`mn = 2`

The first multiple of 5 at least 2 is 5.

Since `5 > 3`, no feasible multiple exists, so the output is:

```
-1
```

Finally consider:

```
4 2
```

The minimum move count is:

`mn = 2`

Since 2 is already divisible by 2, the rounded multiple remains 2.

Because `2 ≤ 4`, the algorithm outputs:

```
2
```

This verifies that the solution correctly handles cases where the optimal answer is exactly the minimum feasible move count.
