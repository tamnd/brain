---
title: "CF 462B - Appleman and Card Game"
description: "Appleman has a collection of n cards, each labeled with a capital letter. Toastman is allowed to pick exactly k cards, and for each card he picks, Appleman pays him coins equal to the number of Toastman's cards that have the same letter as that card."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 462
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 263 (Div. 2)"
rating: 1300
weight: 462
solve_time_s: 69
verified: true
draft: false
---

[CF 462B - Appleman and Card Game](https://codeforces.com/problemset/problem/462/B)

**Rating:** 1300  
**Tags:** greedy  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

Appleman has a collection of _n_ cards, each labeled with a capital letter. Toastman is allowed to pick exactly _k_ cards, and for each card he picks, Appleman pays him coins equal to the number of Toastman's cards that have the same letter as that card. In other words, if Toastman picks several cards with the same letter, each of those cards contributes the count of that letter in his hand to the total sum.

The input gives the number of cards _n_, the number of cards to pick _k_, and a string of length _n_ where each character represents a card's letter. The output should be a single integer: the maximum number of coins Toastman can earn if he picks the cards optimally.

The bounds are significant. With _n_ up to 100,000 and a one-second time limit, any algorithm worse than O(n log n) risks timing out. A naive approach that checks all possible subsets of size _k_ is completely infeasible because the number of subsets grows combinatorially, on the order of n choose k.

A non-obvious edge case occurs when multiple letters appear many times but less than _k_ individually. For example, if the cards are `AABBC` and _k_ is 4, a naive approach that simply takes the first _k_ cards in order could choose `AABB` or `ABBC`. The optimal is `AABB` because selecting two As and two Bs maximizes repeated letters and thus coins. Another edge case is when _k_ exceeds the count of the most frequent letter; the algorithm must then supplement with the next most frequent letters.

## Approaches

The brute-force approach would be to examine all combinations of _k_ cards, compute the coin total for each combination, and keep the maximum. This is correct in principle because it tests every possibility, but the number of combinations is astronomically large for _n_ = 100,000 and even moderate _k_, so it is unusable.

The key observation is that the coin gain is quadratic in the number of times a letter appears among the chosen cards. If Toastman selects _x_ cards of the same letter, they contribute _x²_ to the total coins. Therefore, to maximize coins, he should first select as many cards as possible from the letter that appears most frequently, then the next most frequent letter, and so on, until he has selected _k_ cards in total. If the remaining _k_ is less than the count of the next letter, he simply takes that many cards, contributing the square of the count chosen.

This is a classic greedy strategy: always take the letters with the highest frequency first, because they maximize the quadratic gain. Sorting the counts in descending order ensures we always pick the optimal letters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n choose k) | O(n) | Too slow |
| Optimal | O(n + 26 log 26) ≈ O(n) | O(26) ≈ O(1) | Accepted |

## Algorithm Walkthrough

1. Count the occurrences of each letter in the card string. Use a dictionary or a 26-element array for uppercase letters. This gives the frequency of each letter.
2. Sort the frequencies in descending order. This ensures we always pick letters that contribute the most coins first.
3. Initialize a variable `coins = 0` and `remaining = k`. Loop through the sorted frequencies.
4. For each frequency `f`, if `f <= remaining`, add `f * f` to `coins` and subtract `f` from `remaining`.
5. If `f > remaining`, take only `remaining` cards of that letter, add `remaining * remaining` to `coins`, and set `remaining = 0`. Break the loop since we have chosen exactly _k_ cards.
6. Print `coins`.

Why it works: The invariant is that at every step, we have chosen the set of letters that maximizes the sum of squares for the remaining _k_ picks. Squaring a larger number always yields a larger increment than splitting it into smaller groups. Therefore, no other distribution of the same _k_ cards could yield more coins.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
cards = input().strip()

# Step 1: Count letter frequencies
freq = [0] * 26
for c in cards:
    freq[ord(c) - ord('A')] += 1

# Step 2: Sort frequencies descending
freq.sort(reverse=True)

coins = 0
remaining = k

# Step 3: Greedy selection
for f in freq:
    if remaining == 0:
        break
    take = min(f, remaining)
    coins += take * take
    remaining -= take

print(coins)
```

The first section counts letters using ASCII indices for constant-time access. Sorting ensures the greedy choice picks the largest available group first. In the loop, `take = min(f, remaining)` handles the case where the remaining slots are fewer than the frequency, which is easy to overlook and a common source of off-by-one errors.

## Worked Examples

Sample 1:

Input:

```
15 10
DZFDFZDFDDDDDDF
```

| Step | freq sorted | remaining k | coins accumulated | action |
| --- | --- | --- | --- | --- |
| 1 | [9,3,2,1,0...] | 10 | 0 | take 9 of 'D' → coins += 81 |
| 2 | 3 | 1 | 81 | take 1 of 'F' → coins += 1 → total 82 |
| 3 | ... | 0 | 82 | done |

This confirms that picking the largest group first maximizes coins.

Sample 2:

Input:

```
5 3
AABBC
```

| Step | freq sorted | remaining k | coins accumulated | action |
| --- | --- | --- | --- | --- |
| 1 | [2,2,1,...] | 3 | 0 | take 2 of 'A' → coins += 4 → remaining=1 |
| 2 | 2 | 1 | 4 | take 1 of 'B' → coins += 1 → total 5 |

The algorithm handles the case where remaining < frequency correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + 26 log 26) ≈ O(n) | Counting letters is O(n), sorting 26 frequencies is constant |
| Space | O(26) ≈ O(1) | Only frequency array of 26 letters is used |

With n up to 100,000, the O(n) complexity is acceptable, and the memory usage is trivial.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    cards = input().strip()
    freq = [0] * 26
    for c in cards:
        freq[ord(c) - ord('A')] += 1
    freq.sort(reverse=True)
    coins = 0
    remaining = k
    for f in freq:
        if remaining == 0:
            break
        take = min(f, remaining)
        coins += take * take
        remaining -= take
    return str(coins)

# provided sample
assert run("15 10\nDZFDFZDFDDDDDDF\n") == "82"

# custom cases
assert run("5 3\nAABBC\n") == "5", "mixed letters, k less than max count"
assert run("3 3\nAAA\n") == "9", "all letters same"
assert run("4 2\nABCD\n") == "1", "all different, pick 2"
assert run("1 1\nZ\n") == "1", "single card"
assert run("100000 100000\n" + "A"*100000 + "\n") == "10000000000", "max size all same"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 3, AABBC | 5 | greedy selection with partial frequency |
| 3 3, AAA | 9 | all cards same |
| 4 2, ABCD | 1 | all different letters, k < n |
| 1 1, Z | 1 | minimum input |
| 100000 100000, all A | 10000000000 | maximum input size |

## Edge Cases

When _k_ exceeds the frequency of the most common letter, the algorithm correctly continues to the next highest frequency. For example, with input `AABBC` and *k=4`, the most frequent letter 'A' has frequency 2. The algorithm takes both As, leaving 2 remaining. Next, 'B' has frequency 2, and since remaining=2, it takes both Bs. Total coins = 2² + 2² = 8. A naive approach that always takes the first k letters in order could incorrectly sum differently. The greedy invariant ensures at every step that the largest possible contribution is chosen, guaranteeing correctness.
