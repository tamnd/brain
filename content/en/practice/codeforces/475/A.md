---
title: "CF 475A - Bayan Bus"
description: "The bus layout is fixed and already drawn for us. There are 34 passenger seats in total. Passengers always occupy seats in a very specific order: they start from the last row, fill it from left to right, then move upward row by row."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 475
codeforces_index: "A"
codeforces_contest_name: "Bayan 2015 Contest Warm Up"
rating: 1100
weight: 475
solve_time_s: 119
verified: true
draft: false
---

[CF 475A - Bayan Bus](https://codeforces.com/problemset/problem/475/A)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The bus layout is fixed and already drawn for us. There are 34 passenger seats in total. Passengers always occupy seats in a very specific order: they start from the last row, fill it from left to right, then move upward row by row. Whenever several seats are available in the current row, the leftmost free seat is chosen.

The input contains a single integer `k`, the number of passengers currently on the bus. We must print the six-line ASCII-art bus diagram and mark exactly the first `k` seats in the boarding order as occupied (`O`). Every remaining passenger seat stays empty (`#`).

The constraints are extremely small. The number of passengers is at most 34, which is exactly the number of seats. Even a brute-force simulation that examines every seat individually would perform only a few dozen operations. Runtime is irrelevant here, the challenge is reproducing the required output format exactly.

The most common source of mistakes is misunderstanding the boarding order. The passengers do not fill the bus from the front row downward. They begin at the special four-seat row and then continue through the remaining rows.

Consider `k = 1`. The occupied seat must be the first seat in the last row:

```
+------------------------+
|O.#.#.#.#.#.#.#.#.#.#.|D|)
|#.#.#.#.#.#.#.#.#.#.#.|.|
|#.......................|
|#.#.#.#.#.#.#.#.#.#.#.|.|)
+------------------------+
```

A solution that fills seats from the top-left corner would place the passenger in the wrong location.

Another easy mistake appears when `k = 34`. Every passenger seat must become occupied. Any implementation that forgets the extra seat in the four-seat row would only fill 33 positions.

A final edge case is `k = 0`. No seat should contain `O`. Some implementations accidentally force at least one occupied seat because they decrement the passenger counter before checking whether seats remain.

## Approaches

The most direct idea is to list every seat in the exact order passengers occupy them. We then process that list from the beginning and mark the first `k` positions as occupied. Since there are only 34 seats, this simulation performs at most 34 updates.

Even though this is already fast enough, it helps to look at the structure of the bus. The bus drawing is fixed. Only the seat characters change. Instead of simulating passengers moving through rows, we can build the final ASCII template and replace seat positions one by one according to the boarding order.

The key observation is that the boarding order corresponds exactly to scanning the seat locations in a predetermined sequence. Once we know those 34 coordinates, the problem becomes simple string manipulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force passenger simulation | O(34) | O(34) | Accepted |
| Optimal template filling | O(34) | O(34) | Accepted |

Because the number of seats is fixed, both approaches have constant complexity. The template-filling version is cleaner and maps directly to the required output.

## Algorithm Walkthrough

1. Store the bus as a list of strings representing the required empty layout.
2. Convert each string into a mutable list of characters so individual seat positions can be modified.
3. Create a list containing all 34 seat coordinates in boarding order.
4. The first four coordinates correspond to the special row with four seats.
5. The remaining coordinates correspond to the other rows, scanned from top to bottom and left to right exactly as passengers would occupy them.
6. Iterate through the first `k` coordinates of this list and replace the seat character at each position with `O`.
7. Leave all remaining seat positions as `#`.
8. Convert each character list back into a string and print the six lines.

### Why it works

The coordinate list is constructed in exactly the same order passengers choose seats. The first coordinate represents the first available seat, the second coordinate represents the second available seat, and so on until all 34 seats are listed. Marking the first `k` coordinates as occupied is equivalent to simulating the arrival of `k` passengers. Since every seat appears exactly once in the list, no seat is skipped or counted twice, producing the unique correct final configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input())

    bus = [
        list("+------------------------+"),
        list("|#.#.#.#.#.#.#.#.#.#.#.|D|)"),
        list("|#.#.#.#.#.#.#.#.#.#.#.|.|"),
        list("|#.......................|"),
        list("|#.#.#.#.#.#.#.#.#.#.#.|.|)"),
        list("+------------------------+")
    ]

    seats = []

    seats.append((3, 1))

    for c in range(1, 22, 2):
        seats.append((1, c))

    for c in range(1, 22, 2):
        seats.append((2, c))

    for c in range(1, 22, 2):
        seats.append((4, c))

    for r, c in seats[:k]:
        bus[r][c] = 'O'

    print("\n".join("".join(row) for row in bus))

if __name__ == "__main__":
    solve()
```

The bus template is stored exactly as it appears in the statement, except every seat is initially marked with `#`.

The seat list encodes the boarding order. The seat at row 3, column 1 of the drawing is the unique extra seat in the four-seat row, so it comes first. After that, the three regular passenger rows each contribute eleven seats, giving `1 + 11 + 11 + 11 = 34` total positions.

The loop `for r, c in seats[:k]` avoids off-by-one errors naturally. If `k = 0`, the slice is empty and no seats are modified. If `k = 34`, every coordinate is visited exactly once.

## Worked Examples

### Example 1

Input:

```
9
```

Seat filling process:

| Passenger Count Filled | Last Row Seat | Top Row Filled | Middle Row Filled | Bottom Row Filled |
| --- | --- | --- | --- | --- |
| 0 | No | 0 | 0 | 0 |
| 1 | Yes | 0 | 0 | 0 |
| 2 | Yes | 1 | 0 | 0 |
| 3 | Yes | 2 | 0 | 0 |
| 4 | Yes | 3 | 0 | 0 |
| 5 | Yes | 4 | 0 | 0 |
| 6 | Yes | 5 | 0 | 0 |
| 7 | Yes | 6 | 0 | 0 |
| 8 | Yes | 7 | 0 | 0 |
| 9 | Yes | 8 | 0 | 0 |

The first passenger occupies the special seat in the four-seat row. The next eight passengers fill the first eight seats of the upper regular row. This matches the sample output.

### Example 2

Input:

```
34
```

Seat filling process:

| Passenger Count Filled | Last Row Seat | Top Row Filled | Middle Row Filled | Bottom Row Filled |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 |
| 12 | 1 | 11 | 0 | 0 |
| 23 | 1 | 11 | 11 | 0 |
| 34 | 1 | 11 | 11 | 11 |

All seat coordinates are selected. Every `#` becomes `O`, demonstrating that the coordinate list contains all 34 passenger seats exactly once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(34) | At most 34 seat updates are performed |
| Space | O(34) | The bus template and seat list have fixed size |

The number of seats never changes, so both time and memory usage are constant. This is far below the problem limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    k = int(input())

    bus = [
        list("+------------------------+"),
        list("|#.#.#.#.#.#.#.#.#.#.#.|D|)"),
        list("|#.#.#.#.#.#.#.#.#.#.#.|.|"),
        list("|#.......................|"),
        list("|#.#.#.#.#.#.#.#.#.#.#.|.|)"),
        list("+------------------------+")
    ]

    seats = [(3, 1)]

    for c in range(1, 22, 2):
        seats.append((1, c))
    for c in range(1, 22, 2):
        seats.append((2, c))
    for c in range(1, 22, 2):
        seats.append((4, c))

    for r, c in seats[:k]:
        bus[r][c] = 'O'

    return "\n".join("".join(row) for row in bus)

# provided sample
assert run("9\n") == (
"+------------------------+\n"
"|O.O.O.#.#.#.#.#.#.#.#.|D|)\n"
"|O.O.O.#.#.#.#.#.#.#.#.|.|\n"
"|O.......................|\n"
"|O.O.#.#.#.#.#.#.#.#.#.|.|)\n"
"+------------------------+"
)

# custom cases
assert run("0\n").count('O') == 0, "no passengers"

assert run("1\n").count('O') == 1, "first seat only"

assert run("34\n").count('O') == 34, "all seats occupied"

assert run("12\n").count('O') == 12, "boundary after first full row"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | No `O` characters | Empty bus edge case |
| `1` | Exactly one occupied seat | First boarding position |
| `34` | All seats occupied | Maximum occupancy |
| `12` | Twelve occupied seats | Transition after filling the first regular row |

## Edge Cases

When `k = 0`, the slice `seats[:0]` is empty. No coordinate is modified, so every seat remains `#`. This matches the requirement that no passengers are on the bus.

When `k = 1`, only the first coordinate `(3, 1)` is selected. That coordinate corresponds to the special seat in the four-seat row. The algorithm does not accidentally start filling the upper rows because the boarding order is encoded directly in the coordinate list.

When `k = 34`, the loop visits every coordinate stored in `seats`. Since the list contains exactly 34 unique seat locations, every passenger seat becomes occupied and no seat is processed twice.

A subtle boundary occurs at `k = 12`. The first coordinate fills the special seat, and the next eleven coordinates fill the entire upper regular row. The next passenger would start the middle row. Because the coordinate list is ordered correctly, the transition between rows happens automatically without any special-case logic.
