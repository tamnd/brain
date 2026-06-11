---
title: "CF 1352B - Same Parity Summands"
description: "We are asked to split a given integer n into exactly k positive integers such that all of them share the same parity. That means we must choose a sequence of length k where every element is either odd or even, and their sum equals n."
date: "2026-06-11T14:11:13+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1352
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 640 (Div. 4)"
rating: 1200
weight: 1352
solve_time_s: 152
verified: false
draft: false
---

[CF 1352B - Same Parity Summands](https://codeforces.com/problemset/problem/1352/B)

**Rating:** 1200  
**Tags:** constructive algorithms, math  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to split a given integer `n` into exactly `k` positive integers such that all of them share the same parity. That means we must choose a sequence of length `k` where every element is either odd or even, and their sum equals `n`.

The structure of the output is not just a feasibility check. If such a decomposition exists, we must explicitly construct one valid sequence. If it does not exist, we must report failure.

The constraints make the problem very tight in structure. The number of test cases is up to 1000, but each test is independent. The values of `n` can go up to 10^9, while `k` is small, at most 100. This combination suggests that any solution should run in constant time per test case, since even O(k) per test is trivial, but anything depending on `n` would be too slow.

The main difficulty is not computation but parity consistency under positivity constraints. A naive attempt might try to assign numbers greedily without checking whether the parity requirement can still be satisfied at the end. That fails in cases like `n = 8, k = 3`, where choosing all ones immediately seems plausible but forces a sum of 3, leaving no room to reach 8 with fixed parity.

Another subtle failure case arises when mixing parity implicitly. For example, distributing `n` into mostly ones and adjusting the last element often breaks parity consistency or positivity.

The real constraint hidden in the problem is that once parity is fixed, each element has a minimum value: the smallest odd is 1, and the smallest even is 2. That lower bound determines feasibility immediately.

## Approaches

A brute-force idea would be to try all ways of choosing `k` positive integers that sum to `n`, then filter those whose elements share the same parity. This is combinatorially enormous, since the number of compositions of `n` into `k` parts grows exponentially in `n`. Even ignoring parity, this is roughly C(n-1, k-1), which is completely infeasible.

The structure simplifies once we stop thinking in terms of arbitrary partitions and instead fix parity first. If all numbers are odd, each contributes at least 1, so the minimum possible sum is `k`. If all numbers are even, each contributes at least 2, so the minimum possible sum is `2k`. These two baselines fully determine feasibility.

After fixing parity, the remaining task becomes distributing the leftover sum while preserving parity. If we pick all ones (odd case), the leftover is `n - k`, which must be even so that we can add even increments without changing parity. Similarly, if we pick all twos (even case), the leftover is `n - 2k`, which must also be even.

This reduces the problem to checking at most two candidate constructions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(k) | Too slow |
| Parity Construction | O(k) per test | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. First, check if an all-odd construction is possible. We need at least `k` total sum because each odd number is at least 1. This gives the condition `n >= k`. If this fails, odd construction is impossible.
2. If `n >= k`, compute the remaining value `rem = n - k`. We want to distribute this among `k` numbers while keeping them odd. Adding 2 to any element preserves odd parity, so we require `rem` to be even. If `rem % 2 == 0`, we can construct a valid solution by starting with all ones and distributing `rem` as 2s.
3. If the odd construction fails, try the even construction. Each number must be at least 2, so we need `n >= 2k`. If this fails, no even construction is possible.
4. If `n >= 2k`, compute `rem = n - 2k`. We distribute this by adding multiples of 2 to base twos, so we again require `rem % 2 == 0`.
5. If neither construction works, output NO.
6. When a construction is valid, fill an array with either all 1s or all 2s, then distribute the remaining sum into the last element to keep implementation simple and avoid tracking multiple updates.

### Why it works

Once parity is fixed, the entire problem reduces to choosing a base vector of identical valid parity elements and then adding an even adjustment to some entries. The invariant is that every operation we apply changes values by multiples of 2, so parity never changes. The only global constraint is meeting the sum, and the feasibility reduces to whether the leftover after assigning minimum values is even. Since we only consider two parity classes, we cover all possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(n, k):
    if n >= k and (n - k) % 2 == 0:
        res = [1] * k
        res[-1] += n - k
        return True, res

    if n >= 2 * k and (n - 2 * k) % 2 == 0:
        res = [2] * k
        res[-1] += n - 2 * k
        return True, res

    return False, []

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    ok, ans = solve(n, k)
    if not ok:
        print("NO")
    else:
        print("YES")
        print(*ans)
```

The code directly implements the two construction attempts described earlier. The first branch builds an all-ones vector and adjusts the last element. This preserves odd parity because adding an even number does not change parity.

The second branch does the same starting from all twos. This ensures all numbers remain even.

Adjusting only the last element avoids bookkeeping complexity while preserving correctness, since only the sum matters.

## Worked Examples

### Example 1: `n = 10, k = 3`

We try odd construction first.

| Step | Base Value | Sum | Remaining | Condition |
| --- | --- | --- | --- | --- |
| Init | [1,1,1] | 3 | 7 | n ≥ k |
| Check | 7 % 2 = 1 | - | - | fails |

Odd construction fails.

Even construction:

| Step | Base Value | Sum | Remaining | Condition |
| --- | --- | --- | --- | --- |
| Init | [2,2,2] | 6 | 4 | n ≥ 2k |
| Adjust | [2,2,6] | 10 | 0 | valid |

Output is valid.

This demonstrates how parity choice determines feasibility and how leftover adjustment completes the sum.

### Example 2: `n = 8, k = 7`

Try odd construction:

| Step | Base Value | Sum | Remaining | Condition |
| --- | --- | --- | --- | --- |
| Init | [1 x 7] | 7 | 1 | n ≥ k |
| Check | 1 % 2 = 1 | - | - | fail |

Even construction:

| Step | Base Value | Sum | Remaining | Condition |
| --- | --- | --- | --- | --- |
| Check | n < 2k | - | - | impossible |

No valid construction exists.

This shows a tight case where there is barely enough sum for odd values but parity prevents adjustment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) per test | constructing and printing k numbers |
| Space | O(k) | storing output array |

Since `k ≤ 100` and `t ≤ 1000`, the total work is at most 10^5 operations, easily within limits. The algorithm avoids any dependence on `n`, which is crucial given `n` can be as large as 10^9.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())

        def solve(n, k):
            if n >= k and (n - k) % 2 == 0:
                res = [1] * k
                res[-1] += n - k
                return True, res
            if n >= 2 * k and (n - 2 * k) % 2 == 0:
                res = [2] * k
                res[-1] += n - 2 * k
                return True, res
            return False, []

        ok, ans = solve(n, k)
        if not ok:
            out.append("NO")
        else:
            out.append("YES")
            out.append(" ".join(map(str, ans)))

    return "\n".join(out)

# provided samples
assert "YES" in run("1\n10 3\n")
assert run("1\n8 7\n") == "NO"

# custom cases
assert "NO" in run("1\n2 3\n"), "too small"
assert "YES" in run("1\n9 3\n"), "odd split"
assert "YES" in run("1\n20 5\n"), "even split"
assert "NO" in run("1\n1 2\n"), "impossible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 3 | NO | insufficient sum for any parity |
| 9 3 | YES | odd construction works |
| 20 5 | YES | even construction works |
| 1 2 | NO | smallest impossible case |

## Edge Cases

A key edge case is when `n` is just slightly larger than `k`. For example, `n = 9, k = 8`. The odd construction would start with eight ones summing to 8, leaving 1. Since the leftover is odd, we cannot distribute it without breaking parity. The algorithm correctly rejects this.

Another edge case is when `n` is exactly `2k`. Here the even construction produces all twos with no adjustment needed. The algorithm returns immediately with a valid solution.

A third edge case is when `k = 1`. Any positive integer works because a single number trivially satisfies parity constraints. The algorithm handles this since both constructions reduce to returning `[n]` in the odd branch when `n >= 1`.
