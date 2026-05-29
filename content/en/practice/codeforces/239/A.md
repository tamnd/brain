---
title: "CF 239A - Two Bags of Potatoes"
description: "We know how many potatoes were in the second bag, y. The first bag contained some positive number x, but that value was lost. The only facts that remain are: x + y was divisible by k. x + y was not greater than n."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 239
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 148 (Div. 2)"
rating: 1200
weight: 239
solve_time_s: 94
verified: true
draft: false
---

[CF 239A - Two Bags of Potatoes](https://codeforces.com/problemset/problem/239/A)

**Rating:** 1200  
**Tags:** greedy, implementation, math  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We know how many potatoes were in the second bag, `y`. The first bag contained some positive number `x`, but that value was lost. The only facts that remain are:

`x + y` was divisible by `k`.

`x + y` was not greater than `n`.

The task is to print every possible value of `x` that satisfies those conditions, in increasing order.

Another way to think about the problem is this: we need all multiples of `k` that are larger than `y` and at most `n`. If such a multiple is `m`, then the missing value is simply:

$$x = m - y$$

Since `x` must represent the number of potatoes in a bag, it has to be strictly positive.

The constraints are small in an interesting way. Although `n`, `k`, and `y` can each reach `10^9`, the value of `n / k` is at most `10^5`. That means the number of multiples of `k` up to `n` is never large. We cannot iterate through every integer from `1` to `n`, because that could require a billion iterations, but iterating through all multiples of `k` is completely safe.

A few edge cases are easy to mishandle.

Suppose the total already equals `n` and is divisible by `k`.

Input:

```
10 1 10
```

The only multiple of `1` up to `10` is every number from `1` to `10`, but any valid total must be strictly greater than `y = 10`, otherwise `x = total - y` becomes zero or negative. No valid `x` exists, so the correct output is:

```
-1
```

A careless implementation might incorrectly include `x = 0`.

Another subtle case appears when the first valid multiple is exactly `y`.

Input:

```
5 5 20
```

Multiples of `5` are `5, 10, 15, 20`. The total `5` gives `x = 0`, which is invalid. The correct answers are:

```
5 10 15
```

If the code forgets to enforce `x > 0`, it will print an extra zero.

One more corner case happens when no multiple larger than `y` exists at all.

Input:

```
13 7 15
```

The multiples of `7` up to `15` are `7` and `14`. Only `14` exceeds `13`, giving:

```
1
```

But if the input were:

```
14 7 15
```

then there would be no valid multiple strictly larger than `14`, so the output must be:

```
-1
```

This strict inequality is the main source of off by one mistakes.

## Approaches

A direct brute-force solution would try every possible value of `x` from `1` to `n`. For each candidate, we would check whether `x + y` is divisible by `k` and whether the sum stays within the limit `n`.

This works because the conditions are easy to verify:

$$(x + y) \bmod k = 0$$

and

$$x + y \le n$$

The problem is the running time. In the worst case, `n` can be `10^9`, so scanning all candidates would require up to a billion iterations. That is far beyond what competitive programming time limits allow.

The key observation is that we do not actually care about arbitrary values of `x`. We care about totals `x + y` that are divisible by `k`. Those totals are exactly the multiples of `k`.

Instead of searching over all `x`, we can search over all multiples of `k`:

$$k, 2k, 3k, \dots$$

up to `n`.

For each multiple `m`, we compute:

$$x = m - y$$

If `x > 0`, it is a valid answer.

This changes the complexity dramatically. The number of multiples of `k` up to `n` is:

$$\left\lfloor \frac{n}{k} \right\rfloor$$

and the constraints guarantee this value is at most `10^5`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(n / k) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers `y`, `k`, and `n`.
2. Iterate through every multiple of `k` from `k` up to `n`.

We can generate these values using:

$$m = k, 2k, 3k, \dots$$

These are the only totals that could satisfy the divisibility condition.
3. For each multiple `m`, compute:

$$x = m - y$$

Since `m = x + y`, subtracting `y` reconstructs the missing number of potatoes.
4. Check whether `x > 0`.

The first bag must contain at least one potato. Values `x = 0` or negative are invalid.
5. Store every valid `x` in order.

Since the multiples are processed in increasing order, the answers are automatically sorted.
6. After the loop finishes, print all collected values separated by spaces.
7. If no valid values were found, print `-1`.

### Why it works

Every valid solution must satisfy:

$$x + y \equiv 0 \pmod{k}$$

That means the total `x + y` must be some multiple of `k`. The algorithm enumerates every such multiple up to `n`, so no valid total is missed.

For each multiple `m`, the corresponding candidate:

$$x = m - y$$

is the only possible value that produces that total. The algorithm accepts it exactly when `x > 0`, which matches the requirement that the first bag contain a positive number of potatoes.

Since every accepted value satisfies all constraints, and every valid value appears during enumeration, the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    y, k, n = map(int, input().split())

    ans = []

    multiple = k
    while multiple <= n:
        x = multiple - y

        if x > 0:
            ans.append(str(x))

        multiple += k

    if ans:
        print(" ".join(ans))
    else:
        print(-1)

solve()
```

The solution follows the exact reasoning from the walkthrough.

The loop iterates only over multiples of `k`. This is the critical optimization. Iterating over every possible `x` would be far too slow when `n` is large.

For each multiple, the code reconstructs the missing value using:

```
x = multiple - y
```

The condition:

```
if x > 0:
```

is easy to underestimate, but it is essential. Without it, the program would incorrectly include cases where the first bag contains zero or a negative number of potatoes.

The answers are stored as strings immediately. This avoids an extra conversion step during output formatting.

The loop increments by `k` each time:

```
multiple += k
```

which guarantees we visit every divisible total exactly once and in sorted order.

## Worked Examples

### Example 1

Input:

```
10 1 10
```

| Current multiple | x = multiple - y | Valid? | Answers |
| --- | --- | --- | --- |
| 1 | -9 | No | [] |
| 2 | -8 | No | [] |
| 3 | -7 | No | [] |
| 4 | -6 | No | [] |
| 5 | -5 | No | [] |
| 6 | -4 | No | [] |
| 7 | -3 | No | [] |
| 8 | -2 | No | [] |
| 9 | -1 | No | [] |
| 10 | 0 | No | [] |

No valid positive value of `x` appears. The algorithm correctly prints:

```
-1
```

This example demonstrates why the strict condition `x > 0` matters.

### Example 2

Input:

```
10 6 40
```

| Current multiple | x = multiple - y | Valid? | Answers |
| --- | --- | --- | --- |
| 6 | -4 | No | [] |
| 12 | 2 | Yes | [2] |
| 18 | 8 | Yes | [2, 8] |
| 24 | 14 | Yes | [2, 8, 14] |
| 30 | 20 | Yes | [2, 8, 14, 20] |
| 36 | 26 | Yes | [2, 8, 14, 20, 26] |

The output becomes:

```
2 8 14 20 26
```

Each answer produces a total divisible by `6` while staying within the limit `40`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n / k) | We iterate once over every multiple of `k` up to `n` |
| Space | O(n / k) | In the worst case, all generated values are stored |

The constraint:

$$\frac{n}{k} \le 10^5$$

guarantees that the loop never becomes large. Even in the worst case, the program performs only around one hundred thousand iterations, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    y, k, n = map(int, input().split())

    ans = []

    multiple = k
    while multiple <= n:
        x = multiple - y

        if x > 0:
            ans.append(str(x))

        multiple += k

    if ans:
        print(" ".join(ans))
    else:
        print(-1)

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

# provided sample
assert run("10 1 10\n") == "-1\n", "sample 1"

# custom cases
assert run("10 6 40\n") == "2 8 14 20 26\n", "basic valid case"

assert run("5 5 20\n") == "5 10 15\n", "must exclude x = 0"

assert run("14 7 15\n") == "-1\n", "no multiple strictly larger than y"

assert run("1 1000000000 1000000000\n") == "999999999\n", "large values"

assert run("1 2 3\n") == "1\n", "single valid answer"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `10 6 40` | `2 8 14 20 26` | Normal multi-answer scenario |
| `5 5 20` | `5 10 15` | Excludes invalid zero answer |
| `14 7 15` | `-1` | No valid multiple beyond `y` |
| `1 1000000000 1000000000` | `999999999` | Handles very large numbers correctly |
| `1 2 3` | `1` | Single valid candidate |

## Edge Cases

Consider the input:

```
10 1 10
```

The algorithm generates all multiples of `1` from `1` to `10`. Every computed value:

$$x = multiple - 10$$

is non-positive. Since the condition requires `x > 0`, none are accepted. The answer list stays empty, so the algorithm prints:

```
-1
```

This correctly handles the case where the total cannot exceed the known second bag size.

Now examine:

```
5 5 20
```

The generated multiples are `5`, `10`, `15`, and `20`.

For `5`, the computed value is:

$$x = 5 - 5 = 0$$

which must be rejected.

The remaining values produce:

$$x = 5, 10, 15$$

and all are valid. The algorithm prints:

```
5 10 15
```

This case confirms that the strict positivity check prevents off by one errors.

Finally, consider:

```
14 7 15
```

The multiples of `7` up to `15` are `7` and `14`.

The computed values are:

$$7 - 14 = -7$$

and

$$14 - 14 = 0$$

Neither is positive, so the output becomes:

```
-1
```

This demonstrates that equality is not enough. The total must be strictly larger than `y` so that the first bag contains at least one potato.
