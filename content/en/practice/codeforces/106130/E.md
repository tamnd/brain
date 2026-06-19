---
title: "CF 106130E - \u65b0\u7530\u5fcc\u8d5b\u9a6c"
description: "We are given two descendingly sorted arrays of horse speeds. One belongs to Tian Ji and the other to the King. A match is formed by pairing one unused horse from each side, and the outcome depends on a strict comparison: Tian Ji earns money only when his chosen horse is strictly…"
date: "2026-06-19T19:49:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106130
codeforces_index: "E"
codeforces_contest_name: "GDUT 2025 Monthly competition"
rating: 0
weight: 106130
solve_time_s: 44
verified: true
draft: false
---

[CF 106130E - \u65b0\u7530\u5fcc\u8d5b\u9a6c](https://codeforces.com/problemset/problem/106130/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two descendingly sorted arrays of horse speeds. One belongs to Tian Ji and the other to the King. A match is formed by pairing one unused horse from each side, and the outcome depends on a strict comparison: Tian Ji earns money only when his chosen horse is strictly faster than the opponent’s horse, and in that case the reward equals the opponent’s speed.

The goal is not to maximize wins, but to maximize total reward value, which means we prefer to win against large-valued opponents whenever possible, since beating a stronger opponent yields more money than beating a weak one.

Both arrays are already sorted in non-increasing order, which strongly constrains the structure of any optimal strategy. However, the pairing is not fixed, so the main difficulty is deciding which subset of matches should be used for profit and how to assign horses optimally.

The constraints allow up to 500,000 horses per side, so any solution that tries all pairings or uses quadratic matching is immediately impossible. Even O(n log n) or O(n + m) approaches with careful greedy logic are required. Any strategy involving recomputation of all pairings or backtracking over choices will fail due to time limits.

A subtle edge case arises when many horses have equal speeds. Since winning requires strict inequality, equal speeds behave like losses and can block better matches if handled incorrectly. For example, pairing a slightly stronger horse against an equal opponent wastes a potential win elsewhere.

## Approaches

A brute-force interpretation is to consider all ways of pairing horses and summing rewards from winning pairs. Conceptually, for each horse on Tian Ji’s side, we could choose any unused opponent horse, and recursively explore all possibilities. This is correct but immediately explodes combinatorially: the number of matchings is factorial in the number of horses, and even pruning does not help because each pairing decision changes future availability.

The key observation is that the reward structure is monotonic in the opponent’s strength. Winning against a larger bi always gives at least as much reward as winning against a smaller one, while losing yields zero regardless of pairing choice. This suggests that optimal play must carefully allocate Tian Ji’s stronger horses to beat the strongest possible opponents they can actually defeat, but without wasting them on opponents they could beat more efficiently later.

This transforms the problem into a greedy matching process between two sorted sequences, where we try to match large values from both sides whenever possible, but sometimes deliberately sacrifice a weak horse to preserve stronger ones for better opportunities.

The standard way to express this is a two-pointer greedy strategy: we compare the strongest remaining horses and decide whether to take a profitable match or discard a useless pairing to reposition the remaining candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n + m) | Too slow |
| Greedy Two Pointers | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two pointers, one for Tian Ji’s horses and one for the King’s horses, both starting at the strongest end since arrays are sorted in descending order.

1. Initialize pointer i at 0 for Tian Ji’s array and pointer j at 0 for the King’s array, and initialize a variable for total reward as zero.
2. While both pointers are within bounds, compare ai and bj.
3. If ai > bj, we perform a winning match between these two horses. We add bj to the answer because that is the reward for winning, then move both pointers forward. This is optimal because using the strongest available Tian Ji horse to beat the strongest possible beatable opponent maximizes current gain without harming future options.
4. If ai ≤ bj, Tian Ji cannot earn money from this pairing using ai against bj. However, instead of wasting ai on bj, we discard bj by moving the King’s pointer forward. This is a strategic removal: bj is currently too strong for ai, so it would block weaker Tian Ji horses as well, and removing it may expose a more suitable opponent.
5. Continue until one side is exhausted.

### Why it works

At any point, the algorithm maintains the invariant that all previously considered opponents that remain are strictly stronger than or equal to the current Tian Ji candidate if they were skipped, meaning they cannot be profitably matched with that candidate or any weaker one. Whenever a win is possible, pairing the current strongest viable match is safe because delaying that win would only reduce available options for both sides without increasing reward. Whenever a win is impossible, removing the opponent side reduces future blocking without losing potential profit, since no remaining Tian Ji horse can beat that opponent anyway at that stage.

This greedy elimination ensures that every profitable match is taken exactly when it becomes available, and no profitable pairing is ever skipped in favor of a worse structural outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    i = 0
    j = 0
    ans = 0
    
    while i < n and j < m:
        if a[i] > b[j]:
            ans += b[j]
            i += 1
            j += 1
        else:
            j += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution relies entirely on linear scanning. The decision point is the strict inequality check. When Tian Ji wins, both pointers advance because both horses are consumed. When he loses or ties, only the King’s pointer advances, effectively discarding an unhelpful opponent horse.

A common implementation mistake is reversing pointer movement in the losing case, which would incorrectly consume Tian Ji horses and reduce potential matches. Another subtle issue is forgetting that equality is a loss, which must behave identically to the “cannot win” branch.

## Worked Examples

Consider the case where Tian Ji has `[6, 3, 1]` and the King has `[5, 4, 2]`.

We trace pointer movement:

| i | j | a[i] | b[j] | Action | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 6 | 5 | win, take 5 | 5 |
| 1 | 1 | 3 | 4 | lose, discard b | 5 |
| 1 | 2 | 3 | 2 | win, take 2 | 7 |
| 2 | 3 | 1 | - | stop | 7 |

This shows that skipping stronger opponents when they block future matches is necessary; otherwise 3 would be wasted.

Now consider `[7, 5, 1]` versus `[6, 4, 3]`.

| i | j | a[i] | b[j] | Action | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 7 | 6 | win, take 6 | 6 |
| 1 | 1 | 5 | 4 | win, take 4 | 10 |
| 2 | 2 | 1 | 3 | lose, discard b | 10 |
| 2 | 3 | 1 | - | stop | 10 |

This demonstrates that not every remaining horse can be used, and optimal play depends on avoiding wasted weak matchups against still-too-strong opponents.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each pointer moves forward at most once per element |
| Space | O(1) | Only counters and accumulator are used |

The linear scan is necessary given the input size up to 500,000 per array. Any sorting is unnecessary because inputs are already guaranteed sorted, and any nested comparison strategy would exceed limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import contextlib
    import sys as _sys
    buf = io.StringIO()
    _stdout = _sys.stdout
    _sys.stdout = buf
    try:
        solve()
    finally:
        _sys.stdout = _stdout
    return buf.getvalue().strip()

# simple sample-style cases
assert run("2 2\n4 2\n3 1\n") == "3"
assert run("3 3\n6 3 1\n5 4 2\n") == "7"

# all equal (no wins possible)
assert run("3 3\n5 5 5\n5 5 5\n") == "0"

# strictly increasing difficulty gap
assert run("3 3\n10 9 8\n7 6 5\n") == "18"

# edge: many weak horses vs one strong blocker
assert run("3 5\n3 2 1\n10 9 8 7 6\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| equal arrays | 0 | strict inequality handling |
| strong vs weak | full greedy wins | optimal pairing accumulation |
| all losses | 0 | discard-only behavior |

## Edge Cases

When all values are equal, every comparison fails. For example, `a = [5,5,5]`, `b = [5,5,5]`. The algorithm repeatedly discards from the opponent side, never consuming Tian Ji’s horses, and ends with zero reward. This confirms correct handling of the equality-as-loss rule.

When Tian Ji is strictly stronger overall, such as `a = [10,9,8]`, `b = [7,6,5]`, every comparison yields a win, so both pointers advance in lockstep and all rewards are accumulated. The algorithm never discards unnecessarily because no blocking occurs.

When the opponent has many strong horses and Tian Ji has few weak ones, such as `a = [3,2,1]`, `b = [10,9,8,7,6]`, the algorithm repeatedly discards opponent horses until exhaustion. Tian Ji never wastes a horse on an unwinnable match, which is essential for correctness since premature consumption would reduce already-zero gain but still distort pointer alignment in later states.
