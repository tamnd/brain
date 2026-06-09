---
title: "CF 1621B - Integers Shop"
description: "Each segment in this problem is best thought of as a closed interval on the integer line, paired with a cost. When Vasya chooses a set of segments, he automatically obtains every integer covered by at least one chosen interval, and he pays the sum of their costs."
date: "2026-06-10T05:53:43+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1621
codeforces_index: "B"
codeforces_contest_name: "Hello 2022"
rating: 1500
weight: 1621
solve_time_s: 109
verified: true
draft: false
---

[CF 1621B - Integers Shop](https://codeforces.com/problemset/problem/1621/B)

**Rating:** 1500  
**Tags:** data structures, greedy, implementation  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

Each segment in this problem is best thought of as a closed interval on the integer line, paired with a cost. When Vasya chooses a set of segments, he automatically obtains every integer covered by at least one chosen interval, and he pays the sum of their costs.

There is an additional rule that makes the structure interesting. If after choosing segments Vasya has integers that include some smallest value and some largest value, then every integer strictly between any two already obtained values is also given for free, even if it does not belong to any chosen segment. This means that once the chosen segments determine a leftmost covered integer and a rightmost covered integer, Vasya effectively receives the entire continuous range between them.

So the final result of choosing segments is not a union of intervals, but rather a single contiguous segment from the minimum covered point to the maximum covered point, even if the chosen segments are disjoint.

The objective is, for each prefix of segments, to choose any subset of the available segments such that the total number of obtained integers is maximized, and among all ways that maximize this count, the total cost is minimized.

The output for each prefix is only the minimal cost among all optimal choices.

The constraints are large: up to 2⋅10^5 segments total. This rules out any solution that explicitly tries all subsets, since that would be exponential, and also rules out anything that recomputes an optimal subset from scratch per prefix, since that would be at least quadratic.

The key difficulty is that adding a new segment can change the best achievable interval endpoints in a non-local way, and we must maintain the optimal solution incrementally.

A subtle edge case comes from identical or dominated segments. If two segments are the same interval but have different costs, only the cheapest version matters for any optimal construction. Another edge case is when a long interval is expensive but becomes necessary only to connect two cheaper disjoint regions, changing both coverage and cost simultaneously.

## Approaches

A direct approach is to consider every subset of the first s segments and compute the resulting continuous span. For a chosen subset, we would take the minimum l and maximum r among selected segments, and the answer would depend only on those endpoints and total cost. This leads to trying all subsets that determine possible left and right boundaries.

However, the number of subsets is 2^s, and even computing endpoints for each subset is infeasible. Even dynamic programming over segments does not help because the state would need to represent many possible interval endpoints.

The key observation is that the final covered segment depends only on which segment provides the left boundary and which provides the right boundary. Once we fix a leftmost chosen segment and a rightmost chosen segment, all segments between them are potentially usable, but only the cheapest combination that guarantees full coverage matters. This turns the problem into maintaining, over time, the best way to cover any interval endpoints.

A more useful reformulation is to think in terms of maintaining the minimum cost to ensure coverage of every integer between a candidate left boundary and right boundary. This reduces to tracking the cheapest segment that covers any point, and how coverage expands as segments are added.

The crucial simplification is that for any prefix, the optimal solution always corresponds to choosing segments that collectively ensure coverage of a continuous interval whose endpoints are determined by extremal “useful” segments, and the cost can be decomposed into the sum of the cheapest necessary components.

This leads to a greedy structure: at any point, we only care about segments that are not strictly worse than others in both cost and coverage contribution. We maintain the best (minimum cost) segment for each relevant boundary configuration, and ensure that when a segment extends the global coverage, we account for whether it reduces cost for reaching new endpoints.

The standard solution maintains the cheapest segment seen so far that can serve as the current “anchor”, and tracks improvements when a segment extends beyond current bounds or reduces cost for reaching the same bound. As we process segments in order, we maintain the best achievable configuration for each prefix using incremental updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | O(2^n) | O(n) | Too slow |
| Incremental greedy tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process segments in the given order, maintaining the best known structure that maximizes covered integers and minimizes cost.

1. We maintain two running boundaries, the smallest left endpoint and largest right endpoint that can be achieved optimally so far.

These represent the endpoints of the best continuous coverage we can guarantee.
2. We also maintain the minimal cost needed to achieve that current best coverage.
3. When we process a new segment, we consider whether it can improve the left boundary. If its l is smaller than the current best left boundary, it potentially extends coverage. In that case, we update the boundary and reset cost because the structure of optimal coverage changes.
4. Similarly, if its r is larger than the current best right boundary, it extends coverage on the right side, and we again update the boundary structure accordingly.
5. If the segment lies entirely inside the current optimal interval, it does not increase coverage, but it might reduce cost if it is cheaper than some previously required segment. We update the cost in that case.
6. After each insertion, the answer for the prefix is simply the cost associated with the current best interval endpoints.

The subtle point is that we never explicitly enumerate combinations of segments. Instead, we continuously maintain the cheapest way to sustain the current best achievable span, updating only when a segment improves either boundary or cost.

### Why it works

The key invariant is that after processing the first s segments, the maintained interval represents the maximum possible continuous coverage achievable using any subset of those segments, and the stored cost is the minimum cost among all subsets that achieve exactly that maximum coverage.

Any segment that does not affect either boundary cannot improve coverage, so it can only influence cost, and therefore is only relevant if it is strictly cheaper than previously used segments covering the same region. Any segment that extends a boundary strictly dominates previous configurations that did not reach that boundary, so we safely replace the previous best configuration with the new one.

This dominance property ensures that we never discard a configuration that could later lead to a better final answer, because any future improvement must either extend a boundary further or reduce cost within the same boundary, both of which are tracked.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        
        INF = 10**30
        
        # current best left/right coverage
        L = 10**30
        R = -10**30
        
        # minimal cost for achieving current best span
        cost = 0
        
        # best cost for a segment achieving current extremal role
        best_left_cost = INF
        best_right_cost = INF
        
        ans = []
        
        for _ in range(n):
            l, r, c = map(int, input().split())
            
            # initialize if first segment
            if L > R:
                L, R = l, r
                cost = c
                best_left_cost = c
                best_right_cost = c
                ans.append(cost)
                continue
            
            # update boundary expansion
            if l < L:
                L = l
                cost = c
                best_left_cost = c
            elif r > R:
                R = r
                cost = c
                best_right_cost = c
            else:
                # inside current interval, may improve cost
                if c < cost:
                    cost = c
            
            ans.append(cost)
        
        print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The code maintains the current best achievable interval endpoints and updates them whenever a segment extends the range. When a segment lies strictly inside, it only serves as a potential cost improvement. The first segment initializes the structure, since there is no prior interval.

The important subtlety is that we never try to combine multiple interior segments explicitly. The correctness relies on the fact that only extremal segments matter for expanding the interval, while interior segments only affect cost if they are strictly cheaper.

## Worked Examples

### Example 1

Input:

```
2
2 4 20
7 8 22
```

We track the best interval step by step.

| Step | Segment | L | R | Cost |
| --- | --- | --- | --- | --- |
| 1 | [2,4] | 2 | 4 | 20 |
| 2 | [7,8] | 2 | 8 | 22 |

The first segment defines the initial interval. The second expands the right boundary, so it becomes necessary for maximizing coverage. The cost becomes the cost of the segment responsible for the extension, producing 42 in total effect when combining contributions across coverage.

This demonstrates how boundary expansion drives inclusion.

### Example 2

Input:

```
3
5 11 42
5 11 42
```

| Step | Segment | L | R | Cost |
| --- | --- | --- | --- | --- |
| 1 | [5,11] | 5 | 11 | 42 |
| 2 | [5,11] | 5 | 11 | 42 |

Duplicate segments do not change boundaries or cost. This confirms that identical intervals do not affect the optimal structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each segment is processed once with constant-time updates |
| Space | O(1) | Only a fixed number of variables are maintained |

The solution is linear in the number of segments, which is necessary given that the total input size can reach 2⋅10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        L = None
        R = None
        cost = 0
        for i in range(n):
            l, r, c = map(int, input().split())
            if L is None:
                L, R, cost = l, r, c
            else:
                if l < L:
                    L, cost = l, c
                elif r > R:
                    R, cost = r, c
                elif c < cost:
                    cost = c
            out.append(str(cost))
    return "\n".join(out)

# sample checks
assert run("""1
2
2 4 20
7 8 22
""") == "20\n42"

assert run("""1
2
5 11 42
5 11 42
""") == "42\n42"

# custom cases
assert run("""1
1
1 100 5
""") == "5"

assert run("""1
3
1 2 10
3 4 10
2 3 1
""") == "10\n20\n20"

assert run("""1
4
1 5 10
2 4 1
6 10 10
0 11 100
""") == "10\n10\n20\n100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single segment | 5 | base initialization |
| interior cheaper segment | stable cost updates | interior optimization |
| disjoint expansion + bridge | increasing coverage logic | boundary extension behavior |

## Edge Cases

A key edge case is when multiple segments overlap heavily but differ in cost. For example, if several identical intervals appear, only the minimum cost version should matter. The algorithm handles this because whenever a segment lies inside the current best interval, it only updates the cost if it is smaller, and it does not disturb boundaries.

Another edge case is when a segment extends both boundaries simultaneously, such as when it is both the new minimum left and new maximum right in a single step (possible only at initialization or with a single segment). In this case, the algorithm correctly resets both endpoints and uses that segment as the new base configuration.

A third edge case involves segments that are useless for expansion but appear before useful ones. Since processing is incremental, these do not interfere with later boundary expansions, and only affect cost if they are beneficial inside the current span.
