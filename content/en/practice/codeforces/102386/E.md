---
title: "CF 102386E - \u041e\u0442\u043b\u043e\u0436\u0435\u043d\u043d\u044b\u0435 \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u0438"
description: "We have a sequence of (n) days. On day (i), a homework assignment for subject (ai) appears. Dima may either spend the day doing all currently accumulated homework for one subject, or do nothing. Doing a subject clears every assignment of that subject received so far."
date: "2026-08-14T13:28:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102386
codeforces_index: "E"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b\u0430 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u043c\u0438\u0440\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2019"
rating: 0
weight: 102386
solve_time_s: 173
verified: false
draft: false
---

[CF 102386E - \u041e\u0442\u043b\u043e\u0436\u0435\u043d\u043d\u044b\u0435 \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u0438](https://codeforces.com/problemset/problem/102386/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We have a sequence of (n) days. On day (i), a homework assignment for subject (a_i) appears. Dima may either spend the day doing all currently accumulated homework for one subject, or do nothing. Doing a subject clears every assignment of that subject received so far.

The goal is to choose the smallest possible number of working days while making sure that every assignment has been completed by the end of day (n). The output is an array of length (n). A zero means that Dima rests on that day, while a positive value (c) means that he completes all accumulated homework for subject (c).

The key observation is that assignments of the same subject can be postponed together. If the last assignment for subject (c) arrives on day (p), Dima can simply wait until day (p) and complete all assignments of (c) there. Since different subjects have different last occurrence positions, these operations never conflict.

The constraints make this especially useful. With (n) and (k) both as large as (10^5), an (O(nk)) solution can perform up to (10^{10}) operations, which is far beyond what a typical competitive programming time limit allows. An (O(n)) or (O(n+k)) solution is the appropriate target.

There are several edge cases that a careless implementation can mishandle. If a subject appears only once, its only occurrence must be used as its processing day. For example, with input

```
1 1
1
```

the answer must be

```
1
```

because the only assignment has to be completed.

If the same subject appears many times, processing it after every assignment is unnecessary. For

```
4 2
1 1 1 1
```

the answer

```
0 0 0 1
```

is optimal because all four assignments can be completed together on the last day.

A subject that never appears should not receive an operation. For example,

```
3 5
2 2 2
```

can be answered with

```
0 0 2
```

and subjects (1,3,4,5) require no work at all. An implementation that initializes every subject to some processing day without checking whether it occurs would produce an invalid schedule.

Finally, a subject whose last occurrence is the final day is completely valid. For

```
3 2
1 2 2
```

we can output

```
0 1 2
```

The operation for subject (1) happens on day 2, while subject (2) is processed on day 3 after its final assignment arrives.

## Approaches

A direct approach is to handle each subject independently and search the entire array for its last occurrence. For subject (1), scan from the end until finding (1), then repeat the same search for subject (2), and so on. The resulting positions are exactly the days on which we should work.

This approach is correct because the last occurrence is sufficient to complete every assignment of that subject. It becomes too slow because the same array is scanned repeatedly. In the worst case, with (n=k=10^5), this takes (n\cdot k=10^{10}) array inspections.

The structure of the problem lets us avoid all repeated searches. While scanning the sequence once from left to right, whenever we see subject (a_i), we can simply record that its latest known occurrence is day (i). After the scan, the stored position for every appearing subject is exactly its last occurrence. We then put that subject into the answer at that position and leave every other day as zero.

There is no need for a segment tree or any more complicated data structure. The "deferred" idea is simply realized by postponing each subject's work until its final assignment arrives.

The reason this also gives the minimum number of working days is that every subject that appears at least once must be processed at least once. Otherwise its assignments would remain unfinished. Our construction uses exactly one working day for every subject that appears, so it reaches this unavoidable lower bound.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nk)) | (O(k)) | Too slow |
| Optimal | (O(n+k)) | (O(n+k)) | Accepted |

## Algorithm Walkthrough

1. Read (n), (k), and the sequence (a). Create an array `last` indexed by subject, initially filled with zero. A zero means that the subject has not appeared yet.
2. Scan the days from (1) through (n). For day (i), set `last[a[i]] = i`. If the same subject appears again later, its stored position is overwritten, so after the scan it contains the final occurrence.
3. Create an answer array of (n) zeros. For every subject (c) from (1) through (k), inspect `last[c]`. If it is nonzero, put (c) into the answer at that position.

This is the crucial construction. At the last occurrence of (c), all assignments of (c) have already arrived, so doing all accumulated work there completes every assignment of that subject at once.
4. Print the answer array. Every nonzero position represents exactly one subject's final occurrence, while all other days are left free.

The invariant is that after processing the first (i) days, `last[c]` is exactly the greatest position at most (i) where subject (c) has appeared, or zero if it has not appeared. At the end, every appearing subject is processed exactly once, on its final occurrence. Since every appearing subject requires at least one processing day in any valid solution, the number of working days is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    last = [0] * (k + 1)

    for i, subject in enumerate(a, start=1):
        last[subject] = i

    answer = [0] * n

    for subject in range(1, k + 1):
        pos = last[subject]
        if pos != 0:
            answer[pos - 1] = subject

    print(*answer)

if __name__ == "__main__":
    solve()
```

The `last` array has one entry for every possible subject. Its indexing starts at (1), matching the subject numbering in the input, while position zero is unused.

The enumeration starts at one because the problem describes days using one-based numbering. The final answer uses Python's zero-based indexing, so `last[subject] - 1` is used when writing into `answer`. This is the only indexing conversion in the algorithm and avoids mixing the two conventions elsewhere.

When scanning the input, assigning `last[subject] = i` intentionally overwrites previous positions. We do not need the earlier occurrences because all of that subject's accumulated homework can be completed at its final occurrence.

The second loop checks every possible subject. Subjects with `last[subject] == 0` never appeared, so no operation is generated for them. This prevents unused subjects from accidentally appearing in the answer.

There is no integer overflow concern in Python, and the largest stored day number is only (10^5).

## Worked Examples

For Sample 1, the input is

```
3 3
1 2 3
```

The scan records the latest position of each subject as follows.

| Day | Subject | `last[1]` | `last[2]` | `last[3]` |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 |
| 2 | 2 | 1 | 2 | 0 |
| 3 | 3 | 1 | 2 | 3 |

Every subject has a different final occurrence, so all three days become working days.

| Subject | Last position | Answer position |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |

The resulting answer is

```
1 2 3
```

Every subject appears exactly once, so there is no opportunity to postpone any work beyond its only assignment.

For Sample 2, the input is

```
4 2
1 1 1 1
```

The latest occurrence of subject (1) keeps moving forward, while subject (2) never appears.

| Day | Subject | `last[1]` | `last[2]` |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 0 |
| 2 | 1 | 2 | 0 |
| 3 | 1 | 3 | 0 |
| 4 | 1 | 4 | 0 |

Only subject (1) receives homework, and its final assignment arrives on day 4. All four assignments can be completed together then.

The answer is

```
0 0 0 1
```

This demonstrates why recording only the final occurrence is enough. Earlier occurrences do not need separate processing days.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+k)) | The input is scanned once, then all (k) subjects are inspected once. |
| Space | (O(n+k)) | The sequence, `last`, and answer arrays require linear memory. |

With (n,k\le 10^5), the algorithm performs only a few hundred thousand basic operations. It comfortably avoids the (10^{10}) operations that the repeated-search approach can require.

## Test Cases

The test helper below uses the same `solve` logic but returns the generated output as a string, which lets the cases be checked with Python assertions. Since several valid schedules may exist in general, these assertions target the deterministic schedule produced by this implementation, which always works on the final occurrence of each subject.

```python
import sys
import io

def solution(data: str) -> str:
    lines = data.strip().split()
    it = iter(lines)

    n = int(next(it))
    k = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    last = [0] * (k + 1)

    for i, subject in enumerate(a, start=1):
        last[subject] = i

    answer = [0] * n

    for subject in range(1, k + 1):
        pos = last[subject]
        if pos:
            answer[pos - 1] = subject

    return " ".join(map(str, answer))

def run(inp: str) -> str:
    return solution(inp)

assert run("""3 3
1 2 3
""") == "1 2 3", "sample 1"

assert run("""4 2
1 1 1 1
""") == "0 0 0 1", "sample 2"

assert run("""1 1
1
""") == "1", "minimum size"

assert run("""3 5
2 2 2
""") == "0 0 2", "unused subjects"

assert run("""5 3
1 2 1 3 2
""") == "0 0 1 3 2", "multiple repeated subjects"

assert run("""6 3
1 2 3 1 2 3
""") == "0 0 0 1 2 3", "all subjects repeat"

n = 100000
a = " ".join(["1"] * n)
expected = " ".join(["0"] * (n - 1) + ["1"])
assert run(f"{n} 100000\n{a}\n") == expected, "maximum size"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `1` | Minimum input and a single assignment |
| `3 5 / 2 2 2` | `0 0 2` | Subjects that never occur |
| `5 3 / 1 2 1 3 2` | `0 0 1 3 2` | Several subjects with different final positions |
| `6 3 / 1 2 3 1 2 3` | `0 0 0 1 2 3` | Repeated occurrences and postponement |
| (n=100000), all values equal to `1` | (99999) zeros followed by `1` | Maximum input size and the all-equal case |

## Edge Cases

When a subject appears exactly once, its last occurrence is also its first occurrence. For

```
1 1
1
```

the scan sets `last[1] = 1`, and the answer becomes `1`. There is no way to postpone the work beyond day 1, so the construction is forced and optimal.

When a subject appears repeatedly, earlier occurrences are deliberately forgotten. For

```
4 2
1 1 1 1
```

the values stored for subject (1) are successively (1,2,3,4), leaving `last[1] = 4` after the scan. The answer therefore contains only one operation, `0 0 0 1`. All four assignments are pending by day 4 and are completed together.

When some subjects never occur, their `last` entries remain zero. For

```
3 5
2 2 2
```

we finish with `last[1] = 0`, `last[2] = 3`, and `last[3] = last[4] = last[5] = 0`. Only position 3 receives the value `2`, producing `0 0 2`. The algorithm never invents work for an absent subject.

When a subject's final occurrence is on the last day, the operation is still legal because all assignments for that subject have arrived by that point. For

```
3 2
1 2 2
```

the final positions are `last[1] = 1` and `last[2] = 3`, so the output is `1 0 2`. Subject (1) is completed on its only occurrence, while both assignments for subject (2) are completed together on day 3.

The boundary between two repeated subjects also causes no special handling. For

```
6 3
1 2 3 1 2 3
```

the final positions are (4,5,6), giving `0 0 0 1 2 3`. The first three assignments remain pending while Dima waits, then each subject is completed exactly once after its final assignment.

The central property survives all of these cases: every subject that appears is processed once, at its final occurrence, and every subject that does not appear is processed zero times. Since each appearing subject necessarily requires at least one working day, no valid schedule can use fewer working days than this construction.
