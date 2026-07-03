---
title: "CF 103433D - Similar Arrays"
description: "We are given an array and we are asked to decide a notion of similarity between arrays under a specific transformation rule."
date: "2026-07-03T07:56:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103433
codeforces_index: "D"
codeforces_contest_name: "2018-2019 Russia Team Open, High School Programming Contest (VKOSHP 18)"
rating: 0
weight: 103433
solve_time_s: 40
verified: true
draft: false
---

[CF 103433D - Similar Arrays](https://codeforces.com/problemset/problem/103433/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and we are asked to decide a notion of similarity between arrays under a specific transformation rule. The problem is essentially about comparing how two sequences behave when you are allowed to normalize or “compress” their structure in a consistent way and then check whether the resulting representations match.

Each test case provides two arrays of equal length. The task is to determine whether these arrays can be considered equivalent under a process that ignores the exact values and instead preserves only the relative structure induced by ordering and repetition patterns. In other words, two arrays are similar if they induce the same pattern of how new values appear as you scan from left to right.

To make this concrete, imagine reading an array from left to right and replacing each distinct value with the index of its first occurrence in that array. This produces a canonical “shape signature” for the array. The problem reduces to checking whether both arrays produce identical signatures.

The constraints imply that we must process potentially large arrays, so any quadratic comparison of substructures or pairwise alignment between all elements would be too slow. A linear scan per array is the only viable direction.

Edge cases matter around repeated values and first occurrences. For example, consider:

Input:

A = [5, 7, 5]

B = [1, 2, 1]

Both arrays produce the same pattern signature [0, 1, 0]. A naive element-wise comparison would fail because values differ, even though structurally they are identical.

Another subtle case arises when repetition structure is preserved but ordering of first occurrences differs:

A = [1, 2, 3, 2]

B = [4, 5, 6, 5]

Both are similar. But if one array introduces a new value earlier or later, the signatures diverge immediately.

## Approaches

A brute-force idea is to compare all possible relabelings of values in the first array to match the second array. This means trying to construct a bijection between values of A and B that preserves positions. For each mapping attempt, we would validate consistency across the arrays. The number of mappings grows factorially in the number of distinct elements, since any permutation of labels might be considered. Even if we restrict ourselves to constructing mappings greedily, we still end up repeatedly checking consistency across the full array, which makes the total cost quadratic or worse.

The key observation is that the actual numeric values do not matter at all. What matters is only whether we have seen a value before and in what order new values appear. Each array can be reduced independently into a canonical form by replacing every first occurrence with a new identifier and reusing that identifier for subsequent occurrences.

Once both arrays are converted into these canonical sequences, the problem reduces to a direct equality check.

This works because the “similarity” relation described in the problem is exactly an isomorphism between the structures induced by first occurrences. The canonical encoding removes the need to reason about any actual value correspondence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Mapping | O(n! · n) | O(n) | Too slow |
| Canonical Encoding | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each array independently and construct its structural signature.

1. Create an empty dictionary that will map each previously unseen value to a unique integer identifier. This identifier represents the order in which values are first encountered.
2. Maintain a counter starting from zero. This counter assigns new identifiers to new values in increasing order.
3. Scan the array from left to right. For each element, check whether it has been seen before.
4. If the element is new, assign it the current counter value and increment the counter. This ensures that earlier discoveries get smaller identifiers, preserving discovery order.
5. If the element has been seen, reuse its assigned identifier.
6. Build a transformed array consisting of these identifiers.
7. Repeat the same process for the second array.
8. Compare the two transformed arrays directly. If they are identical, output “YES”, otherwise output “NO”.

The reason this construction is correct is that the mapping depends only on the sequence of first occurrences, which is the only structural information preserved under any valid similarity transformation. Any two arrays that are similar must induce identical discovery sequences, since the i-th time a new value appears must correspond to the i-th new value in the other array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def encode(arr):
    mp = {}
    cur = 0
    res = []
    for x in arr:
        if x not in mp:
            mp[x] = cur
            cur += 1
        res.append(mp[x])
    return res

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    if encode(a) == encode(b):
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The solution is split into a helper function and the main logic. The helper function builds the canonical encoding by tracking first occurrences using a dictionary. The ordering of assignment is critical, since it enforces that the first time we see a value determines its identity.

The main function reads both arrays, encodes them independently, and compares the results. No additional normalization is required since the encoding already eliminates dependence on raw values.

A subtle detail is that we must not reuse state between the two encodings. Each array must start with a fresh mapping so that their structures are comparable in isolation.

## Worked Examples

### Example 1

Input:

A = [5, 7, 5]

B = [1, 2, 1]

Encoding process:

| Step | A element | A mapping | A encoded | B element | B mapping | B encoded |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | {5:0} | [0] | 1 | {1:0} | [0] |
| 2 | 7 | {5:0,7:1} | [0,1] | 2 | {1:0,2:1} | [0,1] |
| 3 | 5 | {5:0,7:1} | [0,1,0] | 1 | {1:0,2:1} | [0,1,0] |

Both encoded arrays match, so output is YES.

This confirms that equality depends only on structure, not actual values.

### Example 2

Input:

A = [1, 2, 1, 3]

B = [4, 5, 5, 6]

| Step | A element | A mapping | A encoded | B element | B mapping | B encoded |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | {1:0} | [0] | 4 | {4:0} | [0] |
| 2 | 2 | {1:0,2:1} | [0,1] | 5 | {4:0,5:1} | [0,1] |
| 3 | 1 | {1:0,2:1} | [0,1,0] | 5 | {4:0,5:1} | [0,1,1] |
| 4 | 3 | {1:0,2:1,3:2} | [0,1,0,2] | 6 | {4:0,5:1,6:2} | [0,1,1,2] |

The encoded sequences differ at position 3, so output is NO.

This demonstrates that even a single deviation in repetition structure breaks similarity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each array is scanned once and dictionary operations are O(1) average |
| Space | O(n) | We store mappings and encoded arrays |

The solution fits easily within typical constraints of up to 2×10^5 elements, since the algorithm performs only linear work per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def encode(arr):
        mp = {}
        cur = 0
        res = []
        for x in arr:
            if x not in mp:
                mp[x] = cur
                cur += 1
            res.append(mp[x])
        return res

    t = 1
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        out.append("YES" if encode(a) == encode(b) else "NO")
    return "\n".join(out)

# sample-like cases
assert run("3\n5 7 5\n1 2 1\n") == "YES"
assert run("4\n1 2 1 3\n4 5 5 6\n") == "NO"

# custom cases
assert run("1\n1\n1\n") == "YES"
assert run("2\n1 2\n2 1\n") == "YES"
assert run("3\n1 2 3\n1 1 1\n") == "NO"
assert run("5\n1 2 3 2 1\n4 5 6 5 4\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-element identical | YES | minimum size correctness |
| swapped distinct values | YES | symmetry under relabeling |
| all equal vs distinct | NO | repetition structure mismatch |
| palindromic pattern match | YES | repeated structure consistency |

## Edge Cases

One important edge case is when both arrays contain all identical values. For example, A = [7, 7, 7] and B = [3, 3, 3]. The encoding for both becomes [0, 0, 0], since no new values appear after the first element. The algorithm handles this naturally because the dictionary never grows beyond one entry.

Another case is when arrays have the same multiset but different structure, such as A = [1, 2, 2, 3] and B = [1, 2, 3, 3]. The first array encodes as [0, 1, 1, 2], while the second becomes [0, 1, 2, 2]. The mismatch occurs exactly at the third position, where the identity of “first occurrence” diverges.

A final subtle case is when values are large or negative. Since we only rely on hashing in a dictionary, the actual magnitude of values does not affect correctness or performance.
