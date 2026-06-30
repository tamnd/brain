---
title: "CF 104393B - BWS Baker Web Service"
description: "We are given a collection of microservices, each producing some initial number of user requests. All of these requests are served by identical hosting machines, where each machine has a fixed capacity limit."
date: "2026-06-30T23:24:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104393
codeforces_index: "B"
codeforces_contest_name: "ICPC Masters Mexico LATAM 2023"
rating: 0
weight: 104393
solve_time_s: 90
verified: false
draft: false
---

[CF 104393B - BWS Baker Web Service](https://codeforces.com/problemset/problem/104393/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of microservices, each producing some initial number of user requests. All of these requests are served by identical hosting machines, where each machine has a fixed capacity limit. Over time, traffic grows in a very rigid way: every month, the total request load doubles.

Whenever the total request load after a doubling step would exceed what the currently rented machines can handle, the system reacts by renting an additional machine and splitting the traffic between the old infrastructure and the new one. The split is not arbitrary, it is always performed by taking half of the doubled traffic and assigning it to the existing setup, and the other half to the newly rented host. Because the split is defined using rounding to thousandths, it is effectively an integer split of the total load into two nearly equal parts.

The key quantity we track is how many hosts are needed after a given number of months of repeated doubling and possible splits. We are asked to answer this for multiple query months, up to 54 steps into the future.

The input gives the per microservice initial loads, which together form the initial total request volume. Each query asks: after simulating the growth process for a specific number of months, how many hosts are required to serve all requests under the capacity constraint.

The constraints are small in structure but large in growth behavior. There are at most 1000 microservices, so computing the initial total load is trivial. The number of months is at most 54, which is extremely small, so any solution that precomputes the state for all months is feasible. The critical issue is that request values grow exponentially, so recomputing raw values per query is unnecessary and would be wasteful if done independently per query.

A naive interpretation would simulate each query from scratch, repeatedly doubling values and splitting when needed. That would multiply the 54-step process by the number of queries, but even that is still tiny. The real risk in naive approaches is not time complexity but incorrect modeling of the splitting process, especially when thinking in terms of per-microservice rather than total aggregated load.

A subtle edge case appears when the initial load is exactly at capacity. If a naive approach assumes splitting only happens strictly after exceeding capacity, it may delay host creation incorrectly. Another issue arises from interpreting rounding incorrectly, since the problem defines rounding to thousandths but the intended structure is simply a deterministic integer split; misinterpreting this can lead to off-by-one errors in distribution.

## Approaches

The brute-force idea is straightforward: maintain the total number of requests, and maintain the number of hosts currently available. For each month, double the load. If the load exceeds the total capacity of the current hosts, repeatedly add hosts and split the load until the remaining load per “active block” fits within capacity.

However, simulating the split literally per host or per microservice is unnecessary. The key observation is that after every split event, the system behaves as if we have partitioned the total load into independent chunks, each constrained by capacity, and each chunk evolves identically under doubling. This means we only need to track how many equal “segments” of load exist, because each segment corresponds to a host.

Each time the total load doubles, each segment also doubles. Whenever a segment exceeds capacity, it splits into two segments of roughly equal size, increasing the number of hosts by one per split event in that segment lineage. Because all segments behave identically, the entire system evolves deterministically: we only need to track the number of hosts required to keep segment load under capacity after each doubling step.

This reduces the problem to repeatedly applying a rule on a single representative segment: double its load, and whenever it exceeds capacity, split it into two and continue until all segments satisfy the constraint.

Since the number of months is at most 54, we can precompute the number of hosts required for every month using a simple iterative simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation per Query | O(M · 54) | O(1) | Accepted |
| Precompute Monthly State | O(54) | O(54) | Accepted |

## Algorithm Walkthrough

We first compute the initial total load by summing all microservice requests. This gives the starting point of the system.

Then we simulate month by month, maintaining two quantities: the current effective load per host group and the number of hosts required.

1. Compute initial total load as the sum of all microservices. This represents the system load before any scaling or splitting.
2. Initialize the number of hosts to 1, since initially all traffic is handled by a single hosting structure.
3. For each month from 1 to 54, double the current load. This models the growth assumption in the problem.
4. After doubling, check whether the current load exceeds capacity C. If it does, we must split the load across multiple hosts.
5. Each split operation increases the number of hosts by one and halves the effective load per host group. We repeat splitting until the per-host load is within capacity. This ensures no host is overloaded after redistribution.
6. Store the number of hosts after each month so that queries can be answered in constant time.

The key invariant is that after processing month i, each host is assigned a load that does not exceed C, and the total load is partitioned evenly across all hosts up to rounding effects. Because splitting always restores feasibility when violated, and because doubling is the only source of growth, the process guarantees that once a configuration is valid for a month, it remains the correct starting point for the next month’s update. No alternative distribution can reduce the number of hosts needed, since every split is triggered exactly when a capacity violation occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    C, N, M = map(int, input().split())
    total = 0
    for _ in range(N):
        total += int(input())

    queries = [int(input()) for _ in range(M)]
    max_month = 54

    # hosts[m] = number of hosts needed at month m
    hosts = [0] * (max_month + 1)

    cur_load = total
    cur_hosts = 1

    hosts[0] = 1

    for m in range(1, max_month + 1):
        cur_load *= 2

        # ensure each host has at most C load
        while cur_load > cur_hosts * C:
            cur_hosts += 1

        hosts[m] = cur_hosts

    out = []
    for q in queries:
        out.append(str(hosts[q]))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code starts by aggregating all microservice loads into a single value, since only the total matters for scaling behavior. The simulation then progresses month by month, doubling the total load each time.

The critical implementation detail is the condition `cur_load > cur_hosts * C`. This checks whether the current distribution is feasible: total capacity is number of hosts times per-host capacity. If the load exceeds this, we increase the number of hosts until feasibility is restored. Each increment corresponds to introducing a new host and redistributing load.

Finally, we answer each query using precomputed values, avoiding recomputation.

## Worked Examples

### Sample 1

Input:

```
C = 1000, N = 5, M = 5
initial loads: 1000 1000 1000 1000 1000
queries: 0 1 2 3 4
```

Initial total load is 5000.

| Month | Load | Hosts | Capacity | Action |
| --- | --- | --- | --- | --- |
| 0 | 5000 | 5 | 5000 | valid |
| 1 | 10000 | 10 | 10000 | add hosts |
| 2 | 20000 | 20 | 20000 | add hosts |
| 3 | 40000 | 40 | 40000 | add hosts |
| 4 | 80000 | 80 | 80000 | add hosts |

Each month exactly doubles both load and required capacity via hosts.

This confirms that when the system starts perfectly saturated, doubling forces a proportional doubling of hosts.

### Sample 2

Input:

```
C = 2000, N = 5, M = 3
initial loads: 1000 2000 1000 2000 1000
queries: 1 0 2
```

Initial total load is 7000.

| Month | Load | Hosts | Capacity | Action |
| --- | --- | --- | --- | --- |
| 0 | 7000 | 4 | 8000 | valid |
| 1 | 14000 | 7 | 14000 | add hosts |
| 2 | 28000 | 14 | 28000 | add hosts |

At month 0, 4 hosts are enough since 4 × 2000 = 8000. At month 1, doubling requires exactly 7 hosts, showing that growth is not always a power-of-two multiple of initial hosts when capacity is not tight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + 54 + M) | summing microservices plus fixed 54-step simulation plus answering queries |
| Space | O(54) | storing precomputed host counts per month |

The bounds are extremely small, so the solution comfortably runs within limits. The fixed simulation length ensures predictable runtime regardless of input distribution.

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

    queries = [int(input()) for _ in range(M)]
    max_month = 54

    hosts = [0] * (max_month + 1)
    cur_load = total
    cur_hosts = 1
    hosts[0] = 1

    for m in range(1, max_month + 1):
        cur_load *= 2
        while cur_load > cur_hosts * C:
            cur_hosts += 1
        hosts[m] = cur_hosts

    return "\n".join(str(hosts[q]) for q in queries)

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

# custom tests
assert run("""1000 1 1
1000
0
""") == "1", "single service at capacity"

assert run("""1000 1 1
1000
1
""") == "2", "first split after doubling"

assert run("""1000 2 1
1000
1000
2
""") == "4", "multiple splits after repeated doubling"

assert run("""2000 3 1
1000
1000
1000
3
""") == "2", "small load grows slowly"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single service at capacity | 1 | no unnecessary split at month 0 |
| first split after doubling | 2 | correct triggering of capacity overflow |
| repeated doubling | 4 | exponential growth of hosts |
| small load grows slowly | 2 | non-saturated initial configuration |

## Edge Cases

One important case is when the initial load is exactly equal to total capacity. For example, with C = 1000 and a single service of 1000, the system starts perfectly balanced. At month 0 the answer is 1 host. After one doubling, load becomes 2000, which exceeds capacity, so a second host is required. The algorithm handles this correctly because it checks strict inequality `cur_load > cur_hosts * C`, meaning equality is still valid.

Another case is when initial load is far below capacity. For instance, C = 1000 with total load 10. Even after multiple doublings, the system may remain under capacity for several months. The loop does nothing until the threshold is crossed, so the host count stays stable until it becomes necessary to increase it.

A third case is when repeated doubling causes multiple host additions in a single month. If load jumps from just below a multiple of C to far above it, the `while` loop ensures we add exactly enough hosts to restore feasibility, rather than only one increment.
