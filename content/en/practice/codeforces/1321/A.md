---
problem: 1321A
contest_id: 1321
problem_index: A
name: "Contest for Robots"
contest_name: "Codeforces Round 625 (Div. 2, based on Technocup 2020 Final Round)"
rating: 900
tags: ["greedy"]
answer: passed_samples
verified: true
solve_time_s: 275
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2dea0c-3f38-83ec-99b2-4ad1063464b8
---

# CF 1321A - Contest for Robots

**Rating:** 900  
**Tags:** greedy  
**Model:** gpt-5-3-mini  
**Solve time:** 4m 35s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2dea0c-3f38-83ec-99b2-4ad1063464b8  

---

## Solution

## Problem Understanding

We are given two fixed binary strings of length $n$, describing how two robots behave across a set of tasks. For each task $i$, the first robot either solves it or not, and the same for the second robot. Polycarp assigns a positive integer score $p_i \ge 1$ to each task, and a robot’s total score becomes the sum of scores of tasks it solves.

The freedom is in choosing the values $p_i$, but there is a constraint: we want the first robot to end up with a strictly larger total score than the second robot. Among all such valid assignments, we want to minimize the largest assigned value.

The interaction between tasks is completely independent except through this global maximum constraint. Each task contributes either equally to both robots, only to one of them, or to none. This structure suggests that what matters is not the absolute values of $p_i$, but how they amplify differences between the two robots.

The constraints $n \le 100$ imply that even quadratic or cubic reasoning over tasks is feasible, but the solution ends up being linear once the correct aggregation is identified. The key difficulty is that each $p_i$ is not fixed to a small set, it can vary independently, so a naive search over assignments is impossible.

A subtle edge case occurs when both robots behave identically on every task. In that situation, any assignment produces identical scores, so strict superiority is impossible. Another failure case arises when the first robot never solves a task that the second robot solves, since then the first robot can never gain an advantage regardless of scoring.

## Approaches

A brute-force approach would try all possible assignments of values $p_i$ up to some bound $K$, and check whether there exists an assignment making the first robot’s score larger. Even for a fixed $K$, each $p_i$ has $K$ choices, so this is $K^n$, which is far beyond feasible even for tiny $n$.

The key observation is that the score difference is linear in the chosen values. Each task contributes either positively, negatively, or not at all to the difference between robots. Since we control each coefficient $p_i$ independently within $[1, K]$, the optimal strategy is to push positive contributions as high as possible and negative contributions as low as possible.

This reduces the entire problem to counting how many tasks help the first robot and how many help the second robot, then balancing their contributions under extreme assignments of $p_i$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over assignments | Exponential | O(n) | Too slow |
| Greedy value separation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We classify each task by comparing robot behaviors. Let us define three groups: tasks solved by both robots, tasks solved only by the first robot, and tasks solved only by the second robot.

We then reason about how to assign values to maximize the score difference in favor of the first robot while respecting a maximum value $K$.

1. Count how many tasks are solved by the first robot but not the second. Call this $A$. These tasks create positive difference, so we want them as large as possible, meaning we assign them value $K$.
2. Count how many tasks are solved by the second robot but not the first. Call this $B$. These tasks create negative difference, so we want them as small as possible, meaning we assign them value $1$.
3. Tasks solved by both or neither contribute equally to both robots, so their contribution cancels out in the difference regardless of assignment.
4. Under optimal assignment, the score difference becomes $A \cdot K - B$.
5. We need this difference to be strictly positive, so we require $A \cdot K > B$.
6. If $A = 0$, then the difference is always $-B$, which can never become positive unless $B = 0$, but even then both robots remain equal, so strict inequality is impossible.
7. Otherwise, the minimal valid $K$ is the smallest integer satisfying $K > \frac{B}{A}$, which is $\left\lfloor \frac{B}{A} \right\rfloor + 1$.

### Why it works

The crucial invariant is that every task contributes independently and linearly to the score difference, and each coefficient $p_i$ is only bounded below and above. Since positive and negative contributions can be separated and independently pushed to extremes, any optimal solution must saturate these bounds: maximizing weights on positive-difference tasks and minimizing weights on negative-difference tasks. This guarantees that no mixed assignment can outperform the constructed extremal one, so the inequality check on $A \cdot K - B$ fully characterizes feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
r = list(map(int, input().split()))
b = list(map(int, input().split()))

A = 0
B = 0

for i in range(n):
    if r[i] == 1 and b[i] == 0:
        A += 1
    elif r[i] == 0 and b[i] == 1:
        B += 1

if A == 0:
    print(-1)
else:
    K = (B // A) + 1
    print(K)
```

The solution separates tasks into the only two categories that affect the difference. The loop is linear and constructs the counts directly. The final formula comes directly from solving the inequality $A \cdot K > B$ under integer constraints.

A common mistake is to attempt assigning values to all four possible patterns independently; only the asymmetric patterns matter for optimization. Another subtlety is handling $A = 0$, where division would be invalid and the answer is always impossible.

## Worked Examples

### Example 1

Input:

```
5
1 1 1 0 0
0 1 1 1 1
```

Here the classification is:

| i | r | b | type | effect |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | A | + |
| 2 | 1 | 1 | neutral | 0 |
| 3 | 1 | 1 | neutral | 0 |
| 4 | 0 | 1 | B | - |
| 5 | 0 | 1 | B | - |

So $A = 1$, $B = 2$. We need $1 \cdot K > 2$, so $K = 3$.

This demonstrates how a single strongly positive task can compensate for multiple negative tasks, but only by increasing the maximum allowed value.

### Example 2

Input:

```
3
1 0 1
1 0 1
```

Both robots behave identically on every task, so there are no $A$ or $B$ contributions. We get $A = 0$, $B = 0$. The difference is always zero, so strict dominance is impossible, producing $-1$.

This shows that even though scores can be assigned arbitrarily, identical behavior removes any controllable leverage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass counting task categories |
| Space | O(1) | Only a few counters are used |

The algorithm fits easily within limits since $n \le 100$, and even large generalizations would remain linear.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    n = int(input())
    r = list(map(int, input().split()))
    b = list(map(int, input().split()))

    A = 0
    B = 0

    for i in range(n):
        if r[i] == 1 and b[i] == 0:
            A += 1
        elif r[i] == 0 and b[i] == 1:
            B += 1

    if A == 0:
        print(-1)
    else:
        print(B // A + 1)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.strip()

# provided sample
assert run("5\n1 1 1 0 0\n0 1 1 1 1\n") == "3"

# both identical
assert run("3\n1 0 1\n1 0 1\n") == "-1"

# first dominates completely
assert run("3\n1 1 1\n0 0 0\n") == "1"

# second dominates completely
assert run("3\n0 0 0\n1 1 1\n") == "-1"

# mixed case
assert run("4\n1 0 1 0\n0 1 0 1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical arrays | -1 | impossible strict inequality |
| full dominance | 1 | simplest positive case |
| reverse dominance | -1 | symmetry failure |
| alternating pattern | 1 | balanced edge structure |

## Edge Cases

When both robots solve exactly the same set of problems, every task falls into the neutral category. The algorithm produces $A = 0$, immediately triggering the impossibility condition. Even though scores can be assigned arbitrarily, every assignment yields identical totals, so no configuration can satisfy strict superiority.

When the second robot dominates all tasks, every contribution is negative or neutral. The computed $B > 0$ with $A = 0$ again forces failure. This shows that the condition is not about totals alone, but about the existence of at least one lever where the first robot can gain relative advantage.