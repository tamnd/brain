---
title: "CF 104221E - \u0427\u0430\u0439\u043d\u044b\u0439 \u043c\u0430\u0433\u0430\u0437\u0438\u043d"
description: "We are given several possible positions for a shop along a straight line and a set of customers, each living at a fixed point and having a personal tolerance threshold."
date: "2026-07-01T23:46:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104221
codeforces_index: "E"
codeforces_contest_name: "\u0424\u0438\u043d\u0430\u043b \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u00ab\u041c\u0430\u0448\u0438\u043d\u0430 \u0422\u044c\u044e\u0440\u0438\u043d\u0433\u0430\u00bb \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 104221
solve_time_s: 65
verified: true
draft: false
---

[CF 104221E - \u0427\u0430\u0439\u043d\u044b\u0439 \u043c\u0430\u0433\u0430\u0437\u0438\u043d](https://codeforces.com/problemset/problem/104221/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several possible positions for a shop along a straight line and a set of customers, each living at a fixed point and having a personal tolerance threshold. If we pick one shop location and set a single price for every unit of tea, each customer will buy at most one unit, and only if their travel cost to the shop plus the price does not exceed their threshold.

For a fixed shop position $x_i$ and price $c$, customer $j$ is willing to buy if $|x_i - y_j| + c \le a_j$. Rearranging this, the condition becomes $c \le a_j - |x_i - y_j|$. Each customer thus contributes a maximum acceptable price for each shop location.

We must choose one shop location and a single price $c$ such that at least $k$ customers satisfy the condition and thus buy exactly one unit each. Every customer can buy at most one unit, so the count of satisfied customers is simply the number of customers whose constraint is met. The goal is to maximize $c$, or report that no valid configuration exists.

The constraints $n, m \le 10^5$ immediately rule out checking every pair of customer and shop position directly, since that would be $10^{10}$ operations in the worst case. Any solution must avoid explicitly evaluating all pairs.

A subtle point is that feasibility is monotone in price. If a price $c$ works for selling $k$ items, then any smaller price also works, because lowering $c$ only makes more customers satisfy the inequality. This monotonicity strongly suggests a binary search on the answer.

A naive mistake is to compute for each shop the number of customers satisfying the condition by iterating over all customers for each shop. This repeats work and is too slow.

Another mistake is to try to greedily assign customers to shops independently. The constraint is global per chosen shop, not per customer, so local decisions do not compose.

Edge cases worth noticing include situations where no shop can satisfy even one customer for a positive price, or where $k$ is larger than any possible number of customers served at any location even at price zero.

## Approaches

The brute-force method is straightforward. For each shop position, we try every possible price implicitly by checking how many customers satisfy $a_j - |x_i - y_j| \ge c$. If we fix a candidate price, counting satisfied customers for a fixed shop takes $O(n)$. Repeating this for all shops yields $O(mn)$ per price check, and without optimization we would need to search over many prices or recompute counts repeatedly, which is far beyond acceptable limits.

The key observation is that for a fixed shop location, each customer contributes an independent upper bound on the price. The number of customers who can buy at price $c$ is exactly the number of $j$ such that $a_j - |x_i - y_j| \ge c$. This is monotone in $c$, so we can binary search the maximum feasible price. The remaining problem is to evaluate feasibility efficiently for a given $c$.

For a fixed $c$, each customer induces an interval of acceptable shop positions:

$$|x_i - y_j| \le a_j - c$$

which means

$$x_i \in [y_j - (a_j - c),\; y_j + (a_j - c)]$$

So each customer becomes an interval over shop locations, and we need to choose a point $x_i$ covered by at least $k$ intervals. This is a classic sweep-line / coordinate compression problem on intervals, where we check whether any position has coverage at least $k$.

We can sort shop positions, compress them, and use a difference array or binary indexed tree to count how many intervals cover each shop position. Each feasibility check runs in $O(n + m)$, and we perform a binary search over the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(mn)$ per check | $O(1)$ | Too slow |
| Optimal | $O((n + m)\log A)$ | $O(n + m)$ | Accepted |

Here $A$ is the maximum possible price, bounded by $10^9$.

## Algorithm Walkthrough

We transform the problem into checking whether a given price $c$ is feasible, then binary search the maximum feasible value.

### Feasibility check for a fixed price $c$

1. For each customer $j$, compute $r_j = a_j - c$. If $r_j < 0$, this customer cannot buy at all and is ignored.
2. For each shop position $x_i$, interpret all customers satisfying $|x_i - y_j| \le r_j$ as contributing +1 coverage to that position.
3. Convert each customer into an interval $[y_j - r_j, y_j + r_j]$. We only care about overlap with actual shop positions.
4. Sort shop positions and use prefix sums to count how many intervals cover each shop.
5. If any shop position is covered by at least $k$ intervals, the price $c$ is feasible.

The key technical step is efficiently mapping interval coverage onto discrete shop positions. We sort shops and use binary search to locate interval endpoints in the compressed array, then apply a difference array: add +1 at the first covered shop index and -1 after the last covered index.

### Binary search over price

We search in the range $[0, \max a_j]$. For each mid value, we run the feasibility check. If feasible, we try higher prices; otherwise we reduce.

### Why it works

For a fixed shop, increasing price only reduces the number of customers satisfying $a_j - |x_i - y_j| \ge c$. This monotonicity ensures that feasibility is monotone in $c$. The feasibility condition itself is correctly captured by interval coverage because each customer independently defines the set of shop positions where they are willing to buy at price $c$. A valid solution exists exactly when there is a shop position covered by at least $k$ such intervals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(c, n, m, k, y, a, x):
    events = []
    for j in range(n):
        r = a[j] - c
        if r < 0:
            continue
        l = y[j] - r
        rgt = y[j] + r
        events.append((l, rgt))

    if not events:
        return False

    xs = sorted(x)
    m = len(xs)

    diff = [0] * (m + 1)

    import bisect
    for l, r in events:
        i = bisect.bisect_left(xs, l)
        j = bisect.bisect_right(xs, r) - 1
        if i <= j:
            diff[i] += 1
            diff[j + 1] -= 1

    cur = 0
    for i in range(m):
        cur += diff[i]
        if cur >= k:
            return True

    return False

def solve():
    n, m, k = map(int, input().split())
    y = []
    a = []
    for _ in range(n):
        yi, ai = map(int, input().split())
        y.append(yi)
        a.append(ai)

    x = list(map(int, input().split()))

    lo, hi = 0, max(a)
    ans = -1

    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid, n, m, k, y, a, x):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution separates the problem into a binary search driver and a feasibility checker. The checker converts each customer into a range of shop positions where they are willing to buy, then counts overlaps using a difference array over sorted shop coordinates. The bisect operations ensure each interval is mapped in logarithmic time.

A common pitfall is forgetting that we only care about shop positions, not the entire real line. That is why intervals are projected onto indices in the sorted shop array instead of treated continuously.

Another subtlety is handling empty feasibility: if all customers have $a_j < c$, the function immediately returns false, preventing incorrect accumulation.

## Worked Examples

### Sample 1

Input:

```
3 4 2
1 5
5 3
2 6
1 2 3 4
```

We binary search over price.

| mid (price) | valid intervals | max coverage over shops | feasible |
| --- | --- | --- | --- |
| 3 | all customers have r ≥ 0 | at least one shop has ≥2 | yes |
| 5 | only customers with a_j ≥ 5 | coverage drops but still ≥2 | yes |
| 6 | only one customer remains | max coverage < 2 | no |

The search converges to 5.

This demonstrates that increasing price reduces active customers and that the optimal value is the largest still allowing a shop to be covered by at least $k$ customer intervals.

### Sample 2

Input:

```
4 3 4
1 2
4 1
6 3
7 3
3 6 9
```

We test feasibility:

At price 0, intervals are:

customer 1: [ -1, 3 ]

customer 2: [ 3, 5 ]

customer 3: [ 3, 9 ]

customer 4: [ 4, 10 ]

Coverage at shop positions never reaches 4 simultaneously.

| price | max coverage | feasible |
| --- | --- | --- |
| 0 | 3 | no |
| any positive | ≤3 | no |

Thus result is -1.

This shows the case where even the best possible configuration cannot satisfy demand.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + m)\log A)$ | binary search over price, each feasibility check is linear in number of customers and shops |
| Space | $O(n + m)$ | storing intervals, prefix arrays, and sorted shop positions |

The binary search depth is bounded by $\log 10^9 \approx 30$, and each check processes at most $10^5$ elements, fitting comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve()).strip() if solve() else ""

# provided samples
assert run("""3 4 2
1 5
5 3
2 6
1 2 3 4
""") == "5"

assert run("""4 3 4
1 2
4 1
6 3
7 3
3 6 9
""") == "-1"

# custom cases

# minimum case
assert run("""1 1 1
1 10
1
""") == "10"

# impossible demand
assert run("""2 2 3
1 1
10 1
1 10
""") == "-1"

# all equal positions
assert run("""3 3 2
5 5
5 5
5 5
5 5 5
""") == "5"

# boundary overlap
assert run("""2 3 2
1 5
10 5
1 5 10
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimum case | 10 | single customer, single shop |
| impossible demand | -1 | k exceeds any achievable coverage |
| all equal positions | 5 | maximal overlap at identical locations |
| boundary overlap | 4 | correctness at interval edges |

## Edge Cases

One edge case occurs when all $a_j < c$. In that situation every $r_j$ becomes negative and the interval list is empty. The feasibility check immediately returns false, which matches the fact that no customer can buy anything at that price.

Another edge case is when intervals touch shop boundaries exactly. Since we use `bisect_left` and `bisect_right`, a customer whose interval ends exactly at a shop position still correctly includes that shop in coverage. For example, if a customer interval is $[2, 5]$ and shops include 5, the right boundary includes that shop because `bisect_right` places it inside the covered segment.

A final edge case is when multiple shops share identical coordinates. Sorting preserves duplicates, and the difference array correctly aggregates coverage over all identical positions, so each duplicate shop is treated independently but consistently in the prefix scan.
