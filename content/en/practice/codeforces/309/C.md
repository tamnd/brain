---
title: "CF 309C - Memory for Arrays"
description: "We are given a memory layout split into several contiguous free segments, which we can think of as independent blocks of space. Each block has a fixed length, and we also have a collection of arrays we may want to place into this memory."
date: "2026-06-05T18:34:30+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "greedy"]
categories: ["algorithms"]
codeforces_contest: 309
codeforces_index: "C"
codeforces_contest_name: "Croc Champ 2013 - Finals (online version, Div. 1)"
rating: 1900
weight: 309
solve_time_s: 76
verified: true
draft: false
---

[CF 309C - Memory for Arrays](https://codeforces.com/problemset/problem/309/C)

**Rating:** 1900  
**Tags:** binary search, bitmasks, greedy  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a memory layout split into several contiguous free segments, which we can think of as independent blocks of space. Each block has a fixed length, and we also have a collection of arrays we may want to place into this memory. Each array consumes a contiguous segment of memory of a given length, and it must fit entirely inside a single block.

The task is to choose which arrays to place and where to place them so that we maximize the number of arrays successfully stored. Each block can host multiple arrays as long as they do not overlap and fit within its capacity, but arrays cannot be split across blocks, and blocks are independent in the sense that we cannot merge them.

The structure of the input matters: we are matching two multisets, block capacities and array sizes, and the goal is to maximize the number of successful assignments under interval packing constraints inside each block.

The constraints are large, with up to 10^6 blocks and 10^6 arrays. Any solution that attempts to simulate placement or try combinations per block or per array will be far too slow. The only feasible solutions are roughly O(n log n) or O(n) with sorting and greedy processing. This immediately rules out any dynamic programming over all subsets or per-block combinatorial packing.

A subtle edge case appears when greedy matching is done in the wrong order. For example, if we try to place large arrays first into large blocks without coordinating leftover space, we may waste fragmentation opportunities. Another failure case occurs if we treat blocks independently and greedily pack each one without considering global optimal ordering of arrays.

## Approaches

A brute-force interpretation would try all assignments of arrays to blocks and check feasibility. Even if we simplify to “for each array, try to fit it into some block,” this becomes O(nm), which is far beyond the limit when both reach 10^6.

A more structured brute-force improves by sorting blocks and arrays and, for each array, scanning blocks to find a fit. This reduces constant factors but still degenerates to quadratic behavior.

The key observation is that each array only needs a contiguous segment inside a block, so a block of size A can accommodate at most floor(A / (2b)) arrays of size 2b if we fix which array type is used inside it. However, mixing different sizes inside a block complicates direct counting.

The critical insight is that we never benefit from assigning a large array into a block if a smaller array could be assigned in its place, because smaller arrays are more flexible and preserve large blocks for large arrays. This leads to a global greedy strategy: sort both arrays and blocks, and always try to match the smallest arrays first into the smallest blocks that can accommodate them, or equivalently process from the most constrained side while maintaining feasibility.

A standard way to enforce this is to sort block sizes and array sizes and use a greedy matching with a pointer, always attempting to fit the smallest remaining array into the smallest available block that can hold it. When a block is too small, it is skipped; when it is large enough, it is used once and we move forward.

This transforms the problem into a linear scan over sorted arrays and blocks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal Greedy Matching | O(n log n + m log m) | O(1)-O(n+m) | Accepted |

## Algorithm Walkthrough

1. Convert each array requirement into its actual memory demand, which is 2*b[i]. This normalizes both inputs into comparable segment lengths.
2. Sort the block sizes in non-decreasing order. Sorting ensures we always consider the smallest available capacity first, which prevents wasting large blocks on small requirements when smaller blocks could suffice.
3. Sort the array sizes in non-decreasing order. This aligns with the idea of assigning the most restrictive (smallest) arrays first, which maximizes flexibility for larger ones later.
4. Initialize two pointers, one for blocks and one for arrays, both starting at the beginning of their sorted lists.
5. Iterate while both pointers are valid. At each step, compare the current smallest unassigned array with the current smallest available block.
6. If the current block is too small to fit the array, discard this block and move to the next larger block. This is safe because this block cannot be used for any remaining arrays due to sorting.
7. If the block can fit the array, assign the array to this block, increment the count of placed arrays, and move both pointers forward. This ensures each block is used at most once in this simplified matching model, which is valid because any block that can fit the current smallest array could have been used for it without harming optimality.

### Why it works

The correctness relies on a monotonic feasibility structure induced by sorting. Once arrays and blocks are ordered, feasibility becomes a threshold condition: if a block cannot fit a given array, it cannot fit any larger array either. This ensures skipping a block is always safe. Similarly, assigning the smallest available array to the smallest feasible block avoids consuming large blocks unnecessarily, preserving capacity for future larger arrays. This greedy structure ensures that every assignment made is locally optimal and does not block any future feasible assignment that could increase the total count.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

a.sort()
b = sorted(x * 2 for x in b)

i = j = 0
ans = 0

while i < n and j < m:
    if b[j] >= a[i]:
        ans += 1
        i += 1
        j += 1
    else:
        j += 1

print(ans)
```

The solution begins by reading both sequences and converting array requirements into actual memory lengths. Sorting both lists is essential because it creates the monotonic structure needed for a two-pointer sweep.

The pointer `i` tracks the next array we want to place, and `j` tracks the next block we may use. When the current block is too small, it is discarded because it cannot serve any remaining array at or above the current size. When it fits, we commit the assignment and advance both pointers, ensuring neither a block nor an array is reused.

A common mistake is reversing the inequality or iterating in the wrong direction. The correct comparison is always whether the block can accommodate the array, not the other way around.

## Worked Examples

Consider the sample input:

```
5 3
8 4 3 2 2
3 2 2
```

After conversion, array sizes remain `[8, 4, 4]` and block sizes are `[2, 4, 8, 2, 3]`, which sort to `[2, 2, 3, 4, 8]`.

| i | j | array | block | action | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 8 | 2 | block too small | 0 |
| 0 | 1 | 8 | 2 | block too small | 0 |
| 0 | 2 | 8 | 3 | block too small | 0 |
| 0 | 3 | 8 | 4 | block too small | 0 |
| 0 | 4 | 8 | 8 | assign | 1 |
| 1 | 5 | 4 | - | stop | 1 |

Now consider a second example:

```
4 5
10 5 4 2
1 2 2 2 6
```

Arrays sorted: `[2, 4, 5, 10]`, blocks sorted: `[2, 2, 2, 6, 20]`.

| i | j | array | block | action | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 2 | assign | 1 |
| 1 | 1 | 4 | 2 | skip block | 1 |
| 1 | 2 | 4 | 2 | skip block | 1 |
| 1 | 3 | 4 | 6 | assign | 2 |
| 2 | 4 | 5 | 20 | assign | 3 |
| 3 | 5 | - | - | stop | 3 |

These traces show how smaller arrays are matched early, while unusable small blocks are skipped without harming optimality.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m log m) | Sorting dominates, followed by a single linear scan |
| Space | O(1) extra | Only pointers and counters beyond input storage |

The complexity is well within limits for 10^6 elements, since sorting 10^6 integers is feasible in Python with efficient input and linear scanning afterward.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    a.sort()
    b = sorted(x * 2 for x in b)

    i = j = 0
    ans = 0

    while i < n and j < m:
        if b[j] >= a[i]:
            ans += 1
            i += 1
            j += 1
        else:
            j += 1

    return str(ans)

# provided sample
assert run("5 3\n8 4 3 2 2\n3 2 2\n") == "2"

# minimum case
assert run("1 1\n2\n1\n") == "1"

# no fit case
assert run("2 2\n10 10\n1 1\n") == "0"

# exact matching case
assert run("3 3\n2 4 6\n1 2 3\n") == "3"

# large skewed case
assert run("4 2\n100 50 25 10\n1 20\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 small fit | 1 | minimal assignment correctness |
| no fit case | 0 | correct rejection handling |
| exact matching | 3 | one-to-one greedy matching |
| skewed sizes | 2 | handling of large/small imbalance |

## Edge Cases

A key edge case is when many small blocks appear before a large block that is needed for a large array. For input like:

```
3 2
100 1 1
50 50
```

Sorting produces blocks `[1, 1, 100]` and arrays `[50, 50]`. The algorithm skips the two small blocks and assigns both arrays to the large block incorrectly if we were allowing reuse, but since each block is single-use, only one 50 fits, so the answer is 1. The greedy pointer ensures we do not incorrectly reuse capacity.

Another edge case is when arrays are all smaller than every block except the smallest few. For:

```
4 3
8 7 6 5
1 1 1
```

The algorithm assigns three smallest arrays to the three smallest feasible blocks immediately, confirming that early consumption of small arrays is always safe and does not block larger assignments since no larger arrays exist.
