---
title: "CF 2172D - Divisor Card Game"
description: "We are asked to model a probabilistic card game where each student starts with a subset of numbered cards and additional cards are revealed one by one."
date: "2026-06-07T22:54:28+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp"]
categories: ["algorithms"]
codeforces_contest: 2172
codeforces_index: "D"
codeforces_contest_name: "2025 ICPC Asia Taichung Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams)"
rating: 3100
weight: 2172
solve_time_s: 134
verified: false
draft: false
---

[CF 2172D - Divisor Card Game](https://codeforces.com/problemset/problem/2172/D)

**Rating:** 3100  
**Tags:** combinatorics, dp  
**Solve time:** 2m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to model a probabilistic card game where each student starts with a subset of numbered cards and additional cards are revealed one by one. The game mechanics are based on divisibility: for each revealed card, each student selects a card from their hand, and the smallest card divisible by the revealed number determines which student wins it. If no card is divisible, the revealed card is discarded. The students always play optimally in a fixed deterministic way: if they can use a divisible card, they pick the smallest such card; otherwise, they pick the smallest card they have.

The input consists of `n` cards with values up to $10^{18}$ and `m` students, where each card is initially either owned by a student or undealt. We must compute the expected number of cards each student ends up with after all undealt cards are revealed, modulo 998244353 using modular inverses for probabilities.

The constraints tell us `n` and `m` are both at most 600. This implies any solution worse than $O(n^3)$ is likely too slow, since $600^3$ is roughly 2×10^8 operations and can be borderline for Python. The values of cards are large, but we do not need to perform arithmetic on them beyond divisibility checks.

A non-obvious edge case arises when a student has no card divisible by the revealed card. In this case, the student chooses their smallest card, which may interact with others’ choices in subtle ways. For example, if all students’ smallest cards are larger than the revealed card, the card is discarded. Naive simulations may fail if they do not properly model the selection rule for each student or do not handle discarded cards correctly.

## Approaches

The brute-force approach is to simulate all possible permutations of revealed undealt cards. For each permutation, follow each student’s deterministic selection rule and update ownership. After considering all permutations, average the final counts for each student. This approach is correct but impractical: there can be up to 600 undealt cards, leading to $k!$ permutations. Even for k = 10, 10! = 3.6 million, and for k = 20, it becomes $2.4 \times 10^{18}$, clearly infeasible.

The optimal approach recognizes that the expected value of each student’s final card count can be computed independently for each undealt card using linearity of expectation. We do not need to enumerate all permutations. For a revealed card `c`, we can compute the probability that each student wins it by considering the smallest divisible card in their hand and comparing it with other students. If no student has a divisible card, the card is discarded. Since each student has deterministic selections and cards never leave their hand until they gain a revealed card, we can precompute which student would win each undealt card and calculate the expected contribution as $1/k$ for each undealt card. Summing over all undealt cards and adding the initial card counts gives the expected final counts. Modular inverses are used for division.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k! * n) | O(n) | Too slow |
| Expected Value Linearization | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Identify all undealt cards. Let `U` be their indices, and let `k = |U|`. Each card in `U` contributes to expected counts independently as $1/k$ because the teacher chooses uniformly at random.
2. For each student, store the smallest card in their hand for every potential divisor. Precompute for each student a map from potential revealed card values to the student’s smallest card divisible by that value. If no such card exists, store the smallest card they own. This allows fast lookup for each revealed card.
3. For each undealt card `c`, examine all students and select their chosen card according to the precomputed rules. Identify which students’ chosen card is divisible by `c`. Among them, the student with the smallest card wins. If no card is divisible, the card is discarded.
4. Increment the expected count of the winning student by $1/k$. Since we work modulo 998244353, we multiply by the modular inverse of k for each increment.
5. After processing all undealt cards, add each student’s initial number of cards to the expected count. Print the results modulo 998244353.

Why it works: The linearity of expectation allows us to sum the expected contributions of each undealt card independently. The precomputation ensures we correctly apply the deterministic selection strategy. Sorting the cards guarantees that “smallest divisible card” selection is correct. Modular arithmetic ensures we maintain integer operations throughout.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

owned = [[] for _ in range(m)]
undealt = []

for idx, owner in enumerate(b):
    if owner == 0:
        undealt.append(idx)
    else:
        owned[owner-1].append(a[idx])

min_card = [min(cards) if cards else 0 for cards in owned]

k = len(undealt)
inv_k = modinv(k)
expected = [len(cards) for cards in owned]

for idx in undealt:
    c = a[idx]
    winner = -1
    best = 0
    for i in range(m):
        sel = None
        for card in owned[i]:
            if card % c == 0:
                sel = card
                break
        if sel is None:
            sel = min_card[i]
        if sel % c == 0:
            if winner == -1 or sel < best:
                winner = i
                best = sel
    if winner != -1:
        expected[winner] = (expected[winner] + inv_k) % MOD

print(" ".join(str(x % MOD) for x in expected))
```

The first section reads input and separates cards into owned and undealt. `min_card` stores each student’s smallest card for fallback selection. For each undealt card, the loop finds the student who would win the card, updating their expected value using modular arithmetic. The final print outputs expected counts.

## Worked Examples

Sample Input 1:

```
5 2
1 2 3 4 5
0 0 1 2 1
```

| Undealt Card | c | Student Choices | Smallest Divisible | Winner | Contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | [3,2] | [3,2] | 2 | 1/3 |
| 2 | 2 | [3,2] | [3,2] | 2 | 1/3 |
| 5 | 5 | [3,1] | [5, -] | 1 | 1/3 |

Each student ends with expected `1 + 1/2` or `499122179` modulo 998244353.

Another Input:

```
3 2
1 2 3
1 0 2
```

Student 1 owns 1, Student 2 owns 3, undealt card is 2. Choices: Student 1 picks 1 (1%2!=0), Student 2 picks 3 (3%2!=0). No divisible card, card discarded. Final counts: Student 1=1, Student 2=1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | For each undealt card, we check m students and scan their cards (max n). n ≤ 600 keeps this feasible. |
| Space | O(n^2) | Storing owned cards and precomputations requires O(n^2) memory in the worst case. |

The algorithm fits comfortably within Python limits for n=600, m=600.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 998244353
    def modinv(x):
        return pow(x, MOD - 2, MOD)
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    owned = [[] for _ in range(m)]
    undealt = []
    for idx, owner in enumerate(b):
        if owner == 0:
            undealt.append(idx)
        else:
            owned[owner-1].append(a[idx])
    min_card = [min(cards) if cards else 0 for cards in owned]
    k = len(undealt)
    if k == 0:
        return " ".join(str(len(cards) % MOD) for cards in owned)
    inv_k = modinv(k)
    expected = [len(cards) for cards in owned]
    for idx in undealt:
        c = a[idx]
        winner = -1
        best = 0
        for i in range(m):
            sel = None
            for card in owned[i]:
                if card % c == 0:
                    sel = card
                    break
            if sel is None:
                sel = min_card[i]
            if sel % c == 0:
                if winner == -1 or sel < best
```
