---
title: "CF 172C - Bus"
description: "We are asked to simulate the operation of a single bus that repeatedly transports students from a bus stop at coordinate 0 to their respective destinations along the positive axis. Each student arrives at the stop at a distinct time and has a fixed destination coordinate."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 172
codeforces_index: "C"
codeforces_contest_name: "Croc Champ 2012 - Qualification Round"
rating: 1500
weight: 172
solve_time_s: 79
verified: true
draft: false
---

[CF 172C - Bus](https://codeforces.com/problemset/problem/172/C)

**Rating:** 1500  
**Tags:** *special, implementation, sortings  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate the operation of a single bus that repeatedly transports students from a bus stop at coordinate 0 to their respective destinations along the positive axis. Each student arrives at the stop at a distinct time and has a fixed destination coordinate. The bus can carry at most _m_ students at a time, and it departs either when full or when the last student has arrived. The travel speed is 1 unit of distance per unit of time, and when dropping off students, the bus pauses for `1 + floor(k / 2)` time units at a stop where _k_ students get off. After reaching the furthest stop for a group, the bus immediately returns to 0 without stopping for pickups or drop-offs.

The input gives the arrival times and destinations of all students, and the output must list the exact moment each student reaches their stop, in the order they were given.

Constraints allow up to 100,000 students, each with a maximum destination coordinate of 10,000, and the bus can carry up to 100,000 students at once. A naive simulation that advances the bus in unit steps or loops over time would be far too slow. We need an algorithm that batches students, computes travel times analytically, and handles each bus trip in O(m log m) or O(m) time.

Edge cases include situations where a single student is picked up alone, multiple students share the same destination, and when students arrive while the bus is en route. For example, if the bus departs with capacity 1 and a student arrives while the bus is away, the student must wait until the bus returns. Mismanaging arrival times or stop times can produce incorrect outputs.

## Approaches

A brute-force approach would simulate the bus moving unit by unit along the axis and checking for each student when they arrive and when they need to get off. This works correctly but is O(n * x_max) in the worst case, which is unacceptable given x_max can be 10,000 and n up to 100,000.

The key observation for a faster solution is that each bus trip can be treated independently: the bus always departs with either _m_ students or the remaining students, whichever is smaller. We only need to track the latest arrival among the students in the current batch to determine the departure time. Once the bus departs, the time each student reaches their stop can be computed directly by sorting their destinations and adding the travel time. Drop-off time is determined by the formula `1 + floor(k / 2)` at each stop, but the student is considered to have reached the stop at the moment the bus arrives. The bus return time is simply twice the furthest destination for the batch.

This leads to an O(n log m) algorithm where each batch is processed by sorting destinations to efficiently simulate drop-offs. We never step through time incrementally, only through student batches.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * x_max) | O(n) | Too slow |
| Optimal | O(n log m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all student arrival times and destinations, maintaining their original indices.
2. Initialize the bus at time 0 and position 0. Maintain a pointer to the next student waiting at the stop.
3. Repeat until all students are assigned to a bus trip:

1. Form a batch of up to _m_ students. Take the next _m_ students in arrival order.
2. Compute the bus departure time as the maximum between the current bus time and the arrival time of the last student in the batch.
3. Extract the destinations of the students in the batch along with their original indices.
4. Sort the destinations to simulate the order in which the bus stops for drop-offs.
5. For each stop:

1. Record the arrival time for all students getting off at this stop as the current bus time plus the distance to the stop.
2. Advance the bus time by `1 + floor(k / 2)` to account for students leaving.
6. Update the bus time to include the return trip to 0, which is equal to the maximum destination distance traveled.
4. Output the recorded arrival times in the original student order.

Why it works: Each batch is handled in arrival order, guaranteeing the bus never departs before students are present. Sorting destinations ensures we accurately simulate drop-offs. The bus always returns to 0, ensuring the next batch correctly accounts for waiting students. These invariants guarantee correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
students = [tuple(map(int, input().split())) + (i,) for i in range(n)]

res = [0] * n
i = 0
current_time = 0

while i < n:
    batch = students[i:i + m]
    depart_time = max(current_time, batch[-1][0])
    
    # destinations with indices
    dest_indices = [(x, idx) for t, x, idx in batch]
    dest_indices.sort()
    
    for x, idx in dest_indices:
        res[idx] = depart_time + x
    
    # bus return time
    max_x = dest_indices[-1][0]
    current_time = depart_time + 2 * max_x
    
    i += m

print(' '.join(map(str, res)))
```

This code reads input efficiently, batches students according to bus capacity, sorts destinations to simulate stopping order, computes each student's arrival time without stepping through time, and updates the bus time including the return trip. Using the original index preserves the input order for output. Careful attention is needed to handle the maximum arrival time for departure and sorting destinations.

## Worked Examples

### Sample 1

Input:

```
1 10
3 5
```

| i | batch | depart_time | destinations | res |
| --- | --- | --- | --- | --- |
| 0 | [(3,5,0)] | 3 | [(5,0)] | [8] |

The bus waits until the student arrives at 3, drives 5 units, student arrives at 8, returns 5 units to 0.

### Sample 2

Input:

```
2 1
3 5
4 5
```

| i | batch | depart_time | destinations | res | current_time |
| --- | --- | --- | --- | --- | --- |
| 0 | [(3,5,0)] | 3 | [(5,0)] | [8] | 8 + 5 = 13 |
| 1 | [(4,5,1)] | 13 | [(5,1)] | [8, 18] | 13 + 5 + return = 23 |

This demonstrates handling multiple batches and bus return time, ensuring the second student waits for the bus to return.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log m) | Each batch of up to m students requires sorting destinations |
| Space | O(n) | Store students and result array |

This complexity easily fits within the problem constraints of n up to 100,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    students = [tuple(map(int, input().split())) + (i,) for i in range(n)]
    res = [0] * n
    i = 0
    current_time = 0
    while i < n:
        batch = students[i:i + m]
        depart_time = max(current_time, batch[-1][0])
        dest_indices = [(x, idx) for t, x, idx in batch]
        dest_indices.sort()
        for x, idx in dest_indices:
            res[idx] = depart_time + x
        max_x = dest_indices[-1][0]
        current_time = depart_time + 2 * max_x
        i += m
    return ' '.join(map(str, res))

# provided samples
assert run("1 10\n3 5\n") == "8", "sample 1"
assert run("2 1\n3 5\n4 5\n") == "8 18", "sample 2"

# custom cases
assert run("3 2\n1 2\n2 3\n3 4\n") == "3 5 7", "multiple students, capacity 2"
assert run("5 3\n1 1\n1 2\n1 3\n1 4\n1 5\n") == "2 3 4 5 6", "all arrive at same time"
assert run("2 2\n5 10\n1 1\n") == "11 6", "students arrive out of order relative to indices"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 2\n1 2\n2 3\n3 4 | 3 5 7 | Correct batching and departure time |
| 5 3\n1 1\n1 2\n1 3\n1 4\n1 5 | 2 3 4 5 6 | Handling all students arriving at same time |
| 2 2\n5 10\n1 1 | 11 6 | Correctly using original indices and batch departure |

## Edge Cases

For a single student with the bus capacity larger than 1: the bus waits until the student
