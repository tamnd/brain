---
title: "CF 104969C - Running out of Pizza Taco"
description: "We are given a fixed queue of people before Shelly arrives, and a shared supply of pizza slices, tacos, and sauce portions."
date: "2026-06-28T18:51:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104969
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 1 (Advanced)"
rating: 0
weight: 104969
solve_time_s: 82
verified: false
draft: false
---

[CF 104969C - Running out of Pizza Taco](https://codeforces.com/problemset/problem/104969/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed queue of people before Shelly arrives, and a shared supply of pizza slices, tacos, and sauce portions. Each person in the queue independently chooses how many items to take, but they are limited by two rules: they can take at most two food items in total, and if they take exactly two sauces, they are allowed to take one extra food item of their choice.

Shelly’s order is already fixed as one pizza slice and one taco, so her concern is not about her own choice but whether the people ahead of her can consume enough resources to exhaust either pizza or tacos before she reaches the counter. The question is whether there exists any sequence of valid choices for the people in front such that at least one of pizza or taco stock becomes zero or negative before Shelly’s turn.

The input gives the number of people before Shelly, followed by the initial quantities of pizza, tacos, and sauces. The output is simply whether depletion of either pizza or tacos is possible under any valid sequence of choices.

The constraints allow up to 100,000 people and item counts up to 100,000. This immediately rules out any simulation that tries to explore all possible combinations of choices per person, since even a small branching factor would explode to exponential time. A solution must reduce the problem to reasoning about worst-case consumption per person.

A subtle issue is that sauce availability can change what each person can take. Without careful handling, one might incorrectly assume sauces are irrelevant or always sufficient. Another trap is assuming each person always takes the same number of items, when in fact the “extra item with two sauces” rule creates two distinct consumption modes that affect whether someone can maximize pizza or taco usage.

The core edge case is when sauces are just enough to enable extra consumption for all people, which can significantly increase total possible demand and change whether depletion is achievable.

## Approaches

A brute-force perspective would try to simulate all possible ways each of the n people can choose items subject to constraints, tracking remaining pizza, tacos, and sauces. For each person, we would branch on whether they take zero, one, or two food items, and whether they spend sauces or not. Even if we prune invalid states when resources go negative, the number of possible states grows exponentially with n, since each person introduces multiple independent decisions. At n = 10^5, this is completely infeasible.

The key observation is that we do not care about the exact sequence of choices, only whether there exists a sequence that exhausts pizza or tacos. This turns the problem into a “maximum possible consumption” question. Instead of simulating people individually, we ask: what is the maximum number of pizza or taco items that could be taken by the first n people under optimal adversarial behavior?

Each person can take up to two items, and sometimes a third if they have exactly two sauces. This means the real question is how many people can be “upgraded” to taking 3 items instead of 2. Since each such upgrade consumes exactly 2 sauces, the number of upgraded people is limited by both Z and n.

So the total maximum number of items taken is bounded by maximizing how many people take 3 items, then the rest take 2. From this we compute the worst-case consumption of a single item type by assuming all items taken are concentrated on pizza (or tacos). If either X or Y is less than or equal to this maximum possible demand for a single category, then depletion is possible.

The problem reduces to checking whether:

we can allocate enough “item slots” among n people, given that at most min(n, Z // 2) people can take 3 items, and the rest take 2 items.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in n | O(n) recursion/state | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We transform the problem into computing the maximum number of items that can be consumed by the first n people.

1. Compute how many people can receive the extra item from sauces. Each such person requires 2 sauces, so the number of upgraded people is `k = min(n, Z // 2)`. This maximizes the number of people who can exploit sauces without exceeding either sauce supply or available people.
2. For these k people, each takes 3 items instead of 2, contributing `3k` total items consumed.
3. For the remaining `n - k` people, each takes only the base maximum of 2 items, contributing `2(n - k)` items.
4. Sum these contributions to get the total maximum number of items that can be consumed before Shelly arrives: `total = 3k + 2(n - k)`.
5. Since we only care about whether pizza or tacos can run out, we consider the worst-case concentration: if all consumed items were of one type, then the maximum possible consumption of a single resource is `total`. We compare `total` against both X and Y.
6. If either X <= total or Y <= total, output “yes”, otherwise output “no”.

### Why it works

The key invariant is that every valid ordering of choices corresponds to a selection of at most two items per person, with a subset of people optionally gaining exactly one additional item if and only if they spend two sauces. The expression `3k + 2(n-k)` captures the maximum total number of item slots any valid configuration can generate, because it saturates both constraints independently: sauce-limited upgrades and per-person caps. Any real execution cannot exceed this bound, and there exists a strategy that achieves it by always maximizing item count per person whenever possible. This reduces the adversarial question to a single scalar comparison.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    X, Y, Z = map(int, input().split())

    k = min(n, Z // 2)
    total = 3 * k + 2 * (n - k)

    if X <= total or Y <= total:
        print("yes")
    else:
        print("no")

if __name__ == "__main__":
    solve()
```

The implementation directly computes the number of people who can be upgraded using sauces, then derives total consumption capacity. The only subtlety is ensuring integer division `Z // 2`, since each upgraded person consumes exactly two sauces.

The final comparison checks both resources independently because depletion of either is sufficient.

## Worked Examples

### Sample 1

Input:

```
n = 21
X = 60
Y = 70
Z = 108
```

We compute how many people can use sauces for upgrades.

| Step | k = min(n, Z//2) | total items | X | Y | Condition |
| --- | --- | --- | --- | --- | --- |
| 1 | min(21, 54) = 21 | 3_21 + 2_0 = 63 | 60 | 70 | X <= total |

Here, all 21 people can be upgraded because 108 sauces allow 54 upgrades, but only 21 people exist. Each takes 3 items, so total consumption is 63. Since pizza supply is 60, it is possible for pizza to be exhausted before Shelly arrives.

This trace shows that sauce abundance allows every person to maximize consumption, increasing pressure on resources.

### Sample 2

Input:

```
n = 19
X = 60
Y = 70
Z = 108
```

| Step | k | total items | X | Y | Condition |
| --- | --- | --- | --- | --- | --- |
| 1 | min(19, 54) = 19 | 3*19 = 57 | 60 | 70 | X > total and Y > total |

Even with full sauce usage, total consumption is only 57 items. Both pizza and tacos exceed this bound, so neither can be fully depleted.

This demonstrates that when supply exceeds maximum possible consumption capacity, no ordering strategy can cause exhaustion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations regardless of input size |
| Space | O(1) | No auxiliary structures are used |

The computation is constant time, which fits easily within constraints up to 100,000 people and item counts.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []

    def input():
        return sys.stdin.readline()

    n = int(sys.stdin.readline().strip())
    X, Y, Z = map(int, sys.stdin.readline().split())

    k = min(n, Z // 2)
    total = 3 * k + 2 * (n - k)

    return "yes\n" if (X <= total or Y <= total) else "no\n"

# provided samples (adapted formatting)
assert run("21\n60 70 108\n") == "yes\n", "sample 1"
assert run("19\n60 70 108\n") == "no\n", "sample 2"

# custom cases
assert run("0\n1 1 1\n") == "no\n", "no people means no consumption"
assert run("1\n1 1 10\n") == "yes\n", "single person can fully consume"
assert run("5\n100 100 0\n") == "no\n", "no sauce, limited consumption"
assert run("10\n5 100 100\n") == "yes\n", "small pizza forces yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0, small supply | no | zero queue edge case |
| 1 person, large sauce | yes | minimal case triggering depletion |
| no sauce | no | verifies 2-item cap only |
| small X | yes | boundary where pizza is exhausted early |

## Edge Cases

One edge case is when there are no people in front. In that case, no consumption happens and neither pizza nor tacos can run out before Shelly. The formula gives `k = 0`, `total = 0`, and correctly yields “no”.

Another case is when sauce supply is extremely large but n is small. Even if Z is huge, upgrades are capped by n, so the algorithm correctly prevents overestimating consumption.

A third case is when Z is zero. Then no upgrades are possible, and total consumption is strictly `2n`. This correctly models the constraint that no one can exceed two items.
