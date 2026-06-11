---
title: "CF 1211A - Three Problems"
description: "We are asked to help Polycarp select three problems from his collection such that their complexities form a strictly increasing sequence. The input gives the number of problems n and an array of integers representing the complexity of each problem."
date: "2026-06-11T23:09:09+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1211
codeforces_index: "A"
codeforces_contest_name: "Kotlin Heroes: Episode 2"
rating: 1000
weight: 1211
solve_time_s: 111
verified: false
draft: false
---

[CF 1211A - Three Problems](https://codeforces.com/problemset/problem/1211/A)

**Rating:** 1000  
**Tags:** *special, implementation  
**Solve time:** 1m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to help Polycarp select three problems from his collection such that their complexities form a strictly increasing sequence. The input gives the number of problems `n` and an array of integers representing the complexity of each problem. The output must be either three indices corresponding to problems with strictly increasing complexity or `-1 -1 -1` if no such selection exists.

The first important observation is that `n` is at most 3000, and each complexity can be up to 10^9. This is a manageable size, so an algorithm with cubic time complexity, `O(n^3)`, is theoretically possible, but we can do better. The smallest allowed input, `n=3`, forms a natural lower bound: if the three complexities are all equal or any two are equal, no solution exists. An edge case to consider is when all problems have the same complexity, for example `[5, 5, 5]`. A careless implementation might pick consecutive indices without checking the strict inequality, producing an incorrect output.

Another subtlety arises if there are duplicates in the list. For instance, `[1, 2, 2, 3]` contains multiple ways to pick three numbers, but any solution must avoid picking the two identical `2`s as the middle and last problems. Failing to account for strict inequalities would break correctness.

## Approaches

The naive solution would be to try every triple of problems `(i, j, k)` with `i < j < k` and check if `r[i] < r[j] < r[k]`. This works because it checks all possible triples systematically, ensuring correctness. However, in the worst case, this is `O(n^3)`, which for `n=3000` results in roughly 27 billion operations - far too slow for a 3-second time limit.

The key observation that leads to an optimal solution is that we only need to find **any three distinct numbers in strictly increasing order**. Sorting the list with their original indices preserves order and allows us to scan for three numbers with distinct values. Once we have three distinct values, we can simply take their first occurrences in the original array. Sorting takes `O(n log n)` and scanning is `O(n)`, which is efficient enough.

Another insight is that we do not need the globally smallest and largest numbers; we only need three numbers such that the first is strictly less than the second, and the second is strictly less than the third. By keeping track of the first occurrence of each unique complexity while iterating, we can directly construct a valid triple without checking every combination.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Pair each problem complexity with its original index. This preserves the original numbering, which is required in the output.
2. Sort the list of pairs by complexity. After this step, the smallest complexity comes first, the largest last, and duplicates are adjacent.
3. Iterate over the sorted list to find the first three distinct complexities. Keep track of their original indices. Since the array is sorted, once we see a complexity strictly greater than the previous, we store its index.
4. If we find three distinct complexities, output their original indices. The order does not matter as long as it follows the increasing complexity. If fewer than three distinct numbers exist, output `-1 -1 -1`.

Why it works: Sorting ensures that distinct complexities appear in increasing order. By selecting the first three distinct values, we guarantee a strictly increasing sequence. The algorithm never picks duplicates for the triple, so the strict inequality is maintained.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
r = list(map(int, input().split()))

# Pair each complexity with its original index (1-based)
paired = [(val, idx + 1) for idx, val in enumerate(r)]
paired.sort()  # Sort by complexity

result = []
last_val = -1

for val, idx in paired:
    if val != last_val:
        result.append(idx)
        last_val = val
    if len(result) == 3:
        break

if len(result) < 3:
    print(-1, -1, -1)
else:
    print(result[0], result[1], result[2])
```

The solution first reads input and pairs each complexity with its index. Sorting ensures increasing complexity order. We iterate through the sorted list, storing the first occurrence of each new complexity. Once three distinct numbers are collected, we output their indices. If fewer than three distinct numbers exist, we print `-1 -1 -1`. The 1-based indexing is handled by adding one to each original array index.

## Worked Examples

**Sample Input 1**

```
6
3 1 4 1 5 9
```

| Step | Sorted Pair | last_val | result |
| --- | --- | --- | --- |
| 1 | (1,2) | -1 | [2] |
| 2 | (3,1) | 1 | [2,1] |
| 3 | (4,3) | 3 | [2,1,3] |

Output: `2 1 3` (or any triple preserving strict increase)

**Sample Input 2**

```
4
5 5 5 5
```

| Step | Sorted Pair | last_val | result |
| --- | --- | --- | --- |
| 1 | (5,1) | -1 | [1] |
| 2 | (5,2) | 5 | [1] |
| 3 | (5,3) | 5 | [1] |
| 4 | (5,4) | 5 | [1] |

Output: `-1 -1 -1`

This trace shows the algorithm correctly handles the all-equal edge case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; iteration to collect three indices is O(n) |
| Space | O(n) | Storing pairs of (value, index) |

The algorithm easily fits within the time limit for `n` up to 3000 and uses negligible additional memory relative to the limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    r = list(map(int, input().split()))
    paired = [(val, idx + 1) for idx, val in enumerate(r)]
    paired.sort()
    result = []
    last_val = -1
    for val, idx in paired:
        if val != last_val:
            result.append(idx)
            last_val = val
        if len(result) == 3:
            break
    if len(result) < 3:
        return "-1 -1 -1"
    else:
        return f"{result[0]} {result[1]} {result[2]}"

# Provided samples
assert run("6\n3 1 4 1 5 9\n") in ["2 1 3", "2 3 5"], "sample 1"
assert run("4\n5 5 5 5\n") == "-1 -1 -1", "all equal"

# Custom cases
assert run("3\n1 2 3\n") == "1 2 3", "minimum size, increasing"
assert run("5\n2 2 1 3 3\n") in ["3 1 4", "3 1 5"], "duplicates present"
assert run("10\n10 20 30 10 20 30 40 50 60 70\n") in ["1 2 3", "1 3 7"], "multiple options"
assert run("3\n7 7 7\n") == "-1 -1 -1", "minimum size, all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 2 3 | 1 2 3 | minimum size with valid triple |
| 5 2 2 1 3 3 | 3 1 4 | duplicates handled |
| 10 10 20 30 10 20 30 40 50 60 70 | 1 2 3 | multiple valid triples exist |
| 3 7 7 7 | -1 -1 -1 | minimum size all equal |

## Edge Cases

When all complexities are equal, the algorithm correctly produces `-1 -1 -1`. For example, with input `[5, 5, 5, 5]`, the sorted list is all `(5, idx)`. Since we never see a new complexity beyond the first, the `result` list never reaches three items, so the algorithm prints the failure output.

When there are duplicates but at least three distinct numbers exist, such as `[2, 2, 1, 3, 3]`, the algorithm collects the first occurrence of each distinct value in increasing order: `(1,3)`, `(2,1)`, `(3,4)`, which satisfies the strict inequality condition.
