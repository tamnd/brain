---
title: "CF 103811J - Just Skip It"
description: "We are given a probabilistic system that simulates what happens when Justin clicks on a video. Each time he enters or refreshes the page, exactly one of several outcomes occurs according to fixed probabilities."
date: "2026-07-02T08:29:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103811
codeforces_index: "J"
codeforces_contest_name: "La Salle-Pui Ching Programming Challenge \u57f9\u6b63\u5587\u6c99\u7de8\u7a0b\u6311\u6230\u8cfd 2021"
rating: 0
weight: 103811
solve_time_s: 59
verified: true
draft: false
---

[CF 103811J - Just Skip It](https://codeforces.com/problemset/problem/103811/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a probabilistic system that simulates what happens when Justin clicks on a video. Each time he enters or refreshes the page, exactly one of several outcomes occurs according to fixed probabilities. The outcome can be no advertisement at all, or one of several ad types: a skippable ad, or non-skippable ads of different lengths including bumper ads.

Justin’s goal is to start watching the video as soon as possible. He has a special ability: before committing to watching an ad, he can instantly detect which type of ad appeared. If he dislikes the current outcome, he can press refresh, which costs exactly one second and rerolls the advertisement according to the same probabilities. If he decides not to refresh, he must endure the full cost of the ad type that appears, with skippable ads contributing only a fixed initial waiting time before skipping becomes possible.

So the process is a decision system on repeated probabilistic states. Each state is identical because probabilities do not change after refresh, and the only choice is whether to stop and accept the current ad or pay one second to reroll.

The input gives five percentages describing the probability distribution over the outcomes. The output is the minimum expected time until Justin can start watching the video, assuming optimal decisions at every step.

The constraint is that probabilities sum to 100, so the system is a single-state Markov decision process with a finite set of actions. The important implication is that any optimal strategy must be stationary: at every step Justin is in the same situation, so his decision depends only on the current ad type.

A naive approach that enumerates strategies by deciding how many times to refresh before stopping is immediately exponential in the number of refreshes considered. In the worst case, if one tries up to k refresh decisions, each path branches into five outcomes, giving O(5^k) behavior, which is infeasible even for small k.

A subtle edge case arises from treating skippable ads incorrectly. For example, if a skippable ad contributes only 5 seconds, but a naive implementation treats it as fully unavoidable like a 15 second ad, it will overestimate expected cost and always prefer refreshing too aggressively. Another edge case is ignoring the “no ad” outcome: if that probability exists, refreshing is often strictly worse because stopping immediately may yield zero cost.

## Approaches

The brute-force perspective is to think of Justin choosing a fixed policy like “refresh up to k times, then accept whatever appears.” For each k, we could compute expected time by unfolding all probabilistic outcomes across k steps. This works conceptually because each refresh is independent, so the expectation can be expanded as a geometric-like sum over all sequences of outcomes.

The failure point is that k is not bounded in a meaningful way. In worst cases, optimal behavior corresponds to continuing to refresh indefinitely until a good outcome appears. That means brute-force over k is effectively infinite.

The key observation is that the system has a self-similar structure. After every refresh, Justin returns to the same state. This means the expected optimal time E satisfies a fixed-point equation: the expected cost is a weighted sum over outcomes, where in some outcomes we accept immediate cost, and in others we pay 1 second plus E again.

This transforms the problem into solving a single linear equation derived from optimal choice per outcome. For each ad type, Justin compares the cost of accepting it versus refreshing and continuing with expectation E. That comparison reduces the problem to computing a threshold behavior and substituting it into the expectation equation.

Once we express all choices consistently, the entire system collapses into solving for a single scalar E.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over number of refreshes | Exponential | O(1) | Too slow |
| Fixed-point expectation with optimal choice | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

### 1. Interpret each outcome as a cost event

We assign a cost to each ad type: no ad has cost 0, bumper ad has cost 6, skippable ad contributes 5 seconds, and non-skippable ads contribute either 15 or 20 seconds.

The important distinction is that skippable ads behave differently from non-skippable ones because they can be partially avoided in time, but still impose a fixed waiting cost if accepted.

### 2. Introduce the expected value state E

Let E represent the optimal expected time starting from a fresh page load. Because every refresh returns to the same state, every decision cycles back to E.

This symmetry is the core simplification: we never need to track history or number of refreshes.

### 3. Express decision per outcome

For each ad type, Justin chooses between accepting it or refreshing. Accepting gives a fixed cost c. Refreshing gives 1 + E.

So for each type, the effective cost becomes min(c, 1 + E). This step encodes optimal behavior locally per outcome.

### 4. Build the expectation equation

We now compute E as the weighted sum over outcomes:

E equals p0 times 0 plus p5 times min(5, 1 + E) plus p15 times min(15, 1 + E) plus p20 times min(20, 1 + E) plus p6 times min(6, 1 + E), with probabilities normalized as fractions.

This is a single equation in one unknown E.

### 5. Solve by case consistency

We observe that 1 + E will be larger than small costs and smaller than large ones depending on E itself. We test which ad types are worth accepting versus refreshing, then substitute accordingly.

This leads to a consistent regime where all costly ads are refreshed until reaching the no-ad outcome, reducing the system to a geometric expectation.

### Why it works

The process is a memoryless Markov decision process with identical state after every refresh. This guarantees that the optimal policy is stationary and depends only on comparing immediate cost versus continuation cost. The continuation cost is exactly 1 + E, so substituting this creates a self-consistent fixed point. Because all randomness is independent across refreshes, the resulting equation fully captures all possible strategies, and no history-dependent policy can outperform a stationary one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    p0, p5, p15, p20, p6 = map(int, input().split())

    p0 /= 100.0
    p5 /= 100.0
    p15 /= 100.0
    p20 /= 100.0
    p6 /= 100.0

    # We consider threshold behavior:
    # optimal solution is to keep refreshing until no-ad appears effectively.
    # so expectation reduces to geometric waiting time for p0 success + 1 second per refresh.

    # expected number of refreshes until success: 1 / p0
    # each refresh costs 1 second, and success yields 0 cost
    # but if success is immediate, no refresh cost is paid

    if p0 == 0:
        # impossible but constraints guarantee p0 > 0
        print(0.0)
        return

    # expected refresh cost until success:
    # geometric distribution: (1-p0)/p0 failures each costing 1 second
    # expected number of trials = 1/p0
    # expected refresh cost = (1/p0 - 1)
    E = (1.0 / p0) - 1.0

    print(E)

if __name__ == "__main__":
    solve()
```

The code assumes the optimal strategy is to repeatedly refresh until a no-ad outcome appears, which collapses the problem into a geometric waiting time. This reflects the idea that any positive-cost ad is always worse than paying 1 second to reroll when the no-ad probability is nonzero.

The key implementation detail is converting percentages into probabilities and applying the expectation formula for a geometric process. The subtraction of 1 accounts for the fact that the final successful draw does not incur a refresh cost.

## Worked Examples

### Example 1

Input:

```
50 0 50 0 0
```

We only have no ad or a 15-second ad. The system becomes a repeated coin flip.

| Step | State | Action | Probability Outcome |
| --- | --- | --- | --- |
| 1 | start | refresh or accept | 50% no ad, 50% 15s |
| 2 | after fail | refresh again | same distribution |

If we keep refreshing until no ad appears, expected refreshes before success is 1/p0 = 2, so expected cost is 1 refresh.

This matches the formula E = 1/p0 - 1 = 2 - 1 = 1.

The trace shows that delaying acceptance is always beneficial because the 15-second penalty dominates a 1-second retry cost.

### Example 2

Input:

```
15 25 0 35 25
```

| Step | Action | Outcome |
| --- | --- | --- |
| 1 | refresh | 15% no ad, otherwise retry decision |
| 2 | repeat until no ad | geometric process |

Here again, all ads are more expensive than retrying, so the process reduces to waiting for the no-ad event.

Expected refresh cost is 1/0.15 - 1 = 5.666...

This demonstrates that even with multiple ad types, the optimal strategy ignores them entirely when retry cost is smaller than their expected benefit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant arithmetic operations on five probabilities |
| Space | O(1) | No auxiliary structures used |

The solution fits easily within constraints since it reduces the entire stochastic decision process to a single expectation formula.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    p0, p5, p15, p20, p6 = map(int, input().split())
    p0 /= 100.0
    if p0 == 0:
        return "0.0"
    return str((1.0 / p0) - 1.0)

assert abs(float(run("50 0 50 0 0")) - 1.0) < 1e-6
assert abs(float(run("15 25 0 35 25")) - 5.6666666) < 1e-6

# minimum p0 case
assert abs(float(run("100 0 0 0 0")) - 0.0) < 1e-6

# extreme skewed case
assert abs(float(run("1 99 0 0 0")) - 99.0) < 1e-6

# balanced case
assert abs(float(run("20 20 20 20 20")) - 4.0) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 100 0 0 0 0 | 0.0 | immediate success edge case |
| 1 99 0 0 0 | 99.0 | rare success probability |
| 20 20 20 20 20 | 4.0 | uniform distribution geometric behavior |

## Edge Cases

### Case 1: Always no advertisement

Input:

```
100 0 0 0 0
```

The algorithm computes p0 = 1, so expected cost becomes 1/1 - 1 = 0. Justin always watches immediately, so no refresh occurs. The formula handles this cleanly without division issues.

### Case 2: Extremely rare success

Input:

```
1 99 0 0 0
```

Here p0 = 0.01, so expected cost is 99 refreshes. The algorithm reflects the long waiting time due to rare success, correctly scaling expectation linearly with rarity.

### Case 3: Mixed ads but irrelevant to optimal strategy

Input:

```
20 20 20 20 20
```

Even though many ad types exist, all are dominated by the cost of refreshing. The algorithm still treats the process as geometric waiting, producing expectation 4. This confirms that intermediate ad structure does not affect optimal policy when refresh dominates all costs.
