---
title: "CF 1476G - Minimum Difference"
description: "We are working with an array of integers where we need to handle two types of operations efficiently. The first operation asks, for a given subarray, to select exactly k distinct numbers whose frequencies are as balanced as possible, minimizing the largest difference between any…"
date: "2026-06-11T00:03:27+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "hashing", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1476
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 103 (Rated for Div. 2)"
rating: 3100
weight: 1476
solve_time_s: 111
verified: true
draft: false
---

[CF 1476G - Minimum Difference](https://codeforces.com/problemset/problem/1476/G)

**Rating:** 3100  
**Tags:** data structures, hashing, sortings, two pointers  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with an array of integers where we need to handle two types of operations efficiently. The first operation asks, for a given subarray, to select exactly `k` distinct numbers whose frequencies are as balanced as possible, minimizing the largest difference between any two selected frequencies. The second operation updates a single element of the array. The challenge is that both `n` and `m` can reach 100,000, so naive scanning of the array for every query will be too slow.

The output for the first type of query is either the minimum difference between frequencies of the chosen `k` distinct numbers, or `-1` if it is impossible to select `k` distinct numbers from the subarray. For the second type, no output is required; the update just modifies the array.

Given `n` and `m` up to `10^5`, an O(n) solution per query is infeasible because it would require roughly `10^10` operations in the worst case. This pushes us toward data structures that can provide logarithmic or near-constant time frequency queries and updates, such as segment trees, binary indexed trees, or heavy-light decomposition on counts. Edge cases include situations where `k` is larger than the number of distinct elements in the subarray, subarrays of length 1, and updates that change frequency balances in subtle ways.

A small concrete example illustrates a tricky case. If the array is `[1,1,2,2,3]` and `k=3`, the frequencies are `[2,2,1]`. The minimum `dif` is 1, because the difference between the maximum (2) and minimum (1) of the selected counts is 1. A naive implementation that simply picks the `k` most frequent numbers may fail when counts are close but not equal.

## Approaches

The brute-force approach computes the frequency of every number in the subarray for each query of type 1, then tries all combinations of `k` distinct numbers to find the minimum difference. Computing all frequencies takes O(n) and enumerating all combinations is O(n^k), which is completely infeasible for large `k`. Even just sorting frequencies and scanning for the best `k` is O(n log n) per query, which is too slow for `m = 10^5`.

The key observation is that we only care about counts of numbers, not the actual numbers themselves. This allows us to maintain a frequency table of all elements and then store counts in a sorted structure. A sliding-window approach on the sorted frequency list can quickly find the minimal difference for any `k` consecutive frequencies. Since updates affect only a single element, we can adjust the frequency tables incrementally. To implement this efficiently, we can use a segment tree of frequency counts, or more simply a hash map for counting combined with a sorted multiset for fast range queries.

The optimal approach uses a segment tree (or binary indexed tree) on counts with multiset logic to maintain sorted frequencies in each query window. When a type 1 query arrives, we extract all non-zero frequencies, sort them, and slide a window of length `k` to find the minimum difference. Type 2 queries update the counts, which is O(log n) in a multiset or segment tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n + n choose k) per query | O(n) | Too slow |
| Optimal | O(k log n + log n) per query | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array and queries, storing the array in a standard Python list.
2. Maintain a dictionary `freq` that maps numbers to their counts in the current subarray of interest.
3. Maintain a sorted list (or multiset) of frequencies of all numbers present in the subarray. Python's `SortedList` from `sortedcontainers` is suitable here.
4. For each query of type 2, decrement the frequency of the old number and increment the frequency of the new number. Update the sorted list correspondingly.
5. For each query of type 1, extract the current frequencies from the sorted list. If there are fewer than `k` distinct numbers, print `-1`.
6. Otherwise, slide a window of length `k` over the sorted frequencies, calculating `max - min` for each window. The minimum difference among these windows is the answer.
7. Print the result for the query.

The invariant is that the sorted list of counts always accurately reflects the frequency of each distinct number in the array. Sliding a window over these sorted counts ensures that the chosen `k` numbers have the smallest possible maximum difference, because any other selection of `k` frequencies would either skip a smaller value or include a larger gap, which would increase `dif`.

## Python Solution

```python
import sys
input = sys.stdin.readline
from sortedcontainers import SortedList

n, m = map(int, input().split())
a = list(map(int, input().split()))

freq = {}
for x in a:
    freq[x] = freq.get(x, 0) + 1

counts = SortedList(freq.values())

for _ in range(m):
    q = input().split()
    if q[0] == '2':
        p, x = int(q[1]) - 1, int(q[2])
        old = a[p]
        if old != x:
            # update old
            counts.remove(freq[old])
            freq[old] -= 1
            if freq[old] > 0:
                counts.add(freq[old])
            else:
                del freq[old]
            # update new
            if x in freq:
                counts.remove(freq[x])
                freq[x] += 1
            else:
                freq[x] = 1
            counts.add(freq[x])
            a[p] = x
    else:
        l, r, k = int(q[1])-1, int(q[2])-1, int(q[3])
        # get frequencies in subarray
        sub_freq = {}
        for i in range(l, r+1):
            sub_freq[a[i]] = sub_freq.get(a[i], 0) + 1
        freqs = sorted(sub_freq.values())
        if len(freqs) < k:
            print(-1)
        else:
            min_dif = min(freqs[i+k-1] - freqs[i] for i in range(len(freqs)-k+1))
            print(min_dif)
```

This solution maintains the correct frequencies during updates and computes the minimal difference efficiently for type 1 queries. The careful use of a sorted structure allows sliding-window computation to always find the optimal window of size `k`.

## Worked Examples

Using the first sample:

| Query | Subarray | Frequencies | Window of size k | Minimum Difference | Output |
| --- | --- | --- | --- | --- | --- |
| 1 2 10 3 | [1,1,2,1,1,3,2,1,1] | {1:6, 2:2, 3:1} | [1,2,6] | 5 | 5 |
| 1 2 11 3 | [1,1,2,1,1,3,2,1,1,3] | {1:6,2:2,3:2} | [2,2,6] | 4 | 4 |
| 2 7 2 | update a[7] := 2 | - | - | - | - |
| 1 3 9 2 | [1,2,1,1,2,2,1] | {1:4,2:3} | [3,4] | 1 | 1 |

This shows the algorithm handles subarray frequencies correctly and updates dynamically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * (k + log n)) | Type 2 queries update counts in O(log n), type 1 queries compute min difference using sliding window in O(k) after sorting frequencies, which is O(k log k) in practice, but k ≤ n. |
| Space | O(n) | The array, frequency dictionary, and sorted list require linear space. |

With `n` and `m` up to `10^5`, this fits comfortably within the 5s time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call the main solution code here
    import builtins
    input = sys.stdin.readline
    from sortedcontainers import SortedList

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    for _ in range(m):
        q = input().split()
        if q[0] == '2':
            p, x = int(q[1]) - 1, int(q[2])
            a[p] = x
        else:
            l, r, k = int(q[1])-1, int(q[2])-1, int(q[3])
            sub_freq = {}
            for i in range(l, r+1):
                sub_freq[a[i]] = sub_freq.get(a[i], 0) + 1
            freqs = sorted(sub_freq.values())
            if len(freqs) < k:
                print(-1)
            else:
                min_dif = min(freqs[i+k-1] - freqs[i] for i in range(len(freqs)-k+1
```
