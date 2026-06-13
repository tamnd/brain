---
title: "CF 1458B - Glass Half Spilled"
description: "We have up to 100 glasses. Glass i can hold ai units of water and currently contains bi units. We are allowed to move water between glasses. The catch is that every transfer loses half of the transferred amount."
date: "2026-06-11T02:31:24+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1458
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 691 (Div. 1)"
rating: 2000
weight: 1458
solve_time_s: 130
verified: true
draft: false
---

[CF 1458B - Glass Half Spilled](https://codeforces.com/problemset/problem/1458/B)

**Rating:** 2000  
**Tags:** dp  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We have up to 100 glasses. Glass `i` can hold `a_i` units of water and currently contains `b_i` units.

We are allowed to move water between glasses. The catch is that every transfer loses half of the transferred amount. If we pour `x` units out of a glass, only `x/2` units can potentially reach the destination. Any excess beyond the destination's capacity is lost as well.

For every `k` from `1` to `n`, we must choose exactly `k` glasses and maximize the amount of water that can end up inside those chosen glasses after performing any sequence of transfers.

The answer for each `k` is the maximum total water that can be secured inside some set of `k` glasses.

The constraints are the first clue toward the intended solution. There are only 100 glasses, and every capacity and initial amount is at most 100. The total capacity is at most 10000, and the total water is also at most 10000. This is small enough for a dynamic programming state indexed by capacity sums, but far too large for any enumeration of subsets of glasses, since `2^100` possibilities are completely impossible.

The subtle part of the problem is understanding what transfers can actually achieve.

Consider choosing some set of glasses `S`.

Let

- `A = Σ a_i` over glasses in `S`
- `B = Σ b_i` over glasses in `S`
- `T = Σ b_i` over all glasses

The chosen glasses already contain `B` units of water. Outside the set there are `T - B` units.

Any water coming from outside suffers a 50% loss before reaching the chosen set. Therefore, even if we use all outside water, at most `(T - B)/2` additional units can be delivered into the chosen glasses.

At the same time, the chosen glasses cannot hold more than total capacity `A`.

Hence the amount of water achievable inside this chosen set is

$$\min\left(A,\; B + \frac{T-B}{2}\right)$$

A careless approach often misses one of these two limits.

For example:

```
2
100 0
1 1
```

For `k=1`, choosing the first glass gives capacity 100 but only 1 unit exists globally. After the spill, at most 0.5 reaches it, so the answer is 0.5, not 100.

Conversely:

```
2
5 5
100 100
```

Choosing only the first glass gives

$$\min(5,\;5+100/2)=5$$

The capacity limit dominates.

The whole problem becomes finding, for every `k`, the subset maximizing that expression.

## Approaches

A brute force solution would enumerate every subset of glasses. For each subset we would compute its total capacity `A`, its initial water `B`, and evaluate

$$\min\left(A,\; B+\frac{T-B}{2}\right).$$

This is correct because the expression fully characterizes the achievable amount for that subset.

The issue is the number of subsets. With `n = 100`, there are `2^{100}` possibilities, which is astronomically large.

The key observation is that the value of a subset depends only on two aggregate quantities:

$$A=\sum a_i,\qquad B=\sum b_i.$$

Individual identities no longer matter once these sums are known.

The total capacity is at most

$$100 \cdot 100 = 10000.$$

This suggests a knapsack-style dynamic programming where we track, for every subset size and every capacity sum, the maximum obtainable `B`.

Suppose we know, for each pair `(k, A)`, the largest possible value of `B` among subsets of size `k` whose capacities sum to `A`.

Then the answer for that state is simply

$$\min\left(A,\; \frac{T+B}{2}\right),$$

because

$$B+\frac{T-B}{2} = \frac{T+B}{2}.$$

For fixed `(k, A)`, larger `B` always gives a larger objective, so storing only the maximum `B` is sufficient.

This transforms the problem into a classical 0/1 knapsack with two dimensions: number of chosen glasses and total capacity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(1)$ | Too slow |
| Optimal DP | $O(n^2 \cdot \sum a_i)$ | $O(n \cdot \sum a_i)$ | Accepted |

## Algorithm Walkthrough

1. Read all glasses and compute the total amount of water

$$T=\sum b_i.$$
2. Let `MAXA = Σ a_i`.
3. Create a DP table where

$$dp[j][s]$$

stores the maximum total initial water `B` obtainable by choosing exactly `j` glasses whose capacities sum to `s`.

Unreachable states are initialized to `-1`.
4. Set

$$dp[0][0]=0.$$
5. Process glasses one by one.

For a glass `(a,b)`, iterate `j` and `s` in decreasing order and perform the standard 0/1 knapsack transition:

$$dp[j+1][s+a] = \max(dp[j+1][s+a],\, dp[j][s]+b).$$

Descending iteration prevents using the same glass multiple times.
6. After all glasses are processed, compute answers for every `k`.
7. For every reachable state `(k,s)` with stored value `B`, evaluate

$$\min\left(s,\frac{T+B}{2}\right).$$

This is the maximum water achievable for that particular aggregate pair `(A=s,B)`.
8. Take the maximum value among all states belonging to the same `k`.
9. Output all answers with sufficient precision.

### Why it works

Fix any chosen set of glasses.

Let `A` be their total capacity and `B` their initial water. The remaining glasses contain `T-B` units.

Every unit arriving from outside must be transferred at least once, so at most half of outside water can end up inside the chosen set. Thus the total water that can be gathered into the chosen glasses is at most

$$B+\frac{T-B}{2} = \frac{T+B}{2}.$$

The chosen glasses also cannot contain more than their total capacity `A`. Hence no strategy can exceed

$$\min\left(A,\frac{T+B}{2}\right).$$

This bound is achievable. Keep all water already inside the chosen set. Transfer outside water toward the chosen set as needed. Up to half of outside water can be delivered, and the process can stop once capacity `A` is reached. Thus the exact optimum for that subset equals

$$\min\left(A,\frac{T+B}{2}\right).$$

The DP enumerates every possible pair `(A,B)` achievable by subsets of size `k`. For each capacity sum `A`, it stores the largest possible `B`, which is sufficient because the objective increases monotonically with `B`. Therefore the maximum value computed for each `k` is exactly the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    glasses = []
    total_water = 0
    total_capacity = 0

    for _ in range(n):
        a, b = map(int, input().split())
        glasses.append((a, b))
        total_water += b
        total_capacity += a

    dp = [[-1] * (total_capacity + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    current_capacity_sum = 0

    for a, b in glasses:
        for cnt in range(n - 1, -1, -1):
            for cap in range(current_capacity_sum, -1, -1):
                if dp[cnt][cap] == -1:
                    continue

                nxt_cap = cap + a
                nxt_water = dp[cnt][cap] + b

                if nxt_water > dp[cnt + 1][nxt_cap]:
                    dp[cnt + 1][nxt_cap] = nxt_water

        current_capacity_sum += a

    ans = [0.0] * (n + 1)

    for k in range(1, n + 1):
        best = 0.0

        for cap in range(total_capacity + 1):
            inside_water = dp[k][cap]
            if inside_water == -1:
                continue

            value = min(float(cap), (total_water + inside_water) / 2.0)
            if value > best:
                best = value

        ans[k] = best

    print(*("{:.10f}".format(x) for x in ans[1:]))

if __name__ == "__main__":
    solve()
```

The DP table is the heart of the solution.

`dp[k][cap]` does not store the answer directly. Instead, it stores the largest possible amount of initially present water among all subsets of size `k` whose capacities sum to `cap`.

This choice is what makes the state space manageable. Capacity sums range only up to 10000, so the entire DP contains about one million states.

The descending loops are essential. If capacities were processed in increasing order, a glass could be reused multiple times within the same iteration, turning the transition into an unbounded knapsack and producing incorrect results.

After the knapsack finishes, each reachable state corresponds to some subset aggregate `(A,B)`. The formula

$$\min\left(A,\frac{T+B}{2}\right)$$

is evaluated directly, and the best value for each subset size is retained.

No integer overflow concerns exist because all sums are at most 10000.

## Worked Examples

### Example 1

Input:

```
3
6 5
6 5
10 2
```

Total water:

$$T=12$$

Relevant DP states after processing all glasses:

| k | Capacity A | Water B |
| --- | --- | --- |
| 1 | 6 | 5 |
| 1 | 10 | 2 |
| 2 | 12 | 10 |
| 2 | 16 | 7 |
| 3 | 22 | 12 |

Evaluation:

| k | A | B | min(A, (T+B)/2) |
| --- | --- | --- | --- |
| 1 | 6 | 5 | 6 |
| 1 | 10 | 2 | 7 |
| 2 | 12 | 10 | 11 |
| 2 | 16 | 7 | 9.5 |
| 3 | 22 | 12 | 12 |

Best answers:

| k | Answer |
| --- | --- |
| 1 | 7 |
| 2 | 11 |
| 3 | 12 |

This example shows both limiting factors. For `k=1`, the larger-capacity glass wins despite having less initial water because it can receive spilled water from elsewhere.

### Example 2

Input:

```
2
100 0
1 1
```

Total water:

$$T=1$$

States:

| k | A | B |
| --- | --- | --- |
| 1 | 100 | 0 |
| 1 | 1 | 1 |
| 2 | 101 | 1 |

Evaluation:

| k | A | B | Value |
| --- | --- | --- | --- |
| 1 | 100 | 0 | 0.5 |
| 1 | 1 | 1 | 1 |
| 2 | 101 | 1 | 1 |

Answers:

| k | Answer |
| --- | --- |
| 1 | 1 |
| 2 | 1 |

This demonstrates that huge capacity alone is useless when there is not enough water available globally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 \cdot \sum a_i)$ | Knapsack transitions over subset size and capacity |
| Space | $O(n \cdot \sum a_i)$ | DP table |

Since `n ≤ 100` and `Σa_i ≤ 10000`, the number of DP states is about one million. The total number of transitions is roughly `100 × 100 × 10000 = 10^8`, but the actual implementation only iterates over reachable capacity ranges and passes comfortably within the contest limits in optimized Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())

    glasses = []
    total_water = 0
    total_capacity = 0

    for _ in range(n):
        a, b = map(int, input().split())
        glasses.append((a, b))
        total_water += b
        total_capacity += a

    dp = [[-1] * (total_capacity + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    cur = 0

    for a, b in glasses:
        for k in range(n - 1, -1, -1):
            for s in range(cur, -1, -1):
                if dp[k][s] == -1:
                    continue
                dp[k + 1][s + a] = max(
                    dp[k + 1][s + a],
                    dp[k][s] + b
                )
        cur += a

    ans = []

    for k in range(1, n + 1):
        best = 0.0
        for s in range(total_capacity + 1):
            B = dp[k][s]
            if B == -1:
                continue
            best = max(best, min(float(s), (total_water + B) / 2.0))
        ans.append(f"{best:.10f}")

    return " ".join(ans) + "\n"

# sample
out = run(
"""3
6 5
6 5
10 2
"""
).strip().split()

assert abs(float(out[0]) - 7.0) < 1e-9
assert abs(float(out[1]) - 11.0) < 1e-9
assert abs(float(out[2]) - 12.0) < 1e-9

# minimum size
out = run(
"""1
5 3
"""
).strip()
assert abs(float(out) - 3.0) < 1e-9

# empty water except one glass
out = run(
"""2
100 0
1 1
"""
).strip().split()
assert abs(float(out[0]) - 1.0) < 1e-9
assert abs(float(out[1]) - 1.0) < 1e-9

# all equal glasses
out = run(
"""3
10 10
10 10
10 10
"""
).strip().split()
assert abs(float(out[0]) - 10.0) < 1e-9
assert abs(float(out[1]) - 20.0) < 1e-9
assert abs(float(out[2]) - 30.0) < 1e-9

# capacity bottleneck
out = run(
"""2
5 5
100 100
"""
).strip().split()
assert abs(float(out[0]) - 100.0) < 1e-9
assert abs(float(out[1]) - 105.0) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single glass | Existing water amount | Base case |
| One full and one almost empty glass | Transfer-loss behavior | Half-spill rule |
| All glasses identical | Symmetry handling | No dependence on ordering |
| Capacity bottleneck example | Capacity cap dominates | Correct use of `min(A, ...)` |

## Edge Cases

Consider:

```
2
100 0
1 1
```

For `k=1`, choosing the large glass gives `A=100`, `B=0`. The algorithm evaluates

$$\min(100,(1+0)/2)=0.5.$$

Choosing the small glass gives

$$\min(1,(1+1)/2)=1.$$

The DP keeps both states and returns the larger value, which is correct.

Now consider:

```
2
5 5
100 100
```

Choosing only the first glass yields

$$A=5,\quad B=5.$$

The formula gives

$$\min(5,(105)/2)=5.$$

Even though enormous water exists elsewhere, the chosen glass cannot exceed its capacity. The algorithm enforces this automatically through the `min`.

Finally:

```
3
10 0
10 0
10 0
```

All states have `B=0` and total water `T=0`. Every evaluation becomes zero, so every answer is exactly zero. The DP correctly handles glasses that initially contain no water because `0` is stored as a valid reachable water sum rather than being confused with an unreachable state.
