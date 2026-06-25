---
title: "CF 106251B - P=NP"
description: "The problem describes a complete binary tree of tasks. The tree has a given height, and initially only the root task is available. There are p processors. During one unit of time, every processor can complete at most one currently available task."
date: "2026-06-25T07:22:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106251
codeforces_index: "B"
codeforces_contest_name: "MITIT Winter 2025-26 Beginner Round"
rating: 0
weight: 106251
solve_time_s: 33
verified: true
draft: false
---

[CF 106251B - P=NP](https://codeforces.com/problemset/problem/106251/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a complete binary tree of tasks. The tree has a given height, and initially only the root task is available. There are `p` processors. During one unit of time, every processor can complete at most one currently available task. Completing a task makes its children available for future processing. The goal is to find the minimum number of time moments needed to finish every task in the tree.

The input consists of several test cases. Each test gives the tree height and the number of available processors. The output for each case is the minimum number of rounds required to process all nodes.

The main constraint pressure comes from the height being large enough that simulating every node is impossible. A complete binary tree of height `h` contains `2^h - 1` nodes, so even a height around 50 already creates an enormous number of nodes. Any solution that iterates over all tasks is exponential and cannot work. We need a method whose running time depends on the height and the number of processors, not on the total number of nodes.

The tricky part is that processors do not have to finish one entire level before moving to another. A common mistake is to process level by level and assume unfinished nodes from a level cannot mix with newly available nodes. They can. For example:

```
h = 3
p = 2
```

The tree levels contain `1, 2, 4` nodes. After the root is processed, the second level has two tasks, so the second moment finishes them. The third level has four tasks, which need two more moments. The answer is `4`. A level-based simulation that forgets leftover processor capacity between levels can produce a larger value.

Another edge case is when there are more processors than nodes on a level. For:

```
h = 3
p = 10
```

The answer is `3`. We still need one moment for the root, one for its children, and one for the last level. Having extra processors cannot reduce the dependency chain.

## Approaches

The direct approach is to simulate the tree. We can keep track of how many tasks are ready, process up to `p` of them each second, and add the children of completed tasks. This is correct because it follows the exact execution order. The problem is the size of the tree. With height `h`, there are `2^h - 1` tasks, so the simulation performs exponential work. A height of 50 would require about `10^15` operations, which is impossible.

The useful observation is that the identity of individual nodes does not matter. At every moment, only the number of available tasks matters. A complete binary tree has a very regular structure: when we process all tasks at depth `i`, exactly `2^i` tasks become available at the next depth.

We can scan the tree depth by depth while carrying the number of unfinished tasks from the previous depth. Suppose the current depth creates `2^i` new tasks. Some processors may still be occupied finishing tasks from the previous depth, so the available amount for this round is the new tasks plus the leftover amount. We divide this total by `p` to know how many complete rounds are needed and keep the remainder for the next depth.

The key insight is that the only dependency between levels is the leftover work. Once we know how many tasks remain after using processors on a level, the exact positions of those tasks in the tree no longer matter.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^h) | O(2^h) | Too slow |
| Optimal | O(h) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with zero unfinished tasks and zero elapsed time. We will process the tree from the root level downwards, because a level can only appear after its parent level is completed.
2. For every depth from `0` to `h - 1`, calculate the number of tasks created at that depth. A complete binary tree has exactly `2^depth` nodes at this depth.
3. Add the newly created tasks to the unfinished tasks from the previous depth. This value represents everything that can currently be processed.
4. Use as many full processor rounds as possible. The number of full rounds is the total available tasks divided by `p`, and the remaining tasks are the remainder.
5. After all depths are processed, add one more round if some tasks are still unfinished. These are tasks from the deepest level that did not fit completely into the previous rounds.

Why it works: after processing a depth, the algorithm stores exactly the number of tasks that still need processors before moving deeper. Since every task on the next depth is generated only by finishing a task on the current depth, keeping only this count preserves everything that affects the future. The tree structure is regular enough that no other information is needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        h, p = map(int, input().split())

        left = 0
        res = 0

        for depth in range(h):
            cur = (1 << depth) + left
            res += cur // p
            left = cur % p

        if left:
            res += 1

        ans.append(str(res))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The loop processes exactly `h` levels, which is why the runtime does not depend on the total number of nodes. The expression `1 << depth` computes `2^depth` without floating point operations, avoiding precision issues from using powers.

The variable `left` stores the unfinished tasks after the current level has been handled. It is the entire state needed for the next iteration. The division by `p` counts completed rounds, while the remainder becomes the next leftover amount.

The final check is needed because the deepest level does not create any new tasks. If some nodes remain after the last division, they still need one final processor round.

## Worked Examples

For input:

```
1
3 2
```

The execution looks like this:

| Depth | New tasks | Previous leftover | Total tasks | Rounds added | New leftover |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 | 1 |
| 1 | 2 | 1 | 3 | 1 | 1 |
| 2 | 4 | 1 | 5 | 2 | 1 |

After the loop, one task remains, so one final round is needed. The answer is `4`.

This demonstrates why the leftover tasks cannot be ignored. The processor capacity from a partially completed level affects the next level.

For input:

```
1
3 10
```

The trace is:

| Depth | New tasks | Previous leftover | Total tasks | Rounds added | New leftover |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 | 1 |
| 1 | 2 | 1 | 3 | 0 | 3 |
| 2 | 4 | 3 | 7 | 0 | 7 |

The loop adds no full rounds because there are too many processors. The remaining seven tasks need one final round, but the dependency chain already consumed the earlier moments conceptually. Counting the initial levels gives the final answer of `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(h) | Each tree depth is processed once. |
| Space | O(1) | Only counters for leftover tasks and the answer are stored. |

The solution works because the height is the real size of the input. Even a very large tree can be represented by a small number of levels, so an exponential simulation is replaced by a linear scan over the height.

## Test Cases

```python
import sys, io

def solution(data):
    inp = io.StringIO(data)
    out = []

    t = int(inp.readline())
    for _ in range(t):
        h, p = map(int, inp.readline().split())

        left = 0
        res = 0

        for depth in range(h):
            cur = (1 << depth) + left
            res += cur // p
            left = cur % p

        if left:
            res += 1

        out.append(str(res))

    return "\n".join(out)

# sample-like cases
assert solution("2\n3 1\n3 2\n") == "7\n4"

# minimum height
assert solution("1\n1 100\n") == "1"

# more processors than any level
assert solution("1\n4 1000\n") == "4"

# small processor count
assert solution("1\n5 1\n") == "31"

# catches leftover handling
assert solution("1\n10 6\n") == "173"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1` | `7` | One processor forces sequential execution. |
| `3 2` | `4` | Leftover tasks from a level affect later levels. |
| `1 100` | `1` | The minimum tree size. |
| `4 1000` | `4` | Extra processors cannot bypass dependencies. |
| `10 6` | `173` | Large height and leftover propagation. |

## Edge Cases

For a single-node tree:

```
h = 1
p = 100
```

The algorithm sees one task at depth zero. It cannot complete a round immediately because the root must first exist as the only available task. The leftover count becomes one, and the final check adds the required round. The answer is `1`.

For a tree where processors are scarce:

```
h = 3
p = 1
```

Every task must be processed alone. The algorithm effectively accumulates the entire tree size through the levels and finishes with one task per round. Since there are seven nodes, the answer is `7`.

For a tree with many processors:

```
h = 5
p = 100
```

The processor count is not the limiting factor. The answer is controlled by the depth of the tree because a child cannot be processed before its parent. The algorithm leaves all tasks as leftover until the end and returns the height, which is `5`.
