---
title: "CF 1716A - 2-3 Moves"
description: "We are standing at position 0 on a number line, and we want to reach a target coordinate n. In one minute, we can move either 2 or 3 units in either direction. The task is to compute the minimum number of minutes needed to reach n exactly."
date: "2026-06-09T19:51:20+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1716
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 133 (Rated for Div. 2)"
rating: 800
weight: 1716
solve_time_s: 130
verified: true
draft: false
---

[CF 1716A - 2-3 Moves](https://codeforces.com/problemset/problem/1716/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are standing at position 0 on a number line, and we want to reach a target coordinate `n`. In one minute, we can move either 2 or 3 units in either direction. The task is to compute the minimum number of minutes needed to reach `n` exactly. The input consists of `t` test cases, each giving a single integer `n`. For each `n`, we must print the fewest number of moves required.

The key constraints are that `n` can be as large as $10^9$ and there are up to $10^4$ test cases. This rules out any solution that iterates over positions or tries every sequence of moves explicitly because that would be far too slow. Instead, we need an approach that works in constant or logarithmic time per test case.

A subtle edge case is when `n` is small, particularly `1`. Since we can only move in increments of 2 or 3, we cannot reach 1 in a single move. The minimum number of moves would then be 2: either go 2 forward then 1 backward, or 3 forward then 2 backward, resulting in exactly 1. Similarly, all numbers not divisible by 2 or 3 must be handled carefully. A naive `n // 3` or `n // 2` calculation would fail for these small offsets.

## Approaches

The brute-force approach is to simulate every combination of moves until we reach `n`. This works by trying all sequences of 2s and 3s until the sum equals `n`. It is correct because eventually, any integer can be reached by adding some combination of 2s and 3s. However, its complexity is exponential. If `n` is $10^9$, this would take far too long.

The key insight comes from modular arithmetic. Every number can be expressed as a combination of 2s and 3s because the greatest common divisor of 2 and 3 is 1. That guarantees reachability. To minimize the number of moves, we prefer the largest possible move, 3, first, and then fill the remainder with 2s.

Specifically, for a given `n`, we can estimate `n // 3` moves of 3. If the remainder is 0, we are done. If the remainder is 1, we need to replace one 3 with two 2s, which increases the total moves by 1. If the remainder is 2, we simply add one more 2 move. This logic works for all positive integers, small or large, and runs in constant time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`. The goal is to compute the minimum number of moves to reach `n` from 0 using moves of size 2 or 3.
2. Compute `q` as `n // 3` and `r` as `n % 3`. Here `q` represents the maximum number of 3-unit moves, and `r` is the leftover distance we still need to cover.
3. If `r` is 0, the answer is simply `q` because the 3-unit moves cover exactly `n`.
4. If `r` is 1, we cannot cover it with a single 2-unit move, so we reduce one 3-unit move to create space, then use two 2-unit moves to cover the leftover distance. This increases the move count by 1.
5. If `r` is 2, we can cover it with one extra 2-unit move, so the total moves are `q + 1`.

Why it works: Every integer is reachable using some combination of 2s and 3s. By maximizing 3-unit moves first, we minimize the total move count. Adjustments based on the remainder ensure the leftover distance is covered optimally. The formula guarantees that we never underestimate the number of moves because any leftover is corrected either by adding 2s or replacing a 3 with two 2s.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    q, r = divmod(n, 3)
    if r == 0:
        print(q)
    elif r == 1:
        if q >= 1:
            print(q + 1)  # replace one 3 with two 2s
        else:
            print(2)      # n=1 or n=1 scenario
    else:  # r == 2
        print(q + 1)
```

The `divmod` function splits `n` into a quotient and remainder efficiently. We check the remainder and adjust the moves accordingly. A subtlety is handling very small `n` values (like 1) where there are not enough 3-unit moves to swap, so we manually return 2 moves in that scenario.

## Worked Examples

### Example 1: n = 1

| n | q | r | computed moves |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 2 |

Explanation: We cannot reach 1 with a single move, so we need two moves: +2 then -1. The algorithm handles this via the `q < 1` branch.

### Example 2: n = 12

| n | q | r | computed moves |
| --- | --- | --- | --- |
| 12 | 4 | 0 | 4 |

Explanation: 12 can be covered with 4 moves of size 3. No remainder, so no extra adjustment is needed.

### Example 3: n = 4

| n | q | r | computed moves |
| --- | --- | --- | --- |
| 4 | 1 | 1 | 2 |

Explanation: One move of 3 covers 3 units. The remainder 1 is handled by replacing the 3 with two 2s. Total moves: 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | All operations are arithmetic and conditionals. |
| Space | O(1) | Only a few integers are stored. |

Given up to $10^4$ test cases, this runs in $10^4$ operations at most, which is well within the 1-second time limit. Memory use is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    for _ in range(t):
        n = int(input())
        q, r = divmod(n, 3)
        if r == 0:
            print(q)
        elif r == 1:
            if q >= 1:
                print(q + 1)
            else:
                print(2)
        else:
            print(q + 1)
    
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("4\n1\n3\n4\n12\n") == "2\n1\n2\n4", "Sample 1"

# Custom cases
assert run("3\n2\n5\n7\n") == "1\n2\n3", "Small numbers"
assert run("2\n10\n1000000000\n") == "4\n333333334", "Large numbers"
assert run("1\n1\n") == "2", "Minimum input"
assert run("1\n2\n") == "1", "Minimum 2 reachable in one move"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 5 7 | 1 2 3 | Small numbers with remainders |
| 10 1000000000 | 4 333333334 | Correctness for very large numbers |
| 1 | 2 | Minimum input edge case |
| 2 | 1 | Minimum input that is reachable in one move |

## Edge Cases

For `n = 1`, the algorithm chooses 2 moves, correctly handling the impossibility of reaching 1 with a single move. For `n = 2`, it directly returns 1, showing that small numbers are correctly mapped to minimal moves. For `n = 4`, it replaces a single 3-unit move with two 2-unit moves, producing the minimum move count. The `divmod` approach with remainder adjustment guarantees correctness across all edge cases up to $10^9$.

This editorial presents a concrete, fast, and reliable way to compute the minimal number of moves for any positive integer `n` using only arithmetic, avoiding any brute-force search.
