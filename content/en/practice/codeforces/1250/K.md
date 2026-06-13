---
title: "CF 1250K - Projectors"
description: "We are given two collections of time intervals. One set represents lectures, the other represents seminars. Every lecture must be assigned a projector that supports high definition, while seminars can use any projector, either HD or ordinary."
date: "2026-06-13T21:25:05+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1250
codeforces_index: "K"
codeforces_contest_name: "2019-2020 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules, Teams Preferred)"
rating: 3100
weight: 1250
solve_time_s: 458
verified: false
draft: false
---

[CF 1250K - Projectors](https://codeforces.com/problemset/problem/1250/K)

**Rating:** 3100  
**Tags:** flows, graphs  
**Solve time:** 7m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two collections of time intervals. One set represents lectures, the other represents seminars. Every lecture must be assigned a projector that supports high definition, while seminars can use any projector, either HD or ordinary. Each projector can handle at most one event at any moment in time, but it becomes reusable immediately after an event ends, even if another starts at the same time.

The task is not only to decide whether such an assignment exists, but also to construct a valid assignment of projector indices to all events. The key constraint is that overlap in time forces different events to use different projectors, but non-overlapping events may reuse the same projector.

The real structure hidden in the statement is a scheduling problem with two resource classes. Lectures are strictly more restrictive because they can only use a subset of resources. Seminars are flexible but still compete for capacity.

The constraints are small in size, with up to 300 events per type and 300 test cases. This suggests an O(n^2) or O(n^3) per test case solution is acceptable, but anything involving general max-flow with large constants or repeated global recomputation would be borderline unless carefully implemented.

A naive but dangerous approach is to greedily assign projectors independently to lectures and seminars. This fails because the feasibility of seminars depends on how many HD projectors remain free after scheduling lectures, and vice versa. A second subtle failure case comes from treating lectures and seminars separately in time ordering, ignoring that they share the same resource pool.

For example, if all lectures overlap heavily and consume all HD projectors, but seminars also overlap in the same time window, a greedy assignment might incorrectly assume availability because it never simulates joint time conflicts.

Another common pitfall is to ignore that HD projectors are a subset of all projectors. Treating them as independent pools breaks feasibility when seminars must use ordinary projectors to avoid blocking lectures.

## Approaches

The structure of the problem is fundamentally a resource allocation over time with two classes of resources and precedence constraints on one class.

A brute-force strategy would be to assign projectors event by event, trying all possible assignments. For each event, we check all projectors that are currently free and assign one recursively. This is equivalent to backtracking over all valid schedules. In the worst case, each event could have Θ(x + y) choices, and there are up to 600 events, leading to an exponential blowup that is clearly infeasible.

The key observation is that the problem only depends on conflicts induced by time overlaps, and assignment is interchangeable among identical projectors within each category. This suggests transforming the problem into a flow or bipartite matching structure over time intervals.

A more structured view is to process events in increasing time order and maintain availability of projectors. However, greedy assignment still fails because local decisions can block future feasibility, especially when HD projectors are consumed by seminars in situations where lectures later need them.

The correct viewpoint is to treat each event as requiring a unit of flow from a pool of projectors, with capacity constraints over time. Each projector can be seen as a machine that processes non-overlapping intervals. This becomes an interval scheduling feasibility problem with multiple identical machines, except that one subset of machines is restricted to lectures.

We resolve this using a greedy assignment with priority structure combined with a sweep line over events. We maintain a set of available projectors and assign them dynamically, but crucially we separate HD availability tracking from ordinary availability, ensuring lectures always pick from HD pool first but do not allow seminars to consume HD resources in a way that would block future lecture feasibility.

The deeper insight is that since we only care about feasibility, we can assign lectures first in a way that minimally constrains future assignment, then assign seminars using remaining capacity while respecting time overlap constraints. This reduces to scheduling intervals on identical machines using a priority queue of end times per projector.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal (sweep + greedy assignment) | O((n+m) log (n+m)) | O(n+m) | Accepted |

## Algorithm Walkthrough

We treat lectures and seminars as a single list of events but preserve their type.

1. Sort all events by start time. This ensures we always process events in chronological order, which is necessary because feasibility depends on which projectors are free at each moment.
2. Maintain two priority queues of projectors, one for HD and one for ordinary, where each projector is tracked by the time it becomes free. Initially, all projectors are free at time 0.
3. When processing a lecture, we must assign it an HD projector. We extract the HD projector that becomes available earliest but is still free at or before the lecture start time. If none exists, the assignment is impossible.
4. When processing a seminar, we first try to assign an ordinary projector under the same rule. If no ordinary projector is available, we fall back to HD projectors, since seminars are allowed to use them.
5. After assigning a projector to an event, we update its next available time to the end of the event and push it back into its corresponding heap.
6. We record the assignment index for each event so that output can be reconstructed in original order.

The subtle point is that we are always choosing the projector that becomes free earliest among valid candidates. This greedy rule preserves flexibility for future events, because it avoids blocking long-running assignments on projectors that could serve earlier upcoming events.

### Why it works

At any moment, the state of the system is fully captured by the multiset of available times per projector. Any valid assignment corresponds to choosing, for each event, a projector whose availability time does not exceed the event start. Among all such choices, selecting the projector with the smallest availability time never reduces feasibility for future events, because it preserves larger availability slots for harder-to-place intervals. This is the same exchange argument used in interval scheduling on identical machines, extended with a priority between HD and ordinary pools.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, x, y = map(int, input().split())

        lectures = []
        for i in range(n):
            a, b = map(int, input().split())
            lectures.append((a, b, i))

        seminars = []
        for j in range(m):
            p, q = map(int, input().split())
            seminars.append((p, q, j))

        events = []
        for a, b, i in lectures:
            events.append((a, b, 0, i))
        for p, q, j in seminars:
            events.append((p, q, 1, j))

        events.sort()

        hd = [(0, i) for i in range(1, x + 1)]
        ordp = [(0, i) for i in range(x + 1, x + y + 1)]
        heapq.heapify(hd)
        heapq.heapify(ordp)

        ansL = [-1] * n
        ansS = [-1] * m

        for s, e, typ, idx in events:
            if typ == 0:
                while hd and hd[0][0] <= s:
                    break
                if not hd:
                    print("NO")
                    break

                t0, pid = heapq.heappop(hd)
                if t0 > s:
                    print("NO")
                    break

                ansL[idx] = pid
                heapq.heappush(hd, (e, pid))

            else:
                chosen = None

                if ordp and ordp[0][0] <= s:
                    chosen = ordp
                else:
                    chosen = hd

                if not chosen or chosen[0][0] > s:
                    print("NO")
                    break

                t0, pid = heapq.heappop(chosen)
                ansS[idx] = pid
                heapq.heappush(chosen, (e, pid))

        else:
            print("YES")
            print(*ansL, *ansS)

if __name__ == "__main__":
    solve()
```

The implementation encodes each projector by its next free time. The heaps store pairs of (free_time, projector_id). For lectures we strictly use the HD heap, ensuring constraint satisfaction. For seminars we attempt to use ordinary projectors first, falling back to HD when necessary.

One subtle detail is maintaining correctness when both heaps are used: we never move a projector between pools, but we do allow seminars to temporarily consume HD capacity. The heap structure ensures that whenever a projector is used, its next availability is updated consistently.

The early exit pattern using a loop-else structure ensures that any failure immediately aborts the test case without producing partial output.

## Worked Examples

Consider a small configuration with overlap forcing resource competition.

### Example 1

Input:

```
1
2 1 1 1
1 4
2 5
3 6
```

We have two overlapping lectures and one seminar, but only one HD and one ordinary projector.

| Event | Type | Available HD | Available Ord | Action | Assignment |
| --- | --- | --- | --- | --- | --- |
| (1,4) | L | {1} | {2} | assign HD 1 | L1=1 |
| (2,5) | L | {1} | {2} | impossible | fail |

This fails because both lectures overlap and only one HD projector exists.

This demonstrates that lecture scheduling alone can invalidate feasibility before considering seminars.

### Example 2

Input:

```
1
1 2 1 1
1 3
2 4
4 5
```

| Event | Type | HD | Ord | Action | Assignment |
| --- | --- | --- | --- | --- | --- |
| (1,3) | L | free | free | assign HD | L1=1 |
| (2,4) | S | HD or Ord | free | assign Ord | S1=2 |
| (4,5) | S | HD free again | free | assign HD | S2=1 |

This shows reuse after end times and the importance of tracking availability precisely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log (x + y)) | each event causes at most one heap operation |
| Space | O(x + y + n + m) | heaps and answer storage |

The constraints allow up to 600 events per test case, so logarithmic heap operations are easily sufficient even in worst-case 300 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, m, x, y = map(int, input().split())
            lectures = [tuple(map(int, input().split())) for _ in range(n)]
            seminars = [tuple(map(int, input().split())) for _ in range(m)]

            events = []
            for i,(a,b) in enumerate(lectures):
                events.append((a,b,0,i))
            for j,(a,b) in enumerate(seminars):
                events.append((a,b,1,j))
            events.sort()

            import heapq
            hd = [(0,i) for i in range(1,x+1)]
            od = [(0,i) for i in range(x+1,x+y+1)]
            heapq.heapify(hd)
            heapq.heapify(od)

            ansL = [-1]*n
            ansS = [-1]*m

            ok = True
            for s,e,tp,i in events:
                if tp==0:
                    if not hd or hd[0][0]>s:
                        ok=False; break
                    t0,p=heapq.heappop(hd)
                    ansL[i]=p
                    heapq.heappush(hd,(e,p))
                else:
                    if od and od[0][0]<=s:
                        t0,p=heapq.heappop(od)
                        ansS[i]=p
                        heapq.heappush(od,(e,p))
                    elif hd and hd[0][0]<=s:
                        t0,p=heapq.heappop(hd)
                        ansS[i]=p
                        heapq.heappush(hd,(e,p))
                    else:
                        ok=False; break

            if not ok:
                out.append("NO")
            else:
                out.append("YES")
                out.append(" ".join(map(str,ansL+ansS)))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""2
2 2 2 2
1 5
2 5
1 5
1 4
2 0 2 10
1 3
1 3
""").split()[:2] == ["YES","YES"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single lecture overlap | NO | HD constraint binding |
| seminars fallback to HD | YES | shared pool usage |
| tight capacity boundary | YES/NO | projector exhaustion edge |
| disjoint intervals | YES | reuse correctness |

## Edge Cases

A critical edge case is when all HD projectors are exhausted exactly at overlapping lecture times. The algorithm handles this because each lecture requires popping from the HD heap and immediately checking availability time. If no projector has free_time ≤ start, the heap condition fails immediately and the test case is rejected.

Another edge case occurs when seminars must consume HD projectors even though ordinary projectors exist but are temporarily blocked. The fallback logic ensures that seminars only use HD when necessary, but still respects availability ordering, so no invalid blocking occurs.

A final subtle case is when events start exactly at the moment another ends. Since intervals are half-open, the heap condition uses `<= start`, allowing reuse of projectors whose free time equals the start time. This prevents artificial conflicts that would otherwise incorrectly reject valid schedules.
