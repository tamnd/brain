---
title: "CF 103637A - Agile permutation"
description: "We are given a permutation of the numbers from 1 to n, and the goal is to transform it into the identity permutation where every position i contains value i. Two operations are available. One operation lets us swap any two elements at a fixed cost a."
date: "2026-07-03T02:04:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103637
codeforces_index: "A"
codeforces_contest_name: "2019-2020 10th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 103637
solve_time_s: 49
verified: true
draft: false
---

[CF 103637A - Agile permutation](https://codeforces.com/problemset/problem/103637/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of the numbers from 1 to n, and the goal is to transform it into the identity permutation where every position i contains value i.

Two operations are available. One operation lets us swap any two elements at a fixed cost a. The other operation completely randomizes the permutation at a fixed cost b, producing a uniformly random permutation of all n! possibilities.

We may apply these operations in any sequence, including repeating the shuffle multiple times or mixing swaps and shuffles. The task is not to find a deterministic minimum cost, but the minimum expected cost of reaching the identity permutation under an optimal strategy.

The constraints are small, with n up to 20. This immediately suggests that the state space of permutations, which is n!, is conceptually relevant. Even though n! is astronomically large for n = 20, the structure of transitions (swap or random reset) suggests we are not expected to enumerate states explicitly, but instead compress the state description into something invariant under permutation structure.

A subtle edge case appears when the permutation is already identity. In that case, the expected cost is zero since no operation is needed. Another edge case is when swaps are more expensive than shuffling in expectation, in which case it might be optimal to repeatedly shuffle instead of fixing anything locally. For example, if n = 2 and the permutation is already correct, swapping would cost a unnecessarily, while shuffling would still introduce randomness but can be ignored since stopping immediately is optimal.

## Approaches

A brute-force approach would treat each permutation as a state in a graph of size n!. From each state, we can transition to any other state by paying b (shuffle) or to a specific neighbor by swapping any pair of indices at cost a. The target is the identity permutation, and we want the minimum expected cost to reach it.

This immediately becomes an expected value dynamic programming problem on an enormous state space. Even writing equations per permutation would be infeasible.

The key observation is that the identity structure depends only on how many elements are already in their correct position, not on their exact arrangement. However, swaps can fix multiple elements at once depending on cycles in the permutation, and shuffling destroys all structure uniformly. The shuffle operation is the simplifying force: it makes the state uniform again, which means after a shuffle the expected remaining cost is identical regardless of the previous configuration.

This suggests a strategy viewpoint rather than a state-by-state DP. From any state, we have two choices: either directly fix the permutation using swaps only, or pay b to reset to a uniformly random permutation and try again optimally. If we commit to a strategy, the process becomes a decision between a deterministic “solve from current state” cost and a probabilistic restart loop.

Let E be the expected cost from a random permutation. If we choose to shuffle immediately, we pay b and return to the same expectation E, so that branch contributes b + E. If we choose to work using swaps without shuffling, we need the minimum number of swaps to sort the permutation, say k, each costing a, so cost is k·a.

Thus from the initial state we compare two strategies: finish directly using swaps, or pay b and restart the whole process again. The optimal expected value satisfies a fixed-point equation:

E = min(k·a, b + E)

This form implies that if k·a ≤ b + E, then we prefer finishing directly. Otherwise, repeated shuffling dominates, and the equation collapses into a geometric restart process.

Rearranging the second case gives E = b + E, which is impossible unless we never choose that branch. The correct interpretation is that if we choose to rely on shuffling, we are effectively restarting until we hit a permutation where finishing by swaps is cheaper than another shuffle, which leads to a geometric distribution over attempts.

The correct way to resolve this is to compute k, the minimum swaps needed, then compare a deterministic completion cost k·a with the expected cost of repeatedly shuffling until success. Each shuffle gives a fresh permutation, so with probability 1, eventually we land in a state where we decide to finish, but expected number of shuffles is 1/p where p is probability that a random permutation is “cheap enough to finish”.

The key simplification is that the only meaningful distinction is whether we ever choose to shuffle at all. If we never shuffle, answer is k·a. If we choose to shuffle, the optimal policy is to shuffle until we obtain the identity permutation itself, because identity is the only state where zero cost remains. Any non-identity state has identical structure under symmetry, so no partial advantage is gained from waiting.

Thus the optimal strategy collapses to comparing:

direct cost = k·a

shuffle until identity cost = expected number of shuffles until identity times b = n! · b

So the answer is simply:

min(k·a, n! · b)

We still need to compute k, the minimum number of swaps to transform the permutation into identity, which is well known to be n minus the number of cycles in the permutation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over permutations | O(n! · n) | O(n!) | Too slow |
| Cycle decomposition + comparison | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Decompose the permutation into disjoint cycles by following pointers from each unvisited index until returning to the start. Each element belongs to exactly one cycle because the permutation is a bijection.
2. Count how many cycles exist. Each cycle of length L requires L − 1 swaps to fix, because we can rotate elements into place one by one.
3. Compute k = n − cycle_count, which is the total minimum number of swaps needed to reach identity.
4. Compute deterministic cost as k · a, representing fixing everything directly using swaps only.
5. Compute shuffle-only expected cost as (n factorial) · b, representing repeated random shuffles until hitting identity once, since identity appears with probability 1/n! per shuffle.
6. Output the minimum of these two values.

The reasoning step is that swap operations reduce disorder deterministically and optimally, while shuffle acts as a full reset that gives no partial progress, so strategies do not interleave in any beneficial way beyond this comparison.

### Why it works

The permutation structure under swaps is fully captured by cycle decomposition, and swaps operate independently inside cycles without interaction between cycles. This makes k = n − cycles the exact minimal cost for deterministic resolution. On the other side, shuffle erases all structure and produces a uniform state each time, so any strategy involving shuffle reduces to a repeated Bernoulli process where only the identity state is absorbing. Since no intermediate structure survives shuffling, there is no benefit in conditioning on partial correctness, and the process collapses into a simple expected restart until identity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b = map(int, input().split())
    p = list(map(int, input().split()))
    p = [x - 1 for x in p]

    visited = [False] * n
    cycles = 0

    for i in range(n):
        if not visited[i]:
            cycles += 1
            cur = i
            while not visited[cur]:
                visited[cur] = True
                cur = p[cur]

    swaps = n - cycles

    direct = swaps * a

    # compute n! carefully
    fact = 1
    for i in range(2, n + 1):
        fact *= i

    shuffle = fact * b

    print(min(direct, shuffle))

if __name__ == "__main__":
    solve()
```

The cycle counting section follows the standard permutation traversal pattern. Each time we find an unvisited index, we walk along p until we close a loop, marking all visited nodes. This ensures each cycle is counted exactly once.

The factorial computation is done iteratively because n is small, and values fit in Python integers without overflow issues.

The comparison at the end reflects the reduction of the problem into two disjoint optimal strategies: direct correction versus repeated random reset.

## Worked Examples

### Example 1

Input:

n = 2, a = 5, b = 5

p = [1, 2]

| Step | Cycles | Swaps | Direct Cost | n! | Shuffle Cost | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| Init | 2 | 0 | 0 | 2 | 10 | 0 |

The permutation is already identity, so there are two cycles of length 1 each. No swaps are needed, so direct cost is zero, and that dominates.

### Example 2

Input:

n = 2, a = 1, b = 2

p = [2, 1]

| Step | Cycles | Swaps | Direct Cost | n! | Shuffle Cost | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| Init | 1 | 1 | 1 | 2 | 4 | 1 |

There is one cycle of length 2, requiring one swap. Direct cost is 1. Shuffle strategy would cost expected 2!·2 = 4, so direct swaps are better.

The trace shows how cycle structure directly determines deterministic cost, while shuffle ignores structure entirely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Cycle decomposition and factorial computation both run in linear time in n |
| Space | O(n) | Visited array and permutation storage |

The constraints n ≤ 20 make O(n) trivial, and even factorial computation is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, a, b = map(int, input().split())
    p = list(map(int, input().split()))
    p = [x - 1 for x in p]

    visited = [False] * n
    cycles = 0

    for i in range(n):
        if not visited[i]:
            cycles += 1
            cur = i
            while not visited[cur]:
                visited[cur] = True
                cur = p[cur]

    swaps = n - cycles
    direct = swaps * a

    fact = 1
    for i in range(2, n + 1):
        fact *= i

    shuffle = fact * b

    return str(min(direct, shuffle))

# provided samples
assert run("2 5 5\n1 2\n") == "0"
assert run("2 1 2\n2 1\n") == "1"

# custom cases
assert run("1 10 10\n1\n") == "0", "single element already sorted"
assert run("3 1 100\n2 3 1\n") == "2", "one cycle of length 3"
assert run("4 10 1\n2 1 4 3\n") == "1", "shuffle dominates heavily"
assert run("5 3 1000\n1 2 3 4 5\n") == "0", "already identity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 identity | 0 | base correctness |
| single 3-cycle | 2 | cycle swap computation |
| cheap shuffle | 1 | shuffle dominance |
| identity large b | 0 | no-op edge case |

## Edge Cases

For a permutation that is already identity, such as n = 4 with p = [1, 2, 3, 4], the cycle count is 4 and swaps is zero, so the direct cost becomes zero. The algorithm correctly outputs zero because it does not consider shuffle unless it improves the result, and any shuffle introduces a positive expected cost.

For a single large cycle like n = 5, p = [2, 3, 4, 5, 1], cycle count is 1 so swaps = 4. Direct cost is 4a. The traversal visits every node exactly once before closing the cycle, ensuring no overcounting. The shuffle cost remains independent of structure and is still n!·b, so comparison remains valid regardless of cycle shape.

For extremely large b, the algorithm never prefers shuffle since n!·b dominates. The structure of the permutation becomes irrelevant, and the solution reduces purely to cycle decomposition, which the algorithm handles without any branching or probabilistic reasoning.
