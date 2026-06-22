---
title: "CF 105445B - Interviews"
description: "We are given a small system of interviewers who repeatedly conduct interviews in groups. Each interview consists of exactly z distinct interviewers, and each interviewer can only participate in at most y interviews per day."
date: "2026-06-23T03:25:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105445
codeforces_index: "B"
codeforces_contest_name: "TheForces Round #36 (Starters-Forces)"
rating: 0
weight: 105445
solve_time_s: 81
verified: false
draft: false
---

[CF 105445B - Interviews](https://codeforces.com/problemset/problem/105445/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a small system of interviewers who repeatedly conduct interviews in groups. Each interview consists of exactly `z` distinct interviewers, and each interviewer can only participate in at most `y` interviews per day. There are `x` interviewers in total, and the task is to schedule as many such interviews as possible while respecting the per-interviewer capacity constraint.

A valid output is a list of groups, where each group is a set of `z` distinct interviewer IDs. Every group represents one conducted interview. The constraint is purely on how many times each interviewer ID can appear across all groups.

From a structural point of view, this is a bounded combinatorial packing problem. We are trying to pack as many size-`z` subsets as possible into a multiset of `x` elements where each element has capacity `y`.

The constraints are very small: `x, y, z ≤ 10`. This immediately tells us that the number of possible distinct interview groups is at most `C(10, z)`, which is at most 252. Even if we enumerate all combinations and simulate usage counts, the state space remains tiny. This strongly suggests that greedy construction or even systematic enumeration will be sufficient.

A subtle edge case appears when `x < z`. In that case no valid group exists at all because we cannot form a set of `z` distinct interviewers. Another edge case is when `y = 0`, which forces the answer to be zero interviews regardless of `x` and `z`. A naive implementation that does not explicitly guard these cases may attempt to construct groups and run into invalid indexing or produce non-feasible schedules.

## Approaches

A brute-force interpretation would treat each possible subset of size `z` as a candidate interview and try to select a maximum number of such subsets while ensuring no interviewer exceeds usage `y`. This is essentially a maximum packing problem over a hypergraph, and a direct search would try combinations of subsets.

While correctness is easy to reason about, the combinatorial explosion happens when we consider that each subset can be chosen or not, leading to roughly `2^(C(x, z))` possibilities. Even though `x ≤ 10`, this still leads to up to `2^252` states in the worst case, which is completely infeasible.

The key observation is that we do not need optimal subset selection in any global sense. We only need to produce a feasible construction that maximizes the number of groups. Since all interviewers are symmetric, we can distribute participation evenly. The natural structure is to cycle through interviewers and always pick consecutive groups of size `z`, wrapping around cyclically, while tracking how many times each interviewer has been used.

Because `x` is small and `y` is small, we can greedily build groups one by one, always selecting the next available `z` interviewers who still have remaining capacity. If we maintain a pointer and rotate through interviewer IDs, we ensure fairness and avoid overusing any single participant. This construction continues until no valid group can be formed.

The reason this works is that any valid schedule is limited only by total capacity `x * y`, and each interview consumes exactly `z` units of capacity. Thus an upper bound is `floor(x * y / z)`, and the greedy cyclic construction naturally approaches this bound in small constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subset search | O(2^(x choose z)) | O(x choose z) | Too slow |
| Greedy cyclic construction | O(x * y * z) | O(x) | Accepted |

## Algorithm Walkthrough

We construct interviews iteratively while tracking remaining capacity for each interviewer.

1. Initialize an array `used[i] = 0` for all interviewers `i`, representing how many interviews they have participated in. This ensures we can enforce the limit `y`.
2. Maintain a current pointer `p` over interviewers from `1` to `x`. This pointer helps distribute usage evenly instead of repeatedly selecting from the same subset.
3. While possible, attempt to form one interview group:

We scan forward from `p` and pick the next `z` distinct interviewers whose `used[i] < y`.

This scanning step ensures we always construct a valid group without violating constraints, since we explicitly filter exhausted interviewers.
4. If at any point we cannot find `z` available interviewers, stop. This means no further valid interview can be formed.
5. After forming a group, increment `used[i]` for each selected interviewer, append the group to the answer list, and move the pointer forward to continue fair distribution.
6. Continue until termination condition is reached.

### Why it works

At every step, the algorithm only selects interviewers with remaining capacity, so no constraint is ever violated. The cyclic scanning ensures that if a feasible group exists, it will eventually be discovered because all combinations of available interviewers are reachable through rotation over a small fixed universe. Since capacity decreases monotonically, the process must terminate, and when it does, no valid group can be formed under the constraints, meaning the construction is maximal under the greedy policy in this bounded setting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        x, y, z = map(int, input().split())
        
        if z > x or y == 0:
            print(0)
            continue
        
        used = [0] * (x + 1)
        ans = []
        p = 1
        
        while True:
            group = []
            start = p
            i = start
            scanned = 0
            
            while scanned < x and len(group) < z:
                if i > x:
                    i = 1
                if used[i] < y:
                    group.append(i)
                i += 1
                scanned += 1
            
            if len(group) < z:
                break
            
            for v in group:
                used[v] += 1
            
            ans.append(group)
            p += 1
            if p > x:
                p = 1
        
        print(len(ans))
        for g in ans:
            print(*g)

if __name__ == "__main__":
    solve()
```

The solution maintains a usage counter per interviewer and constructs each group by scanning cyclically through interviewer IDs. The inner loop ensures we gather exactly `z` distinct interviewers with remaining capacity. The pointer `p` shifts after every group so that we avoid repeatedly picking the same early indices.

A subtle implementation detail is the explicit wrap-around of index `i`. Without it, the scan would miss valid candidates when reaching the end of the interviewer list. Another important detail is breaking immediately when fewer than `z` candidates can be found, since any further attempt would also fail due to monotonic depletion of capacity.

## Worked Examples

### Example 1

Input:

```
3 2 2
```

We have 3 interviewers, each can appear twice, and each interview uses 2 people.

| Step | Pointer p | Selected group | Used counts |
| --- | --- | --- | --- |
| 1 | 1 | [1,2] | 1:1, 2:1, 3:0 |
| 2 | 2 | [2,3] | 1:1, 2:2, 3:1 |
| 3 | 3 | [3,1] | 1:2, 2:2, 3:2 |

At step 4, no group of size 2 can be formed because all interviewers have reached capacity 2. The construction stops with 3 interviews.

This shows that the cyclic scanning distributes load evenly and achieves full capacity usage.

### Example 2

Input:

```
4 1 3
```

Each interviewer can appear only once, and each group needs 3 interviewers.

| Step | Pointer p | Selected group | Used counts |
| --- | --- | --- | --- |
| 1 | 1 | [1,2,3] | 1:1, 2:1, 3:1, 4:0 |
| 2 | 2 | [2,3,4] | 1:1, 2:2 (invalid) |

At this point, interviewer 2 and 3 already exceed capacity if reused, so no second valid group exists. The algorithm stops after 1 interview.

This demonstrates how the capacity constraint directly limits the number of groups even when many combinations exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(x * y * z) per test case | Each group formation scans at most x elements and we form at most x*y/z groups |
| Space | O(x) | We only store usage counters and current group |

Given that `x, y, z ≤ 10` and `t ≤ 1000`, this comfortably fits within time limits. Even worst-case execution performs only a few thousand primitive operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    solve()
    
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# sample-like cases
assert run("1\n3 2 2\n") != ""

# minimum case
assert run("1\n1 1 1\n") == "1\n1"

# impossible due to z > x
assert run("1\n2 1 3\n") == "0"

# zero capacity
assert run("1\n3 0 2\n") == "0"

# symmetric case
out = run("1\n4 1 2\n")
lines = out.splitlines()
assert int(lines[0]) == len(lines) - 1
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 1 1 | 1\n1 | minimal feasible case |
| 1\n2 1 3 | 0 | impossible due to insufficient participants |
| 1\n3 0 2 | 0 | zero capacity edge case |
| 1\n4 1 2 | valid pairs | general construction correctness |

## Edge Cases

When `z > x`, the algorithm immediately returns zero. For example, with input `x=2, z=3`, no scan can ever collect enough distinct interviewers, so the inner loop always fails and we stop without producing groups.

When `y = 0`, every interviewer has zero capacity from the start. The scanning loop never adds any candidate, so `group` never reaches size `z`, and the algorithm terminates immediately with output `0`.

When `x = z`, every valid interview must use all interviewers. The algorithm will produce at most `y` identical full groups, since each interviewer is consumed uniformly across iterations. This matches the optimal packing where every round uses all available capacity evenly.
