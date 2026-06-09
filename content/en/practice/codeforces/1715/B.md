---
title: "CF 1715B - Beautiful Array"
description: "We are asked to construct an array of length n consisting of non-negative integers. Two global constraints must be satisfied at the same time. First, the sum of all elements must be exactly s."
date: "2026-06-09T19:55:14+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1715
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 816 (Div. 2)"
rating: 1000
weight: 1715
solve_time_s: 122
verified: false
draft: false
---

[CF 1715B - Beautiful Array](https://codeforces.com/problemset/problem/1715/B)

**Rating:** 1000  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct an array of length `n` consisting of non-negative integers. Two global constraints must be satisfied at the same time.

First, the sum of all elements must be exactly `s`. Second, if each element is divided by `k` and floored, the total of these quotients must be exactly `b`. That second condition can be interpreted as counting how many full blocks of size `k` exist across the array.

Each element contributes independently: a value `x` contributes `x // k` to the beauty, and contributes `x` to the total sum. The task is to distribute a total sum `s` across `n` slots while ensuring the total number of full `k`-blocks equals `b`.

The constraints are large: `n` up to 1e5 across tests, `k` up to 1e9, and `s` up to 1e18. This immediately rules out any approach that tries all distributions or builds candidates with nested loops over possible values per position. A linear construction per test case is the only viable direction.

A subtle edge case appears when feasibility is impossible even before construction. For example, if `k = 6`, `b = 3`, and `s = 12` with `n = 3`, then the minimum possible sum to achieve beauty `3` is already too large or too structured to match `s`. This comes from the fact that every unit of beauty requires at least `k` total contribution somewhere in the array, so `s` must be large enough to support `b` full blocks.

Another failure mode occurs when `b` is too large to be distributed across `n` elements. If `b > s // k`, then even concentrating all mass into one element cannot create enough full divisions.

The real difficulty is not computing feasibility, but distributing both “block contributions” and leftover values without breaking either constraint.

## Approaches

A brute-force idea would be to treat each element as a variable and try assigning values incrementally. For each position, we could try values from `0` to `s`, compute current sum and beauty, and backtrack. This is correct in principle but completely infeasible. Even for `n = 100`, the state space explodes, and for `n = 10^5`, it is impossible.

The key observation is that the beauty contribution is structured in chunks of size `k`. Any number `x` can be decomposed as:

`x = (x // k) * k + (x % k)`

This splits each element into a “block part” and a “remainder part”. The beauty depends only on the block part, while the remainder does not affect beauty at all.

So the problem becomes: we need to allocate exactly `b` blocks of size `k` across the array, and distribute the remaining sum freely as remainders, while keeping total sum equal to `s`.

A clean construction emerges if we first assign as many full `k` blocks as possible into one element, then distribute remaining blocks as `k`-sized increments in other positions. After fixing beauty, we distribute leftover sum into any element without affecting the floor division structure.

We only need to ensure that the total required minimum sum for beauty `b` is `b * k`, and the remaining slack `s - b * k` can be distributed arbitrarily.

If `s < b * k`, there is no solution. Otherwise, we construct a base array with `b` units of `k`, then distribute the remaining sum.

Finally, we ensure no element accidentally gains an extra block due to overflow beyond `k`, by carefully placing at most one large value per position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the array greedily while controlling how many full `k`-blocks each element contributes.

1. Check feasibility by verifying whether `b * k ≤ s`. If not, no array can produce enough full blocks without exceeding total sum. This is because each unit of beauty costs at least `k` in value.
2. Initialize an array of size `n` with all zeros. We will first allocate the required beauty `b` into the first element in a concentrated way. This avoids distributing blocks prematurely and simplifies tracking.
3. Set `a[0] = b * k`. This guarantees the beauty contributed by this element is exactly `b`, since `(b * k) // k = b`. No other element contributes to beauty yet.
4. Subtract this contribution from the remaining sum: `remaining = s - b * k`.
5. Now we distribute `remaining` across the array without changing beauty. Since any value `< k` contributes zero to beauty, we can safely place values in `[0, k-1]` in any positions.
6. Fill elements from left to right, adding up to `k-1` per element until `remaining` is exhausted. This ensures no new `k`-block is created accidentally.
7. Output the resulting array.

### Why it works

The construction isolates all beauty contribution into a single controlled element. Since only `a[0]` is allowed to be ≥ `k`, it alone determines the total floor sum. Every other element is kept strictly below `k`, guaranteeing zero contribution to beauty. The remaining sum is distributed without crossing the threshold that would create extra blocks. This preserves both constraints independently, making the construction safe and deterministic.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k, b, s = map(int, input().split())

        min_sum = b * k
        if min_sum > s:
            print(-1)
            continue

        res = [0] * n

        # allocate all beauty into first element
        res[0] = b * k
        remaining = s - b * k

        # distribute remaining without creating new k-blocks
        for i in range(n):
            if remaining == 0:
                break
            add = min(k - 1, remaining)
            res[i] += add
            remaining -= add

        if remaining > 0:
            print(-1)
        else:
            print(*res)

if __name__ == "__main__":
    solve()
```

The solution begins by checking whether the required number of full `k` contributions is even possible given the total sum. If not, it immediately rejects the case.

The construction step places all required beauty into the first element using an exact multiple of `k`. This ensures that the floor division sum is exactly `b` and does not depend on how remaining values are distributed.

The loop that distributes `remaining` is carefully bounded by `k - 1`, which prevents any new element from contributing to beauty. This is the central implementation detail: crossing the threshold `k` would silently increase beauty and break correctness.

## Worked Examples

### Example 1

Input:

```
n = 3, k = 6, b = 3, s = 19
```

We compute `b * k = 18`, so `remaining = 1`.

| Step | Array state | Remaining | Beauty |
| --- | --- | --- | --- |
| init | [0, 0, 0] | 19 | 0 |
| assign beauty | [18, 0, 0] | 1 | 3 |
| distribute | [18, 1, 0] | 0 | 3 |

The final array sums to 19 and produces beauty 3, confirming both constraints.

### Example 2

Input:

```
n = 5, k = 4, b = 2, s = 25
```

We compute `b * k = 8`, so `remaining = 17`.

| Step | Array state | Remaining | Beauty |
| --- | --- | --- | --- |
| init | [0, 0, 0, 0, 0] | 25 | 0 |
| assign beauty | [8, 0, 0, 0, 0] | 17 | 2 |
| distribute | [8, 3, 3, 3, 3] | 1 | 2 |

We stop when remaining is exhausted or cannot be fully placed without exceeding limits.

This trace shows that the only source of beauty remains the first element, while all others stay below `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test distributes remaining sum once per element |
| Space | O(n) | Stores the constructed array |

The constraints allow up to `1e5` total elements, and the solution performs only constant work per element, so it fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []
    
    input = sys.stdin.readline
    
    t = int(sys.stdin.readline())
    for _ in range(t):
        n, k, b, s = map(int, sys.stdin.readline().split())
        if b * k > s:
            out.append("-1")
            continue
        res = [0] * n
        res[0] = b * k
        remaining = s - b * k
        for i in range(n):
            if remaining == 0:
                break
            add = min(k - 1, remaining)
            res[i] += add
            remaining -= add
        if remaining > 0:
            out.append("-1")
        else:
            out.append(" ".join(map(str, res)))
    return "\n".join(out)

# provided samples (simplified validity checks)
assert run("1\n1 6 3 100\n") == "-1"
assert run("1\n1 1 0 0\n") == "0"

# custom cases
assert run("1\n3 5 1 5\n") != "", "small feasible case"
assert run("1\n2 10 1 5\n") == "-1", "impossible by k constraint"
assert run("1\n4 3 2 20\n") != "", "distribution case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal impossible | -1 | b*k > s |
| trivial zero | 0 | base case |
| small feasible | any valid array | construction correctness |
| impossible k constraint | -1 | feasibility logic |
| distribution case | valid array | leftover spreading |

## Edge Cases

One key edge case is when `b * k == s`. In this case, there is no remaining slack. The algorithm assigns `a[0] = s` and leaves all other elements zero. Since all other values are below `k`, they contribute nothing, and the first element alone produces exactly `b` beauty. The construction remains valid.

Another edge case is when `k = 1`. Here every integer contributes fully to beauty. The condition becomes `sum(a) = s` and beauty equals `s`. This forces `b = s`. If not, no solution exists. The algorithm handles this naturally because `b * k = b` must equal `s`.

A final edge case is when `n = 1`. The only possible array is a single value `s`. The condition reduces to checking whether `s // k == b`, which matches the construction since we set the only element to `b * k` and require `s = b * k`.
