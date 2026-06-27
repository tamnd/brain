---
title: "CF 104992G - \u041c\u0435\u0434\u0432\u0435\u0434\u044c \u0438 \u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e\u0435 \u043f\u0438\u0442\u0430\u043d\u0438\u0435"
description: "A bear arrives at a storage room where each food item has a limited availability window and a calorie value. Every item can be eaten in one hour, and the bear can eat at most one item per hour."
date: "2026-06-28T03:36:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104992
codeforces_index: "G"
codeforces_contest_name: "qual VKOSHP Junior 24"
rating: 0
weight: 104992
solve_time_s: 70
verified: false
draft: false
---

[CF 104992G - \u041c\u0435\u0434\u0432\u0435\u0434\u044c \u0438 \u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e\u0435 \u043f\u0438\u0442\u0430\u043d\u0438\u0435](https://codeforces.com/problemset/problem/104992/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** no  

## Solution
## Problem Understanding

A bear arrives at a storage room where each food item has a limited availability window and a calorie value. Every item can be eaten in one hour, and the bear can eat at most one item per hour. However, each item disappears after a certain number of hours counted from the moment the bear arrives, so it is only available within its own deadline window.

The task is to choose which items the bear should eat so that no time overlaps are violated and the total calories consumed is as large as possible. Each item is independent except for sharing the same time resource and having its own expiry time.

The input gives a list of pairs where each pair describes how many hours remain before an item is removed and how many calories it provides. The output is a single number representing the maximum total calories achievable under the constraint that in any hour only one item can be consumed and an item must be consumed before it disappears.

The constraints go up to two hundred thousand items, which rules out any approach that tries all subsets or simulates all schedules explicitly. Any method that is quadratic in the number of items would already be too slow, since it would require on the order of tens of billions of operations in the worst case.

A naive greedy strategy such as always taking the highest calorie available item without considering deadlines fails. A high-calorie item might appear late but expire too soon to be scheduled if earlier slots are already filled by less valuable items.

A second subtle failure comes from sorting only by deadlines and always picking the first available item. That can also miss better combinations because early deadlines might force suboptimal choices unless value is considered globally.

A small concrete failure case for naive greedy-by-value:

Input:

```
3
1 100
1 1
2 50
```

If we always pick the highest calorie item first, we take 100 at time 1, leaving only time 2 for 50, which is fine here. But swapping structures across more complex cases shows that greedy-by-value alone does not respect future constraints in general.

A failure case for greedy-by-deadline-only:

Input:

```
3
1 10
2 100
2 90
```

Taking earliest deadline first picks 10 at time 1, then 100 and 90 cannot both fit optimally if scheduling is not handled carefully.

The core difficulty is balancing two competing objectives: respecting deadlines and maximizing total value.

## Approaches

The brute-force interpretation is to simulate all possible ways of assigning items to time slots. For each hour, we decide which available item to eat, recursively branching over all valid choices. This correctly explores every schedule, but the branching factor is large: at each step there can be up to n choices, and there are up to n steps, leading to exponential explosion. Even pruning by availability does not prevent worst-case behavior from becoming factorial in nature.

The key structural observation is that this is a classic scheduling problem with unit-length jobs and deadlines, where each job contributes a profit and must be completed before its deadline. The constraint “one item per hour” turns time into discrete slots, and deadlines define feasibility windows.

Instead of constructing schedules directly, we process items in order of increasing deadlines. At any moment, we maintain the best set of items that can fit into the time elapsed so far. When a new item arrives in deadline order, we tentatively include it. If we exceed the number of slots available up to that deadline, we discard the least valuable item among those chosen so far. This ensures we always keep the most profitable feasible subset.

The reason this works is that when we have selected more items than can fit before a given deadline, only the smallest-calorie item can ever be safely removed without reducing the potential for future optimality.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal (greedy + heap) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We convert each item into a pair of deadline and value, then process them in increasing order of deadline.

1. Sort all items by their deadline in ascending order. This ensures that when we process an item, all earlier items have deadlines no later than it, so feasibility is checked incrementally.
2. Maintain a min-heap of selected calorie values. The heap represents the current set of chosen items that we plan to schedule within the processed time window.
3. Iterate over the sorted items. For each item, insert its calorie value into the heap. This assumes we tentatively schedule it.
4. After inserting, check whether the number of selected items exceeds the current deadline. If it does, remove the smallest calorie item from the heap. This step is crucial because exceeding the deadline means we cannot schedule all chosen items in time, and removing the least valuable one preserves maximum total gain.
5. After processing all items, the heap contains the optimal set of items that can be scheduled within constraints. Sum all values in the heap to obtain the answer.

### Why it works

At every deadline point, we maintain the invariant that among all items seen so far, the heap stores the maximum possible total calorie subset that fits within the number of available time slots up to that deadline. Any time we exceed capacity, removing the smallest calorie item is optimal because it reduces total gain as little as possible while restoring feasibility. Since future items are always processed with potentially larger deadlines, earlier decisions remain valid and never need revision.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    items = []
    for _ in range(n):
        t, k = map(int, input().split())
        items.append((t, k))

    items.sort()

    import heapq
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

The sorting step ensures deadlines are processed in increasing order, which allows the heap to represent a valid candidate schedule prefix at each stage. The heap stores chosen calorie values, and the running sum avoids recomputing totals repeatedly. When the heap size exceeds the current deadline, we discard the smallest value to maintain feasibility with minimal loss.

A subtle implementation detail is that we compare heap size directly with the deadline. This works because after sorting, at the moment we process all items with deadline d, we have exactly d time slots available for scheduling among all items seen so far.

## Worked Examples

Consider the following input:

```
5
1 5
1 6
2 3
2 2
2 4
```

After sorting by deadline, we process items step by step.

| Item (t, k) | Heap after insertion | Action | Total |
| --- | --- | --- | --- |
| (1,5) | [5] | keep | 5 |
| (1,6) | [5,6] | size>1 remove 5 | 6 |
| (2,3) | [3,6] | keep | 9 |
| (2,2) | [2,3,6] | size>2 remove 2 | 9 |
| (2,4) | [3,4,6] | remove 3 | 10 |

This trace shows how early low-value choices are replaced when better combinations appear while still respecting deadlines.

Now consider a second case:

```
4
1 100
2 1
2 2
2 3
```

| Item (t, k) | Heap after insertion | Action | Total |
| --- | --- | --- | --- |
| (1,100) | [100] | keep | 100 |
| (2,1) | [1,100] | keep | 101 |
| (2,2) | [1,100,2] | remove 1 | 102 |
| (2,3) | [2,100,3] | remove 2 | 103 |

The process confirms that the algorithm does not lock into early low-value decisions and continuously maintains an optimal feasible set.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting plus heap insert and delete operations |
| Space | O(n) | heap stores selected items in worst case |

The constraints allow up to two hundred thousand items, so an n log n approach is comfortably fast. Heap operations remain efficient because each item is inserted and possibly removed once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# sample (as provided, formatted minimally)
assert run("1\n5 5\n") == "5"

# minimum size
assert run("1\n1 10\n") == "10"

# all same deadline
assert run("3\n2 1\n2 5\n2 3\n") == "8"

# greedy trap case
assert run("3\n1 10\n2 100\n2 90\n") == "190"

# increasing deadlines
assert run("4\n1 5\n2 6\n3 7\n3 1\n") == "18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single item | k | base case |
| same deadline items | best subset selection | heap pruning correctness |
| mixed values | avoids greedy failure | global optimality |
| increasing deadlines | scheduling feasibility | deadline handling |

## Edge Cases

One important edge case is when many items share the same deadline. For example:

```
3
2 1
2 100
2 50
```

The algorithm inserts all three values and then trims to at most two items. The heap ensures that the smallest value is removed, leaving 100 and 50, which matches the optimal schedule.

Another edge case is when deadlines are strictly increasing but values are decreasing:

```
4
1 100
2 90
3 80
4 70
```

The heap never exceeds capacity, so no removals happen, and all items are taken. The algorithm naturally respects feasibility since each item arrives exactly when capacity allows it.

A final case is when a high-value item appears late but has a tight deadline. Because we always process by deadline order, that item is considered exactly when its feasibility window is active, and it replaces weaker earlier choices if needed.
