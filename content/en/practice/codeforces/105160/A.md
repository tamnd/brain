---
title: "CF 105160A - \u6211\u662f\u7ec4\u9898\u4eba"
description: "We are given a list of problem difficulties, where each problem also has an implicit identifier given by its position in the input. The task is to reorder the problem indices according to difficulty from smallest to largest."
date: "2026-06-27T11:00:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105160
codeforces_index: "A"
codeforces_contest_name: "2024 University of Shanghai for Science and Technology(USST) Freshman Challenge Contest"
rating: 0
weight: 105160
solve_time_s: 51
verified: true
draft: false
---

[CF 105160A - \u6211\u662f\u7ec4\u9898\u4eba](https://codeforces.com/problemset/problem/105160/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of problem difficulties, where each problem also has an implicit identifier given by its position in the input. The task is to reorder the problem indices according to difficulty from smallest to largest. When two problems share the same difficulty, the one with the smaller original index must appear first.

The output is not the sorted difficulties themselves, but the sequence of original indices after sorting by this rule.

The input size is small, with at most 1000 problems. This immediately allows any approach around quadratic time or better. A solution that performs on the order of one million basic operations is completely safe, while anything involving repeated full scans inside another loop would still likely pass but is unnecessary.

A common mistake is to sort only the difficulty values without tracking indices, which loses the required output. Another mistake is to sort indices but forget the tie-break rule, which leads to incorrect ordering when equal values appear. For example, if input is `3 1 1`, the correct output is `2 3 1`, because the two `1`s keep their original order.

Another subtle edge case appears when all values are equal. If `a = [5, 5, 5]`, the output must be `1 2 3`, preserving original ordering entirely.

## Approaches

The brute-force way to think about this problem is to repeatedly search for the smallest remaining difficulty, mark it as used, and append its index to the result. Each selection requires scanning the full array to find the next minimum that has not been used yet. This is essentially a selection process repeated n times, and each scan costs O(n), leading to O(n²) total operations.

This approach is correct because it directly follows the sorting rule: always pick the smallest available element, and the scan naturally resolves ties by choosing the smallest index among equal values if implemented carefully. However, it becomes inefficient conceptually as it redundantly re-examines already processed elements many times.

The key observation is that the ordering rule is exactly what a standard sorting algorithm already provides if we package each element with its index. If we sort pairs `(ai, i)`, the sorting comparison first uses difficulty and automatically falls back to index order when difficulties are equal. This transforms the problem into a single sort over n items.

The improvement comes from recognizing that the structure is static. Nothing changes during processing, so we do not need incremental selection. A one-time global ordering is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Selection | O(n²) | O(n) | Accepted but unnecessary |
| Pair Sorting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer n and the array of difficulties. Each position implicitly represents a problem identifier starting from 1.
2. Construct a list of pairs where each element stores both the difficulty and its original index. This preserves the identity of each problem while enabling comparison.
3. Sort the list of pairs. The sorting rule first compares difficulty, and if two difficulties are equal, it compares indices. This ensures the required ordering is enforced in a single operation.
4. Traverse the sorted list and extract only the indices, producing the final output order.

### Why it works

Sorting imposes a global order consistent with the problem’s required ordering relation. The comparison function defines a total ordering where `(ai, i)` ensures that difficulty is the primary key and index is the tie-breaker. Once sorted, any two elements appear in correct relative order, and transitivity of sorting guarantees the entire sequence is consistent without needing further adjustment.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
a = list(map(int, input().split()))

pairs = []
for i in range(n):
    pairs.append((a[i], i + 1))

pairs.sort()

res = [str(idx) for _, idx in pairs]
print(" ".join(res))
```

The core idea in the implementation is the construction of `(value, index)` pairs. The index is shifted to be 1-based because the output expects problem numbering starting from 1.

The built-in sort in Python compares tuples lexicographically, meaning it automatically compares the first element, and only if they are equal does it compare the second element. This directly encodes the required tie-breaking rule without extra logic.

The final loop only extracts indices in order, converting them to strings for fast joining. Using `sys.stdin.readline` ensures input handling is efficient, although for n up to 1000 this is not strictly necessary.

## Worked Examples

### Example 1

Input:

```
5
3 1 1 4 2
```

We form pairs:

| Step | Pair list |
| --- | --- |
| Initial | (3,1), (1,2), (1,3), (4,4), (2,5) |
| After sort | (1,2), (1,3), (2,5), (3,1), (4,4) |

Extracted indices:

```
2 3 5 1 4
```

This shows that equal values 1 and 1 keep their relative index order, demonstrating correct tie handling.

### Example 2

Input:

```
4
2 2 2 2
```

Pairs:

| Step | Pair list |
| --- | --- |
| Initial | (2,1), (2,2), (2,3), (2,4) |
| After sort | (2,1), (2,2), (2,3), (2,4) |

Output:

```
1 2 3 4
```

This confirms that when all values are identical, the algorithm preserves original order exactly as required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting n pairs dominates runtime |
| Space | O(n) | Storage for pair list |

With n up to 1000, sorting at most 1000 elements is trivial. The algorithm runs comfortably within both time and memory limits, with a large safety margin.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n = int(input().strip())
    a = list(map(int, input().split()))
    pairs = [(a[i], i + 1) for i in range(n)]
    pairs.sort()
    return " ".join(str(idx) for _, idx in pairs)

# provided sample style case
assert run("5\n3 1 1 4 2\n") == "2 3 5 1 4"

# all equal
assert run("3\n5 5 5\n") == "1 2 3"

# already sorted
assert run("4\n1 2 3 4\n") == "1 2 3 4"

# reverse order
assert run("4\n4 3 2 1\n") == "4 3 2 1"

# minimum size
assert run("1\n7\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 3 1 1 4 2 | 2 3 5 1 4 | General sorting with tie handling |
| 3 5 5 5 | 1 2 3 | All equal stability |
| 4 1 2 3 4 | 1 2 3 4 | Already sorted case |
| 4 4 3 2 1 | 4 3 2 1 | Reverse ordering |
| 1 7 | 1 | Minimum input size |

## Edge Cases

When all difficulties are identical, such as input `5 5 5 5`, the algorithm constructs identical first elements in all pairs. The sort then falls back entirely on indices, preserving natural order. The output becomes `1 2 3 4 5`, matching the requirement that ties resolve by original position.

When the array is strictly increasing, such as `1 2 3 4`, sorting does not change the order of pairs at all. The algorithm still runs the same steps, but the output is identical to input indices in order.

When the array is strictly decreasing, such as `4 3 2 1`, the sorting fully reverses the structure. Each element moves to its correct position based on value, and since values are distinct, indices do not affect ordering.
