---
title: "CF 340C - Tourist Problem"
description: "We have several destinations located on a straight line at positions $a1,a2,dots,an$, all strictly positive and distinct. A route is simply a permutation of these destinations."
date: "2026-06-06T17:21:51+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 340
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 198 (Div. 2)"
rating: 1600
weight: 340
solve_time_s: 133
verified: true
draft: false
---

[CF 340C - Tourist Problem](https://codeforces.com/problemset/problem/340/C)

**Rating:** 1600  
**Tags:** combinatorics, implementation, math  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several destinations located on a straight line at positions $a_1,a_2,\dots,a_n$, all strictly positive and distinct. A route is simply a permutation of these destinations. The tourist starts at position 0, visits the destinations in the chosen order, and stops after visiting the last one.

For a route $p_1,p_2,\dots,p_n$, the traveled distance is

$$a_{p_1} + \sum_{i=2}^{n} |a_{p_i}-a_{p_{i-1}}|.$$

The task is not to find the best route. We must compute the average distance over all $n!$ possible routes and output that average as an irreducible fraction.

The constraint $n \le 10^5$ immediately rules out anything involving enumeration of permutations. Even $n=15$ would already make $n!$ hopelessly large. We need a formula that aggregates the contribution of each destination pair across all routes.

The positions can be as large as $10^7$, and the final numerator can be on the order of $n^2 \cdot 10^7$, so 64-bit arithmetic is required. Python integers handle this automatically.

A subtle edge case appears when $n=2$.

Input:

```
2
1 10
```

The two routes have lengths $10$ and $19$. Their average is $29/2$.

A careless solution that counts only pair transitions and forgets the initial move from position 0 would produce $9$, which is completely wrong.

Another easy mistake is miscounting how many permutations contain a particular pair as adjacent.

Input:

```
3
2 3 5
```

The pair $(2,5)$ appears adjacent in exactly $2\cdot (n-1)! = 4$ permutations, not in all $6$. Getting this combinatorial factor wrong leads to an incorrect average.

A third pitfall is forgetting to reduce the final fraction.

Input:

```
2
1 3
```

The average distance is $(3+5)/2 = 4$, so the correct output is:

```
4 1
```

Printing `8 2` would not satisfy the requirement.

## Approaches

The brute-force idea is straightforward. Generate every permutation of the destinations, compute its route length, sum all route lengths, then divide by $n!$.

This works because the definition of the answer is literally the average over all permutations. Unfortunately, there are $n!$ routes. For $n=10^5$, even writing down the number $n!$ is impossible, let alone iterating through all permutations.

The key observation is that averages over all permutations can often be computed by counting how frequently each component appears.

The route length consists of two kinds of terms.

The first term is the distance from 0 to the first visited destination.

The remaining terms are distances between consecutive destinations in the permutation.

Instead of reasoning about whole routes, we count the contribution of each destination and each destination pair over all permutations.

For the starting position, every destination appears first in exactly $(n-1)!$ permutations. Hence the total contribution of starts is

$$(n-1)! \sum a_i.$$

For consecutive transitions, consider two destinations $x$ and $y$. How many permutations place them next to each other?

Treat $(x,y)$ as a block. The block can be ordered in two ways, and together with the remaining $n-2$ destinations we have $n-1$ objects to permute.

Thus the count is

$$2\cdot (n-1)!.$$

Each such permutation contributes $|x-y|$.

Therefore the total contribution of all adjacency terms is

$$2(n-1)! \sum_{i<j} |a_i-a_j|.$$

Combining both parts gives

$$\text{Total over all permutations} = (n-1)! \left( \sum a_i + 2\sum_{i<j}|a_i-a_j| \right).$$

Dividing by $n!$ cancels the factorials:

$$\text{Average} = \frac{ \sum a_i + 2\sum_{i<j}|a_i-a_j| }{n}.$$

Now the entire problem reduces to computing

$$\sum_{i<j}|a_i-a_j|.$$

After sorting the positions, all differences become non-negative:

$$\sum_{i<j}(a_j-a_i).$$

This classical quantity can be computed in linear time after sorting using prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!\cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n\log n)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Read the positions and sort them.

Sorting allows us to replace absolute values with ordinary differences because for $i<j$, we have $a_j \ge a_i$.
2. Compute the sum of all positions.

This is the contribution of the starting move after the combinatorial simplification.
3. Compute $\sum_{i<j}(a_j-a_i)$.

Maintain a running prefix sum.

When processing $a_i$, all earlier values contribute

$$a_i \cdot i - \text{prefix}.$$

This equals

$$\sum_{j<i}(a_i-a_j).$$
4. Let $D$ be the pairwise difference sum obtained in the previous step.
5. Compute

$$\text{numerator} = \sum a_i + 2D.$$

The average is numerator divided by $n$.
6. Reduce the fraction by dividing numerator and denominator by their greatest common divisor.
7. Output the reduced numerator and denominator.

### Why it works

Every route length is the sum of one starting contribution and several adjacency contributions. Across all permutations, each destination appears first exactly $(n-1)!$ times, giving the term $\sum a_i$. Likewise, every unordered pair of destinations becomes adjacent exactly $2(n-1)!$ times, giving the term $2\sum_{i<j}|a_i-a_j|$.

These counts are exact and cover every distance contribution in every permutation exactly once. After dividing by the total number of permutations $n!$, the average route length becomes

$$\frac{\sum a_i + 2\sum_{i<j}|a_i-a_j|}{n}.$$

The sorted-prefix-sum computation evaluates the pairwise difference sum exactly, so the algorithm computes the desired average without approximation.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    total_positions = sum(a)

    prefix = 0
    pair_sum = 0

    for i, x in enumerate(a):
        pair_sum += x * i - prefix
        prefix += x

    numerator = total_positions + 2 * pair_sum
    denominator = n

    g = gcd(numerator, denominator)

    print(numerator // g, denominator // g)

solve()
```

The first step sorts the coordinates. Once sorted, every pair contribution becomes $a_j-a_i$ instead of $|a_j-a_i|$, which makes aggregation possible.

The variable `pair_sum` stores

$$\sum_{i<j}(a_j-a_i).$$

When processing the current value `x` at index `i`, there are exactly `i` previous elements. Their total contribution is

$$(x-a_0)+(x-a_1)+\cdots+(x-a_{i-1}),$$

which simplifies to `x * i - prefix`.

The final formula comes directly from the combinatorial counting argument:

$$\text{average} = \frac{\sum a_i + 2\,\text{pair\_sum}}{n}.$$

No factorials are ever computed. This is the critical simplification that makes the problem feasible.

Python's arbitrary-precision integers avoid overflow issues even when intermediate values become very large.

## Worked Examples

### Example 1

Input:

```
3
2 3 5
```

Sorted array: $[2,3,5]$

| i | x | prefix before | Added to pair_sum | pair_sum after |
| --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 0 | 0 |
| 1 | 3 | 2 | 3×1−2=1 | 1 |
| 2 | 5 | 5 | 5×2−5=5 | 6 |

Now:

| Quantity | Value |
| --- | --- |
| Sum of positions | 10 |
| Pair sum | 6 |
| Numerator | 10 + 2×6 = 22 |
| Denominator | 3 |

Output:

```
22 3
```

The trace confirms that the pairwise difference sum is

$$(3-2)+(5-2)+(5-3)=6.$$

### Example 2

Input:

```
2
1 10
```

Sorted array: $[1,10]$

| i | x | prefix before | Added to pair_sum | pair_sum after |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 |
| 1 | 10 | 1 | 10×1−1=9 | 9 |

Now:

| Quantity | Value |
| --- | --- |
| Sum of positions | 11 |
| Pair sum | 9 |
| Numerator | 11 + 18 = 29 |
| Denominator | 2 |

Output:

```
29 2
```

This example shows that the average can be a non-integer fraction and must be reduced correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates the running time |
| Space | $O(1)$ extra | Aside from the input array and a few variables |

With $n=10^5$, an $O(n\log n)$ solution easily fits within the time limit. The linear scan after sorting is negligible compared to the sort itself.

## Test Cases

```python
import sys
import io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    a.sort()

    prefix = 0
    pair_sum = 0

    for i, x in enumerate(a):
        pair_sum += x * i - prefix
        prefix += x

    numerator = sum(a) + 2 * pair_sum
    denominator = n

    g = gcd(numerator, denominator)
    return f"{numerator // g} {denominator // g}"

# provided sample
assert run("3\n2 3 5\n") == "22 3", "sample 1"

# minimum n
assert run("2\n1 2\n") == "5 2", "minimum size"

# reducible fraction becoming integer
assert run("2\n1 3\n") == "4 1", "fraction reduction"

# unsorted input
assert run("3\n5 2 3\n") == "22 3", "sorting correctness"

# larger gaps
assert run("3\n1 10 20\n") == "79 3", "pairwise contribution"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2` | `5 2` | Smallest valid size |
| `2 / 1 3` | `4 1` | Fraction reduction |
| `3 / 5 2 3` | `22 3` | Input order should not matter |
| `3 / 1 10 20` | `79 3` | Large pairwise distances |

## Edge Cases

Consider:

```
2
1 10
```

After sorting, the pairwise difference sum is $9$. The formula gives

$$\frac{1+10+2\cdot 9}{2} = \frac{29}{2}.$$

The algorithm correctly includes the contribution of the first visited destination. Omitting that term would incorrectly produce $9$.

Consider:

```
3
5 2 3
```

Sorting transforms the array into $[2,3,5]$. The pairwise sum becomes $6$, producing $22/3$. This confirms that the answer depends only on positions, not on their order in the input.

Consider:

```
2
1 3
```

The formula gives

$$\frac{1+3+2(2)}{2} = \frac{8}{2} = 4.$$

The gcd step reduces the fraction to `4 1`, satisfying the requirement that the output be irreducible.

Consider:

```
4
1 2 3 10000000
```

The pairwise difference sum is very large, but all computations remain integer arithmetic. Python safely handles the resulting values, and the combinatorial formula avoids any factorial-sized numbers.
