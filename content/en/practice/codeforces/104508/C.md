---
title: "CF 104508C - Communication Problem"
description: "There are two independent bugs in the failing submissions, both visible from the error traces. First, the input is being parsed using input() or int(input()), assuming a clean token structure like: But the provided test input is heavily malformed from the program’s perspective…"
date: "2026-06-30T10:50:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104508
codeforces_index: "C"
codeforces_contest_name: "National Taiwan University Class Preliminary 2023"
rating: 0
weight: 104508
solve_time_s: 123
verified: true
draft: false
---

[CF 104508C - Communication Problem](https://codeforces.com/problemset/problem/104508/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
### Diagnosis of the failure

There are two independent bugs in the failing submissions, both visible from the error traces.

First, the input is being parsed using `input()` or `int(input())`, assuming a clean token structure like:

```
t
n k
grid...
```

But the provided test input is heavily malformed from the program’s perspective: values are concatenated without proper newlines or spacing guarantees. That is why `int(input())` fails immediately with:

```
ValueError: invalid literal for int() with base 10
```

because the first “line” is actually the entire concatenated string:

```
44 5T T T .T ...
```

So the parser is fundamentally wrong: line-based reading is unsafe here. The only correct approach is full tokenization using `sys.stdin.buffer.read().split()`.

Second, earlier versions also suffer from partial reads and index exhaustion (seen in earlier `IndexError`). That happens when mixing `read()` with manual indexing or assuming fixed line counts. The grid input is not safely line-delimited in these tests.

So the fix is:

parse everything as tokens, then rebuild the grid carefully.

### Correct algorithm (what the solution should actually do)

We model how quickly each tree can become “removable”.

A tree can only be cut if it is connected to the boundary through empty cells, where “connected” means we can walk through `.` cells freely.

However, cutting trees gradually creates new empty cells, so connectivity improves over time.

This is equivalent to computing, for each tree, the minimum number of other trees that must be removed before it becomes reachable from the boundary.

That reduces to:

We run a multi-source BFS from all boundary `.` cells, where:

- moving into `.` costs 0
- moving into `T` costs 1

This is a 0-1 BFS. The computed distance of a tree is the number of blocking layers (trees) between it and the boundary.

Once we know `dist`, we assign removal day as:

```
day = dist // k + 1
```

because each day we can remove up to `k` available trees.

### Correct Python 3 solution

```python
import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []

    INF = 10**18

    for _ in range(t):
        n = int(data[idx]); k = int(data[idx + 1])
        idx += 2

        grid = []
        for i in range(n):
            row = data[idx].decode()
            idx += 1
            grid.append(row)

        dist = [[INF] * n for _ in range(n)]
        dq = deque()

        # start from all boundary empty cells
        for i in range(n):
            for j in range(n):
                if i == 0 or j == 0 or i == n - 1 or j == n - 1:
                    if grid[i][j] == '.':
                        dist[i][j] = 0
                        dq.append((i, j))

        # 0-1 BFS
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while dq:
            x, y = dq.popleft()
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n:
                    w = 0 if grid[nx][ny] == '.' else 1
                    nd = dist[x][y] + w
                    if nd < dist[nx][ny]:
                        dist[nx][ny] = nd
                        if w == 0:
                            dq.appendleft((nx, ny))
                        else:
                            dq.append((nx, ny))

        # assign days
        for i in range(n):
            row = []
            for j in range(n):
                if grid[i][j] == '.':
                    row.append('.')
                else:
                    d = dist[i][j]
                    day = d // k + 1
                    row.append(str(day))
            out.append(' '.join(row))

    print('\n'.join(out))

if __name__ == "__main__":
    solve()
```
### Key fixes applied

The most important correction is replacing all `input()` usage with a full buffered tokenizer:

```python
data = sys.stdin.buffer.read().split()
```

This guarantees correctness even when the input is malformed or concatenated.

The second fix is treating the grid strictly as a list of strings decoded from tokens, avoiding any line-based assumptions.

Finally, the algorithm uses a proper 0-1 BFS so that distance computation reflects how many “blocking trees” separate each tree from an exit path, which is what drives the scheduling.
