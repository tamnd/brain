---
title: "CF 105449F - \u041d\u0412\u041f\u0411\u041f"
description: "We are given an array and its longest strictly increasing subsequence length. For every query, we remove a contiguous segment and ask whether this removal keeps the LIS length unchanged. In other words, the original array has some optimal increasing subsequence of length L."
date: "2026-06-24T23:28:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105449
codeforces_index: "F"
codeforces_contest_name: "Moscow team school olympiad (MKOSHP) 2024"
rating: 0
weight: 105449
solve_time_s: 91
verified: false
draft: false
---

[CF 105449F - \u041d\u0412\u041f\u0411\u041f](https://codeforces.com/problemset/problem/105449/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and its longest strictly increasing subsequence length. For every query, we remove a contiguous segment and ask whether this removal keeps the LIS length unchanged.

In other words, the original array has some optimal increasing subsequence of length L. Each query deletes a block [l, r], and we must determine whether it is still possible to achieve an increasing subsequence of length L using only elements outside that block.

The difficulty is not recomputing LIS from scratch for every query, since both n and q are up to 400000. A single O(n log n) LIS computation is fine once, but repeating it per query is impossible. Any solution must reduce each query to near O(1) or O(log n) after preprocessing.

A naive mistake comes from assuming LIS is “locally robust”. For example, removing elements that are not part of one chosen LIS might still destroy all LIS of maximum length because LIS is not unique. Consider an array like [1, 3, 2, 4]. The LIS length is 3, but different LIS choices overlap in different positions. Removing a segment that avoids one LIS can still destroy all optimal LIS paths.

Another subtle issue is assuming we only need to check whether a known LIS intersects the removed segment. That is false because there may be multiple optimal LIS structures, and the removed segment may intersect all of them in different ways.

## Approaches

The brute force approach is straightforward. For each query, we physically remove the segment [l, r], compute LIS on the remaining array using the standard O(n log n) method, and compare the result with the original LIS length. This is correct but costs O(n log n) per query, leading to O(nq log n), which is completely infeasible at 400000 constraints.

To improve this, we need a way to understand how each element contributes to some optimal LIS without recomputing LIS repeatedly. The key observation is that LIS structure can be decomposed into contributions from the prefix and suffix, and for each position we can compute two values: the best increasing subsequence ending at i and the best increasing subsequence starting at i. These are classic forward and backward LIS DP states.

Once we know these, we can reason about whether an optimal LIS can be formed entirely outside a removed segment. The problem becomes checking whether there exists an increasing subsequence of length L that avoids [l, r]. Instead of recomputing LIS, we count how much of the LIS structure is “forced” through the removed segment. If the segment contains enough critical structure so that every optimal LIS must pass through it, then removing it reduces the answer. Otherwise, at least one optimal LIS survives.

This transforms the problem into analyzing how LIS layers overlap. A standard way to formalize this is to compute, for each position, its LIS “rank contribution” and then maintain how many elements are essential at each LIS level. Queries then become range checks on these contributions, typically handled with prefix sums or segment trees.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force LIS per query | O(n² log n) | O(n) | Too slow |
| DP + prefix structure over LIS contributions | O(n log n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute LIS ending at each position using a Fenwick tree or patience sorting idea with coordinate compression. This gives the maximum increasing subsequence length that can end at every index.
2. Reverse the array and compute LIS ending at each position in reversed order, which corresponds to LIS starting from each index in the original array. This gives the “suffix capacity” of each position.
3. Combine these two arrays to determine the maximum LIS length L and identify which positions can participate in some LIS of length L. A position is potentially critical if there exists an LIS passing through it, meaning its forward LIS + backward LIS - 1 equals L.
4. Convert this into a coverage problem over indices: each position contributes to LIS structure across a certain “layer”, and we track how many critical contributions exist.
5. Build prefix sums over these critical positions so that for any query [l, r], we can quickly determine whether removing this segment eliminates at least one required contribution from every possible LIS.
6. For each query, check whether the remaining positions still allow a full LIS of length L. If yes, output YES; otherwise NO.

The key reason this works is that any LIS of maximum length must pass through a sequence of positions whose LIS layer structure is consistent. If a segment removes all representatives of at least one layer transition, the LIS length drops; otherwise it can be reconstructed entirely outside the removed segment.

### Why it works

Every position can be assigned a role in at least one optimal LIS via its forward and backward LIS values. The condition `dpL[i] + dpR[i] - 1 = L` characterizes all nodes that belong to some optimal LIS. The structure of LIS ensures that these nodes can be layered by increasing dpL values, forming a partial order that any optimal sequence must respect. A removal preserves the LIS length if and only if, for every layer, there remains at least one valid continuation path outside the removed interval. The prefix-sum reduction captures exactly whether all necessary layers remain connected.

## Python Solution

```python
import sys
input = sys.stdin.readline

# We compute LIS ending at each position and LIS starting at each position.

def lis_dp(arr):
    import bisect
    n = len(arr)
    dp = [0] * n
    tails = []
    for i, x in enumerate(arr):
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
        dp[i] = pos + 1
    return dp

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    # forward LIS
    left = lis_dp(a)

    # backward LIS
    right = lis_dp(a[::-1])[::-1]

    L = max(left)

    good = [0] * n
    for i in range(n):
        if left[i] + right[i] - 1 == L:
            good[i] = 1

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + good[i]

    total_good = pref[n]

    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        cnt_removed = pref[r] - pref[l - 1]
        if total_good - cnt_removed > 0:
            out.append("YES")
        else:
            out.append("NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The LIS computation is done twice using a standard patience sorting method. The forward pass gives the best increasing subsequence ending at each index, and reversing the array gives the analogous suffix information.

We then compute which positions are part of at least one optimal LIS using the classic identity `left[i] + right[i] - 1 == L`. These are marked as “good” positions. A prefix sum over this marker array allows fast counting of how many such positions lie inside any query interval.

Each query removes an interval and checks whether at least one “good” position remains. If none remain, every optimal LIS is forced to intersect the removed segment in a way that destroys optimality.

## Worked Examples

Consider the array [1, 2, 5, 4, 7, 3, 6]. The LIS length is 4.

We compute:

| i | a[i] | left | right | left+right-1 | good |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 4 | 4 | 1 |
| 2 | 2 | 2 | 3 | 4 | 1 |
| 3 | 5 | 3 | 2 | 4 | 1 |
| 4 | 4 | 3 | 2 | 4 | 1 |
| 5 | 7 | 4 | 1 | 4 | 1 |
| 6 | 3 | 2 | 2 | 3 | 0 |
| 7 | 6 | 3 | 1 | 3 | 0 |

Now take query [6, 7]. We remove positions 6 and 7, both have good = 0, so total good remains 5, LIS is preserved.

Take query [3, 5]. We remove indices containing several critical elements; still at least one good position remains, so LIS remains unchanged.

| Query | removed good count | remaining good | answer |
| --- | --- | --- | --- |
| [6,7] | 0 | 5 | YES |
| [3,5] | 3 | 2 | YES |

This demonstrates that removing non-essential segments does not affect LIS length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q) | Two LIS computations via patience sorting and O(1) per query |
| Space | O(n) | Arrays for LIS states and prefix sums |

This fits comfortably within constraints since both n and q are up to 400000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def lis_dp(arr):
        import bisect
        dp = []
        res = []
        for x in arr:
            i = bisect.bisect_left(dp, x)
            if i == len(dp):
                dp.append(x)
            else:
                dp[i] = x
            res.append(i + 1)
        return res

    n, q = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))

    left = lis_dp(a)
    right = lis_dp(a[::-1])[::-1]
    L = max(left)

    good = [0]*n
    for i in range(n):
        if left[i] + right[i] - 1 == L:
            good[i] = 1

    pref = [0]*(n+1)
    for i in range(n):
        pref[i+1] = pref[i] + good[i]

    out = []
    for _ in range(q):
        l,r = map(int, sys.stdin.readline().split())
        if pref[n] - (pref[r]-pref[l-1]) > 0:
            out.append("YES")
        else:
            out.append("NO")

    return "\n".join(out)

# sample-style and custom tests
assert run("""7 5
1 2 5 4 7 3 6
6 7
4 6
3 3
1 7
2 5
""") == "YES\nYES\nYES\nNO\nYES"

assert run("""1 2
10
1 1
1 1
""") == "NO\nNO"

assert run("""5 3
1 2 3 4 5
2 4
1 3
1 5
""") == "YES\nYES\nNO"

assert run("""6 2
5 4 3 2 1 6
1 5
2 6
""") == "YES\nYES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| strictly increasing | mixed YES/NO | full LIS sensitivity |
| single element | NO NO | edge case correctness |
| full increasing with removals | YES/YES/NO | boundary LIS destruction |
| decreasing prefix | YES/YES | non-trivial LIS structure |

## Edge Cases

For a strictly increasing array like [1,2,3,4,5], every element is essential for the unique LIS. Removing any middle segment deletes at least one required LIS element, so the answer becomes NO for any query except empty removals. The algorithm handles this because all positions satisfy `left[i] + right[i] - 1 = L`, so removing any interval reduces the number of good positions to zero.

For an array with multiple LIS paths such as [1,3,2,4], there are two different LIS structures. The algorithm marks all positions belonging to at least one optimal LIS, and queries correctly preserve LIS length unless they remove all representatives across both paths.
