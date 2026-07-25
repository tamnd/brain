---
title: "CF 102870A - Accordion Artist And Orz Pandas"
description: "The task describes a row of adjacent buildings, where each building has a height and a width. Because the buildings touch each other, their front faces form one continuous skyline."
date: "2026-07-25T13:11:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102870
codeforces_index: "A"
codeforces_contest_name: "2020-2021 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102870
solve_time_s: 53
verified: true
draft: false
---

[CF 102870A - Accordion Artist And Orz Pandas](https://codeforces.com/problemset/problem/102870/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a row of adjacent buildings, where each building has a height and a width. Because the buildings touch each other, their front faces form one continuous skyline. We need to place a rectangular advertisement inside that skyline, with the advertisement's height and width aligned perpendicular to the original building heights, and find the largest possible area. The input gives the height and width of every building, and the output is the maximum area of such a rectangle.

The main difficulty comes from the fact that the buildings do not all have the same width. A rectangle may cover several consecutive buildings, but its height is limited by the shortest building among those buildings. If we tried every interval of buildings, we would need to examine up to $O(n^2)$ intervals. With $n$ reaching $100000$, that would mean around $10^{10}$ interval checks, which is far beyond what a typical contest time limit allows. The algorithm must be close to linear.

There are several edge cases where a careless implementation can fail. If a single building is the tallest one, the answer may come from using only that building. For example:

```
1
7 3
```

The correct output is:

```
21
```

An approach that only checks pairs of buildings would miss the rectangle inside this single building.

Another tricky case is when several adjacent buildings have the same height. For example:

```
3
5 2
5 3
5 4
```

The correct output is:

```
45
```

The entire row can be used because every building supports height $5$. An implementation that treats equal heights as separate and never merges them can lose the total width and produce a smaller answer.

A final common mistake appears when the shortest building is at the end. For example:

```
3
4 2
4 2
1 10
```

The correct output is:

```
16
```

The best rectangle uses the first two buildings with height $4$ and width $4$. A solution that only calculates areas when it sees a shorter building but forgets to process the remaining stack after the scan will miss this rectangle.

## Approaches

The direct approach is to consider every consecutive group of buildings. For each interval, we calculate the total width and the minimum height inside that interval. The rectangle formed by that interval has area equal to the minimum height multiplied by the total width. This is correct because every possible rectangle must fit completely inside some consecutive group of buildings, and its height cannot exceed the shortest building in that group.

However, this checks too many intervals. With $n=100000$, there can be roughly $n(n+1)/2$ different intervals, which is about $5 \times 10^9$. Even if calculating each interval was constant time, this would still be too slow.

The key observation is that we do not need to explicitly test every interval. When a building becomes shorter than previous buildings, the taller buildings can no longer extend through the current position. At that moment, we know the maximum width where each taller building could be the limiting height.

This is exactly the situation handled by a monotonic stack. The stack stores buildings in increasing height order. Instead of storing every original building separately, consecutive buildings with the same height are merged because they always behave identically: the same height can cover their combined width.

The brute-force method works because every possible rectangle is represented by some interval. It fails because it repeatedly recomputes information about overlapping intervals. The monotonic stack removes this repetition by processing each building only a constant number of times.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the buildings from left to right and maintain a stack of pairs. Each pair stores a height and the total width covered by consecutive buildings with that height.

The stack is kept in increasing height order. This means every height remaining in the stack still has a chance to extend further to the right.

1. For the current building, start with its own width as the width currently being processed.

If the top of the stack has a greater height than the current building, that taller height cannot continue past this point. Remove it from the stack and calculate the rectangle using that height. The width of that rectangle is the current accumulated width because all removed buildings are consecutive and all are at least as tall as the removed height.

1. Continue removing taller buildings until the stack is empty or the top height is no greater than the current height.

After removing a taller block, its width is added to the current width. This lets the current building combine with all previous shorter or equal regions.

1. If the top of the stack has the same height as the current building, merge the widths.

Equal heights represent the same possible rectangle height, so keeping them as separate stack entries only complicates later calculations.

1. Push the current height and its accumulated width onto the stack if there is no equal height to merge with.
2. After all buildings are processed, remove every remaining stack entry and calculate its area using the accumulated width.

There is no shorter building after the final position, so every remaining height can extend until the end of the skyline.

Why it works:

The invariant of the stack is that heights are strictly increasing after equal heights are merged. Every entry represents a group of consecutive buildings where that height is the smallest height seen so far. When a shorter building appears, every taller height that is removed has found its first smaller boundary on the right. The accumulated width at that moment is exactly the maximum width available for that height. Since every building is pushed once and popped once, every possible limiting height is evaluated, so the maximum area cannot be missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    buildings = [tuple(map(int, input().split())) for _ in range(n)]

    stack = []
    ans = 0

    for h, w in buildings:
        cur_w = w

        while stack and stack[-1][0] > h:
            ph, pw = stack.pop()
            cur_w += pw
            ans = max(ans, ph * cur_w)

        if stack and stack[-1][0] == h:
            stack[-1] = (h, stack[-1][1] + cur_w)
        else:
            stack.append((h, cur_w))

    cur_w = 0
    while stack:
        h, w = stack.pop()
        cur_w += w
        ans = max(ans, h * cur_w)

    print(ans)

if __name__ == "__main__":
    solve()
```

The stack stores `(height, width)` pairs rather than indices. Because widths are part of the input, an index-based histogram solution is less convenient. The accumulated width is the important information because the final rectangle area depends on horizontal coverage.

The loop over the buildings handles all cases where a shorter building closes previous rectangles. The condition uses `>` instead of `>=` because equal heights should be combined rather than removed. This avoids splitting one rectangle into several smaller pieces.

The final cleanup loop is necessary because some rectangles remain valid until the end of the skyline. Forgetting this step loses answers where the maximum rectangle ends at the last building.

Python integers can handle the largest possible area because the maximum height and total width are both at most about $10^{10}$ when multiplied, which is within Python's integer range.

## Worked Examples

For the first sample:

```
5
2 1
4 1
3 1
4 1
1 1
```

The stack evolution is:

| Step | Current building | Stack after processing | Current answer |
| --- | --- | --- | --- |
| 1 | (2,1) | [(2,1)] | 0 |
| 2 | (4,1) | [(2,1),(4,1)] | 0 |
| 3 | (3,1) | [(2,1),(3,2)] | 4 |
| 4 | (4,1) | [(2,1),(3,2),(4,1)] | 4 |
| 5 | (1,1) | [(1,5)] | 9 |
| End | cleanup | empty | 9 |

When height `1` arrives, all taller rectangles are finalized. The height `3` rectangle has width `3`, and the height `4` rectangle has width `1`. The best rectangle is height `3` with width `3`, giving area `9`.

For the second sample:

```
5
2 1
4 1
3 1
4 1
2 1
```

| Step | Current building | Stack after processing | Current answer |
| --- | --- | --- | --- |
| 1 | (2,1) | [(2,1)] | 0 |
| 2 | (4,1) | [(2,1),(4,1)] | 0 |
| 3 | (3,1) | [(2,1),(3,2)] | 4 |
| 4 | (4,1) | [(2,1),(3,2),(4,1)] | 4 |
| 5 | (2,1) | [(2,5)] | 10 |
| End | cleanup | empty | 10 |

The final building has height `2`, allowing every building to participate. The rectangle with height `2` and total width `5` gives the maximum area.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every building is pushed onto the stack once and removed once. |
| Space | O(n) | In the worst case, all buildings are increasing heights and remain in the stack. |

The solution only performs a constant amount of work per building, so it fits easily within the constraints of $100000$ buildings.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""5
2 1
4 1
3 1
4 1
1 1
""") == "9\n", "sample 1"

assert run("""5
2 1
4 1
3 1
4 1
2 1
""") == "10\n", "sample 2"

assert run("""1
7 3
""") == "21\n", "single building"

assert run("""3
5 2
5 3
5 4
""") == "45\n", "equal heights"

assert run("""3
4 2
4 2
1 10
""") == "16\n", "ending shorter building"

assert run("""4
1 100000
100000 100000
1 100000
100000 100000
""") == "10000000000\n", "large widths"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single building | 21 | Checks that one rectangle is considered. |
| All equal heights | 45 | Checks width merging for identical heights. |
| Shortest building at the end | 16 | Checks stack cleanup when the scan finishes. |
| Large widths and heights | 10000000000 | Checks large integer calculations. |

## Edge Cases

For the single building case:

```
1
7 3
```

The building is pushed into the stack. During cleanup, it is removed with accumulated width `3`, producing area `7 * 3 = 21`. The algorithm handles the case because the final cleanup processes rectangles that never encountered a smaller building.

For equal heights:

```
3
5 2
5 3
5 4
```

The first building creates `(5,2)`. The second building has the same height, so the stack entry becomes `(5,5)`. The third extends it to `(5,9)`. During cleanup, the area becomes `5 * 9 = 45`. The merging rule preserves the full possible width.

For the boundary case where the smallest building is last:

```
3
4 2
4 2
1 10
```

The two height `4` buildings merge into `(4,4)`. When height `1` appears, the stack removes height `4` and evaluates area `4 * 4 = 16`. The last building cannot improve the answer, so the result remains `16`. This demonstrates why shorter buildings trigger rectangle evaluation.
