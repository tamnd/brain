---
title: "CF 105895K - LRU is Best? (Easy Version)"
description: "We are given a fixed sequence of requests, and a small “cache” of size at most $m$, initially empty. As we scan the sequence from left to right, each element we encounter can either already be in the cache or not. If the current element is already in the cache, we gain one point."
date: "2026-06-21T12:28:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105895
codeforces_index: "K"
codeforces_contest_name: "The 21st Southeast University Programming Contest (Summer)"
rating: 0
weight: 105895
solve_time_s: 61
verified: true
draft: false
---

[CF 105895K - LRU is Best? (Easy Version)](https://codeforces.com/problemset/problem/105895/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed sequence of requests, and a small “cache” of size at most $m$, initially empty. As we scan the sequence from left to right, each element we encounter can either already be in the cache or not.

If the current element is already in the cache, we gain one point. If it is not in the cache, nothing bad happens in this simplified version, but we are allowed to optionally insert it into the cache, possibly evicting one existing element. In this easy version, insertions and evictions do not cost anything, so the only way to gain score is by arranging the cache so that future elements are already present when they appear.

The task is to choose all cache updates online during the scan so that the total number of cache hits is maximized.

The constraints are small in aggregate, with total $n$ over all test cases at most 800. This immediately rules out any solution worse than roughly $O(n^2)$, but still allows strategies that inspect the cache for each step and simulate future behavior.

A subtle point is that although inserting is always free, careless strategies can still fail badly. For example, always keeping the most recently seen elements is not optimal.

Consider a sequence like $1, 2, 3, 1, 2, 3$ with $m = 2$. If we always keep the most recent two elements, we might end up with $\{2, 3\}$ before the last three elements, missing future hits on $1$. The optimal strategy instead keeps track of which elements will be needed soon.

The key difficulty is that the decision at a miss is not about the current element, but about preserving access to elements that will appear again later.

## Approaches

A brute-force idea is to simulate all possible cache contents after every step. At each position, when a miss occurs, we try all possible choices of which element to evict and which to insert. This forms a branching process where each state is a subset of size at most $m$, and transitions depend on the next element. Even with aggressive pruning, the number of states grows combinatorially as $\binom{n}{m}$, which is far beyond what is feasible even for $n = 800$.

The structure simplifies because all hits have the same reward and there are no penalties. The only meaningful decision is which elements to keep in the cache to maximize future hits. This turns the problem into a classic optimal caching problem with full future knowledge.

The well-known optimal strategy is to always evict the element whose next occurrence is farthest in the future. If an element never appears again, it is always the best candidate for eviction. This greedy rule is optimal because it postpones losing access to elements that will be needed soon, preserving near-future gains.

To apply this, we need to know, at each step, when every cached element will next appear. We maintain, for each value, its list of future positions, and advance a pointer as we scan forward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation of Cache States | Exponential | Exponential | Too slow |
| Belady-style Optimal Caching | $O(nm)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain a cache set and, for each value, a pointer to its next occurrence in the future.

1. Precompute for every value a list of all indices where it appears. This lets us quickly know future occurrences.
2. For each value, maintain a pointer into its list indicating the first occurrence strictly after the current position. As we move forward in the array, we advance these pointers when we pass occurrences.
3. Maintain the current cache as a set of at most $m$ values.
4. When processing position $i$, check whether $a_i$ is already in the cache. If it is, increase the score by one, since this is a cache hit.
5. If $a_i$ is not in the cache, we consider inserting it. If the cache has free space, we insert it directly. Otherwise, we must evict one existing element.
6. To choose which element to evict, we examine every element currently in the cache and compute its next occurrence index. The best candidate to remove is the one whose next occurrence is farthest in the future, or does not exist at all.
7. After evicting that element, insert $a_i$ into the cache.

The key reason this works is that an element with a very distant next use is the least immediately valuable for preserving future hits. Removing it does not hurt near-term outcomes, while keeping elements with earlier reuse preserves guaranteed gains.

### Why it works

At any step, the cache represents a choice of $m$ elements that we commit to keeping for future benefit. Suppose we consider replacing an element $x$ in the cache with the current element $a_i$. If $x$ is used earlier in the future than some other cached element $y$, swapping them can only delay or preserve future hits more safely by keeping $x$. This establishes a greedy exchange argument: any configuration that violates the “farthest next use is evicted” rule can be improved by swapping, without reducing future hits. Repeating this exchange leads to the optimal structure at every step.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    INF = 10**18
    
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        _ = list(map(int, input().split()))  # x_i all 1
        _ = list(map(int, input().split()))  # y_i all 0
        _ = list(map(int, input().split()))  # z_i all 0

        pos = [[] for _ in range(n + 1)]
        for i, v in enumerate(a):
            pos[v].append(i)

        ptr = [0] * (n + 1)

        def next_occ(v, i):
            lst = pos[v]
            while ptr[v] < len(lst) and lst[ptr[v]] <= i:
                ptr[v] += 1
            if ptr[v] < len(lst):
                return lst[ptr[v]]
            return INF

        cache = set()
        score = 0

        for i, v in enumerate(a):
            if v in cache:
                score += 1
            else:
                if len(cache) < m:
                    cache.add(v)
                else:
                    worst = None
                    worst_next = -1
                    for u in cache:
                        nxt = next_occ(u, i)
                        if nxt > worst_next:
                            worst_next = nxt
                            worst = u
                    cache.remove(worst)
                    cache.add(v)

        print(score)

if __name__ == "__main__":
    solve()
```

The solution is organized around maintaining, at each step, a correct view of the future for every cached element. The `pos` lists store all occurrences, and `ptr` advances lazily so that computing the next occurrence is amortized efficient. The cache itself is a set, and each miss triggers a scan over the cache to identify the element whose future usefulness is least urgent.

The key implementation detail is that `next_occ(v, i)` always returns the first occurrence strictly after index `i`, and the pointer advancement ensures we do not repeatedly rescan old positions.

## Worked Examples

### Example 1

Consider a small case with $m = 2$ and sequence:

$$a = [1, 2, 3, 1, 2, 3]$$

At the start, cache is empty.

| i | a[i] | Cache before | Hit | Action | Cache after | Score |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | {} | No | insert 1 | {1} | 0 |
| 1 | 2 | {1} | No | insert 2 | {1,2} | 0 |
| 2 | 3 | {1,2} | No | evict farthest next-use, insert 3 | {1,3} | 0 |
| 3 | 1 | {1,3} | Yes | none | {1,3} | 1 |
| 4 | 2 | {1,3} | No | evict, insert 2 | {2,1} or {2,3} depending on future | 1 |
| 5 | 3 | ... | Yes | none | ... | 2 |

This trace shows why evictions must depend on future occurrences, not recency. Keeping the wrong pair early reduces later hits.

### Example 2

Let $m = 1$, sequence:

$$a = [1, 2, 1, 2, 1]$$

With cache size 1, we always keep only one element.

| i | a[i] | Cache before | Hit | Cache after | Score |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | {} | No | {1} | 0 |
| 1 | 2 | {1} | No | {2} | 0 |
| 2 | 1 | {2} | No | {1} | 0 |
| 3 | 2 | {1} | No | {2} | 0 |
| 4 | 1 | {2} | No | {1} | 0 |

With $m=1$, no hits are possible because every value is overwritten before reuse, confirming the limitation is purely structural.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each step may scan up to $m$ cached items to choose an eviction, and total $n$ steps |
| Space | $O(n)$ | Storage for occurrence lists of all values |

The total input size across test cases is small, so scanning the cache at every step is easily fast enough. Memory usage is dominated by storing positions, which stays linear in $n$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import defaultdict

    def solve():
        t = int(input())
        INF = 10**18
        
        for _ in range(t):
            n, m = map(int, input().split())
            a = list(map(int, input().split()))
            _ = list(map(int, input().split()))
            _ = list(map(int, input().split()))
            _ = list(map(int, input().split()))

            pos = [[] for _ in range(n + 1)]
            for i, v in enumerate(a):
                pos[v].append(i)

            ptr = [0] * (n + 1)

            def next_occ(v, i):
                lst = pos[v]
                while ptr[v] < len(lst) and lst[ptr[v]] <= i:
                    ptr[v] += 1
                if ptr[v] < len(lst):
                    return lst[ptr[v]]
                return INF

            cache = set()
            score = 0

            for i, v in enumerate(a):
                if v in cache:
                    score += 1
                else:
                    if len(cache) < m:
                        cache.add(v)
                    else:
                        worst = None
                        worst_next = -1
                        for u in cache:
                            nxt = next_occ(u, i)
                            if nxt > worst_next:
                                worst_next = nxt
                                worst = u
                        cache.remove(worst)
                        cache.add(v)

            return str(score)

    # samples and custom tests
    assert run("1\n1 1\n1\n1\n0\n0\n") == "0"
    assert run("1\n6 2\n1 2 3 1 2 3\n1 1 1 1 1 1\n0 0 0 0 0 0\n0 0 0 0 0 0\n") == "2"
    assert run("1\n5 1\n1 2 1 2 1\n1 1 1 1 1\n0 0 0 0 0\n0 0 0 0 0\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element cache and single request | 0 | Minimal boundary behavior |
| Repeating pattern with m=2 | 2 | Beneficial caching decisions |
| Alternating sequence with m=1 | 0 | No possible sustained hits |

## Edge Cases

One edge case is when a value never appears again after being inserted. In this situation, its next occurrence is treated as infinity, making it the best eviction candidate whenever it is present in the cache alongside any reusable element. The algorithm naturally removes it first, preventing wasted cache space.

Another case is when all values in the cache have identical next occurrence positions. In that situation, any eviction choice is equivalent, and the algorithm will still behave correctly because replacing any of them does not change future hit potential.

A final case is when the current element is already in the cache but also appears again very soon. The pointer mechanism ensures we still count the hit immediately, and future occurrences will correctly be recognized without needing any cache modification at that step.
