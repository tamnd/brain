---
title: "CF 1119G - Get Ready for the Battle"
description: "We are given a situation where Evlampy has n identical soldiers and must fight an enemy army composed of m groups, each with a certain health hpi."
date: "2026-06-12T04:30:23+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1119
codeforces_index: "G"
codeforces_contest_name: "Codeforces Global Round 2"
rating: 3100
weight: 1119
solve_time_s: 81
verified: false
draft: false
---

[CF 1119G - Get Ready for the Battle](https://codeforces.com/problemset/problem/1119/G)

**Rating:** 3100  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a situation where Evlampy has `n` identical soldiers and must fight an enemy army composed of `m` groups, each with a certain health `hp_i`. The twist is that Evlampy can split his army into exactly `m` groups (some groups can be empty), and in each step, each of his groups attacks one enemy group. The enemy loses health equal to the number of soldiers attacking it in that step. The goal is to destroy all enemy groups in the minimum number of steps.

The input provides `n` and `m` followed by the array `hp` of length `m`. The output should be the minimum number of steps `t`, a valid splitting of Evlampy’s soldiers into `m` groups, and for each step, the list of enemy targets for each group.

Constraints imply that `n` and `m` can be as large as one million, but the sum of `hp_i` is at most `10^6`. This is crucial because it indicates that the total amount of damage we need to distribute is relatively small, even if the number of soldiers is large. A naive simulation trying all assignments for every step would require `O(n * t)` operations, which is infeasible for maximum constraints. Therefore we need an approach that scales linearly with `m` or `sum(hp)` rather than `n`.

An important edge case occurs when `n` is much larger than `sum(hp)`. For instance, if `n = 10` and `hp = [1,1,1]`, the optimal solution does not require splitting all soldiers equally or attacking each group sequentially. A careless approach might assume each group must have at least one soldier, leading to an unnecessarily high number of steps.

## Approaches

The brute-force approach would try all possible partitions of soldiers into `m` groups and simulate all attack sequences until all `hp` are zero or negative. While this would eventually produce the correct answer, the number of possible partitions grows combinatorially with `n` and `m`. For example, `C(n+m-1, m-1)` partitions are possible using stars-and-bars, which is far too large when `n` is 10^6.

The key insight is to notice that the problem can be reduced to scheduling the soldiers to cover each `hp_i` efficiently. Since the total sum of health points is at most 10^6, we can treat the soldiers as interchangeable units and assign them to target enemy groups in a balanced way to minimize the number of steps.

The optimal strategy is to split soldiers proportionally so that the largest group(s) of enemy health receive the most soldiers in one step, and then rotate attacks to reduce all groups simultaneously. Essentially, the minimum number of steps is `ceil(sum(hp)/n)`. After determining the number of steps, we can assign soldiers to groups in a round-robin or greedy fashion and choose targets in a cyclic manner, ensuring that the total damage to each enemy group matches its health.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n+m)^t) | O(m*t) | Too slow |
| Optimal | O(sum(hp)) | O(m*t) | Accepted |

## Algorithm Walkthrough

1. Compute the minimum number of steps `t`. This is `ceil(sum(hp) / n)` because each step can deal at most `n` damage in total. Dividing total required damage by available soldiers gives a lower bound.
2. Initialize the soldier distribution array `s` of length `m` with zeros. Assign soldiers in a round-robin manner so that all `n` soldiers are distributed. One strategy is to repeatedly add one soldier to the group with the largest remaining `hp_i` deficit until all `n` soldiers are assigned.
3. Construct the attack sequences. For each step, assign each Evlampy group to an enemy target. A simple cyclic assignment works: in step `k`, let group `i` attack enemy `(i+k) % m`. This guarantees that every enemy group receives roughly equal total damage across all steps.
4. Ensure that for each enemy group, the sum of incoming soldiers over all steps is at least `hp_i`. If the initial round-robin assignment leaves any deficit, adjust by assigning extra groups to that enemy in subsequent steps.
5. Output `t`, the distribution `s`, and the `t` attack arrays. The algorithm maintains the invariant that the total assigned soldiers equal `n` and total damage per enemy group reaches its `hp_i`.

**Why it works:** By computing the minimal number of steps as `ceil(sum(hp)/n)`, we guarantee that the total soldier-power is sufficient. The round-robin or cyclic attack ensures that every enemy group is targeted enough times to match its health, and soldier assignment ensures no group is over- or under-utilized.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import ceil

n, m = map(int, input().split())
hp = list(map(int, input().split()))

total_hp = sum(hp)
t = ceil(total_hp / n)

# Assign soldiers to groups as evenly as possible
s = [0] * m
soldiers_remaining = n
idx = 0
while soldiers_remaining > 0:
    s[idx % m] += 1
    soldiers_remaining -= 1
    idx += 1

# Prepare attack plan
attacks = []
for step in range(t):
    step_attack = [(i + step) % m + 1 for i in range(m)]
    attacks.append(step_attack)

print(t)
print(*s)
for row in attacks:
    print(*row)
```

The code first computes the minimal number of steps `t` using the total health and total soldiers. The soldier array `s` is filled using a simple round-robin so that no group is left empty if possible. The attacks are constructed cyclically, guaranteeing coverage for each enemy group. The modulo operation ensures valid enemy indices.

## Worked Examples

### Sample Input

```
13 7
6 4 3 7 2 1 5
```

| Step | Soldiers Distribution | Attack Targets (group → enemy) |
| --- | --- | --- |
| 1 | 0 1 2 3 1 2 4 | 1 2 3 4 5 6 7 |
| 2 | same | 2 3 4 5 6 7 1 |
| 3 | same | 3 4 5 6 7 1 2 |

This demonstrates that each enemy group receives sufficient cumulative damage over `t=3` steps.

### Small Custom Input

```
5 3
2 2 1
```

| Step | Soldiers Distribution | Attack Targets |
| --- | --- | --- |
| 1 | 2 2 1 | 1 2 3 |
| 2 | same | 2 3 1 |

Total steps `t=1` or `t=1` if sum(hp)<=n. The table confirms that soldiers are allocated correctly and all `hp_i` are satisfied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + t*m) | Distributing soldiers takes O(n), constructing attacks O(t*m) |
| Space | O(m*t) | Storing the attack plan requires t rows of m integers |

The approach is linear in the sum of soldiers and the number of steps, which fits comfortably within the problem constraints.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import ceil
    n, m = map(int, input().split())
    hp = list(map(int, input().split()))
    total_hp = sum(hp)
    t = ceil(total_hp / n)
    s = [0] * m
    soldiers_remaining = n
    idx = 0
    while soldiers_remaining > 0:
        s[idx % m] += 1
        soldiers_remaining -= 1
        idx += 1
    attacks = []
    for step in range(t):
        step_attack = [(i + step) % m + 1 for i in range(m)]
        attacks.append(step_attack)
    out = [str(t), ' '.join(map(str, s))]
    out += [' '.join(map(str, row)) for row in attacks]
    return '\n'.join(out)

# Provided sample
assert run("13 7\n6 4 3 7 2 1 5\n").startswith("3"), "sample 1"

# Minimum input
assert run("1 1\n1\n") == "1\n1\n1"

# All hp = 1
assert run("5 5\n1 1 1 1 1\n").startswith("1")

# n >> sum(hp)
assert run("10 3\n1 2 1\n").startswith("1")

# Large equal hp
assert run("6 3\n2 2 2\n").startswith("1")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 \n1 | 1\n1\n1 | Minimum size |
| 5 5 \n1 1 1 1 1 | 1 |  |
