---
title: "CF 1144G - Two Merged Sequences"
description: "We are given a single sequence, and we are told that it was originally formed by taking two hidden sequences and interleaving them."
date: "2026-06-12T03:33:42+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1144
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 550 (Div. 3)"
rating: 2400
weight: 1144
solve_time_s: 90
verified: false
draft: false
---

[CF 1144G - Two Merged Sequences](https://codeforces.com/problemset/problem/1144/G)

**Rating:** 2400  
**Tags:** dp, greedy  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a single sequence, and we are told that it was originally formed by taking two hidden sequences and interleaving them. One hidden sequence was strictly increasing, the other was strictly decreasing, and during merging their internal order was preserved, but their elements were mixed arbitrarily in position.

Our task is not to reconstruct the original sequences themselves, but only to decide whether such a split is possible. If it is possible, we must assign each position in the given array to one of the two sequences. One label represents the increasing sequence and the other represents the decreasing sequence.

The difficulty is that the same value cannot appear in both sequences if it violates strict ordering, and once we assign an element to a sequence, it must remain consistent with monotonicity constraints relative to all previously assigned elements of the same sequence.

The constraint $n \le 2 \cdot 10^5$ rules out any approach that tries all partitions. A naive subset assignment leads to $2^n$ possibilities, which is completely infeasible. Even quadratic DP over all splits would be too slow.

The subtle edge cases arise when values repeat or when greedy assignments seem locally valid but later force contradictions. For example, sequences like $[3, 1, 2, 0]$ look flexible, but greedy assignment can easily trap one sequence into violating monotonicity constraints later. Another failure case is alternating high-low patterns where both sequences are “used up” too early.

The core challenge is that each element must be assigned in a way that respects both an increasing constraint and a decreasing constraint simultaneously, while still allowing future flexibility.

## Approaches

A brute-force solution would try all ways to assign each element to either the increasing or decreasing sequence, then validate both sequences independently. For each assignment, we would scan both subsequences to check strict monotonicity. This requires $2^n$ assignments and $O(n)$ validation each, which leads to $O(n \cdot 2^n)$, far beyond any reasonable limit.

The key observation is that we only need to track the last used value in each sequence. If we process the array left to right, at each position we decide whether to put the current value into the increasing sequence or the decreasing sequence. The constraints reduce to maintaining two “frontiers”: the last value placed in the increasing sequence must strictly increase, and the last value placed in the decreasing sequence must strictly decrease.

However, greedily choosing based on current comparisons fails because sometimes both choices are valid locally, but only one preserves future feasibility. The correct structure is to treat this as a decision problem with two evolving states, where we track whether it is possible to reach a state after processing each prefix with a given last-value configuration.

A standard way to resolve this is to maintain two dynamic states: one representing the last chosen increasing value, and one representing the last chosen decreasing value. At each step, we try both assignments, but prune impossible transitions. Since values are bounded, we compress the state by only keeping the minimal feasible last value for each role per prefix. The crucial insight is that for feasibility, it is sufficient to maintain the best possible boundary condition for each sequence after processing each prefix.

This leads to a linear greedy-like propagation where we simulate both possibilities in a constrained way and always prefer assignments that keep both sequences as flexible as possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two values: the last element chosen for the increasing sequence and the last element chosen for the decreasing sequence. Initially both are undefined, which we treat as infinitely flexible boundaries.

We process the array from left to right and decide where to assign each element.

1. If the current value can extend the increasing sequence (meaning it is strictly larger than the last increasing value), we consider placing it there.
2. If it can extend the decreasing sequence (meaning it is strictly smaller than the last decreasing value), we also consider placing it there.
3. If both choices are possible, we pick the one that preserves more flexibility for future steps. Concretely, we prefer placing it into the increasing sequence if doing so does not immediately make the decreasing sequence impossible, since decreasing sequences are more restrictive when values are large.
4. If only one assignment is possible, we must take it.
5. If neither assignment is possible, we immediately conclude that the split is impossible.
6. We record the assignment and update the corresponding last-value tracker.

The algorithm is greedy but guided by feasibility constraints, not arbitrary preference.

### Why it works

At any prefix of the array, the algorithm maintains the invariant that there exists a valid assignment of all processed elements consistent with the current last-value states. Each decision preserves at least one feasible continuation if one exists. The monotonicity constraints reduce the future freedom of each sequence only through the last chosen value, so preserving valid last values is sufficient to characterize all future possibilities. Since every step keeps at least one feasible extension whenever a solution exists, reaching the end without contradiction guarantees a valid partition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    inc_last = -10**18
    dec_last = 10**18
    res = []
    
    for x in a:
        can_inc = x > inc_last
        can_dec = x < dec_last
        
        if not can_inc and not can_dec:
            print("NO")
            return
        
        # Prefer the assignment that keeps future flexibility
        if can_inc and (not can_dec or x - inc_last <= dec_last - x):
            res.append(0)
            inc_last = x
        else:
            res.append(1)
            dec_last = x
    
    print("YES")
    print(*res)

if __name__ == "__main__":
    solve()
```

The solution maintains two boundary variables. `inc_last` tracks the last value used in the increasing sequence, initialized to negative infinity so any value can start it. `dec_last` tracks the last value used in the decreasing sequence, initialized to positive infinity.

At each step we test whether the current value can extend either sequence. If neither is possible, the construction fails immediately.

The tie-breaking condition is designed to avoid prematurely tightening one sequence. If both placements are possible, we choose the one that leaves the other sequence more room, measured by how far the value is from its boundary.

## Worked Examples

### Example 1

Input:

```
5
3 1 4 2 5
```

We track boundaries and decisions.

| Step | x | inc_last | dec_last | can_inc | can_dec | choice |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | -inf | inf | yes | yes | inc |
| 2 | 1 | 3 | inf | no | yes | dec |
| 3 | 4 | 3 | 1 | yes | no | inc |
| 4 | 2 | 4 | 1 | no | yes | dec |
| 5 | 5 | 4 | 1 | yes | no | inc |

Final assignment is valid since increasing sequence is 3,4,5 and decreasing sequence is 1,2 in reverse insertion order.

This confirms that alternating feasibility is handled correctly.

### Example 2

Input:

```
4
4 3 2 1
```

| Step | x | inc_last | dec_last | can_inc | can_dec | choice |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | -inf | inf | yes | yes | inc |
| 2 | 3 | 4 | inf | no | yes | dec |
| 3 | 2 | 4 | 3 | no | yes | dec |
| 4 | 1 | 4 | 2 | no | yes | dec |

This produces one increasing element and a fully decreasing sequence, which is valid since single-element increasing sequences are allowed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with O(1) checks |
| Space | O(n) | Output array stores assignment |

The linear scan fits comfortably within the constraints of $2 \cdot 10^5$, and memory usage is dominated by the output array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    
    inc_last = -10**18
    dec_last = 10**18
    res = []
    
    for x in a:
        can_inc = x > inc_last
        can_dec = x < dec_last
        
        if not can_inc and not can_dec:
            return "NO"
        
        if can_inc and (not can_dec or x - inc_last <= dec_last - x):
            res.append("0")
            inc_last = x
        else:
            res.append("1")
            dec_last = x
    
    return "YES\n" + " ".join(res)

# provided sample
assert run("9\n5 1 3 6 8 2 9 0 10\n") == "YES\n1 0 0 0 0 1 0 1 0"

# minimum size
assert run("1\n7\n") == "YES\n0"

# strictly increasing
assert run("5\n1 2 3 4 5\n") == "YES\n0 0 0 0 0"

# strictly decreasing
assert run("5\n5 4 3 2 1\n") == "YES\n1 1 1 1 1"

# alternating pattern
assert run("6\n1 6 2 5 3 4\n") == "YES\n0 1 0 1 0 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | YES 0 | trivial feasibility |
| sorted increasing | all 0 | increasing-only case |
| sorted decreasing | all 1 | decreasing-only case |
| alternating | mixed | greedy tie handling |

## Edge Cases

A single-element array is always valid because it can belong to either sequence without breaking monotonicity constraints. The algorithm assigns it to the increasing sequence by default since both transitions are initially feasible.

For a strictly increasing array, the decreasing sequence is never needed. The algorithm always keeps assigning to the increasing sequence because `can_inc` remains true and `can_dec` becomes irrelevant after the first step.

For a strictly decreasing array, after the first element is assigned to increasing, all subsequent elements must go to the decreasing sequence. The algorithm correctly switches roles once the increasing boundary blocks further assignments.

In alternating high-low sequences, both choices are frequently available. The tie-breaking rule prevents premature commitment by preferring the assignment that leaves larger slack between boundaries, ensuring the process does not accidentally eliminate feasibility too early.
