---
title: "CF 102860K - Checkers"
description: "We have two types of checkers: white pieces and black pieces. We need arrange all of them into one vertical tower."
date: "2026-07-25T14:16:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102860
codeforces_index: "K"
codeforces_contest_name: "2020-2021 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 20)"
rating: 0
weight: 102860
solve_time_s: 44
verified: true
draft: false
---

[CF 102860K - Checkers](https://codeforces.com/problemset/problem/102860/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two types of checkers: white pieces and black pieces. We need arrange all of them into one vertical tower. A black stripe is one maximal consecutive block of black pieces, meaning every black piece in the block touches another black piece above or below, and the block is separated from other black blocks by white pieces or by the ends of the tower.

The task is to find the largest possible number of separate black stripes after choosing the best ordering of all pieces.

The input contains the number of white pieces and the number of black pieces. The output is the maximum number of black groups that can be created.

The constraints allow the counts to be extremely large, up to around 10^18. This immediately rules out any simulation, construction of the tower, or dynamic programming over the number of pieces. The solution has to depend only on the mathematical relationship between the two quantities and run in constant time.

The key edge cases come from the fact that white pieces are the separators. For example, if there are no black pieces, there cannot be any black stripe.

Example input:

```
5 0
```

The correct output is:

```
0
```

A solution that always returns at least one stripe would be wrong.

Another important case is having black pieces but no white separators.

Example input:

```
0 3
```

The only possible tower is three black pieces together, so the answer is:

```
1
```

A careless approach that returns the number of black pieces would incorrectly output 3.

A final boundary case is when there are enough white pieces to separate every black piece.

Example input:

```
10 3
```

The three black pieces can be placed as `BWBWB`, with remaining white pieces anywhere else. The answer is:

```
3
```

A solution that only considers the number of white pieces as the answer would fail because the number of stripes cannot exceed the number of black pieces.

## Approaches

The brute-force way would be to try different orders of the pieces and count the resulting stripes. This is correct because every possible arrangement is considered, but the number of possible towers is enormous. With 10^18 pieces, even representing the tower is impossible, so any approach based on enumeration or simulation cannot work.

The useful observation is that a white piece can create at most one separation between two groups of black pieces. If we have `a` white pieces, they can create at most `a + 1` places where black stripes can appear: before the first white piece, between white pieces, and after the last white piece.

At the same time, every stripe must contain at least one black piece. With `b` black pieces, we cannot create more than `b` stripes.

The maximum number of stripes is the smaller of these two limits:

`min(number of black pieces, number of possible gaps created by whites)`

The optimal arrangement simply places black pieces into as many available gaps as possible, using whites as separators.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of arrangements) | O(number of pieces) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of white pieces and black pieces.
2. If there are no black pieces, output `0`, because a stripe must contain at least one black piece.
3. Compute the number of available positions for black stripes. With `a` white pieces, there are `a + 1` possible separated regions in the tower.
4. The answer is the smaller value between the number of black pieces and the number of available regions.

The reason this works is that every stripe consumes at least one black piece, and every separation between stripes requires a white piece. The construction can always achieve this bound by placing one black piece into each chosen region.

Why it works:

Suppose an arrangement has `x` black stripes. Since every stripe contains at least one black piece, `x` cannot be larger than the total number of black pieces. Also, between every pair of consecutive stripes there must be at least one white piece, so `x` stripes need at least `x - 1` white separators. This means the number of stripes cannot exceed `a + 1`. Since both restrictions are necessary, the answer cannot exceed `min(b, a + 1)`. We can always achieve exactly that many stripes by placing one black piece into each available region until either the black pieces or regions run out.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())

    if b == 0:
        print(0)
    else:
        print(min(b, a + 1))

if __name__ == "__main__":
    solve()
```

The solution reads the two counts directly and never tries to build the tower. This is necessary because the values can be far too large for iteration.

The special handling of `b == 0` is not strictly required in Python because `min(0, a + 1)` would also produce zero, but keeping the condition makes the reasoning explicit. The expression `a + 1` is safe because Python integers have arbitrary precision.

## Worked Examples

### Sample 1

Input:

```
1 2
```

The key variables evolve as follows:

| Step | White pieces | Black pieces | Available regions | Answer |
| --- | --- | --- | --- | --- |
| Initial | 1 | 2 | 2 | 2 |
| Apply minimum | 1 | 2 | 2 | 2 |

There is one white piece, so the tower can have two black regions. Since there are also two black pieces, both regions can receive one black piece.

### Sample 2

Input:

```
5 2
```

| Step | White pieces | Black pieces | Available regions | Answer |
| --- | --- | --- | --- | --- |
| Initial | 5 | 2 | 6 | 2 |
| Apply minimum | 5 | 2 | 6 | 2 |

There are many possible separators, but only two black pieces exist. Each black piece can form its own stripe, so the answer is two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No additional data structures are used |

The solution only depends on two integers, so it easily fits the limits even when the values are as large as 10^18.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

def solve():
    a, b = map(int, sys.stdin.readline().split())
    if b == 0:
        print(0)
    else:
        print(min(b, a + 1))

# provided samples
assert run("1 2\n") == "2\n", "sample 1"
assert run("5 2\n") == "2\n", "sample 2"
assert run("0 3\n") == "1\n", "sample 3"

# custom cases
assert run("0 0\n") == "0\n", "no pieces"
assert run("1000000000000000000 1\n") == "1\n", "huge whites"
assert run("1 1000000000000000000\n") == "2\n", "huge blacks"
assert run("10 10\n") == "10\n", "enough separators"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `0` | No black pieces means no stripes |
| `1000000000000000000 1` | `1` | Very large values and one black piece |
| `1 1000000000000000000` | `2` | Stripe count limited by available gaps |
| `10 10` | `10` | Every black piece can become its own stripe |

## Edge Cases

For the case with no black pieces:

```
0 0
```

The algorithm sees `b == 0` and returns zero immediately. There is no possible black stripe because the tower contains no black pieces.

For the case with no white pieces:

```
0 3
```

The number of available regions is `0 + 1 = 1`. The formula becomes `min(3, 1)`, giving `1`. All black pieces must stay connected because there is no white separator.

For the case where white pieces are abundant:

```
10 3
```

There are `10 + 1 = 11` possible regions, but only three black pieces. The answer is `min(3, 11) = 3`. Each black piece can occupy a different region, creating three separate stripes.

For the case where black pieces are abundant but separators are limited:

```
2 10
```

There are only `2 + 1 = 3` possible regions. Even though ten black pieces exist, they can form at most three stripes, so the output is:

```
3
```

The algorithm handles this by applying both limits instead of considering only one side.
