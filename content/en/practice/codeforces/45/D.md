---
title: "CF 45D - Event Dates"
description: "Each event has a range of possible days when it could have happened. For the -th event, any integer day between and is acceptable. We must assign exactly one day to every event, and no two events may share the same day."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "meet-in-the-middle", "sortings"]
categories: ["algorithms"]
codeforces_contest: 45
codeforces_index: "D"
codeforces_contest_name: "School Team Contest 3 (Winter Computer School 2010/11)"
rating: 1900
weight: 45
solve_time_s: 95
verified: true
draft: false
---
[CF 45D - Event Dates](https://codeforces.com/problemset/problem/45/D)

**Rating:** 1900  
**Tags:** greedy, meet-in-the-middle, sortings  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

Each event has a range of possible days when it could have happened. For the $i$-th event, any integer day between $l_i$ and $r_i$ is acceptable. We must assign exactly one day to every event, and no two events may share the same day.

The task is not to count assignments or optimize anything. We only need to construct one valid assignment.

The constraints are surprisingly small. There are at most 100 events, while the day values themselves can be as large as $10^7$. The huge coordinate range means we cannot build an array indexed by days, but the small number of intervals means an $O(n^2)$ or $O(n^3)$ solution is completely fine. Even something like $100^3 = 10^6$ operations easily fits within the limit.

The tricky part is that making locally reasonable choices can destroy the possibility of finishing later. Suppose we process events in input order and always pick the earliest unused day.

Consider this example:

```
2
1 100
1 1
```

If we assign day 1 to the first event, the second event becomes impossible. The correct assignment is:

```
2 1
```

The narrow interval must receive priority.

Another subtle case appears when several intervals overlap heavily.

```
3
1 2
1 2
2 2
```

A careless greedy strategy might assign:

```
1 2 ?
```

and get stuck on the last event. The only valid structure is:

```
1 2 2
```

which is impossible because days must be distinct. This means the actual valid assignment must instead be:

```
1 ? 2
```

and the remaining interval gets the unused day 1, which also fails. Looking closer, this input actually has no solution. The statement guarantees solvability, but this example shows why greedy decisions matter.

Now consider a valid version:

```
3
1 3
1 2
2 3
```

Choosing days in the wrong order can still fail even though a solution exists. A robust algorithm must preserve future flexibility.

## Approaches

A brute-force solution would try every possible day inside every interval and backtrack whenever two events collide. Since each interval can span up to $10^7$ values, the search space is astronomically large. Even if intervals were tiny, the number of assignments could approach $n!$, which becomes infeasible very quickly.

The brute-force approach works conceptually because the problem only asks for existence of a distinct assignment satisfying interval constraints. Backtracking naturally explores all possibilities until it finds one. The issue is that it repeats huge amounts of work and does not exploit any structure of the intervals.

The key observation is that intervals behave nicely when processed by their right endpoints. If an event ends earlier than another, delaying it is dangerous because its available choices disappear sooner.

This leads to a classic greedy strategy:

1. Sort intervals by increasing right endpoint.
2. For each interval, assign the smallest unused day that still lies inside the interval.

Why does the smallest available day help? Because larger days remain available for future intervals that may need them. Why does sorting by right endpoint help? Because intervals with tight deadlines are handled before flexible ones.

Suppose we process an interval $[l, r]$. If we choose the earliest unused day inside it, every smaller feasible day is already occupied by intervals with smaller or equal right endpoints. Those intervals could not safely move later, while the current interval still can.

Since $n \le 100$, we do not need sophisticated data structures. We can simply scan forward from $l$ until we find an unused day.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | $O(n)$ recursion stack | Too slow |
| Optimal Greedy | $O(n^2)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all intervals and remember their original indices.

We sort intervals during processing, but the output must follow input order.
2. Sort the intervals by increasing right endpoint.

Intervals that end earlier are more restrictive. Handling them first prevents future dead ends.
3. Maintain a set of already used days.

Every assigned day must be unique.
4. For each interval $[l, r]$ in sorted order, scan days starting from $l$.

We search for the first unused day inside the interval.
5. Assign the first unused day $d$ such that $l \le d \le r$.

Choosing the smallest feasible day preserves larger days for future intervals.
6. Store the assigned day in the answer array using the interval's original index.

This restores the required output order.
7. Print the answer array.

### Why it works

The greedy choice is safe because intervals are processed in increasing order of their right endpoints.

When handling an interval $[l, r]$, every earlier processed interval has right endpoint at most $r$. Those intervals are at least as urgent as the current one. Assigning the current interval the smallest available day leaves as much room as possible for later intervals, whose right endpoints are larger.

Suppose the algorithm assigns day $d$ to the current interval. Every smaller feasible day has already been used by earlier intervals. Moving one of those earlier intervals to a larger day would only make its situation worse, because its deadline is no later than the current interval's deadline.

This exchange argument shows that the greedy assignment never blocks a valid solution if one exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

events = []

for i in range(n):
    l, r = map(int, input().split())
    events.append((r, l, i))

events.sort()

used = set()
ans = [0] * n

for r, l, idx in events:
    day = l

    while day in used:
        day += 1

    ans[idx] = day
    used.add(day)

print(*ans)
```

The solution starts by storing each interval together with its original position. The tuple order is `(r, l, idx)` because Python sorts tuples lexicographically, so intervals automatically become ordered by increasing right endpoint.

The `used` set tracks which days have already been assigned. Since only 100 events exist, a hash set is more than enough.

For each interval, the code scans upward starting from `l`. The statement guarantees that a valid assignment exists, so eventually an unused day not exceeding `r` will appear. We do not need an explicit bounds check inside the loop because solvability is guaranteed.

One subtle point is preserving output order. After sorting, intervals are no longer in their original positions. The `idx` field lets us place each chosen day back into the correct slot of the answer array.

Another subtle detail is that the algorithm intentionally chooses the earliest available day, not an arbitrary one. Picking a later day can easily block tighter intervals later.

## Worked Examples

### Example 1

Input:

```
3
1 2
2 3
3 4
```

Sorted intervals:

```
[1,2], [2,3], [3,4]
```

| Step | Interval | Used Days Before | Chosen Day | Used Days After |
| --- | --- | --- | --- | --- |
| 1 | [1,2] | {} | 1 | {1} |
| 2 | [2,3] | {1} | 2 | {1,2} |
| 3 | [3,4] | {1,2} | 3 | {1,2,3} |

Final output:

```
1 2 3
```

This example shows the straightforward case where every interval naturally receives its left endpoint.

### Example 2

Input:

```
4
1 100
1 1
2 2
3 3
```

Sorted intervals:

```
[1,1], [2,2], [3,3], [1,100]
```

| Step | Interval | Used Days Before | Chosen Day | Used Days After |
| --- | --- | --- | --- | --- |
| 1 | [1,1] | {} | 1 | {1} |
| 2 | [2,2] | {1} | 2 | {1,2} |
| 3 | [3,3] | {1,2} | 3 | {1,2,3} |
| 4 | [1,100] | {1,2,3} | 4 | {1,2,3,4} |

Final output in original order:

```
4 1 2 3
```

This trace demonstrates why sorting by right endpoint matters. If the large interval were processed first, it could consume day 1 and break the singleton interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | For each interval, we may scan through up to $n$ used days |
| Space | $O(n)$ | The answer array and used set store at most $n$ elements |

With $n \le 100$, even the quadratic scan is tiny. The algorithm comfortably fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    events = []

    for i in range(n):
        l, r = map(int, input().split())
        events.append((r, l, i))

    events.sort()

    used = set()
    ans = [0] * n

    for r, l, idx in events:
        day = l

        while day in used:
            day += 1

        ans[idx] = day
        used.add(day)

    print(*ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""3
1 2
2 3
3 4
"""
) == "1 2 3", "sample 1"

# minimum size
assert run(
"""1
5 5
"""
) == "5", "single interval"

# intervals requiring sorting by deadline
assert run(
"""4
1 100
1 1
2 2
3 3
"""
) == "4 1 2 3", "deadline priority"

# all intervals identical
out = run(
"""3
1 3
1 3
1 3
"""
)
vals = list(map(int, out.split()))
assert sorted(vals) == [1, 2, 3], "distinct assignments"

# off-by-one boundary case
assert run(
"""2
1 1
2 2
"""
) == "1 2", "boundary endpoints"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single interval `[5,5]` | `5` | Minimum-size input |
| Large flexible interval plus tight intervals | `4 1 2 3` | Correct greedy ordering |
| All intervals `[1,3]` | Any permutation of `1 2 3` | Distinct assignment handling |
| Singleton boundaries | `1 2` | Inclusive endpoint correctness |

## Edge Cases

Consider the case where one interval is extremely flexible while another has only one possible day.

```
2
1 100
1 1
```

The algorithm sorts by right endpoint:

```
[1,1], [1,100]
```

The singleton interval immediately receives day 1. The flexible interval then takes day 2. The final output becomes:

```
2 1
```

A naive input-order greedy strategy would fail here by consuming day 1 too early.

Now consider overlapping intervals with tight deadlines.

```
4
1 2
1 2
2 3
3 4
```

Sorted order:

```
[1,2], [1,2], [2,3], [3,4]
```

Assignments proceed as:

| Interval | Assigned Day |
| --- | --- |
| [1,2] | 1 |
| [1,2] | 2 |
| [2,3] | 3 |
| [3,4] | 4 |

Every interval receives the earliest unused feasible day. The algorithm never wastes small days unnecessarily.

Finally, consider intervals already naturally ordered but touching at boundaries.

```
3
1 1
1 2
2 2
```

Sorted order:

```
[1,1], [1,2], [2,2]
```

Assignments:

| Interval | Assigned Day |
| --- | --- |
| [1,1] | 1 |
| [1,2] | 2 |
| [2,2] | impossible |

This input has no valid solution, which matches the problem guarantee that such cases never appear. The example illustrates why consuming an endpoint carelessly can instantly destroy feasibility.
