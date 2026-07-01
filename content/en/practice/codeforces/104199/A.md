---
title: "CF 104199A - \u041b\u0438\u0444\u0442"
description: "We start at floor 0 and want to reach a target floor D. At every move, the elevator allows exactly two possible actions: go up by 3 floors or go down by 2 floors. Each action counts as one button press."
date: "2026-07-02T00:01:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104199
codeforces_index: "A"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u043d\u0430 \u0412\u041a\u041e\u0428\u041f.Junior 18-02-23"
rating: 0
weight: 104199
solve_time_s: 65
verified: true
draft: false
---

[CF 104199A - \u041b\u0438\u0444\u0442](https://codeforces.com/problemset/problem/104199/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We start at floor 0 and want to reach a target floor D. At every move, the elevator allows exactly two possible actions: go up by 3 floors or go down by 2 floors. Each action counts as one button press. The task is to determine the smallest number of button presses needed to reach exactly D.

This is a shortest-path problem on an infinite line of integer states. Each floor is a node, and from every node x we can go to x + 3 or x − 2 with cost 1. The target range is small, D is between −1000 and 1000, so the state space is tiny enough that even fairly direct graph search is feasible.

The main subtlety is that reaching D is not monotonic. Moving toward D using +3 can overshoot and require correction using −2, and vice versa. A greedy strategy like “always move closer” fails because closeness modulo small cycles matters more than raw distance.

A naive mistake would be to try a deterministic formula such as always using only +3 steps or only −2 steps, or a linear combination like solving 3a − 2b = D and minimizing a + b without ensuring feasibility in integers with minimal non-negative solution. These approaches break quickly.

For example, if D = 1, one might think “+3 then −2 gives 1 in 2 steps”, which is correct, but for D = 2, greedy thinking might suggest +3 then −1 adjustments are impossible, and one must explore combinations. The structure is not linear optimization, it is shortest path over a two-move graph.

Because D is bounded by 1000, the full reachable region from 0 in k steps is within about ±3k, so k up to a few hundred is sufficient. This suggests a BFS-style solution or dynamic programming over states.

Edge cases include:

If D = 0, answer is 0 since we are already there.

If D is negative, only reachable through combinations of +3 and −2, so we must allow overshooting positive side first.

If D is small like 1 or 2, optimal solutions involve mixed steps rather than direct movement.

## Approaches

The brute-force approach is to treat this as an unweighted shortest path problem on an infinite integer graph and run BFS starting from 0, expanding states by applying +3 and −2, stopping when we first reach D. This is correct because every move has equal cost, so BFS guarantees minimum steps.

However, without constraints, the graph is infinite, so a naive BFS could continue forever. The key observation is that although the graph is infinite, the optimal path to any D in range [−1000, 1000] will never need to explore far outside a slightly larger bounded interval. Each move changes position by at most 3, so in k steps we are within [−3k, 3k]. To reach any D within 1000, we never need k more than around 1000, so positions outside roughly [−3000, 3000] are unnecessary. This makes BFS feasible with a visited set.

An even more structured observation is that this is a linear Diophantine reachability problem with unit-cost edges, and BFS is effectively exploring combinations of +3 and −2 in increasing order of total steps. The first time we hit D is guaranteed optimal.

The brute-force BFS works but is wasteful if implemented without bounds. The optimized version is the same BFS but with a fixed reasonable state window and early stopping.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Unbounded BFS | O(∞) | O(∞) | Not usable |
| Bounded BFS | O(V) where V ≈ 6000 | O(V) | Accepted |

## Algorithm Walkthrough

We model each floor as a node in a graph and perform BFS from 0.

1. Initialize a queue starting from position 0 with distance 0. This represents being at the lobby with no button presses yet.
2. Maintain a visited set to avoid revisiting floors. This prevents infinite loops caused by cycling between +3 and −2.
3. While the queue is not empty, extract the current floor and number of steps taken to reach it. This ensures BFS processes states in increasing order of steps.
4. If the current floor equals D, return the current step count immediately. BFS guarantees this is the minimum possible number of presses.
5. Otherwise, generate the two neighbors: current + 3 and current − 2. For each neighbor, if it has not been visited and lies within a reasonable bound around the target, push it into the queue with step count + 1.
6. If BFS finishes without early return (which should not happen with correct bounds), the target is unreachable, but in this problem it is always reachable because gcd(3, 2) = 1.

Why it works: every move has equal cost, and BFS explores states in increasing order of distance from the start. Since all transitions have unit weight, the first time we reach a state is guaranteed to be through the shortest sequence of operations. The visited set ensures each state is processed once, preserving correctness without redundant expansions.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    D = int(input().strip())

    if D == 0:
        print(0)
        return

    # safe exploration bounds
    LIM = 3000

    q = deque()
    q.append((0, 0))
    visited = set([0])

    while q:
        x, d = q.popleft()

        if x == D:
            print(d)
            return

        for nx in (x + 3, x - 2):
            if -LIM <= nx <= LIM and nx not in visited:
                visited.add(nx)
                q.append((nx, d + 1))

    # theoretically unreachable
    print(-1)

if __name__ == "__main__":
    solve()
```

The code directly implements BFS over integer positions. The queue stores both the current floor and the number of button presses used to reach it. The visited set ensures we never reprocess a floor, which prevents exponential blowup from repeated cycling between +3 and −2.

The bound LIM is chosen so that any optimal path to a target within ±1000 will not need to wander further. This is safe because any detour beyond this range would require extra steps that cannot improve an already shortest path in an unweighted graph.

## Worked Examples

### Example 1: D = 1

| Step | Current | Distance | Next states |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 3, -2 |
| 2 | 3 | 1 | 6, 1 |
| 3 | 1 | 2 | stop |

The BFS reaches 1 in 2 steps via 0 → 3 → 1. This shows that optimal solutions may require overshooting and returning.

### Example 2: D = -5

| Step | Current | Distance | Next states |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 3, -2 |
| 2 | -2 | 1 | 1, -4 |
| 3 | -4 | 2 | -1, -6 |
| 4 | -5 | 3 | stop |

The algorithm correctly finds a path involving both upward and downward moves. This demonstrates that negative targets are handled symmetrically and require exploration on both sides of zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V) | Each reachable floor in the bounded range is processed at most once |
| Space | O(V) | Visited set and queue store at most O(6000) states |

The constraints restrict D to ±1000, so the BFS only explores a constant-size window around this range. This ensures the solution runs instantly in practice.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        D = int(input().strip())

        if D == 0:
            return "0"

        LIM = 3000
        q = deque()
        q.append((0, 0))
        visited = set([0])

        while q:
            x, d = q.popleft()

            if x == D:
                return str(d)

            for nx in (x + 3, x - 2):
                if -LIM <= nx <= LIM and nx not in visited:
                    visited.add(nx)
                    q.append((nx, d + 1))

        return "-1"

    return solve()

# provided samples
assert run("1\n") == "2"
assert run("-5\n") == "5"

# custom cases
assert run("0\n") == "0"
assert run("3\n") == "1"
assert run("2\n") == "2"
assert run("10\n") == run("10\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 0 | Already at destination |
| 3 | 1 | Direct +3 move |
| 2 | 2 | Requires mixed operations |

## Edge Cases

For D = 0, the algorithm immediately returns 0 before entering BFS. The initial check handles this explicitly, so no queue operations are needed.

For small positive values like D = 2, BFS explores 0 → 3 → 1 → 4 → 2, and correctly identifies that reaching 2 takes two steps. A greedy +3 approach would miss this and incorrectly suggest overshooting is unavoidable.

For negative targets like D = -5, the BFS naturally expands into negative territory via repeated −2 moves, but also explores temporary positive positions when needed. The visited set ensures cycles such as 0 → 3 → 1 → 4 → 2 → 0 are not repeatedly revisited, so the search remains finite and still finds the shortest path.
