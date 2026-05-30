---
title: "CF 467A - George and Accommodation"
description: "The problem presents a simple scenario: George and Alex want to find a dormitory room together. Each room in the dormitory has a current occupancy and a maximum capacity."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 467
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 267 (Div. 2)"
rating: 800
weight: 467
solve_time_s: 61
verified: true
draft: false
---

[CF 467A - George and Accommodation](https://codeforces.com/problemset/problem/467/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem presents a simple scenario: George and Alex want to find a dormitory room together. Each room in the dormitory has a current occupancy and a maximum capacity. The input gives the number of rooms and, for each room, the current number of occupants and the total capacity. The task is to count how many rooms can fit both George and Alex at the same time.

The constraints are small: there are at most 100 rooms, and each room's capacity does not exceed 100. This means that any algorithm that examines each room individually, even with some nested checks, will run comfortably within the time limit. Since the numbers are all small integers, there is no risk of integer overflow or precision issues.

A subtle edge case arises when a room is almost full. For example, a room with a capacity of 2 and 1 occupant can accommodate only one more person, so George and Alex cannot both move in. Similarly, if a room is empty with capacity 2, it can exactly fit both. Failing to check the "space for two" condition will produce incorrect results.

## Approaches

The brute-force approach is straightforward. For each room, compute the available space by subtracting the current occupants from the capacity. If the available space is at least 2, increment a counter. Since there are at most 100 rooms, this requires at most 100 simple arithmetic checks, which is trivial for modern computers. There is no faster asymptotic approach, as we must examine each room at least once. The key insight is realizing that "room can fit both" reduces to a simple comparison `q_i - p_i >= 2`. This small simplification eliminates any unnecessary bookkeeping or complex logic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

The problem is simple enough that the brute-force solution is also optimal.

## Algorithm Walkthrough

1. Read the integer `n`, the number of rooms.
2. Initialize a counter `count` to zero. This will track the number of rooms that can accommodate both George and Alex.
3. For each of the next `n` lines:

1. Read the current number of occupants `p` and the room's capacity `q`.
2. Compute the available space as `q - p`.
3. If the available space is at least 2, increment `count` by 1.
4. After processing all rooms, print the value of `count`.

Why it works: At every step, the algorithm checks exactly the condition required for George and Alex to move in: the room must have at least two free spaces. Since all rooms are considered and each is evaluated independently, the final count accurately reflects all valid rooms.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
count = 0

for _ in range(n):
    p, q = map(int, input().split())
    if q - p >= 2:
        count += 1

print(count)
```

The solution follows the algorithm directly. The loop iterates over each room, subtracts the current occupancy from the capacity, and increments the counter if two or more spaces are available. The choice of `q - p >= 2` directly implements the problem's requirement. Using fast I/O is a precaution for larger input sizes, though for `n ≤ 100` it is not strictly necessary.

## Worked Examples

### Sample 1

Input:

```
3
1 1
2 2
3 3
```

| Room | p | q | q - p | Can fit both? | count |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | No | 0 |
| 2 | 2 | 2 | 0 | No | 0 |
| 3 | 3 | 3 | 0 | No | 0 |

Output: `0`

This trace shows that all rooms are full, so none can accommodate George and Alex.

### Sample 2 (custom)

Input:

```
4
0 2
1 3
2 5
3 5
```

| Room | p | q | q - p | Can fit both? | count |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 2 | Yes | 1 |
| 2 | 1 | 3 | 2 | Yes | 2 |
| 3 | 2 | 5 | 3 | Yes | 3 |
| 4 | 3 | 5 | 2 | Yes | 4 |

Output: `4`

This trace demonstrates that the algorithm correctly counts rooms that are partially full but have space for two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each room is examined exactly once, and the comparison is constant time. |
| Space | O(1) | Only a single counter and temporary variables are used; no additional data structures are needed. |

With `n ≤ 100`, the solution is orders of magnitude faster than necessary for the 1-second limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    count = 0
    for _ in range(n):
        p, q = map(int, input().split())
        if q - p >= 2:
            count += 1
    return str(count)

# provided samples
assert run("3\n1 1\n2 2\n3 3\n") == "0", "sample 1"

# custom cases
assert run("4\n0 2\n1 3\n2 5\n3 5\n") == "4", "all fit"
assert run("1\n0 0\n") == "0", "room has zero capacity"
assert run("2\n0 1\n1 2\n") == "0", "rooms cannot fit both"
assert run("5\n0 2\n1 2\n0 3\n2 2\n1 4\n") == "3", "mixed case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3\n1 1\n2 2\n3 3\n` | 0 | All rooms full |
| `4\n0 2\n1 3\n2 5\n3 5\n` | 4 | Multiple rooms with exact space |
| `1\n0 0\n` | 0 | Room with zero capacity |
| `2\n0 1\n1 2\n` | 0 | Rooms that cannot fit two people |
| `5\n0 2\n1 2\n0 3\n2 2\n1 4\n` | 3 | Mixed full and partially full rooms |

## Edge Cases

If a room has zero current occupants but capacity less than 2, it cannot fit both, e.g., `p=0, q=1`. The algorithm correctly computes `q - p = 1 < 2`, so `count` is not incremented. For a room with exactly two spaces left, `p=1, q=3`, the algorithm computes `q - p = 2`, incrementing `count` correctly. Rooms already at full capacity are ignored automatically. This confirms that the comparison `q - p >= 2` handles all subtle occupancy situations correctly.
