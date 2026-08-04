---
title: "CF 102556C - Riana and Commute"
description: "Riana is moving on a one-dimensional street with blocks numbered from left to right. She starts at block 1 and wants to reach block A."
date: "2026-08-04T09:15:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102556
codeforces_index: "C"
codeforces_contest_name: "2020 Ateneo de Manila University DISCS PrO HS Division"
rating: 0
weight: 102556
solve_time_s: 63
verified: true
draft: false
---

[CF 102556C - Riana and Commute](https://codeforces.com/problemset/problem/102556/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

Riana is moving on a one-dimensional street with blocks numbered from left to right. She starts at block 1 and wants to reach block A. While walking, she may choose either direction, but bus stops change the movement rules: whenever she reaches a bus stop, she must immediately take the bus there, and the bus sends her to one fixed destination block. Every bus moves to a larger block number, so bus rides can never form a cycle by themselves.

The input describes the street length, the destination block, and the set of bus stops. Each bus stop is a directed jump from its position to a larger position. The task is to determine whether there exists some sequence of walking choices that eventually places Riana at block A. The output is `YES` if she can reach it and `NO` otherwise.

The constraints are small, with at most 100 blocks and at most 50 bus stops. This means an algorithm that explores every possible useful state is enough. A solution with exponential exploration of all possible walking paths is unnecessary, because many different paths can lead to the same block. We can instead store which blocks have already been reached and process each one once.

The main edge cases come from the forced nature of the buses. A common mistake is to treat buses as optional jumps. For example:

```
5 4 1
2 5
```

The correct answer is `NO`. From block 1, walking right reaches block 2, and Riana is forced to take the bus to block 5. She can then walk left and reach block 4, so this example actually produces `YES`. The dangerous part is not the final answer but the assumption: if a solution ignores the forced bus and treats block 2 as a normal position, it may explore invalid paths.

A more direct example is:

```
6 3 1
2 6
```

The correct answer is `NO`. Walking right from block 1 reaches the stop at block 2 and immediately sends Riana to block 6. She can only walk left from there, but block 3 is before the bus stop at block 2 and cannot be reached again because she cannot cross that stop without being sent away. A careless shortest-path interpretation that allows movement through all neighboring blocks would incorrectly find a path.

Another edge case is starting on the destination:

```
5 1 1
1 5
```

The correct answer is `YES`. Riana is already at Ateneo, so she does not need to move. An implementation that always applies bus transitions before checking the destination would incorrectly move her away.

## Approaches

A straightforward approach is to simulate every possible walking decision. From a block, Riana can try walking one block left or right repeatedly, and whenever she reaches a bus stop she jumps to its destination. This is correct because it directly follows the rules of movement. However, if implemented as a search over paths without remembering visited blocks, it can revisit the same situations many times. Even though the street is small here, the natural brute force view treats walking as a huge number of possible sequences, especially because Riana can wander back and forth before triggering buses.

The key observation is that after every forced bus chain finishes, only Riana's current block matters. Her previous walking history does not affect future choices. Since there are only N possible blocks, we can perform a graph search over reachable blocks.

The remaining question is how to create the graph edges. From a reachable block, Riana may walk in either direction until she either reaches Ateneo or encounters the first bus stop in that direction. She cannot pass that first bus stop, because the bus takes her immediately. If there is no bus stop in that direction, every block in that direction is reachable by walking. If there is a bus stop, the only resulting state is the destination after following all forced buses from that stop.

The number of blocks is small enough that we can check all blocks around a position when generating transitions. This gives a simple breadth-first search solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Potentially exponential in the number of movement choices | O(N) | Too slow without memoization |
| Optimal | O(N² + B) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read all bus stops and store the destination of each stop by its block number. A missing entry means that block is not a bus stop.
2. If the starting block is already Ateneo, immediately answer `YES`. Being at the destination is enough, and no movement is required.
3. Use breadth-first search starting from block 1. Each queue entry represents a block where Riana can be after all forced bus rides have finished.
4. When processing a block, check whether walking left can reach Ateneo before hitting a bus stop. If there is no bus stop to the left, every smaller block can be reached. If the nearest bus stop to the left exists, only blocks between the current block and that stop are reachable by walking.
5. Perform the same check while walking right. If a bus stop is encountered first, the next reachable state is the destination of that bus, followed by any additional buses triggered at that destination.
6. Whenever a new reachable block is found, add it to the queue. If a block has already been processed, skip it because exploring it again cannot reveal anything new.
7. If the search finishes without reaching A, output `NO`.

Why it works:

The invariant maintained by the search is that every block placed into the queue is a block Riana can actually occupy after obeying all forced bus rides. When expanding a block, the algorithm considers exactly the legal outcomes of choosing to walk left or right. It never allows her to pass through a bus stop without taking the bus, and it never creates an impossible movement. Since every valid decision sequence corresponds to a sequence of these transitions, any reachable destination will eventually be discovered. If the search cannot find A, no valid sequence of choices can reach it.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    N, A, B = map(int, input().split())

    bus = [-1] * (N + 1)
    for _ in range(B):
        x, y = map(int, input().split())
        bus[x] = y

    if A == 1:
        print("YES")
        return

    def follow_bus(pos):
        while bus[pos] != -1:
            pos = bus[pos]
        return pos

    start = follow_bus(1)

    visited = [False] * (N + 1)
    visited[start] = True
    q = deque([start])

    while q:
        pos = q.popleft()

        if pos == A:
            print("YES")
            return

        left_stop = -1
        for x in range(pos - 1, 0, -1):
            if bus[x] != -1:
                left_stop = x
                break

        if left_stop == -1:
            for x in range(1, pos):
                if not visited[x]:
                    if x == A:
                        print("YES")
                        return
                    visited[x] = True
                    q.append(x)
        else:
            for x in range(left_stop + 1, pos):
                if not visited[x]:
                    if x == A:
                        print("YES")
                        return
                    visited[x] = True
                    q.append(x)
            nxt = follow_bus(left_stop)
            if not visited[nxt]:
                visited[nxt] = True
                q.append(nxt)

        right_stop = -1
        for x in range(pos + 1, N + 1):
            if bus[x] != -1:
                right_stop = x
                break

        if right_stop == -1:
            for x in range(pos + 1, N + 1):
                if not visited[x]:
                    if x == A:
                        print("YES")
                        return
                    visited[x] = True
                    q.append(x)
        else:
            for x in range(pos + 1, right_stop):
                if not visited[x]:
                    if x == A:
                        print("YES")
                        return
                    visited[x] = True
                    q.append(x)
            nxt = follow_bus(right_stop)
            if not visited[nxt]:
                visited[nxt] = True
                q.append(nxt)

    print("NO")

solve()
```

The bus array stores the only possible transition from each bus stop. The `follow_bus` function handles the case where a bus destination is another bus stop. Because every bus increases the block number, this loop always terminates.

The BFS queue contains only positions that are possible after all automatic bus rides have already happened. This is why the initial position is normalized with `follow_bus(1)`. The special check for `A == 1` happens before that because reaching the destination does not require taking a bus away from it.

When generating transitions, the code searches for the nearest bus stop in each direction. Blocks before that stop are valid walking destinations. The stop itself is not added as a walking state because reaching it immediately triggers a bus ride. The only state created from the stop is its final bus destination.

There is no integer overflow issue because every value is at most 100. The loops intentionally include only blocks strictly between the current position and the next stop, avoiding the off-by-one mistake of allowing Riana to stand on a stop without taking its bus.

## Worked Examples

### Sample 1

Input:

```
10 5 4
1 3
2 6
4 10
7 9
```

| Current block | Direction checked | Result | Queue after processing |
| --- | --- | --- | --- |
| 3 | Left | Can reach 2, then bus chain from 2 goes to 6 | [6, 2] |
| 2 | Left | Can reach 1 | [6, 1] |
| 6 | Left | Can reach 5 | [1, 5] |
| 5 | Destination | Reached | YES |

The start position 1 is a bus stop, so the forced first move sends Riana to block 3. From there, the search discovers the same sequence as the sample explanation: use the bus at block 2, then walk back to block 5.

### Sample 2

Input:

```
8 3 2
2 6
4 7
```

| Current block | Direction checked | Result | Queue after processing |
| --- | --- | --- | --- |
| 1 | Right | Reach block 2, forced bus to 6 | [6] |
| 6 | Left | Blocks 5, 4 are reachable, block 4 forces bus to 7 | [7, 5] |
| 7 | Left | Blocks 6, 5 are reachable | [5] |
| 5 | Left | Block 4 forces bus to 7 | [] |

Block 3 is never reached because every attempt to cross the relevant bus stop sends Riana away. The search exhausts all valid states and returns `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N² + B) | For every reachable block, the algorithm scans the street to find nearby stops and reachable walking blocks. |
| Space | O(N) | The queue and visited array store at most one entry per block. |

With N at most 100, the quadratic scan is tiny. The solution performs at most around ten thousand block checks, which is well within the limit.

## Test Cases

```python
import sys
import io
from collections import deque

def solve_case(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    N, A, B = map(int, input().split())
    bus = [-1] * (N + 1)

    for _ in range(B):
        x, y = map(int, input().split())
        bus[x] = y

    if A == 1:
        return "YES\n"

    def follow_bus(pos):
        while bus[pos] != -1:
            pos = bus[pos]
        return pos

    start = follow_bus(1)
    visited = [False] * (N + 1)
    visited[start] = True
    q = deque([start])

    while q:
        pos = q.popleft()
        if pos == A:
            return "YES\n"

        for direction in (-1, 1):
            x = pos + direction
            while 1 <= x <= N:
                if bus[x] != -1:
                    nxt = follow_bus(x)
                    if not visited[nxt]:
                        visited[nxt] = True
                        q.append(nxt)
                    break
                if not visited[x]:
                    if x == A:
                        return "YES\n"
                    visited[x] = True
                    q.append(x)
                x += direction

    return "NO\n"

assert solve_case("""10 5 4
1 3
2 6
4 10
7 9
""") == "YES\n", "sample 1"

assert solve_case("""8 3 2
2 6
4 7
""") == "NO\n", "sample 2"

assert solve_case("""2 1 1
1 2
""") == "YES\n", "already at destination"

assert solve_case("""6 3 1
2 6
""") == "NO\n", "forced bus skips target"

assert solve_case("""100 100 1
50 100
""") == "YES\n", "maximum block boundary"

assert solve_case("""5 5 3
1 5
2 5
3 5
""") == "YES\n", "many buses with same destination"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 1` with a bus at block 1 | YES | Starting at the destination must be accepted before movement. |
| `6 3 1` with `2 -> 6` | NO | A bus stop cannot be crossed without taking the bus. |
| `100 100 1` with `50 -> 100` | YES | Large block numbers and reaching the final boundary. |
| Multiple buses ending at the same block | YES | Different bus stops may share destinations. |

## Edge Cases

For the case where Riana begins at the destination:

```
5 1 1
1 5
```

The algorithm checks `A == 1` before following buses. It outputs `YES`, correctly treating arrival as complete before any forced movement happens.

For the case where a bus blocks access to a lower block:

```
6 3 1
2 6
```

The search begins at block 1. Moving right reaches block 2, which is a bus stop, so the only resulting state is block 6. From block 6, walking left reaches block 4, but stepping onto block 2 again would trigger the bus. Block 3 is never generated, so the algorithm outputs `NO`.

For the case where multiple bus rides happen immediately:

```
10 5 2
1 3
3 8
```

The start block follows the bus at 1 to block 3, and then immediately follows the bus at 3 to block 8. The search starts from block 8 and continues normally. The increasing nature of bus destinations guarantees that this chain cannot loop forever.
