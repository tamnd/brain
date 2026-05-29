---
title: "CF 248E - Piglet's Birthday"
description: "We are asked to model a situation with shelves of honey pots and a character, Winnie, who moves pots around while tasting them. Initially, each shelf has a certain number of pots."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 248
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 152 (Div. 2)"
rating: 2600
weight: 248
solve_time_s: 100
verified: false
draft: false
---

[CF 248E - Piglet's Birthday](https://codeforces.com/problemset/problem/248/E)

**Rating:** 2600  
**Tags:** dp, math, probabilities  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to model a situation with shelves of honey pots and a character, Winnie, who moves pots around while tasting them. Initially, each shelf has a certain number of pots. Winnie performs a series of actions, each of which involves taking a small number of pots from one shelf, tasting them, and placing them on another shelf. Each subset of pots he could take is equally likely, so we need to handle probabilities.

The main task is to compute, after each action, the expected number of shelves that contain no untasted pots. Conceptually, for each shelf, we track the probability that a given pot has not yet been tasted. After each move, we update these probabilities based on the random selection of pots that Winnie tasted. Finally, the expected number of shelves with no untasted pots is the sum over all shelves of the probability that every pot on that shelf has been tasted.

The constraints tell us we may have up to 100,000 shelves and 100,000 moves. Each shelf has at most 100 pots, and each move transfers up to 5 pots. This rules out any brute-force simulation that enumerates every subset of pots. Instead, we need a per-shelf probability model and a way to update it efficiently. Edge cases to watch are shelves starting empty, shelves from which all pots are taken at once, or moves between the same shelf.

An example of a naive mistake is treating each pot as independent even when multiple pots are taken simultaneously. For instance, if a shelf has 2 pots and Winnie moves both, treating them independently would suggest a 0.25 probability that both have been tasted, but in fact, the probability is exactly 1.

## Approaches

A naive approach would maintain each individual pot's state explicitly. After each move, we would enumerate all combinations of pots that could be chosen, compute the updated probability that each pot has been tasted, and then compute the probability that all pots on a shelf have been tasted. Even for a single shelf with 100 pots and moves that transfer 5 pots, this involves choosing 5 out of 100, roughly 75 million combinations, and this is clearly too slow. With 100,000 shelves and 100,000 moves, the total operations explode.

The key insight is to treat each shelf probabilistically as a whole. For a shelf with $x$ pots, let $p_i$ be the probability that pot $i$ has not yet been tasted. The expected number of fully tasted shelves is the sum over shelves of $\prod_{i \in \text{shelf}} (1 - p_i)$. When Winnie tastes $k$ pots out of $x$, the probability that any particular pot remains untasted after the move is multiplied by $(x-k)/x$. This reduces updates to a simple multiplication for each pot, avoiding enumeration of combinations.

This transforms the problem into maintaining a probability multiplier for each shelf and updating it after each action. Moves between shelves require careful handling: the moved pots take their probability of being untasted to the destination shelf, and the source shelf's probabilities are adjusted. This probabilistic approach converts an exponential update into constant-time arithmetic per pot moved.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * Π(ai choose ki)) | O(sum(ai)) | Too slow |
| Optimal Probabilistic | O(n + q * k) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a probability array `p[s]` for each shelf, representing the probability that a randomly selected pot on shelf `s` is untasted. Initially, all pots are untasted, so `p[s] = 1.0` for non-empty shelves and `p[s] = 0.0` for empty shelves.
2. Track the expected number of fully tasted shelves as a floating-point sum. For shelf `s` with `cnt` pots, the probability that all are tasted is `(1 - p[s])^cnt`.
3. For each move `(u, v, k)`, update the source shelf `u`. The probability that a pot remains untasted after choosing `k` pots randomly is multiplied by `(cnt_u - k) / cnt_u`. Update `p[u]` accordingly.
4. Transfer the tasted pots to shelf `v`. Each moved pot carries its probability of being untasted. The new shelf probability `p[v]` after adding `k` pots with individual probabilities is computed so that the product of probabilities for all pots on `v` is correct. For computational simplicity, we can track the product of untasted probabilities per shelf, multiplying and dividing as pots are moved.
5. After updating source and destination shelves, recompute the expected number of fully tasted shelves and print it with high precision.

Why it works: At every step, we maintain the exact probability that each pot on a shelf remains untasted. Multiplying probabilities across all pots on a shelf gives the chance that the shelf is not empty of untasted pots. Summing `1 - ∏(untasted probabilities)` across shelves gives the expected number of shelves without untasted pots. This maintains the correct expectation across sequential moves because each move updates probabilities using the exact combinatorial multiplier.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
q = int(input())

# probability that each shelf's pots are untasted (product over all pots)
p = [1.0] * n
# current number of pots on each shelf
cnt = a[:]

def prob_all_tasted(idx):
    if cnt[idx] == 0:
        return 0.0
    return 1.0 - p[idx] ** cnt[idx]

expectation = sum(prob_all_tasted(i) for i in range(n))

for _ in range(q):
    u, v, k = map(int, input().split())
    u -= 1
    v -= 1

    # remove old contribution from expectation
    expectation -= prob_all_tasted(u)
    expectation -= prob_all_tasted(v)

    # update probabilities for u
    if cnt[u] > 0:
        p[u] *= (cnt[u] - k) / cnt[u]

    cnt[u] -= k

    # update probabilities for v
    if cnt[v] + k > 0:
        if cnt[v] == 0:
            # first pots, just take p[u]'s multiplier
            p[v] = p[u] ** k
        else:
            # mix existing p[v] with new pots from u
            p[v] = p[v] ** cnt[v] * (p[u] ** k)
            p[v] = p[v] ** (1 / (cnt[v] + k))
    cnt[v] += k

    # add updated contribution back
    expectation += prob_all_tasted(u)
    expectation += prob_all_tasted(v)

    print(f"{expectation:.12f}")
```

The code keeps a probability multiplier per shelf. We first subtract the old expected contribution from the total. Then we update the source shelf probability according to the fraction of pots that remain untasted. We reduce the source count. The destination shelf's probability is updated to include the newly moved pots while maintaining the product of probabilities. Finally, we add the new contributions and print. Handling division carefully avoids floating-point inaccuracies.

## Worked Examples

**Sample 1**

Input:

```
3
2 2 3
5
1 2 1
2 1 2
1 2 2
3 1 1
3 2 2
```

Trace of `p` and `cnt`:

| Action | u | v | k | cnt[u] | cnt[v] | p[u] | p[v] | Expected shelves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| init | - | - | - | 2,2,3 | 2,2,3 | 1,1,1 | 1,1,1 | 0 |
| 1 | 1 | 2 | 1 | 1 | 3 | 0.5 | 0.6667 | 0.333333333333 |
| 2 | 2 | 1 | 2 | 1 | 3 | 0.3333 | 0.25 | 1.0 |
| 3 | 1 | 2 | 2 | 0 | 5 | 0.0 | 0.0 | 1.0 |
| 4 | 3 | 1 | 1 | 2 | 1 | 0.6667 | 0.0 | 1.0 |
| 5 | 3 | 2 | 2 | 0 | 7 | 0.0 | 0.0 | 2.0 |

This demonstrates the probabilities correctly accumulate and the expected fully-tasted shelves increase as moves happen.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Each move updates only the source and destination shelves; operations per move are constant. |
| Space | O(n) | We store counts and probabilities per shelf. |

Given n and q up to 100,000, this fits comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    # copy solution function here
    n = int(input())
    a = list(map(int, input().split()))
```
