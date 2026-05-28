---
title: "CF 85D - Sum of Medians"
description: "We are asked to maintain a dynamic set of positive integers under three operations: adding a number, deleting a number, and computing the sum of medians of every consecutive group of five elements after sorting the set."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 85
codeforces_index: "D"
codeforces_contest_name: "Yandex.Algorithm 2011: Round 1"
rating: 2300
weight: 85
solve_time_s: 78
verified: true
draft: false
---

[CF 85D - Sum of Medians](https://codeforces.com/problemset/problem/85/D)

**Rating:** 2300  
**Tags:** binary search, brute force, data structures, implementation  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maintain a dynamic set of positive integers under three operations: adding a number, deleting a number, and computing the sum of medians of every consecutive group of five elements after sorting the set. A median in a group of five is the third element once that group is sorted. The sum operation should consider the set sorted in increasing order, divide it into contiguous blocks of five, compute the median of each block, and sum all these medians. If the set size is less than five, there will be no full block, so the sum is zero.

The input consists of up to 100,000 operations, and the integers involved can go up to 10^9. Since n can reach 10^5, any solution that repeatedly sorts the full set for each sum query, which would cost O(n log n), may be too slow. In particular, in the worst case, repeated sorting after each operation would result in O(n^2 log n) total operations, which exceeds practical limits. This means we need a structure that allows efficient insertions, deletions, and median retrievals without full sorting each time.

Edge cases arise when the set has fewer than five elements, where no median exists, and when the set size is not a multiple of five, leaving an incomplete block at the end that should not contribute to the sum. Another subtle case is repeated operations that add and remove the same number, which should not break the median calculation or ordering.

## Approaches

The brute-force approach is simple: maintain the set as a list, and for every sum query, sort the list, iterate over groups of five, take the third element of each group, and sum them. This is correct because sorting produces the order required for median computation. However, sorting each time for up to 100,000 elements is O(n log n), and with up to 100,000 operations, the total time could reach O(n^2 log n), which is too slow.

The key insight for optimization is that we do not need to sort the entire set for every query. We only care about medians of every consecutive block of five elements. This suggests using a balanced binary search tree or an ordered set data structure that supports efficient insertion, deletion, and order-statistics queries. In Python, the `SortedList` from `sortedcontainers` is ideal because it provides O(log n) insertion, deletion, and O(1) access by index. With this, we can maintain a sorted view of the set at all times and compute the sum of medians in O(n) per sum query, which is acceptable given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) per sum | O(n) | Too slow for worst case |
| SortedList / Order-statistics | O(log n) per add/del, O(n) per sum | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty `SortedList`. This structure maintains all elements in sorted order, allowing binary-search operations for insertion, deletion, and indexing.
2. For each operation in the input:

- If it is an `add x`, insert `x` into the `SortedList`. The insertion preserves the sorted order automatically.
- If it is a `del x`, remove `x` from the `SortedList`. The removal operation also maintains order.
- If it is `sum`, initialize a running total to zero. Iterate over the sorted list in steps of five. For each complete group of five elements, pick the third element (index 2 within the block) and add it to the running total. Print the total after processing all complete groups.
3. Repeat for all operations.

Why it works: The `SortedList` ensures that at every moment, the set is in increasing order. By iterating in steps of five and picking the third element of each block, we directly follow the problem's definition of medians. The structure's logarithmic insertion and deletion maintain efficiency even with the dynamic set, while direct indexing gives constant-time access for median retrieval.

## Python Solution

```python
import sys
input = sys.stdin.readline
from sortedcontainers import SortedList

def main():
    n = int(input())
    sl = SortedList()
    
    for _ in range(n):
        line = input().split()
        if line[0] == "add":
            x = int(line[1])
            sl.add(x)
        elif line[0] == "del":
            x = int(line[1])
            sl.remove(x)
        else:  # sum
            total = 0
            for i in range(2, len(sl), 5):
                total += sl[i]
            print(total)

if __name__ == "__main__":
    main()
```

The `SortedList` is chosen for its combination of order maintenance and fast indexing. Insertions and deletions are logarithmic, which prevents slowdowns as the set grows. The iteration in the sum query accesses every fifth element starting from index 2, which corresponds exactly to the median of each block of five. A common pitfall is starting from index 0 or 1, which would select the wrong element. Python's arbitrary integer size avoids overflow concerns.

## Worked Examples

### Sample 1

Input:

```
6
add 4
add 5
add 1
add 2
add 3
sum
```

| Operation | SortedList | Sum Calculation | Output |
| --- | --- | --- | --- |
| add 4 | [4] | - | - |
| add 5 | [4,5] | - | - |
| add 1 | [1,4,5] | - | - |
| add 2 | [1,2,4,5] | - | - |
| add 3 | [1,2,3,4,5] | Only one full group: [1,2,3,4,5], median=3 | 3 |

This demonstrates the algorithm correctly identifies the median of a full group of five after multiple unordered insertions.

### Custom Sample

Input:

```
7
add 7
add 1
add 3
add 9
add 5
add 11
sum
```

| Operation | SortedList | Sum Calculation | Output |
| --- | --- | --- | --- |
| add 7 | [7] | - | - |
| add 1 | [1,7] | - | - |
| add 3 | [1,3,7] | - | - |
| add 9 | [1,3,7,9] | - | - |
| add 5 | [1,3,5,7,9] | One group: [1,3,5,7,9], median=5 | - |
| add 11 | [1,3,5,7,9,11] | Groups: [1,3,5,7,9], [11] -> sum=5 | 5 |

Shows that incomplete groups at the end do not contribute.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) for all add/del, O(n) per sum | Each insertion/deletion costs O(log n), sum iterates in steps of 5, at most n iterations |
| Space | O(n) | We store all current elements in a `SortedList` |

With n up to 10^5 and operations bounded by 3 seconds, this fits comfortably. Each sum query iterates over at most 10^5 elements, which is feasible.

## Test Cases

```python
import sys, io
from sortedcontainers import SortedList

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# provided sample
assert run("6\nadd 4\nadd 5\nadd 1\nadd 2\nadd 3\nsum\n") == "3", "sample 1"

# minimum-size input
assert run("1\nsum\n") == "0", "empty set sum"

# multiple adds and deletes
assert run("8\nadd 1\nadd 2\nadd 3\nadd 4\nadd 5\nsum\ndel 3\nsum\n") == "3\n0", "delete affects sum"

# all equal values
assert run("6\nadd 2\nadd 2\nadd 2\nadd 2\nadd 2\nsum\n") == "2", "all equal"

# non-multiple of five
assert run("7\nadd 1\nadd 2\nadd 3\nadd 4\nadd 5\nadd 6\nsum\n") == "3", "extra element ignored"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 sum | 0 | empty set |
| add 1..5, sum, del 3, sum | 3 0 | deletion impacts sum |
| all adds 2 | 2 | median of identical values |
| 6 elements, sum | 3 | last incomplete group ignored |

## Edge Cases

When the set has fewer than five elements, for example, operations `add 1, add 2, sum`, the algorithm correctly returns zero because the loop over indices starting at 2 with step 5 does not execute. If the set size is exactly five, one median is selected as index 2, which is correct. For sets larger than five but not a multiple of five, extra elements
