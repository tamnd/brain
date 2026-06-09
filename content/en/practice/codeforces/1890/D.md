---
title: "CF 1890D - Doremy's Connecting Plan"
description: "We have $n$ cities, where city $i$ contains $ai$ people. Initially every city is isolated. An edge between cities $i$ and $j$ can be added only if the total population of all cities belonging to the connected components containing $i$ or $j$ is at least $$i cdot j cdot c."
date: "2026-06-09T01:09:44+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1890
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 906 (Div. 2)"
rating: 1700
weight: 1890
solve_time_s: 138
verified: true
draft: false
---

[CF 1890D - Doremy's Connecting Plan](https://codeforces.com/problemset/problem/1890/D)

**Rating:** 1700  
**Tags:** graphs, greedy, math, sortings  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We have $n$ cities, where city $i$ contains $a_i$ people. Initially every city is isolated.

An edge between cities $i$ and $j$ can be added only if the total population of all cities belonging to the connected components containing $i$ or $j$ is at least

$$i \cdot j \cdot c.$$

Whenever we connect two different components, their populations merge and become available for future operations.

The task is to determine whether there exists some sequence of edge additions that eventually makes the whole graph connected.

The constraints are the first clue. The total number of cities across all test cases is at most $2 \cdot 10^5$, which strongly suggests an $O(n \log n)$ solution. Any algorithm that repeatedly scans all pairs of cities would require $O(n^2)$ or worse operations, which would be far too slow for $n=2\cdot10^5$.

The tricky part is that the validity of an edge depends on the current connected components, not only on the endpoints. After several merges, a previously impossible edge may become possible because the component population has grown.

A common mistake is to think that any pair of cities can serve as the next merge candidate. The city indices appear in the cost formula, and index $1$ is special because

$$1 \cdot i \cdot c = i c$$

is the smallest possible cost involving city $i$.

Consider:

```
n = 3, c = 10
a = [100, 1, 1]
```

City $1$ alone already has population $100$. It can connect to city $2$ because $100+1 \ge 20$, then to city $3$ because $101+1 \ge 30$. The answer is YES.

A naive strategy that tries to connect arbitrary cheapest pairs first may fail to notice that city $1$ is the natural hub.

Another subtle case is:

```
n = 3, c = 1
a = [0, 0, 2]
```

The answer is NO. Although the total population is positive, city $1$ cannot connect to city $2$ because $0+0 < 2$, and city $1$ cannot connect to city $3$ because $0+2 < 3$. No merge is possible.

The solution must correctly identify when the growth process gets stuck before reaching all cities.

## Approaches

A brute-force simulation would treat each city as its own component and repeatedly search for any pair of components that can be merged.

To test whether two components can be connected, we would need their total population and some pair of cities capable of satisfying the inequality. Even with a disjoint-set structure, searching all component pairs after every merge is expensive. There can be $O(n)$ merges, and each step may examine $O(n^2)$ candidates, leading to $O(n^3)$ behavior in the worst case.

The key observation is that city $1$ dominates the problem.

Suppose we already have a component containing city $1$, with total population $S$. To attach city $i$ directly to this component, we need

$$S + a_i \ge i \cdot c.$$

This is the cheapest possible way to bring city $i$ into the growing component, because every other city index $j\ge1$ gives

$$i \cdot j \cdot c \ge i \cdot c.$$

If city $i$ cannot be attached to the component containing city $1$, then connecting it through some other city cannot be easier.

This transforms the problem into a growth process.

Start with the component containing city $1$. Its current population is $a_1$.

For every city $i>1$, define its contribution:

$$gain_i = a_i - i c.$$

If the current population is $S$, then city $i$ is attachable exactly when

$$S + gain_i \ge 0.$$

After attaching it, the population becomes

$$S \leftarrow S + a_i.$$

Among all currently attachable cities, we should take the one with the largest contribution $gain_i$. This maximizes future population growth and can never hurt.

The resulting process is identical to a classic greedy problem. We sort cities by $gain_i$ in descending order and keep adding cities while the current population is large enough to satisfy the corresponding requirement.

If every city can be added, the graph can be connected. Otherwise it cannot.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ worst case | $O(n)$ | Too slow |
| Optimal Greedy + Sorting | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Start with the component containing city $1$. Let its current population be $S=a_1$.
2. For every city $i\ge2$, compute

$$gain_i = a_i - i c.$$

This quantity measures how much population remains after paying the minimum possible connection cost involving city $1$.
3. Sort all cities $i\ge2$ by $gain_i$ in descending order.
4. Process the sorted cities from largest gain to smallest.
5. For the current city, check whether

$$S + gain_i \ge 0.$$

This is equivalent to

$$S + a_i \ge i c,$$

meaning the city can be connected directly to the component containing city $1$.
6. If the condition fails for some city, output `"NO"`.

The remaining cities have gain no larger than the current one, so none of them can be connected either.
7. Otherwise merge the city into the component and update

$$S \leftarrow S + a_i.$$
8. After all cities are processed successfully, output `"YES"`.

### Why it works

Let $S$ be the population of the component containing city $1$.

For any city $i$, the cheapest possible way to attach it to that component is using an edge involving city $1$, whose requirement is $i c$. Any edge using another city $j$ requires $i j c$, which is never smaller.

Hence a city is usable exactly when $S+a_i \ge i c$.

Suppose several cities are currently usable. Choosing the city with the largest gain adds the most population to $S$, producing the largest possible future component. If a solution exists after choosing some other city, it also exists after choosing the largest-gain city because the component population is at least as large afterward.

This exchange argument shows that the greedy choice is always safe. If the greedy process gets stuck at some city, no alternative ordering could have produced a larger current population, so no valid sequence exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    ans = []

    for _ in range(t):
        n, c = map(int, input().split())
        a = list(map(int, input().split()))

        cur = a[0]

        cities = []
        for i in range(2, n + 1):
            gain = a[i - 1] - i * c
            cities.append((gain, a[i - 1]))

        cities.sort(reverse=True)

        ok = True

        for gain, pop in cities:
            if cur + gain < 0:
                ok = False
                break
            cur += pop

        ans.append("YES" if ok else "NO")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The variable `cur` stores the population of the component containing city $1$.

For every other city we store two values. The first is `gain = a[i] - i*c`, which determines whether the city can currently be attached. The second is its population, which will be added to `cur` after the merge.

Sorting by descending gain implements the greedy choice. The check

```
cur + gain < 0
```

is exactly the condition

$$cur + a_i < i c.$$

If it fails, the city cannot be connected. Since all remaining gains are even smaller, no later city can be connected either.

Python integers automatically handle values up to $10^{12}$ and beyond, so there is no overflow risk. In languages with fixed-width integers, 64-bit arithmetic would be required.

## Worked Examples

### Example 1

Input:

```
4 10
0 20 15 10
```

Computed gains:

| City | Population | Gain = ai - i*c |
| --- | --- | --- |
| 2 | 20 | 0 |
| 3 | 15 | -15 |
| 4 | 10 | -30 |

Sorted order remains $2,3,4$.

| Step | Current S | Gain | Check S+Gain >= 0 | New S |
| --- | --- | --- | --- | --- |
| Start | 0 | - | - | 0 |
| City 2 | 0 | 0 | Yes | 20 |
| City 3 | 20 | -15 | Yes | 35 |
| City 4 | 35 | -30 | Yes | 45 |

All cities are attached, so the answer is YES.

This example shows how the component grows over time. Early merges increase the available population and make later merges possible.

### Example 2

Input:

```
5 2
1 1 3 1 1
```

Computed gains:

| City | Population | Gain |
| --- | --- | --- |
| 2 | 1 | -3 |
| 3 | 3 | -3 |
| 4 | 1 | -7 |
| 5 | 1 | -9 |

Sorted gains: $-3,-3,-7,-9$.

| Step | Current S | Gain | Check S+Gain >= 0 |
| --- | --- | --- | --- |
| Start | 1 | - | - |
| First city | 1 | -3 | No |

The process stops immediately, so the answer is NO.

This demonstrates that a positive total population is not enough. The component containing city $1$ must be able to start growing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting the $n-1$ gains dominates |
| Space | $O(n)$ | Storage of gains and populations |

The sum of all $n$ values across test cases is at most $2\cdot10^5$. An $O(n \log n)$ algorithm easily fits within the 1-second limit in Python, and the memory usage is comfortably below the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline

        t = int(input())
        out = []

        for _ in range(t):
            n, c = map(int, input().split())
            a = list(map(int, input().split()))

            cur = a[0]

            cities = []
            for i in range(2, n + 1):
                cities.append((a[i - 1] - i * c, a[i - 1]))

            cities.sort(reverse=True)

            ok = True
            for gain, pop in cities:
                if cur + gain < 0:
                    ok = False
                    break
                cur += pop

            out.append("YES" if ok else "NO")

        return "\n".join(out)

    return solve()

# provided sample
assert run(
"""7
4 10
0 20 15 10
2 1
1 1
5 1
0 1 0 4 199
5 2
1 1 3 1 1
5 5
5 6 1 10 2
5 1000000
1000000000000 1000000000000 1000000000000 1000000000000 1000000000000
3 1
0 0 2
"""
) == """YES
YES
YES
NO
NO
YES
NO"""

# minimum size, connectable
assert run(
"""1
2 1
10 0
"""
) == "YES"

# minimum size, not connectable
assert run(
"""1
2 5
0 0
"""
) == "NO"

# all equal values
assert run(
"""1
4 1
5 5 5 5
"""
) == "YES"

# city 1 cannot start growing
assert run(
"""1
3 1
0 0 2
"""
) == "NO"

# large value boundary
assert run(
"""1
2 1000000
1000000000000 1000000000000
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 10 0` | YES | Minimum valid instance |
| `2 5 / 0 0` | NO | Minimum invalid instance |
| All values equal to 5 | YES | Greedy ordering does not matter |
| `0 0 2` | NO | Component containing city 1 cannot begin growing |
| Large $10^{12}$ values | YES | Correct handling of 64-bit scale numbers |

## Edge Cases

Consider:

```
1
3 1
0 0 2
```

Initially $S=0$. The only gains are $-2$ and $-1$. After sorting, the first candidate still satisfies $S+gain<0$. The algorithm immediately returns NO. No edge can be added in reality either, so the answer is correct.

Consider:

```
1
2 1
1 1
```

We start with $S=1$. The second city has gain $1-2=-1$. Since $1+(-1)=0$, the merge is allowed. The algorithm accepts and outputs YES. This catches a common off-by-one mistake where someone uses `<=` instead of `<`.

Consider:

```
1
4 10
0 20 15 10
```

The initial component has zero population. A careless solution might reject immediately. The algorithm instead checks the cities in gain order. City $2$ has gain $0$, making the first merge possible. After that the component grows and the remaining cities become reachable. The correct answer is YES.

Consider:

```
1
5 5
5 6 1 10 2
```

The best-looking city by population is city $4$, but it is not initially attachable. Sorting by gain correctly prioritizes the cities that can actually be merged. The process eventually gets stuck, and the algorithm outputs NO, matching the official answer.
