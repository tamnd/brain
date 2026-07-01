---
title: "CF 104312E - Attack on Titans"
description: "We are given three independent walls, each described as an array of section heights. Each array contains $n$ integers, where each integer represents the height of a segment in that wall."
date: "2026-07-01T19:52:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104312
codeforces_index: "E"
codeforces_contest_name: "UTPC Spring 2023 Contest (HS)"
rating: 0
weight: 104312
solve_time_s: 60
verified: true
draft: false
---

[CF 104312E - Attack on Titans](https://codeforces.com/problemset/problem/104312/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three independent walls, each described as an array of section heights. Each array contains $n$ integers, where each integer represents the height of a segment in that wall. The goal is not to match positions across walls, but only to find a height value that appears in all three arrays. Among all such shared heights, we must return the largest one. If no height is shared by all three walls, the answer is $-1$.

The key detail is that we are comparing values, not indices. A height is valid if it appears at least once in Wall Maria, at least once in Wall Rose, and at least once in Wall Sina.

The constraint $n \le 10^5$ implies that each wall can contain up to one hundred thousand values, and there are three such arrays. A direct quadratic or cubic comparison across arrays would lead to roughly $10^{10}$ operations in the worst case, which is far beyond what a 2-second limit can handle. This immediately rules out pairwise scanning between all elements of the three arrays.

The values themselves are bounded by $10^5$, which is an important structural hint. It suggests that frequency counting or presence marking over a fixed domain is likely feasible.

A few edge cases matter in practice. If all values in all arrays are distinct, then there is no overlap and the output must be $-1$. If all arrays contain identical values, the answer is simply the maximum value present. Another subtle case arises when duplicates exist within arrays; duplicates should not affect correctness because we only care about existence, not frequency.

## Approaches

The brute-force idea is straightforward. For every value in the first wall, we check whether it appears in the second wall and the third wall. This can be implemented using nested loops or linear searches.

If we do this naively, for each of the $n$ elements in the first array, we may scan up to $n$ elements in the second and another $n$ in the third. This leads to $O(n^3)$ in the worst case if implemented with raw loops, or $O(n^2)$ if we pre-check membership using lists and linear scans. Even $O(n^2)$ translates to $10^{10}$ operations, which is not viable.

The key observation is that we do not need to compare elements pairwise. We only need to know whether a value exists in each array. This transforms the problem into a set intersection problem. Once each array is converted into a membership structure, checking whether a value appears in all three becomes constant time.

Since values are bounded by $10^5$, we can also use a boolean frequency array or a hash set. After marking presence for each wall, we scan through the possible value range and select the largest value that is present in all three.

This reduces the problem from repeated searching to a single linear sweep over the value domain.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ to $O(n^3)$ | $O(1)$ | Too slow |
| Presence arrays / sets | $O(n + V)$ | $O(V)$ | Accepted |

Here $V = 10^5$, the maximum possible value.

## Algorithm Walkthrough

1. Create three boolean arrays (or sets) representing which values appear in each wall. This step converts raw lists into fast membership structures so we can answer existence queries in constant time.
2. For each height in Wall Maria, mark it as present in the first structure. Repeated values do not matter because we only care about existence.
3. Repeat the same marking process for Wall Rose and Wall Sina, filling the second and third structures respectively.
4. Iterate through all possible heights from $1$ to $10^5$, checking whether a value is marked present in all three structures. This works because all valid heights must lie within the given bounds.
5. Track the maximum value that satisfies presence in all three arrays. Since we scan in increasing order, we can simply overwrite the answer whenever we find a valid value.
6. After the scan, if no value was found, return $-1$, otherwise return the recorded maximum.

### Why it works

The algorithm relies on the fact that membership in each wall is independent and orderless. By converting each wall into a set of present values, we preserve exactly the information needed for the problem and discard everything irrelevant, such as ordering and duplicates. The final scan checks each candidate height against a correct representation of existence in all three walls, ensuring that every reported value truly appears in all arrays. Since we evaluate all possible heights in the allowed range, no valid answer can be missed, and selecting the maximum among them guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    m = list(map(int, input().split()))
    r = list(map(int, input().split()))
    s = list(map(int, input().split()))
    
    MAXV = 100000
    
    in_m = [False] * (MAXV + 1)
    in_r = [False] * (MAXV + 1)
    in_s = [False] * (MAXV + 1)
    
    for x in m:
        in_m[x] = True
    for x in r:
        in_r[x] = True
    for x in s:
        in_s[x] = True
    
    ans = -1
    for v in range(1, MAXV + 1):
        if in_m[v] and in_r[v] and in_s[v]:
            ans = v
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first builds three presence tables, one per wall. Each table records whether a height exists in that wall. This avoids repeated scanning and ensures constant-time membership checks.

The final loop scans all possible heights in increasing order. Every time a height is found in all three arrays, it updates the answer. Because we scan upward, the last recorded value is the maximum valid height.

A subtle point is the fixed range $1 \le h \le 10^5$. This allows us to safely allocate arrays of size $100001$ without worrying about dynamic bounds.

## Worked Examples

### Example 1

Input:

```
n = 5
Maria = [1, 2, 3, 8, 5]
Rose  = [5, 6, 7, 8, 9]
Sina  = [8, 12, 14, 19, 12]
```

| v | in Maria | in Rose | in Sina | ans |
| --- | --- | --- | --- | --- |
| 1 | T | F | F | -1 |
| 2 | T | F | F | -1 |
| 3 | T | F | F | -1 |
| 5 | T | T | F | -1 |
| 8 | T | T | T | 8 |

The scan shows that only value 8 appears in all three arrays, so it becomes the final answer.

### Example 2

Input:

```
n = 4
Maria = [10, 20, 30, 40]
Rose  = [15, 20, 35, 45]
Sina  = [5, 25, 20, 60]
```

| v | in Maria | in Rose | in Sina | ans |
| --- | --- | --- | --- | --- |
| 20 | T | T | T | 20 |

Only 20 is common across all arrays, so it is returned directly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + V)$ | Each array is processed once, then we scan the full value range |
| Space | $O(V)$ | Three boolean arrays of size up to $10^5$ |

The constraints allow up to $n = 10^5$, and $V = 10^5$, so the solution runs comfortably within limits. The operations are linear and memory usage is fixed and small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    input = sys.stdin.readline
    
    n = int(input())
    m = list(map(int, input().split()))
    r = list(map(int, input().split()))
    s = list(map(int, input().split()))
    
    MAXV = 100000
    in_m = [False] * (MAXV + 1)
    in_r = [False] * (MAXV + 1)
    in_s = [False] * (MAXV + 1)
    
    for x in m:
        in_m[x] = True
    for x in r:
        in_r[x] = True
    for x in s:
        in_s[x] = True
    
    ans = -1
    for v in range(1, MAXV + 1):
        if in_m[v] and in_r[v] and in_s[v]:
            ans = v
    
    return str(ans)

# provided sample
assert run("""5
1 2 3 8 5
5 6 7 8 9
8 12 14 19 12
""") == "8"

# custom 1: no intersection
assert run("""3
1 2 3
4 5 6
7 8 9
""") == "-1"

# custom 2: all equal
assert run("""3
1 2 3
1 2 3
1 2 3
""") == "3"

# custom 3: single element
assert run("""1
5
5
5
""") == "5"

# custom 4: multiple common, choose max
assert run("""6
1 2 3 4 5 6
2 3 4 5 6 7
0 2 4 6 8 10
""") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no overlap | -1 | absence handling |
| identical arrays | max value | correct max selection |
| single element | value | minimal input correctness |
| multiple overlap | 6 | correct maximum intersection |

## Edge Cases

A case where all arrays contain disjoint values demonstrates the algorithm’s correct handling of absence. For example:

```
Maria = [1,2], Rose = [3,4], Sina = [5,6]
```

During the scan, no index $v$ satisfies all three boolean checks, so `ans` remains $-1$, which is correctly returned.

A second case is when duplicates dominate:

```
Maria = [7,7,7], Rose = [7,7], Sina = [7]
```

Even though counts differ, the presence arrays mark only existence. At $v = 7$, all three flags are true, so the answer is correctly identified as 7.
