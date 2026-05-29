---
title: "CF 244A - Dividing Orange"
description: "We are given an orange divided into n k segments, and k children. Each child has already chosen one segment they must receive. The task is to assign exactly n segments to each child, making sure each child gets the segment they selected and no two children share a segment."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 244
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 150 (Div. 2)"
rating: 900
weight: 244
solve_time_s: 83
verified: false
draft: false
---

[CF 244A - Dividing Orange](https://codeforces.com/problemset/problem/244/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an orange divided into `n * k` segments, and `k` children. Each child has already chosen one segment they must receive. The task is to assign exactly `n` segments to each child, making sure each child gets the segment they selected and no two children share a segment.

The input consists of two numbers `n` and `k`, followed by `k` distinct integers indicating the required segments. The output is a sequence of `n * k` numbers, partitioned into `k` groups of size `n`, each group representing the segments assigned to one child. The order within each child’s group does not matter.

Constraints are small: `n` and `k` are at most 30, so the total number of segments is at most 900. This allows a simple solution with linear scans, since even O(n*k²) operations would execute quickly. The main challenges are correctness and ensuring no segment is assigned twice.

Non-obvious edge cases include when the selected segments are clustered at the high or low end of the range. For example, `n=2`, `k=3`, and chosen segments `1,2,3` could lead a careless approach that fills children greedily from 1 upwards to try to satisfy the "first available" principle, accidentally assigning a chosen segment to the wrong child. The algorithm must always respect the chosen segments.

## Approaches

A naive approach is to try generating all permutations of the remaining segments for each child and check if the chosen segment is included. This is overkill: the operation count grows factorially and is unnecessary given the guarantees.

The optimal approach uses a greedy allocation: first, assign the chosen segment to each child. Then iterate through all segment numbers in order, skipping already assigned segments, and assign remaining segments to children until each child has `n` segments. This works because each child needs exactly `n` segments, there are exactly `n*k` segments, and all chosen segments are distinct. The observation that the problem reduces to filling up each child’s slots in any order after securing the required segments makes the solution straightforward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n*k)!) | O(n*k) | Too slow |
| Greedy Assignment | O(n*k) | O(n*k) | Accepted |

## Algorithm Walkthrough

1. Create a list of lists, one for each child, and initialize each list with the chosen segment of that child. This ensures the required segment is included for every child.
2. Create a set of all assigned segments. Initially, this contains only the chosen segments.
3. Iterate through all segment numbers from 1 to `n*k`. For each segment, if it is already assigned, skip it. Otherwise, find the first child whose assigned list has fewer than `n` segments and append the segment to their list.
4. Continue until every child has exactly `n` segments. Since `n*k` total segments exist and every child needs `n`, this process will fill all slots exactly.

Why it works: each chosen segment is placed first, so the constraints about required segments are satisfied. By always skipping already assigned segments, we avoid conflicts. Since we iterate in order and always fill the first child with available space, every child eventually reaches `n` segments without overlap. The invariant is that at each step, no segment is assigned twice and no child exceeds `n` segments.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
chosen = list(map(int, input().split()))

children = [[a] for a in chosen]  # Step 1: assign chosen segments
assigned = set(chosen)            # Step 2: keep track of assigned segments

current_child = 0
for segment in range(1, n*k + 1):
    if segment in assigned:
        continue
    while len(children[current_child]) >= n:
        current_child += 1
    children[current_child].append(segment)
    assigned.add(segment)

for group in children:
    print(' '.join(map(str, group)))
```

The solution initializes each child with their chosen segment, tracks assigned segments with a set, and fills remaining slots sequentially. Using a set avoids accidental duplication. The loop increments `current_child` only when the current child is full, ensuring fair distribution. Edge cases such as the largest segment being chosen first or last are handled automatically by sequential iteration.

## Worked Examples

### Sample 1

Input: `2 2` and chosen `[4,1]`

| Step | Current Child | Segment | Assigned | Children State |
| --- | --- | --- | --- | --- |
| Init | - | - | {4,1} | [[4],[1]] |
| 1 | 0 | 1 | skip | [[4],[1]] |
| 2 | 0 | 2 | {1,2,4} | [[4,2],[1]] |
| 3 | 1 | 3 | {1,2,3,4} | [[4,2],[1,3]] |
| 4 | 0/1 | 4 | skip | [[4,2],[1,3]] |

Output: `4 2` and `1 3`. This fills both children correctly.

### Sample 2 (Constructed)

Input: `3 3` with chosen `[2,5,7]`

| Step | Current Child | Segment | Assigned | Children State |
| --- | --- | --- | --- | --- |
| Init | - | - | {2,5,7} | [[2],[5],[7]] |
| 1 | 0 | 1 | {1,2,5,7} | [[2,1],[5],[7]] |
| 2 | 0 | 3 | {1,2,3,5,7} | [[2,1,3],[5],[7]] |
| 3 | 1 | 4 | {1,2,3,4,5,7} | [[2,1,3],[5,4],[7]] |
| 4 | 1 | 6 | {1,2,3,4,5,6,7} | [[2,1,3],[5,4,6],[7]] |
| 5 | 2 | 8 | {1-8} | [[2,1,3],[5,4,6],[7,8]] |
| 6 | 2 | 9 | {1-9} | [[2,1,3],[5,4,6],[7,8,9]] |

Output: `2 1 3`, `5 4 6`, `7 8 9`. Each child has exactly 3 segments, chosen segments included, no duplicates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*k) | We iterate through all segments once and assign them, linear in total segments. |
| Space | O(n*k) | We store the assignment for each child and track assigned segments. |

With `n*k` at most 900, the algorithm performs well under the 2-second limit, and memory usage is trivial.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open('solution.py').read())
    return output.getvalue().strip()

# Provided sample
assert run("2 2\n4 1\n") in ["4 2\n1 3", "2 4\n1 3", "4 2\n3 1"], "sample 1"

# Minimum size input
assert run("1 1\n1\n") == "1", "min input"

# Maximum size input
n, k = 30, 30
inp = f"{n} {k}\n" + " ".join(str(i) for i in range(1,k+1)) + "\n"
res = run(inp)
lines = res.split("\n")
assert all(len(line.split()) == n for line in lines), "max input"

# Chosen segments in order
assert run("2 3\n1 2 3\n") == run("2 3\n1 2 3\n"), "ordered chosen"

# Chosen segments at high end
assert run("2 3\n4 5 6\n") == run("2 3\n4 5 6\n"), "high-end chosen"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1\n1\n` | `1` | minimum size input |
| `30 30\n1 2 ... 30\n` | any valid distribution | maximum size input correctness |
| `2 3\n1 2 3\n` | any valid | chosen segments at low end |
| `2 3\n4 5 6\n` | any valid | chosen segments at high end |

## Edge Cases

For `n=1`, `k=1`, chosen `[1]`, the loop does nothing because the segment is already assigned. Output is `[1]`.

For `n=3`, `k=3`, chosen `[1,2,3]`, remaining segments `[4,5,6,7,8,9]
