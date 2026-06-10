---
title: "CF 1510D - Digits"
description: "We have n cards. Each card contains a positive integer. We may choose any non-empty subset of cards and multiply all chosen numbers. The goal is not merely to obtain a product whose last decimal digit equals d."
date: "2026-06-10T19:43:55+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1510
codeforces_index: "D"
codeforces_contest_name: "2020-2021 ICPC, NERC, Northern Eurasia Onsite (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 2100
weight: 1510
solve_time_s: 1394
verified: false
draft: false
---

[CF 1510D - Digits](https://codeforces.com/problemset/problem/1510/D)

**Rating:** 2100  
**Tags:** dp, math, number theory  
**Solve time:** 23m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We have `n` cards. Each card contains a positive integer. We may choose any non-empty subset of cards and multiply all chosen numbers.

The goal is not merely to obtain a product whose last decimal digit equals `d`. Among all such subsets, we want the subset whose product value is as large as possible.

The first observation is that only the last digit of a product matters for the constraint. If a number ends with digit `x`, multiplying by it changes the current last digit `r` into `(r * x) mod 10`.

The second observation is that the actual product can become astronomically large. With `n = 100000`, even storing candidate products is impossible. We need another way to compare products.

The bound `a_i ≤ 1000` is extremely helpful. Every number contributes only one of ten possible last digits. The state space for the last digit is therefore only 10. On the other hand, `n` is very large, so any solution that depends on subset size or product magnitude is ruled out. We need roughly linear time.

A subtle edge case appears when the desired digit can be achieved by several subsets whose products differ greatly.

Example:

```
3 6
2 3 8
```

Both `{8}` and `{2,3}` produce a last digit of `8` and `6` respectively. A greedy strategy based only on last digits would miss the fact that product magnitude matters.

Another tricky case involves the number `1`.

```
3 4
1 4 11
```

Multiplying by `1` does not change the last digit, but it may still belong to an optimal subset. Any reconstruction procedure must allow such elements to appear.

A final edge case occurs when no valid subset exists.

```
2 1
2 4
```

Every product is even, so the last digit can never be `1`. The correct output is `-1`.

## Approaches

The brute force solution examines every subset, computes its product, checks the last digit, and keeps the largest valid product.

This is correct because it explicitly evaluates every possibility. Unfortunately there are `2^n` subsets. For `n = 100000` this is completely infeasible.

The key observation is that the constraint depends only on the last digit of the product. There are only ten possible residues modulo 10.

Suppose we know the last digit of a subset product. To compare two subsets with the same last digit, we only need to know which product is larger. Since

`log(ab) = log(a) + log(b)`,

maximizing the product is equivalent to maximizing the sum of logarithms.

This transforms the problem into a dynamic programming problem with only ten states.

Let `dp[r]` be the maximum possible sum of logarithms among all processed subsets whose product ends with digit `r`.

When we process a new number `a`, whose last digit is `x`, we may either start a new subset containing only `a`, or append `a` to any previously known subset. The resulting last digit becomes `(r * x) mod 10`.

Since there are only ten residues, every element performs only a constant amount of work. The entire DP runs in linear time.

To output the actual subset, we store parent information whenever a state improves. After the DP finishes, we reconstruct the chosen indices by following parent pointers backward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(1) | Too slow |
| DP on last digit | O(10n) | O(10n) | Accepted |

## Algorithm Walkthrough

1. Let `w_i = log(a_i)`.
2. Maintain `dp[10]`, where `dp[r]` stores the maximum logarithmic value of a processed subset whose product ends with digit `r`.
3. Initialize every state to negative infinity.
4. Process numbers one by one.
5. For the current number `a`, let `x = a mod 10`.
6. Create copies of the current DP because transitions must use only states from the previous iteration.
7. Consider the subset consisting only of `a`. It produces residue `x` and value `log(a)`.
8. For every residue `r` that already exists, create a new subset by appending `a`. The new residue becomes `(r * x) mod 10`, and the new value becomes `dp[r] + log(a)`.
9. Whenever a transition improves a state, record enough information to reconstruct the solution later. Store the previous residue and the previous index.
10. After all numbers are processed, inspect residue `d`.
11. If residue `d` is unreachable, print `-1`.
12. Otherwise reconstruct the subset by following parent pointers backward from the final state.
13. Output the corresponding numbers.

### Why it works

For every residue `r`, the DP stores the largest logarithmic value among all subsets ending with residue `r` after processing a prefix of the array.

The singleton transition guarantees that every subset can start at its first chosen element. The extension transition guarantees that every larger subset can be formed from a smaller subset plus one new element.

Because logarithm is strictly increasing, a subset with larger logarithmic sum always has a larger product. Thus the DP keeps exactly the subset with maximum product for every residue class.

By induction over the processed elements, every reachable subset is considered, and for each residue the best one is retained. Consequently the state for residue `d` after processing all numbers corresponds to the maximum possible product whose last digit equals `d`.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

NEG = -1e100

n, d = map(int, input().split())
a = list(map(int, input().split()))

dp = [NEG] * 10

take = [[False] * 10 for _ in range(n)]
prev_digit = [[-1] * 10 for _ in range(n)]
prev_index = [[-1] * 10 for _ in range(n)]

for i, val in enumerate(a):
    x = val % 10
    w = math.log(val)

    ndp = dp[:]

    if w > ndp[x]:
        ndp[x] = w
        take[i][x] = True
        prev_digit[i][x] = -1
        prev_index[i][x] = -1

    for r in range(10):
        if dp[r] <= NEG / 2:
            continue

        nr = (r * x) % 10
        cand = dp[r] + w

        if cand > ndp[nr]:
            ndp[nr] = cand
            take[i][nr] = True
            prev_digit[i][nr] = r
            prev_index[i][nr] = i - 1

    dp = ndp

if dp[d] <= NEG / 2:
    print(-1)
    sys.exit()

res = []
cur_digit = d
idx = n - 1

while idx >= 0:
    if take[idx][cur_digit]:
        res.append(a[idx])
        pd = prev_digit[idx][cur_digit]
        pi = prev_index[idx][cur_digit]

        cur_digit = pd
        idx = pi
    else:
        idx -= 1

print(len(res))
print(*res)
```

The DP array stores only the best logarithmic value for each residue. The reconstruction tables remember which transition created a state.

The comparison uses logarithms instead of products. This avoids huge integers while preserving ordering.

The reconstruction structure is the most delicate part. Whenever a state improves, we record exactly which previous residue produced it. States that are not improved must retain their old meaning, which is why transitions are performed from a copied DP array.

## Worked Example

### Example 1

Input:

```
6 4
4 11 8 2 1 13
```

Key DP states after each step:

| Processed value | Best residue 4 | Best residue 8 | Best residue 2 |
| --- | --- | --- | --- |
| 4 | log(4) | - | - |
| 11 | log(44) | - | - |
| 8 | log(44) | log(88) | - |
| 2 | log(88) | log(88) | log(22) |
| 1 | unchanged | unchanged | unchanged |
| 13 | log(1144) | larger residue-8 state | larger residue-2 state |

The final residue 4 state corresponds to product 1144, which is optimal.

### Example 2

Input:

```
2 1
2 4
```

| Processed value | Reachable residues |
| --- | --- |
| 2 | {2} |
| 4 | {2,4,8} |

Residue 1 never becomes reachable, so the answer is `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10n) | Ten residue transitions per element |
| Space | O(10n) | Reconstruction information for every index and residue |

With `n = 100000`, the algorithm performs about one million DP transitions, which easily fits within the time limit. The reconstruction tables occupy only a few million entries and fit comfortably within the memory limit.

## Test Cases

```
# impossible target digit
2 1
2 4

# single element works
1 7
7

# single element fails
1 7
3

# many ones
5 1
1 1 1 1 1

# target digit zero
4 0
10 3 7 9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 2 4` | `-1` | Unreachable residue |
| `1 7 / 7` | One chosen element | Singleton subset |
| `1 7 / 3` | `-1` | Singleton failure |
| Five ones | Any non-empty subset | Handling of multiplicative identity |
| Target digit zero | Valid subset ending in zero | Residue transitions involving 0 |

## Edge Cases

When all numbers are even and the target digit is odd, no sequence of multiplications can produce an odd final digit. The DP simply never reaches the corresponding residue and correctly prints `-1`.

When several subsets produce the same last digit, the DP compares logarithmic sums rather than subset size. For example:

```
3 6
2 3 16
```

The subset `{2,3}` produces `6`, while `{16}` produces `16`. The residue is the same, but the logarithmic value of `16` is larger, so the DP keeps the second subset.

When the array contains many ones, such as

```
4 4
1 1 1 4
```

the residue remains unchanged when a one is added, but the logarithmic value also remains unchanged. Either choice is valid because both produce the same product. The DP still reconstructs a correct optimal subset.
