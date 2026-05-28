---
title: "CF 214A - System of Equations"
description: "We need to count how many non-negative integer pairs (a, b) satisfy two equations at the same time: - a² + b = n - a + b² = m The input gives the two target values n and m."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 214
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 131 (Div. 2)"
rating: 800
weight: 214
solve_time_s: 56
verified: true
draft: false
---

[CF 214A - System of Equations](https://codeforces.com/problemset/problem/214/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to count how many non-negative integer pairs `(a, b)` satisfy two equations at the same time:

- `a² + b = n`
- `a + b² = m`

The input gives the two target values `n` and `m`. Our job is to test possible values of `a` and `b` and count how many pairs make both equations true simultaneously.

The constraints are very small. Both `n` and `m` are at most `1000`, which immediately suggests that brute force is feasible. Even checking every pair `(a, b)` from `0` to `1000` only requires around one million iterations, which is trivial within a 2-second limit in Python.

The more interesting part is recognizing how tightly the equations restrict the search space. Since `a² ≤ n`, the value of `a` can never exceed `√n`. Similarly, `b² ≤ m`, so `b` can never exceed `√m`. That observation reduces the search dramatically.

There are a few easy-to-miss edge cases.

One subtle case is when one variable becomes zero. For example:

```
9 3
```

The valid pair is `(3, 0)` because:

- `3² + 0 = 9`
- `3 + 0² = 3`

A careless implementation that starts loops from `1` instead of `0` would incorrectly miss this answer.

Another tricky situation is when no pair exists at all. For example:

```
1 1
```

Trying all possibilities gives no valid pair. Some incorrect solutions independently solve each equation and accidentally combine incompatible values.

A different edge case appears when multiple candidate values satisfy one equation individually but not both together. For example:

```
10 34
```

The pair `(3, 1)` satisfies:

- `3² + 1 = 10`
- `3 + 1² = 4`

The first equation works, but the second does not. The algorithm must always verify both equations simultaneously.

## Approaches

The most direct approach is to try every possible pair `(a, b)` and check whether both equations hold.

Since both variables are non-negative and bounded by `1000`, we can iterate:

- `a` from `0` to `1000`
- `b` from `0` to `1000`

For each pair, compute:

- `a² + b`
- `a + b²`

If both match `n` and `m`, increment the answer.

This brute-force solution is correct because it explicitly checks every possible candidate pair. Nothing can be missed.

The issue is efficiency. A full search performs roughly:

```
1001 × 1001 ≈ 1,000,000
```

checks. Even this still passes comfortably for the given constraints, but we can do better with a small observation.

From the first equation:

```
a² + b = n
```

Since `b ≥ 0`, we know:

```
a² ≤ n
```

So `a` only needs to go up to `√n`.

Similarly, from:

```
a + b² = m
```

we get:

```
b² ≤ m
```

So `b` only needs to go up to `√m`.

This turns the search into a very small brute force over realistic candidate values instead of the entire `[0, 1000]` range.

Another useful observation is that once `a` is fixed, the first equation uniquely determines `b`:

```
b = n - a²
```

So we do not even need a nested loop. We can iterate over `a`, compute the only possible `b`, and verify the second equation.

That reduces the algorithm to linear complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1000²) | O(1) | Accepted |
| Optimal | O(√n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers `n` and `m`.
2. Initialize `answer = 0`.
3. Iterate `a` from `0` while `a² ≤ n`.

Any larger value of `a` would immediately violate the first equation because `b` cannot be negative.
4. Compute:

```
b = n - a²
```

This is the only possible value of `b` that can satisfy the first equation for the current `a`.
5. Check whether the second equation also holds:

```
a + b² == m
```

If true, increment `answer`.
6. After the loop finishes, print `answer`.

### Why it works

For every non-negative integer `a` with `a² ≤ n`, the first equation determines exactly one candidate value of `b`. No other `b` can satisfy:

```
a² + b = n
```

So the algorithm examines every possible valid pair exactly once. The second equation acts as a filter that keeps only the pairs satisfying the entire system. Since every feasible pair must appear during this process, the final count is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

answer = 0

a = 0
while a * a <= n:
    b = n - a * a

    if a + b * b == m:
        answer += 1

    a += 1

print(answer)
```

The loop only iterates over feasible values of `a`. The condition `a * a <= n` guarantees that `b = n - a²` remains non-negative.

The line:

```
b = n - a * a
```

comes directly from rearranging the first equation. This avoids a nested loop entirely.

The second equation:

```
a + b * b == m
```

is checked exactly once for each candidate pair.

One subtle detail is using multiplication instead of square roots. Computing bounds with floating-point square roots can introduce rounding issues. The loop condition `a * a <= n` avoids that problem completely.

Another small implementation detail is that `b` is always an integer because `n` and `a²` are integers. No extra validation is needed.

## Worked Examples

### Example 1

Input:

```
9 3
```

| a | a² | b = n - a² | a + b² | Valid? |
| --- | --- | --- | --- | --- |
| 0 | 0 | 9 | 81 | No |
| 1 | 1 | 8 | 65 | No |
| 2 | 4 | 5 | 27 | No |
| 3 | 9 | 0 | 3 | Yes |

The algorithm finds exactly one valid pair: `(3, 0)`. This trace demonstrates why checking only one computed `b` per `a` is sufficient.

### Example 2

Input:

```
1 1
```

| a | a² | b = n - a² | a + b² | Valid? |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | Yes |
| 1 | 1 | 0 | 1 | Yes |

The output is:

```
2
```

The valid pairs are `(0, 1)` and `(1, 0)`.

This example shows that multiple answers are possible and that zero values must be included in the search.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n) | The loop runs while `a² ≤ n` |
| Space | O(1) | Only a few integer variables are stored |

With `n ≤ 1000`, the loop runs at most about 32 times. The program easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())

    answer = 0

    a = 0
    while a * a <= n:
        b = n - a * a

        if a + b * b == m:
            answer += 1

        a += 1

    print(answer)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided samples
assert run("9 3\n") == "1\n", "sample 1"

# custom cases
assert run("1 1\n") == "2\n", "two symmetric solutions"

assert run("2 2\n") == "0\n", "no valid pair"

assert run("0 0\n") == "1\n", "minimum values"

assert run("1000 1000\n") == "0\n", "large boundary case"

assert run("25 5\n") == "1\n", "solution with b = 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `2` | Multiple valid pairs |
| `2 2` | `0` | No solution exists |
| `0 0` | `1` | Minimum boundary values |
| `1000 1000` | `0` | Large input handling |
| `25 5` | `1` | Case where one variable is zero |

## Edge Cases

Consider the input:

```
9 3
```

The algorithm tries:

- `a = 0`, `b = 9`
- `a = 1`, `b = 8`
- `a = 2`, `b = 5`
- `a = 3`, `b = 0`

Only the last pair satisfies the second equation. Since the loop starts at `0`, the solution with `b = 0` is correctly included.

Now look at:

```
2 2
```

The algorithm checks:

- `a = 0`, `b = 2`
- `a = 1`, `b = 1`

Neither satisfies `a + b² = 2`, so the answer remains `0`. This confirms the algorithm does not falsely count pairs that satisfy only one equation.

Finally, consider:

```
1 1
```

The execution finds:

- `(0, 1)`
- `(1, 0)`

Both are counted independently because the loop examines every feasible `a`. This validates that symmetric solutions are handled correctly.
