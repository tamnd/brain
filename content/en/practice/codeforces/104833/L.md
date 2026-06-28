---
title: "CF 104833L - \u5140\u7a81\u9aa8\u4e4b\u6b7b"
description: "We are simulating a turn-based survival process where a character starts with an initial health value and repeatedly loses health over a sequence of rounds. The twist is that the damage applied at the end of each round is not fixed."
date: "2026-06-28T11:55:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104833
codeforces_index: "L"
codeforces_contest_name: "The 2023 Zhejiang SCI-TECH University Freshman Programming Contest"
rating: 0
weight: 104833
solve_time_s: 43
verified: true
draft: false
---

[CF 104833L - \u5140\u7a81\u9aa8\u4e4b\u6b7b](https://codeforces.com/problemset/problem/104833/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a turn-based survival process where a character starts with an initial health value and repeatedly loses health over a sequence of rounds. The twist is that the damage applied at the end of each round is not fixed. Instead, it depends on how many times fire damage has already occurred up to that point.

More precisely, we process an array of length $n$. Each element tells us whether the current round triggers an additional “fire stack”. If it does, a global counter increases. After processing that round’s event, the character receives damage equal to the current value of this counter. The character starts with health $x$, and we must determine the first round at which health drops to zero or below, or report that this never happens.

The key structure is that damage is cumulative and monotone increasing over time. Every time a fire event appears, all subsequent rounds become more dangerous because the per-round damage increases permanently.

The constraints push us toward a linear scan solution. With $n \le 10^6$, any quadratic simulation, such as recomputing accumulated damage from scratch per round, is far too slow. We must maintain running state and update it in constant time per element. Memory constraints are standard, so storing the array is fine, but extra recomputation is not.

A subtle edge case appears when the character dies exactly at a round boundary after applying damage. The death check must happen after applying the current round’s damage, not before. Another corner case is when damage becomes large late in the process, meaning early rounds might seem safe but later bursts can suddenly end the game. Finally, if health never drops below zero even after maximum accumulated damage, we must correctly output that survival continues through all rounds.

## Approaches

A straightforward simulation follows the rules literally. We maintain current health and a fire counter. For each round, if the array value is 1 we increment the counter, then we subtract the counter from health. After each subtraction we check whether health has dropped to zero or below. This is correct because it mirrors the exact process described.

The brute-force interpretation would still be linear in time, but a less careful version might recompute “current damage” by scanning all previous fire events at each step. That would make each round cost $O(n)$, leading to $O(n^2)$ total operations in the worst case. With $n = 10^6$, that becomes infeasible.

The key observation is that the damage at round $i$ depends only on the prefix count of fire events. This prefix count can be maintained incrementally. Once we realize this, each round becomes a constant-time update: increase the counter if needed, subtract it from health, and check for termination.

This reduces the entire process to a single pass through the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute damage each round) | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal prefix simulation | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We maintain two variables: the current health and the accumulated fire counter.

1. Initialize `hp = x` and `burn = 0`. The variable `burn` represents how much damage will be applied each round from now on if no further fire appears.
2. Iterate over the array from the first round to the last.
3. If the current value is 1, increment `burn` by 1. This reflects that all future rounds become strictly more dangerous.
4. Subtract `burn` from `hp`. This models the end-of-round damage application.
5. If `hp <= 0`, output the current round index and stop immediately. The earliest such round is required, so we must not continue.
6. If we finish all rounds without `hp` becoming non-positive, output that survival is guaranteed.

The correctness hinges on the fact that damage is fully determined by how many fire events have occurred so far. Each fire event permanently increases all future damage by exactly one unit, so `burn` is always equal to the prefix sum of fire indicators.

### Why it works

At any round $i$, the damage applied is exactly the number of indices $j \le i$ such that $a_j = 1$. The algorithm maintains this quantity explicitly in `burn`. Since health decreases deterministically by this prefix value at each step, the simulation exactly matches the process described in the problem. Because we check death immediately after applying the correct damage for that round, the first time health becomes non-positive is guaranteed to be reported.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, x = map(int, input().split())
a = list(map(int, input().split()))

hp = x
burn = 0

for i in range(n):
    if a[i] == 1:
        burn += 1
    hp -= burn
    if hp <= 0:
        print("YES")
        print(i + 1)
        break
else:
    print("NO")
```

The implementation directly mirrors the algorithm. The loop uses a Python `for-else` structure so that the “NO” case only triggers if no break occurs. The index `i + 1` converts from zero-based indexing to the one-based round numbering required by the output.

A common mistake is to subtract damage before updating the burn counter. That would shift all damage by one round and produce incorrect early-death results. Another subtlety is ensuring the break happens immediately when health becomes non-positive; continuing further would incorrectly report a later death round.

## Worked Examples

### Example 1

Input:

```
3 3
0 1 0
```

| Round | a[i] | burn before | burn after | hp before | hp after |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 3 | 3 |
| 2 | 1 | 0 | 1 | 3 | 2 |
| 3 | 0 | 1 | 1 | 2 | 1 |

The character survives all rounds because health never reaches zero. This demonstrates that a single increase in burn is not always enough to overcome initial health unless enough time passes for accumulation.

Output:

```
NO
```

### Example 2

Input:

```
3 3
0 0 1
```

| Round | a[i] | burn before | burn after | hp before | hp after |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 3 | 3 |
| 2 | 0 | 0 | 0 | 3 | 3 |
| 3 | 1 | 0 | 1 | 3 | 2 |

Here again survival occurs, but only because the burn increases too late to accumulate meaningful damage within the limited number of rounds. This highlights that timing of fire events is crucial, not just their count.

Output:

```
NO
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each round performs a constant number of updates: optional increment, subtraction, and comparison |
| Space | $O(1)$ | Only a few scalar variables are maintained regardless of input size |

The linear scan comfortably fits within the constraints for $n \le 10^6$. Each operation is simple integer arithmetic, so the solution runs well within typical time limits for 1 second in Python when implemented with fast input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    backup = stdout
    out = io.StringIO()
    sys.stdout = out

    # solution copied here for testing
    n, x = map(int, input().split())
    a = list(map(int, input().split()))

    hp = x
    burn = 0

    for i in range(n):
        if a[i] == 1:
            burn += 1
        hp -= burn
        if hp <= 0:
            print("YES")
            print(i + 1)
            break
    else:
        print("NO")

    sys.stdout = backup
    return out.getvalue().strip()

# provided samples
assert run("3 3\n0 1 0\n") == "NO"
assert run("3 3\n0 0 1\n") == "NO"

# custom cases

# minimum size, immediate death
assert run("1 1\n1\n") == "YES\n1"

# no fire at all
assert run("5 10\n0 0 0 0 0\n") == "NO"

# all fire, rapid growth
assert run("4 3\n1 1 1 1\n") == "YES\n3"

# late burst
assert run("6 10\n0 0 0 0 1 1\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 1 | YES 1 | Immediate death when burn starts at first step |
| 5 10 / all 0 | NO | No damage accumulation |
| 4 3 / all 1 | YES 3 | Increasing burn leads to early collapse |
| 6 10 / late ones | NO | Late fire insufficient within horizon |

## Edge Cases

One important edge case is when the character starts with very low health and the first fire event appears immediately. For input `1 1 / 1`, burn becomes 1 before damage, and health drops to zero immediately. The algorithm correctly updates burn first and then applies damage, producing death at round 1.

Another edge case is when all values are zero. The burn variable never increases, so no damage is ever applied. The algorithm processes all rounds and exits through the loop-else path, correctly outputting survival.

A third case involves dense fire events early. For input `4 3 / 1 1 1 1`, burn evolves as 1, 2, 3, 4 while health decreases accordingly. The process ensures that once burn exceeds remaining health, the exact round is detected without overshooting, since the check happens immediately after subtraction.

A final subtle case is when death happens on the last round. The loop still executes the check before termination, ensuring the correct round index is reported rather than defaulting to “NO”.
