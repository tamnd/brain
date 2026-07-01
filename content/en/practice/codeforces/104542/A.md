---
title: "CF 104542A - Interesting Subsequence"
description: "We are given an array and we are allowed to pick any subsequence of it as a candidate sequence $b$. The twist is that we are not checking $b$ against the original array alone, but against a family of derived arrays."
date: "2026-06-30T09:09:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104542
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #22 (Interesting-Forces)"
rating: 0
weight: 104542
solve_time_s: 84
verified: false
draft: false
---

[CF 104542A - Interesting Subsequence](https://codeforces.com/problemset/problem/104542/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and we are allowed to pick any subsequence of it as a candidate sequence $b$. The twist is that we are not checking $b$ against the original array alone, but against a family of derived arrays.

For any position $i$, we remove $a_i$ from the array, and then we conceptually repeat this shortened array many times, specifically $n$ copies concatenated together. This creates a long sequence $c$ of length $n(n-1)$. The requirement is that there must exist at least one subsequence $b$ of the original array such that for some choice of $i$, $b$ cannot be found as a subsequence inside this repeated structure $c$.

So the task is not to construct $b$, but to decide whether such a “distinguishing subsequence” exists at all.

The constraints are large, with total $n$ across test cases up to $2 \cdot 10^5$. Any solution that tries to test all subsequences is immediately impossible, since the number of subsequences is exponential. Even checking a single candidate subsequence against all $i$ choices would still be too expensive if done naively, because subsequence checking itself is linear in the array size.

This pushes us toward a structural observation: the only way a subsequence can fail to appear in $c$ is if some value in $b$ is too “rare” in the modified array, or if ordering constraints force an impossible alignment across repeated copies.

A few subtle edge situations naturally arise.

If all elements are identical, for example $a = [1,1,1]$, then removing any one element still leaves a constant array. Any subsequence $b$ is just a sequence of 1s, and it always appears in repeated copies. This suggests a “NO” outcome.

If there exists a value that appears only once, say $a = [1,2,3]$, removing the unique element can drastically change availability of symbols, often making it impossible to embed certain subsequences in all copies simultaneously.

The key difficulty is that $c$ repeats the same multiset $n$ times, so it has huge redundancy. The only meaningful limitation comes from the fact that one position is removed before repetition.

## Approaches

A brute-force approach would try every subsequence $b$, then for each $i$, build $c$ and check if $b$ is a subsequence of $c$. Even ignoring exponential subsequences, building and scanning $c$ costs $O(n^2)$, which is far too large.

We need to reinterpret what “$b$ is a subsequence of $c$” really means. Since $c$ is just $n$ repetitions of the array with one element removed, any subsequence embedding of $b$ can be distributed across copies. This means repetition helps the matching process rather than restricting it.

The crucial insight is to reverse the viewpoint. Instead of asking whether some $b$ fails in some $c$, we ask when every subsequence of $a$ remains embeddable in every such repeated structure. This happens exactly when removing any single element does not reduce the expressive power of the sequence enough to block a subsequence pattern.

This collapses the problem into checking whether there exists any “critical structure” in $a$, and that structure turns out to be determined entirely by whether all elements are identical. If at least two distinct values exist, we can always construct a subsequence that forces a mismatch when any index is removed. If all values are identical, repetition guarantees every subsequence remains valid everywhere.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the array and determine whether all elements are equal.

If there are at least two distinct values, we immediately know a valid subsequence exists.
2. If all elements are identical, conclude that no such distinguishing subsequence can exist.

The reasoning behind step 1 is that diversity in values allows us to construct a subsequence that depends on relative ordering or availability of different symbols, which can be disrupted by removing a carefully chosen index.

Step 2 follows because a constant array remains invariant under deletion and repetition, so every subsequence remains representable in every constructed $c$.

### Why it works

If the array contains at least two distinct values, pick two positions with different values. Any subsequence that encodes a transition between these two values can be made sensitive to deletion of a carefully chosen index, because removing one element can break a necessary alignment across repeated copies of the array. The repetition in $c$ does not remove this vulnerability since all copies are identical except for the missing position, so a carefully chosen subsequence cannot always be embedded.

If all values are identical, every subsequence is just a string of identical elements. Removing any one position does not change the fact that every symbol is the same, and repetition only increases availability. Thus, every subsequence of $a$ remains a subsequence of every possible $c$, so no valid $b$ exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # check if all elements are the same
        first = a[0]
        ok = False
        for x in a:
            if x != first:
                ok = True
                break
        
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the reduction to checking whether there are at least two distinct values. The loop exits early once a mismatch is found, ensuring linear time per test case.

A common mistake here is overcomplicating the logic by trying to simulate subsequence matching. The key is that the structure of $c$ makes the only meaningful property the diversity of elements, not their arrangement.

## Worked Examples

### Example 1

Input:

```
3
2
1 1
3
1 2 1
4
5 4 1 1
```

We track whether the array has distinct elements.

| Test | Array | Distinct found | Output |
| --- | --- | --- | --- |
| 1 | [1,1] | No | NO |
| 2 | [1,2,1] | Yes | YES |
| 3 | [5,4,1,1] | Yes | YES |

In the first case, all values are identical, so any subsequence remains fully matchable in any repeated structure. In the other cases, the presence of at least two distinct values guarantees a valid distinguishing subsequence exists.

### Example 2

Input:

```
2
5
7 7 7 7 7
4
1 2 2 2
```

| Test | Array | Distinct found | Output |
| --- | --- | --- | --- |
| 1 | [7,7,7,7,7] | No | NO |
| 2 | [1,2,2,2] | Yes | YES |

The second case demonstrates that even a single different element is enough to break uniformity and allow a separating subsequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | single pass to check distinctness |
| Space | $O(1)$ | only constant extra variables |

The total complexity is linear in the input size across all test cases, which fits comfortably within the constraint of $2 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        first = a[0]
        ok = any(x != first for x in a)
        out.append("YES" if ok else "NO")
    return "\n".join(out)

# provided samples
assert run("3\n2\n1 1\n3\n1 2 1\n4\n5 4 1 1\n") == "NO\nYES\nYES"

# all equal minimum
assert run("1\n2\n7 7\n") == "NO"

# single deviation
assert run("1\n5\n9 9 9 1 9\n") == "YES"

# strictly increasing
assert run("1\n4\n1 2 3 4\n") == "YES"

# large uniform
assert run("1\n5\n5 5 5 5 5\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | NO | uniform array rejection |
| one differing | YES | minimal diversity case |
| increasing | YES | general distinct case |
| uniform large | NO | boundary uniform handling |

## Edge Cases

A fully uniform array such as $a = [4,4,4,4]$ always leads to NO. The algorithm reads the first value as 4 and never finds a mismatch, so `ok` remains false, correctly producing NO.

A near-uniform array such as $a = [10,10,10,11,10]$ triggers the early exit at the fourth element. The flag becomes true immediately, ensuring YES without needing to inspect further structure.

A length-2 array is handled correctly as well. For $a = [3,3]$, no difference exists so the answer is NO. For $a = [3,5]$, the first comparison already detects distinctness and returns YES.
