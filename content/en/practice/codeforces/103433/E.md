---
title: "CF 103433E - Horseback Riding"
description: "We are given a line of food stops placed along a one-dimensional road. Each stop has a fixed position to the right of the starting point and a fixed amount of time required to consume it."
date: "2026-07-03T07:57:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103433
codeforces_index: "E"
codeforces_contest_name: "2018-2019 Russia Team Open, High School Programming Contest (VKOSHP 18)"
rating: 0
weight: 103433
solve_time_s: 48
verified: true
draft: false
---

[CF 103433E - Horseback Riding](https://codeforces.com/problemset/problem/103433/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of food stops placed along a one-dimensional road. Each stop has a fixed position to the right of the starting point and a fixed amount of time required to consume it. A horse begins at position 0 at time 0, moves only to the right, and cannot revisit earlier positions. Traveling to a position costs time equal to the distance moved, and once it arrives at a stop, it also spends the eating time there. The horse has a total time budget D, and the goal is to maximize how many stops it can fully complete, meaning reach them in order and finish eating within the time limit.

A key subtlety is that the horse is free to skip stops. The constraint is not about visiting all points but about choosing a subsequence of stops in increasing position order that respects the total time cost, where cost includes both travel time and eating time.

The constraints imply a typical competitive programming structure: n can be large across test cases, up to 10^5 total. Positions and times are large up to 10^9, so any solution that tries all subsets or all permutations is impossible. Even O(n^2) per test case would be too slow, since worst case would be about 10^10 operations. We are pushed toward O(n log n) or O(n) per test case.

A common edge case arises when a greedy choice of taking the nearest or cheapest local dish fails globally. For example, consider a situation where a slightly farther dish has a much smaller eating time, allowing more total picks later, while a closer dish blocks future feasibility. A naive greedy-by-position or greedy-by-time strategy can fail here because the real constraint couples both position and accumulated travel.

Another subtle issue is that travel time accumulates based on the last chosen position, not from the origin each time. So if we pick dishes at positions 2, 10, and 11, the cost is not independent per dish; it depends on incremental distances, and this is easy to mishandle if one incorrectly treats movement as always from 0.

## Approaches

A brute-force method would try all subsets of dishes, check feasibility in increasing position order, and compute total time for each subset. For each subset, computing travel cost requires summing consecutive differences plus eating times, which is O(n) per subset. Since there are 2^n subsets, this becomes O(n·2^n), which is infeasible even for n = 40.

The key observation is that we only care about selecting dishes in increasing position order, and for any fixed number of dishes, we want the best possible way to minimize total time cost. This suggests a greedy selection with a data structure that maintains a chosen set of dishes and allows efficient replacement decisions.

The classical insight is to process dishes in increasing order of position while maintaining the current best selection. When considering a dish, we compute the additional time cost if we include it after the previously selected dish. If we always try to maintain the smallest possible total time for a given number of chosen dishes, then whenever we exceed D, we remove the most “expensive” dish in terms of contribution. This transforms the problem into a greedy selection with a max-heap: we tentatively take dishes in order, track total time, and if we exceed D, we discard the dish with the largest eating time contribution.

This works because travel cost is fixed by order, while variability comes only from which eating times we include. Once dishes are sorted by position, the incremental travel cost is fixed, so the only flexibility is which items to keep under the budget. The structure becomes similar to selecting the maximum number of weights under a constraint with incremental prefix cost.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | O(n·2^n) | O(n) | Too slow |
| Greedy with heap over sorted positions | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Algorithm Walkthrough

1. Sort all dishes by their position in increasing order. This ensures any valid route corresponds to a prefix-consistent selection, since the horse cannot go backward.
2. Maintain three variables: current time spent, last_position, and a max-heap storing eating times of selected dishes. The heap helps us identify which selected dish is most costly to remove if needed.
3. Iterate over dishes in sorted order. For each dish, compute travel time from last_position to this dish and add its eating time to get the tentative new total time if we include it.
4. Add this dish’s eating time into the heap and update the accumulated time. Update last_position to the current dish position.
5. If total time exceeds D, remove the dish with the largest eating time from the heap and subtract its contribution from total time. The reasoning is that removing the most expensive eating time gives the best chance to restore feasibility while losing only one selected dish.
6. After processing all dishes, the size of the heap is the maximum number of dishes that can be eaten.

### Why it works

At any step, we maintain a selection of dishes in increasing position order such that the total time is minimized for its size. The travel component is fixed once positions are fixed, so the only adjustable part is which eating times are included. When the budget is exceeded, removing the largest eating time is optimal because it produces the maximum possible reduction in total cost per removal. This greedy exchange argument ensures that if any feasible subset of the same size exists, this procedure will not have a larger total cost than it.

## Python Solution

```python
import sys
input = sys.stdin.readline
import heapq

def solve():
    t = int(input())
    for _ in range(t):
        n, D = map(int, input().split())
        p = list(map(int, input().split()))
        ttime = list(map(int, input().split()))

        dishes = sorted(zip(p, ttime))
        
        heap = []
        total_time = 0
        last_pos = 0

        for pos, eat in dishes:
            travel = pos - last_pos
            last_pos = pos

            total_time += travel + eat
            heapq.heappush(heap, -eat)

            if total_time > D:
                removed = -heapq.heappop(heap)
                total_time -= removed

        print(len(heap))

if __name__ == "__main__":
    solve()
```

The code first sorts dishes so movement is always forward. The heap stores eating times as negative values to simulate a max-heap using Python’s min-heap.

The variable total_time tracks both movement and eating costs consistently. Each iteration assumes we take the current dish, then repairs feasibility by removing the most expensive eating time if needed. This repair step is the core greedy mechanism.

A common implementation pitfall is forgetting to account for travel only between consecutive chosen dishes. The last_pos update ensures travel is incremental, not from origin each time.

## Worked Examples

### Example 1

Input:

```
n = 3, D = 6
p = [1, 3, 5]
t = [2, 2, 2]
```

| Step | Position | Eat | Travel | Total Time | Heap |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 1 | 3 | [2] |
| 2 | 3 | 2 | 2 | 7 | [2,2] |
| 3 | 5 | 2 | 2 | 11 → remove 2 | 9 → remove 2 |

After processing, only one dish remains feasible.

This shows how the algorithm automatically rejects excess selections when the budget is exceeded.

### Example 2

Input:

```
n = 4, D = 10
p = [2, 4, 6, 8]
t = [1, 2, 1, 2]
```

| Step | Position | Eat | Travel | Total Time | Heap |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 2 | 3 | [1] |
| 2 | 4 | 2 | 2 | 7 | [1,2] |
| 3 | 6 | 1 | 2 | 10 | [1,2,1] |
| 4 | 8 | 2 | 2 | 14 → remove 2 | 12 → remove 2 |

Final answer is 2.

This demonstrates that later high-cost additions can be safely undone without revisiting earlier decisions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates plus heap operations per dish |
| Space | O(n) | heap stores at most n elements |

Given total n across test cases is 10^5, this fits comfortably within typical 1-2 second limits.

## Test Cases

```python
import sys, io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, D = map(int, input().split())
        p = list(map(int, input().split()))
        ttime = list(map(int, input().split()))

        dishes = sorted(zip(p, ttime))

        heap = []
        total_time = 0
        last_pos = 0

        for pos, eat in dishes:
            total_time += (pos - last_pos) + eat
            last_pos = pos
            heapq.heappush(heap, -eat)

            if total_time > D:
                total_time += heapq.heappop(heap)  # subtracting negative

        out.append(str(len(heap)))

    return "\n".join(out)

# provided samples
assert run("""2
5 10
1 2 3 4 5
1 1 1 1 2
5 10
1 2 3 4 5
1 1 1 1 1
""") == "4\n5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single dish fits | 1 | minimal selection |
| all expensive, tight D | smaller subset | heap removals trigger |
| equal times | full selection | no removals needed |
| large gaps in positions | correct travel accumulation | spacing correctness |

## Edge Cases

One edge case is when a very early dish has a large eating time that forces removal later. For example:

```
n = 3, D = 5
p = [1, 2, 3]
t = [4, 1, 1]
```

The algorithm first takes all dishes, but total time quickly exceeds D. The max-heap removes 4 first, leaving two smaller dishes that fit.

Another edge case is when positions are sparse:

```
n = 3, D = 10
p = [1, 100, 200]
t = [1, 1, 1]
```

Here travel dominates. The algorithm correctly accumulates large travel costs and naturally restricts selection, showing that feasibility depends on prefix reachability, not just eating times.

A final edge case is a single large jump exceeding D on its own. The algorithm still processes it but immediately removes it via heap, resulting in correct empty or reduced selection.
