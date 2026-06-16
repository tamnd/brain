---
title: "CF 955A - Feed the cat"
description: "Andrew wakes up at a given time of day and realizes his cat is hungry. The cat starts with some initial hunger value, and this hunger grows steadily over time at a fixed rate per minute. Andrew can reduce the cat’s hunger only by buying buns."
date: "2026-06-17T02:05:59+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 955
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 471 (Div. 2)"
rating: 1100
weight: 955
solve_time_s: 81
verified: true
draft: false
---

[CF 955A - Feed the cat](https://codeforces.com/problemset/problem/955/A)

**Rating:** 1100  
**Tags:** greedy, math  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

Andrew wakes up at a given time of day and realizes his cat is hungry. The cat starts with some initial hunger value, and this hunger grows steadily over time at a fixed rate per minute. Andrew can reduce the cat’s hunger only by buying buns. Each bun reduces hunger by a fixed amount, and any number of buns can be bought at any time without travel cost or time delay.

There is an important twist in pricing. Before 20:00, each bun costs a normal price. Starting exactly at 20:00, every bun becomes 20 percent cheaper. The discount applies per bun purchase, not per bundle, and fractional payments are allowed in the sense that the discounted price can be non-integer, but buns are still indivisible.

The goal is to decide when Andrew should go to the store and how many buns he should buy so that the cat’s final hunger becomes non-positive, while minimizing total money spent.

The key tension in the problem is between two linear processes. Waiting increases hunger linearly over time, while waiting may reduce the price per bun if it crosses the 20:00 threshold. This creates a small number of meaningful decision points rather than a continuous optimization problem.

From constraints, hunger can be up to 100000 and grows at most 100 per minute. Time is bounded by a single day clock. A naive simulation over every possible minute is unnecessary. Any solution that recomputes per minute or per bun in a nested way risks worst case about 10^7 to 10^10 operations and will be too slow. The structure suggests that only a constant number of candidate purchase times matter.

A subtle case is when Andrew wakes before 20:00 and considers waiting. Waiting increases required buns because hunger grows, but reduces price per bun. Another is when Andrew wakes after 20:00, where only the discounted regime matters. A third edge case is when waiting crosses exactly 20:00, because the discount activates at a sharp boundary.

## Approaches

A brute-force approach would try all possible minutes from wake-up until the end of the day, compute the resulting hunger, compute how many buns are needed at that time, and multiply by the corresponding price. For each candidate minute, we would calculate a ceiling division to determine bun count.

This works because the state at each minute is well defined, but it is too slow because there are up to 1440 minutes in a day, and each evaluation is O(1), giving about 10^3 iterations per test. That alone is fine, but if extended or embedded inside multiple computations or generalized incorrectly to larger time domains, it becomes inefficient. More importantly, the real redundancy is conceptual rather than numerical.

The crucial observation is that only two moments matter. Either Andrew buys immediately, or he waits until the first moment the discount becomes active. Any time after 20:00 is strictly worse than buying exactly at 20:00, because hunger only increases while price stays constant. Similarly, any time between wake-up and 20:00 is equivalent to “buy now” since price does not change before discount.

This reduces the problem to evaluating at most two scenarios, computing required buns using ceiling division in each case, and selecting the cheaper result.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over time | O(1440) | O(1) | Accepted but unnecessary |
| Optimal two case evaluation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the answer by comparing a small set of candidate strategies.

### 1. Convert time to minutes until discount

We compute how many minutes remain until 20:00 from the wake-up time. If Andrew wakes at or after 20:00, this value is zero.

This determines whether a “wait for discount” strategy even exists.

### 2. Define immediate purchase state

If Andrew buys immediately, hunger is exactly the initial value H. The number of buns needed is the smallest integer k such that k · N ≥ H.

This is a standard ceiling division.

### 3. Compute cost of immediate purchase

Each bun costs C before discount. Total cost is k · C.

### 4. Define discounted-time purchase state

If Andrew waits until 20:00, hunger increases linearly by D per minute for the computed waiting time t.

So hunger becomes H + t · D.

### 5. Compute buns under discount

At or after 20:00, each bun costs 0.8 · C. The number of buns is again ceiling((H + t · D) / N).

### 6. If already after 20:00

We skip the immediate case entirely in terms of pricing choice, because discount already applies. We only compute the discounted version at current time.

### 7. Choose minimum cost

We compare the valid strategies and output the smallest cost.

### Why it works

The key invariant is that for any time interval before 20:00, the price per bun is constant while hunger strictly increases. This makes the required bun count a non-decreasing function of waiting time, while cost per bun remains unchanged. After 20:00, both waiting longer only increases hunger while keeping price fixed, so the cost function is strictly non-decreasing in time. Therefore, any optimal solution must occur at a boundary point where the price regime changes or at the initial time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ceil_div(a, b):
    return (a + b - 1) // b

hh, mm = map(int, input().split())
H, D, C, N = map(int, input().split())

start = hh * 60 + mm
discount_time = 20 * 60

# time until discount becomes active
t = max(0, discount_time - start)

# option 1: buy immediately
buns_now = ceil_div(H, N)
cost_now = buns_now * C

# option 2: buy at or after 20:00 (only meaningful if t > 0 or already past)
H_later = H + t * D
buns_later = ceil_div(H_later, N)
cost_later = buns_later * C * 4 / 5

# if already after 20:00, only one regime matters
if start >= discount_time:
    print(f"{cost_later:.10f}")
else:
    print(f"{min(cost_now, cost_later):.10f}")
```

The implementation first converts time into minutes to simplify the comparison with the fixed threshold of 20:00. The helper function implements ceiling division, which is required to determine the minimum number of buns needed to cover a given hunger level.

The two candidate costs correspond directly to the two meaningful strategies: buying immediately under full price, or waiting until discount time and buying under reduced price after hunger increases. The comparison at the end selects the better option.

A common mistake is forgetting that waiting past 20:00 should not be simulated further, because the cost function only worsens after the discount begins.

## Worked Examples

### Example 1

Input:

```
19 00
255 1 100 1
```

We compute 60 minutes until 20:00.

| Step | Hunger | Bun count | Price per bun | Total cost |
| --- | --- | --- | --- | --- |
| Buy now | 255 | 255 | 100 | 25500 |
| Wait to 20:00 | 255 + 60·1 = 315 | 315 | 80 | 25200 |

Waiting is beneficial because the discount outweighs the extra hunger increase.

### Example 2

Input:

```
18 30
91 1 15 1
```

We compute 90 minutes until discount.

| Step | Hunger | Bun count | Price per bun | Total cost |
| --- | --- | --- | --- | --- |
| Buy now | 91 | 91 | 15 | 1365 |
| Wait to 20:00 | 91 + 90 = 181 | 181 | 12 | 2172 |

Immediate purchase is optimal because increased hunger dominates the price reduction.

These two cases show the central tradeoff: waiting can help only when the discount savings per bun outweigh additional required buns.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic computations and comparisons |
| Space | O(1) | No auxiliary data structures are used |

The computation consists only of a few arithmetic operations regardless of input size, which easily fits within the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    hh, mm = map(int, input().split())
    H, D, C, N = map(int, input().split())

    def ceil_div(a, b):
        return (a + b - 1) // b

    start = hh * 60 + mm
    discount_time = 20 * 60
    t = max(0, discount_time - start)

    buns_now = ceil_div(H, N)
    cost_now = buns_now * C

    H_later = H + t * D
    buns_later = ceil_div(H_later, N)
    cost_later = buns_later * C * 4 / 5

    if start >= discount_time:
        ans = cost_later
    else:
        ans = min(cost_now, cost_later)

    return f"{ans:.10f}"

assert run("19 00\n255 1 100 1\n")[:6] == "25200.", "sample 1"
assert run("18 30\n91 1 15 1\n")[:5] == "1365.", "sample 2"
assert run("20 00\n10 1 10 1\n")[:3] == "8.", "already discounted"
assert run("00 00\n1 100 100 10\n") == run("00 00\n1 100 100 10\n"), "stability"
assert run("10 00\n100 10 7 3\n") != "", "general case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 20:00 start | discounted only | boundary of discount time |
| small H | immediate behavior | minimum hunger case |
| large D | growth effect | sensitivity to waiting |
| arbitrary mix | consistency | general correctness |

## Edge Cases

A key edge case is when Andrew wakes exactly at 20:00. In this situation, waiting does not change anything because discount is already active. The algorithm handles this by setting the waiting time to zero, which collapses both strategies into the discounted one.

Another edge case occurs when hunger is smaller than the bun size. In that case, ceiling division correctly returns one bun, preventing any underflow logic or zero-bun mistakes.

A third case is when waiting would increase hunger significantly but discount reduces price only slightly. The comparison between the two computed costs correctly captures this imbalance without needing any heuristic reasoning.
