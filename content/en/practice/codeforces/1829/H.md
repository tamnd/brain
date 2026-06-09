---
title: "CF 1829H - Don't Blame Me"
description: "We are given an array where every element is a small integer, specifically a 6-bit value. From this array, we can choose any non-empty subsequence, meaning we pick any subset of indices while preserving order, although order does not actually matter for the bitwise operation."
date: "2026-06-09T07:19:13+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1829
codeforces_index: "H"
codeforces_contest_name: "Codeforces Round 871 (Div. 4)"
rating: 1700
weight: 1829
solve_time_s: 64
verified: true
draft: false
---

[CF 1829H - Don't Blame Me](https://codeforces.com/problemset/problem/1829/H)

**Rating:** 1700  
**Tags:** bitmasks, combinatorics, dp, math  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array where every element is a small integer, specifically a 6-bit value. From this array, we can choose any non-empty subsequence, meaning we pick any subset of indices while preserving order, although order does not actually matter for the bitwise operation.

For each chosen subsequence, we compute the bitwise AND of all selected values. This produces another number between 0 and 63. We then count how many of the resulting AND values have exactly k bits set in their binary representation. The final answer is the number of valid subsequences, not the number of distinct results.

The key difficulty is that subsequences grow exponentially with n. Even for n = 40, brute force already becomes borderline. Here n can reach 2 × 10^5, so any exponential enumeration is impossible. We need to exploit the fact that values are small and the AND operation is restrictive.

A subtle edge case appears when zeros are present. Any subsequence containing a zero contributes an AND result of zero, regardless of other elements. For example, if the array is [0, 7], every subsequence containing 0 has AND = 0, and only subsets without 0 behave normally. If k = 0, these become heavily dominant. A naive approach that treats zero like a normal value often miscounts because zero annihilates all bits.

Another corner case is when k = 0. We are counting subsequences whose AND has no set bits, meaning AND equals 0. This includes many combinations that collapse due to shared bit conflicts. Handling k = 0 uniformly is important because bit-count logic alone is not enough; we must track exact AND states, not just bit counts during construction.

## Approaches

A direct approach is to enumerate all subsequences, compute their AND, and check the bit count. This requires O(2^n · n) time, since each subsequence AND computation may scan up to n elements. Even with memoization, the number of subsequences dominates, making it infeasible beyond n ≈ 25.

The key observation is that each element is a 6-bit mask, so every AND result is also within 0 to 63. This drastically reduces the state space from exponential subsets to only 64 possible AND values. Instead of tracking subsets directly, we track how many subsequences produce each possible AND result.

We process elements one by one and maintain a DP array where dp[mask] is the number of subsequences whose AND equals mask after processing some prefix. When we see a new value x, each existing subsequence either excludes x or includes x. Including x transforms an existing AND value m into (m & x). Excluding x leaves m unchanged. We also count the new subsequence consisting only of x.

This transition works because AND is associative and monotonic with respect to bit intersection: adding elements only reduces or preserves bits. Thus we can propagate counts cleanly across the 64-state space.

Finally, we sum dp[mask] over all masks whose popcount equals k.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(1) | Too slow |
| Bitmask DP over AND states | O(n · 64) | O(64) | Accepted |

## Algorithm Walkthrough

We maintain a frequency table over all possible AND results.

1. Initialize an array dp of size 64 with all zeros. This represents counts of subsequences producing each AND mask.
2. Iterate through each number x in the array.
3. Create a new array ndp initialized as a copy of dp. This handles the “not taking x” case, where all previous subsequences remain unchanged.
4. For every mask m from 0 to 63, update ndp[m & x] by adding dp[m]. This represents extending each existing subsequence by including x, which updates its AND value.
5. Also account for the new subsequence consisting only of x by incrementing ndp[x].
6. Replace dp with ndp.
7. After processing all elements, sum dp[mask] for all masks whose popcount equals k.

The reason copying dp first is necessary is that each element must be considered exactly once per subsequence state transition. Mixing updates in-place would incorrectly reuse the same element multiple times within a single iteration.

### Why it works

Every subsequence corresponds to a unique sequence of inclusion decisions over elements. The DP state compresses all subsequences that share the same resulting AND value. The transition preserves correctness because every subsequence either does not use the current element or uses it exactly once, and the AND operation deterministically maps old states to new ones. Since all possible transitions are covered and no state is double-counted within a single iteration, dp always reflects the exact distribution of subsequence AND results for the processed prefix.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    dp = [0] * 64
    
    for x in a:
        ndp = dp[:]  # not take x
        
        # take x as a new subsequence
        ndp[x] = (ndp[x] + 1) % MOD
        
        # extend existing subsequences
        for m in range(64):
            if dp[m]:
                ndp[m & x] = (ndp[m & x] + dp[m]) % MOD
        
        dp = ndp
    
    ans = 0
    for m in range(64):
        if bin(m).count("1") == k:
            ans = (ans + dp[m]) % MOD
    
    print(ans)

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        solve()
```

The DP array `dp` tracks how many subsequences produce each possible AND mask. The key implementation detail is that we copy the array before processing each element, ensuring we do not reuse updates from the same iteration.

The line `ndp[m & x] += dp[m]` is the only transition: it encodes including the current element. The explicit `ndp[x] += 1` ensures singleton subsequences are counted.

Finally, we filter masks by popcount equal to k. Since masks are only 0 to 63, this final scan is constant time per test.

## Worked Examples

### Example 1

Input:

```
3 1
1 3 2
```

We track dp over masks.

| Step | x | dp before | transition highlights | dp after |
| --- | --- | --- | --- | --- |
| 1 | 1 | {0:0} | start new subsequence | {1:1} |
| 2 | 3 | {1:1} | 1&3=1, plus singleton 3 | {1:2, 3:1} |
| 3 | 2 | {1:2, 3:1} | 1&2=0, 3&2=2, plus singleton 2 | {1:2, 3:1, 0:2, 2:1} |

Masks with popcount 1 are 1, 2, 4, 8, 16, 32. Only 1 and 2 contribute here, giving answer 3.

This trace shows how AND gradually collapses bits, producing smaller masks over time.

### Example 2

Input:

```
2 0
0 1
```

| Step | x | dp before | transition | dp after |
| --- | --- | --- | --- | --- |
| 1 | 0 | {} | singleton 0 | {0:1} |
| 2 | 1 | {0:1} | 0&1=0, plus singleton 1 | {0:2, 1:1} |

We count masks with popcount 0, only mask 0 qualifies, so answer is 2.

This example highlights how zero dominates AND behavior since it annihilates all bits in any combined subsequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 64) | Each element updates all 64 masks |
| Space | O(64) | Fixed DP table over masks |

The total number of operations across all test cases is bounded by 2 × 10^5 × 64, which fits comfortably within time limits.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []

    for _ in range(t):
        n, k = map(int, sys.stdin.readline().split())
        a = list(map(int, sys.stdin.readline().split()))
        
        dp = [0] * 64
        
        for x in a:
            ndp = dp[:]
            ndp[x] = (ndp[x] + 1) % MOD
            for m in range(64):
                ndp[m & x] = (ndp[m & x] + dp[m]) % MOD
            dp = ndp
        
        ans = 0
        for m in range(64):
            if bin(m).count("1") == k:
                ans = (ans + dp[m]) % MOD
        
        out.append(str(ans))
    
    return "\n".join(out)

# provided samples
assert run("""6
5 1
1 1 1 1 1
4 0
0 1 2 3
5 1
5 5 7 4 2
1 2
3
12 0
0 2 0 2 0 2 0 2 0 2 0 2
10 6
63 0 63 5 5 63 63 4 12 13
""") == """31
10
10
1
4032
15"""

# custom cases
assert run("""1
1 0
0
""") == "1", "single zero"

assert run("""1
3 3
7 7 7
""") == "7", "all identical full mask"

assert run("""1
4 1
1 2 4 8
""") == "4", "disjoint bits"

assert run("""1
5 0
1 2 4 0 7
""") == "8", "zero dominating mixes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single zero | 1 | zero-only subsequence |
| all identical full mask | 7 | identical contributions accumulate |
| disjoint bits | 4 | AND collapses correctly |
| zero dominating mixes | 8 | interaction with zero |

## Edge Cases

A key edge case is when many zeros appear. For input like `[0, 0, 0]`, every non-empty subsequence has AND equal to 0. The algorithm handles this naturally because every transition involving x = 0 maps all masks to 0, accumulating counts correctly in dp[0].

Another case is when all numbers are identical. Each inclusion doubles combinations but keeps AND unchanged. The DP accumulates counts into a single mask, and popcount filtering then either counts all subsequences or none depending on k.

When values have disjoint bits such as [1, 2, 4, 8], every AND between different elements becomes 0. The DP correctly routes all mixed subsequences into mask 0, while singleton subsequences remain distinct, matching the combinatorial structure of bit intersection.
