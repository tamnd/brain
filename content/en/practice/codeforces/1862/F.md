---
title: "CF 1862F - Magic Will Save the World"
description: "We are asked to calculate the minimum time Vika, a sorceress, needs to defeat a sequence of monsters. Each monster has a strength, and Vika has two types of magic-water and fire. In one second, she generates fixed amounts of water and fire mana."
date: "2026-06-09T00:14:51+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "brute-force", "dp"]
categories: ["algorithms"]
codeforces_contest: 1862
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 894 (Div. 3)"
rating: 1800
weight: 1862
solve_time_s: 88
verified: true
draft: false
---

[CF 1862F - Magic Will Save the World](https://codeforces.com/problemset/problem/1862/F)

**Rating:** 1800  
**Tags:** binary search, bitmasks, brute force, dp  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to calculate the minimum time Vika, a sorceress, needs to defeat a sequence of monsters. Each monster has a strength, and Vika has two types of magic-water and fire. In one second, she generates fixed amounts of water and fire mana. To defeat a monster, she must spend at least as much mana in a single spell as the monster’s strength, using either type of magic. She can cast multiple spells per second if she has enough accumulated mana. The problem asks, for multiple test cases, to find the minimum number of seconds required to defeat all monsters.

The input gives, per test case, the mana generation rates and the strengths of monsters. Constraints are small: the number of monsters per test case is at most 100, and the sum across all test cases is also at most 100. Each monster’s strength is at most $10^4$, while the mana generation per second can be very large, up to $10^9$. This indicates that we can explore solutions that scale exponentially in the number of monsters, because $2^{100}$ is too big, but clever use of subset sums or DP over sums bounded by the total strength (at most $100 \times 10^4 = 10^6$) is feasible.

An edge case occurs when one type of mana is much larger than the other. For example, if Vika can produce 1 unit of water but 100 units of fire per second, and all monsters have strength 50, she should focus on fire spells. A careless approach that always splits mana evenly or ignores the optimal assignment of monsters to magic type would fail. Another edge case is when the sum of monster strengths exactly matches a multiple of mana rates, or when there is only one monster; these require exact calculations rather than approximations.

## Approaches

The brute-force solution considers all possible assignments of monsters to water or fire spells. Each monster has two choices, so there are $2^n$ total assignments. For each assignment, we compute the total water and fire mana needed, divide by the mana generated per second (rounding up), and take the maximum. This guarantees correctness because it literally checks every way to distribute monsters between the two magic types. However, with $n$ up to 100, $2^{100}$ possibilities are infeasible.

The key observation is that this is a classic two-dimensional subset sum problem. We can focus on water mana allocation, because fire is then determined automatically. If we can find a subset of monsters to assign to water such that the total water mana required is $W$, then the remaining monsters require $F$ mana, and the minimum time is $\max(\lceil W / w \rceil, \lceil F / f \rceil)$. The total sum of all monster strengths is at most $10^6$, so we can perform a dynamic programming over achievable water sums. Specifically, we maintain a boolean DP array where `dp[s]` is true if there exists a subset of monsters whose water strength sum is exactly $s$. Once we have the DP, we iterate over all achievable sums `s` and compute the time as $\max(\lceil s / w \rceil, \lceil (total - s) / f \rceil)$, keeping the minimum.

This reduces the problem from exponential to pseudo-polynomial time. The maximum DP size is the sum of all monster strengths, which is at most $10^6$, and for each monster, we update the DP array. With $n \le 100$, this is efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| DP on subset sums | O(n * S) where S=sum of strengths | O(S) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of monster strengths. Let `total = sum(s_i)`.
2. Initialize a boolean DP array of size `total + 1`, with `dp[0] = True` because a sum of 0 is achievable with no monsters.
3. For each monster strength `s_i`, iterate backwards over the DP array from `total` down to `s_i`. If `dp[j - s_i]` is True, then set `dp[j] = True`. This updates all achievable water sums.
4. Initialize `ans` as infinity. Iterate over all indices `w_sum` in the DP array. For each `w_sum` that is achievable (`dp[w_sum] = True`), compute the remaining fire sum `f_sum = total - w_sum`. Compute the time to accumulate mana: `time = max((w_sum + w - 1) // w, (f_sum + f - 1) // f)`. Update `ans = min(ans, time)`.
5. Output `ans` as the minimum seconds required.

Why it works: the DP guarantees we consider every possible split of monsters between water and fire. Each `w_sum` corresponds to a valid allocation of some monsters to water spells. The complement automatically gives the fire allocation. The computation of `max(ceil(W/w), ceil(F/f))` correctly models the time to accumulate sufficient mana of both types. By iterating over all achievable water sums, we ensure the minimum overall time is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        w, f = map(int, input().split())
        n = int(input())
        s = list(map(int, input().split()))
        total = sum(s)
        dp = [False] * (total + 1)
        dp[0] = True
        for strength in s:
            for j in range(total, strength - 1, -1):
                if dp[j - strength]:
                    dp[j] = True
        ans = float('inf')
        for w_sum in range(total + 1):
            if dp[w_sum]:
                f_sum = total - w_sum
                time = max((w_sum + w - 1) // w, (f_sum + f - 1) // f)
                if time < ans:
                    ans = time
        print(ans)

if __name__ == "__main__":
    solve()
```

The DP section iterates backwards to prevent double-counting a single monster multiple times in the same subset. The computation `(w_sum + w - 1) // w` rounds up integer division, equivalent to `ceil(w_sum / w)`, which ensures partial mana accumulation is counted as a full second.

## Worked Examples

**Sample 1 Input:**

```
w=2, f=3, s=[2,6,7]
```

| Monster subset | Water sum | Fire sum | Time for water | Time for fire | Max time |
| --- | --- | --- | --- | --- | --- |
| [2,6,7] water | 15 | 0 | 8 | 0 | 8 |
| [2] water | 2 | 13 | 1 | 5 | 5 |
| [2,7] water | 9 | 6 | 5 | 2 | 5 |
| [6,7] water | 13 | 2 | 7 | 1 | 7 |
| [6] water | 6 | 9 | 3 | 3 | 3 |
| [7] water | 7 | 8 | 4 | 3 | 4 |
| [] water | 0 | 15 | 0 | 5 | 5 |

The minimum maximum time is 3 seconds, achieved by assigning the 6-strength monster to water and the others to fire.

**Sample 2 Input:**

```
w=37, f=58, s=[93]
```

| Subset | Water | Fire | Time water | Time fire | Max |
| --- | --- | --- | --- | --- | --- |
| [93] water | 93 | 0 | 3 | 0 | 3 |
| [] water | 0 | 93 | 0 | 2 | 2 |

Optimal assignment is to cast fire spell, taking 2 seconds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * sum(s_i)) | DP over achievable water sums, iterating backwards for each monster |
| Space | O(sum(s_i)) | Boolean DP array storing achievable water sums |

Given that total sum of strengths ≤ 100 * 10^4 = 10^6, and n ≤ 100, the solution fits comfortably within 4-second time limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("4\n2 3\n3\n2 6 7\n37 58\n1\n93\n190 90\n2\n23 97\n13 4\n4\n10 10 2 45\n") == "3\n2\n1\n5", "sample 1"

# Custom tests
assert run("1\n1 1\n1\n1\n") == "1", "single monster, equal mana"
assert run("1\n10 100\n2\n50 50\n") == "1", "fire should handle both"
assert run("1\n5
```
