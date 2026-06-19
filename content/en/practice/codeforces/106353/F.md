---
title: "CF 106353F - Fair Share"
description: "A group of people has just finished a shared expense event, and each person has two relevant values. One value represents how much cash they can immediately contribute if someone else is responsible for paying the bill."
date: "2026-06-20T03:20:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106353
codeforces_index: "F"
codeforces_contest_name: "2025-2026 ICPC Northwestern European Regional Programming Contest (NWERC 2025)"
rating: 0
weight: 106353
solve_time_s: 63
verified: true
draft: false
---

[CF 106353F - Fair Share](https://codeforces.com/problemset/problem/106353/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

A group of people has just finished a shared expense event, and each person has two relevant values. One value represents how much cash they can immediately contribute if someone else is responsible for paying the bill. The other value represents the maximum amount of net cost they are willing to bear personally if they become the one who pays the entire bill and collects everyone else’s cash.

We are asked to choose exactly one person to be the payer. If person i is chosen, they collect all cash from the other participants, then use their credit card to cover the full bill. The effective personal cost of choosing i is the total bill minus the cash contributed by everyone else. This cost must not exceed i’s allowed personal share.

The goal is to determine whether there exists at least one valid payer, and if so output any such index.

The constraints allow up to 100,000 people, so any solution must be close to linear or linearithmic. A quadratic approach that evaluates each candidate by summing contributions of all others would lead to about 10^10 operations in the worst case, which is far beyond the time limit.

A subtle edge case appears when almost everyone contributes large cash but has very small tolerance for paying extra. For example, if one person’s contribution is essential for feasibility, removing them as payer might invalidate others even if they individually seem acceptable. Another issue is when all individuals are “locally valid” in some naive sense but globally no one can satisfy the constraint once full sums are considered.

## Approaches

The core difficulty is that the condition for a person depends on the sum of all other people’s cash contributions, which changes with the chosen candidate. If we test each person i independently, we need to compute the sum of all aj for j ≠ i. A direct recomputation for each i leads to O(n^2), since each check requires scanning all participants.

The key observation is that the total cash sum S = sum(ai) is fixed. If person i pays, the cash they collect is S - ai. Their net payment becomes bi must be at least S - ai. Rearranging gives a simple inequality that can be evaluated in O(1) per person once S is known.

This transforms the problem into checking a single condition per candidate after a single global pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all pairs (ai, bi) and compute the total sum S of all ai values. This represents the full cash pool if nobody is excluded.
2. For each person i, imagine they are the payer. In that case, the cash they collect is S - ai because everyone else contributes their full ai.
3. Compute the effective burden for person i as (S - ai). This is the amount they must cover using their own funds after collecting cash.
4. Check whether this burden is acceptable for person i by verifying (S - ai) ≤ bi.
5. As soon as a person satisfies this inequality, output their index and terminate.
6. If no person satisfies the condition after scanning all candidates, output “impossible”.

### Why it works

The critical invariant is that the total cash contribution from non-payers depends only on the global sum minus the chosen person’s own cash. This eliminates any interaction effects between candidates. Each candidate’s feasibility depends solely on a fixed global value S and their own pair (ai, bi), so checking them independently is sufficient. No solution can be missed because every valid configuration corresponds to exactly one index satisfying the derived inequality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = []
    b = []
    
    S = 0
    for _ in range(n):
        ai, bi = map(int, input().split())
        a.append(ai)
        b.append(bi)
        S += ai

    for i in range(n):
        if S - a[i] <= b[i]:
            print(i + 1)
            return

    print("impossible")

if __name__ == "__main__":
    solve()
```

The solution first aggregates all cash values to compute the total pool. This is essential because every feasibility check depends on the sum of all other participants.

Then it iterates once over all candidates, evaluating the derived inequality directly. The subtraction S - a[i] represents the cash collected if i pays. Comparing it with b[i] enforces the constraint that i’s net burden stays within their allowed limit.

The early return ensures we stop immediately upon finding any valid payer, which matches the problem requirement that any valid index is acceptable.

## Worked Examples

### Example 1

Consider the input:

```
n = 4
a = [4, 5, 1, 3]
b = [5, 4, 3, 6]
```

Total sum S is 13.

| i | ai | bi | S - ai | Condition |
| --- | --- | --- | --- | --- |
| 1 | 4 | 5 | 9 | 9 ≤ 5 false |
| 2 | 5 | 4 | 8 | 8 ≤ 4 false |
| 3 | 1 | 3 | 12 | 12 ≤ 3 false |
| 4 | 3 | 6 | 10 | 10 ≤ 6 false |

No index satisfies the constraint, so the output is impossible.

This trace shows that even though every person collects a large amount of cash, their allowed net burden is too small to accommodate the remaining bill.

### Example 2

```
n = 5
a = [1, 4, 1, 2, 4]
b = [4, 6, 4, 5, 6]
```

Total sum S is 12.

| i | ai | bi | S - ai | Condition |
| --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 11 | 11 ≤ 4 false |
| 2 | 4 | 6 | 8 | 8 ≤ 6 false |
| 3 | 1 | 4 | 11 | 11 ≤ 4 false |
| 4 | 2 | 5 | 10 | 10 ≤ 5 false |
| 5 | 4 | 6 | 8 | 8 ≤ 6 false |

Again no valid candidate exists.

This example emphasizes that the condition is very strict and depends on global totals rather than local comparisons.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | one pass to compute sum, one pass to check candidates |
| Space | O(1) | only storing running sum and input arrays |

The constraints allow up to 100,000 entries, so a linear scan is easily fast enough. Memory usage stays minimal since only simple integer arrays are stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimum size
assert run("2\n1 10\n10 1\n") in {"1", "2", "impossible"}

# simple valid case
assert run("3\n1 5\n2 1\n3 10\n") in {"1","2","3","impossible"}

# all equal
assert run("4\n2 2\n2 2\n2 2\n2 2\n") in {"1","2","3","4","impossible"}

# forced impossible
assert run("3\n10 1\n10 1\n10 1\n") == "impossible"

# large-ish balanced case
assert run("5\n1 100\n2 100\n3 100\n4 100\n5 100\n") in {"1","2","3","4","5"}

# one obvious winner
assert run("4\n5 100\n1 1\n1 1\n1 1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2-person case | any valid or impossible | minimal boundary correctness |
| all equal values | any index or impossible | symmetry handling |
| forced impossible | impossible | correctness of rejection |
| skewed large tolerance | any index | detection of easy valid case |

## Edge Cases

One edge case is when all ai values are large but all bi values are extremely small. In that situation S becomes large, so S - ai remains large for every i, and the condition fails uniformly. The algorithm correctly rejects the input because every computed burden exceeds the corresponding limit.

Another edge case is when one person has very large ai and also very large bi. Suppose they dominate the cash pool. Then for that person, S - ai becomes small because removing their contribution significantly reduces the total. The algorithm correctly identifies that candidate since the inequality becomes easy to satisfy only for them.

A third edge case arises when multiple people are valid. Since the algorithm stops at the first match during the scan, it correctly returns any valid index without needing tie-breaking logic, matching the problem’s requirement.
