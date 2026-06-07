---
title: "CF 2178B - Impost or Sus"
description: "We start with a string consisting only of s and u. We may repeatedly choose any position containing u and change it into s. We are not allowed to change an s back into u. The final string must satisfy two conditions. First, it must contain at least two occurrences of s."
date: "2026-06-07T22:22:54+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 2178
codeforces_index: "B"
codeforces_contest_name: "Good Bye 2025"
rating: 900
weight: 2178
solve_time_s: 155
verified: false
draft: false
---

[CF 2178B - Impost or Sus](https://codeforces.com/problemset/problem/2178/B)

**Rating:** 900  
**Tags:** dp, greedy, implementation, strings  
**Solve time:** 2m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a string consisting only of `s` and `u`.

We may repeatedly choose any position containing `u` and change it into `s`. We are not allowed to change an `s` back into `u`.

The final string must satisfy two conditions. First, it must contain at least two occurrences of `s`. Second, every remaining `u` must sit exactly halfway between its two nearest `s` characters.

The task is to find the minimum number of `u → s` operations required.

The total length of all strings across the test cases is at most `2 · 10^5`. Any solution that examines each character only a constant number of times is easily fast enough. Quadratic approaches are ruled out because a single test could already contain `200000` characters.

The tricky part is understanding what a valid final string actually looks like.

Consider two consecutive `s` characters in the final string.

If their distance is `1`, they form `"ss"` and there is no `u` between them.

If their distance is `2`, they form `"sus"`, and the middle position is perfectly centered.

If the distance is larger than `2`, there are multiple positions between them. Only the exact midpoint would be equally distant from both `s`, so every other position would violate the condition.

This means that in any suspicious string:

- every `u` is surrounded by `s` on both sides,
- no two `u` characters are adjacent,
- the first and last characters cannot be `u`.

For example, `"suss"` is valid because the only `u` is between two `s` characters.

For example, `"suus"` is invalid because the two middle `u` characters cannot both be centered between the same pair of `s`.

A common mistake is to focus on distances between existing `s` characters. Since we are allowed to create new `s` characters anywhere by converting `u`, the important question is not where the current `s` characters are, but which `u` characters we choose to keep.

Consider:

```
uuuu
```

A greedy idea might try to place `s` only at the ends. That gives `"suus"`, which is still invalid. The optimal answer is `3`, producing something like `"suss"`.

Another easy-to-miss case is:

```
sus
```

The answer is `0`. The string already satisfies all requirements.

Finally:

```
uuu
```

Only the middle `u` can remain. Both end positions must become `s`, so the answer is `2`.

## Approaches

A brute-force solution would consider every subset of `u` positions to convert into `s`. For each choice, we could check whether the resulting string is suspicious.

If a string contains `k` occurrences of `u`, this requires examining `2^k` possibilities. With `k` potentially near `200000`, this is completely infeasible.

To do better, we need to characterize which `u` characters are allowed to survive.

From the structural observation above, every surviving `u` must satisfy two properties.

First, it cannot be at either end of the string.

Second, it cannot be adjacent to another surviving `u`.

Nothing else matters.

If a `u` is internal and all neighboring positions become `s`, then it automatically sits between two `s` characters at distance `1` on both sides.

This transforms the problem into a maximum-keeping problem.

We want to keep as many original `u` characters as possible, subject to:

- kept `u` positions are not at the ends,
- no two kept `u` positions are adjacent.

Every `u` that is not kept must be converted into `s`.

So:

```
answer = total_u - maximum_keepable_u
```

Finding the maximum number of non-adjacent kept positions is a standard path DP.

Let:

- `dp0` = best number of kept `u` so far when the previous position is not a kept `u`,
- `dp1` = best number of kept `u` so far when the previous position is a kept `u`.

We scan left to right and update these states in constant time per character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k · n) | O(n) | Too slow |
| Optimal DP | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count the number of `u` characters in the string.
2. Maintain two DP states.

`dp0` stores the maximum number of kept `u` characters so far when the previous position is not kept.

`dp1` stores the maximum number of kept `u` characters so far when the previous position is kept.
3. Process the string from left to right.
4. If the current character is `s`, it cannot be kept as a `u`.

Merge both previous states into the new `dp0`.
5. If the current character is `u`, we have two choices.

Convert it to `s`.

In that case, the previous state does not matter, and we transition into `dp0`.
6. If the current character is an internal position, meaning it is neither the first nor the last character, we may keep it as `u`.

To keep it, the previous position must not already be a kept `u`, so the transition comes only from `dp0`.
7. After processing all positions, the maximum number of keepable `u` characters is `max(dp0, dp1)`.
8. The answer is:

```
total_u - maximum_keepable_u
```

### Why it works

A suspicious string is completely determined by which original `u` characters remain unchanged.

A remaining `u` mu
