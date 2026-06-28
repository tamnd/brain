---
title: "CF 104745C - Maximum profit"
description: "We are given a sequence of bank checks, each with a fixed monetary value. From this sequence, we are allowed to pick at most k checks in a single day, and our goal is to maximize the total value of the selected checks."
date: "2026-06-28T23:01:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104745
codeforces_index: "C"
codeforces_contest_name: "CAMA 2023"
rating: 0
weight: 104745
solve_time_s: 49
verified: true
draft: false
---

[CF 104745C - Maximum profit](https://codeforces.com/problemset/problem/104745/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of bank checks, each with a fixed monetary value. From this sequence, we are allowed to pick at most `k` checks in a single day, and our goal is to maximize the total value of the selected checks. There is no restriction on which checks we pick other than the limit on how many we can take.

The input describes two things: the number of available checks `n`, and the maximum number `k` that can be redeemed. Then follows an array of `n` integers representing the value of each check. The output is a single number, the largest possible sum we can obtain by selecting no more than `k` elements from the array.

The constraint `n ≤ 10^4` means that even quadratic solutions like checking all subsets or simulating combinations will be too slow. An `O(n^2)` approach already risks around 10^8 operations, which is borderline in Python for a strict 1-second limit. Anything exponential is immediately impossible.

The structure of the problem hides no ordering requirement. We are not required to pick contiguous checks or preserve stack order. Any subset of size up to `k` is valid, which simplifies the problem into a pure selection task.

The main edge cases come from understanding the phrase “at most k checks.” For example, if `k = n`, we must take all elements. If `k = 1`, we simply choose the maximum single value.

Consider these scenarios:

Input:

```
5 1
3 10 2 8 7
```

Output:

```
10
```

A naive approach might try combinations, but the correct answer is just the maximum element.

Input:

```
4 4
1 2 3 4
```

Output:

```
10
```

Here, we must take everything since the limit allows all elements.

Any incorrect approach typically comes from misunderstanding whether the selection is constrained by position or order. In this problem, it is purely combinatorial.

## Approaches

A brute-force interpretation would try every subset of at most `k` elements, compute its sum, and track the best result. This is correct because it directly matches the definition of the task, but the number of subsets is enormous. Even restricting to exactly `k` elements gives $\binom{n}{k}$, which grows too quickly to enumerate once `n` reaches even a few dozen.

The key observation is that the order of elements is irrelevant. The sum of any chosen subset depends only on which values are included, not their positions. This reduces the task to selecting the largest `k` values from the array. Any optimal solution must include the largest elements because replacing a smaller chosen element with a larger unused one always improves or preserves the total.

This transforms the problem into a classic selection problem: either sort the array and take the top `k` values, or maintain a running structure that tracks the `k` largest elements.

Sorting is the simplest and most direct approach. After sorting in descending order, the answer is just the sum of the first `k` elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Sorting Top k | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

We solve the problem by focusing on the fact that only the largest values contribute to an optimal selection.

1. Read `n` and `k`, then read the list of check values. This defines the full pool of candidates we can choose from.
2. Sort the list in descending order so that the largest values appear first. This step ensures that the best candidates are positioned at the front, making selection trivial.
3. Take the first `k` elements from the sorted list. These correspond to the highest possible values available.
4. Compute the sum of these `k` elements and output it as the answer.

Each step reduces the problem complexity: instead of reasoning about subsets, we reduce it to ordering and slicing, which is deterministic after sorting.

### Why it works

The correctness comes from a simple exchange argument. Suppose an optimal selection includes some element `a` while excluding a larger element `b` not in the selection. Replacing `a` with `b` increases the total sum without violating the constraint of selecting at most `k` elements. Repeating this replacement process ensures that any optimal solution can be transformed into one that consists exactly of the `k` largest values. Therefore, selecting the top `k` after sorting is always optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    arr.sort(reverse=True)
    print(sum(arr[:k]))

if __name__ == "__main__":
    solve()
```

The solution reads input using fast I/O since Python’s default input can be slow for large arrays. The sorting step places larger values first. The slice `arr[:k]` extracts exactly the number of allowed checks, and summing them produces the optimal total.

A subtle detail is ensuring that we do not accidentally include more than `k` elements. Since slicing is exclusive of bounds and safe even when `k = n`, this avoids edge-case handling entirely.

## Worked Examples

### Example 1

Input:

```
3 2
11 5 10
```

Sorted array: `[11, 10, 5]`

| Step | Array state | Chosen elements | Sum |
| --- | --- | --- | --- |
| After sorting | 11 10 5 | - | 0 |
| Take first k=2 | 11 10 | 11 10 | 21 |

This demonstrates how sorting directly exposes the optimal subset without any combinatorial reasoning.

### Example 2

Input:

```
5 3
4 1 7 3 9
```

Sorted array: `[9, 7, 4, 3, 1]`

| Step | Array state | Chosen elements | Sum |
| --- | --- | --- | --- |
| After sorting | 9 7 4 3 1 | - | 0 |
| Take first k=3 | 9 7 4 | 9 7 4 | 20 |

This confirms that even when large values are scattered in the original array, sorting normalizes the structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, summation is linear |
| Space | O(1) | Sorting is in-place aside from input storage |

The constraints `n ≤ 10^4` make an `n log n` approach easily fast enough, since this is at most about 10^5 operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    arr.sort(reverse=True)
    return str(sum(arr[:k]))

# provided sample
assert run("3 2\n11 5 10\n") == "21"

# minimum n
assert run("1 1\n7\n") == "7"

# k = n
assert run("4 4\n1 2 3 4\n") == "10"

# all equal
assert run("5 3\n5 5 5 5 5\n") == "15"

# mixed values
assert run("6 2\n-1 10 3 7 2 8\n") == "18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 7 | 7 | minimum size case |
| 4 4 / 1 2 3 4 | 10 | selecting all elements |
| 5 3 / all 5s | 15 | uniform values |
| mixed array | 18 | correct greedy selection |

## Edge Cases

A key edge case is when `k` equals `n`. The algorithm sorts the array and takes all elements. Since slicing does not truncate beyond bounds, the sum naturally includes every value.

For input:

```
4 4
3 1 4 2
```

After sorting:

`[4, 3, 2, 1]`

We take all 4 elements:

sum = 10

This matches the requirement because selecting at most `k` allows using the entire set.

Another edge case is when `k = 1`. The algorithm reduces to selecting the maximum element. Sorting guarantees it is at position zero.

For input:

```
5 1
2 9 1 8 3
```

Sorted:

`[9, 8, 3, 2, 1]`

We take only the first element, producing 9, which is optimal by definition since any other choice would be smaller.
