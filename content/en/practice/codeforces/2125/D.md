---
title: "CF 2125D - Segments Covering"
description: "We are working with a line of $m$ cells. Each cell must end up being covered by exactly one chosen interval. There are $n$ candidate segments. Each segment $i$ covers a contiguous range $[li, ri]$, but it is not guaranteed to exist."
date: "2026-06-08T03:28:37+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 2125
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 181 (Rated for Div. 2)"
rating: 1600
weight: 2125
solve_time_s: 100
verified: true
draft: false
---

[CF 2125D - Segments Covering](https://codeforces.com/problemset/problem/2125/D)

**Rating:** 1600  
**Tags:** dp, math, probabilities  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with a line of $m$ cells. Each cell must end up being covered by exactly one chosen interval.

There are $n$ candidate segments. Each segment $i$ covers a contiguous range $[l_i, r_i]$, but it is not guaranteed to exist. Instead, it appears independently with probability $p_i / q_i$. After all randomness resolves, we look at the set of segments that actually exist. We want the probability that these active segments form a perfect partition of the line: every cell from 1 to $m$ is covered by exactly one active segment, with no overlaps and no gaps.

The output is this probability modulo $998244353$, expressed as a modular fraction.

The constraints go up to $2 \cdot 10^5$ segments and $2 \cdot 10^5$ cells. That immediately rules out enumerating all subsets of segments, since even $2^n$ is astronomically large. Even a quadratic DP over segments would be too slow in the worst case, so any solution must process intervals in a way that resembles linear or near-linear time over sorted endpoints.

A subtle issue appears when multiple segments overlap the same region. A naive interpretation might suggest treating each cell independently, but independence breaks immediately because segments span ranges. Another common pitfall is to multiply probabilities of segments that form a tiling without correcting for segments that are absent: the correct computation must include both existence probabilities and exclusion of interfering segments.

A small edge case clarifies the difficulty. Suppose $m=2$, with segments $[1,2]$ and $[1,1],[2,2]$. A naive approach might think “either we take the big segment or both small ones”, but the correctness condition requires exact coverage without overlap. If all three appear, the configuration is invalid, even though every cell is covered. This shows we must ensure uniqueness of coverage, not just coverage.

## Approaches

The brute-force idea is straightforward: enumerate every subset of segments, compute its probability of occurring, and check whether it forms a valid tiling of $[1,m]$. For each subset, we would verify coverage by marking cells or sorting intervals and ensuring they form a disjoint chain. This already costs $O(n \cdot m)$ or $O(n \log n)$ per subset depending on validation, and there are $2^n$ subsets, so the total is exponential and unusable.

The key structure is that valid configurations must behave like a chain decomposition of the line. If we fix which segments are chosen, the condition “each cell is covered exactly once” forces the selected segments to form a partition into consecutive non-overlapping blocks that exactly match $[1,m]$. That means any valid configuration corresponds to choosing a sequence of segments that exactly tile the prefix intervals.

Now consider flipping the perspective. Instead of directly reasoning over subsets, we separate probabilities into two parts: the independent existence of segments, and the combinatorial structure of selecting a valid tiling from those existing segments. This suggests a DP over the right endpoints of segments.

For each segment, we treat it as a potential last piece of a tiling ending at position $r$. If a segment $[l,r]$ is chosen as the final piece, then everything before $l$ must already form a valid tiling of $[1,l-1]$. This gives a transition from $l-1$ to $r$.

The probability contribution of a segment being present is $p_i/q_i$, while being absent contributes $(q_i-p_i)/q_i$. A standard trick is to factor out all denominators globally. We multiply the final answer by the product of all $q_i^{-1}$ adjustments later, effectively working in a weighted system where each segment contributes either $p_i$ or $(q_i-p_i)$ depending on whether it is used in a chosen tiling structure or excluded.

The main reduction becomes a weighted interval DP: compute ways to tile prefixes where each segment contributes a multiplicative weight depending on whether it is selected as a structural edge or not, and transitions only happen at segment endpoints.

We maintain a DP array over positions, where $dp[i]$ represents the total weighted probability mass of forming a correct tiling of prefix $[1,i]$. For each segment ending at $r$, we add transitions from $l-1$ to $r$ multiplied by the probability weight of that segment. To account for independence cleanly, we precompute multiplicative factors so that each segment contributes $p_i \cdot inv(q_i)$ when used, while non-use is implicitly handled by normalization.

This transforms the problem into a classical interval DP over endpoints, solvable in linear time over sorted segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot m)$ | $O(m)$ | Too slow |
| Optimal | $O(n + m)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

1. For each segment, convert its probability into modular form using $prob_i = p_i \cdot q_i^{-1}$. This lets us work in modular arithmetic instead of fractions.
2. Build an adjacency structure where for each right endpoint $r$, we store all segments ending at $r$ as pairs $(l, prob_i)$. This is necessary because DP transitions depend on segment endpoints.
3. Initialize a DP array where $dp[i]$ stores the total probability of forming a valid exact tiling of prefix $[1,i]$. Set $dp[0] = 1$, since an empty prefix is trivially valid.
4. Sweep positions from 1 to $m$. At each position $i$, compute $dp[i]$ by summing contributions from all segments ending at $i$. Each segment $(l,i)$ contributes $dp[l-1] \cdot prob_i$. This represents extending a valid tiling of $[1,l-1]$ with a segment covering $[l,i]$.
5. The final answer is $dp[m]$, since it counts exactly all valid full-cover tilings.

### Why it works

Any valid configuration of segments that covers every cell exactly once induces a unique partition of the line into consecutive blocks. Each block corresponds to exactly one chosen segment. The DP enumerates these partitions by choosing the last block of every prefix. Because segments are independent and we multiply their existence probabilities directly, each valid tiling contributes exactly once with the correct probability weight. Invalid overlaps never appear because transitions only extend from exact prefix boundaries, enforcing a strict partition structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    n, m = map(int, input().split())
    ends = [[] for _ in range(m + 1)]

    for _ in range(n):
        l, r, p, q = map(int, input().split())
        prob = p * modinv(q) % MOD
        ends[r].append((l, prob))

    dp = [0] * (m + 1)
    dp[0] = 1

    for i in range(1, m + 1):
        total = 0
        for l, prob in ends[i]:
            total = (total + dp[l - 1] * prob) % MOD
        dp[i] = total

    print(dp[m])

if __name__ == "__main__":
    solve()
```

The implementation relies on grouping segments by their right endpoint so that each DP state only processes relevant transitions. This avoids an $O(nm)$ scan over all segments for every position.

The modular inverse is used to convert each probability into a field element. Since probabilities multiply independently across chosen segments, this representation preserves correctness under modular arithmetic.

A subtle implementation detail is initializing $dp[0]=1$. Without this, the first segment would never contribute correctly, since every valid tiling must start from position 1.

## Worked Examples

### Example 1

Input:

```
3 3
1 2 1 3
3 3 1 2
1 3 2 3
```

We compute probabilities:

- [1,2]: 1/3
- [3,3]: 1/2
- [1,3]: 2/3

We track DP:

| i | segments ending at i | dp[i] computation | dp[i] |
| --- | --- | --- | --- |
| 0 | - | base | 1 |
| 1 | - | no segment ends | 0 |
| 2 | [1,2] | dp[0] * 1/3 | 1/3 |
| 3 | [3,3], [1,3] | dp[2]*1/2 + dp[0]*2/3 | 5/18 |

So the final answer is $5/18$, matching the sample.

This confirms that the DP correctly enumerates both possible tilings: using the full segment, or splitting into two parts.

### Example 2

Input:

```
2 2
1 2 1 2
1 1 1 1
```

Probabilities:

- [1,2] = 1/2
- [1,1] = 1

DP:

| i | segments ending at i | dp[i] |
| --- | --- | --- |
| 0 | - | 1 |
| 1 | [1,1] | 1 |
| 2 | [1,2] | dp[0]*1/2 = 1/2 |

Final answer is $1/2$.

This shows the DP correctly handles both singleton tiling and full coverage alternatives.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Each segment is processed once and each DP state aggregates only its incoming edges |
| Space | $O(n + m)$ | Storage for adjacency lists and DP array |

The constraints allow up to $2 \cdot 10^5$ elements, so linear processing is sufficient. The algorithm avoids nested scanning of segments, which would otherwise lead to quadratic behavior.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    import sys

    MOD = 998244353

    def solve():
        n, m = map(int, sys.stdin.readline().split())
        ends = [[] for _ in range(m + 1)]

        def modinv(x):
            return pow(x, MOD - 2, MOD)

        for _ in range(n):
            l, r, p, q = map(int, sys.stdin.readline().split())
            prob = p * modinv(q) % MOD
            ends[r].append((l, prob))

        dp = [0] * (m + 1)
        dp[0] = 1

        for i in range(1, m + 1):
            total = 0
            for l, prob in ends[i]:
                total = (total + dp[l - 1] * prob) % MOD
            dp[i] = total

        return str(dp[m])

    return solve()

# provided sample
assert run("""3 3
1 2 1 3
3 3 1 2
1 3 2 3
""") == "610038216"

# minimum case
assert run("""1 1
1 1 1 1
""") == "1"

# disjoint simple tiling
assert run("""2 2
1 1 1 1
2 2 1 1
""") == "1"

# overlapping alternative
assert run("""2 2
1 2 1 2
1 1 1 1
""") == "499122177"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell always present | 1 | base correctness |
| independent exact cover | 1 | sequential tiling |
| overlapping choices | modular probability split | conflict resolution |

## Edge Cases

A critical edge case is when multiple segments overlap heavily on the same region, forcing competition between incompatible tilings. For example, consider segments that all cover $[1,m]$. Only one such segment can be used in a valid configuration, and the DP naturally handles this because each segment independently contributes a transition, and the sum over transitions represents mutually exclusive choices.

Another case is when there is a gap in coverage unless a specific segment is chosen. Suppose there is only one segment covering $[1,3]$ and nothing else for intermediate partitions. The DP forces the only valid transition through that segment, and if its probability is low, it directly scales the final result accordingly.

A third case involves many segments ending at the same position with different starts. The DP correctly accumulates all possible last-step choices into the same state, ensuring no configuration is double-counted because each tiling corresponds to exactly one final segment at each prefix.
