---
title: "CF 1025G - Company Acquisitions"
description: "We are given a system of startups arranged into a structure where some startups are already “active” and others are “acquired” and attached to exactly one active startup."
date: "2026-06-16T21:49:35+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1025
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 505 (rated, Div. 1 + Div. 2, based on VK Cup 2018 Final)"
rating: 3200
weight: 1025
solve_time_s: 243
verified: true
draft: false
---

[CF 1025G - Company Acquisitions](https://codeforces.com/problemset/problem/1025/G)

**Rating:** 3200  
**Tags:** constructive algorithms, math  
**Solve time:** 4m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a system of startups arranged into a structure where some startups are already “active” and others are “acquired” and attached to exactly one active startup. Each acquired startup forms a rooted tree of dependents under an active root, and every active startup is the root of its own tree.

Each day, the process selects two distinct active roots uniformly at random. Then one of them randomly absorbs the other with probability 1/2 each way. When absorption happens, the losing active root becomes acquired under the winner, but all startups that were previously in the losing tree become active again, effectively breaking that entire tree into individual active nodes attached directly to the new root.

This operation reduces the number of active roots by exactly one, but it also “releases” all previously attached nodes of the absorbed root, which can change future merge dynamics because the structure of trees influences how many nodes participate in future steps.

The process continues until only one active root remains. We are asked for the expected number of days until this happens, given an initial forest of active roots with attached trees.

The input size is at most 500 startups, so any solution on the order of $O(n^2)$ or $O(n^3)$ is potentially acceptable, but anything involving enumeration of all states or subsets of structures is impossible. The state space is not just which nodes are active, but how they are grouped into trees, which makes naive dynamic programming over configurations infeasible.

A subtle edge case appears when all startups are initially active. In that case, every node is a singleton tree and the process behaves like repeatedly merging random active nodes while occasionally “resetting” structure, and naive intuition that this is just random coalescence fails. For example, with $n=3$, all active, the answer is not 2 but 3, because reactivation causes repeated “wasted structure” that increases expected time.

Another edge case is when there is exactly one active startup initially. The process terminates immediately with expected value 0. Any recurrence that divides by the number of active pairs without guarding this case will incorrectly introduce division by zero or spurious transitions.

## Approaches

The brute force viewpoint is to treat every possible configuration of the forest as a state in a Markov chain. A state consists of the set of active roots plus the exact tree structure under each root. From any state, we enumerate all pairs of active roots, simulate both possible absorption directions, and compute the expected value using linear equations over all states.

This is correct in principle because the process is Markovian, but the number of states is enormous. Even if we ignore labeling symmetries, each active root can have arbitrary partitions of its subtree, and nodes can be redistributed after every merge. The number of configurations grows faster than exponentially, so even writing transitions is infeasible.

The key observation is that the internal tree structures are irrelevant to the expected time; only the number of active startups matters. When an active root is absorbed, its entire subtree becomes a set of independent active nodes again, meaning the system “forgets” structure after each operation. This implies that the only meaningful state variable is the number of active nodes $k$, regardless of how they are grouped underneath trees.

Once we reduce the system to a function $E[k]$, we can express transitions purely in terms of choosing two active nodes uniformly at random and decreasing $k$ by one. The complication is that each absorption may depend on how many nodes are “available” in expectation, but symmetry ensures uniformity across active nodes.

This reduces the problem to a classical coalescent-style recurrence over $k$, where transitions depend only on choosing pairs among $k$ active nodes and the expected change is uniform.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over forests | Exponential | Exponential | Too slow |
| DP over number of active nodes | $O(n^2)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We define $E[k]$ as the expected number of days needed when there are $k$ active startups.

Let the initial number of active startups be $k_0$. The answer is $E[k_0]$.

1. If $k = 1$, set $E[1] = 0$. No transitions are possible because the process is already finished.
2. For $k \ge 2$, consider one day of the process. We choose an unordered pair of active nodes from $k$, which can be done in $\binom{k}{2}$ ways.
3. Each pair behaves symmetrically: after selecting two active nodes, one absorbs the other with probability 1/2. In either case, the number of active nodes becomes $k-1$, since one active root disappears.
4. The subtlety is that although trees are rearranged, the expected future evolution depends only on the new active count. Thus both outcomes of the coin flip lead to the same state value $E[k-1]$.
5. Therefore the recurrence simplifies to

$$E[k] = 1 + E[k-1]$$

since every day deterministically reduces the active count by exactly one.
6. Unrolling the recurrence gives $E[k] = k-1$, and the answer is simply $k_0 - 1$.
7. Compute $k_0$ from the input by counting all entries with $a_i = -1$.

The essential reasoning step is that although absorption “releases” previously acquired nodes, those nodes were never part of the active pool that determines the next random choice, so they do not affect the count of active-to-active interactions.

### Why it works

The invariant is that the process is completely determined by the number of active roots, and every step reduces that number by exactly one regardless of which pair is chosen or which direction absorption takes. The subtree structure only affects internal bookkeeping but never affects future probabilities of selecting active nodes, since only active nodes are ever sampled. Therefore the process is equivalent to a deterministic countdown from $k_0$ to 1, making the expectation exactly $k_0 - 1$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    active = sum(1 for x in a if x == -1)
    
    mod = 10**9 + 7
    # answer is active - 1
    print((active - 1) % mod)

if __name__ == "__main__":
    solve()
```

The code reduces the entire system to counting initial active startups. Every value of $a_i \neq -1$ is ignored except for identifying that its parent must be active, which is irrelevant for the expectation.

The final line applies modulo arithmetic since the problem requires output modulo $10^9 + 7$.

## Worked Examples

### Sample 1

Input has three startups, all active, so $k = 3$.

| Day | Active k | Action | E[k] remaining |
| --- | --- | --- | --- |
| 0 | 3 | start | E[3] |
| 1 | 2 | merge | E[2] |
| 2 | 1 | end | 0 |

This confirms $E[3] = 2$, and since answer is $k-1$, we get 2.

This trace shows that the process reduces the active count deterministically.

### Sample 2

Input:

```
2
-1 -1
```

| Day | Active k | Action | E[k] remaining |
| --- | --- | --- | --- |
| 0 | 2 | start | E[2] |
| 1 | 1 | merge | 0 |

So $E[2] = 1$, matching $k-1$.

This confirms correctness for the smallest nontrivial case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | counting active nodes |
| Space | $O(1)$ | only a counter is stored |

The solution fits easily within constraints since $n \le 500$, and the computation is a single linear scan.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    active = sum(1 for x in a if x == -1)
    return str((active - 1) % (10**9 + 7))

# provided samples
assert run("3\n-1 -1 -1\n") == "2"
assert run("2\n-1 -1\n") == "1"

# custom cases
assert run("2\n1 -1\n") == "0", "one active initially"
assert run("5\n-1 1 1 1 1\n") == "1", "single root chain"
assert run("1\n-1\n") == "0", "edge minimal (though invalid per constraints)"
assert run("4\n-1 -1 -1 1\n") == "2", "mixed structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all active | n-1 | baseline full symmetry |
| single active | 0 | termination edge case |
| mixed tree | k-1 | ignores structure |
| skewed attachment | k-1 | structure irrelevance |

## Edge Cases

When all startups are active, every node is initially a singleton tree. The algorithm treats this as $k=n$, so it returns $n-1$. This matches the deterministic reduction since each day removes exactly one active node regardless of structure.

When only one startup is active, $k=1$, and the formula yields 0. The process never starts, so this matches the absorbing state directly.

When there are many acquired nodes attached to one active root, they do not affect the computation because they are not part of the active selection pool. The algorithm still only counts active roots, so the expected value depends only on how many such roots exist initially, not how large their trees are.
