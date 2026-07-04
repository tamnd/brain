---
title: "CF 102961U - Factory Machines"
description: "We are given a collection of independent factory machines, each of which can repeatedly produce identical items. The i-th machine produces one item every fixed amount of time, so if it runs for a total time T, it contributes roughly T divided by its processing time, rounded down…"
date: "2026-07-04T06:56:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102961
codeforces_index: "U"
codeforces_contest_name: "CSES Problem Set: Sorting and Searching"
rating: 0
weight: 102961
solve_time_s: 43
verified: true
draft: false
---

[CF 102961U - Factory Machines](https://codeforces.com/problemset/problem/102961/U)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of independent factory machines, each of which can repeatedly produce identical items. The i-th machine produces one item every fixed amount of time, so if it runs for a total time T, it contributes roughly T divided by its processing time, rounded down to whole items.

Alongside these machines, there is a target number of items that the factory must produce. All machines operate in parallel, and their outputs accumulate. The task is to determine the smallest amount of time needed so that the total number of produced items across all machines is at least the required target.

The input consists of the number of machines, the production requirement, and a list of machine speeds. Each speed indicates how long that machine takes to produce a single item. The output is a single integer representing the minimum time at which the production requirement is satisfied.

The constraint structure typically implies up to around 10^5 machines and large target values, often up to 10^18 or similar magnitudes. This immediately rules out any simulation that advances time step by step, since even iterating over time units would be far beyond feasible limits. Even per-unit simulation would explode to 10^18 operations in worst cases, and even per-event simulation would still be too slow because events across all machines interleave densely.

A few edge cases tend to break naive reasoning. If there is a single very fast machine among many slow ones, any approach that distributes work greedily per machine without aggregating over time will underestimate contributions. For example, if machine times are [1, 100, 100] and the target is 5, the correct answer is 5, since the first machine alone completes everything. A faulty greedy distribution that tries to "assign items" to machines in order without modeling parallel time will incorrectly spread the load.

Another subtle case appears when all machines are slow but the target is small. For instance, machines [10, 10, 10] with target 1 should return 10. Any approach that mistakenly tries to average processing times will incorrectly suggest a smaller time.

## Approaches

The brute-force idea is to simulate time starting from zero and increment it step by step. At each time value, we compute how many items each machine has produced by dividing the elapsed time by its processing time and summing across machines. Once the total reaches the target, we return the current time.

This approach is correct because it directly mirrors the definition of production over time. Every machine contributes exactly floor(T / a_i) items at time T, so checking each time step guarantees correctness.

The failure point is the growth of the time axis. If machine times and target sizes are large, the answer can be up to 10^18. Even a single pass over this range is impossible. Computing production at each step also costs O(n), so the total complexity becomes O(n · answer), which is unusable.

The key observation is that the total number of items produced by time T is monotonic in T. If we have enough items at time T, then any larger time will also satisfy the requirement. This monotonic structure allows us to replace linear search over time with binary search.

Instead of simulating every moment, we ask a feasibility question: given a fixed time T, can all machines together produce at least k items? This check is fast because it only requires summing floor(T / a_i) over all machines. With this predicate, we binary search the smallest T that satisfies it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n · T) | O(1) | Too slow |
| Binary Search on Time | O(n log T) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the problem to finding the minimum time T such that the production function reaches the target.

1. Define a function that computes how many items are produced by all machines in a given time T by summing T // a_i over all machines. This function models the entire factory output at a fixed moment.
2. Choose a search range for time. The lower bound is zero, and the upper bound can safely be the slowest possible scenario where one machine alone produces all items, often set as max(a_i) * k.
3. Perform binary search over this time range. At each midpoint T, compute total production using the function from step 1.
4. If production at T is at least the target, record T as a candidate answer and move the search left, because we try to minimize time.
5. Otherwise, move the search right since T is too small to satisfy production requirements.
6. Continue until the search space is exhausted, returning the smallest feasible T.

The crucial design choice is that the check function is recomputed from scratch each time. This is acceptable because the computation is linear in number of machines, while the search depth is logarithmic in the answer range.

### Why it works

The correctness relies on the monotonicity of the production function. For any fixed set of machine speeds, increasing T can only increase or maintain the number of produced items, never decrease it. This guarantees that the feasibility condition forms a contiguous interval on the number line: all times below a certain threshold are invalid, and all times above it are valid. Binary search is therefore guaranteed to converge to the smallest valid time without skipping the true boundary.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(machines, t, k):
    total = 0
    for a in machines:
        total += t // a
        if total >= k:
            return True
    return False

def solve():
    n, k = map(int, input().split())
    machines = list(map(int, input().split()))

    lo, hi = 0, min(machines) * k
    ans = hi

    while lo <= hi:
        mid = (lo + hi) // 2
        if can(machines, mid, k):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The core of the solution is the `can` function, which evaluates whether a candidate time is sufficient. It sums contributions from each machine using integer division, which directly encodes how many full items each machine completes by time `t`.

The binary search maintains a shrinking window of possible answers. Whenever a midpoint is feasible, it is stored and the search continues left to find a smaller valid time. The upper bound is chosen as `min(machines) * k` because even the fastest machine alone could produce all items in that time, making it a safe worst-case bound.

Care must be taken with overflow in languages with fixed integer types, since `t` and `k` can be large. In Python this is naturally handled.

## Worked Examples

### Example 1

Input:

```
3 7
3 2 5
```

We want 7 items, machines produce every 3, 2, and 5 units of time.

| mid time T | T//3 | T//2 | T//5 | total | feasible |
| --- | --- | --- | --- | --- | --- |
| 5 | 1 | 2 | 1 | 4 | no |
| 10 | 3 | 5 | 2 | 10 | yes |
| 7 | 2 | 3 | 1 | 6 | no |
| 8 | 2 | 4 | 1 | 7 | yes |

The binary search narrows toward 8 as the smallest time producing at least 7 items. This demonstrates how feasibility sharply transitions from false to true.

### Example 2

Input:

```
2 1
10 10
```

Only one item is needed, and both machines are slow.

| T | T//10 | T//10 | total | feasible |
| --- | --- | --- | --- | --- |
| 5 | 0 | 0 | 0 | no |
| 10 | 1 | 1 | 2 | yes |

The answer is 10, showing that even multiple machines do not help if the target is extremely small and each machine has identical slow speed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(max(a_i) · k)) | Each binary search step scans all machines, and the number of steps is logarithmic in the search range |
| Space | O(1) | Only a few counters and the input array are stored |

The complexity fits comfortably within typical constraints of up to 10^5 machines and large target values, since about 60 binary search iterations are sufficient even for very large ranges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def can(machines, t, k):
        total = 0
        for a in machines:
            total += t // a
            if total >= k:
                return True
        return False

    def solve():
        n, k = map(int, input().split())
        machines = list(map(int, input().split()))

        lo, hi = 0, min(machines) * k
        ans = hi

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(machines, mid, k):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        return str(ans)

    return solve()

# custom cases
assert run("3 7\n3 2 5\n") == "8", "basic case"
assert run("2 1\n10 10\n") == "10", "small target"
assert run("1 5\n2\n") == "10", "single machine"
assert run("4 10\n1 2 3 4\n") == "6", "mixed speeds"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 7 / 3 2 5 | 8 | standard binary search transition |
| 2 1 / 10 10 | 10 | minimal target edge case |
| 1 5 / 2 | 10 | single machine correctness |
| 4 10 / 1 2 3 4 | 6 | heterogeneous speeds and accumulation |

## Edge Cases

When there is only one machine, the binary search collapses into finding the smallest multiple of its processing time that reaches the target. For input `1 5` with machine `[2]`, the feasibility check grows from 0 items at time 1 to 5 items at time 10, and the algorithm correctly converges to 10 because only full production cycles matter.

When all machines are identical, the solution depends entirely on multiplication of counts rather than distribution. For `[5, 5, 5]` and target 3, time 5 already produces 3 items, and any naive attempt to assign tasks per machine sequentially would incorrectly assume multiple cycles are needed, while the correct model aggregates contributions in one step.

When the target is extremely large, such as near 10^18, only binary search remains viable. The algorithm never iterates over time explicitly, and every step remains a bounded sum over machines, ensuring correctness even at extreme scales.
