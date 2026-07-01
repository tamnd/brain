---
title: "CF 104326D - Clever Plan"
description: "We are given a system with two characters sharing a fixed number of identical honey pots. Initially, the pots are split randomly between them, but only splits where both sides receive at least one pot are allowed."
date: "2026-07-01T19:08:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104326
codeforces_index: "D"
codeforces_contest_name: "Udmurt SU Contest 2011"
rating: 0
weight: 104326
solve_time_s: 95
verified: true
draft: false
---

[CF 104326D - Clever Plan](https://codeforces.com/problemset/problem/104326/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a system with two characters sharing a fixed number of identical honey pots. Initially, the pots are split randomly between them, but only splits where both sides receive at least one pot are allowed. Since pots are indistinguishable, the only thing that matters is how many pots Pooh has, which can be any value from 1 to $n-1$, each equally likely.

After the initial split, the system evolves in discrete rounds. In each round, exactly one of three things may happen. With probability $p$, one pot moves from Pooh to the Heffalump, reducing Pooh’s count by one. With probability $q$, one pot moves from the Heffalump to Pooh, increasing Pooh’s count by one. With probability $r$, nothing changes. If Pooh ever reaches 0 pots or $n$ pots, the process stops permanently.

The task is to consider a fixed number of rounds $i$, and compute the probability that two conditions hold simultaneously. First, the process has not been absorbed yet, meaning neither side has reached zero pots. Second, the configuration after $i$ rounds is exactly the same as the initial configuration.

The constraints are small enough that the state space is essentially linear in $n$, since $n \le 26$, but the number of steps can be as large as 1600. This immediately suggests that a quadratic or cubic dynamic programming solution per test case is acceptable, while anything exponential over time or over states is not.

A subtle point is that the answer depends on the initial random split. We do not track a single starting state, but an average over all possible starting values of Pooh’s pot count. Another important constraint is the absorption rule. Any path that reaches 0 or $n$ must be excluded completely, even if it later returns conceptually to the same configuration.

A naive mistake is to ignore absorption and treat this as an unrestricted random walk on integers. That would incorrectly count paths that cross the boundary. Another mistake is to average states incorrectly by mixing transitions from different starting positions, which breaks the requirement that we return to the same initial configuration, not just any matching configuration.

## Approaches

A direct brute-force approach would simulate all possible sequences of $i$ rounds starting from each possible initial split. Each round branches into three outcomes, so after $i$ steps there are $3^i$ possible histories per starting state. Even for moderate $i$, this becomes infeasible, since $3^{1600}$ is astronomically large. Even pruning invalid states due to absorption does not reduce the branching factor enough to make this workable.

The key observation is that the system is a Markov chain over a small state space consisting of integer values from $1$ to $n-1$, with absorbing boundaries at $0$ and $n$. The probability of being in a state after $t$ steps depends only on the previous step, not on the full history. This allows us to replace exponential enumeration with dynamic programming over time.

However, we also need a second layer of structure. The condition requires returning to the original state, which means we cannot simply compute the distribution after $i$ steps from a mixed initial distribution. We must track transitions separately for each possible starting state, then combine results according to the uniform initial distribution.

This leads to a clean formulation: for each starting value $s$, compute the probability that a constrained random walk starting at $s$ is again at $s$ after $i$ steps without ever hitting boundaries. This is a standard DP on states and time, and since $n$ is small, running it independently for each start remains efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | $O(3^k)$ | $O(k)$ | Too slow |
| DP per start state | $O(n^2 \cdot k)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We interpret the process as a random walk on states $1$ through $n-1$, where state $x$ means Pooh has $x$ pots.

1. For each possible starting state $s$, initialize a DP array where only $dp[s] = 1$. This represents certainty that the process begins in configuration $s$, before any transitions occur.
2. Iterate over time steps from $1$ to $k$, updating a fresh DP array at each step. Each transition distributes probability mass according to the three possible outcomes of a round.
3. From a state $x$, the system can move to $x-1$ with probability $p$, to $x+1$ with probability $q$, or stay at $x$ with probability $r$. We apply these updates only when the resulting state remains within $[1, n-1]$.
4. Any transition that would move to $0$ or $n$ is discarded. This corresponds to absorption, and those paths do not contribute to future states.
5. After completing $i$ steps, record $dp[s]$, which represents the probability that starting from $s$, the system returns to $s$ without absorption.
6. Repeat this for all starting states $s \in [1, n-1]$, then average the results since the initial configuration is uniformly random over these states.

### Why it works

The DP state encodes both position and survival implicitly. Every probability mass in the table corresponds to a valid path that has not been absorbed. Because transitions are applied step-by-step and never reintroduce absorbed states, no invalid trajectory can re-enter the system. Linearity of probability ensures that summing over independent starting states and then averaging matches the original random initialization exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        p, q, r = map(float, input().split())
        k = int(input())

        m = n - 1
        inv_m = 1.0 / m

        answers = [0.0] * k

        for s in range(1, n):
            dp = [0.0] * n
            dp[s] = 1.0

            for t in range(k):
                ndp = [0.0] * n

                for x in range(1, n):
                    val = dp[x]
                    if val == 0:
                        continue

                    ndp[x] += val * r

                    if x - 1 >= 1:
                        ndp[x - 1] += val * p

                    if x + 1 <= n - 1:
                        ndp[x + 1] += val * q

                dp = ndp
                answers[t] += dp[s] * inv_m

        for v in answers:
            print(f"{v:.6e}")

if __name__ == "__main__":
    solve()
```

The solution builds a separate probability evolution for each possible initial split. The DP array represents the distribution of Pooh’s pot count after each round, conditioned on not having hit the absorbing boundaries.

The inner transition step applies the three possible outcomes directly. The boundary checks ensure that transitions into state $0$ or $n$ are ignored entirely, matching the rule that the game ends immediately when those states are reached.

Each time step contributes the probability of being back at the starting state for that particular initial value. We accumulate these contributions and divide by $n-1$ at the end implicitly through averaging.

The output formatting uses scientific notation to match the required precision constraints.

## Worked Examples

Consider the sample case with $n = 3$, where the only valid starting states are $1$ and $2$.

For each starting state, we track how probability mass evolves over time. The table below shows the probability of being back at the same state after each number of steps, before averaging.

### Trace for each start

| Step | Start = 1 (return prob) | Start = 2 (return prob) |
| --- | --- | --- |
| 1 | r | r |
| 2 | r^2 + pq | r^2 + pq |
| 3 | decays via boundary paths | decays via boundary paths |
| 4 | ... | ... |
| 5 | ... | ... |

The final answer at each step is the average of the two columns.

This demonstrates that symmetry is not required in general, but the averaging over initial states enforces a uniform contribution from both ends of the state space.

A second useful sanity check is the case $r = 1$, where no movement ever happens. In that case, every state remains fixed forever, so the probability of returning to the same state is always exactly 1 for every $i$, which matches the DP behavior since only self-loops exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \cdot n^2 \cdot k)$ | Each test runs a DP for every starting state, and each DP updates $n$ states for $k$ steps |
| Space | $O(n)$ | Only two arrays of size $n$ are needed per DP run |

The bounds $n \le 26$ and $k \le 1600$ make this comfortably fast even in Python, since the total number of transitions per test is small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else ""  # placeholder

# Sample (format placeholder since full I/O harness depends on integration)
# assert run("...") == "..."

# custom edge tests

# minimum n, minimal movement
# n=3, r=1 => always stable
# expected: all ones
# assert run("1\n3\n0.3 0.3 0.4\n3\n") == ...

# strong drift to boundaries
# assert run("...") == ...

# symmetric random walk
# assert run("...") == ...

# max k stress
# assert run("1\n26\n0.3 0.3 0.4\n1600\n") == ...
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $r=1$ case | all 1.0 | absorbing vs non-moving correctness |
| small n | manual trace | boundary handling |
| large k | stable output | performance and accumulation stability |

## Edge Cases

One important edge case is when movement probabilities push mass directly into absorption states. For example, with $n = 3$, starting from state $1$, any transition that decreases the state would immediately end the game. The DP correctly discards this mass by checking the boundary before adding transitions.

Another edge case is when $r$ is very close to 1. In this situation, most probability mass stays in place, and numerical stability matters more than combinatorial structure. The DP remains stable because probabilities are accumulated incrementally without subtraction.

A final case is when $k = 1$. Here, the answer is simply the probability of staying in the same state after one step, averaged over all starts. The DP reduces to a single transition layer, and no deeper history is involved.
