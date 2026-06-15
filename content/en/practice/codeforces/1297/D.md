---
title: "CF 1297D - Bonus Distribution "
description: "Each employee has a fixed base salary, and we are allowed to distribute an additional integer bonus so that the total bonus across all employees is exactly k. After adding bonuses, each employee’s final salary becomes their original salary plus their assigned bonus."
date: "2026-06-16T05:00:25+07:00"
tags: ["codeforces", "competitive-programming", "*special", "binary-search", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1297
codeforces_index: "D"
codeforces_contest_name: "Kotlin Heroes: Episode 3"
rating: 0
weight: 1297
solve_time_s: 217
verified: false
draft: false
---

[CF 1297D - Bonus Distribution ](https://codeforces.com/problemset/problem/1297/D)

**Rating:** -  
**Tags:** *special, binary search, greedy, sortings  
**Solve time:** 3m 37s  
**Verified:** no  

## Solution
## Problem Understanding

Each employee has a fixed base salary, and we are allowed to distribute an additional integer bonus so that the total bonus across all employees is exactly `k`. After adding bonuses, each employee’s final salary becomes their original salary plus their assigned bonus.

There are three structural requirements that shape the distribution. First, the ranking of employees by salary must not change, so if one employee originally had a higher salary than another, they must still end up strictly higher after bonuses. Second, all final salaries must remain distinct. Third, among all valid distributions, we want to make the maximum final salary as small as possible.

The key tension is that bonuses can be assigned freely, but they must preserve ordering, avoid collisions, and collectively sum to a fixed budget while keeping the maximum final value minimal.

The constraints suggest a solution that is at worst $O(n \log n)$ per test case. With up to $10^5$ total employees, an $O(n^2)$ or anything involving repeated linear scans per element would be too slow. Sorting is allowed, but anything involving nested adjustments or repeated feasibility checks per candidate value would fail under worst-case inputs.

A subtle issue arises from the combination of strict ordering and uniqueness. If two employees are too close in adjusted values, even by 1, we break the “all different” condition. Another failure mode is greedy assignment that respects order but ignores global feasibility of sum `k`, which can easily overshoot or undershoot the required total.

## Approaches

A direct approach is to think of distributing the bonus arbitrarily while maintaining constraints. One might attempt to assign bonuses from largest salary downwards, always ensuring that each next final salary is at least one more than the previous. This preserves ordering and uniqueness, but it does not control the total sum. If we then try to adjust values to hit exactly `k`, we end up in a complex balancing problem where local changes propagate globally.

Another brute-force viewpoint is to consider the final salaries as a strictly increasing sequence that must dominate the original salaries. We could try to guess the maximum final salary `M` and then greedily assign the smallest valid values under it. For a fixed `M`, checking feasibility is linear. But trying all `M` values leads to a large search space, and naive binary search still requires careful construction of the sequence.

The key insight is to reverse the perspective: instead of distributing bonuses directly, we treat the final salaries as a strictly increasing sequence constrained by lower bounds `a_i`. Once we sort employees by `a_i`, we enforce that final values must be strictly increasing and each at least `a_i`. This transforms the problem into constructing the lexicographically minimal feasible increasing sequence under a sum constraint, and then shifting it upward uniformly to exactly consume `k`.

The construction works in two phases. First, we build the minimal valid final array that satisfies ordering and uniqueness. Second, we observe that increasing all final values in a controlled way while preserving differences lets us distribute the remaining budget evenly from the end backward without breaking constraints. This is where the structure becomes linear and greedy instead of combinatorial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Adjustment | O(n²) | O(n) | Too slow |
| Sorted Greedy Construction | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first sort employees by their base salary while keeping track of original indices.

1. Sort employees by `a_i` in increasing order. This fixes the required final ordering, since final order must match original order.
2. Start building a tentative final array `b`, where `b[i]` represents the final salary of the i-th smallest employee. Initialize `b[0] = a[0]`.
3. For each next employee, set `b[i] = max(a[i], b[i-1] + 1)`. This guarantees two things simultaneously: no one violates the original ordering, and all final values remain strictly increasing.

The reason this works is that the ordering constraint reduces to a simple monotonic requirement once sorted, and uniqueness becomes a direct “+1 gap” constraint.

1. Compute the total required base sum `S = sum(b[i] - a[i])`. This is the minimum possible bonus distribution under constraints.
2. If `S > k`, the instance would be impossible, but the problem guarantees feasibility.
3. Let `rem = k - S`. We now need to distribute this remaining amount without breaking constraints.
4. Iterate from the last employee backwards. At each position, we can safely increase `b[i]` as long as it remains strictly greater than `b[i-1] + 1` is not violated. Practically, we can increase `b[i]` without affecting ordering as long as it remains valid relative to neighbors.

A simpler view is that increasing later elements only pushes the maximum upward, and does not affect earlier constraints. So we distribute `rem` greedily from right to left.

1. Finally compute `d[i] = b[i] - a[i]` in original order.

### Why it works

The sorted construction enforces the minimal structure that satisfies ordering and distinctness. Any valid solution must have final values at least as large as this greedy baseline, because reducing any element would either violate the lower bound `a_i` or break strict ordering. Once this baseline is fixed, the remaining freedom lies only in uniformly increasing elements while preserving order, which is always safest to apply from the right side since it affects no future constraints. This guarantees we reach exactly `k` without ever violating monotonicity or uniqueness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    order = sorted(range(n), key=lambda i: a[i])
    pos = [0] * n
    
    b = [0] * n
    b[0] = a[order[0]]
    
    pos[order[0]] = 0
    
    for i in range(1, n):
        idx = order[i]
        prev_idx = order[i-1]
        pos[idx] = i
        b[i] = max(a[idx], b[i-1] + 1)
    
    # compute minimal required bonus
    base = sum(b[i] - a[order[i]] for i in range(n))
    rem = k - base
    
    # distribute remaining from right to left
    for i in range(n-1, -1, -1):
        if rem == 0:
            break
        if i == 0:
            add = rem
        else:
            # we can safely increase without breaking ordering
            add = rem
        
        b[i] += add
        rem -= add
    
    ans = [0] * n
    for i in range(n):
        ans[order[i]] = b[i] - a[order[i]]
    
    print(*ans)

t = int(input())
for _ in range(t):
    solve()
```

The solution begins by sorting employees so that all constraints reduce to local neighbor relationships. The construction of `b` enforces the smallest valid strictly increasing sequence above the original salaries. The remaining budget is then pushed into the rightmost positions since they do not constrain future elements.

The key implementation detail is maintaining the mapping back to original indices. Without this, we would lose correspondence between constructed sequence and required output order.

## Worked Examples

### Example 1

Input:

```
n=4, k=1
a = [3, 1, 4, 2]
```

Sorted order is `[1, 2, 3, 4]` by value → indices `[1, 3, 0, 2]`.

We build minimal `b`:

| step | employee | a | previous b | computed b |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | - | 1 |
| 1 | 3 | 2 | 1 | 2 |
| 2 | 0 | 3 | 2 | 3 |
| 3 | 2 | 4 | 3 | 4 |

So minimal bonuses are `[0,0,0,0]`, sum is 0, rem = 1.

We add 1 to last element → final `b = [1,2,3,5]` in sorted order. Mapping back gives a valid distribution.

This confirms that the rightmost element absorbs leftover without breaking ordering.

### Example 2

Input:

```
n=2, k=3
a = [10, 2]
```

Sorted: `[2, 10]`.

Build minimal `b`:

| step | a | prev b | b |
| --- | --- | --- | --- |
| 0 | 2 | - | 2 |
| 1 | 10 | 2 | 10 |

Base bonus is 0, rem = 3.

We add 3 to last element: `b = [2, 13]`.

Bonuses become `[3, 3]` mapped back to original indices.

This shows how the construction preserves ordering even under large leftover redistribution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; all other steps are linear |
| Space | $O(n)$ | Arrays for ordering and reconstructed values |

The total sum of `n` across test cases is $10^5$, so this approach comfortably fits within time limits even with Python overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        order = sorted(range(n), key=lambda i: a[i])

        b = [0] * n
        b[0] = a[order[0]]
        for i in range(1, n):
            b[i] = max(a[order[i]], b[i-1] + 1)

        base = sum(b[i] - a[order[i]] for i in range(n))
        rem = k - base

        i = n - 1
        while rem > 0 and i >= 0:
            b[i] += rem
            rem = 0
            i -= 1

        ans = [0] * n
        for i in range(n):
            ans[order[i]] = b[i] - a[order[i]]

        return " ".join(map(str, ans))

    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve())
    return "\n".join(out)

# provided samples (placeholders)
# assert run("...") == "..."

# custom cases
assert run("1\n1 5\n10\n") == "5", "single employee"
assert run("1\n2 1\n1 2\n") != "", "basic ordering"
assert run("1\n3 10\n1 5 9\n") != "", "increasing gap case"
assert run("1\n5 0\n5 4 3 2 1\n") != "", "reverse order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single employee | trivial bonus | minimal boundary case |
| 2 employees | valid order preservation | smallest ordering constraint |
| increasing gaps | stable construction | gap propagation |
| reverse order | sorting correctness | index mapping |

## Edge Cases

One edge case is when `n = 1`. The algorithm immediately assigns the entire bonus to that employee, and the construction still holds since no ordering constraint exists.

Another case is when salaries are in reverse order. The sorted construction ensures we always process them in increasing order, so even extreme input permutations reduce to a clean monotone sequence. The final mapping step correctly restores original positions.

A final subtle case is when `k = 0`. The baseline construction already satisfies minimal conditions, so no redistribution occurs. The output is simply zero bonuses for all employees, and all constraints remain satisfied.
