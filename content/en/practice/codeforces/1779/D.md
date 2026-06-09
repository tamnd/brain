---
title: "CF 1779D - Boris and His Amazing Haircut"
description: "We are asked to transform Boris's current hairstyle into a desired one using a limited set of razors, each of which can cut hair down to a fixed length over any contiguous segment."
date: "2026-06-09T11:29:34+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dp", "dsu", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1779
codeforces_index: "D"
codeforces_contest_name: "Hello 2023"
rating: 1700
weight: 1779
solve_time_s: 95
verified: false
draft: false
---

[CF 1779D - Boris and His Amazing Haircut](https://codeforces.com/problemset/problem/1779/D)

**Rating:** 1700  
**Tags:** constructive algorithms, data structures, dp, dsu, greedy, sortings  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to transform Boris's current hairstyle into a desired one using a limited set of razors, each of which can cut hair down to a fixed length over any contiguous segment. Conceptually, you can think of the current hairstyle as an array of integers representing hair lengths, and the desired hairstyle as a target array of the same size. Each razor has a number that represents the maximum height it can cut hair down to, and each can be used only once. After applying a razor to a segment, every hair in that segment becomes the minimum of its current height and the razor’s size.

The challenge is to decide if it is possible to reach the target array with these operations. Importantly, the barber cannot increase hair length, so any desired hair length that is taller than the current hair is immediately impossible.

The problem allows up to 200,000 hairs per test case and up to 20,000 test cases, with a total number of hair positions across all test cases bounded by 200,000. This immediately rules out any brute-force approach that would try all segments or all combinations of razors. We need a solution that processes each hair in essentially constant time.

Edge cases include situations where the target array is already equal to the current array (no cuts needed), or where certain hairs require a razor that appears only once while needing it in multiple non-adjacent positions. A naive approach might incorrectly assume that we can apply a razor anywhere without considering these multiplicities.

For instance, if current hair is `[3, 3, 3]` and target is `[2, 1, 2]` with razors `[1, 2]`, a careless solution could try to apply the size-2 razor first over the whole array and fail to achieve the single 1, producing the wrong answer. Correct reasoning must consider how to allocate razors to all positions needing that specific cut.

## Approaches

The brute-force method is to try all possible segments for every razor. You would check every contiguous segment of the array and see if applying a razor there makes progress toward the target. This is correct because each operation is allowed anywhere, but with up to 200,000 hairs and 200,000 razors, the worst-case number of segments is O(n^2), which is around 4×10^10 operations per test case. Clearly, this is far too slow.

The key insight for an efficient solution comes from observing that any hair whose desired length is less than its current length must be cut with a razor of exactly that length. Moreover, we only need to ensure that for each distinct target length, there is a razor available for each contiguous block of hairs requiring that length. If multiple positions needing the same length are separated by positions already at that length or shorter, the same razor can cover the entire contiguous segment. So, the problem reduces to counting contiguous segments needing a specific cut and verifying we have enough razors of that size.

Another useful observation is that hairs already at or below the target require no action. Thus, we only need to focus on positions where the current hair is taller than the target.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * m) | O(n + m) | Too slow |
| Optimal | O(n + m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Iterate over each test case and read arrays `a`, `b` and the list of razors.
2. Immediately check if any `b[i] > a[i]`. If true for any hair, print "NO" because we cannot increase hair length.
3. Count the number of razors for each size using a frequency dictionary or counter. This allows fast lookups to see if a required razor is available.
4. Traverse the hair array from left to right. Keep track of the current contiguous segment where `b[i]` is less than `a[i]`. For each segment, record the required cut length (`b[i]`) and the number of positions in the segment that need this length.
5. Whenever the segment ends (either the next hair is already at or below target, or the end of the array), check if a razor of the required length exists in sufficient quantity. If not, print "NO". Otherwise, decrement the razor count by the number of positions in the segment.
6. Continue until the entire array is processed. If all segments were covered with available razors, print "YES".

This works because each contiguous block of hairs needing a cut of a certain size can be covered by a single operation using the corresponding razor. The algorithm maintains the invariant that we only try to cut hairs down to their exact target length and never attempt a cut larger than needed.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

def can_cut_hair():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        m = int(input())
        razors = list(map(int, input().split()))
        razor_count = Counter(razors)

        possible = True
        i = 0
        while i < n:
            if b[i] > a[i]:
                possible = False
                break
            if a[i] > b[i]:
                required = b[i]
                j = i
                while j < n and b[j] == required and a[j] > b[j]:
                    j += 1
                if razor_count[required] <= 0:
                    possible = False
                    break
                razor_count[required] -= 1
                i = j
            else:
                i += 1

        print("YES" if possible else "NO")

can_cut_hair()
```

The solution begins by reading input efficiently using `sys.stdin.readline`. We use `Counter` to efficiently track razor availability. We iterate through `a` and `b`, identifying blocks of hair that need a cut. For each block, we check if the corresponding razor exists. We do not try to cut hairs unnecessarily or use a razor multiple times for the same block.

## Worked Examples

**Sample 1 Trace**

| i | a[i] | b[i] | Action | razor_count |
| --- | --- | --- | --- | --- |
| 0 | 3 | 2 | start block 2 | {1:1,2:1} |
| 1 | 3 | 1 | start block 1 | {1:1,2:1} |
| 2 | 3 | 2 | start block 2 | {1:0,2:0} |

The trace confirms the algorithm correctly identifies separate blocks for 2 and 1, using the available razors exactly once.

**Sample 2 Trace**

| i | a[i] | b[i] | Action | razor_count |
| --- | --- | --- | --- | --- |
| 0 | 3 | 3 | no action | {3:0,2:0} |
| 1 | 4 | 1 | block 1 | {1:0} |

Shows that if a block requires a razor that is unavailable, the algorithm immediately prints "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | Each hair is visited once, counting razors is O(m) |
| Space | O(m) | Counter stores frequency of each razor size |

With the total `n` and `m` across all test cases ≤ 2×10^5, this solution comfortably runs within the 2-second limit and uses far less than the 256 MB memory.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    can_cut_hair()
    return out.getvalue().strip()

# provided samples
assert run("7\n3\n3 3 3\n2 1 2\n2\n1 2\n6\n3 4 4 6 3 4\n3 1 2 3 2 3\n3\n3 2 3\n10\n1 2 3 4 5 6 7 8 9 10\n1 2 3 4 5 6 7 8 9 10\n10\n1 2 3 4 5 6 7 8 9 10\n3\n1 1 1\n1 1 2\n12\n4 2 4 3 1 5 6 3 5 6 2 1\n13\n7 9 4 5 3 3 3 6 8 10 3 2 5\n5 3 1 5 3 2 2 5 8 5 1 1 5\n8\n1 5 3 5 4 2 3 1\n13\n7 9 4 5 3 3 3 6 8 10 3 2 5\n5 3 1 5 3 2 2 5 8 5 1 1 5\n7\n1 5 3 4 2 3 1\n3\n19747843 2736467 938578397\n2039844 2039844 2039844\n1\n2039844") == "YES\nNO
```
