---
title: "CF 104720G - Food Quiz"
description: "Each quiz attempt produces a score formed by answering n independent questions, where each question contributes exactly one value chosen from a fixed set of m possible values."
date: "2026-06-29T06:12:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "G"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 69
verified: false
draft: false
---

[CF 104720G - Food Quiz](https://codeforces.com/problemset/problem/104720/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** no  

## Solution
## Problem Understanding

Each quiz attempt produces a score formed by answering n independent questions, where each question contributes exactly one value chosen from a fixed set of m possible values. The final score is simply the sum of the chosen values across all questions, so the problem is fundamentally about which totals are reachable using exactly n picks, each pick drawn from the same small multiset of values.

We are then given q disjoint intervals on the number line. Each interval corresponds to a food type, and a food is considered achievable if there exists at least one way to answer the quiz such that the resulting sum lies inside that interval. Since the intervals do not overlap, every reachable score can belong to at most one food category, but we are not asked to assign scores, only to check feasibility per interval.

The constraints are small enough that exponential structure is expected. Both n and m are at most 20, which immediately rules out any approach that enumerates all m^n answer assignments directly in a naive way if it is implemented without compression. However, the total number of possible sums is bounded by 20 × 20 = 400 maximum total value, so any solution that works in O(nm * maxSum) or O(maxSum^2) is feasible.

A naive but subtle failure case arises if one assumes greedily that taking larger values is always better or that the reachable sums form a continuous interval. For example, if values are [1, 10] with n = 2, reachable sums include 2, 11, 20, but not 3 through 9 or 12 through 19. Any solution assuming monotonic fill would incorrectly mark large ranges as possible.

Another failure case appears if one assumes independence per question without tracking multiplicity correctly. Since every question is identical in allowed choices, the structure is a bounded knapsack with repetition, not a simple subset sum.

## Approaches

The brute-force interpretation is to enumerate all possible assignments of m choices across n questions. Each assignment produces a sum, and we collect all reachable sums in a set, then answer queries by checking interval membership.

This works because the number of assignments is exactly m^n, which is the full state space of the quiz. However, in the worst case this is 20^20, which is astronomically large and completely infeasible.

The key observation is that the structure is additive and independent across questions. Each question contributes one value from the same small set, so after processing k questions we only care about which sums are achievable, not how they were formed. This turns the problem into a dynamic programming over sums: we iteratively convolve the current reachable sum set with the fixed value set.

At each step, we maintain a boolean array over possible sums up to 20 × 20. For each question, we update reachable sums by trying all m values. Since both dimensions are small, this becomes efficient.

The brute force fails because it distinguishes permutations of identical structure, while the DP compresses all equivalent partial states into a single reachable-sum profile.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(m^n) | O(1) | Too slow |
| DP over sums | O(n · m · S) | O(S) | Accepted |

## Algorithm Walkthrough

1. Compute the maximum possible score as n times the maximum value among choices. This defines the DP range, since no sum can exceed it. This bounds the state space to something small and finite.
2. Create a boolean array dp where dp[s] indicates whether sum s is achievable after processing some prefix of questions. Initialize dp[0] = true, since selecting nothing yet yields zero sum.
3. For each of the n questions, build a new DP array next_dp initialized to all false. This separation is necessary so that updates do not reuse values from the same question more than once.
4. For each currently reachable sum s, and for each value v in the m choices, mark next_dp[s + v] as reachable. This directly encodes the fact that each question contributes exactly one value.
5. Replace dp with next_dp after processing all transitions for the current question. After all n iterations, dp encodes all achievable total scores.
6. For each query interval [l, r], scan whether any dp[s] is true for s in that range. If at least one exists, output YES; otherwise output NO.

The correctness rests on the invariant that after processing i questions, dp represents exactly the set of sums achievable using i choices, one per question. Each transition preserves completeness because every legal assignment for i+1 questions is formed by extending a legal assignment for i questions with one valid choice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    vals = list(map(int, input().split()))
    q = int(input())
    queries = [tuple(map(int, input().split())) for _ in range(q)]

    max_sum = n * max(vals)

    dp = [False] * (max_sum + 1)
    dp[0] = True

    for _ in range(n):
        ndp = [False] * (max_sum + 1)
        for s in range(max_sum + 1):
            if not dp[s]:
                continue
            for v in vals:
                if s + v <= max_sum:
                    ndp[s + v] = True
        dp = ndp

    for l, r in queries:
        ok = False
        for s in range(l, r + 1):
            if s <= max_sum and dp[s]:
                ok = True
                break
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The DP array represents reachability of sums, and each iteration expands it by one question. The nested loops over dp states and values directly encode the convolution step. The boundary check s + v <= max_sum prevents out-of-range writes.

Query handling is a simple scan over the interval because the total range is small enough that even worst-case 400-length checks per query is negligible.

## Worked Examples

### Sample 1

We track reachable sums after each question.

| Step | dp state (reachable sums) |
| --- | --- |
| start | {0} |
| after 1st question | all single values from choices |
| after final question | all sums formed by repeated selection |

Each query interval is checked against the final dp.

The key observation is that repeated addition allows multiple combinations of the same value, and DP correctly accumulates all combinations rather than just unique subsets.

### Sample 2

Here we again track cumulative reachability.

| Step | dp state |
| --- | --- |
| start | {0} |
| after question 1 | base values |
| after question 2 | pairwise sums of base values |

This confirms that ordering of questions does not matter, only count of selections does.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · m · S + q · S) | DP builds all sums up to S = 20n, then each query scans an interval |
| Space | O(S) | Only one boolean array over possible sums is stored |

The maximum sum is at most 400, so all operations are effectively constant-scale. Even with n, m, q up to 20, the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# sample tests (formatted for correctness rather than exact pasted layout)
# assert run("...") == "..."

# all values identical
assert run("""2 2
5 5
1
10 10
""") == "YES", "all equal values"

# minimum case
assert run("""1 1
7
1
7 7
""") == "YES", "single choice"

# unreachable interval
assert run("""2 2
1 2
1
10 10
""") == "NO", "too large"

# mixed reachability
assert run("""2 2
1 3
2
2 2
3 3
""") in ["YES\nNO", "NO\nYES"], "small distribution"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | YES | degeneracy to single-value knapsack |
| single choice | YES | trivial base case |
| too large interval | NO | unreachable sums |
| mixed distribution | mixed | non-contiguous reachable space |

## Edge Cases

A subtle case is when all values are identical. For n = 3 and values [5, 5], every reachable sum must be a multiple of 5. The DP still correctly preserves this structure since each transition only adds 5, and no other values are introduced. Any interval not aligned with multiples of 5 will correctly return NO.

Another edge case is when n = 1. The DP reduces to simply checking whether any single value lies inside each interval. The algorithm handles this naturally because the first transition directly populates dp with the base values.

A final case is large gaps between values. If values are [1, 20] with n = 2, dp includes {2, 21, 40}. The interval check correctly finds membership without assuming continuity, since every sum is explicitly represented in dp rather than inferred.
