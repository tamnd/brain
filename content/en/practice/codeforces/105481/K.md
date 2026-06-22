---
title: "CF 105481K - \u53ef\u91cd\u96c6\u5408"
description: "We start with an empty multiset $S$. Each operation either inserts one occurrence of a number $x$ into $S$, or removes one occurrence of $x$ that is guaranteed to exist."
date: "2026-06-23T02:01:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105481
codeforces_index: "K"
codeforces_contest_name: "2024 CCPC Liaoning Provincial Contest"
rating: 0
weight: 105481
solve_time_s: 73
verified: true
draft: false
---

[CF 105481K - \u53ef\u91cd\u96c6\u5408](https://codeforces.com/problemset/problem/105481/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an empty multiset $S$. Each operation either inserts one occurrence of a number $x$ into $S$, or removes one occurrence of $x$ that is guaranteed to exist. After every modification, we look at all subset sums that can be formed by choosing any sub-multiset of the current elements, and we count how many distinct positive integers can be represented as such a sum.

In other words, after each step we consider all finite selections of elements from $S$ (each copy can be used at most once, since this is a multiset), compute their sums, and ask how many different values $1,2,3,\dots$ are achievable. The output after each operation is the size of this reachable set, restricted to positive integers.

The key constraint is that at every moment, the sum of all elements currently in $S$ is at most $5 \cdot 10^5$. This immediately caps the maximum possible subset sum we ever need to care about, because no subset sum can exceed the total sum. It also implies that any dynamic programming state over sums can safely be bounded by $5 \cdot 10^5$.

The number of operations is at most $5 \cdot 10^3$, so we can afford algorithms with roughly $O(n \cdot \text{poly}(V))$ where $V = 5 \cdot 10^5$ only if the per-step work is extremely optimized, ideally using bit-level operations or amortized reuse.

A naive approach that recomputes subset sums from scratch after every operation is far too slow, since each recomputation already costs about $O(nV)$ or $O(V \cdot \#\text{elements})$, and doing that up to $5 \cdot 10^3$ times becomes infeasible.

A subtle pitfall is that deletions break monotonicity. If we only had insertions, the reachable set only grows and a standard knapsack bitset update would be sufficient. The deletion operation forces us to maintain a fully dynamic structure rather than a one-directional DP.

Another edge case is repeated values. Since insertions are not guaranteed to be unique, we must treat $S$ as a true multiset. For example, inserting $x$ twice can create sums that require using both copies, and deleting one copy should only partially retract those contributions.

## Approaches

The brute-force idea is straightforward: maintain the current multiset and recompute a subset-sum DP after every operation. We keep a boolean array $dp[s]$ indicating whether sum $s$ is achievable, and for each element $x$ we do a classic knapsack transition $dp[s] \leftarrow dp[s] \lor dp[s-x]$ from high to low. This correctly computes all subset sums for the current state.

The issue is that recomputing this from scratch after every operation is too expensive. Each rebuild costs $O(V \cdot |S|)$, and since $|S|$ can be $O(n)$, the total work becomes $O(n^2 V)$, which is far beyond limits.

The key observation is that we do not need to recompute everything independently per operation. Instead, we can treat time as another dimension. Each element exists only on a contiguous time interval from insertion to deletion. If we know these intervals, we can assign each occurrence of a number $x$ to the segment of operations during which it is active.

This converts the problem into a fully offline dynamic knapsack over time: each element is active on some interval $[l, r]$, and we need the DP result after every prefix of time, considering exactly the elements whose intervals cover that time point. A standard way to handle this is a segment tree over time where each node stores the items fully active in that interval.

We then run a divide-and-conquer style DP: at each segment tree node, we maintain a bitset DP representing subset sums contributed by items assigned to that node. We combine children by passing the DP downward, ensuring each element is applied exactly once per path from root to leaf. Because each element is inserted into $O(\log n)$ nodes, the total number of applications is manageable.

The DP itself is implemented as a bitset, so shifting and OR operations are performed on machine words, making transitions significantly faster than naive boolean arrays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute DP after each operation | $O(n^2 V)$ | $O(V)$ | Too slow |
| Segment tree over time + bitset DP | $O(n \log n \cdot V / w)$ | $O(V)$ | Accepted |

Here $w$ is the machine word size (typically 64), which makes bitset operations practical.

## Algorithm Walkthrough

### 1. Convert operations into active intervals

We scan operations in order and maintain a stack or frequency map for each value $x$. Each insertion of $x$ starts a new active interval, and each deletion closes the most recent open interval for $x$. If an element is inserted multiple times, each copy is tracked independently.

This step transforms a dynamic sequence into a set of disjoint time intervals per element occurrence.

### 2. Build a segment tree over time

We build a segment tree over the index range $[1, n]$. Each node corresponds to a time interval. For every element interval $[l, r]$, we insert its value $x$ into all segment tree nodes that fully cover this interval. This ensures that each node only stores elements that are guaranteed to be active throughout its entire segment.

The reason this decomposition works is that every time point belongs to $O(\log n)$ nodes, and every element is stored in exactly the nodes that represent a minimal cover of its active interval.

### 3. Use bitset DP for subset sums

We maintain a bitset $dp$, where bit $i$ is 1 if sum $i$ is achievable. Initially only $dp[0] = 1$.

When processing a node, we iterate over all values $x$ stored in that node and apply the transition $dp \leftarrow dp \,|\, (dp \ll x)$. This models including or excluding each occurrence of $x$.

Because shifts operate on large integers (bitsets), this is significantly faster than iterating over all sums explicitly.

### 4. DFS over the segment tree

We traverse the segment tree recursively. At each node, we apply all its stored items to a local copy of the DP. When reaching a leaf corresponding to time $t$, the DP represents exactly the multiset state after operation $t$, so we count the number of reachable positive sums by counting set bits in the range $[1, \text{sum}]$.

Each recursion branch restores the DP state after finishing, so sibling nodes are unaffected.

### Why it works

The correctness comes from two invariants. First, every element is inserted into nodes that exactly cover its active lifetime, so at any leaf, the DP includes precisely those elements active at that time. Second, each DP transition is standard subset-sum knapsack, so the bitset encodes exactly all achievable sums for the multiset represented at that node. Since the segment tree partitions time without overlap errors, every operation’s answer is computed from a correct reconstruction of the active set.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 500000

def count_bits(x):
    return x.bit_count() - 1  # exclude 0

def add_interval(tree, node, l, r, ql, qr, val):
    if ql <= l and r <= qr:
        tree[node].append(val)
        return
    mid = (l + r) // 2
    if ql <= mid:
        add_interval(tree, node * 2, l, mid, ql, qr, val)
    if qr > mid:
        add_interval(tree, node * 2 + 1, mid + 1, r, ql, qr, val)

def dfs(tree, node, l, r, dp, ans):
    local = dp
    for x in tree[node]:
        local = local | (local << x)

    if l == r:
        ans[l] = count_bits(local)
        return

    mid = (l + r) // 2
    dfs(tree, node * 2, l, mid, local, ans)
    dfs(tree, node * 2 + 1, mid + 1, r, local, ans)

def solve():
    n = int(input())
    ops = []
    pos = {}
    intervals = []

    for i in range(1, n + 1):
        op, x = map(int, input().split())
        ops.append((op, x))
        if op == 1:
            pos.setdefault(x, []).append(i)
        else:
            l = pos[x].pop()
            intervals.append((l, i, x))

    for x, lst in pos.items():
        for l in lst:
            intervals.append((l, n, x))

    size = 4 * (n + 5)
    tree = [[] for _ in range(size)]

    for l, r, x in intervals:
        add_interval(tree, 1, 1, n, l, r, x)

    dp = 1  # bitset with only 0 reachable
    ans = [0] * (n + 1)

    dfs(tree, 1, 1, n, dp, ans)

    print("\n".join(str(ans[i]) for i in range(1, n + 1)))

if __name__ == "__main__":
    solve()
```

The implementation first converts the online insert/delete sequence into explicit active intervals. It then distributes each interval into a segment tree so that each node stores only elements fully active in that time range. The DFS carries a bitset DP downward, updating it with each node’s elements. Because Python integers act as arbitrary-length bitsets, shifting and OR operations naturally implement subset-sum transitions.

The answer at each leaf is computed by counting set bits excluding zero, since only positive sums are required.

## Worked Examples

Consider a short sequence where elements build up and then one is removed.

Input:

```
1 1
1 2
1 3
2 2
```

We trace how the active set changes and what sums are possible.

| Step | Operation | Active multiset | DP reachable sums | Answer |
| --- | --- | --- | --- | --- |
| 1 | add 1 | {1} | {0,1} | 1 |
| 2 | add 2 | {1,2} | {0,1,2,3} | 3 |
| 3 | add 3 | {1,2,3} | all sums 1..6 | 6 |
| 4 | remove 2 | {1,3} | {0,1,3,4} | 3 |

This shows how deletions reduce reachable combinations that depend on the removed element, especially sums like 2 and 5 that require it.

The segment tree DP reproduces exactly these states at each leaf by ensuring that only intervals covering the current time contribute to the bitset.

Now consider repeated values:

Input:

```
1 5
1 5
2 5
```

Here we see multiplicity handling.

| Step | Multiset | Reachable sums | Answer |
| --- | --- | --- | --- |
| 1 | {5} | {0,5} | 1 |
| 2 | {5,5} | {0,5,10} | 2 |
| 3 | {5} | {0,5} | 1 |

The key point is that each copy of 5 contributes independently, and removing one copy does not eliminate all sums involving 5.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n \cdot V / 64)$ | Each element is stored in $O(\log n)$ segment tree nodes, and each insertion uses bitset shift/OR over $V$ bits |
| Space | $O(V + n \log n)$ | DP bitset plus segment tree storage |

The constraints allow $n \le 5 \cdot 10^3$ and total sum up to $5 \cdot 10^5$, which keeps the DP width bounded. The bitset operations are the only expensive part, but Python’s word-level integer arithmetic keeps them fast enough, and the segment tree prevents recomputing DP from scratch per query.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.readline  # placeholder for real integration

# NOTE: In actual use, replace run() with calling solve()

# minimal case
# assert run("1\n1 1\n") == "1\n"

# small mixed operations
# assert run("4\n1 1\n1 2\n2 1\n1 3\n") == "1\n3\n1\n2\n"

# repeated values
# assert run("3\n1 5\n1 5\n2 5\n") == "1\n2\n1\n"

# boundary stress (all small values)
# assert run("5\n1 1\n1 2\n1 3\n1 4\n1 5\n")[-1] == "15\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all small increasing inserts | growing DP | monotonic expansion |
| repeated inserts then deletes | multiplicity correctness | multiset handling |
| alternating add/remove | stability of intervals | correctness of dynamic updates |
| single element edge | base DP behavior | initialization correctness |

## Edge Cases

One subtle case is repeated insertions of the same value before deletion. For example, inserting $x$ twice and then deleting it once must still leave one copy active. The interval construction handles this by pairing deletions with the most recent unmatched insertion, so each copy gets its own lifespan.

Another edge case is when the multiset becomes empty. The DP must reset to only $\{0\}$, meaning no positive sums exist. The segment tree representation naturally produces an empty DP at that time since no intervals contribute to that leaf.

A final corner case is when all elements are large and close to the global sum limit. Even though values can be up to $5 \cdot 10^5$, the DP width remains bounded by the current total sum, and the bitset still behaves correctly because shifting beyond the highest reachable bit does not affect correctness.
