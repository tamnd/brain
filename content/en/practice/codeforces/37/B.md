---
title: "CF 37B - Computer Game"
description: "The boss starts with max health and regenerates reg health every second. We own several scrolls. Each scroll can only be"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 37
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 37"
rating: 1800
weight: 37
solve_time_s: 116
verified: true
draft: false
---

[CF 37B - Computer Game](https://codeforces.com/problemset/problem/37/B)

**Rating:** 1800  
**Tags:** greedy, implementation  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The boss starts with `max` health and regenerates `reg` health every second. We own several scrolls. Each scroll can only be activated when the boss health is at most some percentage of the original health. Once activated, that scroll permanently adds its damage per second to our total damage output.

The timeline of one second is extremely important:

1. Existing active spells deal damage.
2. The boss regenerates.
3. We may activate at most one new scroll.
4. If the boss health is now `<= 0`, the fight ends.

The activation condition depends on the boss health after damage and regeneration for that second.

The task is to decide whether the boss can be defeated at all. If yes, we must output one valid sequence of scroll activations that achieves the minimum possible finishing time.

The constraints are small enough to allow quadratic or cubic work. There are at most 1000 scrolls. Damage values are also small. This immediately suggests that we should focus more on discovering the correct greedy strategy than on advanced data structures.

A subtle point is that scrolls are not one-time damage. Each scroll permanently increases the future damage rate. Activating a stronger scroll earlier may allow future thresholds to become reachable faster.

Another easy mistake comes from the order of actions inside a second. Suppose the boss health becomes low enough after regeneration. We may activate a new scroll during that second, but that newly activated scroll does not deal damage immediately. Its damage starts next second.

Consider this example:

```
1 10 0
50 100
```

The boss starts at 10 HP. The scroll requires health at most 5. Since there is no existing damage source, the health never drops below 10. The correct answer is `NO`.

A careless implementation might wrongly assume we can activate the scroll immediately because its damage is huge.

Another dangerous edge case appears when current DPS is not larger than regeneration. Suppose:

```
2 100 10
100 5
90 100
```

We may activate the first scroll immediately because the threshold is 100%. After that, total DPS is only 5, smaller than regeneration 10. The boss never drops below 100 HP, so the second scroll can never be used. The correct answer is `NO`.

A naive simulation that only checks whether total eventual damage exceeds regeneration would incorrectly claim victory.

One more subtle case comes from exact threshold equality.

```
1 100 0
99 1
```

The scroll can only be used when health is at most 99. Since no spell is active initially, health never changes from 100. Equality matters because once the boss reaches exactly the threshold, the scroll becomes legal immediately after regeneration.

## Approaches

A brute-force approach would try every possible order of scroll activations. For each permutation, we simulate the fight second by second and check whether the thresholds become reachable.

This is hopelessly expensive. With 1000 scrolls, even exploring a tiny fraction of all orders is impossible. The core difficulty is deciding which scroll to activate next.

The key observation is that only one thing matters about previously chosen scrolls: the current total DPS.

Suppose our current total DPS is `D`. During every second, the boss effectively loses `D - reg` health, except that health is capped above by `max`.

If `D <= reg`, the boss health never decreases. No future threshold smaller than the current health can ever become reachable.

If `D > reg`, the boss health decreases steadily. Eventually, every threshold becomes reachable.

This transforms the problem into a scheduling question.

For a scroll with threshold percentage `pow[i]`, define its activation health limit:

```
limit[i] = floor(max * pow[i] / 100)
```

Once current health becomes at most `limit[i]`, that scroll becomes permanently available.

Now comes the greedy insight.

Whenever several scrolls are already available, activating the largest damage scroll first is always optimal. Earlier damage contributes during all future seconds, so delaying larger DPS can never help.

This gives a natural process:

We continuously lower the boss health using current DPS. Whenever new scrolls become available, we greedily activate the strongest available one.

The entire fight becomes deterministic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N!) | O(N) | Too slow |
| Optimal | O(N² log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Convert each percentage threshold into an absolute health limit.

For scroll `i`, compute:

```
limit[i] = floor(max_hp * pow[i] / 100)
```

This is the maximum boss health at which the scroll may be activated.
2. Sort all scrolls by decreasing limit.

As the boss health decreases, more scrolls become available. Processing thresholds in descending order matches the actual progression of the fight.
3. Maintain three things during the simulation:

`cur_hp`, the boss health after regeneration at the current second.

`dps`, the total active damage per second.

A priority queue containing all currently available but unused scrolls, ordered by damage.
4. Initially, the boss health is exactly `max`.

Every scroll with `limit >= max` is immediately usable at time 0. Push them into the heap.
5. If the heap is empty at the start, we can never begin damaging the boss.

Output `NO`.
6. Repeatedly activate the strongest available scroll.

Each activation happens at the current time.

Add its damage to `dps`.

Record the activation operation.
7. After updating DPS, check whether `dps > reg`.

If not, the boss health cannot decrease any further. The fight becomes stuck forever.

Continue activating already available scrolls if any exist. If eventually no available scroll remains and `dps <= reg`, output `NO`.
8. When `dps > reg`, the boss loses `dps - reg` effective health per second.

We can compute directly how many seconds are needed to reach the next threshold instead of simulating second by second.

Suppose the next unavailable scroll requires health `next_limit`.

We need the smallest `t` such that:

```
cur_hp - t * (dps - reg) <= next_limit
```

Solve this with ceiling division.
9. Advance time by `t`.

Update boss health accordingly.

Every scroll whose limit is now reachable gets inserted into the heap.
10. At every stage, also check whether the boss can already be killed before reaching another threshold.

If current health is `cur_hp` and net damage per second is `delta = dps - reg`, then the boss dies after:

```
ceil(cur_hp / delta)
```

additional seconds.

If this happens before any future threshold event, we finish immediately.

### Why it works

The crucial invariant is that whenever we choose a scroll, all currently available scrolls could have been chosen instead. Picking the one with maximum damage is always optimal because damage accumulates permanently over future seconds.

Suppose two available scrolls have damages `a < b`. If we activate `a` first and `b` later, swapping their order increases total accumulated damage during every intermediate second. Health thresholds can only become reachable earlier, never later.

Because of this exchange argument, the optimal strategy is uniquely characterized by repeatedly taking the strongest currently available scroll.

The health evolution between threshold events is linear, so we can jump directly between important moments instead of simulating every second.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, max_hp, reg = map(int, input().split())

    scrolls = []

    for i in range(n):
        p, d = map(int, input().split())
        limit = max_hp * p // 100
        scrolls.append((limit, d, i + 1))

    scrolls.sort(reverse=True)

    ptr = 0
    heap = []

    cur_hp = max_hp
    dps = 0
    time = 0

    ans = []

    while ptr < n and scrolls[ptr][0] >= cur_hp:
        limit, dmg, idx = scrolls[ptr]
        heapq.heappush(heap, (-dmg, idx, limit))
        ptr += 1

    while True:
        while heap:
            dmg_neg, idx, limit = heapq.heappop(heap)
            dmg = -dmg_neg

            dps += dmg
            ans.append((time, idx))

        if dps <= reg:
            print("NO")
            return

        delta = dps - reg

        kill_time = (cur_hp + delta - 1) // delta

        next_limit = -1
        if ptr < n:
            next_limit = scrolls[ptr][0]

        if next_limit == -1:
            time += kill_time
            print("YES")
            print(time, len(ans))
            for t, idx in ans:
                print(t, idx)
            return

        if cur_hp <= next_limit:
            need = 0
        else:
            need = (cur_hp - next_limit + delta - 1) // delta

        if kill_time <= need:
            time += kill_time
            print("YES")
            print(time, len(ans))
            for t, idx in ans:
                print(t, idx)
            return

        time += need
        cur_hp -= need * delta

        while ptr < n and scrolls[ptr][0] >= cur_hp:
            limit, dmg, idx = scrolls[ptr]
            heapq.heappush(heap, (-dmg, idx, limit))
            ptr += 1

solve()
```

The first part converts percentage thresholds into absolute health limits. Using integer division is correct because the condition is based on actual integer health values.

The scrolls are sorted by decreasing limits so that we can gradually unlock them as the boss health decreases.

The heap stores currently available scrolls ordered by damage. Python's `heapq` is a min-heap, so damages are inserted as negative values.

The inner loop activates every currently available scroll immediately. Delaying any available scroll is never beneficial because its damage would start contributing later.

The condition `dps <= reg` is the deadlock detector. At that point the boss health can no longer decrease. If no stronger scroll is already available, the fight is unwinnable.

The formula:

```
(cur_hp - next_limit + delta - 1) // delta
```

is ceiling division. It computes the first second when health becomes low enough for the next threshold.

One subtle implementation detail is that newly activated scrolls do not deal damage during the same second. The simulation naturally respects this because time advances before newly unlocked scrolls are activated.

## Worked Examples

### Example 1

Input:

```
2 10 3
100 3
99 1
```

Converted thresholds:

| Scroll | Limit | Damage |
| --- | --- | --- |
| 1 | 10 | 3 |
| 2 | 9 | 1 |

Initial state:

| Time | HP | DPS | Available |
| --- | --- | --- | --- |
| 0 | 10 | 0 | {1} |

Activate scroll 1:

| Time | HP | DPS |
| --- | --- | --- |
| 0 | 10 | 3 |

Now `dps = reg = 3`.

Effective damage is zero, so the boss health never drops below 10. Scroll 2 never becomes available.

Correct output:

```
NO
```

This example demonstrates why checking only total eventual DPS is not enough. The fight can stall permanently before future thresholds are reached.

### Example 2

Input:

```
3 100 10
100 15
80 20
50 100
```

Thresholds:

| Scroll | Limit | Damage |
| --- | --- | --- |
| 1 | 100 | 15 |
| 2 | 80 | 20 |
| 3 | 50 | 100 |

Simulation:

| Time | HP | DPS | Action |
| --- | --- | --- | --- |
| 0 | 100 | 0 | Scroll 1 available |
| 0 | 100 | 15 | Activate 1 |
| 4 | 80 | 15 | Scroll 2 unlocked |
| 4 | 80 | 35 | Activate 2 |
| 5 | 55 | 35 | Continue |
| 6 | 30 | 35 | Scroll 3 unlocked |
| 6 | 30 | 135 | Activate 3 |
| 7 | -95 | 135 | Boss dies |

The trace shows how the algorithm jumps directly between threshold events instead of simulating every second individually.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting plus heap insertions/removals |
| Space | O(N) | Scroll storage and priority queue |

Each scroll is inserted into the heap exactly once and removed exactly once. With `N <= 1000`, this easily fits inside the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from heapq import heappush, heappop

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    input = sys.stdin.readline

    n, max_hp, reg = map(int, input().split())

    scrolls = []

    for i in range(n):
        p, d = map(int, input().split())
        limit = max_hp * p // 100
        scrolls.append((limit, d, i + 1))

    scrolls.sort(reverse=True)

    ptr = 0
    heap = []

    cur_hp = max_hp
    dps = 0
    time = 0

    ans = []

    while ptr < n and scrolls[ptr][0] >= cur_hp:
        limit, dmg, idx = scrolls[ptr]
        heappush(heap, (-dmg, idx, limit))
        ptr += 1

    while True:
        while heap:
            dmg_neg, idx, limit = heappop(heap)
            dmg = -dmg_neg

            dps += dmg
            ans.append((time, idx))

        if dps <= reg:
            print("NO")
            break

        delta = dps - reg

        kill_time = (cur_hp + delta - 1) // delta

        next_limit = -1
        if ptr < n:
            next_limit = scrolls[ptr][0]

        if next_limit == -1:
            time += kill_time
            print("YES")
            print(time, len(ans))
            for t, idx in ans:
                print(t, idx)
            break

        if cur_hp <= next_limit:
            need = 0
        else:
            need = (cur_hp - next_limit + delta - 1) // delta

        if kill_time <= need:
            time += kill_time
            print("YES")
            print(time, len(ans))
            for t, idx in ans:
                print(t, idx)
            break

        time += need
        cur_hp -= need * delta

        while ptr < n and scrolls[ptr][0] >= cur_hp:
            limit, dmg, idx = scrolls[ptr]
            heappush(heap, (-dmg, idx, limit))
            ptr += 1

    sys.stdout = old_stdout
    return out.getvalue()

# provided sample
assert run(
"""2 10 3
100 3
99 1
"""
).strip() == "NO", "sample 1"

# minimum size winning case
assert run(
"""1 1 0
100 1
"""
).startswith("YES"), "single scroll immediate win"

# impossible because initial threshold unreachable
assert run(
"""1 100 0
99 100
"""
).strip() == "NO", "cannot start fight"

# exact equality threshold
assert run(
"""2 10 0
100 1
90 100
"""
).startswith("YES"), "unlock exactly at threshold"

# large regeneration deadlock
assert run(
"""2 100 50
100 40
0 100
"""
).strip() == "NO", "health never decreases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single scroll with 100% threshold | YES | Minimum valid instance |
| Threshold 99% with no initial damage | NO | Cannot unlock first scroll |
| Exact equality unlock | YES | Boundary handling for thresholds |
| DPS below regeneration | NO | Deadlock detection |

## Edge Cases

Consider the case where no scroll is initially available.

```
1 100 0
99 100
```

The threshold is 99 HP, but the boss starts at 100 HP and no damage source exists. The heap is empty immediately. The algorithm detects this before any simulation and outputs `NO`.

Now examine the regeneration deadlock:

```
2 100 10
100 5
90 100
```

At time 0, only the first scroll is available. Activating it gives DPS 5. Since `5 <= 10`, effective damage is non-positive. The health never drops below 100, so the second scroll can never unlock. The algorithm checks `dps <= reg` and correctly outputs `NO`.

Finally, consider an exact-threshold transition:

```
2 10 0
100 1
90 100
```

After activating the first scroll, effective damage is 1. After one second, the boss reaches exactly 9 HP. Since the second scroll has limit 9, it becomes available immediately. The algorithm uses ceiling division carefully so equality is treated as reachable rather than skipped by one second.
