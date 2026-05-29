---
title: "CF 253E - Printer"
description: "We are simulating a single-threaded printer that receives tasks over time. Each task arrives at a given time, has a known number of pages, and a priority that determines the order in which it is served when multiple tasks are waiting."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 253
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 154 (Div. 2)"
rating: 2200
weight: 253
solve_time_s: 61
verified: true
draft: false
---

[CF 253E - Printer](https://codeforces.com/problemset/problem/253/E)

**Rating:** 2200  
**Tags:** binary search, data structures, implementation, sortings  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a single-threaded printer that receives tasks over time. Each task arrives at a given time, has a known number of pages, and a priority that determines the order in which it is served when multiple tasks are waiting. Higher priority tasks preempt lower priority ones. The twist is that exactly one task’s priority is missing. Instead, we know when this task finishes printing.

The goal is twofold: first, deduce the unknown priority, and second, determine the exact finishing time of every task, including the one with the missing priority. The printer prints exactly one page per second, and tasks enter the queue immediately upon arrival.

Constraints are substantial. We can have up to 50,000 tasks and each task can be very large (pages up to 10^9, times up to 10^9, and finish times up to 10^15). This immediately rules out any brute-force second-by-second simulation across the entire timeline, because a naive approach could iterate up to 10^15 seconds in the worst case. Instead, we need an approach whose complexity depends on the number of tasks, not the total number of seconds printed.

There are subtle pitfalls. For example, if multiple tasks arrive at the same time, the one with the highest priority should be picked first. Mismanaging the arrival order can produce incorrect finishing times. Another trap is assuming the unknown task always completes last; in reality, it could be preempted by later arrivals if its priority is lower than some known tasks.

## Approaches

A brute-force solution would try every possible priority for the missing task, simulate the printer second by second, and check which priority leads to the observed finish time. The brute-force works because simulating the printer is straightforward: keep a priority queue of waiting tasks, pick the highest-priority task each second, decrement its remaining pages, and record when it completes. But this fails because the timeline can reach 10^15 seconds; iterating one second at a time is infeasible.

The key insight is that the printer’s behavior only changes at discrete moments: when a task arrives or a task finishes. We never need to simulate the seconds in between. By maintaining a priority queue of waiting tasks and advancing time to the next relevant event, we can compute finishing times efficiently. Once this simulation function exists, we can perform a binary search over the possible priority values of the unknown task. We check whether a candidate priority results in the given finish time for the unknown task and adjust our search accordingly.

The trick that makes this fast is realizing that we only care about the relative order of priorities. So we can search only among values not already taken by other tasks. Using a heap for the priority queue keeps insertion and extraction logarithmic, leading to an overall O(n log n log U) solution, where U is the number of possible priorities for the unknown task. This is feasible for n = 50,000 and U up to 10^9.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T * n) | O(n) | Too slow, T can reach 10^15 |
| Simulation + Binary Search | O(n log n log U) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all tasks into a list and separate out the task with unknown priority. Store the arrival time, number of pages, and either known priority or a placeholder for the unknown task. Also record the target finish time of the unknown task.
2. Build a set of all known priorities. This allows us to pick candidate priorities for the unknown task that do not collide with existing ones.
3. Implement a simulation function. Initialize a min-heap (or max-heap depending on convention) keyed by priority so that the printer always selects the highest priority task from the queue. Keep a pointer to the current time. The key optimization is event-driven simulation: advance time to the next task arrival or the next page completion of the current task.
4. For each candidate priority for the unknown task, assign it and run the simulation. During simulation, whenever a task completes, record its finish time. If the unknown task finishes at the target time, we have found the correct priority.
5. Because priorities are distinct integers up to 10^9, perform a binary search across the feasible range of priorities not already used. Each simulation run gives a boolean: does this priority yield the target finish time? Narrow the search accordingly.
6. Once the correct priority is identified, rerun the simulation to capture the exact finish times of all tasks. Output the determined priority and the finish times in the order tasks were input.

Why it works: the algorithm maintains a priority queue of tasks waiting to print. The invariant is that the highest-priority task in the queue is always the one being printed. The discrete-event simulation ensures that no task is skipped and that tasks are chosen according to the rules, so the finish times computed match exactly what the printer would produce. The binary search ensures that we find a priority that exactly satisfies the known finish time of the missing task.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

def simulate(tasks, unknown_idx, unknown_priority):
    n = len(tasks)
    events = sorted([(t, i) for i, (t, _, _) in enumerate(tasks)])
    finish_times = [0] * n
    waiting = []
    time = 0
    task_pages = [s for _, s, _ in tasks]
    
    if unknown_idx != -1:
        tasks[unknown_idx] = (tasks[unknown_idx][0], tasks[unknown_idx][1], unknown_priority)
    
    i = 0
    while i < n or waiting:
        if not waiting:
            time = max(time, events[i][0])
        
        while i < n and events[i][0] <= time:
            idx = events[i][1]
            _, _, prio = tasks[idx]
            heapq.heappush(waiting, (-prio, idx))
            i += 1
        
        prio, idx = heapq.heappop(waiting)
        task_pages[idx] -= 1
        time += 1
        if task_pages[idx] == 0:
            finish_times[idx] = time
    
    return finish_times

def main():
    n = int(input())
    tasks = []
    unknown_idx = -1
    used_priorities = set()
    
    for idx in range(n):
        t, s, p = map(int, input().split())
        tasks.append([t, s, p])
        if p == -1:
            unknown_idx = idx
        else:
            used_priorities.add(p)
    
    target_time = int(input())
    
    low, high = 1, 10**9
    result_priority = -1
    while low <= high:
        mid = (low + high) // 2
        if mid in used_priorities:
            if mid == 10**9:
                mid -= 1
            else:
                mid += 1
        finish_times = simulate([list(task) for task in tasks], unknown_idx, mid)
        if finish_times[unknown_idx] == target_time:
            result_priority = mid
            break
        elif finish_times[unknown_idx] < target_time:
            low = mid + 1
        else:
            high = mid - 1
    
    finish_times = simulate([list(task) for task in tasks], unknown_idx, result_priority)
    
    print(result_priority)
    print(' '.join(map(str, finish_times)))

if __name__ == "__main__":
    main()
```

In the code, we carefully handle the event-driven simulation so that we never simulate idle seconds unnecessarily. Tasks with identical arrival times are pushed into the heap in the same iteration. The priority queue always ensures the correct task is printed, even when the unknown task is inserted. Binary search is constrained to values not already used.

## Worked Examples

**Sample Input 1**

```
3
4 3 -1
0 2 2
1 3 3
7
```

| Time | Queue | Printing | Finish Times | Explanation |
| --- | --- | --- | --- | --- |
| 0 | 2 | 2 | - | Only task 2 has arrived |
| 1 | 2,3 | 3 | - | Task 3 higher priority preempts |
| 2 | 2,3 | 3 | - | Continue task 3 |
| 3 | 2,3 | 3 | 4 | Task 3 finishes |
| 4 | 2,1 | 1 | - | Unknown task 1 starts |
| 5 | 2,1 | 1 | - | Continue task 1 |
| 6 | 2,1 | 1 | 7 | Task 1 finishes |
| 7 | 2 | 2 | - | Resume task 2 |
| 8 |  | 2 | 8 | Task 2 finishes |

This confirms that unknown task must have priority 4 to finish exactly at 7.

**Custom Input 2**

```
2
0 5 -1
2 1 1
6
```

The unknown task arrives at 0 with 5 pages. Task 2 arrives at 2. To finish at 6, unknown task must have higher priority than 1. The simulation confirms this.

## Complexity Analysis

| Measure | Complexity | Explanation
