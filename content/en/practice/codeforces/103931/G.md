---
title: "CF 103931G - Gua!"
description: "We are given a single weapon model described by two parameters and a replay of a match segment. The weapon deals at most $B$ damage per bullet and has a firing rate of $R$ rounds per minute. From this we can deduce how frequently bullets can be fired."
date: "2026-07-02T07:17:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103931
codeforces_index: "G"
codeforces_contest_name: "2022 Shanghai Collegiate Programming Contest"
rating: 0
weight: 103931
solve_time_s: 49
verified: true
draft: false
---

[CF 103931G - Gua!](https://codeforces.com/problemset/problem/103931/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single weapon model described by two parameters and a replay of a match segment. The weapon deals at most $B$ damage per bullet and has a firing rate of $R$ rounds per minute. From this we can deduce how frequently bullets can be fired. The replay tells us that the player accumulated a total damage value $D$ during a time interval of $S$ seconds, measured from the moment the first bullet is fired to the moment the last bullet lands.

The task is not to simulate the fight, but to decide whether the reported damage is physically possible under the weapon’s firing constraints. If the damage exceeds what any valid sequence of shots could produce, we must output that the player is certainly cheating.

The key constraint is the firing rate. If $R > 0$, the minimum time between two bullets is $60 / R$ seconds. This implies a maximum number of bullets that can be fired in a given time window. If $R = 0$, the weapon cannot fire at all, so any positive damage immediately implies cheating unless damage is zero.

The subtlety is how to interpret the time window $S$. Since it is defined as the time from the first bullet to the last bullet, the number of shots $k$ satisfies that the last shot happens at time $S$, but the first shot is at time $0$. Thus, $k$ bullets require $k - 1$ intervals, each at least $60 / R$, meaning:

$$(k - 1) \cdot \frac{60}{R} \le S$$

so:

$$k \le \left\lfloor \frac{S \cdot R}{60} \right\rfloor + 1$$

Edge cases matter heavily. If $R = 0$, then $k = 0$ unless no damage is dealt. If $S = 0$, the window allows only a single shot, because first and last bullet coincide in time.

A naive approach that tries to enumerate all possible firing sequences or simulate per-millisecond shooting would be unnecessary and error-prone, but more importantly, it would struggle with interpreting floating-point cooldowns correctly.

Another common pitfall is ignoring that damage per bullet is capped at $B$, but real damage could be less per bullet. However, since we are only checking if the damage is achievable, we assume best case: every bullet deals $B$ damage, so the minimum number of bullets needed is:

$$\left\lceil \frac{D}{B} \right\rceil$$

So the problem reduces to checking whether:

$$\left\lceil \frac{D}{B} \right\rceil \le \text{max bullets allowed by firing rate and time}$$

with special handling for zero cases.

## Approaches

A brute-force interpretation would attempt to simulate shot timings. We could iterate time in small increments, schedule shots whenever cooldown allows, and accumulate damage. This is conceptually correct, but it introduces unnecessary complexity and precision issues. With $S$ up to 2000 seconds and RPM up to 2000, the simulation might need to consider thousands of potential firing events per test case, and with up to $10^3$ test cases this becomes inefficient and fragile.

The key observation is that we do not need to simulate time at all. The firing constraint directly translates into a simple bound on the number of shots in an interval. Similarly, the damage constraint reduces to a lower bound on required shots. Once both quantities are expressed as integers, the problem becomes a direct comparison.

So instead of modeling gameplay, we convert the physics into two integers: maximum possible bullets and minimum required bullets. If the required number exceeds the maximum, cheating is guaranteed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation | O(T · S · R) | O(1) | Too slow / fragile |
| Direct math | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read $B, R, D, S$. These define damage per bullet, fire rate, total damage, and time window.
2. If $R = 0$, the weapon cannot fire. In this case, if $D > 0$, output “gua!” because any damage is impossible. Otherwise output “ok”.
3. If $B = 0$, each bullet deals no damage. If $D > 0$, it is impossible regardless of shots, so output “gua!”. If $D = 0$, it is always valid.
4. Compute the minimum number of bullets needed to reach damage $D$. Since each bullet contributes at most $B$, this is:

$$\text{need} = \left\lceil \frac{D}{B} \right\rceil$$

This ensures we assume optimal damage per bullet.

1. Compute the maximum number of bullets allowed by the firing rate in $S$ seconds. Each shot requires $60 / R$ seconds of cooldown after the first. Rearranging gives:

$$\text{max} = \left\lfloor \frac{S \cdot R}{60} \right\rfloor + 1$$

This accounts for the first bullet at time zero.

1. If $\text{need} > \text{max}$, output “gua!”, otherwise output “ok”.

### Why it works

The algorithm compresses all valid firing sequences into a single constraint: the number of shots is bounded by time and rate, independent of exact timing. Any valid sequence corresponds to a non-decreasing sequence of shot times with fixed minimum gaps, and such sequences are fully characterized by how many shots fit into the interval. On the other side, damage accumulation is maximized by assigning full $B$ damage to each shot, so feasibility depends only on whether enough shots can exist to reach $D$. Since both constraints become tight integer bounds, comparing them is sufficient to determine feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        B, R, D, S = map(int, input().split())

        if D == 0:
            print("ok")
            continue

        if R == 0 or B == 0:
            print("gua!")
            continue

        need = (D + B - 1) // B
        max_shots = (S * R) // 60 + 1

        if need > max_shots:
            print("gua!")
        else:
            print("ok")

if __name__ == "__main__":
    solve()
```

The implementation follows the derived constraints directly. The ceiling division `(D + B - 1) // B` computes required bullets safely without floating point operations. The maximum shots formula uses integer arithmetic throughout, avoiding precision issues. Special cases for $R = 0$ and $B = 0$ are handled early to prevent invalid arithmetic.

## Worked Examples

Consider the first sample input: $B = 38, R = 156, D = 152, S = 1$.

We compute required bullets as $\lceil 152 / 38 \rceil = 4$. The firing rate allows:

$$\left\lfloor \frac{1 \cdot 156}{60} \right\rfloor + 1 = 2 + 1 = 3$$

Since 4 exceeds 3, the output is “gua!”.

| Step | Value |
| --- | --- |
| D | 152 |
| B | 38 |
| need | 4 |
| max_shots | 3 |
| decision | gua |

This shows a classic violation where damage implies more shots than physically possible in the time window.

Now consider a valid case: $B = 99, R = 51, D = 9, S = 10$.

Required bullets:

$$\lceil 9 / 99 \rceil = 1$$

Maximum shots:

$$\left\lfloor \frac{10 \cdot 51}{60} \right\rfloor + 1 = 8 + 1 = 9$$

| Step | Value |
| --- | --- |
| D | 9 |
| B | 99 |
| need | 1 |
| max_shots | 9 |
| decision | ok |

This confirms that when damage is small relative to per-shot capacity, constraints are trivially satisfied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case requires constant-time arithmetic operations |
| Space | O(1) | No extra storage beyond variables |

The constraints allow up to $10^3$ test cases, so a linear scan is easily fast enough. All operations are integer arithmetic, making the solution both efficient and numerically safe.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        B, R, D, S = map(int, input().split())

        if D == 0:
            out.append("ok")
            continue

        if R == 0 or B == 0:
            out.append("gua!")
            continue

        need = (D + B - 1) // B
        max_shots = (S * R) // 60 + 1

        out.append("gua!" if need > max_shots else "ok")

    return "\n".join(out)

# provided samples
assert run("1\n38 156 152 1\n") == "gua!"
assert run("1\n280 25 280 0\n") == "ok"

# custom cases
assert run("1\n0 0 1 1\n") == "gua!"          # no damage possible
assert run("1\n10 60 0 5\n") == "ok"          # zero damage always ok
assert run("1\n5 60 100 1\n") == "gua!"       # impossible damage burst
assert run("1\n10 60 10 0\n") == "ok"         # single instant shot
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| R = 0 with D > 0 | gua! | no firing possible |
| D = 0 | ok | trivial feasibility |
| high damage, small S | gua! | rate limit violation |
| S = 0 boundary | ok/gua! correctness | single-shot window behavior |

## Edge Cases

When $R = 0$, the algorithm immediately classifies any positive damage as impossible. This avoids dividing by zero or incorrectly assuming some implicit firing capability. For example, input $B=99, R=0, D=1, S=10$ leads directly to “gua!”, since no bullets can be fired.

When $S = 0$, the formula still works correctly because $(S \cdot R) // 60 + 1 = 1$, meaning only one bullet can exist in the timeline. If $D$ requires more than one bullet, the inequality fails naturally.

When $B = 0$, the required damage becomes impossible to achieve unless $D = 0$, since no finite number of zero-damage bullets can reach a positive target. The early check prevents invalid ceiling division.

These cases show that all pathological inputs collapse cleanly into integer comparisons without needing special simulation logic.
