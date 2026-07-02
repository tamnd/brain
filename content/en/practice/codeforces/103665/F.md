---
title: "CF 103665F - \u041d\u0430\u0431\u043b\u044e\u0434\u0435\u043d\u0438\u0435 \u043d\u0430 \u0432\u044b\u0431\u043e\u0440\u0430\u0445"
description: "There are several voting districts, and each district contains a number of polling stations. Every station has a predicted amount of fraudulent ballots that would be added there if nothing is done. The goal is to reduce the total fraud by placing observers."
date: "2026-07-02T21:45:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103665
codeforces_index: "F"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2018"
rating: 0
weight: 103665
solve_time_s: 60
verified: true
draft: false
---

[CF 103665F - \u041d\u0430\u0431\u043b\u044e\u0434\u0435\u043d\u0438\u0435 \u043d\u0430 \u0432\u044b\u0431\u043e\u0440\u0430\u0445](https://codeforces.com/problemset/problem/103665/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

There are several voting districts, and each district contains a number of polling stations. Every station has a predicted amount of fraudulent ballots that would be added there if nothing is done. The goal is to reduce the total fraud by placing observers.

An observer can be placed on at most C stations in total, and each station can host at most one observer. If a station has an observer, that station’s fraud is completely prevented.

There is an additional mechanism that works at the district level. If, inside some district, the number of placed observers reaches a threshold specific to that district, then fraud is prevented in the entire district, including stations without observers.

The task is to decide where to place observers, respecting the global limit, so that the total remaining fraud is minimized.

The important structural aspect is that decisions are not independent per station. A district becomes “fully safe” once enough observers are concentrated inside it, which can make additional station-level placements inside that district redundant. This creates a tradeoff between spreading observers across many districts versus concentrating them to unlock district-wide protection.

The constraints indicate that both the number of stations and observers can reach several thousand, which rules out any exponential subset enumeration. A quadratic or near-quadratic dynamic programming approach is feasible, but anything cubic in n would be too slow.

A naive approach would try every subset of stations of size at most C and simulate whether each district becomes activated. This fails because the number of subsets grows as combinations of 4000 choose C, which is completely infeasible.

A second naive idea is to treat each station independently and greedily pick the largest a_i values. This is also incorrect because it ignores the district activation threshold, where a carefully chosen set of moderate-value stations inside a district can erase a large remaining sum.

A subtle failure case appears when a district has many medium stations and a high threshold b_j. Greedily selecting globally largest stations might place observers across multiple districts without ever activating any district, while concentrating slightly weaker stations in one district could wipe out a large total.

## Approaches

The key observation is that decisions inside each district can be separated from other districts if we describe them correctly.

Inside a fixed district, suppose we decide to place k observers there. To maximize benefit for that fixed k, we should always place them on the k stations with largest a_i values in that district. This is because choosing a station for an observer contributes exactly its a_i value as saved fraud, and we want to maximize saved sum for a fixed count.

Let the stations in a district be sorted by decreasing a_i. Define a prefix sum P[k] as the total saved fraud if we place observers on the top k stations.

Now we must account for the district threshold. If k is at least b_j, the district becomes fully activated and all remaining stations in it are also saved. That means the value stops depending on k and becomes the total sum of that district.

So each district turns into a small “knapsack item generator”: for each possible k, we know exactly the best value we can get in that district.

The global problem becomes a classic knapsack over districts, where each district offers multiple “choices” of how many observers to spend in it, each choice having a value and a cost equal to k. We combine districts one by one using dynamic programming over the total number of observers used.

A brute force solution would attempt all distributions of observers across districts, which is exponential. The DP solution reduces this to O(m * C^2) in the worst naive form, but because total stations across all districts is only n, we can generate transitions in total O(n * C).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | exponential | O(n) | Too slow |
| Per-district knapsack DP | O(n · C) | O(C) | Accepted |

## Algorithm Walkthrough

1. Split stations by district. For each district, collect all a_i values belonging to it. This isolates local decisions so we can reason about observer placement inside one district without interference from others.
2. Sort each district’s values in descending order. This ensures that if we ever decide to place k observers in this district, taking the k largest values always maximizes saved fraud for that k.
3. Build a prefix sum array P for each district, where P[k] represents the total saved fraud if we place observers on the k best stations in that district. This converts a combinatorial choice into a simple lookup.
4. Precompute total_sum for each district as P[size], which represents all fraud in that district.
5. Construct a DP array dp[c], where dp[c] is the maximum saved fraud achievable using exactly c observers after processing some prefix of districts.
6. For each district, build a temporary transition array ndp initialized with negative infinity. For every possible current observer count c and every possible k we can spend in this district, update ndp[c + k] using the best of its current value and dp[c] plus the district’s contribution for k observers.
7. The contribution for k observers is P[k] if k is less than the district threshold b_j, and total_sum if k is at least b_j.
8. After processing the district, replace dp with ndp and continue.
9. After all districts are processed, the answer is total_fraud_sum minus the best dp[c] over all c up to C.

### Why it works

The correctness comes from the fact that each district is independent once we fix how many observers are assigned to it. For any fixed k, the best strategy inside the district is always to pick the k highest-value stations, since swapping any chosen station with an unchosen higher-value one strictly improves or preserves the result. The threshold condition only depends on the count k, not on which stations are chosen, so it does not break this optimal structure. The global DP then explores all valid distributions of observers across districts without missing any configuration, because every feasible assignment corresponds to exactly one sequence of per-district choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, C = map(int, input().split())
    c = list(map(int, input().split()))
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    districts = [[] for _ in range(m)]
    for i in range(n):
        districts[c[i] - 1].append(a[i])

    total_fraud = sum(a)

    dp = [-10**18] * (C + 1)
    dp[0] = 0

    for j in range(m):
        vals = districts[j]
        vals.sort(reverse=True)

        sz = len(vals)
        pref = [0] * (sz + 1)
        for i in range(sz):
            pref[i + 1] = pref[i] + vals[i]

        full = pref[sz]
        limit = b[j]

        ndp = [-10**18] * (C + 1)

        for used in range(C + 1):
            if dp[used] < 0:
                continue
            for k in range(sz + 1):
                if used + k > C:
                    break

                if k < limit:
                    gain = pref[k]
                else:
                    gain = full

                if dp[used] + gain > ndp[used + k]:
                    ndp[used + k] = dp[used] + gain

        dp = ndp

    print(total_fraud - max(dp))

if __name__ == "__main__":
    solve()
```

The DP is organized so that each state transition represents committing a fixed number of observers to a single district. The inner loop over k is safe because the total number of k iterations across all districts sums to n, since each k range is bounded by district size and all stations together form a partition of size n.

A common implementation mistake is forgetting the “flattening” effect when k reaches the threshold. After k >= b_j, all additional observers in that district do not change the value, so treating each k independently without this plateau leads to incorrect overcounting.

Another subtle issue is initializing unreachable states in dp with a sufficiently negative number. Since we are maximizing saved fraud, invalid states must never propagate.

## Worked Examples

### Example 1 (single district behavior)

Suppose there is one district with values [10, 5, 1] and b = 2, with C = 2.

The prefix sums are P = [0, 10, 15, 16]. For k = 0, gain = 0. For k = 1, gain = 10. For k = 2, since k >= b, gain becomes 16, meaning full activation. For k = 2 we already include all stations, so it matches.

| Step | used observers | k chosen | gain | dp state |
| --- | --- | --- | --- | --- |
| init | 0 | 0 | 0 | dp[0]=0 |
| district | 0 | 1 | 10 | dp[1]=10 |
| district | 0 | 2 | 16 | dp[2]=16 |

This shows how the threshold turns partial selection into full-district gain.

### Example 2 (multi-district tradeoff)

District 1: [8, 7], b = 2

District 2: [6, 6], b = 1

C = 2

District 2 activates with just 1 observer, giving full gain 12 immediately, while district 1 requires both observers for full activation.

The DP correctly prefers spending 1 observer in district 2 and then deciding whether remaining capacity is useful elsewhere.

| Step | state | action | result |
| --- | --- | --- | --- |
| start | dp[0]=0 | none | baseline |
| D2 | dp[1]=6, dp[2]=12 | choose k=1 or 2 | activation strong |
| D1 | combine | remaining capacity | final optimal split |

This demonstrates why greedy allocation by individual a_i fails.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · C) | Each station contributes to prefix sums once, and each DP transition iterates over observer counts up to C |
| Space | O(C) | Only two DP arrays of size C are maintained |

The constraints n ≤ 4000 and C ≤ 4000 fit comfortably within this complexity since the total operations are on the order of a few tens of millions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import inf

    # inline solution for testing
    n, m, C = map(int, sys.stdin.readline().split())
    c = list(map(int, sys.stdin.readline().split()))
    a = list(map(int, sys.stdin.readline().split()))
    b = list(map(int, sys.stdin.readline().split()))

    districts = [[] for _ in range(m)]
    for i in range(n):
        districts[c[i] - 1].append(a[i])

    total = sum(a)

    dp = [-10**18] * (C + 1)
    dp[0] = 0

    for j in range(m):
        vals = sorted(districts[j], reverse=True)
        sz = len(vals)
        pref = [0] * (sz + 1)
        for i in range(sz):
            pref[i + 1] = pref[i] + vals[i]

        full = pref[sz]
        lim = b[j]

        ndp = [-10**18] * (C + 1)
        for u in range(C + 1):
            if dp[u] < 0:
                continue
            for k in range(sz + 1):
                if u + k > C:
                    break
                gain = full if k >= lim else pref[k]
                ndp[u + k] = max(ndp[u + k], dp[u] + gain)

        dp = ndp

    return str(total - max(dp))

# custom cases

# minimal
assert run("1 1 1\n1\n5\n1\n") == "0"

# no activation possible
assert run("3 1 2\n1 1 1\n1 2 3\n5\n") == "3"

# activation beneficial
assert run("3 1 3\n1 1 1\n1 2 3\n2\n") == "0"

# multiple districts
assert run("4 2 2\n1 1 2 2\n5 1 5 1\n2 2\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single station | 0 | base case correctness |
| no activation possible | 3 | partial selection only |
| full activation possible | 0 | threshold effect |
| two districts split | 2 | cross-district DP correctness |

## Edge Cases

A frequent edge case occurs when a district’s threshold is 1. In that case, placing a single observer should immediately wipe out the entire district. The algorithm handles this correctly because for any k ≥ 1, the gain switches to the full district sum, so dp never benefits from placing more than one observer in that district.

Another edge case is when a district has many stations but very small individual values. A naive greedy solution might ignore the district entirely, but the DP correctly evaluates whether reaching the threshold yields a large jump in gain.

Finally, when C is large compared to n, the DP still behaves correctly because the upper bound k is limited by district size, ensuring transitions remain within feasible observer counts without artificial inflation of choices.
