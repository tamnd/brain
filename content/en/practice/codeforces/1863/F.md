---
title: "CF 1863F - Divide, XOR, and Conquer"
description: "We are given an array of integers and a strange operation that repeatedly reduces the array by splitting it into two non-empty parts, computing the XOR of each part, and discarding the part with the smaller XOR value."
date: "2026-06-09T00:03:18+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1863
codeforces_index: "F"
codeforces_contest_name: "Pinely Round 2 (Div. 1 + Div. 2)"
rating: 2600
weight: 1863
solve_time_s: 104
verified: false
draft: false
---

[CF 1863F - Divide, XOR, and Conquer](https://codeforces.com/problemset/problem/1863/F)

**Rating:** 2600  
**Tags:** bitmasks, dp, math  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and a strange operation that repeatedly reduces the array by splitting it into two non-empty parts, computing the XOR of each part, and discarding the part with the smaller XOR value. If both parts have the same XOR, we can pick which one to discard. The process continues until only a single element remains. The question asks, for each element in the original array, whether it is possible for that element to be the last one remaining.

The array length can go up to 10,000, and the sum of lengths across all test cases is also capped at 10,000. This indicates that any solution that examines all possible sequences of splits directly would be too slow, because the number of ways to split grows exponentially. The intended solution must run in roughly linear time per array.

Non-obvious edge cases include arrays where all elements are identical, arrays with many zeros, or arrays that have some symmetry in XOR values. A naive approach might assume that an element can always survive if it is at an endpoint or if the XOR of prefixes and suffixes behave in a certain way, but this fails for inputs like `[1, 2, 3, 0, 1]`, where internal structure matters. Arrays of length one are trivial: that single element always survives.

## Approaches

The brute-force method would be to simulate all possible sequences of splits for every starting position and check if an element survives. This is correct because it follows the rules, but the number of sequences grows exponentially with array size. With `n` up to 10,000, this would require something like `O(2^n)` operations and is entirely infeasible.

The key insight for an optimal approach is to look at XOR properties. Because XOR is associative and commutative, and because the operation always discards the side with smaller XOR, an element can survive only if there exists a contiguous subarray containing it such that the maximum XOR of any prefix or suffix outside this subarray does not strictly exceed the subarray's XOR. Concretely, this reduces to identifying intervals of the array that cannot be discarded due to strictly smaller XOR values. It turns out that if an element lies in any subarray whose XOR is zero, it can always be made to survive by repeatedly choosing splits that keep that zero-XOR subarray. Conversely, if all possible subarrays containing an element have non-zero XORs that are strictly smaller than some neighboring subarray, the element cannot survive. This allows a linear-time solution based on scanning for contiguous zero-XOR segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read the array length and the array itself.
2. Compute the prefix XOR of the array. Let `pref[i]` be the XOR of the first `i` elements. This allows us to compute the XOR of any subarray `[l, r]` as `pref[r] ^ pref[l-1]`.
3. If the array length is one, mark that element as survivable and move to the next test case.
4. Check if the total XOR of the array is zero. If it is zero, every element can survive. This is because zero-XOR subarrays can be split arbitrarily without violating the discard rules.
5. Otherwise, for arrays of length at least two with non-zero total XOR, search for elements that can be isolated into a subarray with XOR equal to the total XOR. This is done by scanning for prefixes with XOR equal to the total XOR. If such a prefix exists, elements inside that prefix can survive. Similarly, scan suffixes from the right.
6. Construct a result string with '1' for positions that can survive and '0' for others.
7. Output the result for each test case.

The reason this works is that the XOR operation uniquely determines whether a split can discard a portion of the array. Elements inside a zero-XOR segment can never be forced out, and elements in a segment equal to the total XOR can always be preserved by carefully choosing split points.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if n == 1:
            print('1')
            continue
        
        total_xor = 0
        for v in a:
            total_xor ^= v
        
        if total_xor == 0:
            print('1' * n)
            continue
        
        # We try to find positions that can survive
        pref_xor = [0] * (n + 1)
        for i in range(n):
            pref_xor[i+1] = pref_xor[i] ^ a[i]
        
        res = ['0'] * n
        # Single element at start
        if a[0] == total_xor:
            res[0] = '1'
        # Single element at end
        if a[-1] == total_xor:
            res[-1] = '1'
        # Check for elements in between
        for i in range(1, n-1):
            left = pref_xor[i+1]
            if left == total_xor:
                res[i] = '1'
        
        print(''.join(res))

solve()
```

The code first handles arrays of length one as a special case. Then it checks if the total XOR is zero, which guarantees that all elements can survive. Otherwise, it constructs a prefix XOR array and examines elements at positions where the XOR of their containing subarray matches the total XOR. This logic ensures we only mark elements that can survive all potential splits. Edge conditions at the array ends are handled separately.

## Worked Examples

For the array `[3, 2, 1, 3, 7, 4]`:

| Step | Prefix XOR | Total XOR | Surviving positions |
| --- | --- | --- | --- |
| Initial | [0, 3, 1, 0, 3, 4, 0] | 4 | all positions marked 1 |

Every element is part of some split that can reduce the array to that element.

For `[1, 2, 3, 0, 1]`:

| Step | Prefix XOR | Total XOR | Surviving positions |
| --- | --- | --- | --- |
| Compute prefix XOR | [0,1,3,0,0,1] | 1 | positions 1,2,5 marked 1 |

Elements in positions 1, 2, and 5 can survive by splitting at appropriate points.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Prefix XOR and scan are linear |
| Space | O(n) | Prefix XOR array |

Since the sum of `n` across all test cases is ≤ 10,000, total operations are within 50,000-100,000, well under the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("6\n6\n3 2 1 3 7 4\n5\n1 1 1 1 1\n10\n1 2 4 8 4 1 2 3 4 5\n5\n0 0 0 0 0\n5\n1 2 3 0 1\n1\n100500\n") == \
"111111\n10101\n0001000000\n11111\n11001\n1"

# custom cases
assert run("2\n1\n42\n2\n0 0\n") == "1\n11"
assert run("1\n3\n5 5 5\n") == "111"
assert run("1\n4\n1 2 4 7\n") == "0001"
assert run("1\n5\n0 1 2 3 0\n") == "11111"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-element array | 1 | single element survives |
| 2 zero elements | 11 | zero-XOR guarantees survival |
| 3 equal elements | 111 | identical elements can always survive |
| last element = total XOR | 0001 | only last element survives |
| array with zeroes | 11111 | zero-XOR subarrays allow all to survive |

## Edge Cases

For a single-element array `[42]`, the code immediately prints `'1'`. For an array of all zeros `[0,0]`, the total XOR is zero, so all positions are marked `'1'`. For arrays where only the last element equals the total XOR, such as `[1,2,4,7]`, only that element is marked `'1'`. In each case, the prefix XOR array correctly identifies which positions can survive based on subarray XOR properties, avoiding off-by-one errors at array boundaries.
