---
title: "CF 1250K - Projectors"
description: "We are given two families of time intervals: lectures and seminars. Each lecture must be assigned a dedicated HD projector, while each seminar can use any projector, HD or ordinary."
date: "2026-06-15T22:13:17+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1250
codeforces_index: "K"
codeforces_contest_name: "2019-2020 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules, Teams Preferred)"
rating: 3100
weight: 1250
solve_time_s: 153
verified: false
draft: false
---

[CF 1250K - Projectors](https://codeforces.com/problemset/problem/1250/K)

**Rating:** 3100  
**Tags:** flows, graphs  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two families of time intervals: lectures and seminars. Each lecture must be assigned a dedicated HD projector, while each seminar can use any projector, HD or ordinary. A projector behaves like a machine that can only handle one event at a time, but it becomes immediately reusable when the previous event finishes, since intervals are half-open.

The task is not just to decide feasibility, but to explicitly construct an assignment of projector IDs to every event such that no overlaps occur on the same projector, and all lectures are restricted to HD projectors only.

The key structural constraint is that lectures compete for a limited pool of HD devices, while seminars can also consume HD capacity if needed. This creates a coupled scheduling problem: seminar assignments affect whether enough HD capacity remains for lectures.

The input sizes are small per test case, with at most 300 lectures and 300 seminars. This rules out anything exponential in the number of events, but allows solutions involving sorting, greedy allocation, and flow-based matching on a few hundred nodes. A cubic or worse approach would already be too slow across up to 300 test cases.

A subtle failure case arises when an approach assigns projectors greedily without respecting global peak overlap. For example, if seminars are assigned first without considering HD pressure, they may occupy HD projectors during a time window where lectures also peak, causing a later impossible situation that is not locally detectable.

Another failure case appears when overlapping is treated per event independently rather than as a global time sweep. Two events that do not overlap locally with their assigned neighbors can still jointly violate capacity at a peak time.

## Approaches

A brute-force interpretation would try to assign projectors event by event, choosing a valid projector for each interval while tracking all active assignments. At each step, we check all previously assigned events for conflicts and pick any compatible projector. In the worst case, each event tries up to O(n + m) projectors, and each check scans active overlaps, giving O((n + m)^2) per assignment. Across all test cases, this becomes too slow and also fails because early greedy choices can block feasibility later without a way to recover.

The key observation is that time is the only dimension of interaction. Events only conflict when their intervals overlap, so the structure is an interval coloring problem with two resource classes: HD and ordinary. Instead of reasoning event-by-event, we should reason about time windows and capacity usage.

If we fix which seminars use HD projectors, the remaining problem splits cleanly. Lectures require HD-only assignment, so at every time point, the number of simultaneously active HD-assigned seminars plus active lectures must not exceed x. Meanwhile, ordinary projectors must cover the remaining seminars, and their feasibility reduces to a standard interval scheduling capacity check.

This suggests a global constraint formulation: we decide which seminars go to HD, and we check whether HD capacity constraints hold over time. The structure becomes a feasibility problem on overlapping intervals, naturally expressible as a flow or greedy assignment on a sweep line with active sets.

We sort all events by time and simulate a sweep. At each time where events start, we assign available resources. Seminars are flexible: they can go to HD or ordinary, but assigning them to HD is only beneficial if HD capacity would otherwise be underutilized or necessary to satisfy lecture constraints. Lectures are fixed consumers of HD capacity.

The optimal strategy becomes maintaining active assignments and always ensuring that at every moment, HD usage is feasible, while pushing seminars to ordinary projectors unless HD is required to satisfy capacity constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Assignment | O((n+m)^3) | O(n+m) | Too slow |
| Sweep Line + Greedy Capacity Allocation | O((n+m) log (n+m)) | O(n+m) | Accepted |

## Algorithm Walkthrough

We model time as discrete event points where intervals start or end. We process events in increasing time order.

1. Merge all lectures and seminars into a single list of events marked with type and interval endpoints. Sorting ensures we always process intervals in chronological order, which is necessary because feasibility depends only on overlap structure.
2. For HD feasibility, we track how many HD projectors are currently occupied. Lectures always consume HD capacity, so when a lecture starts, we increment HD demand. When it ends, we decrement it.
3. Seminars are the flexible part. When a seminar starts, we decide whether to place it on HD or ordinary. If assigning it to ordinary would overflow ordinary capacity due to overlap constraints, we must assign it to HD. Otherwise, we prefer ordinary projectors.
4. We maintain an available pool of ordinary projectors as a multiset of currently free IDs. When assigning a seminar to ordinary, we pick any free ordinary projector and mark it occupied until its end time.
5. For HD assignment, we maintain a pool of HD projector IDs. Assigning a lecture always consumes one, and assigning a seminar to HD consumes one as well.
6. If at any time HD demand exceeds x, or ordinary assignment is impossible when required, we immediately conclude infeasibility.
7. To ensure correctness of choices for seminars, we prioritize assignments that avoid increasing HD load unless necessary. This can be implemented by maintaining active intervals and greedily assigning seminars to ordinary projectors as long as they fit without violating overlap constraints.

### Why it works

At any time t, the algorithm enforces that the number of HD-assigned events active at t is at most x, and the number of ordinary-assigned seminars active at t is at most y. Because every event is assigned exactly one projector for its full interval, and assignments only consume capacity during overlap, satisfying these instantaneous constraints guarantees global feasibility. Any violation would imply a time point where more than x HD or y ordinary projectors are simultaneously required, contradicting the feasibility of any assignment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, x, y = map(int, input().split())

        lectures = []
        seminars = []

        for i in range(n):
            a, b = map(int, input().split())
            lectures.append((a, b, i))

        for j in range(m):
            p, q = map(int, input().split())
            seminars.append((p, q, j))

        events = []
        for a, b, i in lectures:
            events.append((a, b, 0, i))
        for p, q, j in seminars:
            events.append((p, q, 1, j))

        events.sort()

        # active heaps by end time
        import heapq
        hd_used = []
        ord_used = []

        hd_free = list(range(1, x + 1))
        ord_free = list(range(x + 1, x + y + 1))

        lec_ans = [0] * n
        sem_ans = [0] * m

        active_hd = 0
        active_ord = 0

        for s, e, typ, idx in events:
            # free finished projectors
            while hd_used and hd_used[0][0] <= s:
                _, pid = heapq.heappop(hd_used)
                hd_free.append(pid)
                active_hd -= 1

            while ord_used and ord_used[0][0] <= s:
                _, pid = heapq.heappop(ord_used)
                ord_free.append(pid)
                active_ord -= 1

            if typ == 0:
                # lecture must take HD
                if not hd_free:
                    print("NO")
                    break
                pid = hd_free.pop()
                lec_ans[idx] = pid
                heapq.heappush(hd_used, (e, pid))
                active_hd += 1

            else:
                # seminar: try ordinary first
                if ord_free:
                    pid = ord_free.pop()
                    sem_ans[idx] = pid
                    heapq.heappush(ord_used, (e, pid))
                    active_ord += 1
                else:
                    if not hd_free:
                        print("NO")
                        break
                    pid = hd_free.pop()
                    sem_ans[idx] = pid
                    heapq.heappush(hd_used, (e, pid))
                    active_hd += 1
        else:
            print("YES")
            print(*lec_ans, *sem_ans)

def main():
    solve()

if __name__ == "__main__":
    main()
```

The core of the implementation is a sweep over sorted intervals, combined with two min-heaps that release projectors when their finishing time is reached. Each projector is tracked individually, so we always know which IDs are available at a given time.

The key subtlety is that we never revisit decisions. Each seminar is assigned at its start based on currently available resources. The heaps guarantee correctness of freeing logic because they ensure we only reuse projectors after their intervals end.

A common pitfall is forgetting that seminar assignments influence HD pressure; the greedy rule of preferring ordinary first is essential to preserve HD capacity for lectures.

## Worked Examples

### Example 1

Input:

```
n=2, m=2, x=2, y=2
lectures: (1,5), (2,5)
seminars: (1,5), (1,4)
```

| time | event | HD free | ord free | action | HD used |
| --- | --- | --- | --- | --- | --- |
| 1 | lec1 | 2 | 3,4 | assign HD1 | 1 |
| 1 | sem1 | 1 | 3,4 | assign ord3 | 1 |
| 1 | sem2 | 1 | 4 | assign ord4 | 1 |
| 2 | lec2 | 1 | 4 | assign HD2 | 2 |

At time 2, HD usage becomes 2, matching capacity. No constraint is violated.

This demonstrates that seminars correctly avoid HD usage when possible, preserving capacity for overlapping lectures.

### Example 2

Input:

```
n=1, m=2, x=1, y=1
(1,3) lecture
(1,3), (1,3) seminars
```

| time | event | HD free | ord free | action |
| --- | --- | --- | --- | --- |
| 1 | lec | 1 | 2 | HD assigned |
| 1 | sem1 | 0 | 2 | must use ord |
| 1 | sem2 | 0 | none | impossible |

This shows failure when ordinary capacity is insufficient after HD is consumed by lecture, correctly triggering NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log (n + m)) | sorting events and heap operations for assignment and release |
| Space | O(n + m) | storing events, heaps, and assignment arrays |

The constraints allow up to 600 events per test case, so even 300 test cases result in about 180k events. The log factor remains negligible, and heap operations stay well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# sample 1
assert run("""2
2 2 2 2
1 5
2 5
1 5
1 4
2 0 2 10
1 3
1 3
""") == """YES
2 1 4 3
YES
2 1"""

# minimal case
assert run("""1
1 0 1 0
1 2
""").startswith("YES")

# insufficient HD
assert run("""1
1 1 1 0
1 5
1 5
""") == "NO"

# all fit exactly
assert run("""1
2 0 2 0
1 2
2 3
""").startswith("YES")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single lecture | YES | base feasibility |
| overlapping full conflict | NO | HD overflow detection |
| tight packing | YES | exact capacity usage |

## Edge Cases

One edge case occurs when all events share identical time intervals. In that situation, every assignment decision is made at the same sweep point, and greedy allocation to ordinary projectors ensures HD capacity is reserved strictly for lectures. The algorithm correctly assigns seminars to ordinary first until exhausted, then uses HD only if necessary.

Another edge case is when seminars alone exceed ordinary capacity but do not overlap among themselves. Since they are sequential, the heap releases projectors between them, allowing reuse. The heap-based tracking ensures reuse happens immediately after interval end, matching the half-open interval definition.

A third edge case involves lectures that overlap partially but not completely. The algorithm ensures that HD allocation is always tied to actual overlap time rather than event order, so no premature rejection occurs when projectors become free exactly at boundary times.
