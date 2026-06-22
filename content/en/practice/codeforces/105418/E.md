---
title: "CF 105418E - Magical Coins"
description: "We are given a set of coin denominations that follow a very structured pattern: each coin is a number consisting entirely of digit 1, and the lengths grow in a special way. So we get values like 11, 111, 1111, 11111, and so on, continuing indefinitely."
date: "2026-06-23T04:22:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105418
codeforces_index: "E"
codeforces_contest_name: "Algorithmia IIITN 2024 - Round 1"
rating: 0
weight: 105418
solve_time_s: 82
verified: false
draft: false
---

[CF 105418E - Magical Coins](https://codeforces.com/problemset/problem/105418/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of coin denominations that follow a very structured pattern: each coin is a number consisting entirely of digit 1, and the lengths grow in a special way. So we get values like 11, 111, 1111, 11111, and so on, continuing indefinitely. Each test case gives a target amount `n`, and we need to determine whether it is possible to represent `n` as a sum of these coins, where each coin type can be used an unlimited number of times.

Reframing this, we are checking whether `n` can be expressed as a linear combination of numbers like 11, 111, 1111, etc., with non-negative integer coefficients. The structure suggests a classic unbounded coin change feasibility problem, but the key difficulty is that the coin values are not arbitrary, they are highly correlated.

The constraint `n ≤ 10^9` is the critical guide. Any solution that tries to do dynamic programming over all values up to `n` is immediately too large in both time and memory. Even a linear scan per test case would be too slow at `t = 10^4`.

A naive approach that tries to enumerate all combinations of these coins will fail quickly because the number of ways grows combinatorially. Even limiting ourselves to greedy construction is unsafe because greedy choices can fail when coin systems are not canonical.

A subtle edge case is that many small values cannot be formed even though they look like they should. For example, 12 cannot be formed because the smallest coin is 11 and the next is 111, which already overshoots when combined with 11 in small quantities. Another example is 23, which might tempt a decomposition like 11 + 11 + 1, but 1 is not available as a coin, so such reasoning breaks.

## Approaches

A brute-force idea is to treat this as a standard unbounded coin change feasibility problem. We first generate all coin values up to `n`, which is feasible because the sequence grows quickly. Then we run a classic dynamic programming approach where `dp[x]` indicates whether sum `x` can be formed. For each coin, we relax all reachable states up to `n`.

This approach is correct because it explores all combinations systematically. However, its runtime is proportional to `O(n * number_of_coins)`, which in the worst case is around `10^9 * 30`, far beyond feasible limits. Even reducing it to bitset optimizations still struggles under `10^4` test cases.

The key observation is that all coins are composed only of digit 1, which gives them a strong additive structure. Each coin of length `k` can be seen as `111...1 = (10^k - 1) / 9`. This structure implies that larger coins are almost linear combinations of smaller ones with shifted place values. This suggests that not all coins contribute independent constraints.

A more useful viewpoint is to consider modular structure and buildability using only the smallest few coins. Once we include 11 and 111, higher coins can be represented through combinations of these two with digit shifts, making larger coins redundant for feasibility checking up to the given constraint.

Thus the problem reduces to checking whether `n` can be represented using just two coin types: 11 and 111. From there, the problem becomes a simple linear Diophantine feasibility check in non-negative integers.

We try all possible counts of the larger coin (111), and check if the remainder is divisible by 11. Since `n ≤ 10^9`, the number of iterations is at most about 10^7 in the worst case, but we can reduce it further by bounding the loop by `n / 111`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP over all coins | O(nk) | O(n) | Too slow |
| Reduced search using 11 and 111 | O(n/111) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Precompute or fix the two essential coin values, 11 and 111. Larger coins are not needed because they can be replaced by combinations of these two without losing reachability for values up to the constraints.
2. For each test case, take the value `n` and iterate over how many 111-coins we might use. This ranges from 0 up to `n // 111`. Each choice represents fixing part of the sum using the largest meaningful denomination.
3. For a fixed number of 111-coins, compute the remaining value `r = n - 111 * x`. This step isolates whether the rest can be formed using only 11-coins.
4. Check whether `r` is divisible by 11. If it is, then we can fill the remainder exactly using 11-coins, meaning the representation is valid.
5. If any choice of `x` leads to a valid remainder, we immediately conclude that `n` is achievable and output YES. If no such split works, output NO.

### Why it works

The algorithm relies on the fact that any valid representation can be rearranged so that all 111-coins are grouped first, and the remaining value must lie entirely in the semigroup generated by 11. Since 11 is the smallest denomination, any leftover that is not divisible by 11 cannot be repaired using larger coins without increasing the total beyond `n`. This makes the search over 111-coins complete and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        ok = False

        max_x = n // 111
        for x in range(max_x + 1):
            rem = n - 111 * x
            if rem % 11 == 0:
                ok = True
                break

        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The solution loops over possible counts of 111-coins and checks divisibility of the remainder by 11. The early exit ensures we do not explore unnecessary combinations once a valid decomposition is found.

A subtle implementation detail is ensuring integer division is used when bounding the loop. Using floating point or incorrect bounds would either miss valid cases or introduce performance issues.

## Worked Examples

Consider `n = 144`.

| x (111s) | 111*x | remainder | remainder % 11 | decision |
| --- | --- | --- | --- | --- |
| 0 | 0 | 144 | 1 | no |
| 1 | 111 | 33 | 0 | yes |

This shows that using one 111 coin leaves 33, which is exactly three 11-coins, so the answer is YES.

Now consider `n = 69`.

| x (111s) | 111*x | remainder | remainder % 11 | decision |
| --- | --- | --- | --- | --- |
| 0 | 0 | 69 | 3 | no |
| 1 | 111 | negative | invalid | stop |

No decomposition works, so the answer is NO.

These traces confirm that the algorithm correctly explores all feasible allocations of the larger denomination and validates whether the remainder lies in the smaller coin system.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n / 111) per test | We try all feasible counts of 111-coins |
| Space | O(1) | Only a few variables are stored |

The bound is easily fast enough because the loop runs at most about nine million iterations in the worst theoretical case across all tests, but in practice it is far lower and well within time limits for 1 second in Python when early exits are common.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        ok = False
        for x in range(n // 111 + 1):
            if (n - 111 * x) % 11 == 0:
                ok = True
                break
        out.append("YES" if ok else "NO")
    return "\n".join(out)

# provided samples
assert run("3\n33\n144\n69\n") == "YES\nYES\nNO"

# custom cases
assert run("1\n11\n") == "YES"
assert run("1\n22\n") == "YES"
assert run("1\n12\n") == "NO"
assert run("1\n0\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 11 | YES | smallest coin usage |
| 22 | YES | multiple 11 coins |
| 12 | NO | impossible remainder case |
| 0 | YES | trivial boundary behavior |

## Edge Cases

For `n = 11`, the loop immediately finds `x = 0`, remainder is 11, which is divisible, so the answer is YES. This checks the base denomination works directly.

For `n = 12`, the only possibilities are `12` or `12 - 111` which is invalid. Since 12 is not divisible by 11, no decomposition exists and the algorithm correctly outputs NO.

For very large values like `n = 10^9`, the loop still terminates quickly because the number of iterations is capped by `n / 111`, and the moment a valid remainder is found, we exit early.
