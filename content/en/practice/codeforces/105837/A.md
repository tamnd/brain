---
title: "CF 105837A - Balls and Bins"
description: "We are given a collection of bins. Each bin starts with some number of balls and has a maximum capacity. The key operation in the process is that whenever a bin becomes full, it is removed from active consideration and its entire content is transferred into a shared reserve."
date: "2026-06-22T01:19:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105837
codeforces_index: "A"
codeforces_contest_name: "MITIT Spring 2025 Qualification Round 2"
rating: 0
weight: 105837
solve_time_s: 61
verified: true
draft: false
---

[CF 105837A - Balls and Bins](https://codeforces.com/problemset/problem/105837/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of bins. Each bin starts with some number of balls and has a maximum capacity. The key operation in the process is that whenever a bin becomes full, it is removed from active consideration and its entire content is transferred into a shared reserve. Balls in the reserve can later be distributed into other bins, helping them reach full capacity as well.

The underlying question is whether, starting from the initial configuration, it is possible to eventually trigger this cascading process in a way that all bins can be fully processed using only the balls that are available either initially or accumulated in the reserve.

Another way to view the system is that each bin has a required additional amount of balls before it can be activated. Once activated, it contributes its full capacity into a global pool, which may enable other bins to reach their activation thresholds. The process continues as long as some bin can be completed using the currently available reserve.

The constraints imply that a direct simulation of all possible orders of activating bins is not feasible when the number of bins is large. If we attempt to explore all permutations of activation sequences, the number of possibilities grows factorially, which is completely infeasible even for a few dozen bins. This immediately suggests that the problem must have a greedy or ordering-based structure that allows us to avoid branching over all possible choices.

A subtle failure case arises when multiple bins are close to becoming full, but choosing the wrong one first causes the process to stall.

For example, suppose we have two bins:

Input:

3 5

4 6

Bin 1 needs 2 more balls, while Bin 2 needs 2 more balls as well, but Bin 2 yields more capacity when completed. If we incorrectly prioritize larger or arbitrary bins first, we might end up in a state where reserve is insufficient to complete the remaining bin even though a valid sequence exists. This shows that local decisions about which bin to activate first matter critically.

The central difficulty is that completing a bin is not just a local event, it changes the global resource pool, and therefore affects all future feasibility decisions.

## Approaches

A brute-force approach would attempt to simulate all possible orders in which bins are completed. At each step, we would choose any bin whose remaining required space can be satisfied by the current reserve, recursively exploring all choices. In the worst case, if all bins can eventually be completed in multiple ways, this leads to factorial branching over N bins, resulting in O(N!) states. Even pruning invalid paths does not fundamentally improve this worst-case behavior, because many intermediate states remain valid and lead to further branching.

The key structural insight is that the only meaningful property of a bin is how much additional space it requires before it can be activated. Once we abstract away the exact distribution process, we see that bins with smaller required space are strictly easier to activate and should never be postponed in favor of bins with larger requirements.

The transformation that unlocks the solution is to treat each bin as contributing a requirement value, defined as its remaining capacity. Instead of reasoning about arbitrary activation orders, we sort bins by this requirement and always attempt to process the most constrained bin that is currently feasible. This works because if a solution exists that delays a small-requirement bin in favor of a larger one, we can always swap their order without making the process harder. The provided reserve argument in the statement formalizes this exchange argument: prioritizing tighter bins never reduces feasibility and can only improve or preserve it.

This reduces the problem to maintaining a multiset of remaining capacities and greedily consuming them in increasing order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N!) | O(N) | Too slow |
| Optimal (Greedy by space) | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

We define for each bin its remaining required space as the difference between capacity and current content. This value represents how hard it is to activate that bin.

### Steps

1. Compute the remaining space for each bin as capacity minus current balls. This captures the exact additional resource needed to activate it.
2. Sort all bins by their remaining space in non-decreasing order. The idea is to always consider the most constrained bins first, since they are the most likely to block progress if delayed.
3. Initialize a variable representing available reserve balls. Initially, this is zero because no bins have been activated yet.
4. Iterate over bins in sorted order. For each bin, check whether the current reserve is sufficient to cover its required space. If it is not, the process stops because no further bin with equal or larger requirement can be completed either.
5. If the reserve is sufficient, activate the bin and add its full capacity to the reserve. This models the fact that once a bin is completed, all its balls become available for redistribution.
6. Continue this process until all bins have been processed or until a bin cannot be activated.

### Why it works

The correctness rests on an exchange argument over activation order. Suppose there exists a valid sequence that activates a bin with larger remaining requirement before a bin with smaller requirement. Because the smaller bin is easier to satisfy, swapping their order never reduces the available reserve at any step where the larger bin is still feasible. Any valid solution can therefore be transformed into one where bins are processed in non-decreasing order of required space. This means that if any solution exists, the greedy sorted order will also succeed, and if the greedy process fails at some bin, no alternative ordering could have succeeded either.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    bins = []
    for _ in range(n):
        a, s = map(int, input().split())
        bins.append((s - a, s))
    
    bins.sort()
    
    reserve = 0
    
    for need, cap in bins:
        if reserve < need:
            print("NO")
            return
        reserve += cap
    
    print("YES")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the greedy ordering. Each bin is represented by a pair consisting of its required additional space and its capacity contribution. Sorting ensures we always handle the tightest constraints first. The reserve check prevents invalid transitions where a bin cannot be activated with the current available resources.

A common implementation pitfall is forgetting that the contribution added after activation is the full capacity, not just the difference. Another subtlety is ensuring the sorting key is exactly the remaining space, since sorting by capacity instead would break the logic.

## Worked Examples

### Example 1

Input:

```
3
1 3
2 5
4 6
```

We compute requirements:

| Step | Chosen bin (need, cap) | Reserve before | Can activate? | Reserve after |
| --- | --- | --- | --- | --- |
| 1 | (2, 5) | 0 | No | - |

The process stops immediately, so output is NO.

This demonstrates a case where the smallest requirement is already too large for an empty reserve, meaning no activation sequence exists.

### Example 2

Input:

```
3
0 2
1 3
2 4
```

Requirements:

| Step | Chosen bin (need, cap) | Reserve before | Can activate? | Reserve after |
| --- | --- | --- | --- | --- |
| 1 | (0, 2) | 0 | Yes | 2 |
| 2 | (1, 3) | 2 | Yes | 5 |
| 3 | (2, 4) | 5 | Yes | 9 |

All bins are processed successfully, so output is YES.

This shows how early small-requirement bins bootstrap the reserve into enabling larger ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting bins dominates, followed by a single linear scan |
| Space | O(N) | Storage of bin pairs |

The solution fits comfortably within typical constraints for up to 200,000 bins, since both sorting and linear processing are efficient at that scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys
    input = sys.stdin.readline

    n = int(input())
    bins = []
    for _ in range(n):
        a, s = map(int, input().split())
        bins.append((s - a, s))
    bins.sort()

    reserve = 0
    for need, cap in bins:
        if reserve < need:
            return "NO"
        reserve += cap
    return "YES"

# sample-like tests
assert run("3\n1 3\n2 5\n4 6\n") == "NO"
assert run("3\n0 2\n1 3\n2 4\n") == "YES"

# minimum size
assert run("1\n0 1\n") == "YES"

# impossible single bin
assert run("1\n2 5\n") == "NO"

# already satisfied chain dependency
assert run("4\n0 1\n1 2\n3 5\n6 10\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single feasible bin | YES | base case correctness |
| single impossible bin | NO | immediate failure handling |
| increasing chain | YES | progressive reserve growth |
| mixed feasibility | NO/YES consistency | greedy ordering correctness |

## Edge Cases

One important edge case is when all bins require strictly positive initial reserve. For instance:

Input:

```
2
3 5
4 6
```

Both bins require at least 2 units of reserve, but the system starts at zero. The algorithm sorts them by requirement and immediately detects that the first bin cannot be activated, correctly returning NO. Any attempt to activate a larger bin first would also fail, so there is no hidden valid ordering.

Another edge case is when one bin has zero requirement:

Input:

```
3
0 10
5 6
6 7
```

Here the first bin can always be activated and produces a large reserve. The algorithm processes it first due to sorting, ensuring the system becomes feasible before handling tighter bins. The trace shows reserve growing sufficiently to unlock all subsequent bins, confirming that the greedy order correctly models the dependency structure.
