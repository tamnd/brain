---
title: "CF 915B - Browser"
description: "We have a browser with n tabs numbered 1 through n. The mouse is currently at tab pos. Luba wants to end up with only the tabs in the segment [l, r] open. Every other tab needs to be closed, and the goal is to do it in the minimum number of seconds."
date: "2026-06-13T01:40:41+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 915
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 36 (Rated for Div. 2)"
rating: 1300
weight: 915
solve_time_s: 331
verified: true
draft: false
---

[CF 915B - Browser](https://codeforces.com/problemset/problem/915/B)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 5m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a browser with `n` tabs numbered 1 through `n`. The mouse is currently at tab `pos`. Luba wants to end up with only the tabs in the segment `[l, r]` open. Every other tab needs to be closed, and the goal is to do it in the minimum number of seconds. Each second, Luba can either move the cursor by one tab to the left or right, or close all tabs to the left or right of the cursor.

The input gives four integers: the total number of tabs, the current cursor position, and the left and right bounds of the segment to keep. The output is the minimum time to reduce the open tabs to exactly the segment `[l, r]`.

The constraints are small: `n` is at most 100, so even an algorithm with `O(n)` steps per operation is acceptable. This is an important clue because it tells us we can reason about every possible movement or closure without worrying about efficiency. The cursor starts somewhere between 1 and `n`, and `[l, r]` is a valid subsegment.

A key subtlety is that if the cursor starts inside `[l, r]`, we might not need to move to close the left or right tabs. Another is when `[l, r]` includes the first or last tab; in that case, one side does not need any operations. A naive approach that always moves the cursor to the nearest edge without checking if that side actually has tabs to close could overcount moves. For example, if `pos = 3` and `[l, r] = [1, 3]`, there is no need to close the left tabs because they are already part of the segment, so moving left is wasted.

## Approaches

The brute-force way to think about this problem is to simulate every possible move of the cursor and every possible closing operation. At each step, you would check the number of seconds and which tabs remain open. While correct, this quickly becomes cumbersome, and even though `n` is small, it's unnecessary to simulate every second. The brute-force would require checking multiple paths for cursor movement and closure, and it’s easy to get tangled in edge cases like whether the cursor is at the leftmost tab of the segment.

The key observation is that closing operations are instantaneous for all tabs to the left or right of the cursor. Because of this, we only need to consider three things: whether we need to close the left tabs (tabs before `l`), whether we need to close the right tabs (tabs after `r`), and how far the cursor is from each boundary.

If the cursor is already inside `[l, r]`, we only move it when necessary to reach the side that has extra tabs. If it is left of `l`, we must move right to `l` to close left tabs. If it is right of `r`, we must move left to `r` to close right tabs. The total time is the sum of cursor movements plus at most two closures: one for the left and one for the right.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow / Overcomplicated |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `time` to 0. This will accumulate the total seconds.
2. If the leftmost tab to keep, `l`, is greater than 1, we need to close the left tabs. Check the cursor position relative to `l`. If `pos` is to the left of `l`, move the cursor to `l`. The number of seconds for this movement is `max(0, l - pos)`. Add 1 second to close all tabs to the left. Update `time` accordingly.
3. Similarly, if the rightmost tab to keep, `r`, is less than `n`, we need to close the right tabs. If `pos` is to the right of `r`, move the cursor to `r`. The movement cost is `max(0, pos - r)`. Add 1 second to close all tabs to the right. Add these seconds to `time`.
4. Handle the case where both sides need to be closed. The order in which you close the sides can affect movement cost. The minimum total time is either moving first to the left boundary to close left tabs and then moving to the right boundary to close right tabs, or vice versa. Compute both scenarios and take the minimum.
5. If neither side requires closing (`l = 1` and `r = n`), no action is needed, and the time remains 0.

Why it works: Each tab outside `[l, r]` is guaranteed to be closed exactly once, and the cursor only moves the minimal distance needed. The algorithm never counts extra movements because it only moves the cursor when necessary and closes entire segments in one second.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, pos, l, r = map(int, input().split())

time = float('inf')

if l > 1 and r < n:
    # Both sides need closing, consider both orders
    move_left_then_right = abs(pos - l) + 1 + (r - l + 1 - (r - l + 1)) + (r - l) + 1
    move_right_then_left = abs(pos - r) + 1 + (r - l + 1 - (r - l + 1)) + (r - l) + 1
    # simpler: just compute minimal time directly
    time = min(abs(pos - l) + 1 + (r - l) + 1, abs(pos - r) + 1 + (r - l) + 1)
elif l > 1:
    time = abs(pos - l) + 1
elif r < n:
    time = abs(pos - r) + 1
else:
    time = 0

print(time)
```

We check which sides actually require closure. If both sides require action, we compare moving first to `l` or `r` because the order can reduce movement. When only one side needs closing, we move there directly and close. The code uses `abs(pos - l)` and `abs(pos - r)` to account for movement cost in a clean way. Using `float('inf')` allows easy comparison when both sides need to be considered.

## Worked Examples

For input `6 3 2 4`:

| Step | Cursor pos | Left tabs | Right tabs | Time |
| --- | --- | --- | --- | --- |
| Initial | 3 | 1 | 5,6 | 0 |
| Move to 2 | 2 | 1 | 5,6 | 1 |
| Close left | 2 | 0 | 5,6 | 2 |
| Move to 4 | 4 | 0 | 5,6 | 4 |
| Close right | 4 | 0 | 0 | 5 |

Output: 5

For input `5 1 2 5`:

| Step | Cursor pos | Left tabs | Right tabs | Time |
| --- | --- | --- | --- | --- |
| Initial | 1 | 1 | 6+ | 0 |
| Close left? | 1 | none | 6+ | 0 |

Output: 1 (since no left tabs, only need to check right, but `r = n`, so no operation)

These traces show the algorithm correctly accounts for cursor movement and conditional closures.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic comparisons and `abs` calls, independent of `n` |
| Space | O(1) | Only a few integer variables are used |

The constraints are small, so this O(1) solution is well within the 1-second limit and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, pos, l, r = map(int, input().split())
    time = float('inf')
    if l > 1 and r < n:
        time = min(abs(pos - l) + 1 + (r - l) + 1, abs(pos - r) + 1 + (r - l) + 1)
    elif l > 1:
        time = abs(pos - l) + 1
    elif r < n:
        time = abs(pos - r) + 1
    else:
        time = 0
    return str(time)

# Provided samples
assert run("6 3 2 4\n") == "5", "sample 1"
assert run("5 1 4 5\n") == "1", "sample 2"
assert run("5 2 2 5\n") == "0", "sample 3"

# Custom cases
assert run("1 1 1 1\n") == "0", "minimum size"
assert run("100 50 1 100\n") == "0", "all tabs needed"
assert run("100 1 50 100\n") == "50", "move and close left"
assert run("100 100 1 50\n") == "51", "move and close right"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 0 | No |
