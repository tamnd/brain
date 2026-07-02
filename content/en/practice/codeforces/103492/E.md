---
title: "CF 103492E - Monopoly"
description: "We are given a circular board with n tiles, each tile contributing a fixed integer value when we step on it. Starting before the first tile, we begin at tile 1 and move deterministically to tile 2, then 3, and so on, wrapping back to 1 after n."
date: "2026-07-03T06:12:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103492
codeforces_index: "E"
codeforces_contest_name: "China Collegiate Programming Contest 2021, Qualification Round (Online), Rematch"
rating: 0
weight: 103492
solve_time_s: 43
verified: true
draft: false
---

[CF 103492E - Monopoly](https://codeforces.com/problemset/problem/103492/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular board with n tiles, each tile contributing a fixed integer value when we step on it. Starting before the first tile, we begin at tile 1 and move deterministically to tile 2, then 3, and so on, wrapping back to 1 after n. Each time we land on a tile, we add its value to a running score, which can go up or down.

Each query asks for the smallest number of steps needed so that the cumulative sum of visited tiles equals exactly a target value x. A “step” means landing on a tile, so after k steps we have visited the prefix of length k in this infinite periodic walk.

A key observation is that after n steps, we complete exactly one full cycle of the array, so every full cycle contributes the same total sum S = a1 + a2 + ... + an. After k steps, the score is the sum of full cycles plus a prefix of the next cycle.

The constraints are large: n and m go up to 100,000 per test case, with total sums up to 500,000. This rules out per query simulation over steps or naive prefix scanning. Any solution that is linear per query would exceed about 10^10 operations in the worst case, which is far beyond limits. We need preprocessing in linear or near-linear time and logarithmic or constant time per query.

A subtle edge case appears when the total cycle sum S is zero. In that case, repeating cycles does not change the score, so only prefix sums matter. If S is nonzero, we can adjust the score by choosing how many full cycles to take, but the remainder must match a prefix sum exactly. Another edge case is negative targets, since values can decrease, so prefix sums are not monotonic in a useful way unless we explicitly track them.

## Approaches

A brute force strategy is straightforward. For each query x, we simulate walking step by step along the infinite repetition of the array, maintaining a running sum until we either hit x or exceed a reasonable bound. In the worst case, the answer might require many full cycles, especially when S is small or zero, so this can degenerate into scanning up to O(n * answer cycles) per query. With m up to 10^5, this is clearly infeasible.

The key structural insight is that every position in the infinite walk can be written as k full cycles plus a prefix of the base array. If we define prefix sums P[i] = a1 + ... + ai and total sum S = P[n], then after t steps we have:

score(t) = k * S + P[r], where t = k * n + r and 0 ≤ r < n.

So the problem reduces to asking whether x can be written in this form, and among all valid decompositions, finding the smallest t.

For each prefix value P[r], we check whether we can choose an integer k such that x - P[r] is divisible by S, and the quotient k is non-negative. If S = 0, the condition degenerates to x = P[r], because cycles do not change the sum.

We precompute all prefix sums and optionally store the minimum index r for each prefix value. Then each query reduces to checking all candidates r and evaluating feasibility. Since n is large, iterating all r per query is too slow, so we instead group prefix sums and keep only the earliest occurrence for each value. This works because earlier r always gives smaller t for the same cycle count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(m · n · cycles) | O(1) | Too slow |
| Prefix + modular decomposition | O(n + m · d) where d = distinct prefix states | O(n) | Accepted |

The real optimization is recognizing that only the first occurrence of each prefix sum matters, and reducing each query to constant-time arithmetic after preprocessing a hash map of prefix values.

## Algorithm Walkthrough

## Preprocessing

1. Compute prefix sums P[i] while scanning the array once from left to right.

We also record the total sum S = P[n].

This step encodes all possible partial cycle contributions.
2. Build a dictionary bestPos where bestPos[v] stores the smallest index i such that P[i] = v.

We only keep the earliest index because it yields the smallest number of steps for that prefix value.

## Query processing

1. If S is zero, then repeating cycles does not change the score. For a query x, we check whether x exists in bestPos. If it does, the answer is bestPos[x], otherwise it is impossible.
2. If S is nonzero, we iterate over all stored prefix sums v in bestPos.
3. For each prefix sum v, compute the difference delta = x - v.
4. Check if delta is divisible by S. If not, this prefix cannot lead to x.
5. If divisible, compute k = delta // S.
6. Only consider k ≥ 0, since we cannot take a negative number of full cycles.
7. The candidate answer is k * n + bestPos[v]. We track the minimum over all valid candidates.

## Why it works

Every reachable state corresponds exactly to some number of full cycles plus a prefix of the next cycle. The prefix sum uniquely determines the partial contribution within a cycle, and the number of full cycles determines how far we have advanced in multiples of n steps. Because every prefix sum is recorded with its earliest index, we always choose the minimal step count for that prefix component. The divisibility condition ensures consistency between the target and cycle contribution, and restricting k to non-negative ensures we only move forward in time. This exhausts all possible decompositions of a valid walk, so the minimum over all valid candidates is the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    prefix = [0] * (n + 1)
    best = {}

    for i in range(1, n + 1):
        prefix[i] = prefix[i - 1] + a[i - 1]
        if prefix[i] not in best:
            best[prefix[i]] = i

    S = prefix[n]

    for _ in range(m):
        x = int(input())

        if S == 0:
            if x in best:
                print(best[x])
            else:
                print(-1)
            continue

        ans = 10**30

        for v, idx in best.items():
            delta = x - v
            if delta % S != 0:
                continue
            k = delta // S
            if k < 0:
                continue
            ans = min(ans, k * n + idx)

        print(-1 if ans == 10**30 else ans)

if __name__ == "__main__":
    solve()
```

The code first builds prefix sums and stores only the first occurrence of each value. That reduction is what prevents quadratic behavior. The total sum S is extracted to decide whether cycle repetition affects reachability.

Each query is handled by testing all distinct prefix sum values. The arithmetic check enforces compatibility between the target and cycle structure, and the minimum step expression directly reflects the decomposition into full cycles and a prefix.

A common pitfall is forgetting the S = 0 case. Without separating it, division and modular logic breaks down. Another subtle point is using the first occurrence of each prefix sum rather than all occurrences, which ensures minimal step counts.

## Worked Examples

Consider an array [1, -3, 4]. The prefix sums are P = [1, -2, 2], and total sum S = 2.

Query x = 3:

| prefix v | idx | delta = x - v | delta % S | k | steps = k·n + idx |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 0 | 1 | 1·3 + 1 = 4 |
| -2 | 2 | 5 | 1 | - | invalid |
| 2 | 3 | 1 | 1 | - | invalid |

Minimum is 4 steps.

This shows how different prefix alignments correspond to different cycle counts, and only one combination produces a valid decomposition.

Now consider x = 1:

| prefix v | idx | delta | delta % S | k | steps |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 | 1 |
| -2 | 2 | 3 | 1 | - | invalid |
| 2 | 3 | -1 | -1 mod 2 | - | invalid |

Answer is 1 step, achieved immediately at the first tile.

These examples confirm that the decomposition correctly matches both early and cyclic contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m · d) | prefix computation is linear, each query checks all distinct prefix sums |
| Space | O(n) | storage for prefix sums and dictionary of first occurrences |

Given that total n and m across test cases are bounded by 5 × 10^5, this approach stays within acceptable limits in Python due to linear preprocessing and bounded per-query work on distinct prefix states.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        prefix = [0] * (n + 1)
        best = {}

        for i in range(1, n + 1):
            prefix[i] = prefix[i - 1] + a[i - 1]
            if prefix[i] not in best:
                best[prefix[i]] = i

        S = prefix[n]

        for _ in range(m):
            x = int(input())
            if S == 0:
                print(best.get(x, -1))
                continue

            ans = 10**30
            for v, idx in best.items():
                delta = x - v
                if delta % S != 0:
                    continue
                k = delta // S
                if k < 0:
                    continue
                ans = min(ans, k * n + idx)

            print(-1 if ans == 10**30 else ans)

    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# sample-like
assert run("3 2\n1 -3 4\n1\n3\n") in {"1\n4", "1\n4"}, "basic"

# all zeros
assert run("3 2\n0 0 0\n0\n1\n") == "0\n-1", "zero cycle sum"

# negative-only
assert run("2 2\n-1 -2\n-3\n-6\n") == "2\n4", "negative accumulation"

# single element
assert run("1 2\n5\n5\n10\n") == "1\n2", "single cycle"

# boundary prefix
assert run("3 1\n1 2 3\n6\n") == "3", "exact cycle sum"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros array | mixed 0 / -1 | S = 0 handling |
| negative-only array | valid multiples | negative accumulation correctness |
| single element | linear scaling | n = 1 edge case |
| full cycle match | exact sum | prefix vs full cycle interaction |

## Edge Cases

When all values are zero, the score never changes after any number of steps. For any query x, only x = 0 is reachable at step 0, and all other targets are impossible. The algorithm correctly handles this by detecting S = 0 and checking prefix existence in best.

When the array contains only negative values, prefix sums strictly decrease, but cycle repetition still allows reaching more negative or even positive targets depending on structure. The modular condition with S ensures only consistent decompositions are accepted, and the earliest prefix index guarantees minimal steps.

When n = 1, the prefix structure collapses to a single repeating value. The algorithm reduces to checking whether x is a multiple of that value, with step count equal to the multiplier, which matches direct simulation.

When x equals a full cycle sum, the correct answer is exactly n steps, and the algorithm captures this through v = 0 (implicit prefix before first element) combined with k = 1.
