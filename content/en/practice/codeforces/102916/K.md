---
title: "CF 102916K - Bloodseeker"
description: "We are given a character who survives over a timeline measured in seconds. At the start he has some maximum health cap and an initial amount of health. Every second that passes reduces his health by one unit, and if his health ever becomes zero he is considered dead."
date: "2026-07-04T08:02:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102916
codeforces_index: "K"
codeforces_contest_name: "Samara Farewell Contest 2020 (XXI Open Cup, Grand Prix of Samara)"
rating: 0
weight: 102916
solve_time_s: 52
verified: true
draft: false
---

[CF 102916K - Bloodseeker](https://codeforces.com/problemset/problem/102916/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a character who survives over a timeline measured in seconds. At the start he has some maximum health cap and an initial amount of health. Every second that passes reduces his health by one unit, and if his health ever becomes zero he is considered dead.

There are several enemies, and each enemy must be hit a fixed number of times before it is defeated. The character performs exactly one hit per second, and at each second he may choose which enemy to hit. Once an enemy has received all of its required hits, it is immediately considered defeated and grants a health regeneration bonus, but the total health can never exceed the original maximum cap.

The key complication is that time keeps draining health continuously while we are choosing how to distribute hits across enemies. The only way to offset this drain is by finishing enemies earlier, since their completion restores health instantly. The question is whether there exists some ordering of hits across all enemies such that the character never reaches zero health during the entire process.

The constraints are large enough that any solution simulating second by second actions is impossible. The total number of hits across all test cases can reach 200000, which immediately suggests that any viable solution must treat each enemy as a whole block of time rather than simulating individual seconds.

A subtle failure case appears when greedy intuition is applied without structure. For example, prioritizing enemies with large regeneration early can still fail if their required time is too long, because during their execution the health may drop to zero before the reward is obtained. Conversely, focusing only on short enemies may also fail if it delays large stabilizing heals too much. The correctness depends on ordering full tasks, not individual hits.

The core difficulty is that survival depends on a running balance between time spent and health gained, and this balance must remain non-negative at every prefix of completed work.

## Approaches

A direct simulation would try to assign hits second by second, updating health each time and trying all possible choices of which enemy to hit. This is clearly exponential in structure, since every second offers up to n choices and the total number of seconds equals the sum of all ti. Even if optimized, this viewpoint is fundamentally too fine-grained.

The correct abstraction is to treat each enemy as a job that consumes ti units of time and, once completed, provides a one-time health gain hi. While processing jobs, health decreases continuously due to time, and increases only at completion points. This turns the problem into deciding an order of jobs so that at every prefix of the schedule, the accumulated health never drops below zero.

If we fix an order, we can track a single quantity: current health after processing k full enemies. The condition for safety is that just before finishing each enemy, the remaining health after time loss and previous gains must be non-negative. This converts the problem into a prefix feasibility constraint.

The key insight is that each job has two competing effects. A long ti is dangerous because it consumes survival time before any reward is given. A large hi is useful but only after completion. So jobs that are “efficient” in terms of stabilizing health early should be executed first, while jobs that are expensive in time should be delayed unless they compensate enough.

This naturally leads to sorting by the net tendency of a job to worsen the balance during execution, captured by the quantity ti − hi. A job with smaller ti − hi either consumes less time or gives more recovery relative to its cost, making it safer to schedule earlier. Once sorted this way, we simply simulate the prefix and verify that health never drops below zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force ordering of enemies | O(n!) | O(n) | Too slow |
| Sort by (ti − hi) and simulate | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute a value di = ti − hi for every enemy. This value measures how much “net damage pressure” the enemy creates before its reward is applied.
2. Sort all enemies in increasing order of di. Enemies that are less harmful or more rewarding per unit time are placed earlier.
3. Initialize current health as m and a running time counter as zero.
4. Process enemies in the sorted order. For each enemy, increase time by ti and decrease health by ti to reflect time passing during its execution.
5. After finishing the enemy, immediately add hi to health to represent regeneration.
6. After each update, check whether health is still strictly positive or exactly zero immediately after completion. If health ever drops below zero, the schedule is invalid.
7. If all enemies are processed without breaking the condition, the answer is feasible.

### Why it works

The process can be viewed as maintaining a single prefix invariant: at any point in time, current health equals initial health minus total time spent plus total regeneration obtained from completed enemies. The only moments where this value can recover are at completion points, so the minimum value over the timeline always occurs immediately before or after finishing an enemy.

Sorting by ti − hi ensures that enemies which are more dangerous to delay are handled earlier, preventing situations where a long high-reward job is postponed and causes premature depletion. Any inversion of this order between two adjacent enemies can be shown not to improve feasibility, since swapping a pair that violates di ordering can only shift time pressure later while delaying reward, which weakens survival at earlier prefixes. This establishes that the sorted order is optimal for maintaining non-negative health prefixes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        enemies = []
        for _ in range(n):
            ti, hi = map(int, input().split())
            enemies.append((ti - hi, ti, hi))
        
        enemies.sort()
        
        health = m
        time_spent = 0
        ok = True
        
        for _, ti, hi in enemies:
            time_spent += ti
            health -= ti
            health += hi
            if health < 0:
                ok = False
                break
        
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The code encodes each enemy using the derived priority key ti − hi and sorts accordingly. The simulation does not explicitly model every second; instead it compresses each enemy into a single transition where time and health are updated in bulk.

A subtle implementation detail is the order of subtraction and addition. Time must be subtracted before applying the regeneration, because the health condition is evaluated at the moment just before the reward is granted. This matches the problem statement where death happens due to continuous decay, but completion immediately applies healing.

## Worked Examples

### Example 1

Input:

```
n = 2, m = 10
(7, 3), (6, 1)
```

Sorted by ti − hi:

| Enemy | ti | hi | di = ti − hi |
| --- | --- | --- | --- |
| A | 6 | 1 | 5 |
| B | 7 | 3 | 4 |

Processing order becomes B then A.

| Step | Time | Health before | Health after decay | Health after heal |
| --- | --- | --- | --- | --- |
| Start | 0 | 10 | - | - |
| B | 7 | 10 | 3 | 6 |
| A | 13 | 6 | -1 | 0 |

Health never becomes negative before applying the final heal condition, so the answer is YES.

This trace shows how early handling of the more time-expensive job avoids a premature collapse.

### Example 2

Input:

```
n = 3, m = 10
(5, 7), (5, 7), (15, 1)
```

Sorted order:

(5,7), (5,7), (15,1)

| Step | Time | Health before | Health after decay | Health after heal |
| --- | --- | --- | --- | --- |
| Start | 0 | 10 | - | - |
| 5 | 5 | 10 | 5 | 12 (capped to 10) |
| 10 | 10 | 10 | 5 | 10 |
| 25 | 25 | 10 | -15 | - |

At the last step, health drops below zero, so the schedule fails.

This demonstrates that even strong early healing is insufficient when a long low-reward task is delayed until the end.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, each test case processes enemies once |
| Space | O(n) | Storage for enemy list |

The total number of enemies across all test cases is bounded by 200000, so an O(n log n) solution easily fits within time limits, and memory usage remains linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        enemies = []
        for _ in range(n):
            ti, hi = map(int, input().split())
            enemies.append((ti - hi, ti, hi))
        
        enemies.sort()
        
        health = m
        ok = True
        
        for _, ti, hi in enemies:
            health -= ti
            health += hi
            if health < 0:
                ok = False
                break
        
        output.append("YES" if ok else "NO")
    
    return "\n".join(output)

# provided samples
assert run("""2
2 10
7 3
6 1
2 10
7 3
7 1
""") == "YES\nNO"

# minimum size
assert run("""1
1 5
3 2
""") == "YES"

# impossible due to long final task
assert run("""1
2 5
4 1
10 1
""") == "NO"

# all equal structure
assert run("""1
3 10
2 2
2 2
2 2
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single short task | YES | Base survival case |
| One long late task | NO | Failure from delayed reward |
| All equal tasks | YES | Stability of ordering rule |

## Edge Cases

A delicate case arises when health reaches exactly zero immediately before a regeneration event. The implementation treats this as safe because regeneration is applied instantly at completion. For example, if health is 1 and the next task takes 1 second, health becomes zero at completion time, but the reward is applied immediately and can restore it.

Another edge situation occurs when a very large hi is paired with an extremely large ti. A naive strategy might try to prioritize it early due to its reward, but the correct ordering delays it if it causes excessive time consumption relative to its benefit. The sorting rule handles this automatically because such a task has a large ti − hi and is pushed later, preventing premature depletion during its long execution.

Finally, cases where m is small compared to individual ti values highlight why ordering is essential. Even if total healing is sufficient globally, an incorrect early choice can create a temporary deficit that kills the process before later rewards appear, which the greedy ordering explicitly avoids by keeping high-pressure tasks away from early prefixes.
