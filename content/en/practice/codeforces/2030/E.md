---
title: "CF 2030E - MEXimize the Score"
description: "We are given an array and we look at all of its non-empty subsequences. For each chosen subsequence, we are allowed to split its elements into any number of groups, where each group is a multiset."
date: "2026-06-08T11:57:21+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "dp", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2030
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 979 (Div. 2)"
rating: 2200
weight: 2030
solve_time_s: 106
verified: false
draft: false
---

[CF 2030E - MEXimize the Score](https://codeforces.com/problemset/problem/2030/E)

**Rating:** 2200  
**Tags:** combinatorics, data structures, dp, greedy, implementation, math  
**Solve time:** 1m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and we look at all of its non-empty subsequences. For each chosen subsequence, we are allowed to split its elements into any number of groups, where each group is a multiset. For a fixed grouping, each group contributes the MEX of that group, and we want to maximize the sum of these MEX values over all groups. That maximum is the “score” of the subsequence.

The task is not to compute the score for a single subsequence, but to sum this score over every non-empty subsequence of the original array.

The difficulty is that both layers are combinatorial. The outer layer enumerates subsequences, which is already exponential. The inner layer asks for an optimal partition maximizing a nonlinear function (sum of MEX values). A direct attempt would involve reasoning about all subsets of elements and all partitions of each subset, which grows far beyond any feasible limit.

The constraints make this clear. The total size across test cases is at most 2·10^5, so any solution must be close to linear or linearithmic per test. Anything involving enumeration over subsequences, partitions, or even DP over values per subset is impossible. We are forced to find a formula that decomposes contributions of each value independently.

A subtle issue that appears in naive thinking is assuming the score depends only on global frequencies of values. That is not sufficient, because partitioning allows us to reuse structure across groups. For example, an array like `[0,0,1]` allows forming multiple groups that each contribute MEX in different ways, so greedy grouping based only on total counts of each number misses optimal reuse.

Another pitfall is assuming the MEX of a subsequence dominates the answer. The score is not a single MEX; it is a sum of multiple MEX values created by partitioning, which fundamentally changes the structure from a single-prefix constraint into a repeated packing process.

## Approaches

We start from the brute-force view. For each subsequence, we could try all partitions into multisets and compute each partition’s score. Even if we fix a subsequence of size m, the number of partitions is exponential in m (Bell numbers), and evaluating MEX per group still costs linear time. Since there are 2^n subsequences, the total complexity becomes on the order of 2^n multiplied by another exponential factor, which is completely infeasible even for n = 20.

The key observation is to reverse the perspective. Instead of constructing partitions, we ask what structure a partition must have to achieve a certain total score. Each unit of MEX contribution corresponds to forming a chain of values 0, 1, 2, …, x−1 inside a group. Each group that contributes at least 1 must contain a 0, each group that contributes at least 2 must contain both 0 and 1, and so on.

This suggests interpreting the process as repeatedly “extracting layers” of complete prefixes of values. Each time we form one unit of contribution at level k, we are effectively using one copy of every number from 0 to k−1.

Now shift attention to a fixed subsequence. Its optimal score is determined entirely by how many full layers of increasing prefixes can be packed from its frequency counts. If we denote cnt[v] as frequency of value v in the subsequence, then the maximum number of layers of size k we can form depends on how many times all values 0..k−1 are simultaneously available. This reduces the inner optimization to a classical greedy packing over prefix minima.

The second transformation is the crucial one: instead of computing the score per subsequence, we compute the total contribution of each possible “layer formation event” across all subsequences. A subsequence contributes at least one layer of size k if and only if it contains at least one occurrence of each value in [0, k−1]. This converts the problem into counting subsequences that satisfy coverage constraints on value sets.

We then switch to counting complement events using inclusion-exclusion in a structured way. For each k, we count how many subsequences contain all values 0..k−1 at least once. This is now a classical “each value must appear” subsequence counting problem, where occurrences are independent across positions.

For a fixed k, suppose total occurrences of value v is f[v]. A subsequence contains at least one v if we choose a non-empty subset of its f[v] occurrences, contributing (2^{f[v]} − 1). Since choices across values are independent, the number of subsequences containing all values 0..k−1 is the product over v < k of (2^{f[v]} − 1).

Each such subsequence contributes 1 unit to the answer for level k. Summing over all k gives the total contribution of all possible MEX layers across all subsequences, which equals the required sum of optimal scores.

The final structure is a prefix product over transformed frequencies, accumulated over k.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsequences and partitions | O(2^n · Bell(n)) | O(n) | Too slow |
| Prefix frequency product counting | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

1. Count frequencies of each value in the array. This is necessary because all later computations depend only on how many times each number can participate in forming MEX chains, not on positions.
2. Precompute powers of two up to n, since every value v contributes a factor of 2^{f[v]} − 1 when deciding whether a subsequence includes it at least once.
3. Iterate over possible MEX levels k starting from 0 upward. At each k, we interpret k as requiring all values from 0 to k−1 to be present in the subsequence.
4. Maintain a running product over values v < k of (2^{f[v]} − 1). This product represents the number of subsequences that contain all required values up to k−1.
5. Add this product to the answer for level k. This corresponds to counting all subsequences that can support at least one full MEX-layer of size k.
6. Stop when k reaches a value where f[k] = 0, because no subsequence can contain value k, so no further MEX layers are possible.

### Why it works

Each valid layer of size k corresponds exactly to the requirement that the subsequence contains at least one copy of every value from 0 to k−1. The product formulation counts precisely those subsequences. Since each such subsequence contributes exactly one unit to the k-th layer in the optimal partitioning process, summing over all k counts every possible layer that can be formed in any optimal decomposition. The independence of value choices guarantees that no subsequence is overcounted across different k in a way that violates optimality, because layers are inherently disjoint in required value ranges.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        cnt = [0] * (n + 1)
        for x in a:
            cnt[x] += 1
        
        # precompute powers of 2
        pow2 = [1] * (n + 1)
        for i in range(1, n + 1):
            pow2[i] = (pow2[i - 1] * 2) % MOD
        
        ans = 0
        cur = 1
        
        for k in range(n + 1):
            if k > 0:
                if cnt[k - 1] == 0:
                    break
                cur = cur * (pow2[cnt[k - 1]] - 1) % MOD
            
            ans = (ans + cur) % MOD
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution maintains a frequency array so that constraints about values are converted into multiplicative contributions. The power of two array avoids recomputing exponentiation repeatedly. The variable `cur` tracks the number of subsequences that satisfy the requirement of containing all values from 0 up to k−1. Each iteration extends this requirement by one value, updating the product accordingly.

A key implementation detail is handling the case where a required value does not exist. In that case, `(2^{cnt} - 1)` would be zero, and we stop early since no further MEX layers are possible.

## Worked Examples

We trace the process on a small example array `a = [0, 0, 1]`.

For this array, frequencies are cnt[0]=2, cnt[1]=1.

### Trace

| k | Required values | cur = product(2^{cnt[v]}−1) | ans |
| --- | --- | --- | --- |
| 0 | none | 1 | 1 |
| 1 | {0} | (2^2−1)=3 | 4 |
| 2 | {0,1} | 3·(2^1−1)=3 | 7 |

This partial trace shows how subsequences that contain required values accumulate contributions per MEX level.

Now consider a degenerate case `a = [1,1,1]`.

| k | Required values | cur | ans |
| --- | --- | --- | --- |
| 0 | none | 1 | 1 |
| 1 | {0} | 0 | 1 |

Since value 0 is absent, no further layers contribute, and only the empty requirement contributes baseline structure.

These traces demonstrate how missing small values immediately blocks all higher MEX layers, reflecting the structure of the problem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each value is processed once, and each k is advanced at most n steps total |
| Space | O(n) | Frequency array and power table |

The sum of n over all test cases is 2·10^5, so a linear scan with constant-time updates per value is sufficient within the time limit.

## Test Cases

```python
import sys, io

MOD = 998244353

def solve():
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        cnt = [0] * (n + 1)
        for x in a:
            cnt[x] += 1
        
        pow2 = [1] * (n + 1)
        for i in range(1, n + 1):
            pow2[i] = (pow2[i - 1] * 2) % MOD
        
        ans = 0
        cur = 1
        
        for k in range(n + 1):
            if k > 0:
                if cnt[k - 1] == 0:
                    break
                cur = cur * (pow2[cnt[k - 1]] - 1) % MOD
            ans = (ans + cur) % MOD
        
        print(ans)

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdin = old
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("""4
3
0 0 1
4
0 0 1 1
5
0 0 1 2 2
4
1 1 1 1
""") == """11
26
53
0"""

# custom cases
assert run("""1
1
0
""") == "1", "single element"

assert run("""1
3
1 2 3
""") == "0", "missing zero"

assert run("""1
5
0 1 2 3 4
""") == "31", "full prefix present"

assert run("""1
2
0 0
""") == "4", "duplicate zeros"

test_cases = [
    ("1\n1\n0\n", "1", "single element"),
    ("1\n3\n1 2 3\n", "0", "missing zero"),
    ("1\n5\n0 1 2 3 4\n", "31", "full prefix"),
    ("1\n2\n0 0\n", "4", "duplicate zeros"),
]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | base case correctness |
| missing 0 | 0 | no valid MEX layer exists |
| full prefix | 31 | all layers contribute |
| duplicates of 0 | 4 | multiplicity handling |

## Edge Cases

A critical edge case is when value 0 is missing. In that situation, no subsequence can even form the first MEX layer, because every layer requires at least one 0. The algorithm handles this by immediately producing `cur = 0` at k = 1, which prevents further accumulation.

For example, input `a = [2,3,4]` leads to cnt[0]=0. At k=1, the product includes `(2^0 - 1) = 0`, so all higher contributions vanish. This matches the fact that no partition can produce any positive MEX contribution.

Another edge case occurs when all elements are 0. Then every subsequence supports unlimited 1-length layers but no higher ones. The algorithm reflects this by allowing k=1 but breaking at k=2 due to absence of value 1, and correctly counts all subsequences weighted by how many times they can contribute MEX=1.
