---
title: "CF 1982C - Boring Day"
description: "We are asked to simulate a game with a deck of cards arranged in a specific order. Each card has a positive integer on it."
date: "2026-06-08T16:41:55+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1982
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 955 (Div. 2, with prizes from NEAR!)"
rating: 1200
weight: 1982
solve_time_s: 115
verified: true
draft: false
---

[CF 1982C - Boring Day](https://codeforces.com/problemset/problem/1982/C)

**Rating:** 1200  
**Tags:** binary search, data structures, dp, greedy, two pointers  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a game with a deck of cards arranged in a specific order. Each card has a positive integer on it. Egor takes a non-zero number of cards from the top of the deck each round, and the round is won if the sum of the taken cards lies within a given range $[l, r]$. The task is to maximize the total number of rounds won, but there is no requirement that the winning rounds occur consecutively. Input gives multiple independent test cases, each specifying the number of cards, the target range, and the sequence of card values. Output for each test case is a single integer: the maximum number of winning rounds.

Constraints allow up to $10^5$ cards per test case, and the sum of $n$ over all test cases is $2 \cdot 10^5$. This rules out $O(n^2)$ solutions, since iterating over all possible contiguous subarrays for each round would result in over $10^{10}$ operations. Each card value and the bounds $l, r$ can be up to $10^9$, so we must carefully handle integer sums without relying on array indexing tricks that assume small numbers.

Edge cases include sequences where all cards are too large to ever fit in $[l, r]$ individually, sequences where individual cards already satisfy the range, and sequences where multiple small cards must be grouped to reach the range. For example, with cards `[1, 2, 1]` and range `[3, 3]`, we cannot take any single card, but taking the first two cards sums to 3, yielding a winning round. A naive greedy approach of always taking the top card and checking if it wins may miss opportunities to combine small cards.

## Approaches

The brute-force approach is to examine every possible prefix of the remaining deck to find a contiguous sum in the winning range. While this is correct, it requires $O(n^2)$ per test case because, in the worst case, we might have to check all possible prefix lengths at each step. With $n$ up to $10^5$, this is too slow.

The key observation is that the problem reduces to counting the number of prefixes whose sums fall in $[l, r]$. Consider the prefix sums array $S$ where $S_i = a_1 + a_2 + ... + a_i$. Each round corresponds to choosing a starting and ending index of a prefix such that the sum is within $[l, r]$. Since Egor must always take cards from the top, each round starts at the first remaining card. Therefore, we only need to find, for each position, the shortest prefix starting from the current card that lies in $[l, r]$. The sum of the first $k$ cards is $S_k$, so the problem becomes finding the largest $k$ such that $S_k - S_{prev}$ lies in $[l, r]$, where $S_{prev}$ is the sum of all previously removed cards. Using a two-pointer technique on prefix sums allows us to compute this in linear time.

Another insight is that since card values are positive, sums are strictly increasing as we include more cards. This ensures that the two-pointer approach will always find the minimal-length prefix satisfying the range without backtracking, as any larger prefix is also strictly larger and can be checked sequentially.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Two-Pointer on Prefix Sums | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$, $l$, $r$, and the array of card values $a$. Initialize a prefix sum array $S$ with $S_0 = 0$ and $S_i = S_{i-1} + a_i$. This allows us to compute the sum of any top segment in $O(1)$ as $S[j] - S[i-1]$.
2. Initialize a counter `wins = 0` and a pointer `start = 0`, which indicates the position of the first card remaining in the deck.
3. Use a pointer `end` to iterate over the prefix sums from `start + 1` up to `n`. For each `end`, compute `sum_segment = S[end] - S[start]`.
4. If `sum_segment` exceeds `r`, we cannot take more cards for this round, so increment `start` until `sum_segment <= r` or `start = end`. This is valid because all card values are positive; adding more cards only increases the sum.
5. If `sum_segment` is at least `l` and at most `r`, it counts as a winning round. Increment `wins` and move `start` to `end` to begin the next round with the next card.
6. Repeat until all cards are processed. Output `wins` for this test case.

Why it works: The algorithm maintains the invariant that `start` always points to the first uncollected card, and `end` grows monotonically. Since card values are positive, the sum from `start` to `end` increases with `end`. Two pointers ensure we skip over segments that are too small or too large efficiently. Each card is visited at most twice (once by `start` and once by `end`), guaranteeing linear time per test case.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, l, r = map(int, input().split())
        a = list(map(int, input().split()))
        
        wins = 0
        start = 0
        prefix_sum = [0]*(n+1)
        for i in range(n):
            prefix_sum[i+1] = prefix_sum[i] + a[i]
        
        end = 1
        while start < n:
            while end <= n and prefix_sum[end] - prefix_sum[start] < l:
                end += 1
            if end <= n and prefix_sum[end] - prefix_sum[start] <= r:
                wins += 1
                start = end
                end = start + 1
            else:
                start += 1
                if end <= start:
                    end = start + 1
        print(wins)

if __name__ == "__main__":
    solve()
```

The code initializes prefix sums to quickly compute segment sums. `start` marks the first uncollected card, while `end` searches for the shortest segment whose sum is in the winning range. We increment `wins` when a segment fits the criteria and move `start` to `end` to start the next round. The nested loops never backtrack because all values are positive, so each index is processed linearly.

## Worked Examples

**Sample 1:**

Input: `5 3 10` with cards `[2, 1, 11, 3, 7]`

| start | end | sum_segment | wins |
| --- | --- | --- | --- |
| 0 | 1 | 2 | 0 |
| 0 | 2 | 3 | 1 (take first two cards) |
| start → 2 | end = 3 | 11 | 1 |
| start → 3 | end = 4 | 3 | 2 (take 3) |
| start → 4 | end = 5 | 7 | 3 (take 7) |

**Sample 2:**

Input: `10 1 5` with cards `[17, 8, 12, 11, 7, 11, 21, 13, 10, 8]`

| start | end | sum_segment | wins |
| --- | --- | --- | --- |
| 0 | 1 | 17 | too large |
| start → 1 | end = 2 | 8 | too large |
| ... | ... | ... | 0 |

No segment fits in `[1,5]`, so `wins = 0`.

These traces demonstrate that the two-pointer method correctly identifies winning rounds and skips unfit segments without missing combinations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each card is visited at most twice by `start` and `end` pointers. |
| Space | O(n) | Prefix sum array of size n+1 |

The total sum of `n` across all test cases is $2 \cdot 10^5$, making the total operations under $10^6$. Memory usage is also within the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("8\n5 3 10\n2 1 11 3 7\n10 1 5\n17 8 12 11 7 11 21 13 10 8\n3 4 5\n3 4 2\n8 12 25\n10 7 5 13 8 9 12 7\n2 3 3\n5 2\n9 7 9\n2 10 5 1 3 7 6 2 3\n1
```
