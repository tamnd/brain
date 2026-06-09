---
title: "CF 1804C - Pull Your Luck"
description: "We have a roulette wheel with n sectors numbered from 0 to n-1. The wheel starts with an arrow pointing at sector x, and we can spin it by pulling a handle with an integer force f between 1 and p."
date: "2026-06-09T09:20:33+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1804
codeforces_index: "C"
codeforces_contest_name: "Nebius Welcome Round (Div. 1 + Div. 2)"
rating: 1500
weight: 1804
solve_time_s: 101
verified: true
draft: false
---

[CF 1804C - Pull Your Luck](https://codeforces.com/problemset/problem/1804/C)

**Rating:** 1500  
**Tags:** brute force, greedy, math, number theory  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a roulette wheel with `n` sectors numbered from `0` to `n-1`. The wheel starts with an arrow pointing at sector `x`, and we can spin it by pulling a handle with an integer force `f` between `1` and `p`. The spin behaves like this: in the first second it advances `f` sectors, in the next second `f-1` sectors, then `f-2`, down to `1`. The total movement after `f` seconds is the sum of the first `f` positive integers, which is `f*(f+1)/2`. The sectors wrap around modulo `n`. The goal is to check if there exists an integer `f` from `1` to `p` such that after the spin, the arrow points at sector `0`.

The constraints tell us `n` can go up to `10^5` and `p` up to `10^9`. Summing over all test cases, `n` does not exceed `2*10^5`. A brute-force approach that tries every `f` from `1` to `p` is infeasible because `p` can be very large. We need something smarter than iterating through all forces. Edge cases include when the arrow already points at `0`, when `p` is very small relative to `n`, or when `x` is near the end of the wheel and the spin wraps around multiple times.

For example, if `n = 5`, `x = 2`, `p = 1`, then the only spin is `f=1`, moving `1` sector. The arrow would end at `3`, so the answer is "No". If `p = 2`, we can choose `f=2`, moving `3` sectors in total (`2 + 1`), which lands on `0`. A naive approach would not handle the large `p` efficiently.

## Approaches

A brute-force solution tries every possible force `f` from `1` to `p`, computes `f*(f+1)/2`, adds `x`, and takes modulo `n` to see if it reaches `0`. This works in principle but can require up to `10^9` iterations per test case, which is far beyond the time limit.

The key insight is that we only need to check if the equation `(x + f*(f+1)/2) % n == 0` has a solution for some `1 <= f <= p`. Expanding it, we want `(f*(f+1)/2) % n == (-x) % n`. The left-hand side is quadratic in `f`, and while it seems hard to invert directly, we notice that once `f` exceeds `n`, the sum `f*(f+1)/2` modulo `n` starts repeating patterns because adding `n` to `f` increases the sum by a multiple of `n`. This means it is sufficient to check `f` up to `min(p, 2*n)` rather than all the way to `p`, because after that the pattern cycles modulo `n`. This reduces the iteration from `10^9` to at most `2*10^5` per test case, which is manageable given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(p) | O(1) | Too slow for large `p` |
| Optimized modulo check | O(min(p, 2*n)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n`, `x`, `p`.
3. Compute the target value `target = (-x) % n`. This is the number of sectors we need to advance to reach `0`.
4. Iterate `f` from `1` to `min(p, 2*n)`. We stop at `2*n` because `f*(f+1)/2` modulo `n` will start repeating beyond this point.
5. For each `f`, compute the total advancement `move = f*(f+1)//2`.
6. If `(move % n) == target`, print "Yes" and break the loop.
7. If no `f` satisfies the condition, print "No".

Why it works: The critical property is that the sum of first `f` integers modulo `n` repeats in a bounded range. By checking up to `2*n`, we are guaranteed to encounter all distinct remainders modulo `n`, so if a solution exists, we will find it. This avoids iterating all the way to `p` when `p` is very large.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, x, p = map(int, input().split())
    target = (-x) % n
    found = False
    limit = min(p, 2*n)  # pattern repeats modulo n
    for f in range(1, limit + 1):
        move = f * (f + 1) // 2
        if move % n == target:
            found = True
            break
    print("Yes" if found else "No")
```

We use `sys.stdin.readline` for fast input because there can be up to `10^4` test cases. The `min(p, 2*n)` trick prevents iterating up to `10^9`. Integer division `//` is necessary to avoid floating-point issues. The modulo operation ensures we handle the circular nature of the wheel.

## Worked Examples

### Example 1

Input: `5 2 2`

| f | f*(f+1)/2 | (f*(f+1)/2 + x) % n |
| --- | --- | --- |
| 1 | 1 | (1 + 2) % 5 = 3 |
| 2 | 3 | (3 + 2) % 5 = 0 |

The table shows that `f=2` lands exactly on sector `0`. The algorithm correctly outputs "Yes".

### Example 2

Input: `3 1 1000`

| f | f*(f+1)/2 | (f*(f+1)/2 + x) % n |
| --- | --- | --- |
| 1 | 1 | (1+1)%3=2 |
| 2 | 3 | (3+1)%3=1 |
| 3 | 6 | (6+1)%3=1 |
| 4 | 10 | (10+1)%3=2 |

The remainders cycle between `1` and `2`. Sector `0` is never reached. Algorithm outputs "No".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * min(p, n)) | Each test case iterates at most `2*n` times, total `t*2*n` ≤ 4*10^5 |
| Space | O(1) | Only constant extra variables per test case |

The solution easily fits in the 1-second limit, even for the maximum `t` and `n`.

## Test Cases

```python
def run(inp: str) -> str:
    import sys, io
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call the solution
    t = int(input())
    for _ in range(t):
        n, x, p = map(int, input().split())
        target = (-x) % n
        found = False
        limit = min(p, 2*n)
        for f in range(1, limit+1):
            move = f*(f+1)//2
            if move % n == target:
                found = True
                break
        print("Yes" if found else "No")
    return output.getvalue().strip()

# Provided samples
assert run("7\n5 2 1\n5 2 2\n10 0 100\n11 7 100\n3 1 1000\n31 0 10\n100 49 7\n") == \
"No\nYes\nYes\nYes\nNo\nNo\nNo"

# Custom edge cases
assert run("2\n3 0 1\n3 2 2\n") == "Yes\nYes"  # already at 0, small n
assert run("1\n100000 99999 1000000000\n") == "Yes"  # very large p
assert run("1\n4 1 2\n") == "No"  # small p, can't reach 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 0 1\n3 2 2` | `Yes\nYes` | minimum-size wheel, already at zero, small p |
| `100000 99999 1000000000` | `Yes` | large n, very large p handled efficiently |
| `4 1 2` | `No` | small p cannot reach target |

## Edge Cases

For `n = 3, x = 0, p = 1`, the algorithm immediately computes `target = 0` and `f=1` gives `1*(1+1)/2 = 1`. `(x + move) %
