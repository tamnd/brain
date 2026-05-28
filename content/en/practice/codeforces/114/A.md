---
title: "CF 114A - Cifera"
description: "We are given two integers, k and l. The task is to determine whether l can be written as an exact power of k. In other words, we need to check whether there exists a non-negative integer n such that: $l = k^n$ If such an n exists, we print \"YES\" and also print the importance of…"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 114
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 86 (Div. 2 Only)"
rating: 1000
weight: 114
solve_time_s: 118
verified: true
draft: false
---

[CF 114A - Cifera](https://codeforces.com/problemset/problem/114/A)

**Rating:** 1000  
**Tags:** math  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers, `k` and `l`. The task is to determine whether `l` can be written as an exact power of `k`.

In other words, we need to check whether there exists a non-negative integer `n` such that:

$l = k^n$

If such an `n` exists, we print `"YES"` and also print the importance of the number, which is exactly `n - 1` in the terminology of the statement. For example, `k^1` has zero occurrences of `"la"`, `k^2` has one occurrence, and so on.

The constraints are small enough that we do not need advanced mathematics or logarithms. Both numbers fit inside 32-bit signed integers, so repeated multiplication or division is completely feasible. Since powers of `k` grow exponentially, the number of steps before exceeding `l` is at most around 31 when `k >= 2`.

The main danger is handling the exponent count correctly. A careless implementation can easily print the wrong importance value because the statement counts the number of `"la"` words, not the exponent itself.

Consider this example:

Input:

```
5
25
```

Here:

$25 = 5^2$

The exponent is `2`, but the importance is `1`, because `"petricium la petricium"` contains one `"la"`.

Another subtle edge case appears when `l` is not divisible by `k` during the process.

Input:

```
3
10
```

A naive loop that keeps multiplying powers might overshoot or use floating-point logarithms and run into precision issues. The correct answer is `"NO"` because no integer power of `3` equals `10`.

One more important case is when `l = k`.

Input:

```
7
7
```

This corresponds to:

$7 = 7^1$

The answer should be:

```
YES
0
```

because the importance counts `"la"` words, and there are none in the first power.

## Approaches

The brute-force idea is straightforward. Start from `1`, repeatedly multiply by `k`, and check whether we eventually reach `l`.

For example:

```
1 -> k -> k^2 -> k^3 -> ...
```

This works because every valid number in the sequence is generated in increasing order. The moment the current value exceeds `l`, we know `l` is impossible.

Even though this approach is already fast enough for the given constraints, there is an even cleaner way to think about the problem. Instead of building powers upward, we can reduce `l` downward.

If `l` is truly a power of `k`, then dividing by `k` repeatedly must eventually reach `1`.

For example:

$125 \to 25 \to 5 \to 1$

Each successful division removes one factor of `k`. If at some point `l` is not divisible by `k`, then the representation is impossible.

This division-based method is simpler because it never risks overflow and naturally gives us the exponent count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(logₖ l) | O(1) | Accepted |
| Optimal | O(logₖ l) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers `k` and `l`.
2. Initialize a counter `cnt = 0`. This counter will track how many times we successfully divide by `k`.
3. While `l` is divisible by `k`, divide `l` by `k` and increment `cnt`.

Each division removes one power of `k` from the number.
4. After the loop finishes, check whether `l == 1`.

If we reached `1`, then the original number was exactly a power of `k`.
5. If `l == 1`, print `"YES"` and print `cnt - 1`.

The exponent itself is `cnt`, but the problem asks for the number of `"la"` words, which is one less.
6. Otherwise, print `"NO"`.

### Why it works

The algorithm maintains the invariant that after each iteration, the current value of `l` equals the original number divided by `k^cnt`.

If the original number was truly:

$l = k^n$

then after exactly `n` divisions we must obtain `1`.

If at some point division is impossible because `l % k != 0`, then at least one prime factor does not belong to `k`, so the number cannot be a pure power of `k`.

Because the loop removes exactly one factor of `k` per iteration, `cnt` becomes the exponent, and `cnt - 1` becomes the required importance.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input())
    l = int(input())

    cnt = 0

    while l % k == 0:
        l //= k
        cnt += 1

    if l == 1:
        print("YES")
        print(cnt - 1)
    else:
        print("NO")

solve()
```

The solution repeatedly removes factors of `k` from `l`.

The loop condition is the key detail:

```
while l % k == 0:
```

We only divide when the division is exact. This prevents invalid states where integer division would silently discard information.

The variable `cnt` stores how many times division succeeded. If the original number was `k^n`, then the loop runs exactly `n` times.

The final subtraction:

```
cnt - 1
```

is easy to miss. The problem does not ask for the exponent itself. It asks for the number of `"la"` connectors in the phrase representation.

No overflow issues exist because division only decreases the value of `l`.

## Worked Examples

### Example 1

Input:

```
5
25
```

Trace:

| Current l | l % k | cnt |
| --- | --- | --- |
| 25 | 0 | 0 |
| 5 | 0 | 1 |
| 1 | stop | 2 |

Final state:

```
l = 1
cnt = 2
```

Output:

```
YES
1
```

This demonstrates that the algorithm correctly identifies:

$25 = 5^2$

and converts exponent `2` into importance `1`.

### Example 2

Input:

```
3
10
```

Trace:

| Current l | l % k | cnt |
| --- | --- | --- |
| 10 | 1 | 0 |

The loop never starts because `10` is not divisible by `3`.

Final state:

```
l = 10
```

Output:

```
NO
```

This example shows why divisibility is the correct criterion. A number that is not divisible by `k` cannot possibly contain only factors of `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(logₖ l) | Each iteration divides `l` by `k` |
| Space | O(1) | Only a few integer variables are used |

Since `l` decreases exponentially with each division, the loop executes at most about 31 times for 32-bit integers. This easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    k = int(input())
    l = int(input())

    cnt = 0

    while l % k == 0:
        l //= k
        cnt += 1

    if l == 1:
        print("YES")
        print(cnt - 1)
    else:
        print("NO")

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run("5\n25\n") == "YES\n1\n", "sample 1"

# minimum valid power
assert run("2\n2\n") == "YES\n0\n", "k^1 should have importance 0"

# not a power
assert run("3\n10\n") == "NO\n", "10 is not a power of 3"

# larger exact power
assert run("2\n1024\n") == "YES\n9\n", "1024 = 2^10"

# boundary style case
assert run("2147483647\n2147483647\n") == "YES\n0\n", "largest value equal to k"

# close but invalid
assert run("4\n63\n") == "NO\n", "63 is not a power of 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2` | `YES 0` | Smallest exponent case |
| `3 10` | `NO` | Non-divisible number |
| `2 1024` | `YES 9` | Multiple successful divisions |
| `2147483647 2147483647` | `YES 0` | Largest valid equal-values case |
| `4 63` | `NO` | Near-power false positive prevention |

## Edge Cases

Consider the case where the exponent is exactly `1`.

Input:

```
7
7
```

Execution:

| Current l | Action | cnt |
| --- | --- | --- |
| 7 | divide by 7 | 1 |
| 1 | stop | 1 |

The algorithm prints:

```
YES
0
```

This correctly handles the difference between exponent and importance.

Now consider a number that partially factors into `k` but not completely.

Input:

```
6
72
```

Execution:

| Current l | Action | cnt |
| --- | --- | --- |
| 72 | divide by 6 | 1 |
| 12 | divide by 6 | 2 |
| 2 | stop | 2 |

The remaining value is `2`, not `1`, so the answer is `"NO"`.

This confirms the invariant that a valid power must reduce completely to `1`.

Finally, consider a very large valid power.

Input:

```
2
1073741824
```

This equals:

$1073741824 = 2^{30}$

The loop performs exactly 30 divisions and prints:

```
YES
29
```

The logarithmic number of iterations keeps the solution extremely fast even near the upper constraint boundary.
