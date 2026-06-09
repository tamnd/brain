---
title: "CF 2047A - Alyona and a Square Jigsaw Puzzle"
description: "Alyona builds a square puzzle layer by layer around a central piece. The first layer consists of only the center piece, so it contains 1 tile. Every later layer forms a complete square ring around the previous puzzle. Each day she adds some number of pieces, given by the array a."
date: "2026-06-09T03:34:37+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2047
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 990 (Div. 2)"
rating: 800
weight: 2047
solve_time_s: 132
verified: true
draft: false
---

[CF 2047A - Alyona and a Square Jigsaw Puzzle](https://codeforces.com/problemset/problem/2047/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

Alyona builds a square puzzle layer by layer around a central piece.

The first layer consists of only the center piece, so it contains 1 tile. Every later layer forms a complete square ring around the previous puzzle. Each day she adds some number of pieces, given by the array `a`.

Alyona is happy at the end of a day if the total number of pieces assembled so far exactly completes some square layer. If she finishes a layer and immediately starts the next one on the same day, she is not happy, because an unfinished layer already exists at the end of that day.

We are given the number of pieces placed each day and must count how many days end exactly at a layer boundary.

The key observation comes from the geometry of square layers. After finishing several layers, the assembled puzzle is always a complete square. The total number of pieces after finishing layer `k` is

$$1, 9, 25, 49, 81, \dots$$

These are exactly the odd squares:

$$1^2,\; 3^2,\; 5^2,\; 7^2,\dots$$

So a day is happy precisely when the cumulative number of placed pieces is an odd perfect square.

The constraints are very small. Each test case has at most 100 days, and there are at most 500 test cases. Even an algorithm that performs a small amount of work per day is easily fast enough. The challenge is recognizing the mathematical pattern behind the square layers.

A common mistake is to check whether the cumulative number of pieces is any perfect square. Only odd squares correspond to completed layers.

Consider:

```
1
2
1 3
```

The cumulative sums are `1` and `4`. While `4` is a perfect square, it is not an odd square, so the second day is not happy. The correct answer is:

```
1
```

Another easy mistake is to count a day whenever a layer is completed during that day's additions. Happiness depends on the state at the end of the day.

For example:

```
1
2
1 10
```

The cumulative sums are `1` and `11`. Day 2 passes through `9`, which completes a layer, but ends at `11`, where the next layer has already started. The correct answer is:

```
1
```

## Approaches

A brute-force solution can simulate the layer sizes directly.

The center contributes 1 piece. The next layers contribute:

$$8,\;16,\;24,\;32,\dots$$

because the perimeter added by the square ring of side length $2k+1$ is $8k$.

We could keep generating layer boundaries and, after each day, check whether the cumulative number of pieces equals one of them. This is correct because layer boundaries are exactly the totals after finishing each ring.

Even though this works for the given constraints, it relies on explicitly generating geometric layer information.

The more elegant observation is that completed layers always form squares of odd side length:

$$1 \times 1,\; 3 \times 3,\; 5 \times 5,\; 7 \times 7,\dots$$

Hence the total number of pieces at a completed layer is:

$$1^2,\;3^2,\;5^2,\;7^2,\dots$$

The problem immediately becomes:

"Count how many prefix sums are odd perfect squares."

Since the maximum possible total number of pieces is only $100 \times 100 = 10000$, we can precompute all odd squares up to 10000 and check membership in a set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n + number of layers) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Precompute all odd perfect squares up to 10000 and store them in a set.
2. For each test case, initialize a running prefix sum `s = 0`.
3. Process the days in order.
4. Add the number of pieces placed on the current day to `s`.
5. Check whether `s` belongs to the set of odd squares.
6. If it does, increment the answer because the puzzle ends exactly at a completed layer.
7. After all days are processed, output the answer.

### Why it works

A completed puzzle layer always forms a square whose side length is odd. After finishing the first layer we have $1^2$ pieces, after finishing the second layer we have $3^2$ pieces, after finishing the third layer we have $5^2$ pieces, and so on.

Conversely, every odd square corresponds to a completely finished collection of layers. Thus a day is happy exactly when the cumulative number of placed pieces equals an odd square. The algorithm counts precisely those days, so it cannot overcount or undercount.

## Python Solution

```python
import sys
input = sys.stdin.readline

# all possible totals are at most 100 * 100 = 10000
odd_squares = set()
k = 1
while k * k <= 10000:
    odd_squares.add(k * k)
    k += 2

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    s = 0
    ans = 0

    for x in a:
        s += x
        if s in odd_squares:
            ans += 1

    print(ans)
```

The first section precomputes every odd square that can possibly appear as a prefix sum. Since the total number of pieces never exceeds 10000, only odd squares up to that limit are needed.

For each test case, the variable `s` stores the cumulative number of pieces assembled so far. After processing a day, we check whether this cumulative total equals an odd square.

Using a set makes membership checks constant time on average. No square-root calculations are needed, which keeps the implementation simple and avoids any floating-point concerns.

The boundary conditions are straightforward. The first day always contributes exactly one piece, so the first prefix sum is `1`, which is correctly recognized as the first odd square.

## Worked Examples

### Example 1

Input:

```
n = 5
a = [1, 3, 2, 1, 2]
```

| Day | Pieces Added | Prefix Sum | Odd Square? | Happy Days |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | Yes | 1 |
| 2 | 3 | 4 | No | 1 |
| 3 | 2 | 6 | No | 1 |
| 4 | 1 | 7 | No | 1 |
| 5 | 2 | 9 | Yes | 2 |

The prefix sums hit the odd squares `1` and `9`. Those correspond to completed layers, so the answer is 2.

### Example 2

Input:

```
n = 2
a = [1, 8]
```

| Day | Pieces Added | Prefix Sum | Odd Square? | Happy Days |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | Yes | 1 |
| 2 | 8 | 9 | Yes | 2 |

The second layer contains exactly 8 pieces. Adding them after the center reaches a total of 9 pieces, which is $3^2$. Both days are happy.

This example illustrates the geometric interpretation directly: each completed layer corresponds to an odd square.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass through the days |
| Space | O(1) | The set of odd squares has fixed size |

The maximum total work is tiny. Even with 500 test cases and 100 days per test case, only 50,000 prefix sums are examined. The solution comfortably fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    odd_squares = set()
    k = 1
    while k * k <= 10000:
        odd_squares.add(k * k)
        k += 2

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        s = 0
        ans = 0

        for x in a:
            s += x
            if s in odd_squares:
                ans += 1

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run(
"""5
1
1
2
1 8
5
1 3 2 1 2
7
1 2 1 10 2 7 2
14
1 10 10 100 1 1 10 1 10 2 10 2 10 1
"""
) == """1
2
2
2
3"""

# minimum size
assert run(
"""1
1
1
"""
) == "1"

# reaches 9 exactly
assert run(
"""1
2
1 8
"""
) == "2"

# hits even square but not odd square
assert run(
"""1
2
1 3
"""
) == "1"

# maximum style boundary, final total 81
assert run(
"""1
2
1 80
"""
) == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `1` | Smallest possible case |
| `1 / 2 / 1 8` | `2` | Completion of second layer |
| `1 / 2 / 1 3` | `1` | Even perfect squares must not count |
| `1 / 2 / 1 80` | `2` | Larger odd square boundary |

## Edge Cases

Consider:

```
1
2
1 3
```

The prefix sums are `1` and `4`. A careless solution that checks for any perfect square would count both days. The algorithm checks membership in the set of odd squares, so only `1` counts. The output is:

```
1
```

Consider:

```
1
2
1 10
```

The prefix sums are `1` and `11`. During day 2 the running total passes through `9`, but the day ends at `11`. Happiness depends only on the final state of the day. Since `11` is not an odd square, the algorithm counts only the first day:

```
1
```

Consider:

```
1
2
1 8
```

The prefix sums are `1` and `9`. Both are odd squares, corresponding to fully completed layers. The algorithm counts both days and outputs:

```
2
```

This confirms that exact layer boundaries are recognized correctly, including the transition from one completed square to the next.
