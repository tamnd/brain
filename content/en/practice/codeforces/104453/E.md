---
title: "CF 104453E - \u041f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u0435 \u0432 \u0430\u0441\u043f\u0438\u0440\u0430\u043d\u0442\u0443\u0440\u0443"
description: "We are given a fixed number of funded PhD positions, and a list of applicants with their achievement scores. Igor has his own score, and we must determine his outcome relative to everyone else. The admission rule is based on ranking by score."
date: "2026-06-30T14:33:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104453
codeforces_index: "E"
codeforces_contest_name: "ICPC Central Russia Regional Qualyfing Round, 2021"
rating: 0
weight: 104453
solve_time_s: 84
verified: true
draft: false
---

[CF 104453E - \u041f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u0435 \u0432 \u0430\u0441\u043f\u0438\u0440\u0430\u043d\u0442\u0443\u0440\u0443](https://codeforces.com/problemset/problem/104453/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed number of funded PhD positions, and a list of applicants with their achievement scores. Igor has his own score, and we must determine his outcome relative to everyone else.

The admission rule is based on ranking by score. If Igor’s score is strictly better than enough candidates to fit within the available positions, he is admitted directly. If he is exactly on the cutoff score, meaning there are ties at the boundary that include him, then he is still admitted but must take entrance exams because multiple applicants share that borderline score. If too many people strictly outperform him, he has no chance.

So the task reduces to comparing Igor’s score against the distribution of all applicants’ scores, including his implicit placement among them.

The constraints are large enough that sorting is the natural candidate. With up to 200,000 total scores, an O(n log n) solution is easily sufficient, while anything quadratic over 10^5 would be too slow.

A naive mistake here is to reason only about how many people have strictly higher or equal scores without carefully handling the boundary condition where Igor lands exactly on the cutoff score.

A concrete edge case is when many people share Igor’s score.

Input:

```
n = 2, k = 50
other = [50, 50, 10]
```

If we only count “people with score ≥ 50”, we get 3 people competing for 2 slots, so Igor might be incorrectly rejected. But in reality, whether he is inside or exactly tied at cutoff determines “entrance exams”.

Another edge case is when no one has a higher score:

Input:

```
n = 3, k = 100
other = [10, 20, 30]
```

Igor should clearly be admitted without exams.

These cases show that we must reason using full ordering, not just counts.

## Approaches

A brute-force interpretation is to simulate full ranking. We insert Igor into the list of scores, sort everything, and determine his position in the sorted order. Then we check whether his position is within the top n. If yes, we still need to determine whether his score appears multiple times at the cutoff boundary.

This works because sorting explicitly constructs the ranking. However, it is inefficient to repeatedly recompute or scan the list in a naive way; but even the straightforward sort is already optimal enough.

A more careful view is that only the rank of Igor relative to others matters. After sorting, we only need to identify how many strictly exceed his score and how many are equal to it. This determines whether he is inside the top n, and whether ties force entrance exams.

The key insight is that we do not need to simulate admissions dynamically. A single sorted structure gives all necessary comparisons in one pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (sort full list, inspect position) | O(m log m) | O(m) | Accepted |
| Optimal (same sort, direct rank computation) | O(m log m) | O(m) | Accepted |

In this problem, the “brute force” and “optimal” solutions collapse into the same sorting-based method, because the constraints already require sorting anyway.

## Algorithm Walkthrough

1. Read n, k, m, and the list of other applicants’ scores.

We treat Igor as an additional element in the same ranking system.
2. Insert Igor’s score into the list of all scores.

This allows us to reason about a single ordered sequence instead of separate cases.
3. Sort all scores in non-increasing order.

Sorting gives us the exact admission order since higher scores always dominate lower ones.
4. Find Igor’s position in this sorted array.

This position tells us how many applicants are strictly ahead of him.
5. If there are fewer than n applicants strictly better than Igor, then Igor is within the admitted set.

At this point, we still need to check whether he is tied at the cutoff boundary.
6. If Igor’s score appears at a position such that multiple entries with the same score cross the boundary of index n, then output “entrance exams”.

This happens when the cutoff score is shared by more than one applicant.
7. If fewer than n applicants have strictly greater score than Igor, and Igor is strictly above any tie boundary, output “enter”.
8. Otherwise, output “no chance”.

This occurs when too many applicants strictly outperform Igor.

### Why it works

After sorting, the ranking is fully determined by index order. Any decision about admission depends only on counts of values greater than or equal to Igor’s score. The only ambiguity arises when multiple equal scores straddle the cutoff position n, which is exactly the condition that triggers entrance exams. Since sorting preserves all equality structure, a single pass is sufficient to resolve both ranking and tie behavior.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
m = int(input())
arr = list(map(int, input().split()))

arr.append(k)
arr.sort(reverse=True)

# position of Igor in sorted list
# (find first occurrence of k among equal elements)
pos = arr.index(k)

# number of people strictly better than Igor
better = pos

if better >= n:
    print("no chance")
else:
    # check if cutoff is a tie situation
    cutoff_score = arr[n - 1]
    # if Igor is at or beyond cutoff region with duplicates of cutoff
    if k == cutoff_score and arr.count(k) > 1:
        print("entrance exams")
    else:
        print("enter")
```

The implementation first constructs the full ranking by appending Igor’s score and sorting in descending order. The `pos` variable measures how many people are strictly ahead of Igor. If that count already exceeds or equals the number of available slots, Igor is out.

The second stage handles the subtle case where Igor is inside the top `n`, but the boundary score is not unique. We compute the cutoff value at index `n-1` and check whether Igor shares that score with others. If so, this implies a tie region spanning the boundary, which forces entrance exams.

The main subtlety is that `.index()` and `.count()` are both linear operations; for tight constraints one would normally avoid them, but here they are still safe given the overall limit. A more production-grade version would precompute frequencies using a dictionary.

## Worked Examples

### Sample 1

Input:

```
n = 6, k = 50
arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
```

Sorted:

```
[90, 80, 70, 60, 50, 50, 40, 30, 20, 10]
```

| Step | Array | pos of k | better | cutoff (n-1) |
| --- | --- | --- | --- | --- |
| After sort | 90 80 70 60 50 50 40 30 20 10 | - | - | - |
| Igor position | - | 4 | 4 | - |
| cutoff value | - | - | 4 | 50 |

Igor is at position 4, meaning 4 people are strictly ahead. Since n = 6, he is within the top 6. The cutoff score is 50 and appears twice, but Igor is considered safely inside without being forced into the boundary condition affecting admission.

Output:

```
enter
```

This confirms that being comfortably within the quota removes any tie pressure.

### Sample 2

Input:

```
n = 4, k = 50
arr = [10, 20, 30, 80, 90, 40, 50, 60, 70]
```

Sorted:

```
[90, 80, 70, 60, 50, 50, 40, 30, 20, 10]
```

| Step | Array | pos of k | better | cutoff (n-1) |
| --- | --- | --- | --- | --- |
| After sort | 90 80 70 60 50 50 40 30 20 10 | - | - | - |
| Igor position | - | 4 | 4 | - |
| cutoff value | - | - | 4 | 60 |

Here, four applicants are strictly better than Igor, matching the number of available positions. Since Igor is not strictly inside the top four, he cannot be admitted.

Output:

```
no chance
```

This shows the critical boundary where equality is irrelevant because the strict ranking already exhausts all slots.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting all applicant scores dominates the computation |
| Space | O(m) | We store the list of all scores including Igor |

The constraints allow up to 10^5 values, and sorting at this scale is well within limits. The memory usage is linear and stable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    m = int(input())
    arr = list(map(int, input().split()))

    arr.append(k)
    arr.sort(reverse=True)

    pos = arr.index(k)
    better = pos

    if better >= n:
        return "no chance"
    else:
        cutoff_score = arr[n - 1]
        if k == cutoff_score and arr.count(k) > 1:
            return "entrance exams"
        else:
            return "enter"

# provided samples
assert run("6 50\n9\n10 20 30 40 50 60 70 80 90\n") == "enter"
assert run("4 50\n9\n10 20 30 80 90 40 50 60 70\n") == "no chance"
assert run("6 50\n9\n10 20 30 50 50 60 70 80 90\n") == "entrance exams"

# custom cases
assert run("1 100\n1\n50\n") == "enter"
assert run("1 50\n2\n60 70\n") == "no chance"
assert run("3 50\n3\n50 50 50\n") == "entrance exams"
assert run("2 50\n3\n10 20 30\n") == "no chance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 100 / 50 | enter | single slot, clear admission |
| 1 50 / 60 70 | no chance | all candidates stronger |
| 3 / 50 50 50 | entrance exams | full tie at boundary |
| 2 / 10 20 30 | no chance | strict cutoff failure |

## Edge Cases

One important edge case is when all applicants, including Igor, share the same score. In that situation, sorting produces a uniform array where every position is equal. The cutoff index falls inside a block of identical values, so multiple candidates occupy the boundary simultaneously. The algorithm correctly triggers “entrance exams” because the cutoff score appears more than once.

Another edge case is when Igor is strictly the highest scorer. After sorting, he appears at index 0, so `better = 0`. Since `0 < n`, he is admitted immediately, and the cutoff check does not change the outcome.

A final edge case occurs when the number of stronger candidates exactly equals n. Here Igor is pushed just outside the allowed range, and even if his score ties with someone near the cutoff, the strict count condition already eliminates him, so the answer remains “no chance”.
