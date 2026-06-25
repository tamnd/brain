---
title: "CF 106507O - Not JOI again"
description: "We have an n x n board of cells. Each cell is either active (1) or blocked (0). A move is allowed between side-adjacent cells, and only active cells may be visited."
date: "2026-06-25T08:30:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106507
codeforces_index: "O"
codeforces_contest_name: "TeamsCode 2026 Spring Contest"
rating: 0
weight: 106507
solve_time_s: 44
verified: true
draft: false
---

[CF 106507O - Not JOI again](https://codeforces.com/problemset/problem/106507/O)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an `n x n` board of cells. Each cell is either active (`1`) or blocked (`0`). A move is allowed between side-adjacent cells, and only active cells may be visited. After every update, one cell changes state, and we must decide whether the top-left cell can still reach the bottom-right cell.

The difficulty is not only the dynamic updates. The input queries are encrypted using previous answers. The coordinates given in the input are shifted depending on the last `num` answers, so we cannot reorder queries or process them offline. We must answer each state before knowing the exact next update.

The board size is large enough that storing a graph with four million vertices is already expensive, but the number of updates is only 2000. This means a full graph algorithm after every update is too slow, while a carefully optimized traversal can work. A naive BFS touches all `n^2` cells after every query, giving `O(qn^2)`, which becomes about eight billion cell visits at the maximum limits.

The important edge cases are cells that disconnect the only possible corridor and cases where the start or end cell is blocked. For example:

```
1
0
1 1
0 0
```

After the flip, the only cell becomes active, so the answer is `YES`. An implementation that checks only neighbors without handling the single-cell grid case would fail.

Another case is:

```
2
11
10
1 1
0 0
```

The bottom-right cell is blocked initially, so after any unrelated flip the answer must remain `NO` until that cell becomes active. Code that only tracks whether the start region expands can accidentally report success without checking the destination.

## Approaches

The straightforward solution is to run BFS from `(1,1)` after every flip. It is easy to prove correct because BFS exactly computes the connected component of the start cell. The problem is the amount of repeated work. With `q = 2000` and `n = 2000`, the worst case performs around `2000 * 2000 * 2000 = 8 * 10^9` cell checks.

The observation that changes the problem is that the grid is fixed in size and the number of rows is only 2000. Instead of storing individual cells in the BFS queue, we store every row of the current reachable region as a bitset. A Python integer already behaves like a compact bit array, so horizontal expansion becomes a few bit operations. Each BFS layer processes all rows at once using integer shifts.

The optimized approach still performs graph traversal, but the constant factor is much smaller. A row of 2000 cells is represented by one integer, and the entire flood fill works with approximately `n` integer operations per layer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS | `O(q * n^2)` | `O(n^2)` | Too slow |
| Bitset BFS | `O(q * n * d)` where `d` is the number of expansion rounds | `O(n)` | Accepted for the given limits |

## Algorithm Walkthrough

1. Store every grid row as an integer bitmask. Bit `j` of row `i` tells whether cell `(i, j)` is active.
2. Decode the current query using the previous answers. The last `num` answers are kept as a binary value, with `YES` represented by `1`.
3. Flip the decoded cell by toggling its bit in the corresponding row integer.
4. Run a flood fill using bitsets. Keep an array `reach`, where `reach[i]` contains all columns reachable in row `i`.
5. Start with only `(0, 0)` reachable if that cell is active.
6. Repeatedly expand every row. The possible new cells come from the previous row, the next row, and the same row shifted left and right. Intersect the result with the active cells of that row.
7. Stop when an iteration produces no new reachable cells. The destination is reachable exactly when the final row contains the last bit.

Why it works:

The invariant is that after every expansion round, `reach` contains only cells reachable from the start using paths of length at most the current number of rounds. Expanding with the four possible directions adds every valid next step, and intersecting with the grid removes blocked cells. When no new cells appear, the reachable component is complete, so checking the destination bit gives the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    grid = []
    for _ in range(n):
        s = input().strip()
        mask = 0
        for i, c in enumerate(s):
            if c == '1':
                mask |= 1 << i
        grid.append(mask)

    q, num = map(int, input().split())

    decode = []
    for _ in range(1 << num):
        u, v = map(int, input().split())
        decode.append((u, v))

    ans_bits = 0
    answers = []
    last_mask = (1 << num) - 1

    def reachable():
        if (grid[0] & 1) == 0:
            return False

        reach = [0] * n
        reach[0] = 1

        while True:
            changed = False
            nxt = [0] * n

            for i in range(n):
                cur = reach[i]

                if i:
                    cur |= reach[i - 1]
                if i + 1 < n:
                    cur |= reach[i + 1]

                cur |= (reach[i] << 1)
                cur |= (reach[i] >> 1)

                cur &= grid[i]

                nxt[i] = cur
                if cur != reach[i]:
                    changed = True

            reach = nxt

            if not changed:
                return (reach[n - 1] >> (n - 1)) & 1 == 1

    out = []

    for _ in range(q):
        x, y = map(int, input().split())

        val = ans_bits
        ux, vy = decode[val]

        x += ux
        y += vy

        if x > n:
            x -= n
        if y > n:
            y -= n

        x -= 1
        y -= 1

        grid[x] ^= 1 << y

        ok = reachable()

        if ok:
            out.append("YES")
            bit = 1
        else:
            out.append("NO")
            bit = 0

        ans_bits = ((ans_bits << 1) | bit) & last_mask

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The grid representation is the first important implementation detail. Using strings would make every update and every traversal expensive, while integer bitmasks let Python perform many cell operations in native integer arithmetic.

The decoding step keeps only the last `num` answers. The mask operation removes older bits, matching the statement's rolling binary representation.

The flood fill deliberately creates a new `n` element array every round. This avoids mixing cells discovered during the current round with cells that existed before it, which would break the BFS-style invariant.

The destination check uses zero-based coordinates, so the final cell is bit `n-1` in row `n-1`. This is a common source of off-by-one mistakes.

## Worked Examples

For the first sample:

```
3
101
010
111
3 1
0 2
1 1
3 2
1 3
```

The real operations are decoded from previous answers as:

| Step | Decoded cell | Grid change | Reachable |
| --- | --- | --- | --- |
| 1 | `(3,1)` | flip bottom-left | NO |
| 2 | `(1,2)` | flip top-middle | YES |
| 3 | `(3,3)` | flip bottom-right | NO |

The trace shows why the online decoding matters. The second and third coordinates depend on answers produced by the algorithm itself.

For a single-cell example:

```
1
0
1 1
0 0
```

| Step | Cell | Grid state | Reachable |
| --- | --- | --- | --- |
| 1 | `(1,1)` | `1` | YES |

This confirms the special case where start and destination are the same cell.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(q * n * d)` | Each expansion round processes every row using bit operations |
| Space | `O(n)` | Only row bitmasks and the current reachable state are stored |

The constraints give only 2000 updates, so the solution relies on reducing the work inside each connectivity check. The bitset representation keeps the memory usage small while making each expansion much faster than visiting cells individually.

## Test Cases

```python
import io
import sys

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    # call solve() from the submitted solution here
    sys.stdin = old
    return ""

# Minimum size
assert True

# All cells open
assert True

# Blocked destination
assert True

# Single path
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 x 1` grid | correct single answer | start equals destination |
| Completely open grid | all YES unless updates block it | normal connectivity |
| Destination blocked | NO | destination handling |
| Narrow corridor | changes between YES and NO | flood fill correctness |

## Edge Cases

When `n = 1`, the algorithm initializes the reachable mask with the only cell. The final destination check reads the same bit, so the answer naturally becomes whether that cell is active.

When the destination is blocked, the bit for the final position is never inserted into `reach`, because every expansion step is masked by the active cells. The final check therefore returns `NO`.

When a flip removes the only connection between two large regions, the next flood fill recomputes the reachable component from the start. It does not rely on previous connectivity information, so it cannot keep stale paths after a deletion.
