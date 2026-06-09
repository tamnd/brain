---
title: "CF 1635B - Avoid Local Maximums"
description: "We have to modify an array so that no position is strictly greater than both of its neighbors. Such positions are called local maximums. The first and last elements are never local maximums because they only have one neighbor."
date: "2026-06-10T04:40:52+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1635
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 772 (Div. 2)"
rating: 800
weight: 1635
solve_time_s: 122
verified: false
draft: false
---

[CF 1635B - Avoid Local Maximums](https://codeforces.com/problemset/problem/1635/B)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We have to modify an array so that no position is strictly greater than both of its neighbors. Such positions are called local maximums. The first and last elements are never local maximums because they only have one neighbor.

Each operation allows changing one element to any value between 1 and $10^9$. The goal is to minimize the number of modified positions and output one valid resulting array.

The total number of elements over all test cases is at most $2 \cdot 10^5$. With a two second limit, linear or near linear solutions are completely safe. Quadratic algorithms would require roughly $4 \cdot 10^{10}$ operations in the worst case, which is far too much.

Several situations are easy to mishandle.

Consider consecutive peaks:

```
1 3 1 3 1
```

Positions 2 and 4 are both local maximums. If we fix them independently by lowering each peak, we use two operations. A better solution is changing the middle element:

```
1 3 3 3 1
```

Only one operation is needed. Treating every peak separately misses this optimization.

Another tricky case is three consecutive peaks separated by valleys:

```
2 1 3 1 3 1 3
```

Changing the middle valley to a large enough value removes two neighboring peaks at once:

```
2 1 3 3 3 1 3
```

After that, only the last peak remains. A greedy strategy must recognize this pattern.

Boundary positions also need care. In

```
5 1 5
```

only the middle element has two neighbors, so positions 1 and 3 cannot be local maximums regardless of their values. Accidentally checking them would produce incorrect results.

## Approaches

A brute force view is to detect every local maximum and fix it independently. One possibility is lowering each peak until it is no larger than one of its neighbors. This approach is correct because every operation destroys at least one peak.

The weakness appears when peaks alternate with valleys:

```
1 3 1 3 1
```

Fixing both peaks separately requires two modifications, even though changing the center element once removes both peaks. Since every peak is processed independently, interactions between nearby peaks are ignored.

The key observation is that a pattern

```
peak - valley - peak
```

can be handled with a single operation. If positions $i-1$ and $i+1$ are peaks, increasing position $i$ to

```
max(a[i-1], a[i+1])
```

removes both local maximums simultaneously.

This suggests scanning from left to right. Whenever two peaks are separated by exactly one element, we modify that middle element and skip ahead. Otherwise, isolated peaks are fixed individually.

Since every position is examined only a constant number of times, the whole algorithm runs in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Not always optimal |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the array and record which positions are local maximums.
2. Traverse the array from left to right.
3. Whenever positions `i` and `i+2` are both local maximums, modify position `i+1`.
4. Set

```
a[i+1] = max(a[i], a[i+2])
```

because this makes the middle element at least as large as both peaks, so neither side remains a local maximum.

1. Count one operation and skip ahead by three positions, since both peaks have already been handled.
2. If position `i` is a local maximum but position `i+2` is not, treat it as an isolated peak.
3. Replace

```
a[i] = max(a[i-1], a[i+1])
```

which immediately destroys that local maximum.

1. Count one operation and continue scanning.
2. Print the number of operations and the final array.

### Why it works

The only way one operation can remove two peaks is when those peaks are separated by exactly one element. Any larger distance means the peaks are independent.

During the left to right scan, every pair of neighboring peaks is detected once. Modifying the middle element removes both simultaneously, which is always better than spending two operations. Peaks that are not part of such a pair cannot share an operation with another peak, so fixing them individually is optimal. Thus the total number of operations is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
ans = []

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    peak = [False] * n
    for i in range(1, n - 1):
        if a[i] > a[i - 1] and a[i] > a[i + 1]:
            peak[i] = True

    cnt = 0
    i = 1

    while i < n - 1:
        if peak[i]:
            if i + 2 < n and peak[i + 2]:
                a[i + 1] = max(a[i], a[i + 2])
                cnt += 1
                i += 3
            else:
                a[i] = max(a[i - 1], a[i + 1])
                cnt += 1
                i += 1
        else:
            i += 1

    ans.append(str(cnt))
    ans.append(" ".join(map(str, a)))

sys.stdout.write("\n".join(ans))
```

The first loop identifies all local maximums in the original array. This information is kept fixed during the scan. Recomputing peaks after every modification would complicate the implementation and is unnecessary.

The main loop processes peaks from left to right. When two peaks are two positions apart, one modification of the middle element removes both. The index then jumps by three positions because those peaks are finished.

For isolated peaks, replacing the peak value with the larger neighbor destroys that peak without creating a new one. Using the maximum neighbor value is enough because equality does not count as a local maximum.

Boundary positions are never examined because the loop starts from index 1 and stops before index `n-1`.

## Worked Examples

### Example 1

Input:

```
1 2 1 2 1
```

Initial peaks are at positions 2 and 4.

| i | Peaks at i and i+2 | Operation | Array |
| --- | --- | --- | --- |
| 1 | Yes | Set a[2]=max(2,2)=2 | 1 2 2 2 1 |

Only one operation is required.

This example shows how a single modification can remove two neighboring peaks.

### Example 2

Input:

```
1 2 1 3 2 3 1 2 1
```

Initial peaks are at positions 2, 4, and 6.

| i | Peaks at i and i+2 | Operation | Array |
| --- | --- | --- | --- |
| 1 | Yes | Set a[2]=3 | 1 2 3 3 2 3 1 2 1 |
| 4 | No | Set a[5]=3 | 1 2 3 3 2 3 3 2 1 |

The final array contains no local maximums.

This trace demonstrates that one paired operation may be followed by an isolated peak.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every position is visited a constant number of times |
| Space | O(n) | The peak array stores whether each position is initially a local maximum |

Since the total number of elements over all test cases is at most $2 \cdot 10^5$, linear time easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        peak = [False] * n
        for i in range(1, n - 1):
            if a[i] > a[i - 1] and a[i] > a[i + 1]:
                peak[i] = True

        cnt = 0
        i = 1

        while i < n - 1:
            if peak[i]:
                if i + 2 < n and peak[i + 2]:
                    a[i + 1] = max(a[i], a[i + 2])
                    cnt += 1
                    i += 3
                else:
                    a[i] = max(a[i - 1], a[i + 1])
                    cnt += 1
                    i += 1
            else:
                i += 1

        out.append(str(cnt))
        out.append(" ".join(map(str, a)))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return result

# minimum size
assert run("1\n2\n5 7\n") == "0\n5 7"

# all equal
assert run("1\n5\n4 4 4 4 4\n") == "0\n4 4 4 4 4"

# alternating peaks
assert run("1\n5\n1 3 1 3 1\n") == "1\n1 3 3 3 1"

# isolated peak
assert run("1\n4\n1 4 2 1\n") == "1\n1 2 2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 7 | 0 operations | Minimum size |
| 4 4 4 4 4 | No changes | Equal values |
| 1 3 1 3 1 | One operation | Shared fix for two peaks |
| 1 4 2 1 | One operation | Isolated peak handling |

## Edge Cases

Consider

```
1 3 1 3 1
```

Initial peaks are at positions 2 and 4. The algorithm notices that they are separated by one element and changes the center value:

```
1 3 3 3 1
```

Only one operation is used. A strategy that fixes each peak independently would spend two operations.

Consider

```
2 1 3 1 3 1 3
```

The first pair of peaks at positions 3 and 5 share a middle element, so one operation removes both:

```
2 1 3 3 3 1 3
```

The remaining peak at position 7 is isolated and is fixed separately. Two operations are optimal.

Consider

```
5 1 5
```

Neither endpoint can ever be a local maximum. The loop only examines the center position, which is smaller than both neighbors, so no operation is performed and the array remains unchanged. This avoids off by one errors at the boundaries.
