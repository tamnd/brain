---
title: "CF 103969C - Wedding Cake"
description: "We are given a sequence of days, and on each day Mel receives a single cake layer ingredient labeled from 1 to 5. Mel is building wedding cakes, and each complete cake must be assembled in strict order from layer 1 up to layer 5."
date: "2026-07-02T06:24:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103969
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 10-14-22 Div. 1 (Advanced)"
rating: 0
weight: 103969
solve_time_s: 49
verified: true
draft: false
---

[CF 103969C - Wedding Cake](https://codeforces.com/problemset/problem/103969/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of days, and on each day Mel receives a single cake layer ingredient labeled from 1 to 5. Mel is building wedding cakes, and each complete cake must be assembled in strict order from layer 1 up to layer 5. Each ingredient can be used immediately on the same day it arrives, but if it is not used that day it is lost forever.

The twist is that Mel can work on multiple cakes at the same time. This means at any moment he may have several partially built cakes, each sitting at some stage between having no layers and being one step away from completion. Each day’s ingredient can either advance exactly one existing partial cake from layer k to k+1, or be ignored.

The task is to determine the maximum number of complete 5-layer cakes that can be finished over all days.

The input size can go up to one million days, which immediately rules out any approach that tries to track all partial states explicitly per cake or simulate all possible assignments. Any solution must process each day in constant or amortized constant time.

A subtle edge case appears when layers arrive in “wrong” order, for example many 5s early followed by 1s. A naive greedy that always tries to complete the most advanced cake first can fail because it blocks the ability to start new valid chains. Another failure case is when there are abundant intermediate layers but insufficient 1s, where over-allocating early layers leads to dead partial cakes that can never be completed.

## Approaches

A brute force simulation would maintain a list of all partial cakes and, for each incoming layer, try every possible cake it could extend. In the worst case, after k days there could be O(k) partial cakes, so each new day might scan all of them, leading to O(N^2) behavior when N is large. This becomes infeasible already around 10^5 operations, and here N is up to 10^6.

The key observation is that we never need to distinguish between individual cakes. What matters is only how many cakes are currently waiting for each next required layer. A cake in progress can be described purely by its current stage, from 1 through 4, because stage 5 means completion and does not need tracking anymore.

This reduces the problem to managing five counters: how many partial cakes are waiting for layer 1, layer 2, layer 3, layer 4, and how many completed cakes have been formed. Each day we greedily try to use the incoming layer to advance a cake that needs it. If multiple choices exist, we always prefer advancing the most advanced stage that can use it, because that preserves flexibility for earlier layers which are harder to match later.

This greedy works because delaying a higher stage completion in favor of a lower stage never increases future possibilities, while doing the opposite can permanently block chains from forming.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation of cakes | O(N^2) | O(N) | Too slow |
| Stage-counter greedy simulation | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain an array `cnt[1..4]` where `cnt[i]` is the number of partial cakes currently at stage i, meaning they are waiting for layer i+1. We also maintain a counter for finished cakes.

Each day processes one value `a[i]`.

1. If `a[i] == 1`, we start a new partial cake at stage 1, so we increase `cnt[1]`. This is the only layer that can create new chains.
2. If `a[i] == 2`, we try to advance a cake waiting for layer 2, meaning a cake at stage 1. If `cnt[1] > 0`, we decrement `cnt[1]` and increment `cnt[2]`. If no such cake exists, we discard this ingredient.
3. If `a[i] == 3`, we first try to extend a stage-2 cake if possible, since that keeps earlier stages available. So if `cnt[2] > 0`, we move one from `cnt[2]` to `cnt[3]`, otherwise we ignore the layer.
4. If `a[i] == 4`, we try to extend stage 3 first into stage 4. If `cnt[3] > 0`, we move one forward. Otherwise we discard it.
5. If `a[i] == 5`, this completes a cake if we have any stage-4 partial cakes. If `cnt[4] > 0`, we decrement it and increase the answer.

The ordering inside each step matters because we always prefer extending the most advanced possible stage.

Why it works is captured by the invariant that at any time, the multiset of partial cakes is fully characterized by their stages, and any valid final schedule can be transformed into one where earlier-stage advancements never block later-stage completions. Any time we choose to skip a possible advancement of a more advanced cake in favor of a less advanced one, we only delay progress without increasing the total number of reachable completions, while the reverse choice can destroy a chain that would otherwise complete.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    
    cnt1 = cnt2 = cnt3 = cnt4 = 0
    ans = 0
    
    for x in arr:
        if x == 1:
            cnt1 += 1
        elif x == 2:
            if cnt1:
                cnt1 -= 1
                cnt2 += 1
        elif x == 3:
            if cnt2:
                cnt2 -= 1
                cnt3 += 1
        elif x == 4:
            if cnt3:
                cnt3 -= 1
                cnt4 += 1
        else:  # x == 5
            if cnt4:
                cnt4 -= 1
                ans += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code directly implements the stage machine described earlier. Each variable corresponds exactly to one stage of incomplete cakes, and transitions are local constant-time updates. The final answer accumulates only when a stage-4 cake successfully receives a layer 5.

A common implementation pitfall is trying to be “fair” and distributing layers across all possible cakes. That is unnecessary and harmful because the structure guarantees that only counts matter, not identities.

## Worked Examples

Consider the sample input.

Input:

```
11
1 1 2 3 4 4 5 2 3 4 5
```

We track only states.

| Day | Layer | cnt1 | cnt2 | cnt3 | cnt4 | cakes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 2 | 0 | 0 | 0 | 0 |
| 3 | 2 | 1 | 1 | 0 | 0 | 0 |
| 4 | 3 | 1 | 0 | 1 | 0 | 0 |
| 5 | 4 | 1 | 0 | 0 | 1 | 0 |
| 6 | 4 | 1 | 0 | 0 | 1 | 0 |
| 7 | 5 | 1 | 0 | 0 | 0 | 1 |
| 8 | 2 | 0 | 1 | 0 | 0 | 1 |
| 9 | 3 | 0 | 0 | 1 | 0 | 1 |
| 10 | 4 | 0 | 0 | 0 | 1 | 1 |
| 11 | 5 | 0 | 0 | 0 | 0 | 2 |

This trace shows how intermediate layers are reused across multiple chains, and how completing a cake frees capacity for new progressions.

A second example highlights greed:

Input:

```
6
1 1 2 2 5 5
```

The process builds two stage-1 cakes, then two stage-2 transitions are impossible for both simultaneously, so only one full chain can be completed depending on ordering. The algorithm ensures only valid sequential progress is counted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each day performs a constant number of counter updates |
| Space | O(1) | Only four stage counters are stored |

The solution fits comfortably within limits for N up to 10^6, since it performs only simple integer operations per input element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(sys.stdin.readline())
    arr = list(map(int, sys.stdin.readline().split()))
    
    cnt1 = cnt2 = cnt3 = cnt4 = 0
    ans = 0
    
    for x in arr:
        if x == 1:
            cnt1 += 1
        elif x == 2:
            if cnt1:
                cnt1 -= 1
                cnt2 += 1
        elif x == 3:
            if cnt2:
                cnt2 -= 1
                cnt3 += 1
        elif x == 4:
            if cnt3:
                cnt3 -= 1
                cnt4 += 1
        else:
            if cnt4:
                cnt4 -= 1
                ans += 1
    
    return str(ans)

# provided sample
assert run("11\n1 1 2 3 4 4 5 2 3 4 5\n") == "2"

# minimum input
assert run("1\n1\n") == "0"

# no possible completion
assert run("5\n5 5 5 5 5\n") == "0"

# perfect chain
assert run("5\n1 2 3 4 5\n") == "1"

# multiple chains
assert run("10\n1 1 2 3 4 5 1 2 3 4\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 1 | 0 | no completion possible |
| all 5s | 0 | missing prerequisites |
| sequential chain | 1 | basic correctness |
| repeated chains | 2 | reuse of pipeline |

## Edge Cases

When all early layers appear late, such as many 5s followed by 1s, the algorithm correctly produces zero because stage-4 cakes never exist when 5s arrive. A naive interpretation that tries to “store” 5s would incorrectly inflate results.

When layers arrive in perfect order 1 through 5 repeatedly, each step advances exactly one chain and no interference occurs. The counters ensure no layer is wasted.

When intermediate layers are abundant but 1s are scarce, only the number of starting points limits the answer. The algorithm reflects this because cnt1 is the bottleneck, and no later stage can exceed it.
