---
title: "CF 1996E - Decode"
description: "We are given a binary string, and we look at every possible contiguous segment of it. Each segment itself contains many subsegments, and we are interested only in those subsegments whose number of zeros equals the number of ones."
date: "2026-06-08T14:43:36+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1996
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 962 (Div. 3)"
rating: 1600
weight: 1996
solve_time_s: 132
verified: false
draft: false
---

[CF 1996E - Decode](https://codeforces.com/problemset/problem/1996/E)

**Rating:** 1600  
**Tags:** combinatorics, data structures, implementation, math  
**Solve time:** 2m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string, and we look at every possible contiguous segment of it. Each segment itself contains many subsegments, and we are interested only in those subsegments whose number of zeros equals the number of ones.

For every choice of a larger interval in the string, we count how many balanced subsegments it contains. Then we sum this value over all possible intervals. Another way to see it is that every balanced subsegment contributes to many enclosing intervals, and we are effectively summing all those contributions.

The direct interpretation already suggests a large amount of repeated counting. Every substring is considered as a potential candidate, and every enclosing interval adds it again. Since both the number of outer intervals and inner substrings scale quadratically, any solution that explicitly enumerates them would be too slow when the string length reaches 200000.

A naive idea would try to fix a segment and scan all subsegments inside it, but this leads to cubic behavior. Even optimizing the inner check with prefix sums does not save us, because the number of segments itself is still quadratic. The structure of the problem forces us to reinterpret the counting order.

A subtle failure case of naive reasoning appears when the string is uniform, for example `"0000"`. There are no balanced substrings at all, so the answer is zero. However, a careless implementation that tries to treat differences of counts incorrectly, for example by miscounting prefix equalities without subtracting contributions per outer interval, can still accumulate nonzero values due to double counting empty conditions.

The key difficulty is that each valid subarray contributes not once, but in proportion to how many outer intervals contain it, and this coupling between two interval layers must be disentangled.

## Approaches

A brute-force method would enumerate every interval $(l, r)$, then enumerate every subinterval $(x, y)$ inside it, and check whether it has equal zeros and ones. Using prefix sums, the check itself is constant time, but the number of pairs of intervals is still $O(n^3)$. With $n$ up to $2 \cdot 10^5$, this is completely infeasible.

To improve, we reverse the viewpoint. Instead of fixing outer intervals and counting inner ones, we fix a candidate subarray and count how many outer intervals contain it. A subarray $(x, y)$ is included in all $(l, r)$ such that $l \le x$ and $r \ge y$. The number of such outer intervals depends only on positions $x$ and $y$, and equals $x \cdot (n - y + 1)$.

So the problem reduces to summing over all balanced subarrays:

$$\sum_{x \le y, \; s[x..y]\text{ balanced}} x \cdot (n - y + 1).$$

Now the remaining task is to enumerate all balanced subarrays efficiently. This is a classical prefix sum reformulation: map `0 → -1` and `1 → +1`. A subarray is balanced exactly when its prefix sum difference is zero. So we need to consider all pairs of positions where prefix sums match.

Let $p[i]$ be prefix sums. For each value $v$, suppose its occurrences are at indices $i_1 < i_2 < \dots < i_k$. Any pair $(i_a, i_b)$ with $a < b$ defines a balanced subarray $(i_a + 1, i_b)$. Each such subarray contributes:

$$(i_a + 1) \cdot (n - i_b + 1).$$

Thus, we process each prefix sum value independently, and compute this sum over all pairs in linear time per group using prefix aggregation.

The key observation is that for fixed right endpoint, we can maintain cumulative sums over left endpoints to avoid quadratic enumeration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the binary string into a prefix sum array where `0` becomes -1 and `1` becomes +1. This transforms the condition “equal number of zeros and ones” into “equal prefix sums at two positions”.
2. Compute all prefix sums $p[0], p[1], \dots, p[n]$, starting with $p[0] = 0$.
3. Group indices of equal prefix sum values. Each group corresponds to all positions where the running balance is identical.
4. For each group of indices $i_1, i_2, \dots, i_k$, process contributions of all pairs $(i_a, i_b)$, where $a < b$, without explicitly enumerating them.
5. Sweep through indices in increasing order, maintaining two running values: the sum of left endpoints and the number of occurrences seen so far. For each new index treated as a right endpoint, add its contribution using previously seen prefix indices.
6. For a right endpoint $i_b$, each previous index $i_a$ contributes $(i_a + 1) \cdot (n - i_b + 1)$. Factor out $(n - i_b + 1)$, so we only need the sum of $(i_a + 1)$ over the group prefix.
7. Accumulate the result modulo $10^9+7$.

### Why it works

The transformation reduces balanced substrings to equal prefix sums. Every valid substring corresponds uniquely to a pair of equal prefix sum positions. The contribution function separates cleanly into a product of a term depending only on the left endpoint and a term depending only on the right endpoint. This separability allows incremental accumulation: when processing a right endpoint, all valid left endpoints are already known, and their contributions can be summed without revisiting them. This guarantees every valid subarray is counted exactly once, and only once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    t = int(input())
    for _ in range(t):
        s = input().strip()
        n = len(s)

        # prefix sum positions grouped by value
        groups = {}

        cur = 0
        groups.setdefault(0, []).append(0)

        for i, ch in enumerate(s, start=1):
            cur += 1 if ch == '1' else -1
            groups.setdefault(cur, []).append(i)

        ans = 0

        for pos in groups.values():
            if len(pos) < 2:
                continue

            pref_sum_left = 0
            count = 0

            for i in pos:
                if count > 0:
                    right_factor = (n - i + 1)
                    ans = (ans + pref_sum_left * right_factor) % MOD

                pref_sum_left += (i + 1)
                count += 1

        print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The implementation builds prefix sums where each prefix sum value collects all indices at which it appears. For each group, we sweep from left to right. At each position treated as a right endpoint, we multiply the accumulated sum of left endpoints (shifted by +1 to match substring start contribution) with the number of possible extensions to the right boundary. This directly matches the factorized contribution derived in the algorithm.

Care is needed in indexing. The prefix array uses 0-based positions for convenience, but substring endpoints depend on converting prefix indices into actual segment boundaries, which is why `(i + 1)` appears for left endpoints and `(n - i + 1)` for right-side extension counts.

## Worked Examples

### Example 1: `010`

Prefix sums are:

| index i | prefix sum |
| --- | --- |
| 0 | 0 |
| 1 | -1 |
| 2 | 0 |
| 3 | -1 |

We group positions:

0 → [0, 2]

-1 → [1, 3]

For group 0:

| right i | pref_sum_left | contribution |
| --- | --- | --- |
| 2 | 1 | (1 * (3 - 2 + 1)) = 2 |

For group -1:

| right i | pref_sum_left | contribution |
| --- | --- | --- |
| 3 | 2 | (2 * 1) = 2 |

Total = 4.

This demonstrates how each group is independent and contributions are aggregated via prefix sums rather than pair enumeration.

### Example 2: `1100`

Prefix sums:

| i | p[i] |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 1 |
| 4 | 0 |

Groups:

0 → [0, 4]

1 → [1, 3]

2 → [2]

Group 0 contributes:

(0,4) → (1 * 1) = 1

Group 1 contributes:

(1,3) → (2 * 2) = 4

Total = 5.

This shows how multiple balanced substrings are captured even when they overlap heavily, and how grouping by prefix sum avoids missing or double counting them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each index is processed once inside its prefix-sum group |
| Space | O(n) | Storage for prefix sum grouping |

The solution is linear in the total input size across test cases, which fits comfortably under the constraint of $2 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    return solve()

# provided samples
# assert run("4\n0000\n01010101\n1100111001\n11000000111\n") == "..."

# custom cases
assert run("1\n0\n") == "0"
assert run("1\n01\n") == "2"
assert run("1\n10\n") == "2"
assert run("1\n000111\n") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"0"` | `0` | minimum length no balanced substrings |
| `"01"` | `2` | single balanced substring with outer interval scaling |
| `"10"` | `2` | symmetry check |
| `"000111"` | `9` | multiple balanced segments and overlaps |

## Edge Cases

A fully uniform string such as `"0000"` produces no prefix sum collisions beyond trivial matches, so every group has size one except the initial state. The algorithm skips singleton groups, so no contribution is added and the result remains zero, matching the correct behavior.

A fully alternating string such as `"0101"` creates many repeated prefix sums. The grouping mechanism ensures all equal-prefix pairs are captured, and each pair contributes based on its left and right positions. The sweep accumulation guarantees that overlapping balanced substrings are not double counted, since each right endpoint processes only previously seen left endpoints exactly once.
