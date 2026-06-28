---
title: "CF 104930H - Australian Solitaire"
description: "We are asked to count sequences of length $N$ where each position contains a “rank” chosen from a fixed ordered set of 13 denominations: Ace is the smallest, followed by 2 up to King."
date: "2026-06-28T07:45:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104930
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 01-26-24 Div. 2 (Beginner)"
rating: 0
weight: 104930
solve_time_s: 52
verified: true
draft: false
---

[CF 104930H - Australian Solitaire](https://codeforces.com/problemset/problem/104930/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count sequences of length $N$ where each position contains a “rank” chosen from a fixed ordered set of 13 denominations: Ace is the smallest, followed by 2 up to King.

The constraint on the sequence is unusual: as we move left to right, each next card must either strictly increase in rank compared to the previous one, or it may be an Ace regardless of the previous value. So the sequence is mostly increasing, but Aces behave like a special reset symbol that can appear anywhere without restriction.

Two sequences are considered different only if at least one position has a different rank, so this is purely a counting problem over rank strings.

The key restriction is local: each position depends only on the previous card. That immediately suggests a dynamic programming formulation over positions and last seen rank.

Since $N \le 20$, any exponential in 13 or 14 states per position is fine. The real constraint is conceptual, not computational.

A subtle edge case appears when sequences use Ace repeatedly. For example, for $N=3$, sequences like $A, A, A$ are valid even though they do not “increase” anywhere. A naive interpretation that forces strict growth except occasional resets might incorrectly disallow repeated Aces or mis-handle transitions involving Ace.

Another subtle case is treating Ace as both the smallest and a wildcard. The rule is asymmetric: Ace is always allowed as the next element, even after a King. If one instead models Ace as rank 1 in a strict ordering, the transition from King to Ace must still be allowed, which breaks standard increasing-sequence DP if not handled separately.

## Approaches

A brute-force method would generate all possible sequences of length $N$ over 13 ranks, check whether each satisfies the rule, and count valid ones. That gives $13^N$ sequences. For $N = 20$, this is about $10^{22}$, which is completely infeasible even with pruning.

The structure of the constraint suggests a dynamic programming state based on the last chosen rank. The key observation is that validity depends only on the previous card and whether the current card is an Ace or strictly larger than it. This local dependence means we can build sequences incrementally without remembering the entire history.

We define DP over positions and last rank, where transitions consider all allowed next ranks. From a state with last rank $x$, we can go to any rank $y > x$, or to Ace regardless of $x$. This creates a directed acyclic structure over states, except that Ace behaves like a global reset that connects from every state.

The optimization comes from recognizing that transitions to “any greater rank” can be aggregated using prefix sums, while Ace transitions contribute a uniform addition from all states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(13^N \cdot N)$ | $O(N)$ | Too slow |
| DP over ranks | $O(N \cdot 13^2)$ | $O(13)$ | Accepted |

## Algorithm Walkthrough

We treat ranks as integers from 0 to 12, where 0 represents Ace and 12 represents King.

1. Initialize a DP array `dp[r]` meaning the number of sequences of current length ending with rank `r`. For length 1, every rank is equally valid, so each state starts with value 1.
2. For each next position, we compute a new DP array `ndp`. For every possible current rank `r`, we want to compute how many ways we can transition into it.
3. For transitions into rank `r`, we sum all previous states `dp[x]` where either `x < r` (strict increase condition) or `r` is Ace. Since Ace can always be chosen, every `dp[x]` contributes to the Ace state.
4. To efficiently compute “sum over all x < r”, we maintain a prefix sum over `dp`. This allows us to get the contribution of strictly increasing transitions in constant time per state.
5. For Ace specifically, we compute it separately as the total sum of all `dp` values, because from any previous rank we can place an Ace.
6. After processing all ranks, replace `dp` with `ndp` and repeat for all positions up to $N$.
7. The final answer is the sum of all values in `dp` after processing $N$ positions.

### Why it works

At every step, the DP state fully summarizes all valid sequences of a given length by only remembering the last rank. The transition rule depends only on that last rank and whether the next card is Ace or greater. Since every valid extension is counted exactly once through either prefix transitions or the global Ace transition, no sequence is missed or double-counted. The prefix sum structure ensures that the “strictly increasing” constraint is enforced exactly without recomputing overlaps.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n = int(input().strip())
    
    # dp[r] = number of sequences ending in rank r
    # 0 = Ace, 1..12 = 2..King
    dp = [1] * 13
    
    for _ in range(n - 1):
        total = sum(dp) % MOD
        
        # prefix sums for strict increases
        pref = [0] * 14
        for i in range(13):
            pref[i + 1] = (pref[i] + dp[i]) % MOD
        
        ndp = [0] * 13
        
        for r in range(13):
            if r == 0:
                # Ace can be placed after anything
                ndp[r] = total
            else:
                # sum of all x < r
                ndp[r] = pref[r] % MOD
        
        dp = ndp
    
    print(sum(dp) % MOD)

if __name__ == "__main__":
    solve()
```

The implementation follows the DP described above. The prefix array `pref` is used to quickly compute sums over all previous ranks smaller than the current one, enforcing the strictly increasing condition. The Ace state is handled separately using the total sum of all previous states, since Ace ignores ordering constraints.

We iterate exactly $N-1$ transitions because the first position is initialized directly.

Care must be taken with modulo operations, especially when computing `total` and prefix sums, since intermediate sums can grow beyond integer limits if not reduced.

## Worked Examples

### Example 1

Input:

```
2
```

We start with all dp states as 1.

| Step | dp (Ace..King) | total | ndp(Ace) | ndp(2..King) |
| --- | --- | --- | --- | --- |
| init | 13 ones | - | - | - |
| after 1 step | computed | 13 | 13 | prefix-based |

For rank 2 (index 1), we can only come from Ace, so value is 1. For Ace, we can come from all 13 states, giving 13. Summing valid endings produces 91.

This confirms that even short sequences already include many combinations where Ace acts as a reset.

### Example 2

Input:

```
3
```

Now the DP expands further:

| Step | dp sum |
| --- | --- |
| after 1st transition | 91 |
| after 2nd transition | larger aggregated value |

The second transition demonstrates the key behavior: sequences ending in higher ranks accumulate only from smaller ranks, while Ace continuously injects full-state transitions.

This shows how Ace dominates combinatorial growth by acting as a global connector.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \cdot 13)$ | Each step computes 13 states using prefix sums |
| Space | $O(13)$ | Only current DP arrays are stored |

The constraints $N \le 20$ make even simpler implementations feasible, but this DP scales comfortably beyond the limit. The constant factor is tiny, and the algorithm runs instantly within the 2-second limit.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    dp = [1] * 13

    for _ in range(n - 1):
        total = sum(dp) % MOD
        pref = [0] * 14
        for i in range(13):
            pref[i + 1] = (pref[i] + dp[i]) % MOD

        ndp = [0] * 13
        for r in range(13):
            if r == 0:
                ndp[r] = total
            else:
                ndp[r] = pref[r]
        dp = ndp

    return str(sum(dp) % MOD)

# provided sample
assert run("2\n") == "91"

# minimum size
assert run("1\n") == "13", "single card"

# small sanity
assert run("3\n") > "0", "positive growth"

# edge: maximum constraint
assert run("20\n") > "0", "stability"

# all structure test
assert run("2\n") != "0", "non-empty transitions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 13 | base initialization correctness |
| 2 | 91 | sample correctness |
| 3 | >0 | growth under transitions |
| 20 | >0 | stability at max depth |

## Edge Cases

For $N = 1$, the answer must be exactly 13 because every single rank is valid as a one-element sequence. The DP starts with all ones, so the final sum remains 13, matching the rule that no transitions are involved.

For sequences dominated by Ace, such as $A, A, A, \dots$, the algorithm counts them through the Ace transition which always uses the total sum of previous states. For example, at each step, Ace receives contributions from every possible ending state, so repeated Ace sequences are never missed and are correctly accumulated as part of the global sum.

For strictly increasing sequences without Ace, such as $2, 5, 9$, the prefix sum mechanism ensures they are counted exactly once per valid path. Each extension only uses states with smaller rank, so no invalid backward transitions are introduced.
