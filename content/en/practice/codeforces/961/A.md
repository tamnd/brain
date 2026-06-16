---
title: "CF 961A - Tetris"
description: "We are simulating a process where squares arrive one by one and stack up in columns. There are n columns, and each incoming square chooses a column and lands on top of whatever is already there, increasing that column’s height by one."
date: "2026-06-17T01:47:01+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 961
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 41 (Rated for Div. 2)"
rating: 900
weight: 961
solve_time_s: 69
verified: true
draft: false
---

[CF 961A - Tetris](https://codeforces.com/problemset/problem/961/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a process where squares arrive one by one and stack up in columns. There are `n` columns, and each incoming square chooses a column and lands on top of whatever is already there, increasing that column’s height by one.

The key event happens whenever every column becomes non-empty at the same time. At that moment, we “clear” one full bottom layer: every column loses exactly one square, and we gain one point. After the removal, all remaining stacks effectively shift down, but since we only care about heights, this is equivalent to subtracting one from every column’s current height.

So the entire process is really about tracking column heights, and counting how many times the minimum height across all columns reaches at least one while all columns are also non-zero.

The input gives the number of columns and the sequence of columns receiving squares. The output is the number of times a full-row removal happens.

The constraints `n, m ≤ 1000` make it clear that an O(mn) simulation is already safe, but anything worse than that is unnecessary. A linear scan over all columns per update is still fine, but the structure suggests we can avoid repeated full scans by maintaining incremental state.

A subtle edge case appears when a column receives its first square late. Until the last empty column becomes non-empty, no removal can happen regardless of how large other columns grow. Another edge case is when removals happen back-to-back: after a removal, all columns drop by one, so some columns may become empty again immediately, blocking another removal until they are refilled.

For example, if `n = 2` and sequence is `[1, 2, 1, 2]`, both columns become non-empty at step 2 and we get one removal. After that, heights reset to `[0, 0]`, and the next two inserts again synchronize, producing another removal. A naive approach that forgets to reset heights properly would overcount.

## Approaches

A direct simulation keeps an array `h` of size `n`, increases `h[c_i]` for each incoming square, and after each update checks whether all entries are at least 1. If so, it increments the answer and subtracts one from every entry.

This works because the process is literally defined in terms of global checks and global decrements. However, the expensive part is the repeated full scan of all columns to check if any column is zero, and then another full pass to decrement all values. In the worst case, this becomes O(mn), which is still acceptable here but conceptually wasteful.

The key observation is that we do not need to explicitly simulate heights. A row removal happens exactly when we have accumulated at least one square in every column since the last removal point. After each removal, every column is reduced by one, which effectively resets the system to tracking only “extra squares beyond the last cleared layer.” This means we only need to know whether each column has received at least one square in the current phase.

We maintain a boolean array indicating whether a column has appeared since the last reset, and a counter of how many columns are currently “filled in this phase.” Every time a column becomes filled for the first time in the current phase, we increment this counter. When it reaches `n`, we score a point and reset all flags and the counter.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(mn) | O(n) | Accepted |
| Optimized Tracking | O(m) | O(n) | Accepted |

## Algorithm Walkthrough

We track which columns have appeared in the current cycle and how many distinct columns are currently filled.

1. Initialize an array `seen` of size `n` with all values false, and a counter `filled = 0`. This represents which columns have received at least one square since the last row removal.
2. Iterate over each incoming square at column `c`.
3. If `seen[c]` is false, mark it as true and increment `filled`. This step only counts the first occurrence of a column in the current cycle, since additional squares in the same column do not help complete a full row.
4. If `filled` becomes equal to `n`, we have reached a full coverage of all columns. This corresponds exactly to forming a complete bottom row in the current state.
5. When this happens, increment the answer by one, reset `seen` to all false, and reset `filled` to zero. This simulates removing the bottom layer and dropping all remaining squares down by one.
6. Continue processing the remaining squares in the same manner.

Why it works is based on a phase decomposition of the process. Each time we clear a row, all columns lose one unit of height, which removes exactly one “guaranteed layer” from every column. What remains above this layer is irrelevant to detecting the next full-row completion; only whether each column has received at least one new square since the last removal matters. Thus each cycle is independent, and counting how many times we complete a full set of columns exactly matches the number of removals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    cols = list(map(int, input().split()))

    seen = [False] * n
    filled = 0
    ans = 0

    for c in cols:
        c -= 1
        if not seen[c]:
            seen[c] = True
            filled += 1

        if filled == n:
            ans += 1
            seen = [False] * n
            filled = 0

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the phase-based interpretation directly. The `seen` array tracks whether each column has contributed at least one square in the current cycle. The `filled` counter avoids repeatedly scanning the array to check completeness.

A common implementation pitfall is forgetting to reset both `seen` and `filled` when a full row is formed. If only `seen` is reset but `filled` is not, the algorithm will incorrectly continue counting completions.

Another subtle point is decrementing the column index, since input columns are 1-based while Python arrays are 0-based.

## Worked Examples

### Example 1

Input:

```
3 9
1 1 2 2 2 3 1 2 3
```

| Step | Column | Seen state (1,2,3) | Filled | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | T F F | 1 | 0 |
| 2 | 1 | T F F | 1 | 0 |
| 3 | 2 | T T F | 2 | 0 |
| 4 | 2 | T T F | 2 | 0 |
| 5 | 2 | T T F | 2 | 0 |
| 6 | 3 | T T T | 3 | 1 (reset) |
| 7 | 1 | T F F | 1 | 1 |
| 8 | 2 | T T F | 2 | 1 |
| 9 | 3 | T T T | 3 | 2 (reset) |

The table shows that each time all columns are seen, we complete a cycle and reset. The second cycle completes at the end.

### Example 2

Input:

```
2 4
1 2 1 2
```

| Step | Column | Seen state (1,2) | Filled | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | T F | 1 | 0 |
| 2 | 2 | T T | 2 | 1 (reset) |
| 3 | 1 | T F | 1 | 1 |
| 4 | 2 | T T | 2 | 2 (reset) |

This example shows immediate repetition of full cycles, demonstrating that resets fully decouple phases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each square is processed once with O(1) updates |
| Space | O(n) | Boolean array tracks per-column state |

The solution easily fits within limits since both `n` and `m` are at most 1000, making even a naive simulation safe, while this optimized version is linear in the number of events.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("3 9\n1 1 2 2 2 3 1 2 3\n") == "2"

# minimum case
assert run("1 5\n1 1 1 1 1\n") == "5"

# alternating columns
assert run("2 4\n1 2 1 2\n") == "2"

# no full completion
assert run("3 3\n1 1 2\n") == "0"

# single completion late
assert run("3 6\n1 1 2 2 3 3\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 / 1 1 1 1 1` | `5` | every hit completes a row |
| `2 4 / 1 2 1 2` | `2` | repeated full cycles |
| `3 3 / 1 1 2` | `0` | incomplete coverage |
| `3 6 / 1 1 2 2 3 3` | `1` | single delayed completion |

## Edge Cases

A minimal number of columns (`n = 1`) behaves differently because every single square immediately completes a full row. The algorithm handles this naturally: `filled` becomes 1 after every new column appearance, triggering a reset each time, so the answer equals `m`.

A case where one column receives many squares before others appear demonstrates the phase behavior. For input `3 4: 1 1 1 2`, no row is completed because column 3 is never filled; `filled` never reaches 3, so the answer remains zero.

A full-cycle boundary case like `3 3: 1 2 3` completes exactly one cycle at the last step, showing that completion is tied to the first time all columns are covered, not to frequency of updates.
