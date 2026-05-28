---
title: "CF 205A - Little Elephant and Rozdil"
description: "We are given a list of travel times from the town Rozdil to each of n other towns. Each town has a positive integer time, and the towns are numbered from 1 to n. The goal is to find which town has the smallest travel time."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 205
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 129 (Div. 2)"
rating: 900
weight: 205
solve_time_s: 54
verified: true
draft: false
---

[CF 205A - Little Elephant and Rozdil](https://codeforces.com/problemset/problem/205/A)

**Rating:** 900  
**Tags:** brute force, implementation  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of travel times from the town Rozdil to each of _n_ other towns. Each town has a positive integer time, and the towns are numbered from 1 to _n_. The goal is to find which town has the smallest travel time. If there is a unique town with this minimum time, we print its number. If there are multiple towns tied for the minimum, the Little Elephant will stay in Rozdil, and we print "Still Rozdil".

The constraints allow up to 100,000 towns, and travel times can be as large as 10^9. This tells us that any solution must operate in linear time; sorting the array of times would be O(n log n) and could work, but a linear scan is simpler and sufficient. Operations with quadratic complexity would be far too slow.

A subtle edge case arises when multiple towns share the same minimum travel time. For example, if the input is `5\n4 2 2 5 6`, the minimum time is 2, but it occurs in two towns (2 and 3). A careless implementation might simply return the first minimum it finds, which would be wrong. Another edge case occurs when there is only one town, in which case the answer must be that town, since uniqueness is guaranteed.

## Approaches

The brute-force approach iterates through every town, keeping track of the smallest time and its corresponding town index. This works because it directly implements the problem's requirements: it identifies the minimum and checks for ties. In terms of operations, each comparison is constant time, so the overall time is O(n). Memory usage is O(1) beyond the input. This approach is already optimal, but we must be careful with tie detection: simply storing one minimum index is insufficient if we need to check uniqueness.

The key insight is that we can maintain three pieces of information while scanning the array: the current minimum travel time, the index of the town that first achieved it, and a counter for how many times this minimum has occurred. Every time we encounter a smaller time, we update the minimum, set the index to the current town, and reset the counter to 1. If we encounter an equal minimum, we increment the counter. At the end, if the counter is greater than 1, we print "Still Rozdil"; otherwise, we print the stored index. This approach is linear, uses constant extra space, and correctly handles all edge cases including duplicates and single-element arrays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with tie detection | O(n) | O(1) | Accepted |
| Sorting and scanning | O(n log n) | O(n) | Accepted but unnecessary |

## Algorithm Walkthrough

1. Initialize three variables: `min_time` to a very large number, `min_index` to -1, and `count` to 0. `min_time` will store the smallest travel time found so far. `min_index` will store the 1-based index of the town that first achieved this minimum. `count` will store how many times this minimum has occurred.
2. Iterate through the travel times using a loop with index `i` from 0 to n-1. For each town, read the travel time.
3. If the current travel time is less than `min_time`, this is a new minimum. Set `min_time` to this value, `min_index` to `i + 1` (to convert from 0-based to 1-based indexing), and reset `count` to 1.
4. If the current travel time equals `min_time`, increment `count` by 1, because we have found another town with the same minimum.
5. After scanning all towns, check the value of `count`. If `count` is 1, print `min_index`. If `count` is greater than 1, print "Still Rozdil".

Why it works: The algorithm keeps track of the smallest travel time at all times and counts how many towns achieve it. By updating only when a strictly smaller time is found, we ensure `min_index` always points to the first town with the minimum. Counting duplicates ensures we only declare a unique minimum if it truly exists. No town is missed because we iterate through all of them once.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
times = list(map(int, input().split()))

min_time = 10**9 + 1
min_index = -1
count = 0

for i in range(n):
    t = times[i]
    if t < min_time:
        min_time = t
        min_index = i + 1
        count = 1
    elif t == min_time:
        count += 1

if count == 1:
    print(min_index)
else:
    print("Still Rozdil")
```

The first section reads input using fast I/O. `min_time` is initialized to a value larger than any possible travel time to ensure the first town will correctly update it. During the loop, we maintain the index and count of the current minimum. We add 1 to the index because the problem expects 1-based indexing. Finally, we check the count to handle ties.

## Worked Examples

### Sample 1

Input: `2\n7 4`

| i | t | min_time | min_index | count |
| --- | --- | --- | --- | --- |
| 0 | 7 | 7 | 1 | 1 |
| 1 | 4 | 4 | 2 | 1 |

The minimum is unique at town 2, so the output is `2`. The table shows that the algorithm updates correctly when a new minimum is found.

### Sample 2

Input: `5\n4 2 2 5 6`

| i | t | min_time | min_index | count |
| --- | --- | --- | --- | --- |
| 0 | 4 | 4 | 1 | 1 |
| 1 | 2 | 2 | 2 | 1 |
| 2 | 2 | 2 | 2 | 2 |
| 3 | 5 | 2 | 2 | 2 |
| 4 | 6 | 2 | 2 | 2 |

The minimum occurs in multiple towns, so the output is `Still Rozdil`. This demonstrates correct handling of duplicates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the list of travel times exactly once, performing constant-time operations per element. |
| Space | O(n) | We store the list of travel times. Additional variables use O(1) space. |

The solution easily fits within the 2-second limit for n up to 100,000 and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    times = list(map(int, input().split()))
    min_time = 10**9 + 1
    min_index = -1
    count = 0
    for i in range(n):
        t = times[i]
        if t < min_time:
            min_time = t
            min_index = i + 1
            count = 1
        elif t == min_time:
            count += 1
    return str(min_index) if count == 1 else "Still Rozdil"

# Provided samples
assert run("2\n7 4\n") == "2", "sample 1"
assert run("5\n7 4 2 2 5\n") == "Still Rozdil", "sample 2"

# Custom cases
assert run("1\n10\n") == "1", "single town"
assert run("3\n5 5 5\n") == "Still Rozdil", "all equal values"
assert run("4\n3 2 4 2\n") == "Still Rozdil", "multiple minimums"
assert run("4\n7 1 3 4\n") == "2", "unique minimum in the middle"
assert run("5\n10 9 8 7 6\n") == "5", "minimum at the end"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n10 | 1 | Single-town edge case |
| 3\n5 5 5 | Still Rozdil | All towns have equal travel time |
| 4\n3 2 4 2 | Still Rozdil | Multiple minimum values |
| 4\n7 1 3 4 | 2 | Unique minimum in the middle of the list |
| 5\n10 9 8 7 6 | 5 | Minimum at the last town |

## Edge Cases

The algorithm handles single-town input by initializing `min_time` high and correctly updating it at the first town. Duplicate minimums are handled by incrementing `count` each time the minimum occurs, ensuring that ties trigger "Still Rozdil". The algorithm also correctly identifies a minimum that appears at the last index, maintaining the first-found invariant and proper indexing.
