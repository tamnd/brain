---
title: "CF 1130A - Be Positive"
description: "We are given an array containing positive numbers, negative numbers, and possibly zeros. We need to choose a non-zero integer $d$ such that after dividing every element by $d$, at least half of the array elements are positive."
date: "2026-06-12T04:16:47+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1130
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 542 [Alex Lopashev Thanks-Round] (Div. 2)"
rating: 800
weight: 1130
solve_time_s: 112
verified: false
draft: false
---

[CF 1130A - Be Positive](https://codeforces.com/problemset/problem/1130/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array containing positive numbers, negative numbers, and possibly zeros. We need to choose a non-zero integer $d$ such that after dividing every element by $d$, at least half of the array elements are positive. More precisely, the number of positive values after division must be at least $\lceil n/2 \rceil$.

The actual magnitudes after division do not matter. Only the sign matters. A value such as $2.5$ is still positive, while $0$ remains neither positive nor negative.

The constraints are very small. The array contains at most 100 elements, and every value lies between $-1000$ and $1000$. With only 100 numbers, even a brute-force examination of the array is trivial.

The key observation comes from how division affects signs. Dividing by a positive number keeps every sign unchanged. Dividing by a negative number flips every positive number into a negative one and every negative number into a positive one. Zeros remain zero in either case.

Several edge cases can easily cause mistakes.

Consider:

```
3
0 0 5
```

If we divide by a positive number, the array signs remain $(0,0,+)$, so there is only one positive value. Since $\lceil 3/2 \rceil = 2$, this is not enough. A careless solution that ignores zeros might incorrectly conclude that positives are a majority.

Consider:

```
5
-1 -2 -3 0 0
```

Using a negative divisor flips the three negatives into positives, giving three positive values. The correct answer is $-1$. A solution that only checks positive divisors would incorrectly print 0.

Consider:

```
4
1 -1 0 0
```

There is one positive and one negative. A positive divisor yields one positive number. A negative divisor also yields one positive number. We need at least two positives, so the correct answer is 0.

The presence of many zeros is the main subtlety because zeros never become positive regardless of the divisor.

## Approaches

A brute-force approach would try every valid divisor from $-1000$ to $1000$, excluding zero. For each divisor, we would divide every array element and count how many results are positive.

This works because the search space is tiny. There are only 2000 possible divisors and at most 100 array elements. The worst-case work is about $2000 \times 100 = 200{,}000$ operations, which easily fits within the limits.

The interesting part is noticing that the exact value of the divisor is irrelevant. Only its sign matters.

If $d > 0$, every positive element stays positive and every negative element stays negative.

If $d < 0$, every positive element becomes negative and every negative element becomes positive.

That means there are only two distinct situations to check:

First, use a positive divisor. The number of positive values equals the count of positive elements in the original array.

Second, use a negative divisor. The number of positive values equals the count of negative elements in the original array.

Let:

- $pos$ be the number of positive elements.
- $neg$ be the number of negative elements.
- $need = \lceil n/2 \rceil$.

If $pos \ge need$, we can print any positive divisor, for example 1.

Otherwise, if $neg \ge need$, we can print any negative divisor, for example -1.

Otherwise neither sign choice can produce enough positive values, so we print 0.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2000·n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array and count how many elements are positive. Store this count in `pos`.
2. Count how many elements are negative. Store this count in `neg`.
3. Compute the required number of positive values:

$$need = \left\lceil \frac{n}{2} \right\rceil$$

In integer arithmetic this is `(n + 1) // 2`.
4. If `pos >= need`, print `1`.

A positive divisor preserves all signs, so the number of positive values after division is exactly `pos`.
5. Otherwise, if `neg >= need`, print `-1`.

A negative divisor flips signs, so every negative element becomes positive. The number of positive values becomes exactly `neg`.
6. Otherwise print `0`.

Neither sign choice can produce enough positive values.

### Why it works

The sign of every non-zero quotient depends only on the sign of the dividend and the sign of the divisor. The divisor's magnitude never affects whether a result is positive.

Using a positive divisor preserves the original sign distribution, producing exactly `pos` positive values. Using a negative divisor swaps positive and negative counts, producing exactly `neg` positive values. Since these are the only two possible outcomes, checking whether either count reaches $\lceil n/2 \rceil$ completely characterizes all valid answers. If neither count is large enough, no divisor can satisfy the requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

pos = sum(1 for x in a if x > 0)
neg = sum(1 for x in a if x < 0)

need = (n + 1) // 2

if pos >= need:
    print(1)
elif neg >= need:
    print(-1)
else:
    print(0)
```

The first part counts positive and negative elements separately. Zeros are ignored because they never contribute to the number of positive values after division.

The variable `need` stores $\lceil n/2 \rceil$. Using `(n + 1) // 2` correctly handles both even and odd values of `n`.

The order of checks matters only for choosing which valid answer to print when both counts satisfy the requirement. The problem allows any valid divisor, so printing `1` first is perfectly acceptable.

No actual division is performed. The solution relies entirely on sign behavior, which is the key simplification.

## Worked Examples

### Example 1

Input:

```
5
10 0 -7 2 6
```

Here `need = (5 + 1) // 2 = 3`.

| Element | Positive Count | Negative Count |
| --- | --- | --- |
| 10 | 1 | 0 |
| 0 | 1 | 0 |
| -7 | 1 | 1 |
| 2 | 2 | 1 |
| 6 | 3 | 1 |

Final values:

| Variable | Value |
| --- | --- |
| pos | 3 |
| neg | 1 |
| need | 3 |

Since `pos >= need`, we print:

```
1
```

This demonstrates that any positive divisor works because the original array already contains enough positive elements.

### Example 2

Input:

```
5
-1 -2 -3 0 0
```

Here `need = 3`.

| Element | Positive Count | Negative Count |
| --- | --- | --- |
| -1 | 0 | 1 |
| -2 | 0 | 2 |
| -3 | 0 | 3 |
| 0 | 0 | 3 |
| 0 | 0 | 3 |

Final values:

| Variable | Value |
| --- | --- |
| pos | 0 |
| neg | 3 |
| need | 3 |

`pos` is insufficient, but `neg >= need`, so we print:

```
-1
```

A negative divisor flips the three negative numbers into positives, reaching the required count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass through the array |
| Space | O(1) | Only a few counters are stored |

With at most 100 elements, the algorithm runs essentially instantly. The memory usage is constant and far below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    pos = sum(1 for x in a if x > 0)
    neg = sum(1 for x in a if x < 0)

    need = (n + 1) // 2

    if pos >= need:
        print(1)
    elif neg >= need:
        print(-1)
    else:
        print(0)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    result = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return result

# sample-style case
assert run("5\n10 0 -7 2 6\n") == "1"

# minimum size, positive
assert run("1\n5\n") == "1"

# minimum size, negative
assert run("1\n-5\n") == "-1"

# impossible because zeros dominate
assert run("4\n1 -1 0 0\n") == "0"

# all negatives
assert run("5\n-1 -2 -3 -4 -5\n") == "-1"

# all positives
assert run("6\n1 1 1 1 1 1\n") == "1"

# boundary count exactly equal to need
assert run("5\n1 2 3 0 -1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5` | `1` | Minimum-size positive array |
| `1 / -5` | `-1` | Minimum-size negative array |
| `4 / 1 -1 0 0` | `0` | Zeros preventing a majority |
| `5 / all negatives` | `-1` | Sign-flipping via negative divisor |
| `6 / all positives` | `1` | Positive divisor case |
| `5 / 1 2 3 0 -1` | `1` | Exact threshold equality |

## Edge Cases

Consider:

```
4
1 -1 0 0
```

We have:

```
pos = 1
neg = 1
need = 2
```

A positive divisor yields one positive value. A negative divisor also yields one positive value. Neither reaches two, so the algorithm prints:

```
0
```

This correctly handles arrays where zeros occupy too much of the array.

Consider:

```
5
-1 -2 -3 0 0
```

The counts are:

```
pos = 0
neg = 3
need = 3
```

Since `neg` reaches the threshold, the algorithm prints `-1`. Dividing by a negative number turns all three negatives into positives, satisfying the requirement.

Consider:

```
3
0 0 5
```

The counts are:

```
pos = 1
neg = 0
need = 2
```

Neither count reaches the threshold, so the algorithm prints:

```
0
```

This confirms that zeros never help increase the number of positive values, regardless of the divisor chosen.
