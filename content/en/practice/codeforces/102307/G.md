---
title: "CF 102307G - Graduation"
description: "Each course is a vertex in a directed graph. If a[i] = j, then course i must be completed before course j. A course with a[i] = 0 has no course after it in this prerequisite relation."
date: "2026-08-13T07:19:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102307
codeforces_index: "G"
codeforces_contest_name: "2019 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102307
solve_time_s: 111
verified: true
draft: false
---

[CF 102307G - Graduation](https://codeforces.com/problemset/problem/102307/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

Each course is a vertex in a directed graph. If `a[i] = j`, then course `i` must be completed before course `j`. A course with `a[i] = 0` has no course after it in this prerequisite relation.

The crucial structural restriction is that every course can be a prerequisite for at most one other course. In graph terms, every vertex has outdegree at most one. Since graduation is guaranteed to be possible, the relevant graph contains no directed cycle. The graph is consequently a collection of trees whose edges point toward their final course.

A semester can contain at most `k` courses, and every course placed in a semester must have all of its prerequisites completed in earlier semesters. The task is to minimize the number of semesters needed to complete all `n` courses.

The value of `n` can reach `10^4`, while `k` is at most `10`. This immediately rules out subset dynamic programming over all courses, because `2^10000` states is far beyond anything that can run in one second. The small value of `k` is useful for describing possible semester choices, but it does not make brute force practical because there can still be an enormous number of available courses.

There are several edge cases that can make a straightforward topological sort give the wrong answer. First, simply taking arbitrary available courses is not optimal. Consider

```
5 2
2 3 0 0 0
```

Courses `1 -> 2 -> 3` form a chain, while courses `4` and `5` are independent. The answer is `3`: take courses `1,4`, then `2,5`, then `3`. A careless algorithm could take `4,5` first and would then need four semesters.

Second, having enough capacity to take every currently available course does not mean that newly unlocked courses can be taken immediately. For

```
4 2
3 3 4 0
```

courses `1` and `2` unlock course `3`, which then unlocks course `4`. The answer is `3`, not `2`. Courses completed during a semester cannot satisfy a prerequisite until the next semester.

Finally, a course with no successor is not necessarily available initially. For

```
3 3
0 1 2
```

the edges are `3 -> 2 -> 1`. Although course `1` is the final course, it cannot be taken until courses `3` and `2` have been completed. The answer is `3`, even though `k = 3`.

## Approaches

A natural brute-force solution would represent the set of already completed courses and recursively try every legal choice of up to `k` currently available courses for the next semester. This is correct because every possible valid schedule appears somewhere in the search tree, so taking the minimum over all schedules gives the optimum.

The problem is the number of states. A subset DP already has `2^n` possible sets of completed courses. For `n = 10000`, that means `2^10000` states. If we also enumerate the possible groups of courses to take in a semester, the first state alone can have

[
\sum_{j=1}^{10} {10000 \choose j}
]

possible choices, with the largest term `C(10000,10)` approximately `2.76 * 10^33`. The brute-force approach is not merely a little too slow, its state space is fundamentally exponential.

The graph restriction gives us a much stronger way to reason about the schedule. Every course has at most one successor, so from any course there is a unique path toward a final course. Define the level of a course as the length of the longest path starting from that course and following prerequisites toward its final course. A final course has level `0`, its immediate prerequisites have level `1`, and so on.

Suppose two courses are currently available. If one has a larger level, completing it is more urgent because there is a longer chain of courses that still has to follow it. Spending a semester on a level `0` independent course while leaving a level `5` course untouched can delay an entire critical chain.

This leads to the highest-level-first greedy algorithm. At the beginning of every semester, among all currently available courses, take the at most `k` courses with the largest levels. After the whole semester finishes, remove those courses from the graph and add every course that has now lost all prerequisites.

This is the classical highest-level-first algorithm for unit-time scheduling on an in-tree, which is exactly the structure obtained here because every course has at most one successor. The algorithm is known to produce a minimum-makespan schedule for this special precedence structure.

The brute-force works because it explicitly considers every possible schedule, but fails when the number of schedules becomes exponential. The observation that the prerequisite graph is an in-tree forest lets us assign every course a critical-path level and replace schedule enumeration with a priority queue.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential, at least `O(2^n)` states | `O(2^n)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read the successor `a[i]` of every course and compute the number of prerequisites of every course. For course `v`, this is the number of courses `u` satisfying `a[u] = v`. A course with prerequisite count zero is available at the start.
2. Compute the level of every course. Start with all courses that have no prerequisites, because they are the leaves of the prerequisite trees. Give each such course level `0`, then process them in topological order. When a course `u` points to `v`, update `v` with `level[u] + 1`. Since `v` becomes available only after all its prerequisites have been processed, the maximum such value is exactly the length of the longest path from `v` to a final course.
3. Restore the original prerequisite counts. The first topological pass was only for calculating levels, while the second pass will represent the actual semester schedule.
4. Put every initially available course into a max-priority queue, using its level as the priority. Python's `heapq` is a min-heap, so store `-level` instead.
5. At the beginning of each semester, remove at most `k` courses from the priority queue and put them into a separate batch. The separation matters because courses unlocked by this batch cannot be taken during the same semester.
6. After the batch has been chosen, mark all its courses as completed. For every completed course `u`, look at its unique successor `v`. Decrease `v`'s remaining prerequisite count. If it becomes zero, insert `v` into the priority queue with its level.
7. Increment the semester count and repeat until all courses have been completed. The number of iterations is the minimum number of semesters.

### Why it works

The key invariant is that the priority queue always contains exactly the courses that are legally available at the beginning of the current semester, ordered by the length of the remaining critical path.

For this graph structure, a course with a larger level lies at the head of a longer chain that must still be completed. Highest-level-first scheduling fills each semester with the courses whose postponement has the greatest potential to extend the final completion time. Because every course has at most one successor and every course takes exactly one semester of work, the precedence constraints form an in-tree forest, the exact setting where highest-level-first scheduling is optimal. Thus every greedy semester can be chosen without increasing the minimum possible finishing time, and after all courses are processed the resulting semester count is optimal.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve(stream):
    data = list(map(int, stream.read().split()))
    if not data:
        return ""

    it = iter(data)
    n = next(it)
    k = next(it)

    nxt = [next(it) - 1 for _ in range(n)]

    # indeg[v] = number of prerequisites of v.
    indeg = [0] * n
    for v in nxt:
        if v != -1:
            indeg[v] += 1

    # First topological pass: calculate the level of every course.
    # level[u] is the length of the longest path from u to a terminal course.
    rem = indeg[:]
    level = [0] * n
    q = []

    for u in range(n):
        if rem[u] == 0:
            q.append(u)

    head = 0
    while head < len(q):
        u = q[head]
        head += 1

        v = nxt[u]
        if v != -1:
            level[v] = max(level[v], level[u] + 1)
            rem[v] -= 1
            if rem[v] == 0:
                q.append(v)

    # Second pass: actually construct the optimal schedule.
    rem = indeg[:]

    pq = []
    for u in range(n):
        if rem[u] == 0:
            heapq.heappush(pq, (-level[u], u))

    completed = 0
    semesters = 0

    while completed < n:
        batch = []

        # Choose the courses for this semester before releasing
        # anything unlocked by them.
        take = min(k, len(pq))
        for _ in range(take):
            _, u = heapq.heappop(pq)
            batch.append(u)

        # Complete the whole batch simultaneously.
        for u in batch:
            completed += 1

        # Only now can successors become available.
        for u in batch:
            v = nxt[u]
            if v != -1:
                rem[v] -= 1
                if rem[v] == 0:
                    heapq.heappush(pq, (-level[v], v))

        semesters += 1

    return str(semesters)

def main():
    print(solve(sys.stdin))

if __name__ == "__main__":
    main()
```

The first part of `solve` reads the successor array and builds `indeg`. Since each course has at most one successor, there is no adjacency list to maintain. The single value `nxt[u]` is enough to find the only course that can be unlocked when `u` is completed.

The first topological pass uses a copy called `rem`. Every initial leaf has `rem[u] == 0`, so it can start the traversal. When `u` is processed, its successor `v` gets a candidate level of `level[u] + 1`. Taking the maximum is necessary because a course may have many prerequisites, and its level must account for the longest of their chains.

The second pass copies `indeg` again because the first pass consumed the prerequisite counts. Reusing the modified array would make every course appear available too early.

The priority queue stores `(-level[u], u)`. Negating the level turns Python's min-heap into the required max-heap. The course number is used only as a deterministic tie breaker and has no effect on correctness.

The `batch` array is a subtle but necessary detail. We first remove all courses for the current semester, then process their successors. If successors were inserted into the heap immediately after each removal and the heap were allowed to supply another course in the same iteration, a course could be taken in the same semester as its prerequisite. The separate batch prevents that off-by-one error.

No integer overflow is possible in Python, and the maximum level is at most `n - 1`. The heap contains at most `n` entries, so its memory usage remains linear.

## Worked Examples

### Sample 1

The input is

```
4 2
3 3 4 0
```

The edges are `1 -> 3`, `2 -> 3`, and `3 -> 4`. The levels are `level[1] = 2`, `level[2] = 2`, `level[3] = 1`, and `level[4] = 0`.

| Semester | Available before semester | Levels | Courses taken | Newly available |
| --- | --- | --- | --- | --- |
| 1 | `1, 2` | `2, 2` | `1, 2` | `3` |
| 2 | `3` | `1` | `3` | `4` |
| 3 | `4` | `0` | `4` | none |

The first semester consumes both courses on the critical level `2`. After they are completed, course `3` becomes available. Course `4` cannot join the second semester because course `3` is completed during that semester. The answer is `3`.

### Sample 2

The input is

```
3 3
0 1 2
```

The graph is the single chain `3 -> 2 -> 1`. Its levels are `2`, `1`, and `0`.

| Semester | Available before semester | Levels | Courses taken | Newly available |
| --- | --- | --- | --- | --- |
| 1 | `3` | `2` | `3` | `2` |
| 2 | `2` | `1` | `2` | `1` |
| 3 | `1` | `0` | `1` | none |

Although the capacity is three courses per semester, the precedence chain permits only one course at each stage. The answer is `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Each course enters and leaves the priority queue at most once, and every edge is processed a constant number of times |
| Space | `O(n)` | The successor array, prerequisite counts, levels, topological queue, and priority queue are all linear |

There are only `n` prerequisite relations because every course has at most one successor. With `n <= 10000`, `O(n log n)` performs only a small number of heap operations and fits comfortably within the one-second limit. The linear auxiliary storage is also far below the 256 MB memory limit.

## Test Cases

```python
import sys
import io
import heapq

input = sys.stdin.readline

def solve(stream):
    data = list(map(int, stream.read().split()))
    if not data:
        return ""

    it = iter(data)
    n = next(it)
    k = next(it)
    nxt = [next(it) - 1 for _ in range(n)]

    indeg = [0] * n
    for v in nxt:
        if v != -1:
            indeg[v] += 1

    rem = indeg[:]
    level = [0] * n
    q = []

    for u in range(n):
        if rem[u] == 0:
            q.append(u)

    head = 0
    while head < len(q):
        u = q[head]
        head += 1

        v = nxt[u]
        if v != -1:
            level[v] = max(level[v], level[u] + 1)
            rem[v] -= 1
            if rem[v] == 0:
                q.append(v)

    rem = indeg[:]
    pq = []

    for u in range(n):
        if rem[u] == 0:
            heapq.heappush(pq, (-level[u], u))

    completed = 0
    semesters = 0

    while completed < n:
        batch = []

        for _ in range(min(k, len(pq))):
            _, u = heapq.heappop(pq)
            batch.append(u)

        completed += len(batch)

        for u in batch:
            v = nxt[u]
            if v != -1:
                rem[v] -= 1

        for u in batch:
            v = nxt[u]
            if v != -1 and rem[v] == 0:
                heapq.heappush(pq, (-level[v], v))

        semesters += 1

    return str(semesters)

def run(inp: str) -> str:
    return solve(io.StringIO(inp)).strip()

# Provided samples
assert run("4 2\n3 3 4 0\n") == "3", "sample 1"
assert run("3 3\n0 1 2\n") == "3", "sample 2"

# Minimum-size input
assert run("1 1\n0\n") == "1", "single course"

# Maximum-size input, all values equal to zero
assert run("10000 10\n" + " ".join(["0"] * 10000) + "\n") == "1000", \
    "10000 independent courses with capacity 10"

# Capacity is large enough for all courses, but precedence still forces a chain
assert run("4 4\n2 3 4 0\n") == "4", \
    "large semester capacity cannot bypass prerequisites"

# Taking arbitrary available courses first would be suboptimal
assert run("5 2\n2 3 0 0 0\n") == "3", \
    "highest-level priority is necessary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0` | `1` | Minimum-size instance |
| `10000 10 / all zeros` | `1000` | Maximum `n`, maximum batching, and all-equal successor values |
| `4 4 / 2 3 4 0` | `4` | Precedence dominates capacity and catches same-semester unlocking errors |
| `5 2 / 2 3 0 0 0` | `3` | Shows why arbitrary topological scheduling is not optimal |

## Edge Cases

For the single-course case

```
1 1
0
```

the only course has prerequisite count zero and level zero. It enters the priority queue immediately, is selected in the first batch, and the completed count becomes one. The loop stops after one semester, producing `1`.

For the case where every course is independent,

```
6 2
0 0 0 0 0 0
```

all six courses have level zero and are initially available. The priority queue contains all six courses, and the algorithm takes two at a time. The batches contain two, two, and two courses, so the answer is `3`. This is exactly `ceil(6 / 2)`.

For a large capacity with a long chain,

```
4 4
2 3 4 0
```

all four courses could theoretically fit into one semester, but only course `1` is initially available. After semester one, course `2` becomes available, followed by course `3`, and finally course `4`. The algorithm produces four semesters because precedence constraints are checked before every batch.

The most revealing case is

```
5 2
2 3 0 0 0
```

Initially, courses `1`, `4`, and `5` are available. Their levels are `2`, `0`, and `0`. The priority queue chooses `1` together with one independent course, then chooses `2` together with the remaining independent course, and finally chooses `3`. The result is three semesters. If the implementation simply consumed available courses in queue order, it could choose `4` and `5` first and obtain four semesters, which is why the level priority is essential.

Finally, newly unlocked courses must wait for the next semester. In

```
4 2
3 3 4 0
```

courses `1` and `2` are taken in semester one. Only after that entire semester finishes does course `3` enter the available set. Course `4` is released after semester two, so it must be taken in semester three. The batch-based implementation handles this correctly because successor updates happen only after all courses for the current semester have already been selected.
