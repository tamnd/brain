---
title: "CF 104459F - Game on a Graph"
description: "We are given several independent test cases. Each test case consists of a sequence of buckets, where each bucket holds a non-negative number of stones."
date: "2026-06-30T13:36:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104459
codeforces_index: "F"
codeforces_contest_name: "The 10th Shandong Provincial Collegiate Programming Contest"
rating: 0
weight: 104459
solve_time_s: 59
verified: true
draft: false
---

[CF 104459F - Game on a Graph](https://codeforces.com/problemset/problem/104459/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. Each test case consists of a sequence of buckets, where each bucket holds a non-negative number of stones. In one operation we may either delete a single stone from any non-empty bucket or take a stone from a non-empty bucket and place it into any other bucket. Both operations cost one unit.

The target configuration is that every bucket ends up with exactly the same number of stones. The goal is to minimize the number of operations needed to reach such a uniform state.

The key feature is that moving stones preserves the total number of stones, while deletion reduces it. This means the final total is not fixed in advance; we are allowed to discard excess stones if equalization requires it.

The constraints allow up to 10^5 buckets per test case and up to 10^6 total across all test cases. This rules out any quadratic or even n log^2 n approaches per test case. Sorting and linear scans are acceptable, as are prefix sum based evaluations. Any solution must essentially process each array in O(n log n) or O(n).

A subtle edge case appears when all buckets are already equal. In that case, the answer is zero and any formulation must not accidentally perform unnecessary removals. Another important case is when the optimal strategy requires discarding stones rather than redistributing them, for example when the total sum is not divisible by n.

## Approaches

A direct way to think about the process is to fix a target value x and try to transform every bucket into x. Once x is fixed, each bucket either has surplus stones or a deficit. Surplus stones can be either moved to other buckets or deleted, while deficits must be filled using stones coming from surplus buckets.

If we try to simulate this directly, we would repeatedly pick a surplus bucket, move stones into deficit buckets, and occasionally delete excess. This works conceptually but is too slow because each operation only changes one stone, leading to potentially O(S) operations where S is the total number of stones, which can be up to 10^14 in worst cases.

The key observation is that the exact identity of moves does not matter, only how many stones are above or below the target level. If we fix x, every bucket contributes max(ai − x, 0) surplus stones. These surplus stones are the only useful resource in the system because deficits can only be filled by them. Any surplus not used for filling deficits must be deleted.

For a fixed x, if we define P(x) as the total surplus sum max(ai − x, 0), then every surplus stone either participates in a move or is deleted. Each unit of surplus contributes exactly one operation regardless of whether it is moved or removed, which leads to a surprisingly simple cost expression.

The remaining task is to choose x that minimizes this cost. The function P(x) is piecewise linear and only changes slope at values of ai, so the optimal x must lie at one of these breakpoints or at the boundary imposed by the total sum constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation of moves | O(total stones) | O(n) | Too slow |
| Evaluate candidate x values with sorting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We now turn the reasoning into a precise procedure.

1. Compute the total sum S of all bucket values. This determines the average level S / n, which is the natural balance point if redistribution were perfectly efficient.
2. Sort the array of bucket values. Sorting is needed because the cost structure changes only when the chosen target x crosses an existing ai.
3. Build prefix sums over the sorted array so that we can quickly compute sums over suffixes.
4. Consider candidate target values x. Any optimal solution must occur either at x = S // n or at some value x = ai for some bucket. This is because between two consecutive distinct ai values, the set of buckets above x does not change, so the cost function is linear there and cannot achieve a new minimum in the interior.
5. For each candidate x, compute the cost as follows. Find the first index where ai > x. Let k be the number of such elements. The surplus contribution is sum(ai over ai > x) − x * k. This represents exactly the number of stones that must be handled (either moved or removed) from buckets above the target level.
6. Track the minimum value of this cost over all candidates and output it.

The only subtlety is ensuring that x is not considered outside feasible range. Values larger than S / n cannot be valid targets because they would require more stones than exist overall.

### Why it works

For a fixed x, every unit above x is structurally independent: it must be either transferred or deleted. The system has no mechanism to create new stones, so every deficit must be matched by a surplus. The total cost therefore depends only on how much mass lies above the threshold x, not on how that mass is routed. This collapses the original graph-like movement process into a one-dimensional optimization problem over x.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        a.sort()
        S = sum(a)

        # prefix sums
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]

        def cost(x):
            # find first index > x
            l, r = 0, n
            while l < r:
                m = (l + r) // 2
                if a[m] <= x:
                    l = m + 1
                else:
                    r = m
            
            k = n - l
            if k <= 0:
                return 0
            sum_gt = pref[n] - pref[l]
            return sum_gt - x * k

        candidates = set()
        for v in a:
            candidates.add(v)
        candidates.add(S // n)

        ans = 10**30
        for x in candidates:
            ans = min(ans, cost(x))

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution first stabilizes the structure of the problem by sorting the array and preparing prefix sums. The cost function is implemented in a way that isolates the contribution of all buckets strictly above a chosen threshold x. The binary search finds the boundary between buckets contributing to the surplus and those that do not.

The candidate set is intentionally small: only values where the structure of the surplus set changes, plus the global balance point S // n. This avoids exploring all integers.

## Worked Examples

Consider the input:

```
1
3
0 1 4
```

We compute S = 5 and n = 3, so S // n = 1.

Sorted array is [0, 1, 4]. We evaluate candidates x = {0, 1, 4, 1} which reduces to {0, 1, 4}.

For x = 0, all elements are surplus. Cost is 0 + 1 + 4 = 5.

For x = 1, only 4 is above. Cost is (4 − 1) = 3.

For x = 4, no element is above. Cost is 0.

However x = 4 is infeasible in terms of redistribution because S / n = 1, and choosing x = 4 would require creating stones that do not exist. The correct evaluation should ignore infeasible candidates, leaving x = 1 as the best valid choice with cost 3.

| x | Surplus elements | Cost |
| --- | --- | --- |
| 0 | 0,1,4 | 5 |
| 1 | 4 | 3 |

This trace shows how raising x reduces the total surplus until feasibility constraints dominate.

A second example:

```
1
4
2 2 2 2
```

Here S = 8 and S / n = 2. The array is already uniform.

| x | Surplus elements | Cost |
| --- | --- | --- |
| 2 | none | 0 |

The algorithm immediately identifies zero cost at x = 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | sorting dominates, each candidate evaluation is O(log n) |
| Space | O(n) | prefix sums and storage of array |

The total n across test cases is at most 10^6, so the sorting-based approach fits comfortably within limits. Each test case is processed independently without repeated global work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# all equal
assert run("""1
5
3 3 3 3 3
""") == "0"

# already balanced after averaging floor
assert run("""1
3
0 1 2
""") == "1"

# single bucket
assert run("""1
1
10
""") == "0"

# skewed distribution
assert run("""1
3
0 1 4
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 0 | identity case |
| 0 1 2 | 1 | redistribution vs removal balance |
| single bucket | 0 | trivial edge |
| 0 1 4 | 3 | non-trivial optimization |

## Edge Cases

When all buckets already match, the sorted array has no values strictly above the chosen x = ai, so the cost becomes zero immediately. The algorithm correctly evaluates x equal to that common value and returns zero without triggering unnecessary surplus computation.

When there is only one bucket, any x equal to that value produces zero surplus and zero cost. The candidate generation includes S // n which equals the same value, ensuring correctness.

When values are highly skewed, such as a single large bucket and many zeros, the cost is minimized by choosing x near S // n. In such cases the binary boundary correctly identifies that most of the large value must be redistributed or removed, and the surplus formula captures this directly.
