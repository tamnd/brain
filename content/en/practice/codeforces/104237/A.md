---
title: "CF 104237A - Fun with Food Audits"
description: "Four trash bins are placed around a campus, and at the end of lunch each bin is weighed. Each bin has a known empty weight of six pounds, and the input gives the total measured weight of each bin after use."
date: "2026-07-01T23:19:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104237
codeforces_index: "A"
codeforces_contest_name: "Harker Programming Invitational 2023 Novice"
rating: 0
weight: 104237
solve_time_s: 70
verified: true
draft: false
---

[CF 104237A - Fun with Food Audits](https://codeforces.com/problemset/problem/104237/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

Four trash bins are placed around a campus, and at the end of lunch each bin is weighed. Each bin has a known empty weight of six pounds, and the input gives the total measured weight of each bin after use. The goal is to determine how much food waste is inside all four bins combined.

The key observation is that the measured weight includes two components: the fixed container weight and the variable food waste. Since every bin has identical empty weight, the waste in a single bin is simply its measured weight minus six. The final answer is the sum of these per-bin waste values across all four bins.

The input size is fixed at exactly four integers, so there are no scaling concerns. Even in the most general interpretation, the computation is constant time and requires only a few arithmetic operations. This rules out any need for loops over large structures, data structures, or optimization techniques. A correct solution is purely arithmetic.

The main edge case is implicit underflow if someone forgets to subtract the empty weight per bin and instead subtracts it once globally or not at all. For example, if all bins are empty and each weighs six, the correct answer is zero. A naive sum without subtraction would incorrectly report twenty four.

Another subtle failure mode is mixing up the interpretation and subtracting incorrectly per total instead of per bin. For instance, given `18 10 9 25`, the correct waste is `(18-6) + (10-6) + (9-6) + (25-6) = 12 + 4 + 3 + 19 = 38`. If one subtracts six only once from the total sum `62 - 6`, the result becomes 56, which is wrong because the empty weight applies independently to each bin.

## Approaches

The direct way to think about the problem is to simulate the situation literally. We read four weights, assume each includes six pounds of container mass, and for each bin we compute its food content by subtraction, then sum them. This is already the full solution.

A more naive framing would be to separate each bin’s total weight into “container + food” explicitly and attempt to accumulate container mass and food mass separately. That still leads to the same computation but introduces unnecessary bookkeeping. Since every container has identical known weight, there is no need to model them separately.

The key insight is that the container contribution is a constant repeated four times. Instead of thinking in terms of total weight decomposition, we can directly subtract the fixed overhead per item. This reduces the problem to a single linear pass over four values with constant arithmetic per element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct per-bin subtraction | O(1) | O(1) | Accepted |
| Redundant decomposition | O(1) | O(1) | Accepted but unnecessary |

## Algorithm Walkthrough

1. Read four integers representing the measured weights of the bins. Each value already includes both container and food mass.
2. For each weight, subtract six to isolate only the food waste inside that bin. This step is done independently per bin because each container contributes its own fixed weight.
3. Add the four computed waste values together to obtain the total food waste across the campus.
4. Output the resulting sum.

### Why it works

Each measured value can be expressed as `w_i = 6 + f_i`, where `f_i` is the food waste in bin i. Summing all four gives `Σ w_i = 24 + Σ f_i`. Subtracting 24 implicitly is equivalent to subtracting six from each bin individually. The algorithm performs this decomposition locally per element, ensuring the fixed component is removed exactly once per bin and leaving only the total waste.

## Python Solution

```python
import sys
input = sys.stdin.readline

weights = list(map(int, input().split()))
total_waste = 0

for w in weights:
    total_waste += (w - 6)

print(total_waste)
```

The solution reads the four integers in a single line, which is safe because the input size is fixed. Each value is processed independently, subtracting the constant empty weight of six pounds.

The loop is the cleanest way to express per-bin decomposition. Even though unrolling the loop is possible for four values, keeping it explicit avoids hardcoding and makes the logic clearer.

The subtraction is done before accumulation, which ensures we never mistakenly aggregate container weight into the final sum. Since all inputs are guaranteed to be at least one, subtracting six can produce negative intermediate values only in physically meaningless cases, but within constraints it remains safe.

## Worked Examples

### Example 1

Input:

```
18 10 9 25
```

| Bin | Weight | Waste Calculation | Waste |
| --- | --- | --- | --- |
| 1 | 18 | 18 - 6 | 12 |
| 2 | 10 | 10 - 6 | 4 |
| 3 | 9 | 9 - 6 | 3 |
| 4 | 25 | 25 - 6 | 19 |

Total waste = 12 + 4 + 3 + 19 = 38

This confirms that each bin is processed independently and the constant container weight is removed per item.

### Example 2

Input:

```
6 6 6 6
```

| Bin | Weight | Waste Calculation | Waste |
| --- | --- | --- | --- |
| 1 | 6 | 6 - 6 | 0 |
| 2 | 6 | 6 - 6 | 0 |
| 3 | 6 | 6 - 6 | 0 |
| 4 | 6 | 6 - 6 | 0 |

Total waste = 0

This case verifies the boundary condition where no food is present and all bins match their empty weight exactly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Exactly four arithmetic operations and four subtractions regardless of input values |
| Space | O(1) | Only a constant number of integer variables are stored |

The computation is constant-time because the input size is fixed. It easily satisfies any realistic constraints, including strict time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    weights = list(map(int, input().split()))
    print(sum(w - 6 for w in weights))

# provided sample
assert run("18 10 9 25") == "38\n", "sample 1"

# all empty bins
assert run("6 6 6 6") == "0\n", "all empty"

# single heavy bin
assert run("6 6 6 100") == "94\n", "one full bin"

# minimal allowed weights
assert run("1 1 1 1") == "-20\n", "below empty weight edge"

# mixed values
assert run("7 8 9 10") == "10\n", "mixed small values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 18 10 9 25 | 38 | sample correctness |
| 6 6 6 6 | 0 | empty bins boundary |
| 6 6 6 100 | 94 | single dominant bin |
| 1 1 1 1 | -20 | subtraction behavior at minimum |
| 7 8 9 10 | 10 | general mixed case |

## Edge Cases

The most important edge case is when all bins are exactly empty. For input `6 6 6 6`, each subtraction produces zero, and the final sum remains zero. The algorithm processes each bin independently, so no hidden accumulation error occurs.

Another edge case is when weights are close to the minimum allowed value. For input `1 1 1 1`, each bin contributes `1 - 6 = -5`, leading to a total of `-20`. The computation still follows the defined arithmetic structure even though the physical interpretation becomes nonsensical. The algorithm does not assume non-negativity; it simply applies the given transformation consistently.

A final edge case is skewed distribution such as `6 6 6 100`. Only one bin contributes non-zero waste, and the rest cancel exactly to zero. The per-bin subtraction ensures there is no coupling between values, so large outliers do not affect correctness of other bins.
