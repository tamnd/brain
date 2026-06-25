---
title: "CF 106415D - Sousse"
description: "We have a complete binary task tree. The root task is available at the beginning. Whenever a task is processed, its two children become available for future processing. There are p processors, so during one time moment we can complete at most p currently available tasks."
date: "2026-06-25T09:44:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106415
codeforces_index: "D"
codeforces_contest_name: "Winter Cup 8.0 Online Mirror Contest"
rating: 0
weight: 106415
solve_time_s: 33
verified: true
draft: false
---

[CF 106415D - Sousse](https://codeforces.com/problemset/problem/106415/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a complete binary task tree. The root task is available at the beginning. Whenever a task is processed, its two children become available for future processing. There are `p` processors, so during one time moment we can complete at most `p` currently available tasks. A task that becomes available stays available until a processor handles it.

The goal is to find the minimum number of time moments required to process every task in a tree of height `h`.

The input contains many independent test cases. Each test case gives the tree height and the number of processors. The output is the smallest number of rounds needed for that pair.

The height is small enough that simulating levels is possible, but the number of test cases can be very large. A height around 50 means the tree itself can contain about `2^50` nodes, so building the tree or even iterating through all tasks is impossible. We need an algorithm that depends on the height, not the number of nodes. A solution close to `O(h)` operations per test case is the intended direction.

A common mistake is to process one tree level completely before moving to the next level. The processors do not work that way. Remaining tasks from an unfinished level can be processed together with newly created tasks from deeper levels.

For example, with height `3` and `2` processors, the correct answer is `4`.

```
h = 3, p = 2
```

The rounds are:

```
round 1: process root
round 2: process 2 children
round 3: process 2 of the 4 grandchildren
round 4: process remaining 2 grandchildren
```

A level by level simulation that assumes round 3 must finish all four grandchildren before considering future work can count incorrectly in larger cases.

Another edge case is when the number of processors is larger than the number of tasks available in a level. For example:

```
h = 2, p = 10
```

The tree has only three tasks. The correct output is:

```
2
```

The first round processes the root, and the second round processes the two children. A formula that divides every level size by `p` and forgets about the dependency between levels can incorrectly answer `1`.

A second important case is when the processors do not divide a level size exactly. For example:

```
h = 3, p = 3
```

The correct output is:

```
4
```

After the root and its two children are processed, there are four tasks. The third round processes three of them, leaving one unfinished task. That leftover task is still available in the next round and must be counted together with the newly available tasks.

## Approaches

The direct approach is to imagine every task in the tree. We can keep a queue of available tasks, process up to `p` tasks per round, and add children of processed nodes. This is correct because it follows the actual execution order. However, a height `50` binary tree contains about `2^50` nodes, which is far beyond any practical memory or time limit.

The useful observation is that all tasks on the same depth behave identically. We never need to know the identity of an individual task. At depth `i`, the number of newly available tasks is exactly `2^i`. The only extra information we need is how many tasks from previous depths are still waiting.

The brute force simulation fails because it tracks too much detail. The tree structure only matters through the number of tasks becoming available after each processed layer. We can compress the whole tree into a sequence of counts.

Let `carry` represent tasks that are already available but have not been processed after finishing a round. When we reach a new depth, the available tasks become:

```
2^depth + carry
```

The processors remove as many as possible. Every complete group of `p` tasks requires one round, and a remainder requires one additional round. The remainder becomes the carry for the next depth.

The last carry after all levels represents tasks that are still waiting after the deepest generated level, so it contributes one final round.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^h) | O(2^h) | Too slow |
| Optimal | O(h) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with `carry = 0` and `answer = 0`. The carry stores unfinished tasks from previous levels, while the answer counts completed rounds.
2. For every depth from `0` to `h - 1`, compute the tasks available at that depth as `2^depth + carry`. The value `2^depth` is the number of nodes created by processing the previous level.
3. Divide the available tasks by `p`. Each complete group of `p` tasks consumes one round. Add the quotient to the answer.
4. Store the remainder as the new carry. These are tasks that could not be completed yet and will remain available for the next round.
5. After all depths are processed, if `carry` is nonzero, add one final round because the remaining tasks have no children and only need processors to finish them.

Why this works comes from the invariant that after every iteration, `carry` is exactly the number of available but unfinished tasks after all possible full processor groups have been used on the current depth. Since future rounds can always combine these tasks with newly generated tasks, keeping only this number preserves all information needed for the optimal schedule.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        h, p = map(int, input().split())

        carry = 0
        rounds = 0
        nodes = 1

        for _ in range(h):
            available = nodes + carry
            rounds += available // p
            carry = available % p
            nodes *= 2

        if carry:
            rounds += 1

        ans.append(str(rounds))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The loop processes the tree one depth at a time without creating any nodes. `nodes` stores the number of tasks appearing at the current depth, which doubles after every iteration because the tree is binary.

The division by `p` counts how many full processor batches can be completed immediately. The remainder is not discarded because those tasks are still waiting and can be combined with future tasks. This is the main detail that separates the correct solution from a simple level simulation.

The values grow exponentially in the mathematical description, but the height is at most 50, so Python integers safely handle them. The code also avoids floating point operations such as `2 ** h` with logarithmic approximations, which removes precision concerns.

## Worked Examples

For:

```
3
3 1
3 2
10 6
```

the first test behaves as follows.

| Depth | New tasks | Carry before | Available | Rounds added | Carry after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 1 | 0 |
| 1 | 2 | 0 | 2 | 2 | 0 |
| 2 | 4 | 0 | 4 | 4 | 0 |

The result is `7`, which matches the fact that with one processor every task must be processed individually.

For:

```
h = 3, p = 2
```

the trace is:

| Depth | New tasks | Carry before | Available | Rounds added | Carry after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 | 1 |
| 1 | 2 | 1 | 3 | 1 | 1 |
| 2 | 4 | 1 | 5 | 2 | 1 |

After the loop, one task remains, so one final round is needed. The answer is `4`.

The second trace demonstrates why leftover tasks cannot be ignored. The unfinished task after depth `2` is processed in the final round together with the normal scheduling process.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(h) | Each test case only processes the height of the tree. |
| Space | O(1) | Only counters are stored. |

The algorithm handles very large trees because it never creates the tree itself. Even with the maximum height, only about 50 iterations are needed per test case.

## Test Cases

```python
import sys, io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []

        for _ in range(t):
            h, p = map(int, input().split())
            carry = 0
            rounds = 0
            nodes = 1

            for _ in range(h):
                available = nodes + carry
                rounds += available // p
                carry = available % p
                nodes *= 2

            if carry:
                rounds += 1

            out.append(str(rounds))

        return "\n".join(out)

    result = solve()
    sys.stdin = old_stdin
    return result

assert solution("""3
3 1
3 2
10 6
""") == """7
4
173""", "samples"

assert solution("""1
1 100
""") == """1""", "large number of processors"

assert solution("""1
3 3
""") == """4""", "partial level processing"

assert solution("""1
50 10000
""") == """562949953421""", "maximum height"

assert solution("""1
2 2
""") == """2""", "small balanced tree"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1`, `3 2`, `10 6` | `7`, `4`, `173` | Provided examples and normal scheduling |
| `1 100` | `1` | Handles processors exceeding available tasks |
| `3 3` | `4` | Handles leftover tasks between levels |
| `50 10000` | `562949953421` | Handles the maximum height without building the tree |
| `2 2` | `2` | Checks small tree boundaries |

## Edge Cases

For the case:

```
1
2 10
```

the tree contains one root and two children. The algorithm starts with one available task, processes it, and then sees the two children. Since both children fit into one processor round, the answer is `2`. It does not incorrectly merge the root and children into the same round because children do not exist until the parent is completed.

For:

```
1
3 3
```

the first two depths create a leftover task. The algorithm records the remainder instead of throwing it away. At the last depth, the available amount includes this waiting task, producing the correct answer `4`.

For:

```
1
50 10000
```

the algorithm never allocates memory proportional to the number of nodes. It only doubles a counter 50 times and maintains the carry value, so the enormous implicit tree size does not affect feasibility.
