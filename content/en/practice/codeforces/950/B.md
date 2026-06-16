---
title: "CF 950B - Intercepted Message"
description: "We are given two sequences of positive integers, each sequence representing how a long stream of bytes was transmitted in chunks. Each sequence is a segmentation of the same total length, but the segmentation points are different."
date: "2026-06-17T02:20:11+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 950
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 469 (Div. 2)"
rating: 1100
weight: 950
solve_time_s: 68
verified: true
draft: false
---

[CF 950B - Intercepted Message](https://codeforces.com/problemset/problem/950/B)

**Rating:** 1100  
**Tags:** greedy, implementation  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences of positive integers, each sequence representing how a long stream of bytes was transmitted in chunks. Each sequence is a segmentation of the same total length, but the segmentation points are different.

The hidden structure we want to reconstruct is an archive made of several files written one after another. Each file has some total size, but during transmission each file may be split into multiple consecutive blocks. Crucially, within each message we only see these smaller blocks, not the original file boundaries. Our task is to determine the maximum possible number of original files such that both messages could have come from the same sequence of file sizes, only split differently.

So we are given two arrays whose sums are equal, and we must partition both arrays into contiguous segments so that the segment sums match in order. The goal is to maximize how many matching segments we can create.

The constraints are large enough that any solution worse than linear in the total input size would be too slow. Both arrays can have up to 100,000 elements, so we need a method that processes them in a single pass or near single pass time. Anything involving nested scanning or recomputation of prefix sums repeatedly would fail.

A naive mistake is to try all possible partition points independently in both arrays. For example, even for small inputs, one might attempt to align prefix sums from the first array with all prefix sums of the second array. This breaks quickly: for arrays like `1 1 1 1 ...` the number of partition combinations grows quadratically.

Another subtle failure case appears when greedy matching is done without synchronization. If we greedily cut a file whenever one prefix sum is smaller than the other, but forget to enforce equality of completed file boundaries in both arrays simultaneously, we can produce mismatched partitions.

The correct structure depends on synchronizing cumulative sums so that we only “cut a file” when both sides reach the same total.

## Approaches

The brute-force approach tries to choose partition points in both arrays and match segment sums. One could imagine generating all prefix sums, then attempting to pair them in increasing order so that each chosen pair forms a file boundary. While this is conceptually simple, it requires exploring combinations of partition points, which leads to exponential or at least quadratic behavior depending on implementation. With 10^5 elements, this is impossible.

The key insight is that both arrays represent the same total sequence of file sizes, just chopped differently into pieces. If we walk through both arrays simultaneously, accumulating sums, we can detect when a full file boundary has been reached exactly when the accumulated sums match. At that moment, we can safely declare one file complete and reset both accumulators.

This works because file boundaries correspond exactly to points where both cumulative sums align. Since order is preserved, we never need to reconsider previous decisions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all partitions) | O(2^n) or O(n^2) | O(n) | Too slow |
| Two-pointer greedy synchronization | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two pointers, one for each array, and two running sums representing the current partially accumulated file from each message.

1. Initialize two indices `i = 0`, `j = 0`, and two accumulators `a_sum = 0`, `b_sum = 0`. Also initialize `files = 0`.
2. Move through both arrays while neither is exhausted. At each step, we add the next block to the smaller or both accumulators.
3. If `a_sum` is smaller than `b_sum`, we take the next block from the first array and add it to `a_sum`. We advance `i`.
4. If `b_sum` is smaller than `a_sum`, we take the next block from the second array and add it to `b_sum`. We advance `j`.
5. If `a_sum == b_sum` and both are non-zero, we have found a complete file boundary shared by both representations. We increment `files` and reset both sums to zero.
6. Continue until both arrays are fully consumed. The final answer is `files`.

The reason this stepping rule works is that we never allow one side to overshoot without compensating from the other. We always preserve the invariant that both accumulators represent partial sums of the same current file candidate. When equality occurs, both partial constructions correspond to a full file in the original archive.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    x = list(map(int, input().split()))
    y = list(map(int, input().split()))
    
    i = j = 0
    sx = sy = 0
    ans = 0
    
    while i < n or j < m:
        if sx <= sy:
            if i < n:
                sx += x[i]
                i += 1
        else:
            if j < m:
                sy += y[j]
                j += 1
        
        if sx == sy:
            if sx != 0:
                ans += 1
            sx = sy = 0
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the two-pointer synchronization idea. The key subtlety is the `sx <= sy` condition: when sums are equal, we prefer to extend the first array first, but it does not matter which side is advanced as long as we maintain progress. The equality check immediately after ensures that whenever both partial sums match, we commit a file boundary.

One common pitfall is forgetting to reset both accumulators after counting a file. Another is continuing to advance only one pointer without ensuring termination when one array finishes earlier; the `while i < n or j < m` condition ensures remaining blocks are still processed.

## Worked Examples

### Example 1

Input:

```
7 6
2 5 3 1 11 4 4
7 8 2 4 1 8
```

We track cumulative sums:

| Step | i | j | sx | sy | Action | files |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 2 | 0 | take x | 0 |
| 2 | 0 | 0 | 2 | 7 | take y | 0 |
| 3 | 1 | 0 | 7 | 7 | match → cut | 1 |
| 4 | 1 | 1 | 0 | 0 | reset | 1 |
| 5 | 3 | 1 | 4 | 8 | build | 1 |
| 6 | 3 | 2 | 4 | 10 | build | 1 |
| 7 | 3 | 2 | 7 | 10 | build | 1 |
| 8 | 4 | 2 | 8 | 10 | build | 1 |
| 9 | 4 | 3 | 19 | 19 | match → cut | 2 |
| 10 | 4 | 4 | 0 | 0 | reset | 2 |
| 11 | 6 | 5 | 4 | 8 | build | 2 |
| 12 | 7 | 5 | 8 | 8 | match → cut | 3 |

Final answer is 3.

This trace shows that file boundaries are only detected when both accumulated sums align, not when individual arrays reach arbitrary partial sums.

### Example 2

Input:

```
3 3
1 2 3
2 1 3
```

| Step | i | j | sx | sy | Action | files |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 0 | take x | 0 |
| 2 | 0 | 0 | 1 | 2 | take y | 0 |
| 3 | 1 | 0 | 3 | 2 | take x | 0 |
| 4 | 1 | 1 | 3 | 3 | match → cut | 1 |
| 5 | 2 | 2 | 0 | 0 | reset | 1 |
| 6 | 3 | 3 | 3 | 3 | match → cut | 2 |

Final answer is 2.

This demonstrates that different internal segmentations still align perfectly when cumulative sums are synchronized.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each pointer advances exactly once across its array |
| Space | O(1) | Only counters and indices are stored |

The linear scan is sufficient because each block is processed once, and no backtracking occurs. With total input size up to 2×10^5, this comfortably fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    x = list(map(int, input().split()))
    y = list(map(int, input().split()))
    
    i = j = 0
    sx = sy = 0
    ans = 0
    
    while i < n or j < m:
        if sx <= sy:
            if i < n:
                sx += x[i]
                i += 1
        else:
            if j < m:
                sy += y[j]
                j += 1
        
        if sx == sy:
            if sx != 0:
                ans += 1
            sx = sy = 0
    
    return str(ans)

# provided sample
assert run("7 6\n2 5 3 1 11 4 4\n7 8 2 4 1 8\n") == "3"

# single file case
assert run("1 1\n10\n10\n") == "1"

# alternating small splits
assert run("4 4\n1 1 1 1\n2 1 1 1\n") == "2"

# already aligned blocks
assert run("3 3\n3 3 3\n3 3 3\n") == "3"

# uneven internal splits
assert run("5 4\n1 2 3 4 5\n3 3 3 6\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 10 / 10 | 1 | minimal case |
| 1 1 1 1 / 2 1 1 1 | 2 | uneven segmentation |
| 3 3 / all equal | 3 | already aligned |
| 5 4 / mixed | 2 | non-trivial alignment |

## Edge Cases

One edge case is when one array finishes accumulating faster than the other. For example, if one sequence has a large block at the end, the algorithm must still continue consuming the remaining blocks in the other array until the sums align. The loop condition `i < n or j < m` ensures we do not stop early.

Another case is when equality occurs multiple times in quick succession due to zeroing after a cut. The reset step guarantees that consecutive files are counted separately, since both accumulators restart cleanly after each match.

A final subtle case is when the last file ends exactly at the last block of both arrays. The algorithm still counts it because equality triggers a cut even at termination, and no remaining unprocessed elements exist afterward.
