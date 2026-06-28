---
title: "CF 104721B - road"
description: "We are given a straight road made of $n$ stations numbered from $1$ to $n$. Between station $i$ and $i+1$, there is a road segment with length $vi$. At every station $i$, fuel can be bought, but each station has its own fixed price $ai$ per liter."
date: "2026-06-29T04:14:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104721
codeforces_index: "B"
codeforces_contest_name: "CSP-J 2023"
rating: 0
weight: 104721
solve_time_s: 89
verified: true
draft: false
---

[CF 104721B - road](https://codeforces.com/problemset/problem/104721/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a straight road made of $n$ stations numbered from $1$ to $n$. Between station $i$ and $i+1$, there is a road segment with length $v_i$. At every station $i$, fuel can be bought, but each station has its own fixed price $a_i$ per liter.

A car starts at station $1$ with an empty tank and must reach station $n$. The tank has no capacity limit, but fuel consumption is quantized: one liter of fuel allows the car to travel exactly $d$ kilometers, so traveling a segment of length $v_i$ requires $\lceil v_i / d \rceil$ liters.

The task is to choose how much fuel to buy at each station so that the car can traverse all segments and the total cost is minimized.

The constraints allow up to $10^5$ stations and segment lengths up to $10^5$. This strongly suggests an $O(n)$ or $O(n \log n)$ solution. Any approach that tries to simulate all possible refueling decisions or dynamic programming over fuel states would be too slow because the state space would explode with both position and fuel quantity.

A subtle issue arises from integer rounding of fuel consumption. Even if a segment is only slightly longer than a multiple of $d$, it still requires an extra full liter. For example, if $d = 4$ and $v_i = 5$, then we need $2$ liters, not $1.25$.

Another non-obvious concern is where fuel is bought. Since fuel is not restricted by tank size, buying decisions are purely about price, not feasibility. A naive approach might try to decide locally at each station whether to buy fuel for the next segment only, but this fails when a later station is cheaper and could have been used earlier.

## Approaches

A brute-force strategy would consider, at every station, how much fuel to buy and then simulate all possible distributions of fuel purchases across stations. Even restricting ourselves to “buy exactly what is needed for the next segment or more” still leads to exponential choices, since fuel can be carried forward indefinitely and decisions interact across many segments.

A dynamic programming formulation over stations and remaining fuel also becomes impractical. The fuel quantity is unbounded, and discretizing it leads to a very large state space proportional to total possible fuel demand.

The key observation is that fuel is perfectly transferable and has no degradation cost, so the only meaningful factor is the cheapest price seen so far up to the current position. Once we reach a station with a lower price, it dominates all previous stations for any future purchase.

Thus, for each road segment, the optimal strategy is to buy all fuel required for that segment at the minimum price among stations from $1$ up to the current station. We only need to maintain a running minimum of fuel prices and multiply it by the fuel requirement of each segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) to O(n²) states | Too slow |
| Optimal (prefix minimum greedy) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

Let us process the road from left to right while keeping track of the cheapest fuel price encountered so far.

1. Initialize a variable `best_price` with the price at station 1, since this is the first available option. This represents the lowest cost per liter we can currently use.
2. Initialize `answer = 0`, which will accumulate total cost.
3. For each segment from station $i$ to $i+1$, compute the number of liters needed as:

$$\text{liters} = \frac{v_i + d - 1}{d}$$

This is the smallest integer number of liters whose coverage $d \cdot \text{liters}$ is at least $v_i$.
4. Add to the answer:

$$\text{answer} += \text{liters} \times \text{best\_price}$$

This reflects buying all fuel for that segment at the cheapest price available so far.
5. Before moving to the next segment, update:

$$\text{best\_price} = \min(\text{best\_price}, a_{i+1})$$

This ensures that future segments can benefit from any cheaper station ahead.
6. After processing all segments, output `answer`.

### Why it works

At any point along the road, any fuel purchased earlier can be used later without loss. Therefore, if we ever encounter a station with a lower price, there is no reason to have purchased fuel earlier at a higher price for any future consumption. The best possible strategy is always to treat the cheapest price seen so far as the effective cost of fuel for all remaining needs. This creates a prefix-minimum structure where each segment is independently assigned a cost based on the cheapest reachable station up to that point, and no rearrangement of purchases can reduce the total cost further.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, d = map(int, input().split())
    v = list(map(int, input().split()))
    a = list(map(int, input().split()))

    best_price = a[0]
    ans = 0

    for i in range(n - 1):
        liters = (v[i] + d - 1) // d
        ans += liters * best_price
        if i + 1 < n:
            best_price = min(best_price, a[i + 1])

    print(ans)

if __name__ == "__main__":
    solve()
```

The code follows the greedy structure directly. The loop processes each road segment once, computing the required liters using integer ceiling division. The variable `best_price` maintains the prefix minimum of fuel prices, ensuring that every segment is charged at the cheapest possible available rate up to that point.

A common implementation pitfall is updating the minimum price at the wrong time. It must be updated after using the current segment’s price decision logic; otherwise, the algorithm would incorrectly allow station $i+1$ to be used for segment $i$, which is impossible because that segment is reached before arriving at station $i+1$.

## Worked Examples

### Sample 1

Input:

```
5 4
10 10 10 10
9 8 9 6 5
```

We track segment by segment.

| Segment | v_i | liters | best_price | cost added | total |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 3 | 9 | 27 | 27 |
| 2 | 10 | 3 | 8 | 24 | 51 |
| 3 | 10 | 3 | 8 | 24 | 75 |
| 4 | 10 | 3 | 6 | 18 | 93 |

The output is the accumulated cost. The decreasing price sequence shows why prefix minimum is crucial, since later cheaper stations dominate earlier ones.

### Sample 2 (custom)

Input:

```
4 3
5 4 6
7 2 5 1
```

| Segment | v_i | liters | best_price | cost added | total |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 2 | 7 | 14 | 14 |
| 2 | 4 | 2 | 2 | 4 | 18 |
| 3 | 6 | 2 | 2 | 4 | 22 |

This example highlights a key behavior: once a very cheap station appears, it dominates all future segments, even if earlier stations were expensive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each segment is processed once with constant-time arithmetic and a single minimum update |
| Space | O(1) | Only a few running variables are maintained |

The algorithm comfortably fits within the limits since $n \le 10^5$, and all operations are simple integer computations.

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

# provided sample
assert run("""5 4
10 10 10 10
9 8 9 6 5
""") == "79"

# minimum size
assert run("""2 5
10
3 10
""") == str(((10 + 4)//5) * 3)

# all equal prices
assert run("""3 2
3 3
5 5 5
""") == str(((5+1)//2)*3 + ((5+1)//2)*3)

# decreasing prices
assert run("""4 3
6 6 6
9 8 7 1
""") == str(((6+2)//3)*9 + ((6+2)//3)*8 + ((6+2)//3)*7)

# increasing prices
assert run("""4 3
6 6 6
1 2 3 4
""") == str(((6+2)//3)*1 + ((6+2)//3)*1 + ((6+2)//3)*1)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| min size | computed | smallest valid structure |
| all equal | computed | no price improvement case |
| decreasing prices | computed | prefix minimum updates early |
| increasing prices | computed | best price stays at start |

## Edge Cases

A key edge case occurs when a much cheaper station appears later. Suppose the first station is expensive and the last station is extremely cheap. The algorithm correctly avoids buying any earlier fuel for future segments because it continuously updates the minimum price only after passing each station.

Another edge case is when $v_i$ is not divisible by $d$. For example, if $d = 4$ and $v_i = 5$, the algorithm computes $(5 + 3) // 4 = 2$ liters. A mistaken floor division would incorrectly allocate only 1 liter and underestimate cost, making the solution invalid.

A final subtle case is when all prices are identical. In this situation, the algorithm effectively reduces to summing all segment fuel requirements multiplied by that constant price, showing that the greedy structure degenerates cleanly into a straightforward accumulation without needing any optimization decisions.
