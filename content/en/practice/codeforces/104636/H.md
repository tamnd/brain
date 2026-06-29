---
title: "CF 104636H - Hotelier"
description: "We are simulating a very small hotel with exactly ten rooms indexed from 0 to 9. Each room can either be empty or occupied by exactly one guest. Over time, guests either arrive from one of two entrances or leave from a specific room."
date: "2026-06-29T17:07:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104636
codeforces_index: "H"
codeforces_contest_name: "\u041c\u0438\u0441\u0438\u0441 2023 \u043e\u0441\u0435\u043d\u044c - \u043c\u0430\u0441\u0441\u0438\u0432\u044b, \u0441\u0442\u0440\u043e\u043a\u0438"
rating: 0
weight: 104636
solve_time_s: 64
verified: true
draft: false
---

[CF 104636H - Hotelier](https://codeforces.com/problemset/problem/104636/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a very small hotel with exactly ten rooms indexed from 0 to 9. Each room can either be empty or occupied by exactly one guest. Over time, guests either arrive from one of two entrances or leave from a specific room.

The behavior on arrivals is the key rule: if a guest enters from the left entrance, they always take the leftmost currently empty room. If they enter from the right entrance, they always take the rightmost currently empty room. Departures are explicit: when we see a digit x, the guest currently occupying room x leaves, making it empty again.

The input is a chronological sequence of these events. We must simulate them in order and maintain the occupancy state of the ten rooms. The final output is a 10-character binary string where each position indicates whether that room is occupied at the end.

The constraints are large in terms of event count, up to 100,000 operations. This immediately tells us that any solution must process each event in constant time. Since the state space is tiny (only 10 rooms), we are not constrained by memory or structure size, only by avoiding repeated scanning work per event that would multiply into something like 10 × 100,000, which is still fine, but anything more complex or indirect would be unnecessary.

A naive mistake often comes from trying to reconstruct assignments or track “who is in which position” dynamically with complex data structures or recomputation of nearest empty rooms using full scans for every event without careful structure. Even though scanning 10 positions is constant, repeating unnecessary logic or mismanaging state updates on departures can cause incorrect results.

One subtle edge case is reusing rooms after a departure. For example, if a room is freed and later another arrival should reuse it based on proximity rules, the algorithm must correctly reconsider it as available immediately.

Another potential pitfall is misunderstanding that departures do not depend on arrival order but on room indices directly. A wrong approach might try to track guests in queues per entrance, but that is unnecessary and error-prone.

## Approaches

A straightforward simulation works because the system is extremely small. We maintain an array of size 10 representing whether each room is occupied. For each arrival, we scan left to right or right to left to find the first empty slot and assign it. For each departure, we simply mark the given room as empty.

This brute-force approach is already optimal in practice because scanning 10 elements is constant time. Even with 100,000 operations, we perform at most about 1,000,000 primitive checks, which is trivial.

We could attempt to “optimize” by maintaining separate structures for nearest free rooms from each side, but that would add complexity without benefit, since recomputing over 10 positions is already negligible.

The key insight is recognizing that the state space is fixed and tiny, so direct simulation is the intended solution. The problem is designed to test careful implementation rather than algorithmic optimization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(10n) | O(1) | Accepted |
| Optimal direct simulation | O(10n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a list `rooms` of size 10, initially all zeros.

### Steps

1. Initialize an array `rooms` of length 10 with all values set to 0.

This represents that all rooms are empty at the start.
2. Process each character in the input sequence in order.

The correctness depends on preserving exact chronological order.
3. If the character is `'L'`, scan from room 0 upward until we find the first empty room.

Assign it as occupied and stop immediately.

The reason this works is that the rule explicitly prioritizes the leftmost available slot.
4. If the character is `'R'`, scan from room 9 downward until we find the first empty room.

Assign it as occupied and stop immediately.

This enforces the symmetric rightmost selection rule.
5. If the character is a digit from `'0'` to `'9'`, convert it to an integer x and mark `rooms[x] = 0`.

This directly models a departure, freeing the specified room regardless of previous state.
6. After processing all events, output the array as a string of 0s and 1s.

### Why it works

At every step, `rooms[i]` exactly reflects whether room `i` is occupied after processing all previous events. Arrivals always choose the first available room in the required direction, and departures only clear a specific slot without affecting others. Since no event depends on anything except the current occupancy state, maintaining this invariant guarantees correctness for the final configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
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

    print(''.join(map(str, rooms)))

if __name__ == "__main__":
    main()
```

The implementation directly follows the simulation model. The only subtle part is handling arrivals with a linear scan in the correct direction. Since the array size is fixed at 10, this remains constant time per event.

The digit handling relies on ASCII conversion, which avoids any parsing overhead and ensures each departure directly maps to a room index.

## Worked Examples

### Example 1

Input:

```
8
LLRL1RL1
```

We track the room state:

| Step | Event | Rooms state |
| --- | --- | --- |
| 0 | initial | 0000000000 |
| 1 | L | 1000000000 |
| 2 | L | 1100000000 |
| 3 | R | 1100000001 |
| 4 | L | 1110000001 |
| 5 | 1 | 1010000001 |
| 6 | R | 1010000011 |
| 7 | L | 1110000011 |
| 8 | 1 | 1010000011 |

Final output is `1010000011`.

This trace confirms that arrivals always pick boundary-most free rooms, while deletions immediately open reuse opportunities for later arrivals.

### Example 2

Input:

```
9
L0L0LLRR9
```

| Step | Event | Rooms state |
| --- | --- | --- |
| 0 | initial | 0000000000 |
| 1 | L | 1000000000 |
| 2 | 0 | 0000000000 |
| 3 | L | 1000000000 |
| 4 | 0 | 0000000000 |
| 5 | L | 1000000000 |
| 6 | L | 1100000000 |
| 7 | R | 1100000001 |
| 8 | R | 1100000011 |
| 9 | 9 | 1100000010 |

Final output is `1100000010`.

This demonstrates repeated reuse of the same room after departures, showing that the system does not track identity of guests, only occupancy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10n) | Each event triggers a scan over at most 10 rooms |
| Space | O(1) | Only a fixed-size array of 10 rooms is maintained |

With n up to 100,000, the total operations remain around one million simple checks, which is easily within limits.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

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
            rooms[ord(c) - 48] = 0

    return ''.join(map(str, rooms))

# provided samples
assert solve("8\nLLRL1RL1\n") == "1010000011"
assert solve("9\nL0L0LLRR9\n") == "1100000010"

# custom cases
assert solve("1\nL\n") == "1000000000"
assert solve("2\nLR\n") == "1000000001"
assert solve("10\nLLLLLLLLLL\n") == "1111111111"
assert solve("20\nLRLRLRLRLRLRLRLRLRLR\n") == "1111111111"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 L | 1000000000 | single left arrival |
| LR | 1000000001 | reuse after right arrival |
| all L | 1111111111 | full occupancy |
| alternating LR | 1111111111 | stability under mixed arrivals |

## Edge Cases

One important edge case is repeated filling and emptying of the same room. Consider the input `L0L`. After the first arrival, room 0 is filled. The digit `0` frees it again, and the final `L` must correctly reuse room 0 as the leftmost available slot. The algorithm handles this naturally because every arrival always scans from the start of the array, and the freed slot is immediately visible.

Another edge case is alternating arrivals that constantly flip occupancy at both ends, such as `LRLRLR...`. The system must never “skip” a free room due to stale state. Since each step recomputes availability directly from `rooms`, no historical assumptions are made, so reuse always reflects the current configuration.

A third case is full occupancy followed by departures. Even if all rooms become full, a digit event immediately frees one room, and the next arrival must correctly choose based on updated state. Because every operation updates the same shared array, there is no hidden state that could delay availability updates.
