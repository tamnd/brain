---
title: "CF 166C - Median"
description: "We start with an array of integers and a target value x. We may append any number of extra integers to the array, and we want the median of the final array to become exactly x. The task is to compute the smallest number of added elements needed to make that happen."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 166
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 113 (Div. 2)"
rating: 1500
weight: 166
solve_time_s: 97
verified: true
draft: false
---

[CF 166C - Median](https://codeforces.com/problemset/problem/166/C)

**Rating:** 1500  
**Tags:** greedy, math, sortings  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array of integers and a target value `x`. We may append any number of extra integers to the array, and we want the median of the final array to become exactly `x`. The task is to compute the smallest number of added elements needed to make that happen.

The definition of median here follows Codeforces convention. After sorting the array, the median is the element at position `⌊(n + 1) / 2⌋` using 1-based indexing. For an array of even length, this means the left middle element is chosen.

The constraints are small enough that sorting repeatedly is completely affordable. The original array length is at most `500`, and every added element increases the size only slightly. Even an `O(n^2 log n)` solution would pass comfortably. The challenge is not performance, it is understanding exactly what conditions make `x` the median and how to achieve them with the fewest insertions.

The first subtle case appears when `x` does not exist in the array at all.

Example:

```
n = 3, x = 10
array = [20, 30, 40]
```

The answer is not `0`, even though we could imagine shifting positions somehow. If `10` is absent, the median can never become `10`, because the median must be an actual array element after sorting. We must insert at least one `10`.

Another easy mistake comes from misunderstanding which middle element is used for even lengths.

Example:

```
n = 4, x = 4
array = [1, 4, 5, 6]
```

Sorted order is:

```
[1, 4, 5, 6]
```

The median position is `⌊(4 + 1) / 2⌋ = 2`, so the median is `4`, not `5`. A careless implementation that uses the right middle element would produce the wrong answer.

A more subtle edge case happens when `x` already exists, but there are too many smaller elements before it.

Example:

```
n = 5, x = 4
array = [1, 2, 3, 4, 100]
```

The sorted array is:

```
[1, 2, 3, 4, 100]
```

The median is `3`, not `4`. We cannot fix this by inserting numbers smaller than `4`, because that only pushes `4` even farther right. The only useful additions are numbers greater than or equal to `4`, which shift the median position toward the occurrence of `4`.

The opposite scenario also matters.

Example:

```
n = 5, x = 10
array = [10, 20, 30, 40, 50]
```

The median is already `30`. Here, inserting large numbers does not help. We need smaller numbers to pull the median position leftward until it lands on `10`.

These directional effects are the key observation behind the solution.

## Approaches

A brute-force approach is surprisingly natural here. We can repeatedly test whether the current median equals `x`. If not, we insert one carefully chosen number and try again.

The simplest version works like this. Sort the array. If the median is smaller than `x`, insert another `x`. If the median is larger than `x`, also insert another `x`. Continue until the median becomes `x`.

This is correct because every insertion of `x` increases the number of occurrences of `x` and gradually pulls the median toward it. Since the constraints are tiny, even repeatedly sorting after every insertion is fast enough.

The weakness of this brute-force idea is conceptual rather than computational. It does not explain why the process works or what condition actually defines success. We need a clearer characterization.

The important observation is that after sorting, some occurrence of `x` must occupy the median position. Suppose we sort the array and look at the first occurrence of `x`.

If that occurrence lies to the left of the median position, then there are too many elements greater than `x`. We must add smaller numbers to shift the median index left relative to `x`.

If that occurrence lies to the right of the median position, then there are too many elements smaller than `x`. We must add larger numbers to shift the median index right relative to `x`.

A cleaner way to implement this is even simpler. We keep inserting `x` itself until the median becomes `x`.

Why does this work? Adding `x` never changes the relative ordering between smaller and larger values. It only increases the block of equal values. Eventually, the median index must fall inside that block.

Since at most a few hundred insertions are needed, repeatedly sorting is perfectly acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k · n log n) | O(n) | Accepted |
| Optimal | O(k · n log n) | O(n) | Accepted |

Here, `k` is the number of inserted elements. Under the given constraints, `k` remains small.

## Algorithm Walkthrough

1. Read the array and insert one copy of `x` immediately if the array does not already contain it.

This step is mandatory because the median must equal an actual array element.
2. Sort the array.

The median depends only on sorted order, so every check must happen after sorting.
3. Compute the median index as `(len(array) - 1) // 2`.

This is the zero-based version of the problem's definition.
4. Check whether the median element equals `x`.

If it does, stop immediately. The current number of insertions is minimal because we only inserted when necessary.
5. If the median is smaller than `x`, append another `x`.

This increases the number of elements greater than or equal to `x`, pushing the median value upward.
6. If the median is larger than `x`, also append another `x`.

This increases the number of elements less than or equal to `x`, pushing the median value downward.
7. Repeat from step 2 until the median becomes `x`.

### Why it works

Each insertion adds another copy of `x`, expanding the contiguous block of `x` values in sorted order. The median position changes as the array grows, but the block of `x` values also grows. Eventually, the median index lands inside that block.

Since every operation increases the count of `x` by exactly one, no smaller sequence of operations could make the median become `x` earlier. The first moment when the median equals `x` is necessarily optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, x = map(int, input().split())
arr = list(map(int, input().split()))

added = 0

while True:
    arr.sort()

    median = arr[(len(arr) - 1) // 2]

    if median == x:
        print(added)
        break

    arr.append(x)
    added += 1
```

The implementation is intentionally compact because the underlying idea is simple.

The loop always begins by sorting the array. Since the median depends on sorted order, checking before sorting would be meaningless.

The median index uses:

```
(len(arr) - 1) // 2
```

This matches the problem's left-middle definition for even lengths. Using `len(arr) // 2` would incorrectly select the right middle element and fail on many cases.

Whenever the median is not `x`, we append another `x`. There is no need to distinguish whether the median is too small or too large. Adding `x` helps in both directions because it enlarges the block of equal values.

The variable `added` tracks how many numbers we inserted. Since every loop iteration inserts exactly one value, the first successful state is automatically minimal.

## Worked Examples

### Example 1

Input:

```
3 10
10 20 30
```

Initial array:

```
[10, 20, 30]
```

| Step | Sorted Array | Median Index | Median Value | Action |
| --- | --- | --- | --- | --- |
| 1 | [10, 20, 30] | 1 | 20 | append 10 |
| 2 | [10, 10, 20, 30] | 1 | 10 | stop |

Answer:

```
1
```

This example shows how adding one occurrence of `x` expands its range in sorted order until the median index falls onto it.

### Example 2

Input:

```
5 4
1 2 3 4 100
```

Initial array:

```
[1, 2, 3, 4, 100]
```

| Step | Sorted Array | Median Index | Median Value | Action |
| --- | --- | --- | --- | --- |
| 1 | [1, 2, 3, 4, 100] | 2 | 3 | append 4 |
| 2 | [1, 2, 3, 4, 4, 100] | 2 | 3 | append 4 |
| 3 | [1, 2, 3, 4, 4, 4, 100] | 3 | 4 | stop |

Answer:

```
2
```

This trace demonstrates the case where too many smaller elements initially push `x` to the right of the median position. Repeated insertions gradually move the median index into the block of `4`s.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k · n log n) | The array is sorted after each insertion |
| Space | O(n) | The array itself stores all elements |

With `n ≤ 500`, repeated sorting is easily fast enough. Even if we inserted hundreds of elements, the total amount of work would remain tiny compared to the 2-second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, x = map(int, input().split())
    arr = list(map(int, input().split()))

    added = 0

    while True:
        arr.sort()

        median = arr[(len(arr) - 1) // 2]

        if median == x:
            return str(added)

        arr.append(x)
        added += 1

# provided sample
assert run("3 10\n10 20 30\n") == "1", "sample 1"

# already correct
assert run("5 3\n1 2 3 4 5\n") == "0", "already median"

# x absent initially
assert run("3 5\n1 2 3\n") == "4", "x missing"

# single element
assert run("1 7\n7\n") == "0", "minimum size"

# all equal but wrong value
assert run("4 10\n1 1 1 1\n") == "5", "all values smaller"

# even length left-middle check
assert run("4 4\n1 4 5 6\n") == "0", "left middle median"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 3 / 1 2 3 4 5` | `0` | Median already correct |
| `3 5 / 1 2 3` | `4` | Missing `x` must first be inserted |
| `1 7 / 7` | `0` | Minimum-size array |
| `4 10 / 1 1 1 1` | `5` | Many insertions required |
| `4 4 / 1 4 5 6` | `0` | Correct left-middle definition |

## Edge Cases

Consider the case where `x` is absent.

Input:

```
3 5
1 2 3
```

Execution:

```
[1, 2, 3] -> median = 2
append 5

[1, 2, 3, 5] -> median = 2
append 5

[1, 2, 3, 5, 5] -> median = 3
append 5

[1, 2, 3, 5, 5, 5] -> median = 3
append 5

[1, 2, 3, 5, 5, 5, 5] -> median = 5
```

Output:

```
4
```

The algorithm succeeds because every insertion enlarges the block of `5`s until the median index reaches it.

Now consider the even-length definition.

Input:

```
4 4
1 4 5 6
```

Sorted array:

```
[1, 4, 5, 6]
```

Median index:

```
(4 - 1) // 2 = 1
```

Median value:

```
4
```

Output:

```
0
```

A wrong implementation using index `len(arr) // 2` would choose `5` instead and incorrectly continue inserting elements.

Finally, consider a case where `x` is far to the left.

Input:

```
5 10
10 20 30 40 50
```

Execution:

```
[10, 20, 30, 40, 50] -> median = 30
append 10

[10, 10, 20, 30, 40, 50] -> median = 20
append 10

[10, 10, 10, 20, 30, 40, 50] -> median = 20
append 10

[10, 10, 10, 10, 20, 30, 40, 50] -> median = 10
```

Output:

```
3
```

Adding copies of `10` shifts the median position leftward relative to the larger values until it lands inside the `10` block.
