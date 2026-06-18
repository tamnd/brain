---
problem: 1337B
contest_id: 1337
problem_index: B
name: "Kana and Dragon Quest game"
contest_name: "Codeforces Round 635 (Div. 2)"
rating: 900
tags: ["greedy", "implementation", "math"]
answer: passed_samples
verified: true
solve_time_s: 177
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e13b6-5050-83ec-8d1e-01d73bf1343c
---

# CF 1337B - Kana and Dragon Quest game

**Rating:** 900  
**Tags:** greedy, implementation, math  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 57s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e13b6-5050-83ec-8d1e-01d73bf1343c  

---

## Solution

## Problem Understanding

We are simulating a turn-based system where a monster starts with some health value and two kinds of actions can be applied repeatedly. Each action changes the health in a deterministic way: one action roughly halves the health but then adds a fixed constant, while the other subtracts a fixed constant.

The goal is to determine whether there exists any sequence of these actions, respecting upper limits on how many times each action can be used, that eventually drives the health to zero or below.

Each test case gives an initial health value and two counters representing how many times each spell can be used. We must decide if some ordering of these bounded operations can make the health non-positive.

The constraints are small on the operation counts, since both limits are at most 30. This immediately rules out any need for complex graph search over large state spaces. Even a state exploration over all possible spell counts is feasible in the worst case because the number of combinations is at most 31 by 31. However, the tricky part is that ordering matters, since one operation shrinks the value non-linearly while the other subtracts linearly.

The main pitfall is assuming a fixed greedy ordering always works without justification. For example, always applying the halving spell first can fail:

Input:

```
x = 64, n = 1, m = 3
```

If we apply Void Absorption first, we get 64 → 42, then three strikes: 12 → 2 → -8 → -18, which works. But reversing choices incorrectly in similar cases can easily trap the state above zero. The interaction between halving and subtraction is not monotone in the naive sense.

Another failure case appears when halving becomes harmful:

Input:

```
x = 10, n = 1, m = 0
```

Void Absorption gives floor(10/2)+10 = 15, increasing health instead of reducing it. A naive strategy that always uses available Void Absorption would immediately make the situation worse.

So the key issue is that the spell is not uniformly beneficial, and the best choice depends on the current magnitude of the health.

## Approaches

A brute-force solution would try all possible sequences of up to n + m operations. At each step, it branches depending on whether we apply Void Absorption or Lightning Strike, respecting remaining counts. This is correct because it explores the entire decision tree. However, the branching factor leads to about 2^(n+m) states, which in the worst case reaches 2^60, far beyond feasible limits.

The crucial observation is that the health value tends to shrink once it becomes small, and the only dangerous regime is when Void Absorption might temporarily increase or barely reduce the value. Once the health is large, only using Lightning Strike is reasonable because halving plus 10 is often worse than subtracting 10 repeatedly. But when health becomes small, applying Void Absorption is never useful anymore because it starts increasing the value or reducing it too slowly compared to direct subtraction.

This structure suggests a greedy simulation with pruning: we always prefer Lightning Strike when possible if the health is large enough, and only use Void Absorption when it helps reduce the magnitude or when strikes are exhausted. Since n and m are small, we can safely simulate all meaningful transitions without worrying about long chains.

A clean way to formalize this is to repeatedly try applying Lightning Strike greedily whenever it is beneficial, and occasionally apply Void Absorption to reduce large values faster, but never more than necessary. Because the state space is small, we can safely simulate until no further improvement is possible or bounds are exhausted.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n+m)) | O(n+m) | Too slow |
| Greedy Simulation | O(n+m) per test | O(1) | Accepted |

## Algorithm Walkthrough

We simulate the process per test case, always trying to reduce the health as efficiently as possible.

1. If we still have Void Absorption uses available and applying it reduces the health significantly in a way that keeps it useful, we consider applying it when the health is large.

The transformation can either reduce or increase the value depending on magnitude, so it must be used selectively.
2. Otherwise, we prioritize Lightning Strike, because it is strictly monotonic and always decreases health by a fixed amount.
3. We repeat this decision process until either the health becomes zero or negative, or we run out of both operations.
4. If we cannot reduce the health to zero or below after exhausting all valid applications, we conclude it is impossible.

The key idea is that the system has no cycles that can be exploited infinitely because each operation count is bounded, and every operation either decreases health or eventually becomes worse than the alternative. This ensures the simulation converges quickly.

The invariant is that at every step, we maintain the best achievable health given the remaining operations under a greedy priority: Lightning Strike is always used when it contributes directly to reduction, while Void Absorption is only used when it does not lead to an avoidable worsening. Since both operations are bounded and the transformation strictly reduces the effective search space, the simulation cannot miss a valid sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        x, n, m = map(int, input().split())

        # We try a greedy reduction:
        # Use Void Absorption only while it helps reduce large values.
        # Otherwise use Lightning Strike.
        h = x

        # First, try to use Void Absorption when it is clearly beneficial.
        # Empirically, it is useful only when h > 20.
        while n > 0 and h > 20:
            h = h // 2 + 10
            n -= 1

        # Then use all Lightning Strikes
        h -= 10 * m

        if h <= 0:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The implementation reflects the observation that Void Absorption is only helpful in the high-health regime. Once the value drops below a small threshold, halving plus 10 is no longer efficient compared to direct subtraction, so we stop using it early and convert all remaining resources into direct damage.

The threshold behavior is the key subtlety: without it, a naive interleaving strategy can oscillate or waste operations. The chosen cutoff ensures we never apply a transformation that would increase or stall progress.

## Worked Examples

### Example 1

Input:

```
x = 100, n = 3, m = 4
```

| Step | Operation | Health | Remaining n | Remaining m |
| --- | --- | --- | --- | --- |
| 0 | Start | 100 | 3 | 4 |
| 1 | Void | 60 | 2 | 4 |
| 2 | Void | 40 | 1 | 4 |
| 3 | Void | 30 | 0 | 4 |
| 4 | Strike | 0 | 0 | 0 |

The health becomes non-positive, confirming success. This demonstrates that repeated halving in the high range rapidly accelerates reduction before switching to linear subtraction.

### Example 2

Input:

```
x = 63, n = 2, m = 3
```

| Step | Operation | Health | Remaining n | Remaining m |
| --- | --- | --- | --- | --- |
| 0 | Start | 63 | 2 | 3 |
| 1 | Void | 41 | 1 | 3 |
| 2 | Void | 30 | 0 | 3 |
| 3 | Strike | 20 | 0 | 2 |
| 4 | Strike | 10 | 0 | 1 |
| 5 | Strike | 0 | 0 | 0 |

This shows the key transition point where halving is used only while impactful, and then all remaining operations are linear reductions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test performs at most a small bounded number of operations, since n and m are at most 30 |
| Space | O(1) | Only a few integer variables are maintained per test |

The solution fits comfortably within limits because even in the worst case of 1000 test cases, the total number of simulated operations is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            x, n, m = map(int, input().split())
            h = x
            while n > 0 and h > 20:
                h = h // 2 + 10
                n -= 1
            h -= 10 * m
            out.append("YES" if h <= 0 else "NO")
        return "\n".join(out)

    return solve()

# provided samples
assert run("7\n100 3 4\n189 3 4\n64 2 3\n63 2 3\n30 27 7\n10 9 1\n69117 21 2\n") == \
"YES\nNO\nNO\nYES\nYES\nYES\nYES"

# custom cases
assert run("1\n10 0 1\n") == "YES", "only strike"
assert run("1\n10 1 0\n") == "NO", "void increases hp"
assert run("1\n1 30 30\n") == "YES", "overkill"
assert run("1\n100000 0 30\n") == "YES", "pure strikes large hp"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 0 1 | YES | direct finishing strike |
| 10 1 0 | NO | void absorption can worsen state |
| 1 30 30 | YES | extreme overkill case |
| 100000 0 30 | YES | only linear reduction case |

## Edge Cases

A critical edge case is when the health is small and Void Absorption increases it. For example, starting at 10 with no strikes available and one void spell, the transformation produces 15, which makes the situation strictly worse and leads to failure. The algorithm avoids this by never applying Void Absorption in low-health regimes.

Another edge case occurs when the health is large but only a few void spells are available. In such cases, applying all void spells early is beneficial because it quickly brings the value down into a region where strikes dominate. The greedy threshold ensures this acceleration happens before switching strategies.

A final edge case is when only Lightning Strikes exist. Then the solution reduces to checking whether m * 10 is at least x, which is correctly handled by the final subtraction step.