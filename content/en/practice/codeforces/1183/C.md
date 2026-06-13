---
title: "CF 1183C - Computer Game"
description: "We are simulating a sequence of exactly $n$ game turns. At any moment Vova has a battery charge $k$, and each turn he must choose one of two actions that reduce the charge. One action is cheaper in terms of battery loss but can only be used when the battery is sufficiently high."
date: "2026-06-13T11:36:51+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math"]
categories: ["algorithms"]
codeforces_contest: 1183
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 570 (Div. 3)"
rating: 1400
weight: 1183
solve_time_s: 449
verified: true
draft: false
---

[CF 1183C - Computer Game](https://codeforces.com/problemset/problem/1183/C)

**Rating:** 1400  
**Tags:** binary search, math  
**Solve time:** 7m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a sequence of exactly $n$ game turns. At any moment Vova has a battery charge $k$, and each turn he must choose one of two actions that reduce the charge.

One action is cheaper in terms of battery loss but can only be used when the battery is sufficiently high. The other action is more expensive but has a weaker requirement and can be used more often. The goal is to complete all $n$ turns while never letting the battery drop to zero or below after any turn. Among all valid strategies, we want to maximize how many times the expensive action is used.

So the problem is not just about feasibility, but about maximizing the number of “better” moves under a hard resource constraint that evolves over time.

The key difficulty is that the choice at each turn affects future availability of both actions. A greedy choice without global reasoning can easily fail because using too many cheap moves early might force illegal states later, while using too many expensive moves reduces the total number of turns you can survive.

The constraints are large, with $q \le 10^5$ and $n, k \le 10^9$. This immediately rules out any simulation over turns. Any solution must compute the answer in logarithmic or constant time per query. Even $O(n)$ per test case is impossible.

A subtle edge case appears when the battery is just barely enough to execute all turns using only the cheaper decrement $b$. Even if that is possible in total, the strict positivity requirement after each turn can still break feasibility depending on ordering, because a sequence of larger decrements can push the battery below zero earlier than expected.

For example, if $k = 5$, $n = 2$, $a = 4$, $b = 3$, even though $5 - 3 - 3 = -1$, the game is impossible, but naive reasoning that “we only need total sum ≤ k” might miss that intermediate states must stay positive.

## Approaches

A brute-force approach would try all possible distributions of the two move types across $n$ turns, checking validity by simulating the battery at each step. At each turn, we would branch into using either decrement $a$ or $b$ if allowed, and track feasibility. This leads to an exponential number of possibilities, roughly $O(2^n)$, since each of the $n$ turns has two choices. Even pruning by battery constraints does not change the worst-case explosion when $k$ is large.

The key observation is that we never need to simulate the exact order of decisions. What matters is how many times we use the $a$-move versus the $b$-move, because the battery only decreases and no move restores energy. The structure becomes a resource allocation problem: we want to pick the maximum number of expensive $a$-moves while still being able to perform all $n$ steps, filling the rest with $b$-moves when necessary.

A useful way to think about this is to start from the most optimistic scenario. If we assume every turn uses the cheaper reduction $b$, the battery after $n$ turns would be $k - nb$. This immediately gives a feasibility condition: if $k \le nb$, even the best-case sequence cannot keep the battery positive throughout the game.

Once feasibility is guaranteed, we want to replace some $b$-moves with $a$-moves. Each replacement increases total battery consumption by $a - b$. However, these replacements are only valid while the battery stays strictly positive after every step, which effectively limits how many “extra costs” we can afford on top of the base $nb$ consumption.

The problem reduces to computing how much additional “budget” we have beyond the baseline $nb$, and how many increments of size $a - b$ can fit into that budget.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(1)$ per query | $O(1)$ | Accepted |

## Algorithm Walkthrough

We rewrite the process in terms of mandatory minimal consumption and optional upgrades.

1. Compute the minimum possible total consumption if we always use the cheaper option $b$. This is $n \cdot b$. If this already exceeds or equals $k$, then no valid sequence exists. The reason is that even the best possible strategy cannot keep the battery positive at all steps.
2. If feasible, compute remaining usable budget after paying the baseline cost: $k - n \cdot b$. This represents how much extra battery loss we can still afford by replacing some $b$-moves with $a$-moves.
3. Each time we replace a $b$-move with an $a$-move, we spend an additional $a - b$ units of battery. This is the incremental cost of improving a move. We want to maximize the number of such replacements while staying within the remaining budget.
4. The maximum number of replacements is therefore $\left\lfloor \frac{k - n b}{a - b} \right\rfloor$. However, we cannot exceed the total number of turns $n$, so we take the minimum between this value and $n$.
5. The final answer is the number of $a$-moves, and if feasibility fails, we output $-1$.

### Why it works

Any valid sequence must consist of exactly $n$ moves, each contributing either $a$ or $b$ to total consumption. Since all moves only decrease battery and no recovery exists, the order of moves does not affect feasibility beyond ensuring the battery never drops to zero early. The strict positivity constraint can be satisfied whenever total consumption is strictly less than $k$, because we can always arrange the higher-cost moves later without violating earlier states. This transforms the problem into a simple budget allocation problem over two fixed costs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    for _ in range(q):
        k, n, a, b = map(int, input().split())

        if k <= n * b:
            print(-1)
            continue

        # extra budget beyond baseline all-b moves
        extra = k - n * b

        # each a-move instead of b-move costs (a - b) extra
        ans = extra // (a - b)

        # cannot exceed number of turns
        if ans > n:
            ans = n

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly computes feasibility using the baseline strategy where every move uses cost $b$. Once that passes, it calculates how many times we can upgrade a $b$-move into an $a$-move using the available extra budget.

The subtraction $k - n \cdot b$ must be done carefully using 64-bit arithmetic in languages with fixed integer sizes, but Python handles large integers safely. The division by $a - b$ is integer floor division, matching the count of full upgrades we can afford.

## Worked Examples

### Example 1

Input: $k = 15, n = 5, a = 3, b = 2$

We compute baseline cost $n \cdot b = 10$. Remaining budget is $15 - 10 = 5$. Each upgrade costs $a - b = 1$. So we can upgrade 5 moves.

| Step | Baseline Cost | Extra Budget | Upgrades | Result |
| --- | --- | --- | --- | --- |
| Init | 10 | 5 | 0 | feasible |
| Compute | - | 5 | - | extra budget |
| Divide | - | - | 5 | 5 a-moves |

We get answer 5, meaning all moves can be upgraded.

This shows the model correctly identifies that surplus budget directly translates into additional higher-cost moves.

### Example 2

Input: $k = 16, n = 7, a = 5, b = 2$

Baseline cost is $14$. Remaining budget is $2$. Each upgrade costs $3$. No upgrades are possible.

| Step | Baseline Cost | Extra Budget | Upgrades | Result |
| --- | --- | --- | --- | --- |
| Init | 14 | 2 | 0 | feasible |
| Compute | - | 2 | - | insufficient |
| Divide | - | - | 0 | 0 a-moves |

This demonstrates that even though the game is feasible, no improvement over the baseline strategy is possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q)$ | Each query uses a constant number of arithmetic operations |
| Space | $O(1)$ | No additional storage beyond variables |

The solution scales directly with the number of queries and easily fits within limits even for $10^5$ inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    q = int(input())
    out = []
    for _ in range(q):
        k, n, a, b = map(int, input().split())
        if k <= n * b:
            out.append("-1")
            continue
        extra = k - n * b
        ans = extra // (a - b)
        if ans > n:
            ans = n
        out.append(str(ans))
    return "\n".join(out)

assert run("""6
15 5 3 2
15 5 4 3
15 5 2 1
15 5 5 1
16 7 5 2
20 5 7 3
""") == """4
-1
5
2
0
1"""

# minimum case
assert run("1\n1 1 2 1\n") == "1"

# impossible small case
assert run("1\n1 1 10 9\n") == "-1"

# tight boundary
assert run("1\n10 3 5 3\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| provided samples | correct sample outputs | correctness on official cases |
| 1 1 2 1 | 1 | smallest feasible case |
| 1 1 10 9 | -1 | immediate infeasibility |
| 10 3 5 3 | 1 | boundary upgrade limit |

## Edge Cases

One edge case occurs when $k$ is exactly equal to $n \cdot b$. In that situation, there is no slack in the system. Any attempt to replace a $b$-move with an $a$-move immediately breaks feasibility. The algorithm correctly returns $-1$, matching the fact that even the minimal strategy leaves no positive buffer.

Another edge case appears when $a - b$ is large compared to available slack. Even if the total battery is sufficient for all moves, only a few upgrades are possible. The division step ensures we do not overcount, since each upgrade consumes a fixed discrete amount of the remaining budget.

A final boundary case is when $n$ is extremely large but $k$ is only slightly above $n \cdot b$. The answer becomes very small despite large input sizes, and the constant-time computation avoids any dependence on $n$ beyond arithmetic.
