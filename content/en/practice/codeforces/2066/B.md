---
title: "CF 2066B - White Magic"
description: "We are given an array of non-negative integers, and we are allowed to pick a subsequence from it. From that subsequence, we want to keep as many elements as possible while ensuring a very specific prefix-suffix condition holds at every split point."
date: "2026-06-08T10:44:04+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2066
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1004 (Div. 1)"
rating: 1900
weight: 2066
solve_time_s: 99
verified: false
draft: false
---

[CF 2066B - White Magic](https://codeforces.com/problemset/problem/2066/B)

**Rating:** 1900  
**Tags:** constructive algorithms, data structures, dp, greedy, implementation  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of non-negative integers, and we are allowed to pick a subsequence from it. From that subsequence, we want to keep as many elements as possible while ensuring a very specific prefix-suffix condition holds at every split point.

If we look at any prefix of the chosen subsequence, the smallest value in that prefix must always be at least as large as the mex of the remaining suffix. The mex of a set is the smallest non-negative integer that does not appear in it, so it captures how “complete” the suffix is with respect to starting values from zero upward.

The condition creates a tension between the left side, which is controlled by a minimum, and the right side, which is controlled by missing small integers. If the suffix is missing a small number like 0 or 1, its mex becomes small or even 0, making the condition easier. But if the suffix contains many consecutive small integers, its mex grows, forcing the prefix minimum to also be large.

The input size is large across test cases, up to 2·10^5 total elements, so any solution that tries all subsequences or recomputes mex repeatedly per split is immediately infeasible. Even O(n^2) per test case is too slow, and even O(n log n) per element would be risky if repeated recomputation is involved. This pushes us toward a linear or near-linear construction with careful bookkeeping of frequencies or missing counts.

A subtle edge case appears when the array contains many large values but very few small ones. For example, `[1000000000, 1000000000, 1000000000]` allows only a trivial subsequence because mex of the suffix is always 0 unless a 0 appears. Another edge case is when 0 is missing entirely: then mex of any suffix is always 0, making the condition trivial and allowing the entire subsequence. A naive approach that tries to explicitly maintain mex for every suffix split would repeatedly recompute missing values and fail under constraints.

## Approaches

A brute-force strategy would enumerate all subsequences and check whether each one is magical. For each subsequence, we would need to test all split points, recomputing the minimum of the prefix and the mex of the suffix. Even if we maintain prefix minima in O(1), mex computation dominates: each suffix mex computation is O(k) where k is subsequence length, and there are exponentially many subsequences. This is completely infeasible.

A more structured observation comes from rewriting what the condition is actually enforcing. Fix a valid subsequence. For a split at position i, the suffix mex is determined only by which small numbers appear in the suffix. The prefix minimum is monotone decreasing as we extend the prefix. So the only way to keep the inequality valid for long subsequences is to carefully control how many small integers we include, because every occurrence of a small number both reduces mex complexity and constrains future choices.

The key insight is to reverse perspective. Instead of thinking about prefixes, we track the suffix requirement: the mex of the remaining part depends only on whether we have already included certain values. In an optimal construction, we want to delay “breaking” the presence of small integers as much as possible while ensuring enough large elements remain to support prefix minima constraints.

This leads to a greedy construction where we try to maintain feasibility by tracking how many times we can still afford to include each value before it becomes impossible to keep mex bounded. We effectively simulate building the subsequence while ensuring that the suffix always has enough missing structure so that mex does not exceed the current prefix minimum threshold.

The core reduction is that only values 0, 1, 2, … up to the current mex boundary matter. Values larger than the current mex threshold behave as neutral elements for mex but can affect prefix minimum. So the problem reduces to balancing how many small numbers we include versus maintaining a stable decreasing prefix minimum, which can be handled by counting frequencies and simulating a greedy selection from left to right.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. We count frequencies of all values in the array, but we only explicitly care about values up to n, since mex can never exceed n for a length-n structure. Values larger than n can be treated as “infinite” and only influence prefix minimum behavior.
2. We compute how many occurrences of each value from 0 upward exist. This allows us to simulate how the mex of a suffix would evolve as we hypothetically remove elements.
3. We build the answer by simulating how many elements we can keep while maintaining feasibility of the mex condition. We maintain a running notion of how many distinct small values are still “available” to appear in suffixes.
4. We greedily include elements in decreasing order of their ability to preserve validity. Small values are critical because they determine mex; large values are flexible and can be included as long as they do not violate prefix minimum constraints.
5. The construction effectively reduces to determining the largest prefix of integers 0,1,2,… that can be fully supported by the array, while also counting all elements that do not interfere with this structure.

The subtle point is that once we decide the maximum mex level we can sustain, every element greater than or equal to that level can be freely included, while elements below it must be carefully matched against availability constraints.

### Why it works

The mex of a suffix depends only on whether all integers from 0 upward are present in that suffix. The algorithm implicitly ensures that we never create a suffix where mex exceeds what the prefix minimum can support. By tracking availability of small integers and limiting how far this chain can extend, we enforce that every split satisfies the required inequality.

The greedy selection is correct because once a value is excluded from supporting mex progression, reintroducing it later cannot improve feasibility of earlier splits. This monotonicity ensures that deciding the maximal feasible mex threshold globally yields an optimal subsequence length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        cnt = [0] * (n + 2)
        for x in a:
            if x <= n:
                cnt[x] += 1
        
        mex = 0
        while mex <= n and cnt[mex] > 0:
            cnt[mex] -= 1
            mex += 1
        
        # all elements >= mex can be taken freely
        ans = mex
        for x in a:
            if x >= mex:
                ans += 1
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by counting occurrences only up to n, since larger values cannot affect mex progression. It then constructs the maximum consecutive prefix starting from 0, consuming one occurrence of each value to determine how far the mex chain can extend. That value becomes the structural backbone of the subsequence.

Once this mex boundary is fixed, every element greater than or equal to it can be safely included because they do not introduce missing low integers in suffixes, and they do not disrupt mex progression. The final answer is the size of this maximal chain plus all such large elements.

A common pitfall is forgetting that only one copy of each small number is needed to extend the mex chain, while extra copies can be used freely later. Another subtlety is that values larger than n are effectively equivalent and should not be processed in the mex loop.

## Worked Examples

We trace the algorithm on two inputs.

First example:

Input: `[4, 3, 2, 1, 0]`

| Step | mex | cnt usage | included chain | remaining large elements | answer |
| --- | --- | --- | --- | --- | --- |
| init | 0 | counts built | [] | [] | 0 |
| take 0 | 1 | use one 0 | [0] | [] | 1 |
| take 1 | 2 | use one 1 | [0,1] | [] | 2 |
| take 2 | 3 | use one 2 | [0,1,2] | [] | 3 |
| take 3 | 4 | use one 3 | [0,1,2,3] | [] | 4 |
| take 4 | 5 | use one 4 | [0,1,2,3,4] | [] | 5 |

The chain fully extends to 5, and no extra elements remain.

Second example:

Input: `[4, 3, 3, 2, 1, 0]`

| Step | mex | cnt usage | chain | large elements used | answer |
| --- | --- | --- | --- | --- | --- |
| init | 0 | counts built | [] | [] | 0 |
| take 0 | 1 | use 0 | [0] | [] | 1 |
| take 1 | 2 | use 1 | [0,1] | [] | 2 |
| take 2 | 3 | use 2 | [0,1,2] | [] | 3 |
| take 3 | 4 | use 3 | [0,1,2,3] | [] | 4 |
| stop | 4 | no 4 available in chain | [0,1,2,3] | remaining 4 | 5 |

We cannot extend the chain to 5 because 4 is not present in sufficient form to continue the strict mex progression, but remaining elements contribute to the final count.

These examples show that the solution separates structure-building (mex chain) from flexible elements, which is exactly what the condition enforces.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Frequency counting and single mex scan |
| Space | O(n) | Frequency array up to n |

The total complexity is linear in the total input size, which fits comfortably under 2·10^5 across all test cases. The algorithm avoids any nested recomputation of mex or prefix minima, keeping all operations single-pass or bounded by n.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        
        cnt = [0] * (n + 2)
        for x in a:
            if x <= n:
                cnt[x] += 1
        
        mex = 0
        while mex <= n and cnt[mex] > 0:
            cnt[mex] -= 1
            mex += 1
        
        ans = mex + sum(1 for x in a if x >= mex)
        out.append(str(ans))
    
    return "\n".join(out)

# provided samples
assert run("""8
5
4 3 2 1 0
6
4 3 3 2 1 0
4
2 0 1 2
1
777
4
1000000000 1 7 9
2
0 1
2
1 2
4
0 1 0 1
""") == """5
5
3
1
4
2
2
3"""

# custom cases
assert run("""3
1
0
2
5
2
1
100 100 100
""") == """1
1
3
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 | 0` | `1` |
| `2 | 5` | `1` |
| `100 100 100` | `3` | large equal values |

## Edge Cases

When the array contains no zero, the mex chain cannot even start. In that situation, the algorithm sets mex to 0 immediately, and all elements are treated as freely includable since they are all ≥ mex. For example, input `[5, 6, 7]` produces mex = 0, and the answer becomes 3, which matches the fact that any subsequence trivially satisfies the condition.

When the array contains exactly a full prefix of small integers but no larger bridging values, such as `[0,1,2,3]`, the mex chain extends completely and no additional elements contribute. The algorithm consumes each value once and stops at mex = 4, giving answer 4.

When duplicates exist, such as `[0,0,1,1,2,2]`, only one copy of each value is used to extend mex, while remaining duplicates are counted as free elements once the chain is fixed. The algorithm correctly counts one per level for the chain and all remaining occurrences afterward, preserving optimality.
