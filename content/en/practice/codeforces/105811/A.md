---
title: "CF 105811A - Fishy Tank"
description: "The task is to draw a rectangular fish tank using ASCII characters. The tank always has a fixed size of 15 rows and 25 columns. The border uses o, -, and The input contains one integer representing the number of fish that must appear."
date: "2026-06-25T15:18:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105811
codeforces_index: "A"
codeforces_contest_name: "UT Open 2025"
rating: 0
weight: 105811
solve_time_s: 37
verified: true
draft: false
---

[CF 105811A - Fishy Tank](https://codeforces.com/problemset/problem/105811/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to draw a rectangular fish tank using ASCII characters. The tank always has a fixed size of 15 rows and 25 columns. The border uses `o`, `-`, and `|`, and the inside is empty space. We need to place exactly `n` fish inside the tank, where each fish is three characters long and looks either like `><>` or `<><`. Fish cannot touch the border and two fish cannot overlap. The required output is simply the finished drawing. The problem asks for any valid arrangement, not a unique one.

The input contains one integer representing the number of fish that must appear. Since the limit is only up to 10 fish, the main challenge is not performance but finding a simple construction that always leaves enough valid positions. Any approach doing search over possible drawings would be unnecessary. A constant time construction is enough because the output size itself is fixed at 15 by 25 characters, meaning we only ever create 375 cells.

A common mistake is to place fish without checking the available interior width. A fish occupies three consecutive columns, so putting one at the last two columns of the inside area would make it cross the border.

For example:

```
1
```

The output cannot place the fish starting at column 23 of the row because the tank width ends at column 24. The correct idea is to use only safe interior positions.

Another edge case is when all fish are placed in the same row. A careless implementation might make them touch each other. For example:

```
3
```

A row like:

```
|><><><><>|
```

is invalid because the fish overlap. The fish must be separated by at least one empty character.

A final edge case is the maximum number of fish. Since there are only 10 fish, a construction must reserve enough space for all of them. A fixed pattern of rows and columns avoids running out of space.

## Approaches

The brute force approach would be to try every possible placement of fish inside the tank, checking whether each candidate drawing contains exactly the required number of non-overlapping fish. This is correct because eventually every possible drawing is considered, but the search space is enormous compared with the tiny input. There are hundreds of possible positions for each fish, and trying combinations of positions grows exponentially. Even before checking all arrangements, the number of candidates becomes far larger than what is needed for a fixed-size output problem.

The observation that changes the problem is that the judge only verifies whether the final picture is valid. It does not care about the positions or directions of the fish. Since there are only 10 possible fish, we can prepare a deterministic layout with enough slots and fill the first `n` slots. The problem becomes a simple construction problem.

The tank can be initialized completely, then fish can be inserted into safe locations. Choosing positions separated by empty cells guarantees that no two fish overlap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of possible placements | O(15 * 25) | Too slow and unnecessary |
| Optimal | O(15 * 25) | O(15 * 25) | Accepted |

## Algorithm Walkthrough

1. Create a 15 by 25 grid filled with spaces. This gives us the empty interior of the tank.
2. Draw the border by placing `o` in the four corners, `-` across the top and bottom, and `|` along the left and right sides. This recreates the required tank shape.
3. Prepare a list of safe positions where fish can be placed. Each position must be inside the border and have three consecutive columns available.
4. For each fish that is required, place a `><>` pattern at the next available position. The exact direction does not matter because the only requirement is that each fish has one of the two valid shapes.
5. Print the completed grid row by row.

Why it works:

The only thing that can make the drawing invalid is an incorrectly shaped fish, overlap, or touching the border. Every chosen position is inside the tank and leaves enough room for three characters. Because positions are chosen without reuse and with spacing, every inserted fish is independent. After placing exactly `n` fish, the grid contains exactly the required number of valid fish.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    h, w = 15, 25
    grid = [[' ' for _ in range(w)] for _ in range(h)]

    for j in range(w):
        grid[0][j] = '-'
        grid[h - 1][j] = '-'

    for i in range(h):
        grid[i][0] = '|'
        grid[i][w - 1] = '|'

    grid[0][0] = 'o'
    grid[0][w - 1] = 'o'
    grid[h - 1][0] = 'o'
    grid[h - 1][w - 1] = 'o'

    positions = []
    for r in range(1, h - 1):
        for c in range(2, w - 3, 4):
            positions.append((r, c))

    for i in range(n):
        r, c = positions[i]
        grid[r][c] = '>'
        grid[r][c + 1] = '<'
        grid[r][c + 2] = '>'

    print('\n'.join(''.join(row) for row in grid))

if __name__ == "__main__":
    solve()
```

The grid is represented as a mutable list of character lists because individual cells need to be changed. Building the border first guarantees the container is valid before adding anything inside it.

The position generation starts from an interior row and leaves enough distance between starting columns. The step of four columns is deliberate. A fish uses three columns, and the extra column between fish prevents accidental touching.

The insertion loop only uses the first `n` generated positions. Since the problem guarantees `n` is at most 10, the list always contains enough safe locations.

The output conversion joins each row into a string. There is no need for special handling of spaces because Python preserves them when joining characters.

## Worked Examples

For input:

```
2
```

The algorithm selects the first two positions.

| Step | Fish count placed | Current action |
| --- | --- | --- |
| 1 | 0 | Empty tank with border |
| 2 | 1 | Place first `><>` |
| 3 | 2 | Place second `><>` |

The result contains two separated fish. This trace demonstrates that the placement rule keeps fish independent.

For input:

```
5
```

The algorithm continues filling the next available slots.

| Step | Fish count placed | Current action |
| --- | --- | --- |
| 1 | 0 | Create tank |
| 2 | 1 | Place fish at first slot |
| 3 | 2 | Place fish at second slot |
| 4 | 3 | Place fish at third slot |
| 5 | 4 | Place fish at fourth slot |
| 6 | 5 | Place fish at fifth slot |

The trace shows that even with the largest required count, the same construction continues without any collision.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(15 * 25) | The grid has a fixed number of cells and each cell is processed a constant number of times |
| Space | O(15 * 25) | The whole drawing is stored before printing |

The constraints are tiny, and the solution does a fixed amount of work regardless of the fish count. The algorithm easily fits within any normal contest time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())

    h, w = 15, 25
    grid = [[' ' for _ in range(w)] for _ in range(h)]

    for j in range(w):
        grid[0][j] = '-'
        grid[h - 1][j] = '-'

    for i in range(h):
        grid[i][0] = '|'
        grid[i][w - 1] = '|'

    grid[0][0] = 'o'
    grid[0][w - 1] = 'o'
    grid[h - 1][0] = 'o'
    grid[h - 1][w - 1] = 'o'

    positions = []
    for r in range(1, h - 1):
        for c in range(2, w - 3, 4):
            positions.append((r, c))

    for i in range(n):
        r, c = positions[i]
        grid[r][c] = '>'
        grid[r][c + 1] = '<'
        grid[r][c + 2] = '>'

    ans = '\n'.join(''.join(row) for row in grid)
    sys.stdin = old_stdin
    return ans

def count_fish(out):
    return out.count('><>') + out.count('<><')

assert count_fish(run("1\n")) == 1, "minimum case"
assert count_fish(run("10\n")) == 10, "maximum case"
assert count_fish(run("5\n")) == 5, "sample style case"
assert count_fish(run("3\n")) == 3, "spacing case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | One fish | Minimum size handling |
| `10` | Ten fish | Maximum allowed number of fish |
| `5` | Five fish | Multiple placements |
| `3` | Three fish | Spacing between fish |

## Edge Cases

For the minimum case:

```
1
```

The algorithm creates the border and inserts only the first fish position. Since that position is not on the border and has exactly three available cells, the output contains one valid fish.

For the maximum case:

```
10
```

The generated position list contains enough locations because it uses multiple rows. The algorithm never tries to reuse a slot, so all ten fish remain separate.

For the spacing case:

```
3
```

The fish are placed at columns separated by four positions. A fish occupies three columns, leaving a blank column after it. This prevents a mistaken drawing where two fish merge into a longer invalid pattern.
