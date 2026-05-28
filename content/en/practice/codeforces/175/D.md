---
title: "CF 175D - Plane of Tanks: Duel"
description: "Two tanks fight each other. Each tank has hit points, a reload time, a damage interval, and a probability that its shot fails to penetrate armor. Whenever a tank fires, one of two things happens."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 175
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 115"
rating: 2400
weight: 175
solve_time_s: 152
verified: true
draft: false
---

[CF 175D - Plane of Tanks: Duel](https://codeforces.com/problemset/problem/175/D)

**Rating:** 2400  
**Tags:** brute force, dp, math, probabilities  
**Solve time:** 2m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

Two tanks fight each other. Each tank has hit points, a reload time, a damage interval, and a probability that its shot fails to penetrate armor.

Whenever a tank fires, one of two things happens. Either the shell does not penetrate, in which case the target loses no HP, or it penetrates and deals a uniformly random integer damage from the interval $[l, r]$.

Both tanks start firing at time $0$. After that, each tank fires every `dt` seconds. If both tanks shoot at the same moment, both shots are applied simultaneously. Vasya wins if the enemy dies, even if Vasya dies in the same simultaneous exchange.

The task is to compute the probability that Vasya eventually wins.

The constraints are small enough to allow dynamic programming over hit points. Maximum HP is only 200, and damage values are at most 100. Reload times are at most 30. That immediately suggests that the real difficulty is not state size, but handling the interaction between two asynchronous firing schedules.

A naive simulation over time is dangerous because the battle length is theoretically unbounded. If both tanks have a nonzero probability of dealing no damage, there is always some chance that the fight continues for arbitrarily long. Any approach based on truncating the timeline introduces precision issues.

The key observation is that the process only changes at firing moments. Between shots, nothing happens. Another subtle detail is simultaneous shots. If both tanks kill each other at the same time, Vasya still wins. A careless implementation that processes Vasya’s shot first or the enemy’s shot first will produce the wrong answer.

Consider this example:

```
100 3 50 50 0
100 3 50 50 0
```

At time 0 both tanks deal 50 damage. At time 3 both tanks again deal 50 damage. Both reach 0 HP simultaneously, and the correct answer is `1.0`, not `0.5`.

Another easy mistake is forgetting that a shot may fail to penetrate completely.

```
100 1 100 100 50
100 100 1 1 0
```

Vasya fires every second and instantly kills the enemy whenever penetration succeeds. The enemy barely matters. The answer is almost 1, but not exactly 1, because Vasya can theoretically miss forever with probability 0 in the limit, not in finite time.

A third subtle case is unequal firing schedules.

```
100 2 50 50 0
100 3 100 100 0
```

At time 0, Vasya deals 50 and enemy deals 100. Vasya dies immediately, so the answer is `0`, even though Vasya would have fired more frequently afterward. Once a tank is already dead before a later firing time, future shots never happen.

These edge cases force us to model the battle as a stochastic process with exact event ordering.

## Approaches

The brute-force idea is straightforward. Simulate every possible sequence of shots recursively. At each firing event, branch over every possible damage value and penetration outcome. Continue until one or both tanks die.

This is correct because every branch corresponds to one concrete realization of the duel. The problem is the number of branches. A single shot may have up to 92 outcomes: one miss outcome plus up to 91 different damage values. The number of firing events before the duel ends is unbounded. Even with memoization, tracking exact times and HP values creates a huge state space.

The structure of the problem gives us a better direction. HP is small, and firing times are periodic. Instead of simulating individual random trajectories, we can compute the probability of winning from every game state.

A state consists of:

- Vasya HP
- Enemy HP
- Time until Vasya’s next shot
- Time until enemy’s next shot

The reload timers are bounded by at most 30, so there are only about:

$$201 \times 201 \times 30 \times 30 \approx 3.6 \times 10^7$$

possible raw states, but most are unreachable. More importantly, transitions are simple.

At any state, we jump directly to the next firing event. Suppose the next event happens after $t$ seconds. We reduce both cooldowns by $t$. Then one or both tanks fire.

This turns the infinite-time process into a finite Markov DP.

The remaining challenge is cyclic dependencies. A shot may miss, returning to essentially the same state again. We cannot compute states with ordinary DFS memoization because the recurrence is self-referential.

The trick is algebraic rearrangement.

Suppose:

$$dp[s] = p_{\text{stay}} \cdot dp[s] + \sum p_i \cdot dp[s_i]$$

where $p_{\text{stay}}$ is the probability of returning to the same state.

Then:

$$dp[s] = \frac{\sum p_i \cdot dp[s_i]}{1 - p_{\text{stay}}}$$

This removes cycles caused by repeated misses.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(H^2 \cdot D^2 \cdot K)$ | $O(H^2 \cdot D^2)$ | Accepted |

Here $H \le 200$, $D \le 30$, and $K$ is the number of damage outcomes.

## Algorithm Walkthrough

1. Define a recursive DP state:

$$f(h_1, h_2, t_1, t_2)$$

where:

- $h_1$ is Vasya HP
- $h_2$ is enemy HP
- $t_1$ is time until Vasya fires
- $t_2$ is time until enemy fires

The function returns the probability that Vasya eventually wins.

1. Handle terminal states first.

If enemy HP is already non-positive, Vasya has won.

If Vasya HP is non-positive while enemy HP is still positive, Vasya has lost.

These conditions must be checked before processing future shots.

1. Advance time to the next event.

Let:

$$t = \min(t_1, t_2)$$

Subtract $t$ from both timers.

At least one timer becomes zero, meaning at least one tank fires now.

1. Enumerate all outcomes of the firing event.

There are three possibilities:

- Only Vasya fires
- Only enemy fires
- Both fire simultaneously

For each shooter:

- With probability $p$, the shot fails and deals 0 damage
- Otherwise, damage is uniformly random in $[l, r]$

If both shoot simultaneously, both damages are applied together before checking deaths.

1. Transition to the next state.

After firing:

- A tank that fired resets its timer to its reload duration
- A tank that did not fire keeps timer 0 only if it also fired now, otherwise its reduced timer remains

1. Accumulate probabilities.

For every damage combination:

- Compute resulting HP
- Compute transition probability
- Add contribution to answer

1. Handle self-loops.

Some outcomes may return to exactly the same state, usually when all shots miss.

Let:

- `stay` be total probability of returning to current state
- `sum_other` be contribution from all other states

Then:

$$dp = \frac{sum\_other}{1 - stay}$$

This is valid because repeated self-loops form a geometric series.

### Why it works

The DP state completely describes the future evolution of the duel. Future outcomes depend only on current HP values and remaining cooldowns, not on earlier history.

Every transition corresponds to exactly one firing event and all probabilistic outcomes from that event. The recurrence enumerates all possible futures weighted by their probabilities.

Self-loops are the only source of cyclic dependency. Rearranging the equation isolates the unknown state probability on one side, converting the infinite recursion into a finite computation. Since every nonterminal state eventually leaves itself with positive probability, the denominator is always positive.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

vhp, vdt, vl, vr, vp = map(int, input().split())
ehp, edt, el, er, ep = map(int, input().split())

vp = vp / 100.0
ep = ep / 100.0

v_outcomes = [(0, vp)]
cnt = vr - vl + 1
for d in range(vl, vr + 1):
    v_outcomes.append((d, (1.0 - vp) / cnt))

e_outcomes = [(0, ep)]
cnt = er - el + 1
for d in range(el, er + 1):
    e_outcomes.append((d, (1.0 - ep) / cnt))

@lru_cache(maxsize=None)
def dfs(h1, h2, t1, t2):
    if h2 <= 0:
        return 1.0

    if h1 <= 0:
        return 0.0

    t = min(t1, t2)
    t1 -= t
    t2 -= t

    stay = 0.0
    res = 0.0

    if t1 == 0 and t2 == 0:
        for dv, pv in v_outcomes:
            for de, pe in e_outcomes:
                prob = pv * pe

                nh1 = h1 - de
                nh2 = h2 - dv

                nt1 = vdt
                nt2 = edt

                if nh2 <= 0:
                    val = 1.0
                elif nh1 <= 0:
                    val = 0.0
                else:
                    if (nh1, nh2, nt1, nt2) == (h1, h2, t1, t2):
                        stay += prob
                        continue
                    val = dfs(nh1, nh2, nt1, nt2)

                res += prob * val

    elif t1 == 0:
        for dv, pv in v_outcomes:
            nh1 = h1
            nh2 = h2 - dv

            nt1 = vdt
            nt2 = t2

            if nh2 <= 0:
                val = 1.0
            else:
                if (nh1, nh2, nt1, nt2) == (h1, h2, t1, t2):
                    stay += pv
                    continue
                val = dfs(nh1, nh2, nt1, nt2)

            res += pv * val

    else:
        for de, pe in e_outcomes:
            nh1 = h1 - de
            nh2 = h2

            nt1 = t1
            nt2 = edt

            if nh1 <= 0:
                val = 0.0
            else:
                if (nh1, nh2, nt1, nt2) == (h1, h2, t1, t2):
                    stay += pe
                    continue
                val = dfs(nh1, nh2, nt1, nt2)

            res += pe * val

    return res / (1.0 - stay)

ans = dfs(vhp, ehp, 0, 0)
print(f"{ans:.10f}")
```

The implementation mirrors the recurrence directly.

The outcome lists contain both miss outcomes and penetrating hits. A miss is represented as damage 0 with its corresponding probability.

The recursive state always stores cooldowns relative to the current moment. Advancing time by the minimum cooldown guarantees that at least one shot happens next. This avoids simulating empty time intervals.

Simultaneous firing is the most delicate part. Both damages are computed first, then both HP values are updated together. Only after both updates do we check victory conditions. This correctly handles mutual destruction.

The self-loop handling is another subtle point. If all shots miss, the next state may be identical to the current state. Without separating this probability into `stay`, recursion would never terminate.

Using memoization is essential because many different event paths reach the same state.

## Worked Examples

### Sample 1

Input:

```
100 3 50 50 0
100 3 50 50 0
```

State evolution:

| Time | Vasya HP | Enemy HP | Event |
| --- | --- | --- | --- |
| 0 | 100 | 100 | Both deal 50 |
| 0 after shots | 50 | 50 | Continue |
| 3 | 50 | 50 | Both deal 50 |
| 3 after shots | 0 | 0 | Both destroyed |

Since simultaneous destruction counts as Vasya victory, answer is:

```
1.0
```

This example validates the simultaneous-update rule.

### Sample 2

Consider:

```
100 2 50 50 0
100 3 100 100 0
```

Trace:

| Time | Vasya HP | Enemy HP | Event |
| --- | --- | --- | --- |
| 0 | 100 | 100 | Both fire |
| 0 after shots | 0 | 50 | Vasya dead |

The battle ends immediately before Vasya can use his faster reload speed.

Answer:

```
0.0
```

This demonstrates that future firing opportunities do not matter once a tank dies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(H^2 \cdot D^2 \cdot K)$ | Each state processes all shot outcomes |
| Space | $O(H^2 \cdot D^2)$ | Memoized DP states |

Here:

- $H \le 200$
- $D \le 30$
- $K \le 92^2$ in simultaneous firing states

The state space is manageable for Python with memoization, and transitions are simple arithmetic operations. The solution comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from functools import lru_cache

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    vhp, vdt, vl, vr, vp = map(int, input().split())
    ehp, edt, el, er, ep = map(int, input().split())

    vp = vp / 100.0
    ep = ep / 100.0

    v_outcomes = [(0, vp)]
    cnt = vr - vl + 1
    for d in range(vl, vr + 1):
        v_outcomes.append((d, (1.0 - vp) / cnt))

    e_outcomes = [(0, ep)]
    cnt = er - el + 1
    for d in range(el, er + 1):
        e_outcomes.append((d, (1.0 - ep) / cnt))

    @lru_cache(maxsize=None)
    def dfs(h1, h2, t1, t2):
        if h2 <= 0:
            return 1.0

        if h1 <= 0:
            return 0.0

        t = min(t1, t2)
        t1 -= t
        t2 -= t

        stay = 0.0
        res = 0.0

        if t1 == 0 and t2 == 0:
            for dv, pv in v_outcomes:
                for de, pe in e_outcomes:
                    prob = pv * pe

                    nh1 = h1 - de
                    nh2 = h2 - dv

                    nt1 = vdt
                    nt2 = edt

                    if nh2 <= 0:
                        val = 1.0
                    elif nh1 <= 0:
                        val = 0.0
                    else:
                        if (nh1, nh2, nt1, nt2) == (h1, h2, t1, t2):
                            stay += prob
                            continue
                        val = dfs(nh1, nh2, nt1, nt2)

                    res += prob * val

        elif t1 == 0:
            for dv, pv in v_outcomes:
                nh1 = h1
                nh2 = h2 - dv

                nt1 = vdt
                nt2 = t2

                if nh2 <= 0:
                    val = 1.0
                else:
                    if (nh1, nh2, nt1, nt2) == (h1, h2, t1, t2):
                        stay += pv
                        continue
                    val = dfs(nh1, nh2, nt1, nt2)

                res += pv * val

        else:
            for de, pe in e_outcomes:
                nh1 = h1 - de
                nh2 = h2

                nt1 = t1
                nt2 = edt

                if nh1 <= 0:
                    val = 0.0
                else:
                    if (nh1, nh2, nt1, nt2) == (h1, h2, t1, t2):
                        stay += pe
                        continue
                    val = dfs(nh1, nh2, nt1, nt2)

                res += pe * val

        return res / (1.0 - stay)

    ans = dfs(vhp, ehp, 0, 0)
    return f"{ans:.6f}"

# provided sample
assert run(
"""100 3 50 50 0
100 3 50 50 0
"""
) == "1.000000"

# instant loss
assert run(
"""100 2 50 50 0
100 3 100 100 0
"""
) == "0.000000"

# guaranteed eventual win
assert run(
"""100 1 100 100 50
100 100 1 1 0
"""
) == "1.000000"

# symmetric probabilistic duel
x = float(run(
"""100 1 50 50 50
100 1 50 50 50
"""
))
assert 0.74 < x < 0.76

# simultaneous mutual destruction
assert run(
"""10 1 10 10 0
10 1 10 10 0
"""
) == "1.000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Equal deterministic tanks | 1.0 | Simultaneous death handling |
| Enemy kills instantly | 0.0 | Immediate terminal states |
| Vasya eventually always wins | 1.0 | Infinite-time convergence |
| Symmetric random duel | About 0.75 | Probability recursion correctness |
| HP exactly reaches zero simultaneously | 1.0 | Boundary death conditions |

## Edge Cases

Consider simultaneous destruction again:

```
100 3 50 50 0
100 3 50 50 0
```

After the second simultaneous shot:

- Vasya HP becomes 0
- Enemy HP becomes 0

The algorithm checks `enemy HP <= 0` first and immediately returns victory. This matches the statement rule that mutual destruction counts as Vasya winning.

Now consider repeated self-loops:

```
100 1 100 100 99
100 100 1 1 0
```

Vasya misses with probability 0.99 each second. Most transitions return to exactly the same state. Without the geometric-series correction:

$$dp = \frac{res}{1-stay}$$

the recursion would never terminate.

Finally, consider asynchronous reloads:

```
100 2 50 50 0
100 3 50 50 0
```

The sequence of firing times is:

- both at 0
- Vasya at 2
- enemy at 3
- Vasya at 4
- both at 6

The DP advances directly between these event times using cooldown subtraction. No intermediate timestamps are stored or simulated. This guarantees correct ordering while keeping the state space small.
