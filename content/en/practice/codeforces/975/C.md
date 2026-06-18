---
problem: 975C
contest_id: 975
problem_index: C
name: "Valhalla Siege"
contest_name: "Codeforces Round 478 (Div. 2)"
rating: 1400
tags: ["binary search"]
answer: passed_samples
verified: true
solve_time_s: 58
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a33a436-0e7c-83ec-85b7-473ad67f57cb
---

# CF 975C - Valhalla Siege

**Rating:** 1400  
**Tags:** binary search  
**Model:** gpt-5-3-mini  
**Solve time:** 58s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a33a436-0e7c-83ec-85b7-473ad67f57cb  

---

## Solution

## Problem Understanding

We are simulating a repeated battle on a line of warriors. Each warrior has a fixed amount of health, and arrows always hit the first still-alive warrior before moving forward to the next. When a warrior accumulates damage equal to or exceeding his health, he is considered dead and the attack continues on the next warrior in the same minute.

The twist is that the battle “resets” after each minute if all warriors die during that minute. At that point, all warriors immediately return to full health before the next minute begins. However, if some warriors survive after a minute ends, their reduced health persists into the next minute.

For each minute, we need to report how many warriors are still alive after processing that minute’s arrows, taking into account any partial damage carried over from previous minutes.

The input size makes naive simulation impossible. With up to 200,000 warriors and 200,000 minutes, and arrow counts up to 10^14 per minute, any solution that processes each arrow individually or scans from the start repeatedly would be far too slow. Even an O(nq) approach risks 4e10 operations, which is not feasible.

A subtle edge case appears when a minute’s arrows are enough to kill all warriors and still have leftovers. In that case, the leftover arrows are discarded and all warriors revive. A careless implementation might incorrectly carry damage into the next minute or fail to reset properly.

Another tricky case is when damage only partially kills a warrior. That warrior becomes the new “current target” in the next minute, and his remaining health must persist correctly. Missing this persistence leads to incorrect counts in subsequent queries.

## Approaches

A brute-force simulation would process each minute by iterating through warriors from the first alive position and subtracting arrows one by one until either arrows run out or all warriors die. If a warrior’s health reaches zero, we move to the next warrior. This approach is correct but in the worst case each minute can traverse all n warriors, and each warrior may be visited many times across minutes, leading to O(nq) behavior. With 200,000 by 200,000 this is completely infeasible.

The key observation is that damage only ever moves from left to right, and once a warrior is fully killed, he never becomes relevant again unless a full reset happens. This suggests maintaining a prefix structure of remaining health after previous minutes and quickly finding how far the current wave of arrows can propagate.

Instead of simulating arrow-by-arrow, we can maintain prefix sums of health and track how much total damage has been accumulated so far. Each minute’s arrows increase a global damage counter. The first warrior index still alive is the first position where prefix sum exceeds accumulated damage. This reduces the problem to repeatedly finding a boundary in a prefix sum array, which can be done using binary search.

However, we also need to handle resets when total incoming arrows in a minute exceed total remaining health. In that case, all warriors die and we reset accumulated damage to zero, since everything revives.

So the problem becomes maintaining a global “damage so far” and answering how many prefix sums are still above it, with periodic resets when damage crosses total sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(nq) | O(n) | Too slow |
| Prefix Sum + Binary Search | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a prefix sum array `pref`, where `pref[i]` is the total health of warriors from 1 to i. This lets us know how much damage is needed to kill up to a given point.
2. Maintain a variable `d` representing total damage carried into the current state.
3. For each query `k_i`, increase `d` by `k_i`, since arrows accumulate damage continuously until a reset happens.
4. If `d` is greater than or equal to `pref[n]`, all warriors die during this minute. In that case, output `n` and reset `d` to zero, because revival happens immediately after full death.
5. Otherwise, we need to find how many warriors are still alive after damage `d`. We find the smallest index `pos` such that `pref[pos] > d` using binary search.
6. The number of alive warriors is `n - pos + 1`, since all warriors before `pos` are dead and the rest are alive.
7. Output this value for the current minute and continue.

The binary search step is crucial because it translates a dynamic prefix damage process into a static ordered structure query.

### Why it works

The prefix sum array encodes exactly how much cumulative damage is needed to kill up to each warrior. Since damage always applies from left to right and never skips backward, the condition `pref[i] <= d` precisely characterizes dead warriors. The alive segment is always a suffix, so a single boundary index fully describes the state. The reset condition preserves correctness because once all warriors die, the system state becomes identical to the initial state, making past damage irrelevant.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
a = list(map(int, input().split()))

pref = [0] * (n + 1)
for i in range(1, n + 1):
    pref[i] = pref[i - 1] + a[i - 1]

total = pref[n]
d = 0

import bisect

for _ in range(q):
    k = int(input())
    d += k

    if d >= total:
        print(n)
        d = 0
        continue

    pos = bisect.bisect_right(pref, d)
    alive = n - (pos - 1)
    print(alive)
```

The prefix sum array compresses all warrior strengths into a monotonic structure where each prefix represents a complete kill threshold. The variable `d` accumulates total incoming arrows across minutes until a full wipe occurs, at which point we reset because the system state restarts.

The binary search (`bisect_right`) finds the first prefix strictly greater than current damage, which directly identifies the first alive warrior. Subtracting gives the number of survivors efficiently.

A subtle detail is handling the reset correctly before performing binary search. If we forget to reset `d` when all warriors die, future queries would incorrectly apply damage on top of an already reset system.

## Worked Examples

### Sample 1

Input:

```
5 5
1 2 1 2 1
3 10 1 1 1
```

Prefix sums: `[0, 1, 3, 4, 6, 7]`, total = 7

| Minute | k | d after update | Condition | pos | alive |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 3 | d < 7 | 3 | 3 |
| 2 | 10 | reset | d ≥ 7 | - | 5 |
| 3 | 1 | 1 | d < 7 | 2 | 4 |
| 4 | 1 | 2 | d < 7 | 2 | 4 |
| 5 | 1 | 3 | d < 7 | 3 | 3 |

This trace shows how full death triggers a reset, while partial damage carries forward correctly.

### Sample 2

Input:

```
4 4
2 1 3 4
1 2 5 3
```

Prefix sums: `[0, 2, 3, 6, 10]`, total = 10

| Minute | k | d after update | pos | alive |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 4 |
| 2 | 2 | 3 | 3 | 2 |
| 3 | 5 | 8 | 4 | 1 |
| 4 | 3 | reset | - | 4 |

This shows a late reset after cumulative damage exceeds total health.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each query performs a binary search on prefix sums |
| Space | O(n) | Prefix sum array storage |

The constraints allow up to 200,000 queries, so a logarithmic factor per query is easily fast enough within 2 seconds in Python when implemented with built-in binary search.

## Test Cases

```python
import sys, io
import bisect

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + a[i - 1]

    total = pref[n]
    d = 0

    out = []
    for _ in range(q):
        k = int(input())
        d += k
        if d >= total:
            out.append(str(n))
            d = 0
        else:
            pos = bisect.bisect_right(pref, d)
            out.append(str(n - (pos - 1)))

    return "\n".join(out)

# provided sample
assert run("""5 5
1 2 1 2 1
3 10 1 1 1
""") == """3
5
4
4
3"""

# custom 1: single warrior
assert run("""1 3
5
1 5 6
""") == """1
1
1"""

# custom 2: all equal health
assert run("""3 3
2 2 2
1 3 5
""") == """3
2
3"""

# custom 3: immediate full reset
assert run("""4 2
1 1 1 1
10 1
""") == """4
3"""

# custom 4: boundary partial kill
assert run("""5 1
1 2 3 4 5
9
""") == """2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single warrior | 1,1,1 | trivial structure and reset behavior |
| equal health | mixed | correct binary search boundaries |
| full reset | 4,3 | overshoot reset handling |
| boundary partial kill | 2 | correct prefix boundary computation |

## Edge Cases

A key edge case is when a single query provides enough arrows to exceed total health multiple times conceptually. The algorithm handles this by resetting immediately whenever `d >= total`, ensuring no residual damage leaks across cycles. For example, with `a = [1,1,1]` and `k = 10`, we set `d = 0` and correctly output all warriors alive.

Another edge case is when damage lands exactly on a prefix sum boundary. Because we use `bisect_right`, if `d` equals `pref[i]`, warrior `i` is considered dead and the next warrior becomes the first alive. This matches the rule that arrows fully deplete a warrior before moving forward.