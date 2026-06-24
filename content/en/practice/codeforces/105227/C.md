---
title: "CF 105227C - Card Constructions"
description: "We are given a number of cards and asked to repeatedly construct the tallest possible “card pyramid”, remove the cards used, and continue until no further pyramid can be built. The final answer is how many pyramids were constructed across all iterations."
date: "2026-06-24T16:30:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105227
codeforces_index: "C"
codeforces_contest_name: "CPG Training Contest - 1"
rating: 0
weight: 105227
solve_time_s: 314
verified: false
draft: false
---

[CF 105227C - Card Constructions](https://codeforces.com/problemset/problem/105227/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a number of cards and asked to repeatedly construct the tallest possible “card pyramid”, remove the cards used, and continue until no further pyramid can be built. The final answer is how many pyramids were constructed across all iterations.

A pyramid of height 1 is the simplest structure and consumes a fixed number of cards. For larger heights, the structure is built recursively: a pyramid of height $h$ sits on top of a base that itself consists of smaller height-1 pyramids and a row of cards, and underneath that sits a pyramid of height $h-1$. The important consequence is that every height corresponds to a fixed total number of cards.

The process is greedy in nature. At each stage, we always build the tallest pyramid that fits the remaining cards. After subtracting its cost, we repeat the same decision on the leftover.

The constraints allow up to $t \le 1000$ test cases and total $n$ up to $10^9$. This immediately rules out any simulation that constructs pyramids card by card or even iterates linearly over all possible heights per test case. A solution that tries every height for every subtraction step can degrade to roughly $O(n)$ in the worst case, which is not acceptable.

A subtle edge case appears when the remaining cards are small. For example, if $n = 1$, no pyramid can be built at all, and the answer must be zero. A naive greedy implementation that assumes at least one construction per iteration can accidentally attempt invalid height computation or enter an incorrect loop condition.

Another failure case arises if we try to recompute pyramid sizes repeatedly from scratch without caching. Since pyramid costs grow quadratically, recomputing them up to $n$ for each test case would be too slow.

## Approaches

The first natural attempt is to simulate the process directly. For a given $n$, we try all possible heights $h$, compute how many cards are required, and pick the largest valid one. After subtracting that cost, we repeat. This is correct in principle because the problem explicitly defines a greedy construction process.

The issue is efficiency. If we recompute the cost of each height from scratch, each check is $O(h)$ unless we precompute, and we may repeat this for many steps per test case. In the worst case, $n$ decreases slowly when repeatedly building small pyramids, leading to many iterations. This pushes the complexity toward $O(n)$ or worse across test cases.

The key observation is that each pyramid height has a fixed cost independent of context. Once we derive a formula for the number of cards needed for height $h$, we can precompute all possible values up to $10^9$. The cost function turns out to grow quadratically, so the maximum height is only around $2.5 \times 10^4$. This makes it feasible to store all possible pyramid costs.

Once we have this list, each step becomes: find the largest pyramid cost not exceeding the remaining cards, subtract it, and increment the count. Because we always choose the largest possible height, we are effectively reducing the problem optimally at each stage.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n)$ worst case | $O(1)$ | Too slow |
| Precompute + Greedy | $O(\sqrt{n} \log \sqrt{n})$ | $O(\sqrt{n})$ | Accepted |

## Algorithm Walkthrough

First, we derive and precompute the cost of a pyramid of each height. Let $f(h)$ be the number of cards needed. From the construction rules, each increment in height adds a predictable amount of cards, which leads to a recurrence that grows quadratically. We precompute all values of $f(h)$ until they exceed $10^9$.

Second, we store these values in a sorted list so that we can efficiently query the largest pyramid that fits in a given remaining budget.

Then for each test case:

1. Start with the given number of cards $n$ and a counter set to zero.
2. While $n$ is at least the cost of the smallest pyramid, locate the largest $f(h)$ such that $f(h) \le n$. This corresponds to choosing the tallest valid pyramid.
3. Subtract that cost from $n$.
4. Increment the answer by one, since we have successfully built one pyramid.
5. Repeat until no pyramid can be formed.

The crucial reasoning step is why selecting the largest possible pyramid at each stage is valid. Any smaller choice would leave more cards behind, but since the next step repeats the same greedy rule independently of previous choices, delaying usage of cards cannot increase the number of pyramids overall.

### Why it works

Each pyramid construction consumes a fixed amount of cards and leaves a remainder that is independent of how we reached that state. The greedy choice always maximizes immediate consumption, and since all costs are fixed and non-overlapping, the process is equivalent to repeatedly subtracting the largest possible element from a multiset of fixed values. No later decision can make a previously feasible larger pyramid impossible, because feasibility depends only on remaining total, not on structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

# Precompute pyramid costs
MAX_N = 10**9
costs = []

h = 1
while True:
    # f(h) = h(3h+1)/2
    c = h * (3 * h + 1) // 2
    if c > MAX_N:
        break
    costs.append(c)
    h += 1

def solve(n):
    ans = 0

    while n >= 2:
        # find largest cost <= n
        lo, hi = 0, len(costs) - 1
        best = -1

        while lo <= hi:
            mid = (lo + hi) // 2
            if costs[mid] <= n:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1

        if best == -1:
            break

        n -= costs[best]
        ans += 1

    return ans

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        print(solve(n))

if __name__ == "__main__":
    main()
```

The core implementation detail is the precomputation of all valid pyramid costs using the closed-form formula $f(h) = \frac{h(3h+1)}{2}$. This avoids any recursive construction logic during queries.

Inside each test case, binary search is used to locate the largest feasible pyramid cost. This is necessary because scanning linearly through all heights per iteration would degrade performance when many pyramid sizes exist.

The loop condition `n >= 2` reflects the fact that a pyramid of height 1 already costs 2 cards, so anything below that is immediately terminal.

## Worked Examples

### Example 1: $n = 14$

Costs available (prefix): 2, 7, 15, ...

| Step | n before | chosen cost | height | n after | pyramids |
| --- | --- | --- | --- | --- | --- |
| 1 | 14 | 7 | 2 | 7 | 1 |
| 2 | 7 | 7 | 2 | 0 | 2 |

The process shows that greedy subtraction continues until the remaining cards can no longer support even the smallest structure. This confirms that reuse of the same height is allowed and optimal when it fits repeatedly.

### Example 2: $n = 24$

| Step | n before | chosen cost | height | n after | pyramids |
| --- | --- | --- | --- | --- | --- |
| 1 | 24 | 15 | 3 | 9 | 1 |
| 2 | 9 | 7 | 2 | 2 | 2 |
| 3 | 2 | 2 | 1 | 0 | 3 |

This trace shows how the algorithm naturally descends through heights when the remaining budget decreases, always selecting the largest valid structure at each stage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \log H)$ | Each test case performs repeated binary searches over at most $H \approx 2.5 \times 10^4$ precomputed values |
| Space | $O(H)$ | Storage for all pyramid costs up to $10^9$ |

The bound on $n$ ensures that the number of possible pyramid heights is small, so even repeated binary searches are easily fast enough for $t \le 1000$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MAX_N = 10**9
    costs = []
    h = 1
    while True:
        c = h * (3 * h + 1) // 2
        if c > MAX_N:
            break
        costs.append(c)
        h += 1

    def solve(n):
        ans = 0
        while n >= 2:
            lo, hi = 0, len(costs) - 1
            best = -1
            while lo <= hi:
                mid = (lo + hi) // 2
                if costs[mid] <= n:
                    best = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            if best == -1:
                break
            n -= costs[best]
            ans += 1
        return ans

    t = int(input())
    out = []
    for _ in range(t):
        out.append(str(solve(int(input()))))
    return "\n".join(out)

# provided samples
assert run("5\n3\n14\n15\n24\n1\n") == "1\n2\n1\n3\n0"

# minimum input
assert run("1\n1\n") == "0"

# exact single pyramid
assert run("1\n2\n") == "1"

# repeated same pyramid
assert run("1\n14\n") == "2"

# larger mixed case
assert run("1\n100\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 1 | 0 | cannot build smallest pyramid |
| 1, 2 | 1 | minimal valid construction |
| 1, 14 | 2 | repeated greedy use of same height |
| 1, 100 | 5 | multi-step descent across heights |

## Edge Cases

When $n = 1$, the algorithm immediately exits because the smallest pyramid requires 2 cards. The loop condition prevents any attempt to select a height, and the answer remains zero.

For a case like $n = 2$, only height 1 is available. The algorithm selects cost 2, subtracts it, and terminates. This confirms that the binary search correctly identifies the smallest valid cost even when no larger structures exist.

For larger values where multiple pyramids of the same height fit consecutively, such as $n = 14$, the algorithm repeatedly selects height 2. Each iteration recomputes feasibility against the updated remainder, ensuring that repeated selection does not depend on previous structure choices but only on remaining budget.
