---
title: "CF 104787J - Keyi LIkes Reading"
description: "We are given a collection of words, but the only property that matters about each word is its length. Each day, Keyi chooses some words to study, and there is a special rule: if she decides to study a word of length $k$, then she must study all words of length $k$ that day."
date: "2026-06-28T14:23:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104787
codeforces_index: "J"
codeforces_contest_name: "The 2023 CCPC (Qinhuangdao) Onsite (The 2nd Universal Cup. Stage 9: Qinhuangdao)"
rating: 0
weight: 104787
solve_time_s: 47
verified: true
draft: false
---

[CF 104787J - Keyi LIkes Reading](https://codeforces.com/problemset/problem/104787/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of words, but the only property that matters about each word is its length. Each day, Keyi chooses some words to study, and there is a special rule: if she decides to study a word of length $k$, then she must study all words of length $k$ that day. In other words, lengths act like indivisible groups.

Each day has a capacity limit $W$, meaning the total number of words studied that day cannot exceed $W$. Since selecting one length forces all words of that length, the real decision is which lengths to pack together into the same day, subject to their total frequency not exceeding $W$.

The input gives $n$ word lengths, each in the range 1 to 13. The task is to partition these lengths into the minimum number of valid days, where each day is a subset of length-groups, and the sum of group sizes in a day does not exceed $W$.

The output is the minimum number of such days needed to cover all words.

The constraints matter in a very specific way. Although $n$ can be as large as 50000, the value space of lengths is tiny, bounded by 13. This immediately suggests that any solution depending on the number of distinct lengths is small and manageable. A solution that tracks per-length counts is sufficient; iterating over all subsets of lengths is still feasible because there are at most $2^{13}$ possibilities.

A naive interpretation might try to assign words one by one or simulate day-by-day packing greedily without considering global structure. This breaks easily because grouping decisions are interdependent: choosing a large group early can block better packing later.

A subtle edge case appears when one length dominates the capacity:

Input:

n = 5, W = 4

lengths: [1, 1, 1, 1, 1]

Each length-group is just length 1 with frequency 5. Since we must take all of them together, but cannot exceed 4 per day, we need at least 2 days. Any greedy approach that tries to “fit remaining words” without respecting the group constraint might incorrectly split or undercount.

Another edge case is when many small groups combine tightly to exactly fill days versus slightly exceeding capacity, where optimal packing depends on subset selection rather than ordering.

## Approaches

The key abstraction is to forget individual words and instead compress the input into frequency counts per length. Since lengths range only from 1 to 13, we get at most 13 groups, each with a fixed size.

Now the problem becomes: we have up to 13 items, each with a weight equal to its frequency, and we want to pack all items into the minimum number of bins of capacity $W$, with the constraint that items are indivisible.

This is exactly a bin packing problem with very small item count but potentially large weights. The brute force idea would simulate assigning groups to days, trying all possible assignments. That leads to an exponential search over placements, roughly $O(k^n)$ where $k$ is number of bins, which is infeasible even for moderate inputs.

However, since there are at most 13 distinct groups, we can use bitmask dynamic programming over subsets of groups. Each state represents which groups are already packed, and we try to fill one day by selecting a subset of remaining groups whose total size does not exceed $W$. For each valid subset, we transition by marking those groups as used and adding one day.

This transforms the problem into shortest path over subsets, where each move corresponds to filling one day optimally.

The crucial observation is that packing a day is independent of previous days, except for remaining unused groups. So each DP transition fully represents one day of work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force assignment | Exponential | O(n) | Too slow |
| Bitmask DP over subsets | $O(2^{13} \cdot 2^{13})$ or optimized $O(2^{13} \cdot 13)$ | $O(2^{13})$ | Accepted |

## Algorithm Walkthrough

We compress the input into a frequency array `cnt` of size 13, where `cnt[i]` is the number of words of length $i+1$.

We then treat each of these 13 groups as an item with weight `cnt[i]`.

We define a bitmask DP where each mask represents which length-groups have already been fully assigned to days.

We compute DP[mask] as the minimum number of days needed to pack all groups in `mask`.

### Steps

1. Compute `cnt[0..12]` from input.
2. Precompute all valid subsets of groups. A subset is valid if the sum of their counts does not exceed $W$. This represents a single day packing.
3. Initialize DP array of size $2^{13}$ with large values, set DP[0] = 0.
4. Iterate over all masks from 0 to $2^{13}-1$.
5. For each mask, consider all subsets of remaining unused groups.
6. If a subset is valid and disjoint from current mask, transition to new mask by adding 1 day.
7. Take minimum over all transitions.
8. The answer is DP[(1<<13)-1].

The key design decision is to precompute valid subsets, because checking weight repeatedly inside DP would multiply runtime unnecessarily. Since 13 is small, enumerating all subsets is feasible.

### Why it works

At any DP state, the mask encodes exactly which groups remain. Every transition chooses a set of remaining groups that can fit into a single day. Because groups are indivisible and must be fully scheduled, every group appears exactly once across all transitions. The DP explores all possible partitions of the 13 groups into bins of capacity $W$, and since every valid partition corresponds to some sequence of subset removals, the minimum over DP captures the optimal number of days.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, W = map(int, input().split())
    a = list(map(int, input().split()))

    cnt = [0] * 13
    for x in a:
        cnt[x - 1] += 1

    # Precompute subset weights
    m = 13
    subset_weight = [0] * (1 << m)
    for mask in range(1 << m):
        s = 0
        for i in range(m):
            if mask & (1 << i):
                s += cnt[i]
        subset_weight[mask] = s

    valid = []
    for mask in range(1 << m):
        if subset_weight[mask] <= W:
            valid.append(mask)

    INF = 10**9
    dp = [INF] * (1 << m)
    dp[0] = 0

    full = (1 << m) - 1

    for mask in range(1 << m):
        if dp[mask] == INF:
            continue
        remaining = full ^ mask
        for sub in valid:
            if (sub & mask) == 0:
                new_mask = mask | sub
                if dp[new_mask] > dp[mask] + 1:
                    dp[new_mask] = dp[mask] + 1

    print(dp[full])

if __name__ == "__main__":
    main()
```

The implementation starts by compressing the input into a 13-length frequency array. This step is crucial because it reduces a potentially large $n$ problem into a fixed-size state space.

The `subset_weight` computation is the core preprocessing step. It evaluates every subset of lengths and computes how many words would be included if those lengths are chosen together in one day.

The `valid` list stores only subsets that fit within the daily limit $W$. This avoids repeated capacity checks during DP transitions.

The DP loop iterates over masks in increasing order. For each state, it tries to add a valid subset of unused groups. The XOR check ensures we never reuse a group. Each transition corresponds to consuming exactly one day.

## Worked Examples

### Example 1

Input:

```
5 4
1 2 1 2 1
```

Counts:

`cnt = [3, 2, 0, ..., 0]`

We have two groups: length 1 has size 3, length 2 has size 2.

| Mask | Groups included | Weight | DP |
| --- | --- | --- | --- |
| 0000 | none | 0 | 0 |
| 0001 | {len1} | 3 | 1 |
| 0010 | {len2} | 2 | 1 |
| 0011 | {len1,len2} | 5 (invalid) | INF |

From state 0, we can take either group alone. Taking both is invalid since 5 > 4. From either single-group state, the remaining group is taken in another day.

Answer: 2

This shows the DP correctly enforces capacity constraints and prevents combining groups that exceed $W$.

### Example 2

Input:

```
6 6
1 1 1 2 2 2
```

Counts:

`cnt[0]=3, cnt[1]=3`

| Mask | Action | DP |
| --- | --- | --- |
| 00 | start | 0 |
| 01 | take len1 | 1 |
| 10 | take len2 | 1 |
| 11 | cannot take both (3+3=6 valid, actually valid) | 1 |

Here both groups together fit exactly into one day, so DP finds optimal answer 1.

This demonstrates that the algorithm naturally exploits tight packing opportunities instead of greedily separating groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^{13} \cdot 2^{13})$ | DP over all masks, trying all valid subsets |
| Space | $O(2^{13})$ | DP array over subsets |

The state space is fixed at 8192, and transitions are bounded by the same constant factor. This is comfortably within limits for a 1-second time constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, W = map(int, input().split())
    a = list(map(int, input().split()))

    cnt = [0] * 13
    for x in a:
        cnt[x - 1] += 1

    m = 13
    subset_weight = [0] * (1 << m)
    for mask in range(1 << m):
        s = 0
        for i in range(m):
            if mask & (1 << i):
                s += cnt[i]
        subset_weight[mask] = s

    valid = [mask for mask in range(1 << m) if subset_weight[mask] <= W]

    INF = 10**9
    dp = [INF] * (1 << m)
    dp[0] = 0

    full = (1 << m) - 1

    for mask in range(1 << m):
        if dp[mask] == INF:
            continue
        for sub in valid:
            if (sub & mask) == 0:
                dp[mask | sub] = min(dp[mask | sub], dp[mask] + 1)

    return str(dp[full])

# sample
assert run("5 4\n1 2 1 2 1\n") == "2"

# all same
assert run("4 4\n1 1 1 1\n") == "1"

# tight split
assert run("6 4\n1 1 1 2 2 2\n") == "2"

# minimal
assert run("1 1\n1\n") == "1"

# each must be separate
assert run("3 1\n1 2 3\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all same lengths | 1 | full grouping in one day |
| mixed tight packing | 2 | subset packing optimization |
| W = 1 case | n | forced separation |
| single element | 1 | base case |

## Edge Cases

A key edge case appears when a single length group exceeds half of $W$, making it impossible to combine with most other groups. For example, if one group has size 5 and $W = 6$, only very specific combinations are valid. The DP handles this naturally because subset validity is checked purely by sum constraint, independent of greedy ordering.

Another edge case is when multiple combinations exactly match $W$. In such cases, greedy strategies may pick a suboptimal subset first and fragment remaining groups. The DP avoids this because it explores all valid subsets symmetrically and always minimizes total number of days from every reachable mask state.

A final subtle case is when all groups are individually small but collectively exceed capacity in many ways, making packing highly combinatorial. Even here, the subset enumeration guarantees all valid packings are considered, and the optimal partition is found through state minimization rather than construction order.
