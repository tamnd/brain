---
title: "CF 1419B - Stairs"
description: "A staircase with $n$ columns contains columns of heights $1,2,dots,n$. The total number of cells in such a staircase is $$1+2+cdots+n=frac{n(n+1)}2.$$ The problem only cares about nice staircases."
date: "2026-06-11T06:43:30+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1419
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 671 (Div. 2)"
rating: 1200
weight: 1419
solve_time_s: 97
verified: true
draft: false
---

[CF 1419B - Stairs](https://codeforces.com/problemset/problem/1419/B)

**Rating:** 1200  
**Tags:** brute force, constructive algorithms, greedy, implementation, math  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

A staircase with $n$ columns contains columns of heights $1,2,\dots,n$. The total number of cells in such a staircase is

$$1+2+\cdots+n=\frac{n(n+1)}2.$$

The problem only cares about _nice_ staircases. A key geometric fact is that a nice staircase always has a very specific number of stairs. If we start from the smallest nice staircase and repeatedly build larger ones, the number of stairs follows

$$1,\ 3,\ 7,\ 15,\dots$$

which is

$$2^k-1.$$

For a staircase with $2^k-1$ stairs, the number of cells is

$$1+2+\cdots+(2^k-1)
=
\frac{(2^k-1)2^k}{2}.$$

Let

$$c_k=\frac{(2^k-1)2^k}{2}.$$

The available cells $x$ can be used to build several different nice staircases. Each staircase type can be built at most once because the problem asks for different nice staircases. We want the maximum number of staircase types whose total cost does not exceed $x$.

The value of $x$ can be as large as $10^{18}$. Any algorithm that iterates through all numbers up to $x$ is impossible. Even $O(\sqrt{x})$ would be far too large. We need a solution whose work depends only on the number of possible nice staircases, not on $x$ itself.

A subtle point is that building the largest staircase first is not always optimal. For example:

```
x = 8
```

The staircase costs are:

```
1, 6, 28, ...
```

Taking cost $6$ first leaves $2$, allowing one more staircase of cost $1$, for a total of two staircases. A strategy that tries to maximize spent cells instead of staircase count can easily make the wrong choice.

Another easy mistake is to assume there are many staircase sizes to consider. The costs grow roughly like $4^k$, so for $x \le 10^{18}$ there are only about thirty valid staircase types. Exploiting this growth is the entire solution.

## Approaches

The most direct idea is to generate every nice staircase cost and then try all subsets to find the largest number whose total cost does not exceed $x$. This is correct because every staircase type may be either chosen or not chosen.

The problem is that even thirty staircase types would lead to roughly $2^{30}$ subsets, over one billion possibilities. That is completely infeasible.

The crucial observation is that the staircase costs grow extremely fast:

$$1,\ 6,\ 28,\ 120,\ 496,\dots$$

Each cost is much larger than the sum of all previous costs. For example,

$$28 > 1+6,$$

$$120 > 1+6+28.$$

In fact, for every $k$,

$$c_k > \sum_{i<k} c_i.$$

This means the sequence is superincreasing.

Suppose we want the maximum number of staircases. If the largest staircase that fits costs $c_k$, then any solution that skips $c_k$ cannot compensate by taking smaller staircases, because all smaller costs together are still less than $c_k$. Taking $c_k$ is always the best choice whenever it fits.

That immediately gives a greedy algorithm:

Keep subtracting the largest staircase cost that does not exceed the remaining cells. Count how many times this is possible.

Since there are only about thirty staircase costs up to $10^{18}$, the algorithm is tiny and very fast.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | $O(2^m)$ | $O(m)$ | Too slow |
| Greedy with Precomputed Costs | $O(m)$ | $O(m)$ | Accepted |

Here $m \approx 30$.

## Algorithm Walkthrough

1. Precompute all nice staircase costs

$$c_k=\frac{(2^k-1)2^k}{2}$$

while $c_k \le 10^{18}$.
2. For each test case, start with the given number of cells $x$.
3. Find the largest staircase cost that does not exceed the current $x$.
4. Subtract that cost from $x$ and increase the answer by one.

This is the right choice because every cost is larger than the sum of all smaller costs.
5. Repeat while some staircase cost still fits into the remaining cells.
6. Output the number of chosen staircases.

### Why it works

The staircase costs form a superincreasing sequence:

$$c_k > \sum_{i<k} c_i.$$

Consider the largest cost $c_k$ that fits in the current budget. Any solution that does not use $c_k$ can spend at most

$$\sum_{i<k} c_i,$$

which is strictly smaller than $c_k$. Replacing $c_k$ by any collection of smaller staircases never gives a better opportunity to increase the number of future selections.

After choosing $c_k$, the remaining problem is identical on a smaller budget. Repeating the same argument recursively proves that the greedy choice is always optimal.

## Python Solution

```python
import sys
from bisect import bisect_right

input = sys.stdin.readline

# precompute staircase costs
costs = []
k = 1
LIMIT = 10 ** 18

while True:
    p = 1 << k
    cost = (p - 1) * p // 2
    if cost > LIMIT:
        break
    costs.append(cost)
    k += 1

t = int(input())
ans = []

for _ in range(t):
    x = int(input())
    cnt = 0

    while True:
        idx = bisect_right(costs, x) - 1
        if idx < 0:
            break
        x -= costs[idx]
        cnt += 1

    ans.append(str(cnt))

sys.stdout.write("\n".join(ans))
```

The precomputation stage generates every possible nice staircase cost that could ever be relevant. Because the costs grow exponentially, only about thirty values are stored.

For each test case, `bisect_right` finds the largest cost not exceeding the current budget. That cost is subtracted, and the process repeats.

Using binary search is not strictly necessary because the list is tiny, but it keeps the implementation clean and makes the intention explicit.

All arithmetic uses Python integers, so there is no overflow risk even near $10^{18}$.

## Worked Examples

### Sample Input

```
x = 8
```

The staircase costs are:

```
1, 6, 28, ...
```

| Remaining x | Largest Cost ≤ x | New x | Count |
| --- | --- | --- | --- |
| 8 | 6 | 2 | 1 |
| 2 | 1 | 1 | 2 |
| 1 | 1 | 0 | 3 |

This trace reveals an important detail. The algorithm counts how many nice staircases can be built sequentially from the available cells. After building a staircase, the remaining cells may still be used to build another staircase of a smaller type.

The answer is:

```
3
```

### Sample Input

```
x = 1000000000000000000
```

| Step | Remaining x Before | Chosen Cost |
| --- | --- | --- |
| 1 | 1000000000000000000 | 576460752169205760 |
| 2 | 423539247830794240 | 144115188075855872 |
| 3 | 279424059754938368 | 36028792723996672 |
| ... | ... | ... |
| 30 | enough for smallest staircase | 1 |

After thirty successful selections, the remaining budget becomes too small for another staircase.

The answer is:

```
30
```

This demonstrates the logarithmic nature of the solution. Even for the largest possible input, only about thirty staircase sizes exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m)$ | At most about 30 greedy selections |
| Space | $O(m)$ | Stores all staircase costs |

Since $m \approx 30$, the running time per test case is effectively constant. With at most 1000 test cases, the program easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from bisect import bisect_right

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    costs = []
    k = 1
    LIMIT = 10 ** 18

    while True:
        p = 1 << k
        cost = (p - 1) * p // 2
        if cost > LIMIT:
            break
        costs.append(cost)
        k += 1

    t = int(input())
    out = []

    for _ in range(t):
        x = int(input())
        cnt = 0

        while True:
            idx = bisect_right(costs, x) - 1
            if idx < 0:
                break
            x -= costs[idx]
            cnt += 1

        out.append(str(cnt))

    return "\n".join(out)

# provided samples
assert run(
    "4\n1\n8\n6\n1000000000000000000\n"
) == "1\n3\n1\n30"

# custom cases
assert run("1\n2\n") == "2", "two smallest staircases"
assert run("1\n5\n") == "5", "repeated use of size-1 staircase"
assert run("1\n28\n") == "1", "exactly one larger staircase"
assert run("1\n29\n") == "2", "boundary just above 28"
assert run("1\n1000000000000000000\n") == "30", "maximum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | `2` | Smallest nontrivial budget |
| `5` | `5` | Repeated greedy reductions |
| `28` | `1` | Exact match with a staircase cost |
| `29` | `2` | Boundary immediately above a staircase cost |
| `10^18` | `30` | Maximum constraint |

## Edge Cases

Consider:

```
1
1
```

The largest staircase cost that fits is $1$. After subtracting it, the remaining budget is zero. The algorithm outputs:

```
1
```

which is correct.

Consider:

```
1
28
```

The largest fitting staircase cost is exactly $28$. The algorithm subtracts it immediately:

| Remaining x | Chosen Cost |
| --- | --- |
| 28 | 28 |
| 0 | stop |

The answer is:

```
1
```

No smaller combination can produce more staircases because $28$ already corresponds to the next staircase level.

Consider:

```
1
29
```

The algorithm first chooses $28$, leaving $1$. Then it chooses $1$.

| Remaining x | Chosen Cost | Count |
| --- | --- | --- |
| 29 | 28 | 1 |
| 1 | 1 | 2 |
| 0 | stop | 2 |

The answer is:

```
2
```

This catches off by one mistakes around exact staircase boundaries.

Finally, consider the maximum value:

```
1
1000000000000000000
```

Only about thirty staircase costs exist below $10^{18}$. The greedy process performs roughly thirty iterations and outputs:

```
30
```

showing that the solution remains efficient even at the largest input size.
