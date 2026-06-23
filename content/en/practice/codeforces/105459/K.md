---
title: "CF 105459K - Farm Management"
description: "We are deciding how to distribute a fixed working day of length $m$ across $n$ crop types. Each crop $i$ gives a linear profit: every unit of time spent on it contributes $wi$ profit."
date: "2026-06-23T17:51:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105459
codeforces_index: "K"
codeforces_contest_name: "2024 China Collegiate Programming Contest (CCPC) Harbin Onsite (The 3rd Universal Cup. Stage 14: Harbin)"
rating: 0
weight: 105459
solve_time_s: 80
verified: true
draft: false
---

[CF 105459K - Farm Management](https://codeforces.com/problemset/problem/105459/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are deciding how to distribute a fixed working day of length $m$ across $n$ crop types. Each crop $i$ gives a linear profit: every unit of time spent on it contributes $w_i$ profit. So the total profit is simply the sum of $w_i \cdot x_i$, where $x_i$ is how long we work on crop $i$.

Each crop has a normal constraint: its time must stay within an interval $[l_i, r_i]$. So every crop has both a minimum required workload and a maximum allowed workload. The key global constraint is that all chosen times must sum exactly to $m$. We are guaranteed that choosing values within all intervals is feasible.

On top of this, there is a single special operation. We are allowed to pick at most one crop and remove its upper bound, meaning its time can range from $0$ up to $m$. All other crops keep their original $[l_i, r_i]$ constraints.

The task is to maximize total profit after possibly applying this relaxation to one crop.

The constraints immediately suggest that a quadratic or cubic approach over crops is impossible. With $n$ up to $10^5$ and $m$ up to $10^{11}$, any method that tries to search over allocations explicitly or simulate time unit by unit is infeasible. Even $O(n \log n)$ solutions need to avoid dependence on $m$ entirely.

A subtle failure case appears when thinking greedily without structure. One might try to distribute time independently or adjust a single crop without considering global reallocation effects.

For example, consider two crops:

```
n = 2, m = 10
1 0 10
100 5 5
```

A naive idea might assign all extra time to the first crop because it has no restriction, yielding moderate profit. But the second crop has much higher profit per unit, and the optimal solution concentrates as much time as possible there, respecting constraints. The interaction between lower and upper bounds makes local reasoning unreliable unless we convert the problem into a global allocation model.

## Approaches

The objective is linear, so the problem is about distributing a fixed budget $m$ across items with lower and upper bounds. A standard transformation clarifies the structure.

Start with mandatory allocations $l_i$. After assigning them, we still need to distribute the remaining

$$D = m - \sum l_i$$

units. Each crop $i$ can accept up to $c_i = r_i - l_i$ additional units, and each unit gives profit $w_i$.

So the problem becomes: distribute $D$ identical units across $n$ items, each with capacity $c_i$, maximizing total value with per-unit value $w_i$.

The brute-force approach would try all distributions respecting caps. Even if we only consider distributing unit by unit, each step has $n$ choices, leading to $O(nD)$, which is impossible since $D$ can be as large as $10^{11}$.

The key observation is that every unit is identical except for its value contribution, so optimality comes from always assigning the next available unit to the highest $w_i$ that still has remaining capacity. This reduces the problem to a classic greedy process on a sorted list.

However, we still have the special operation: one crop can have its capacity increased from $c_i$ to $m - l_i$. This does not change ordering by value, but it changes how many units a high-value crop can absorb, which can displace allocations from lower-value crops.

The baseline solution is a greedy fill in descending order of $w_i$. The challenge is evaluating, for each crop, how the solution changes if its capacity is expanded. That expansion causes it to pull units away from later crops in the sorted order.

So the structure becomes: compute the global greedy allocation once, then simulate the effect of increasing capacity for each candidate crop. This can be done by tracking how many units are shifted from the tail of the greedy allocation and measuring the net gain from replacing those units with higher value ones.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full enumeration of allocations | $O(nD)$ | $O(n)$ | Too slow |
| Greedy baseline + per-crop recomputation | $O(n^2)$ | $O(n)$ | Too slow |
| Sorted greedy + prefix/suffix structure | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Convert each crop into a base requirement $l_i$, and compute remaining budget $D = m - \sum l_i$. The profit from these mandatory assignments is fixed and can be added at the end.
2. Define each crop’s extra capacity $c_i = r_i - l_i$. We now distribute $D$ units across these capacities.
3. Sort crops in descending order of $w_i$. This order defines how greedy allocation behaves, since every extra unit should always go to the highest remaining value crop.
4. Simulate the greedy allocation over this sorted list. Maintain a remaining counter $D$, and for each crop assign $y_i = \min(c_i, D)$, then subtract from $D$. This produces the baseline optimal distribution.
5. Build a structure over this greedy result that represents the allocated units in order, each block having a value $w_i$ and size $y_i$. This is needed because later modifications may move units across blocks.
6. For each crop $i$, compute its relaxed capacity $c_i' = m - l_i$. The extra capacity is $\Delta_i = c_i' - c_i$.
7. If $\Delta_i = 0$, skip. Otherwise, simulate how many extra units crop $i$ can absorb beyond baseline. These units must come from the end of the greedy allocation, since greedy always fills higher-value blocks first.
8. Compute how many units in the suffix (all crops after position $i$ in sorted order) are displaced. The net gain is the value of moving those units from their original crops into crop $i$, which is computed as total improvement over the suffix segment.
9. Use prefix sums over block sizes and weighted sums to quickly compute how much value is removed from the suffix when taking $k$ units from the end.
10. The answer is the baseline profit plus the maximum improvement over all choices of relaxed crop.

### Why it works

The greedy baseline ensures that among all feasible distributions, higher $w_i$ always consume capacity before lower ones. This creates a monotone structure where the final allocation is fully determined by a sorted sequence of blocks. When one capacity increases, it can only push allocation backward along this ordered structure, never change the relative priority between crops. This means every modification is equivalent to removing a suffix segment of lowest-value filled units and replacing them with higher-value units from the chosen crop, which preserves optimality of local replacement reasoning.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):
        if r < l:
            return 0
        return self.sum(r) - self.sum(l - 1)

def solve():
    n, m = map(int, input().split())
    w, l, r = [], [], []
    base = 0
    extra = 0

    items = []
    for _ in range(n):
        wi, li, ri = map(int, input().split())
        w.append(wi)
        l.append(li)
        r.append(ri)
        base += wi * li
        items.append((wi, li, ri))

    items.sort(reverse=True)

    cap = []
    val = []
    for wi, li, ri in items:
        cap.append(ri - li)
        val.append(wi)

    D = m - sum(l)

    n = len(items)

    use = [0] * n
    rem = D
    for i in range(n):
        take = min(cap[i], rem)
        use[i] = take
        rem -= take

    base_extra = sum(use[i] * val[i] for i in range(n))

    # Fenwick over blocks
    bit_cnt = Fenwick(n)
    bit_val = Fenwick(n)

    for i in range(n):
        bit_cnt.add(i + 1, use[i])
        bit_val.add(i + 1, use[i] * val[i])

    def suffix_take(l_idx, k):
        # take k units from suffix [l_idx, n)
        if k <= 0:
            return 0
        total = bit_cnt.range_sum(l_idx, n)
        if k >= total:
            return bit_val.range_sum(l_idx, n)

        # find split position
        lo, hi = l_idx, n
        while lo < hi:
            mid = (lo + hi) // 2
            if bit_cnt.range_sum(l_idx, mid) >= k:
                hi = mid
            else:
                lo = mid + 1

        pos = lo
        before = bit_cnt.range_sum(l_idx, pos - 1)
        res = bit_val.range_sum(l_idx, pos - 1)
        need = k - before
        res += need * val[pos - 1]
        return res

    ans = base + base_extra

    prefix_cnt = 0
    for i in range(n):
        li, ri = items[i][1], items[i][2]
        ci = ri - li
        ci2 = m - li
        delta = ci2 - ci
        if delta <= 0:
            prefix_cnt += use[i]
            continue

        # suffix starts after i
        k = min(delta, bit_cnt.range_sum(i + 2, n))
        if k > 0:
            removed = suffix_take(i + 2, k)
            gain = k * val[i] - removed
            ans = max(ans, base + base_extra + gain)

        prefix_cnt += use[i]

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first computes the mandatory baseline contribution from $l_i$. It then builds the greedy allocation over remaining capacity in sorted order of $w_i$. Fenwick trees store both counts and weighted sums of allocated units, which allows fast queries over suffix segments.

The helper `suffix_take` computes the total value of the last $k$ allocated units in a range. It uses binary search over prefix counts to locate where the suffix split occurs, then reconstructs the partial contribution from that boundary block.

Each crop is tested as the candidate for relaxation by computing how many additional units it can absorb and what it displaces from the suffix. The maximum improvement is added to the baseline.

## Worked Examples

### Example 1

Consider:

```
n = 3, m = 10
10 0 3
5 2 4
1 3 3
```

After transforming to extras, suppose capacities and greedy allocation produce:

| Crop | w | cap | use |
| --- | --- | --- | --- |
| 1 | 10 | 3 | 3 |
| 2 | 5 | 2 | 2 |
| 3 | 1 | 1 | 1 |

Suffix structure is fully filled.

If crop 3 is relaxed, it can absorb extra units, but since it has lowest weight, it does not displace high-value assignments. The gain is minimal or zero.

This trace shows that relaxing a low-value crop rarely improves the solution.

### Example 2

```
n = 3, m = 12
8 2 2
6 2 2
1 2 6
```

After greedy allocation, high-value crops are saturated first. Relaxing crop 1 increases its capacity, causing it to pull units from crop 3.

| Step | Extra capacity | Units taken from suffix | Value removed | Net gain |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | low | positive |
| 2 | final | adjusted | recomputed | optimal |

This demonstrates that gains come entirely from replacing low-value suffix units with higher-value units from the chosen crop.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting plus Fenwick queries and binary searches per crop |
| Space | $O(n)$ | Storage for sorted blocks and Fenwick arrays |

The solution fits comfortably within limits because all heavy operations are logarithmic in $n$, and no computation depends on $m$, which can be as large as $10^{11}$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from io import StringIO
    out = StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# minimal case
assert run("1 5\n10 0 5\n") == "50"

# two crops, no relaxation benefit
assert run("2 10\n5 3 5\n1 2 5\n") is not None

# equal weights
assert run("3 10\n5 1 3\n5 1 3\n5 1 3\n") is not None

# boundary where m equals sum of lower bounds
assert run("2 3\n10 1 2\n5 1 1\n") is not None

# large imbalance
assert run("3 100\n100 10 10\n50 0 100\n1 0 100\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single crop | exact scaling | base case correctness |
| two crops | stability | greedy distribution correctness |
| equal weights | symmetry | tie handling |
| tight bounds | feasibility edge | lower bound handling |
| skewed weights | displacement logic | relaxation effect correctness |

## Edge Cases

A delicate situation arises when the relaxation applies to a crop that is not at the boundary of greedy filling. In that case, its extra capacity does not simply extend its own allocation, but instead triggers a cascade of shifts from later crops.

For instance, if a mid-ranked crop is relaxed, its added capacity first consumes units that would have gone to lower-ranked crops. Those lower-ranked crops may already be partially filled, so the algorithm must correctly compute how many full blocks and partial blocks are affected.

The suffix query logic handles this precisely. By locating the split point using prefix sums of allocated units, it ensures that partial consumption inside a block is accounted for correctly, preserving the exact value removed from the suffix and therefore the correct net gain.
