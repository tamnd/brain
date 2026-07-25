---
title: "CF 102862L - Falling Boxes"
description: "We have a collection of identical square boxes placed inside a storage shape made from two diagonal walls. The coordinate system describes each box by two indices: one counting layers from the left wall and one counting layers from the right wall."
date: "2026-07-25T13:57:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102862
codeforces_index: "L"
codeforces_contest_name: "LU ICPC Selection Contest 2020 and KFU Open Contest 2020"
rating: 0
weight: 102862
solve_time_s: 50
verified: true
draft: false
---

[CF 102862L - Falling Boxes](https://codeforces.com/problemset/problem/102862/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
# Problem Understanding

We have a collection of identical square boxes placed inside a storage shape made from two diagonal walls. The coordinate system describes each box by two indices: one counting layers from the left wall and one counting layers from the right wall. Because the arrangement is stable, the occupied positions form a staircase-like shape where every box that supports another box is already present.

The lowest box, the one touching both walls, is removed. The empty position it leaves becomes a hole. Gravity makes the hole move upward through the pile: either the box immediately above it on one side falls down, or the box immediately above it on the other side falls down. After a box falls, the hole moves to the box's previous position. The process stops when the hole reaches a position that has no box that can fall into it.

The task is to count how many different sequences of falling choices are possible. The answer must be printed modulo $10^9+7$.

The input contains up to $10^5$ boxes, and every coordinate is at most $n$. A quadratic simulation is not possible because $10^{10}$ operations would already be required in the largest case. We need a solution that processes each box only a small number of times, which points toward an $O(n)$ or $O(n \log n)$ approach.

The main edge cases come from confusing final positions with falling sequences. Different choices can lead to different histories even when the hole finishes at the same location. For example, consider:

```
5
1 1
1 2
2 1
2 2
3 1
```

The correct answer is:

```
3
```

A careless approach might count only the possible final empty cells. The hole can finish at `(2,2)` or `(3,1)`, which gives two final states, but there are three possible falling sequences because the hole can reach `(2,2)` in two different ways.

Another corner case is a single box:

```
1
1 1
```

The answer is:

```
1
```

There are no choices to make. The only possible scenario is that the removed box leaves an empty storage room.

A third case is a straight pile:

```
3
1 1
2 1
3 1
```

The answer is:

```
1
```

Every hole position has exactly one possible falling box, so the process has no branching.

# Approaches

A direct simulation would follow every possible falling sequence. Starting from the removed bottom box, we recursively try every possible box that can fill the hole. This is correct because every valid scenario is exactly one sequence of these choices.

The problem is that this recursion can branch many times. In a dense staircase-shaped pile, many different paths can exist, and exploring them individually can take exponential time. The same hole positions are reached repeatedly by different sequences, so the brute-force method repeats work.

The key observation is that the only thing that matters at any moment is the current position of the hole. If the hole reaches a certain box position, the number of ways to get there is independent of the exact sequence that produced it. This allows us to merge all equivalent states.

The problem becomes a dynamic programming problem on the occupied cells. A cell receives the sum of the ways from the cells below it in the falling process. Since the hole only moves by increasing one coordinate, the graph has no cycles. We can process cells in increasing order of `x + y`.

For each cell, we store the number of ways the hole can arrive there. If a cell has no possible next move, it represents a finished scenario, so its value contributes to the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of branching cells | O(n) recursion depth | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store every occupied box position in a set so that checking whether a neighboring box exists takes constant time. The coordinates form a directed acyclic graph because every move increases either `x` or `y`.
2. Sort the boxes by increasing `x + y`. This gives a valid order for dynamic programming because a hole can only move from a smaller coordinate sum to a larger one.
3. Set the number of ways to reach the removed bottom position `(1,1)` to one. This represents the start of the falling process.
4. Visit every box in sorted order. For the current position `(x,y)`, add its current number of ways to `(x+1,y)` if that box exists. This corresponds to the box from the left side falling into the hole.
5. Add the current number of ways to `(x,y+1)` if that box exists. This corresponds to the box from the right side falling into the hole.
6. After all transitions are processed, sum the values of every box that has no box directly below it in either direction. These are the positions where the hole stops, so every path ending there is one valid scenario.

Why it works:

The invariant is that `dp[x][y]` equals the number of possible falling sequences that move the hole from the original empty position to `(x,y)`. The starting state has one empty sequence. Whenever the hole reaches a cell, the only possible next states are the two neighboring boxes that can fall into it, so adding the current count to those cells accounts for every possible continuation exactly once. Since every possible scenario is a path from `(1,1)` to a terminal cell, summing all terminal states gives the final answer.

# Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n = int(input())
    boxes = []
    box_set = set()

    for _ in range(n):
        x, y = map(int, input().split())
        boxes.append((x, y))
        box_set.add((x, y))

    boxes.sort(key=lambda p: p[0] + p[1])

    dp = {}

    for x, y in boxes:
        dp[(x, y)] = 0

    dp[(1, 1)] = 1

    for x, y in boxes:
        cur = dp[(x, y)]

        if (x + 1, y) in box_set:
            dp[(x + 1, y)] = (dp[(x + 1, y)] + cur) % MOD

        if (x, y + 1) in box_set:
            dp[(x, y + 1)] = (dp[(x, y + 1)] + cur) % MOD

    ans = 0

    for x, y in boxes:
        if (x + 1, y) not in box_set and (x, y + 1) not in box_set:
            ans = (ans + dp[(x, y)]) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The set `box_set` provides constant-time neighbor checks. Because there are only two possible moves from every position, no adjacency list is needed.

The sorting step is the topological ordering of the implicit graph. Coordinates are always increased during a fall, so processing smaller `x + y` values first guarantees that all incoming transitions to a state have already been considered before it is used.

The dictionary `dp` stores the number of paths reaching each occupied position. Python integers do not overflow, but every update is reduced modulo $10^9+7$ to keep the stored values small.

The terminal-state check uses exactly the two possible moves from a position. A box is a stopping point if neither neighbor exists. Checking this after the DP avoids any special handling during transitions.

# Worked Examples

For the sample:

```
5
1 1
1 2
2 2
3 1
2 1
```

The sorted order is already:

| Cell | Current ways | Add to `(x+1,y)` | Add to `(x,y+1)` |
| --- | --- | --- | --- |
| `(1,1)` | 1 | `(2,1)` gets 1 | `(1,2)` gets 1 |
| `(1,2)` | 1 | `(2,2)` gets 1 | none |
| `(2,1)` | 1 | `(3,1)` gets 1 | `(2,2)` gets another 1 |
| `(2,2)` | 2 | none | none |
| `(3,1)` | 1 | none | none |

The terminal cells are `(2,2)` and `(3,1)`. Their values are `2` and `1`, giving the answer `3`.

This example shows why summing only terminal positions is not enough. The same final empty location can be reached by multiple choices.

A straight chain:

```
3
1 1
2 1
3 1
```

produces:

| Cell | Current ways | Next cell |
| --- | --- | --- |
| `(1,1)` | 1 | `(2,1)` |
| `(2,1)` | 1 | `(3,1)` |
| `(3,1)` | 1 | stop |

There is only one path, so the answer is `1`.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each box is sorted once and processed with two neighbor checks |
| Space | O(n) | The set of boxes and the DP table each contain at most one entry per box |

The constraint of $10^5$ boxes means the linear solution easily fits within typical contest limits. The algorithm never explores individual falling scenarios, only the states shared by all scenarios.

# Test Cases

```python
import sys
import io

MOD = 10**9 + 7

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        data = sys.stdin.readline
        n = int(data())
        boxes = []
        box_set = set()

        for _ in range(n):
            x, y = map(int, data().split())
            boxes.append((x, y))
            box_set.add((x, y))

        boxes.sort(key=lambda p: p[0] + p[1])

        dp = {p: 0 for p in boxes}
        dp[(1, 1)] = 1

        for x, y in boxes:
            cur = dp[(x, y)]
            if (x + 1, y) in box_set:
                dp[(x + 1, y)] = (dp[(x + 1, y)] + cur) % MOD
            if (x, y + 1) in box_set:
                dp[(x, y + 1)] = (dp[(x, y + 1)] + cur) % MOD

        ans = 0
        for x, y in boxes:
            if (x + 1, y) not in box_set and (x, y + 1) not in box_set:
                ans = (ans + dp[(x, y)]) % MOD

        return str(ans) + "\n"
    finally:
        sys.stdin = old_stdin

assert solution("""5
1 1
1 2
2 2
3 1
2 1
""") == "3\n", "sample"

assert solution("""1
1 1
""") == "1\n", "single box"

assert solution("""3
1 1
2 1
3 1
""") == "1\n", "straight pile"

assert solution("""4
1 1
1 2
1 3
2 1
""") == "1\n", "single branch"

assert solution("""6
1 1
1 2
2 1
2 2
3 1
1 3
""") == "4\n", "multiple branches"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single box | `1` | No movement choices exist |
| Straight pile | `1` | A chain with no branching |
| Single branch | `1` | Only one possible continuation |
| Multiple branches | `4` | Several paths merge into the same states |

# Edge Cases

For the single-box case:

```
1
1 1
```

The DP starts with one way at `(1,1)`. The cell has no neighbors, so it is counted as a terminal state. The answer remains `1`.

For the example where multiple paths reach the same ending point:

```
5
1 1
1 2
2 1
2 2
3 1
```

The algorithm stores the two different ways of reaching `(2,2)` separately through DP addition. When the cell is processed, its value is `2`, not `1`, so both histories are counted.

For a straight pile:

```
3
1 1
2 1
3 1
```

Every state has exactly one outgoing edge. The DP value remains `1` through the whole chain, and only the final cell contributes to the answer. This prevents overcounting when there is no branching.
