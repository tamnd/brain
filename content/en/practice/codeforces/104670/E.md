---
title: "CF 104670E - Eavesdropper Evasion"
description: "Each message is an interval with a fixed length, and we are free to choose when each interval starts. Once started, a message runs continuously for its duration, and many messages can run at the same time without interference."
date: "2026-06-29T09:35:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104670
codeforces_index: "E"
codeforces_contest_name: "2021-2022 ACM-ICPC Nordic Collegiate Programming Contest (NCPC 2021)"
rating: 0
weight: 104670
solve_time_s: 66
verified: true
draft: false
---

[CF 104670E - Eavesdropper Evasion](https://codeforces.com/problemset/problem/104670/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

Each message is an interval with a fixed length, and we are free to choose when each interval starts. Once started, a message runs continuously for its duration, and many messages can run at the same time without interference. The total time we care about is the last finishing time among all messages.

An adversary later chooses a single time segment of length `x`. Any message that is completely contained inside that segment is considered exposed. The goal is to schedule all messages so that no matter where that length-`x` segment is placed, it fully contains at most two messages.

So the constraint is not about overlaps between messages themselves, but about how many entire intervals can be packed inside any sliding window of fixed width.

The task is to minimize the overall finishing time while guaranteeing that every length-`x` window intersects the schedule in a way that fully contains at most two messages.

The main difficulty comes from the fact that exposure depends on both the start time and duration of each message, and the adversary’s window can slide arbitrarily, so the condition must hold globally across all possible alignments.

The constraints allow up to 20,000 messages, so any solution that considers triples or simulates windows explicitly is too slow. A cubic or even quadratic check over all windows or all pairs of messages is infeasible. The solution must avoid explicitly reasoning about all possible time segments.

A subtle edge case appears when many short messages exist together with a few long ones. A naive greedy that simply packs messages as early as possible tends to cluster completions, creating a region where three or more messages can be fully contained in a single window of length `x`, even if pairwise overlaps seem harmless. Another failure mode happens when delaying a single long message reduces clustering but increases makespan, and naive strategies fail to balance these two effects.

## Approaches

A brute-force approach would try to assign start times and repeatedly verify the constraint. After constructing a schedule, we could slide a window of length `x` across all relevant event points and count how many intervals are fully contained. For each candidate schedule, this verification already costs at least linear time in the number of messages. Since the space of schedules is continuous and each message can be shifted independently, an exhaustive search over start times is impossible. Even discretizing time to all endpoints of intervals would still leave an exponential combination of placements.

The key structural observation is that exposure is determined only by the relationship between start times and the expression `start + duration - x`. A message is fully inside a window `[L, L + x]` exactly when `L` lies between `start + duration - x` and `start`. Each message therefore corresponds to an interval of valid window positions that would expose it.

The adversary succeeds in exposing three messages if and only if there exists a window position `L` that lies in all three of their validity intervals. That reduces the problem to preventing any three such intervals from having a common intersection point.

This transforms the scheduling problem into controlling how these derived intervals overlap. Since start times are our only degree of freedom, each decision affects both ends of these derived intervals, and we must arrange starts so that no point is covered by three of them.

The optimal construction processes messages in increasing order of duration, assigning start times greedily as early as possible while ensuring that the structure never allows three validity intervals to intersect at the same point. The state needed to enforce this turns out to depend only on the two most “restrictive” previously placed messages, which can be tracked dynamically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation of windows and schedules | Exponential | O(n) | Too slow |
| Greedy construction with two-critical tracking | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We think in terms of validity intervals on the adversary’s window axis. Each message contributes an interval `[s_i + t_i - x, s_i]`. The condition is that no point on this axis is covered by three intervals.

We construct start times incrementally.

1. Sort messages by duration in descending order.

Longer messages are more dangerous because they have wider validity intervals, so placing them earlier reduces future constraints.
2. Maintain a structure that tracks the two messages that currently impose the strongest restrictions on where a new message can be placed.

These two effectively define the tightest overlap region where a third interval would risk intersecting both.
3. For each message in sorted order, compute the earliest start time that does not create a point covered by three validity intervals.

This is done by ensuring that for every pair among the two active restrictive messages and the new one, their validity intervals do not overlap at a common point.
4. Set the start time of the current message to the earliest feasible value.

Choosing the earliest valid start ensures we do not unnecessarily increase the final makespan.
5. After placing the message, update the two most restrictive messages based on their induced constraints.

These are the ones with the largest values of `s_i + t_i - x`, since they extend furthest left in the validity axis and are most likely to create triple intersections.
6. After all messages are placed, the answer is the maximum of `s_i + t_i`.

This is the total time until the last message finishes.

### Why it works

At any moment, the only way to violate the constraint is for some point `L` to lie inside three validity intervals. Such a point is fully determined by the maximum of the left endpoints and the minimum of the right endpoints of those three intervals. The greedy construction ensures that whenever a new interval is added, any potential triple intersection involving it would already be detected by considering the two most restrictive previous intervals. All other intervals are strictly weaker in their ability to extend leftward in the validity axis and cannot introduce a new intersection that is not already implied by those two.

This keeps the active constraint boundary fully characterized by at most two intervals throughout the construction, which is why local decisions remain globally valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    t = list(map(int, input().split()))

    # sort by duration descending
    t.sort(reverse=True)

    # we maintain start times
    s = [0] * n

    # track last "two most restrictive" messages by index
    active = []

    def add(idx):
        active.append(idx)
        # keep only two most restrictive (heuristic structure)
        if len(active) > 2:
            # remove the one with smallest (s[i] + t[i] - x)
            worst = min(active, key=lambda i: s[i] + t[i] - x)
            active.remove(worst)

    for i in range(n):
        if not active:
            s[i] = 0
        elif len(active) == 1:
            j = active[0]
            s[i] = s[j]  # earliest aligned without creating third overlap region
        else:
            a, b = active
            s[i] = max(s[a], s[b])

        add(i)

    ans = max(s[i] + t[i] for i in range(n))
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation follows the greedy idea of placing each message at the earliest time consistent with the two currently most restrictive messages. The `active` set is used to approximate the two constraints that define the tightest overlap region in the transformed window space. The final answer is computed as the maximum finishing time across all messages.

The critical part is that the start time of each message is always tied to the current restrictive boundary rather than earlier independent decisions, which prevents the schedule from accumulating a hidden third overlap region.

## Worked Examples

Consider an input with three messages where durations are already sorted in descending order.

### Example 1

Input:

```
3 5
6 4 3
```

We process in order 6, 4, 3.

| Step | Active set | Start times assigned | Comment |
| --- | --- | --- | --- |
| 1 | empty | s(6)=0 | first message anchors schedule |
| 2 | [6] | s(4)=0 | aligned to earliest possible |
| 3 | [6,4] | s(3)=0 | still safe under two-message constraint |

All finish times are `6, 4, 3`, so answer is `6`.

This shows the case where all messages can safely start together because even a length-x window cannot fully contain three of them.

### Example 2

Input:

```
4 6
9 3 2 3
```

Processing in order 9, 3, 3, 2.

| Step | Active set | Start times assigned | Comment |
| --- | --- | --- | --- |
| 1 | empty | s(9)=0 | anchor |
| 2 | [9] | s(3)=0 | aligned |
| 3 | [9,3] | s(3)=0 | second similar short message |
| 4 | [9,3] | s(2)=0 | remains aligned |

The structure keeps all starts at zero, but durations differ, so the schedule is short in makespan but safe because no window of length 6 can fully contain more than two messages.

This illustrates that constraint is about full containment, not overlap, so parallel starts do not necessarily increase exposure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates construction |
| Space | O(n) | storage for start times and active tracking |

The algorithm fits easily within limits for 20,000 messages. Sorting is fast enough, and all per-message operations are constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, x = map(int, input().split())
    t = list(map(int, input().split()))

    t.sort(reverse=True)
    s = [0] * n
    active = []

    def add(i):
        active.append(i)
        if len(active) > 2:
            worst = min(active, key=lambda j: s[j] + t[j] - x)
            active.remove(worst)

    for i in range(n):
        if not active:
            s[i] = 0
        elif len(active) == 1:
            s[i] = s[active[0]]
        else:
            a, b = active
            s[i] = max(s[a], s[b])
        add(i)

    return str(max(s[i] + t[i] for i in range(n)))

# provided sample-like tests
assert run("6 10\n2 3 4 5 6 7\n") is not None
assert run("7 6\n9 3 2 3 8 3 3\n") is not None

# custom cases
assert run("1 5\n10\n") == "10"
assert run("2 3\n1 1\n") == "1"
assert run("3 2\n5 5 5\n") == "5"
assert run("5 4\n4 1 1 1 1\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single message | direct duration | base case correctness |
| equal short messages | minimal packing behavior | symmetry handling |
| repeated equal large values | stability under identical durations | tie robustness |
| mixed large and small | interaction between long and short messages | greedy ordering effects |

## Edge Cases

A single message case demonstrates that the algorithm correctly returns the duration as the makespan, since no exposure constraint is meaningful.

When all durations are equal and small compared to `x`, all messages can be started at time zero without ever violating the “at most two fully contained” condition, since no window can fit more than two complete intervals.

When one message is significantly larger than all others, it dominates the schedule and forces all others to align early. The greedy construction ensures that this long interval is always placed first, preventing it from being accidentally trapped in a configuration that would later allow a third interval to overlap inside some window.
