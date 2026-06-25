---
title: "CF 106102F - Plane Seating Roulette"
description: "Passengers board an airplane one by one. Every passenger has a fixed row and a fixed seat in that row. Within a row, seat 1 is next to the window and seat m is next to the aisle. A passenger always enters from the aisle side and walks toward their assigned seat."
date: "2026-06-25T11:49:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106102
codeforces_index: "F"
codeforces_contest_name: "AGM 2025, Final Round, Day 1"
rating: 0
weight: 106102
solve_time_s: 44
verified: true
draft: false
---

[CF 106102F - Plane Seating Roulette](https://codeforces.com/problemset/problem/106102/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

Passengers board an airplane one by one. Every passenger has a fixed row and a fixed seat in that row.

Within a row, seat `1` is next to the window and seat `m` is next to the aisle. A passenger always enters from the aisle side and walks toward their assigned seat.

Suppose a passenger wants seat `s`. While walking from the aisle toward that seat, they pass all seats with numbers larger than `s`. If some of those seats are already occupied, the seated passengers must stand up to let the newcomer pass. Each standing action contributes `1` to the answer.

The task is to compute the total number of times passengers stand up during the entire boarding process.

The number of rows and seats can be as large as `10^9`, but only `k ≤ 10^5` passengers are actually present. This immediately tells us that any solution depending on all rows or all seat numbers is impossible. The only relevant data are the occupied seats that appear in the input.

A subtle point is that interactions never happen between different rows. A passenger walking to a seat in row `r` only affects people already seated in the same row.

Consider a row whose passengers arrive in this order:

```
seat 5
seat 2
```

When the second passenger arrives, seat `5` is already occupied and lies between the aisle and seat `2`, so the passenger at seat `5` stands once. The contribution is `1`.

Now consider:

```
seat 2
seat 5
```

The second passenger walks only to seat `5`, which is next to the aisle. Nobody blocks the way. The contribution is `0`.

A careless implementation might count occupied seats with smaller seat numbers instead of larger ones and obtain the opposite result.

Another easy mistake is to mix passengers from different rows.

Example:

```
row 1 seat 5
row 2 seat 4
row 1 seat 2
```

Only the passenger in row `1`, seat `5` matters for the last arrival. The passenger in row `2` is irrelevant because rows are independent.

The correct answer is `1`, not `2`.

## Approaches

A direct simulation is straightforward.

For every arriving passenger, scan all previously seated passengers in the same row and count how many occupy seats with larger seat numbers. Each such passenger must stand once.

This is correct because a seated passenger blocks the path exactly when their seat lies between the aisle and the destination seat.

The problem is the running time. With `k = 100000`, checking all earlier passengers for every arrival requires roughly

```
1 + 2 + ... + 99999 ≈ 5 × 10^9
```

comparisons in the worst case, which is far beyond the limit.

The key observation is that, within a fixed row, we are counting inversions.

Suppose the arrival order of seats in a row is

```
a1, a2, a3, ...
```

When passenger `ai` arrives, every earlier occupied seat larger than `ai` causes one stand-up event.

So the contribution of this row is exactly the number of pairs

```
i < j and ai > aj
```

which is the classical inversion count.

Once the problem is reduced to inversion counting, we can process each row independently using a Fenwick tree. Since seat numbers can be as large as `10^9`, we compress the seat numbers that actually appear in the row.

The total number of passengers over all rows is at most `100000`, so the overall complexity becomes `O(k log k)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k²) | O(k) | Too slow |
| Optimal | O(k log k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read all passengers in boarding order.
2. Group seat numbers by row while preserving arrival order inside each row.
3. For each row, collect all seat numbers appearing in that row and sort them to build a coordinate compression mapping.
4. Create a Fenwick tree whose size equals the number of distinct seats in that row.
5. Process the passengers of that row in arrival order.
6. For the current seat `s`, find its compressed position `p`.
7. Let `seen` be the number of passengers already processed in this row.
8. Query the Fenwick tree for how many processed seats have compressed index `≤ p`.
9. The number of earlier seats strictly greater than `s` is

```
seen - count(≤ s)
```

Add this value to the answer.
10. Insert seat `s` into the Fenwick tree and continue.
11. Sum the contributions from all rows and print the result.

### Why it works

For a passenger assigned to seat `s`, the only people who must stand are passengers already seated at seats with larger numbers in the same row. Those are exactly the seats located between the aisle and `s`.

When processing a row in arrival order, every stand-up event corresponds to a pair of passengers where the earlier passenger sits at a larger seat number than the later passenger. Such pairs are precisely inversions of the seat-number sequence for that row.

The Fenwick tree maintains all previously processed seats. At each step it counts how many earlier seats are larger than the current one, which is exactly the number of stand-up events caused by this passenger. Summing these values over all rows gives the required total.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, val):
        while idx <= self.n:
            self.bit[idx] += val
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        while idx > 0:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

def solve():
    n, m, k = map(int, input().split())

    rows = {}

    for _ in range(k):
        r, s = map(int, input().split())
        rows.setdefault(r, []).append(s)

    answer = 0

    for seats in rows.values():
        vals = sorted(set(seats))
        comp = {v: i + 1 for i, v in enumerate(vals)}

        fw = Fenwick(len(vals))
        seen = 0

        for seat in seats:
            pos = comp[seat]

            not_greater = fw.sum(pos)
            greater = seen - not_greater

            answer += greater

            fw.add(pos, 1)
            seen += 1

    print(answer)

solve()
```

The dictionary `rows` stores, for every row, the sequence of seat numbers in boarding order. Preserving the order is essential because inversions depend on arrival order.

For each row, seat numbers are coordinate-compressed. The original seat numbers may be as large as `10^9`, but only the relative ordering matters for inversion counting.

The Fenwick tree stores frequencies of previously processed seats. When processing a seat, `fw.sum(pos)` gives the number of earlier seats whose seat number is less than or equal to the current one. Subtracting this from `seen` leaves exactly the number of earlier seats that are larger.

The answer can reach roughly

```
100000 × 99999 / 2
```

so it must be stored in a 64-bit capable integer. Python integers handle this automatically.

## Worked Examples

### Example 1

Input:

```
1 5 3
1 5
1 2
1 4
```

Seat sequence in the only row:

```
[5, 2, 4]
```

| Passenger | Seat | Seen Before | Earlier Greater Seats | Added |
| --- | --- | --- | --- | --- |
| 1 | 5 | 0 | 0 | 0 |
| 2 | 2 | 1 | 1 | 1 |
| 3 | 4 | 2 | 1 | 1 |

Total answer:

```
2
```

The second passenger is blocked by seat `5`. The third passenger is also blocked by seat `5`, but not by seat `2`.

### Example 2

Input:

```
2 10 5
1 8
2 7
1 3
2 2
1 5
```

Row 1 sequence:

```
[8, 3, 5]
```

Row 2 sequence:

```
[7, 2]
```

For row 1:

| Passenger | Seat | Earlier Greater Seats |
| --- | --- | --- |
| 1 | 8 | 0 |
| 2 | 3 | 1 |
| 3 | 5 | 1 |

Contribution = 2.

For row 2:

| Passenger | Seat | Earlier Greater Seats |
| --- | --- | --- |
| 1 | 7 | 0 |
| 2 | 2 | 1 |

Contribution = 1.

Final answer:

```
3
```

This example demonstrates that rows are processed independently and their inversion counts are simply added together.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log k) | Each passenger participates in one Fenwick update and one query |
| Space | O(k) | Stored passenger data, compression arrays, and Fenwick trees |

Since `k ≤ 100000`, `O(k log k)` is easily fast enough. The memory usage is linear in the number of passengers and remains comfortably within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, idx, val):
            while idx <= self.n:
                self.bit[idx] += val
                idx += idx & -idx

        def sum(self, idx):
            res = 0
            while idx:
                res += self.bit[idx]
                idx -= idx & -idx
            return res

    n, m, k = map(int, input().split())

    rows = {}
    for _ in range(k):
        r, s = map(int, input().split())
        rows.setdefault(r, []).append(s)

    ans = 0

    for seats in rows.values():
        vals = sorted(set(seats))
        comp = {v: i + 1 for i, v in enumerate(vals)}

        fw = Fenwick(len(vals))
        seen = 0

        for seat in seats:
            p = comp[seat]
            ans += seen - fw.sum(p)
            fw.add(p, 1)
            seen += 1

    return str(ans) + "\n"

assert run("1 5 1\n1 3\n") == "0\n", "single passenger"

assert run(
    "1 5 3\n"
    "1 5\n"
    "1 2\n"
    "1 4\n"
) == "2\n", "basic inversion counting"

assert run(
    "2 10 5\n"
    "1 8\n"
    "2 7\n"
    "1 3\n"
    "2 2\n"
    "1 5\n"
) == "3\n", "multiple rows"

assert run(
    "1 5 5\n"
    "1 1\n"
    "1 2\n"
    "1 3\n"
    "1 4\n"
    "1 5\n"
) == "0\n", "already increasing"

assert run(
    "1 5 5\n"
    "1 5\n"
    "1 4\n"
    "1 3\n"
    "1 2\n"
    "1 1\n"
) == "10\n", "maximum inversions for five elements"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One passenger | 0 | Minimum size |
| `[5,2,4]` in one row | 2 | Basic inversion logic |
| Multiple rows | 3 | Row independence |
| Increasing seats | 0 | No stand-up events |
| Decreasing seats | 10 | Maximum inversion count |

## Edge Cases

### Passengers in different rows must not interact

Input:

```
2 10 3
1 5
2 4
1 2
```

Row 1 sequence is `[5, 2]`, producing one inversion.

Row 2 sequence is `[4]`, producing zero inversions.

The algorithm stores rows separately, so the passenger in row 2 never affects row 1. The final answer is:

```
1
```

### Larger seat numbers block smaller seat numbers

Input:

```
1 10 2
1 2
1 8
```

Sequence:

```
[2, 8]
```

There is no inversion because `2 < 8`.

The second passenger sits near the aisle and does not pass seat `2`. The Fenwick query returns zero larger earlier seats, so the answer is:

```
0
```

### Multiple blockers for one passenger

Input:

```
1 10 3
1 9
1 7
1 2
```

When seat `2` arrives, both seats `9` and `7` are occupied and lie between the aisle and seat `2`.

The inversion pairs are:

```
(9, 7)
(9, 2)
(7, 2)
```

Total answer:

```
3
```

The algorithm counts all three inversions, matching the number of stand-up events exactly.
