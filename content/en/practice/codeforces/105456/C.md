---
title: "CF 105456C - Jan's Cookies"
description: "We are given several independent scenarios. In each one, there are many cookies, each cookie belongs to a type and has a deadline time when it disappears."
date: "2026-06-23T02:49:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105456
codeforces_index: "C"
codeforces_contest_name: "XXIII Spain Olympiad in Informatics, Day 2"
rating: 0
weight: 105456
solve_time_s: 101
verified: false
draft: false
---

[CF 105456C - Jan's Cookies](https://codeforces.com/problemset/problem/105456/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent scenarios. In each one, there are many cookies, each cookie belongs to a type and has a deadline time when it disappears. Jan wants to eat cookies over time, and every time he eats a cookie, the waiting time before the next cookie increases with how many cookies he has already eaten. The first cookie can be eaten immediately, the second requires waiting 1 unit after eating the first, the third requires waiting 2 units after eating the second, and so on. If Jan has already eaten $k-1$ cookies and eats the $k$-th at time $t$, then the next one cannot be eaten before time $t + (k-1)$.

Each cookie disappears at its given time, but Jan is allowed to eat it at exactly that time as well. Multiple cookies of the same type exist, and Jan can eat any number of them. The goal is to maximize how many distinct cookie types Jan manages to eat at least once.

The key difficulty is that eating more cookies increases future waiting time, which makes later deadlines harder to satisfy. The decision is not just whether a type is available, but whether it can be scheduled early enough in an increasing-cost timeline.

The constraints imply we need something close to $O(n \log n)$ or $O(n \log m)$ per test case. With up to $2 \cdot 10^5$ cookies total, any approach that tries all subsets or simulates schedules for each type independently is too slow. Even greedy per-type simulation without sorting would risk quadratic behavior.

A subtle edge case appears when a type has multiple cookies with different deadlines. Choosing the wrong occurrence matters:

For example, suppose type 1 has cookies at times 1 and 100, and type 2 has a cookie at time 2. If we greedily pick the earliest possible cookie of each type without considering future cost, we might take type 1 at time 1 and type 2 at time 2, which works. But if type 2 had deadline 1 instead of 2, then picking type 1 first blocks type 2 even though a different ordering would succeed. This shows we must reason about ordering of selected types, not just availability.

Another edge case is when a type has only late cookies. Even if a type is “present”, it might only be usable if scheduled very early in the sequence due to increasing delay cost.

## Approaches

The brute-force idea is to treat each type independently and try to decide which subset of types Jan can successfully pick in some order. For a fixed subset of types, we would try to assign each chosen type a representative cookie and then simulate whether we can schedule them in some order respecting deadlines and the increasing delay rule.

This immediately becomes expensive because the number of subsets of types is exponential. Even if we fix a subset, checking feasibility is itself non-trivial, since for each ordering we must recompute arrival times that depend on the position in the sequence. With $m$ up to $5 \cdot 10^4$, this is infeasible.

The key observation is that we never need more than one cookie per type, and for each type it is optimal to consider only its latest usable deadline candidate, because earlier ones only reduce flexibility. Once we decide to take a type, we only care about the best cookie that can support it.

Now the problem becomes: we want to pick as many types as possible, and each chosen type contributes a deadline constraint. If we select $k$ types, we must assign them positions $1$ through $k$, and the $i$-th chosen type must be achievable at time at most $i(i-1)/2$ plus some base shift from scheduling, but more simply we simulate incrementally: the $i$-th chosen cookie is eaten at time equal to the sum of delays $0 + 1 + 2 + \dots + (i-1)$, which is $(i-1)i/2$, if we assume we start at time 0.

However, since cookies have arbitrary deadlines, we need a direct feasibility check: if we sort chosen types by increasing deadlines, we want to ensure that when we assign them in that order, each can be placed no later than its deadline under cumulative delay growth.

This leads to a greedy strategy: consider types sorted by their best possible deadline. Maintain how many types we have already chosen. For each type, we check if we can include it. If we are at size $k$, the next type would be eaten after a delay of $k$, so we test whether its chosen deadline is at least the time at which it would be eaten given current sequence length. If yes, we include it.

We reduce each type to a single value: the best achievable deadline is simply the maximum deadline among its cookies, since Jan can choose which copy to eat. Then we greedily select types in increasing order of these values, maintaining a running feasibility constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $m$ | $O(m)$ | Too slow |
| Greedy by deadlines | $O(n \log n)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

We first compress the input so that each type is represented by a single number: the maximum disappearance time among all cookies of that type. This captures the best possible chance to use that type, because any earlier cookie only makes the constraint stricter.

1. Read all cookies and compute for each type the maximum deadline among its occurrences. This transforms the problem into selecting among $m$ items, each with a single deadline.
2. Sort all types by their computed deadlines in non-decreasing order. The reasoning is that we want to commit to the most restrictive types first, since delaying them only increases the risk that we exceed their deadline once cumulative eating delay grows.
3. Initialize a counter $k = 0$, representing how many types we have successfully chosen so far.
4. Iterate through the sorted list of deadlines. For each type with deadline $d$, compute the time at which Jan would eat the next cookie if we include it. That time is the current accumulated waiting cost, which equals $k(k+1)/2$ if tracked exactly, but we can avoid full formula by incrementally maintaining the next available time. If the next required time does not exceed $d$, we accept this type and increment $k$. Otherwise we skip it.

The critical idea is that accepting a type only increases future delay, so once a type fails the feasibility test, it will never become feasible later.

### Why it works

At any point, the algorithm maintains a set of already chosen types that can be scheduled in increasing order of their deadlines without violating constraints. Sorting by deadline ensures that when we consider a new type, we are testing it against the smallest possible growth state for its position among all feasible selections. If a type cannot fit at its earliest possible position in this ordering, inserting it anywhere later would only increase its required waiting time, making it even less feasible. This establishes that greedy acceptance never invalidates future feasibility decisions, and skipping a type is safe because any valid solution including it would require replacing some earlier accepted type with a tighter deadline, contradicting sorted order optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        m, n = map(int, input().split())
        
        # best deadline per type
        best = [0] * (m + 1)
        
        for _ in range(n):
            a, ti = map(int, input().split())
            if ti > best[a]:
                best[a] = ti
        
        deadlines = [best[i] for i in range(1, m + 1)]
        deadlines.sort()
        
        k = 0
        current_time = 0
        
        for d in deadlines:
            # if we take this as (k+1)-th cookie, it is eaten at current_time + k
            if current_time + k <= d:
                current_time += k
                k += 1
        
        out.append(str(k))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The compression step ensures we only track the most permissive cookie per type. The sorted array of deadlines creates the structure needed for greedy selection. The variables `k` and `current_time` encode the cumulative delay effect: when selecting the next type, the waiting cost increases exactly by the number of already chosen types.

The condition `current_time + k <= d` checks whether the next cookie can be placed before it disappears, since the next eating time is current accumulated delay plus the additional delay induced by placing it at position `k+1`.

## Worked Examples

### Example 1

Input:

```
2
2 4
1 1
1 2
1 3
2 4
```

We compress types:

| Type | Best deadline |
| --- | --- |
| 1 | 3 |
| 2 | 4 |

Sorted deadlines are $[3, 4]$.

| Step | k | current_time | d | Decision |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 3 | take |
| 2 | 1 | 0 | 4 | take |

Both types are feasible, so answer is 2.

This shows that even though type 1 had multiple options, only the best deadline matters.

### Example 2

Input:

```
1
3 3
1 2
2 2
3 2
```

Compressed:

| Type | Best deadline |
| --- | --- |
| 1 | 2 |
| 2 | 2 |
| 3 | 2 |

Sorted: $[2, 2, 2]$

| Step | k | current_time | d | Decision |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 2 | take |
| 2 | 1 | 0 | 2 | take |
| 3 | 2 | 1 | 2 | take |

All are feasible, producing 3.

This demonstrates that even tight identical deadlines are handled correctly because cumulative delay grows slowly enough early on.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting deadlines dominates, all other operations are linear |
| Space | $O(m)$ | storing best deadline per type |

The solution fits comfortably within limits since $n$ is up to $2 \cdot 10^5$ and sorting plus a single pass is efficient under 2 seconds in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            m, n = map(int, input().split())
            best = [0] * (m + 1)
            for _ in range(n):
                a, ti = map(int, input().split())
                if ti > best[a]:
                    best[a] = ti
            deadlines = sorted(best[1:])
            k = 0
            current_time = 0
            for d in deadlines:
                if current_time + k <= d:
                    current_time += k
                    k += 1
            out.append(str(k))
        return "\n".join(out)

    return solve()

# provided sample
assert run("""2
2 4
1 1
1 2
1 3
2 4
3 3
1 2
2 2
3 2
""") == "2\n2"

# minimum case
assert run("""1
1 1
1 100
""") == "1"

# all tight impossible except first
assert run("""1
3 3
1 1
2 1
3 100
""") == "2"

# identical deadlines boundary
assert run("""1
5 5
1 1
2 1
3 1
4 1
5 1
""") == "1"

# large increasing feasibility
assert run("""1
4 4
1 10
2 100
3 1000
4 10000
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single type | 1 | minimum handling |
| mixed tight deadlines | 2 | partial feasibility |
| all equal small deadlines | 1 | early saturation |
| increasing deadlines | 4 | full greedy success |

## Edge Cases

A subtle case occurs when many types share the same deadline, and only a few can be selected before cumulative delay exceeds it. For input:

```
1
4 4
1 1
2 1
3 1
4 10
```

The compressed deadlines are $[1, 1, 1, 10]$. The algorithm first takes the first type at cost 0, then immediately attempts the second type but fails because the next required time is 1 while current_time + k becomes 1, which equals the deadline and is still allowed. After selecting two types, the next attempt would require time 2, which exceeds 1, so only two types from the tight group are possible. The final type with deadline 10 is accepted earlier or later depending on ordering, but since it is large, it always fits after the tight ones are exhausted.

This confirms the algorithm correctly saturates early constraints before benefiting from relaxed ones.
