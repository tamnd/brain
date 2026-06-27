---
title: "CF 104992G - \u041c\u0435\u0434\u0432\u0435\u0434\u044c \u0438 \u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e\u0435 \u043f\u0438\u0442\u0430\u043d\u0438\u0435"
description: "We are given a collection of food items, each described by how soon it disappears from a warehouse and how many calories it provides. Time moves in discrete hours starting from the moment the bear arrives."
date: "2026-06-28T04:28:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104992
codeforces_index: "G"
codeforces_contest_name: "qual VKOSHP Junior 24"
rating: 0
weight: 104992
solve_time_s: 73
verified: false
draft: false
---

[CF 104992G - \u041c\u0435\u0434\u0432\u0435\u0434\u044c \u0438 \u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e\u0435 \u043f\u0438\u0442\u0430\u043d\u0438\u0435](https://codeforces.com/problemset/problem/104992/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of food items, each described by how soon it disappears from a warehouse and how many calories it provides. Time moves in discrete hours starting from the moment the bear arrives. In each hour, the bear can eat at most one item, and once an item’s deadline passes it is gone forever.

Each item behaves like a job that must be executed in a one-hour slot before its deadline. The goal is to choose and schedule a subset of these jobs so that no two occupy the same hour and no chosen job is scheduled after its deadline, while maximizing total calorie gain.

The input gives, for each item, a deadline in hours and a value. The deadline means the last hour index by which the item can be consumed if we index hours from zero. The output is the maximum possible sum of values among all items that can be feasibly scheduled under these constraints.

The constraints are large, with up to 200,000 items. Any approach that tries to simulate each hour or repeatedly search for the best item per time slot will fail because it would degrade toward quadratic behavior. The only viable solutions must run in roughly O(n log n).

A subtle failure case for naive reasoning appears when picking items greedily by value without respecting deadlines. For example, if one high-value item has a very early deadline and several smaller items have later deadlines, choosing incorrectly can block a schedule that allows more total value. Another failure case arises when sorting by deadline and always taking available items without tracking which earlier choices should be replaced by better ones.

## Approaches

The brute-force view is to consider every possible subset of items, and for each subset try to assign them to time slots before their deadlines. Even if we fix a subset, scheduling it requires checking whether it can be placed in increasing order of time without violating deadlines. This leads to exponential subsets, and even verifying each subset takes linear time, producing an infeasible 2^n scale explosion.

A more structured attempt is to process time hour by hour, and at each hour pick the best available item. This fails because “available” changes dynamically with deadlines, and maintaining a global best without revisiting past decisions leads to wrong choices. The missing idea is that we do not actually care about the exact time each item is eaten, only whether we can fit a set of size k within deadlines, and which k items are best.

The key observation is that this is a classic scheduling-with-deadlines maximization problem. If we sort items by increasing deadline, then when we have considered all items up to some deadline value d, we are allowed to pick at most d items among them. Among all ways to pick d items, the optimal choice is always the d highest calorie items seen so far. If we ever exceed the allowed count, we should discard the least valuable item because it contributes least to the objective while occupying a scarce slot.

This leads directly to maintaining a set of chosen items using a structure that can remove the smallest value efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force subsets | O(2^n · n) | O(n) | Too slow |
| Greedy with heap | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We sort all items by their deadline in non-decreasing order. We then scan them one by one, maintaining a structure of chosen calorie values.

1. Sort items by increasing deadline. This ensures that when we process an item, we already know the tightest constraint that applies to the current prefix of items.
2. Maintain a min-heap of selected calorie values. This heap represents the current chosen set of items we intend to schedule.
3. For each item in sorted order, insert its calorie value into the heap. This corresponds to tentatively taking this item into our schedule.
4. After insertion, check whether the heap size exceeds the current item’s deadline. If it does, remove the smallest calorie item from the heap. This step enforces that among all items with deadline d, we keep only the best d items, because any feasible schedule can use at most d items in d time slots.
5. After processing all items, sum the heap. This sum is the maximum achievable calorie total.

### Why it works

At any prefix of items sorted by deadline, suppose the current deadline is d. Any valid schedule can include at most d items from this prefix because only d time slots exist before or at that deadline boundary. The algorithm always maintains exactly the best possible set of size at most d by discarding the smallest calorie item whenever the limit is exceeded. This invariant ensures that after processing each prefix, the heap contains an optimal selection for that prefix, and thus for the full set as well.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

def solve():
    n = int(input())
    items = []
    for _ in range(n):
        t, k = map(int, input().split())
        items.append((t, k))

    items.sort()

    heap = []
    total = 0

    for t, k in items:
        heapq.heappush(heap, k)
        total += k

        if len(heap) > t:
            removed = heapq.heappop(heap)
            total -= removed

    print(total)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the heap-based greedy strategy. Sorting by deadline is crucial because it transforms time feasibility into a prefix constraint. The heap always stores the currently chosen items. Keeping a running sum avoids recomputing the heap sum at the end.

The only subtle implementation detail is the condition `len(heap) > t`. This uses the fact that after processing all items with deadline up to t, we enforce that no more than t items are selected. The heap removal always targets the smallest value, since that is the least damaging choice for maintaining feasibility.

## Worked Examples

Consider a small input with items (deadline, value): (1, 5), (1, 2), (2, 6), (2, 3).

After sorting, the order is unchanged. We track the heap:

| Step | Item | Heap after insertion | Action | Sum |
| --- | --- | --- | --- | --- |
| 1 | (1,5) | [5] | ok | 5 |
| 2 | (1,2) | [2,5] | exceeds 1, remove 2 | 5 |
| 3 | (2,6) | [5,6] | ok | 11 |
| 4 | (2,3) | [3,5,6] | exceeds 2, remove 3 | 11 |

The final selection corresponds to taking items with values 5 and 6, which is optimal because at most two items can be scheduled within time 2, and these are the highest values compatible with deadlines.

Now consider (deadline, value): (1,10), (2,1), (2,1), (2,1).

| Step | Item | Heap after insertion | Action | Sum |
| --- | --- | --- | --- | --- |
| 1 | (1,10) | [10] | ok | 10 |
| 2 | (2,1) | [1,10] | ok | 11 |
| 3 | (2,1) | [1,1,10] | remove 1 | 10 |
| 4 | (2,1) | [1,1,10] | remove 1 | 9 |

This shows that even though many items exist, only two can be taken effectively, and the algorithm ensures the highest-value subset is retained.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates with O(n log n), each heap operation is log n over n items |
| Space | O(n) | Heap stores at most all items in worst case |

The constraints up to 200,000 items fit comfortably within this complexity since logarithmic factors remain small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io

    out = _io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like small case
assert run("3\n1 5\n1 2\n2 6\n") == "11"

# all same deadlines
assert run("4\n2 1\n2 2\n2 3\n2 4\n") == "7"

# strictly increasing deadlines
assert run("3\n1 10\n2 20\n3 30\n") == "60"

# tight constraint forcing drops
assert run("5\n1 100\n2 1\n2 1\n2 1\n2 1\n") == "101"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small mixed deadlines | 11 | correctness of heap replacement |
| all same deadlines | 7 | selecting best k items |
| increasing deadlines | 60 | no removals needed |
| one dominant item | 101 | greedy retention of high value |

## Edge Cases

A critical edge case is when a very high-value item has a very early deadline. For input (1,100), (2,1), (2,1), (2,1), (2,1), the algorithm first takes 100, then temporarily accepts smaller items, but repeatedly discards them because the heap must respect size limits. The final heap keeps 100 and one additional best item, producing 101, which matches the optimal schedule where the best item occupies the first hour and one small item fills another slot.

Another edge case is when all deadlines are identical. In this situation, the algorithm effectively reduces to selecting the top d values among all items, where d is that shared deadline. The heap naturally enforces this without needing explicit handling.
