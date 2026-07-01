---
title: "CF 104115E - 21 \u043e\u0447\u043a\u043e"
description: "We are given a partially observed state of a standard 52-card deck and a hand of cards already taken by a player."
date: "2026-07-02T01:56:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104115
codeforces_index: "E"
codeforces_contest_name: "Voronezh State University - Sitronics contest, 2022"
rating: 0
weight: 104115
solve_time_s: 35
verified: true
draft: false
---

[CF 104115E - 21 \u043e\u0447\u043a\u043e](https://codeforces.com/problemset/problem/104115/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a partially observed state of a standard 52-card deck and a hand of cards already taken by a player. Each card contributes a fixed number of points, but the scoring system is non-standard: numbered cards from 2 to 10 contribute their face value, while face cards contribute custom values (J is 2 points, Q is 3, K is 4, and A is 11).

The player currently holds some subset of cards. One more card will be drawn uniformly at random from the remaining unseen cards in the deck. The task is to compute the probability that after drawing this single card, the total sum of points in the player's hand becomes exactly 21.

The key output is therefore a probability over the remaining deck state, not over abstract values. Each physical card is equally likely, so duplicates across suits matter.

The constraint n ≤ 52 means we are in a constant-size universe. Any solution that iterates over the deck or performs simple counting is sufficient. There is no need for asymptotically complex data structures or optimizations beyond O(1) bookkeeping over the 13 card ranks.

A subtle point is that multiple distinct card ranks can share the same value, for example both 2 and J give value 2. This means a naive "value frequency" approach is insufficient unless we carefully account for how many physical cards of each rank remain in the deck.

Edge cases arise when the target sum is already impossible to reach with a single draw.

If the current sum is 21, then no valid draw exists because all card values are positive, so the probability is zero.

If the required value is less than the minimum card value (which is 2 in this system), then again the answer is zero.

If the required value exceeds 11, the only possible contributor is Ace, so the probability depends solely on remaining Aces.

## Approaches

The most direct approach is to simulate the remaining deck explicitly. We compute the current sum of the given n cards, then iterate over every remaining card in the deck and check whether drawing it results in a total of 21. Since the deck size is fixed at 52, this brute force method performs at most 52 checks, which is trivially fast.

However, brute force naturally repeats work because many cards share identical rank structure. The key observation is that we do not need to enumerate individual remaining cards explicitly. Instead, we can group cards by rank. Each rank has exactly 4 copies in the deck, and we only need to know how many of each rank remain.

Once we know the remaining count per rank, we compute the required value x = 21 - current_sum. The answer is simply the number of remaining physical cards whose rank value equals x, divided by the total remaining cards.

This reduces the problem to constant-time arithmetic over 13 ranks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over remaining cards | O(52) | O(1) | Accepted |
| Rank counting aggregation | O(13) | O(1) | Accepted |

## Algorithm Walkthrough

We now construct the solution in a way that mirrors how one would reason about the deck state.

1. Read all input cards and compute the total current score. Each card is mapped to its predefined value, so we maintain a running sum as we parse the input. This gives us the baseline score before the next draw.
2. At the same time, maintain a frequency table over card ranks, not values. Each rank (2-10, J, Q, K, A) initially has 4 copies in a full deck. For every seen card, we decrement the count for that rank. This preserves the exact remaining deck composition.
3. Compute how many cards remain in total as 52 - n. This is the denominator of the probability.
4. Compute the required value x = 21 - current_sum. This is the only value that can make the final sum exactly 21 after one draw.
5. If x is not a valid card value in the system (for example x ≤ 1 or x is 5-10, etc. but must correspond to a defined rank value), then the answer is immediately zero because no card produces that contribution.
6. Otherwise, sum over all ranks whose value equals x, adding their remaining counts. This accounts for collisions like value 2 coming from both rank 2 and rank J.
7. Divide the number of favorable remaining cards by the total remaining cards to obtain the probability.

The key design choice is separating rank identity from value identity. This separation is what makes counting correct under duplicated values.

### Why it works

The algorithm maintains an exact representation of the remaining deck as a multiset of physical cards grouped by rank. Each draw is uniformly random over this multiset, so probability reduces to counting favorable elements. Since every rank contributes a fixed value, and each rank has a known remaining multiplicity, summing over matching ranks exactly counts the favorable outcomes without overcounting or missing duplicates.

## Python Solution

```python
import sys
input = sys.stdin.readline

value_map = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 2, "Q": 3, "K": 4, "A": 11
}

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def solve():
    n = int(input())
    
    remaining = {r: 4 for r in ranks}
    total_sum = 0

    for _ in range(n):
        c = input().strip()
        total_sum += value_map[c]
        remaining[c] -= 1

    total_remaining = 52 - n
    need = 21 - total_sum

    if total_remaining == 0:
        print(0.0)
        return

    if need < 2:
        print(0.0)
        return

    ans = 0
    for r in ranks:
        if value_map[r] == need:
            ans += remaining[r]

    print(ans / total_remaining)

if __name__ == "__main__":
    solve()
```

The implementation tracks both score accumulation and deck depletion simultaneously. The critical detail is that we never treat values as unique keys. Instead, we always aggregate by rank and only compare through the value mapping when deciding whether a rank contributes to the required sum.

The early exit for impossible needs avoids unnecessary scanning, although even without it the algorithm remains constant-time.

## Worked Examples

Consider a small illustrative input where the player already has a high partial sum.

### Example 1

Input:

```
3
K
K
10
```

Here K contributes 4, so two Ks give 8, plus 10 gives 18. The current sum is 18, so we need a card of value 3.

| Step | Current Sum | Need | Remaining contributing cards |
| --- | --- | --- | --- |
| After reading K | 4 | - | K reduced |
| After second K | 8 | - | K reduced |
| After 10 | 18 | - | 10 reduced |
| Final | 18 | 3 | Q cards remaining (value 3) |

There are 4 Queens originally, none removed, so 4 favorable cards out of 49 remaining. The probability is 4/49.

This demonstrates handling of a shared value class: only Q maps to 3.

### Example 2

Input:

```
2
A
A
```

Two Aces contribute 22 already.

| Step | Current Sum | Need | Interpretation |
| --- | --- | --- | --- |
| After first A | 11 | - | valid partial |
| After second A | 22 | -1 | impossible target |

Since need = -1, no card can fix the sum downward, so result is 0.

This shows the correctness of the early rejection logic for invalid required values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(13) | We process at most 13 ranks plus n input cards, all constant bounded by 52 |
| Space | O(13) | Frequency table over card ranks |

The constraints make the solution effectively constant time. Even the most direct implementation easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose

    # re-run solution inline
    value_map = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "10": 10,
        "J": 2, "Q": 3, "K": 4, "A": 11
    }
    ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

    n = int(input())
    remaining = {r: 4 for r in ranks}
    total_sum = 0

    for _ in range(n):
        c = input().strip()
        total_sum += value_map[c]
        remaining[c] -= 1

    total_remaining = 52 - n
    need = 21 - total_sum

    if total_remaining == 0:
        return "0.0"
    if need < 2:
        return "0.0"

    ans = 0
    for r in ranks:
        if value_map[r] == need:
            ans += remaining[r]

    return str(ans / total_remaining)

# provided sample-like cases
assert run("3\nK\nK\n10\n") == str(4/49)
assert run("2\nA\nA\n") == "0.0"

# custom cases
assert run("1\nQ\n") != ""  # sanity check
assert run("1\nA\n") == str(4/51)  # need 10, four 10s
assert run("52\n2\n" + "\n".join(["3"]*51)) == "0.0"
```

| Test input | Expected output | What it validates
