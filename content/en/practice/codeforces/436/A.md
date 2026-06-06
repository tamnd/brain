---
title: "CF 436A - Feed with Candy"
description: "We have up to 2000 candies. Each candy has a type, either 0 or 1, a required jump height, and a mass. Om Nom starts with jump power x. He may eat any uneaten candy whose height is at most his current jump power. After eating a candy with mass m, his jump power increases by m."
date: "2026-06-07T03:00:51+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 436
codeforces_index: "A"
codeforces_contest_name: "Zepto Code Rush 2014"
rating: 1500
weight: 436
solve_time_s: 96
verified: true
draft: false
---

[CF 436A - Feed with Candy](https://codeforces.com/problemset/problem/436/A)

**Rating:** 1500  
**Tags:** greedy  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We have up to 2000 candies. Each candy has a type, either 0 or 1, a required jump height, and a mass.

Om Nom starts with jump power `x`. He may eat any uneaten candy whose height is at most his current jump power. After eating a candy with mass `m`, his jump power increases by `m`.

There is one additional restriction: consecutive candies must have different types. If the last candy eaten was type 0, the next one must be type 1, and vice versa.

The goal is to maximize the total number of candies eaten.

The constraints are surprisingly small. With `n ≤ 2000`, an `O(n²)` solution is completely safe, since it performs roughly four million operations. On the other hand, exponential search over all valid eating orders is impossible because the number of orders grows factorially.

The tricky part is that eating a candy changes future reachability. A choice that looks good locally may unlock many more candies later.

One easy mistake is to always take the reachable candy with the smallest height.

Example:

```
3 3
0 2 10
1 3 1
1 20 1
```

Correct output:

```
2
```

If we eat the type-0 candy first, jump power becomes 13 and we can still eat the type-1 candy. If we instead focus on height rather than gained mass, we may fail to maximize future reachability.

Another subtle case is that the optimal sequence may start with either type.

```
2 1
0 1 1
1 100 100
```

Correct output:

```
1
```

Starting from type 0 gives one candy. Starting from type 1 gives zero. Any solution that assumes a fixed starting type will fail.

A third pitfall is assuming that among reachable candies of the required type, any choice is equally good.

```
3 5
0 5 1
0 5 10
1 15 1
```

Correct output:

```
2
```

When choosing a type-0 candy first, taking mass 10 is strictly better than taking mass 1 because it immediately unlocks the type-1 candy.

## Approaches

The brute-force idea is straightforward. At every step, try every reachable candy of the required type, recurse, and take the best result. This explores all valid eating orders.

The brute-force is correct because it explicitly checks every legal sequence. Unfortunately, the number of sequences is enormous. Even for a few dozen candies it becomes infeasible, and for `n = 2000` it is completely impossible.

To obtain something faster, we need to understand what actually matters.

Suppose the next candy must have type 0. Among all reachable unused type-0 candies, imagine choosing one with mass `a` while another reachable choice has larger mass `b`.

After eating the larger-mass candy, the jump power becomes larger than after eating the smaller one. Every candy reachable after gaining `a` is also reachable after gaining `b`. The larger gain never removes possibilities.

This observation is the key greedy property. Whenever we must choose a candy of a certain type, the best choice is simply the reachable candy of that type with maximum mass.

The only remaining uncertainty is the starting type. Since there are only two types, we can simulate the greedy process twice.

In one simulation we insist that the first candy is type 0.

In the other simulation we insist that the first candy is type 1.

For each simulation:

1. Repeatedly find the unused reachable candy of the required type with maximum mass.
2. Eat it.
3. Increase jump power.
4. Switch the required type.

When no reachable candy of the required type exists, the simulation ends.

The answer is the larger result of the two simulations. This greedy strategy is the standard accepted solution for the problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal Greedy Simulation | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all candies and store their type, height, and mass.
2. Run a simulation assuming the first eaten candy must be type 0.
3. Create a `used` array marking which candies have already been eaten.
4. Set the current jump power to `x`.
5. Let `need_type` be the type that must be eaten next.
6. Scan all candies and find an unused candy whose type is `need_type`, whose height is at most the current jump power, and whose mass is maximum among all such candidates.
7. If no candidate exists, stop this simulation.

At this point no legal move is available because the next candy must have the required type.
8. Eat the chosen candy.

Increase jump power by its mass, mark it as used, increment the answer for this simulation, and flip `need_type`.
9. Repeat from step 6.
10. Perform the same procedure again, this time starting with type 1.
11. Output the larger of the two results.

### Why it works

Consider any step where the next candy must have some fixed type.

Among all reachable candies of that type, let `A` be the candy with maximum mass. Suppose another reachable candy `B` is chosen instead.

After eating `A`, the jump power becomes at least as large as after eating `B`. Every candy reachable after choosing `B` remains reachable after choosing `A`. Since the type alternation requirement depends only on candy types and not on masses, choosing `A` cannot reduce the set of future valid moves.

Replacing any smaller-mass choice by the largest reachable mass never hurts. Applying this argument at every step proves that the greedy choice is always optimal for a fixed starting type.

Since every valid sequence must start with either type 0 or type 1, checking both starting types guarantees that the global optimum is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def simulate(start_type, candies, x):
    n = len(candies)
    used = [False] * n

    cur_jump = x
    need_type = start_type
    eaten = 0

    while True:
        best_idx = -1
        best_mass = -1

        for i, (t, h, m) in enumerate(candies):
            if not used[i] and t == need_type and h <= cur_jump:
                if m > best_mass:
                    best_mass = m
                    best_idx = i

        if best_idx == -1:
            break

        used[best_idx] = True
        cur_jump += candies[best_idx][2]
        eaten += 1
        need_type ^= 1

    return eaten

def solve():
    n, x = map(int, input().split())

    candies = []
    for _ in range(n):
        t, h, m = map(int, input().split())
        candies.append((t, h, m))

    ans = max(
        simulate(0, candies, x),
        simulate(1, candies, x)
    )

    print(ans)

solve()
```

The simulation function implements the greedy process directly. The `used` array prevents reusing candies. At each step we search all candies and select the reachable candy of the required type with maximum mass.

The comparison uses mass rather than height because the proof relies on maximizing future jump power. Choosing the highest reachable candy would not preserve the greedy property.

The order of updates matters. We first mark the candy as used, then add its mass to the jump power, then switch the required type. This exactly matches the problem's sequence of events.

All values easily fit in Python integers. Even in the extreme case, total gained mass is at most `2000 × 2000 = 4,000,000`.

## Worked Examples

### Sample 1

Input:

```
5 3
0 2 4
1 3 1
0 8 3
0 20 10
1 5 5
```

Starting with type 0:

| Step | Need Type | Jump Power Before | Chosen Candy | Mass | Jump Power After |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | (0,2,4) | 4 | 7 |
| 2 | 1 | 7 | (1,5,5) | 5 | 12 |
| 3 | 0 | 12 | (0,8,3) | 3 | 15 |
| 4 | 1 | 15 | (1,3,1) | 1 | 16 |

No reachable type-0 candy remains, so the process stops with 4 candies.

Starting with type 1 yields only 3 candies, so the answer is 4.

This example shows how maximizing mass among reachable candies quickly increases the jump power and unlocks more options later.

### Custom Example

Input:

```
3 5
0 5 1
0 5 10
1 15 1
```

Starting with type 0:

| Step | Need Type | Jump Power Before | Chosen Candy | Mass | Jump Power After |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 5 | (0,5,10) | 10 | 15 |
| 2 | 1 | 15 | (1,15,1) | 1 | 16 |

Result: 2 candies.

If we had chosen the mass-1 candy first, jump power would become only 6 and the type-1 candy would remain unreachable.

This demonstrates exactly why the greedy criterion is based on mass.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Two simulations, each performs at most n iterations and scans all n candies |
| Space | O(n) | Storage for candies and used array |

With `n ≤ 2000`, `O(n²)` means roughly four million checks, which is comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    n, x = map(int, input().split())

    candies = [tuple(map(int, input().split())) for _ in range(n)]

    def simulate(start_type):
        used = [False] * n
        cur = x
        need = start_type
        ans = 0

        while True:
            best = -1
            best_mass = -1

            for i, (t, h, m) in enumerate(candies):
                if not used[i] and t == need and h <= cur and m > best_mass:
                    best_mass = m
                    best = i

            if best == -1:
                break

            used[best] = True
            cur += candies[best][2]
            ans += 1
            need ^= 1

        return ans

    print(max(simulate(0), simulate(1)))

def run(inp: str) -> str:
    global input
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old
    return out.getvalue().strip()

# provided sample
assert run(
"""5 3
0 2 4
1 3 1
0 8 3
0 20 10
1 5 5
"""
) == "4", "sample 1"

# minimum size
assert run(
"""1 1
0 1 1
"""
) == "1", "single reachable candy"

# unreachable candy
assert run(
"""1 1
0 2 1
"""
) == "0", "cannot reach"

# must choose larger mass
assert run(
"""3 5
0 5 1
0 5 10
1 15 1
"""
) == "2", "greedy by mass"

# alternating restriction
assert run(
"""4 10
0 1 1
0 1 1
1 1 1
1 1 1
"""
) == "4", "alternation handled"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single reachable candy | 1 | Minimum valid instance |
| Single unreachable candy | 0 | Reachability check |
| Two reachable candies of same type with different masses | 2 | Greedy must maximize mass |
| Two candies of each type | 4 | Alternation logic works correctly |

## Edge Cases

### Only one starting type works

Input:

```
2 1
0 1 1
1 100 100
```

Starting with type 0, Om Nom eats one candy and reaches jump power 2.

Starting with type 1, there is no reachable candy.

The algorithm explicitly simulates both starting types and returns the better result, which is 1.

### Larger mass is not optional

Input:

```
3 5
0 5 1
0 5 10
1 15 1
```

At jump power 5, both type-0 candies are reachable.

The algorithm selects mass 10, raising jump power to 15 and unlocking the type-1 candy.

Had it selected mass 1, the jump power would become only 6 and the answer would drop from 2 to 1.

### Reachable candies but wrong type

Input:

```
3 10
0 1 1
0 2 1
1 20 1
```

After eating one type-0 candy, the next required type is 1.

Even though another type-0 candy is reachable, it cannot be eaten immediately because of the alternation rule.

The simulation stops correctly when no reachable candy of the required type exists. This matches the problem statement exactly.
