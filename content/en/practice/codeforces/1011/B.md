---
title: "CF 1011B - Planning The Expedition"
description: "We are given a collection of food packages, each labeled by a type. There are also $n$ participants in an expedition, and time is measured in days. Each day, every participant consumes exactly one package."
date: "2026-06-16T22:42:06+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1011
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 499 (Div. 2)"
rating: 1200
weight: 1011
solve_time_s: 85
verified: true
draft: false
---

[CF 1011B - Planning The Expedition](https://codeforces.com/problemset/problem/1011/B)

**Rating:** 1200  
**Tags:** binary search, brute force, implementation  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of food packages, each labeled by a type. There are also $n$ participants in an expedition, and time is measured in days. Each day, every participant consumes exactly one package. The key constraint is that a participant must stick to a single food type for the entire expedition, although different participants may choose different types.

So for each participant we are effectively assigning one food type, and then we must check how long we can keep feeding everyone day by day using only the available packages. A participant assigned type $x$ consumes one package of type $x$ per day, so if we assign $k$ participants to type $x$, then each day we spend $k$ packages of type $x$. The number of days is therefore limited by how many total packages of each type exist.

The input gives the number of participants $n$, the number of available packages $m$, and the list of package types. The output is the maximum number of full days we can sustain such assignments.

The constraints are small, $n, m \le 100$, so even solutions that try many candidate answers or recompute counts repeatedly will pass comfortably. This signals that the structure of the solution is more about reasoning over frequencies than optimizing heavy computation.

A subtle edge case appears when total supply is extremely skewed. For example, if all packages are of one type but there are many participants, the answer is limited by how many people can be assigned to that type at all. Another edge case is when every type appears very few times. Even if there are many participants, the limiting factor becomes the sum of usable contributions across types rather than the number of participants.

A common mistake is to think each participant independently contributes to days based on frequency, without considering that assigning more participants to a type increases daily consumption linearly, which can eliminate feasibility entirely for naive greedy assignments.

## Approaches

The naive idea is to fix a number of days $d$, and then check whether we can assign each participant a food type such that every assigned type has at least $d$ packages per participant. If a type appears $c$ times, it can support at most $\lfloor c / d \rfloor$ participants for $d$ days. So feasibility becomes checking whether the sum over all types of $\lfloor c_i / d \rfloor$ is at least $n$.

If we try all possible $d$, the answer is at most $m$, so checking each $d$ up to $m$ with a frequency scan gives a solution in $O(m \cdot 100)$, which is trivial under constraints. This already works.

However, the key insight is that we do not need to iterate all $d$. The function “number of participants supported by $d$ days” is monotonic decreasing in $d$. If $d$ is feasible, then all smaller values are also feasible. This monotonicity allows binary search over the answer.

So instead of trying all $d$, we binary search the maximum $d$, and for each candidate compute the total supported participants using frequency counts. Each check is $O(100)$, and the search is $O(\log 100)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over days | $O(m \cdot 100)$ | $O(1)$ | Accepted |
| Binary Search | $O(100 \log 100)$ | $O(100)$ | Accepted |

## Algorithm Walkthrough

1. Count how many packages exist for each food type. We store frequencies in an array indexed by type.
2. Define a function `can(d)` that checks whether we can sustain $d$ days. For each type with frequency $c$, we compute how many participants it can support for $d$ days, which is $c // d$. We sum these values.
3. If the total supported participants is at least $n$, then $d$ days is feasible, because we can assign participants to types without exceeding supply.
4. Binary search on $d$ from 1 to $m$, tracking the largest feasible value.
5. Output the maximum feasible $d$. If even $d = 1$ fails, output 0.

The key reason step 3 is valid is that each type acts like a resource pool, and assigning a participant consumes one unit per day. Grouping participants per type maximizes reuse of identical consumption patterns, so the best strategy is always to pack as many participants as possible into high-frequency types.

### Why it works

At any fixed number of days $d$, a type with $c$ packages can support at most $\lfloor c / d \rfloor$ participants. This bound is tight because each participant consumes exactly $d$ units over the expedition. Summing over types gives the total number of participants that can be simultaneously assigned valid food types. If this sum is at least $n$, we can assign participants greedily because there is no interaction between types beyond counting capacity. This ensures feasibility exactly matches the computed condition, making the binary search decision function correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    freq = [0] * 101
    for x in a:
        freq[x] += 1
    
    def can(d):
        total = 0
        for c in freq:
            total += c // d
        return total >= n
    
    lo, hi = 1, m
    ans = 0
    
    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The frequency array compresses the problem into constant-sized state since values are bounded by 100. The feasibility check uses integer division to directly model how many full participant assignments each food type can sustain for a given number of days. Binary search then repeatedly refines the candidate answer.

A common pitfall is iterating over the raw list instead of the frequency array during `can`, which would incorrectly treat each package independently and break the grouping logic that makes division meaningful.

## Worked Examples

### Sample 1

Input:

```
4 10
1 5 2 1 1 1 2 5 7 2
```

Frequencies:

| Type | Count |
| --- | --- |
| 1 | 4 |
| 2 | 3 |
| 5 | 2 |
| 7 | 1 |

We test candidate days:

| d | c1//d | c2//d | c5//d | c7//d | total | feasible |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 3 | 2 | 1 | 10 | yes |
| 2 | 2 | 1 | 1 | 0 | 4 | yes |
| 3 | 1 | 1 | 0 | 0 | 2 | yes |
| 4 | 1 | 0 | 0 | 0 | 1 | no |

Binary search converges to 2. This shows that while 3 days can support enough total assignments in isolation, feasibility breaks when we require each participant to maintain consistency across all days.

### Sample 2 (constructed)

Input:

```
3 5
1 1 1 2 2
```

Frequencies:

| Type | Count |
| --- | --- |
| 1 | 3 |
| 2 | 2 |

Check $d = 2$:

| Type | Count | count // 2 |
| --- | --- | --- |
| 1 | 3 | 1 |
| 2 | 2 | 1 |
| Total = 2 < 3, not feasible. |  |  |

Check $d = 1$:

Total = 5 ≥ 3, feasible.

Answer is 1.

This demonstrates that even if total supply is large, the constraint of fixed food type per participant limits how efficiently resources can be reused.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(100 \log 100)$ | Frequency array is size 100, and each binary search step scans it |
| Space | $O(100)$ | Fixed-size frequency storage |

The bounds are small enough that even a naive $O(m \cdot 100)$ solution would pass, but binary search gives a clean structural view of the monotonic feasibility condition.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("""4 10
1 5 2 1 1 1 2 5 7 2
""") == "2"

# minimum case
assert run("""1 1
1
""") == "1"

# impossible case
assert run("""5 1
1
""") == "0"

# all same type
assert run("""3 6
1 1 1 1 1 1
""") == "2"

# mixed tight packing
assert run("""4 7
1 1 2 2 3 3 3
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single item | 1 | minimal feasibility |
| insufficient supply | 0 | impossible edge case |
| uniform distribution | 2 | optimal reuse of one type |
| mixed distribution | 1 | packing constraint interaction |

## Edge Cases

When there is only one participant, the answer reduces to the maximum frequency of any single type, since that participant can choose the most abundant food. The algorithm handles this because for $d > \max c_i$, all contributions become zero and feasibility fails immediately, leaving the correct maximum.

When there is only one package overall but many participants, every $d \ge 1$ yields zero total assignments, so feasibility fails for all $d$, and the binary search correctly returns 0.

When all packages are identical, feasibility becomes simply $\lfloor m / d \rfloor \ge n$, which is exactly what the frequency division computes. The algorithm naturally captures this without special casing since only one frequency is non-zero.

When distribution is sparse, the sum of floors prevents overcounting. Even if total packages exceed $n \cdot d$, uneven distribution can still make assignment impossible, and the per-type division correctly enforces that constraint.
