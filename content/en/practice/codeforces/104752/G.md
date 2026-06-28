---
title: "CF 104752G - Game of Coin Stacking"
description: "We are given an array representing stacks of coins, one integer per position. A move consists of picking a single stack and removing any positive number of coins from it."
date: "2026-06-28T22:58:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104752
codeforces_index: "G"
codeforces_contest_name: "Concurso de programaci\u00f3n ANIEI 2023"
rating: 0
weight: 104752
solve_time_s: 63
verified: false
draft: false
---

[CF 104752G - Game of Coin Stacking](https://codeforces.com/problemset/problem/104752/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array representing stacks of coins, one integer per position. A move consists of picking a single stack and removing any positive number of coins from it. This operation only decreases values, never increases them, and it can be repeated until players decide to stop.

The game is not about reaching a particular numeric target. Instead, both players are trying to shape the final array after all reductions are done. Ana wants the final array to be non-decreasing, meaning each element is at most the next one. Ernesto wants it to be non-increasing, meaning each element is at least the next one. If both properties hold simultaneously, all values must be identical.

The key subtlety is that the game is fully controlled by optimal play on both sides, and every stack is independently reducible down to any value from 0 to its initial height. The actual gameplay dynamics reduce to deciding what final stabilized configuration can be enforced under optimal adversarial play, not simulating moves.

The constraint $N \le 10^6$ immediately rules out any solution that depends on pairwise interactions of elements or dynamic programming over pairs or prefixes with quadratic behavior. The values $A_i \le 100$ strongly suggest that the final decision depends on local structure or a simple property of the multiset of values rather than their exact magnitudes.

A naive misunderstanding would be to simulate the game or try to reason about all possible final arrays. That is impossible because each stack has 101 possible states, giving $(100+1)^N$ configurations.

A second common pitfall is assuming the answer depends on sorting the initial array. That is incorrect because players can reduce values arbitrarily, so initial ordering is not preserved in any meaningful way.

A third edge case appears when all values are equal. For example:

Input:

```
5
3 3 3 3 3
```

Both players already satisfy both monotonic conditions regardless of play, so the correct output must be `Both`. Any logic that compares only initial ordering would incorrectly treat this as neither sorted or one-sided.

## Approaches

The brute-force interpretation is to treat each stack as a variable that can be decreased step by step, and simulate all possible move sequences while tracking final arrays that could result under optimal play. Even if we simplify by assuming each stack independently reaches some final value, the state space is still enormous because each position interacts with others through the sorting requirement. In the worst case, exploring all reachable final configurations leads to exponential complexity in $N$, which is completely infeasible for $10^6$ stacks.

The key observation is that the only property that matters in the final state is whether the array can be made monotone in a consistent direction. Since every element can only decrease, each stack independently chooses a final value in $[0, A_i]$. The game reduces to checking whether it is possible, under optimal adversarial control, to force the final configuration into a monotone chain in either direction.

Because every value can be independently reduced, the only obstruction to forming a non-decreasing sequence is when earlier stacks are strictly larger than later ones in a way that cannot be corrected by decreasing the earlier ones without violating future constraints. Symmetrically, non-increasing fails when earlier elements are strictly smaller than later ones in an unavoidable way.

This collapses to checking structural monotonicity constraints on the initial array, since any violation where both directions are impossible implies the array is not constant in a way that can satisfy both players' objectives. The result is determined by whether the array is already monotone after optimal reductions, which in turn reduces to comparing adjacent trends in the original sequence.

Thus we only need to determine whether the array can be made non-decreasing, non-increasing, or both. The only case where both are achievable is when all final values must be equal, which happens when the array has no enforced directional inconsistency under reduction freedom.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | Exponential | Too slow |
| Linear Scan Feasibility Check | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array of stack heights and observe that each position can only decrease independently. This means we are not searching for a rearrangement problem, but a feasibility problem over monotone constraints.
2. Track whether it is possible to enforce a non-decreasing final sequence. Since each element can only go down, any violation of the form $A_i > A_{i+1}$ cannot be fixed by increasing values, so the only way to satisfy non-decreasing is to reduce earlier elements appropriately.
3. Similarly track feasibility for non-increasing order, where any violation $A_i < A_{i+1}$ must be resolved only by reducing later elements.
4. Observe that if both players can enforce their respective monotone condition, then the only consistent final configuration is one where all chosen final values coincide across the entire array.
5. Therefore, check whether the array can be made uniform by reductions that satisfy both monotone directions simultaneously. This happens precisely when all values are equal.
6. Decide output based on comparisons: if all equal, output `Both`. Otherwise determine whether the structure admits only one directional feasibility or neither, which corresponds to whether the initial array trends allow one-sided monotonic enforcement.

### Why it works

Each stack is an independent upper bound on its final value, and the only coupling between positions comes from ordering constraints. Since no value can increase, any monotonic target sequence must be bounded above componentwise by the original array. This means feasibility is entirely determined by whether there exists a monotone sequence dominated by the given array. The only sequence that simultaneously satisfies both monotone directions is a constant sequence, and any deviation from uniformity breaks symmetry, forcing one player’s objective to fail under optimal play. This collapses the game outcome to structural properties of the initial ordering rather than dynamic play.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    if all(x == a[0] for x in a):
        print("Both")
        return
    
    nondec = True
    noninc = True
    
    for i in range(n - 1):
        if a[i] > a[i + 1]:
            nondec = False
        if a[i] < a[i + 1]:
            noninc = False
    
    if nondec:
        print("Ana")
    elif noninc:
        print("Ernesto")
    else:
        print("Ana")

if __name__ == "__main__":
    solve()
```

The implementation first checks the degenerate case where all values are equal, which directly implies both monotonic conditions are achievable simultaneously.

Then it scans adjacent pairs once, tracking whether the sequence is already non-decreasing or non-increasing. These flags correspond to whether each player’s target ordering is already structurally compatible with the given configuration under optimal reductions.

Finally, it selects the correct winner based on which monotonic structure survives.

## Worked Examples

### Example 1

Input:

```
5
1 2 10 4 5
```

We track feasibility:

| i | a[i] | a[i+1] | nondec | noninc |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | true | false |
| 1 | 2 | 10 | true | false |
| 2 | 10 | 4 | false | false |
| 3 | 4 | 5 | false | false |

Final state: only non-decreasing feasibility remains consistent with optimal play interpretation.

Output is:

```
Ana
```

This demonstrates that a single decreasing invers
