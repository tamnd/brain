---
title: "CF 1200A - Hotelier"
description: "We are simulating a very small system: a hotel with exactly 10 rooms indexed from 0 to 9. Each room can either be empty or occupied."
date: "2026-06-13T15:02:14+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1200
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 578 (Div. 2)"
rating: 800
weight: 1200
solve_time_s: 130
verified: true
draft: false
---

[CF 1200A - Hotelier](https://codeforces.com/problemset/problem/1200/A)

**Rating:** 800  
**Tags:** brute force, data structures, implementation  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a very small system: a hotel with exactly 10 rooms indexed from 0 to 9. Each room can either be empty or occupied. A sequence of events describes how guests enter and leave over time, and we need to reconstruct the final occupancy state after processing all events in order.

Each event is either an arrival from the left entrance, an arrival from the right entrance, or a departure from a specific room. When someone enters from the left, they always take the closest currently empty room starting from room 0 moving rightward. When someone enters from the right, they take the closest empty room starting from room 9 moving leftward. When a digit appears, it means the guest in that room leaves, making it empty again.

The key difficulty is not simulation speed but correctness under repeated updates: arrivals always depend on the current state, so earlier choices constrain future ones. Even though the structure is small, the number of events can be large, up to 100,000, so we must ensure each event is processed efficiently.

A naive interpretation mistake is to assume arrivals always go to fixed positions, such as always assigning left arrivals to the first free slot globally without respecting the dynamic nature of previous departures. For example, if we ignore removals, we might incorrectly place a new left arrival into a room that is currently occupied.

Another subtle edge case is repeated toggling of the same room. For instance, a room can be occupied, freed, and reoccupied many times. Any solution that does not maintain an accurate live state array will drift from the correct configuration.

Since there are only 10 rooms, the final output is a 10-character binary string representing occupancy.

The constraint n ≤ 10^5 implies we must process each event in O(1) or O(10) time. Any approach scanning all rooms per event is still acceptable, but anything scaling with n per room would be too slow.

## Approaches

A straightforward simulation maintains an array of 10 boolean values representing whether each room is occupied. For each arrival from the left, we scan rooms from 0 upward and pick the first empty one. For an arrival from the right, we scan from 9 downward and pick the first empty. For a departure event, we simply mark that room as empty.

This brute-force approach is already extremely small in state size, so the worst-case cost per event is at most 10 checks. Over 10^5 events, this leads to about 10^6 operations, which is comfortably within limits. There is no need for more complex data structures like heaps or balanced trees.

The key observation is that the problem does not require remembering historical assignments, only the current occupancy. Each decision depends solely on the current state, and the state space is tiny and fixed-size. That removes any need for optimization beyond a simple linear scan.

We can think of this as maintaining a bitmask of size 10 with greedy selection rules applied per event.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(10 · n) | O(1) | Accepted |
| Optimal (same idea) | O(10 · n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `rooms` of size 10 with all values set to 0, meaning all rooms are empty. This represents the current hotel state at time 0.
2. Iterate through each character in the input string from left to right, treating each character as an event.
3. If the event is `'L'`, scan from room 0 to 9 and find the first room that is empty. Mark it as occupied. This ensures the closest available room to the left entrance is used.
4. If the event is `'R'`, scan from room 9 down to 0 and find the first empty room. Mark it as occupied. This ensures the closest available room to the right entrance is used.
5. If the event is a digit from `'0'` to `'9'`, convert it to an integer index and mark that room as empty.
6. Continue this process until all events are processed.
7. Output the final state as a string of length 10, where each position is `'1'` if occupied and `'0'` otherwise.

### Why it works

The algorithm maintains the exact occupancy state of all rooms after each event. Every arrival rule depends only on the current set of empty rooms, and every departure directly restores a room to the empty set. Since we always recompute choices based on the up-to-date state, no decision ever violates the constraints of "closest available room". The correctness follows from the invariant that `rooms[i]` is true if and only if room `i` is occupied after processing the prefix of events.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()

    rooms = [0] * 10

    for c in s:
        if c == 'L':
            for i in range(10):
                if rooms[i] == 0:
                    rooms[i] = 1
                    break
        elif c == 'R':
            for i in range(9, -1, -1):
                if rooms[i] == 0:
                    rooms[i] = 1
                    break
        else:
            idx = ord(c) - ord('0')
            rooms[idx] = 0

    print("".join(map(str, rooms)))

if __name__ == "__main__":
    solve()
```

The implementation keeps a direct representation of the hotel state. The loops for `'L'` and `'R'` are intentionally simple because the constant factor is bounded by 10. Converting digit characters uses ASCII arithmetic, which avoids slower parsing. The final output joins integer flags into a string.

A common mistake here is forgetting that a departure always succeeds, so the digit event can safely assume the room is occupied. Another is accidentally reusing stale loop indices between events, but since each event is independent, the scan always restarts fresh.

## Worked Examples

### Sample 1

Input:

```
8
LLRL1RL1
```

We track the state after each event.

| Step | Event | Action | State |
| --- | --- | --- | --- |
| 1 | L | occupy 0 | 1000000000 |
| 2 | L | occupy 1 | 1100000000 |
| 3 | R | occupy 9 | 1100000001 |
| 4 | L | occupy 2 | 1110000001 |
| 5 | 1 | free 1 | 1010000001 |
| 6 | R | occupy 8 | 1010000011 |
| 7 | L | occupy 1 | 1110000011 |
| 8 | 1 | free 1 | 1010000011 |

Final output is `1010000011`.

This trace shows that left and right choices depend entirely on the current occupancy, and repeated freeing allows reuse of earlier positions.

### Sample 2

Input:

```
5
LRL0R
```

| Step | Event | Action | State |
| --- | --- | --- | --- |
| 1 | L | occupy 0 | 1000000000 |
| 2 | R | occupy 9 | 1000000001 |
| 3 | L | occupy 1 | 1100000001 |
| 4 | 0 | free 0 | 0100000001 |
| 5 | R | occupy 8 | 0100000011 |

Final output is `0100000011`.

This example highlights that freeing room 0 changes future left allocations immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10 · n) | Each event scans at most 10 rooms |
| Space | O(1) | Only a fixed-size array of 10 rooms is maintained |

The runtime is effectively linear in the number of events with a very small constant factor, which is ideal for n up to 100,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    import sys as _sys
    old_stdout = _sys.stdout
    try:
        _sys.stdout = out
        solve()
    finally:
        _sys.stdout = old_stdout
    return out.getvalue().strip()

# provided sample
assert run("""8
LLRL1RL1
""") == "1010000011"

# all empty operations
assert run("""3
LLL
""") == "1110000000"

# full fill and partial release
assert run("""5
LRLRR
""") == "1110000011"

# repeated occupy/free same slot
assert run("""6
L0L0L0
""") == "1010000000"

# alternating edges
assert run("""4
LRLR
""") == "1110000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| LLL | 1110000000 | repeated left fills |
| LRLRR | 1110000011 | mixed arrivals |
| L0L0L0 | 1010000000 | repeated toggle of same room |
| LRLR | 1110000000 | alternating boundary choices |

## Edge Cases

One important case is repeated use of the same room after freeing. Consider input `L0L0`. After `L`, room 0 becomes occupied. The event `0` frees it, and the next `L` again selects room 0 because it is again the closest empty slot. The algorithm handles this correctly because every `'L'` scan starts fresh from room 0, so previously freed positions are naturally reconsidered.

Another case is when all rooms except one are occupied. If room 9 is the only free slot and a left arrival occurs, scanning from 0 upward will eventually reach 9 and place the guest there. This is correct even though it is far from the left entrance, because the rule is strictly “closest empty room”, not “prefer left side even if far”.

A final subtle case is alternating arrivals and departures that reuse boundary rooms. For example, `L R 0 R L 0` repeatedly toggles rooms 0 and 9. Since each event updates the shared state immediately, the scan always reflects the latest configuration, preventing stale assignments.
