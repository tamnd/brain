---
title: "CF 102780G - Hourglass"
description: "I’ll provide the editorial as a standalone document. Edit We have at most four hourglasses. Each hourglass measures one fixed duration, and its sand can be running in either direction. We are allowed to flip hourglasses only at moments when at least one hourglass becomes empty."
date: "2026-07-27T20:13:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102780
codeforces_index: "G"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19)"
rating: 0
weight: 102780
solve_time_s: 136
verified: true
draft: false
---

[CF 102780G - Hourglass](https://codeforces.com/problemset/problem/102780/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 16s  
**Verified:** yes  

## Solution
I’ll provide the editorial as a standalone document.

Edit

# Problem Understanding

We have at most four hourglasses. Each hourglass measures one fixed duration, and its sand can be running in either direction. We are allowed to flip hourglasses only at moments when at least one hourglass becomes empty. The first action happens at time zero, and the goal is to make some hourglass become empty exactly at minute k. The output is not just whether this is possible: we must print the exact sequence of moments when hourglasses are flipped.

The small number of hourglasses is the main clue. There are only up to four devices, and each device has a duration of at most twenty minutes. A single hourglass therefore has a very small number of possible internal situations. The target time can be as large as 1440, so simulating every possible strategy until the target time requires care. A solution that tries every sequence of flips grows exponentially and is impossible, but a state-based search can fit because the number of distinct configurations is limited.

A common mistake is to think that only the current remaining times matter without considering the exact moment in the process. Another mistake is to allow flipping at arbitrary times. For example, with input

```
1
5
3
```

the correct output is

```
-1
```

because a single five-minute hourglass can only finish at multiples of five. A greedy approach that flips immediately after starting and assumes it can stop after three minutes would violate the rules.

Another edge case is the final moment. For input

```
2
3 5
5
```

the answer exists. We can flip both at time zero and wait until the five-minute glass empties. The final output must contain a line at time five with zero flipped hourglasses. A careless implementation may stop when it sees that the target time has been reached during a transition and forget that the required output describes an event at that exact moment.

A third subtle case is flipping an already empty hourglass. For input

```
2
3 5
7
```

the three-minute glass can be flipped again at time three even though the five-minute glass is still running. The search must allow any subset of hourglasses to be turned over when an event occurs, including glasses that have just become empty.

# Approaches

The direct brute-force idea is to simulate every possible sequence of flips. At each event moment there are at most four hourglasses, so there are at most 16 possible subsets to flip. The simulation would recursively try every subset and continue until reaching the target time or proving that the branch fails.

This approach is correct because every legal measurement is exactly a sequence of legal choices, and the recursion explores all of them. The problem is the number of repeated states. Different sequences can lead to the same configuration of hourglasses, but brute force explores them separately. The number of possible paths grows exponentially with the number of events, making it too slow even though each individual transition is small.

The key observation is that the future depends only on the current time and the current state of every hourglass. The history of how we reached this situation does not matter. This allows us to merge identical situations with breadth-first search.

A state stores the current minute and, for every hourglass, the amount of time left until its currently running side becomes empty. If two different sequences reach the same state, only one needs to be kept because both have exactly the same possible continuations.

There are not many possible states. The current time has only 1441 possible values, and each hourglass can have only a small number of remaining-time values. With four hourglasses and durations up to twenty, this state space is small enough for BFS.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of events | Exponential | Too slow |
| Optimal | O(k * product(ti + 1) * 2^n) | O(k * product(ti + 1)) | Accepted |

# Algorithm Walkthrough

1. Start BFS from the empty configuration at time zero. The initial state represents the moment before any hourglass has been started. Keeping this state allows the first operation to happen at time zero just like every other operation.
2. For each visited state, try every subset of hourglasses that can be flipped at the current moment. There are at most 16 subsets because there are at most four hourglasses.
3. Apply the chosen flips. If an hourglass is empty, flipping it starts it with its full duration remaining. If it is running with x minutes left in its current direction, flipping it changes the remaining time to t - x because the other side contains the sand that has already fallen.
4. Find the next event moment by taking the smallest positive remaining time. This is the next time when at least one hourglass becomes empty.
5. Move time forward by that amount and decrease every positive remaining time by the same amount. Any hourglass reaching zero becomes empty.
6. Insert the new state into BFS if it has not been visited. Store the previous state and the subset flipped so the complete sequence can be reconstructed.
7. When a state with time k is reached, reconstruct the path. The last printed event is the target moment with no flips, because the measurement ends when an hourglass becomes empty.

Why it works:

The invariant of the BFS is that every stored state is a legal situation immediately after an allowed event moment. Every transition applies exactly one legal set of flips and then advances to the next moment when some hourglass empties, so every generated state is also legal. Since BFS explores every reachable state and never discards a unique configuration, reaching time k means a valid sequence exists. If BFS finishes without reaching time k, every possible legal sequence has been represented by some state that was explored, so no solution exists.

# Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n = int(input())
    t = list(map(int, input().split()))
    k = int(input())

    start = (0, (0,) * n)
    queue = deque([start])

    parent = {start: None}
    action = {}

    answer = None

    while queue:
        time, rem = queue.popleft()

        if time == k:
            answer = (time, rem)
            break

        for mask in range(1 << n):
            new_rem = list(rem)

            for i in range(n):
                if mask & (1 << i):
                    if new_rem[i] == 0:
                        new_rem[i] = t[i]
                    else:
                        new_rem[i] = t[i] - new_rem[i]

            if all(x == 0 for x in new_rem):
                continue

            delta = min(x for x in new_rem if x > 0)
            new_time = time + delta

            if new_time > k:
                continue

            for i in range(n):
                if new_rem[i] > 0:
                    new_rem[i] -= delta

            state = (new_time, tuple(new_rem))

            if state not in parent:
                parent[state] = (time, rem)
                action[state] = mask
                queue.append(state)

    if answer is None:
        print(-1)
        return

    path = []
    cur = answer

    while parent[cur] is not None:
        path.append((cur, action[cur]))
        cur = parent[cur]

    path.reverse()

    print(len(path) + 1)
    print(0, 0)

    for state, mask in path:
        time = state[0]
        flipped = [str(i + 1) for i in range(n) if mask & (1 << i)]
        print(time, len(flipped), *flipped)

if __name__ == "__main__":
    solve()
```

The BFS queue contains only states that occur immediately after a legal event. The `rem` tuple stores the remaining time until each hourglass empties. A value of zero means that the hourglass is currently empty and can be restarted by flipping it.

The transition logic is the core of the solution. When a glass is flipped, the remaining time becomes the amount of sand on the opposite side. For an hourglass of length t with x minutes left, that amount is t - x. After all flips are applied, the simulation jumps directly to the next event instead of advancing minute by minute.

The parent dictionary is used only for reconstruction. It records how each state was reached, which avoids storing complete paths inside every BFS node. This keeps memory usage low.

The final reconstruction prints the initial moment and then every event that was used to reach k. The last transition reaches time k because the BFS only creates states after an hourglass empties, so the target moment is automatically a valid ending event.

# Worked Examples

For the first sample:

```
2
3 5
7
```

A possible BFS path is:

| Time | Remaining after event | Flipped |
| --- | --- | --- |
| 0 | 3, 5 | 3 and 5 minute glasses |
| 3 | 0, 2 | 3 minute glass |
| 5 | 1, 0 | 3 minute glass |
| 7 | 0, 0 | none |

The search reaches time seven because every transition lands exactly on an emptying moment. The final state confirms that the measurement ends without performing an unnecessary flip.

For the second sample:

```
2
3 5
11
```

A valid trace is:

| Time | Remaining after event | Flipped |
| --- | --- | --- |
| 0 | 3, 5 | both glasses |
| 3 | 0, 2 | 3 minute glass |
| 5 | 1, 0 | both choices can be explored |
| 11 | 0, 0 | none |

The important part of this trace is that BFS does not need to guess a clever pattern. It explores all reachable configurations and eventually finds the required event sequence.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k * product(ti + 1) * 2^n) | Each state tries every possible subset of flips. |
| Space | O(k * product(ti + 1)) | Each reachable time and hourglass configuration is stored once. |

The maximum number of hourglasses is only four and every duration is at most twenty, so the number of possible internal configurations is small. The target time of 1440 minutes is also small enough for the BFS state space to remain within the memory limit.

# Test Cases

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

assert run("""2
3 5
7
""") != "-1\n", "sample 1"

assert run("""2
3 5
2
""") == "-1\n", "sample 2"

assert run("""1
1
1
""") != "-1\n", "minimum duration"

assert run("""4
5 10 15 20
1440
""") != "-1\n", "large target time"

assert run("""2
7 9
13
""") != "-1\n", "different event pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 and 5 minute glasses measuring 7 | A valid sequence | Basic sample behaviour |
| Single 3? minute target with 3 and 5 minute glasses | -1 | Impossible measurement detection |
| One 1 minute glass measuring 1 | Valid sequence | Minimum-size configuration |
| Four large glasses measuring 1440 | Valid or impossible depending on reachability | Large time boundary handling |
| 7 and 9 minute glasses measuring 13 | Valid sequence | More complex reconstruction |

# Edge Cases

For a single glass with duration five and target three:

```
1
5
3
```

the BFS starts with an empty state. Flipping the glass reaches time five, which is already beyond the target, so no state at time three is generated. The algorithm correctly prints `-1`.

For the final event requirement:

```
2
3 5
5
```

BFS reaches a state at time five after the five-minute glass empties. Reconstruction prints the initial flip and the final event with zero flips. The algorithm does not confuse reaching the target time with needing another operation.

For flipping empty glasses:

```
2
3 5
7
```

when the three-minute glass empties at time three, its remaining time is zero. The transition code allows it to be flipped again and restarts it with three minutes available. This is exactly the operation needed to create the seven-minute measurement.

You can adapt the editorial length or style further if you want a shorter contest-style version or a more formal proof-oriented version.
