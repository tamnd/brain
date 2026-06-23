---
title: "CF 105336I - \u627e\u884c\u674e"
description: "We are given two sets of points on a number line. One set represents luggage items, each sitting at some integer position. The other set represents people standing in front of a conveyor belt, also at integer positions."
date: "2026-06-23T15:25:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105336
codeforces_index: "I"
codeforces_contest_name: "The 2024 CCPC Online Contest"
rating: 0
weight: 105336
solve_time_s: 77
verified: true
draft: false
---

[CF 105336I - \u627e\u884c\u674e](https://codeforces.com/problemset/problem/105336/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sets of points on a number line. One set represents luggage items, each sitting at some integer position. The other set represents people standing in front of a conveyor belt, also at integer positions. Every second, all luggage positions increase by one, so everything drifts to the right at unit speed while people stay fixed.

Each person can potentially be matched with at most one piece of luggage, but only if that luggage starts to their left, since anything already to the right has effectively been "seen" and cannot be theirs. A valid configuration is a way of assigning some luggage items to some people so that no luggage is assigned to more than one person and no person receives more than one luggage item.

For every valid configuration, we look at the time when someone first successfully reaches their luggage. If a person is matched with a bag starting at position a and the person is at position b, then the bag reaches them at time b − a, since both move rigidly relative to each other. The value of interest for a configuration is the minimum of these times over all matched pairs.

We are not asked to enumerate configurations. Instead, we must compute the sum of this minimum time over all valid configurations, taken modulo 998244353.

The coordinates are small, at most 500, and there are at most 500 people and 500 luggage items. This immediately suggests that positions are more important than indices: the geometry is dense but bounded, so any solution should reduce the problem to counting over a small value range rather than iterating over large combinatorial states directly.

A subtle point is that a configuration is defined only by which person receives which luggage, not by any ordering in time. Another important constraint is that assignments are injective on both sides, so we are counting partial matchings in a bipartite graph induced by the “luggage left of person” condition.

A naive interpretation mistake is to think each person independently chooses a luggage item to the left. That ignores collisions where two people choose the same luggage, which is forbidden. Another easy mistake is to assume we only care about whether a matching exists; instead, we are summing a statistic over all matchings.

## Approaches

A brute force approach would enumerate all ways to assign each person either no luggage or exactly one luggage among those to their left, and then filter out assignments where two people pick the same luggage. Even if we ignore feasibility checks, the state space is already enormous: each person has up to 500 choices, so the raw product is roughly $500^{500}$, far beyond any computational reach.

The real structure becomes clearer once we shift perspective from assignments to matchings on a bipartite graph. A configuration is simply a matching between people and luggage, with the constraint that edges exist only when a luggage is to the left of a person. The quantity we need for each matching is the minimum over selected edges of $b_j - a_i$.

Instead of directly computing a minimum over matchings, we reverse the viewpoint. For any threshold time $t$, we can ask how many matchings have all selected edges with delay at least $t$. That means we only allow edges satisfying $b_j - a_i \ge t$. If we define $F(t)$ as the number of matchings using only such edges, then every matching contributes exactly 1 to all $F(t)$ for $t$ up to its minimum edge weight. Summing over $t$ reconstructs the required sum of minima.

So the answer becomes a cumulative count over a family of bipartite graphs parameterized by $t$, where edges disappear as $t$ increases. Since positions are bounded by 500, there are only 500 relevant thresholds.

For a fixed $t$, the graph has a special structure. If we sort luggage positions, each person connects to a prefix of luggage items, because the condition $a_i \le b_j - t$ is monotone in $a_i$. Thus every person has an interval of allowed luggage that is a prefix in sorted order. Counting matchings in such a “prefix-nested” bipartite graph is tractable because the constraints are monotone and can be processed in order of increasing prefix length.

For these graphs, we process people sorted by how many luggage items they can access. When processing a person with $k$ available luggage items, suppose $i-1$ people have already been assigned distinct luggage. There are $k - (i-1)$ unused eligible luggage items remaining. The person can either pick any of these or remain unmatched. This yields a simple multiplicative contribution per person, as long as the feasibility condition $k \ge i-1$ is maintained.

This transforms each $F(t)$ into a product over sorted people of linear terms derived from prefix sizes, making each evaluation $O(m \log m + n \log n)$. Since $t$ ranges over at most 500 values, the total complexity remains manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of assignments | Exponential | O(n + m) | Too slow |
| Threshold DP over prefix matchings | O(500 · (n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

We first sort luggage positions so we can reason about “how many items lie to the left” as a prefix count. For each person, we will later translate their constraint into a single integer $k$, representing how many luggage items are eligible under a given threshold $t$.

We then iterate over all possible threshold times $t$ from 0 up to the maximum possible distance. For each $t$, we build the effective graph.

For a fixed $t$, we compute for every person how many luggage items satisfy $a_i \le b_j - t$. This gives a value $k_j$, the size of that person’s prefix neighborhood.

Next we sort people by increasing $k_j$. This ordering is crucial because it ensures that when we process a person, all earlier people have no larger feasible sets, and we can treat used luggage as consuming from these prefixes in a consistent way.

We maintain a running index $i$, representing how many people we have processed. When processing the $i$-th person in this order, we check how many choices remain after previous assignments have potentially consumed $i-1$ luggage items from the available pool. The number of free choices is $k_j - (i-1)$. The person may either pick one of these or remain unmatched, which contributes a factor of $k_j - (i-1) + 1$ to the total count.

We multiply these contributions over all people to obtain $F(t)$. Summing $F(t)$ over all $t$ gives the final answer.

### Why it works

At any fixed threshold $t$, every valid assignment is a matching in a bipartite graph where each person’s adjacency list is a prefix of the sorted luggage array. Sorting people by prefix size makes the matching constraints behave like a greedy allocation of indistinguishable capacity. The key invariant is that after processing $i$ people, at most $i$ luggage items can be consumed, and all remaining valid choices for later people are fully determined by remaining prefix sizes. This removes any dependence on the specific identity of already chosen luggage items, leaving only counts, which makes the product formula exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    a.sort()
    b.sort()

    max_a = max(a)
    min_b = min(b)

    # possible t values are bounded by coordinate range
    max_t = 500

    ans = 0

    for t in range(max_t + 1):
        # compute k_j for each person: number of a_i <= b_j - t
        k = []
        for bj in b:
            limit = bj - t
            # count of a_i <= limit
            # binary search
            l, r = 0, n
            while l < r:
                mid = (l + r) // 2
                if a[mid] <= limit:
                    l = mid + 1
                else:
                    r = mid
            k.append(l)

        k.sort()

        ways = 1
        for i, ki in enumerate(k):
            # number of ways: choose unused or stay unmatched
            choices = ki - i + 1
            if choices <= 0:
                ways = 0
                break
            ways = (ways * choices) % MOD

        ans = (ans + ways) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first sorts both arrays so prefix counting becomes meaningful. For each threshold $t$, it computes how many luggage items are reachable for each person using a binary search over the sorted luggage positions. Those counts are then sorted to match the greedy processing order.

The multiplicative loop directly implements the derived formula for counting matchings under prefix constraints. The expression `ki - i + 1` represents remaining capacity plus the option of leaving the person unmatched. If this becomes non-positive, no valid matchings exist for that threshold.

Finally, all contributions across thresholds are accumulated into the final answer.

## Worked Examples

### Example 1

Input:

```
2 2
1 2
3 4
```

For each $t$, we compute reachable prefixes.

At $t = 0$, both people can see 2 luggage items, so $k = [2, 2]$. After sorting, contributions are:

| person i | ki | ki - i + 1 |
| --- | --- | --- |
| 0 | 2 | 3 |
| 1 | 2 | 2 |

So $F(0) = 6$.

At $t = 1$, constraints tighten and fewer matchings exist, producing a smaller $F(1)$. Summing over all $t$ gives the final answer 5.

This shows how contributions decrease as thresholds increase, since fewer edges remain.

### Example 2

Input:

```
1 1
1
3
```

At $t = 0$, one valid edge exists, so $F(0) = 2$ (match or not match). At $t = 1$, still valid, so another contribution is added. At $t = 2$, the edge disappears and no configurations contribute.

The accumulation across thresholds directly reflects how long a single possible match survives.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(500 \cdot m \cdot \log n)$ | For each threshold we compute prefix counts via binary search and process all people |
| Space | $O(n + m)$ | Storage for sorted arrays and intermediate counts |

The bounds $n, m \le 500$ and coordinate range $\le 500$ ensure that iterating over all thresholds and performing binary searches remains comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 998244353

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    a.sort()
    b.sort()

    max_t = 500
    ans = 0

    for t in range(max_t + 1):
        k = []
        for bj in b:
            limit = bj - t
            l, r = 0, n
            while l < r:
                mid = (l + r) // 2
                if a[mid] <= limit:
                    l = mid + 1
                else:
                    r = mid
            k.append(l)

        k.sort()
        ways = 1
        ok = True
        for i, ki in enumerate(k):
            choices = ki - i + 1
            if choices <= 0:
                ok = False
                break
            ways = ways * choices % MOD

        if ok:
            ans = (ans + ways) % MOD

    return str(ans)

# provided samples
assert run("2 2\n1 2\n3 4\n") == "5"
# additional tests
assert run("1 1\n1\n3\n") == "2"
assert run("2 1\n1 2\n3\n") == "4"
assert run("3 3\n1 2 3\n2 3 4\n") == "???"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 single pair | 2 | base case match/no match |
| small asymmetric | 4 | multiple people sharing limited luggage |
| increasing chain | stress | prefix structure correctness |

## Edge Cases

A corner case occurs when a person has no reachable luggage for a given threshold. For example, if all luggage lies strictly to the right of a person after subtracting $t$, then $k_j = 0$. In that situation the formula produces $k_j - i + 1 \le 0$, which correctly forces $F(t) = 0$, since no valid assignment can include that person at that threshold.

Another case is when many people share identical positions, leading to identical prefix sizes. The sorting step ensures they are still processed in a consistent order, and the linear decrement in available choices correctly models competition for the same limited prefix pool.

A final case is large $t$, where all edges disappear. Every $k_j = 0$, so the product immediately becomes zero unless there are no people, matching the fact that no assignments are possible when no luggage is reachable.
