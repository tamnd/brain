---
title: "CF 103800C - Ginger's sequence"
description: "We are given an array of integers and a modulus value k. From the array, we can choose any non-empty subsequence, meaning we pick some indices while preserving order, but order itself does not affect the sum so effectively we only care about which elements are selected."
date: "2026-07-02T08:42:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103800
codeforces_index: "C"
codeforces_contest_name: "The 2022 SDUT Summer Trials"
rating: 0
weight: 103800
solve_time_s: 58
verified: true
draft: false
---

[CF 103800C - Ginger's sequence](https://codeforces.com/problemset/problem/103800/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a modulus value k. From the array, we can choose any non-empty subsequence, meaning we pick some indices while preserving order, but order itself does not affect the sum so effectively we only care about which elements are selected.

Each chosen subsequence has a sum. The task is to determine whether it is possible to find two different non-empty subsequences whose sums leave the same remainder when divided by k.

Equivalently, we want to know whether there exist two distinct subset sums that are congruent modulo k. The distinction between subsequences and subsets does not matter here because the sum depends only on the chosen elements.

The constraints n ≤ 10^5 and k ≤ 10^5 immediately rule out any approach that enumerates subsequences or even subset sums explicitly. The number of subsequences is 2^n, which is far beyond feasible computation. Even dynamic programming over all subsets is impossible if it tries to track exact sums up to large values.

The only manageable state space is modulo k, which suggests that all relevant information collapses into k possible residues.

A key subtle edge case is when k = 1. In that case, every subsequence sum is congruent to 0, so if there are at least two different non-empty subsequences, the answer is always YES. Since n ≥ 1 implies at least one subsequence, but we need two distinct ones, the only problematic situation would be n = 1, where there is only one non-empty subsequence. So for n ≥ 2 and k = 1, the answer is trivially YES.

Another edge case appears when many elements are zero or multiples of k. These do not change residues, so they can artificially inflate the number of subsequences producing the same remainder, making duplicates unavoidable unless n is extremely small.

## Approaches

The brute-force approach would enumerate all subsequences, compute each sum, take it modulo k, and check for collisions. This is correct because it directly inspects every possible subsequence sum. However, the number of subsequences is 2^n, so for n = 100000 this is impossible even conceptually, and even for n = 40 it already becomes borderline.

A more structured view comes from realizing we do not actually care about full sums, only their residues modulo k. Each element ai contributes a residue ai mod k, and we are forming subset sums modulo k. This becomes a classic subset sum in a cyclic group of size k.

We can maintain which residues are reachable using dynamic programming over k states. Each element updates the set of reachable residues by adding ai mod k. However, this only tells us which residues are achievable, not how many different subsequences achieve them. The problem asks for existence of two different subsequences with the same sum modulo k, meaning we want to detect whether any residue can be formed in at least two distinct ways.

This reduces to detecting whether the number of distinct subsequences exceeds k, but with a stronger constraint: collisions in modulo space must occur during construction. The key observation is that if at any point we have more than k distinct subset sums modulo k, then by pigeonhole principle two distinct subsets must share the same remainder. Since there are only k possible remainders, any set of k+1 distinct subsequences must collide.

We can therefore construct a set of reachable states and stop as soon as we exceed k distinct states.

We track DP states as a boolean array over residues. Each element updates the set, and we also track whether we create a new subset that did not exist before. If at any point the total number of reachable subsets exceeds k, we can immediately return YES.

A more efficient interpretation avoids full subset DP and instead uses a standard trick: if n > k, answer is always YES. This is because consider prefix subsequences: among the first k+1 elements, consider their prefix sums modulo k. There are k residues but k+1 prefixes, so two must match, producing a valid pair of different subsequences with equal sum mod k.

If n ≤ k, we can safely run subset DP over modulo states using bitsets or sets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsequences | O(2^n · n) | O(n) | Too slow |
| Modular subset DP | O(n · k) | O(k) | Accepted |

## Algorithm Walkthrough

We split the solution into two regimes depending on the relationship between n and k.

1. If n > k, we immediately conclude the answer is YES. This follows from the pigeonhole principle applied to prefix sums modulo k, where k+1 prefixes guarantee a repeated remainder difference, implying two different subsequences with equal modular sum.
2. If n ≤ k, we maintain a boolean array dp of size k, where dp[x] indicates whether there exists a subsequence whose sum is congruent to x modulo k.
3. Initialize dp with dp[0] = True, representing the empty subsequence. We conceptually exclude it later since we only need non-empty subsequences, but it is useful for transitions.
4. For each element value v in the array, compute r = v mod k, and update the dp array by considering all existing reachable states. For each residue x where dp[x] is true, we can form a new subsequence with residue (x + r) mod k.
5. While updating, if we ever try to set a residue that was already set in this iteration in a way that indicates multiple constructions of the same residue via different subset choices, we detect that a collision exists and return YES.
6. If after processing all elements no collision is found, return NO.

Why it works: the dp array represents the set of all achievable subset sums modulo k. If at any point two distinct subsets produce the same residue, then dp would attempt to assign the same state through different combinations. The moment such duplication becomes unavoidable corresponds exactly to the existence of two different subsequences with equal sum modulo k. The state space is bounded by k residues, so once construction forces overlap beyond uniqueness, a valid pair must exist.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    if k == 1:
        # all sums are 0 mod 1, need two distinct non-empty subsequences
        return "YES" if n >= 2 else "NO"

    if n > k:
        return "YES"

    dp = [False] * k
    dp[0] = True

    seen_count = [0] * k
    seen_count[0] = 1

    for v in a:
        r = v % k
        new_seen = seen_count[:]  # copy counts

        for x in range(k):
            if seen_count[x]:
                nx = (x + r) % k
                new_seen[nx] += seen_count[x]

                if new_seen[nx] >= 2:
                    return "YES"

        seen_count = new_seen

    return "NO"

if __name__ == "__main__":
    print(solve())
```

The code first handles the degenerate modulus case k = 1 separately. It then applies the observation that large n relative to k forces a collision.

For the DP phase, instead of only tracking reachability, it tracks how many ways each residue can be formed. This allows early detection of when a residue is produced in more than one distinct way, which corresponds to two different subsequences with the same sum modulo k.

The key implementation detail is copying the state array before updating. This ensures we do not reuse newly updated states within the same iteration, which would incorrectly merge different subset sizes.

## Worked Examples

### Example 1

Input:

n = 5, k = 10

array = [1, 2, 3, 4, 5]

We track residue counts.

| Step | Element | Update residue | Key dp state change | Collision? |
| --- | --- | --- | --- | --- |
| 0 | - | {0:1} | initial | No |
| 1 | 1 | 1 | 0→1 adds residue 1 | No |
| 2 | 2 | 2 | creates new residues including 3 | No |
| 3 | 3 | 3 | multiple new combinations emerge | No |
| 4 | 4 | 4 | further growth | No |
| 5 | 5 | 5 | residue space becomes crowded | YES eventually |

At the end, multiple distinct subsets generate overlapping residues modulo 10, so the answer is YES. This aligns with the fact that subset combinations grow faster than available residues.

### Example 2

Input:

n = 2, k = 100

array = [1, 2]

| Step | Element | Residues formed | Collision? |
| --- | --- | --- | --- |
| 0 | - | {0} | No |
| 1 | 1 | {0,1} | No |
| 2 | 2 | {0,1,2,3} | No |

No residue is produced in two different ways, so answer is NO.

This shows that small n relative to k can avoid collisions entirely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk) | Each element updates k residues in the worst case |
| Space | O(k) | We store counts for k residue classes |

Since n and k are both up to 10^5, the O(nk) bound is too large in worst case, but the early exit for n > k and the typical pruning behavior in practice keeps it within limits intended by the problem structure. The real intended solution relies primarily on the pigeonhole argument for n > k and small DP otherwise.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# sample
assert run("5 10\n1 2 3 4 5\n") == "YES"

# minimum size
assert run("1 5\n7\n") == "NO"

# k = 1 edge
assert run("1 1\n10\n") == "NO"
assert run("3 1\n1 2 3\n") == "YES"

# identical elements
assert run("3 5\n5 5 5\n") == "YES"

# n > k immediate YES
assert run("6 5\n1 1 1 1 1 1\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1,k=5 | NO | single subsequence only |
| k=1,n=3 | YES | all sums identical mod 1 |
| repeated multiples of k | YES | trivial collisions |
| n > k | YES | pigeonhole shortcut |

## Edge Cases

For k = 1, every subsequence sum is 0 modulo 1. If n = 1, there is only one non-empty subsequence, so no pair exists and the answer is NO. For n ≥ 2, there are multiple distinct subsequences all mapping to the same residue, so the answer becomes YES.

For small n but large k, for example n = 2, k = 100, no collision can occur because there are at most 3 non-empty subsequences and 100 possible residues, so each subset sum modulo k remains unique. The DP will maintain distinct residues without any duplication, correctly returning NO.
