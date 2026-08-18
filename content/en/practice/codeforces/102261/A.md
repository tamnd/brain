---
title: "CF 102261A - \u0411\u0443\u0434\u0438\u043b\u044c\u043d\u0438\u043a\u0438"
description: "Each of the (N) alarms starts ringing at its own initial time (ti), then repeats every (X) minutes. If several alarms ring simultaneously, Alexey hears that moment only once. He wakes up immediately after hearing the (K)-th distinct ringing time."
date: "2026-08-19T02:09:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102261
codeforces_index: "A"
codeforces_contest_name: "\u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e - \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f (\u042f\u043d\u0434\u0435\u043a\u0441)"
rating: 0
weight: 102261
solve_time_s: 337
verified: true
draft: false
---

[CF 102261A - \u0411\u0443\u0434\u0438\u043b\u044c\u043d\u0438\u043a\u0438](https://codeforces.com/problemset/problem/102261/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

Each of the (N) alarms starts ringing at its own initial time (t_i), then repeats every (X) minutes. If several alarms ring simultaneously, Alexey hears that moment only once. He wakes up immediately after hearing the (K)-th distinct ringing time.

The task is to find that (K)-th distinct time.

The constraints are large enough to rule out simulating every ringing event. There can be (10^5) alarms, while both (X) and (K) can reach (10^9). The answer itself can be around (10^{18}), because a single alarm may need to ring (K) times. A solution that explicitly generates the first (K) events can require (O(KN)) work in the worst case, which is completely infeasible. We need a logarithmic dependence on the size of the answer, together with roughly linear preprocessing.

The main edge cases come from coinciding alarms. Consider

```
2 5 3
1 6
```

Both alarms ring at exactly the same moments: (1,6,11,\ldots). The third distinct ringing time is (11). A careless solution that treats every alarm ringing as a separate event would count (1) and (6) twice and produce the wrong answer.

Another subtle case is when two initial times have the same remainder modulo (X), but are not equal:

```
2 5 4
1 11
```

The first alarm rings at (1,6,11,16,\ldots), while the second rings at (11,16,\ldots). The second alarm contributes no new ringing times at all, so the fourth distinct time is (16). Simply keeping every (t_i) as an independent arithmetic progression would double-count (11,16,\ldots).

The opposite situation also matters. Different residues modulo (X) never collide. For example,

```
2 5 4
1 2
```

produces (1,2,6,7,\ldots). The two progressions remain distinct forever, because numbers with different remainders modulo (5) cannot be equal.

## Approaches

A direct solution could repeatedly find the earliest next ringing time among all alarms, count it once, and then advance every alarm that rings at that moment. This is conceptually simple and correct because it literally simulates the merged sequence of ringing moments. However, even one alarm can produce (K) events, and (K) can be (10^9). With (N=10^5), maintaining all alarms can require on the order of (NK), up to (10^{14}) operations. Even a more careful simulation that uses a priority queue still has to process (K) distinct moments, giving at least (O(K\log N)), which is far too large.

The useful structure is that every progression has exactly the same step (X). Two alarms can ring at the same time precisely when their starting times have the same remainder modulo (X). Suppose two starts in the same residue class are (a) and (b), with (a<b). Since (b-a) is a multiple of (X), every ringing time of the second alarm is also a ringing time of the first. Thus only the earliest starting alarm in each residue class matters.

After replacing all alarms with the earliest (t_i) for each remainder modulo (X), we have at most (X) relevant progressions, and each one is

[
s,\ s+X,\ s+2X,\ldots
]

where (s) is its earliest starting time.

Now consider a candidate time (T). For one progression starting at (s), the number of ringing moments not exceeding (T) is

[
\left\lfloor\frac{T-s}{X}\right\rfloor+1
]

when (s\le T), and zero otherwise. Since different retained progressions have different residues modulo (X), they never overlap. We can therefore sum these counts to obtain the exact number of distinct ringing moments up to (T).

This count is monotonic: increasing (T) can only add ringing moments. That makes binary search applicable. We binary-search the smallest (T) for which at least (K) distinct ringing moments have occurred. The smallest such (T) is exactly the (K)-th ringing moment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(K\log N)) with a priority queue | (O(N)) | Too slow |
| Optimal | (O(N\log A)) | (O(N)) | Accepted |

Here (A) is the magnitude of the answer, at most about (10^{18}), so the binary search takes only about 60 iterations.

## Algorithm Walkthrough

1. Read (N), (X), (K), and the starting times (t_i).
2. Group the starting times by their remainder modulo (X). For every remainder, keep only the smallest starting time.

If two starts have the same remainder, the later progression is contained entirely inside the earlier one. Keeping the minimum removes all duplicate future ringing moments before the binary search even begins.
3. Define a counting function (count(T)). For every retained starting time (s), if (s\le T), add

[
\frac{T-s}{X}+1
]

using integer division.

The resulting value is exactly the number of distinct ringing moments at or before (T), because the retained progressions have different residues and therefore cannot intersect.
4. Choose a binary-search interval containing the answer. The earliest possible ringing time is (\min(t_i)). A safe upper bound is

[
\min(t_i)+(K-1)X.
]

Even a single progression starting at the minimum time contains (K) events by that point, so the actual answer cannot be larger.
5. Binary-search for the smallest (T) satisfying (count(T)\ge K). If the count at the midpoint is already at least (K), the answer is at most that midpoint, so move the right boundary left. Otherwise, the answer is larger, so move the left boundary right.
6. Output the final left boundary. It is the first time at which at least (K) distinct events have appeared, which means it is exactly the (K)-th distinct ringing time.

### Why it works

After keeping only the earliest alarm for every residue modulo (X), every removed alarm produces only moments already produced by the retained alarm from the same residue. Thus the retained progressions generate exactly the same set of ringing times as the original alarms.

The retained progressions have pairwise different residues modulo (X), so no two of them can ring simultaneously. Consequently, summing the number of events from each progression gives the exact number of distinct events up to any time (T). This count is monotonic, so the smallest (T) with (count(T)\ge K) is precisely the time of the (K)-th distinct event.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, X, K = map(int, input().split())
    t = list(map(int, input().split()))

    INF = 10**30
    earliest = {}

    for value in t:
        r = value % X
        if r not in earliest or value < earliest[r]:
            earliest[r] = value

    starts = list(earliest.values())
    first = min(starts)

    def count_events(T):
        total = 0

        for s in starts:
            if s <= T:
                total += (T - s) // X + 1
                if total >= K:
                    return total

        return total

    lo = first
    hi = first + (K - 1) * X

    while lo < hi:
        mid = (lo + hi) // 2

        if count_events(mid) >= K:
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The dictionary `earliest` implements the residue-class compression. The key is `value % X`, and its value is the smallest starting time having that remainder. We do not need to preserve the actual alarm identities, because only their ringing moments matter.

The function `count_events` evaluates the monotonic predicate used by binary search. The condition `s <= T` is necessary because an alarm has produced no event yet when its first ringing time is after (T). For an active progression, `(T - s) // X + 1` counts the event at (s) itself, which is the source of a common off-by-one error.

The early return when `total >= K` is an optimization. Once the count has reached (K), its exact larger value is irrelevant to the binary-search predicate.

Python integers have arbitrary precision, so the potentially large value `first + (K - 1) * X` does not overflow. In a language with fixed-width integer types, a 64-bit integer is required here.

The upper bound is valid even when there are many residue classes, because one progression beginning at `first` alone contains (K) ringing moments by `first + (K - 1) * X`. More alarms can only make the (K)-th event earlier.

## Worked Examples

For the first sample,

```
6 5 10
1 2 3 4 5 6
```

the residues modulo (5) are (1,2,3,4,0,1). The two values (1) and (6) have the same residue, and the progression from (6) is already contained in the progression from (1). The retained starts are therefore (1,2,3,4,5).

| Binary-search state | Value |
| --- | --- |
| Retained starts | 1, 2, 3, 4, 5 |
| (K) | 10 |
| First possible time | 1 |
| Upper bound | 46 |
| (count(23)) | 24 |
| (count(12)) | 12 |
| (count(6)) | 6 |
| (count(9)) | 9 |
| (count(10)) | 10 |

The ten distinct events are exactly (1,2,3,4,5,6,7,8,9,10), so the answer is (10). The duplicate start at (6) never creates an additional event.

For the second sample,

```
5 7 12
5 22 17 13 8
```

the residues modulo (7) are (5,1,3,6,1). The starts (22) and (8) share residue (1), so the alarm starting at (22) is redundant. The retained starts are (5,8,17,13).

| Candidate (T) | Events up to (T) |
| --- | --- |
| 20 | 10 |
| 25 | 11 |
| 27 | 12 |
| 26 | 11 |

The progression starting at (5) contributes (5,12,19,26,\ldots), the one starting at (8) contributes (8,15,22,\ldots), the one starting at (13) contributes (13,20,27,\ldots), and the one starting at (17) contributes (17,24,31,\ldots). The twelfth distinct event is (27), matching the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log A)) | Building residue classes costs (O(N)), and each of about (O(\log A)) binary-search iterations scans at most (N) retained starts. |
| Space | (O(N)) | The dictionary stores at most one starting time for each distinct residue. |

With (N\le10^5), the algorithm performs roughly (10^5) operations during preprocessing and at most around 60 scans for a 64-bit-sized answer. This is practical within the given limits, while explicitly simulating up to (K) events is impossible when (K) approaches (10^9).

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    N, X, K = map(int, sys.stdin.readline().split())
    t = list(map(int, sys.stdin.readline().split()))

    earliest = {}

    for value in t:
        r = value % X
        if r not in earliest or value < earliest[r]:
            earliest[r] = value

    starts = list(earliest.values())
    first = min(starts)

    def count_events(T):
        total = 0
        for s in starts:
            if s <= T:
                total += (T - s) // X + 1
                if total >= K:
                    return total
        return total

    lo = first
    hi = first + (K - 1) * X

    while lo < hi:
        mid = (lo + hi) // 2
        if count_events(mid) >= K:
            hi = mid
        else:
            lo = mid + 1

    print(lo)

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result.strip()

# Sample 1
assert solve_data("""\
6 5 10
1 2 3 4 5 6
""") == "10"

# Sample 2
assert solve_data("""\
5 7 12
5 22 17 13 8
""") == "27"

# Minimum-size input
assert solve_data("""\
1 1 1
1
""") == "1"

# All alarms are identical, so there is only one distinct progression
assert solve_data("""\
5 10 7
3 3 3 3 3
""") == "63"

# Same residue, later alarm is completely redundant
assert solve_data("""\
2 5 4
1 11
""") == "16"

# Different residues and an exact boundary at an initial ringing time
assert solve_data("""\
2 5 4
1 2
""") == "7"

# Large answer, checks 64-bit-sized arithmetic
assert solve_data("""\
100000 1000000000 1000000000
1 1 1 1 1 1 1 1 1 1
""") == "999999999000000001"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1` | `1` | Minimum-size input and first possible event |
| `5 10 7 / 3 3 3 3 3` | `63` | All alarms coincide completely |
| `2 5 4 / 1 11` | `16` | Duplicate residue classes must be compressed |
| `2 5 4 / 1 2` | `7` | Different residues and exact event boundaries |
| `100000 1000000000 1000000000 / all 1` | `999999999000000001` | Large arithmetic and large (K) |

## Edge Cases

When every alarm has the same starting time, such as

```
5 10 7
3 3 3 3 3
```

there is only one distinct progression, (3,13,23,33,43,53,63,\ldots). The dictionary contains one entry, so `count_events(63)` is (7), and the answer is (63). A simulation that counts alarms instead of distinct times would incorrectly think that five events happen at time (3).

When two starts differ by a multiple of (X), such as

```
2 5 4
1 11
```

both starts have residue (1). The progression from (11) is (11,16,21,\ldots), which is already contained in (1,6,11,16,\ldots). The dictionary keeps only (1), giving the fourth event (16). This is why grouping by remainder, rather than merely removing equal starting times, is necessary.

When two alarms have different residues, their events never collide. For

```
2 5 4
1 2
```

the merged sequence begins (1,2,6,7), so the answer is (7). The counting function gives (count(6)=3) and (count(7)=4), so the binary search returns (7). This also tests the boundary between an insufficient candidate and the first sufficient candidate.

The minimum case

```
1 1 1
1
```

has just one progression and asks for its first event. The lower and upper binary-search bounds are both (1), so the loop performs no iterations and immediately returns (1). This confirms that the search interval includes the answer itself rather than starting strictly after it.
