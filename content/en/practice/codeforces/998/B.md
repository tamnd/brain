---
problem: 998B
contest_id: 998
problem_index: B
name: "Cutting"
contest_name: "Codeforces Round 493 (Div. 2)"
rating: 1200
tags: ["dp", "greedy", "sortings"]
answer: passed_samples
verified: true
solve_time_s: 64
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a329797-db90-83ec-b163-c4de935bce59
---

# CF 998B - Cutting

**Rating:** 1200  
**Tags:** dp, greedy, sortings  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 4s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a329797-db90-83ec-b163-c4de935bce59  

---

## Solution

## Problem Understanding

We are given a sequence of integers and we are allowed to split it into contiguous segments by making cuts between adjacent elements. Each segment must satisfy a structural constraint: the number of even values inside the segment must equal the number of odd values.

Every potential cut has a cost determined locally by the absolute difference of the two numbers it separates. We are given a budget, and we want to maximize how many cuts we perform while keeping the total cost within this budget and maintaining the validity condition on every resulting segment.

The key constraint is that the sequence already contains an equal number of even and odd values overall, which guarantees that at least one valid full-sequence segmentation exists without cuts.

The bounds are small, with n up to 100 and budget up to 100, which immediately suggests that quadratic or cubic dynamic programming is acceptable. Any solution that tries to enumerate all segmentations directly is exponential in nature, since every of the n−1 gaps can either be cut or not, leading to 2^(n−1) possibilities. That becomes around 10^30 in the worst case, which is far beyond any feasible computation.

A naive greedy strategy like “cut whenever it looks cheap” fails because a cheap early cut can block a better global arrangement. For example, if making a small-cost cut forces you to later spend expensive cuts to rebalance parity in segments, the local decision is misleading.

Another subtle failure case appears when there are multiple valid places where a segment becomes balanced. Choosing the earliest possible cut may waste budget needed for a later cut that yields more balanced segments overall.

The real difficulty is that cuts are not independent: deciding where one segment ends determines the structure of all future segments.

## Approaches

A brute-force approach would consider every subset of the n−1 possible cut positions. For each subset, we would check whether every resulting segment has equal even and odd counts, and compute the total cost of chosen cuts. This is correct because it explicitly verifies all possibilities.

However, this requires iterating over 2^(n−1) subsets, and for each subset we may scan segments in O(n), giving an exponential total complexity. Even at n = 100, this is completely infeasible.

The key observation is that we do not actually need to reason about all subsets globally. Instead, we can process the array left to right and keep track of how many evens and odds we have seen in the current segment. The moment a segment becomes balanced, we have a candidate position where a cut is allowed.

At each such candidate cut position, we face a choice: either cut here or skip it. Cutting consumes cost and increases the number of cuts by one, while skipping keeps the segment open, potentially merging future valid endpoints. This is exactly a classic “maximize count under budget” dynamic programming problem.

We define a DP state by position and remaining budget, and try all valid cut points. Since valid cut points can be precomputed, transitions become manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| DP over states | O(n^2 · B) | O(n · B) | Accepted |

## Algorithm Walkthrough

1. Precompute all positions where a cut is allowed. We scan the array while maintaining a running difference between number of even and odd elements. Whenever this difference becomes zero, the prefix ending here can form a valid segment boundary.
2. Let these valid cut positions be stored in increasing order. We only consider cuts at these positions because any valid segmentation must end each segment at such a balance point.
3. Define a dynamic programming table dp[i][b], where i represents how many valid cut positions we have considered so far, and b represents remaining budget. The value stored is the maximum number of cuts achievable.
4. Initialize dp[0][b] = 0 for all b, since before any cut position no cuts are made.
5. For each valid cut position i, compute the cost of cutting there, which is abs(a[pos] - a[pos+1]). This cost is fixed and independent of other decisions.
6. For each budget value, propagate transitions: either we do not cut at i and carry dp[i−1][b] forward, or we cut if b is sufficient, updating dp[i][b] = max(dp[i][b], dp[i−1][b − cost] + 1).
7. The final answer is the maximum value in dp[last][b] over all b ≤ B.

### Why it works

The crucial invariant is that dp[i][b] represents the best achievable number of cuts using only the first i valid cut positions and spending at most b budget. Every valid segmentation must choose cut boundaries from this set because only these positions preserve balanced segments. Since each state transition either includes or excludes a cut at a fixed valid boundary, we enumerate all structurally valid segmentations without redundancy, and budget is enforced exactly through the DP dimension.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, B = map(int, input().split())
    a = list(map(int, input().split()))

    # find valid cut positions (prefix balanced in parity sense)
    valid = []
    diff = 0  # evens - odds

    for i in range(n - 1):
        if a[i] % 2 == 0:
            diff += 1
        else:
            diff -= 1

        if diff == 0:
            cost = abs(a[i] - a[i + 1])
            valid.append(cost)

    # dp[i][b]: using first i cuts, budget b
    m = len(valid)
    dp = [[0] * (B + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        cost = valid[i - 1]
        for b in range(B + 1):
            dp[i][b] = dp[i - 1][b]
            if b >= cost:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + 1)

    print(max(dp[m]))

if __name__ == "__main__":
    solve()
```

The implementation first compresses the problem into a list of candidate cut positions where a prefix is balanced. Each candidate stores only the cost of cutting there, since the structure guarantees independence between positions.

The DP table is built row by row over these candidates. At each step we either skip or take the cut, respecting the remaining budget. The final maximum over all budgets captures the best achievable number of cuts.

A subtle detail is that we only compute cost at valid prefix boundaries. This avoids considering illegal cuts that would break the parity requirement, ensuring the DP state space is correct.

## Worked Examples

### Example 1

Input:

```
6 4
1 2 5 10 15 20
```

Valid cut positions are found by tracking parity balance:

| i | a[i] | diff | balanced? | cost |
| --- | --- | --- | --- | --- |
| 0 | 1 | -1 | no | - |
| 1 | 2 | 0 | yes | 3 |
| 2 | 5 | -1 | no | - |
| 3 | 10 | 0 | yes | 5 |
| 4 | 15 | -1 | no | - |

So valid costs are [3, 5].

Now DP considers subsets of these cuts under budget 4. Only the first cut is affordable, so result is 1.

### Example 2

Input:

```
4 1
1 3 5 7
```

Here no prefix ever has equal even and odd counts, so there are no valid cut positions. The DP table remains zero throughout, and answer is 0.

This demonstrates that absence of valid balance points correctly forbids all cuts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · B) | We evaluate at most n valid cut points, each with budget transitions up to B |
| Space | O(n · B) | DP table stores states for each prefix of cut positions and budget |

With n, B ≤ 100, the total operations are at most 10^4 states transitions, which is comfortably within limits.

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

# provided sample
assert run("6 4\n1 2 5 10 15 20\n") == "1"

# no valid cuts
assert run("4 10\n1 3 5 7\n") == "0"

# minimal balanced immediate cut
assert run("2 10\n1 2\n") == "0"

# multiple valid cuts but tight budget
assert run("6 3\n1 2 3 4 5 6\n") in ["1"]

# exact budget match for two cuts
assert run("6 100\n1 2 3 4 5 6\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no balanced prefixes | 0 | no cuts possible |
| minimal size | 0 | edge handling |
| tight budget | 1 | greedy limitation avoidance |
| large budget | 2 | full DP accumulation |

## Edge Cases

A critical edge case is when the sequence never forms a balanced prefix before the end. In that situation, valid list is empty and DP never transitions. For input `1 3 5 7`, the algorithm produces no candidates, so dp remains zero and the output is correctly 0.

Another case is when many balanced prefixes exist but their costs exceed the budget. Even though structurally many cuts are possible, DP correctly rejects them due to budget constraints, ensuring no invalid overcounting occurs.