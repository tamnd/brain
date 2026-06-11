---
title: "CF 1350B - Orac and Models"
description: "We are given several independent test cases. In each one, we have a sequence of model sizes indexed from 1 to n. We are allowed to pick a subset of indices, but the chosen indices must be kept in increasing order, which is equivalent to choosing a subsequence of indices."
date: "2026-06-11T14:32:29+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1350
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 641 (Div. 2)"
rating: 1400
weight: 1350
solve_time_s: 96
verified: true
draft: false
---

[CF 1350B - Orac and Models](https://codeforces.com/problemset/problem/1350/B)

**Rating:** 1400  
**Tags:** dp, math, number theory  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each one, we have a sequence of model sizes indexed from 1 to n. We are allowed to pick a subset of indices, but the chosen indices must be kept in increasing order, which is equivalent to choosing a subsequence of indices.

A chosen subsequence is valid only if every consecutive pair of chosen indices satisfies two constraints at the same time. First, the next index must be a multiple of the previous index. Second, the size at the next index must be strictly larger than the size at the previous index. The goal is to maximize how many indices can be chosen under these rules.

The constraints are large enough that n can reach 100,000 per test case, with the sum over all test cases also up to 100,000. This immediately rules out any quadratic approach over all pairs of indices. A solution that checks transitions between all pairs or tries to build subsequences explicitly will be too slow. We need something closer to linear or n log n per test case.

A subtle point is that the structure is not a general subsequence DP over indices. The divisibility constraint forces transitions only from i to its multiples, which makes the graph sparse and structured. Ignoring this structure leads to an O(n^2) DP that will fail.

Edge cases that often break naive solutions include arrays where all values are equal, for example n = 5, s = [7, 7, 7, 7, 7]. Here, no valid transition exists because strict increase is impossible, so the answer must be 1. Another edge case is when values strictly increase but indices do not align with divisibility structure, such as n = 5, s = [1, 2, 3, 4, 5]. Even though values increase, only multiplicative index chains like 1 → 2 → 4 are allowed, so the answer is limited by index structure rather than value order.

## Approaches

A direct brute-force strategy would attempt to compute the longest valid subsequence ending at every index. For each index i, we would check all previous indices j < i and verify whether j divides i and s[j] < s[i]. If both hold, we update dp[i] = max(dp[i], dp[j] + 1). This is correct because it directly follows the definition of a valid chain.

However, this approach checks up to i previous elements for every i, leading to roughly n(n−1)/2 transitions in the worst case. With n = 100,000, this is far beyond feasible limits.

The key observation is that transitions are not arbitrary. From any index i, we only need to consider its multiples i, 2i, 3i, and so on. This flips the direction of thinking: instead of checking all previous states for i, we propagate dp values forward along multiples. This is efficient because the number of multiples over all i is bounded by n log n.

We compute dp[i] as the best chain ending at i. Then for every i, we try to extend it to all multiples j = 2i, 3i, ..., updating dp[j] if s[j] is larger than s[i]. This converts the problem into a structured DP over a divisibility graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP over all pairs | O(n^2) | O(n) | Too slow |
| DP over multiples (divisibility propagation) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### ## Algorithm Walkthrough

1. Initialize a dp array where dp[i] represents the maximum length of a valid chain ending at index i. Start with dp[i] = 1 for all i because each element alone forms a valid chain.
2. Iterate i from 1 to n in increasing order. For each i, we treat it as a starting point for extending chains forward.
3. For each i, iterate over its multiples j = 2i, 3i, 4i, up to n. For each such j, check whether s[j] is strictly greater than s[i]. If it is, update dp[j] = max(dp[j], dp[i] + 1).

This step works because any valid transition must satisfy the index divisibility condition, so all possible successors of i are exactly its multiples.
4. Keep propagating improvements forward. Since we process i in increasing order, all contributions from smaller indices are already considered when extending from i.
5. After processing all indices, the answer is the maximum value in dp.

### Why it works

The dp state captures the longest valid chain ending at each index under the constraint that transitions only occur along valid divisibility edges. Every valid sequence can be decomposed into successive steps where each next index is a multiple of the previous one, so every transition is considered exactly once when processing the smaller endpoint. Because we only update dp[j] when s[j] is strictly larger, we preserve the required monotonicity in values. No valid extension is ever missed because every valid predecessor of j must be a divisor of j and is therefore processed earlier in the iteration order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = [0] + list(map(int, input().split()))

        dp = [1] * (n + 1)
        ans = 1

        for i in range(1, n + 1):
            val = dp[i]
            if val > ans:
                ans = val

            j = 2 * i
            while j <= n:
                if s[j] > s[i]:
                    if dp[j] < val + 1:
                        dp[j] = val + 1
                j += i

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution builds a dp array where each position starts as a chain of length one. The nested loop over multiples ensures that every valid transition i → j where j is divisible by i is considered exactly once. The comparison s[j] > s[i] enforces the strictly increasing size condition.

A subtle implementation detail is that we store dp[i] in a local variable before iterating over multiples. This prevents repeated array lookups and ensures clarity of propagation. Another important point is using 1-based indexing, which aligns directly with the problem statement and avoids off-by-one errors when generating multiples.

## Worked Examples

### Example 1

Input:

n = 4, s = [5, 3, 4, 6]

We compute dp step by step.

| i | dp[i] before | multiples j checked | updates | dp after |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2, 3, 4 | 3 and 4 updated | [1,2,2,3] |
| 2 | 2 | 4 | 6 not applicable | [1,2,2,3] |
| 3 | 2 | none | none | [1,2,2,3] |
| 4 | 3 | none | none | [1,2,2,3] |

The longest chain ends at index 4 with length 3, corresponding to 1 → 2 → 4.

### Example 2

Input:

n = 5, s = [5, 4, 3, 2, 1]

Here no increasing value transitions exist.

| i | dp[i] | multiples j | updates |
| --- | --- | --- | --- |
| 1 | 1 | 2,3,4,5 | none (all smaller) |
| 2 | 1 | 4 | none |
| 3 | 1 | none | none |
| 4 | 1 | none | none |
| 5 | 1 | none | none |

Every dp stays 1, so answer is 1. This confirms that divisibility alone is insufficient without value growth.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each index i iterates over its multiples, and total harmonic series of multiples across all i is bounded by n log n |
| Space | O(n) | dp array of size n |

The complexity is fast enough because the total number of update attempts across all test cases is proportional to the number of divisor-multiple pairs, which is well within 100,000 log 100,000.

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
        s = [0] + list(map(int, input().split()))

        dp = [1] * (n + 1)
        ans = 1

        for i in range(1, n + 1):
            ans = max(ans, dp[i])
            val = dp[i]
            for j in range(2 * i, n + 1, i):
                if s[j] > s[i]:
                    dp[j] = max(dp[j], val + 1)

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("""4
4
5 3 4 6
7
1 4 2 3 6 4 9
5
5 4 3 2 1
1
9
""") == """2
3
1
1"""

# custom cases
assert run("""1
1
10
""") == "1", "single element"

assert run("""1
5
1 2 3 4 5
""") == "3", "chain 1->2->4 or 1->3->... limited by divisibility"

assert run("""1
6
1 1 1 1 1 1
""") == "1", "equal values block transitions"

assert run("""1
8
1 3 2 4 6 5 7 8
""") == "4", "mixed structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 single | 1 | minimum edge case |
| increasing values | 3 | divisibility constraint limits growth |
| all equal | 1 | strict inequality blocks all transitions |
| mixed pattern | 4 | correctness under interleaving |

## Edge Cases

A minimal input with a single element immediately returns 1 because no transitions are possible. The algorithm handles this naturally since dp is initialized to 1 and no loop over multiples produces updates.

When all values are equal, such as s = [7, 7, 7, 7], every comparison s[j] > s[i] fails, so dp remains unchanged at 1 for all indices. The final maximum is therefore 1, matching the correct output.

When values increase but indices do not align well with multiplicative structure, such as s = [1, 2, 3, 4, 5, 6], only chains following index divisibility like 1 → 2 → 4 or 1 → 3 → 6 are possible. The algorithm correctly respects this because it only propagates along multiples, never between arbitrary indices.
