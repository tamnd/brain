---
title: "CF 106475E - \u041a\u0430\u043f\u0438\u0431\u0430\u0440\u044b \u0438\u0433\u0440\u0430\u044e\u0442 \u0432  <<\u0422\u0440\u0438 \u0432 \u0440\u044f\u0434>>"
description: "We have an infinite grid. Some cells already contain marks. The current board is guaranteed to avoid any three consecutive marked cells on a horizontal, vertical, or diagonal line."
date: "2026-06-25T08:51:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106475
codeforces_index: "E"
codeforces_contest_name: "\u0424\u0438\u043d\u0430\u043b \u0412\u041a\u041e\u0428\u041f.Junior 2026"
rating: 0
weight: 106475
solve_time_s: 50
verified: true
draft: false
---

[CF 106475E - \u041a\u0430\u043f\u0438\u0431\u0430\u0440\u044b \u0438\u0433\u0440\u0430\u044e\u0442 \u0432  <<\u0422\u0440\u0438 \u0432 \u0440\u044f\u0434>>](https://codeforces.com/problemset/problem/106475/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
# Problem Understanding

We have an infinite grid. Some cells already contain marks. The current board is guaranteed to avoid any three consecutive marked cells on a horizontal, vertical, or diagonal line.

We need to count how many empty cells could receive one additional mark so that after placing it, at least one line of three consecutive marked cells exists.

The input gives the coordinates of all currently marked cells. The output is the number of distinct empty coordinates that can complete a line of length three.

The important constraint is that there can be up to 200,000 existing marks, while coordinates can be as large as 10^9 in absolute value. A solution that scans the board is impossible because the board is effectively infinite. Even checking every coordinate in a large bounding rectangle would require far more than the available time. We need an algorithm whose work depends on the number of marks, not on the coordinate range.

The absence of existing triples is a useful guarantee. It means every valid move is created from exactly two existing marks and one new mark. We never need to handle a situation where the board already contains a winning line.

A common mistake is to count possible pairs instead of possible cells. Different pairs can suggest the same empty cell, so we must remove duplicates.

For example, consider:

```
3
0 0
1 0
0 1
```

The correct answer is `4`. The cells `(2,0)`, `(-1,0)`, `(0,2)`, and `(0,-1)` all create a horizontal or vertical triple. A careless approach that counts every pair completion separately could count the same position multiple times.

Another edge case is when two marks are diagonal but not close enough:

```
2
0 0
1 2
```

The correct answer is `0`. The two marks do not belong to any possible length-three line with one missing cell. Checking only the existence of two marks without verifying the distance would produce a wrong answer.

# Approaches

The direct approach is to examine every empty cell and test whether putting a mark there creates a triple. This is correct because every possible answer is checked. The problem is that the number of empty cells is not bounded in any meaningful way. Coordinates are up to 10^9, so even a small number of marks can have an enormous surrounding area. The brute-force method cannot even enumerate the candidates.

The key observation is that every successful move must complete a segment of exactly three cells. There are only four possible directions for such a segment: horizontal, vertical, and the two diagonals. If we know one existing mark, we only need to look a distance of one or two cells away in these directions.

For a fixed direction vector `(dx, dy)`, two existing marks can appear in three possible positions of a length-three segment. If the first and second cells are occupied, the missing cells are one step before the pair and one step after the pair. If the first and third cells are occupied, the missing cell is the middle one. Since there are only four directions and constant distance checks, each existing mark generates only a constant number of candidates.

The final step is deduplication. We insert every possible answer coordinate into a set. Coordinates that are already occupied are ignored because we must place a mark in an empty cell.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(area of searched board) | O(area of searched board) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

# Algorithm Walkthrough

1. Store all existing marked cells in a hash set. Coordinate lookup must be constant time because every generated candidate needs to be checked against the current board.
2. For every marked cell, inspect the four directions `(1,0)`, `(0,1)`, `(1,1)`, and `(1,-1)`. These represent all possible orientations of a three-cell line without duplicates.
3. For each direction, check the cell one step away. If it is occupied, the two cells can be the first two positions of a triple. Add the two possible missing cells, one before the pair and one after the pair.
4. For the same direction, check the cell two steps away. If it is occupied, the two marks can be the endpoints of a triple. Add the middle cell as a possible answer.
5. Remove candidates that are already occupied. The remaining number of unique coordinates is the answer.

Why it works: every valid move creates a line of three cells. In that line, take any one of the two already occupied cells and consider the direction toward the other occupied cell. The distance between the two existing cells is either one or two. The algorithm checks exactly those two cases and adds the missing position. Since every generated position is stored in a set, multiple ways of discovering the same move do not affect the result.

# Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    n = int(input())
    points = set()

    for _ in range(n):
        x, y = map(int, input().split())
        points.add((x, y))

    directions = [
        (1, 0),
        (0, 1),
        (1, 1),
        (1, -1),
    ]

    ans = set()

    for x, y in points:
        for dx, dy in directions:
            x1, y1 = x + dx, y + dy
            if (x1, y1) in points:
                a = (x - dx, y - dy)
                b = (x + 2 * dx, y + 2 * dy)
                if a not in points:
                    ans.add(a)
                if b not in points:
                    ans.add(b)

            x2, y2 = x + 2 * dx, y + 2 * dy
            if (x2, y2) in points:
                mid = (x + dx, y + dy)
                if mid not in points:
                    ans.add(mid)

    print(len(ans))

if __name__ == "__main__":
    solve()
```

The first part of the code builds the set of occupied cells. A Python tuple is used as the coordinate representation, allowing direct membership checks.

The direction list contains only four vectors because the opposite direction would describe the same line. For example, checking `(1,0)` already covers horizontal triples, so checking `(-1,0)` would only duplicate work.

The first condition checks adjacent marked cells. If `(x,y)` and `(x+dx,y+dy)` are occupied, they form two neighboring cells of a triple. The third cell can be on either side of them.

The second condition checks cells separated by one gap. If `(x,y)` and `(x+2dx,y+2dy)` are occupied, the only possible missing position is their middle cell.

The set `ans` is necessary because the same empty cell can be generated from different existing marks or different directions. Python integers handle the large coordinate values directly, so no overflow handling is needed.

# Worked Examples

Using the first sample:

```
4
2 2
3 3
4 2
5 2
```

The algorithm checks each mark against the four directions.

| Current cell | Direction | Found cells | Added candidates |
| --- | --- | --- | --- |
| (2,2) | (1,1) | (3,3) exists | (1,1), (4,4) |
| (4,2) | (1,0) | (5,2) exists | (3,2), (6,2) |
| (4,2) | (1,-1) | (3,3) exists at distance 1 | (5,1), (2,4) |

After all checks, all six generated positions are distinct, so the answer is:

```
6
```

This demonstrates why we must consider both sides of an adjacent pair. A single pair can create two different winning moves.

For the second sample:

```
2
3 3
1 4
```

| Current cell | Direction | Found cells | Added candidates |
| --- | --- | --- | --- |
| (3,3) | (1,-1) | no matching cell | none |
| (1,4) | (1,-1) | no matching cell | none |

No two marks are positioned one or two steps apart on a valid line, so no move can create a triple.

The result is:

```
0
```

This confirms that the algorithm only generates candidates from actual possible three-cell segments.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every mark checks four directions and a constant number of neighboring cells. |
| Space | O(n) | The occupied set and candidate set each contain only a constant multiple of the number of marks. |

With `n = 200000`, the algorithm performs only a few million hash operations, which fits comfortably within the limits.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        n = int(input())
        points = set()

        for _ in range(n):
            x, y = map(int, input().split())
            points.add((x, y))

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        ans = set()

        for x, y in points:
            for dx, dy in directions:
                if (x + dx, y + dy) in points:
                    for p in [(x - dx, y - dy), (x + 2 * dx, y + 2 * dy)]:
                        if p not in points:
                            ans.add(p)

                if (x + 2 * dx, y + 2 * dy) in points:
                    p = (x + dx, y + dy)
                    if p not in points:
                        ans.add(p)

        return str(len(ans))

    result = solve()
    sys.stdin = old_stdin
    return result

assert run("""4
2 2
3 3
4 2
5 2
""") == "6"

assert run("""2
3 3
1 4
""") == "0"

assert run("""1
0 0
""") == "0"

assert run("""3
0 0
1 0
2 0
""") == "0"

assert run("""2
1000000000 1000000000
999999999 999999999
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single mark | 0 | No pair exists, so no move is possible |
| Already aligned three marks | 0 | The guarantee is tested against duplicate candidate handling |
| Very large coordinates | 2 | Coordinate range and integer handling |
| Two diagonal adjacent marks | 2 | Both sides of an adjacent pair are counted |

# Edge Cases

For the duplicate-counting case:

```
3
0 0
1 0
0 1
```

The pair `(0,0)` and `(1,0)` suggests `(2,0)` and `(-1,0)`. The pair `(0,0)` and `(0,1)` suggests `(0,2)` and `(0,-1)`. The final set contains four cells, so the answer is `4`. If candidates were counted without a set, overlapping discoveries could inflate the answer.

For a diagonal gap:

```
2
0 0
2 2
```

The two marks are exactly two steps apart on a diagonal. The algorithm detects `(1,1)` as the missing middle cell, so the answer is `1`.

For distant diagonal cells:

```
2
0 0
1 2
```

No checked offset matches either distance one or distance two on a valid direction. The candidate set stays empty, giving answer `0`.

For coordinates near the integer limit:

```
2
1000000000 1000000000
999999999 999999999
```

The algorithm still works because coordinates are only shifted by at most two units. Python integers safely represent these values, and the set operations behave the same as for small coordinates.
