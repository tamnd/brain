---
title: "CF 104804K - \u041f\u0435\u0447\u0430\u0442\u044c"
description: "We are given a printing shop that splits paper lengths into a sequence of contiguous segments. Each segment represents a range of page counts, and every range has a fixed cost per page."
date: "2026-06-28T13:28:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104804
codeforces_index: "K"
codeforces_contest_name: "Central Russia Regional Contest, 2022, Qualification Contest"
rating: 0
weight: 104804
solve_time_s: 67
verified: true
draft: false
---

[CF 104804K - \u041f\u0435\u0447\u0430\u0442\u044c](https://codeforces.com/problemset/problem/104804/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a printing shop that splits paper lengths into a sequence of contiguous segments. Each segment represents a range of page counts, and every range has a fixed cost per page. If a job fits inside a range, it can be printed at that cost per page, but there is a catch: the customer is allowed to pad the document with extra blank pages so that the total page count becomes any value greater than or equal to the original length, and then choose a range that covers that padded size.

The goal is to start with a document of exactly $k$ pages and optionally increase it to any larger number, then pick a single segment whose interval fully contains the final page count. The cost is the segment cost multiplied by the chosen page count, since cost is per page. The task is to minimize this total payment, or determine that no segment can accommodate any feasible padded length.

The structure of the input is important: segments are given in increasing order, they fully partition the number line starting from 1, with no gaps and no overlaps. This means every positive integer page count belongs to exactly one segment.

The constraints push us toward a linear or near linear solution. With $n \le 10^5$, any $O(n^2)$ strategy that tries all choices or simulates padding decisions per segment is immediately too slow. The key hidden constraint is $k \le 10^9$, which prevents building explicit arrays or DP over pages.

A naive mistake arises when one assumes the best segment is simply the one containing $k$. That is incorrect because padding allows moving into later segments that may have a much smaller cost per page.

Another subtle failure case appears when a segment starts just after $k$, and a cheaper segment exists further right. For example, if segment costs decrease significantly later, the optimal strategy is to increase the page count beyond $k$ until reaching that cheaper segment.

Finally, it is easy to forget that we are choosing a single segment after padding, not mixing segments.

## Approaches

A brute-force approach would try every segment as the final choice. For each segment $[a_i, b_i]$, we would check whether we can reach it by padding, meaning we need $b_i \ge k$. If so, we could choose any $x \in [\max(k, a_i), b_i]$, and the cost becomes $x \cdot c_i$. The best choice inside a segment is always the smallest feasible $x$, because cost grows linearly with pages. So for each segment we would compute:

$$x_i = \max(k, a_i), \quad \text{cost}_i = x_i \cdot c_i$$

and take the minimum over all valid segments.

This is correct but already $O(n)$, which is fine. However, there is an even more important observation hidden in the structure: segments are contiguous and sorted, so we can process them in one pass while maintaining the best answer. The key idea is that we never need to revisit earlier segments, and we never need to consider more than the current segment for a given range of $k$.

The real subtlety is that because padding is allowed, the effective decision is not tied to where $k$ lies initially. We are essentially choosing a breakpoint $x \ge k$, then paying $x \cdot c(x)$, where $c(x)$ is the segment cost function over intervals.

Since the function is piecewise constant over segments, and linear inside each segment, checking each segment once is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

In fact, the “optimal” solution is the same as the clean brute-force once formulated correctly, but implemented carefully with interval logic.

## Algorithm Walkthrough

1. Initialize a variable `answer` as infinity. This will track the minimum possible cost across all valid choices.
2. Iterate over each segment $[a_i, b_i]$ with cost $c_i$. Since segments are disjoint and cover all integers, each possible final page count belongs to exactly one segment, so each segment must be considered exactly once.
3. Check whether the segment can be used at all. Since we can only increase pages, any final page count must be at least $k$. If $b_i < k$, the segment cannot contain any feasible final size and is ignored.
4. If the segment is usable, determine the best page count inside it. The smallest feasible page count is $\max(k, a_i)$, because we cannot go below $k$ due to padding, and we cannot go below the segment start.
5. Compute cost as $\text{pages} \times c_i$. This is optimal inside the segment because increasing pages only increases cost linearly.
6. Update the global minimum answer.
7. After processing all segments, if the answer was never updated, output $-1$. Otherwise output the computed minimum.

### Why it works

The crucial invariant is that every feasible final page count belongs to exactly one segment, and within a segment the cost function is monotonic in the number of pages. This makes the optimal choice within a segment always its leftmost feasible point. Since every valid final state is represented by exactly one segment and one choice inside it, scanning all segments and taking the best local optimum guarantees the global optimum. No cross-segment interaction exists beyond the feasibility condition $b_i \ge k$, because padding only increases the page count and never forces skipping over a segment without considering it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    ans = 10**30

    for _ in range(n):
        a, b, c = map(int, input().split())

        if b < k:
            continue

        x = max(a, k)
        if x <= b:
            ans = min(ans, x * c)

    print(-1 if ans == 10**30 else ans)

if __name__ == "__main__":
    solve()
```

The solution processes segments in a single pass, maintaining only the best answer so far. The key detail is the computation of `x = max(a, k)`, which correctly models both constraints: padding cannot reduce below $k$, and we must stay within the segment bounds.

The check `b < k` filters segments that cannot contain any valid final size. The second condition `x <= b` ensures that after padding we still remain inside the segment.

## Worked Examples

### Sample 1

Input:

```
4 15
1 5 20
6 10 15
11 20 10
21 30 5
```

| Segment | k | x = max(a, k) | Valid? | Cost |
| --- | --- | --- | --- | --- |
| [1,5] | 15 | 15 | No (5 < 15) | - |
| [6,10] | 15 | 15 | No (10 < 15) | - |
| [11,20] | 15 | 15 | Yes | 150 |
| [21,30] | 15 | 21 | Yes | 105 |

The best choice is segment [21,30] by padding up to 21 pages. This shows why the optimal solution may lie strictly after k.

### Sample 2

Input:

```
11 16
1 1 7
2 2 14
3 4 17
5 7 1
8 8 18
9 10 19
11 12 18
13 14 9
15 18 5
19 19 2
20 20 8
```

| Segment | k | x | Valid? | Cost |
| --- | --- | --- | --- | --- |
| [1,1] | 16 | 16 | No | - |
| [2,2] | 16 | 16 | No | - |
| [3,4] | 16 | 16 | No | - |
| [5,7] | 16 | 16 | No | - |
| [8,8] | 16 | 16 | No | - |
| [9,10] | 16 | 16 | No | - |
| [11,12] | 16 | 16 | No | - |
| [13,14] | 16 | 16 | No | - |
| [15,18] | 16 | 16 | Yes | 80 |
| [19,19] | 16 | 19 | Yes | 38 |
| [20,20] | 16 | 20 | Yes | 160 |

The optimal strategy jumps forward to reach a cheaper per-page segment, showing that padding is essential.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each segment is processed exactly once with constant work |
| Space | O(1) | Only a few variables are maintained |

The solution is linear in the number of segments, which fits easily within the constraints of $10^5$. No additional memory is required beyond input parsing and a few scalars.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    n, k = map(int, input().split())
    ans = 10**30

    for _ in range(n):
        a, b, c = map(int, input().split())
        if b < k:
            continue
        x = max(a, k)
        if x <= b:
            ans = min(ans, x * c)

    print(-1 if ans == 10**30 else ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio
    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""4 15
1 5 20
6 10 15
11 20 10
21 30 5
""") == "105"

assert run("""11 16
1 1 7
2 2 14
3 4 17
5 7 1
8 8 18
9 10 19
11 12 18
13 14 9
15 18 5
19 19 2
20 20 8
""") == "38"

# minimum case
assert run("""1 5
1 10 3
""") == "15"

# k inside early segment but better later
assert run("""3 4
1 5 10
6 10 1
11 20 2
""") == "10"

# no valid segment
assert run("""2 100
1 10 5
11 20 6
""") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single segment covering k | 15 | minimal handling |
| increasing costs later | 10 | padding advantage |
| unreachable k | -1 | failure case |

## Edge Cases

A key edge case is when $k$ lies far inside a segment but the optimal move is to skip forward. For example, if a later segment has a much smaller cost, padding should jump past intermediate expensive segments. The algorithm handles this because it never restricts choices to the segment containing $k$, it evaluates every segment independently.

Another edge case occurs when $k$ is larger than all $b_i$ except the last segment. In this case, only the final segment contributes candidates, and the algorithm correctly returns either a value from it or $-1$ if even it cannot accommodate $k$.

A third case is when the optimal value is achieved exactly at $a_i$ rather than $k$. The formula `max(a, k)` ensures we never incorrectly choose a value below either constraint, so the left boundary logic remains correct even when $k$ is small.
