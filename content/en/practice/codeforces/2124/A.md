---
title: "CF 2124A - Deranged Deletions"
description: "We are given an array and may delete any number of elements while preserving the relative order of the remaining ones. After the deletions, the remaining sequence must be non-empty."
date: "2026-06-08T03:31:30+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2124
codeforces_index: "A"
codeforces_contest_name: "EPIC Institute of Technology Round Summer 2025 (Codeforces Round 1036, Div. 1 + Div. 2)"
rating: 800
weight: 2124
solve_time_s: 129
verified: false
draft: false
---

[CF 2124A - Deranged Deletions](https://codeforces.com/problemset/problem/2124/A)

**Rating:** 800  
**Tags:** greedy, sortings  
**Solve time:** 2m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and may delete any number of elements while preserving the relative order of the remaining ones. After the deletions, the remaining sequence must be non-empty.

A sequence is called a derangement if, after sorting a copy of it in non-decreasing order, every position changes value. In other words, if the remaining array is `b` and its sorted version is `c`, then we need `b[i] != c[i]` for every index.

The task is not to maximize or minimize anything. We only need to determine whether some subsequence of the original array forms a derangement, and if it does, output any such subsequence.

The constraints are very small. Each test case has at most 100 elements, and there are at most 100 test cases. Even algorithms with quadratic or cubic complexity are completely safe. This means we should focus on finding a simple structural observation rather than worrying about heavy optimization.

The main difficulty is understanding what kind of subsequence can ever become a derangement.

Consider the array `[1, 1, 1]`. Every non-empty subsequence consists only of ones. After sorting, it remains unchanged, so no derangement exists.

Consider `[2, 1]`. The whole array becomes `[1, 2]` after sorting. Both positions change, so the answer is YES.

A subtle case is `[2, 2, 3]`. The sorted order is already `[2, 2, 3]`. Deleting the `3` gives `[2, 2]`, which is still unchanged after sorting. Deleting one of the `2`s gives `[2, 3]`, whose sorted order is also `[2, 3]`. Every non-empty subsequence fails, so the answer is NO.

A careless approach might try to use the entire array whenever it is not already sorted. That fails on inputs such as `[3, 1, 2]`. The whole array is not a derangement because after sorting we get `[1, 2, 3]` and the middle element becomes `2`, matching its sorted position. We must verify every position, not merely check that the array differs from its sorted version.

## Approaches

The most direct brute-force idea is to examine every non-empty subsequence. For each subsequence, sort a copy and check whether every position differs. This is obviously correct because it tests every possible answer.

The problem is that an array of length `n` has `2^n - 1` non-empty subsequences. Even for `n = 100`, this is completely impossible.

The key observation comes from looking at the smallest element.

Let `mn` be the minimum value in the current sequence. After sorting, all occurrences of `mn` must appear at the beginning. If a position already contains `mn` and remains among the first positions after sorting, that position can never differ from its sorted value.

Suppose we choose all elements of some subsequence and sort them. If an element is already in the same position as it would be in the sorted order, the derangement condition fails.

A much simpler way to think about the problem is to sort the original array and compare it with the original order. Every index where

`a[i] != sorted_a[i]`

is "good", because that element already differs from what the sorted sequence would place there.

Every index where

`a[i] == sorted_a[i]`

is "bad", because if we keep that position, it immediately violates the derangement condition.

This suggests taking exactly the positions where the original array differs from its sorted version. Let those elements form a subsequence `d`.

For every retained position, the original value and the sorted value are different. The sorted multiset of `d` is precisely the corresponding values taken from the sorted array. Hence every position of `d` differs from its position in its sorted version, making `d` a valid derangement.

If no such positions exist, then the array is already equal to its sorted version. In that case every element matches its sorted position, and no valid subsequence can be formed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n log n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array `a`.
2. Create a sorted copy `b = sorted(a)`.
3. Find every index `i` such that `a[i] != b[i]`.

These are exactly the positions that already disagree with the sorted arrangement.
4. Collect the corresponding values `a[i]` into a new array `ans`.
5. If `ans` is empty, print `NO`.

This means the original array was already identical to its sorted version, so no derangement subsequence exists.
6. Otherwise print `YES`, the length of `ans`, and the elements of `ans`.

### Why it works

Let `S` be the set of indices where `a[i] != b[i]`, where `b` is the sorted version of `a`.

We construct `ans` using exactly those positions.

The sorted version of `ans` is obtained by taking the elements `b[i]` for the same indices `i ∈ S`. This follows from the fact that `b` is the globally sorted arrangement of the same multiset.

For every retained position, we have `a[i] != b[i]` by construction. Thus each position of `ans` differs from the corresponding position in its sorted version.

Hence `ans` is a derangement.

If `S` is empty, then `a = b`, meaning the entire array is already sorted. Every subsequence of a sorted array is also sorted, so some position will always coincide with its sorted version. No derangement can exist.

This proves both correctness and completeness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        b = sorted(a)

        ans = []
        for i in range(n):
            if a[i] != b[i]:
                ans.append(a[i])

        if not ans:
            print("NO")
        else:
            print("YES")
            print(len(ans))
            print(*ans)

solve()
```

The solution begins by sorting the array. The sorted copy represents the target arrangement against which the derangement condition is measured.

The loop collects exactly the indices where the original value differs from the value in the sorted array. These are the only positions that can participate in a valid answer.

If no such positions exist, the array is already sorted and no valid subsequence exists.

Otherwise the collected elements form a valid derangement. The implementation directly outputs them.

The most common mistake is trying to keep indices where `a[i] == b[i]`. Such positions immediately violate the derangement requirement because the value already matches its sorted position.

Another easy mistake is checking only whether the whole array differs from its sorted version. A derangement requires every position to differ, not merely at least one position.

## Worked Examples

### Example 1

Input:

```
5
4 5 5 2 4
```

Sorted copy:

```
2 4 4 5 5
```

| Index | a[i] | sorted[i] | Keep? | ans |
| --- | --- | --- | --- | --- |
| 0 | 4 | 2 | Yes | [4] |
| 1 | 5 | 4 | Yes | [4, 5] |
| 2 | 5 | 4 | Yes | [4, 5, 5] |
| 3 | 2 | 5 | Yes | [4, 5, 5, 2] |
| 4 | 4 | 5 | Yes | [4, 5, 5, 2, 4] |

The resulting subsequence is the whole array. Its sorted version is `[2,4,4,5,5]`, and every position differs.

### Example 2

Input:

```
3
2 2 3
```

Sorted copy:

```
2 2 3
```

| Index | a[i] | sorted[i] | Keep? | ans |
| --- | --- | --- | --- | --- |
| 0 | 2 | 2 | No | [] |
| 1 | 2 | 2 | No | [] |
| 2 | 3 | 3 | No | [] |

No position differs from the sorted array, so `ans` remains empty.

The algorithm prints `NO`. This demonstrates the case where the original array is already sorted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the running time |
| Space | O(n) | Sorted copy and answer array |

With `n ≤ 100`, this complexity is far below the limits. Even across all test cases, the amount of work is tiny.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        b = sorted(a)

        ans = [a[i] for i in range(n) if a[i] != b[i]]

        if not ans:
            print("NO")
        else:
            print("YES")
            print(len(ans))
            print(*ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# sample 1
assert run(
"""3
3
2 2 3
5
4 5 5 2 4
1
1
"""
) == (
"""NO
YES
5
4 5 5 2 4
NO
"""
)

# minimum size
assert run(
"""1
1
1
"""
) == (
"""NO
"""
)

# simple derangement
assert run(
"""1
2
2 1
"""
) == (
"""YES
2
2 1
"""
)

# all equal
assert run(
"""1
5
3 3 3 3 3
"""
) == (
"""NO
"""
)

# already sorted
assert run(
"""1
4
1 2 3 4
"""
) == (
"""NO
"""
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1]` | NO | Smallest possible array |
| `[2,1]` | YES | Smallest positive instance |
| `[3,3,3,3,3]` | NO | All values equal |
| `[1,2,3,4]` | NO | Already sorted array |
| `[4,5,5,2,4]` | YES | Typical mixed case with duplicates |

## Edge Cases

Consider:

```
1
1
1
```

The sorted copy is identical. No index satisfies `a[i] != b[i]`, so the answer array is empty and the algorithm prints `NO`. A non-empty derangement cannot exist because the only available subsequence is `[1]`.

Consider:

```
1
5
3 3 3 3 3
```

Again the sorted copy is identical. Every subsequence consists entirely of threes, and sorting never changes anything. The algorithm correctly finds no differing positions and prints `NO`.

Consider:

```
1
2
2 1
```

The sorted copy is `[1,2]`. Both positions differ, so the algorithm keeps both elements. The resulting array `[2,1]` has sorted version `[1,2]`, and every position differs. The algorithm prints `YES`.

Consider:

```
1
3
3 1 2
```

The sorted copy is `[1,2,3]`. All three positions differ, so the whole array is selected. Comparing `[3,1,2]` with `[1,2,3]`, every position differs, making it a valid derangement. The algorithm outputs the entire array.
