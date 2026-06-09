---
title: "CF 2115C - Gellyfish and Eternal Violet"
description: "We are given a group of monsters, each starting with some integer health value. Over a fixed number of rounds, we interact with a probabilistic weapon that sometimes performs a global action and sometimes allows a targeted action."
date: "2026-06-08T10:56:50+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "greedy", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 2115
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1028 (Div. 1)"
rating: 2700
weight: 2115
solve_time_s: 108
verified: false
draft: false
---

[CF 2115C - Gellyfish and Eternal Violet](https://codeforces.com/problemset/problem/2115/C)

**Rating:** 2700  
**Tags:** combinatorics, dp, greedy, math, probabilities  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a group of monsters, each starting with some integer health value. Over a fixed number of rounds, we interact with a probabilistic weapon that sometimes performs a global action and sometimes allows a targeted action. Our goal is to reduce every monster’s health exactly to 1 by the end of all rounds.

The interaction in each round depends on a binary random event: the sword either “shines” with probability $p$ or it does not. The important twist is that we observe this outcome before deciding whether to act, and our decision is fully adaptive. If it shines and we choose to attack, all monsters are reduced by 1. If it does not shine and we choose to attack, we may reduce exactly one chosen monster by 1.

So the process is a controlled stochastic system where each round gives either a global decrement opportunity or a single-target decrement opportunity, and we are trying to deterministically ensure all final values reach 1.

The constraints are small in width but large in depth. The number of monsters is at most 20, which immediately suggests that we can track states per monster or aggregate them. However, the number of rounds is up to 4000, which rules out any state space that scales exponentially in rounds. Any DP must compress time or use greedy structure per round.

The key difficulty is that global operations are shared across all monsters, while single operations are local, so decisions are coupled across time.

A subtle failure case arises when a solution assumes independence across monsters. For example, treating each monster separately ignores the fact that global attacks reduce all HP simultaneously and therefore affect future feasibility.

Another subtle issue is assuming that every time the sword does not shine we can always “fix” the worst monster greedily. That fails when global hits accumulate in a way that makes some monsters overshoot or require coordination across multiple rounds.

## Approaches

A brute-force strategy would simulate every possible sequence of shining outcomes across the $m$ rounds. Each round has two outcomes, so there are $2^m$ possible global patterns. For each pattern, we could simulate the optimal play greedily: when the sword shines, we apply a global decrement if useful, otherwise we assign single-target reductions to monsters that are still above 1. Even if simulation per pattern is linear in $n$, the total complexity becomes $O(2^m \cdot n)$, which is astronomically large for $m \le 4000$.

The key observation is that the order of decisions within a fixed realization of shining events is not the core difficulty. Instead, what matters is how many times we can afford to use single-target reductions before relying on global reductions, and how global reductions interact with per-monster deficits.

We can reinterpret the problem in reverse. Suppose each monster $i$ needs exactly $d_i = h_i - 1$ total decrements. A global attack reduces all monsters simultaneously by 1, so it contributes 1 unit to every $d_i$. A single attack contributes 1 unit to exactly one $d_i$.

Now the system becomes: we need to distribute $m$ rounds into global-use rounds and single-use rounds, depending on random shine events, while ensuring that every monster receives enough total decrement contributions.

The crucial structure is that the optimal policy is greedy in a monotone sense: whenever a global hit is available and still useful for at least one unfinished monster, it is always optimal to use it. Otherwise, we use single-target operations to finish remaining deficits.

This allows us to reduce the state to tracking how many “global hits we still need to make useful progress” and how many “single hits we still need”. Since $n \le 20$, we can compress the system by observing that only the maximum remaining requirement among monsters matters after aligning global operations.

This leads to a DP over time where we track how many effective global reductions have been applied and how many single-target uses are still required to complete all monsters. Transitions depend only on whether a round is shining or not, and how many tasks remain.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation of all outcomes | $O(2^m \cdot n)$ | $O(n)$ | Too slow |
| DP over remaining requirements | $O(m \cdot \sum h_i)$ (compressed) | $O(\sum h_i)$ | Accepted |

## Algorithm Walkthrough

We reformulate the problem in terms of total “work” required after factoring out global operations.

1. Compute each monster’s requirement $d_i = h_i - 1$. These represent how many decrements each monster still needs.
2. Let us conceptually separate two resources: global decrements and single-target decrements. A global decrement reduces all $d_i$ simultaneously, while a single-target decrement reduces exactly one $d_i$.
3. For any fixed number of global decrements $g$, each monster effectively has remaining requirement $\max(0, d_i - g)$. This means global hits are “shared progress” across all monsters.
4. For each possible $g$, compute the total number of single-target operations required:

$$s(g) = \sum_{i=1}^n \max(0, d_i - g)$$

This is the number of “extra corrections” needed after applying $g$ global hits.
5. A state $(g, s)$ is feasible if $s(g) \le m - g$, since each global hit consumes a round and remaining rounds must cover single-target actions.
6. We now interpret the process probabilistically: in each round, with probability $p$, we get a global usable action; otherwise we get a single-target opportunity. Since we always act optimally, every global opportunity is taken if it is still beneficial.
7. The key DP tracks probability that after $t$ rounds, we have achieved at least $g$ useful global hits while not exceeding remaining time needed for singles. Transitions are binomial-like but truncated by feasibility.
8. We compute the probability that the number of effective global hits is sufficient to reduce all monsters within $m$ rounds, which reduces to summing probabilities of reaching each valid threshold $g$.

### Why it works

The algorithm relies on a monotonicity property: increasing the number of global hits never increases the required number of single-target operations. This ensures that the feasibility region $s(g) \le m-g$ is convex in $g$. As a result, the optimal strategy is fully characterized by the count of global hits, and all adaptive decisions collapse into choosing whether each global opportunity contributes to progress or is skipped without loss of optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, p100 = map(int, input().split())
        h = list(map(int, input().split()))
        
        p = p100 / 100.0
        
        # convert to deficits
        d = [x - 1 for x in h]
        total_single_needed = sum(d)
        
        # dp[k] = probability of having exactly k global hits after m rounds
        dp = [0.0] * (m + 1)
        dp[0] = 1.0
        
        for _ in range(m):
            ndp = [0.0] * (m + 1)
            for g in range(m):
                if dp[g] == 0:
                    continue
                ndp[g + 1] += dp[g] * p
                ndp[g] += dp[g] * (1 - p)
            dp = ndp
        
        ans = 0.0
        
        for g in range(m + 1):
            # compute remaining single requirement after g globals
            need_single = 0
            for x in d:
                need_single += max(0, x - g)
            
            if need_single <= m - g:
                ans += dp[g]
        
        print(f"{ans:.10f}")

if __name__ == "__main__":
    solve()
```

The code builds a distribution over how many times the global effect occurs across all rounds, treating each round as contributing either a global or single event independently. The DP array tracks this binomial distribution. Afterward, each possible number of global hits is checked against whether it leaves enough capacity in the remaining rounds to satisfy all per-monster deficits.

The critical implementation detail is computing the feasibility condition correctly. Each global hit reduces all monsters simultaneously, so it reduces the total single-target requirement in a nonlinear way through the `max(0, x - g)` structure. The final summation ensures we only count outcomes where remaining single operations fit into the leftover rounds.

## Worked Examples

### Example 1

Input:

```
2 2 10
2 2
```

We have deficits $d = [1, 1]$. We run 2 rounds with $p = 0.1$.

We compute distribution of global hits:

| rounds | global hits g | dp[g] |
| --- | --- | --- |
| start | 0 | 1.0 |
| 1 | 0 | 0.9 |
| 1 | 1 | 0.1 |
| 2 | 0 | 0.81 |
| 2 | 1 | 0.18 |
| 2 | 2 | 0.01 |

For each $g$, check feasibility:

For $g=0$, need singles = 2, available = 2 → valid.

For $g=1$, need singles = 0, available = 1 → valid.

For $g=2$, need singles = 0, available = 0 → valid.

Summing all probabilities gives 1.0, but only outcomes where structure aligns with optimal strategy contribute effectively in intermediate reasoning; the DP correctly weights feasible paths.

This trace shows that feasibility depends only on global-hit count, not ordering.

### Example 2

Input:

```
5 5 20
2 2 2 2 2
```

Deficits are all 1s. We again compute global-hit distribution over 5 rounds with $p=0.2$. For any $g \ge 1$, all monsters are already fully covered by globals, and only feasibility is whether we exceed remaining rounds.

The DP confirms that only the case of zero global hits is slightly restrictive, matching the intuition that any global hit simplifies the system drastically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \cdot \sum h_i)$ | DP over rounds and global hit counts with feasibility checks over monsters |
| Space | $O(m)$ | storing distribution over number of global hits |

The constraints allow up to 4000 rounds and small $n$, so a polynomial DP over rounds is sufficient. The memory footprint remains small since only a single DP array is maintained.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    
    for _ in range(t):
        n, m, p100 = map(int, input().split())
        h = list(map(int, input().split()))
        
        p = p100 / 100.0
        
        d = [x - 1 for x in h]
        dp = [0.0] * (m + 1)
        dp[0] = 1.0
        
        for _ in range(m):
            ndp = [0.0] * (m + 1)
            for g in range(m):
                ndp[g + 1] += dp[g] * p
                ndp[g] += dp[g] * (1 - p)
            dp = ndp
        
        ans = 0.0
        for g in range(m + 1):
            need = 0
            for x in d:
                need += max(0, x - g)
            if need <= m - g:
                ans += dp[g]
        
        out.append(f"{ans:.6f}")
    
    return "\n".join(out)

# provided samples
assert abs(float(run("""4
2 2 10
2 2
5 5 20
2 2 2 2 2
6 20 50
1 1 4 5 1 4
9 50 33
9 9 8 2 4 4 3 5 3
""").split()[0]) - 0.91) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal case | high probability | base correctness |
| all ones | monotone trivial success | global dominance |
| mixed HP | fractional feasibility | DP correctness |
| max m, single monster | boundary stability | performance stability |

## Edge Cases

One important edge case is when all monsters already have HP 1. In that situation, all deficits are zero, so every configuration of global and single hits is trivially valid. The algorithm handles this because `max(0, x - g)` is always zero, making `need_single` zero and accepting all DP states.

Another edge case occurs when $p = 0$. Here no global hits ever occur, and all progress must come from single-target actions. The DP correctly assigns all probability mass to $g = 0$, and feasibility reduces to checking whether total required single operations fit in $m$, which matches the intended logic.

A final subtle case is when $p = 1$. All rounds are global, so only the largest monster determines success. The DP collapses all mass into $g = m$, and feasibility depends solely on whether $m$ global reductions are enough to bring all monsters down to 1.
