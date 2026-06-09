---
title: "CF 1890A - Doremy's Paint 3"
description: "We are given several test cases, each consisting of an array of positive integers. The task is not to construct a new array from scratch but to decide whether we can reorder the given elements so that every pair of adjacent elements in the resulting sequence has the same sum."
date: "2026-06-08T22:03:52+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1890
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 906 (Div. 2)"
rating: 800
weight: 1890
solve_time_s: 80
verified: true
draft: false
---

[CF 1890A - Doremy's Paint 3](https://codeforces.com/problemset/problem/1890/A)

**Rating:** 800  
**Tags:** constructive algorithms  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases, each consisting of an array of positive integers. The task is not to construct a new array from scratch but to decide whether we can reorder the given elements so that every pair of adjacent elements in the resulting sequence has the same sum. In other words, after rearrangement, the sum of the first and second element must equal the sum of the second and third, and this equality must continue all the way through the array.

The key constraint is that we are allowed to permute the array arbitrarily, so the structure is not fixed. We only care whether some ordering exists that satisfies the adjacency sum condition.

The input size is small, with at most 100 elements per test case and at most 100 test cases. This means any solution up to roughly quadratic per test case would already be fast enough, but we should still aim for a constant or linear check per case since the structure of the problem allows a direct characterization.

A naive approach would try all permutations of the array and check the condition. That is factorial in complexity and becomes impossible even for n equal to 10.

A more subtle incorrect approach would assume that sorting helps directly, for example checking whether a sorted array satisfies the condition. This fails because the condition depends on adjacency structure, not order magnitude.

A typical misleading scenario appears when values repeat. For example, an array like 1, 1, 4, 5 cannot be made valid even though it contains duplicates that might suggest flexibility. A greedy rearrangement attempt often fails because local fixes break global equality of adjacent sums.

The core difficulty is that the constraint couples every adjacent pair, so local consistency forces a very rigid global structure.

## Approaches

If we attempt brute force, we generate every permutation of the array and check whether all adjacent sums are equal. For each permutation we compute n minus one sums, so the total complexity becomes O(n! · n). Even with n equal to 10, this already exceeds feasible limits.

The key observation comes from writing down what the condition implies algebraically. Suppose a valid arrangement exists. Then for every index i, we must have b[i] + b[i+1] equal to the same constant k. Comparing consecutive equalities gives b[i] + b[i+1] = b[i+1] + b[i+2], which simplifies immediately to b[i] = b[i+2]. This means the sequence must alternate strictly between two values.

Once we reach this point, the entire structure collapses into a very simple pattern. Any valid array must look like x, y, x, y, x, y and so on, or the reverse starting point. Therefore, at most two distinct values can appear in the array. If more than two distinct values exist, no permutation can satisfy the condition.

When exactly two values exist, say x and y with frequencies c1 and c2, the only remaining question is whether we can place them in alternating positions. The positions split into two groups: indices 1, 3, 5, and so on, and indices 2, 4, 6, and so on. One of these groups must be entirely x and the other entirely y. This forces the multiset of counts to match the parity split of the array length.

For length n, one group has size ceil(n/2) and the other has size floor(n/2). So the frequencies must match these sizes exactly in some order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Frequency Analysis | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array for the test case and compute the frequency of each distinct value. This step reduces the problem from ordering elements to reasoning about counts, since order will be constructed implicitly.
2. If the number of distinct values is greater than two, immediately conclude that no valid arrangement exists. This follows from the alternation requirement, which allows only two values in any valid sequence.
3. If there is only one distinct value, the array is already trivially valid because every adjacent sum is identical.
4. If there are exactly two distinct values, extract their frequencies c1 and c2. Compute the two required group sizes, which are floor(n/2) and ceil(n/2).
5. Check whether the multiset of frequencies matches these two group sizes. If c1 and c2 are exactly these two values in any order, then a valid alternating arrangement exists.
6. Otherwise, return that no valid arrangement is possible.

The reasoning behind these steps comes from the forced equality b[i] = b[i+2]. This collapses any valid configuration into a strict two-coloring of positions, and the only remaining freedom is assigning which value goes to odd indices and which goes to even indices.

### Why it works

The adjacent sum condition forces equality between every second element because equal sums eliminate the middle term when subtracting consecutive constraints. This creates a rigid periodic structure of period two. Once this structure is known, the problem reduces entirely to checking whether the given multiset can be split into two groups matching the fixed position counts of that alternating pattern.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    freq = {}
    for x in a:
        freq[x] = freq.get(x, 0) + 1
    
    if len(freq) == 1:
        print("Yes")
        return
    
    if len(freq) > 2:
        print("No")
        return
    
    vals = list(freq.values())
    vals.sort()
    
    n1 = n // 2
    n2 = n - n1
    
    if (vals[0] == n1 and vals[1] == n2) or (vals[0] == n2 and vals[1] == n1):
        print("Yes")
    else:
        print("No")

t = int(input())
for _ in range(t):
    solve()
```

The solution compresses the array into a frequency map, which is the critical transformation that replaces permutation reasoning with counting reasoning. The special cases for one and more than two distinct values directly encode the structural constraint derived earlier. The final check aligns frequencies with the forced parity split of indices.

A common implementation pitfall is forgetting that the two values can be assigned to either parity class. This is why both assignments are checked symmetrically.

## Worked Examples

### Example 1

Input:

```
3
1 1 2
```

| Step | Distinct Values | Frequencies | Decision |
| --- | --- | --- | --- |
| Initial | {1, 2} | 1:2, 2:1 | Two distinct values |
| Split sizes | - | n1 = 1, n2 = 2 | Need 1 and 2 split |
| Check | - | {1,2} matches | Yes |

This demonstrates that even though the array is not already alternating, it can be rearranged into 1, 2, 1, satisfying constant adjacent sums.

### Example 2

Input:

```
4
1 1 4 5
```

| Step | Distinct Values | Frequencies | Decision |
| --- | --- | --- | --- |
| Initial | {1,4,5} | 1:2, 4:1, 5:1 | More than two values |
| Rule | - | - | Impossible |

This shows why having three distinct values breaks the alternation structure, since a period-two sequence cannot accommodate a third symbol.

The second example confirms that the algorithm rejects cases where structural constraints are violated even if local rearrangements seem plausible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once to build frequencies |
| Space | O(n) | Frequency map stores at most n distinct keys |

Given that n is at most 100 per test case, this solution is comfortably within limits even under the maximum number of test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = []
    
    t = int(input())
    
    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        
        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1
        
        if len(freq) == 1:
            out.append("Yes")
            return
        
        if len(freq) > 2:
            out.append("No")
            return
        
        vals = list(freq.values())
        vals.sort()
        
        n1 = n // 2
        n2 = n - n1
        
        if (vals[0] == n1 and vals[1] == n2) or (vals[0] == n2 and vals[1] == n1):
            out.append("Yes")
        else:
            out.append("No")
    
    for _ in range(t):
        solve()
    
    return "\n".join(out)

# provided samples
assert run("""5
2
8 9
3
1 1 2
4
1 1 4 5
5
2 3 3 3 3
4
100000 100000 100000 100000
""") == """Yes
Yes
No
No
Yes"""

# custom cases
assert run("""3
2
1 2
3
7 7 7
4
1 2 3 4
""") == """Yes
Yes
No"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2, 1 2 | Yes | Minimum n=2 always works |
| 3, 7 7 7 | Yes | All equal values |
| 4, 1 2 3 4 | No | More than two distinct values |

## Edge Cases

One edge case is when the array has exactly two elements. Any ordering of two numbers trivially satisfies the condition because there is only one adjacent sum. The algorithm handles this implicitly because the frequency sizes match the required split of 1 and 1.

Another edge case is when all elements are identical. In that situation, the frequency map has size one, and the algorithm immediately returns success. This matches the fact that any permutation preserves constant adjacency sums.

A further subtle case occurs when there are exactly two distinct values but the counts are imbalanced in a way that does not match the parity split. For instance, in an array of length five, if counts are 4 and 1, no alternating arrangement can distribute values into positions 1,3,5 and 2,4 correctly. The algorithm rejects this because the sorted frequency pair does not match 3 and 2.

These cases confirm that the frequency-based condition fully captures all structural constraints imposed by the adjacency sum requirement.
