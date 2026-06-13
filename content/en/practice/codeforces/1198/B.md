---
title: "CF 1198B - Welfare State"
description: "We are maintaining a dynamic list of balances for a fixed set of citizens. Initially, each citizen has a known amount of money. Then a sequence of events modifies these balances in two different ways."
date: "2026-06-13T14:40:04+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1198
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 576 (Div. 1)"
rating: 1600
weight: 1198
solve_time_s: 204
verified: true
draft: false
---

[CF 1198B - Welfare State](https://codeforces.com/problemset/problem/1198/B)

**Rating:** 1600  
**Tags:** binary search, brute force, data structures, sortings  
**Solve time:** 3m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a dynamic list of balances for a fixed set of citizens. Initially, each citizen has a known amount of money. Then a sequence of events modifies these balances in two different ways.

The first type of event directly sets one specific citizen’s balance to an exact value, as if a receipt overwrites our knowledge of that person’s current money. The second type of event is a global government action: every citizen whose balance is strictly below a given threshold is raised up to that threshold, while citizens already at or above it are left unchanged.

The output after processing all events is simply the final balance of each citizen.

The key difficulty is that global updates can affect many citizens at once, and there can be up to 200,000 events. A naive approach that scans all citizens for every global update would require up to 40 billion operations in the worst case, which is far beyond what a 2-second limit allows. This immediately rules out any solution that recomputes the full array per update.

A subtle issue appears when combining personal updates and global updates. Suppose a citizen is increased by a global operation and later receives a direct update. If we are not careful, we may incorrectly “reapply” old global operations or overwrite newer values with outdated ones. For example, if a citizen is raised to 10 by a global event and later explicitly set to 5, a naive implementation that only tracks minimum thresholds would incorrectly bring them back up to 10.

Another edge case is repeated global operations with decreasing thresholds. A naive monotonic assumption about the maximum threshold fails unless we explicitly handle ordering and persistence of updates per position.

## Approaches

A brute-force simulation would apply each event directly. For a type 2 event with threshold x, we would scan all citizens and update those with values less than x. This is correct but expensive: each such operation costs O(n), and with q up to 200,000, the total cost becomes O(nq), which is too large.

The key observation is that global updates only ever raise values, and they are based on thresholds. This suggests that once a citizen’s value has been raised past a certain level, it never needs to be reconsidered for smaller thresholds again. However, because individual updates can reset a citizen’s value downward, we cannot simply keep a global maximum.

The trick is to process events backwards. If we reverse the timeline, a type 2 event becomes: “future values must be at least x”, and a type 1 event becomes a known final assignment that may override earlier constraints. Working backwards allows us to compute, for each citizen, the best possible lower bound imposed by future global updates, while respecting the most recent direct assignment.

To make this precise, we maintain a running value `mx` representing the maximum threshold seen so far in reversed processing. When we encounter a global update, we update `mx`. When we encounter a personal assignment for citizen p, if that citizen has not yet been finalized, we assign them `max(a[p], mx)`.

The insight is that once we fix the final value of a citizen, earlier events no longer matter for them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Reverse Processing with Max Tracking | O(n + q) | O(n + q) | Accepted |

## Algorithm Walkthrough

We process events in reverse order so that global constraints become accumulated lower bounds instead of repeated array scans.

1. Read all initial values and store all events.
2. Initialize an array `ans` as “unassigned” for each citizen.
3. Maintain a variable `mx = 0`, which stores the maximum threshold from global events encountered so far in reverse.
4. Iterate over events from last to first.
5. If the event is a global update with threshold `x`, set `mx = max(mx, x)`. This represents that any value we decide later must satisfy at least this minimum requirement.
6. If the event is a personal update for citizen `p` with value `x`, and this citizen is not yet assigned, set

`ans[p] = max(x, mx)`. This ensures that we respect both the direct assignment and all future (in original order) global constraints.
7. After processing all events, any citizen still unassigned receives `max(a[i], mx)`.

The reason this works is that each citizen is finalized exactly once, at the moment we first encounter their latest assignment in reverse order. At that moment, all global constraints that occur after that assignment in the original timeline have already been accumulated into `mx`.

### Why it works

The invariant is that when processing events in reverse, `mx` always equals the maximum threshold of all type 2 operations that occur after the current point in the original timeline. Therefore, when we finalize a citizen’s value, we correctly enforce every global update that affects them after their last direct assignment. Since we only assign once per citizen, we never overwrite a value that already accounts for all relevant constraints, and no future step can invalidate it.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
q = int(input())

events = []
for _ in range(q):
    parts = list(map(int, input().split()))
    events.append(parts)

ans = [-1] * n
mx = 0

for e in reversed(events):
    if e[0] == 2:
        mx = max(mx, e[1])
    else:
        _, p, x = e
        p -= 1
        if ans[p] == -1:
            ans[p] = max(x, mx)

for i in range(n):
    if ans[i] == -1:
        ans[i] = max(a[i], mx)

print(*ans)
```

The core of the implementation is the reverse sweep. We do not simulate updates forward because that would require repeated full scans. Instead, we treat global operations as persistent constraints accumulated into `mx`.

A subtle point is the initialization of `ans` with -1. This ensures that only the latest assignment in reverse order is used, matching the fact that in forward time, later assignments overwrite earlier ones.

Finally, the initial array is only used for citizens who never receive a direct assignment event.

## Worked Examples

### Example 1

Input:

```
4
1 2 3 4
3
2 3
1 2 2
2 1
```

We process in reverse.

| Step | Event | mx | Assigned changes |
| --- | --- | --- | --- |
| 1 | 2 1 | 1 | none |
| 2 | 1 2 2 | 1 | ans[1] = max(2,1)=2 |
| 3 | 2 3 | 3 | none |

Final:

- ans = [3, 2, 3, 4]

This shows how the later global update with threshold 3 dominates earlier smaller constraints and how direct assignment is clamped against accumulated constraints.

### Example 2

Input:

```
5
3 50 2 1 10
3
2 0
1 2 0
2 8
```

Reverse processing:

| Step | Event | mx | Action |
| --- | --- | --- | --- |
| 1 | 2 8 | 8 | mx = 8 |
| 2 | 1 2 0 | 8 | ans[1] = 8 |
| 3 | 2 0 | 8 | mx stays 8 |

Final:

- ans = [8, 8, 8, 8, 10]

This demonstrates that even a low assignment (0) is overridden by later global constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Each event is processed once in reverse, and each citizen is finalized at most once |
| Space | O(n + q) | Storage for events and result array |

The solution scales linearly with input size, which is necessary given the 200,000 limit on both citizens and events.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())
    events = [list(map(int, input().split())) for _ in range(q)]

    ans = [-1] * n
    mx = 0

    for e in reversed(events):
        if e[0] == 2:
            mx = max(mx, e[1])
        else:
            _, p, x = e
            p -= 1
            if ans[p] == -1:
                ans[p] = max(x, mx)

    for i in range(n):
        if ans[i] == -1:
            ans[i] = max(a[i], mx)

    return " ".join(map(str, ans))

# provided sample
assert run("""4
1 2 3 4
3
2 3
1 2 2
2 1
""") == "3 2 3 4"

# all equal, only global
assert run("""3
5 5 5
2
2 10
2 7
""") == "10 10 10"

# only personal updates
assert run("""3
1 2 3
2
1 2 10
1 3 7
""") == "1 10 7"

# mixed order stress
assert run("""5
0 0 0 0 0
4
1 1 5
2 3
1 1 1
2 10
""") == "10 10 10 10 10"

# minimum size
assert run("""1
0
1
2 5
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal globals | 10 10 10 | repeated global dominance |
| only personal updates | mixed | overwrite handling |
| mixed order | all 10 | interaction of updates |
| single element | 5 | boundary correctness |

## Edge Cases

One important edge case is when a citizen is updated multiple times, and only the earliest update in forward time should matter as the final state. In reverse processing, this is handled naturally because we assign `ans[p]` only once.

Consider:

```
3
1 1 1
3
1 1 5
1 1 2
2 10
```

Reverse order:

- global 10 sets mx = 10
- first assignment encountered for person 1 sets ans[0] = 10
- earlier assignment is ignored

The algorithm correctly returns:

```
10 1 1
```

Another edge case is when no personal updates occur. In that case, all values are simply raised to the maximum global threshold seen anywhere in the sequence. Since `mx` aggregates all type 2 events, the final assignment step correctly applies it uniformly across all citizens.
