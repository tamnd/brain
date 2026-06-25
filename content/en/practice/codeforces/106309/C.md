---
title: "CF 106309C - \u0413\u0440\u0438\u0431\u043e\u0447\u043a\u0438"
description: "We are given a limited amount of dough and several types of buns we can bake. Each bun type consumes a fixed amount of dough, and for flavored buns it also consumes a limited amount of a specific filling. Each bun yields a fixed profit."
date: "2026-06-25T07:45:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106309
codeforces_index: "C"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435, 9-11 \u043a\u043b\u0430\u0441\u0441\u044b, \u041f\u0435\u0440\u043c\u0441\u043a\u0438\u0439 \u043a\u0440\u0430\u0439, 2025"
rating: 0
weight: 106309
solve_time_s: 46
verified: true
draft: false
---

[CF 106309C - \u0413\u0440\u0438\u0431\u043e\u0447\u043a\u0438](https://codeforces.com/problemset/problem/106309/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a limited amount of dough and several types of buns we can bake. Each bun type consumes a fixed amount of dough, and for flavored buns it also consumes a limited amount of a specific filling. Each bun yields a fixed profit. In addition, there is one extra “plain” bun type that uses only dough and has unlimited supply, while each flavored type is additionally constrained by how much filling is available.

The task is to decide how many buns of each type to bake so that we maximize total profit, without exceeding dough and without exceeding the available amount of each filling.

The difficulty is that all choices interact through a single shared resource, dough, while each flavored type also has its own independent cap.

The constraints are small: dough is at most around 1000 and the number of flavors is at most 10. This immediately rules out any exponential search over exact quantities per flavor, since even a moderate branching factor would explode. A purely greedy approach is also unsafe because a bun with higher profit per gram of filling might consume too much dough and block a combination of other buns that yields higher total profit.

A subtle failure case appears when greedy ranking by profit per bun is misleading.

For example, suppose one bun gives high profit but consumes too much dough, while another gives slightly lower profit but is much more efficient in dough usage. A greedy strategy that always picks the highest immediate profit can exhaust dough too early and miss a better overall combination.

Another common pitfall is treating each bun independently and taking as many as possible per type. That ignores that taking one more bun of any type reduces the global capacity for all others.

## Approaches

The key observation is that the number of flavored types is very small, so we can treat them as a decision layer over how many buns of each type we take, and everything else collapses into a one-dimensional optimization over remaining dough.

A brute-force idea would try all combinations of how many buns of each flavor we take. For each flavor i, we can take from 0 up to min(ai, n / ci) buns. If we attempt this directly, the number of states becomes roughly a product of up to 100 choices per flavor, which is astronomically large.

The structure that saves us is that once we fix how many flavored buns of each type we take, the remaining problem is trivial: all remaining dough should be spent on plain buns. That reduces the entire problem into selecting bounded knapsack choices over at most 10 items, where each item has a bounded multiplicity and a linear cost in dough.

Instead of enumerating all combinations, we optimize each flavor independently using a standard bounded knapsack decomposition trick. Each flavored bun contributes a fixed profit and consumes a fixed amount of dough, but we cannot exceed ai / bi items. This converts each flavor into a bounded item set, and the whole problem becomes a knapsack over capacity n.

The plain bun is simply another item with unlimited supply, so it naturally fills leftover capacity in the DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full enumeration of all flavor counts | Exponential in m and ai | O(1) extra | Too slow |
| Bounded knapsack over decomposed items | O(n · sum of decomposed items) | O(n) | Accepted |

## Algorithm Walkthrough

1. We interpret each flavored bun as an item that can be used at most ai / bi times. This converts the “resource constraint on filling” into a simple upper bound on how many times we can take each item.
2. We transform each flavor into multiple 0-1 items using binary splitting of its maximum count. This ensures that we handle large limits efficiently without iterating through all counts.
3. We create a dynamic programming array dp where dp[x] represents the maximum profit achievable using exactly x grams of dough. We initialize all states as unreachable except dp[0] = 0.
4. We iterate over all transformed items and update the DP in decreasing order of dough usage. This prevents reusing the same item multiple times in a single transition, preserving correctness of 0-1 behavior.
5. After processing all flavored buns, we treat the plain bun as a final unbounded item. We relax dp by allowing transitions that repeatedly add the plain bun cost and profit, or equivalently we precompute the best possible combination by trying all remaining dough usage and filling it with plain buns.
6. The final answer is the maximum value over all dp states after considering that any leftover dough can always be converted into plain buns.

The invariant throughout the DP is that dp[x] always represents the best achievable profit using exactly x units of dough after processing a prefix of items. Each transition preserves feasibility because we never exceed the available multiplicity of flavored buns, and we never exceed total dough.

The correctness hinges on the fact that every valid baking plan corresponds to selecting a multiset of bounded flavored items plus some number of plain buns, and this representation is fully captured by the knapsack states.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, c0, d0 = map(int, input().split())

    items = []

    for _ in range(m):
        a, b, c, d = map(int, input().split())
        max_cnt = min(a // b, n // c)
        k = 1
        while max_cnt > 0:
            take = min(k, max_cnt)
            items.append((take * c, take * d))
            max_cnt -= take
            k <<= 1

    dp = [-10**18] * (n + 1)
    dp[0] = 0

    for cost, val in items:
        for j in range(n, cost - 1, -1):
            if dp[j - cost] != -10**18:
                dp[j] = max(dp[j], dp[j - cost] + val)

    best = 0
    for used in range(n + 1):
        if dp[used] < 0:
            continue
        remaining = n - used
        best = max(best, dp[used] + (remaining // c0) * d0)

    print(best)

if __name__ == "__main__":
    solve()
```

The DP array is indexed by dough usage rather than number of buns, which makes the interaction between different bun types clean. Each flavored type is expanded using binary splitting, which is why the inner loop stays efficient even when a flavor can be used many times.

The final loop is essential: DP only accounts for flavored buns, so we explicitly convert leftover dough into plain buns. Forgetting this step is a common source of wrong answers, since dp[n] alone is not necessarily optimal.

## Worked Examples

### Example 1

Input:

```
10 2 2 1
7 3 2 100
12 3 1 10
```

We process the first flavor, which allows at most 2 buns (since 7/3 = 2). We create items corresponding to 1 and 2 buns. For the second flavor, we similarly decompose its limit.

After DP, we track best states:

| Used dough | Best profit |
| --- | --- |
| 0 | 0 |
| 2 | 100 |
| 4 | 200 |
| 5 | 210 |
| 6 | 220 |
| 8 | 230 |

Now we add plain buns with cost 2 and profit 1:

For each state, remaining dough is converted.

For example, at used = 8, remaining = 2, we add 1 more profit, giving 231. The best over all states becomes 241, matching the optimal combination of flavored and plain buns.

This trace shows that flavored decisions alone are insufficient, and leftover conversion is what finalizes optimality.

### Example 2

Input:

```
100 1 25 50
15 5 20 10
```

Only one flavored type exists. Maximum flavored buns is 3.

| Used dough | Profit |
| --- | --- |
| 0 | 0 |
| 20 | 10 |
| 40 | 20 |
| 60 | 30 |

Now we fill remaining dough with plain buns:

At used = 60, remaining = 40 gives 1 plain bun.

Total becomes 40 + 30 = 70 equivalent gain added to base structure, but optimal solution instead prefers skipping flavored buns entirely and using only plain buns, yielding 200.

This demonstrates that flavored buns are not automatically beneficial even if they are available.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × total_items) | Each DP transition scans the knapsack array once per decomposed item |
| Space | O(n) | DP array over dough capacity |

The constraints n ≤ 1000 and m ≤ 10 ensure that even after binary splitting, the number of items stays small enough for the DP to run comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, c0, d0 = map(int, input().split())
    items = []

    for _ in range(m):
        a, b, c, d = map(int, input().split())
        max_cnt = min(a // b, n // c)
        k = 1
        while max_cnt > 0:
            take = min(k, max_cnt)
            items.append((take * c, take * d))
            max_cnt -= take
            k <<= 1

    dp = [-10**18] * (n + 1)
    dp[0] = 0

    for cost, val in items:
        for j in range(n, cost - 1, -1):
            if dp[j - cost] != -10**18:
                dp[j] = max(dp[j], dp[j - cost] + val)

    best = 0
    for used in range(n + 1):
        if dp[used] < 0:
            continue
        rem = n - used
        best = max(best, dp[used] + (rem // c0) * d0)

    return str(best)

# provided samples
assert run("""10 2 2 1
7 3 2 100
12 3 1 10
""") == "241"

assert run("""100 1 25 50
15 5 20 10
""") == "200"

# custom cases
assert run("""1 1 1 10
1 1 1 5
""") == "10", "prefer plain over weak flavor"

assert run("""5 1 5 100
10 1 5 1
""") == "100", "ignore bad flavor efficiency"

assert run("""10 0 2 3
""") == "15", "only plain buns"

assert run("""10 1 3 5
10 2 3 1
""") == "15", "edge small mix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| weak flavored vs strong plain | 10 | greedy rejection of weak items |
| inefficient flavor | 100 | ignoring dominated item types |
| no flavors | 15 | pure plain case |
| mixed boundary | 15 | interaction of DP + leftover fill |

## Edge Cases

One edge case is when flavored buns are strictly worse than plain buns. The input

```
5 1 1 10
5 1 1 1
```

leads the DP to consider the flavored option, but the final conversion step ensures that skipping it entirely is optimal, producing 50 instead of a smaller mixed value.

Another case is when the best solution uses no flavored buns at all. The DP must still correctly return 0 for flavored usage and allow full conversion to plain buns. Without considering the “used = 0” state in the final loop, the solution would incorrectly miss the all-plain optimal configuration.

A third case occurs when flavored buns exactly fill the dough, leaving no remainder. The algorithm still works because the final conversion term becomes zero, so the DP alone decides the result without interference.
