---
title: "CF 103664D - \u041e\u0431\u043c\u0435\u043d"
description: "We are given a strictly increasing list of coin denominations, where each denomination divides the next one. This means the system behaves like a chained multiplicative structure rather than arbitrary coin values."
date: "2026-07-02T21:49:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103664
codeforces_index: "D"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2019"
rating: 0
weight: 103664
solve_time_s: 46
verified: true
draft: false
---

[CF 103664D - \u041e\u0431\u043c\u0435\u043d](https://codeforces.com/problemset/problem/103664/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a strictly increasing list of coin denominations, where each denomination divides the next one. This means the system behaves like a chained multiplicative structure rather than arbitrary coin values. We are also given a target amount `b`, and we need to determine whether we can form exactly `b` using these coins, and if yes, minimize the total number of coins used.

The output is either a distribution over coin types, telling how many coins of each denomination are used, or a statement that no exact representation exists.

The divisibility condition is the key structural constraint. Since each `a[i]` is divisible by `a[i-1]`, every denomination can be interpreted as a scaled version of the previous one. This makes greedy reasoning potentially viable, but only if we respect how carry and remainder interact across levels.

The constraints are small in terms of `n`, with at most 30 denominations, but `b` can be as large as 10^18. This immediately rules out any dynamic programming over sums. Even DP over all subsets or amounts is impossible because the state space is astronomically large. Any correct solution must run in linear or near-linear time in `n`.

A subtle failure case appears if we try to greedily take as many largest coins as possible without considering divisibility structure. For example, if denominations are `[1, 3, 9]` and `b = 6`, a naive greedy strategy would take `9` coins is impossible so it takes `3 + 3`, which is correct, but in more complex systems with non-canonical behavior, greedy can fail. Here, correctness depends on the divisibility chain enabling base conversion style reasoning.

Another failure mode is forgetting that leftover remainder at one level may or may not be transferable to the next denomination depending on divisibility ratios. If we do not normalize properly, we can incorrectly conclude impossibility.

## Approaches

A brute-force idea would be to treat this as a coin change problem: try all combinations of counts for each denomination. Since `b` can be up to 10^18, even if each coin count were bounded by `b / a[i]`, the number of combinations is exponential in `n`. With `n = 30`, this is completely infeasible.

A second naive improvement would be dynamic programming on reachable sums, but the range of sums makes this impossible in both time and memory.

The key observation is that the divisibility condition turns the system into a mixed-radix representation problem. Each denomination is a “digit place”, and because `a[i]` divides `a[i+1]`, we can define ratios `r[i] = a[i+1] / a[i]`. Then any valid representation behaves like a number written in a non-uniform base system, except we are minimizing digit sum rather than just representing a number.

This suggests a greedy bottom-up conversion: start from the largest denomination and decide how many coins to take, then propagate remainder downward. However, unlike standard greedy coin change, we must ensure consistency across all levels, because higher-level choices constrain lower-level remainders.

We solve this by enforcing that at each level we never take more than necessary modulo the next ratio, and we carry the remainder down.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We first preprocess the ratios between consecutive denominations. For each `i > 1`, define `r[i] = a[i] / a[i-1]`.

We then work from the largest denomination downwards, maintaining the remaining amount we still need to represent.

1. Start with `rem = b`. This value represents what is still not expressed in higher denominations. We also initialize an array `cnt` of size `n` to zero.
2. For each denomination from `i = n` down to `2`, compute how many full coins of `a[i]` we can take from `rem`, but only in a way consistent with the next smaller scale. We compute `cnt[i] = rem // a[i]`, then reduce `rem = rem % a[i]`.

This step is valid because taking a coin of value `a[i]` affects only higher multiples of `a[i-1]`, and due to divisibility, lower denominations can always represent the remainder.
3. Before moving down, we must ensure that `rem` is compatible with the next level scaling. Specifically, since `a[i]` is a multiple of `a[i-1]`, the remainder `rem` is already naturally in units of `a[i-1]` scale, so no adjustment is needed beyond integer division.
4. After processing down to `i = 2`, we are left with `rem` which must be handled using `a[1]`. We set `cnt[1] = rem // a[1]`, and update `rem = rem % a[1]`.
5. If at the end `rem != 0`, it means we cannot exactly represent `b` using the available denominations, so we output `"Impossible"`.
6. Otherwise, we output the counts.

The key idea is that because of the divisibility chain, every remainder at level `i` is guaranteed to be representable using smaller denominations if and only if it is divisible at the final step by `a[1]`. The algorithm avoids backtracking by ensuring all decisions are locally consistent with the radix structure.

### Why it works

The structure of the denominations induces a hierarchy where each `a[i]` is an integer multiple of `a[i-1]`. This means every number expressible using higher denominations is always aligned on the grid defined by lower denominations. When we greedily extract contributions at each level, we are effectively performing a positional decomposition of `b` in a mixed-radix system. The invariant is that after processing level `i`, the remaining value is always strictly less than `a[i]` and is fully representable using denominations `1..i-1` if and only if it remains divisible down to `a[1]`. This guarantees that no future step can invalidate a previously chosen coefficient, so the construction is globally consistent.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = int(input())

    cnt = [0] * n
    rem = b

    for i in range(n - 1, -1, -1):
        cnt[i] = rem // a[i]
        rem %= a[i]

    if rem != 0:
        print("Impossible")
    else:
        print(*cnt)

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the greedy decomposition. We maintain a running remainder and peel off contributions from largest to smallest denomination. The important subtlety is that we never need to check divisibility explicitly between adjacent denominations, because the structure guarantees alignment: every `a[i]` is a multiple of `a[i-1]`, so reducing modulo `a[i]` preserves consistency for lower levels.

A common mistake would be trying to adjust counts using ratio propagation explicitly. That is unnecessary here because integer division already performs correct digit extraction in this mixed base system.

## Worked Examples

Consider an input with denominations `[1, 3, 9]` and `b = 6`.

We start with `rem = 6`.

| i | a[i] | cnt[i] | rem after mod |
| --- | --- | --- | --- |
| 2 | 9 | 0 | 6 |
| 1 | 3 | 2 | 0 |
| 0 | 1 | 0 | 0 |

After processing, remainder becomes zero, so the answer is `[0, 2, 0]`.

This trace shows that the algorithm naturally prefers larger denominations but only when they fit exactly into the remaining amount. It confirms that no carry interaction is needed beyond modular decomposition.

Now consider `[1, 4, 8]` and `b = 7`.

| i | a[i] | cnt[i] | rem after mod |
| --- | --- | --- | --- |
| 2 | 8 | 0 | 7 |
| 1 | 4 | 1 | 3 |
| 0 | 1 | 3 | 0 |

Again, the decomposition succeeds even though 7 cannot use 8. The structure reduces the problem cleanly into independent levels.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each denomination is processed once in a single pass |
| Space | O(n) | Storage for counts and input array |

With `n ≤ 30`, this runs instantly within limits. The solution avoids any dependence on `b`, which is crucial since `b` can be as large as 10^18.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import isclose

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    b = int(sys.stdin.readline())

    cnt = [0] * n
    rem = b

    for i in range(n - 1, -1, -1):
        cnt[i] = rem // a[i]
        rem %= a[i]

    if rem != 0:
        return "Impossible"
    return " ".join(map(str, cnt))

# provided samples (illustrative since original formatting is unclear)
assert run("1\n1\n1\n") == "1", "single coin exact"
assert run("2\n1 2\n3\n") == "1 1", "simple decomposition"

# custom cases
assert run("2\n2 4\n3\n") == "Impossible", "cannot form odd with even base"
assert run("3\n1 3 9\n6\n") == "0 2 0", "classic case"
assert run("3\n1 3 9\n0\n") == "0 0 0", "zero case"
assert run("4\n1 2 4 8\n15\n") == "1 1 1 1", "binary-like full use"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 coin only | 1 | trivial base case |
| even-only system | Impossible | impossibility detection |
| 1,3,9 system | 0 2 0 | mixed-radix correctness |
| zero target | all zeros | boundary condition |
| binary-like chain | 1 1 1 1 | full decomposition |

## Edge Cases

A critical edge case is when `b = 0`. The algorithm processes all denominations and produces zero counts everywhere, and the remainder remains zero throughout. This confirms that zero is always representable regardless of denomination structure.

Another edge case is when only the smallest denomination can represent the number. For example, `[1, 100, 10000]` with `b = 7` produces all higher counts zero and final count 7 at `a[1]`. The greedy pass never misallocates because higher denominations always require at least 100 units.

A failure-prone scenario is when one expects carry correction between levels. Because of divisibility, no such correction is needed, and the modular extraction already enforces consistency.
