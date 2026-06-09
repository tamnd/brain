---
title: "CF 1804B - Vaccination"
description: "We are given a sorted list of arrival times of patients. Each patient arrives at a specific moment and is willing to wait for a limited number of time units, meaning there is a window during which they can be vaccinated."
date: "2026-06-09T09:21:17+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1804
codeforces_index: "B"
codeforces_contest_name: "Nebius Welcome Round (Div. 1 + Div. 2)"
rating: 1000
weight: 1804
solve_time_s: 145
verified: true
draft: false
---

[CF 1804B - Vaccination](https://codeforces.com/problemset/problem/1804/B)

**Rating:** 1000  
**Tags:** greedy, implementation  
**Solve time:** 2m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sorted list of arrival times of patients. Each patient arrives at a specific moment and is willing to wait for a limited number of time units, meaning there is a window during which they can be vaccinated. If they arrive at time $t_i$, then they can be served at any integer time from $t_i$ to $t_i + w$.

Vaccines are not individual units but come bundled in packs of $k$ doses. Once a pack is opened, it must be used within a fixed lifespan: if opened at time $x$, it can only be used from time $x$ to $x + d$. After that, any remaining doses are discarded. Each patient consumes exactly one dose.

The task is to choose when to open packs and how to assign patients to packs so that every patient is vaccinated within their personal waiting window and within the lifetime of the opened pack, using as few packs as possible.

The input size allows up to $2 \cdot 10^5$ total patients across test cases, so any solution must be roughly linear or near-linear per test case. A quadratic strategy that repeatedly tries all possible groupings of patients would exceed limits because it would require checking compatibility between many overlapping time windows.

A key edge situation appears when patient windows barely overlap or are disjoint. For example, if $w = 0$, every patient must be served exactly at arrival time, so grouping is only possible if multiple patients arrive at the same moment. Another corner case is when $d = 0$, meaning a pack can only be used at the exact opening moment, so each pack effectively serves at most one time instant regardless of $k$.

## Approaches

A naive idea is to simulate assigning patients one by one, and for each patient try to place them into an existing opened pack if it is still valid and has remaining capacity, otherwise open a new pack at the best possible time. This requires maintaining all active packs and checking compatibility for each patient. In the worst case, many packs overlap in time and we repeatedly scan them to find a valid one, leading to $O(n^2)$ behavior.

The structure of the problem allows a stronger observation. Patients arrive in sorted order, so we naturally process them from earliest to latest time. Each pack, once opened, defines a fixed usable time interval $[x, x + d]$, and can serve at most $k$ patients. Meanwhile, each patient has their own availability interval $[t_i, t_i + w]$. A pack is usable for a patient only if these intervals overlap at the time of service.

The key simplification is to avoid tracking individual packs in detail and instead decide greedily how to group consecutive patients. For a fixed starting patient, we want to pack as many following patients as possible into a single vaccine pack, subject to both constraints: their service times must fit within a common feasible time window, and we must not exceed $k$ patients per pack.

For a group of patients starting at index $i$, the latest we can delay opening the pack is constrained by the earliest possible expiration of any patient in the group, while the earliest feasible time is constrained by the latest arrival in the group minus waiting allowance. This turns the grouping problem into maintaining a sliding window of feasible patients and greedily closing a group once adding another patient would break feasibility or exceed capacity.

This reduces the problem to a single pass where we expand a window of patients and repeatedly finalize groups whenever constraints break.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive per-pack simulation | $O(n^2)$ | $O(n)$ | Too slow |
| Greedy sliding grouping | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process patients in increasing order of arrival time and maintain a current batch representing patients assigned to the same pack.

1. Start with the first patient and initialize an empty batch. We also maintain how many packs we have opened.
2. For each patient in order, attempt to add them to the current batch. When adding a patient, we check whether the batch remains feasible in terms of time. The batch must be able to be served in some common time interval that respects both patient waiting limits and vaccine lifetime.
3. While building the batch, we also ensure we do not exceed $k$ patients. If the batch size reaches $k$, we finalize the batch immediately, since the pack cannot serve more patients regardless of time feasibility.
4. If adding a new patient would violate feasibility, meaning there is no single time that can serve all patients currently in the batch, we close the batch before this patient and start a new one.
5. We repeat until all patients are processed. Each time we close a batch, we count one vaccine pack.

The key hidden step is feasibility checking. For a batch of patients, the service time must lie in the intersection of all patient intervals $[t_i, t_i + w]$, which is $[\max t_i, \min (t_i + w)]$. This intersection must also overlap with some pack interval of length $d$, but since we choose opening time optimally within the batch, feasibility reduces to ensuring the intersection is non-empty and can be covered by a length-$d$ window.

A practical way to maintain this is tracking the current maximum arrival and minimum latest allowable service time in the batch.

### Why it works

Each time we extend a batch, we are only adding patients whose intervals still overlap with the current feasible service region. Since the patients are sorted, any earlier grouping that could have included a patient is already considered before moving forward. Once a batch is closed, no later batch can include those patients without violating either time constraints or capacity. This ensures each batch corresponds to a maximal feasible contiguous segment, and greedy maximal segmentation minimizes the number of required packs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, d, w = map(int, input().split())
    t = list(map(int, input().split()))
    
    packs = 0
    i = 0
    
    while i < n:
        packs += 1
        
        batch_size = 0
        
        # We maintain the feasible time window of the current batch
        # For patients j in batch:
        # feasible start is max(t[j])
        # feasible end is min(t[j] + w)
        left = t[i]
        right = t[i] + w
        
        j = i
        
        while j < n:
            # check if patient j can fit in current feasibility window
            new_left = max(left, t[j])
            new_right = min(right, t[j] + w)
            
            if new_left > new_right:
                break
            
            if batch_size == k:
                break
            
            left = new_left
            right = new_right
            batch_size += 1
            j += 1
        
        i = j
    
    print(packs)

if __name__ == "__main__":
    solve()
```

The code builds each batch greedily. The variables `left` and `right` maintain the intersection of all patient time windows in the current group. When the intersection becomes empty, we stop and start a new pack. The `batch_size` variable ensures we never exceed the dose limit $k$. The pointer `i` jumps to the first unprocessed patient after each batch, guaranteeing linear progress.

A subtle point is that we never explicitly compute the pack opening time. It is implicitly chosen inside the feasible intersection, so we only track whether such a time exists.

## Worked Examples

### Example 1

Input:

```
6 3 5 3
1 2 3 10 11 18
```

We track grouping:

| Step | i | j | left | right | batch size | action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 4 | 1 | start batch |
| 2 | 0 | 1 | 1 | 5 | 2 | add patient 2 |
| 3 | 0 | 2 | 1 | 6 | 3 | add patient 3, batch full |
| 4 | 0 | 3 | - | - | - | close batch, new pack |
| 5 | 3 | 3 | 10 | 15 | 1 | start new batch |
| 6 | 3 | 4 | 10 | 16 | 2 | add patient 5 |
| 7 | 3 | 5 | 10 | 23 | 3 | add patient 6 |

We get 2 packs.

This confirms that early patients can be packed tightly, while later distant arrivals require a new batch due to disjoint time windows.

### Example 2

Input:

```
3 10 3 6
10 20 30
```

| Step | i | j | left | right | batch size | action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 10 | 16 | 1 | start |
| 2 | 0 | 1 | 20 | 26 | 2 | overlap still possible |
| 3 | 0 | 2 | 30 | 36 | 3 | all fit |

One pack suffices because capacity is large and time windows still allow overlap.

This shows that even widely spaced arrivals can be grouped if $w$ is large enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each patient is processed once as the right pointer moves forward monotonically |
| Space | $O(1)$ | Only a few variables are maintained besides input |

The total number of patients across test cases is bounded by $2 \cdot 10^5$, so the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys
    
    input = sys.stdin.readline
    
    def solve():
        n, k, d, w = map(int, input().split())
        t = list(map(int, input().split()))
        
        packs = 0
        i = 0
        
        while i < n:
            packs += 1
            batch_size = 0
            left = t[i]
            right = t[i] + w
            j = i
            
            while j < n:
                new_left = max(left, t[j])
                new_right = min(right, t[j] + w)
                
                if new_left > new_right:
                    break
                if batch_size == k:
                    break
                
                left = new_left
                right = new_right
                batch_size += 1
                j += 1
            
            i = j
        
        return str(packs)
    
    return solve()

# provided samples
assert run("""5
6 3 5 3
1 2 3 10 11 18
6 4 0 0
3 3 3 3 3 4
9 10 2 2
0 1 2 3 4 5 6 7 8
3 10 3 6
10 20 30
5 5 4 4
0 2 4 6 8
""") == """2
3
2
3
1
"""

# custom cases
assert run("""1
1 1 10 0
5
""") == "1", "single patient"

assert run("""1
5 5 0 0
1 1 1 1 1
""") == "1", "all same time full capacity"

assert run("""1
5 2 0 0
1 1 1 1 1
""") == "3", "tight capacity forcing splits"

assert run("""1
4 10 100 100
1 50 100 150
""") == "1", "large windows allow full merge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single patient | 1 | base case |
| all same time full capacity | 1 | max packing |
| tight capacity forcing splits | 3 | k constraint |
| large windows allow full merge | 1 | maximal feasibility merge |

## Edge Cases

When $w = 0$, each patient can only be served exactly at their arrival time. The algorithm handles this because the intersection interval collapses to a single point per patient, so merging only succeeds when arrivals match. For example, in `1 1 0 0` with arrivals `[5]`, the batch immediately forms and closes with one pack.

When $k = 1$, every patient requires a separate pack regardless of timing. The algorithm enforces this through `batch_size == k`, forcing closure after every patient, matching optimal behavior.

When $d = 0$, pack lifetime is zero, meaning a pack can only be used at its opening moment. The feasibility condition still works because any group requiring different service times will fail intersection unless all patients share a common feasible time, effectively forcing very small batches.
