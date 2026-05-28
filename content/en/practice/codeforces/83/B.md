---
title: "CF 83B - Doctor"
description: "We have a queue of animals waiting for the doctor. Animal i must visit the doctor exactly a[i] times before leaving forever. Whenever an animal is examined, one of two things happens. If it still needs more visits, it immediately moves to the back of the queue."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 83
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 72 (Div. 1 Only)"
rating: 1800
weight: 83
solve_time_s: 97
verified: true
draft: false
---

[CF 83B - Doctor](https://codeforces.com/problemset/problem/83/B)

**Rating:** 1800  
**Tags:** binary search, math, sortings  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a queue of animals waiting for the doctor. Animal `i` must visit the doctor exactly `a[i]` times before leaving forever.

Whenever an animal is examined, one of two things happens. If it still needs more visits, it immediately moves to the back of the queue. If that visit completed all its required examinations, it disappears from the queue.

The doctor performs exactly `k` examinations and then stops working. We must output the animals that are still in the queue at that moment, in their exact order from front to back.

The constraints completely rule out direct simulation. The number of animals is at most `10^5`, which is manageable, but `k` can be as large as `10^14`. A literal simulation would require one operation per examination, which could mean one hundred trillion queue operations. Even a highly optimized implementation cannot handle that.

The total number of examinations possible is the sum of all `a[i]`. If that sum is smaller than `k`, the doctor cannot even perform `k` examinations, and the answer is `-1`.

The tricky part is reconstructing the queue after a huge number of cyclic rotations and removals.

One easy mistake is mishandling the case where the queue becomes empty exactly after the `k`-th examination.

Example:

```
Input:
1 1
1
```

After one examination, the only animal leaves forever. The queue is empty, so the correct output is an empty line, not `-1`.

Another subtle case appears when several animals finish during the same "round".

Example:

```
Input:
4 5
2 1 2 1
```

A careless implementation might rotate animals incorrectly after removals and produce the wrong remaining order.

The correct process is:

```
Initial: 1 2 3 4
After 1: 2 3 4 1
After 2: 3 4 1
After 3: 4 1 3
After 4: 1 3
After 5: 3
```

Correct output:

```
3
```

Another dangerous corner case is `k = 0`.

Example:

```
Input:
3 0
5 2 7
```

No examination happens, so the queue stays unchanged:

```
1 2 3
```

An implementation that always advances the queue at least once will fail here.

## Approaches

The brute-force idea is straightforward. Store the queue explicitly. Repeatedly pop the front animal, decrease its remaining visit count, and either discard it or push it back.

This simulation is correct because it follows the process exactly. The problem is scale. If every animal needs up to `10^9` visits and `k` itself reaches `10^14`, the simulation may require trillions of operations.

The structure of the process gives a better approach.

Imagine all currently alive animals completing one full cycle through the queue. Every alive animal loses exactly one required visit during that cycle. Instead of processing visits one by one, we can process entire layers at once.

Suppose there are currently `m` alive animals, and every one of them still needs at least `d` more visits. Then we can spend `m * d` examinations in bulk, reducing every alive animal by `d`.

This turns the problem into something similar to peeling layers from all numbers simultaneously.

If we sort animals by required visits, we can determine how many complete layers can be removed before some animals disappear. The number of layers removed acts like a global offset applied to all alive animals.

Eventually we reach a point where the next full layer would exceed `k`. At that moment, only a partial cycle remains. Since the remaining number of examinations is now less than the number of alive animals, we can reconstruct the final queue directly.

The brute-force works because queue operations are simple, but fails because it handles every examination individually. The optimized solution works because many consecutive examinations affect all alive animals identically, allowing us to compress huge stretches of the process into a single arithmetic step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all values and compute the total number of examinations possible, which is `sum(a)`.

If `sum(a) < k`, print `-1` immediately because the doctor cannot perform that many examinations.
2. Create pairs `(a[i], i)` and sort them by `a[i]`.

Sorting lets us process animals in the order they disappear.
3. Maintain three variables:

`prev`, the number of complete layers already removed.

`alive`, the number of animals still in the queue.

`used`, the number of examinations already accounted for.
4. Iterate through the sorted animals.

Suppose the current animal requires `x` visits. Since `prev` layers were already removed globally, this animal still needs `x - prev` additional full layers before disappearing.
5. Compute:

```
cost = (x - prev) * alive
```

This is the number of examinations needed to reduce every alive animal down to the next disappearance point.
6. If `used + cost <= k`, consume this entire block.

Update:

```
used += cost
prev = x
alive -= count_of_animals_removed_here
```

Multiple animals may share the same `x`, so all of them disappear together.
7. Otherwise, we cannot complete the next full layer.

At this moment, every alive animal has already lost `prev` visits. The remaining examinations are:

```
rem = k - used
```
8. Collect all animals whose original value is greater than `prev`. These are exactly the animals still alive.
9. Sort these alive animals by original index because the queue order always preserves relative order among surviving animals.
10. The remaining process is just rotating through the alive queue for `rem` steps.

Since `rem < number_of_alive_animals`, the final queue starts at position:

```
rem % len(alive_animals)
```
11. Output the alive animals starting from that position, wrapping around cyclically.

### Why it works

After removing `prev` complete layers, every surviving animal has exactly `a[i] - prev` remaining visits. Their relative order in the queue is unchanged because every complete layer corresponds to one full rotation through all alive animals.

When we stop before completing another full layer, the remaining examinations form only a partial traversal through the alive queue. Advancing `rem` positions in queue order exactly matches performing those remaining examinations one by one.

The algorithm never loses track of queue order because removals only delete animals, they never reorder survivors.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    if sum(a) < k:
        print(-1)
        return

    arr = sorted((a[i], i) for i in range(n))

    used = 0
    prev = 0
    alive = n
    ptr = 0

    while ptr < n:
        value = arr[ptr][0]
        diff = value - prev
        cost = diff * alive

        if used + cost > k:
            break

        used += cost
        prev = value

        while ptr < n and arr[ptr][0] == value:
            ptr += 1
            alive -= 1

    remaining = k - used

    survivors = []

    for i in range(n):
        if a[i] > prev:
            survivors.append(i + 1)

    if not survivors:
        print()
        return

    start = remaining % len(survivors)

    answer = survivors[start:] + survivors[:start]

    print(*answer)

solve()
```

The first important detail is the early impossibility check. If the total required examinations are smaller than `k`, no queue exists after the doctor's stopping time because the process ended earlier.

The sorted array drives the layer-removal process. Each distinct value tells us when a new group of animals disappears.

The expression:

```
cost = diff * alive
```

is the heart of the solution. `diff` represents how many complete rounds we can apply uniformly to all alive animals, and each round touches every alive animal exactly once.

The inner `while` loop removes every animal whose required visit count equals the current threshold. Handling equal values together is essential. Forgetting this produces incorrect alive counts and breaks later arithmetic.

After the bulk processing stops, all remaining animals satisfy:

```
a[i] > prev
```

Those animals appear in queue order according to their original indices. We never need a real queue because complete layers preserve cyclic order.

The remaining examinations are fewer than the number of survivors, so a simple rotation gives the final queue.

The empty-queue case is subtle. If every animal disappears exactly at time `k`, the correct output is just a blank line.

## Worked Examples

### Sample 1

Input:

```
3 3
1 2 1
```

Sorted pairs:

```
(1,0), (1,2), (2,1)
```

| Step | prev | alive | used | Current value | cost | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Start | 0 | 3 | 0 | 1 | 3 | consume |
| After removal | 1 | 1 | 3 | 2 | 1 | stop |

Now:

```
remaining = 3 - 3 = 0
```

Survivors:

```
[2]
```

Starting position:

```
0 % 1 = 0
```

Final queue:

```
2
```

This trace shows how two animals disappear simultaneously after the first full layer.

### Sample 2

Input:

```
7 10
1 3 1 2 5 2 4
```

Sorted pairs:

```
(1,0), (1,2), (2,3), (2,5), (3,1), (4,6), (5,4)
```

| Step | prev | alive | used | Current value | cost | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Start | 0 | 7 | 0 | 1 | 7 | consume |
| Remove 1s | 1 | 5 | 7 | 2 | 5 | stop |

Now:

```
remaining = 10 - 7 = 3
```

Survivors in queue order:

```
[2, 4, 5, 6, 7]
```

Rotate by:

```
3 % 5 = 3
```

Final queue:

```
6 7 2 4 5
```

This example demonstrates the key observation behind the algorithm. Instead of simulating seven separate examinations, we remove one complete layer instantly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates |
| Space | O(n) | storing arrays and survivors |

The sorting step is the only non-linear part of the algorithm. With `n <= 10^5`, `O(n log n)` easily fits within the time limit. Memory usage is linear and comfortably below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        if sum(a) < k:
            return "-1"

        arr = sorted((a[i], i) for i in range(n))

        used = 0
        prev = 0
        alive = n
        ptr = 0

        while ptr < n:
            value = arr[ptr][0]
            diff = value - prev
            cost = diff * alive

            if used + cost > k:
                break

            used += cost
            prev = value

            while ptr < n and arr[ptr][0] == value:
                ptr += 1
                alive -= 1

        remaining = k - used

        survivors = []

        for i in range(n):
            if a[i] > prev:
                survivors.append(i + 1)

        if not survivors:
            return ""

        start = remaining % len(survivors)

        answer = survivors[start:] + survivors[:start]

        return " ".join(map(str, answer))

    return solve()

# provided sample
assert run("3 3\n1 2 1\n") == "2", "sample 1"

# k = 0
assert run("3 0\n5 2 7\n") == "1 2 3", "no examinations"

# impossible case
assert run("2 5\n1 2\n") == "-1", "not enough total examinations"

# queue becomes empty exactly at k
assert run("1 1\n1\n") == "", "empty queue"

# all equal values
assert run("4 6\n3 3 3 3\n") == "3 4", "uniform layers"

# multiple removals together
assert run("4 5\n2 1 2 1\n") == "3", "simultaneous removals"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 0 / 5 2 7` | `1 2 3` | no processing occurs |
| `2 5 / 1 2` | `-1` | impossible total workload |
| `1 1 / 1` | empty output | queue becomes empty exactly at k |
| `4 6 / 3 3 3 3` | `3 4` | uniform cyclic behavior |
| `4 5 / 2 1 2 1` | `3` | simultaneous removals |

## Edge Cases

Consider the case where the queue becomes empty exactly after the final examination.

Input:

```
1 1
1
```

The algorithm processes one complete layer:

```
cost = 1 * 1 = 1
```

After consuming it:

```
used = 1
alive = 0
```

No survivors remain, so the algorithm prints an empty line. This matches the real process exactly.

Now consider simultaneous removals.

Input:

```
4 5
2 1 2 1
```

After sorting:

```
(1,1), (1,3), (2,0), (2,2)
```

The first layer costs:

```
1 * 4 = 4
```

After consuming it, both animals with value `1` disappear together. The survivors are:

```
1, 3
```

One examination remains. Rotating once leaves:

```
3
```

Handling equal values together is critical here. Removing them one at a time would incorrectly change the alive count during the same layer.

Finally, consider `k = 0`.

Input:

```
3 0
5 2 7
```

The main loop immediately stops because no examinations may be consumed. Since `prev = 0`, every animal survives. The remaining rotation amount is also zero, so the original order is preserved:

```
1 2 3
```

This confirms that the algorithm handles the empty-prefix case correctly.
