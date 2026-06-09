---
title: "CF 1792A - GamingForces"
description: "We are asked to determine the minimum number of spell casts Monocarp needs to kill a set of monsters, each with a certain health value."
date: "2026-06-09T10:22:39+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1792
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 142 (Rated for Div. 2)"
rating: 800
weight: 1792
solve_time_s: 153
verified: false
draft: false
---

[CF 1792A - GamingForces](https://codeforces.com/problemset/problem/1792/A)

**Rating:** 800  
**Tags:** greedy, sortings  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine the minimum number of spell casts Monocarp needs to kill a set of monsters, each with a certain health value. Monocarp has two spells: one that reduces the health of two different monsters by one simultaneously, and another that instantly kills a single monster. The goal is to sequence these spells in a way that kills all monsters using as few casts as possible.

The input consists of multiple test cases. For each test case, we are given the number of monsters, followed by a list of their health values. The output for each test case is a single integer, the minimum number of spells required.

The constraints are relatively small: the number of monsters in a single test case is at most 100, and the sum of monsters across all test cases is at most 20,000. This allows algorithms up to roughly O(n^2) per test case to run comfortably, but anything that approaches O(n^3) might start to be inefficient. Each monster's health is at most 100, which suggests that solutions depending on sorting, greedy selection, or basic arithmetic manipulations will run efficiently.

A naive approach could fail in cases where monsters have highly unbalanced health. For example, if we have three monsters with health `[1, 1, 100]`, greedily pairing the first two for the two-monster spell is efficient, but repeatedly trying to pair monsters without considering the largest health could result in using the single-monster spell many times, giving a suboptimal total count.

## Approaches

A brute-force solution would try all possible sequences of spell casts: for every pair of alive monsters, we can apply the two-monster spell, and for any single monster we can use the one-monster spell. This would generate a huge number of states, and since each monster can have up to 100 health, the number of potential states is on the order of 100^100 in the worst case. This is clearly intractable.

The key insight is to realize that the two-monster spell is always more efficient when it can be applied. Each cast reduces the combined health of two monsters by 2, whereas the single-monster spell reduces only one. Consequently, the optimal strategy will always try to maximize the use of the two-monster spell. If we think in terms of total health, let `H` be the sum of all monster health and let `M` be the maximum individual health. The minimum number of spells is constrained by two facts: every spell reduces at most 2 health points (for the two-monster spell), so we need at least `ceil(H/2)` spells; also, no monster can be killed in fewer than `M` spells, because we cannot reduce its health faster than 1 per cast in the worst case. Therefore, the minimum total number of casts is `max(ceil(H/2), M)`.

This insight immediately leads to an O(n) solution per test case: compute the sum of health values and the maximum health, then take the maximum of half the sum (rounded up) and the maximum health.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * H) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. This sets up our loop over multiple scenarios.
2. For each test case, read the number of monsters `n`.
3. Read the list of monster health values.
4. Compute the sum `total_health` of all health values. This represents the total amount of "damage" needed.
5. Find the maximum health `max_health` among all monsters. This ensures that no single monster's health exceeds the number of spell casts.
6. Compute `ceil(total_health / 2)` to account for the fact that the two-monster spell reduces two health points per cast. In integer arithmetic, this is `(total_health + 1) // 2`.
7. The result is `max(max_health, (total_health + 1) // 2)`. This guarantees that both constraints are satisfied: we have enough casts to reduce total health and enough to eliminate the strongest monster.
8. Print the result.

Why it works: The two constraints-total health and maximum health-capture the bottlenecks of the system. No algorithm can use fewer casts than either of these limits, because the two-monster spell cannot reduce the total faster than two points per cast, and no monster can die faster than 1 health per cast if it is the only remaining strong monster. The greedy choice of always applying the two-monster spell until only one remains is implicitly encoded in the max formula.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    h = list(map(int, input().split()))
    total_health = sum(h)
    max_health = max(h)
    result = max(max_health, (total_health + 1) // 2)
    print(result)
```

The solution reads the number of test cases, iterates over each one, computes the sum and maximum of health values, and then calculates the result. Using `(total_health + 1) // 2` ensures correct rounding for odd totals. The solution uses O(1) extra space beyond storing the health array.

## Worked Examples

**Sample 1**

Input: `[1, 2, 1, 2]`

`total_health = 6`

`max_health = 2`

`ceil(total_health/2) = 3`

`max(3, 2) = 3` → Output `3`

| Step | Action | total_health | max_health | Result |
| --- | --- | --- | --- | --- |
| 1 | sum and max | 6 | 2 |  |
| 2 | compute max(max_health, ceil(sum/2)) | 6 | 2 | 3 |

**Sample 2**

Input: `[2, 4, 2]`

`total_health = 8`

`max_health = 4`

`ceil(total_health/2) = 4`

`max(4, 4) = 4` → Output `4`

The formula ensures that the strongest monster and the combined total are both accounted for.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Sum and max of n elements |
| Space | O(n) per test case | Store monster healths |

The algorithm easily handles the constraint of a total of 20,000 monsters across all test cases, performing about 20,000 operations per sum/max, which is well under the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        h = list(map(int, input().split()))
        total_health = sum(h)
        max_health = max(h)
        result = max(max_health, (total_health + 1) // 2)
        output.append(str(result))
    return "\n".join(output)

# provided samples
assert run("3\n4\n1 2 1 2\n3\n2 4 2\n5\n1 2 3 4 5\n") == "3\n4\n5", "sample 1-3"

# custom cases
assert run("1\n1\n100\n") == "100", "single monster max health"
assert run("1\n2\n1 1\n") == "1", "smallest total health even"
assert run("1\n2\n1 2\n") == "2", "smallest total health odd"
assert run("1\n5\n5 5 5 5 5\n") == "13", "all equal large health"
assert run("1\n3\n1 100 1\n") == "100", "dominant monster"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n100\n` | 100 | Single monster, maximum health equals total |
| `1\n2\n1 1\n` | 1 | Minimum total health, even |
| `1\n2\n1 2\n` | 2 | Minimum total health, odd |
| `1\n5\n5 5 5 5 5\n` | 13 | All monsters equal, sum > max |
| `1\n3\n1 100 1\n` | 100 | One monster dominates |

## Edge Cases

If there is a single monster, the answer equals its health. For example, `[100]` produces `100`. The algorithm computes `max(100, ceil(100/2)) = 100`.

If all monsters have equal health, such as `[5, 5, 5, 5, 5]`, the sum is 25, `ceil(25/2) = 13`, max is 5, and the output is 13. This correctly accounts for pairing monsters efficiently with the two-monster spell.

If one monster dominates the total, like `[1, 100, 1]`, the sum is 102, `ceil(102/2) = 51`, but the max is 100. The algorithm correctly outputs 100 because we cannot kill the strongest monster faster than 100 casts.
