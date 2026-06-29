---
title: "CF 104636B - Vlad and Cafes"
description: "We are given a sequence of cafe visits, where each number represents the index of a cafe Vlad visited at that moment in time. Cafes can repeat, meaning Vlad may visit the same cafe multiple times, and we only care about the order of visits."
date: "2026-06-29T17:05:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104636
codeforces_index: "B"
codeforces_contest_name: "\u041c\u0438\u0441\u0438\u0441 2023 \u043e\u0441\u0435\u043d\u044c - \u043c\u0430\u0441\u0441\u0438\u0432\u044b, \u0441\u0442\u0440\u043e\u043a\u0438"
rating: 0
weight: 104636
solve_time_s: 108
verified: true
draft: false
---

[CF 104636B - Vlad and Cafes](https://codeforces.com/problemset/problem/104636/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of cafe visits, where each number represents the index of a cafe Vlad visited at that moment in time. Cafes can repeat, meaning Vlad may visit the same cafe multiple times, and we only care about the order of visits.

The task is to identify the cafe whose most recent visit is the earliest among all cafes that appear in the sequence. In simpler terms, for each distinct cafe, we look at when it was last visited, and we want the cafe whose last occurrence is farthest in the past.

The constraints allow up to 200,000 visits, so any solution that repeatedly scans the array for each distinct cafe would be too slow. A quadratic approach would involve scanning the whole array per cafe, which can degrade to about 4 × 10^10 operations in the worst case, which is not feasible in 2 seconds. This immediately pushes us toward a linear or near-linear solution.

A subtle edge case arises when multiple cafes appear only once. In that case, the answer is the cafe whose single occurrence is earliest in the array, since its last visit is also that occurrence. Another edge case occurs when all values are identical, where the answer is trivially that cafe.

A common mistake is trying to track the first occurrence instead of the last. For example, in a sequence like 2 1 2 3, cafe 1 appears once but not necessarily relevant, while cafe 2 appears twice and its last occurrence is later. The correct answer depends only on last positions, not first appearances.

## Approaches

A brute-force solution would consider each distinct cafe, scan the entire array, and record the last position where it appears. After computing all last occurrences, we choose the minimum among them. While correct, this approach repeats a full scan for every unique cafe. If there are k distinct cafes, the worst-case time complexity becomes O(nk), which degenerates to O(n^2) when all values are distinct.

The key observation is that we do not need to recompute last occurrences repeatedly. Each time we see a cafe in the array, we can overwrite its stored position. By the end of the scan, the stored value for each cafe is exactly its last occurrence index. This reduces the problem to a single pass through the array, followed by a simple selection step over the recorded positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal (last occurrence tracking) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a dictionary or array `last` that maps each cafe index to its most recent position in the sequence. We initialize it as empty because no cafe has been seen yet.
2. Iterate through the visit sequence from left to right. For each position `i`, store `last[a[i]] = i`. This ensures that every time we see a cafe, we overwrite its previous record, so only the most recent position remains.
3. After processing the entire sequence, we now have the last occurrence index for every cafe that appears at least once.
4. Scan through all recorded cafes and choose the one with the smallest stored index. This corresponds to the cafe whose last visit is the farthest in the past.
5. Output the index of that cafe.

The reason we scan all recorded cafes at the end instead of maintaining a running minimum is that we only know the final last positions after processing the full sequence.

### Why it works

At any point in the iteration, `last[x]` is exactly the most recent position of cafe `x` among the prefix processed so far. Once the loop ends, this value becomes the true last occurrence in the full array. Since the final answer depends only on these last occurrences, selecting the minimum index among them correctly identifies the cafe whose last visit is earliest in time.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

last = {}

for i, x in enumerate(a):
    last[x] = i

ans = None
best_pos = 10**18

for x, pos in last.items():
    if pos < best_pos:
        best_pos = pos
        ans = x

print(ans)
```

The first pass through the array builds the mapping from cafe to its last seen index. The enumeration index `i` naturally represents the visit time. Each assignment overwrites earlier positions, which is essential to ensure correctness.

The second loop compares stored last positions. We track both the best position and the corresponding cafe. Using a large initial value ensures the first comparison always succeeds.

A common pitfall is using 1-based vs 0-based indexing inconsistently. Here we use 0-based indices internally, but since we only compare relative ordering, the final answer remains correct regardless of indexing base.

## Worked Examples

### Sample 1

Input:

```
5
1 3 2 1 2
```

| i | cafe | last after step |
| --- | --- | --- |
| 0 | 1 | {1:0} |
| 1 | 3 | {1:0, 3:1} |
| 2 | 2 | {1:0, 3:1, 2:2} |
| 3 | 1 | {1:3, 3:1, 2:2} |
| 4 | 2 | {1:3, 3:1, 2:4} |

Final last occurrences are 1 → 3, 3 → 1, 2 → 4. The minimum is position 1, corresponding to cafe 3.

Output:

```
3
```

This trace shows that only the final overwrite matters. Earlier occurrences of cafe 1 and 2 are irrelevant once their last visit is updated.

### Sample 2

Input:

```
6
2 1 2 2 4 1
```

| i | cafe | last after step |
| --- | --- | --- |
| 0 | 2 | {2:0} |
| 1 | 1 | {2:0, 1:1} |
| 2 | 2 | {2:2, 1:1} |
| 3 | 2 | {2:3, 1:1} |
| 4 | 4 | {2:3, 1:1, 4:4} |
| 5 | 1 | {2:3, 1:5, 4:4} |

Final last positions are 2 → 3, 1 → 5, 4 → 4. The minimum is 3, corresponding to cafe 2.

Output:

```
2
```

This example highlights repeated overwriting. Cafe 2 appears multiple times, but only its final occurrence determines its score.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to record last occurrences and one pass over distinct keys |
| Space | O(n) | Stores at most one entry per distinct cafe |

The solution fits comfortably within constraints since 200,000 operations are trivial for a linear pass in Python, and dictionary operations are amortized constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    last = {}
    for i, x in enumerate(a):
        last[x] = i

    ans = None
    best_pos = 10**18
    for x, pos in last.items():
        if pos < best_pos:
            best_pos = pos
            ans = x

    return str(ans)

# provided samples
assert run("5\n1 3 2 1 2\n") == "3"
assert run("6\n2 1 2 2 4 1\n") == "2"

# minimum size
assert run("1\n7\n") == "7"

# all equal
assert run("5\n9 9 9 9 9\n") == "9"

# strictly increasing distinct
assert run("4\n1 2 3 4\n") == "1"

# last is earliest candidate
assert run("5\n5 4 3 2 1\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | same element | minimum boundary case |
| all equal | that value | repeated overwrite correctness |
| increasing sequence | first element | earliest last occurrence |
| decreasing sequence | last element | reverse ordering correctness |

## Edge Cases

### Single visit

Input:

```
1
10
```

The algorithm stores `last[10] = 0`. No other entries exist, so the minimum is trivially 10. The output is correct because the only cafe is both first and last by definition.

### All cafes identical

Input:

```
5
3 3 3 3 3
```

Every iteration overwrites `last[3]`, but the value remains 3 with final position 4. Since there is only one key in the dictionary, it is automatically selected. This confirms that repeated overwriting does not affect correctness.

### All distinct cafes

Input:

```
4
8 1 6 2
```

Final last map is `{8:0, 1:1, 6:2, 2:3}`. The minimum index is 0, so cafe 8 is chosen. This shows the solution correctly reduces to finding the earliest occurrence when no repeats exist.
