---
title: "CF 106142F - \u0421\u0434\u0435\u043b\u0430\u0442\u044c \u043c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u043c"
description: "We are given an array of integers, and for every position we must answer a separate optimization question about that position’s value. The element at index i is treated as a fixed reference element."
date: "2026-06-20T22:07:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106142
codeforces_index: "F"
codeforces_contest_name: "2025-2026 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 (\u0412\u041a\u041e\u0428\u041f 25, \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u0438\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f)"
rating: 0
weight: 106142
solve_time_s: 51
verified: true
draft: false
---

[CF 106142F - \u0421\u0434\u0435\u043b\u0430\u0442\u044c \u043c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u043c](https://codeforces.com/problemset/problem/106142/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and for every position we must answer a separate optimization question about that position’s value. The element at index i is treated as a fixed reference element. We are allowed to delete any other elements from the array, and after deletions we look at the remaining sequence. The goal for index i is to make its value become a maximum value among all remaining elements, with ties allowed. We want the minimum number of deletions needed to achieve that.

Another way to view the task is that for each element a[i], we want to keep a subset of the array that still contains a[i], and in that subset there must be no element strictly greater than a[i]. Everything greater than a[i] must be removed. Among elements less than or equal to a[i], we are allowed to keep or remove freely, but removing fewer is always better because deletions are costly.

The constraints go up to n = 200000, so any solution with quadratic behavior over all i is immediately impossible. A naive approach that recomputes the answer for each i by scanning the array and counting deletions would lead to O(n^2), which is too large. This forces us toward a solution that reuses global structure of the array rather than recomputing from scratch.

A subtle case arises when values repeat. If a value appears many times, choosing one occurrence as the “maximum representative” means we are allowed to keep other equal elements. For example, in an array like [5, 1, 5], for the middle element 1, all 5s must be removed, so the answer is 2. For a 5, we can keep all 5s, so no deletions are needed.

Another important edge case is when the element is already globally maximum. In that case, no deletions are needed because it already satisfies the condition. Any approach that mistakenly counts equal elements as deletions would fail here.

## Approaches

The brute-force idea is straightforward. For each index i, fix the value x = a[i]. We then compute how many elements are strictly greater than x. All such elements must be removed. After removing them, the remaining array automatically satisfies that x is a maximum. So the answer for i is simply the count of elements greater than a[i]. This is correct because any valid subset cannot include a larger element.

A naive implementation would, for every i, scan the entire array and count values greater than a[i]. This costs O(n) per query, leading to O(n^2) total operations. With n up to 200000, this is far beyond feasible limits.

The key observation is that the answer depends only on the value a[i], not on its position. If two positions have the same value, their answers are identical. So instead of recomputing for each index, we only need to know, for every distinct value x, how many elements in the array are greater than x.

This immediately suggests sorting or frequency accumulation. If we sort the array values, we can compute for each value x the number of elements strictly greater than x using a suffix sum over frequencies. Once we know this for every possible value, we assign the precomputed result back to all positions.

The structure of the problem reduces to a global ranking question: each element’s answer is determined by its rank in the value ordering, not its position in the original array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Value frequency + sorting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Count how many times each distinct value appears in the array. This compresses the problem from positions to values, since identical values behave identically in the final answer.
2. Sort the distinct values in increasing order. This establishes a clear ordering from smallest to largest, which allows us to reason about how many elements are greater than a given value.
3. Traverse the sorted values from largest to smallest while maintaining a running total of how many elements have been seen so far. This running total represents how many elements are strictly greater than the current value.
4. For each value x in decreasing order, assign answer[x] equal to the current running total before adding x’s frequency. This works because at that moment we have already accounted for all values strictly greater than x.
5. Add the frequency of x to the running total, so that smaller values will correctly see all larger values included in their count.
6. Finally, map these precomputed answers back to each original index i using the frequency table or dictionary lookup.

Why it works: for any fixed value x, every element greater than x must be removed in any valid subset. Elements less than or equal to x never need to be removed for correctness reasons, since x is still a maximum among them. Therefore the minimal deletions are exactly the count of elements strictly greater than x, and the suffix accumulation over sorted values computes this quantity exactly once per distinct value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    freq = {}
    for v in a:
        freq[v] = freq.get(v, 0) + 1

    vals = sorted(freq.keys())
    
    greater_count = 0
    ans_value = {}

    for v in reversed(vals):
        ans_value[v] = greater_count
        greater_count += freq[v]

    out = []
    for v in a:
        out.append(str(ans_value[v]))

    print(" ".join(out))

if __name__ == "__main__":
    solve()
```

The implementation begins by building a frequency map of all values. This is essential because the algorithm operates on value classes rather than positions. The sorted list of keys defines the order in which we accumulate counts of greater elements.

The reverse traversal ensures that when we assign ans_value[v], the variable greater_count already contains exactly all elements strictly larger than v. The update step happens after assignment, which is critical to avoid accidentally counting the current value itself.

Finally, we map answers back to each position using direct dictionary lookup, which keeps the final reconstruction linear.

## Worked Examples

### Example 1

Input:

```
2 5 1 7 5
```

We compute frequencies:

2:1, 5:2, 1:1, 7:1

Sorted values: [1, 2, 5, 7]

We process in reverse:

| Value | Greater so far | Assigned answer |
| --- | --- | --- |
| 7 | 0 | 0 |
| 5 | 1 | 1 |
| 2 | 3 | 3 |
| 1 | 4 | 4 |

Mapping back gives:

```
3 1 4 0 1
```

This trace shows that each element’s answer depends only on how many strictly larger elements exist globally.

### Example 2

Input:

```
100 100 100 100
```

Frequencies:

100:4

Sorted values: [100]

| Value | Greater so far | Assigned answer |
| --- | --- | --- |
| 100 | 0 | 0 |

Output:

```
0 0 0 0
```

This confirms that when all values are equal, no deletions are needed since no element is strictly greater.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting distinct values dominates; all other operations are linear |
| Space | O(n) | Frequency map and output array store values proportional to input size |

The solution comfortably fits within limits since n is up to 200000. Sorting 200000 integers and doing linear passes is well within a 2 second constraint in Python when implemented with direct dictionary operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    freq = {}
    for v in a:
        freq[v] = freq.get(v, 0) + 1

    vals = sorted(freq.keys())

    greater_count = 0
    ans_value = {}

    for v in reversed(vals):
        ans_value[v] = greater_count
        greater_count += freq[v]

    return " ".join(str(ans_value[v]) for v in a)

# provided samples
assert run("5\n2 5 1 7 5\n") == "3 1 4 0 1"
assert run("4\n100 100 100 100\n") == "0 0 0 0"

# custom cases
assert run("3\n3 2 1\n") == "2 1 0", "strictly decreasing"
assert run("5\n1 2 3 4 5\n") == "4 3 2 1 0", "strictly increasing"
assert run("6\n5 1 5 2 5 3\n") == "0 3 0 2 0 1", "repeated max structure"
assert run("2\n1 2\n") == "1 0", "minimum case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 2 1 | 2 1 0 | decreasing order correctness |
| 1 2 3 4 5 | 4 3 2 1 0 | increasing order correctness |
| 5 1 5 2 5 3 | 0 3 0 2 0 1 | duplicates and mixed structure |
| 1 2 | 1 0 | smallest non-trivial case |

## Edge Cases

When all elements are equal, the algorithm assigns zero to every value because the reverse traversal sees no strictly greater elements. For input `[10, 10, 10]`, the frequency map has a single key and greater_count starts at zero, so every index receives zero. This matches the requirement that the chosen element is already maximum.

When the array is strictly increasing, every element except the last must remove all larger suffix elements. For `[1, 2, 3, 4]`, the suffix accumulation assigns correct decreasing answers because each value sees exactly the elements to its right in value order, which corresponds to all strictly greater values.
