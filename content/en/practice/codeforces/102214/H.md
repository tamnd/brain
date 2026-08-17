---
title: "CF 102214H - Schedule"
description: "The problem asks us to consider (n) lessons, where lesson (i) occupies the time interval ([li,ri]). Two lessons are compatible when they do not overlap. Touching at one endpoint is allowed, so ([1,3]) and ([3,5]) are compatible. We must cancel exactly one lesson."
date: "2026-08-18T00:17:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102214
codeforces_index: "H"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u043e\u0435 \u043b\u0438\u0447\u043d\u043e\u0435 \u043f\u0435\u0440\u0432\u0435\u043d\u0441\u0442\u0432\u043e \u0418\u041a\u0418\u0422 \u0421\u0424\u0423 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2015"
rating: 0
weight: 102214
solve_time_s: 98
verified: true
draft: false
---

[CF 102214H - Schedule](https://codeforces.com/problemset/problem/102214/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to consider (n) lessons, where lesson (i) occupies the time interval ([l_i,r_i]). Two lessons are compatible when they do not overlap. Touching at one endpoint is allowed, so ([1,3]) and ([3,5]) are compatible.

We must cancel exactly one lesson. The goal is to find every lesson whose cancellation leaves all remaining lessons pairwise non-overlapping. The output is the number of such lessons, followed by their indices in increasing order. The original Codeforces problem is listed as 31C, Schedule, with (n \le 5000), (l_i,r_i \le 10^6), a 2 second time limit, and 256 MB of memory.

The bound (n \le 5000) is the key constraint. An (O(n^2)) algorithm performs at most about 25 million pair checks, which is reasonable in a compiled language and still manageable in optimized Python. An (O(n^3)) algorithm would require roughly (5000^3/2 = 62.5) billion pair comparisons in the worst case, which is far beyond the limit. We therefore need to avoid checking every pair separately for every possible cancelled lesson.

The most useful way to think about the problem is to identify the pairs of lessons that actually conflict. If there are no conflicting pairs, cancelling any lesson works. If there are conflicting pairs, a lesson can be cancelled only if it belongs to every conflicting pair.

An endpoint case is easy to mishandle. For input

```
2
1 3
3 5
```

the correct output is

```
2
1 2
```

because the lessons only touch at time 3. A careless implementation using `r >= l` as the overlap condition would incorrectly regard them as conflicting.

Another important case is when several conflicts exist but share one lesson:

```
3
1 10
2 3
4 5
```

The correct output is

```
1
1
```

Lessons 1 and 2 conflict, and lessons 1 and 3 conflict. Removing lesson 1 eliminates both conflicts. Removing either short lesson leaves the other conflict intact. A solution that only finds one conflicting pair and returns both of its endpoints would incorrectly output lessons 1 and 2.

A final boundary case occurs when the schedule is already valid:

```
3
1 2
2 4
4 7
```

The correct output is

```
3
1 2 3
```

Every pair is compatible because touching endpoints are allowed. Since the problem requires exactly one cancellation, every lesson is a valid choice.

## Approaches

The direct brute-force approach considers every possible lesson to cancel. For each candidate, it examines every pair among the remaining (n-1) lessons and checks whether their intervals overlap. This is correct because the resulting schedule is valid exactly when no remaining pair intersects. However, one candidate requires (O(n^2)) comparisons, and there are (n) candidates, giving (O(n^3)) time. For (n=5000), this is on the order of (62.5) billion pair checks in the worst case.

The structure of the problem lets us avoid repeating almost all of this work. Instead of asking, for every possible cancellation, whether a pair overlaps, we can first determine which pairs overlap in the original schedule. Suppose there are (m) conflicting pairs. If lesson (i) is cancelled, exactly the conflicting pairs containing (i) disappear. Thus the cancellation works precisely when every one of the (m) conflicting pairs contains (i).

This gives a very simple counting criterion. For every lesson, count how many conflicting pairs contain it. If the total number of conflicting pairs is (m), then lesson (i) is a valid cancellation exactly when its conflict count is (m).

We can find all conflicting pairs by checking every unordered pair once. There are only (O(n^2)) such pairs, so this fits the constraint. We do not even need to store the pairs. We only need the total number of conflicts and, for each lesson, how many conflicts touch it.

The two approaches can be compared as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) | (O(n)) | Too slow |
| Optimal | (O(n^2)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read all lesson intervals and store their starting and finishing times together with their original indices.
2. Create an array `conflicts` where `conflicts[i]` counts how many other lessons overlap lesson (i). Also maintain `total_conflicts`, the total number of overlapping unordered pairs.
3. Examine every pair of lessons (i<j). They overlap exactly when

`l[i] < r[j] and l[j] < r[i]`.

This strict comparison is what makes intervals sharing an endpoint compatible. When the pair overlaps, increment `total_conflicts`, `conflicts[i]`, and `conflicts[j]`.
4. After all pairs have been processed, examine every lesson (i). If `conflicts[i] == total_conflicts`, add its index to the answer.

The reason is that cancelling (i) removes exactly those conflicting pairs that contain (i). All conflicts disappear if and only if every conflict contains (i).
5. Print the number of valid indices and then the indices themselves in increasing order. Since we inspect lessons from index 1 through (n), the collected indices already have the required ordering.

### Why it works

Consider the set of all conflicting lesson pairs. Let its size be (m). Cancelling lesson (i) can affect only conflicts containing (i), so exactly `conflicts[i]` conflicting pairs disappear. The remaining schedule has no overlap exactly when all (m) conflicting pairs disappear. Hence lesson (i) is a valid answer exactly when `conflicts[i] = m`.

If (m=0), every lesson has conflict count zero, so every lesson is correctly accepted. If (m>0), the same equality precisely identifies the lessons that participate in every conflict. Thus the algorithm outputs exactly all valid cancellations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    intervals = [tuple(map(int, input().split())) for _ in range(n)]

    conflicts = [0] * n
    total_conflicts = 0

    for i in range(n):
        li, ri = intervals[i]
        for j in range(i + 1, n):
            lj, rj = intervals[j]

            # The intervals overlap only if neither one ends
            # at or before the other one starts.
            if li < rj and lj < ri:
                total_conflicts += 1
                conflicts[i] += 1
                conflicts[j] += 1

    answer = [
        i + 1
        for i in range(n)
        if conflicts[i] == total_conflicts
    ]

    print(len(answer))
    print(*answer)

if __name__ == "__main__":
    solve()
```

The interval list stores the input exactly as given, so the original lesson index is simply its zero-based position plus one. There is no need to sort the intervals, which also means the output order comes naturally.

The nested loops use `i + 1` as the starting point for `j`, so each unordered pair is examined exactly once. The overlap condition uses strict inequalities. For example, `[1,3]` and `[3,7]` satisfy neither `1 < 7` and `3 < 3` together, so they are correctly treated as non-overlapping.

For every conflicting pair, both endpoints of that pair receive one conflict count. If a lesson participates in five different conflicting pairs, its counter becomes five. The total counter also becomes five if those are the only conflicts, so that lesson is a valid cancellation.

Python integers have arbitrary precision, so there is no overflow concern. In fact, the largest possible number of conflicting pairs is only (\binom{5000}{2}=12,497,500), which is small enough for ordinary integer arithmetic.

## Worked Examples

### Sample 1

The first sample is

```
3
3 10
20 30
1 3
```

The three lessons are pairwise compatible. The first and third lessons touch at time 3, while the second lesson starts much later.

| (i) | (j) | Interval (i) | Interval (j) | Overlap? | `total_conflicts` |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | [3,10] | [20,30] | No | 0 |
| 1 | 3 | [3,10] | [1,3] | No | 0 |
| 2 | 3 | [20,30] | [1,3] | No | 0 |

At the end, `total_conflicts = 0` and every lesson has `conflicts[i] = 0`.

| Lesson | `conflicts[i]` | `total_conflicts` | Valid? |
| --- | --- | --- | --- |
| 1 | 0 | 0 | Yes |
| 2 | 0 | 0 | Yes |
| 3 | 0 | 0 | Yes |

The output is `3` followed by `1 2 3`. This demonstrates the case where the original schedule is already valid.

### Sample 2

The second sample is

```
4
3 10
20 30
1 3
1 39
```

Lesson 4 overlaps every other lesson. The other three lessons do not overlap each other.

| (i) | (j) | Overlap? | `conflicts[i]` | `conflicts[j]` | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | No | 0 | 0 | 0 |
| 1 | 3 | No | 0 | 0 | 0 |
| 1 | 4 | Yes | 1 | 1 | 1 |
| 2 | 3 | No | 0 | 0 | 1 |
| 2 | 4 | Yes | 1 | 2 | 2 |
| 3 | 4 | Yes | 1 | 3 | 3 |

The final state is

| Lesson | `conflicts[i]` | `total_conflicts` | Valid? |
| --- | --- | --- | --- |
| 1 | 1 | 3 | No |
| 2 | 1 | 3 | No |
| 3 | 1 | 3 | No |
| 4 | 3 | 3 | Yes |

Only lesson 4 belongs to all three conflicting pairs, so removing it resolves every conflict. The output is `1` followed by `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2)) | Every unordered pair of lessons is checked once. |
| Space | (O(n)) | The intervals and one conflict counter per lesson are stored. |

For (n=5000), the pair loop examines at most 12,497,500 pairs. That is the intended scale for the given constraints and is dramatically smaller than the roughly 62.5 billion comparisons required by the brute-force (O(n^3)) method. The memory usage is linear in the number of lessons.

## Test Cases

```python
# helper: run solution logic on input string, return output string
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.strip().split()
    it = iter(data)

    n = int(next(it))
    intervals = [(int(next(it)), int(next(it))) for _ in range(n)]

    conflicts = [0] * n
    total_conflicts = 0

    for i in range(n):
        li, ri = intervals[i]
        for j in range(i + 1, n):
            lj, rj = intervals[j]
            if li < rj and lj < ri:
                total_conflicts += 1
                conflicts[i] += 1
                conflicts[j] += 1

    answer = [
        str(i + 1)
        for i in range(n)
        if conflicts[i] == total_conflicts
    ]

    return f"{len(answer)}\n{' '.join(answer)}\n"

# Provided sample 1
assert solve_data(
    """3
3 10
20 30
1 3
"""
) == "3\n1 2 3\n", "sample 1"

# Provided sample 2
assert solve_data(
    """4
3 10
20 30
1 3
1 39
"""
) == "1\n4\n", "sample 2"

# Provided sample 3
assert solve_data(
    """3
1 5
2 6
3 7
"""
) == "0\n\n", "sample 3"

# Minimum size
assert solve_data(
    """1
5 10
"""
) == "1\n1\n", "single lesson"

# All lessons touch but never overlap
assert solve_data(
    """4
1 3
3 5
5 8
8 10
"""
) == "4\n1 2 3 4\n", "endpoint touching"

# One lesson is the common cause of every conflict
assert solve_data(
    """4
1 2
2 3
1 10
3 4
"""
) == "1\n3\n", "one common conflicting lesson"

# Maximum-size case, every interval is identical.
# After removing one interval, many conflicts still remain.
n = 5000
max_case = str(n) + "\n" + ("1 2\n" * n)
assert solve_data(max_case) == "0\n\n", "maximum size all-overlapping case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5 10` | `1 / 1` | Minimum size and exactly-one cancellation |
| Four intervals touching at endpoints | `4 / 1 2 3 4` | Endpoint equality must not count as overlap |
| One interval overlapping every conflict | `1 / 3` | A valid answer can be the common endpoint of every conflict |
| 5000 identical intervals | `0` | Maximum input size and rejection when one deletion cannot remove all conflicts |

## Edge Cases

For endpoint touching, consider

```
2
1 3
3 5
```

The pair test evaluates `1 < 5` as true but `3 < 3` as false, so the pair is not counted as a conflict. The total conflict count is zero, both lessons have conflict count zero, and the output is

```
2
1 2
```

This is why using strict inequalities rather than `<=` is essential.

For a common conflicting lesson, consider

```
3
1 10
2 3
4 5
```

The pairs `(1,2)` and `(1,3)` conflict, while `(2,3)` does not. The conflict counts are `[2,1,1]` and the total number of conflicts is `2`. Only lesson 1 has a conflict count equal to the total, so the output is

```
1
1
```

Removing lesson 1 eliminates both conflicts at once.

For an already valid schedule, consider

```
3
1 2
2 4
4 7
```

Every pair either lies completely before the next pair or touches at an endpoint. Consequently the total number of conflicts is zero. Since every lesson has zero conflicts as well, every index satisfies `conflicts[i] == total_conflicts`, producing

```
3
1 2 3
```

For a dense conflict graph, consider 5000 identical intervals `[1,2]`. Every pair conflicts, so there are 12,497,500 conflicting pairs. Each lesson participates in 4,999 of them. Since `4999 != 12497500`, no lesson can eliminate all conflicts by itself, and the correct answer is zero. The algorithm handles this without constructing the enormous set of conflicting pairs, because it stores only the total count and one incident count per lesson.
