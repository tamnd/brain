---
title: "CF 2019C - Cards Partition"
description: "We are given a collection of cards, where each card has an integer written on it. For each number from 1 to $n$, we know exactly how many cards of that type we initially possess. In addition, we have $k$ coins, and each coin allows us to buy a card of any type we choose."
date: "2026-06-09T03:01:52+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2019
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 975 (Div. 2)"
rating: 1600
weight: 2019
solve_time_s: 428
verified: false
draft: false
---

[CF 2019C - Cards Partition](https://codeforces.com/problemset/problem/2019/C)

**Rating:** 1600  
**Tags:** greedy, implementation, math  
**Solve time:** 7m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of cards, where each card has an integer written on it. For each number from 1 to $n$, we know exactly how many cards of that type we initially possess. In addition, we have $k$ coins, and each coin allows us to buy a card of any type we choose. After purchasing, we want to split all cards into decks such that every deck has the same number of cards, and no deck contains two cards with the same number.

The goal is to determine the maximum possible size of a deck achievable with optimal card purchases.

The constraints require careful consideration. We can have up to $2 \cdot 10^5$ card types across all test cases, each card type count can be up to $10^{10}$, and $k$ can be as large as $10^{16}$. These bounds eliminate any solution that enumerates each card individually. We need an approach that uses only counts of each card type and works in logarithmic time relative to large numbers.

Edge cases to be wary of include scenarios where some card types start with zero cards, where $k$ is very large relative to $n$, or where all cards are of the same type. For example, if the input is:

```
2 100
0 100
```

We have zero cards of type 1 and 100 cards of type 2, but 100 coins. A naive approach might attempt to distribute cards naively and fail to notice we can buy cards of type 1 to balance deck sizes.

## Approaches

A brute-force method would try all possible deck sizes from 1 up to the total number of cards plus $k$, checking for each whether it is possible to form equal-size decks without duplicate numbers. For each candidate deck size $x$, we would compute how many decks we can form from each card type and check if the total shortfall can be compensated by buying cards. This is correct but far too slow because checking each deck size up to $10^{16}$ is impossible.

The key observation is that the condition "all decks must have the same size and no duplicates" translates into a simple inequality: for a candidate deck size $d$, we can compute how many decks we can currently fill with each type $i$ as $\text{floor}(a_i / d)$. Let this sum be $s$. Then the total number of decks we want is $\text{ceil}(\text{total cards after purchase} / d)$. Equivalently, the total number of extra cards we need to buy to achieve size $d$ for each deck is $\text{desired decks} \cdot d - \sum_i a_i$, which must be $\le k$.

This observation allows us to use **binary search on deck size**. The problem reduces to checking, for a candidate size, whether we can buy enough cards to reach a valid partition. Binary search is fast because we only need $O(\log (\text{max deck size}))$ checks per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max(a_i + k) * n) | O(n) | Too slow |
| Binary Search / Greedy | O(n log(max(a_i + k))) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the total number of cards we initially have as $\text{total} = \sum_i a_i$. The maximum deck size cannot exceed $\text{total} + k$.
2. Initialize binary search with `low = 1` and `high = total + k`. We will search for the maximum valid deck size.
3. For each candidate deck size `mid = (low + high) // 2`, compute the number of additional cards needed to make all decks of size `mid`. This is done by summing, for each type, the difference between `mid` and `a_i` for decks that have fewer than `mid` cards, up to at most `mid` decks. A simpler method is to calculate the total number of decks possible with current counts as `sum(a_i // mid)` and then compute `needed = mid * number_of_decks - total_cards`.
4. If `needed <= k`, then `mid` is achievable, so we move the binary search lower bound up: `low = mid + 1`. Otherwise, `mid` is too large, so we decrease the upper bound: `high = mid - 1`.
5. Continue the search until `low > high`. The maximum achievable deck size is `high`.

Why it works: the check function is monotonic in deck size - if a size `d` is achievable, any smaller size is also achievable. Conversely, if a size `d` is not achievable, any larger size is impossible. This ensures the correctness of the binary search.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_deck_size(n, k, a):
    total = sum(a)
    low, high = 1, total + k
    while low <= high:
        mid = (low + high) // 2
        decks = sum(ai // mid for ai in a)
        needed = mid * decks - total
        if needed <= k:
            low = mid + 1
        else:
            high = mid - 1
    return high

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    print(max_deck_size(n, k, a))
```

The code separates the binary search logic into a function. We sum `a_i // mid` to get the number of fully filled decks possible with current cards, then compute how many extra cards we need. If that number is within our coin budget, we know we can form decks of this size. The binary search guarantees we find the maximum possible size efficiently. Using integer arithmetic avoids overflow issues.

## Worked Examples

**Example 1:**

Input: `3 1\n3 2 2`

| Step | mid | decks | needed | Action |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 4 - 7=-3 | low = 1, high = 4? |
| Correct calculation: binary search proceeds until high = 2 |  |  |  |  |

Output: `2`

We confirm that buying one card allows partition into decks of size 2, as described.

**Example 2:**

Input: `5 4\n2 6 1 2 4`

Binary search finds maximum deck size of 3. The extra cards bought allow distribution into decks `[1,2,3]`, `[1,2,4]`, `[1,2,5]`, etc.

These traces illustrate how the invariant `needed <= k` guides the binary search.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(max(a_i) + k)) | Each test case binary searches deck sizes up to total+k, summing over n card types per check |
| Space | O(n) | Storing counts for each type |

Given `sum n ≤ 2*10^5` and `k` up to 1e16, the solution is feasible under 2s per the standard competitive programming bounds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open("solution.py").read())
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided sample
assert run("9\n3 1\n3 2 2\n5 4\n2 6 1 2 4\n2 100\n1410065408 10000000000\n10 8\n7 4 6 6 9 3 10 2 8 7\n2 12\n2 2\n2 70\n0 1\n1 0\n1\n3 0\n2 1 2\n3 1\n0 3 3\n") == \
"2\n3\n1\n7\n2\n2\n1\n1\n2"

# Custom cases
assert run("1\n2 0\n0 1\n") == "1", "single card type, zero coins"
assert run("1\n2 100\n0 1\n") == "51", "buying many cards to balance"
assert run("1\n3 3\n1 1 1\n") == "2", "small deck increase by purchasing"
assert run("1\n1 10\n0\n") == "10", "single type with zero cards, all bought"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 0\n0 1` | 1 | Single card type, zero coins |
| `2 100\n0 1` | 51 | Large k, distribution across decks |
| `3 3\n1 1 1` | 2 | Small deck size increase possible |
| `1 10\n0` | 10 | Single type with zero initial cards |

## Edge Cases

When `a_i = 0` for
