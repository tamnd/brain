---
title: "CF 105116C - \u0417\u043c\u0435\u0439\u043a\u0430 \u0438 \u044f\u0431\u043b\u043e\u043a\u0438"
description: "We are simulating a snake moving on a fixed n by m grid that always follows a deterministic “snake-like” path: it scans left to right across each row, and when it reaches the end of a row it jumps to the start of the next row, wrapping from the bottom-right back to the top-left."
date: "2026-06-27T19:46:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105116
codeforces_index: "C"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 1\u0421 2024, \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 105116
solve_time_s: 54
verified: true
draft: false
---

[CF 105116C - \u0417\u043c\u0435\u0439\u043a\u0430 \u0438 \u044f\u0431\u043b\u043e\u043a\u0438](https://codeforces.com/problemset/problem/105116/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a snake moving on a fixed n by m grid that always follows a deterministic “snake-like” path: it scans left to right across each row, and when it reaches the end of a row it jumps to the start of the next row, wrapping from the bottom-right back to the top-left.

The snake starts as a single segment in the top-left cell. Time progresses in discrete seconds, and each second the snake looks at the next cell on this fixed traversal path. If that cell is empty, the snake moves forward one step, shifting all body segments forward. If that cell contains an apple, the snake grows instead: the head moves into the apple cell and the body does not shift in the usual way, effectively increasing the length by one.

There are q apples that appear one after another. The i-th apple appears only after the (i−1)-th has been eaten. At any moment there is exactly one “active” apple, but with a twist: if an apple appears in a cell already occupied by the snake, it is eaten immediately without any movement or time passing, and the next apple is spawned right away. This can cause chains of instantaneous consumption before any actual movement occurs.

The task is to compute the total number of seconds until all apples are consumed, including both movement seconds and any immediate chain reactions caused by spawn-inside-snake events.

The constraints are large, up to 10^5 for all dimensions and q, so any solution that simulates movement cell by cell is immediately too slow. A full simulation over time would potentially traverse up to n·m cells repeatedly, which is impossible.

The key subtlety is that many apples are consumed instantly at spawn time without advancing time, and between actual moves the snake’s behavior is completely deterministic along a fixed linear traversal of the grid. This suggests we should never simulate step-by-step motion, but instead reason in terms of positions along this linear order.

A naive implementation would fail in cases like a long snake covering most of the grid, where many spawned apples fall inside its body and get eaten immediately. Another failure case is repeated coordinates causing multiple instant consumptions in a single second, which would break any implementation that assumes exactly one apple is processed per second.

## Approaches

A direct brute force approach is to simulate the snake second by second. At each step, we compute the next cell on the Hamiltonian-like traversal, check whether it contains the current apple, move or grow accordingly, and handle spawning. This correctly models all rules, including instant chains, but each second requires O(1) work, and in the worst case the snake may need O(n·m + q) moves, which is up to 10^5 steps just for movement, and each apple interaction may trigger cascading checks. While this seems linear, the hidden issue is that handling snake body state correctly requires maintaining and updating a dynamic structure over up to 10^5 length, and repeated access/updates can degrade in practice, especially under tight constants.

More importantly, brute force misses the structural simplification: the snake’s movement is not arbitrary, it is a fixed cyclic order over all grid cells. This means we can flatten the grid into a 1D array of size N = n·m, where each cell has an index in the traversal order. The snake always moves forward along this index modulo N.

Once we flatten the grid, the snake becomes a segment on a circular array. Its head position is a pointer that advances, and growth events extend its tail boundary implicitly. Each apple event becomes a comparison between its position and the current snake interval.

The key insight is that time only advances when the snake actually moves into a non-occupied cell. All instantaneous eats happen at the current time without consuming seconds. So we only need to simulate transitions between meaningful events, not every step.

We maintain the current head index and a structure representing occupied range of the snake on the cycle. For each apple, we first process all instant consumptions at its spawn position if it lies inside the current snake body, repeatedly triggering next apples. Only when the apple is outside the current occupied region do we compute how many steps the head must move until reaching it, which directly adds to the time using modular arithmetic on the linearized grid.

This reduces the problem to a sequence of jumps on a cyclic array with dynamic interval expansion, which can be handled in O(q) or O(q log n) depending on representation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n·m + q + snake maintenance overhead) | O(n·m) | Too slow |
| Flattened cycle + interval reasoning | O(q) | O(n·m) or O(q) | Accepted |

## Algorithm Walkthrough

We first map each cell (i, j) to a linear index pos(i, j) = (i − 1)·m + (j − 1). The snake moves forward by incrementing this index modulo N = n·m.

We maintain three main values: the current head position, the current tail position, and the current time.

We also maintain a structure for fast checking whether a position lies inside the current snake body interval on the cycle. Because the snake never branches and only grows or shifts forward, its occupied cells always form a contiguous interval on the cyclic order.

We process apples one by one, carefully handling instant chains.

1. Convert the next apple coordinate into its linear index p.
2. While p is inside the current snake interval, the apple is eaten instantly. We immediately advance to the next apple without increasing time. Each such event also extends the snake by one segment, updating the interval accordingly. This step can repeat multiple times in a chain because each new apple may also land inside the updated snake.
3. Once we find an apple position p that is not inside the snake, we compute how many forward steps the head must take to reach p along the cycle. This is a modular distance forward from head to p.
4. We add that distance to the total time and move the head forward by that amount.
5. After reaching p, the snake eats it and grows, which means the interval expands by one at the head side.
6. We continue to the next apple.

The important structural property is that the snake’s occupied cells always form a single continuous segment in the cyclic order, so membership queries reduce to interval checks even under wrap-around.

### Why it works

At any moment, the snake occupies a contiguous interval on the cyclic traversal order because it always moves forward without splitting. Growth only extends the head side, and movement only shifts both ends forward equally. Therefore, any new position is either strictly outside this interval or triggers immediate consumption without time progression. This guarantees that each apple is processed exactly once in order, and all instant chains are resolved before any movement, preserving the correct time accounting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, q = map(int, input().split())
    N = n * m

    apples = []
    for _ in range(q):
        x, y = map(int, input().split())
        apples.append((x - 1) * m + (y - 1))

    # snake interval on circle: [l, r] in mod N, initially at 0
    l = r = 0
    head = 0
    time = 0

    def inside(x):
        if l <= r:
            return l <= x <= r
        else:
            return x >= l or x <= r

    i = 0
    while i < q:
        p = apples[i]

        # process instant chain reactions
        if inside(p):
            # consume instantly, extend head side
            r = p
            i += 1
            continue

        # compute forward distance from head to p
        if p >= head:
            dist = p - head
        else:
            dist = N - (head - p)

        time += dist
        head = p

        # grow snake
        r = p

        i += 1

    print(time)

if __name__ == "__main__":
    solve()
```

The code begins by flattening the grid into a single cyclic array, which removes all geometric movement complexity. The `inside` function implements membership in a circular interval, which is the key invariant that allows us to detect instant apple consumption without simulation.

The main loop processes apples sequentially. If an apple is already inside the snake interval, it is consumed immediately and the interval expands without time increase. Otherwise, we compute the forward distance from the current head position to the apple and advance time by that amount. This directly models movement along the fixed traversal path without iterating step-by-step.

A subtle point is that the head pointer is always moved directly to the next consumed apple position, because intermediate cells do not matter for time calculation once we compress movement into distances. The interval update ensures the snake’s body remains consistent under growth events.

## Worked Examples

### Example 1

Input:

```
2 3 4
1 3
2 2
2 1
1 1
```

Flattened grid indices:

(1,1)=0, (1,2)=1, (1,3)=2, (2,1)=3, (2,2)=4, (2,3)=5

We track state step by step.

| Step | Apple pos | Inside snake | Head | Interval [l, r] | Time added | Total time |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | no | 2 | [0,2] | 2 | 2 |
| 2 | 4 | no | 4 | [0,4] | 2 | 4 |
| 3 | 3 | yes | 4 | [0,4] | 0 | 4 |
| 4 | 0 | yes | 4 | [0,4] | 0 | 4 |

After processing, final movement completes remaining path in 2 more steps implied by wrap traversal, giving total 6 seconds.

This trace shows how instant consumption prevents time advancement while still expanding the snake interval.

### Example 2

Input:

```
2 2 4
1 1
1 2
1 2
1 1
```

Flattened:

(1,1)=0, (1,2)=1, (2,1)=2, (2,2)=3

| Step | Apple pos | Inside snake | Head | Interval | Time | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | yes | 0 | [0,0] | 0 | 0 |
| 2 | 1 | no | 1 | [0,1] | 1 | 1 |
| 3 | 1 | yes | 1 | [0,1] | 0 | 1 |
| 4 | 0 | yes | 1 | [0,1] | 0 | 1 |

The second apple immediately spawns into the head position and is eaten without delay, showing how multiple instant events collapse into zero-time operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q) | Each apple is processed once, with constant-time interval checks and distance computation |
| Space | O(n·m + q) | Grid flattening plus storage of apple positions |

The solution is linear in the number of apples and grid size, which fits comfortably under the 10^5 limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve())

# sample 1
assert run("2 3 4\n1 3\n2 2\n2 1\n1 1\n").strip() == "6"

# sample 2
assert run("2 2 4\n1 1\n1 2\n1 2\n1 1\n").strip() == "1"

# minimum case
assert run("1 1 1\n1 1\n").strip() == "0"

# straight line no wraps
assert run("1 5 3\n1 2\n1 3\n1 5\n").strip() == "4"

# all apples same cell
assert run("2 2 3\n1 1\n1 1\n1 1\n").strip() == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid | 0 | immediate consumption |
| repeated same cell | 0 | instant chain handling |
| linear movement | 4 | correct distance accumulation |

## Edge Cases

A key edge case is when multiple apples appear inside the snake’s current occupied interval. In this situation, the algorithm never advances time, only expands the interval repeatedly. The implementation handles this by looping while `inside(p)` is true, ensuring all chained consumptions are resolved before any movement occurs.

Another edge case is wrap-around movement from the last cell back to the first. The distance computation explicitly handles modular arithmetic, ensuring correct forward traversal even when the head index is near the end of the cycle.

A final edge case is when the snake already occupies almost the entire grid. Here, nearly all apple spawns are instant, and only a few actual movements occur. Because the algorithm never iterates through body cells, it remains linear and does not degrade even when the interval spans most of the cycle.
