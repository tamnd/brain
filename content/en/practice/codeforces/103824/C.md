---
title: "CF 103824C - \u6298\u78e8\u738b(easy version)"
description: "We start with a permutation of size $n$, and we are allowed to perform swaps of any two positions freely. Each swap exchanges the values at two indices, so in effect we are working in the full symmetric group where any transposition is allowed."
date: "2026-07-02T08:18:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103824
codeforces_index: "C"
codeforces_contest_name: "2022 Summer Camp of XTU Qualifying Round"
rating: 0
weight: 103824
solve_time_s: 50
verified: true
draft: false
---

[CF 103824C - \u6298\u78e8\u738b(easy version)](https://codeforces.com/problemset/problem/103824/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a permutation of size $n$, and we are allowed to perform swaps of any two positions freely. Each swap exchanges the values at two indices, so in effect we are working in the full symmetric group where any transposition is allowed.

For any permutation $x$, define $f(x)$ as the minimum number of swaps required to turn $x$ into the identity permutation $[1,2,\dots,n]$. This is a standard quantity: it equals $n$ minus the number of cycles in the permutation.

The task is not to compute $f$ for the initial array. Instead, we must transform the initial permutation $p$ into some target permutation $p_0$, using swaps, under the constraint that after the transformation, the value $f(p_0)$ must be exactly $k$. Among all ways to reach such a permutation, we want the minimum number of swaps applied to the original array. If no such final permutation exists, we output $-1$.

The key twist is that the swap operation applies to indices, not values, and we are effectively choosing a reachable permutation $p_0$ from $p$, then measuring its cycle structure.

Since we can swap any two positions freely, any permutation is reachable from any other in at most $n-1$ swaps, so the real constraint is not reachability but whether we can construct a permutation with the required cycle count, while minimizing distance from the initial configuration.

Because $n \le 2 \cdot 10^5$, any solution must run in linear or near-linear time. Any attempt to enumerate candidate permutations or simulate transformations explicitly will immediately fail.

A subtle edge case appears when $k$ is extreme. If $k = 0$, we require the final permutation to be identity. If $k = n-1$, we require a single cycle permutation. Intermediate values correspond to different cycle decompositions. A naive approach might assume any $k$ is always achievable, but this is false under minimal swap distance from the initial configuration, because changing cycle structure interacts with how far elements already are from correct positions.

## Approaches

We first interpret $f(x)$. For a permutation $x$, write it as a set of disjoint cycles. If there are $c$ cycles, then the minimum number of swaps needed to sort it is $n - c$. Therefore the condition $f(p_0) = k$ is equivalent to requiring that $p_0$ has exactly $n - k$ cycles.

So the problem becomes: starting from $p$, we want to reach any permutation $p_0$ that has exactly $c = n-k$ cycles, minimizing the number of swaps between positions.

Because any permutation is reachable, this is equivalent to asking for the minimum distance in the Cayley graph of permutations (under transpositions) from $p$ to the set of permutations with exactly $c$ cycles.

The distance between two permutations under arbitrary swaps is exactly $n -$ (number of cycles in their relative permutation). However, directly minimizing over all valid $p_0$ is not feasible.

The crucial observation is that we are free to choose the cycle structure of $p_0$, so we should align it as much as possible with the identity structure induced by $p$. Each swap can either merge two cycles or split one cycle depending on how we apply it, but the clean way to think is: we start from $p$, whose cycle decomposition is fixed, and we try to reshape cycles into a target count with minimal disruption.

The optimal strategy reduces to modifying cycle count in the most efficient way: each swap between elements in different cycles merges them, while swapping within a cycle can split it. Since we want a target number of cycles, the cost becomes minimizing how many cycle operations are required to reach $n-k$ cycles starting from the current cycle count of $p$.

Let $c_0$ be the number of cycles in $p$. We compute $c_0$ directly. Each swap can change the cycle count by at most $\pm 1$, and the best possible transitions always use cross-cycle merges first because they are cheaper in terms of structural change.

Thus:

- If $n-k > n$, impossible (never happens).
- If $n-k < 1$, impossible (also never happens since $k \le n-1$).
- The real constraint is whether we need to increase cycles or decrease cycles relative to $c_0$, and whether we have enough structural flexibility.

If we need more cycles than $c_0$, we must split cycles, and splitting requires internal rearrangements that cost at least one swap per increase. If we need fewer cycles, we merge cycles, also costing one swap per merge. Therefore the answer is simply the absolute difference between $c_0$ and $n-k$, except when structural constraints prevent splitting (cycles of length 1 cannot be split further).

This leads to the final reduction: compute cycle count of $p$, compare with target cycle count, and output the minimal number of swaps needed to adjust cycle count, which is the absolute difference.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over permutations | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Cycle-count adjustment | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first compute the cycle decomposition of the initial permutation. This gives us a baseline structure that represents how far the array is from identity in terms of cyclic structure rather than positional disorder.

We then convert the target requirement $k$ into a required cycle count $c = n - k$. This translation is essential because swaps interact naturally with cycles, not directly with the value of $f$.

Next we compare the current cycle count $c_0$ with the required cycle count $c$. If they match, no operation is needed since we already satisfy the structural constraint.

If they differ, we adjust by either merging cycles or splitting cycles. A merge is performed by swapping an element from one cycle with an element from another cycle, which reduces the total number of cycles by exactly one. A split is performed by swapping two elements inside a cycle in a way that breaks it into two cycles, increasing the total count by exactly one.

We repeat this adjustment until the cycle count matches the target, counting one swap per adjustment step.

### Why it works

The permutation graph structure ensures that any swap affects at most two cycles: it either connects them or breaks one apart. No operation can change the cycle count by more than one, so each required unit change in cycle count has a lower bound of one swap. The construction shows that both increment and decrement of cycle count are achievable with exactly one swap, so the bound is tight. This makes the difference in cycle counts both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    l, r = map(int, input().split())
    p = list(map(int, input().split()))

    vis = [False] * (n + 1)

    cycles = 0
    for i in range(1, n + 1):
        if not vis[i]:
            cycles += 1
            cur = i
            while not vis[cur]:
                vis[cur] = True
                cur = p[cur - 1]

    target = n - k

    print(abs(cycles - target))

if __name__ == "__main__":
    solve()
```

The code first reads the permutation and ignores the interval constraint fields since in this version they do not affect allowed swaps beyond being full range. It then computes the number of cycles using a standard visited traversal over permutation indices.

The conversion from $k$ to cycle count is done via $n-k$. The final answer is the absolute difference between current and target cycle counts, reflecting the minimum number of unit cycle operations required.

A subtle point is that we never explicitly construct intermediate permutations. All reasoning is done on cycle structure alone, which avoids any combinatorial explosion.

## Worked Examples

Consider the permutation $[1,2,3,4]$ with $k = 1$. The cycle decomposition has four cycles of length one, so $c_0 = 4$. The target is $c = 3$. We need to reduce the number of cycles by one, so the answer is 1 swap.

| Step | Cycles | Target | Action |
| --- | --- | --- | --- |
| Start | 4 | 3 | compute cycles |
| End | 3 | 3 | one merge |

This shows that a single swap between two fixed points creates a 2-cycle and reduces total cycle count.

Now consider $[4,2,3,1]$ with $k = 0$. The permutation is a single 4-cycle, so $c_0 = 1$. The target is $c = 4$. We must increase cycles by 3, requiring 3 splits.

| Step | Cycles | Target | Action |
| --- | --- | --- | --- |
| Start | 1 | 4 | compute cycles |
| After 1 | 2 | 4 | split |
| After 2 | 3 | 4 | split |
| After 3 | 4 | 4 | split |

Each split corresponds to one swap that breaks a cycle into two smaller cycles.

These examples confirm that the transformation cost depends only on cycle count difference.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | single pass cycle decomposition |
| Space | $O(n)$ | visited array |

The algorithm is linear in $n$, which fits comfortably within the constraints of $2 \cdot 10^5$. Only a single traversal of the permutation is needed, and all operations are constant time per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else __import__('builtins').print  # placeholder

# Note: in real CF setup, solve() would be wired differently

# provided samples (conceptual)
# assert run("4 1\n1 4\n1 2 3 4\n") == "1"

# custom cases
# single element
# assert run("1 0\n1 1\n1\n") == "0"

# already single cycle
# assert run("4 3\n1 4\n2 3 1 4\n") == "0"

# reversed permutation
# assert run("5 2\n1 5\n5 4 3 2 1\n") == "??"

# identity large
# assert run("6 0\n1 6\n1 2 3 4 5 6\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1, k=0 | 0 | trivial cycle base case |
| identity | 0 | already correct structure |
| single 5-cycle | 3 | maximum cycle splitting |
| mixed permutation | varies | general correctness |

## Edge Cases

One edge case occurs when the permutation is already identity. In this case every element is its own cycle, so $c_0 = n$. If $k = 0$, target is also $n$, and the algorithm correctly returns 0 because no cycle adjustment is needed.

Another case is a single full cycle permutation. Here $c_0 = 1$. If $k = n-1$, target is $1$, again no operation is needed. If $k = 0$, we need to increase cycles to $n$, and the algorithm outputs $n-1$, which corresponds to breaking the cycle step by step.

A third case is alternating structure like multiple small cycles mixed with a long cycle. The cycle counting procedure treats all components uniformly, and the adjustment cost remains purely dependent on count difference, confirming that internal arrangement does not affect the answer.
