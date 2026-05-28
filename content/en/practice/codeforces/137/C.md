---
title: "CF 137C - History"
description: "Each historical event is represented by a time interval [a, b], where a is the starting year and b is the ending year. One event is considered contained inside another if it starts later and ends earlier."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 137
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 98 (Div. 2)"
rating: 1500
weight: 137
solve_time_s: 96
verified: true
draft: false
---

[CF 137C - History](https://codeforces.com/problemset/problem/137/C)

**Rating:** 1500  
**Tags:** sortings  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

Each historical event is represented by a time interval `[a, b]`, where `a` is the starting year and `b` is the ending year. One event is considered contained inside another if it starts later and ends earlier. Formally, event `j` contains event `i` when:

- `a_j < a_i`
- `b_i < b_j`

The task is to count how many events are contained in at least one other event.

The input gives up to `10^5` intervals. A quadratic solution that compares every pair of events would require roughly `10^10` comparisons in the worst case, which is far beyond what fits in a 2-second limit. This immediately rules out any `O(n^2)` approach. We need something around `O(n log n)`, which strongly suggests sorting.

A subtle detail is that containment depends on both coordinates at the same time. Looking only at starting years or only at ending years is not enough.

Consider this example:

```
3
1 10
2 5
6 9
```

The correct answer is:

```
2
```

Both `[2,5]` and `[6,9]` are inside `[1,10]`.

A careless implementation that only checks neighboring intervals after sorting could miss one of them.

Another easy mistake is forgetting that strict inequalities are required. If equal endpoints were allowed, we would need to distinguish between strict and non-strict containment carefully. This problem avoids that complication because all starts and all ends are distinct, but the algorithm should still rely on the strict ordering correctly.

This example demonstrates why tracking the maximum ending year seen so far works:

```
4
1 4
2 10
3 5
6 8
```

The correct answer is:

```
1
```

Only `[3,5]` is contained, because it lies inside `[2,10]`.

A naive "current interval ends earlier than previous interval" check would incorrectly count `[6,8]`, even though its start is already outside `[2,10]`.

## Approaches

The brute-force approach is straightforward. For every interval `i`, scan all other intervals `j` and check whether:

```
a_j < a_i and b_i < b_j
```

If such an interval exists, mark `i` as contained.

This works because the definition can be tested directly in constant time for every pair. The problem is scale. With `10^5` intervals, the number of comparisons becomes:

```
10^5 × 10^5 = 10^10
```

That is far too slow.

The key observation is that containment becomes much easier after sorting by starting year.

Suppose we sort intervals by increasing `a`. When processing an interval `[a_i, b_i]`, every earlier interval in the sorted order already has a smaller starting year. The first containment condition is automatically satisfied. We only need to know whether any earlier interval has a larger ending year.

That transforms the problem into a prefix maximum query.

As we scan from left to right, we maintain the maximum `b` seen so far. If the current interval has:

```
b_i < max_b
```

then some previous interval ends later, and because it also started earlier due to sorting, the current interval is contained.

This reduces the entire problem to one sort plus one linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all intervals into a list.

We need all intervals together because the solution depends on sorting them globally.
2. Sort the intervals by starting year in increasing order.

After sorting, every earlier interval automatically satisfies the condition `a_j < a_i`.
3. Initialize a variable `max_b` with a very small value.

This stores the largest ending year among all previously processed intervals.
4. Scan the sorted intervals from left to right.

For each interval `[a, b]`, check whether `b < max_b`.
5. If `b < max_b`, increment the answer.

Some earlier interval has a larger ending year, and because earlier intervals also start earlier, the current interval is contained.
6. Update `max_b = max(max_b, b)`.

Future intervals may be contained inside the current one if it has the largest ending year seen so far.
7. Print the final count.

### Why it works

After sorting by starting year, every processed interval before the current one has a strictly smaller start. The only remaining requirement for containment is finding an earlier interval whose ending year is larger.

The variable `max_b` always stores the largest ending year among all earlier intervals. If the current interval ends before `max_b`, then there exists some earlier interval that starts earlier and ends later, which means the current interval is contained.

If `b >= max_b`, then no earlier interval ends later than the current one, so containment is impossible.

Because every interval is processed exactly once under this invariant, the algorithm counts precisely the intervals contained inside another interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    intervals = []
    
    for _ in range(n):
        a, b = map(int, input().split())
        intervals.append((a, b))
    
    intervals.sort()
    
    max_b = -1
    ans = 0
    
    for a, b in intervals:
        if b < max_b:
            ans += 1
        
        max_b = max(max_b, b)
    
    print(ans)

solve()
```

The solution begins by reading all intervals and sorting them by starting year. Python sorts tuples lexicographically, so `intervals.sort()` naturally sorts by `a`.

The variable `max_b` tracks the largest ending year among intervals already processed. Initially it is set to `-1`, which is safely smaller than any valid ending year.

During the scan, the condition:

```
if b < max_b:
```

detects containment. Because the intervals are processed in increasing start order, any interval contributing to `max_b` already starts earlier. The current interval is contained exactly when its ending year is smaller.

The update:

```
max_b = max(max_b, b)
```

must happen after the containment check. Updating first would make every interval compare against itself, which would be incorrect.

Python integers handle the endpoint range up to `10^9` safely without overflow concerns.

## Worked Examples

### Example 1

Input:

```
5
1 10
2 9
3 8
4 7
5 6
```

Sorted intervals remain the same.

| Current Interval | max_b Before | Contained? | Answer | max_b After |
| --- | --- | --- | --- | --- |
| (1, 10) | -1 | No | 0 | 10 |
| (2, 9) | 10 | Yes | 1 | 10 |
| (3, 8) | 10 | Yes | 2 | 10 |
| (4, 7) | 10 | Yes | 3 | 10 |
| (5, 6) | 10 | Yes | 4 | 10 |

Final answer:

```
4
```

This trace shows the central invariant clearly. Once the interval `(1,10)` establishes `max_b = 10`, every later interval ending earlier is automatically contained.

### Example 2

Input:

```
4
1 4
2 10
3 5
6 8
```

Sorted intervals:

```
(1,4), (2,10), (3,5), (6,8)
```

| Current Interval | max_b Before | Contained? | Answer | max_b After |
| --- | --- | --- | --- | --- |
| (1, 4) | -1 | No | 0 | 4 |
| (2, 10) | 4 | No | 0 | 10 |
| (3, 5) | 10 | Yes | 1 | 10 |
| (6, 8) | 10 | Yes | 2 | 10 |

Final answer:

```
2
```

This example demonstrates that containment does not require nested chains. One large interval can contain multiple unrelated intervals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the runtime |
| Space | O(n) | The interval list stores all events |

With `n = 10^5`, an `O(n log n)` solution easily fits within the time limit. The memory usage is also small because only the interval array is stored.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    
    n = int(input())
    
    intervals = []
    
    for _ in range(n):
        a, b = map(int, input().split())
        intervals.append((a, b))
    
    intervals.sort()
    
    max_b = -1
    ans = 0
    
    for a, b in intervals:
        if b < max_b:
            ans += 1
        
        max_b = max(max_b, b)
    
    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    
    solve()
    
    out = sys.stdout.getvalue()
    
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    
    return out.strip()

# provided sample
assert run(
"""5
1 10
2 9
3 8
4 7
5 6
"""
) == "4", "sample 1"

# minimum size
assert run(
"""1
1 2
"""
) == "0", "single interval"

# no interval contained
assert run(
"""4
1 2
3 4
5 6
7 8
"""
) == "0", "disjoint intervals"

# one large interval contains all others
assert run(
"""5
1 100
2 10
20 30
40 50
60 70
"""
) == "4", "one container"

# mixed ordering
assert run(
"""4
6 8
1 4
3 5
2 10
"""
) == "2", "unsorted input"

# nested chain
assert run(
"""4
1 8
2 7
3 6
4 5
"""
) == "3", "deep nesting"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single interval | 0 | Minimum input size |
| Disjoint intervals | 0 | No false positives |
| One large interval | 4 | Multiple intervals contained by one event |
| Mixed ordering | 2 | Sorting is necessary |
| Nested chain | 3 | Repeated containment detection |

## Edge Cases

Consider the smallest possible input:

```
1
1 2
```

After sorting, there is only one interval. `max_b` starts at `-1`, so `2 < -1` is false. The answer remains `0`, which is correct because no other interval exists.

Now consider completely disjoint intervals:

```
4
1 2
3 4
5 6
7 8
```

The scan proceeds as follows:

- `(1,2)` sets `max_b = 2`
- `(3,4)` has `4 < 2`, false
- `(5,6)` has `6 < 4`, false
- `(7,8)` has `8 < 6`, false

No interval is counted. Every interval ends later than all previous ones, so containment never occurs.

Finally, consider a case where one interval contains many unrelated intervals:

```
5
1 100
2 10
20 30
40 50
60 70
```

Sorted order stays the same. After processing `(1,100)`, `max_b = 100`. Every later interval has a smaller ending year, so all four are counted.

This confirms the invariant behind the algorithm. Once an interval with a very large ending year appears, every later interval ending earlier is guaranteed to be contained because the start ordering has already been handled by sorting.
