---
title: "CF 463B - Caisa and Pylons"
description: "We are given a sequence of pylons arranged in a line, starting from position 0 up to position n. The first pylon is fixed at height 0, and every other pylon has a given height."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 463
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 264 (Div. 2)"
rating: 1100
weight: 463
solve_time_s: 59
verified: true
draft: false
---

[CF 463B - Caisa and Pylons](https://codeforces.com/problemset/problem/463/B)

**Rating:** 1100  
**Tags:** brute force, implementation, math  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of pylons arranged in a line, starting from position 0 up to position n. The first pylon is fixed at height 0, and every other pylon has a given height. A player starts at pylon 0 with zero energy and moves strictly forward, one step at a time, from pylon k to pylon k+1.

Each move changes the energy by the difference between the current height and the next height. If the next pylon is lower, energy increases, and if it is higher, energy decreases. The key constraint is that energy is never allowed to drop below zero at any point during the journey.

We are allowed to increase the height of any pylon by spending one dollar per unit increase, and we want to minimize the total dollars spent so that the journey from 0 to n becomes feasible.

The constraint n ≤ 100000 immediately rules out any approach that tries all possible height modifications or simulates expensive search over configurations. Any solution must be linear or close to linear in n. Even O(n log n) is acceptable, but anything quadratic is not.

A naive approach might try to simulate the journey and whenever energy becomes negative, increase some previous or current height greedily without a clear strategy. This fails because early adjustments affect later transitions in non-local ways.

A subtle failure case appears when local fixes are shortsighted. For example, if heights are:

```
n = 3
h = [5, 1, 5]
```

A greedy simulation might fix the drop from 5 to 1, but later still fail at 1 to 5, leading to redundant or misplaced upgrades. The correct solution must reason globally about the worst deficit encountered along the path, not react step by step.

## Approaches

The brute-force idea is to simulate the journey and, whenever energy would become negative, try increasing some pylon height to compensate. One could attempt all choices of where to spend money at each failure point. This quickly becomes combinatorial: each correction changes future differences, and in the worst case we might reconsider earlier decisions repeatedly. With n up to 100000, even a few thousand branching corrections is enough to explode beyond limits.

The key insight is to stop thinking in terms of energy evolution and instead rewrite what actually matters. Each move contributes a difference h[k] - h[k+1]. Summing these over time gives a cumulative energy that depends only on prefix behavior. The only time energy becomes problematic is when a prefix sum of these differences drops below zero.

Rearranging the expression shows that the only dangerous moments are when a height h[i] is larger than anything we can afford from accumulated energy. Instead of tracking energy explicitly, we can maintain how much "free budget" we have and ensure it never goes negative. The only time we need to pay money is when a decrease cannot cover a previous increase.

A simpler interpretation emerges: whenever we encounter a height that is larger than all previous effective heights, we must "pay" to lift our baseline so that we can reach it without negative energy. This reduces the problem to tracking a running maximum of heights and accumulating deficits relative to the starting level.

The optimal solution is therefore linear: we scan from left to right, maintaining the highest height seen so far, and whenever the next height is greater than our current effective capacity, we pay exactly the difference.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We reinterpret the journey as maintaining a baseline height that guarantees non-negative energy.

1. Start with a baseline equal to 0, since we begin at pylon 0 with height 0 and zero energy. We also initialize the answer as 0, representing total money spent.
2. Iterate through pylons from 1 to n. At each step, compare the current height with the baseline requirement.
3. If the current height is greater than the baseline, we must increase our baseline to match it. The difference represents exactly how many dollars we must spend at this point, because without raising earlier pylons effectively, the energy would become negative when stepping into this higher pylon.
4. Add this difference to the answer. This models spending money to increase a suitable pylon so that the transition remains feasible.
5. Update the baseline to be the maximum of its current value and the current height.
6. Continue until the last pylon is processed. The accumulated cost is the minimum required spending.

### Why it works

The crucial invariant is that after processing pylon i, the baseline equals the maximum height seen so far. This guarantees that all previously processed transitions are safe, meaning no prefix of moves has negative energy. Whenever a new height exceeds this maximum, the only way to avoid a negative energy drop at that step is to have already compensated for it by raising some earlier pylon. Since each unit increase costs exactly one dollar regardless of where it is applied, increasing the baseline incrementally at the moment we encounter a new maximum is optimal and never overpays. Any delayed correction would still need to match the same height gap, so this greedy accumulation is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    h = list(map(int, input().split()))

    current_max = 0
    cost = 0

    for x in h:
        if x > current_max:
            cost += x - current_max
            current_max = x

    print(cost)

if __name__ == "__main__":
    solve()
```

The implementation keeps a running maximum height seen so far. Whenever a new height exceeds it, we add the difference to the cost. This directly encodes the idea that we must "lift" earlier terrain to meet the new peak.

A common mistake is trying to simulate energy directly using prefix differences. That approach complicates the problem and introduces unnecessary state. The greedy maximum-tracking approach avoids explicit energy tracking entirely.

Another subtle point is that we never adjust anything explicitly in an array. The reasoning relies on equivalence: increasing an earlier pylon or conceptually increasing the baseline produces the same effect on all future differences.

## Worked Examples

### Example 1

Input:

```
5
3 4 3 2 4
```

We track current_max and cost.

| i | height | current_max before | action | cost | current_max after |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 | +3 | 3 | 3 |
| 2 | 4 | 3 | +1 | 4 | 4 |
| 3 | 3 | 4 | none | 4 | 4 |
| 4 | 2 | 4 | none | 4 | 4 |
| 5 | 4 | 4 | none | 4 | 4 |

This trace shows that only new peaks require spending. Every time we see a value higher than all previous ones, we pay exactly the gap.

### Example 2

Input:

```
4
1 2 2 5
```

| i | height | current_max before | action | cost | current_max after |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | +1 | 1 | 1 |
| 2 | 2 | 1 | +1 | 2 | 2 |
| 3 | 2 | 2 | none | 2 | 2 |
| 4 | 5 | 2 | +3 | 5 | 5 |

This confirms that repeated values do not trigger spending, while only strict increases matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over all pylons, constant work per element |
| Space | O(1) | Only a few variables used regardless of input size |

The solution fits comfortably within limits since n is up to 100000 and the algorithm performs only simple comparisons and additions per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    h = list(map(int, input().split()))

    current_max = 0
    cost = 0

    for x in h:
        if x > current_max:
            cost += x - current_max
            current_max = x

    return str(cost)

# provided sample
assert run("5\n3 4 3 2 4\n") == "4"

# minimum input
assert run("1\n1\n") == "1"

# already decreasing sequence
assert run("4\n5 4 3 2\n") == "5"

# strictly increasing
assert run("4\n1 2 3 4\n") == "4"

# all equal
assert run("5\n2 2 2 2 2\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimal case handling |
| 5 4 3 2 | 5 | decreasing sequence |
| 1 2 3 4 | 4 | increasing sequence accumulation |
| 2 2 2 2 2 | 2 | no repeated spending |

## Edge Cases

A minimal case like `n = 1, h = [1]` demonstrates that we must still spend when the first pylon exceeds zero. The algorithm correctly adds `1 - 0 = 1` immediately.

A strictly decreasing sequence such as `5 4 3 2` never triggers additional spending after the first step. The first value sets the required baseline, and everything afterward is safely below it. The algorithm processes this by updating `current_max` to 5 at the first step and never changing it again, yielding total cost 5.

A strictly increasing sequence such as `1 2 3 4` forces spending at every step because each new height exceeds the previous maximum. The algorithm adds differences cumulatively: 1, then 1, then 1, then 1, matching the intuitive need to continuously raise the baseline.
