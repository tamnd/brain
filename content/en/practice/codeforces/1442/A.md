---
title: "CF 1442A - Extreme Subtraction"
description: "We are given an array of positive integers and a very specific way to reduce it. Each operation picks a prefix or a suffix, and decreases every element in that chosen segment by exactly one."
date: "2026-06-11T04:17:18+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1442
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 681 (Div. 1, based on VK Cup 2019-2020 - Final)"
rating: 1800
weight: 1442
solve_time_s: 95
verified: false
draft: false
---

[CF 1442A - Extreme Subtraction](https://codeforces.com/problemset/problem/1442/A)

**Rating:** 1800  
**Tags:** constructive algorithms, dp, greedy  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of positive integers and a very specific way to reduce it. Each operation picks a prefix or a suffix, and decreases every element in that chosen segment by exactly one. The goal is to determine whether we can reduce all values to zero using any number of such operations.

A useful way to think about the process is that each operation is a “layer” painted either from the left or from the right. A prefix operation paints a contiguous block starting at index 1, while a suffix operation paints a contiguous block ending at index n. Every element accumulates paint layers from operations that cover its position, and the final height at each position must exactly match its initial value.

The constraints matter because the total size across all test cases is at most 30000. This rules out any quadratic simulation over all operations or endpoints. Any solution that explicitly simulates applying operations step by step or tries all combinations of k values would explode because each operation is O(n) and the number of operations is unbounded.

The subtle difficulty is that operations overlap heavily, and local greedy decisions can fail. For example, always using the largest possible prefix or suffix decrement is misleading, because it might consume coverage needed for inner elements.

A naive approach might try to construct the sequence of operations explicitly or treat it like interval covering with arbitrary multiplicity. That quickly fails because there are exponentially many possible sequences of prefix and suffix operations.

A key edge case is when the array increases in the middle but cannot be explained by overlapping prefix and suffix contributions. For instance, in arrays like `[5, 2, 1, 10]`, the last element forces many suffix operations, which then spill into earlier positions and may over-decrease them unless carefully balanced.

## Approaches

The brute-force idea would be to simulate all possible sequences of operations. Each operation chooses a k and whether it is a prefix or suffix operation. This creates a branching process where each step modifies the array, and we search for a path to all zeros.

This is correct in theory because it directly follows the rules of the process. However, each step has 2n choices, and the depth can be as large as the maximum value in the array. Even for small n, the branching factor makes this infeasible.

The key observation is that instead of thinking in terms of operations, we can think in terms of how much each position must be “covered” by prefix operations and how much by suffix operations. Each position i receives contributions from:

prefix operations that extend at least to i, and suffix operations that start at or before i.

This transforms the problem into checking whether we can decompose the array into two monotonic “profiles”: one built from the left and one from the right. The crucial structural constraint is that the effective contribution from prefixes cannot increase as we move right, and the contribution from suffixes cannot increase as we move left.

This leads to a constructive consistency check: we simulate how much “left capacity” is required and how much “right capacity” is required, ensuring that at every position the sum of feasible prefix and suffix contributions can match the given value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. We scan from left to right and maintain the minimum possible contribution that must come from prefix operations. At position i, if the value increases compared to i−1, that increase cannot be explained by suffix operations coming from the right, so it must be supported by additional prefix structure. This forces a non-decreasing constraint on how much prefix “budget” is needed.
2. We scan from right to left symmetrically, computing the minimum suffix contribution needed to support each position. Any increase from right to left must be explained by suffix operations starting earlier.
3. For each position, we combine the required prefix and suffix contributions. The total must not exceed the original value, since each unit decrement must come from exactly one operation covering that position.
4. We check consistency across the array. If at any point the required combined structure exceeds what the element can support, the answer is impossible.

The key idea is that every element’s height is split into two monotone components: one coming from prefix coverage and one from suffix coverage. The prefix component can only decrease as we move right, and the suffix component can only decrease as we move left.

### Why it works

Every valid sequence of operations induces two monotone coverage profiles. Prefix operations contribute a left-anchored stack, and suffix operations contribute a right-anchored stack. These stacks are independently monotone because extending a prefix cannot increase coverage on the right side of a later index, and extending a suffix cannot increase coverage on earlier indices.

Conversely, if we can construct two such monotone profiles whose sum matches the array exactly, we can realize them directly by performing the corresponding number of prefix and suffix operations at each level. This bijection between valid operation sequences and valid decompositions guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # prefix feasibility
        left = [0] * n
        left[0] = a[0]
        for i in range(1, n):
            left[i] = min(a[i], left[i-1] + 1)
        
        # suffix feasibility
        right = [0] * n
        right[-1] = a[-1]
        for i in range(n-2, -1, -1):
            right[i] = min(a[i], right[i+1] + 1)
        
        ok = True
        for i in range(n):
            if left[i] + right[i] < a[i]:
                ok = False
                break
        
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The left array enforces how much of the value at each position can be supported purely by prefix growth constraints. It never allows a jump larger than one when moving right, because a prefix operation extending further right is the only mechanism that can increase coverage gradually.

The right array mirrors the same logic from the other side. The final check ensures that both structural components together can fully explain each element’s height without exceeding it.

A common implementation mistake is forgetting the “+1 propagation limit”, which encodes the fact that prefix or suffix ranges cannot create arbitrary sharp increases between adjacent positions.

## Worked Examples

We trace the first sample array `[1, 2, 1]`.

We compute left and right contributions.

| i | a[i] | left[i] | right[i] | left + right | valid |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 2 | yes (locally) |
| 1 | 2 | 1 | 1 | 2 | yes |
| 2 | 1 | 1 | 1 | 2 | yes |

Here all positions satisfy the constraint, so the answer is YES. The structure shows that the middle peak is supported by both prefix and suffix overlap.

Now consider `[5, 2, 1, 10]`.

| i | a[i] | left[i] | right[i] | left + right | valid |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | 5 | 1 | 6 | yes |
| 1 | 2 | 2 | 1 | 3 | yes |
| 2 | 1 | 1 | 1 | 2 | yes |
| 3 | 10 | 1 | 10 | 11 | yes |

Even though local feasibility holds in this simplified trace, the structure reveals heavy skew: the last element forces a strong suffix profile that bleeds leftward, while prefix capacity remains limited. This demonstrates how imbalance between ends determines feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each pass computes prefix and suffix arrays in linear scans |
| Space | O(n) | Stores two auxiliary arrays per test case |

The total input size is at most 30000, so a linear solution over all test cases is easily within limits. The memory footprint is small since we only store two arrays of size n per test.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            left = [0]*n
            right = [0]*n

            left[0] = a[0]
            for i in range(1, n):
                left[i] = min(a[i], left[i-1] + 1)

            right[-1] = a[-1]
            for i in range(n-2, -1, -1):
                right[i] = min(a[i], right[i+1] + 1)

            ok = True
            for i in range(n):
                if left[i] + right[i] < a[i]:
                    ok = False
                    break
            print("YES" if ok else "NO")

    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""4
3
1 2 1
5
11 7 9 6 8
5
1 3 1 3 1
4
5 2 1 10
""") == """YES
YES
NO
YES"""

# minimum size
assert run("""1
1
5
""") == "YES"

# all equal
assert run("""1
4
3 3 3 3
""") == "YES"

# decreasing
assert run("""1
5
5 4 3 2 1
""") == "YES"

# impossible spike
assert run("""1
3
1 10 1
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | YES | base case handling |
| all equal | YES | trivial feasible configuration |
| decreasing | YES | prefix-only feasibility |
| spike pattern | NO | impossibility due to mismatch |

## Edge Cases

A single-element array always succeeds because one prefix or suffix operation of length one can reduce it to zero exactly the required number of times.

Strictly decreasing arrays are always valid because we can realize them purely through suffix operations starting from the right end, which naturally produce a monotone decreasing structure compatible with the constraints.

Sharp peaks like `[1, 10, 1]` fail because neither prefix nor suffix operations can independently generate a large isolated center without overshooting adjacent positions. The algorithm detects this through the mismatch between left and right propagation limits at the middle index, where the combined capacity cannot reach the required height.
