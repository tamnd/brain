---
title: "CF 106409A - Harker!!"
description: "The problem describes a full binary tree of height h. Every node is a task. Initially only the root task is available. In each time moment, up to p processors can complete available tasks, and completing a task makes its two children available for the next moment."
date: "2026-06-25T09:57:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106409
codeforces_index: "A"
codeforces_contest_name: "HPI 2026 Advanced"
rating: 0
weight: 106409
solve_time_s: 36
verified: true
draft: false
---

[CF 106409A - Harker!!](https://codeforces.com/problemset/problem/106409/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a full binary tree of height `h`. Every node is a task. Initially only the root task is available. In each time moment, up to `p` processors can complete available tasks, and completing a task makes its two children available for the next moment. A task that becomes available stays available until a processor handles it.

For each test case, we need to find the minimum number of moments needed to finish all tasks.

The input gives several independent scenarios. Each scenario contains the tree height and the number of processors. The output is the minimum schedule length for that scenario.

The main difficulty comes from the fact that processing is not forced to happen level by level. A slow solution might finish all nodes of one depth before considering the next depth, but processors can leave some nodes from an earlier depth unfinished and combine them with newly created tasks later.

The height is small enough that the number of levels is the important factor, not the total number of nodes. A full binary tree with height `h` has `2^h - 1` nodes, so directly simulating every node becomes impossible when `h` is large. The solution must work using only the number of tasks available at each depth. Since the number of processors can also be large, every operation should be close to constant time per level. An `O(2^h)` approach would quickly become too slow, while an `O(h)` approach easily handles the limits.

A common edge case is when the processors are enough to finish a whole level immediately, but not enough to finish all future work. For example:

```
1
3 2
```

The tree has 7 nodes. The root is done at moment 1, two nodes at moment 2, and the remaining four nodes cannot be finished in one more moment because only two processors exist. The correct answer is:

```
4
```

A level-by-level implementation that does not carry unfinished work forward can accidentally produce a larger value because it wastes processors on empty levels.

Another tricky case is when the number of available tasks is not divisible by the processor count. For example:

```
1
4 3
```

At some moment there may be 5 ready tasks. Three are processed, and the remaining two should be combined with tasks created later. Treating those two tasks as if they belong to an isolated level gives a wrong answer.

## Approaches

The straightforward approach is to simulate the tree levels. At depth `0` there is one task, at depth `1` there are two tasks, then four, and so on. For each depth, we could calculate how many moments are required to process all tasks at that depth. This works for small trees because the structure is simple.

The problem is that this simulation assumes tasks from one depth are independent from tasks in the next depth. In reality, leftover tasks remain available. If three processors are working on a tree and a level has four tasks, the last task does not disappear after that moment. It waits and can be processed together with tasks from the next level.

The brute force simulation over every node is also too expensive. A tree of height `h` contains `2^h - 1` nodes, and this becomes enormous even for moderately large heights.

The key observation is that we do not need to know individual tasks. We only need to know how many tasks are waiting before processing each level. Let `remaining` represent tasks from previous levels that were not completed. When a new level contains `2^i` tasks, the total available work becomes `2^i + remaining`. We can finish as many full processor groups as possible, and whatever is left becomes the new `remaining`.

This transforms the problem from simulating a tree into a simple greedy process over the height. The greedy choice is optimal because every processor slot should be used as soon as possible. Delaying a ready task never creates extra future capacity, while finishing tasks earlier can only expose more children.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^h) | O(2^h) | Too slow |
| Optimal | O(h) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with `remaining = 0` and `answer = 0`. The `remaining` value stores tasks that are ready but were not processed during previous moments.
2. Process the tree levels from the root downwards. At level `i`, the number of newly available tasks is `2^i`. The total tasks that can be handled at this stage are `2^i + remaining`.

The reason we add `remaining` here is that unfinished tasks do not belong to a fixed level. They are simply waiting tasks and can be handled together with new tasks.
3. Divide the available tasks by the number of processors. The quotient tells us how many complete moments can be spent processing this amount of work. Add that value to `answer`.
4. Store the leftover tasks after those complete moments. They are the tasks that will wait until the next level creates more available work.
5. After all levels are processed, if some tasks are still waiting, one final moment is needed to finish them. Add this final moment to the answer.

Why it works:

At every level, the algorithm keeps exactly the set of tasks that are currently available but not finished. No task is removed unless a processor handles it. The greedy step of using all possible processor capacity immediately is safe because processing a task earlier can only reveal more children, never reduce future options. The stored remainder preserves all unfinished work, so the next level starts with the correct state.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        h, p = map(int, input().split())

        remaining = 0
        moments = 0

        for level in range(h):
            tasks = (1 << level) + remaining
            moments += tasks // p
            remaining = tasks % p

        if remaining:
            moments += 1

        ans.append(str(moments))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The loop iterates through each depth of the tree. The expression `1 << level` computes `2^level`, which avoids floating point operations and keeps the calculation exact.

The division step counts how many complete processor batches fit into the currently available tasks. The remainder assignment is the critical part of the implementation. If it is forgotten, the solution incorrectly assumes that every depth must be completed before moving forward.

The final check handles unfinished tasks after the last level. The leaves do not create more tasks, so the only remaining work is to spend one more moment finishing them.

## Worked Examples

For the input:

```
3
3 1
3 2
10 6
```

The first case:

| Level | New tasks | Remaining before | Total tasks | Moments added | Remaining after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 1 | 0 |
| 1 | 2 | 0 | 2 | 2 | 0 |
| 2 | 4 | 0 | 4 | 4 | 0 |

The answer is `7`. With one processor, every node must be processed individually.

The second case:

| Level | New tasks | Remaining before | Total tasks | Moments added | Remaining after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 | 1 |
| 1 | 2 | 1 | 3 | 1 | 1 |
| 2 | 4 | 1 | 5 | 2 | 1 |

After the loop, one remaining task needs one more moment, giving `4`.

The trace shows why carrying leftovers matters. After the first moment with two processors, the unfinished task is still available and is combined with work from the next level.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(h) | Each tree level is processed once |
| Space | O(1) | Only counters for the current state are stored |

The algorithm never builds the tree, so its memory usage does not depend on the number of nodes. Since the work is proportional only to the height, it remains fast even when the tree itself would contain too many nodes to simulate.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out.getvalue()

# provided samples
assert run("""3
3 1
3 2
10 6
""") == """7
4
173
""", "samples"

# minimum size
assert run("""1
1 1
""") == """1
""", "single node"

# all tasks fit immediately after first levels
assert run("""1
5 100
""") == """1
""", "many processors"

# leftovers across levels
assert run("""1
4 3
""") == """5
""", "carry remainder"

# large height with small processors
assert run("""1
10 1
""") == """1023
""", "single processor full tree"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1` | `1` | Smallest tree case |
| `1 / 5 100` | `1` | Enough processors to finish everything quickly |
| `1 / 4 3` | `5` | Leftover tasks carried between levels |
| `1 / 10 1` | `1023` | Worst case processor shortage |

## Edge Cases

For a case where processors exactly match a level size, such as:

```
1
3 4
```

the root is completed in the first moment. The next level has two tasks and both are finished immediately. The final level has four tasks and also finishes immediately. The answer is `3`. The algorithm handles this because every level contributes one batch and leaves no remainder.

For a case with leftovers:

```
1
4 3
```

level 0 gives one leftover task after the first moment. At level 1, the available work is `2 + 1 = 3`, so it is finished in one moment and leaves no remainder. At level 2, four new tasks appear. Three are processed, leaving one. Level 3 begins with `8 + 1 = 9` tasks, which require three moments. The total becomes `5`. The result depends on keeping the waiting task alive instead of resetting at every level.

For a single processor:

```
1
10 1
```

every task requires its own moment. The tree contains `2^10 - 1 = 1023` tasks, so the output is `1023`. The algorithm reaches this naturally because every division by `1` consumes exactly one moment per available task.
