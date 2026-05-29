---
title: "CF 244A - Dividing Orange"
description: "We are asked to divide an orange consisting of nk segments among k children so that each child receives exactly n segments, each child definitely receives the segment they chose, and no segment is given to more than one child."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 244
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 150 (Div. 2)"
rating: 900
weight: 244
solve_time_s: 193
verified: false
draft: false
---

[CF 244A - Dividing Orange](https://codeforces.com/problemset/problem/244/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 3m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to divide an orange consisting of `n*k` segments among `k` children so that each child receives exactly `n` segments, each child definitely receives the segment they chose, and no segment is given to more than one child. The input provides the total number of segments per child `n`, the number of children `k`, and a list of `k` distinct segment numbers, each corresponding to the segment a child wants.

The output is a list of `n*k` integers partitioned into `k` consecutive groups of `n` numbers, representing the segments assigned to each child. The order within each child’s group does not matter.

The constraints `1 ≤ n, k ≤ 30` mean the total number of segments is at most `900`, so any algorithm that iterates over segments or children a few times is feasible. The low bounds also imply that we do not need to optimize heavily for time, as even a simple greedy approach that picks unused segments one by one will run comfortably.

An edge case arises when children pick segments that are at the extreme ends of the total segments, such as `1` or `n*k`. If one implements the solution by filling children’s segments sequentially without checking which segments are free, it is easy to accidentally assign the same segment to multiple children or miss filling a child’s quota.

## Approaches

A brute-force approach would be to generate all permutations of the segments and then test each assignment to see if it satisfies the constraints. This would be correct but impractical because the number of permutations of `n*k` segments grows factorially. Even for `n=k=10`, there are `100!` permutations, which is infeasible.

The key observation is that we do not need to consider all permutations. Each child already “reserves” one segment. We can fill the remaining `n-1` segments for each child from the set of unassigned segments. Since the problem guarantees that an answer exists and segments can be assigned in any order, a simple greedy approach works: iterate over all segments in increasing order and assign each unassigned segment to the current child until their quota is met. This avoids collisions because we maintain a record of assigned segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n*k)!) | O(n*k) | Too slow |
| Greedy Assignment | O(n*k) | O(n*k) | Accepted |

## Algorithm Walkthrough

1. Read the input values for `n`, `k`, and the list of chosen segments `a`.
2. Initialize a set `used` to track segments already assigned.
3. Initialize a list of lists `children_segments`, each with the segment the child specifically requested. Add this segment to the `used` set.
4. Create an iterator over all possible segment numbers from `1` to `n*k`.
5. For each child, fill their remaining `n-1` segments by iterating over all segment numbers and picking those not in `used`. After assigning a segment, add it to `used`.
6. After all children have `n` segments, flatten the `children_segments` list and print the numbers in the required format.

Why it works: Every child starts with their chosen segment. The greedy assignment ensures no segment is repeated because we always check against `used`. Since the total number of segments is exactly `n*k` and each child receives exactly `n` segments, all segments are used exactly once, fulfilling all constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

used = set(a)
children_segments = [[x] for x in a]

all_segments = iter(range(1, n*k + 1))

for i in range(k):
    while len(children_segments[i]) < n:
        seg = next(all_segments)
        if seg not in used:
            children_segments[i].append(seg)
            used.add(seg)

# Output the segments child by child
for child in children_segments:
    print(" ".join(map(str, child)))
```

The code first reads the input and initializes each child with their desired segment. A set ensures we do not assign the same segment twice. Iterating over all segments guarantees that every child eventually receives exactly `n` segments. Flattening and printing is done in child order to match the required output format.

## Worked Examples

**Sample 1**

Input:

```
2 2
4 1
```

| Step | Child 1 segments | Child 2 segments | Next available segments |
| --- | --- | --- | --- |
| Initial | [4] | [1] | 1,2,3,4 |
| Fill Child 1 | [4,2] | [1] | used = {1,2,4} |
| Fill Child 2 | [4,2] | [1,3] | used = {1,2,3,4} |

Output:

```
4 2
1 3
```

This confirms that each child receives exactly 2 segments, including their chosen one, without duplication.

**Sample 2**

Input:

```
3 3
3 1 9
```

| Step | Child 1 | Child 2 | Child 3 | Next available |
| --- | --- | --- | --- | --- |
| Initial | [3] | [1] | [9] | 1..9 |
| Fill Child 1 | [3,2,4] | [1] | [9] | used={1,2,3,4,9} |
| Fill Child 2 | [3,2,4] | [1,5,6] | [9] | used={1,2,3,4,5,6,9} |
| Fill Child 3 | [3,2,4] | [1,5,6] | [9,7,8] | used={1..9} |

Output:

```
3 2 4
1 5 6
9 7 8
```

The trace confirms that the greedy assignment satisfies all constraints for more children and segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*k) | Each segment is considered at most once; each child is filled exactly to `n` segments. |
| Space | O(n*k) | Storage for assigned segments and the set of used segments. |

Given `n*k ≤ 900`, the algorithm performs at most 900 iterations, well within 2 seconds, and the memory footprint is small, under 1 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    used = set(a)
    children_segments = [[x] for x in a]
    all_segments = iter(range(1, n*k + 1))
    for i in range(k):
        while len(children_segments[i]) < n:
            seg = next(all_segments)
            if seg not in used:
                children_segments[i].append(seg)
                used.add(seg)
    return "\n".join(" ".join(map(str, child)) for child in children_segments)

# provided sample
assert run("2 2\n4 1\n") == "4 2\n1 3" or run("2 2\n4 1\n") == "2 4\n1 3"

# custom: minimum input
assert run("1 1\n1\n") == "1"

# custom: maximum n and k
inp = "30 30\n" + " ".join(map(str, range(1,31))) + "\n"
out = run(inp)
assert all(len(line.split()) == 30 for line in out.split("\n"))

# custom: chosen segments at edges
assert run("3 2\n1 6\n") in ["1 2 3\n6 4 5","1 3 2\n6 4 5","1 2 3\n6 5 4"]

# custom: consecutive chosen segments
assert run("2 3\n2 3 4\n") in ["2 1\n3 5\n4 6"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n1 | 1 | minimum size |
| 30 30 + 1..30 | Each line has 30 numbers | maximum size, all children filled |
| 3 2\n1 6 | 1 2 3\n6 4 5 | chosen segments at boundaries |
| 2 3\n2 3 4 | 2 1\n3 5\n4 6 | consecutive chosen segments |

## Edge Cases

For a single child and one segment `1 1\n1`, the algorithm initializes the child with the chosen segment and the while loop is skipped, producing `[1]` correctly.

For maximum-size input `n=k=30` with first 30 segments chosen by children, the algorithm sequentially fills the remaining 29 segments per child from unassigned numbers 31 to 900. The invariant that no segment is reused holds because each newly assigned segment is checked against the `used` set. This confirms that the algorithm scales to upper bounds without violating the problem’s constraints.
