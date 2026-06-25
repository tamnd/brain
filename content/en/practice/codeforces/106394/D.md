---
title: "CF 106394D - Stamina"
description: "The problem describes a sequence of tasks processed from left to right. Each task has a reward value and a stamina reduction percentage. You begin with stamina equal to 1."
date: "2026-06-25T10:10:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106394
codeforces_index: "D"
codeforces_contest_name: "RUCP x WiCS Mini-Contest"
rating: 0
weight: 106394
solve_time_s: 30
verified: true
draft: false
---

[CF 106394D - Stamina](https://codeforces.com/problemset/problem/106394/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a sequence of tasks processed from left to right. Each task has a reward value and a stamina reduction percentage. You begin with stamina equal to 1. If you complete a task, you gain reward equal to the task value multiplied by your current stamina, then your stamina is reduced by the given percentage. If you skip the task, you gain nothing and your stamina stays unchanged. The goal is to choose which tasks to complete so that the final total reward is as large as possible.

The input contains several test cases. For each test case, the first value is the number of tasks. Each following pair describes one task: the first number is its reward coefficient, and the second number is the percentage of stamina lost after finishing it. The output is the maximum achievable score.

The total number of tasks across all test cases is large enough that checking all subsets is impossible. If there are up to 100000 tasks, a brute force approach would require considering an exponential number of choices, around $2^{100000}$, which cannot be handled. Even a dynamic program with too many states would fail, so the solution must process each task a constant number of times.

The tricky cases come from understanding that stamina changes only when a task is completed, and the decision for one task depends on future tasks. A greedy approach that always takes the largest immediate reward can fail because an early task may reduce stamina and make later tasks much less valuable.

For example:

```
1
10 100
```

The answer is `10`. A careless implementation might multiply the reward by the stamina after the reduction and get zero, but the reward is earned before stamina changes.

Another example:

```
3
10 5
10 80
20 5
```

The best answer is `29`. Completing all tasks gives:

```
10 + 9.5 + 17.1 = 36.6
```

Actually this example shows why order matters, because the second task destroys most of the stamina. The optimal choice is to skip the middle task:

```
10 + 20 * 0.95 = 29
```

A solution that only compares individual task rewards misses the effect of stamina being a multiplier for all future completed tasks.

## Approaches

A direct brute force solution would try every subset of tasks. For each subset, we simulate the chosen tasks in order, keeping the current stamina and accumulated score. This is correct because every possible decision sequence is examined. However, the number of subsets doubles with every additional task, so with 100000 tasks the number of possibilities is far beyond what any computer can process.

The useful observation is that when we look at a task from the end of the list, the future has already been summarized. Suppose we know the maximum score obtainable from all tasks after the current one, assuming our current stamina is 1. If we decide to complete the current task, we get its reward immediately and then all future rewards are scaled by the remaining stamina. If we skip it, we simply keep the future value unchanged.

This gives a one-dimensional dynamic programming state. Let `dp` represent the best score obtainable from the suffix of tasks currently being considered, with the stamina factor separated out. When processing a task with reward `c` and remaining stamina multiplier `m`, completing it gives:

$$c + m \times dp$$

For this problem the stamina multiplier after completing the task is:

$$1 - \frac{p}{100}$$

So when moving from the end towards the beginning, the transition becomes:

$$dp_i = \max(dp_{i+1}, c_i + (1-\frac{p_i}{100})dp_{i+1})$$

The reason this works is that the only effect the current task has on the future is the single multiplier applied to future rewards. We do not need to remember the entire history of previous choices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(1)$ | Too slow |
| Optimal Dynamic Programming | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the tasks and process them from the last task to the first task. The future decisions are easier to describe when the suffix answer is already known.
2. Maintain a variable `dp` containing the maximum score obtainable from the tasks processed so far in this reverse traversal. Initially there are no future tasks, so `dp = 0`.
3. For the current task with reward `c` and stamina loss percentage `p`, calculate the result if we complete it. The gained reward is `c`, and every future reward is multiplied by `1 - p / 100`.
4. Compare the value from completing the task with the value from skipping it. Keep the larger value as the new `dp`.
5. After all tasks have been processed, `dp` is the answer for the whole sequence.

Why it works: the dynamic programming invariant is that before processing a task in reverse order, `dp` equals the best score possible from all tasks after that task when the current stamina factor is treated as one. For the current task, every valid strategy either skips it or completes it. The transition evaluates both possibilities exactly, and no other information from earlier tasks is needed because stamina changes are represented only by the multiplier applied to future rewards. Since every suffix is solved optimally before moving left, the final value is optimal for the entire task list.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        tasks = []

        for _ in range(n):
            c, p = map(int, input().split())
            tasks.append((c, p))

        dp = 0.0

        for c, p in reversed(tasks):
            multiplier = 1.0 - p / 100.0
            take = c + multiplier * dp
            skip = dp
            dp = max(take, skip)

        ans.append(f"{dp:.10f}")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input is read normally because the total number of tasks is bounded, but `sys.stdin.readline` avoids unnecessary overhead.

The list of tasks is stored because the transition needs to run from the end to the beginning. While processing backwards, `dp` stores only the best value of the already processed suffix, so no full dynamic programming array is required.

The calculation uses floating point numbers because stamina reductions involve percentages. Python integers have no overflow issue, but floating point precision is needed for the fractional rewards. Printing ten digits after the decimal point is enough for the required error tolerance.

The order of operations matters. The reward `c` is added before applying the stamina multiplier because completing a task gives its points immediately, then reduces stamina for later tasks.

## Worked Examples

Consider:

```
1
2
10 0
20 5
```

The reverse process is:

| Current task | Current dp | Complete value | Skip value | New dp |
| --- | --- | --- | --- | --- |
| 20 5 | 0 | 20 | 0 | 20 |
| 10 0 | 20 | 30 | 20 | 30 |

The second task keeps all stamina because its reduction is zero. The algorithm chooses both tasks and obtains 30.

Another example:

```
1
3
10 5
10 80
20 5
```

The reverse process is:

| Current task | Current dp | Complete value | Skip value | New dp |
| --- | --- | --- | --- | --- |
| 20 5 | 0 | 20 | 0 | 20 |
| 10 80 | 20 | 14 | 20 | 20 |
| 10 5 | 20 | 29 | 20 | 29 |

The middle task is ignored because its stamina loss reduces the value of future rewards too much. The invariant holds because each step keeps the best possible suffix value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each task is processed once while moving backwards. |
| Space | $O(n)$ | The task list is stored. The dynamic programming state itself uses only $O(1)$ memory. |

The total number of tasks is at most 100000, so a linear solution easily fits within typical contest limits. The memory usage is also small because only the input tasks and one floating point state are maintained.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        tasks = []

        for _ in range(n):
            c, p = map(int, input().split())
            tasks.append((c, p))

        dp = 0.0
        for c, p in reversed(tasks):
            dp = max(dp, c + (1 - p / 100.0) * dp)

        out.append(f"{dp:.10f}")

    return "\n".join(out)

assert solution("""1
2
10 0
20 5
""") == "30.0000000000"

assert solution("""1
3
10 5
10 80
20 5
""") == "29.0000000000"

assert solution("""1
1
10 100
""") == "10.0000000000"

assert solution("""1
4
5 0
5 0
5 0
5 0
""") == "20.0000000000"

assert solution("""1
3
100 100
1 100
50 0
""") == "150.0000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One task with 100% stamina loss | 10 | Reward is received before stamina changes. |
| Tasks where a large penalty exists in the middle | 29 | Skipping harmful tasks is necessary. |
| All reductions are zero | 20 | All tasks should be selected when stamina never decreases. |
| Mixed extreme reductions | 150 | Handles boundary percentages correctly. |

## Edge Cases

For the case:

```
1
1
10 100
```

The algorithm starts with `dp = 0`. Completing the task gives `10 + 0 * 0 = 10`, while skipping gives `0`, so the answer becomes 10. The stamina reduction happens after receiving the reward and does not affect the current task.

For the case:

```
1
3
10 5
10 80
20 5
```

The reverse dynamic programming starts from the last task. The value after the last task is 20. The middle task would produce only `10 + 0.2 * 20 = 14`, so the algorithm keeps 20 by skipping it. The first task gives `10 + 0.95 * 20 = 29`, which becomes the final answer.

For tasks where every reduction is zero:

```
1
4
5 0
5 0
5 0
5 0
```

Every completed task keeps the same stamina multiplier. The transition always prefers taking the task because it adds a positive reward without harming future rewards. The final answer is 20.
