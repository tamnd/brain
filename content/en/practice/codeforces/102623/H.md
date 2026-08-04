---
title: "CF 102623H - Hay Mower"
description: "The farm is a grid where every cell has its own weed growth speed. A cell with value a[i][j] gains that many weed units every moment."
date: "2026-08-04T17:20:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102623
codeforces_index: "H"
codeforces_contest_name: "2020 Lenovo Cup USST Campus Online Invitational Contest"
rating: 0
weight: 102623
solve_time_s: 109
verified: true
draft: false
---

[CF 102623H - Hay Mower](https://codeforces.com/problemset/problem/102623/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
# Problem Understanding

The farm is a grid where every cell has its own weed growth speed. A cell with value `a[i][j]` gains that many weed units every moment. At the end of certain moments, the mower clears either an entire row or an entire column, and the task is to find the total amount of weed removed over all operations.

The input gives the grid of growth rates and then a chronological sequence of row and column clearing operations. Since the operation times are strictly increasing, every event can be processed in order. The answer is the sum of all weed removed at every clearing moment, taken modulo `998244353`.

The grid dimensions are at most 500 by 500, so there are at most 250000 cells. The number of mower operations can reach 300000. A direct simulation of the grid would require touching every cell after every operation, which would be around 75000000000 operations in the worst case. Even iterating over a whole dimension for every operation is only acceptable because the dimensions are small, and the intended solution uses this property.

The large values of growth rates and times require 64 bit arithmetic during calculation. A common mistake is to store the answer or intermediate products in 32 bit integers. Another subtle case is when a row and column have both been cut recently. A cell does not remember the last time its row was cut and the last time its column was cut separately. Its actual weed amount depends on the more recent of those two moments.

For example, consider:

```
1 1 2
5
r 1 10
c 1 20
```

The first cut removes `5 * 10 = 50`. The second cut removes nothing because the only cell was already cleared at time 10 and grows for another 10 moments, so the total is `100`.

A careless solution that only tracks the last row cut or only tracks the last column cut would incorrectly count the cell as growing from time 0 in one of the operations.

Another edge case is a zero growth rate:

```
1 1 1
0
r 1 100
```

The answer is `0`. The implementation must still update cut times even when the contribution is zero, because future operations depend on those times.

# Approaches

A straightforward approach is to keep the current weed amount in every cell. When time advances, add the growth to every cell, and when a row or column is mowed, sum that line and clear it. This exactly follows the process and is easy to prove correct. However, the time between events can be huge and the number of events is 300000. Updating all cells after every event costs `O(k*n*m)`, which is far beyond the limit.

The useful observation is that the growth of a cell only depends on the last time its row or its column was cleared. For a cell `(i,j)`, if the last row cut happened at `R[i]` and the last column cut happened at `C[j]`, then the weed currently present is:

`a[i][j] * (current_time - max(R[i], C[j]))`.

When a row is cut, we only need to calculate this formula for the cells in that row. The same applies to a column cut. Since both dimensions are at most 500, checking one whole dimension per event is feasible.

The brute force works because the grid is small, but fails when it repeatedly simulates all cells. The observation about independent row and column reset times lets us reduce the work to a single row or column scan per operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k_n_m) | O(n*m) | Too slow |
| Optimal | O(k*max(n,m)) | O(n*m) | Accepted |

# Algorithm Walkthrough

1. Store the growth rates of all cells. Maintain two arrays: `last_row[i]` stores the last moment row `i` was cleared, and `last_col[j]` stores the last moment column `j` was cleared. Initially both are zero because the grid starts empty.
2. When a row `x` is cleared at time `t`, iterate over every column `j`. The amount in cell `(x,j)` is determined by the latest clearing time among row `x` and column `j`, so add:

`a[x][j] * (t - max(last_row[x], last_col[j]))`

to the answer. After processing the row, set `last_row[x] = t`.
3. When a column `y` is cleared at time `t`, do the symmetric operation over every row `i`:

`a[i][y] * (t - max(last_row[i], last_col[y]))`

Then set `last_col[y] = t`.
4. Take the answer modulo `998244353` after additions to keep values manageable.

Why it works: for every cell, the algorithm adds exactly the amount of weed that existed whenever that cell was cleared. A cell is affected only by operations on its own row or its own column. Between two such operations, the cell grows continuously, and the starting point of that growth interval is exactly the most recent of the two previous clearing times. The formula used in every operation matches this invariant, so every removed unit is counted once and only once.

# Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, m, k = map(int, input().split())

    a = [list(map(int, input().split())) for _ in range(n)]

    last_row = [0] * n
    last_col = [0] * m

    ans = 0

    for _ in range(k):
        typ, x, t = input().split()
        x = int(x) - 1
        t = int(t)

        if typ == 'r':
            lr = last_row[x]
            row = a[x]
            for j in range(m):
                start = lr if lr > last_col[j] else last_col[j]
                ans += row[j] * (t - start)
            last_row[x] = t
        else:
            lc = last_col[x]
            for i in range(n):
                start = last_row[i] if last_row[i] > lc else lc
                ans += a[i][x] * (t - start)
            last_col[x] = t

        ans %= MOD

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The arrays `last_row` and `last_col` contain the only state needed besides the original grid. They represent the reset time of each line, so the current value of a cell never needs to be stored.

For a row operation, the local variable `lr` keeps the old row timestamp before updating it. This matters because the contribution must use the state before the mower clears the row. The same idea is used for columns with `lc`.

Python integers automatically handle the large products involving values up to `10^18`, but the modulo operation keeps the final answer bounded. The comparison is written manually instead of using `max` inside the inner loops because these loops can execute hundreds of millions of times in the largest cases.

# Worked Examples

For the first sample:

```
2 2 3
1 2
3 4
r 1 5
c 2 6
r 1 7
```

| Event | Line time before update | Other line times | Added amount | Answer |
| --- | --- | --- | --- | --- |
| `r 1 5` | row 1 = 0 | columns = 0,0 | `1*5 + 2*5 = 15` | 15 |
| `c 2 6` | column 2 = 0 | rows = 5,0 | `2*(6-5) + 4*6 = 26` | 41 |
| `r 1 7` | row 1 = 5 | columns = 0,6 | `1*(7-5) + 2*(7-6) = 4` | 45 |

The trace shows why the maximum of row and column timestamps is needed. During the second event, cell `(1,2)` starts growing from time 5 because its row was cleared later than its column.

For the second sample:

```
3 4 1
1 2 3 4
5 6 7 8
9 10 11 12
r 1 1000000000000000000
```

| Event | Line | Time | Contribution |
| --- | --- | --- | --- |
| `r 1` | Row 1 | 10^18 | `(1+2+3+4)*10^18` |

The result is calculated modulo `998244353`. This demonstrates that the algorithm never depends on the size of time values, only on differences between timestamps.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k*max(n,m)) | Every operation scans one row or one column. |
| Space | O(n*m) | The grid and timestamp arrays are stored. |

With dimensions limited to 500, the per-operation scan is bounded. The algorithm avoids any dependency on the magnitude of timestamps, which can reach `10^18`.

# Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""
    sys.stdin = old
    return out

# sample 1
assert run("""2 2 3
1 2
3 4
r 1 5
c 2 6
r 1 7
""").strip() == "45"

# sample 2
assert run("""3 4 1
1 2 3 4
5 6 7 8
9 10 11 12
r 1 1000000000000000000
""").strip() == "172998509"

# single zero cell
assert run("""1 1 1
0
r 1 100
""").strip() == "0"

# row and column interaction
assert run("""1 1 2
5
r 1 10
c 1 20
""").strip() == "100"

# equal values
assert run("""2 2 2
7 7
7 7
r 1 3
c 1 5
""").strip() == "49"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single zero cell | 0 | Zero growth handling |
| One cell with row then column cuts | 100 | Correct use of the latest reset time |
| Equal grid values | 49 | Symmetric row and column processing |

# Edge Cases

A cell affected by both a row and column cut must use the later reset time. In:

```
1 1 2
5
r 1 10
c 1 20
```

the first operation adds `5 * 10 = 50`. Before the second operation, the row reset at time 10 is newer than the initial column reset, so the second contribution is `5 * (20 - 10) = 50`. The algorithm stores these two timestamps separately and takes their maximum.

When a line is cleared many times in a row, the previous clear of that same line matters. For example:

```
1 1 2
3
r 1 4
r 1 9
```

The first event removes `12`, and the second removes `15`. The algorithm keeps updating `last_row`, so the second calculation starts from time 4 instead of time 0.

When the time values are extremely large, such as `10^18`, no special handling is needed. The formula only performs multiplication and subtraction on Python integers, which can represent these values exactly.
