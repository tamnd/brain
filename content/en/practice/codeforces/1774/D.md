---
title: "CF 1774D - Same Count One"
description: "We have n binary rows, each of length m. A single operation chooses two rows and one column, then swaps the values in that column between those two rows. Because the swap happens inside the same column, the total number of 1s in the whole matrix never changes."
date: "2026-06-09T12:00:44+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1774
codeforces_index: "D"
codeforces_contest_name: "Polynomial Round 2022 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1600
weight: 1774
solve_time_s: 129
verified: true
draft: false
---

[CF 1774D - Same Count One](https://codeforces.com/problemset/problem/1774/D)

**Rating:** 1600  
**Tags:** brute force, constructive algorithms, greedy, implementation, two pointers  
**Solve time:** 2m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` binary rows, each of length `m`. A single operation chooses two rows and one column, then swaps the values in that column between those two rows.

Because the swap happens inside the same column, the total number of `1`s in the whole matrix never changes. What changes is how those `1`s are distributed among the rows.

The goal is to make every row contain the same number of `1`s. If that is impossible, we output `-1`. Otherwise, we must output the minimum number of operations and a valid sequence of swaps that achieves the target.

The first observation is that the total number of `1`s is invariant. If the total number of `1`s is not divisible by `n`, then equalization is impossible because every row would need the same integer count of `1`s.

The input size is large. Although `n` and `m` can individually reach `10^5`, the sum of `n·m` over all test cases is at most `10^6`. This strongly suggests that an algorithm linear or nearly linear in the matrix size is required. Any approach that repeatedly scans all rows for every operation would become too slow.

The tricky part is not deciding whether a solution exists. The challenge is constructing the minimum number of swaps.

A common mistake is to think that whenever one row has too many `1`s and another has too few, we can always transfer a `1` directly. That is not true. A transfer is only possible in a column where the donor row has `1` and the receiver row has `0`.

Consider:

```
2 2
1 1
1 1
```

Both rows already contain two `1`s, so the answer is zero operations.

Now consider:

```
2 2
1 0
1 0
```

The total number of `1`s is two, so the target is one per row. Both rows already have one `1`, so again the answer is zero.

A careless implementation that tries to "balance columns" instead of row counts could perform unnecessary swaps.

Another subtle case is:

```
2 2
1 1
0 0
```

The target is one `1` per row. Only one swap is needed. We swap column 1 or column 2 between the rows. Any solution using two swaps is correct in the final state but not minimal.

The minimum-operation requirement matters.

## Approaches

A brute-force strategy is to repeatedly choose an overfull row and an underfull row, then search all columns until a transferable position is found. After each transfer, recompute everything and continue.

This works because every successful swap decreases the imbalance by one. Eventually all rows reach the target count.

The problem is efficiency. Suppose there are `O(nm)` required transfers. If every transfer scans the entire matrix again, the complexity can approach `O(nm·min(n,m))` or worse, which is far beyond what the limits allow.

The key observation is that a useful swap always looks the same.

A row with count greater than the target must donate some `1`s.

A row with count smaller than the target must receive some `1`s.

For a fixed column, if one row has `1` and needs to donate while another row has `0` and needs to receive, then that column can perform exactly one required transfer.

This suggests processing columns independently. For each column, we collect:

First, rows that currently have `1` in this column and still have excess `1`s overall.

Second, rows that currently have `0` in this column and still need additional `1`s overall.

Matching one row from the first group with one row from the second group produces a valid swap. Every such swap decreases one surplus and one deficit simultaneously.

Why is this optimal?

Each swap changes the count of exactly two rows by one unit in opposite directions. If a row exceeds the target by `d`, it must participate as a donor at least `d` times. Summing over all surplus rows gives the minimum number of transfers required. Our construction performs exactly one swap for every transferred `1`, so it reaches this lower bound.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²m) or worse | O(1) | Too slow |
| Optimal | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Read the matrix and compute the number of `1`s in every row.
2. Compute the total number of `1`s in the matrix.
3. If the total is not divisible by `n`, output `-1`.
4. Let `target = total // n`.
5. For every column, build two temporary lists.

The first list contains rows whose count is greater than `target` and whose value in this column is `1`.

The second list contains rows whose count is smaller than `target` and whose value in this column is `0`.
6. Match rows from the two lists in order.

Each matched pair represents one valid transfer. Swap the column value between the donor and receiver.
7. After recording the operation, decrease the donor's row count by one and increase the receiver's row count by one.

This update is crucial because a row may stop being a donor or receiver after enough transfers.
8. Continue through all columns.
9. Output all recorded operations.

### Why it works

Let `target` be the desired number of `1`s in every row.

A row with surplus `s = count - target` must donate exactly `s` ones. A row with deficit `d = target - count` must receive exactly `d` ones. The total surplus equals the total deficit.

Whenever we perform a swap, we choose a column where the donor has `1` and the receiver has `0`. After the swap, the donor loses one `1` and the receiver gains one `1`. No other row counts change.

Each operation reduces total imbalance by two units, one surplus and one deficit. Since every operation transfers exactly one required `1`, the number of operations equals the total surplus, which is the smallest possible number of swaps. Thus the construction is both correct and minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())

        a = []
        cnt = []

        total = 0

        for _ in range(n):
            row = list(map(int, input().split()))
            a.append(row)

            s = sum(row)
            cnt.append(s)
            total += s

        if total % n != 0:
            print(-1)
            continue

        target = total // n
        ops = []

        for col in range(m):
            donors = []
            receivers = []

            for row in range(n):
                if cnt[row] > target and a[row][col] == 1:
                    donors.append(row)
                elif cnt[row] < target and a[row][col] == 0:
                    receivers.append(row)

            k = min(len(donors), len(receivers))

            for i in range(k):
                x = donors[i]
                y = receivers[i]

                cnt[x] -= 1
                cnt[y] += 1

                a[x][col] = 0
                a[y][col] = 1

                ops.append((x + 1, y + 1, col + 1))

        print(len(ops))
        for x, y, z in ops:
            print(x, y, z)

solve()
```

The solution begins by counting the number of `1`s in every row. Those counts are the only quantities that matter for deciding who must donate and who must receive.

The divisibility check comes first because no sequence of swaps can change the total number of `1`s in the matrix.

For each column we identify current donors and receivers using the up-to-date row counts. The counts are updated immediately after every swap. This detail is essential. A row that started with surplus three should stop donating after exactly three transfers.

The matrix itself is also updated after every operation. Without updating the column values, later processing could incorrectly reuse the same `1` multiple times.

The recorded operation `(x+1, y+1, col+1)` follows the 1-based indexing required by the statement.

## Worked Examples

### Example 1

Input:

```
3 4
1 1 1 0
0 0 1 0
1 0 0 1
```

Row counts are:

| Row | Count |
| --- | --- |
| 1 | 3 |
| 2 | 1 |
| 3 | 2 |

Total = 6, target = 2.

Processing columns:

| Column | Donors | Receivers | Operation |
| --- | --- | --- | --- |
| 1 | {1} | {2} | (1,2,1) |
| 2 | {} | {} | none |
| 3 | {} | {} | none |
| 4 | {} | {} | none |

After the swap:

| Row | New Count |
| --- | --- |
| 1 | 2 |
| 2 | 2 |
| 3 | 2 |

All rows reach the target with one operation.

This example demonstrates how a single column can resolve both one surplus and one deficit simultaneously.

### Example 2

Input:

```
4 3
1 0 0
0 1 1
0 0 1
0 0 0
```

Counts:

| Row | Count |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 1 |
| 4 | 0 |

Total = 4, target = 1.

Processing:

| Column | Donors | Receivers | Operation |
| --- | --- | --- | --- |
| 1 | {} | {} | none |
| 2 | {2} | {4} | (2,4,2) |
| 3 | {} | {} | none |

Final counts:

| Row | Count |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |

This trace shows that we only need to process columns where a donor has `1` and a receiver has `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every cell is examined a constant number of times |
| Space | O(nm) | Matrix storage plus operation list |

The total value of `n·m` across all test cases is at most `10^6`. A linear scan of all cells is easily fast enough for a 2-second limit in Python. The memory usage also fits comfortably within the 512 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    def solve():
        input = sys.stdin.readline

        t = int(input())

        for _ in range(t):
            n, m = map(int, input().split())

            a = []
            cnt = []
            total = 0

            for _ in range(n):
                row = list(map(int, input().split()))
                a.append(row)
                s = sum(row)
                cnt.append(s)
                total += s

            if total % n:
                print(-1)
                continue

            target = total // n
            ops = []

            for col in range(m):
                donors = []
                receivers = []

                for row in range(n):
                    if cnt[row] > target and a[row][col] == 1:
                        donors.append(row)
                    elif cnt[row] < target and a[row][col] == 0:
                        receivers.append(row)

                k = min(len(donors), len(receivers))

                for i in range(k):
                    x = donors[i]
                    y = receivers[i]

                    cnt[x] -= 1
                    cnt[y] += 1

                    a[x][col] = 0
                    a[y][col] = 1

                    ops.append((x + 1, y + 1, col + 1))

            print(len(ops))
            for op in ops:
                print(*op)

    solve()

    sys.stdout = old_stdout
    return out.getvalue().strip()

# impossible case
assert run(
"""1
2 2
0 0
0 1
"""
) == "-1"

# already balanced
assert run(
"""1
2 2
1 0
0 1
"""
).splitlines()[0] == "0"

# one transfer needed
assert run(
"""1
2 2
1 1
0 0
"""
).splitlines()[0] == "1"

# all zeros
assert run(
"""1
3 3
0 0 0
0 0 0
0 0 0
"""
).splitlines()[0] == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[[0,0],[0,1]]` | `-1` | Total ones not divisible by `n` |
| `[[1,0],[0,1]]` | `0` operations | Already balanced |
| `[[1,1],[0,0]]` | `1` operation | Minimum non-trivial transfer |
| All-zero matrix | `0` operations | Target count equals zero |

## Edge Cases

Consider:

```
2 2
0 0
0 1
```

The total number of `1`s is one. Since `1 % 2 != 0`, no equal distribution exists. The algorithm detects this immediately and outputs `-1`.

Consider:

```
2 2
1 0
0 1
```

Each row already contains one `1`. The target is also one. During column processing, neither row becomes a donor or receiver. No operations are recorded and the answer is zero.

Consider:

```
2 2
1 1
0 0
```

The counts are `(2,0)` and the target is one. In the first column, the first row is a donor and the second row is a receiver. One swap balances both rows immediately. The algorithm outputs exactly one operation, which is minimal.

Consider:

```
3 3
1 1 1
0 0 0
0 0 0
```

The total number of `1`s is three, so the target is one. The first row has surplus two. The other rows each have deficit one. Processing columns independently finds two transferable positions and performs exactly two swaps. After those two transfers every row contains one `1`, and the number of operations equals the total surplus, which is the minimum possible.
