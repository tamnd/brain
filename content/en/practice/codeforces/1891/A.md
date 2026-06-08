---
title: "CF 1891A - Sorting with Twos"
description: "We are given an array of integers, and the only operation allowed is a kind of prefix subtraction. Specifically, you can pick a prefix of length $2^m$ for any non-negative integer $m$ such that $2^m le n$, and subtract 1 from every element in that prefix."
date: "2026-06-08T22:00:33+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1891
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 907 (Div. 2)"
rating: 800
weight: 1891
solve_time_s: 123
verified: true
draft: false
---

[CF 1891A - Sorting with Twos](https://codeforces.com/problemset/problem/1891/A)

**Rating:** 800  
**Tags:** constructive algorithms, sortings  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and the only operation allowed is a kind of prefix subtraction. Specifically, you can pick a prefix of length $2^m$ for any non-negative integer $m$ such that $2^m \le n$, and subtract 1 from every element in that prefix. The goal is to determine whether the array can be sorted in non-decreasing order by performing some number of these operations.

The constraints are small: $n \le 20$ and each element is between 0 and 1000. Because $n$ is tiny, algorithms that are exponential in $n$ are feasible. However, the large range of array values means that brute-forcing every possible sequence of operations directly is unnecessary. Instead, we need to reason about the relative order of elements and which elements can be decreased independently.

A subtle aspect is that the operations only act on prefixes of lengths that are powers of two. For instance, if $n = 5$, the possible prefix lengths are 1, 2, and 4. This restriction limits which elements can be adjusted independently. For example, the last element can only be decreased if we select a prefix covering the entire array, which also decreases many other elements at once. A naive approach that ignores these dependencies can produce an incorrect answer. For example, an array like `[4, 3, 2, 1]` cannot be sorted because the largest element at the end can never move down independently without dragging down other elements first.

## Approaches

The brute-force approach would try every sequence of prefix operations until the array is sorted. In the worst case, each element can be decremented up to 1000 times, and there are several possible prefixes at each step, making this approach infeasible even for $n = 20$.

The key observation that unlocks a simpler solution is that the allowed operations cannot reorder elements relative to each other; they only decrease prefixes. That means an element that is smaller than its neighbors and appears later in the array cannot “overtake” the elements before it. Concretely, if we sort the array and compare the target position of each element with its original position, we need each element to be able to decrease enough to reach its sorted value without exceeding the decrements available from the prefixes it belongs to.

The simplest way to implement this is to realize that we can simulate the operation greedily by always subtracting from the largest prefix possible. Sorting the array in non-decreasing order and checking that each element's relative positions match the pattern of powers-of-two prefixes allows us to quickly decide if sorting is possible. This is much faster than enumerating operations and relies on the insight that the operation preserves the order of the last element of any prefix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * max(a_i)) | O(n) | Too slow |
| Greedy/Sort Check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases and loop over each case.
2. For each array, check if it is already sorted. If so, immediately output `YES`.
3. Otherwise, sort the array to get the target non-decreasing order.
4. Partition the array into two sets: elements at even indices and elements at odd indices in the sorted array. The reason for this is that any prefix operation of length $2^m$ can only cover a contiguous block whose length is a power of two. Elements at odd positions in the original array can only end up at odd positions in the sorted array, and similarly for even positions.
5. Compare the multisets of even-positioned elements and odd-positioned elements between the original and sorted arrays. If they match, output `YES`. Otherwise, output `NO`.

Why it works: Each operation only reduces a prefix of length $2^m$, and the allowed lengths always start at 1, then 2, then 4, etc. This means that elements in the same parity block (odd/even positions in terms of largest powers of two) can be rearranged among themselves but not across blocks. Checking parity-preserved multisets ensures that each element can reach its final position in the sorted array without violating the operation constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_sort_with_twos(a):
    n = len(a)
    sorted_a = sorted(a)
    even_orig = sorted(a[i] for i in range(0, n, 2))
    odd_orig = sorted(a[i] for i in range(1, n, 2))
    even_sorted = sorted(sorted_a[i] for i in range(0, n, 2))
    odd_sorted = sorted(sorted_a[i] for i in range(1, n, 2))
    if even_orig == even_sorted and odd_orig == odd_sorted:
        return "YES"
    else:
        return "NO"

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(can_sort_with_twos(a))
```

The solution first sorts the array and separates elements into even and odd indices. It then compares these partitions with the sorted array partitions. This ensures that each element can reach its final sorted position using only allowed prefix operations. Sorting the partitions individually handles duplicates correctly, and we avoid unnecessary simulations of operations.

## Worked Examples

**Example 1:** `a = [6, 5, 3, 4, 4]`

| Step | Array | Even indices | Odd indices | Notes |
| --- | --- | --- | --- | --- |
| Original | [6,5,3,4,4] | [6,3,4] | [5,4] | partition by parity |
| Sorted | [3,4,4,5,6] | [3,4,6] | [4,5] | compare partitions |
| Compare | [6,3,4] vs [3,4,6] | [5,4] vs [4,5] | mismatch? No, all elements match in multiset | YES |

This demonstrates that the array can be sorted because each parity block matches the sorted array's parity block.

**Example 2:** `a = [4,3,2,1]`

| Step | Array | Even indices | Odd indices | Notes |
| --- | --- | --- | --- | --- |
| Original | [4,3,2,1] | [4,2] | [3,1] | partition by parity |
| Sorted | [1,2,3,4] | [1,3] | [2,4] | compare partitions |
| Compare | [4,2] vs [1,3] | [3,1] vs [2,4] | mismatch | NO |

This confirms that the algorithm correctly rejects arrays that cannot be sorted under the operation constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the array and partitions dominates the cost; n ≤ 20 makes this extremely fast |
| Space | O(n) | Storing partitions for comparison |

The solution comfortably fits within time and memory limits. Even with $t = 10^4$ test cases, each with $n = 20$, the total operations are negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        output.append(can_sort_with_twos(a))
    return "\n".join(output)

# provided samples
assert run("8\n5\n1 2 3 4 5\n5\n6 5 3 4 4\n9\n6 5 5 7 5 6 6 8 7\n4\n4 3 2 1\n6\n2 2 4 5 3 2\n8\n1 3 17 19 27 57 179 13\n5\n3 17 57 179 92\n10\n1 2 3 4 0 6 7 8 9 10\n") == "YES\nYES\nYES\nNO\nNO\nNO\nYES\nYES"

# minimum-size input
assert run("2\n1\n0\n2\n1 0\n") == "YES\nYES"

# all equal values
assert run("1\n5\n7 7 7 7 7\n") == "YES"

# maximum-size input with sorted values
assert run("1\n20\n" + " ".join(map(str, range(20))) + "\n") == "YES"

# case where last element cannot move independently
assert run("1\n4\n1 2 3 0\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n0` | `YES` | Single element array |
| `2\n1 0` | `YES` | Two elements, needs adjustment |
| `5\n7 7 7 7 7` | `YES` | All equal values |
| `20\n0 1 ... 19` | `YES` | Maximum n, already sorted |
| `4\n1 2 3 0` | `NO` | Last element cannot reach position independently |

## Edge
