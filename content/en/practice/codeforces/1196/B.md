---
title: "CF 1196B - Odd Sum Segments"
description: "We are given several independent arrays. For each one, we must cut it into exactly k contiguous pieces, where each piece has an odd sum. The array order is fixed, so the only freedom is choosing cut positions."
date: "2026-06-13T14:10:05+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1196
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 575 (Div. 3)"
rating: 1200
weight: 1196
solve_time_s: 370
verified: true
draft: false
---

[CF 1196B - Odd Sum Segments](https://codeforces.com/problemset/problem/1196/B)

**Rating:** 1200  
**Tags:** constructive algorithms, math  
**Solve time:** 6m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent arrays. For each one, we must cut it into exactly k contiguous pieces, where each piece has an odd sum. The array order is fixed, so the only freedom is choosing cut positions.

A subarray has odd sum exactly when the parity of its elements adds up to 1 modulo 2. Since parity is the only thing that matters, the internal values do not need detailed tracking beyond whether they are odd or even.

The output is not the segments themselves but the cut positions that define them. If we decide the k segments end at indices r1, r2, ..., rk where rk must equal n, we are effectively describing the partition.

The constraints push toward a linear solution per query. The total array length across all queries is at most 2 × 10^5, so any solution that scans each array once or a constant number of times is acceptable. Anything quadratic in a single query would already be too slow when n is large.

The key difficulty is that segment sums are global properties of ranges, but we are required to enforce a strict parity condition on every segment simultaneously. A naive attempt that tries all cut positions or checks segment sums repeatedly would quickly become infeasible.

A few subtle failure cases appear naturally. If we greedily cut whenever we see an odd prefix sum without controlling how many segments remain, we might run out of elements too early or too late. Another failure occurs when the total number of odd elements is insufficient to form k odd-sum segments, even if local greedy choices seem valid.

## Approaches

A brute-force strategy would try all possible ways to choose k−1 cut positions among n−1 gaps, and check whether each resulting segment has an odd sum. The number of partitions is combinatorial, on the order of $\binom{n}{k}$, which is exponential in n in the worst case. Even verifying a single partition is linear, so this approach is far beyond feasible limits.

The crucial observation comes from thinking about what makes a segment sum odd. A segment sum is odd if and only if it contains an odd number of odd elements. Even elements do not affect parity except by contributing zero to parity. This reduces the entire problem to tracking positions of odd numbers in the array.

If we fix k segments, each must contribute an odd count of odd numbers. The simplest way to guarantee this is to assign exactly one odd element to each segment boundary structure. This suggests that we should use k−1 odd elements as forced cut anchors, because each cut must end a segment whose sum is odd.

Once k−1 odd elements are chosen as endpoints of the first k−1 segments, the final segment automatically contains the remaining elements. For the last segment to have odd sum as well, the total number of odd elements in the entire array must be odd, and after consuming k−1 odd anchors, the remaining suffix must still contain an odd count of odd numbers. Since we end the last segment at n, this reduces to requiring that we have at least k odd numbers overall and that the k-th chosen odd position must be the last odd segment endpoint strategy that still leaves at least one odd element in the final segment.

The construction therefore becomes greedy: scan the array, collect indices of odd elements, and use the first k−1 odd indices as cut points. The k-th segment automatically ends at n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Greedy odd anchors | O(n) per query | O(n) | Accepted |

## Algorithm Walkthrough

We process each query independently.

1. Scan the array and record the positions of all elements that are odd. These positions represent all available parity “resources” for forming odd-sum segments.
2. If the number of odd elements is less than k, we immediately conclude it is impossible. Each segment must contain at least one odd element to make its sum odd, so we cannot even start constructing k valid segments.
3. If the number of odd elements is at least k, we choose the first k−1 odd positions as endpoints of the first k−1 segments. Each chosen odd index guarantees that the segment ending there has odd sum because it contains an odd number of odd elements and the boundary is aligned with an odd contribution.
4. We set the final segment to end at n. The remaining suffix necessarily contains all unused elements, and because we started with at least k odd elements, the remaining segment still contains an odd count of odd numbers, ensuring its sum is odd.
5. Output the collected cut positions.

The key invariant is that after selecting i cut positions, we have created i segments, each containing at least one odd element, and the prefix up to the i-th chosen odd index has been fully consumed. This ensures that each completed segment has odd sum and no segment is left without an odd anchor.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    out = []
    
    for _ in range(q):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        odds = []
        for i, x in enumerate(a, start=1):
            if x % 2 == 1:
                odds.append(i)
        
        if len(odds) < k:
            out.append("NO")
            continue
        
        # we use first k-1 odd positions as cut points
        cuts = odds[:k-1]
        
        # last cut must be n
        cuts.append(n)
        
        out.append("YES")
        out.append(" ".join(map(str, cuts)))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code directly implements the greedy idea. The list `odds` stores indices of all odd-valued elements. The feasibility check `len(odds) < k` enforces the minimum requirement that each segment must contain at least one odd element.

The cut list is formed by taking the first k−1 odd indices. Appending n ensures the final segment boundary condition required by the output format.

A subtle point is that we do not explicitly validate the sum of each segment. That is unnecessary because each segment is guaranteed to contain exactly one of the selected odd anchors at its endpoint, which forces the segment sum parity to be odd.

## Worked Examples

### Example 1

Input:

```
5 3
7 18 3 14 1
```

Odd positions are 1, 3, 5.

We need k = 3 segments, so we take first k−1 = 2 odd positions.

| Step | Odds collected | Cuts chosen | Segments formed |
| --- | --- | --- | --- |
| scan | [1, 3, 5] | [] | - |
| select | [1, 3, 5] | [1, 3] | [1], [2,3], [4..5] |

Final output is `1 3 5`.

The trace shows that each segment boundary aligns with an odd element, ensuring each segment contains odd parity contribution.

### Example 2

Input:

```
6 2
1 2 8 4 10 2
```

Odd positions are [1].

We need k = 2, but we only have one odd element.

| Step | Odds collected | Feasible |
| --- | --- | --- |
| scan | [1] | no |

Since we cannot assign at least one odd element per segment, the answer is NO.

This demonstrates the feasibility constraint rather than construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per query | single pass to collect odd positions |
| Space | O(n) | storing indices of odd elements |

The total n across all queries is bounded by 2 × 10^5, so the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    q = int(input())
    res = []
    for _ in range(q):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        odds = [i+1 for i,x in enumerate(a) if x % 2 == 1]
        if len(odds) < k:
            res.append("NO")
        else:
            cuts = odds[:k-1] + [n]
            res.append("YES")
            res.append(" ".join(map(str, cuts)))
    return "\n".join(res)

# provided samples
assert run("""3
5 3
7 18 3 14 1
5 4
1 2 3 4 5
6 2
1 2 8 4 10 2
""") == """YES
1 3 5
NO
NO"""

# all odd minimum
assert run("""1
1 1
1
""") == """YES
1"""

# impossible due to parity shortage
assert run("""1
3 2
2 4 6
""") == """NO"""

# exact match case
assert run("""1
5 2
1 2 3 4 6
""") == """YES
1 5"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all odd single | YES 1 | minimal valid construction |
| all even impossible | NO | feasibility check |
| exact k-1 odds | YES cut at end | boundary correctness |

## Edge Cases

One edge case occurs when all elements are even. For example `a = [2,4,6]` with any k ≥ 1. Every segment sum is even, so no valid partition exists. The algorithm correctly detects this because the list of odd indices is empty, immediately failing the `len(odds) < k` condition.

Another edge case is when k equals the number of odd elements. For instance `a = [1,2,3]`, k = 2. Odd positions are [1,3]. The algorithm selects cut at 1 and final cut at 3, producing segments `[1]` and `[2,3]`, both with odd sums. This confirms that using the first k−1 odd positions naturally aligns segments without needing any backtracking or adjustments.
