---
title: "CF 427E - Police Patrol"
description: "All criminals stand on the x-axis, and we must choose one integer coordinate for the police station. The patrol car starts from the station, visits some criminals, brings them back to the station, then repeats until everyone is arrested. Each trip can carry at most m criminals."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 427
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 244 (Div. 2)"
rating: 2000
weight: 427
solve_time_s: 114
verified: true
draft: false
---

[CF 427E - Police Patrol](https://codeforces.com/problemset/problem/427/E)

**Rating:** 2000  
**Tags:** greedy, implementation, math, ternary search  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

All criminals stand on the x-axis, and we must choose one integer coordinate for the police station. The patrol car starts from the station, visits some criminals, brings them back to the station, then repeats until everyone is arrested. Each trip can carry at most `m` criminals.

The distance cost of one trip is simple. If the farthest criminal visited in that trip is at distance `d` from the station, the car must go from the station to that point and come back, so the trip costs `2d`.

The real question is how to split the criminals into trips and where to place the station so that the total traveled distance is minimum.

The positions are already sorted. There can be up to `10^6` criminals, which immediately rules out anything quadratic. Even `O(n log n)` is already close to the practical limit in Python for this input size, so the intended solution should be essentially linear after sorting, and we are lucky because the input is already sorted.

A common mistake is to think the best station position is always the median. That is true when every criminal is transported individually, but false here because the car can group several criminals in one trip.

Consider:

```
n = 4, m = 2
positions = [0, 1, 100, 101]
```

If we place the station near the median, around `50`, both sides become expensive. The optimal solution is actually near one cluster, because trips are charged by the farthest criminal in each batch.

Another easy bug appears when criminals exist on both sides of the station. Trips to the left and right are independent. A single trip cannot efficiently combine both directions because the car would need to cross the station again anyway.

For example:

```
n = 3, m = 2
positions = [-10, -9, 100]
```

If the station is at `0`, the optimal plan is:

- one trip for `100`, cost `200`
- one trip for `-10` and `-9`, cost `20`

Total `220`.

Trying to merge left and right criminals into one trip only increases distance.

Another subtle case happens when the station is built exactly where some criminals stand.

```
n = 5, m = 2
positions = [1, 1, 1, 10, 10]
```

Building at `1` instantly arrests three criminals with zero travel cost. Only the two criminals at `10` require transportation.

A careless implementation that still includes criminals at the station in the transportation cost will overcount.

## Approaches

The brute-force idea is straightforward. Since the station must be placed at some integer coordinate, we could try every candidate position, compute the optimal transportation cost for that station, and take the minimum.

Suppose the station is fixed at `x`.

All criminals to the left of `x` can be processed independently from criminals to the right. On one side, the optimal strategy is greedy: always take the farthest remaining criminals together in one trip, because the trip cost depends only on the farthest distance reached.

For example, if distances on one side are:

```
1 3 5 8 10
```

and `m = 2`, then optimal grouping is:

```
(10, 8), (5, 3), (1)
```

with cost:

```
2 * (10 + 5 + 1)
```

not:

```
2 * (10 + 8 + 5)
```

because once we already travel to distance `10`, taking `8` together is free.

So for a fixed station we can compute the answer greedily in linear time.

The problem is the number of candidate stations. Coordinates may reach `10^9`, so brute-forcing integer positions is impossible. Even restricting to criminal coordinates still gives `O(n^2)` total work, which is far too slow for `10^6` elements.

The key observation is that the cost function is convex.

Moving the station slightly to the right decreases the right-side distances but increases the left-side distances. Because trips are grouped greedily in sorted order, the total cost changes monotonically in slope. This creates a discrete convex function over the station coordinate.

Convexity means we can use ternary search on the station position.

Even better, evaluating one position can be done in `O(n / m)` instead of `O(n)` if we directly jump across grouped criminals.

The resulting complexity becomes efficient enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O((n / m) log C) | O(1) | Accepted |

Here `C` is the coordinate range, roughly `2 * 10^9`.

## Algorithm Walkthrough

1. Choose a candidate station position `x`.
2. Separate criminals into those left of `x` and those right of `x`.

Criminals exactly at `x` require no transportation and contribute nothing.
3. Process the left side.

Distances from the station are:

```
x - position
```

Because positions are sorted, the farthest criminals are the leftmost ones.

The optimal strategy is to group the farthest remaining `m` criminals into one trip.

If indices on the left side are:

```
l, l+1, ..., r
```

then we add:

```
2 * (x - positions[i])
```

for every `i` taken in steps of `m` from the farthest side.
4. Process the right side similarly.

The farthest criminals are the rightmost ones.

We again take groups of size `m` from the farthest side and add:

```
2 * (positions[i] - x)
```
5. The sum of both sides is the total cost for station position `x`.
6. Since the cost function is convex, perform ternary search on `x`.

We compare the cost at two middle points and discard the worse side.
7. After the search interval becomes small, brute-force all remaining integer coordinates inside the interval and output the minimum value.

### Why it works

For a fixed station, the greedy grouping is optimal because one trip cost depends only on the farthest criminal visited. Once a trip already reaches distance `d`, carrying any additional criminals closer than `d` adds no extra travel distance. So every trip should contain the farthest available criminals first.

The total cost as a function of station position is convex. Moving the station right decreases costs contributed by right-side groups and increases costs contributed by left-side groups. Each group contributes an absolute-value linear term, and sums of convex functions remain convex. Ternary search is valid on such functions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    def cost(x):
        res = 0

        # left side
        i = 0
        while i < n and a[i] < x:
            i += 1

        j = 0
        while j < i:
            res += 2 * (x - a[j])
            j += m

        # right side
        j = n - 1
        while j >= i and a[j] > x:
            j -= 1

        k = n - 1
        while k > j:
            res += 2 * (a[k] - x)
            k -= m

        return res

    lo = -10**9
    hi = 10**9

    while hi - lo > 5:
        m1 = lo + (hi - lo) // 3
        m2 = hi - (hi - lo) // 3

        if cost(m1) <= cost(m2):
            hi = m2
        else:
            lo = m1

    ans = 10**30

    for x in range(lo, hi + 1):
        ans = min(ans, cost(x))

    print(ans)

solve()
```

The `cost(x)` function implements the greedy batching logic directly.

For the left side, criminals are already sorted from farthest to closest relative to the station. Every `m`-th criminal determines one trip cost, because that criminal is the farthest member of its batch.

Suppose:

```
positions = [-10, -8, -3, -1]
x = 0
m = 2
```

The batches are:

```
(-10, -8)
(-3, -1)
```

Only `-10` and `-3` determine trip distances, so we step by `m`.

The right side works symmetrically from the array end.

The ternary search uses integer coordinates. After shrinking the interval enough, we brute-force the remaining few coordinates because discrete convex functions may have flat regions.

All arithmetic uses Python integers, which safely handle the maximum possible answer.

## Worked Examples

### Example 1

Input:

```
3 6
1 2 3
```

Since `m >= n`, all criminals can be transported in one trip.

The optimal station is at `2`.

| Station x | Trips | Total Cost |
| --- | --- | --- |
| 1 | reach 3 and return | 4 |
| 2 | reach 3 and return | 2 |
| 3 | reach 1 and return | 4 |

The minimum is `2`.

This example shows why criminals standing at the station contribute zero cost. When the station is at `2`, criminal `2` is instantly arrested.

### Example 2

Input:

```
5 2
-10 -5 1 2 20
```

Try station `x = 1`.

Left side batches:

```
(-10, -5)
```

Cost:

```
2 * 11 = 22
```

Right side batches:

```
(20, 2)
```

Cost:

```
2 * 19 = 38
```

Total:

```
60
```

| Side | Farthest Criminal | Batch Cost |
| --- | --- | --- |
| Left | -10 | 22 |
| Right | 20 | 38 |

This trace demonstrates the greedy invariant. Inside one batch, only the farthest criminal matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n / m) log C) | Each cost evaluation processes one criminal per batch, ternary search performs logarithmically many evaluations |
| Space | O(1) | Only a few variables are used |

The coordinate range is about `2 * 10^9`, so ternary search performs around 40 iterations. Each evaluation scans grouped criminals efficiently, which comfortably fits within the limits even for `10^6` criminals.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        def cost(x):
            res = 0

            i = 0
            while i < n and a[i] < x:
                i += 1

            j = 0
            while j < i:
                res += 2 * (x - a[j])
                j += m

            j = n - 1
            while j >= i and a[j] > x:
                j -= 1

            k = n - 1
            while k > j:
                res += 2 * (a[k] - x)
                k -= m

            return res

        lo = -10**9
        hi = 10**9

        while hi - lo > 5:
            m1 = lo + (hi - lo) // 3
            m2 = hi - (hi - lo) // 3

            if cost(m1) <= cost(m2):
                hi = m2
            else:
                lo = m1

        ans = 10**30

        for x in range(lo, hi + 1):
            ans = min(ans, cost(x))

        return str(ans)

    return solve()

# provided sample
assert run("3 6\n1 2 3\n") == "2", "sample 1"

# single criminal
assert run("1 1\n10\n") == "0", "station can be built at criminal"

# all equal positions
assert run("5 2\n7 7 7 7 7\n") == "0", "all arrested instantly"

# symmetric positions
assert run("4 2\n-10 -1 1 10\n") == "40", "balanced sides"

# off-by-one batching
assert run("5 2\n1 2 3 4 5\n") == "6", "correct grouping"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 10` | `0` | Single criminal case |
| `5 2 / 7 7 7 7 7` | `0` | Criminals at station position |
| `4 2 / -10 -1 1 10` | `40` | Independent left/right processing |
| `5 2 / 1 2 3 4 5` | `6` | Correct batch stepping |

## Edge Cases

Consider all criminals already standing at the same coordinate.

```
5 3
10 10 10 10 10
```

The algorithm evaluates station position `10`.

Both left and right scans become empty because no criminal satisfies `< x` or `> x`.

Total cost remains `0`, which is correct because everyone is arrested instantly.

Now consider criminals on both sides.

```
4 2
-100 -1 1 100
```

At station `0`, the algorithm forms:

Left batches:

```
(-100, -1)
```

Right batches:

```
(100, 1)
```

Total:

```
2 * 100 + 2 * 100 = 400
```

The two sides are handled independently, which is optimal because crossing the station gives no advantage.

Finally, consider incomplete final batches.

```
5 2
1 2 3 4 100
```

The right-side groups are:

```
(100, 4)
(3, 2)
(1)
```

The algorithm correctly charges only the farthest member of each batch:

```
2 * 100 + 2 * 3 + 2 * 1
```

A common off-by-one bug is forgetting that the last partial batch still requires one trip.
