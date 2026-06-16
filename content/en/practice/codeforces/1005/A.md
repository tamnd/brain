---
title: "CF 1005A - Tanya and Stairways"
description: "We are given a single sequence of integers that represents what Tanya says while climbing stairs in a building. Each time she starts a new stairway, she always begins counting from 1 and increases by 1 for each step until she reaches the last step of that stairway."
date: "2026-06-16T23:20:36+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1005
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 496 (Div. 3)"
rating: 800
weight: 1005
solve_time_s: 181
verified: true
draft: false
---

[CF 1005A - Tanya and Stairways](https://codeforces.com/problemset/problem/1005/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 3m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single sequence of integers that represents what Tanya says while climbing stairs in a building. Each time she starts a new stairway, she always begins counting from 1 and increases by 1 for each step until she reaches the last step of that stairway.

So the sequence is not arbitrary. It is formed by concatenating several consecutive segments, where each segment is a prefix of the natural numbers starting at 1 and ending at some value x. Our task is to split the sequence back into those segments and report how many segments there are and the length of each segment.

The input size is at most 1000 numbers. This immediately tells us that any solution that scans the array a constant number of times or even nested linear scans is easily fast enough. There is no need for preprocessing, hashing, or advanced data structures.

The only subtlety lies in correctly identifying where one stairway ends and the next begins. A naive mistake is to assume that every time the sequence value decreases, or every time we see a 1, we start a new segment without carefully handling boundaries. For example, in a sequence like `1 2 3 1 2 3 4`, the restart at 1 is obvious, but in more general sequences, the break always happens exactly when the sequence stops being consecutive increasing-by-one starting from 1.

A typical incorrect approach is to only check for `a[i] == 1` as a boundary marker. This works here because the problem guarantees validity, but a careless implementation might miss that the last element of a segment is not necessarily followed by 1; instead, the segment ends when the next value is 1 or when we reach the end of the array.

The correct interpretation is that each stairway is a maximal contiguous segment where values are exactly `1, 2, 3, ..., k`.

## Approaches

A brute-force way to think about this is to try every possible partition of the sequence into valid stairways and verify each one. At each potential cut position, we would check whether the segment from that start index forms a valid sequence starting from 1 and increasing by 1. In the worst case, we might repeatedly re-scan parts of the array for validation, leading to quadratic or even cubic behavior depending on how the checks are structured. While this is still within limits for n up to 1000, it is unnecessary and conceptually heavier than needed.

The key observation is that we do not need to guess where segments end. A segment must end exactly when the current value equals the length of the segment so far, because valid stairways always look like `1, 2, ..., length`. So we can greedily extend a segment until we have just seen the number equal to the current segment size, then close it.

This reduces the problem to a single linear pass, maintaining the current expected next value in the segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Partition Checking | O(n²) | O(n) | Too slow / unnecessary |
| Greedy single pass | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start scanning the array from left to right, treating each new segment as a fresh stairway.

We know every stairway must begin with 1, so we expect the first element of any segment to be 1.
2. When we begin a new segment, set a counter `expected = 1` and record that this segment has started.
3. Move forward in the array, checking each value.

If the current value matches `expected`, we are still inside a valid stairway, so we increment `expected` by 1.
4. If at any point we reach a position where `expected` becomes 1 again after finishing a segment, that indicates the start of a new stairway.
5. A segment ends exactly when we have consumed a full prefix from 1 up to some k, which corresponds to the moment we are about to start a new 1 or we reach the end of the array.
6. Store the length of each segment as we finish it.

### Why it works

Each valid stairway is uniquely determined by its starting point and must strictly follow increasing consecutive integers starting from 1. Because the input is guaranteed valid, there is no ambiguity in segmentation: once we see a 1, a new segment must begin, and between two consecutive 1s the sequence must form a continuous increasing run. This structure ensures that greedy segmentation never needs backtracking or guessing, since any deviation from increasing-by-one would contradict validity.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

segments = []
i = 0

while i < n:
    expected = 1
    length = 0
    
    while i < n and a[i] == expected:
        length += 1
        expected += 1
        i += 1
    
    segments.append(length)

print(len(segments))
print(*segments)
```

The code scans the array once. The outer loop advances between stairways, and the inner loop consumes exactly one valid stairway by matching the increasing sequence starting from 1. The `expected` variable enforces the structure of a valid stairway, and `length` records how many steps it contained.

A subtle point is that we never explicitly search for the next 1. Instead, the inner loop naturally stops when the sequence breaks, which can only happen at the boundary between stairways because the input is guaranteed valid.

## Worked Examples

### Example 1

Input:

```
7
1 2 3 1 2 3 4
```

| i | a[i] | expected | length | segment ended |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | no |
| 1 | 2 | 2 | 2 | no |
| 2 | 3 | 3 | 3 | yes |
| 3 | 1 | 1 | 1 | no |
| 4 | 2 | 2 | 2 | no |
| 5 | 3 | 3 | 3 | no |
| 6 | 4 | 4 | 4 | yes |

We obtain two segments of lengths 3 and 4. The trace shows that each time `expected` completes a full run, a stairway ends exactly at that point.

### Example 2

Input:

```
5
1 2 1 1 2
```

| i | a[i] | expected | length | segment ended |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | no |
| 1 | 2 | 2 | 2 | yes |
| 2 | 1 | 1 | 1 | yes |
| 3 | 1 | 1 | 1 | no |
| 4 | 2 | 2 | 2 | yes |

Output is `3` segments with lengths `2 1 2`.

This trace highlights that single-element stairways are valid and correctly handled when the sequence restarts immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is visited exactly once as part of a segment scan |
| Space | O(1) | Only counters and a small list of segment lengths are used |

The input size is at most 1000, so a linear scan is far below the time limit. Memory usage is constant aside from the output storage, which is unavoidable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    segments = []
    i = 0

    while i < n:
        expected = 1
        length = 0
        while i < n and a[i] == expected:
            length += 1
            expected += 1
            i += 1
        segments.append(length)

    return str(len(segments)) + "\n" + " ".join(map(str, segments))

# provided sample
assert run("7\n1 2 3 1 2 3 4\n") == "2\n3 4"

# single stairway
assert run("3\n1 2 3\n") == "1\n3"

# multiple single-step stairways
assert run("3\n1 1 1\n") == "3\n1 1 1"

# alternating short stairs
assert run("5\n1 2 1 2 3\n") == "2\n2 3"

# maximum length single staircase
assert run("1\n1\n") == "1\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 | 1 / 3 | single full stairway |
| 1 1 1 | 3 / 1 1 1 | consecutive restarts |
| 1 2 1 2 3 | 2 / 2 3 | mixed segmentation |
| 1 | 1 / 1 | minimum size |

## Edge Cases

One edge case is when the entire sequence consists of multiple independent stairways of length 1, such as `1 1 1 1`. The algorithm starts a segment at each `1`, immediately matches `expected = 1`, consumes a single element, and closes the segment. This produces four segments of length 1, matching the intended interpretation.

Another edge case is a single long stairway like `1 2 3 4 5`. Here, the inner loop never breaks early, `expected` increases smoothly until the end, and exactly one segment is recorded with correct full length.
