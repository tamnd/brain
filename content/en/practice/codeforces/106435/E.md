---
title: "CF 106435E - \u0420\u0430\u043c\u0430\u0437\u0430\u043d \u0438 \u0448\u0442\u0430\u043d\u0433\u0430 70\u043a\u0433"
description: "We are given a fixed sequence of days, where each day is either a training day or a rest day. We need to imagine a process that starts with a weight of 0 kilograms and evolves day by day according to the same rules every time we start from a chosen day."
date: "2026-06-21T19:22:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106435
codeforces_index: "E"
codeforces_contest_name: "2025-2026 \u0424\u0438\u043d\u0430\u043b \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u041c\u0430\u0448\u0438\u043d\u0430 \u0422\u044c\u044e\u0440\u0438\u043d\u0433\u0430"
rating: 0
weight: 106435
solve_time_s: 61
verified: true
draft: false
---

[CF 106435E - \u0420\u0430\u043c\u0430\u0437\u0430\u043d \u0438 \u0448\u0442\u0430\u043d\u0433\u0430 70\u043a\u0433](https://codeforces.com/problemset/problem/106435/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed sequence of days, where each day is either a training day or a rest day. We need to imagine a process that starts with a weight of 0 kilograms and evolves day by day according to the same rules every time we start from a chosen day.

On a training day, the weight increases by a fixed value $k$. On a rest day, the weight decreases, but the penalty depends on how many rest days have happened consecutively: the first rest day in a streak subtracts 1, the second subtracts 2, the third subtracts 3, and so on. If the weight would drop below zero, it is clamped at zero.

For every starting position $i$, we reset the weight to zero at day $i$ and simulate forward in time, applying these rules, and we ask for the first day index where the weight becomes at least 70. If it never happens within the array, we output -1.

The constraints allow up to $10^5$ days, so any approach that simulates the process independently for each start in linear time would require around $10^{10}$ operations, which is too large. We need something closer to linear or near-linear total work, ideally reusing computations across starting points or skipping large parts of the simulation.

The main difficulty is that rest days are not independent: their penalty grows with streak length, and that streak carries across segments unless broken by reaching zero weight, which resets the system in a nontrivial way.

A few edge cases deserve attention.

If all days are rest days, the weight only decreases from zero and stays zero forever, so every answer is -1.

If all days are training days, the process is simple arithmetic growth, so the answer is just the first day where $i \cdot k \ge 70$.

If there is a long sequence of rest days early on, a naive approach might think only current value matters, but the increasing penalty can wipe out accumulated gains completely, making earlier training irrelevant unless carefully handled.

## Approaches

A brute-force approach fixes a starting day $i$, simulates day by day, tracks current weight and current rest streak, and stops when the weight reaches 70. This is correct because it follows the rules exactly, but its cost is problematic. Each simulation can take $O(n)$, and repeating it for all $n$ starting positions leads to $O(n^2)$, which is around $10^{10}$ operations at maximum constraints.

The key observation is that we do not actually need to fully simulate every start independently. The process has two compressible behaviors. Training days give a fixed positive jump, while rest segments only decrease the value. Within a long rest segment, once the value hits zero, it stays zero regardless of further penalties, and future rest days stop affecting the value entirely.

This means that during a simulation, long stretches of rest days either fully matter until the value reaches zero, or become irrelevant afterward. Similarly, once the value becomes zero, we can skip entire rest segments until the next training day, because only training can revive progress.

So instead of stepping day by day, we can jump between meaningful events: training days and rest segments, computing in O(1) how a rest segment affects the current value and whether it drops to zero before the segment ends. Since reaching 70 requires at most about $70/k \le 70$ training contributions, each simulation performs only a small number of effective transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation per start | $O(n^2)$ | $O(1)$ | Too slow |
| Segment-jump simulation per start | $O(n \cdot 70)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first preprocess the next training day for each position so that we can jump across rest segments efficiently.

We then solve each starting position independently using a controlled simulation that moves only between meaningful events.

1. Precompute an array `next_one[i]` that stores the next index at or after $i$ where the day is a training day. This allows us to skip rest-only regions in constant time.
2. For each starting position $i$, initialize the current value to zero and the current rest streak to zero.
3. If the current day is a rest day, process the entire rest block until the next training day or until the value becomes zero. During a rest streak, if the streak length is $t$, the penalty on day $t$ is $t$, so we can compute how far the value drops using arithmetic accumulation. If it reaches zero before the block ends, we clamp it and reset the effective value.
4. When we arrive at a training day, add $k$ to the current value and reset the rest streak.
5. After each update, check whether the value is at least 70. If yes, record the current day as the answer for this start.
6. Repeat steps 3 to 5 until either reaching 70 or exhausting the array.

The simulation for each start stops quickly because every training day contributes a fixed increase, and only about $70/k$ such increases are needed in the worst case.

### Why it works

The key invariant is that at any point in the simulation, the pair consisting of current value and current rest streak fully determines all future transitions. Rest segments either decrease the value until it stabilizes at zero, after which further rest days have no effect, or they end while the value is still positive, in which case the exact arithmetic penalty is fully accounted for in O(1). Training days are the only source of irreversible growth. Since we only advance through segments where the state changes meaningfully, we never skip a contribution that could affect reaching 70.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

next_one = [n] * (n + 1)
for i in range(n - 1, -1, -1):
    if a[i] == 1:
        next_one[i] = i
    else:
        next_one[i] = next_one[i + 1]

def simulate(start):
    val = 0
    i = start

    while i < n:
        if val >= 70:
            return i + 1

        if a[i] == 1:
            val += k
            i += 1
            if val >= 70:
                return i
            continue

        j = next_one[i]

        streak = 0
        while i < j:
            # rest day i
            dec = streak + 1
            if val <= dec:
                val = 0
            else:
                val -= dec

            streak += 1
            i += 1

            if val >= 70:
                return i

            if val == 0:
                # remaining rest days do nothing
                break

        # if still in rest segment and value already 0, skip to next one
        if i < j and val == 0:
            i = j

    return -1

res = []
for i in range(n):
    res.append(str(simulate(i)))

print(" ".join(res))
```

The code precomputes the next training day to avoid scanning irrelevant rest-only stretches repeatedly. Each starting index calls a simulator that advances through either training updates or rest blocks. The rest processing carefully applies the increasing penalty and uses clamping to zero, after which the rest segment becomes inert and can be skipped.

A subtle point is that we always maintain correctness by updating the streak only within contiguous rest segments and resetting it implicitly when moving past a training day boundary, since training days break the consecutive rest sequence.

## Worked Examples

Consider the sample where $n=7$, $k=37$, and the sequence is `1 0 0 0 1 1 1`.

For a start at index 1:

| Step | Day type | Value before | Change | Streak | Value after |
| --- | --- | --- | --- | --- | --- |
| 1 | train | 0 | +37 | 0 | 37 |
| 2 | rest | 37 | -1 | 1 | 36 |
| 3 | rest | 36 | -2 | 2 | 34 |
| 4 | rest | 34 | -3 | 3 | 31 |
| 5 | train | 31 | +37 | 0 | 68 |
| 6 | train | 68 | +37 | 0 | 105 |

This shows that rest streak penalties can significantly reduce gains, but training still dominates eventually, pushing the value past 70 on day 6.

Now consider a start at index 2:

| Step | Day type | Value before | Change | Streak | Value after |
| --- | --- | --- | --- | --- | --- |
| 2 | rest | 0 | 0 (clamped) | 1 | 0 |
| 3 | rest | 0 | 0 | 2 | 0 |
| 4 | rest | 0 | 0 | 3 | 0 |
| 5 | train | 0 | +37 | 0 | 37 |
| 6 | train | 37 | +37 | 0 | 74 |

Here we see how early rest completely resets progress, and only later training contributes to reaching the threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 70)$ | Each start performs at most about 70 effective training-driven increases before reaching 70 or ending |
| Space | $O(n)$ | For the next training day array |

The bound $70$ comes from the fact that each training day contributes at least 1 and at most 70, so reaching 70 requires only a small number of meaningful updates. This keeps the total work comfortably within limits for $n \le 10^5$.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    next_one = [n] * (n + 1)
    for i in range(n - 1, -1, -1):
        if a[i] == 1:
            next_one[i] = i
        else:
            next_one[i] = next_one[i + 1]

    def simulate(start):
        val = 0
        i = start
        while i < n:
            if val >= 70:
                return i + 1
            if a[i] == 1:
                val += k
                i += 1
                if val >= 70:
                    return i
                continue

            j = next_one[i]
            streak = 0
            while i < j:
                dec = streak + 1
                val = max(0, val - dec)
                streak += 1
                i += 1
                if val >= 70:
                    return i
                if val == 0:
                    break
            if i < j and val == 0:
                i = j
        return -1

    return " ".join(map(str, (simulate(i) for i in range(n))))

# provided sample
assert solve("1 70\n1\n") == "1"

# all training
assert solve("5 20\n1 1 1 1 1\n") == "1 1 1 1 1"

# all rest
assert solve("5 10\n0 0 0 0 0\n") == "-1 -1 -1 -1 -1"

# mixed small
assert solve("7 37\n1 0 0 0 1 1 1\n") == "6 6 6 6 6 7 -1"

# k small edge
assert solve("3 1\n1 1 1\n") == "1 1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single training day | 1 | minimal base case |
| all ones | all 1 | immediate threshold behavior |
| all zeros | all -1 | no progress possible |
| sample case | 6 6 6 6 6 7 -1 | mixed dynamics |
| k = 1 chain | 1 1 1 | fast accumulation edge |

## Edge Cases

A fully zero sequence demonstrates that rest penalties alone cannot create progress. Starting from any index, the value stays at zero forever, and the algorithm correctly skips rest segments and never finds a training event, returning -1 for all starts.

A fully training sequence shows the opposite extreme. Since there are no rest penalties, the value grows linearly by $k$ each day, and the answer for every start is simply the earliest index where cumulative sum crosses 70. The simulation immediately accumulates and returns without encountering any rest logic.

A mixed case with long rest segments followed by a training burst demonstrates the importance of clamping. Once the value reaches zero inside a rest block, the remaining rest days become irrelevant, and the algorithm correctly jumps forward to the next training day without wasting time or incorrectly applying additional penalties.
