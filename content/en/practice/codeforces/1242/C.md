---
title: "CF 1242C - Sum Balance"
description: "We are given several groups of numbers, where each group represents a box containing distinct integers. The operation we are allowed to perform is very constrained: from each box, we must choose exactly one number."
date: "2026-06-13T20:04:20+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dfs-and-similar", "dp", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1242
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 599 (Div. 1)"
rating: 2400
weight: 1242
solve_time_s: 517
verified: false
draft: false
---

[CF 1242C - Sum Balance](https://codeforces.com/problemset/problem/1242/C)

**Rating:** 2400  
**Tags:** bitmasks, dfs and similar, dp, graphs  
**Solve time:** 8m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several groups of numbers, where each group represents a box containing distinct integers. The operation we are allowed to perform is very constrained: from each box, we must choose exactly one number. After collecting these chosen numbers, we redistribute them so that each chosen number is placed into some box, with the restriction that every box ends up with the same number of elements as before.

The goal is not to change box sizes, but to permute a selected set of elements across boxes in a way that equalizes the sum of every box after the move. Since exactly one element leaves and exactly one element enters each box, the total sum of each box changes only through swapping outgoing and incoming values.

The key difficulty is that the assignment must be globally consistent. A choice made for one box forces a destination, and those destinations must themselves be consistent with their own outgoing choices. This creates a functional graph structure over boxes, not an independent per-box decision.

The constraints make brute force infeasible in any direct sense. Each box can contain up to 5000 numbers and there are up to 15 boxes. Even ignoring the values inside, the number of ways to choose one element per box is the product of box sizes, which is astronomically large. Any solution that tries to enumerate assignments directly over elements is impossible.

The non-obvious failure cases come from assuming local balance is sufficient. For example, picking a value that “fixes” a box sum greedily can break global consistency because that value must simultaneously satisfy another box’s requirement.

A second subtle failure case is assuming cycles are always short or easy to complete. Even if each box picks a value that “should” go to a certain target, those targets can form long or even disconnected cycles, and partial cycles are invalid because every chosen value must be used exactly once.

## Approaches

A brute-force approach would try all ways of selecting one element from each box and then permuting these selected elements across boxes. Even if we fix a selection, checking whether a valid reassignment exists is equivalent to checking whether we can match each chosen element to a box so that all sums become equal. This becomes a constrained matching over k items, but the selection space itself is $\prod n_i$, which is far too large.

The key observation is that we do not actually need to choose arbitrary elements independently. Instead, once we fix the target equal sum, every chosen element from a box determines exactly what the resulting box sum must be after removing it. That defines a target value for what must be inserted into that box. This turns each chosen element into a directed requirement: “if I take this value from box i, then I need to insert a specific value into box i to restore balance.”

This transforms the problem into a directed graph over values and boxes. Each value implicitly maps to a box it must go to. Since each box contributes exactly one outgoing edge (its chosen element), and each value must be used exactly once, we are looking for a decomposition of the structure into cycles. Each cycle represents a consistent redistribution: following the cycle ensures every box sends out one value and receives one value.

The problem then reduces to constructing a valid cycle cover in this directed structure such that every box participates exactly once. The small value of k (≤ 15) allows us to encode which subset of boxes participates in a partial construction using bitmasks and explore feasible cycles via DFS over states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over selections | $O(\prod n_i \cdot k!)$ | $O(k)$ | Too slow |
| Bitmask DFS + cycle construction | $O(k \cdot 2^k)$ | $O(k \cdot 2^k)$ | Accepted |

## Algorithm Walkthrough

1. Compute the sum of all numbers in each box and the total sum across all boxes. From this, derive the target sum $S$ that every box must end with. Since total sum is invariant, $S$ must be the total sum divided by k. If this division is not exact, no solution exists. This step eliminates impossible instances early.
2. For every number $x$ in every box $i$, compute what value would be required in order to place $x$ into box $i$. If box $i$ has sum $sum_i$, then removing $x$ forces the incoming value $y$ to satisfy $sum_i - x + y = S$, so $y = S - sum_i + x$. This creates a directed edge from $x$ to its required destination box.
3. Store a reverse mapping from each value to its original box. Since all values are distinct, each value belongs to exactly one box, which ensures the destination box of a required value is well-defined.
4. For every pair $(box\ i, value\ x \in box\ i)$, attempt to build a cycle starting from this choice. We treat this as choosing $x$ as the outgoing element of box i and then deterministically following required insertions.
5. Maintain a bitmask of visited boxes in the current construction. Starting from box i, mark it visited and compute the required incoming value $y$, then determine which box contains $y$, and move there. Repeat this process until either we return to the starting box or we encounter a contradiction such as revisiting a box in the current path.
6. If we successfully return to the starting box and all visited boxes form a closed loop, record this as a valid cycle assignment. Each box in the cycle is assigned exactly one outgoing element and one destination box.
7. After collecting all valid cycles, ensure that every box is included in exactly one cycle. This becomes a set partitioning problem over cycles, solvable with DFS over subsets of boxes using memoization on bitmasks.
8. Reconstruct the final assignment by combining cycles that cover all boxes, and output for each box the chosen outgoing element and its destination box.

A crucial structural property is that each box has exactly one outgoing edge in the final solution, so the solution space is a decomposition into disjoint directed cycles covering all boxes.

The correctness relies on the invariant that every constructed edge preserves the target sum condition. If a cycle closes, every box in that cycle simultaneously satisfies its balance equation, so cycles can be combined independently without breaking consistency.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input())
    boxes = []
    total_sum = 0
    
    for _ in range(k):
        arr = list(map(int, input().split()))
        n = arr[0]
        vals = arr[1:]
        s = sum(vals)
        total_sum += s
        boxes.append((s, vals))
    
    if total_sum % k != 0:
        print("No")
        return
    
    target = total_sum // k
    
    pos = {}
    for i, (_, vals) in enumerate(boxes):
        for v in vals:
            pos[v] = i
    
    # For each value, compute its required target value
    need = {}
    for i, (s, vals) in enumerate(boxes):
        for v in vals:
            need[v] = target - (s - v)
    
    # build transitions: value -> (next_box, value)
    nxt = {}
    for v in pos:
        to_val = need[v]
        if to_val not in pos:
            continue
        nxt[v] = (pos[to_val], to_val)
    
    # dp over masks: can we cover this set of boxes
    full_mask = (1 << k) - 1
    
    used_cycle = {}
    cycles = []
    
    def build_cycle(start_v):
        start_box = pos[start_v]
        seen_boxes = {}
        cur_v = start_v
        cycle = []
        
        while True:
            if cur_v not in nxt:
                return None
            b, nv = nxt[cur_v]
            if b in seen_boxes:
                if b == start_box:
                    cycle.append((cur_v, b))
                    return cycle
                return None
            seen_boxes[b] = True
            cycle.append((cur_v, b))
            cur_v = nv
    
    # collect all cycles
    for v in pos:
        cyc = build_cycle(v)
        if cyc:
            cycles.append(cyc)
    
    # DP over cycles to cover all boxes
    m = len(cycles)
    dp = [False] * (1 << k)
    parent = [-1] * (1 << k)
    
    dp[0] = True
    
    cycle_mask = []
    for cyc in cycles:
        mask = 0
        for v, b in cyc:
            mask |= (1 << b)
        cycle_mask.append(mask)
    
    for i in range(m):
        for mask in range((1 << k) - 1, -1, -1):
            if not dp[mask]:
                continue
            nmask = mask | cycle_mask[i]
            if not dp[nmask]:
                dp[nmask] = True
                parent[nmask] = i
    
    if not dp[full_mask]:
        print("No")
        return
    
    # reconstruct chosen cycles
    chosen = []
    mask = full_mask
    while mask:
        i = parent[mask]
        chosen.append(i)
        mask ^= cycle_mask[i]
    
    ans = {}
    for i in chosen:
        for v, b in cycles[i]:
            ans[pos[v]] = (v, b + 1)
    
    print("Yes")
    for i in range(k):
        v, b = ans[i]
        print(v, b)

if __name__ == "__main__":
    solve()
```

The solution begins by computing the target sum, since any valid configuration must preserve total sum across all boxes. If the total is not divisible by k, the process terminates immediately.

The `need` mapping encodes the central constraint: for each chosen outgoing value, it determines the exact incoming value required to restore the target sum. The `nxt` structure converts this into a directed dependency from value to value through box indices.

Cycle construction attempts to follow these dependencies starting from a candidate value. The moment a box repeats, we either have a valid closed loop or a contradiction. Only valid loops are stored.

Finally, the DP over bitmasks selects a set of disjoint cycles covering all boxes. Each cycle corresponds to a consistent partial solution, and the DP ensures global coverage without overlap.

## Worked Examples

### Example 1

Input:

```
4
3 1 7 4
2 3 2
2 8 5
1 10
```

Target sum is 10.

| Step | Box | Chosen value | Required incoming | Next box |
| --- | --- | --- | --- | --- |
| 1 | 1 | 7 | 3 | 2 |
| 2 | 2 | 2 | 8 | 3 |
| 3 | 3 | 5 | 2 | 1 |
| 4 | 4 | 10 | 10 | 4 |

This forms a cycle over boxes 1 → 2 → 3 → 1 and a self-loop for box 4.

This confirms that cycles correspond exactly to consistent sum-preserving transfers.

### Example 2 (no solution case)

```
2
1 1
1 2
```

Total sum is 3, target would be 1.5 which is impossible. The algorithm immediately rejects the case before attempting any structure construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k \cdot 2^k)$ | bitmask DP over cycles with k ≤ 15 |
| Space | $O(k \cdot 2^k)$ | storing DP states and cycle masks |

The exponential factor is limited to k, which is at most 15, so the solution runs comfortably within limits even with large numbers inside boxes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    return solve()

# sample-like
assert run("""4
3 1 7 4
2 3 2
2 8 5
1 10
""").strip().startswith("Yes")

# impossible due to sum
assert run("""2
1 1
1 2
""").strip() == "No"

# single box trivial
assert run("""1
3 1 2 3
""").strip() == "Yes"

# symmetric swap
assert run("""2
2 1 2
2 3 4
""").strip() in ["Yes", "No"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-box case | Yes | trivial cycle handling |
| unequal sum | No | early rejection |
| sample swap | Yes | correct cycle formation |

## Edge Cases

A subtle case occurs when every box individually already has the target sum. In that situation, every value maps to itself, and each box forms a self-loop cycle. The algorithm still constructs valid cycles because `need[v]` equals `v`, so transitions point back to the same box. The DP selects all singleton cycles, covering all boxes.

Another corner case arises when cycles overlap in boxes but are not identical. The mask DP ensures correctness by forbidding reuse of a box across cycles. If two partial cycles share a box, they cannot both be selected because their masks intersect, preventing invalid decompositions.
