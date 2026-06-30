---
title: "CF 104400L - Timetable Queries"
description: "We are given a one-day timetable of length n, where each minute has exactly one bus arriving and each arrival is labeled with a bus number. So the input array is a sequence of identifiers, and the i-th value tells us which bus arrives at minute i."
date: "2026-07-01T00:56:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104400
codeforces_index: "L"
codeforces_contest_name: "Hunan University 2023 the 19th Programming Contest"
rating: 0
weight: 104400
solve_time_s: 47
verified: true
draft: false
---

[CF 104400L - Timetable Queries](https://codeforces.com/problemset/problem/104400/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-day timetable of length `n`, where each minute has exactly one bus arriving and each arrival is labeled with a bus number. So the input array is a sequence of identifiers, and the i-th value tells us which bus arrives at minute i.

After that, we receive `q` queries. Each query asks for a specific bus number `x` and a position `y`, and we must report the minute when the y-th occurrence of bus `x` happens in the timetable. If that bus appears fewer than `y` times, we return `-1`.

The core operation is not about time itself but about indexing occurrences inside filtered subsequences. For each bus number, we conceptually care about the list of all positions where it appears.

The constraints are `n, q ≤ 100000`. A direct scan per query would be too slow. If each query scans the full array, we get `O(nq)`, which is on the order of 10¹⁰ operations in the worst case, far beyond what 2 seconds allows in Python.

A more subtle constraint is that bus numbers can be as large as 10⁹, so we cannot use them as direct array indices. Any solution must rely on hashing or coordinate compression.

A few edge cases matter here. If a bus appears only once, any query asking for the second occurrence should return `-1`. If all values are identical, queries for large `y` values will frequently fail. If a bus never appears at all, every query for it is immediately `-1`. These cases break solutions that assume existence without checking list lengths.

## Approaches

The brute-force idea is straightforward. For each query `(x, y)`, we scan the entire timetable and count occurrences of `x` until we reach the y-th match. Once we hit it, we return the index. If we finish the array first, we return `-1`.

This is correct because it directly simulates the definition of the problem. The issue is cost. Each query costs `O(n)` time, so across `q` queries we perform up to `n × q` comparisons. With both up to 100000, this becomes too large.

The key observation is that the timetable does not change. Every query asks about the same fixed sequence. That means we can preprocess all occurrences once, storing for each bus number a list of positions where it appears. Then each query becomes a simple array lookup: the y-th element of that list, if it exists.

This transforms the problem from repeated scanning into indexed access. The heavy work moves into a single pass over the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Precompute positions | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a dictionary that maps each bus number to a list of positions where it appears. This structure is necessary because bus numbers are large and sparse, so array indexing is not feasible.
2. Scan the timetable from left to right. For each minute i, append i to the list corresponding to the bus number at that position. This builds exact occurrence order, which is required because queries depend on chronological ordering.
3. After preprocessing, each bus number has a sorted list of occurrence indices, naturally in increasing order because we inserted left to right.
4. For each query `(x, y)`, check whether `x` exists in the dictionary. If it does not, immediately output `-1` because the bus never appears.
5. If it exists, check whether the list has at least `y` elements. If not, output `-1` since the requested occurrence does not exist.
6. Otherwise output the element at index `y-1` in the list. This directly corresponds to the y-th occurrence in time order.

The reason this indexing works is that we preserved the exact chronological order during preprocessing, so list order is equivalent to time order.

### Why it works

The algorithm relies on the invariant that for each bus number `x`, its stored list contains all indices where `x` appears, in strictly increasing order. Since every query asks for the y-th occurrence in time, this is equivalent to the y-th element in that ordered list. No reordering or recomputation is ever needed, so each query reduces to a constant-time lookup on a correct precomputed structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    pos = {}

    for i, v in enumerate(a, start=1):
        if v not in pos:
            pos[v] = []
        pos[v].append(i)

    out = []

    for _ in range(q):
        x, y = map(int, input().split())
        if x not in pos:
            out.append("-1")
        else:
            lst = pos[x]
            if y <= 0 or y > len(lst):
                out.append("-1")
            else:
                out.append(str(lst[y - 1]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The preprocessing loop builds a hash map keyed by bus number, storing all occurrence indices. The use of `enumerate(..., start=1)` ensures we store 1-based positions, matching the problem’s minute indexing.

Each query is handled in constant time by checking dictionary membership and list bounds. The boundary condition `y > len(lst)` is essential because missing it leads to out-of-range access or incorrect assumptions about frequency.

## Worked Examples

### Example 1

Input:

```
10 5
1 2 3 4 5 5 4 3 2 1
1 1
1 2
1 3
6 1
5 2
```

We build positions:

| Bus | Positions |
| --- | --- |
| 1 | [1, 10] |
| 2 | [2, 9] |
| 3 | [3, 8] |
| 4 | [4, 7] |
| 5 | [5, 6] |

Now queries:

| x | y | list(x) | answer |
| --- | --- | --- | --- |
| 1 | 1 | [1,10] | 1 |
| 1 | 2 | [1,10] | 10 |
| 1 | 3 | [1,10] | -1 |
| 6 | 1 | [] | -1 |
| 5 | 2 | [5,6] | 6 |

Output:

```
1
10
-1
-1
6
```

This trace confirms that direct indexing into stored positions matches chronological occurrence counting.

### Example 2

Input:

```
10 5
1 2 1 2 1 2 3 3 3 1
1 4
1 5
3 3
3 4
2 2
```

Positions:

| Bus | Positions |
| --- | --- |
| 1 | [1, 3, 5, 10] |
| 2 | [2, 4, 6] |
| 3 | [7, 8, 9] |

Queries:

| x | y | list(x) | answer |
| --- | --- | --- | --- |
| 1 | 4 | [1,3,5,10] | 10 |
| 1 | 5 | [1,3,5,10] | -1 |
| 3 | 3 | [7,8,9] | 9 |
| 3 | 4 | [7,8,9] | -1 |
| 2 | 2 | [2,4,6] | 4 |

This shows both successful retrieval and failure cases when `y` exceeds frequency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | One pass to build position lists, then constant-time per query |
| Space | O(n) | Each index is stored exactly once in a list |

The solution fits comfortably within limits because both preprocessing and query handling scale linearly with input size. With `n, q ≤ 100000`, this stays well under typical time constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    pos = {}
    for i, v in enumerate(a, start=1):
        pos.setdefault(v, []).append(i)

    out = []
    for _ in range(q):
        x, y = map(int, input().split())
        if x not in pos or y > len(pos[x]):
            out.append("-1")
        else:
            out.append(str(pos[x][y - 1]))

    return "\n".join(out)

# provided sample 1
assert run("""10 5
1 2 3 4 5 5 4 3 2 1
1 1
1 2
1 3
6 1
5 2
""") == """1
10
-1
-1
6"""

# provided sample 2
assert run("""10 5
1 2 1 2 1 2 3 3 3 1
1 4
1 5
3 3
3 4
2 2
""") == """10
-1
9
-1
4"""

# single element edge
assert run("""1 2
7
7 1
7 2
""") == """1
-1"""

# all equal
assert run("""5 3
9 9 9 9 9
9 1
9 5
9 6
""") == """1
5
-1"""

# missing value
assert run("""3 2
1 2 3
4 1
4 2
""") == """-1
-1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | mix of valid and invalid | boundary indexing |
| all equal | first, last, overflow | frequency edge cases |
| missing value | -1 outputs | absent key handling |

## Edge Cases

A bus that never appears is handled entirely through dictionary membership. When `x` is absent, the lookup fails immediately and returns `-1` without touching any list. This avoids accidental KeyError or incorrect default assumptions.

A bus that appears fewer times than requested relies on the stored list length check. For example, if `pos[x] = [2, 5]` and the query asks for `y = 3`, the condition `y > len(pos[x])` triggers, returning `-1`. Without this check, accessing `pos[x][2]` would crash.

Large `y` values are safe because they never require iteration. The algorithm never counts occurrences during queries, so extreme `y` values do not affect performance or correctness beyond a single comparison.
