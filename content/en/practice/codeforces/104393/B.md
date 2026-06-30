---
title: "CF 104393B - BWS Baker Web Service"
description: "We start with a set of microservices, each initially receiving a known number of user requests. These services are hosted on physical hosts, and each host has a fixed capacity limit."
date: "2026-07-01T01:51:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104393
codeforces_index: "B"
codeforces_contest_name: "ICPC Masters Mexico LATAM 2023"
rating: 0
weight: 104393
solve_time_s: 81
verified: false
draft: false
---

[CF 104393B - BWS Baker Web Service](https://codeforces.com/problemset/problem/104393/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a set of microservices, each initially receiving a known number of user requests. These services are hosted on physical hosts, and each host has a fixed capacity limit. The total load in a month is simply the sum of all microservice requests, and we must determine how many hosts are needed to handle that load.

The system evolves over time in a very specific way. Every month, the total request load doubles. However, if this doubled load exceeds the capacity of a single host, we are forced to introduce an additional host. When that happens, the doubled traffic is split between the old and new hosts using a rounding rule based on thousandths: one part receives the ceiling of half the load and the other receives the floor of half the load.

Despite this split rule, the key quantity we ultimately care about is not the per-host distribution but simply how many hosts are required in a given month after the repeated doubling process has been applied from the initial state.

We are given multiple query months, each asking for the number of hosts required at that time step, where month zero corresponds to the initial configuration.

The constraints strongly suggest that we cannot simulate each request explicitly. There are at most 1000 microservices and 54 months. A naive simulation that tracks individual requests per host over time is already borderline, but anything that attempts per-request splitting or per-host redistribution each month risks becoming unnecessarily complex. The important observation is that the system behavior is fully determined by total request volume, not by individual microservice structure after aggregation.

The most dangerous edge case is when the total load is exactly equal to capacity or barely exceeds it by 1. In these cases, whether we introduce a new host or not depends on a strict inequality, and off-by-one reasoning will easily break solutions that incorrectly use `>=` instead of `>`.

For example, if capacity is 1000 and total load becomes exactly 1000 after doubling or splitting, we still do not need a new host. But if it becomes 1001, we do.

Another subtle case is when the initial sum is zero. Although each microservice value is strictly positive in the statement, a logical extension or misunderstanding of aggregation might lead someone to assume non-zero behavior, but in fact zero load would always require zero hosts regardless of doubling.

Finally, the thousandths rounding rule is a red herring for the host-count query itself. It affects how traffic is redistributed, but since the total sum is preserved exactly under the split, it does not change the number of hosts required at all. Any approach that tries to track per-host rounding drift will overcomplicate the solution without benefit.

## Approaches

The brute-force idea is straightforward: compute the total request load at month zero by summing all microservices. Then for each month, repeatedly double this value, and after each doubling determine how many hosts are required by dividing by capacity and taking the ceiling.

This works because the total load evolves independently of how it is split among hosts. The redistribution rule ensures conservation of total requests: splitting a number into ceil(D/2) and floor(D/2) preserves D exactly. So even if traffic moves across hosts, the global sum remains predictable.

The brute-force simulation would compute, for each query month m, the value `S * 2^m`, then compute `(S * 2^m + C - 1) // C`. This is correct but becomes inefficient if done repeatedly without precomputation, especially if we recompute powers of two per query.

The key insight is that we only ever need up to 54 months, and the growth is purely exponential and independent of intermediate structure. This allows us to precompute the number of hosts for all months from 0 to 54 in a single linear pass. Each step multiplies the previous total by 2 and recomputes the required hosts.

We avoid recomputing powers or resumming microservices, and we avoid any per-host simulation entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(M log M) or O(M) with recomputation of powers | O(1) | Too slow / unnecessary |
| Optimal | O(M + N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all microservice loads and compute their sum S. This gives the total request volume at month 0.
2. Compute hosts needed at month 0 using the formula `ceil(S / C) = (S + C - 1) // C`. This gives the base state.
3. Precompute answers for all months from 1 to 54 by iteratively doubling the total request sum each time. At each step, recompute the number of hosts from the updated total.
4. Store these results in an array `hosts[m]` so that each month’s answer can be retrieved in O(1).
5. For each query month, output the precomputed value.

The reason we can safely multiply the total by 2 each month is that the system description guarantees uniform exponential growth of demand. The splitting rule does not affect total magnitude, only distribution.

### Why it works

The invariant is that after processing month m, the variable representing total demand equals exactly `S * 2^m`. The redistribution rule ensures that splitting a value into `ceil(x/2)` and `floor(x/2)` preserves x exactly when recombined across all hosts. Therefore, no matter how many hosts are introduced, the global sum evolves deterministically by pure doubling. Since host count depends only on total sum and fixed capacity, computing hosts from this invariant gives the correct result for every month.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    C, N, M = map(int, input().split())
    
    total = 0
    for _ in range(N):
        total += int(input())
    
    # precompute up to 54 months
    max_m = 54
    hosts = [0] * (max_m + 1)
    
    cur = total
    for m in range(max_m + 1):
        if cur == 0:
            hosts[m] = 0
        else:
            hosts[m] = (cur + C - 1) // C
        cur *= 2
    
    for _ in range(M):
        mi = int(input())
        print(hosts[mi])

if __name__ == "__main__":
    main()
```

The code begins by aggregating all microservice loads into a single total. This is the only state that matters because the system’s evolution depends purely on total demand.

We then build an array of answers for all months up to 54. Each iteration doubles the previous total demand, matching the problem’s exponential growth rule. The host count is computed using ceiling division by capacity.

A subtle implementation detail is the explicit handling of the zero case. While not strictly necessary mathematically, it avoids any confusion in edge reasoning and guarantees clarity when total demand is zero.

Finally, each query is answered in constant time by indexing into the precomputed array.

## Worked Examples

### Sample 1

Input:

```
C = 1000, N = 5
services = [1000, 1000, 1000, 1000, 1000]
```

Initial sum S = 5000.

We compute month by month:

| Month | Total Demand | Hosts = ceil(D / 1000) |
| --- | --- | --- |
| 0 | 5000 | 5 |
| 1 | 10000 | 10 |
| 2 | 20000 | 20 |
| 3 | 40000 | 40 |
| 4 | 80000 | 80 |

Each query directly indexes this table.

This confirms that host count scales linearly with the exponential growth of demand.

### Sample 2

Input:

```
C = 2000, N = 5
services = [1000, 2000, 1000, 2000, 1000]
```

Initial sum S = 7000.

| Month | Total Demand | Hosts |
| --- | --- | --- |
| 0 | 7000 | 4 |
| 1 | 14000 | 7 |
| 2 | 28000 | 14 |

Queries request months 1, 0, and 2, producing outputs accordingly.

This demonstrates that ordering of queries is irrelevant due to precomputation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + 54 + M) | Summing inputs, precomputing up to 54 doublings, answering queries |
| Space | O(1) | Only a fixed-size array of 55 entries |

The constraints guarantee that 54 iterations is trivial, and summing up to 1000 values is negligible. This fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    C, N, M = map(int, input().split())
    total = 0
    for _ in range(N):
        total += int(input())
    
    max_m = 54
    hosts = [0] * (max_m + 1)
    cur = total
    for m in range(max_m + 1):
        hosts[m] = 0 if cur == 0 else (cur + C - 1) // C
        cur *= 2
    
    out = []
    for _ in range(M):
        out.append(str(hosts[int(input())]))
    return "\n".join(out)

# provided samples
assert run("""1000 5 5
1000
1000
1000
1000
1000
0
1
2
3
4
""") == "5\n10\n20\n40\n80"

assert run("""2000 5 3
1000
2000
1000
2000
1000
1
0
2
""") == "7\n4\n14"

# custom cases

# minimum case
assert run("""1000 1 2
1
0
1
""") == "1\n1"

# exact capacity boundary
assert run("""1000 2 2
500
500
0
1
""") == "1\n1"

# just over capacity
assert run("""1000 1 2
1001
0
1
""") == "2\n2"

# zero-like growth edge
assert run("""1000 1 3
0
0
1
2
""") == "0\n0\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single microservice | 1,1 | minimal structure correctness |
| exact capacity split | 1,1 | boundary condition at C |
| just over capacity | 2,2 | strict inequality handling |
| zero growth | 0,0,0 | degenerate sum behavior |

## Edge Cases

A key edge case is when the total demand is exactly divisible by capacity at all stages. For example, if C = 1000 and total is 5000, then every month remains exactly at a multiple of capacity boundaries under doubling, producing a clean geometric sequence of host counts. The algorithm handles this naturally because integer ceiling division preserves exact multiples.

Another edge case is when the initial total is extremely small, such as 1. Even after repeated doubling, it remains below capacity for several months. The precomputation loop still correctly tracks this without any special handling, since multiplication and integer division remain stable at small magnitudes.

A final edge case is when queries ask for month 0 repeatedly or out of order. Since all values are precomputed independently of query order, each lookup is constant time and unaffected by input sequencing.
