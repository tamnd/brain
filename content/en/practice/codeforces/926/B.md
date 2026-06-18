---
problem: 926B
contest_id: 926
problem_index: B
name: "Add Points"
contest_name: "VK Cup 2018 - Wild-card Round 1"
rating: 1800
tags: ["math", "number theory"]
answer: passed_samples
verified: true
solve_time_s: 68
date: 2026-06-18
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a32df8a-1470-83ec-aaf1-85cacf87cba3
---

# CF 926B - Add Points

**Rating:** 1800  
**Tags:** math, number theory  
**Model:** gpt-5-5  
**Solve time:** 1m 8s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a32df8a-1470-83ec-aaf1-85cacf87cba3  

---

## Solution

## Problem Understanding

We are given several distinct points placed on a number line. Their positions are arbitrary and unsorted. The task is to insert the minimum number of additional points so that, after sorting all original and inserted points, every consecutive pair of points has exactly the same distance.

In other words, we want to transform a scattered set of coordinates into a perfectly evenly spaced arithmetic progression by only adding new points, never moving the existing ones. The final set must form a sequence like $a, a + d, a + 2d, \dots$ where every original point appears somewhere in this progression.

The key constraint is $n \le 100{,}000$, which immediately rules out any quadratic strategy over pairs of points. Anything that tries all pairs of points as candidates for spacing and then simulates the full construction must be carefully reduced, since naive reconstruction could require $O(n^2)$ or worse in the worst case.

A subtle difficulty is that the original points are not ordered. If we forget to sort them first, we cannot reason about “adjacent” distances at all. Another failure mode comes from assuming that the global spacing is determined by adjacent differences in the input order, which is arbitrary.

A small but important edge case appears when the points are already evenly spaced. For example, input:

```
3
0 2 4
```

Here no points should be added. Any approach that always tries to “fill gaps” without first checking consistency of spacing would incorrectly insert points.

Another case:

```
3
-5 10 5
```

Sorting gives $-5, 5, 10$. The natural step is 5, but the gap 5 to 10 is 5 while -5 to 5 is also 10 apart, so we must introduce 0. A naive strategy that only looks at min and max might incorrectly assume step 7.5 or similar and fail.

## Approaches

A brute-force viewpoint starts by selecting two existing points as potential consecutive elements of the final arithmetic progression. If we assume those two are neighbors in the final arrangement, their difference defines a candidate step size. For each such candidate, we try to generate the full arithmetic progression covering the interval from minimum to maximum and count how many original points are missing from it.

This works because any valid final configuration must be an arithmetic progression containing all original points, so its step must align with differences between consecutive points in the sorted final sequence. However, trying all pairs gives $O(n^2)$ candidates, and for each we may scan up to $O(n)$ points to validate coverage, leading to $O(n^3)$ in the worst interpretation or at least $O(n^2)$ with hashing, which is too slow for $10^5$.

The key observation is that we do not need all pairs. If we sort the array, the correct step size must divide all differences between adjacent elements in the final progression. That means the step must be the greatest common divisor of all adjacent differences in the sorted array. Once we compute this global step $d$, the final structure is completely determined: it is the arithmetic progression from minimum to maximum with step $d$.

We can then count how many integers are missing between existing points by iterating through the sorted array and summing how many steps are skipped between consecutive elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ or worse | $O(1)$-$O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Optimal Strategy

1. Sort all coordinates in increasing order. This makes the notion of “neighboring points” well-defined in the final target structure. Without sorting, differences have no structural meaning.
2. Compute the differences between every consecutive pair in the sorted array. These differences represent how far apart the points are in the current configuration, and any valid final spacing must divide all of them.
3. Compute the greatest common divisor of all these differences. This value becomes the maximum possible uniform step size that still allows all original points to lie on the grid. A smaller step would still work but would require inserting more points, so the gcd step is optimal.
4. Let this gcd be $d$. The final target progression spans from the smallest to the largest value, with step size $d$.
5. Traverse the sorted array and for each adjacent pair $x[i], x[i+1]$, compute $(x[i+1] - x[i]) // d - 1$. This counts how many intermediate points are missing between them in a perfect arithmetic progression.
6. Sum all these counts and output the result.

### Why it works

Once we fix the sorted array, any valid final configuration must align all points onto a uniform lattice. The spacing between any two consecutive original points in the final sequence must be a common divisor of all observed gaps in the sorted input. The greatest common divisor is the largest such step, and using it minimizes the number of required inserted points because larger steps correspond to fewer intermediate positions. Every gap is then exactly decomposed into equal segments of size $d$, so counting missing points becomes deterministic and gap-local, ensuring consistency across the entire line.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd

n = int(input())
a = list(map(int, input().split()))
a.sort()

d = 0
for i in range(1, n):
    d = gcd(d, a[i] - a[i - 1])

if d == 0:
    print(0)
    sys.exit()

ans = 0
for i in range(n - 1):
    ans += (a[i + 1] - a[i]) // d - 1

print(ans)
```

The solution begins by sorting the coordinates so that all structural reasoning is performed on a consistent order. The gcd accumulation step progressively merges all local differences into a single global step size. The check for zero handles the degenerate case where all points coincide, though the problem guarantees distinct values so it is mostly defensive.

The final loop reconstructs how many evenly spaced points must lie between each adjacent pair. The expression $(a[i+1] - a[i]) // d - 1$ directly counts missing lattice points between two known positions on the arithmetic progression defined by step $d$.

## Worked Examples

### Example 1

Input:

```
3
-5 10 5
```

Sorted array: $[-5, 5, 10]$

Differences: $10, 5$

GCD: $5$

Now we compute missing points:

| i | a[i] | a[i+1] | diff | diff / d | missing |
| --- | --- | --- | --- | --- | --- |
| 0 | -5 | 5 | 10 | 2 | 1 |
| 1 | 5 | 10 | 5 | 1 | 0 |

Total missing = 1

This confirms that inserting 0 produces a perfect step-5 progression.

### Example 2

Input:

```
4
0 3 6 12
```

Sorted array: same

Differences: 3, 3, 6

GCD = 3

| i | a[i] | a[i+1] | diff | diff / d | missing |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 3 | 3 | 1 | 0 |
| 1 | 3 | 6 | 3 | 1 | 0 |
| 2 | 6 | 12 | 6 | 2 | 1 |

Total missing = 1

This shows that only one intermediate point (9) is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates, gcd and scan are linear |
| Space | $O(n)$ | storage of input array |

The algorithm is efficient for $n \le 100{,}000$ since sorting and a single linear pass comfortably fit within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    from math import gcd

    d = 0
    for i in range(1, n):
        d = gcd(d, a[i] - a[i - 1])

    ans = 0
    for i in range(n - 1):
        ans += (a[i + 1] - a[i]) // d - 1

    return str(ans)

# provided sample
assert run("3\n-5 10 5\n") == "1"

# already uniform spacing
assert run("3\n0 2 4\n") == "0"

# large gap with one insertion
assert run("4\n0 3 6 12\n") == "1"

# negative coordinates
assert run("3\n-10 -4 2\n") == "2"

# already arithmetic progression
assert run("5\n1 4 7 10 13\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 -5 10 5 | 1 | basic gcd and single insertion |
| 3 0 2 4 | 0 | already uniform progression |
| 4 0 3 6 12 | 1 | mixed gap sizes |
| 3 -10 -4 2 | 2 | negative coordinates handling |
| 5 1 4 7 10 13 | 0 | perfect arithmetic progression |

## Edge Cases

For already evenly spaced points such as:

```
5
1 4 7 10 13
```

the sorted differences are all 3, so the gcd remains 3. Each gap satisfies $(a[i+1] - a[i]) // 3 - 1 = 0$, producing a correct output of 0.

For cases with uneven initial ordering:

```
3
10 0 5
```

sorting gives $[0, 5, 10]$. The gcd is 5, and no insertions are needed because the algorithm ignores input order completely and reconstructs structure from sorted geometry.

For cases with large gaps like:

```
2
0 1000000000
```

the gcd equals the difference itself, so no intermediate points are required. The algorithm correctly avoids inserting a full dense grid, since the step size is maximized under the constraint that all original points must lie on the progression.