---
title: "CF 104180C - Brownie Baking"
description: "We are given two collections of integers. One represents required brownie sizes requested by friends, and the other represents available baking tins, where each tin produces exactly one brownie of its own fixed size."
date: "2026-07-02T00:42:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104180
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 02-10-23 Div. 2 (Beginner)"
rating: 0
weight: 104180
solve_time_s: 105
verified: true
draft: false
---

[CF 104180C - Brownie Baking](https://codeforces.com/problemset/problem/104180/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two collections of integers. One represents required brownie sizes requested by friends, and the other represents available baking tins, where each tin produces exactly one brownie of its own fixed size. A friend is satisfied if the brownie assigned to them has size strictly greater than what they requested. Each tin can be used at most once, and each friend can receive at most one tin.

The task is to match tins to friends in a way that maximizes the number of satisfied friends.

The key structure here is a one-to-one matching problem between two arrays, with a strict inequality constraint on feasibility and a global objective of maximizing the number of successful matches.

The constraints go up to 200,000 elements in each array. A quadratic solution that tries all pairings or greedily checks each friend against all tins would perform on the order of 40 billion comparisons in the worst case, which is far beyond a 2 second limit. This immediately suggests that any viable solution must be at most O(n log n) or O(n).

A few edge cases matter:

If all tins are too small, for example friends request `[10, 20, 30]` and tins are `[1, 2, 3]`, the answer is zero. Any greedy that pairs smallest-to-smallest without checking strict inequality would still correctly fail here, but a reversed inequality bug often causes incorrect counting.

If tins are significantly larger than requests, such as requests `[1, 1, 1]` and tins `[100, 101, 102]`, every friend should be satisfied. A buggy solution might waste large tins on already satisfiable small requests in a non-optimal order if it does not coordinate matching carefully.

A subtle failure case arises when duplicates exist, for example requests `[5, 5, 5]` and tins `[6, 6]`. The correct answer is 2. A naive approach that always pairs the first compatible tin it sees may accidentally reuse logic that does not properly mark tins as consumed, leading to overcounting.

## Approaches

A brute-force idea is to try assigning tins to friends recursively or via bipartite matching. We could attempt every pairing between a friend and an unused tin, choosing whether to assign or skip. This forms a bipartite matching search space with branching at every choice. Even if we prune invalid matches, in the worst case where most tins are large enough, the number of valid partial matchings grows combinatorially. With 200,000 elements this is completely infeasible.

A more structured viewpoint is to sort both arrays. Once sorted, we can try to always satisfy the least demanding friend first using the smallest tin that can satisfy them. This is the critical observation: if we ever assign a large tin to a small requirement while a smaller tin could have worked, we may reduce future flexibility without benefit. The correct strategy is to minimize wasted capacity by always using the smallest possible tin that still works.

This leads to a greedy matching process on sorted arrays. We scan requests in increasing order and maintain a pointer over tins, advancing it until we find a tin that strictly exceeds the current request. When found, we match and move both pointers forward. Otherwise, we stop for that request and continue.

This reduces the problem to a two-pointer sweep over sorted arrays.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(N·M) or exponential | O(N + M) | Too slow |
| Optimal Greedy + Sorting | O(N log N + M log M) | O(1) extra (ignoring sort) | Accepted |

## Algorithm Walkthrough

1. Sort both the request array and the tin array in non-decreasing order. This ensures we always process easier requirements before harder ones, which prevents wasting large tins on small requests.

2. Initialize two pointers: one for requests, one for tins, both starting at index zero. Also maintain a counter for successful matches.

3. For the current request, move the tin pointer forward until we find the first tin whose size is strictly greater than the request. Each skipped tin is too small to satisfy this request or any earlier one, since requests are sorted.

4. If such a tin is found, assign it to the current request, increment the match counter, and advance both pointers. This ensures each tin is used at most once.

5. If no suitable tin exists, move only the request pointer forward. This request cannot be satisfied by any remaining tin.

6. Continue until either list is exhausted.

The important detail is that the tin pointer never moves backward. Once a tin is too small for a given request, it will also be too small for any later request because requests only increase.

### Why it works

The correctness relies on a monotonic feasibility structure after sorting. When both arrays are sorted, matching a smallest feasible tin to the smallest unmet request is always safe because any alternative assignment that uses a larger tin for this request cannot improve the number of matches later. Large tins are more flexible, so preserving them for larger requests cannot reduce optimality. This exchange argument ensures that any optimal solution can be transformed into one that follows this greedy pairing without decreasing the number of satisfied friends.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    req = list(map(int, input().split()))
    tins = list(map(int, input().split()))
    
    req.sort()
    tins.sort()
    
    i = j = 0
    ans = 0
    
    while i < n and j < m:
        while j < m and tins[j] <= req[i]:
            j += 1
        if j < m:
            ans += 1
            i += 1
            j += 1
        else:
            break
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting both arrays so that we can safely process from smallest to largest. The two pointers `i` and `j` track our position in requests and tins respectively.

The inner loop advances `j` until we either find a tin strictly larger than `req[i]` or exhaust all tins. The strict inequality is important; using `<=` ensures we do not incorrectly match equal-sized tins.

Once a valid tin is found, we count it as a successful assignment and advance both pointers, consuming both the request and the tin.

If no tin can satisfy the current request, the loop ends and the answer is printed.

A common implementation mistake is forgetting to advance the request pointer when a match occurs, which would incorrectly reuse the same request multiple times. Another is using a single pass without sorting, which breaks the greedy structure.

## Worked Examples

### Sample 1

Input:
```
5 3
8 12 25 3 10
1 8 20
```

Sorted:
Requests = [3, 8, 10, 12, 25]  
Tins = [1, 8, 20]

| i (req) | j (tin) | req[i] | tins[j] | Action | Matches |
|---|---|---|---|---|---|
| 0 | 0 | 3 | 1 | 1 ≤ 3, skip tin | 0 |
| 0 | 1 | 3 | 8 | 8 > 3, match | 1 |
| 1 | 2 | 8 | 20 | 20 > 8, match | 2 |
| 2 | 3 | 10 | - | no tins left | 2 |

Output is 2.

This trace shows that small tins are correctly discarded when they cannot satisfy the smallest request, and larger tins are preserved for larger requests.

### Sample 2 (constructed)

Input:
```
4 4
5 5 5 5
6 4 6 7
```

Sorted:
Requests = [5, 5, 5, 5]  
Tins = [4, 6, 6, 7]

| i | j | req[i] | tins[j] | Action | Matches |
|---|---|---|---|---|---|
| 0 | 0 | 5 | 4 | too small | 0 |
| 0 | 1 | 5 | 6 | match | 1 |
| 1 | 2 | 5 | 6 | match | 2 |
| 2 | 3 | 5 | 7 | match | 3 |
| 3 | 4 | - | - | done | 3 |

This demonstrates that duplicates are handled naturally and each tin is consumed exactly once.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(N log N + M log M) | sorting dominates, two-pointer scan is linear |
| Space | O(1) extra | sorting in place aside from input arrays |

The constraints allow up to 200,000 elements, so sorting at this scale is comfortably within limits, and the linear scan afterward ensures the solution stays efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("""5 3
8 12 25 3 10
1 8 20
""") == "2"

# all match
assert run("""3 3
1 1 1
2 2 2
""") == "3"

# none match
assert run("""3 3
10 20 30
1 2 3
""") == "0"

# duplicates tin heavy
assert run("""3 5
5 5 5
6 6 6 6 6
""") == "3"

# exact boundary equality should fail equality
assert run("""2 2
5 5
5 6
""") == "1"
```

| Test input | Expected output | What it validates |
|---|---|---|
| all small requests, large tins | 3 | full matching possible |
| all large requests, small tins | 0 | no matches |
| duplicates on both sides | 3 | correctness with repeated values |
| equality boundary case | 1 | strict inequality handling |

## Edge Cases

A key edge case is when many tins are too small for early requests but could still satisfy later ones if we skip properly. For example, requests `[5, 6]` and tins `[4, 7]`. The algorithm first discards `4` for request `5`, then correctly uses `7` for request `6`, achieving one match. A greedy strategy that tries to match each request independently without advancing the tin pointer correctly would either reuse `4` or incorrectly conclude failure.

Another case is when tins are abundant but only a few are large enough. For requests `[1, 2, 3, 4]` and tins `[2, 2, 2, 10]`, the algorithm ensures that the single large tin is reserved for the largest request that can use it, while smaller tins are consumed by smaller requests, yielding optimal utilization.
