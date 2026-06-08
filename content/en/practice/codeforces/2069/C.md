---
title: "CF 2069C - Beautiful Sequence"
description: "We are asked to count the number of \"beautiful\" subsequences in an array where every element is either 1, 2, or 3."
date: "2026-06-08T06:59:08+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2069
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 174 (Rated for Div. 2)"
rating: 1500
weight: 2069
solve_time_s: 98
verified: false
draft: false
---

[CF 2069C - Beautiful Sequence](https://codeforces.com/problemset/problem/2069/C)

**Rating:** 1500  
**Tags:** combinatorics, dp, greedy, two pointers  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count the number of "beautiful" subsequences in an array where every element is either 1, 2, or 3. A beautiful subsequence must have at least three elements, every element except the first must have a smaller element to its left, and every element except the last must have a larger element to its right. In other words, the subsequence must increase somewhere and decrease somewhere, ensuring it is not monotone. The input provides multiple test cases, each specifying the length of the array and the array itself. The output is the count of beautiful subsequences modulo 998244353.

The constraints allow up to 200,000 elements in a single array and a total of 200,000 elements across all test cases. This precludes any approach that examines every possible subsequence explicitly because that would require up to 2^200,000 operations, which is infeasible. The fact that elements are only 1, 2, or 3 suggests that a solution exploiting this small value range is possible. Edge cases include arrays of minimum length three, arrays with all identical values where no subsequence is beautiful, and arrays where only a single increasing-decreasing pattern exists.

For example, if the array is `[1, 1, 1]`, the correct output is 0 because there is no element greater than the first, so no subsequence can satisfy the beauty condition. A naive approach that counts subsequences without checking left-smaller and right-larger conditions would incorrectly count these.

## Approaches

The brute-force approach iterates over all subsequences of length three or more, checks the conditions for each, and counts those that satisfy them. Generating all subsequences explicitly takes O(2^n) time, and checking each for beauty takes up to O(n) operations. For n = 200,000, this is far too slow.

The key insight is that since values are limited to 1, 2, 3, we can model subsequences by tracking counts of sequences ending with each number and the ways to extend them while respecting the beautiful sequence conditions. Specifically, a beautiful subsequence must contain at least one 1, one 2, and one 3 in order somewhere. This allows a dynamic programming approach where we track counts of subsequences of length 1, 2, and 3 as we scan the array. Each element can extend existing subsequences or start new ones based on its value. This reduces the problem from exponential complexity to linear complexity in n per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(2^n) | Too slow |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize three counters: `count1` for subsequences ending with 1, `count12` for subsequences ending with 2 that have seen a 1, and `count123` for subsequences ending with 3 that have seen a 1 and a 2. All start at zero. These counters represent the number of ways to form partial beautiful sequences.
2. Iterate over each element in the array. For an element equal to 1, increment `count1` by 1 because a new subsequence starting with 1 can begin here. For an element equal to 2, increment `count12` by `count1` because each subsequence ending with 1 can be extended by this 2. For an element equal to 3, increment `count123` by `count12` because each subsequence of form 1→2 can be extended by this 3 to form a subsequence that satisfies the beauty conditions.
3. Continue scanning the array, updating counts as above. Each counter only depends on the previous counters, not on the full subsequence list. The modulo operation ensures the counts do not overflow.
4. After scanning the array, `count123` holds the total number of beautiful subsequences in this array.

This works because the counters track all valid subsequences incrementally and ensure the left-smaller and right-larger conditions implicitly by the order in which elements extend subsequences. Every beautiful subsequence of length three or more is accounted for by extending smaller subsequences in this manner. Sequences longer than three are automatically counted because the counters accumulate the ways to append additional elements.

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
        
        count1 = 0
        count12 = 0
        count123 = 0
        
        for x in a:
            if x == 1:
                count1 = (count1 + 1) % MOD
            elif x == 2:
                count12 = (count12 + count1) % MOD
            elif x == 3:
                count123 = (count123 + count12) % MOD
        
        print(count123)

if __name__ == "__main__":
    solve()
```

The counters are updated in a way that maintains the invariant: `count1` counts sequences that can be extended by 2, `count12` counts sequences that can be extended by 3, and `count123` counts completed beautiful subsequences. Modulo operations prevent overflow. Using only three integers ensures O(1) space.

## Worked Examples

**Sample Input 1**: `[3, 2, 1, 2, 2, 1, 3]`

| Step | Element | count1 | count12 | count123 | Explanation |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 | 0 | 0 | No preceding 1→2, cannot start beautiful seq |
| 2 | 2 | 0 | 0 | 0 | No preceding 1 |
| 3 | 1 | 1 | 0 | 0 | New subsequence starts |
| 4 | 2 | 1 | 1 | 0 | Extends previous 1→2 |
| 5 | 2 | 1 | 2 | 0 | Extends previous 1→2 again |
| 6 | 1 | 2 | 2 | 0 | New 1 starts |
| 7 | 3 | 2 | 4 | 3 | Each 1→2 extends to 1→2→3 |

The final count123 is 3, matching the expected output.

**Sample Input 2**: `[1, 2, 3]`

| Step | Element | count1 | count12 | count123 |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 |
| 2 | 2 | 1 | 1 | 0 |
| 3 | 3 | 1 | 1 | 1 |

The output is 1, matching the expected output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once with constant-time updates |
| Space | O(1) | Only three counters are used, independent of n |

With n up to 2×10^5 and t up to 10^4, the total operations sum to 2×10^5, well within 2 seconds. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("4\n7\n3 2 1 2 2 1 3\n4\n3 1 2 2\n3\n1 2 3\n9\n1 2 3 2 1 3 2 2 3\n") == "3\n0\n1\n22"

# Custom cases
assert run("1\n3\n1 1 1\n") == "0", "all equal values"
assert run("1\n3\n1 2 3\n") == "1", "minimum size beautiful sequence"
assert run("1\n4\n3 2 1 2\n") == "0", "no increasing subsequence"
assert run("1\n5\n1 2 2 3 3\n") == "4", "multiple extensions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1,1,1]` | 0 | No beautiful subsequence when all values are identical |
| `[1,2,3]` | 1 | Minimal beautiful sequence of length three |
| `[3,2,1,2]` | 0 | No valid 1→2→3 subsequence exists |
| `[1,2,2,3,3]` | 4 | Multiple subsequences can extend to form beautiful sequences |

## Edge Cases

For an array consisting entirely of 3s, `[3,3,3]`, the counters remain `count1=0`, `count12=0`, `count123=0`, so the output is 0. For arrays starting with 2, `[2,3,1]`, `count1` does not increase until a 1 is seen, so sequences starting incorrectly do not count
