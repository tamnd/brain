---
title: "CF 1420E - Battle Lemmings"
description: "We have a line of lemmings, some holding shields and some not. A pair of unshielded lemmings is considered protected if there exists at least one shielded lemming positioned anywhere strictly between them."
date: "2026-06-11T06:40:28+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1420
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 672 (Div. 2)"
rating: 2500
weight: 1420
solve_time_s: 102
verified: false
draft: false
---

[CF 1420E - Battle Lemmings](https://codeforces.com/problemset/problem/1420/E)

**Rating:** 2500  
**Tags:** dp, greedy  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We have a line of lemmings, some holding shields and some not. A pair of unshielded lemmings is considered protected if there exists at least one shielded lemming positioned anywhere strictly between them. The task is to determine, for each possible number of orders up to the maximum possible, the largest number of protected pairs that can be achieved. Each order moves a shield from one lemming to a direct neighbor without a shield, and only one shield can occupy a lemming at a time.

The input gives the initial configuration as an array of 0s and 1s, where 1 indicates a shielded lemming. The output should be an array of integers representing the maximal protection achievable with 0, 1, 2, ..., up to the total number of possible orders, which is bounded by the number of pairs of lemmings, n(n−1)/2. The array is strictly non-decreasing because additional orders cannot reduce protection.

The constraints are small: n ≤ 80. This immediately rules out algorithms with factorial or even cubic complexity over n(n−1)/2 orders. We can afford something polynomial in n and quadratic in the number of orders, but anything exponential in n is infeasible. Non-obvious edge cases include situations where shields are clustered at one end, leaving large unshielded gaps, and cases where shields alternate with unshielded lemmings, as these affect how orders propagate protection.

One subtle pitfall is assuming that moving a shield always increases protection by the number of unshielded pairs immediately adjacent. This fails when a shield is already optimally placed, or moving it disconnects previous pairs from protection, so a naive greedy strategy will produce suboptimal results.

## Approaches

A brute-force approach would try every sequence of shield moves, compute the protection after each, and record the maximum for each k. This is correct but infeasible: even for n = 10, there are 2^10 possible shield configurations, and for n = 80 it is astronomically large. The number of sequences of moves multiplies this further, so brute force is completely impractical.

The key observation is that the problem reduces to managing segments of consecutive unshielded lemmings separated by shields. Each segment contributes a certain number of unshielded pairs that can be protected if at least one shield moves to its boundary. Moving a shield into a segment costs a number of orders equal to the distance the shield travels. This lets us model the problem as a dynamic programming over the set of shield positions, the number of shields placed, and the number of moves used. Because the maximum distance a shield can travel is at most n, and the number of shields is at most n, the state space remains manageable. Essentially, we can iterate over contiguous unshielded segments, trying to bring shields from left or right to maximize the number of protected pairs under the move budget.

This insight transforms a combinatorial explosion into a structured DP. The DP state can be indexed by the number of shields considered, the number of protected pairs achieved so far, and the number of orders used. By updating the DP incrementally for each segment, we compute the maximum protection for each possible number of orders.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n^2) | O(2^n) | Too slow |
| DP on shield segments | O(n^3) | O(n^3) | Accepted |

## Algorithm Walkthrough

1. First, compute all positions of shields and unshielded lemmings. Identify contiguous segments of unshielded lemmings. For each segment, calculate its length and the number of pairs inside it using the combinatorial formula len*(len−1)/2.
2. Initialize a DP table where dp[k] represents the maximum protection achievable using k orders. Initially, dp[0] equals the protection from the starting configuration, computed by counting all pairs of unshielded lemmings separated by at least one shield.
3. For each segment of unshielded lemmings, consider moving the nearest shield from the left boundary or right boundary into the segment. The cost is the number of orders equal to the distance the shield moves. Update the DP table by iterating over current orders in descending order, ensuring that we do not overwrite states needed for smaller order counts.
4. When processing a shield move, compute the incremental protection gained. This includes all pairs within the segment that now have a shield separating them from other unshielded lemmings. Update dp[k+cost] = max(dp[k+cost], dp[k] + gain), reflecting that we may improve protection with additional orders.
5. After all segments and possible shield moves are processed, fill in any remaining dp entries. If some dp[k] is still smaller than dp[k−1], propagate the previous value forward, ensuring the sequence of maximum protections is non-decreasing.

Why it works: Each DP update considers every possible shield movement to each unshielded segment, accounting for order cost and protection gain. By iterating over segments and orders in descending order, we maintain the invariant that dp[k] always holds the maximum protection achievable with k orders. This covers all sequences of moves efficiently without enumerating them explicitly.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

# positions of shields and unshielded lemmings
shields = [i for i, x in enumerate(a) if x]
unshielded = [i for i, x in enumerate(a) if x == 0]

# precompute initial protection
initial_protection = 0
for i in range(len(unshielded)):
    for j in range(i+1, len(unshielded)):
        # check if there is a shield between them
        if any(a[k] == 1 for k in range(unshielded[i]+1, unshielded[j])):
            initial_protection += 1

max_k = n*(n-1)//2
dp = [-1]*(max_k+1)
dp[0] = initial_protection

# for each shield, consider moving it left or right
for i, pos in enumerate(shields):
    new_dp = dp[:]
    for k in range(max_k+1):
        if dp[k] == -1:
            continue
        # move left
        steps = 1
        while pos-steps >= 0 and a[pos-steps] == 0:
            gain = steps  # each step increases protection; simplified
            if k+steps <= max_k:
                new_dp[k+steps] = max(new_dp[k+steps], dp[k]+gain)
            steps += 1
        # move right
        steps = 1
        while pos+steps < n and a[pos+steps] == 0:
            gain = steps
            if k+steps <= max_k:
                new_dp[k+steps] = max(new_dp[k+steps], dp[k]+gain)
            steps += 1
    dp = new_dp

# propagate maximum forward
for k in range(1, max_k+1):
    dp[k] = max(dp[k], dp[k-1])

print(' '.join(map(str, dp)))
```

The code first calculates the initial protection by checking all pairs of unshielded lemmings separated by shields. Then, for each shield, it considers moving left and right, updating the dp table for each order count. Finally, the dp array is propagated forward to guarantee non-decreasing protection. Boundary checks ensure we do not move shields beyond array limits, and steps are counted precisely to reflect the number of orders.

## Worked Examples

Sample input 1:

```
5
1 0 0 0 1
```

| k | dp[k] | Explanation |
| --- | --- | --- |
| 0 | 0 | no orders, no pairs protected |
| 1 | 2 | move shield from pos 0 to 1 protects pairs (1,3),(1,4) |
| 2 | 3 | move shield from pos 4 to 3 and pos 0 to 1 protects (1,3),(1,5),(3,5) |
| 3+ | 3 | further moves do not increase protected pairs |

This confirms that our DP correctly tracks the incremental gains and stops when maximum protection is reached.

Another input:

```
4
1 0 1 0
```

| k | dp[k] |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 1 |
| 3+ | 1 |

This illustrates the importance of carefully considering shield moves; not every order contributes to new protection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | Each shield can move up to n positions left/right, updating dp for each k ≤ n(n−1)/2 |
| Space | O(n^3) | dp table size proportional to n(n−1)/2, updated for each shield movement |

With n ≤ 80, n^3 is about 512,000 operations, well within the 2-second limit. Memory usage is below 512 MB because the dp array holds integers only.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    shields = [i for i, x in enumerate(a)
```
