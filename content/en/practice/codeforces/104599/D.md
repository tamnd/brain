---
title: "CF 104599D - Dividing Data"
description: "We are given a collection of files, each with a fixed size in bits, and a storage budget $X$. From these files, we want to select as many as possible while ensuring the total size of selected files does not exceed $X$."
date: "2026-06-30T02:59:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104599
codeforces_index: "D"
codeforces_contest_name: "GPL 2023 Novice"
rating: 0
weight: 104599
solve_time_s: 56
verified: true
draft: false
---

[CF 104599D - Dividing Data](https://codeforces.com/problemset/problem/104599/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of files, each with a fixed size in bits, and a storage budget $X$. From these files, we want to select as many as possible while ensuring the total size of selected files does not exceed $X$. Each file can either be taken or skipped, and there is no partial selection.

The input gives $N$ file sizes followed by the storage limit $X$. The task is to output the maximum number of files we can fit into the budget.

The structure immediately suggests a packing problem, but the objective is not to maximize total size or value. Instead, we want to maximize the count of chosen elements under a sum constraint. That changes the optimal strategy significantly.

With $N \le 100{,}000$, any solution that tries all subsets is impossible because it grows exponentially. Even checking all combinations would require on the order of $2^N$ operations, which is completely infeasible. Sorting-based or linear-time greedy strategies are the only realistic candidates.

A few edge cases matter:

If all files are larger than $X$, then no file can be chosen and the answer is zero.

If all files are extremely small, for example all equal to 1 and $X = 10^9$, then the answer is simply $N$, since we can take everything.

If there is one very large file and many small ones, a naive greedy approach that picks large files first would fail, because it would consume budget too early and reduce the count.

## Approaches

A direct brute-force approach would consider every subset of files, compute its total size, and track how many elements it contains if the sum is within $X$. This is correct because it explores all possibilities, but it becomes unusable as soon as $N$ grows beyond small limits. With $N = 100{,}000$, the number of subsets is astronomically large, and even $N = 40$ would already be near the edge of what optimized enumeration techniques can handle.

The key observation is that the order in which we pick files matters if our goal is to maximize the count. If we ever choose a large file while a smaller file exists, we are wasting capacity that could have supported more items. This suggests that to maximize the number of files, we should always prefer smaller files first.

Once we sort all file sizes in ascending order, the best strategy becomes straightforward: take files in increasing order until adding the next one would exceed the budget. This greedy choice is safe because any valid selection of $k$ files can always be transformed into a selection of the $k$ smallest files without increasing the total sum. That exchange argument ensures that sorting does not lose optimal solutions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^N)$ | $O(1)$ | Too slow |
| Optimal (sorting + greedy scan) | $O(N \log N)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Read all file sizes and the storage limit $X$. This is just input preparation before any reasoning begins.
2. Sort the array of file sizes in non-decreasing order. The reason for sorting is that smaller files are always more efficient in terms of "count per unit storage", so we want to prioritize them.
3. Initialize two variables: a running sum of used storage and a counter for how many files have been selected. Both start at zero.
4. Iterate through the sorted file sizes from smallest to largest. At each step, check whether adding the current file would keep the total within $X$.
5. If adding the file does not exceed $X$, include it: increase the running sum and increment the counter.
6. If adding the file exceeds $X$, stop the process immediately. Since the array is sorted, every later file is at least as large, so none of them can be included either without violating the constraint.
7. Output the counter as the final answer.

### Why it works

The correctness rests on a simple exchange property. Suppose an optimal solution selects some set of $k$ files. If that set is not the $k$ smallest files, then there exists a chosen file that is larger than an unchosen file. Swapping them cannot increase the total sum and may reduce it, meaning the swapped solution is still valid and at least as good. Repeating this process transforms any optimal solution into one that consists of the $k$ smallest elements.

Therefore, the best way to maximize the number of files is equivalent to taking the smallest files first until the budget is exhausted. The greedy prefix of the sorted array is always optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    arr = [int(input()) for _ in range(n)]
    
    arr.sort()
    
    total = 0
    cnt = 0
    
    for v in arr:
        if total + v <= x:
            total += v
            cnt += 1
        else:
            break
    
    print(cnt)

if __name__ == "__main__":
    solve()
```

The solution begins by reading $N$ and $X$, followed by all file sizes. Sorting is crucial because it establishes the greedy order in which we consider elements.

The loop maintains two invariants: `total` always equals the sum of chosen files so far, and `cnt` equals how many files have been selected. The early break is safe because once a file is too large, all later ones are at least as large due to sorting.

A subtle point is that we never try to reconsider skipped files. That is valid because once we pass a file in sorted order, using it later would only be possible by removing smaller files, which would never increase the count.

## Worked Examples

### Sample 1

Input:

```
5 34
14
25
47
11
6
```

Sorted array: [6, 11, 14, 25, 47]

| Step | Current Value | Running Sum | Count | Action |
| --- | --- | --- | --- | --- |
| 1 | 6 | 6 | 1 | take |
| 2 | 11 | 17 | 2 | take |
| 3 | 14 | 31 | 3 | take |
| 4 | 25 | 56 | 3 | stop |

The process stops when 25 would exceed the limit. The answer is 3, showing that the best selection is the three smallest feasible files.

### Sample 2

Input:

```
6 18
2 5 6 4 13 1
```

Sorted array: [1, 2, 4, 5, 6, 13]

| Step | Current Value | Running Sum | Count | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | take |
| 2 | 2 | 3 | 2 | take |
| 3 | 4 | 7 | 3 | take |
| 4 | 5 | 12 | 4 | take |
| 5 | 6 | 18 | 5 | take |
| 6 | 13 | 18 | 5 | skip (would exceed) |

We successfully take five files before reaching the limit exactly. This demonstrates that the greedy approach naturally fills the budget as tightly as possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ | sorting dominates, single linear scan afterward |
| Space | $O(1)$ extra (or $O(N)$ depending on storage) | only input array plus counters |

The constraints allow up to $10^5$ elements, so an $O(N \log N)$ sorting solution fits comfortably within time limits. The memory usage is also well within the 256 MB limit since only one integer array is stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, x = map(int, sys.stdin.readline().split())
    arr = [int(sys.stdin.readline()) for _ in range(n)]
    arr.sort()
    
    total = 0
    cnt = 0
    
    for v in arr:
        if total + v <= x:
            total += v
            cnt += 1
        else:
            break
    
    return str(cnt)

# provided samples
assert run("5 34\n14\n25\n47\n11\n6\n") == "3", "sample 1"
assert run("6 18\n2\n5\n6\n4\n13\n1\n") == "5", "sample 2"

# custom cases
assert run("1 10\n5\n") == "1"
assert run("3 3\n4\n5\n6\n") == "0"
assert run("4 10\n1\n1\n1\n1\n") == "4"
assert run("5 9\n9\n8\n7\n6\n5\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single small file | 1 | minimal case where selection always possible |
| all too large | 0 | no feasible selection |
| all equal small | 4 | full capacity utilization |
| descending large values | 1 | confirms sorting is essential |

## Edge Cases

One edge case is when all files exceed the limit. For example, input:

```
3 5
10 20 30
```

After sorting, the first element is already greater than $X$. The loop immediately fails the condition and returns zero. This confirms that early termination behaves correctly even when nothing is selectable.

Another case is when the optimal solution requires taking many small elements instead of a single large one. For example:

```
4 10
6 6 6 6
```

Sorted order remains the same. The first element 6 is taken, but the next 6 would exceed the budget, so the answer is 1. Any attempt to pick multiple elements fails because every combination of two exceeds the limit, which matches the greedy result.
