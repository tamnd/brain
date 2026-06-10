---
title: "CF 1468D - Firecrackers"
description: "A hooligan and a guard stand in a one dimensional corridor. Every second, the hooligan acts first, then already dropped firecrackers may explode, then the guard moves one step toward the hooligan. The hooligan owns several firecrackers."
date: "2026-06-11T01:25:03+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1468
codeforces_index: "D"
codeforces_contest_name: "2020-2021 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules)"
rating: 1700
weight: 1468
solve_time_s: 221
verified: false
draft: false
---

[CF 1468D - Firecrackers](https://codeforces.com/problemset/problem/1468/D)

**Rating:** 1700  
**Tags:** binary search, sortings  
**Solve time:** 3m 41s  
**Verified:** no  

## Solution
## Problem Understanding

A hooligan and a guard stand in a one dimensional corridor. Every second, the hooligan acts first, then already dropped firecrackers may explode, then the guard moves one step toward the hooligan.

The hooligan owns several firecrackers. A firecracker with value `s` explodes exactly `s` seconds after it is lit. The hooligan may only light a firecracker during a second in which he does not move.

The guard always gets closer and eventually catches the hooligan. Before that happens, the hooligan wants as many firecrackers as possible to explode.

The key observation is that the exact positions of the dropped firecrackers never matter. Only the explosion times matter. Once a firecracker is lit at time `T`, it contributes to the answer if and only if `T + s` occurs strictly before the capture process ends.

The corridor length `n` can be as large as `10^9`, so any simulation over cells is impossible. The total number of firecrackers over all test cases is at most `2 · 10^5`, which strongly suggests an `O(m log m)` solution per test case is acceptable, while anything quadratic is not.

The first subtle point is determining how long the hooligan can survive. Suppose `a < b`. The guard starts on the right. The hooligan should run left toward cell `1`, because moving toward the guard only shortens survival. If he reaches cell `1`, he can no longer move away and eventually gets caught there.

For example:

```
n=7, a=3, b=6
```

The hooligan reaches cell `1` after `2` moves. The guard then continues approaching. Capture occurs after `5` seconds.

A common mistake is to use only the initial distance `|a-b| = 3`. The hooligan actually survives longer because he can retreat toward the nearest wall.

The second subtle point is that not every second before capture can be used to light a firecracker. Some seconds are spent moving toward safety. In the example above, the hooligan must spend two seconds moving to reach cell `1`, leaving only three opportunities to light firecrackers.

Another easy mistake is handling the final second incorrectly. If a firecracker explodes at exactly the same second the guard catches the hooligan, it still counts because explosions happen before the guard's movement in the sequence of events.

Consider:

```
7 1 3 6
2
```

The hooligan can light at second `3`, the firecracker explodes at second `5`, and capture also happens during second `5`. The answer is `1`, not `0`.

## Approaches

A brute force approach would model the entire game. At every second we would decide whether to move or light a particular firecracker, keep track of all scheduled explosions, update positions, and search over possible strategies.

Such a search is hopeless. Even with only `m = 200000` firecrackers, the number of possible action sequences is enormous. The corridor itself may contain up to `10^9` cells, making direct simulation impossible.

The structure becomes much simpler once we separate movement from firecracker scheduling.

Suppose `a < b`. The guard is to the right. The best survival strategy is deterministic: keep moving left until reaching cell `1`. Any other movement can only reduce the time before capture.

Let

```
d = b - a
```

be the initial distance between the two people.

After reaching the wall, capture occurs after exactly `b - 1` seconds. Symmetrically, when `a > b`, capture occurs after `n - b` seconds.

Let this value be `limit`.

The hooligan spends some seconds moving toward the wall. The number of such forced moves is

```
move = a - 1      if a < b
move = n - a      if a > b
```

Hence the maximum number of firecrackers that can even be lit is

```
slots = limit - move - 1
```

which simplifies to

```
slots = abs(a - b) - 1
```

This is exactly the number of seconds available for dropping firecrackers.

Now suppose we want to know whether `k` firecrackers can be made to explode.

The available drop times are the latest possible ones:

```
limit - k, limit - k + 1, ..., limit - 1
```

Using late times is always better because every firecracker receives more time before its deadline.

If a firecracker with delay `s` is dropped at time `t`, it succeeds when

```
t + s <= limit
```

To maximize the number of successful firecrackers, we sort delays increasingly and try to schedule the `k` smallest delays. The largest delay among them gets the earliest slot, the second largest gets the second earliest slot, and so on.

This naturally leads to a binary search on the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(m) | Too slow |
| Optimal | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Normalize the situation so that the guard is always on the right. If `a > b`, reflect the corridor by swapping positions conceptually. The formulas become symmetric.
2. Compute the capture deadline.

If `a < b`, capture occurs after `b - 1` seconds.

If `a > b`, capture occurs after `n - b` seconds.

Call this value `limit`.
3. Compute the maximum number of available dropping moments.

The hooligan must spend some time running toward the nearest safe wall. The number of usable dropping moments is

```
slots = abs(a - b) - 1
```

No solution can use more than `slots` firecrackers.
4. Sort the firecracker delays in ascending order.

Smaller delays are always easier to schedule before the deadline.
5. Binary search the answer `k` between `0` and `min(m, slots
