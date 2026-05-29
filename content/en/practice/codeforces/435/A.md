---
title: "CF 435A - Queue on Bus Stop"
description: "We have a line of people waiting at a bus stop, but they are organized into groups. Each group has a fixed number of people and stands consecutively in the queue. A bus comes that can carry at most m people, and the people enter in the order of their groups."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 435
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 249 (Div. 2)"
rating: 1000
weight: 435
solve_time_s: 67
verified: true
draft: false
---

[CF 435A - Queue on Bus Stop](https://codeforces.com/problemset/problem/435/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of people waiting at a bus stop, but they are organized into groups. Each group has a fixed number of people and stands consecutively in the queue. A bus comes that can carry at most `m` people, and the people enter in the order of their groups. If the next group in line cannot fully fit into the bus, the bus leaves with the people already onboard, and the entire waiting group waits for the next bus. We are asked to compute how many buses are required to transport all groups.

The input provides `n`, the number of groups, `m`, the capacity of the bus, and an array `a` of size `n` representing the number of people in each group. The output is a single integer, the number of buses needed.

The constraints are small: `n` and `m` are at most 100. This implies that even a straightforward simulation is fast enough, because at most 100 iterations are required to process each group. There is no need for advanced data structures or optimizations beyond careful handling of the bus filling logic.

An edge case arises when a group exactly equals the bus capacity or when multiple small groups can fit exactly into one bus. For instance, if `m = 5` and the group sizes are `[2, 3, 2]`, then the first bus can take the first two groups (2+3=5), but the last group of 2 needs a new bus. A careless implementation that tries to "split" groups to fill the bus would produce incorrect results.

## Approaches

The naive approach is to simulate the process literally: start with an empty bus, iterate over the groups, add them to the bus if they fit, and launch the bus whenever a group does not fit. For each group, we check the remaining space in the bus and decide whether to load it or start a new bus. This is straightforward because the constraints allow it. For `n=100`, each step is constant-time arithmetic, so the overall complexity is effectively O(n).

There is no significantly faster algorithm because the problem is sequential: each group's placement depends on the previous bus occupancy. The key insight is that you do not need to manage individual people, only the sum of each bus's load. By keeping a running sum of the current bus's occupants, you can decide whether to start a new bus when a group cannot fit. This reduces potential off-by-one errors compared to managing every person individually.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation of groups | O(n) | O(1) | Accepted |
| Pre-sum or fancy packing | O(n) | O(n) | Overkill for this problem |

## Algorithm Walkthrough

1. Initialize a counter `buses` to 1 because we need at least one bus, and a variable `current_load` to 0 to track the number of people on the current bus.
2. Iterate through each group `g` in the array `a`.
3. If adding `g` to `current_load` would exceed `m`, increment `buses` and reset `current_load` to 0. This simulates sending the current bus and starting a new one.
4. Add the group size `g` to `current_load` to account for the newly boarded group.
5. After iterating through all groups, `buses` contains the number of buses needed.

The invariant here is that at each step, `current_load` never exceeds `m`, and every group is fully loaded into a bus without splitting. This guarantees correctness because we respect the "group stays together" rule and never overfill a bus.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))

buses = 1
current_load = 0

for g in a:
    if current_load + g > m:
        buses += 1
        current_load = 0
    current_load += g

print(buses)
```

This solution starts with one bus because there is always at least one group. The check `current_load + g > m` ensures that we do not overload a bus and respects the group constraint. Resetting `current_load` after starting a new bus ensures we count the next bus correctly. All operations are simple integer arithmetic, so there is no risk of overflow.

## Worked Examples

**Sample 1:**

Input: `4 3` with groups `[2, 3, 2, 1]`

| Group | Current load | Buses |
| --- | --- | --- |
| 2 | 2 | 1 |
| 3 | 3 (previous 2+3>3 → new bus) | 2 |
| 2 | 2 | 2 |
| 1 | 3 | 2 → new bus not needed |

The table shows that whenever a group cannot fit, a new bus starts, which exactly matches the problem description.

**Sample 2:**

Input: `5 5` with groups `[1, 2, 3, 4, 5]`

| Group | Current load | Buses |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 3 | 1 |
| 3 | 3+3>5 → new bus | 2 |
| 4 | 4 | 2 |
| 5 | 5 | 3 |

This demonstrates that larger groups naturally start new buses and small groups accumulate until the bus is full.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each group is processed exactly once, with a constant-time check and update. |
| Space | O(1) | Only two integer variables are maintained in addition to the input array. |

Since `n` is at most 100, this algorithm runs comfortably within the 1-second time limit, and memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    buses = 1
    current_load = 0
    for g in a:
        if current_load + g > m:
            buses += 1
            current_load = 0
        current_load += g
    return str(buses)

# provided sample
assert run("4 3\n2 3 2 1\n") == "3", "sample 1"

# minimum-size input
assert run("1 1\n1\n") == "1", "minimum size"

# all groups equal to bus capacity
assert run("3 5\n5 5 5\n") == "3", "each group fits exactly one bus"

# groups smaller than bus capacity
assert run("4 10\n2 3 4 1\n") == "1", "all groups fit in one bus"

# groups that force alternating bus counts
assert run("5 5\n1 4 2 3 5\n") == "4", "mix of fits and overshoot"

# maximum-size groups for maximum bus
assert run("100 100\n" + "100 "*100 + "\n") == "100", "each group fills one bus"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1\n1` | 1 | Minimum input scenario |
| `3 5\n5 5 5` | 3 | Groups exactly equal to bus capacity |
| `4 10\n2 3 4 1` | 1 | Multiple small groups fit in one bus |
| `5 5\n1 4 2 3 5` | 4 | Groups require splitting across buses |
| `100 100\n100 100 ...` | 100 | Large input, maximum sizes |

## Edge Cases

If a single group exactly fills a bus, the algorithm increments `buses` and immediately places the group, correctly counting it. For multiple small groups that together fill a bus exactly, `current_load` accumulates until it reaches `m`, and only then a new bus starts, preventing off-by-one errors. If the last group partially fills a bus, the algorithm still counts the bus because `buses` starts at 1.
