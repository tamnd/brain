---
title: "CF 105818A - Lily Pads"
description: "We have a pond with N rows of lily pads. Each row contains two possible landing positions, left and right. At any moment, exactly one side of a row is above water and can be used. Two frogs start before the first row and both need to cross the pond. A frog always moves forward."
date: "2026-06-25T15:09:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105818
codeforces_index: "A"
codeforces_contest_name: "TeamsCode Spring 2025 Advanced Division"
rating: 0
weight: 105818
solve_time_s: 37
verified: true
draft: false
---

[CF 105818A - Lily Pads](https://codeforces.com/problemset/problem/105818/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a pond with `N` rows of lily pads. Each row contains two possible landing positions, left and right. At any moment, exactly one side of a row is above water and can be used. Two frogs start before the first row and both need to cross the pond.

A frog always moves forward. It enters a row by landing on the currently available lily pad, and when it leaves that row, the used pad sinks while the other pad in the same row rises. Since only one frog can occupy a pad at a time, the frogs must take turns passing through the rows. Whenever a frog lands on the right pad, the total score increases by one.

The input gives the number of rows and the initial state of every row. The output asks for the maximum total score both frogs can obtain.

The main constraint is that `N` is small enough that many solutions could pass, but the real goal is to notice the structure. Even if `N` were much larger, we should look for a solution close to linear time because the input itself contains `N` pieces of information. Simulating all possible orders of the two frogs would create unnecessary states and grows exponentially.

The tricky part is that the frogs are allowed to choose different orders. A careless solution may try to greedily choose which frog goes first based on the current row, but the order chosen for one row affects the state of that row for the second frog. The important observation is that every row is independent in terms of the final score contribution.

For example, with one row:

```
1
L
```

The first frog lands on the left pad and gets no point. The pad flips, and the second frog lands on the right pad and gets one point. The answer is:

```
1
```

A solution that counts only initially right facing pads would output `0`, which is wrong.

Another edge case is when every row starts with the right pad available:

```
3
RRR
```

The first frog gets a point in every row. After each jump, the second frog gets the left pad and no points. The answer is still:

```
3
```

A solution that assumes both frogs should somehow avoid taking the first position in a row could incorrectly think the score can be improved.

## Approaches

A natural brute force approach is to try all possible ways the two frogs can interleave their moves. There are many possible sequences because at every row either frog could be the one that reaches it first. For each ordering, we can simulate the rows and count the points. This is correct because the only decision that matters is which frog arrives first at each row.

The problem is that this explores far more than necessary. There are two choices for who goes first at every row, so the number of possible orders is up to `2^N`. For `N` around `100`, this is already around `10^30` possibilities, which cannot be handled.

The key observation is that every row always gives exactly one point. Suppose a row currently has the left pad available. The first frog to enter gets the left pad and scores zero. When it leaves, the left pad goes underwater and the right pad becomes available, so the second frog gets one point. If the right pad starts available, the first frog scores one point and the second scores zero. In both cases, the total contribution of that row is exactly one.

Since both frogs must cross every row, every row contributes one point regardless of the initial configuration and regardless of the chosen order. The entire problem reduces to counting the rows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N * N) | O(N) | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of rows. The only information needed for the answer is how many rows exist, because each row contributes exactly one point.
2. Ignore the left or right configuration of each row. The first frog to visit a row and the second frog to visit the same row always split the two pads between them, so the combined score from that row is fixed.
3. Output `N`, the number of rows.

Why it works:

For every row, exactly two landings happen, one by each frog. The first landing uses the current floating pad, and the second landing uses the pad that became floating after the first frog leaves. The two frogs together visit both pads in the row once, and exactly one of those pads is the right pad. Hence exactly one point is added per row. Adding this fixed contribution over all `N` rows gives the maximum possible score.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    input().strip()
    print(n)

if __name__ == "__main__":
    solve()
```

The solution only needs the number of rows. The string describing the initial lily pad positions is read because it is part of the input format, but its values do not affect the answer.

There are no boundary issues because the algorithm never indexes into the string. The implementation also avoids storing the string, keeping the memory usage constant. The input size is tiny compared with the capabilities of Python, so fast I/O is more than enough.

## Worked Examples

### Sample 1

Input:

```
1
R
```

| Step | Rows counted | Current row state | Score |
| --- | --- | --- | --- |
| Start | 0 | `R` | 0 |
| Process row 1 | 1 | First frog gets right, second gets left | 1 |
| Finish | 1 | All rows processed | 1 |

The row starts with the right pad available, so the first frog scores. The second frog gets the remaining pad. The final score is one.

### Sample 2

Input:

```
3
LRL
```

| Step | Rows counted | Current row state | Score |
| --- | --- | --- | --- |
| Start | 0 | `LRL` | 0 |
| Process row 1 | 1 | Row contributes one point | 1 |
| Process row 2 | 2 | Row contributes one point | 2 |
| Process row 3 | 3 | Row contributes one point | 3 |

The trace shows that the initial orientation of the rows changes who receives the point, but never changes how many points the row gives in total.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Reading the input and producing the answer takes linear time in the number of rows. |
| Space | O(1) | Only the row count is stored. |

The algorithm easily fits the limits because it performs only constant work after reading the input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    sys.stdin.readline()
    ans = str(n)

    sys.stdin = old
    return ans

# provided sample style
assert run("1\nR\n") == "1", "single row"

# custom cases
assert run("5\nLLLLL\n") == "5", "all left pads"
assert run("4\nRRRR\n") == "4", "all right pads"
assert run("3\nLRL\n") == "3", "mixed rows"
assert run("100\n" + "L" * 100 + "\n") == "100", "large input size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / R` | `1` | Minimum size case |
| `5 / LLLLL` | `5` | All rows starting with left pads |
| `4 / RRRR` | `4` | All rows starting with right pads |
| `3 / LRL` | `3` | Mixed configurations |
| `100 / all L` | `100` | Large boundary case |

## Edge Cases

For a single row starting with `L`, the first frog reaches the left pad and gains nothing. After leaving, the left pad sinks and the right pad becomes available, so the second frog gains one point. The algorithm outputs `1`, matching the actual maximum.

For rows all starting with `R`, the first frog receives the point in every row. The second frog receives no points from those rows because the right pads have already sunk. The algorithm outputs the number of rows, which matches the total score.

For alternating rows such as `LRL`, the frogs may receive points in different rows depending on who arrives first. The total remains unchanged because every row always gives exactly one point, so the answer is still the row count.
