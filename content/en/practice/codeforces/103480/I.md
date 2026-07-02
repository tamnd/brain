---
title: "CF 103480I - \u597d\u60f3\u542c\u8086\u5b9d\u5531\u6b4c\u554a"
description: "We are given a collection of songs, where each song has a unique popularity value and a unique name. The popularity value acts like a strict ranking key: no two songs share the same score, and higher values mean a song is more desired."
date: "2026-07-03T06:32:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103480
codeforces_index: "I"
codeforces_contest_name: "The 4th Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 103480
solve_time_s: 46
verified: true
draft: false
---

[CF 103480I - \u597d\u60f3\u542c\u8086\u5b9d\u5531\u6b4c\u554a](https://codeforces.com/problemset/problem/103480/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of songs, where each song has a unique popularity value and a unique name. The popularity value acts like a strict ranking key: no two songs share the same score, and higher values mean a song is more desired.

The task is to imagine all songs sorted in descending order of popularity. Some number of the most popular songs have already been taken by other users. We are told exactly how many of the top choices, say k of them, are already gone. Our job is to determine the next best available song, meaning the song that would appear in position k + 1 in that sorted order.

The input size can go up to 100,000 songs. This immediately rules out any approach that repeatedly scans the list in linear fashion for each removal or uses repeated sorting inside loops. An O(n log n) solution is acceptable, but anything quadratic will fail under a 1 second limit.

A subtle edge case arises when k is zero. In this case, no songs are taken, so the answer is simply the globally most popular song. Another corner case is when k is n − 1, where only one song remains valid and it must be returned regardless of position.

A naive mistake would be to sort in ascending order and accidentally pick the k-th smallest instead of the k-th largest. For example, if we interpret “most desired” incorrectly, we would reverse the ranking and return the wrong song consistently even though sorting is otherwise correct.

## Approaches

The most straightforward idea is to explicitly sort all songs by their popularity value in descending order. Once sorted, we directly index the k-th position.

This works because sorting gives us a global ordering of all items according to exactly the same comparison rule that defines preference. After sorting, removing the first k items is conceptually equivalent to ignoring them and taking the next one.

A brute-force alternative would be to repeatedly scan the list to find the current maximum, remove it, and repeat this k + 1 times. Each scan costs O(n), and doing it k times leads to O(nk), which in the worst case becomes O(n²). With n up to 10⁵, this is far beyond feasible limits.

The key observation is that we do not need dynamic removal. We only need the final ranking once. That turns the problem into a static ordering problem, which is exactly what sorting solves efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated maximum extraction | O(n²) | O(1) | Too slow |
| Sort by value | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all songs into a list as pairs of (popularity, name). This preserves both the ranking key and the identifier we must output.
2. Sort the list in descending order of popularity. This creates a global ranking where the first element is the most desired song, and each next element is strictly less desired than the previous one. The uniqueness of popularity guarantees there are no ties, so the order is deterministic.
3. Read the integer k, which represents how many top-ranked songs are already taken.
4. Directly access the element at index k in the sorted list. This corresponds to the (k + 1)-th most popular song in 1-based ranking.
5. Output the name associated with that element.

### Why it works

After sorting, the list is a total order of songs by decreasing popularity. Because all popularity values are distinct, this ordering is strict and stable. Removing the top k elements does not change the relative order of the remaining elements, so the first remaining element is exactly the k-th index in zero-based indexing. The algorithm never depends on intermediate updates or deletions, so no state corruption or reordering can occur.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    songs = []
    
    for _ in range(n):
        w, s = input().split()
        w = int(w)
        songs.append((w, s))
    
    k = int(input())
    
    songs.sort(reverse=True)
    
    print(songs[k][1])

if __name__ == "__main__":
    solve()
```

The core of the implementation is the sort call, which orders tuples by the first element in descending order due to `reverse=True`. Since Python compares tuples lexicographically, the name is only used as a secondary key, but it does not matter because weights are guaranteed unique.

The direct indexing `songs[k]` is safe because k is guaranteed to satisfy 0 ≤ k < n. No boundary checks are required beyond trusting the input constraints.

## Worked Examples

### Example 1

Input:

```
3
flos 1
Yellow 3
Starduster 9
1
```

Sorted order becomes:

```
(9, Starduster)
(3, Yellow)
(1, flos)
```

| Step | Action | State |
| --- | --- | --- |
| Read input | store songs | [(1, flos), (3, Yellow), (9, Starduster)] |
| Sort | descending | [(9, Starduster), (3, Yellow), (1, flos)] |
| k = 1 | pick index 1 | (3, Yellow) |

Output:

```
Yellow
```

This confirms that after removing the top song, the second most popular is correctly chosen.

### Example 2

Input:

```
4
A 5
B 2
C 10
D 7
0
```

Sorted order:

```
(10, C), (7, D), (5, A), (2, B)
```

| Step | Action | State |
| --- | --- | --- |
| Read input | store songs | [(5,A),(2,B),(10,C),(7,D)] |
| Sort | descending | [(10,C),(7,D),(5,A),(2,B)] |
| k = 0 | pick index 0 | (10, C) |

Output:

```
C
```

This confirms the edge case where no songs are removed: we directly return the maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | dominated by sorting n songs by popularity |
| Space | O(n) | storing all song pairs |

The constraints allow up to 100,000 songs, and sorting at this scale is well within limits in Python. Memory usage is linear in the number of stored pairs and comfortably under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(input())
    songs = []
    for _ in range(n):
        w, s = input().split()
        songs.append((int(w), s))
    k = int(input())
    
    songs.sort(reverse=True)
    return songs[k][1]

# provided sample style cases
assert run("""3
1 flos
3 Yellow
9 Starduster
1
""") == "Yellow"

assert run("""1
1000000000 Kawakiwoameku
0
""") == "Kawakiwoameku"

# custom cases
assert run("""2
1 A
2 B
0
""") == "B"

assert run("""2
1 A
2 B
1
""") == "A"

assert run("""5
10 A
20 B
30 C
40 D
50 E
4
""") == "A"

assert run("""3
5 X
1 Y
3 Z
2
""") == "Y"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 songs, k=0 | highest song | maximum selection correctness |
| 2 songs, k=1 | lowest song | boundary indexing correctness |
| 5 increasing values | last element | full ordering correctness |
| shuffled values, k=2 | middle element | general ranking correctness |

## Edge Cases

When k is zero, the algorithm directly returns the first element after sorting. For example, with input:

```
3
5 A
2 B
9 C
0
```

After sorting, we get (9, C), (5, A), (2, B). Index 0 is C, which is correct since no songs are considered taken.

When k equals n − 1, only the smallest element remains. For input:

```
3
5 A
2 B
9 C
2
```

Sorted list is (9, C), (5, A), (2, B). Index 2 is (2, B), which is the last remaining choice after removing the top two songs.

Because the algorithm never modifies the list after sorting, these edge cases do not require special handling. The same indexing rule consistently applies across all valid values of k.
