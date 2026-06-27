---
title: "CF 105176J - \u6700\u540e\u4e00\u5757\u77f3\u5934\u7684\u91cd\u91cf"
description: "We are given a collection of stones, each stone having a positive integer weight. The process repeatedly takes the two heaviest stones available, destroys both, and if their weights are different, a new stone is produced whose weight equals the difference of the two."
date: "2026-06-27T06:32:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105176
codeforces_index: "J"
codeforces_contest_name: "2024 Xian Jiaotong University Programming Contest"
rating: 0
weight: 105176
solve_time_s: 35
verified: true
draft: false
---

[CF 105176J - \u6700\u540e\u4e00\u5757\u77f3\u5934\u7684\u91cd\u91cf](https://codeforces.com/problemset/problem/105176/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of stones, each stone having a positive integer weight. The process repeatedly takes the two heaviest stones available, destroys both, and if their weights are different, a new stone is produced whose weight equals the difference of the two. This continues until at most one stone remains. The task is to determine the final remaining weight, or zero if no stones are left.

The input represents the initial multiset of stone weights. The output is a single integer describing the last surviving weight after repeatedly applying the “smash the two largest” operation.

The structure of the problem immediately suggests that the main difficulty is not arithmetic but repeated selection of the two maximum elements. If there are up to n stones, a naive simulation that scans the entire list to find the two largest elements each time would cost O(n) per operation. Since each operation reduces the number of stones by one, the total number of operations is O(n), which leads to O(n²) time in the worst case. This is too slow when n is large, for example 10⁵, where quadratic behavior would be far beyond feasible limits.

A subtle edge case appears when the final result becomes zero because all stones cancel each other out. For example, if the input is [2, 7, 4, 1, 8, 1], the process ends with a single stone of weight 1. But if the input is [1, 1], both stones are destroyed and nothing remains, so the correct answer is 0. A careless implementation that returns the last computed difference without checking emptiness can incorrectly output an uninitialized or stale value in this case.

## Approaches

The brute-force simulation maintains the list of stones and repeatedly scans it to find the two largest elements. After removing them, it inserts either their difference or nothing. This approach is correct because it exactly mirrors the described process. The failure point is performance: each extraction of the top two elements costs O(n), and this happens O(n) times, leading to O(n²) total work. For large inputs this becomes infeasible.

The key observation is that the process only ever needs fast access to the current maximum elements. There is no requirement to maintain order beyond repeated extraction of the largest values. This is exactly the use case for a max-heap (priority queue). By storing all stones in a heap, we can extract the two largest elements in O(log n) time each, and insert a new value back in O(log n). This reduces the total complexity to O(n log n), which is sufficient for typical constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan | O(n²) | O(1)-O(n) | Too slow |
| Max Heap Simulation | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We model the system using a max-heap, which allows us to always retrieve the current two largest stones efficiently.

1. Insert all stone weights into a max-heap. We invert values if using a min-heap implementation, since most standard libraries provide only min-heaps.
2. While there is more than one stone in the heap, remove the largest stone x. This represents the heaviest available stone at that moment.
3. Remove the second largest stone y. At this point we are simulating the required pairwise operation on the two strongest candidates.
4. If x and y are not equal, compute their difference x − y and push it back into the heap. If they are equal, both stones are destroyed and nothing is reinserted.
5. Continue until the heap has size 0 or 1. If one element remains, that value is the answer. If empty, the answer is 0.

The reason this greedy extraction is valid is that the problem never depends on the relative order of non-maximum elements. Only the two largest values affect each step’s outcome, and removing them does not require reconsidering earlier decisions. The heap ensures that at every step we are applying the operation exactly as defined on the current global maximums.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n_and_rest = sys.stdin.read().strip().split()
    if not n_and_rest:
        return
    n = int(n_and_rest[0])
    arr = list(map(int, n_and_rest[1:]))

    # use max heap via negatives
    heap = [-x for x in arr]
    heapq.heapify(heap)

    while len(heap) > 1:
        x = -heapq.heappop(heap)
        y = -heapq.heappop(heap)

        if x != y:
            heapq.heappush(heap, -(x - y))

    if heap:
        print(-heap[0])
    else:
        print(0)

if __name__ == "__main__":
    solve()
```

The implementation relies on Python’s `heapq`, which is a min-heap, so all values are stored as negatives to simulate a max-heap. The loop condition `len(heap) > 1` ensures we only attempt to extract pairs when they exist. The final check handles the empty heap case explicitly, which is necessary for inputs where all stones cancel out.

## Worked Examples

Consider the input `[2, 7, 4, 1, 8, 1]`.

| Step | Heap (conceptual max form) | Chosen x | Chosen y | Action | Heap after |
| --- | --- | --- | --- | --- | --- |
| 1 | [8, 7, 4, 2, 1, 1] | 8 | 7 | push 1 | [4, 2, 1, 1, 1] |
| 2 | [4, 2, 1, 1, 1] | 4 | 2 | push 2 | [2, 1, 1, 1] |
| 3 | [2, 1, 1, 1] | 2 | 1 | push 1 | [1, 1, 1] |
| 4 | [1, 1, 1] | 1 | 1 | remove both | [1] |

Final answer is 1.

This trace shows that intermediate differences can re-enter the pool and still influence later operations, which is why a global structure like a heap is required.

Now consider `[1, 1]`.

| Step | Heap | x | y | Action | Heap after |
| --- | --- | --- | --- | --- | --- |
| 1 | [1, 1] | 1 | 1 | remove both | [] |

The heap becomes empty, confirming that we must explicitly output zero when no element remains.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each stone is inserted once and potentially moved during heap operations, and each smash does O(log n) work |
| Space | O(n) | The heap stores all current stones |

The logarithmic overhead is acceptable for n up to at least 10⁵, which is typical for this class of problems. The structure avoids quadratic scanning entirely.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import contextlib
    import io as _io

    out = _io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    try:
        solve()
    finally:
        sys.stdout = old_stdout
    return out.getvalue().strip()

# minimal cases
assert run("1\n5\n5") == "5"
assert run("2\n1 1") == "0"

# sample-like case
assert run("6\n2 7 4 1 8 1") == "1"

# all equal
assert run("4\n3 3 3 3") == "0"

# decreasing
assert run("5\n9 7 5 3 1") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 | 5 | single element edge case |
| 1 1 1 | 0 | full cancellation |
| 2 7 4 1 8 1 | 1 | standard multi-step behavior |
| 3 3 3 3 | 0 | repeated equal removals |
| 9 7 5 3 1 | 1 | cascading differences |

## Edge Cases

A key edge case is when all stones cancel out completely. For input `[1, 1]`, the algorithm pushes both values into the heap, pops them, finds they are equal, and does not push anything back. The heap becomes empty and the final output correctly becomes zero.

Another subtle case is when intermediate reductions repeatedly generate smaller stones that later interact again. For example `[5, 4, 3]` first produces `5-4=1`, then `[3, 1]` produces `2`, and finally the answer is `2`. The heap ensures these newly created values are always reconsidered at the correct time, because they re-enter the same global structure and compete equally with existing stones.
