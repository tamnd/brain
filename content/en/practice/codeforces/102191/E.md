---
title: "CF 102191E - Snake Moves"
description: "The move string describes a walk on the infinite integer grid, starting from some initial cell. Each character changes the current cell by one unit in one of the four cardinal directions."
date: "2026-08-18T02:40:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102191
codeforces_index: "E"
codeforces_contest_name: "PSUT Coding Marathon 2019"
rating: 0
weight: 102191
solve_time_s: 614
verified: false
draft: false
---

[CF 102191E - Snake Moves](https://codeforces.com/problemset/problem/102191/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 14s  
**Verified:** no  

## Solution
## Problem Understanding

The move string describes a walk on the infinite integer grid, starting from some initial cell. Each character changes the current cell by one unit in one of the four cardinal directions. We need the longest contiguous part of the move string whose corresponding walk never occupies the same cell twice.

The starting cell of the chosen substring counts as a visited cell. This detail matters because a substring such as `RL` first moves right and then immediately returns to its starting cell, so it is invalid.

A useful way to represent the walk is with prefix positions. Let P i ​ be the cell reached after the first i moves, with P 0 ​ being the starting cell. A substring from move l through move r visits exactly the positions

P l−1 ​ ,P l ​ ,…,P r ​ .

Thus the substring is valid exactly when these prefix positions are all distinct. The original movement problem has now become a familiar array problem: find the longest contiguous range of prefix positions containing no duplicate value.

The length can reach 10 6. An O(n 2 ) algorithm would already require roughly 5⋅10 11 iterations in the worst case, far beyond what a 1.5 second time limit permits. We need a linear-time or close-to-linear-time method. The memory limit of 256 MB also means that storing a large collection of Python objects carelessly can become relevant, so the implementation should use compact coordinate representations rather than storing coordinate tuples.

There are several edge cases that easily cause incorrect answers. For `R`, the only visited cells are the starting cell and the cell immediately to its right, so the answer is `1`.

```
1R
```

The correct output is `1`. A careless implementation that counts visited cells instead of moves might output `2`, while the required answer is the number of moves.

For `RL`, the snake returns to its starting cell.

```
2RL
```

The correct output is `1`. A method that only checks whether consecutive moves are different would incorrectly accept the whole string. The repeated cell can be separated by several moves, so we must track positions rather than just directions.

For `RULD`, the final move returns to the initial cell.

```
4RULD
```

The correct output is `3`. The complete walk contains the starting position twice, but the first three moves form a valid walk. The algorithm must shrink the current window rather than discard everything seen before.

Another subtle case is a position whose previous occurrence is already outside the current window. For example, consider `RRLR`. The prefix positions are 0,1,2,1,2. When the second `1` appears, the valid window must move past the old `1`. Later, when `2` repeats, only the current window matters. A common sliding-window mistake is to assign the left boundary directly to `last[position] + 1`, which can move the boundary backwards. The boundary must only move forward.

## Approaches

The direct approach is to choose every possible starting position and extend the substring one move at a time. While extending, we maintain the current coordinates and a set of cells already visited. If the next cell is already in the set, the substring can no longer be extended. Otherwise we insert it and update the answer. This is correct because for every starting position we explicitly find the longest valid prefix of the suffix beginning there.

The problem is the amount of repeated work. On an input such as `RRRR...R`, every starting position produces a valid substring all the way to the end. The algorithm examines

n+(n−1)+⋯+1= 2 n(n+1) ​

extensions, which is 500000500000 for n=10 6. That is already far too large, even before accounting for set operations.

The brute-force works because it independently maintains the set of cells for each starting point, but it throws away information whenever the starting point changes. The key observation is that all substrings correspond to contiguous ranges of the same prefix-position array. If we maintain one window of prefix positions with no duplicates, then when a duplicate appears, we only need to move the left boundary far enough to remove the previous occurrence of that position.

Suppose the current prefix position P i ​ was last seen at index j. If the current valid window begins at L, then a duplicate occurs exactly when j≥L. The new window must begin after j, so we set

L=max(L,j+1).

If j<L, the old occurrence is already outside the current window and nothing needs to change. Each prefix position is processed once, and the left boundary only moves forward, giving an O(n) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n 2 ) | O(n) | Too slow |
| Optimal | O(n) expected | O(n) | Accepted |

## Algorithm Walkthrough

1. Represent the starting cell as prefix position P 0 ​ =(0,0). For every move, update the current coordinate to obtain the next prefix position.
2. Maintain a sliding window of prefix indices [L,i] whose positions are all distinct. The corresponding move substring has length i−L, because it consists of moves L+1,…,i.
3. Store the most recent prefix index at which every coordinate was visited. When P i ​ is generated, look up its previous index j.
4. If j≥L, the current position occurs inside the window, so the window is no longer valid. Move its left boundary to j+1. We use `max` because the left boundary is never allowed to move backwards.
5. Record `i` as the latest occurrence of the current position. This must happen after determining the new boundary, because future occurrences need to know the current index.
6. The current window contains `i-L+1` distinct prefix positions, which corresponds to `i-L` moves. Update the answer with `i-L`.

Why it works: at every iteration, the invariant is that all prefix positions from P L ​ through P i ​ are distinct. If the new position has no previous occurrence inside this window, the invariant remains true. If it does have an occurrence at j, every valid window ending at i must start after j, so moving L to j+1 is necessary and sufficient. Since every valid substring ending at i has to be represented by a duplicate-free window ending at i, the largest such window gives the best answer for that endpoint. Taking the maximum over all endpoints consequently gives the globally longest valid substring.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve(s):    n = len(s)
    # Encode (x, y) into one integer so that the dictionary    # stores only integer keys instead of coordinate tuples.    base = 2 * n + 3    offset = n + 1
    x = 0    y = 0
    # last[position] = latest prefix index containing this position.    last = {offset * base + offset: 0}
    left = 0    ans = 0
    for i, ch in enumerate(s, 1):        if ch == 'R':            x += 1        elif ch == 'L':            x -= 1        elif ch == 'U':            y += 1        else:            y -= 1
        key = (x + offset) * base + (y + offset)
        previous = last.get(key)        if previous is not None and previous >= left:            left = previous + 1
```

The `solve` function processes the moves exactly as in the walkthrough. `x` and `y` store the current prefix position, while `i` is its prefix index.

Coordinates lie between −n and n, because there are only n moves. The expression

```
Pythonkey = (x + offset) * base + (y + offset)
```

maps every possible coordinate pair to a unique integer. Using one integer as the dictionary key is considerably more memory-efficient than using a two-element tuple for every visited cell, which matters when n is as large as 10 6.

The initial position must be inserted with index `0`. Without it, a path that returns to its starting cell would not be detected. This is exactly why `RL` must have answer `1` rather than `2`.

The condition `previous >= left` is another important boundary check. A previous occurrence before the current window does not make the current window invalid. Writing `left = previous + 1` unconditionally would incorrectly move the window backwards.

The answer is `i - left`, not `i - left + 1`. The window contains prefix positions L through i, but there is one fewer move than positions. Python integers do not overflow, so no special handling is required for the coordinate encoding or answer.

## Worked Examples

For Sample 1, the input is `RULD`. The prefix positions are encoded conceptually as coordinates.

| Move index `i` | Move | Position `(x, y)` | Previous index | `left` after update | Current length `i-left` | `ans` |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | start | `(0, 0)` | 0 | 0 | 0 | 0 |
| 1 | `R` | `(1, 0)` | none | 0 | 1 | 1 |
| 2 | `U` | `(1, 1)` | none | 0 | 2 | 2 |
| 3 | `L` | `(0, 1)` | none | 0 | 3 | 3 |
| 4 | `D` | `(0, 0)` | 0 | 1 | 3 | 3 |

At the fourth move, `(0, 0)` was previously visited at prefix index `0`. The window therefore moves from prefix indices `[0,4]` to `[1,4]`. Those four prefix positions correspond to only three moves, giving the correct answer `3`.

For Sample 2, `RRDDLLUUURDDR`, the same mechanism keeps the longest duplicate-free prefix-position window.

| Move index `i` | Move | Position `(x, y)` | Previous index | `left` | Current length | `ans` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `R` | `(1,0)` | none | 0 | 1 | 1 |
| 2 | `R` | `(2,0)` | none | 0 | 2 | 2 |
| 3 | `D` | `(2,-1)` | none | 0 | 3 | 3 |
| 4 | `D` | `(2,-2)` | none | 0 | 4 | 4 |
| 5 | `L` | `(1,-2)` | none | 0 | 5 | 5 |
| 6 | `L` | `(0,-2)` | none | 0 | 6 | 6 |
| 7 | `U` | `(0,-1)` | none | 0 | 7 | 7 |
| 8 | `U` | `(0,0)` | 0 | 1 | 7 | 7 |
| 9 | `U` | `(0,1)` | none | 1 | 8 | 8 |
| 10 | `R` | `(1,1)` | none | 1 | 9 | 9 |
| 11 | `D` | `(1,0)` | 1 | 2 | 9 | 9 |
| 12 | `D` | `(1,-1)` | none | 2 | 10 | 10 |
| 13 | `R` | `(2,-1)` | 3 | 4 | 9 | 10 |

The maximum window contains ten moves after processing position `12`. At position `13`, the repeated cell forces `left` forward, so the answer remains `10`. The final duplicate does not invalidate the previously discovered best window.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) expected | Each move performs a constant number of dictionary operations and coordinate updates. |
| Space | O(n) | At most n+1 distinct prefix positions are stored. |

With n≤10 6, the algorithm performs only one pass over the move string. The dictionary can contain at most one entry per distinct grid cell visited by the walk, so its size is linear in n. The integer encoding avoids the much larger overhead of storing coordinate tuples, keeping the Python implementation suitable for the 256 MB memory limit.

## Test Cases

```python
Pythonimport sysimport io

def solve(s):    n = len(s)    base = 2 * n + 3    offset = n + 1
    x = 0    y = 0
    last = {offset * base + offset: 0}
    left = 0    ans = 0
    for i, ch in enumerate(s, 1):        if ch == 'R':            x += 1        elif ch == 'L':            x -= 1        elif ch == 'U':            y += 1        else:            y -= 1
        key = (x + offset) * base + (y + offset)
        previous = last.get(key)        if previous is not None and previous >= left:            left = previous + 1
        last[key] = i        ans = max(ans, i - left)
    return ans

def run(inp: str) -> str:    data = inp.strip().split()    n = int(data[0])    s = data[1]    assert n == len(s)    return str(solve(s))

# Provided samplesassert run("4\nRULD\n") == "3", "sample 1"assert run("13\nRRDDLLUUURDDR\n") == "10", "sample 2"assert run("3\nRRU\n") == "3", "sample 3"
# Minimum-size inputassert run("1\nR\n") == "1", "minimum size"
# Immediate return to the starting cellassert run("2\nRL\n") == "1", "return to start"
# Repeated cells that require the sliding window to moveassert run("4\nRRLR\n") == "2", "repeated position"
# Maximum-size input, all moves in one directionlarge = "R" * 1_000_000assert run(f"{len(large)}\n{large}\n") == "1000000", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / R` | `1` | Minimum input size and conversion from prefix positions to move count |
| `2 / RL` | `1` | Returning to the initial cell |
| `4 / RRLR` | `2` | Correct movement of the sliding-window boundary |
| `1000000 / R...R` | `1000000` | Maximum input size and linear-time behavior |

## Edge Cases

For the minimum input `1 / R`, the algorithm starts with prefix position `(0,0)`. After `R`, it reaches `(1,0)`, which has not appeared before. The window is `[0,1]`, containing two distinct positions and therefore one move. The output is `1`.

For `RL`, the prefix positions are `(0,0)`, `(1,0)`, and `(0,0)`. When the final position is generated, its previous index is `0`, which lies inside the current window beginning at `0`. The algorithm changes `left` to `1`, leaving prefix positions `1` and `2`. That represents the single valid move `L`, so the output is `1`.

For `RULD`, the fourth move reaches `(0,0)`, whose previous occurrence is at index `0`. The left boundary changes from `0` to `1`, leaving the valid three-move substring `ULD`. The answer was already `3`, so the repeated starting cell does not cause the algorithm to lose the best earlier substring.

For `RRLR`, the prefix positions are `(0,0)`, `(1,0)`, `(2,0)`, `(1,0)`, `(2,0)`. At index `3`, `(1,0)` was last seen at index `1`, so `left` becomes `2`. At index `4`, `(2,0)` was last seen at index `2`, which is exactly the current left boundary, so `left` becomes `3`. The largest window had length `2`, corresponding to the first two moves `RR`, and the output is `2`. This case specifically checks that `left` is advanced only as far as necessary.

For the maximum-size input consisting of one million `R` characters, every prefix position is different because the x-coordinate increases by one after every move. No duplicate is ever found, so `left` remains `0` and the answer grows to `1000000`. The algorithm performs one iteration per character, demonstrating why the O(n) approach handles the upper bound while the quadratic approach cannot.
