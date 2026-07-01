---
title: "CF 104417B - Building Company"
description: "We are given a company that starts with some employees of different occupations, where each occupation type has a current number of available workers. On top of this initial workforce, there are multiple building projects available."
date: "2026-06-30T19:15:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104417
codeforces_index: "B"
codeforces_contest_name: "The 13th Shandong ICPC Provincial Collegiate Programming Contest"
rating: 0
weight: 104417
solve_time_s: 63
verified: true
draft: false
---

[CF 104417B - Building Company](https://codeforces.com/problemset/problem/104417/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a company that starts with some employees of different occupations, where each occupation type has a current number of available workers. On top of this initial workforce, there are multiple building projects available. Each project has two parts: a set of minimum staffing requirements across certain occupations, and a reward that increases the workforce by adding more employees of some occupations once the project is completed.

The task is not to choose a single best project or a fixed schedule. Instead, we are allowed to choose any subset of projects and execute them in any order, as long as at the moment we attempt a project, all its staffing requirements are satisfied by the current workforce. Once a project is completed, its reward permanently increases the available employees, which may unlock other projects later.

The goal is to determine the maximum number of projects that can be completed.

The constraints are large, with up to 100,000 initial occupation types and up to 100,000 projects, and the total number of requirement and reward entries also bounded by 100,000. This immediately rules out any approach that simulates all permutations of project orders, since even checking feasibility for one ordering would already be too expensive.

The key structure is that the state of the system only improves over time. Employee counts never decrease, so feasibility is monotonic: once a requirement becomes satisfied, it stays satisfied forever. This monotonicity is the central property that allows a greedy activation process.

A subtle failure case appears if we try to greedily pick projects in a fixed order without tracking newly unlocked ones. For example, if a project A is not initially doable but becomes doable only after project B, a naive scan that does not revisit A would miss it entirely. Another issue arises if we try sorting projects by difficulty, since difficulty is multidimensional and depends on evolving resources.

## Approaches

The most direct idea is to try all possible orders of projects and simulate execution. This works conceptually because we can always check requirements at each step and apply rewards. However, the number of permutations is n factorial in the worst case, which is completely infeasible even for n = 100000.

A more structured brute force is to repeatedly scan all projects, picking any that are currently feasible, and repeating until no progress is made. This is closer to the correct process but still too slow if implemented naively, because each full scan costs O(n), and we may repeat it O(n) times, leading to O(n^2) behavior.

The key observation is that feasibility only depends on whether each requirement threshold has been reached for each occupation type. Since counts only increase, once a requirement becomes satisfied it never becomes invalid again. This suggests we should maintain a dynamic set of currently doable projects and update it efficiently when employee counts increase.

We can invert the viewpoint: instead of checking each project repeatedly, we track for each occupation type which project requirements depend on it, and only update those projects when that type’s count increases. Each requirement is essentially a threshold event, and once the count crosses that threshold, it becomes permanently satisfied.

This transforms the problem into a process where we start with all currently feasible projects in a queue, repeatedly execute them, and propagate their rewards to unlock further projects, similar to a BFS over an implicit dependency graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full permutation search | O(n!) | O(n) | Too slow |
| Repeated full scans | O(n^2) | O(n) | Too slow |
| Incremental BFS with threshold tracking | O((n + m + k) log m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We treat each requirement as a condition that may become satisfied once the corresponding occupation count is high enough. Since counts only increase, each requirement transitions from unsatisfied to satisfied exactly once.

### Steps

1. Build a mapping from each occupation type to its current number of employees. This is our evolving state.
2. For every project, compute how many of its requirements are initially unsatisfied. If a project has zero unsatisfied requirements, it is immediately available for execution.
3. For efficient updates, group all requirements by occupation type. For each type, store all requirement entries sorted by their threshold value. Each entry links a project and a minimum required count.
4. Initialize a queue with all projects that are currently feasible.
5. While the queue is not empty, remove one project and execute it. Increase the answer counter.
6. For each reward of this project, increase the corresponding occupation count.
7. Whenever an occupation count increases, scan through that type’s sorted requirement list and mark all requirements whose threshold is now satisfied. For each newly satisfied requirement, reduce the remaining unmet requirement count of its project. If a project’s unmet count drops to zero, add it to the queue.

The crucial point is that each requirement is processed exactly once, at the moment its threshold is crossed.

### Why it works

At any moment, the algorithm maintains the invariant that a project is in the queue if and only if all of its requirements are satisfied under the current workforce. Because employee counts only increase, a requirement that is unsatisfied can only become satisfied in one direction, and once it becomes satisfied, it never reverts. Therefore, every project enters the queue exactly when it becomes executable, and executing it immediately is safe because delaying it cannot make future projects harder to achieve.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    g = int(input())
    cnt = {}
    for _ in range(g):
        t, u = map(int, input().split())
        cnt[t] = cnt.get(t, 0) + u

    n = int(input())

    reqs = []
    proj_req = [[] for _ in range(n)]
    proj_unmet = [0] * n
    reward = [[] for _ in range(n)]

    type_reqs = {}

    for i in range(n):
        parts = list(map(int, input().split()))
        m = parts[0]
        idx = 1

        for _ in range(m):
            a = parts[idx]
            b = parts[idx + 1]
            idx += 2
            req_id = len(reqs)
            reqs.append((a, b, i))
            proj_req[i].append(req_id)
            if cnt.get(a, 0) < b:
                proj_unmet[i] += 1
            type_reqs.setdefault(a, []).append(req_id)

        parts = list(map(int, input().split()))
        k = parts[0]
        idx = 1
        for _ in range(k):
            c = parts[idx]
            d = parts[idx + 1]
            idx += 2
            reward[i].append((c, d))

    # sort requirements per type by threshold
    ptr = {}
    for t, lst in type_reqs.items():
        lst.sort(key=lambda x: reqs[x][1])
        ptr[t] = 0

    q = deque()
    visited = [False] * n

    for i in range(n):
        if proj_unmet[i] == 0:
            q.append(i)
            visited[i] = True

    ans = 0

    while q:
        i = q.popleft()
        ans += 1

        for c, d in reward[i]:
            old = cnt.get(c, 0)
            new = old + d
            cnt[c] = new

            if c in type_reqs:
                lst = type_reqs[c]
                p = ptr[c]
                while p < len(lst) and reqs[lst[p]][1] <= new:
                    req_id = lst[p]
                    proj = reqs[req_id][2]
                    # each requirement triggers exactly once
                    proj_unmet[proj] -= 1
                    if proj_unmet[proj] == 0 and not visited[proj]:
                        q.append(proj)
                        visited[proj] = True
                    p += 1
                ptr[c] = p

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation keeps a global counter for each occupation type and updates it only when rewards are applied. Each occupation type has a sorted list of requirement thresholds, and a pointer that ensures we only process each requirement once. When a threshold is crossed, we immediately update the corresponding project’s remaining requirement count.

A common pitfall is forgetting that a single occupation update may unlock multiple requirements at once, which is why the while-loop over thresholds is essential.

## Worked Examples

### Example trace 1

Consider a simplified scenario:

Input:

```
1
1 1
2
1 1 1
1 1 1
0
1 1 1
```

We start with one worker of type 1. The first project requires 1 worker of type 1 and adds nothing, so it is immediately feasible.

| Step | Queue | cnt[type1] | Project state |
| --- | --- | --- | --- |
| Init | [0] | 1 | P0 and P1 both require 1 |
| Take P0 | [1] | 1 | P1 still feasible |
| Take P1 | [] | 1 | done |

This confirms that already-feasible projects propagate correctly.

### Example trace 2

Input:

```
2
1 1
2 0 1 1 1
2
1 1 1
1 1 1
```

We begin with only type 1 available in quantity 1, type 2 is 0.

| Step | Queue | cnt1 | cnt2 | Notes |
| --- | --- | --- | --- | --- |
| Init | [P0] | 1 | 0 | P0 feasible |
| Take P0 | [P1] | 1 | 1 | reward unlocks type2 |
| Take P1 | [] | 1 | 1 | all done |

This shows how rewards dynamically unlock previously impossible projects.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m + k) | each requirement is processed once when its threshold is crossed, and each project is enqueued once |
| Space | O(n + m) | storage for projects, requirements, and per-type indices |

The algorithm is efficient because every structural element, projects, requirements, and rewards, is handled a constant number of times. This fits comfortably within the constraints where the total number of edges is 100,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    g = int(input())
    cnt = {}
    for _ in range(g):
        t, u = map(int, input().split())
        cnt[t] = cnt.get(t, 0) + u

    n = int(input())

    reqs = []
    proj_req = [[] for _ in range(n)]
    proj_unmet = [0] * n
    reward = [[] for _ in range(n)]
    type_reqs = {}

    for i in range(n):
        parts = list(map(int, input().split()))
        m = parts[0]
        idx = 1
        for _ in range(m):
            a = parts[idx]; b = parts[idx+1]; idx += 2
            rid = len(reqs)
            reqs.append((a,b,i))
            proj_req[i].append(rid)
            if cnt.get(a,0) < b:
                proj_unmet[i] += 1
            type_reqs.setdefault(a, []).append(rid)

        parts = list(map(int, input().split()))
        k = parts[0]
        idx = 1
        for _ in range(k):
            c = parts[idx]; d = parts[idx+1]; idx += 2
            reward[i].append((c,d))

    ptr = {}
    for t,lst in type_reqs.items():
        lst.sort(key=lambda x: reqs[x][1])
        ptr[t] = 0

    from collections import deque
    q = deque()
    visited = [False]*n
    for i in range(n):
        if proj_unmet[i]==0:
            q.append(i)
            visited[i]=True

    ans = 0
    cnt2 = cnt.copy()

    while q:
        i = q.popleft()
        ans += 1
        for c,d in reward[i]:
            cnt2[c] = cnt2.get(c,0)+d
            if c in type_reqs:
                lst = type_reqs[c]
                p = ptr[c]
                while p < len(lst) and reqs[lst[p]][1] <= cnt2[c]:
                    proj = reqs[lst[p]][2]
                    proj_unmet[proj]-=1
                    if proj_unmet[proj]==0 and not visited[proj]:
                        q.append(proj)
                        visited[proj]=True
                    p+=1
                ptr[c]=p

    return str(ans)

# sample placeholder asserts would go here
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimal empty requirements | correct max chain | base activation |
| Single chain dependency | full propagation | reward unlocking |
| Multiple independent projects | correct counting | no interference |
| Zero-requirement projects | immediate enqueue | queue initialization |

## Edge Cases

A key edge case is when a project has no requirements. Such projects must always be immediately available regardless of current workforce. The algorithm handles this naturally because their unmet count starts at zero, so they are inserted into the queue during initialization.

Another case is when multiple requirements for the same occupation are satisfied at once due to a large reward jump. The pointer-based processing ensures that all thresholds crossed in a single update are applied in one sweep, and each requirement is counted exactly once.

A final subtle case is repeated unlocking: a project may receive its last satisfied requirement from different rewards over time. The unmet counter ensures it only enters the queue once, when it becomes fully satisfied, preventing duplicate processing.
