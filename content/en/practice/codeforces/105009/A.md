---
title: "CF 105009A - TriNum Array"
description: "We are given a sequence of integers laid out in a single line, and we are asked to find a contiguous segment of this sequence that uses at most three distinct values, while being as long as possible. Think of the array as a timeline of trades in Numerica."
date: "2026-06-28T03:02:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105009
codeforces_index: "A"
codeforces_contest_name: "2024 USACO.Guide Informatics Tournament"
rating: 0
weight: 105009
solve_time_s: 68
verified: true
draft: false
---

[CF 105009A - TriNum Array](https://codeforces.com/problemset/problem/105009/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers laid out in a single line, and we are asked to find a contiguous segment of this sequence that uses at most three distinct values, while being as long as possible.

Think of the array as a timeline of trades in Numerica. Each number is a type of item being traded at that moment. We want to pick a continuous stretch of time where the market only deals with up to three kinds of items. Among all such valid stretches, we want the one with the maximum length.

The output is just one number, the length of that best possible stretch.

The array size can be up to 100000, which immediately rules out any solution that tries to examine every subarray explicitly. A quadratic or cubic approach would require on the order of 10¹⁰ operations in the worst case, which is far beyond what runs in one second. This pushes us toward linear or near-linear techniques, typically involving a sliding window or two pointers.

A subtle issue arises when thinking about greedy expansion. If we extend a segment until it violates the constraint, we must be careful about how we shrink it. A naive approach that restarts from scratch after every violation can miss optimal windows or become too slow.

For example, consider an array like `[1, 2, 3, 4, 1, 2, 3]`. The optimal segment is any window containing only three distinct values, such as `[1, 2, 3, 4]` is invalid, but `[2, 3, 4, 1]` is also invalid due to four distinct values. The correct answer is 3 from segments like `[1, 2, 3]`. If we incorrectly restart whenever we see a fourth distinct value, we may repeatedly discard useful overlap and recompute unnecessarily.

## Approaches

The brute-force method is straightforward. We consider every starting index, and extend the subarray to the right while tracking how many distinct numbers appear. For each start, we expand until we hit four distinct values, and record the best valid length seen before that point.

This works because it explicitly checks every candidate segment. The problem is its cost. For each of the N starting positions, we may scan up to N elements, and maintaining distinct counts in a naive way adds overhead. Even with hashing, the worst-case complexity is O(N²), which leads to around 10¹⁰ operations when N = 10⁵, clearly too slow.

The key observation is that we do not actually need to restart scanning from each index. As we move a right pointer forward, the left pointer only needs to move forward as well to restore the constraint of at most three distinct values. Once a value leaves the window completely, it is removed from our frequency structure. This monotonic movement of both pointers guarantees that each element enters and leaves the window at most once.

This is exactly the sliding window technique: we maintain a window that is always valid (at most three distinct values), and we expand it greedily while fixing violations by shrinking from the left.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) to O(N) | Too slow |
| Optimal Sliding Window | O(N) | O(1) to O(N) | Accepted |

## Algorithm Walkthrough

We maintain a window `[l, r]` and a frequency map of values inside it.

1. Initialize `l = 0`, `best = 0`, and an empty frequency map.

This sets up an empty sliding window.
2. Move the right pointer `r` from left to right across the array.

Each step adds one new element into the current window, gradually exploring all subarrays ending at `r`.
3. When adding `A[r]`, increase its frequency in the map.

This keeps an exact count of how many times each value appears inside the current window.
4. If the number of distinct keys in the map becomes greater than 3, shrink the window from the left.

We repeatedly decrement the frequency of `A[l]` and move `l` forward until the window again contains at most three distinct values. This is necessary because any invalid window cannot contribute to the answer.
5. After restoring validity, update the answer with `best = max(best, r - l + 1)`.

At this point, `[l, r]` is the longest valid subarray ending at `r`, so it is safe to consider it for the global maximum.
6. Continue until `r` reaches the end of the array.

### Why it works

The algorithm relies on a key invariant: at every position of `r`, the window `[l, r]` contains at most three distinct values, and `l` is the smallest index that maintains this property for the current `r`. Because we only move `l` forward when necessary, we never discard a potentially better window ending at `r`. Every valid subarray is represented at some point as a window endpoint, and the maximum over these is the global answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    freq = {}
    l = 0
    best = 0
    
    for r in range(n):
        freq[a[r]] = freq.get(a[r], 0) + 1
        
        while len(freq) > 3:
            freq[a[l]] -= 1
            if freq[a[l]] == 0:
                del freq[a[l]]
            l += 1
        
        best = max(best, r - l + 1)
    
    print(best)

if __name__ == "__main__":
    solve()
```

The solution is built directly around the sliding window invariant. The dictionary `freq` tracks multiplicities, and the condition `len(freq) > 3` detects when the window violates the constraint.

The inner while-loop is crucial: it ensures the window is always repaired immediately after a violation. Without deleting keys when their frequency drops to zero, `len(freq)` would be incorrect, which is a common source of bugs.

The expression `r - l + 1` computes the current window size and represents the best valid subarray ending at `r`.

## Worked Examples

### Example 1

Input:

```
7
1 4 2 1 9 1 10
```

We track `(l, r, window, freq, best)`:

| r | l | window | freq | best |
| --- | --- | --- | --- | --- |
| 0 | 0 | [1] | {1:1} | 1 |
| 1 | 0 | [1,4] | {1:1,4:1} | 2 |
| 2 | 0 | [1,4,2] | {1:1,4:1,2:1} | 3 |
| 3 | 0 | [1,4,2,1] | {1:2,4:1,2:1} | 4 |
| 4 | 1 | [4,2,1,9] → shrink | {2:1,1:1,9:1} | 4 |
| 5 | 2 | [2,1,9,1] | {2:1,1:2,9:1} | 4 |
| 6 | 3 | window shrinks repeatedly | valid windows | 4 |

This shows that once a fourth distinct value appears, the left pointer moves forward until only three remain, and the best valid segment found is length 4.

### Example 2

Input:

```
6
1 2 3 2 1 2
```

| r | l | window | freq | best |
| --- | --- | --- | --- | --- |
| 0 | 0 | [1] | {1:1} | 1 |
| 1 | 0 | [1,2] | {1:1,2:1} | 2 |
| 2 | 0 | [1,2,3] | {1:1,2:1,3:1} | 3 |
| 3 | 0 | [1,2,3,2] | {1:1,2:2,3:1} | 4 |
| 4 | 0 | [1,2,3,2,1] | {1:2,2:2,3:1} | 5 |
| 5 | 0 | [1,2,3,2,1,2] | {1:2,2:3,3:1} | 6 |

Here we never exceed three distinct values, so the entire array is valid.

These traces confirm that the algorithm continuously maintains validity while expanding as far as possible before shrinking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | each element enters and leaves the window at most once |
| Space | O(1) to O(N) | frequency map stores at most 3 keys in the window |

The linear complexity fits comfortably within constraints for N up to 100000, and the memory usage remains small since at most a handful of keys are stored at any time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        
        freq = {}
        l = 0
        best = 0
        
        for r in range(n):
            freq[a[r]] = freq.get(a[r], 0) + 1
            while len(freq) > 3:
                freq[a[l]] -= 1
                if freq[a[l]] == 0:
                    del freq[a[l]]
                l += 1
            best = max(best, r - l + 1)
        
        return best
    
    return str(solve())

assert run("7\n1 4 2 1 9 1 10\n") == "4"
assert run("6\n1 2 3 2 1 2\n") == "6"
assert run("1\n5\n") == "1"
assert run("5\n1 1 1 1 1\n") == "5"
assert run("6\n1 2 3 4 5 6\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimum size |
| all equal | n | no shrinking needed |
| all distinct | 3 | frequent shrinking behavior |
| mixed case | correct window expansion | general correctness |

## Edge Cases

A minimal input like `1` tests whether the algorithm correctly initializes the answer without entering the loop. The window starts and ends at a single element, and the frequency map contains one key, producing output 1 immediately.

A fully uniform array such as `5 5 5 5 5` never triggers the shrinking condition. The frequency map always has size 1, so the window grows monotonically to full length. This confirms that the algorithm does not artificially shrink valid windows.

A strictly alternating pattern like `1 2 3 4 5 6` forces repeated shrinking. When the fourth distinct value appears, the left pointer advances until only three remain. This tests correctness of deletion logic when frequencies drop to zero and ensures that the distinct-count check stays accurate throughout execution.
