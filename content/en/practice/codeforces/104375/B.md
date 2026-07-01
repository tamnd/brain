---
title: "CF 104375B - Bucket storing"
description: "We are given a situation where coffee is first packed into several identical small containers. Each small container always holds exactly $K$ units of coffee, and there are $N$ such containers. So the total amount of coffee is simply $N times K$."
date: "2026-07-01T17:26:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104375
codeforces_index: "B"
codeforces_contest_name: "2023 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 104375
solve_time_s: 64
verified: true
draft: false
---

[CF 104375B - Bucket storing](https://codeforces.com/problemset/problem/104375/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a situation where coffee is first packed into several identical small containers. Each small container always holds exactly $K$ units of coffee, and there are $N$ such containers. So the total amount of coffee is simply $N \times K$.

This coffee must then be repacked into larger containers, where each large container can hold at most $L$ units. The goal is to determine how many large containers are required if we pack optimally, meaning we fill each large container as much as possible before using the next one.

So the task reduces to computing how many capacity-$L$ bins are needed to store a total of $N \cdot K$ units.

The constraints are small: $N, K, L \leq 1000$. This immediately tells us that the total amount of coffee is at most $10^6$, so even a simulation over units or simple arithmetic will be fast enough. Anything up to linear time in the input size or even in the total amount of coffee is acceptable, but we can clearly aim for an $O(1)$ arithmetic solution.

A subtle edge case appears when the total amount is exactly divisible by $L$. For example, if $N=2, K=3, L=6$, the total is $6$, and we need exactly one bucket. A naive integer division approach must ensure it correctly handles both divisible and non-divisible cases by rounding up.

Another corner case is when $L = K$. Then each large bucket holds exactly what one small bucket holds, and the answer becomes exactly $N$. If an implementation mistakenly performs integer division without considering total aggregation, it might incorrectly collapse structure, but here the correct reasoning is still purely total-based.

## Approaches

A straightforward way to think about this is to simulate the process of filling large buckets one unit at a time. We take the total coffee $N \cdot K$, repeatedly subtract $L$, and count how many times we do so. This is correct because each subtraction represents filling one large bucket.

However, this approach becomes inefficient in the worst case. If $N \cdot K$ is large and $L = 1$, we would perform up to $10^6$ iterations. While still borderline acceptable, it is unnecessary given the structure of the problem.

The key observation is that we are essentially partitioning a fixed quantity into groups of size $L$. This is exactly integer division with rounding up. Instead of simulating, we directly compute the ceiling of $\frac{N \cdot K}{L}$. This captures both full buckets and any partially filled final bucket in one expression.

The transition from simulation to arithmetic comes from recognizing that nothing changes during the process, only the total matters. Once we aggregate all coffee into a single value, the internal structure of how it was originally packed is irrelevant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(NK)$ | $O(1)$ | Too slow in worst case |
| Optimal Arithmetic | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the values $N$, $K$, and $L$. These define the number of small containers, their capacity, and the capacity of large containers.
2. Compute the total amount of coffee as $T = N \cdot K$. This step collapses the entire initial configuration into a single quantity, since only total mass matters for repacking.
3. Compute how many full large containers fit into $T$, which is $T // L$.
4. Check whether there is a remainder $T \bmod L$. If there is any leftover coffee, one additional large container is needed to store it.
5. Output $T // L + (1 \text{ if } T \bmod L \neq 0 \text{ else } 0)$.

### Why it works

The process of filling large containers depends only on total volume. Each container independently holds up to $L$ units, so any optimal packing strategy will fill containers completely whenever possible. After extracting as many full groups of size $L$ as possible, any remaining positive amount must occupy exactly one additional container. This guarantees the formula computes the minimal number of containers required.

## Python Solution

```python
import sys
input = sys.stdin.readline

N, K, L = map(int, input().split())

total = N * K

ans = total // L
if total % L != 0:
    ans += 1

print(ans)
```

The solution first compresses the input into a single total value. This avoids simulating any packing process. The integer division gives the number of completely filled large buckets, while the conditional increment handles the leftover case, ensuring correct ceiling behavior.

A common mistake is forgetting the remainder case and printing only `total // L`. That undercounts whenever the total is not an exact multiple of $L$.

## Worked Examples

### Example 1

Input:

```
2 3 6
```

Here $T = 2 \times 3 = 6$.

| Step | Total T | T // L | T % L | Answer |
| --- | --- | --- | --- | --- |
| Compute total | 6 | - | - | - |
| Divide by L | 6 | 1 | 0 | 1 |

The total exactly fills one large bucket, so no remainder appears. This confirms that exact divisibility produces no extra bucket.

### Example 2

Input:

```
5 3 4
```

Here $T = 5 \times 3 = 15$.

| Step | Total T | T // L | T % L | Answer |
| --- | --- | --- | --- | --- |
| Compute total | 15 | - | - | - |
| Divide by L | 15 | 3 | 3 | 4 |

Three full buckets of size 4 account for 12 units, leaving 3 units, which requires a fourth bucket. This demonstrates how the ceiling effect appears when there is a remainder.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a few arithmetic operations are performed regardless of input size |
| Space | $O(1)$ | No additional data structures are used |

The constraints are small enough that even a simulation would pass, but the direct formula ensures constant-time behavior and avoids unnecessary iteration.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    N, K, L = map(int, input().split())
    total = N * K
    ans = total // L
    if total % L != 0:
        ans += 1
    return str(ans)

# provided samples
assert run("2 3 6\n") == "1", "sample 1"
assert run("5 3 4\n") == "4", "sample 2"
assert run("1000 500 1000\n") == "500", "sample 3"

# custom cases
assert run("1 1 1\n") == "1", "minimum case"
assert run("1 1000 1000\n") == "1", "exact fit large bucket"
assert run("3 2 10\n") == "1", "fits into single bucket"
assert run("10 1 3\n") == "4", "remainder case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 | smallest boundary case |
| 1 1000 1000 | 1 | exact division at max capacity |
| 3 2 10 | 1 | multiple small buckets fit in one large |
| 10 1 3 | 4 | ceiling behavior with remainder |

## Edge Cases

When $N = 1, K = 1, L = 1$, the total is exactly 1 and the algorithm computes $1 // 1 = 1$, with no remainder. The answer correctly becomes 1, showing the base case behaves correctly.

When the total is smaller than $L$, for example $N=3, K=2, L=10$, the total is 6. The division gives 0 full buckets and a remainder of 6, triggering the extra bucket. The algorithm outputs 1, which matches the requirement that even small amounts still require one container.

When the total is exactly divisible, such as $N=1000, K=500, L=1000$, the total is 500000. The division gives 500 full buckets and zero remainder, so no extra bucket is added. This confirms that the algorithm does not overcount in clean division cases.
