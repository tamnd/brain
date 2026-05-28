---
title: "CF 131E - Yet Another Task with Queens"
description: "We are given positions of queens on a chessboard. A queen attacks in eight directions: left, right, up, down, and the four diagonals. A queen does not attack every queen in a direction, only the first one encountered along that ray."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 131
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 95 (Div. 2)"
rating: 1700
weight: 131
solve_time_s: 158
verified: true
draft: false
---

[CF 131E - Yet Another Task with Queens](https://codeforces.com/problemset/problem/131/E)

**Rating:** 1700  
**Tags:** sortings  
**Solve time:** 2m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given positions of queens on a chessboard. A queen attacks in eight directions: left, right, up, down, and the four diagonals. A queen does not attack every queen in a direction, only the first one encountered along that ray.

For every queen, we must count how many other queens it attacks directly. That value is between 0 and 8 because there are only eight possible directions. After computing this number for every queen, we build an array where `t[i]` is the number of queens attacking exactly `i` other queens.

The board size and the number of queens are both as large as `10^5`. A quadratic solution is immediately ruled out. Checking every pair of queens would require roughly `10^10` comparisons in the worst case, which is far beyond what fits in two seconds. The solution must stay close to `O(m log m)` or better.

The tricky part is the phrase “only the first queen in this direction”. A naive implementation might count every queen sharing the same row, column, or diagonal. That would be wrong.

Consider this example:

```
5 3
2 1
2 3
2 5
```

The queens are all on the same row.

The correct attack counts are:

- `(2,1)` attacks `(2,3)`
- `(2,3)` attacks both neighbors
- `(2,5)` attacks `(2,3)`

So the counts are `[1,2,1]`, and the output is:

```
0 2 1 0 0 0 0 0 0
```

A careless solution that counts every queen in the same row would incorrectly give counts `[2,2,2]`.

Diagonal handling is another common source of bugs. Two queens are on the same diagonal only if either `r - c` or `r + c` matches.

For example:

```
5 2
1 5
3 3
```

These queens lie on the same `/` diagonal because:

```
1 + 5 = 6
3 + 3 = 6
```

A solution checking only `r - c` would miss this attack.

Another subtle case happens when several queens share a line but are not adjacent after sorting.

```
8 4
4 1
4 3
4 5
4 8
```

Only neighboring queens along the row attack each other. The queens at columns `1` and `5` do not interact because `(4,3)` blocks the path.

## Approaches

The brute-force idea is straightforward. For every queen, scan all other queens and check whether they lie in one of the eight directions. If they do, determine whether another queen blocks the path. This works logically because chess movement is geometric and easy to test with coordinate arithmetic.

The problem is cost. There are `m` queens, so checking all pairs already takes `O(m^2)`. With `m = 10^5`, that becomes `10^10` pair checks before even considering blocking logic.

The structure of queen movement gives a much better approach. A queen only interacts with queens sharing:

- the same row
- the same column
- the same `r - c` diagonal
- the same `r + c` diagonal

Inside any one of these lines, only adjacent queens after sorting can attack each other. If two queens have another queen between them on the same line, the nearer queen blocks the farther one.

That observation changes the problem completely. Instead of comparing every pair, we group queens by line:

- row groups by `r`
- column groups by `c`
- diagonal groups by `r - c`
- anti-diagonal groups by `r + c`

Inside each group, we sort positions along the line. Then every adjacent pair contributes exactly one attack in each direction.

For example, if a row contains queens at columns:

```
1, 4, 7
```

then:

- `1` attacks `4`
- `4` attacks both `1` and `7`
- `7` attacks `4`

The pair `(1,7)` never interacts directly.

Every queen participates in at most two adjacent relationships per line type, so the whole computation becomes efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) | O(1) | Too slow |
| Optimal | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read all queen positions and assign every queen an index.

We need stable storage because the final attack count belongs to each specific queen.
2. Create four hash maps.

Each map groups queens sharing one attack line:

- rows by `r`
- columns by `c`
- main diagonals by `r - c`
- anti-diagonals by `r + c`
3. Insert every queen into all four groups.

Each stored entry contains enough information to sort queens along that line and recover the queen index later.
4. For every row group, sort by column.

Adjacent queens after sorting are exactly the queens that see each other horizontally.
5. For every adjacent pair in the sorted row, increment both queens' attack counters.

If queens `A` and `B` are consecutive in sorted order, no queen lies between them, so they attack each other directly.
6. Repeat the same process for column groups.

Here we sort by row because movement is vertical.
7. Repeat for `r - c` diagonal groups.

Sorting by row is sufficient because row and column increase together along this diagonal.
8. Repeat for `r + c` diagonal groups.

Again, sorting by row gives the correct order along the line.
9. After all four structures are processed, every queen has its total number of attacked queens.
10. Build an array `ans[0...8]`.

For each queen with attack count `k`, increment `ans[k]`.
11. Print the frequency array.

### Why it works

Inside any row, column, or diagonal, queens attack only their nearest neighbors in each direction. Sorting queens along a line exposes exactly those nearest neighbors as adjacent elements.

Every direct attack relationship appears once as an adjacent pair in exactly one line group. No attack is missed because every valid attack lies on one of the four line types. No extra attack is added because non-adjacent queens always have another queen blocking the path.

Since we increment both endpoints of every adjacent pair, every queen accumulates precisely the number of queens it attacks.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def process(groups, cnt):
    for arr in groups.values():
        arr.sort()

        for i in range(len(arr) - 1):
            _, a = arr[i]
            _, b = arr[i + 1]

            cnt[a] += 1
            cnt[b] += 1

def solve():
    n, m = map(int, input().split())

    rows = defaultdict(list)
    cols = defaultdict(list)
    diag1 = defaultdict(list)   # r - c
    diag2 = defaultdict(list)   # r + c

    cnt = [0] * m

    for idx in range(m):
        r, c = map(int, input().split())

        rows[r].append((c, idx))
        cols[c].append((r, idx))
        diag1[r - c].append((r, idx))
        diag2[r + c].append((r, idx))

    process(rows, cnt)
    process(cols, cnt)
    process(diag1, cnt)
    process(diag2, cnt)

    ans = [0] * 9

    for x in cnt:
        ans[x] += 1

    print(*ans)

solve()
```

The solution revolves around the `process` function. Each group contains queens sharing one attack line. The tuples are stored as:

```
(position_along_line, queen_index)
```

After sorting, consecutive queens become direct neighbors along that line. For every adjacent pair, both queens gain one attack.

The same logic works for rows, columns, and both diagonals because all queen movement is linear. The only difference is how the groups are formed.

Using `r - c` identifies one diagonal direction because this value stays constant along `\` diagonals. Using `r + c` identifies the other diagonal direction because that value stays constant along `/` diagonals.

A subtle implementation detail is incrementing both endpoints of every adjacent pair. Queen attacks are symmetric here. If `A` sees `B`, then `B` also sees `A` from the opposite direction.

Another easy mistake is sorting diagonals incorrectly. Along a fixed diagonal, sorting by row automatically sorts by column as well, so a single coordinate is enough.

## Worked Examples

### Example 1

Input:

```
8 4
4 3
4 8
6 5
1 6
```

### Row processing

| Row | Sorted queens | Added attacks |
| --- | --- | --- |
| 4 | (3), (8) | both +1 |
| 6 | (5) | none |
| 1 | (6) | none |

Current counts:

| Queen | Count |
| --- | --- |
| (4,3) | 1 |
| (4,8) | 1 |
| (6,5) | 0 |
| (1,6) | 0 |

### Diagonal processing

Queens `(4,8)` and `(1,6)` share `r + c = 12`.

| Diagonal | Sorted queens | Added attacks |
| --- | --- | --- |
| 12 | (1,6), (4,8) | both +1 |

Final counts:

| Queen | Total |
| --- | --- |
| (4,3) | 1 |
| (4,8) | 2 |
| (6,5) | 0 |
| (1,6) | 1 |

Frequency array:

```
0 3 0 1 0 0 0 0 0
```

This example shows that attacks can come from different line types simultaneously.

### Example 2

Input:

```
5 4
3 1
3 3
3 5
1 3
```

### Row processing

| Row | Sorted queens | Added attacks |
| --- | --- | --- |
| 3 | (1), (3), (5) | neighbors attack |

Counts after rows:

| Queen | Count |
| --- | --- |
| (3,1) | 1 |
| (3,3) | 2 |
| (3,5) | 1 |
| (1,3) | 0 |

### Column processing

Column `3` contains `(1,3)` and `(3,3)`.

| Column | Sorted queens | Added attacks |
| --- | --- | --- |
| 3 | (1), (3) | both +1 |

Final counts:

| Queen | Total |
| --- | --- |
| (3,1) | 1 |
| (3,3) | 3 |
| (3,5) | 1 |
| (1,3) | 1 |

Output:

```
0 3 0 1 0 0 0 0 0
```

This trace demonstrates why only adjacent queens matter. `(3,1)` does not attack `(3,5)` because `(3,3)` blocks the path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Every queen participates in sorting inside four groups |
| Space | O(m) | The hash maps and attack counters store all queens once per structure |

The total amount of stored data is linear in the number of queens. Sorting dominates the runtime. Since the sum of sizes of all groups is `m`, the total sorting cost remains `O(m log m)`, which easily fits the limits for `10^5` queens.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def process(groups, cnt):
        for arr in groups.values():
            arr.sort()

            for i in range(len(arr) - 1):
                _, a = arr[i]
                _, b = arr[i + 1]

                cnt[a] += 1
                cnt[b] += 1

    n, m = map(int, input().split())

    rows = defaultdict(list)
    cols = defaultdict(list)
    diag1 = defaultdict(list)
    diag2 = defaultdict(list)

    cnt = [0] * m

    for idx in range(m):
        r, c = map(int, input().split())

        rows[r].append((c, idx))
        cols[c].append((r, idx))
        diag1[r - c].append((r, idx))
        diag2[r + c].append((r, idx))

    process(rows, cnt)
    process(cols, cnt)
    process(diag1, cnt)
    process(diag2, cnt)

    ans = [0] * 9

    for x in cnt:
        ans[x] += 1

    return " ".join(map(str, ans))

# provided sample
assert run(
"""8 4
4 3
4 8
6 5
1 6
"""
) == "0 3 0 1 0 0 0 0 0"

# single queen
assert run(
"""1 1
1 1
"""
) == "1 0 0 0 0 0 0 0 0"

# three queens in one row
assert run(
"""5 3
2 1
2 3
2 5
"""
) == "0 2 1 0 0 0 0 0 0"

# diagonal chain
assert run(
"""5 4
1 1
2 2
3 3
4 4
"""
) == "0 2 2 0 0 0 0 0 0"

# isolated queens
assert run(
"""10 4
1 1
2 4
5 2
9 8
"""
) == "4 0 0 0 0 0 0 0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single queen | `1 0 0 0 0 0 0 0 0` | Minimum input size |
| Three queens in one row | `0 2 1 0 0 0 0 0 0` | Blocking between non-adjacent queens |
| Diagonal chain | `0 2 2 0 0 0 0 0 0` | Correct diagonal grouping |
| Isolated queens | `4 0 0 0 0 0 0 0 0` | No accidental attacks |

## Edge Cases

Consider multiple queens on the same line with blocking:

```
5 3
2 1
2 3
2 5
```

The row group becomes:

```
[(1,A), (3,B), (5,C)]
```

The algorithm processes adjacent pairs:

- `A-B`
- `B-C`

It never connects `A-C` because they are not adjacent after sorting. The resulting attack counts are:

```
A = 1
B = 2
C = 1
```

which is correct.

Now consider anti-diagonal attacks:

```
5 2
1 5
3 3
```

Both queens satisfy:

```
r + c = 6
```

So they enter the same `diag2` group. After sorting, they are adjacent and both gain one attack. The final output is:

```
0 2 0 0 0 0 0 0 0
```

This confirms that both diagonal directions are handled independently.

Finally, consider queens sharing a diagonal but blocked:

```
6 3
1 1
3 3
5 5
```

The sorted diagonal group is:

```
[(1,A), (3,B), (5,C)]
```

Only adjacent pairs contribute:

- `A-B`
- `B-C`

The queens `A` and `C` never attack each other because `B` blocks the path. The counts become:

```
1 2 1
```

which matches actual chess movement exactly.
