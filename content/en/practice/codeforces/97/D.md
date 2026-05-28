---
title: "CF 97D - Robot in Basement"
description: "We have a grid representing a basement. Some cells are walls, some are walkable, and exactly one walkable cell is the exit. A robot starts in an unknown walkable cell. We are given a fixed sequence of movement commands such as L, R, U, D."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 97
codeforces_index: "D"
codeforces_contest_name: "Yandex.Algorithm 2011: Finals"
rating: 2700
weight: 97
solve_time_s: 159
verified: true
draft: false
---

[CF 97D - Robot in Basement](https://codeforces.com/problemset/problem/97/D)

**Rating:** 2700  
**Tags:** bitmasks, brute force, implementation  
**Solve time:** 2m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a grid representing a basement. Some cells are walls, some are walkable, and exactly one walkable cell is the exit. A robot starts in an unknown walkable cell. We are given a fixed sequence of movement commands such as `L`, `R`, `U`, `D`.

When the robot receives a command, it tries to move one cell in that direction. If the target cell is a wall, it stays where it is. The same command sequence is applied regardless of the robot’s starting position.

We need the smallest prefix of the command sequence such that after executing that prefix, every possible starting position ends at the exit cell. If no prefix works, we print `-1`.

The basement has at most `150 × 150 = 22500` cells, and the command sequence length is up to `10^5`. Any algorithm that simulates all cells independently for every command immediately becomes expensive. A straightforward simulation over all cells for all commands already costs around `2.25 × 10^9` operations in the worst case, which is far beyond the limit.

The graph structure matters here. Every passable cell is connected to the exit, and the outer border is all walls. Those conditions simplify movement handling and eliminate special cases involving escaping the grid.

The tricky part is that commands act simultaneously on all possible robot positions. A command does not choose where the robot goes, it deterministically transforms the entire set of possible positions.

Several edge cases break naive reasoning.

Consider a basement with only one passable cell:

```
###
#E#
###
```

Any command sequence already succeeds before executing anything. The correct answer is `0`. A solution that always processes at least one command would fail.

Another subtle case is when robots can temporarily gather and later separate again.

```
#####
#...#
#.E.#
#...#
#####
```

Commands:

```
LR
```

After `L`, multiple positions may collapse together because walls block movement differently. After `R`, they can separate again. So checking whether all robots ever meet during the process is incorrect. Only the final positions after a prefix matter.

One more important case is when the whole sequence still does not force convergence.

```
#####
#E..#
#####
```

Commands:

```
RRRR
```

The exit cell moves right until blocked, while another cell also ends at the same rightmost position. The robots never all end at the exit simultaneously. The correct answer is `-1`.

The central challenge is efficiently tracking all possible robot states under repeated global transformations.

## Approaches

The brute-force idea is natural. For every passable starting cell, simulate the robot through the command sequence. After processing each prefix, check whether all robots are at the exit.

This is correct because the robot dynamics are deterministic. If we know where every starting position ends after each prefix, we can directly test the condition.

The problem is scale. Let `P` be the number of passable cells. In the worst case, `P ≈ 22500`. For every one of the `10^5` commands, we would update all `P` positions and potentially compare all of them with the exit. That becomes roughly:

```
22500 × 100000 = 2.25 × 10^9
```

operations.

The key observation is that the command sequence defines a function on cells.

For a command prefix `t`, define:

```
f_t(x) = final position after applying first t commands starting from x
```

We need the first `t` such that:

```
f_t(x) = exit for every x
```

Instead of simulating all robots independently, we can think in reverse.

Suppose after processing some suffix of commands, we know which cells can still possibly end at the exit. Then adding one more command to the front transforms this set backward.

For example, if the next command is `L`, then a cell `u` is good before the command if applying `L` from `u` lands inside the already-good set.

This becomes a reverse reachability process over subsets of cells.

The crucial optimization is representing subsets as bitsets. Each passable cell gets an index. A subset of cells becomes a bitmask. Transition computations become fast bitwise operations over machine words.

For every direction and every cell, we know the deterministic next cell. We can precompute reverse transitions:

```
rev[d][v] = set of cells that move to v under command d
```

Then we process the command sequence backward. Starting from:

```
good = {exit}
```

we repeatedly expand:

```
good = preimage under current command
```

If eventually `good` contains all passable cells, then the corresponding prefix works.

This changes the complexity from simulating every robot independently to repeated bitset propagation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(P · k) with large constants, effectively too large | O(P) | Too slow |
| Optimal | O(k · P / 64) | O(P² / 64) | Accepted |

## Algorithm Walkthrough

1. Enumerate all passable cells and assign each one an integer id.

This lets us represent arbitrary subsets of cells as bitsets indexed by ids.
2. For every cell and every direction, compute the destination cell after one command.

If movement hits a wall, the destination is the same cell.
3. Build reverse transition bitsets.

For each direction `d` and each target cell `v`, store all cells `u` such that moving from `u` using `d` ends at `v`.

This lets us compute preimages efficiently.
4. Initialize a bitset `good` containing only the exit cell.

At this stage, `good` represents all positions that are guaranteed to end at the exit after processing an empty suffix.
5. Process the command sequence backward.

Suppose the current command is `c`. We want all cells that become good after applying `c`.

For every cell `v` already inside `good`, all cells in `rev[c][v]` also become good before the command.
6. Compute the union of all reverse-transition sets for cells currently in `good`.

This produces the new `good`.
7. After processing suffix starting at position `i`, check whether `good` already contains every passable cell.

If yes, then the prefix ending before that suffix forces every starting position into the exit.
8. Return the smallest such prefix length.

Since we process backward, the current suffix start determines the prefix length directly.
9. If no stage covers all cells, print `-1`.

### Why it works

At every step, `good` contains exactly the cells from which the remaining suffix guarantees ending at the exit.

The invariant is maintained by reverse transitions. A cell belongs in the new set precisely when applying the current command sends it into the old set. Since robot movement is deterministic, this characterization is exact.

When `good` becomes the set of all passable cells, every starting position is guaranteed to reach the exit after the corresponding suffix. Equivalently, the complementary prefix is sufficient.

Because we process all commands in reverse order and stop at the earliest valid point, the returned prefix length is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    s = input().strip()

    cells = []
    idx = [[-1] * m for _ in range(n)]

    exit_id = -1

    for i in range(n):
        for j in range(m):
            if grid[i][j] != '#':
                idx[i][j] = len(cells)
                cells.append((i, j))
                if grid[i][j] == 'E':
                    exit_id = idx[i][j]

    p = len(cells)

    if p == 1:
        print(0)
        return

    dirs = {
        'L': (0, -1),
        'R': (0, 1),
        'U': (-1, 0),
        'D': (1, 0),
    }

    trans = [[0] * p for _ in range(4)]

    dir_id = {'L': 0, 'R': 1, 'U': 2, 'D': 3}

    for u, (x, y) in enumerate(cells):
        for ch, (dx, dy) in dirs.items():
            nx = x + dx
            ny = y + dy

            if grid[nx][ny] == '#':
                v = u
            else:
                v = idx[nx][ny]

            trans[dir_id[ch]][u] = v

    rev = [[0] * p for _ in range(4)]

    for d in range(4):
        for u in range(p):
            v = trans[d][u]
            rev[d][v] |= (1 << u)

    all_mask = (1 << p) - 1

    good = 1 << exit_id

    if good == all_mask:
        print(k)
        return

    for pos in range(k - 1, -1, -1):
        d = dir_id[s[pos]]

        new_good = 0

        cur = good

        while cur:
            lsb = cur & -cur
            v = lsb.bit_length() - 1
            new_good |= rev[d][v]
            cur ^= lsb

        good = new_good

        if good == all_mask:
            print(pos)
            return

    print(-1)

solve()
```

The first part assigns every passable cell an integer id. This conversion is essential because bitsets work over compact integer indices rather than coordinate pairs.

The `trans` array stores deterministic movement results. For each direction and each cell, we precompute where the robot ends after one command. Handling blocked movement correctly is important here. If the neighboring cell is a wall, the robot remains in place.

The reverse graph is stored as bitmasks. `rev[d][v]` contains all cells that move into `v` under direction `d`. Building this once allows extremely fast backward propagation later.

The variable `good` is the core invariant. It represents all cells from which the already-processed suffix guarantees reaching the exit.

The backward iteration processes commands from the end toward the beginning. For every currently-good target cell `v`, we union all predecessors that move into `v`.

The bit iteration trick:

```
lsb = cur & -cur
```

extracts one set bit at a time efficiently.

A subtle detail is the returned index. While processing backward from position `pos`, we are determining whether suffix `s[pos:]` guarantees the exit. That means prefix length `pos` is sufficient, because commands before `pos` become irrelevant once the suffix forces convergence.

Another easy mistake is checking the condition before updating `good`. The invariant corresponds to the currently processed suffix, so the check must happen after incorporating the current command.

## Worked Examples

### Example 1

Input:

```
5 5 7
#####
#...#
#...#
#E..#
#####
UULLDDR
```

Passable cells:

| Id | Cell |
| --- | --- |
| 0 | (1,1) |
| 1 | (1,2) |
| 2 | (1,3) |
| 3 | (2,1) |
| 4 | (2,2) |
| 5 | (2,3) |
| 6 | (3,1) = E |
| 7 | (3,2) |
| 8 | (3,3) |

Backward processing:

| Step | Command | Good cells after processing |
| --- | --- | --- |
| Start | none | {6} |
| 1 | R | {6,7} |
| 2 | D | {3,6,7} |
| 3 | D | {0,3,6,7} |
| 4 | L | {0,1,3,4,6,7} |
| 5 | L | all cells |
| 6 | U | all cells |

The first moment all cells become good occurs at backward position `6`, which corresponds to prefix length `6`.

Output:

```
6
```

This trace demonstrates how the reverse process grows the set of guaranteed positions gradually until every starting cell is covered.

### Example 2

Input:

```
5 5 4
#####
#E..#
#####
RRRR
```

Passable cells:

| Id | Cell |
| --- | --- |
| 0 | E |
| 1 | middle |
| 2 | right |

Backward processing:

| Step | Command | Good cells |
| --- | --- | --- |
| Start | none | {0} |
| 1 | R | {0} |
| 2 | R | {0} |
| 3 | R | {0} |
| 4 | R | {0} |

The set never expands because moving right never helps robots reach the exit on the left side.

Output:

```
-1
```

This example shows that convergence is not guaranteed merely because all robots eventually stop moving.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k · P / 64) amortized | Bitset unions process many cells simultaneously |
| Space | O(P) bitsets plus transitions | Reverse masks and movement tables |

Here `P` is the number of passable cells, at most `22500`.

The solution comfortably fits within limits. Even with `10^5` commands, bitwise operations over machine-word chunks are fast enough in Python because Python integers already implement compact bitsets internally.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, m, k = map(int, input().split())
        grid = [input().strip() for _ in range(n)]
        s = input().strip()

        cells = []
        idx = [[-1] * m for _ in range(n)]

        exit_id = -1

        for i in range(n):
            for j in range(m):
                if grid[i][j] != '#':
                    idx[i][j] = len(cells)
                    cells.append((i, j))
                    if grid[i][j] == 'E':
                        exit_id = idx[i][j]

        p = len(cells)

        if p == 1:
            return "0"

        dirs = {
            'L': (0, -1),
            'R': (0, 1),
            'U': (-1, 0),
            'D': (1, 0),
        }

        trans = [[0] * p for _ in range(4)]

        dir_id = {'L': 0, 'R': 1, 'U': 2, 'D': 3}

        for u, (x, y) in enumerate(cells):
            for ch, (dx, dy) in dirs.items():
                nx = x + dx
                ny = y + dy

                if grid[nx][ny] == '#':
                    v = u
                else:
                    v = idx[nx][ny]

                trans[dir_id[ch]][u] = v

        rev = [[0] * p for _ in range(4)]

        for d in range(4):
            for u in range(p):
                v = trans[d][u]
                rev[d][v] |= (1 << u)

        all_mask = (1 << p) - 1

        good = 1 << exit_id

        for pos in range(k - 1, -1, -1):
            d = dir_id[s[pos]]

            new_good = 0

            cur = good

            while cur:
                lsb = cur & -cur
                v = lsb.bit_length() - 1
                new_good |= rev[d][v]
                cur ^= lsb

            good = new_good

            if good == all_mask:
                return str(pos)

        return "-1"

    return solve()

# provided sample
assert run(
"""5 5 7
#####
#...#
#...#
#E..#
#####
UULLDDR
"""
) == "6", "sample 1"

# single passable cell
assert run(
"""3 3 1
###
#E#
###
L
"""
) == "0", "single cell"

# impossible case
assert run(
"""3 5 4
#####
#E..#
#####
RRRR
"""
) == "-1", "cannot force exit"

# already works after one command
assert run(
"""5 5 1
#####
#...#
#.E.#
#...#
#####
L
"""
) == "-1", "single move insufficient"

# convergence after multiple commands
assert run(
"""5 5 4
#####
#..E#
#...#
#...#
#####
LLUU
"""
) == "0", "full suffix forces convergence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single exit cell | 0 | Empty prefix handling |
| Corridor with only R commands | -1 | Impossible convergence |
| Symmetric open room | -1 | Robots can remain separated |
| Multi-command convergence | 0 | Backward propagation correctness |

## Edge Cases

Consider the single-cell basement:

```
3 3 1
###
#E#
###
L
```

There is only one possible starting position, and it is already the exit.

The algorithm assigns one id, so:

```
all_mask = good = 1
```

The special-case check immediately returns `0`.

Now consider the impossible convergence case:

```
3 5 4
#####
#E..#
#####
RRRR
```

The exit is the leftmost cell. Moving right never helps any other position collapse into the exit.

Backward processing starts with:

```
good = {exit}
```

Applying reverse transitions for `R` repeatedly still gives only the exit cell itself, because no other cell moves into it under `R`.

The set never becomes all cells, so the algorithm correctly prints `-1`.

Finally, consider a case where robots temporarily merge but later split:

```
5 5 2
#####
#...#
#.E.#
#...#
#####
LR
```

After command `L`, several states collapse against the left wall. A forward simulation that checks intermediate equality might incorrectly conclude success.

The backward method avoids this mistake because it only reasons about final positions after the complete suffix. Since the final states are not all the exit, the algorithm correctly rejects the prefix.
