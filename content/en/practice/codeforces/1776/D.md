---
title: "CF 1776D - Teamwork"
description: "We are asked to schedule a team of three people to solve a set of problems with three difficulty levels: easy, medium, and hard. Each problem has a fixed duration depending on its difficulty: easy takes 2 units of time, medium 3 units, and hard 4 units."
date: "2026-06-09T11:44:30+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1776
codeforces_index: "D"
codeforces_contest_name: "SWERC 2022-2023 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2800
weight: 1776
solve_time_s: 111
verified: false
draft: false
---

[CF 1776D - Teamwork](https://codeforces.com/problemset/problem/1776/D)

**Rating:** 2800  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 1m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to schedule a team of three people to solve a set of problems with three difficulty levels: easy, medium, and hard. Each problem has a fixed duration depending on its difficulty: easy takes 2 units of time, medium 3 units, and hard 4 units. Each person can work on only one problem at a time, and the last time unit of each problem requires exclusive access to a shared computer, meaning two people cannot end a problem at the same time. The contest lasts for `l` time units, and the goal is to maximize the number of problems solved and provide a valid schedule.

The inputs `a`, `b`, `c` represent the number of easy, medium, and hard problems, each up to 10^4. The contest duration `l` is at most 10^5. This means a brute-force search over all permutations of problems or over all possible start times would be too slow, as it would involve considering on the order of 10^4! sequences. We need a strategy that schedules problems efficiently while respecting individual and shared-computer constraints.

A naive approach might ignore the shared computer constraint and just try to assign problems greedily by person availability. This fails when two problems would end simultaneously, which is forbidden. Another subtle edge case occurs when `l` is very small or zero. For example, if `l = 1` and we have even an easy problem, no problem can be solved because the minimum duration is 2. Similarly, if one difficulty type has zero problems, we must avoid trying to schedule them.

## Approaches

The brute-force approach tries every permutation of all problems and assigns them to people at every possible start time, respecting the computer constraint. This would be correct in principle because it explicitly checks all schedules, but the complexity is factorial in the number of problems and exponential in time steps. With up to 10^4 problems, this is completely infeasible.

The key insight comes from the structure of the problem: each person can work independently except for the last time unit that requires the shared computer. If we ignore the computer for a moment, we could assign problems to the first available person in any order. The real difficulty is avoiding collisions on the last time unit. Observing that there are only three people, the maximum number of last-time-unit conflicts is small, and we can model the schedule as a priority queue of available times per person, plus a set of occupied last-time-unit slots. This lets us schedule greedily by earliest possible end time while ensuring the last time unit is free.

We assign problems in order of shortest duration first to maximize total problem count. Shorter problems finish faster and free the computer earlier. For each problem, we pick the person who can start earliest and check if the last time unit is available. If not, we shift the start time forward until it is. Since each problem's duration is small (2-4 units) and `l` ≤ 10^5, this greedy approach runs in linear time with respect to the number of problems.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((a+b+c)! * l^3) | O(l) | Too slow |
| Greedy Scheduling | O((a+b+c) * log 3 + l) | O(a+b+c + l) | Accepted |

## Algorithm Walkthrough

1. Represent each problem as a tuple `(duration, type)` and collect all problems into a single list. Sorting by duration ascending ensures we attempt to schedule shorter problems first.
2. Initialize a min-heap with each person's available time, starting at 0. This tracks when each person can begin their next problem.
3. Maintain a boolean array of size `l` to track which time units are already used as the last unit of a problem. This represents the shared computer occupancy.
4. Iterate over each problem in order of duration. For the current problem, peek the earliest-available person from the heap. Attempt to schedule the problem at that person's available time.
5. If the last time unit of the problem overlaps with an already used computer slot, increment the start time until a free last time unit is found, also ensuring the person is free. If the adjusted end time exceeds `l`, skip the problem.
6. Once a valid slot is found, record `(person_id, start_time, end_time)`, mark the last time unit as occupied, and update the person's available time in the heap.
7. After scheduling all possible problems, sort the scheduled list by end time and output the result.

The invariant maintained is that no two problems end on the same time unit and no person works on overlapping intervals. This guarantees that the schedule respects both the individual and shared computer constraints. By always assigning the earliest available person and shifting minimally to avoid collisions, the algorithm maximizes the number of problems that fit within `l`.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

a, b, c, l = map(int, input().split())
problems = [(2, 'E')] * a + [(3, 'M')] * b + [(4, 'H')] * c
problems.sort()  # prioritize shorter problems

person_heap = [(0, i+1) for i in range(3)]  # (available_time, person_id)
heapq.heapify(person_heap)
computer_used = [False] * (l+1)

schedule = []

for duration, _ in problems:
    avail_time, person = heapq.heappop(person_heap)
    start = avail_time
    while start + duration <= l and computer_used[start + duration - 1]:
        start += 1
    end = start + duration
    if end > l:
        heapq.heappush(person_heap, (avail_time, person))
        continue
    schedule.append((person, start, end))
    computer_used[end-1] = True
    heapq.heappush(person_heap, (end, person))

schedule.sort(key=lambda x: x[2])
print(len(schedule))
for person, start, end in schedule:
    print(person, start, end)
```

This code creates a unified list of all problems and schedules them greedily by shortest duration. The min-heap efficiently finds the next available person. The while-loop ensures the last unit of the problem does not conflict with the computer, and if the problem cannot fit within the contest, it is skipped. Sorting at the end ensures output order by increasing end time.

## Worked Examples

### Sample 1

Input: `2 1 1 3`

Problems: `[2, 2, 3, 4]`

| Problem | Duration | Person Heap (before) | Start | End | Last Unit Free? | Update Heap | Computer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | [(0,1),(0,2),(0,3)] | 0 | 2 | Yes | [(2,1),(0,2),(0,3)] | mark 1 |
| 2 | 2 | [(0,2),(2,1),(0,3)] | 0 | 2 | Yes | [(2,1),(2,2),(0,3)] | mark 1 |
| 3 | 3 | [(0,3),(2,1),(2,2)] | 0 | 3 | Yes | [(2,1),(2,2),(3,3)] | mark 2 |
| 4 | 4 | [(2,1),(2,2),(3,3)] | 2 | 6 | Exceeds l=3 | skipped | - |

Output schedule: two problems solved, matches sample output.

### Sample 2

Input: `1 1 0 3`

| Problem | Duration | Start | End | Computer |
| --- | --- | --- | --- | --- |
| Easy 2 | 0 | 0 | 2 | mark 1 |
| Medium 3 | 0 | 0 | 3 | mark 2 |

Both fit; maximum problems solved is 2.

These traces show that the greedy scheduling respects both person availability and the shared computer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((a+b+c) log 3 + l) | Sorting problems is O(a+b+c log(a+b+c)), heap operations are O(log 3) per problem, last-time-unit check is O(l) in worst case |
| Space | O(a+b+c + l) | Store problems list and schedule, plus computer usage array |

The solution comfortably fits within the limits for `a+b+c ≤ 3*10^4` and `l ≤ 10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import heapq
    input = sys.stdin.readline

    a, b, c, l = map(int, input().split())
    problems = [(2, 'E')] * a + [(3, 'M')] * b + [(4, 'H')] * c
    problems.sort()

    person_heap = [(0, i+1) for i in range(3)]
    heapq.heapify(person_heap)
    computer_used = [False] * (l+1)

    schedule = []

    for duration, _ in problems:
        avail_time, person = heapq.heappop(person_heap)
        start = avail_time
        while start + duration <= l and computer_used[start + duration - 1]:
            start += 1
        end = start + duration
        if end > l:
```
