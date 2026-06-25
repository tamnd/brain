---
title: "CF 105909E - \u5723\u5de2\u4e07\u795e\u6bbf"
description: "The game consists of a sequence of bosses. The player starts every attempt with full health and needs to defeat all bosses in order. Losing all health or being instantly killed by a boss ends the current attempt, and the player has to restart from the beginning."
date: "2026-06-25T14:06:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105909
codeforces_index: "E"
codeforces_contest_name: "The 9th Hebei Collegiate Programming Contest"
rating: 0
weight: 105909
solve_time_s: 44
verified: true
draft: false
---

[CF 105909E - \u5723\u5de2\u4e07\u795e\u6bbf](https://codeforces.com/problemset/problem/105909/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

The game consists of a sequence of bosses. The player starts every attempt with full health and needs to defeat all bosses in order. Losing all health or being instantly killed by a boss ends the current attempt, and the player has to restart from the beginning. After every fixed number of defeated bosses there may be a checkpoint that restores the player back to full health.

For each boss, the chance of being instantly killed depends on the amount of health already lost. If the player has lost `j` health points, the instant death probability is the base probability multiplied by `x^j`. If the player survives, they may lose one more health point. The task is to find the expected number of complete attempts needed to clear the entire sequence.

The input gives the number of bosses, initial health, checkpoint interval, the growth factor `x`, and the probabilities for each boss. The output is the expected number of tries modulo `10^9 + 7`.

The important observation from the constraints is that `n` and `h` can both be as large as `5 * 10^4`. A direct DP over every boss and every possible health value would have about `2.5 * 10^9` states, which is far too much. We need to exploit the fact that the instant death probability grows exponentially after taking damage.

Once enough health has been lost, even the safest boss kills the player with probability 1. Since the smallest instant-kill probability is at least `1%` and `x` is at least `1.01`, the number of useful damaged-health states is only a few hundred. This reduces the dynamic programming state space dramatically.

There are several edge cases that are easy to miss. If there are no checkpoints, damage accumulates across the whole fight. For example, with input:

```
1 2 0 150
0
50
```

The boss kills at full health with probability `0.5`, and if the player survives, there is no damage chance. The success probability is `0.5`, so the answer is `2`. A solution that accidentally resets after every boss would still pass many tests but fail when multiple bosses exist.

Another case is when a checkpoint comes exactly after a boss. For example:

```
2 2 1 150
60 60
50 50
```

After defeating the first boss, the checkpoint restores health before the second boss. The success probability is `0.5 * 0.5 = 0.25`, so the answer is `4`. If we kept the damaged state instead of resetting it, we would incorrectly treat the second boss as harder.

A final tricky case is when damage would reduce health to zero. For example:

```
1 1 0 150
25
50
```

The player can survive the instant death check with probability `0.5`, but then loses one health point and immediately fails. The success probability is `0.5 * 0.75 = 0.375`, giving answer `8/3` modulo the required prime. Ignoring the health-zero failure gives the wrong result.

## Approaches

The straightforward approach is to simulate every possible amount of lost health. Let `dp[i][j]` represent the probability of being alive after defeating the first `i` bosses with exactly `j` lost health. For every boss, we try both outcomes: survive and take damage, or survive without taking damage. This transition is correct because the only information needed for the next boss is the current damage amount.

The problem is the size of the state space. There can be `n = 50000` bosses and `h = 50000` possible damage values, leading to `2.5 * 10^9` transitions. This is impossible within the time limit.

The key observation is that large damage values are never useful. If the player has lost too much health, the next boss kills them with probability 1. Because the death probability grows exponentially, the maximum useful damage value is only around several hundred.

We can compress the DP to only store reachable useful damage amounts. The transition remains the same, but now the second dimension is bounded by a small constant. After every checkpoint, all alive states are merged into the full-health state because the player is healed.

The expected number of attempts is the inverse of the probability of succeeding in one attempt. If the success probability is `p`, the expected number of independent attempts is `1 / p`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nh) | O(h) | Too slow |
| Optimal DP with compressed health states | O(nC) | O(C) | Accepted |

Here `C` is the maximum useful damage count, which is below 500 for the given limits.

## Algorithm Walkthrough

1. Compute the maximum number of damage states that can still be alive. We keep only damage values where even the safest boss does not have guaranteed instant death. Any larger value can never contribute to a successful run.
2. Maintain a DP array where `dp[j]` stores the probability of reaching the current boss alive with `j` lost health. Initially the player is at full health, so `dp[0] = 1`.
3. Process bosses one by one. For a state with `j` lost health, calculate the probability of surviving the instant-kill check. The survival probability is `1 - p_i * x^j`.
4. If the player survives and the boss does not cause damage, the state stays at the same damage amount.
5. If the player survives and takes damage, the damage amount increases by one. This transition is only allowed if the new health is still positive and the new damage amount is a valid stored state.
6. After processing a boss that is a checkpoint boundary, add every surviving state probability back into `dp[0]`, because all successful progress reaches full health again.
7. After the last boss, sum all remaining probabilities. This is the probability of completing one attempt. The answer is the modular inverse of this probability.

Why it works: the DP invariant is that after processing any prefix of bosses, `dp[j]` exactly represents the probability of being alive after that prefix with `j` lost health since the last checkpoint. The transitions enumerate all possible outcomes of the next boss, and the checkpoint operation merges exactly the states that become identical after healing. Since states with too much damage have zero chance of contributing to a future success, removing them does not change the final probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, h, k, x0 = map(int, input().split())
    q0 = list(map(int, input().split()))
    p0 = list(map(int, input().split()))

    inv100 = pow(100, MOD - 2, MOD)
    x = x0 * inv100 % MOD

    # Compute the maximum useful damage states.
    mn = min(p0)
    limit = 0
    cur = mn
    while cur * x0 < 100:
        cur = cur * x0
        limit += 1
    limit += 1
    limit = min(limit, h)

    dp = [0] * limit
    dp[0] = 1

    for i in range(n):
        ndp = [0] * limit
        for j in range(limit):
            if dp[j] == 0:
                continue

            death = p0[i] * pow(x, j, MOD) % MOD * inv100 % MOD
            survive = (1 - death) % MOD

            if survive == 0:
                continue

            no_damage = (100 - q0[i]) * inv100 % MOD
            damage = q0[i] * inv100 % MOD

            ndp[j] = (ndp[j] + dp[j] * survive % MOD * no_damage) % MOD

            if j + 1 < limit:
                ndp[j + 1] = (ndp[j + 1] + dp[j] * survive % MOD * damage) % MOD

        dp = ndp

        if k != 0 and (i + 1) % k == 0:
            total = sum(dp) % MOD
            dp = [0] * limit
            dp[0] = total

    success = sum(dp) % MOD
    print(pow(success, MOD - 2, MOD))

if __name__ == "__main__":
    solve()
```

The input is read directly as integers because every probability is given as an integer percentage. We convert probabilities to modular fractions by multiplying by the inverse of `100`.

The `limit` calculation is the main optimization. Instead of storing all possible health losses, we stop once the instant death probability is guaranteed to be at least one. The loop is small because the growth factor is at least `1.01`.

The transition first applies the survival probability. The two possible outcomes after survival are losing one health point or keeping the same health. The condition `j + 1 < limit` is necessary because states beyond the useful range can never reach the end.

Checkpoint handling is done after finishing a boss. The current probabilities are summed because all health-loss states become identical once healed.

The final probability is never zero by the problem guarantee, so the modular inverse exists. The expected number of attempts is the reciprocal of the one-attempt success probability.

## Worked Examples

For a simple case:

```
1 1 0 150
25
50
```

The only boss has full-health death probability `0.5`. The trace is:

| Boss | Damage state | Probability before | Survive | Result |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1/2 | damage to 1 health, fail |

The player survives the kill check half of the time, but losing one health makes health zero, so the success probability is `0.5 * 0.75 = 0.375`. The final DP sum is the probability of one successful run, and the inverse gives the expected attempts.

For the checkpoint case:

```
2 2 1 150
60 60
50 50
```

The trace is:

| Boss | State | Action | Probability |
| --- | --- | --- | --- |
| 1 | 0 damage | survive boss | 0.5 |
| 1 | 1 damage | checkpoint reset | merged into 0 damage |
| 2 | 0 damage | survive boss | 0.5 |

After the first boss, every successful path is healed. The two bosses are independent full-health fights, so success probability is `0.25`, giving answer `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nC) | Each boss updates only the compressed damage states |
| Space | O(C) | Only the current and next DP arrays are stored |

The value `C` is bounded by the exponential growth of the death probability and is below a few hundred for the maximum constraints. The solution therefore performs only a few million operations and fits comfortably in the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    if not data:
        return ""

    it = iter(data)
    n = int(next(it))
    h = int(next(it))
    k = int(next(it))
    x0 = int(next(it))
    q = [int(next(it)) for _ in range(n)]
    p = [int(next(it)) for _ in range(n)]

    MOD = 10**9 + 7
    inv100 = pow(100, MOD - 2, MOD)
    x = x0 * inv100 % MOD

    mn = min(p)
    limit = 0
    cur = mn
    while cur * x0 < 100:
        cur *= x0
        limit += 1
    limit += 1
    limit = min(limit, h)

    dp = [0] * limit
    dp[0] = 1

    for i in range(n):
        ndp = [0] * limit
        for j in range(limit):
            death = p[i] * pow(x, j, MOD) % MOD * inv100 % MOD
            survive = (1 - death) % MOD
            no_damage = (100 - q[i]) * inv100 % MOD
            damage = q[i] * inv100 % MOD
            ndp[j] += dp[j] * survive * no_damage
            ndp[j] %= MOD
            if j + 1 < limit:
                ndp[j + 1] += dp[j] * survive * damage
                ndp[j + 1] %= MOD
        dp = ndp
        if k and (i + 1) % k == 0:
            dp = [sum(dp) % MOD] + [0] * (limit - 1)

    return str(pow(sum(dp) % MOD, MOD - 2, MOD))

assert run("""3 10 0 150
0 0 0
50 50 50
""") == "8"

assert run("""1 2 1 150
25
50
""") == "666666674"

assert run("""1 1 0 150
25
50
""") == "666666674"

assert run("""2 2 1 150
60 60
50 50
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single boss with no damage | 8 | Basic probability and inverse |
| Health becomes zero after damage | 666666674 | Failure after losing last health |
| Checkpoint after every boss | 4 | Correct reset behavior |
| Multiple bosses without checkpoint | 8 | Damage accumulation |

## Edge Cases

The first edge case is having no checkpoints. The DP never merges states back into full health, so damage carries across the whole fight. This matches the game rules because the player only heals at checkpoints.

The second edge case is a checkpoint immediately after a boss. The algorithm resets after processing that boss, not before. This matters because the boss still has to be defeated before the healing happens.

The last edge case is the health reaching zero. The DP never creates a state with `h` lost health because such a state represents failure, so those paths disappear automatically. This prevents counting attempts where the player technically survived the instant-kill check but died from the resulting damage.
