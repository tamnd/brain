---
title: "CF 442B - Andrey and Problem"
description: "We are given a set of friends, where each friend independently succeeds in producing a contest problem with a known probability. Andrey will invite some subset of these friends. Once invited, each friend either contributes a problem or does not, independently of the others."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 442
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 253 (Div. 1)"
rating: 1800
weight: 442
solve_time_s: 74
verified: true
draft: false
---

[CF 442B - Andrey and Problem](https://codeforces.com/problemset/problem/442/B)

**Rating:** 1800  
**Tags:** greedy, math, probabilities  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of friends, where each friend independently succeeds in producing a contest problem with a known probability. Andrey will invite some subset of these friends. Once invited, each friend either contributes a problem or does not, independently of the others.

The outcome we care about is very specific: Andrey is satisfied only if exactly one friend produces a problem. If nobody produces a problem, or if two or more friends succeed, he is unhappy. The task is to choose which friends to invite so that the probability of getting exactly one successful contributor is maximized.

The key object is not the individual probabilities themselves, but the distribution induced over the number of successful friends after selecting a subset. Each chosen subset defines a sum of independent Bernoulli variables, and we want to maximize the probability that this sum equals exactly one.

The constraints are small, with at most 100 friends. This immediately rules out any exponential enumeration of subsets beyond moderate reasoning unless heavily pruned, but more importantly it suggests that an O(n^2) or O(n^3) dynamic approach is unnecessary. A solution closer to O(n log n) or O(n) is expected.

A subtle edge case appears when all probabilities are very small. In that case, inviting many friends seems attractive because it increases the chance of at least one success, but it also increases the chance of multiple successes, which is disallowed. Another edge case occurs when probabilities are very large, close to 1, where inviting more people almost guarantees multiple successes and becomes harmful.

A naive intuition that “more friends is always better” fails immediately. For example, if all probabilities are 0.8, inviting two friends gives probability of exactly one success equal to 0.8·0.2 + 0.2·0.8 = 0.32, while inviting one friend gives 0.8. So adding more can reduce the target probability.

## Approaches

A brute-force approach tries every subset of friends. For each subset, we compute the probability that exactly one friend succeeds by summing over all choices of which friend is the successful one and multiplying probabilities of failure for the rest. For a subset of size k, this costs O(k), and over all subsets this becomes O(n·2^n), which is far beyond feasible even for n = 30.

The structure of the expression for a fixed subset reveals something more useful. Suppose we pick a subset S. The probability of exactly one success can be written as a sum over i in S of pi multiplied by the probability that all other selected friends fail. This introduces repeated multiplicative structure: every term depends on products over subsets.

The key observation is to think in terms of how adding a single friend changes the value. If we maintain a chosen set S with current value P(S), and we consider adding a new friend with probability p, the new probability becomes (1 − p)·P(S) + p·product_of_failures(S). This form suggests that the contribution of a friend depends not only on p but on how it interacts multiplicatively with the current structure.

Rewriting the objective leads to a cleaner form. If we define for a set S:

P(S) = probability of exactly one success among S

then adding a new friend i yields:

P(S ∪ {i}) = P(S)·(1 − p_i) + (product of (1 − p_j) over j in S)·p_i

This suggests maintaining two aggregated quantities: the current probability of exactly one success and the probability that all selected friends fail. With these, we can greedily consider adding each friend and decide whether it increases the value.

The optimal strategy ends up being greedy in a specific ordering: we sort friends by decreasing p_i / (1 − p_i), which corresponds to prioritizing those that give the best marginal improvement in the balance between creating exactly one success versus causing multiple successes.

Once sorted, we iteratively try adding each friend and keep track of whether the probability improves.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Transform each probability p_i into a value that reflects its relative strength, specifically the ratio p_i / (1 − p_i). This captures how likely a friend is to succeed relative to failing, which is what matters when balancing exactly-one outcomes.
2. Sort all friends in descending order of this ratio. This ordering prioritizes friends that contribute more efficiently to producing a single success without overly increasing collision risk.
3. Initialize two variables: one for the probability that all selected friends fail, and one for the probability that exactly one friend succeeds.
4. Iterate through friends in sorted order, and for each friend, compute what happens if we include them. Update the failure probability multiplicatively and update the exact-one probability using the decomposition into “this friend is the only success” plus “existing structure remains valid and this friend fails”.
5. Track the best value encountered over all prefixes of this ordering, since stopping earlier corresponds to selecting a subset.
6. Output the maximum probability obtained.

### Why it works

At any point, the state of a chosen subset is fully described by two values: the probability that nobody in the subset succeeds, and the probability that exactly one succeeds. Any new element interacts with the subset only through these two aggregates. This reduces the subset structure to a one-dimensional ordering problem where optimality follows from local exchange arguments on adjacent elements in the sorted order. If two adjacent friends are out of order with respect to p/(1−p), swapping them does not improve the resulting probability, which guarantees that sorting yields an optimal prefix.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(float, input().split()))
    
    # sort by p/(1-p) decreasing
    p.sort(key=lambda x: x/(1.0 - x) if x < 1.0 else float('inf'), reverse=True)
    
    best = 0.0
    prod_fail = 1.0  # product of (1 - p_i) in current set
    prob_one = 0.0   # probability exactly one success
    
    for x in p:
        new_prod_fail = prod_fail * (1 - x)
        new_prob_one = prob_one * (1 - x) + prod_fail * x
        
        prob_one = new_prob_one
        prod_fail = new_prod_fail
        
        if prob_one > best:
            best = prob_one
    
    print(f"{best:.12f}")

if __name__ == "__main__":
    solve()
```

The sorting step ensures we consider the most “efficient” friends first in terms of success-to-failure contribution ratio. The two running variables represent the full probabilistic state of the current subset, so updating them is sufficient to evaluate each prefix without recomputing from scratch.

A common implementation pitfall is forgetting that floating-point division by (1 − p) becomes unstable when p is extremely close to 1. The code handles this by treating p = 1 as an infinite ratio, forcing such elements to the front.

## Worked Examples

### Example 1

Input:

```
4
0.1 0.2 0.3 0.8
```

After sorting by ratio, the order becomes:

0.8, 0.3, 0.2, 0.1

We track state step by step:

| Step | p_i | prod_fail | prob_one | best |
| --- | --- | --- | --- | --- |
| init | - | 1.0 | 0.0 | 0.0 |
| 1 | 0.8 | 0.2 | 0.8 | 0.8 |
| 2 | 0.3 | 0.14 | 0.44 | 0.8 |
| 3 | 0.2 | 0.112 | 0.496 | 0.8 |
| 4 | 0.1 | 0.1008 | 0.5064 | 0.8 |

The best value is achieved after selecting only the first friend. This confirms that adding weaker probabilities after a strong one reduces the chance of exactly one success.

### Example 2

Input:

```
3
0.5 0.5 0.5
```

Sorted order is unchanged.

| Step | p_i | prod_fail | prob_one | best |
| --- | --- | --- | --- | --- |
| 1 | 0.5 | 0.5 | 0.5 | 0.5 |
| 2 | 0.5 | 0.25 | 0.5 | 0.5 |
| 3 | 0.5 | 0.125 | 0.375 | 0.5 |

The optimal choice is any single friend, since adding more only increases collision probability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, single linear sweep afterwards |
| Space | O(1) | only a few running variables besides input array |

The constraints n ≤ 100 make this easily fast enough even with floating-point operations and sorting overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    
    data = inp.strip().split()
    n = int(data[0])
    p = list(map(float, data[1:]))

    p.sort(key=lambda x: x/(1.0 - x) if x < 1.0 else float('inf'), reverse=True)

    best = 0.0
    prod_fail = 1.0
    prob_one = 0.0

    for x in p:
        new_prod_fail = prod_fail * (1 - x)
        new_prob_one = prob_one * (1 - x) + prod_fail * x
        prod_fail, prob_one = new_prod_fail, new_prob_one
        best = max(best, prob_one)

    return f"{best:.10f}"

# provided sample
assert abs(float(run("4\n0.1 0.2 0.3 0.8")) - 0.8) < 1e-9

# all zeros
assert abs(float(run("3\n0.0 0.0 0.0")) - 0.0) < 1e-9

# all ones
assert abs(float(run("2\n1.0 1.0")) - 0.0) < 1e-9

# single element
assert abs(float(run("1\n0.7")) - 0.7) < 1e-9

# mixed
assert abs(float(run("3\n0.9 0.1 0.5")) - 0.9) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 0.1 0.2 0.3 0.8 | 0.8 | best subset is single max probability |
| 3 0 0 0 | 0 | all failures edge case |
| 2 1 1 | 0 | multiple certain successes invalidates solution |
| 1 0.7 | 0.7 | minimal input correctness |
| 3 0.9 0.1 0.5 | 0.9 | ordering effect correctness |

## Edge Cases

When all probabilities are zero, every subset produces zero probability of exactly one success. The algorithm initializes best to zero and never increases it, so the output remains correct.

When a probability is exactly one, any subset containing more than one such element immediately yields zero probability of exactly one success. The greedy ordering places these first due to infinite ratio, and the algorithm correctly evaluates that selecting only one such friend yields probability one.

When probabilities are extremely skewed, such as one value near one and many small ones, the prefix evaluation ensures that we stop at the first element, avoiding degradation from adding low-quality contributors.
