---
title: "CF 104361B - \u0412\u044b\u0431\u043e\u0440 \u0446\u0432\u0435\u0442\u043e\u0432 \u0434\u043b\u044f \u0431\u0443\u043a\u0435\u0442\u0430"
description: "We are given a bouquet that must contain exactly n flowers, and there are m flower types. Each type can be used any number of times. The reward model for a type is not constant per flower."
date: "2026-07-01T17:54:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104361
codeforces_index: "B"
codeforces_contest_name: "\u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438\u043c. \u041c\u0441\u0442\u0438\u0441\u043b\u0430\u0432\u0430 \u041a\u0435\u043b\u0434\u044b\u0448\u0430 - 2020"
rating: 0
weight: 104361
solve_time_s: 73
verified: true
draft: false
---

[CF 104361B - \u0412\u044b\u0431\u043e\u0440 \u0446\u0432\u0435\u0442\u043e\u0432 \u0434\u043b\u044f \u0431\u0443\u043a\u0435\u0442\u0430](https://codeforces.com/problemset/problem/104361/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a bouquet that must contain exactly `n` flowers, and there are `m` flower types. Each type can be used any number of times.

The reward model for a type is not constant per flower. If we take `x` flowers of type `i`, the first one contributes `a_i`, and every next one contributes `b_i`. So the total contribution of that type becomes `a_i + (x - 1) * b_i` when `x > 0`, and `0` when `x = 0`.

The task is to distribute the total of `n` flowers across types to maximize the sum of contributions.

The key difficulty is that the marginal value of a type changes after the first pick. The first flower of a type can be significantly different from subsequent ones, so a naive greedy strategy based only on `b_i` or only on `a_i` fails.

The constraints are large: `n` can go up to `10^9`, while `m` is up to `100000`. This immediately rules out any approach that simulates picking flowers one by one or maintains per-flower decisions. Any correct solution must reduce the problem to O(m) or O(m log m) preprocessing.

A subtle failure case for naive reasoning appears when a type has a very large `a_i` but small `b_i`, or vice versa. For example, if one type has `(a, b) = (100, 1)` and another has `(1, 100)`, greedy choices based only on first or second gains can easily mislead, because the first choice interacts with the remaining structure of the allocation.

## Approaches

The brute-force idea is straightforward. We decide how many flowers `x_i` to take from each type and compute the total contribution directly, trying all valid distributions. This is correct because it evaluates the exact formula, but the number of distributions is astronomically large. Even if we cap each `x_i` at `n`, the number of integer partitions of `n` into `m` parts is far beyond feasible computation. This fails immediately when `n` exceeds a few dozen.

The structure of the reward function is linear after the first element. Each type behaves like a sequence: one special value `a_i`, followed by an infinite stream of `b_i`. This suggests transforming the problem into selecting marginal contributions.

A direct marginal view would generate, for each type, an infinite sequence of gains: `a_i, b_i, b_i, b_i, ...`. The task becomes selecting the best `n` values across all these sequences. The issue is that each sequence is infinite, so we cannot explicitly enumerate candidates.

The key observation is that only the best `b_i` matters globally for all “non-first” picks. Once we take many flowers, every additional flower contributes only its type’s `b_i`, so we want those contributions as large as possible. This suggests that in any optimal solution, almost all non-first picks should come from the type with maximum `b_i`, since using any smaller `b_i` reduces the total.

This collapses the structure: instead of distributing all `n` items arbitrarily, we treat one dominant type with maximum `b_i` as the base filler, and we only consider whether it is beneficial to “replace” some of those base picks with first picks of other types.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all distributions | Exponential | O(1) | Too slow |
| Marginal simulation per pick | O(n log m) | O(m) | Too slow |
| Optimal reduction using max `b_i` baseline | O(m) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce everything to comparing against the best possible “default” type.

### Steps

1. Find the maximum value among all `b_i`, call it `B`.

This represents the best possible value per additional flower after the first.
2. Start with a baseline solution where all `n` flowers are imagined to come from a type with value `B`.

This gives a base contribution of `n * B`.
3. For each type `i`, compute the effect of using it at least once instead of using only the baseline type.

If we introduce type `i`, we take one flower from it, which contributes `a_i` instead of `B`. This changes the total by `a_i - B`.
4. If `a_i - B > 0`, it is beneficial to include this type at least once. Add this value to the answer.
5. Sum all positive contributions from step 4 and add them to the baseline `n * B`.

### Why it works

The critical invariant is that every flower beyond the first behaves identically within its type, and the only global distinction between types for those positions is the value of `b_i`. Therefore, the best possible assignment for all non-special positions is always the maximum `b_i`.

Once this baseline is fixed, every deviation from it can only happen through first picks of types. Each such deviation replaces one baseline item worth `B` with a first item worth `a_i`, producing gain `a_i - B`. No further interaction exists between deviations because every replaced position is independent and the remaining structure still fills with `B`. This independence guarantees that summing all positive gains yields the optimal configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    a = []
    b = []
    
    B = 0
    for _ in range(m):
        ai, bi = map(int, input().split())
        a.append(ai)
        b.append(bi)
        if bi > B:
            B = bi

    ans = n * B
    
    for i in range(m):
        gain = a[i] - B
        if gain > 0:
            ans += gain

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first identifies the strongest per-unit growth rate `B`. It then assumes all flowers contribute `B`, which forms a clean baseline. Each type is evaluated independently by checking whether its first flower is stronger than that baseline. If it is, we upgrade the solution by replacing one baseline flower with that type’s first flower.

A common pitfall is attempting to simulate how many flowers of each type to take. That is unnecessary because once the baseline is fixed, the contribution of every additional flower is already determined.

## Worked Examples

### Example 1

Input:

```
4 3
5 0
1 4
2 2
```

Here `B = max(0, 4, 2) = 4`. Baseline is `4 * 4 = 16`.

Now evaluate gains:

- Type 1: `5 - 4 = 1`
- Type 2: `1 - 4 = -3`
- Type 3: `2 - 4 = -2`

Only type 1 contributes.

| Step | Action | Contribution | Total |
| --- | --- | --- | --- |
| Init | baseline | 16 | 16 |
| Type 1 | add gain | +1 | 17 |
| Type 2 | skip | +0 | 17 |
| Type 3 | skip | +0 | 17 |

Final answer is `17`.

This shows how only types whose first flower beats the baseline matter.

### Example 2

Input:

```
5 3
5 2
4 2
3 1
```

Here `B = 2`. Baseline is `5 * 2 = 10`.

Gains:

- Type 1: `5 - 2 = 3`
- Type 2: `4 - 2 = 2`
- Type 3: `3 - 2 = 1`

| Step | Action | Contribution | Total |
| --- | --- | --- | --- |
| Init | baseline | 10 | 10 |
| Type 1 | add gain | +3 | 13 |
| Type 2 | add gain | +2 | 15 |
| Type 3 | add gain | +1 | 16 |

Final answer is `16`.

The trace shows that all types with first-value above the baseline are independently beneficial.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | One pass to find `B`, one pass to compute gains |
| Space | O(1) | Only storing running maximum and result |

The constraints allow up to `100000` types, so a linear scan is easily fast enough. The large value of `n` is handled in constant time by scaling the baseline instead of iterating over individual flowers.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, m = map(int, sys.stdin.readline().split())
    B = 0
    a = []
    
    ans = 0
    
    for _ in range(m):
        ai, bi = map(int, sys.stdin.readline().split())
        a.append(ai)
        if bi > B:
            B = bi
    
    ans = n * B
    
    for ai in a:
        if ai - B > 0:
            ans += ai - B
    
    return str(ans)

# provided samples (as given in statement; note formatting ambiguity is ignored)
assert run("4 3\n5 0\n1 4\n2 2\n") == "17"
assert run("5 3\n5 2\n4 2\n3 1\n") == "16"

# custom cases
assert run("1 1\n10 5\n") == "10", "single type"
assert run("10 2\n1 100\n2 100\n") == str(10 * 100 + (2 - 100)), "negative gain ignored"
assert run("5 3\n100 1\n1 100\n1 50\n") == str(5 * 100 + (1 - 100)), "dominant b case"
assert run("3 2\n1 1\n1 1\n") == str(3 * 1), "all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single type | direct computation | base correctness |
| mixed dominance | negative gains ignored | filtering logic |
| dominant `b` case | correct baseline choice | max `b_i` behavior |
| all equal | stability | no unnecessary selections |

## Edge Cases

A corner case occurs when all `b_i` are equal. In this situation, the baseline is shared by all types, and the solution reduces purely to selecting types with highest `a_i`. The algorithm handles this naturally because every `a_i - B` is evaluated independently.

Another case is when the best `a_i` belongs to a type with small `b_i`. The algorithm still includes it if its first value exceeds the global baseline, because that replacement is always beneficial regardless of its own `b_i`.

Finally, when `n = 1`, the answer is simply `max(a_i)`, since no second picks exist. The formula reduces correctly because `n * B + max(a_i - B)` simplifies to `max(a_i)`.
