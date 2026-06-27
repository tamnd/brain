---
title: "CF 105030A - \u0420\u0430\u0441\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u043f\u0440\u044f\u043d\u043e\u0441\u0442\u0438"
description: "Each unit of spice is labeled with an integer topic. We must distribute all units among as few students as possible. A single student may receive several units, but any two topics assigned to that student must differ by more than k."
date: "2026-06-28T01:33:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105030
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 105030
solve_time_s: 77
verified: true
draft: false
---

[CF 105030A - \u0420\u0430\u0441\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u043f\u0440\u044f\u043d\u043e\u0441\u0442\u0438](https://codeforces.com/problemset/problem/105030/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

Each unit of spice is labeled with an integer topic. We must distribute all units among as few students as possible.

A single student may receive several units, but any two topics assigned to that student must differ by more than `k`. If two topic numbers differ by at most `k`, they are considered similar and cannot belong to the same student.

The task is to compute the minimum number of students needed.

The value of `n` reaches `2 · 10^5`, so any algorithm that compares every pair of topics or tries different assignments is immediately too expensive. Quadratic algorithms require around `4 · 10^10` operations in the worst case, which is far beyond practical limits. We should aim for `O(n log n)` or better.

Several situations deserve special attention.

When `k = 0`, equal topics alone are forbidden within one student's assignment. For example,

```
3 0
3 1 1
```

The correct answer is `2`. One student may receive topics `1` and `3`, while the second student receives the remaining `1`. Simply counting distinct values would incorrectly produce `1`.

Large gaps between values completely remove conflicts. For example,

```
4 5
1 10 20 30
```

The correct answer is `1`, because every pair differs by more than `5`. A solution that only looks at the total number of elements without considering distances would overestimate the answer.

Many equal values together with nearby values are another trap. Consider

```
5 2
5 5 5 6 7
```

The correct answer is `5`. Every copy of `5` conflicts with every other copy, and both `6` and `7` also conflict with every `5`. A greedy assignment that only tracks the previous value in one student's sequence can easily become incorrect if it ignores multiplicities.

## Approaches

A direct approach is to try assigning every topic to existing students and create a new student whenever none can accept it. If implemented carefully, this eventually finds the minimum assignment, because every decision checks all previous students. Unfortunately, each of the `n` topics may scan up to `n` students, producing `O(n²)` work.

The key observation is that after sorting the topic values, every conflict becomes local. A topic only conflicts with values lying within an interval of length `k`. Instead of thinking about students individually, we can ask a different question.

Suppose we look at every interval of values whose maximum minus minimum is at most `k`. Every pair inside such an interval conflicts with each other, so none of them may belong to the same student. If an interval contains `m` elements, at least `m` students are necessary.

The surprising part is that this lower bound is also sufficient.

After sorting, the conflict graph is an interval graph. Interval graphs are perfect graphs, meaning the chromatic number equals the size of the largest clique. Here, a clique is exactly a set of values contained in some interval of length `k`. Consequently, the minimum number of students equals the maximum number of sorted elements contained in any window satisfying `a[r] - a[l] <= k`.

Finding this maximum window size is exactly the classic two pointers technique.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(1) extra, excluding sorting | Accepted |

## Algorithm Walkthrough

1. Read the input and sort all topic values.
2. Maintain two indices, `l` and `r`, describing the current window in the sorted array.
3. Extend `r` from left to right. After inserting a new value, check whether the window still satisfies `a[r] - a[l] <= k`.
4. While the difference exceeds `k`, move `l` forward until the condition becomes true again.

Every time `l` moves, the window becomes narrower, so eventually the condition is restored.
5. The current window now contains the largest suffix ending at `r` whose values all lie within a range of length `k`.
6. Update the answer with the current window length, `r - l + 1`.
7. After processing every position, output the maximum window size.

### Why it works

At every moment, the window contains exactly the elements whose values fit inside one interval of length `k`. Every pair inside that window differs by at most `k`, so they all conflict with each other. They must occupy different students, making the window length a necessary lower bound.

Conversely, the conflict graph formed by intervals on a line is an interval graph. Interval graphs can always be colored using exactly the size of their largest clique. Since every clique corresponds to one such window, the largest window size is also sufficient. The algorithm computes precisely this quantity, so the answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    ans = 0
    l = 0

    for r in range(n):
        while a[r] - a[l] > k:
            l += 1
        ans = max(ans, r - l + 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

Sorting transforms value differences into contiguous segments, allowing the sliding window to work correctly.

The left pointer only moves forward, never backward. This property guarantees linear work after sorting. Every element enters the window once and leaves it once.

The comparison inside the `while` loop must be `> k`. Windows with difference exactly `k` are still valid because those values are considered similar and belong to the same clique.

The answer is updated after restoring the invariant `a[r] - a[l] <= k`. Updating earlier would count invalid windows.

## Worked Examples

### Sample 1

Input

```
3 2
1 2 4
```

After sorting, the array is unchanged.

| r | Value | l after shrinking | Current window | Window size | Best |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | [1] | 1 | 1 |
| 1 | 2 | 0 | [1,2] | 2 | 2 |
| 2 | 4 | 1 | [2,4] | 2 | 2 |

The largest valid window contains two elements, so two students are sufficient and also necessary.

### Sample 2

Input

```
9 2
7 1 2 8 5 4 9 3 6
```

After sorting,

```
1 2 3 4 5 6 7 8 9
```

| r | Value | l after shrinking | Current window | Window size | Best |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | [1] | 1 | 1 |
| 1 | 2 | 0 | [1,2] | 2 | 2 |
| 2 | 3 | 0 | [1,2,3] | 3 | 3 |
| 3 | 4 | 1 | [2,3,4] | 3 | 3 |
| 4 | 5 | 2 | [3,4,5] | 3 | 3 |
| 5 | 6 | 3 | [4,5,6] | 3 | 3 |
| 6 | 7 | 4 | [5,6,7] | 3 | 3 |
| 7 | 8 | 5 | [6,7,8] | 3 | 3 |
| 8 | 9 | 6 | [7,8,9] | 3 | 3 |

Every valid window has size at most three, and many achieve that size. Hence the minimum number of students is `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, the sliding window is linear |
| Space | O(1) extra | Only a few indices are stored beyond the sorted array |

The algorithm easily handles `2 · 10^5` elements. Sorting this many integers is fast, and the two pointers scan the array only once.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    l = 0
    ans = 0
    for r in range(n):
        while a[r] - a[l] > k:
            l += 1
        ans = max(ans, r - l + 1)
    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.getvalue()

# provided samples
assert run("3 2\n1 2 4\n") == "2\n"
assert run("9 2\n7 1 2 8 5 4 9 3 6\n") == "3\n"
assert run("3 0\n3 1 1\n") == "2\n"

# custom cases
assert run("1 100\n42\n") == "1\n"
assert run("5 0\n7 7 7 7 7\n") == "5\n"
assert run("4 5\n1 10 20 30\n") == "1\n"
assert run("5 2\n1 3 3 5 7\n") == "3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 100 / 42` | `1` | Minimum input size |
| `5 0 / 7 7 7 7 7` | `5` | All equal values |
| `4 5 / 1 10 20 30` | `1` | No conflicts at all |
| `5 2 / 1 3 3 5 7` | `3` | Duplicate values together with boundary differences |

## Edge Cases

When `k = 0`, only identical values conflict.

Input:

```
3 0
3 1 1
```

After sorting we obtain `[1, 1, 3]`. The maximum valid window is `[1, 1]`, whose size is `2`. The algorithm outputs `2`, matching the required number of students.

When all values are far apart, every window quickly shrinks to include all processed elements because every difference exceeds `k`.

Input:

```
4 5
1 10 20 30
```

Every valid window has size `1`, so the answer becomes `1`. One student can receive every spice unit because no pair of topics is similar.

When many equal values appear together with nearby values, duplicates are counted naturally because the sliding window operates on elements rather than distinct values.

Input:

```
5 2
5 5 5 6 7
```

The entire array fits inside one window since `7 - 5 = 2`. The window size is `5`, so five students are required. Every copy of `5` conflicts with every other copy, and both `6` and `7` also conflict with them, making any smaller assignment impossible.
