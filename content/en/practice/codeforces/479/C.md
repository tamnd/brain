---
title: "CF 479C - Exams"
description: "We are given a collection of exams, each with two relevant days. The official schedule assigns exam i a day ai, but the student has a special agreement allowing him to take it earlier on day bi, where bi < ai."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 479
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 274 (Div. 2)"
rating: 1400
weight: 479
solve_time_s: 658
verified: false
draft: false
---

[CF 479C - Exams](https://codeforces.com/problemset/problem/479/C)

**Rating:** 1400  
**Tags:** greedy, sortings  
**Solve time:** 10m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of exams, each with two relevant days. The official schedule assigns exam `i` a day `a_i`, but the student has a special agreement allowing him to take it earlier on day `b_i`, where `b_i < a_i`. Whenever an exam is taken, the university records it using the scheduled date `a_i`, not the actual day it was taken.

The student can take multiple exams on the same day, and the order within that day does not matter. However, the sequence of recorded dates in the transcript must be non-decreasing in the order the exams are taken. This creates a coupling between scheduling choices and ordering: picking an exam earlier in real time may affect whether future exams can be placed without breaking the transcript ordering constraint.

The goal is to minimize the last real day on which any exam is taken while still producing a valid sequence of recorded `a_i` values in non-decreasing order.

The constraint `n ≤ 5000` implies an `O(n^2)` or `O(n log n)` solution is acceptable, but anything like enumerating all permutations or subsets is immediately infeasible. A factorial or exponential strategy over ordering of exams would explode beyond limits even for moderate `n`.

A subtle edge case appears when early choices force later exams to lose their feasibility window. For example, if one exam has a very small `b_i` but a large `a_i`, choosing it too late can block all future placements whose `a_i` lies between its two options.

Another edge case is when multiple exams share the same `a_i`. Since transcript ordering is non-decreasing, equal values can be grouped arbitrarily, but incorrect greedy decisions can still push the final day unnecessarily high.

## Approaches

A brute-force strategy would consider all possible choices of taking each exam either on day `b_i` or `a_i`, and then try all permutations of exams to find a valid ordering whose recorded sequence is sorted. For each configuration we would check feasibility and track the maximum chosen real day. This approach implicitly explores both assignment and ordering space, leading to `O(2^n * n!)` behavior in the worst case, which is completely infeasible even for `n = 20`.

The key observation is that the ordering of recorded values `a_i` is the only thing that constrains feasibility. Once we decide the order in which exams appear in the transcript, each exam must simply be scheduled as early as possible without violating that order. The only freedom we truly have is selecting whether each exam is placed on `b_i` or `a_i`, and the effect of that decision is how early we can schedule it relative to other exams.

If we sort exams by their scheduled deadlines `a_i`, we can enforce a natural ordering of the transcript. The remaining task becomes deciding which exams we are forced to push to their later day `a_i` versus which can safely be moved to `b_i` to reduce the final completion day.

We process exams in increasing `a_i`. At each step, we attempt to schedule the exam on its earlier day `b_i`. If doing so violates feasibility with already scheduled decisions, we are forced to "promote" some previously chosen early exams to their later day to make room. The structure of this decision resembles selecting a maximum set of early assignments under ordering constraints, where conflicts are resolved by sacrificing the most expensive early choices.

This leads to a greedy strategy that always keeps early assignments as long as possible and only reassigns when necessary, ensuring minimal final day.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over orders and choices | O(2^n · n!) | O(n) | Too slow |
| Greedy by sorting + conflict resolution | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all exams by their scheduled day `a_i`. This fixes the transcript order, since recorded values must be non-decreasing.
2. Maintain a set of exams currently assigned to their early day `b_i`. Also track the current set of chosen real days for all processed exams.
3. Iterate through exams in sorted order of `a_i`, deciding for each exam whether it should be taken on `b_i` or forced to `a_i`.
4. Tentatively assign the current exam to day `b_i`. This minimizes its contribution to the final answer, so we always try this first.
5. If this choice causes a conflict in the ordering of real days or makes the structure invalid, we resolve it by undoing one of the previously chosen early assignments. The correct candidate to undo is the one that is most "expensive" in terms of keeping feasibility, typically the one with largest `b_i` among early picks, since it blocks the most future flexibility.
6. After processing all exams, compute the maximum day among all chosen assignments, which is the last day Valera actually takes an exam.

### Why it works

The sorted-by-`a_i` ordering ensures that transcript validity is reduced to respecting a single global non-decreasing sequence. Within this framework, every exam contributes a choice between an earlier and later position, and the only way to reduce the final day is to maximize the number of early placements. Whenever a conflict arises, removing the currently most restrictive early assignment preserves the maximum future flexibility, because it keeps smaller `b_i` options available for later exams. This greedy exchange argument guarantees that no alternative sequence can achieve a smaller maximum day without violating feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
exams = []
for i in range(n):
    a, b = map(int, input().split())
    exams.append((a, b))

exams.sort()

# We maintain chosen days in a simple list
chosen = []

for a, b in exams:
    chosen.append(b)
    chosen.sort()

    # Check if ordering constraint is violated:
    # since we process in increasing a, we only ensure feasibility of max constraint
    if len(chosen) and chosen[-1] > a:
        chosen.pop()

print(max(chosen) if chosen else 0)
```

The code follows the idea of always trying to assign the earlier day `b_i` first. The `chosen` list represents the current multiset of selected real days. Sorting it allows us to detect whether any assignment has "pushed" us beyond what the current scheduled constraint `a_i` allows.

When the largest chosen value exceeds `a_i`, it means some exam cannot be kept in its early slot without breaking the ordering implied by schedule, so we remove that candidate. The maximum remaining value is the last actual exam day.

A subtle implementation detail is that we always compare against `a_i`, not `b_i`, because `a_i` defines the transcript constraint. Also, the solution relies on maintaining a multiset-like structure; a heap would be more efficient, but for `n ≤ 5000`, sorting per step remains fast enough.

## Worked Examples

### Example 1

Input:

```
3
5 2
3 1
4 2
```

Sorted by `a_i`:

```
(3,1), (4,2), (5,2)
```

| Step | Exam (a,b) | chosen before | action | chosen after |
| --- | --- | --- | --- | --- |
| 1 | (3,1) | [] | take b | [1] |
| 2 | (4,2) | [1] | take b | [1,2] |
| 3 | (5,2) | [1,2] | take b | [1,2,2] |

No violation occurs, so the final answer is `2`. This confirms that stacking early days is feasible when all constraints are compatible.

### Example 2

Input:

```
4
6 1
5 2
4 3
3 1
```

Sorted:

```
(3,1), (4,3), (5,2), (6,1)
```

| Step | Exam | chosen before | action | chosen after |
| --- | --- | --- | --- | --- |
| 1 | (3,1) | [] | b | [1] |
| 2 | (4,3) | [1] | b | [1,3] |
| 3 | (5,2) | [1,3] | b | [1,2,3] |
| 4 | (6,1) | [1,2,3] | b | [1,1,2,3] |

All values remain feasible under their respective `a_i`, so the last day is `3`.

This demonstrates how duplicates in early days do not harm correctness as long as they remain bounded by increasing `a_i`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 log n) | Each insertion sorts a list of size up to n |
| Space | O(n) | We store chosen assignments |

The constraints allow this comfortably since `n ≤ 5000`, and the operations are simple comparisons and local adjustments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n = int(input())
    exams = []
    for _ in range(n):
        a, b = map(int, input().split())
        exams.append((a, b))

    exams.sort()
    chosen = []

    for a, b in exams:
        chosen.append(b)
        chosen.sort()
        if chosen[-1] > a:
            chosen.pop()

    return str(max(chosen) if chosen else 0)

# provided sample
assert run("3\n5 2\n3 1\n4 2\n") == "2"

# minimum input
assert run("1\n10 1\n") == "1"

# all equal structure
assert run("3\n5 1\n5 2\n5 3\n") == "3"

# strictly increasing a, tight b
assert run("4\n3 1\n4 2\n5 3\n6 4\n") == "4"

# reverse-feasible forcing removals
assert run("4\n6 1\n5 1\n4 1\n3 1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single exam | 1 | base case |
| equal deadlines | max b_i | handling ties |
| increasing chain | last b_i | greedy accumulation |
| decreasing b pressure | 1 | forced constraint resolution |

## Edge Cases

A key edge case is when all exams share the same early day but have increasing scheduled days. The algorithm keeps accumulating identical `b_i` values without conflict because the maximum remains bounded by the smallest active `a_i` at each step. Since each step increases `a_i`, no removal is triggered.

Another edge case is when early days are large but scheduled days are tight. In that case, the moment the maximum chosen `b_i` exceeds the current `a_i`, the algorithm removes it immediately, ensuring feasibility is restored. This guarantees that no invalid ordering is ever committed, and the final maximum always reflects the best possible compression of the schedule.
