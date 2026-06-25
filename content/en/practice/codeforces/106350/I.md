---
title: "CF 106350I - Swap(Mohamed, !Mohamed)"
description: "The problem describes a row of boxes. Some boxes contain Mohamed, represented by 1, while empty boxes are represented by 0. Mohamed wants to choose one box as the final meeting point and move every Mohamed currently in another box to that chosen box."
date: "2026-06-25T08:07:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106350
codeforces_index: "I"
codeforces_contest_name: "Zaglol Contest - FCDS level 1 contest 2026"
rating: 0
weight: 106350
solve_time_s: 31
verified: true
draft: false
---

[CF 106350I - Swap(Mohamed, !Mohamed)](https://codeforces.com/problemset/problem/106350/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes a row of boxes. Some boxes contain Mohamed, represented by `1`, while empty boxes are represented by `0`. Mohamed wants to choose one box as the final meeting point and move every Mohamed currently in another box to that chosen box. Moving a Mohamed from one box to an adjacent box costs one swap, so moving a distance of `d` boxes costs `d` operations. The task is to find the minimum number of swaps needed over all possible destination boxes.

The input contains the number of boxes and a binary string describing their current states. The output is the smallest possible total movement cost.

The constraints are designed to rule out checking every destination and simulating movement repeatedly. If there are `n` boxes and `n` can be large, a solution that tries every destination and scans the whole string would take `O(n^2)` operations, which is too slow. We need a method where each box is processed only a constant number of times.

The main edge cases come from positions with no Mohamed and from rows where all Mohamed are already together. A careless implementation may assume the destination must contain a Mohamed, but the best destination can be an empty box.

For example:

```
5
00100
```

The correct output is:

```
0
```

Choosing the middle box already containing Mohamed requires no movement. A method that only checks empty positions or only considers moving to the edges would fail.

Another example:

```
6
100001
```

The correct output is:

```
5
```

Choosing any middle box gives a larger cost, while choosing either endpoint moves one Mohamed five boxes and leaves the other already there. A naive approach that counts only the number of Mohamed instead of their distances would miss the actual cost.

## Approaches

A straightforward solution is to try every possible destination box. For a chosen destination `i`, scan the whole string, and whenever a box contains Mohamed, add the distance between that box and `i`. This is correct because the total work needed for a destination is exactly the sum of all individual movements.

However, doing this for every destination repeats almost the same calculations many times. With `n` possible destinations and `n` boxes to scan for each one, the worst case is `O(n^2)` operations. For a large row, this quickly becomes impossible.

The key observation is that neighboring destinations are related. If we know the total cost for placing everyone at box `i`, we can derive the cost for box `i + 1` without scanning the whole row again.

When we move the destination one step to the right, every Mohamed on the left side becomes one step farther away, while every Mohamed on the right side becomes one step closer. If we maintain the number of Mohamed on each side, the cost changes by a simple difference. This lets us compute all destinations in linear time.

The brute-force method works because every possible destination is evaluated exactly, but it wastes time recomputing overlapping distances. The observation about how the cost changes between adjacent destinations reduces the problem to prefix and suffix counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the contribution of all Mohamed when the destination is the first box.

For every Mohamed at position `i`, its cost is `i` because it must move `i` boxes to reach the first position. Summing these values gives the initial answer for the first destination.
2. Store this initial cost and prepare to move the destination from left to right.

While shifting the destination, we only need to know how many Mohamed are currently on the left and right sides.
3. Move the destination one position to the right at a time.

Suppose the destination moves from position `i` to `i + 1`. Every Mohamed at positions `0` through `i` becomes one step farther away, increasing the cost by the number of Mohamed on the left. Every Mohamed after `i` becomes one step closer, decreasing the cost by the number of Mohamed on the right.
4. Update the current cost using this difference and keep the minimum value seen.

Since every possible destination is reached exactly once, the smallest recorded value is the optimal answer.

Why it works:

The invariant is that before processing a destination, the stored cost is exactly the number of swaps needed to move every Mohamed to that position. Moving the destination by one position changes each individual distance by exactly one, either increasing or decreasing depending on which side the Mohamed is on. Because all contributions are updated together using their counts, every computed destination cost is correct, so the minimum found is the true optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    total = 0
    ones = 0

    for i, c in enumerate(s):
        if c == '1':
            total += i
            ones += 1

    ans = total

    left = 0
    right = ones

    current = total

    for i in range(n - 1):
        if s[i] == '1':
            left += 1
        right = ones - left

        current += left - right
        ans = min(ans, current)

    print(ans)

if __name__ == "__main__":
    solve()
```

The first loop calculates the cost if the chosen destination is the first box. A Mohamed at index `i` contributes exactly `i` swaps in this situation.

The variables `left` and `right` maintain how many Mohamed are before and after the current destination while scanning from left to right. When the destination moves one position, the `left` group gets farther by one and the `right` group gets closer by one, which is why the update is `left - right`.

The loop stops at `n - 1` because after the final move there is no next destination to evaluate. All arithmetic uses Python integers, so large movement totals do not overflow.

## Worked Examples

Consider:

```
5
00100
```

| Destination after processing | Left Mohamed | Right Mohamed | Current cost | Best answer |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 2 | 2 |
| 1 | 0 | 1 | 1 | 1 |
| 2 | 1 | 0 | 0 | 0 |
| 3 | 1 | 0 | 1 | 0 |
| 4 | 1 | 0 | 2 | 0 |

The only Mohamed starts at the center, so choosing the same box gives zero movement. The transition formula correctly decreases the cost until reaching that position and increases afterwards.

Another example:

```
6
100001
```

| Destination after processing | Left Mohamed | Right Mohamed | Current cost | Best answer |
| --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 5 | 5 |
| 1 | 1 | 1 | 5 | 5 |
| 2 | 1 | 1 | 5 | 5 |
| 3 | 1 | 1 | 5 | 5 |
| 4 | 1 | 1 | 5 | 5 |
| 5 | 2 | 0 | 5 | 5 |

The optimal destination is any endpoint or middle position in this symmetric case. The algorithm evaluates every possibility and keeps the same minimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The string is scanned a constant number of times. |
| Space | O(1) | Only counters and the current answer are stored. |

The algorithm processes each box once, so it scales linearly with the row length and fits the expected limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    data = sys.stdin.readline
    n = int(data())
    s = data().strip()

    total = 0
    ones = 0

    for i, c in enumerate(s):
        if c == '1':
            total += i
            ones += 1

    ans = total
    left = 0
    current = total

    for i in range(n - 1):
        if s[i] == '1':
            left += 1
        right = ones - left
        current += left - right
        ans = min(ans, current)

    sys.stdin = old_stdin
    return str(ans) + "\n"

assert run("5\n00100\n") == "0\n", "single Mohamed already centered"
assert run("6\n100001\n") == "5\n", "symmetric endpoints"
assert run("1\n1\n") == "0\n", "minimum size"
assert run("8\n11111111\n") == "16\n", "all boxes occupied"
assert run("7\n0001000\n") == "0\n", "single Mohamed with many empty boxes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 / 00100` | `0` | Destination already occupied by Mohamed |
| `6 / 100001` | `5` | Symmetric movement and equal costs |
| `1 / 1` | `0` | Smallest possible input |
| `8 / 11111111` | `16` | Dense case with many contributors |
| `7 / 0001000` | `0` | Single Mohamed and boundary distances |

## Edge Cases

For `00100`, the algorithm starts with an initial cost of `2`, because the Mohamed is two positions away from the first box. As the destination moves right, the update changes the cost by the difference between Mohamed on the left and right. When the destination reaches the center, the cost becomes `0`, which is recorded as the answer.

For `100001`, the initial cost is `5`. Moving the destination toward the middle makes one Mohamed closer and the other farther away by the same amount, so the total remains `5`. The algorithm does not assume the middle is always better and correctly returns the minimum value.

For `11111111`, every box contains Mohamed. The algorithm handles this without any special case. Each shift changes the cost according to the balance of Mohamed on both sides, and the minimum occurs near the center, producing the correct total movement.

For a single box such as `1`, the loops do not perform any transitions because there is no neighboring destination. The initial cost is already the final answer, which avoids off-by-one mistakes.
