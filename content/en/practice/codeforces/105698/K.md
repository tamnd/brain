---
title: "CF 105698K - Kaz's Party"
description: "We are given a set of n friends sitting at a party, each of whom has a uniquely preferred drink. Kaz assigns each friend exactly one drink, forming a permutation of size n. Some friends may immediately receive their correct drink, while others do not."
date: "2026-06-22T04:58:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105698
codeforces_index: "K"
codeforces_contest_name: "OCPC 2024 Summer, Day 5: OCPC Potluck Contest 2"
rating: 0
weight: 105698
solve_time_s: 47
verified: true
draft: false
---

[CF 105698K - Kaz's Party](https://codeforces.com/problemset/problem/105698/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of n friends sitting at a party, each of whom has a uniquely preferred drink. Kaz assigns each friend exactly one drink, forming a permutation of size n. Some friends may immediately receive their correct drink, while others do not.

The interesting part is what happens after this initial assignment. Anyone who already has the correct drink leaves the system. The remaining people, who are still unhappy, put all of their drinks back into a common pool. These drinks are then randomly shuffled and redistributed among the remaining people. Again, anyone who now happens to receive their correct drink leaves, and the process repeats. This continues until nobody remains.

The quantity we are asked to control is the expected number of these shuffle rounds. We are allowed to choose the initial assignment of drinks, and we want to maximize how long, in expectation, this repeated random “repair by shuffling” process takes.

The key input is only n, the number of participants. The output consists of two parts: a real number representing the maximum possible expected number of rounds, and a permutation describing how drinks are initially assigned.

The constraint n ≤ 1000 means any solution that simulates randomness explicitly or considers exponential structures is immediately infeasible. Even O(n^2) constructions are fine, but anything involving repeated probabilistic simulation or dynamic states over permutations would be too slow or conceptually unnecessary if a closed-form structure exists.

A subtle edge case appears when n = 1. If the only person receives their own drink, they leave immediately and the process ends with zero rounds. A naive assumption that “there is always at least one round” would fail here.

For n = 2, the structure becomes informative. If both people are swapped, the process finishes in exactly one shuffle round, because the next shuffle immediately resolves both. This already hints that the structure of the initial permutation directly determines how many participants are active at the start of the process, and that this initial state dominates the answer.

## Approaches

The brute-force perspective starts by fixing a permutation and trying to compute the expected number of rounds under the described stochastic process. For any state of k remaining participants, one would simulate that a uniform random permutation is applied to k items, count how many fixed points appear, remove them, and continue. Even if we could compute the expectation for one permutation efficiently, evaluating all n! permutations is impossible.

The critical simplification comes from separating the role of the initial permutation from the randomness of the process. After the first assignment, the only thing that matters is how many people are initially “wrong”, because every subsequent round completely destroys structure by applying a fresh uniform random permutation to the remaining set. The identity of who is wrong is irrelevant, only the size of the remaining set matters.

A key probabilistic fact is that in a uniform random permutation of k elements, the expected number of fixed points is always exactly 1 for k ≥ 1. This means that in every round where there is at least one remaining participant, the expected number of people who leave that round is 1.

So if we start with k people in the system, the expected decrease in the number of active participants per round is 1 each time, until the system becomes empty. This makes the expected number of rounds equal to k.

Therefore, the entire problem collapses into maximizing k, the number of people who are initially wrong. This is achieved by minimizing the number of fixed points in the initial permutation. The best possible permutation is a derangement, where no index i satisfies p[i] = i, so k = n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Construct derangement | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. If n equals 1, output a permutation containing only 1 and set the expected value to 0. The process starts empty because the only participant is already correct, so no shuffle ever occurs.
2. If n is greater than 1, construct any permutation with no fixed points. A simple construction is shifting every index by one position, sending i to i + 1 and sending n to 1. This guarantees every friend initially has the wrong drink.
3. Output the expected number of rounds as n. This follows because all n participants begin in the exchange process and the expected number of participants removed per round is always 1.
4. Output the constructed permutation.

The important design choice is ensuring zero fixed points initially. Any fixed point immediately reduces the initial active set and strictly reduces the expected number of rounds, since every fixed point is a participant who never enters the exchange process at all.

### Why it works

Let k be the number of people who do not initially receive their correct drink. Those are exactly the participants who enter the exchange process. In every round, regardless of history, the remaining set is reshuffled uniformly at random, so the expected number of people who leave in a round is always 1 as long as at least one person remains. By linearity of expectation, the total expected number of rounds is exactly k. Since k cannot exceed n, the maximum is achieved when k = n, which happens exactly when the permutation is a derangement.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

if n == 1:
    print("0.0")
    print(1)
    exit()

# build derangement: shift by 1
p = list(range(2, n + 1)) + [1]

print(float(n))
print(*p)
```

The first step handles the degenerate case where no exchange process is possible. For all larger n, the construction guarantees a permutation without fixed points using a simple cyclic shift. This is sufficient because any derangement is optimal.

The printed value is simply n converted to floating point format. There is no dependence on the structure beyond ensuring maximal initial participation.

A common mistake here is attempting to simulate the process or compute probabilities explicitly. The key is that the process “resets randomness” each round, making the system depend only on the current set size, not on history.

## Worked Examples

Consider n = 3 with permutation [2, 3, 1].

| Round | Active set size | Expected removals | Remaining |
| --- | --- | --- | --- |
| 0 | 3 | - | 3 |
| 1 | 3 | 1 | 2 |
| 2 | 2 | 1 | 1 |
| 3 | 1 | 1 | 0 |

This trace shows that each round removes one participant in expectation until the system empties. The initial size directly determines the expected number of rounds.

For n = 1 with permutation [1], the system starts empty:

| Round | Active set size | Expected removals | Remaining |
| --- | --- | --- | --- |
| 0 | 0 | - | 0 |

This confirms that no shuffle occurs and the expected number of rounds is zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | constructing a simple cyclic permutation |
| Space | O(n) | storing the permutation |

The constraints allow up to 1000 elements, so a linear construction is easily sufficient. There is no simulation or iterative process required beyond building the output permutation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(sys.stdin.readline().strip())

    if n == 1:
        return "0.0\n1\n"

    p = list(range(2, n + 1)) + [1]
    return f"{float(n)}\n" + " ".join(map(str, p)) + "\n"

# provided sample
assert run("2\n") == "2.0\n2 1\n"

# custom cases
assert run("1\n") == "0.0\n1\n", "minimum case"

assert run("3\n") == "3.0\n2 3 1\n", "small derangement"

assert run("5\n") == "5.0\n2 3 4 5 1\n", "cyclic shift correctness"

assert run("1000\n").split("\n")[0] == "1000.0\n".strip(), "large n format check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0.0 / 1 | base case correctness |
| 3 | 3.0 / 2 3 1 | small cycle behavior |
| 5 | 5.0 / 2 3 4 5 1 | general derangement construction |
| 1000 | 1000.0 / permutation | scalability and formatting |

## Edge Cases

For n = 1, the algorithm outputs a trivial permutation and correctly returns 0.0 because no participant enters the exchange process. The constructed logic bypasses the derangement step entirely.

For n = 2, the permutation [2, 1] ensures both participants are initially incorrect. After one shuffle, both are resolved simultaneously in expectation, giving exactly two participants worth of expected rounds.

For larger n, the cyclic shift guarantees no fixed points, meaning all participants contribute to the process from the start. The expected number of rounds scales linearly with n because the process removes exactly one participant per round in expectation.
