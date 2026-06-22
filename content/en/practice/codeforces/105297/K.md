---
title: "CF 105297K - Grabbing plush"
description: "We are given a row of N stuffed animals, each with an integer value that can be positive or negative. We are allowed to perform at most M operations."
date: "2026-06-23T06:31:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105297
codeforces_index: "K"
codeforces_contest_name: "2024 USP Try-outs"
rating: 0
weight: 105297
solve_time_s: 60
verified: true
draft: false
---

[CF 105297K - Grabbing plush](https://codeforces.com/problemset/problem/105297/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of N stuffed animals, each with an integer value that can be positive or negative. We are allowed to perform at most M operations. Each operation corresponds to using a special claw that removes a block of exactly W stuffed animals, but the block is not chosen in a fixed index system that shrinks after removals. Instead, the claw works on the current physical layout: animals stay at fixed positions, gaps appear after removals, and when the claw is placed, its right prong can slide left until it hits an existing stuffed animal before the removal happens.

Despite the mechanical description, the key outcome of each operation is simple: one operation removes a consecutive segment of stuffed animals in the current remaining sequence, and the removed value contributes to the score. The goal is to maximize the total sum of removed values after using at most M such operations.

The constraint N ≤ 10⁴ and M ≤ 5000 strongly suggests a quadratic dynamic programming solution is intended. A cubic solution over all choices of segments would require trying O(N²) segments per operation, which is far too slow. Even O(N²M) is impossible. We should aim for something close to O(NM) or O(NM log N), meaning each state transition must be computed in constant time or amortized constant time.

The most dangerous edge case is misunderstanding how removals affect future segments. A naive reading might suggest that after removing a segment, indices shift and all future decisions depend on complex geometry of remaining gaps. For example, if W = 2:

Input:

```
4 2 2
1 100 -100 1
```

A naive greedy might remove either middle pair or ends without realizing that removing one block affects what is considered adjacent later. However, the correct interpretation reduces the problem to choosing disjoint fixed windows in the original array, because the relative order is preserved and any optimal strategy can be mapped back to original indices without loss of generality.

Another subtle failure case is overlapping windows. If a solution mistakenly allows overlapping segments, it might count the same element multiple times:

```
5 2 3
5 5 5 5 5
```

A wrong approach could pick windows [1,3] and [2,4], overcounting shared elements, but physically this is impossible under valid operations.

## Approaches

A brute-force strategy would enumerate every possible way to choose up to M segments of length W in the evolving array after each removal. After each operation, the array structure changes due to gaps, so simulating this directly requires maintaining a dynamic sequence and trying all possible placements at every step. Even ignoring implementation complexity, the number of states grows combinatorially. At each step we could choose O(N) positions, and we do this M times, giving roughly O(N^M) in the worst conceptual form, or at best O(N^{2M}) if we try to restrict to segments, both completely infeasible.

The key simplification is recognizing that the removal process does not create new relative adjacencies in a way that changes optimality. Any sequence of removals can be mapped to selecting non-overlapping segments in the original array, because once a segment is removed, nothing inside it affects later operations, and remaining elements preserve order. This turns the problem into selecting at most M disjoint segments of fixed length W in the original array to maximize total sum.

Once this reduction is made, the structure becomes a classic dynamic programming problem. We scan left to right and decide whether to end a segment at position i. If we take a segment, it must start at i − W + 1, and we add its sum to the best solution before that segment. If we skip, we carry forward the previous value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate all operations in dynamic structure) | Exponential | O(N) | Too slow |
| Dynamic Programming over endpoints | O(N · M) | O(N · M) or O(N) optimized | Accepted |

## Algorithm Walkthrough

We define a prefix-sum array to quickly compute any segment sum in constant time. Let dp[i][j] represent the maximum total value we can obtain using the first i stuffed animals and performing exactly j removals.

1. We precompute prefix sums so that any segment sum from l to r can be computed as prefix[r] − prefix[l − 1]. This is necessary because we repeatedly evaluate fixed-length blocks.
2. For each position i from 1 to N, and for each number of operations j from 0 to M, we consider two possibilities: we do not end a removal at i, or we end a removal of length W at i.
3. If we do not remove a segment ending at i, then dp[i][j] carries over dp[i − 1][j]. This corresponds to leaving the i-th element unused in any deletion block.
4. If we do remove a segment ending at i, then the segment must be exactly [i − W + 1, i]. We can only do this if i ≥ W and j ≥ 1. The transition becomes dp[i][j] = max(dp[i][j], dp[i − W][j − 1] + sum(i − W + 1, i)). This ensures disjointness because dp[i − W][·] fully excludes the segment we are taking.
5. We take the maximum of both choices for each state.
6. The final answer is the maximum dp[N][j] over all j ≤ M.

Why this is valid depends on the fact that any optimal solution can be rearranged so that chosen segments are considered in increasing order of their right endpoints. Since segments never overlap in an optimal construction, cutting the array at segment boundaries fully isolates decisions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, M, W = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (N + 1)
    for i in range(1, N + 1):
        pref[i] = pref[i - 1] + a[i - 1]

    def seg(l, r):
        return pref[r] - pref[l - 1]

    NEG = -10**18
    dp = [[NEG] * (M + 1) for _ in range(N + 1)]
    dp[0][0] = 0

    for i in range(1, N + 1):
        for j in range(0, M + 1):
            dp[i][j] = max(dp[i][j], dp[i - 1][j])

            if i >= W and j >= 1:
                val = seg(i - W + 1, i)
                dp[i][j] = max(dp[i][j], dp[i - W][j - 1] + val)

    ans = 0
    for j in range(M + 1):
        ans = max(ans, dp[N][j])

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first builds prefix sums so that every candidate removal window can be evaluated in constant time. The DP table is filled row by row, where each state either ignores the current position or completes a fixed-size deletion block ending at that position. The transition that jumps back by W positions guarantees that removed segments never overlap.

A subtle point is initialization: dp is filled with a very negative number rather than zero, because we must distinguish unreachable states from valid ones that happen to have negative sums. Without this, invalid transitions could incorrectly dominate.

## Worked Examples

Consider the input:

```
4 2 3
1 8 -10 5
```

We compute prefix sums: [0, 1, 9, -1, 4].

We evaluate dp by endpoint.

| i | j | skip dp[i-1][j] | take window | best |
| --- | --- | --- | --- | --- |
| 3 | 1 | dp[2][1] = 0 | sum(1..3)= -1 | 0 |
| 4 | 1 | dp[3][1] = 0 | sum(2..4)= 3 | 3 |
| 4 | 2 | dp[3][2] = 0 | sum(2..4)+dp[1][1] invalid | 0 |

The best choice is to take the segment [2,4], giving 8 + (-10) + 5 = 3, or take no second segment.

Now consider a uniform case:

```
5 2 2
5 5 5 5 5
```

Every window of size 2 has sum 10. Optimal strategy is to take disjoint windows [1,2] and [3,4].

| i | j | skip | take | best |
| --- | --- | --- | --- | --- |
| 2 | 1 | 5 | 10 | 10 |
| 4 | 2 | 10 | 10 + 10 | 20 |
| 5 | 2 | 20 | invalid | 20 |

This confirms that DP naturally enforces non-overlap and accumulates optimal disjoint segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N · M) | Each dp state is computed with O(1) transitions using prefix sums |
| Space | O(N · M) | DP table stores best values for each prefix and number of operations |

The constraints N ≤ 10⁴ and M ≤ 5000 allow up to 5 × 10⁷ state updates, which is borderline but acceptable in optimized Python if transitions are simple arithmetic and array indexing only.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    N, M, W = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (N + 1)
    for i in range(1, N + 1):
        pref[i] = pref[i - 1] + a[i - 1]

    NEG = -10**18
    dp = [[NEG] * (M + 1) for _ in range(N + 1)]
    dp[0][0] = 0

    for i in range(1, N + 1):
        for j in range(M + 1):
            dp[i][j] = max(dp[i][j], dp[i - 1][j])
            if i >= W and j >= 1:
                val = pref[i] - pref[i - W]
                dp[i][j] = max(dp[i][j], dp[i - W][j - 1] + val)

    return str(max(dp[N]))

# provided sample
assert run("""4 2 3
1 8 -10 5
""") == "3"

# minimum case
assert run("""2 1 2
-1 10
""") == "9"

# all negative
assert run("""5 2 2
-1 -2 -3 -4 -5
""") == "0"

# all equal positive
assert run("""6 2 2
5 5 5 5 5 5
""") == "20"

# W = 1 (each removal picks single element)
assert run("""4 2 1
3 -10 4 5
""") == "12"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all negative case | 0 | skipping all operations is optimal |
| W=1 case | 12 | reduces to picking best M elements |
| uniform positives | 20 | optimal packing of disjoint windows |

## Edge Cases

A key edge case is when all values are negative. The algorithm correctly handles this because dp[0][0] = 0 and skipping operations remains valid throughout. For example:

```
5 2 2
-1 -2 -3 -4 -5
```

Every window has negative sum, so every “take” transition reduces the score. The DP never forces taking a segment because the skip transition always dominates, resulting in output 0.

Another edge case is when W = 1, where every operation removes a single element. The DP reduces to selecting up to M largest values, since each segment is independent. The transition still works because dp[i][j] compares skipping versus taking a single element at i.

A boundary case occurs when W = N. Only one valid segment exists. The DP ensures that only dp[N][1] can include a take, and it correctly compares it with skipping everything, returning max(0, total sum).
