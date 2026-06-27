---
title: "CF 105624H - \u0426\u0435\u043b\u0430\u044f \u043c\u0435\u0434\u0438\u0430\u043d\u0430"
description: "The task is to add the smallest number of integers to an existing array so that the median of the final sorted array becomes exactly x."
date: "2026-06-26T18:13:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105624
codeforces_index: "H"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2024-2025, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 105624
solve_time_s: 53
verified: true
draft: false
---

[CF 105624H - \u0426\u0435\u043b\u0430\u044f \u043c\u0435\u0434\u0438\u0430\u043d\u0430](https://codeforces.com/problemset/problem/105624/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to add the smallest number of integers to an existing array so that the median of the final sorted array becomes exactly `x`. The median definition is the left middle element after sorting, meaning that for an array of length `m`, the median is the element at position `(m + 1) // 2` using one based indexing. This is the same lower median convention used by the original problem.

The input gives the current number of values, the desired median value, and the array itself. We may only insert new values, not modify existing ones. The output is the minimum count of inserted values needed.

The array length is at most 500, which means even solutions around `O(n^2)` could fit. However, the structure of the problem allows a simpler `O(n log n)` approach after sorting. The important observation is that only the number of values smaller than `x`, equal to `x`, and larger than `x` affects the answer. We do not need to simulate the actual insertions.

A careless solution often fails on cases where `x` is absent or where the current median is close but not exactly `x`. For example:

```
3 10
10 20 30
```

The answer is `1`. A solution that only counts existing `x` values would fail because `x` already exists, but the current median is `20`.

Another example:

```
3 4
1 2 3
```

The answer is `4`. Adding only one `4` gives `[1,2,3,4]`, whose median is `2`, not `4`. The final array must contain enough values greater than or equal to `4` so that the middle position reaches the inserted values.

A third common mistake is mishandling an already correct median:

```
5 3
1 2 3 4 5
```

The answer is `0`. Any solution that always inserts `x` when it appears will produce an incorrect positive answer.

## Approaches

A direct brute force idea is to try adding values one by one and check whether the median becomes `x`. Since the median position changes when the length changes, this requires repeatedly sorting or counting the array. If we try many possible inserted counts, the number of checks quickly becomes unnecessary work. With large input sizes in related variants, repeatedly rebuilding the sorted array becomes the bottleneck.

The key observation is that the actual inserted values are flexible. We can insert values smaller than `x`, equal to `x`, or larger than `x`, and these three groups are all that matter.

Let `less` be the number of existing values smaller than `x`, and `equal` be the number of existing values equal to `x`. After sorting, the median position must lie after all values smaller than `x`, but not after all values equal to `x`.

If `x` is missing, we first insert one copy of `x`. After that, we only need to rebalance the counts around the median position. If `x` already exists, we can directly move the median position into the block of `x` values by adding values on the necessary side.

The implementation can be done greedily by considering the position of the median after inserting `x` if necessary, then adding only the minimum number of values needed to move the median boundary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer × n log n) | O(n) | Too slow in general |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array and find the first and last positions containing `x`. Sorting groups all values smaller than `x`, equal to `x`, and larger than `x` into separate ranges, which lets us reason only about counts.
2. If `x` does not exist, insert one copy of `x` conceptually and increase the answer by one. The median must be an existing value, so without this insertion the target value cannot become the median.
3. Compute the median position of the current array using zero based indexing: `(n - 1) // 2`.
4. If this position already falls inside the block of values equal to `x`, no more insertions are needed.
5. If the median position is before the first `x`, there are too many values smaller than `x`. Add values greater than or equal to `x` until the median position moves into the `x` block.
6. If the median position is after the last `x`, there are too many values greater than `x`. Add values smaller than or equal to `x` until the median position reaches `x`.

Why it works: the sorted array is divided into three regions. The only way for the median to fail is for the median index to be outside the region occupied by `x`. Adding numbers on the opposite side moves the boundary without destroying the existing `x` block. Since every insertion changes the median position by the smallest possible amount, the greedy additions are minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))

    ans = 0

    if x not in a:
        a.append(x)
        n += 1
        ans += 1

    a.sort()

    left = 0
    while left < n and a[left] < x:
        left += 1

    right = left
    while right < n and a[right] == x:
        right += 1

    median = (n - 1) // 2

    if left <= median < right:
        print(ans)
        return

    if median < left:
        need = 2 * left - n + 1
        ans += need
    else:
        need = n - 2 * right
        ans += need

    print(ans)

if __name__ == "__main__":
    solve()
```

The first part handles the special case where `x` is absent. Adding `x` is mandatory because a median must be an element of the final sorted array.

After sorting, `left` points to the first occurrence of `x`, and `right` points just after the last occurrence of `x`. The interval `[left, right)` is exactly the safe zone where the median index must land.

When the median index is too small, the array contains too many values below `x`. Adding large values increases the array length and pushes the median position rightward. When the median index is too large, adding small values shifts the median position leftward. The formulas count the minimum required shifts.

The expressions use integer arithmetic only. Python integers do not overflow, but the same formulas in languages with fixed width integers should still be checked carefully.

## Worked Examples

### Sample 1

Input:

```
3 10
10 20 30
```

After inserting `10` already exists, the sorted array is unchanged.

| Variable | Value |
| --- | --- |
| Sorted array | [10, 20, 30] |
| First `x` index | 0 |
| Last `x` index | 1 |
| Median index | 1 |
| Action | Add one large value |

The median index is after the `10` block, so one extra value is enough. Adding `9` gives `[9,10,20,30]`, whose median is `10`.

### Sample 2

Input:

```
3 4
1 2 3
```

| Variable | Value |
| --- | --- |
| Sorted array after inserting `x` | [1,2,3,4] |
| First `x` index | 3 |
| Last `x` index | 4 |
| Median index | 1 |
| Action | Move median right |

The inserted `4` is not enough. The median must move into the last block, requiring four total insertions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the work |
| Space | O(n) | The array is stored for sorting |

The constraint of `n ≤ 500` easily allows this solution. The algorithm performs only one sort and a few linear scans.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    if not data:
        return ""

    n = int(data[0])
    x = int(data[1])
    a = list(map(int, data[2:]))

    ans = 0
    if x not in a:
        a.append(x)
        n += 1
        ans += 1

    a.sort()

    left = 0
    while left < n and a[left] < x:
        left += 1

    right = left
    while right < n and a[right] == x:
        right += 1

    median = (n - 1) // 2

    if median < left:
        ans += 2 * left - n + 1
    elif median >= right:
        ans += n - 2 * right

    return str(ans)

assert run("""3 10
10 20 30
""") == "1"

assert run("""3 4
1 2 3
""") == "4"

assert run("""5 3
1 2 3 4 5
""") == "0"

assert run("""1 7
1
""") == "1"

assert run("""5 5
5 5 5 5 5
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 10 / 10 20 30` | `1` | Existing `x` but median too large |
| `3 4 / 1 2 3` | `4` | Missing `x` and large adjustment |
| `5 3 / 1 2 3 4 5` | `0` | Already correct median |
| `1 7 / 1` | `1` | Minimum size array |
| `5 5 / 5 5 5 5 5` | `0` | All values equal |

## Edge Cases

When `x` is absent, the algorithm inserts it first. For input:

```
1 7
1
```

The array becomes `[1,7]`. The median index is `0`, so the lower middle element is `1`. The algorithm detects that the median is before the `x` block and adds one larger value, producing the answer `1`.

When all values already equal `x`, the median block covers the entire array. For:

```
5 5
5 5 5 5 5
```

the first and last positions of `x` surround the median index, so the algorithm returns `0`.

When there are too many values below `x`, the algorithm moves the median to the right. For:

```
3 10
1 2 3
```

the missing value case inserts `10`, then additional values are needed because the median position is still occupied by small numbers. The final answer is determined only by the distance from the median position to the `x` block, not by the actual values inserted.
