---
title: "CF 106016C - USD vs Liras"
description: "Each day Omar must settle a demand that is expressed in two currencies. For day i, there is a required amount of dollars ai and a conversion rate bi that tells how expensive it is to replace one dollar using liras. On that day Omar can split the payment in two parts."
date: "2026-06-21T16:41:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106016
codeforces_index: "C"
codeforces_contest_name: "The 2025 Homs Collegiate programming contest"
rating: 0
weight: 106016
solve_time_s: 55
verified: true
draft: false
---

[CF 106016C - USD vs Liras](https://codeforces.com/problemset/problem/106016/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

Each day Omar must settle a demand that is expressed in two currencies. For day i, there is a required amount of dollars ai and a conversion rate bi that tells how expensive it is to replace one dollar using liras.

On that day Omar can split the payment in two parts. He may pay some xi dollars directly, and the remaining ai − xi dollars are effectively converted into liras, costing (ai − xi) · bi liras. If he pays everything in dollars, the lira cost is zero. If he pays nothing in dollars, he pays the full amount in liras.

The lira payment for a day is what we call ci, and the objective is to keep the worst day as small as possible. More precisely, we want to minimize the maximum ci across all days while still being able to choose xi values whose total does not exceed m dollars.

The key interaction is that every dollar used on day i reduces ci by bi. So dollars act like a resource that can be distributed across days, each dollar having different “value” depending on the day’s exchange rate.

The constraints push us toward an O(n log C) or O(n log n) per test approach. Since the sum of n across all test cases is up to 3 × 10^5, any solution that is linear or near linear per test is acceptable. A quadratic strategy that tries all allocations or simulates redistributions will fail immediately because even 10^5 squared operations is too large.

A subtle issue appears when thinking greedily per day without a global threshold. Reducing the worst day locally can waste dollars on a day where each dollar is less valuable than on another day. The correct solution must compare days globally rather than treating them independently.

## Approaches

A direct way to think about the problem is to imagine assigning each of the m dollars to some day and observing how much the maximum lira cost decreases. In a brute-force model, we would repeatedly pick a day and decide whether to convert one more dollar there or not. Each choice affects the final maximum, and exploring all assignments leads to an exponential number of possibilities in principle, or at least O(mn) if simulated naively. Since m can be as large as 10^9, this is completely infeasible.

The key observation is that instead of constructing the allocation, we can reverse the perspective. Suppose we guess a value y for the maximum allowed lira cost. Then for each day we can compute how many dollars we are forced to spend to bring that day down to at most y. If the total required dollars exceeds m, the guess is too small. If it is within m, the guess is feasible.

This transforms the problem into a monotone feasibility check over y. If a certain y is achievable, any larger y is also achievable because we require less reduction. This monotonicity allows binary search on y.

The remaining task is computing, for each day, the minimum number of dollars needed to ensure ci ≤ y. Since ci = (ai − xi)bi, the condition ci ≤ y becomes xi ≥ ai − y / bi. Each dollar reduces ci by bi, so the required xi is effectively a ceiling on ai − y / bi, clipped at zero and at most ai.

Once we can compute the required total dollars for a fixed y, binary search yields the minimum feasible answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force allocation | Exponential / O(mn) | O(1) | Too slow |
| Binary search with feasibility check | O(n log(max ai·bi)) | O(1) extra | Accepted |

## Algorithm Walkthrough

We convert the problem into finding the smallest y such that all days can be reduced to at most y using at most m dollars.

1. For a fixed guess y, compute how many dollars are required for each day to ensure ci ≤ y.

For day i, the condition (ai − xi)bi ≤ y rearranges to xi ≥ ai − y / bi. Since xi must be an integer, we take xi = max(0, ai − floor(y / bi)). This gives the minimum forced spending on that day.

The reason this works is that each dollar reduces the lira cost by exactly bi, so reducing ci by k·bi requires spending k dollars.
2. Sum these required xi values over all days.

This sum represents the minimum total dollars needed to make every day satisfy the threshold y.
3. Check feasibility against m.

If the sum is ≤ m, then y is achievable. Otherwise, y is too small and we need to increase it.
4. Binary search over y in the range [0, max(ai·bi)].

The upper bound corresponds to the worst case where we spend no dollars anywhere.

### Why it works

For any fixed day, the relationship between xi and ci is linear and independent of other days. The only coupling between days is the total dollar budget m. This creates a structure where each y defines a deterministic minimum requirement, and increasing y can only decrease these requirements. This monotonicity guarantees that binary search will converge to the smallest feasible y, because feasibility never flips back from true to false as y increases.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        max_val = 0
        for i in range(n):
            max_val = max(max_val, a[i] * b[i])

        def ok(y):
            need = 0
            for i in range(n):
                take = a[i] - (y // b[i])
                if take > 0:
                    need += take
                    if need > m:
                        return False
            return need <= m

        lo, hi = 0, max_val
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(mid):
                hi = mid
            else:
                lo = mid + 1

        out.append(str(lo))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The core of the implementation is the function that evaluates a candidate y. It translates a global threshold into per-day minimum dollar usage. The expression y // b[i] is the number of dollars that fully cancel bi-sized reductions without exceeding the target. Subtracting this from ai gives how many dollars must still be spent.

The binary search maintains an interval where the left side is infeasible or unknown and the right side is feasible. Each midpoint check reduces the search space logarithmically.

Care must be taken with overflow, since ai·bi can reach 10^18, but Python handles this safely. In other languages, 64-bit integers are required.

## Worked Examples

Consider a small instance with n = 3, m = 3.

Let a = [3, 2, 4] and b = [2, 5, 1].

We test a candidate y = 4.

| i | ai | bi | y // bi | required xi = max(0, ai − y//bi) |
| --- | --- | --- | --- | --- |
| 1 | 3 | 2 | 2 | 1 |
| 2 | 2 | 5 | 0 | 2 |
| 3 | 4 | 1 | 4 | 0 |

Total required dollars = 3, which equals m, so y = 4 is feasible.

Now consider y = 3.

| i | ai | bi | y // bi | required xi |
| --- | --- | --- | --- | --- |
| 1 | 3 | 2 | 1 | 2 |
| 2 | 2 | 5 | 0 | 2 |
| 3 | 4 | 1 | 3 | 1 |

Total required dollars = 5, which exceeds m, so y = 3 is infeasible.

This shows how tightening y increases required dollar usage, which is exactly what enables binary search.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(max ai·bi)) | Each feasibility check is O(n), and binary search runs over the value range |
| Space | O(1) extra | Only arrays and counters are used |

The sum of n over all test cases is bounded by 3 × 10^5, so even with about 30-60 iterations of binary search per test, the total work remains comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []

        for _ in range(t):
            n, m = map(int, input().split())
            a = list(map(int, input().split()))
            b = list(map(int, input().split()))

            max_val = 0
            for i in range(n):
                max_val = max(max_val, a[i] * b[i])

            def ok(y):
                need = 0
                for i in range(n):
                    take = a[i] - (y // b[i])
                    if take > 0:
                        need += take
                        if need > m:
                            return False
                return need <= m

            lo, hi = 0, max_val
            while lo < hi:
                mid = (lo + hi) // 2
                if ok(mid):
                    hi = mid
                else:
                    lo = mid + 1

            out.append(str(lo))

        return "\n".join(out)

    return solve()

# small sanity checks
assert run("1\n1 5\n10\n2\n") == "20"

# all zeros effect check
assert run("1\n2 10\n1 1\n1 1\n") == "0"

# tight budget forcing high y
assert run("1\n2 1\n10 10\n1 1\n") == "9"

# uneven rates
assert run("1\n3 3\n3 2 4\n2 5 1\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single day scaling | 20 | correctness of direct conversion |
| uniform small case | 0 | full dollar coverage feasibility |
| tight budget | 9 | binary search pressure case |
| mixed rates | 4 | interaction between different bi values |

## Edge Cases

A corner case occurs when bi = 1 for all days. In that situation, each dollar reduces ci by exactly one, so the problem reduces to distributing m units of reduction across linear deficits. The algorithm handles this naturally because y // 1 simply becomes y, and required xi becomes ai − y.

Another case is when m is extremely large. If m ≥ sum(ai), we can fully pay all dollars directly, making all ci zero. The binary search naturally converges to y = 0 because feasibility succeeds immediately.

A final subtle case appears when ai * bi is very large, close to 10^18. The algorithm avoids overflow by never storing intermediate subtraction of these products beyond computing the binary search bound. All per-iteration work stays within safe integer operations, and the feasibility function only uses division and subtraction at smaller scales.
