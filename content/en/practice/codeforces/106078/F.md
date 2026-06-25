---
title: "CF 106078F - Jupiter"
description: "The problem models a system where you are given a collection of time intervals, and each interval represents an event that can either contribute to or consume some resource, depending on its type."
date: "2026-06-25T12:09:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106078
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 9-17-25 Div. 1 (Advanced)"
rating: 0
weight: 106078
solve_time_s: 37
verified: true
draft: false
---

[CF 106078F - Jupiter](https://codeforces.com/problemset/problem/106078/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a system where you are given a collection of time intervals, and each interval represents an event that can either contribute to or consume some resource, depending on its type. Each event has a time and a label that determines whether it behaves like an “opening” action or a “closing” action in a scheduling process. The task is to determine the maximum number of complete pairs of compatible events that can be formed under the constraint that pairing is only valid if the timing and ordering conditions are respected.

A more concrete way to see it is that each item can be interpreted as a directed opportunity: some events create capacity at a given moment, and others require that capacity later in time. The goal is to maximize how many requirements can be satisfied using previously created capacity, respecting time ordering.

The input consists of multiple independent scenarios. For each scenario, we read a list of events, each described by a time value and a binary flag indicating whether it is a “supply-type” event or a “demand-type” event. The output for each scenario is a single integer: the maximum number of demand events that can be matched with valid supply events.

The key constraint implication is that the number of events can be large enough that any quadratic pairing strategy is immediately infeasible. A solution that checks all pairs of supply and demand events would require O(n²) comparisons in the worst case, which breaks down once n reaches around 10⁵.

A subtle edge case arises when multiple events share identical timestamps. A naive greedy approach that processes events in arbitrary order can incorrectly pair a demand with a supply that occurs at the same time but is not actually allowed to be used depending on ordering rules. For example, if a demand and supply both occur at time 5, and the rule requires strict temporal precedence, a careless implementation might treat them as interchangeable.

Another failure case appears when all events are of the same type. If all are supply events, no pairing is possible and the answer must be zero. If all are demand events, again no pairing is possible. Any solution that assumes at least one of each type without checking degenerates incorrectly.

## Approaches

The brute-force idea is to explicitly try to match every demand event with every compatible supply event. For each demand, we scan all supplies that occur earlier in time and pick one that has not already been used. This is straightforward and correct because it enforces the pairing constraint directly.

The problem with this approach is that for each of up to n events, we may scan nearly all others. This leads to about n × n comparisons in the worst case, which becomes roughly 10¹⁰ operations when n is 10⁵. That is far beyond what a typical 2-second limit can handle.

The key structural observation is that only the ordering of events in time matters, not their absolute identities. Once we sort events by time, we are effectively simulating a timeline where we can maintain a pool of available supply capacity. Each demand either consumes one unit from this pool or is skipped if the pool is empty.

This transforms the problem into a single pass greedy process. Instead of trying all pairings, we maintain a counter representing how many unused supply events we have seen so far. When we encounter a demand event, we match it immediately if possible, consuming one unit from the counter. When we encounter a supply event, we increase the counter.

This works because any optimal solution never benefits from postponing a supply match in favor of an earlier one that is strictly worse in time ordering. The earliest available supply is always at least as good as any later one for satisfying future demands.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Sort + Greedy Counter | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

1. Read all events in a test case and represent each as a pair of (time, type). This step is necessary to linearize the problem into a form where ordering becomes meaningful.
2. Sort all events by increasing time. This ensures we process the timeline in the exact order events occur, which is required because pairing depends on temporal feasibility.
3. Initialize a counter `available` to zero. This variable tracks how many supply-type events have been seen and are still unused.
4. Iterate through the sorted events. For each event, branch based on its type.
5. If the event is a supply event, increment `available` by one. This represents adding one unit of usable capacity into the system at that time.
6. If the event is a demand event, check whether `available` is positive. If it is, decrement `available` and increase the answer by one, because we can match this demand with some previously seen supply.
7. If `available` is zero when processing a demand, skip it. This means no earlier supply exists that can satisfy it.

### Why it works

At every point in time, `available` represents exactly the number of supply events that have occurred but have not yet been assigned to a demand. Any valid matching must pair each demand with a distinct earlier supply, and the greedy procedure always uses the earliest available supply implicitly by only tracking counts rather than identities. Because future decisions never depend on which specific supply was used, only on how many remain, the counter fully captures all relevant state. This invariant ensures that whenever a demand is matched, replacing that choice with any other earlier unused supply does not change feasibility for the remaining suffix of the timeline.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        events = []
        for _ in range(n):
            time, typ = map(int, input().split())
            events.append((time, typ))

        events.sort()

        available = 0
        ans = 0

        for time, typ in events:
            if typ == 0:
                available += 1
            else:
                if available > 0:
                    available -= 1
                    ans += 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm directly. Sorting is the only non-linear step, and it establishes the temporal structure required for the greedy sweep. The integer `available` is the entire state of the system, which avoids any need for explicit matching structures.

One common implementation mistake is mixing up the interpretation of the type flag. If supply and demand are inverted, the algorithm still runs but produces systematically incorrect results, often appearing plausible on small tests. Another issue is forgetting to sort by time, which breaks the assumption that earlier supplies are always processed first and leads to incorrect pairing order.

## Worked Examples

### Example 1

Consider events: (1, supply), (2, demand), (3, supply), (4, demand)

After sorting, the order is unchanged.

| Event | Available | Answer |
| --- | --- | --- |
| (1,supply) | 1 | 0 |
| (2,demand) | 0 | 1 |
| (3,supply) | 1 | 1 |
| (4,demand) | 0 | 2 |

This trace shows that each demand is matched with the earliest possible supply, confirming the greedy invariant that no supply is wasted unnecessarily.

### Example 2

Consider events: (1,demand), (2,supply), (3,demand), (4,supply)

| Event | Available | Answer |
| --- | --- | --- |
| (1,demand) | 0 | 0 |
| (2,supply) | 1 | 0 |
| (3,demand) | 0 | 1 |
| (4,supply) | 1 | 1 |

This demonstrates that demands arriving before any supply are correctly ignored, while later supplies are still useful for future demands.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, single pass afterward |
| Space | O(n) | storage of event list |

The constraints typical for a Codeforces problem with up to around 10⁵ events make this solution safe, since sorting 10⁵ elements and performing a linear sweep is well within limits for Python and C++ under standard time constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    return solve()  # adjust if solve prints directly

# sample-like cases
assert run("1\n4\n1 0\n2 1\n3 0\n4 1\n") == "2\n"

# minimum case
assert run("1\n1\n1 1\n") == "0\n"

# all supply
assert run("1\n3\n1 0\n2 0\n3 0\n") == "0\n"

# all demand
assert run("1\n3\n1 1\n2 1\n3 1\n") == "0\n"

# unsorted input stress
assert run("1\n5\n5 1\n1 0\n3 1\n2 0\n4 0\n") == "2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 mixed events | 2 | basic pairing correctness |
| single demand | 0 | no supply edge case |
| all supply | 0 | no demand handling |
| all demand | 0 | empty pool behavior |
| shuffled times | 2 | sorting requirement |

## Edge Cases

One important edge case is when a demand appears before any supply. For input `(1,demand) (2,supply)`, the algorithm processes demand first and correctly does nothing because `available` is zero. When the supply arrives later, it becomes usable only for future demands, never retroactively, which preserves correctness.

Another case is multiple supplies before a single demand. For `(1,supply) (2,supply) (3,demand)`, the counter increases twice before being consumed once, leaving one unused supply. The algorithm naturally preserves leftover capacity for later demands without any additional bookkeeping.

A final subtle case is interleaving where greedy order matters visually but not logically, such as `(1,supply) (2,demand) (3,demand)`. The first demand consumes the only available supply, and the second demand is skipped. Any alternative interpretation that tries to “reserve” supply for later demands would not improve the result because supplies are indistinguishable in contribution.
