---
title: "CF 1610B - Kalindrome Array"
description: "We are given an array and allowed to perform a very specific type of transformation: we may pick one value x and remove any occurrences of that value from the array, not necessarily all of them."
date: "2026-06-10T07:09:18+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1610
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 17"
rating: 1100
weight: 1610
solve_time_s: 111
verified: true
draft: false
---

[CF 1610B - Kalindrome Array](https://codeforces.com/problemset/problem/1610/B)

**Rating:** 1100  
**Tags:** greedy, two pointers  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and allowed to perform a very specific type of transformation: we may pick one value `x` and remove any occurrences of that value from the array, not necessarily all of them. After deletion, the remaining elements collapse together, and we check whether the resulting sequence is a palindrome.

The task is to decide whether there exists at least one choice of `x` such that this operation can make the array palindromic. We do not need to construct the deletion explicitly in the final output, only answer whether it is possible.

The constraints allow up to 10^4 test cases and a total array length across all tests up to 2 × 10^5. This immediately implies an O(n^2) per test or anything worse than linear per test is unsafe. Any solution must effectively process each test in linear time, possibly with a small number of linear scans.

A naive approach would try every possible value of `x`, remove it, and check whether the resulting array is a palindrome. That would be O(n^2) per test in the worst case, which is too slow when values repeat frequently.

A subtler failure case appears when arrays are almost palindromes but require removing a value that occurs in many positions. A greedy deletion attempt that removes the first mismatch value encountered will fail because the correct choice of `x` is global, not local.

## Approaches

A brute-force idea is straightforward: for each distinct value in the array, simulate removing all occurrences of that value, then check if the resulting array is a palindrome. Each check costs O(n), and there can be O(n) distinct values, so the total cost becomes O(n^2). This immediately breaks under the constraints.

The key observation is that the structure of a valid solution is heavily constrained by mismatches in the original array. We start from a standard palindrome check using two pointers. If the array is already a palindrome, we are done. Otherwise, we find the first position from the left and right where the values differ. At this point, any valid solution must remove all occurrences of either the left value or the right value involved in the mismatch, because these are the only candidates that can potentially eliminate the conflict at that position.

This reduces the problem to testing at most two candidates. For each candidate value, we simulate a two pointer palindrome check while skipping that value whenever it appears. If either simulation succeeds, the array is kalindrome.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force over all x | O(n^2) | O(n) | Too slow |
| Two-pointer candidate check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We begin with two pointers at the ends of the array. We move them inward while the values match. If we reach the middle, the array is already a palindrome.

If we encounter a mismatch at positions `l` and `r`, the only possible fixes are removing all occurrences of `a[l]` or all occurrences of `a[r]`. We test both options independently.

To test a candidate value `x`, we again use two pointers. Whenever we see `x`, we skip it by moving the pointer inward. Otherwise, we compare normally. If at any point the non-skipped values mismatch, this candidate fails.

We return YES if either candidate succeeds.

The reason this works is that the first mismatch in a two-pointer scan identifies the exact region where symmetry breaks. Any valid solution must remove one of the two conflicting values, otherwise the mismatch persists in every reduced version of the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_pal_after_removal(a, x):
    l, r = 0, len(a) - 1
    while l < r:
        while l < r and a[l] == x:
            l += 1
        while l < r and a[r] == x:
            r -= 1
        if l >= r:
            break
        if a[l] != a[r]:
            return False
        l += 1
        r -= 1
    return True

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        l, r = 0, n - 1
        
        while l < r and a[l] == a[r]:
            l += 1
            r -= 1
        
        if l >= r:
            print("YES")
            continue
        
        x, y = a[l], a[r]
        
        if is_pal_after_removal(a, x) or is_pal_after_removal(a, y):
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

After identifying the first mismatch, the code isolates exactly the two values that can influence the structure of any valid solution. The helper function performs a filtered palindrome check in linear time, skipping one candidate value entirely. This avoids rebuilding arrays and keeps memory usage constant.

A subtle point is that we do not try to remove partial occurrences arbitrarily. The skipping logic implicitly allows selective deletion while preserving order, which matches the problem definition.

## Worked Examples

Consider the input:

```
5
1 4 4 1 4
```

The initial two-pointer scan compares 1 and 4, which mismatch immediately. So candidates are 1 and 4.

Testing removal of 1 yields [4, 4, 4], which is a palindrome.

Testing removal of 4 yields [1, 1], which is also a palindrome.

The algorithm correctly returns YES.

Now consider:

```
3
1 2 3
```

The first mismatch occurs immediately at both ends (1 and 3). Removing only 1 yields [2, 3], not a palindrome. Removing only 3 yields [1, 2], also not a palindrome. The algorithm correctly returns NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n) per test | Each test performs at most two linear scans |
| Space | O(1) | Only pointers and variables are used |

The total input size across tests is bounded by 2 × 10^5, so a linear per-element processing strategy easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    def is_pal_after_removal(a, x):
        l, r = 0, len(a) - 1
        while l < r:
            while l < r and a[l] == x:
                l += 1
            while l < r and a[r] == x:
                r -= 1
            if l >= r:
                break
            if a[l] != a[r]:
                return False
            l += 1
            r -= 1
        return True

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        l, r = 0, n - 1
        while l < r and a[l] == a[r]:
            l += 1
            r -= 1
        if l >= r:
            out.append("YES")
        else:
            x, y = a[l], a[r]
            if is_pal_after_removal(a, x) or is_pal_after_removal(a, y):
                out.append("YES")
            else:
                out.append("NO")
    return "\n".join(out)

assert run("""4
1
1
2
1 2
3
1 2 3
5
1 4 4 1 4
""") == """YES
YES
NO
YES"""
```

| Test input | Expected output | What it validates |
|---|---|---|
| already palindrome | YES | trivial acceptance |
| single mismatch fixable | YES | candidate removal works |
| impossible case | NO | rejection correctness |
| symmetric multi-value case | YES | both candidate paths valid |

## Edge Cases

A critical edge case is when the array is already a palindrome. In that case the mismatch pointers never diverge, and the algorithm correctly terminates early without testing any deletion candidates. This prevents unnecessary computation and avoids false negatives.

Another edge case is when all elements are identical. The mismatch loop never triggers and the answer is immediately YES, since any removal still leaves a palindrome or empty array.
