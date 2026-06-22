---
title: "CF 105582G - Glasses of Solutions"
description: "We are given several containers, each containing a liquid solution. For each container we know two values: the total mass of the solution and how much of that mass is salt."
date: "2026-06-22T17:51:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105582
codeforces_index: "G"
codeforces_contest_name: "Ural Championship 2017"
rating: 0
weight: 105582
solve_time_s: 65
verified: true
draft: false
---

[CF 105582G - Glasses of Solutions](https://codeforces.com/problemset/problem/105582/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several containers, each containing a liquid solution. For each container we know two values: the total mass of the solution and how much of that mass is salt. We want to select a non-empty subset of these containers, pour everything together, and check whether the resulting mixture has a very specific salt concentration.

For any chosen subset, the final concentration is determined by the ratio of total salt mass to total mass. The task is to count how many subsets produce exactly the required fraction a/b after mixing.

The key difficulty is that the condition is not additive in a simple way. We are not just summing values and comparing to a threshold, we must enforce an exact rational equality across subsets.

The constraint n ≤ 35 is the main structural hint. A direct enumeration over all subsets is possible in O(2^n), but 2^35 is too large. This immediately suggests splitting the array and combining partial results.

A subtle edge case comes from empty contributions on one side of the split. For example, if the only valid subset is formed entirely in the right half, or entirely in the left half, or partially from both, we must ensure we do not accidentally count the empty subset, since the problem requires a non-empty selection overall.

Another corner case appears when a = 0. Then the target fraction is zero, meaning the final mixture must contain zero salt. This forces every selected combination to have total salt sum equal to zero, even though total mass may be positive. Any naive floating-point comparison would fail here because all computations must remain exact and integer-based.

## Approaches

A brute-force solution checks every subset of the n glasses, computes total salt and total mass, and verifies whether b * total_salt equals a * total_mass. This is correct and conceptually simple. However, it examines 2^n subsets, which in the worst case is about 3 × 10^10 operations when n = 35, far beyond any practical limit.

The structure of the condition is linear in the sums of selected elements. If we expand a subset into two parts, left and right, the constraint becomes a single linear equation over the combined contributions. This makes meet-in-the-middle applicable.

We split the array into two halves of size at most about 17 or 18. We enumerate all subsets in each half, computing for each subset the pair (sum_mass, sum_salt). Instead of trying to match pairs directly in two dimensions, we transform the condition:

b * (mL + mR) = a * (tL + tR)

Rewriting gives:

(b * mL - a * tL) + (b * mR - a * tR) = 0

This means each subset can be assigned a single scalar value f = b * m - a * t, and valid full subsets correspond exactly to pairs of left and right subsets whose f-values sum to zero.

So we store frequencies of f-values for the right half and match them against negatives from the left half.

We must also remove the empty-empty combination since it is not a valid non-empty subset.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(1) | Too slow |
| Meet in the Middle | O(2^(n/2)) | O(2^(n/2)) | Accepted |

## Algorithm Walkthrough

We process the array by splitting it into two halves.

1. Split the n glasses into two groups of sizes n1 and n2. This reduces the exponential search space into two manageable parts. Each half will be enumerated independently.
2. For every subset of the left half, compute total mass and total salt, then compute the value fL = b * saltL - a * massL. Store all such values in a list. This converts a two-dimensional constraint into a single scalar representation.
3. Repeat the same process for the right half, producing values fR for every subset. Instead of storing a list only, build a frequency map from fR to its occurrence count. This allows fast lookup when matching complementary values.
4. The full subset condition requires fL + fR = 0. For each value in the left list, we add the number of right subsets with value -fL. This aggregates all valid combinations without explicitly constructing full subsets.
5. Subtract one if necessary to exclude the case where both chosen subsets are empty, since the problem requires a non-empty selection overall. The empty subset corresponds to f = 0 in both halves.

The correctness relies on the fact that every subset of the full set corresponds uniquely to a pair of subsets from the two halves, and the transformation preserves the original equality condition exactly.

### Why it works

The expression b * sum(salt) - a * sum(mass) is linear over disjoint unions of subsets. This means the value for a combined subset is exactly the sum of values from its left and right parts. Therefore, the original ratio condition is equivalent to requiring the combined transformed value to be zero. Because every subset decomposition is unique across the split, counting matching complements counts each valid subset exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

def solve():
    n, a, b = map(int, input().split())
    arr = [tuple(map(int, input().split())) for _ in range(n)]
    
    left = arr[:n//2]
    right = arr[n//2:]
    
    def gen(sub):
        res = []
        m = len(sub)
        for mask in range(1 << m):
            sm = 0
            st = 0
            for i in range(m):
                if mask & (1 << i):
                    st += sub[i][0]
                    sm += sub[i][1]
            res.append(b * st - a * sm)
        return res
    
    L = gen(left)
    R = gen(right)
    
    freqR = defaultdict(int)
    for x in R:
        freqR[x] += 1
    
    ans = 0
    for x in L:
        ans += freqR.get(-x, 0)
    
    # exclude empty-empty subset
    # empty subset has value 0 in both halves
    ans -= 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first splits the array to enable enumeration of all subsets within each half. The helper function generates the transformed value f = b * salt - a * mass for every subset. This avoids storing raw pairs and simplifies matching.

A frequency map is built for the right half so that complement lookups are O(1). The final loop accumulates matches from the left half. The subtraction at the end removes the invalid case where both halves choose empty subsets simultaneously.

Care must be taken that all arithmetic stays in integers. Using floating-point division would introduce precision errors and break equality checks.

## Worked Examples

### Example 1

Input:

```
5 1 2
1 2
1 2
1 2
1 2
1 4
```

We split into two halves: left has 2 elements, right has 3 elements.

For each subset, we compute f = 2_salt - 1_mass.

Left subsets:

| subset | salt | mass | f |
| --- | --- | --- | --- |
| ∅ | 0 | 0 | 0 |
| {1} | 1 | 2 | 0 |
| {2} | 1 | 2 | 0 |
| {1,2} | 2 | 4 | 0 |

Right subsets produce values that also frequently evaluate to 0 because all ratios match 1/2.

Matching left and right requires fL + fR = 0, which is always satisfied here, so every combination works except empty-empty.

This demonstrates the degenerate case where all elements already satisfy the target ratio individually, so every subset is valid.

### Example 2

Input:

```
2 0 1
0 1
1 1
```

We require zero salt in total since a = 0.

Left/right split gives single elements.

For each subset, f = 1 * salt - 0 * mass = salt.

| subset | salt | f |
| --- | --- | --- |
| ∅ | 0 | 0 |
| {0,1} | 0 | 0 |
| {1,1} | 1 | 1 |

Only subsets with total salt zero are valid. The algorithm counts only combinations where both halves contribute zero salt.

This confirms the handling of the a = 0 boundary case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^(n/2)) | Each half enumerates all subsets and we combine via hash lookup |
| Space | O(2^(n/2)) | Frequency map stores transformed subset values |

The split ensures at most about 2^17 subsets per half, which is around 130,000 states, easily fitting within the time limit. Memory usage remains similarly bounded.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    n, a, b = map(int, input().split())
    arr = [tuple(map(int, input().split())) for _ in range(n)]
    
    left = arr[:n//2]
    right = arr[n//2:]
    
    def gen(sub):
        res = []
        m = len(sub)
        for mask in range(1 << m):
            sm = 0
            st = 0
            for i in range(m):
                if mask & (1 << i):
                    st += sub[i][0]
                    sm += sub[i][1]
            res.append(b * st - a * sm)
        return res
    
    L = gen(left)
    R = gen(right)
    
    freqR = defaultdict(int)
    for x in R:
        freqR[x] += 1
    
    ans = 0
    for x in L:
        ans += freqR.get(-x, 0)
    
    ans -= 1
    return str(ans)

# provided sample 1
assert run("""5 1 2
1 2
1 2
1 2
1 2
1 4
""") == "15"

# provided sample 2
assert run("""2 0 1
0 1
1 1
""") == "1"

# custom: single valid only
assert run("""1 1 2
1 2
""") == "1"

# custom: impossible
assert run("""3 1 2
1 1
2 1
3 1
""") == "0"

# custom: all zeros
assert run("""3 0 1
0 1
0 1
0 1
""") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all valid ratios | many subsets | full combinatorial matching |
| a = 0 case | restricted subsets | zero-salt constraint |
| single element | 1 | base correctness |
| impossible case | 0 | no accidental matches |
| all-zero salts | all subsets | degenerate equality |

## Edge Cases

When a = 0, every subset must satisfy that total salt is zero. In the algorithm this becomes f = b * salt, so only subsets with salt sum zero contribute f = 0. The matching logic still works because it reduces to counting zero-valued subset pairs, which correctly filters invalid combinations.

When all glasses individually already satisfy the target ratio, every subset produces f = 0. The algorithm counts all pairs across halves, then subtracts the empty-empty case. This matches the fact that every non-empty subset is valid.

When no subset satisfies the equation, both L and R contain values but no complementary pairs exist, so the frequency lookup always returns zero and the answer remains correct.
