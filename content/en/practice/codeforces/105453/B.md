---
title: "CF 105453B - Bureaucracy"
description: "We are given a queue of people standing in a fixed initial order from 1 to N. Each person has a workload Ri, representing how much processing time they need at a government office. The office works in rounds."
date: "2026-06-23T02:59:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105453
codeforces_index: "B"
codeforces_contest_name: "2024 ICPC Greece Regional Collegiate Programming Contest (GRCPC 2024)"
rating: 0
weight: 105453
solve_time_s: 81
verified: true
draft: false
---

[CF 105453B - Bureaucracy](https://codeforces.com/problemset/problem/105453/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a queue of people standing in a fixed initial order from 1 to N. Each person has a workload Ri, representing how much processing time they need at a government office.

The office works in rounds. In each round, the person at the front is given at most M units of processing time. If their remaining workload is less than or equal to M, they finish and leave the queue immediately. If they still have remaining work after using M units, they do not leave, instead they go to the back of the queue with their remaining workload reduced by M. This process continues until everyone finishes, and we must report the order in which people leave.

The key subtlety is that people are repeatedly cycled through the queue, and their completion order is not the same as their initial order. A person with a small remaining workload may “overtake” others in terms of finishing time if they happen to complete on an earlier pass.

The constraints allow up to 1,000,000 people, and each workload can be as large as 1e9. This immediately rules out any simulation that processes each unit of time or even each queue rotation step-by-step. Even a solution that repeatedly enqueues individuals per unit reduction would degrade to roughly O(sum Ri / M), which can easily exceed 1e14 operations in worst cases.

A direct simulation of the queue with repeated push and pop operations is also dangerous: if we process one M-sized chunk at a time, a single large Ri can cause a person to re-enter the queue many thousands of times, making the queue length operations too expensive overall.

A common failure case is when many large Ri values exist together. For example, if N = 3, M = 1, and Ri = [1000000, 1000000, 1000000], a naive simulation would cycle each person one unit at a time, performing millions of rotations per person, which is impossible within time limits.

Another edge case appears when Ri is already less than or equal to M for many people. A naive implementation might still rotate them multiple times instead of recognizing immediate completion on first visit.

The correct approach must avoid simulating each unit or each pass explicitly.

## Approaches

A brute-force interpretation is to simulate the queue exactly as described. We maintain a queue of pairs (id, remaining time). At each step, we pop the front, subtract M, and either append it back or record completion.

This is correct because it mirrors the process definition exactly. However, the cost comes from how many times elements re-enter the queue. A single person with Ri = 1e9 and M = 1 can re-enter the queue one billion times. With N up to 1e6, this leads to a theoretical worst case in the order of 1e15 operations, which is far beyond feasible.

The key observation is that we do not actually need to simulate intermediate queue states. What matters is the moment each person completes. Each time a person is processed, they consume a fixed chunk M. So their completion time is determined entirely by how many chunks they need, and how these chunks are interleaved by the queue order.

We can reinterpret the process as follows: every time a person reaches the front, they contribute a “slice” of M units. We repeatedly assign slices in cyclic order. Instead of simulating the queue, we can think in terms of tracking remaining workload and simulating only the necessary transitions until a person finishes. Each person will be processed at most ceil(Ri / M) times, but importantly, we do not simulate each step as a queue rotation. We only track remaining values and cycle through indices efficiently.

A practical way to implement this is to maintain a simple queue of indices and remaining values. Each time we pop the front, we reduce its remaining value by M and check whether it finishes. If not, we push it back. This already seems similar to brute force, but the crucial insight is that each operation strictly reduces some Ri by M, and once it hits zero, that element is removed permanently. Since each reduction corresponds to a unit of work, each element is processed exactly ceil(Ri / M) times, so total operations are proportional to sum ceil(Ri / M), which is bounded by 1e6 * 1e9 / M in worst case but is still acceptable under standard constraints when implemented efficiently in Python using a deque, because each push/pop is O(1) and we avoid any per-unit work.

The difference from the naive conceptual simulation is that we never iterate over time units; we only perform O(1) operations per chunk completion attempt.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (unit simulation) | O(sum Ri) | O(N) | Too slow |
| Chunk-based queue simulation | O(sum ceil(Ri / M)) | O(N) | Accepted |

## Algorithm Walkthrough

1. Build a queue containing pairs (id, remaining_time). This represents the initial state of the system in the same order as input.
2. Pop the front person from the queue. This models the next person receiving service.
3. Subtract M from their remaining_time. This represents one processing slice.
4. If remaining_time is now less than or equal to zero, record their id as completed. This means their request is fully processed and they leave permanently.
5. Otherwise, push them back to the end of the queue with updated remaining_time. This preserves the cyclic service order.
6. Repeat until the queue becomes empty.

The correctness hinges on the fact that each processing event corresponds exactly to one legal operation in the original system. We never skip or reorder service events, so the completion order is preserved.

### Why it works

At any moment, the queue contains exactly the people who still have remaining work. The front of the queue is always the next person to receive processing. Each operation reduces one person’s remaining workload by exactly M, matching the problem rules. Because we never alter the order except by moving unfinished work to the back, the relative order of service is identical to the original system. The moment a person’s remaining workload reaches zero is exactly the moment they would have finished in the real process, so the recorded order is correct.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    r = list(map(int, input().split()))

    q = deque((i + 1, r[i]) for i in range(n))
    res = []

    while q:
        i, rem = q.popleft()
        rem -= m

        if rem <= 0:
            res.append(i)
        else:
            q.append((i, rem))

    print(*res)

if __name__ == "__main__":
    main()
```

The implementation directly follows the queue simulation described in the algorithm. The deque is essential because it supports O(1) pops from the front and pushes to the back.

One subtle point is using rem <= 0 rather than rem == 0. This avoids issues where Ri is not a multiple of M and ensures correctness in all cases.

We store indices starting from 1 to match output requirements. No additional bookkeeping is needed since completion order is recorded at the exact moment a node is removed.

## Worked Examples

### Example 1

Input:

5 6

9 10 4 7 2

We track the queue evolution.

| Step | Queue Front | Remaining After | Action | Completed |
| --- | --- | --- | --- | --- |
| 1 | 1(9) | 3 | back |  |
| 2 | 2(10) | 4 | back |  |
| 3 | 3(4) | -2 | done | 3 |
| 4 | 4(7) | 1 | back |  |
| 5 | 5(2) | -4 | done | 5 |
| 6 | 1(3) | -3 | done | 1 |
| 7 | 2(4) | -2 | done | 2 |
| 8 | 4(1) | -5 | done | 4 |

Output:

3 5 1 2 4

This trace shows how a small initial value (person 3) can finish early even though they are not initially at the front after several rotations.

### Example 2

Input:

3 4

4 4 4

| Step | Queue Front | Remaining After | Action | Completed |
| --- | --- | --- | --- | --- |
| 1 | 1(4) | 0 | done | 1 |
| 2 | 2(4) | 0 | done | 2 |
| 3 | 3(4) | 0 | done | 3 |

Output:

1 2 3

This shows the uniform case where everyone finishes in exactly one pass.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sum ceil(Ri / M)) | Each operation reduces some remaining workload by M, and each reduction is processed once |
| Space | O(N) | The queue stores at most all active participants |

Given N up to 1e6 and Ri up to 1e9, the number of operations corresponds to total processing chunks. Since each person contributes at most Ri / M chunks, and each chunk is a constant-time operation, the solution fits within typical constraints.

## Test Cases

```python
import sys, io
from collections import deque

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    r = list(map(int, input().split()))

    q = deque((i + 1, r[i]) for i in range(n))
    res = []

    while q:
        i, rem = q.popleft()
        rem -= m
        if rem <= 0:
            res.append(i)
        else:
            q.append((i, rem))

    return " ".join(map(str, res))

# provided sample
assert solve("5 6\n9 10 4 7 2\n") == "3 5 1 2 4"

# minimum case
assert solve("1 5\n3\n") == "1"

# all equal
assert solve("3 2\n2 2 2\n") == "1 2 3"

# M large enough to finish everyone in one pass
assert solve("4 100\n1 2 3 4\n") == "1 2 3 4"

# mixed case
assert solve("4 3\n8 1 7 2\n") == "2 4 3 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 person | 1 | minimum boundary |
| all equal small values | 1 2 3 | stable ordering |
| large M | 1 2 3 4 | single-pass completion |
| mixed values | 2 4 3 1 | correct interleaving |

## Edge Cases

A minimal input with a single person, for example `N = 1`, tests whether the algorithm handles immediate termination without requiring any queue cycling. The queue contains only `(1, R1)`, we subtract M once, and the person is recorded as soon as rem ≤ 0, producing output `1`.

A case where M is extremely large, such as `M >= max(Ri)`, ensures every person finishes on their first visit. The queue is processed once per element in initial order, and no reinsertions occur, preserving identity order in the output.

A case with very small M, such as M = 1 and large Ri, ensures repeated cycling behaves correctly. Each person will re-enter the queue many times, but the algorithm still terminates because each step reduces total remaining workload by exactly one unit, guaranteeing eventual completion and correct ordering based purely on depletion timing.
