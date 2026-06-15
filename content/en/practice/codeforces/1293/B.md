---
title: "CF 1293B - JOE is on TV!"
description: "The game can be seen as a process where we start with n opponents and repeatedly trigger rounds that remove some of them."
date: "2026-06-16T04:35:47+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1293
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 614 (Div. 2)"
rating: 1000
weight: 1293
solve_time_s: 565
verified: false
draft: false
---

[CF 1293B - JOE is on TV!](https://codeforces.com/problemset/problem/1293/B)

**Rating:** 1000  
**Tags:** combinatorics, greedy, math  
**Solve time:** 9m 25s  
**Verified:** no  

## Solution
## Problem Understanding

The game can be seen as a process where we start with `n` opponents and repeatedly trigger rounds that remove some of them. In each round, if there are `s` opponents still in the game and exactly `t` of them fail the current question, JOE earns `t/s` dollars and those `t` eliminated players are removed permanently. The remaining `s - t` continue to the next round.

The key freedom is that we can decide how many opponents fail in each round, as long as it is between `0` and the current number of survivors. The process ends when no opponents remain.

The goal is to choose a sequence of eliminations that maximizes the total money JOE earns.

The constraint `n ≤ 100000` means any solution that tries to simulate all possible ways of distributing eliminations across rounds is infeasible. A naive search over choices of `t` at each state branches heavily and quickly becomes exponential. Even a quadratic dynamic programming over all possible remaining states would be too slow.

The output is a real number, so we also need a stable way to compute a sum that may involve up to `n` fractional terms.

A few edge situations matter for correctness. When `n = 1`, there is only one opponent, and the only meaningful action is to eliminate them in a single round, giving reward `1/1 = 1`. Any reasoning that assumes multiple rounds or splits incorrectly would break here. Another subtle failure case appears when one assumes it is beneficial to eliminate many opponents at once. For example, taking all `n` at once yields reward `n/n = 1`, which looks good locally but ignores future rounds entirely.

## Approaches

A brute-force view treats each state `s` as a choice: pick any `t` from `1` to `s`, gain `t/s`, and move to `s - t`. This forms a decision tree. While correct in principle, it explodes because each state branches into up to `s` possibilities, leading to an enormous number of sequences even for moderate `n`.

The key simplification comes from comparing how reward accumulates when we split eliminations across multiple rounds versus grouping them into one. Suppose at some state `s` we eliminate `k` opponents. Doing it in one round gives `k/s`. If instead we eliminate them one by one in separate rounds, the contribution becomes `1/s + 1/(s-1) + ... + 1/(s-k+1)`, which is strictly larger because each denominator decreases while numerators stay `1`.

This means that concentrating eliminations into a large batch is always worse than spreading them out into single eliminations. So the optimal strategy is forced: in every round we eliminate exactly one opponent.

Once that is fixed, the process becomes deterministic. Starting from `n`, we go to `n-1`, then `n-2`, and so on until `1`, accumulating a simple sum of reciprocals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over elimination choices | Exponential | O(n) recursion | Too slow |
| Optimal harmonic strategy | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal Strategy

1. Start with `s = n` and total reward `ans = 0`. This represents the number of opponents still in the game and the accumulated money.
2. At each step, decide to eliminate exactly one opponent, meaning `t = 1`. This is the smallest possible non-zero elimination, and any larger batch would be suboptimal because it would use a larger denominator earlier.
3. Add the reward `1/s` to the answer. This reflects that exactly one opponent is removed out of `s` remaining.
4. Decrease `s` by one, since exactly one opponent has been eliminated.
5. Repeat until `s` becomes zero. At that point all opponents have been eliminated and the process stops.

### Why it works

The core property is that splitting any elimination of size `k` into `k` separate single eliminations always increases total reward because each subsequent fraction uses a smaller denominator. This creates a forced structure: any optimal solution can be transformed into one where every round removes exactly one opponent without decreasing the answer. Under this structure, the sequence of states is uniquely `n, n-1, ..., 1`, so the total reward is fixed and maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

ans = 0.0
for i in range(1, n + 1):
    ans += 1.0 / i

print(ans)
```

The implementation directly computes the harmonic sum from `1` to `n`. Iterating upward or downward is equivalent; here we sum `1/i` for clarity.

The key subtlety is using floating-point division. Since the required precision is `1e-4`, standard double precision accumulation is sufficient for `n` up to `10^5`.

## Worked Examples

### Example 1: `n = 3`

We compute the sum step by step.

| Step | s | Contribution | Total |
| --- | --- | --- | --- |
| 1 | 3 | 1/3 | 0.3333 |
| 2 | 2 | 1/2 | 0.8333 |
| 3 | 1 | 1/1 | 1.8333 |

The final answer is `1 + 1/2 + 1/3 = 1.8333...`. This shows how each step corresponds to eliminating exactly one opponent.

### Example 2: `n = 5`

| Step | s | Contribution | Total |
| --- | --- | --- | --- |
| 1 | 5 | 1/5 | 0.2 |
| 2 | 4 | 1/4 | 0.45 |
| 3 | 3 | 1/3 | 0.7833 |
| 4 | 2 | 1/2 | 1.2833 |
| 5 | 1 | 1/1 | 2.2833 |

This confirms the deterministic structure: every state contributes exactly the reciprocal of its size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We compute a single summation over all integers from 1 to n |
| Space | O(1) | Only a constant number of variables are used |

The linear scan over at most `10^5` values easily fits within the time limit, and memory usage is constant.

## Test Cases

```python
import sys, io

def solve():
    n = int(sys.stdin.readline())
    ans = 0.0
    for i in range(1, n + 1):
        ans += 1.0 / i
    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio
    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    sys.stdin = old_stdin
    return out.getvalue().strip()

# provided samples
assert abs(float(run("1")) - 1.0) < 1e-9

# custom cases
assert abs(float(run("2")) - (1 + 1/2)) < 1e-9
assert abs(float(run("3")) - (1 + 1/2 + 1/3)) < 1e-9
assert abs(float(run("10")) - sum(1/i for i in range(1, 11))) < 1e-9
assert abs(float(run("100000")) > 0)  # sanity check
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimal case |
| 2 | 1.5 | basic harmonic behavior |
| 3 | 1.8333… | multi-step accumulation |
| 100000 | large harmonic sum | performance and stability |

## Edge Cases

When `n = 1`, the algorithm performs exactly one addition `1/1`. Any approach that assumes at least one “choice” between different elimination sizes would fail here because there is no branching at all.

When `n` is large, such as `100000`, the sum grows slowly and depends on many small fractional contributions. Methods that try to simulate elimination sequences explicitly would exceed time limits, while the harmonic summation remains linear and stable.

When floating-point precision is considered, the accumulation order does not significantly affect correctness at the required tolerance, but mixing integer division or incorrect casting would immediately break results.
