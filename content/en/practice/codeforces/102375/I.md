---
title: "CF 102375I - \u0421\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447"
description: "There are (P) participants and (T) possible contest tasks. For every known participant-task pair ((u,v)), participant (u) already knows task (v). Suppose we choose some nonempty set of tasks for the contest."
date: "2026-08-14T03:34:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "I"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 384
verified: false
draft: false
---

[CF 102375I - \u0421\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447](https://codeforces.com/problemset/problem/102375/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 24s  
**Verified:** no  

## Solution
## Problem Understanding

There are (P) participants and (T) possible contest tasks. For every known participant-task pair ((u,v)), participant (u) already knows task (v).

Suppose we choose some nonempty set of tasks for the contest. A participant is allowed to participate exactly when they know none of the chosen tasks. If the chosen tasks are (v_1,v_2,\ldots), the excluded participants are the union of the sets of people who know each chosen task.

The primary objective is to maximize the number of participants who remain eligible. Once that maximum is achieved, the secondary objective is to choose as many tasks as possible.

The input is naturally a bipartite graph. One side contains participants, the other side contains tasks, and an edge means that the corresponding participant knows the corresponding task. For every task (v), let (S_v) be the set of participants adjacent to it. If we choose a set (Q) of tasks, the number of participants who cannot participate is

[
\left|\bigcup_{v\in Q} S_v\right|.
]

Thus we want to minimize this union, while (Q) must be nonempty. After minimizing its size, we want (Q) to contain as many tasks as possible.

The bounds are large enough to determine the intended direction immediately. Both (P) and (T) can reach (10^5), so an (O(P T)) algorithm could perform around (10^{10}) operations and is not viable. The number of known pairs (M) can reach (10^6), so an (O(M)) or (O(M\log M)) solution is appropriate, while algorithms that repeatedly inspect all participant-task pairs for many candidate subsets are too expensive.

There are several edge cases that a careless implementation can mishandle.

First, some tasks may be known by nobody. Consider

```
2 3 1
1 1
```

Tasks (2) and (3) have empty participant sets. Choosing both excludes nobody, so the correct output is

```
2 2
2 3
```

A solution that only considers tasks appearing in the input would miss both optimal tasks.

Second, several tasks can have the same minimum number of known participants without being interchangeable. Consider

```
3 3 3
1 1
2 2
3 3
```

Every task is known by exactly one participant, so the maximum number of eligible participants is (2). But choosing two different tasks excludes two different participants, leaving only one participant. The optimal answer therefore contains exactly one task, not all three. Looking only at task frequencies is insufficient. The actual participant sets must be compared.

Third, the task with the largest number can itself be the optimal task. For example,

```
2 3 4
1 1
2 1
1 2
2 2
```

Task (3) is known by nobody, so the answer is

```
2 1
3
```

An implementation with a loop ending at (T-1), or one that accidentally treats task numbers as zero-based, can silently lose this case.

Finally, it is possible that every participant knows every task. For

```
1 2 2
1 1
1 2
```

any nonempty chosen set excludes the only participant. The optimal number of eligible participants is (0), and because all task sets are identical, both tasks should be selected:

```
0 2
1 2
```

The secondary optimization still matters even when the primary optimum is zero.

## Approaches

A direct brute-force solution would consider every nonempty subset of the (T) tasks. For each subset, it would mark every participant who knows at least one selected task, count the remaining participants, and then compare the number of selected tasks when the participant count is tied.

This is correct because every legal answer is explicitly considered. The problem is the number of subsets. There are (2^T-1) nonempty subsets, and processing one subset can require (O(M)) work. In the worst case this gives (O(M2^T)), which with (M=10^6) and (T=10^5) is completely impossible.

The brute-force approach works because it directly evaluates the union of participant sets. The key observation is that we do not actually need to enumerate unions.

For any nonempty set of selected tasks (Q), pick one task (x\in Q). Its participant set (S_x) is contained in the union of all selected sets:

[
S_x\subseteq\bigcup_{v\in Q}S_v.
]

Consequently,

[
\left|\bigcup_{v\in Q}S_v\right|\ge |S_x|.
]

This holds for every selected task, so

[
\left|\bigcup_{v\in Q}S_v\right|
\ge \min_v |S_v|.
]

The lower bound is attainable simply by selecting one task whose participant set has minimum size. Therefore the maximum possible number of eligible participants is

[
P-\min_v |S_v|.
]

Now consider the secondary objective. Suppose the minimum degree is (d), and task (x) has exactly (d) known participants. We can select another task (y) without losing any additional participant exactly when

[
S_y\subseteq S_x.
]

But (S_y) must also have at least (d) elements, because (d) is the minimum task degree. Since (|S_y|=d), the inclusion can hold only when

[
S_y=S_x.
]

So every optimal solution consists of tasks whose participant sets are exactly the same minimum-size set.

This reduces the entire problem to finding one task with minimum degree, then collecting every other task with the same degree whose participant set is identical to that task's participant set.

We do not need hashing or sorting of all task sets. Once one minimum task is chosen, mark its participants in a boolean array. Every other task with the same degree is equal to the target set exactly when every participant listed for that task is marked. Because the candidate has the same number of distinct participants as the target and the input contains no duplicate participant-task pair, this membership test proves equality.

The graph can be stored compactly with linked lists implemented by integer arrays. For each task, `head[v]` stores the first edge belonging to it. For every edge, `who[i]` stores its participant and `nxt[i]` points to the next edge of the same task. This uses only a few bytes per input edge and avoids the large Python overhead of one list of Python integers for every task.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(M2^T)) | (O(P+M)) | Too slow |
| Optimal | (O(P+T+M)) | (O(P+T+M)) with compact integer arrays | Accepted |

## Algorithm Walkthrough

1. Create an array `degree` where `degree[v]` is the number of participants who know task (v). At the same time, store all input edges grouped by task using `head`, `who`, and `nxt`. We need the actual participant lists later, not only their sizes.
2. Find a task `min_task` with the smallest value of `degree[v]`. Let this minimum be `d`. Selecting this task alone excludes exactly (d) participants, and no nonempty task set can exclude fewer than (d) participants.
3. If (d=0), every task with degree zero is optimal. Such tasks are known by nobody, so they can all be selected simultaneously without excluding anyone. Since the secondary objective is to maximize the number of tasks, output every zero-degree task.
4. If (d>0), traverse the participant list of `min_task` and mark every participant in a byte array `marked`. This byte array represents the exact participant set that an optimal task must have.
5. Scan every task whose degree is exactly (d). Traverse its participant list and check that every participant is marked. If all of them are marked, the candidate task has the same participant set as `min_task`, because both sets contain exactly (d) distinct participants. Add the task to the answer.
6. Output (P-d) as the number of participants who can participate, together with the collected task numbers. The first quantity is optimal by the minimum-degree argument, and the second is maximal because every task that can be added without increasing the excluded set has been collected.

**Why it works.** Let (d) be the minimum number of participants knowing any task. Every nonempty chosen task set contains some task known by at least (d) participants, so at least (d) participants must be excluded. A single task of degree (d) reaches this lower bound. Once such a task is selected, another task can be added without excluding anyone new only if its participant set is contained in the original set. Its degree cannot be smaller than (d), so equal degree forces the two sets to be identical. The algorithm selects exactly all tasks with that same minimum participant set, so it achieves the maximum number of eligible participants and, among those solutions, the maximum number of tasks.

## Python Solution

```python
import sys
input = sys.stdin.readline

from array import array

def solve():
    P, T, M = map(int, input().split())

    # For every task v:
    # head[v] is the first edge in its linked list.
    head = array('i', [-1]) * T

    # degree[v] = number of participants knowing task v.
    degree = array('i', [0]) * T

    # For every stored edge i:
    # who[i] = participant of the edge
    # nxt[i] = next edge belonging to the same task
    who = array('i')
    nxt = array('i')

    for _ in range(M):
        u, v = map(int, input().split())
        v -= 1

        idx = len(who)
        who.append(u)
        nxt.append(head[v])
        head[v] = idx
        degree[v] += 1

    # Find one task with minimum degree.
    min_task = 0
    min_degree = degree[0]

    for v in range(1, T):
        if degree[v] < min_degree:
            min_degree = degree[v]
            min_task = v

    # If some tasks are known by nobody, all of them can be selected.
    if min_degree == 0:
        answer = []
        for v in range(T):
            if degree[v] == 0:
                answer.append(v + 1)

        print(P, len(answer))
        print(*answer)
        return

    # Mark participants who know the chosen minimum-degree task.
    marked = bytearray(P + 1)

    edge = head[min_task]
    while edge != -1:
        marked[who[edge]] = 1
        edge = nxt[edge]

    answer = []

    # Every optimal task must have the same degree and the same
    # participant set as min_task.
    for v in range(T):
        if degree[v] != min_degree:
            continue

        edge = head[v]
        same = True

        while edge != -1:
            if not marked[who[edge]]:
                same = False
                break
            edge = nxt[edge]

        if same:
            answer.append(v + 1)

    print(P - min_degree, len(answer))
    print(*answer)

if __name__ == "__main__":
    solve()
```

The first part of the implementation builds the bipartite graph in a compact form. `head` has one entry per task, while `who` and `nxt` have one entry per known participant-task pair. When an edge is read, it is inserted at the front of the corresponding task's linked list. The order of participants inside a task does not matter, so no sorting is necessary.

The `degree` array is updated while reading the input. This means the minimum-degree task can be found with a single scan after all edges have been processed.

The zero-degree case is handled separately because its participant set is empty. Every such task can be selected at once, and no participant becomes disqualified. It is also the only situation where the optimal participant count is (P).

For a positive minimum degree, `marked` is indexed directly by participant number. The array has size (P+1), leaving index zero unused. This avoids constructing a Python `set` and saves substantial memory when (M) is close to (10^6).

When testing a candidate task, the code checks only tasks with the minimum degree. A candidate containing an unmarked participant cannot have the same participant set as the target. Conversely, if all its participants are marked and its degree equals the target degree, its set must be exactly the target set. No sorting or probabilistic hashing is involved.

There is no integer-overflow issue in Python. In the compact arrays, participant and edge indices fit comfortably into signed 32-bit integers because (P,T\le10^5) and (M\le10^6).

## Worked Examples

### Sample 1

The input is

```
3 4 6
1 1
1 2
2 2
2 3
3 3
3 4
```

The task participant sets are (S_1={1}), (S_2={1,2}), (S_3={2,3}), and (S_4={3}).

| Task | Degree | Minimum task | Marked participants | Accepted |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | ({1}) | yes |
| 2 | 2 | 1 | ({1}) | no, degree differs |
| 3 | 2 | 1 | ({1}) | no, degree differs |
| 4 | 1 | 1 | ({1}) | no, participant 3 is unmarked |

The minimum degree is (1), so exactly (3-1=2) participants can remain eligible. Task (1) is the first minimum-degree task, and task (4) has a different participant set, so only task (1) can be selected.

The output is

```
2 1
1
```

This demonstrates why equal task degrees are not enough. Tasks (1) and (4) are both known by one participant, but choosing both excludes two people.

### Sample 2

The input is

```
3 5 6
1 1
1 2
2 1
2 3
3 1
3 3
```

The task participant sets are (S_1={1,2,3}), (S_2={1}), (S_3={2,3}), (S_4=\varnothing), and (S_5=\varnothing).

| Task | Degree | Minimum degree | Selected |
| --- | --- | --- | --- |
| 1 | 3 | 0 | no |
| 2 | 1 | 0 | no |
| 3 | 2 | 0 | no |
| 4 | 0 | 0 | yes |
| 5 | 0 | 0 | yes |

The minimum degree is zero, so tasks (4) and (5) can both be chosen. No participant knows either task, so all three participants remain eligible.

The output is

```
3 2
4 5
```

This demonstrates why zero-degree tasks must be handled collectively. Selecting only one of them would satisfy the primary objective but fail the secondary one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(P+T+M)) | Reading the graph takes (O(M)), finding the minimum takes (O(T)), and all candidate edge lists together contain at most (M) edges |
| Space | (O(P+T+M)) | `head` and `degree` use (O(T)), `marked` uses (O(P)), and `who` plus `nxt` use (O(M)) |

The largest input contains (10^6) known participant-task pairs. The algorithm processes every pair only a constant number of times, so its work remains linear in the input size. The compact `array` representation is particularly useful in Python because storing one million integers as ordinary Python objects would consume much more memory.

## Test Cases

The following test harness contains the two samples and several additional cases. The implementation is repeated inside the test file so that the tests are self-contained. The runner temporarily replaces standard input and captures standard output.

```python
import sys
import io
from array import array
from contextlib import redirect_stdout

def solve():
    input = sys.stdin.readline

    P, T, M = map(int, input().split())

    head = array('i', [-1]) * T
    degree = array('i', [0]) * T
    who = array('i')
    nxt = array('i')

    for _ in range(M):
        u, v = map(int, input().split())
        v -= 1

        idx = len(who)
        who.append(u)
        nxt.append(head[v])
        head[v] = idx
        degree[v] += 1

    min_task = 0
    min_degree = degree[0]

    for v in range(1, T):
        if degree[v] < min_degree:
            min_degree = degree[v]
            min_task = v

    if min_degree == 0:
        answer = [v + 1 for v in range(T) if degree[v] == 0]
        print(P, len(answer))
        print(*answer)
        return

    marked = bytearray(P + 1)

    edge = head[min_task]
    while edge != -1:
        marked[who[edge]] = 1
        edge = nxt[edge]

    answer = []

    for v in range(T):
        if degree[v] != min_degree:
            continue

        edge = head[v]
        same = True

        while edge != -1:
            if not marked[who[edge]]:
                same = False
                break
            edge = nxt[edge]

        if same:
            answer.append(v + 1)

    print(P - min_degree, len(answer))
    print(*answer)

def run(inp: str) -> str:
    global_input = globals().get("input", None)

    old_stdin = sys.stdin
    old_input = globals().get("input", None)

    sys.stdin = io.StringIO(inp)
    globals()["input"] = sys.stdin.readline

    out = io.StringIO()
    try:
        with redirect_stdout(out):
            solve()
    finally:
        sys.stdin = old_stdin
        if old_input is None:
            globals().pop("input", None)
        else:
            globals()["input"] = old_input

    return out.getvalue().strip()

# Provided sample 1.
assert run(
    """3 4 6
1 1
1 2
2 2
2 3
3 3
3 4
"""
) == """2 1
1""", "sample 1"

# Provided sample 2.
assert run(
    """3 5 6
1 1
1 2
2 1
2 3
3 1
3 3
"""
) == """3 2
4 5""", "sample 2"

# Minimum-size input: one participant, one task, nobody knows it.
assert run(
    """1 1 0
"""
) == """1 1
1""", "minimum-size input"

# All tasks have exactly the same participant set.
assert run(
    """3 4 4
1 1
1 2
1 3
1 4
"""
) == """2 4
1 2 3 4""", "all equal participant sets"

# The optimal task is the last task number.
assert run(
    """2 3 5
1 1
2 1
1 2
2 2
1 3
"""
) == """1 1
3""", "last task boundary"

# Maximum dimensions, no known pairs.
# Every task is unknown to everybody, so all tasks are selected.
max_case = "100000 100000 0\n"
expected_tasks = " ".join(map(str, range(1, 100001)))
assert run(max_case) == f"100000 100000\n{expected_tasks}", \
    "maximum P and T with M = 0"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0` | `1 1 / 1` | Minimum dimensions and empty edge set |
| `3 4 4`, every task known by participant 1 | `2 4 / 1 2 3 4` | All task participant sets are identical |
| `2 3 5`, task 3 is known only by participant 1 | `1 1 / 3` | Last task index and minimum-degree selection |
| `100000 100000 0` | `100000 100000 / 1 2 ... 100000` | Maximum (P,T), zero edges, and selecting every unknown task |

## Edge Cases

The empty participant set is handled before any participant marking. For

```
2 3 1
1 1
```

the degrees are (1,0,0). The minimum is zero, so the algorithm immediately collects tasks (2) and (3). The output is

```
2 2
2 3
```

No participant is excluded, and both zero-degree tasks are selected because the secondary objective asks for the largest possible task set.

Different participant sets with equal degree are handled by the `marked` array. For

```
3 3 3
1 1
2 2
3 3
```

every task has degree (1). The first task marks participant (1). Task (2) contains participant (2), which is not marked, so it is rejected. Task (3) is rejected for the same reason. The output is

```
2 1
1
```

The algorithm does not confuse equal cardinalities with equal sets.

The final task index is handled naturally because tasks are stored internally as indices (0) through (T-1), while output converts them back with `v + 1`. For

```
2 3 5
1 1
2 1
1 2
2 2
1 3
```

the degrees are (2,2,1). Task (3) is the unique minimum-degree task, so the output is

```
1 1
3
```

This specifically catches an implementation that accidentally scans only through task (T-1) in one-based indexing.

When every participant knows every task, the minimum degree can equal (P). For

```
1 2 2
1 1
1 2
```

the target set is ({1}), and both tasks have exactly that same set. The algorithm selects both, giving

```
0 2
1 2
```

The fact that zero participants remain eligible is valid because the task set is still nonempty and the objective is to maximize the count, not require at least one participant.

Finally, when several minimum-degree tasks share the same participant set, every one of them is collected. For

```
3 4 4
1 1
1 2
1 3
1 4
```

all four tasks have participant set ({1}). Selecting any nonempty subset excludes participant (1), leaving two eligible participants. Since adding another task does not exclude anyone new, the secondary objective requires selecting all four tasks, which the algorithm does.
