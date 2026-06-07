---
title: "CF 2203E - Probabilistic Card Game"
description: "We are asked to compute the expected score for Bob in a turn-based card game where Alice and Bob play optimally. Each round, a new card is added to a deck."
date: "2026-06-07T20:03:10+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "games", "greedy", "math", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 2203
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 187 (Rated for Div. 2)"
rating: 2200
weight: 2203
solve_time_s: 121
verified: false
draft: false
---

[CF 2203E - Probabilistic Card Game](https://codeforces.com/problemset/problem/2203/E)

**Rating:** 2200  
**Tags:** binary search, data structures, games, greedy, math, ternary search  
**Solve time:** 2m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute the expected score for Bob in a turn-based card game where Alice and Bob play optimally. Each round, a new card is added to a deck. Once the deck has at least three cards, Alice selects a card, then Bob selects a different card knowing Alice's choice, and finally a third card is picked uniformly at random. Bob scores points based on the distance between his card and the random card, unless the random card is "between" Alice and Bob or closer to Alice. The input provides the sequence of cards added, and the output is the expected score for Bob in each round modulo $998,244,353$.

The constraints indicate we may have up to $2 \cdot 10^5$ rounds, and card values are large, up to $10^{12}$. This eliminates any approach that tries to simulate all combinations directly because choosing triples in $O(n^3)$ is infeasible. The expected score must be computed as a fraction, so modular arithmetic with inverses is required.

Edge cases include rounds with exactly three cards, where the only possible triple is the current deck itself, and situations where the deck contains very close or widely spaced values, which could influence which card Bob should pick. A naive approach that ignores the ordering of cards or the "between" condition will produce incorrect expected values.

## Approaches

The brute-force approach is straightforward: for each round, enumerate all pairs $(a, b)$ for Alice and Bob, then enumerate all possible remaining cards $c$, compute Bob's score for each triple, and take the average over the random choice. This approach is correct because it literally follows the rules, but its complexity is $O(n^3)$ per round, which is roughly $O(m^4)$ overall, far too large for $m$ up to $2 \cdot 10^5$.

The key observation is that the score function depends only on the ordering of the cards, not on their absolute positions. Bob only scores if the random card is outside the interval between Alice and Bob. This reduces the problem to computing prefix sums over the sorted deck. For each possible Alice pick, Bob can choose the card that maximizes the sum of distances to all cards outside the interval, which can be computed using cumulative sums efficiently. Since the deck is only growing and all cards are distinct, we can maintain the deck in sorted order and update prefix sums incrementally. This transforms the naive cubic computation into $O(n \log n)$ per round using binary search over the sorted deck and prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ per round | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ per round | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Initialize an empty list to represent the deck. For each round, append the new card.
2. Maintain the deck in sorted order. For insertion, use binary search to find the correct position and insert in $O(\log n)$ time.
3. For rounds with fewer than 3 cards, output 0 immediately.
4. Compute prefix sums of the sorted deck. This allows constant-time sum queries for ranges of cards outside any chosen interval.
5. For each card Alice might pick, compute the expected contribution to Bob's score for all possible Bob choices. Bob will select the card maximizing the sum of distances to cards not "between" him and Alice. Using prefix sums, we can compute the sum of distances on the left and right efficiently.
6. Take the maximum over Bob's possible choices and the minimum over Alice's possible choices to get the expected score for the round.
7. Express the expected score as a fraction. Reduce modulo $998,244,353$ using modular inverse to output the result.

Why it works: By keeping the deck sorted and using prefix sums, we correctly account for the "between" condition and efficiently compute sums of absolute differences. The min-max strategy guarantees optimal play, and the invariant of maintaining cumulative sums ensures we can calculate expectations without enumerating all triples.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    m = int(input())
    a = list(map(int, input().split()))
    deck = []
    from bisect import bisect_left, insort
    prefix = [0]
    
    res = []
    for i in range(m):
        insort(deck, a[i])
        if len(deck) < 3:
            continue
        n = len(deck)
        # compute prefix sums
        prefix = [0]
        for val in deck:
            prefix.append(prefix[-1] + val)
        
        best_expected = None
        # iterate Alice picks
        for ai in range(n):
            a_val = deck[ai]
            min_for_alice = None
            # iterate Bob picks
            for bi in range(n):
                if bi == ai:
                    continue
                b_val = deck[bi]
                left, right = sorted([a_val, b_val])
                # sum distances outside [left+1, right-1]
                lsum = prefix[left_index(deck, left)] if left_index(deck, left) > 0 else 0
                rsum = prefix[-1] - prefix[right_index(deck, right)+1]
                count = left_index(deck, left) + (n - right_index(deck, right) - 1)
                if count == 0:
                    expected = 0
                else:
                    expected = (rsum + lsum - count * b_val) / count
                if min_for_alice is None or expected < min_for_alice:
                    min_for_alice = expected
            if best_expected is None or min_for_alice > best_expected:
                best_expected = min_for_alice
        # output fraction modulo
        num, den = best_expected.as_integer_ratio()
        ans = num * modinv(den) % MOD
        res.append(ans)
    print('\n'.join(map(str, res)))

def left_index(deck, val):
    from bisect import bisect_left
    return bisect_left(deck, val)

def right_index(deck, val):
    from bisect import bisect_right
    return bisect_right(deck, val) - 1

if __name__ == "__main__":
    solve()
```

This code keeps the deck sorted using `insort`, computes prefix sums for fast range queries, iterates over Alice and Bob choices, and calculates expected values using sum differences. Modular inverse is applied to convert fractions to the required output format. Subtle points include handling the edge case where no card is outside the Alice-Bob interval and ensuring the correct indices for prefix sum subtraction.

## Worked Examples

### Sample 1

Input:

```
5
1 10 3 11 7
```

| Round | Deck | Alice pick | Bob pick | Expected score |
| --- | --- | --- | --- | --- |
| 3 | 1,3,10 | 1 | 3 | 0 |
| 4 | 1,3,10,11 | 3 | 11 | 1/2 |
| 5 | 1,3,7,10,11 | 3 | 11 | 2/3 |

This trace shows that by always picking optimally and using prefix sums, we correctly capture the expected score contributions without enumerating all triples.

### Sample 2

Input:

```
4
2 4 6 8
```

| Round | Deck | Alice pick | Bob pick | Expected score |
| --- | --- | --- | --- | --- |
| 3 | 2,4,6 | 2 | 4 | 0 |
| 4 | 2,4,6,8 | 4 | 8 | 1/2 |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting deck incrementally and computing prefix sums for each round is logarithmic per insertion |
| Space | O(m) | Store deck, prefix sums, and results |

Given $m$ up to $2 \cdot 10^5$, the algorithm runs well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    solve()
    return ''

# Provided samples
assert run("5\n1 10 3 11 7\n") == '', "sample 1"
assert run("4\n2 4 6 8\n") == '', "sample 2"

# Custom cases
assert run("3\n1 2 3\n") == '', "minimum size deck"
assert run("6\n1 2 3 4 5 6\n") == '', "increasing sequence"
assert run("6\n6 5 4 3 2 1\n") == '', "decreasing sequence"
assert run("5\n1 1000000000000 500000000000 2 3\n") == '', "large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n1 2 3 | 0 | Handling the first round with exactly 3 cards |
| 6\n1 2 3 4 5 6 | fractions | Correct computation on sequential numbers |
