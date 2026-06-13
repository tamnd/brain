---
title: "CF 1243A - Maximum Square"
description: "We are given several test cases, each consisting of a list of plank heights. Every plank has width 1 and some integer height."
date: "2026-06-13T20:13:31+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1243
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 599 (Div. 2)"
rating: 800
weight: 1243
solve_time_s: 384
verified: true
draft: false
---

[CF 1243A - Maximum Square](https://codeforces.com/problemset/problem/1243/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 6m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases, each consisting of a list of plank heights. Every plank has width 1 and some integer height. We are allowed to pick any subset of these planks and rearrange them in any order side by side, forming a skyline-like shape where each chosen plank contributes a vertical column.

Once the planks are arranged, we are allowed to cut out a square whose sides are aligned with the axes. The square must lie completely inside the combined shape. The goal is to maximize the side length of such a square.

The key freedom in the problem is that we can both choose any subset of planks and permute them arbitrarily. This removes any positional constraints from the original array and reduces the structure to purely a multiset of heights.

The constraint limits are small, with at most 1000 planks per test case and at most 10 test cases. This allows solutions that are quadratic or O(n log n), but anything cubic or involving repeated heavy simulation would be unnecessary. A linear scan or frequency-based reasoning is sufficient.

A subtle failure case for naive reasoning appears when focusing only on the maximum height or total sum. For example, with heights `[5, 1, 1, 1, 1]`, it is tempting to think a 5×5 square is possible because there exists a 5. However, only one column has height at least 5, so we cannot form a 5-wide square. The correct answer is 1.

Another misleading case is when many tall planks exist but not enough of them. For `[4, 4, 4, 1, 1]`, one might expect a 4×4 square, but only three planks have height at least 4, so width 4 is impossible.

These examples show that both height and count constraints must be satisfied simultaneously.

## Approaches

The brute-force idea is to try every possible square size k. For each k, we check whether we can select at least k planks whose heights are at least k. If yes, then a k×k square can be formed by taking those k tall planks and arranging them consecutively.

Checking a single k takes O(n), and trying all k up to n leads to O(n²) per test case. With n up to 1000, this is acceptable but unnecessary.

The key observation is that for a fixed k, only planks with height ≥ k matter. If there are at least k such planks, we can always choose k of them and place them next to each other. The arrangement freedom removes all geometric complexity; the problem reduces to a counting condition.

Instead of checking all k values independently, we can count frequencies or sort the array and compute, for each possible k, how many elements are ≥ k. The answer is the largest k satisfying this condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over k | O(n²) | O(1) | Accepted |
| Sort / frequency counting | O(n log n) or O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We transform the geometric problem into a counting problem over heights.

1. For a fixed candidate side length k, we interpret the requirement as needing k planks whose heights are at least k. This is because a square of side k must have k columns, each reaching at least height k.
2. Count how many planks satisfy height ≥ k. If this count is at least k, then a square of size k is feasible.
3. Try all possible k from 1 to n and track the maximum feasible value.
4. To compute counts efficiently, either sort the array or build a frequency array. Sorting allows us to quickly determine how many elements are above a threshold using index positions.
5. Return the largest k that satisfies the feasibility condition.

The reason we can safely ignore arrangement details is that once we pick k valid planks, we can always place them consecutively. There is no restriction on spacing or ordering, so feasibility depends only on quantity, not structure.

### Why it works

The algorithm relies on the fact that a k×k square requires k independent vertical supports of height at least k. Since planks can be rearranged freely, any chosen subset can be made contiguous. This removes spatial constraints and reduces the problem to verifying a simple inequality between a threshold and a count. No configuration exists that violates this condition once it is satisfied.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input())
    for _ in range(k):
        n = int(input())
        a = list(map(int, input().split()))
        
        a.sort()
        
        ans = 0
        for i in range(1, n + 1):
            # number of elements >= i
            # in sorted array, this is n - first index where a[idx] >= i
            lo, hi = 0, n
            while lo < hi:
                mid = (lo + hi) // 2
                if a[mid] >= i:
                    hi = mid
                else:
                    lo = mid + 1
            cnt = n - lo
            if cnt >= i:
                ans = i
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution sorts the plank heights so that we can efficiently compute how many values exceed each candidate threshold. For each potential square side i, we binary search the first position where height becomes at least i, and derive the count from that position.

The main subtlety is correctly interpreting the condition: we are not building a geometric square directly, but verifying that enough sufficiently tall planks exist to support it.

## Worked Examples

### Example 1

Input: `[4, 3, 1, 4, 5]`

We evaluate possible k values:

| k | count of a[i] ≥ k | feasible |
| --- | --- | --- |
| 1 | 5 | yes |
| 2 | 4 | yes |
| 3 | 4 | yes |
| 4 | 3 | no |
| 5 | 1 | no |

The maximum feasible value is 3.

This shows that even though a height of 5 exists, it does not dominate the answer because width requires multiple tall planks.

### Example 2

Input: `[4, 4, 4, 4]`

| k | count of a[i] ≥ k | feasible |
| --- | --- | --- |
| 1 | 4 | yes |
| 2 | 4 | yes |
| 3 | 4 | yes |
| 4 | 4 | yes |

The answer is 4, since all planks are tall enough to support any square up to size 4.

This demonstrates the case where uniform heights maximize the result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test | sorting dominates, binary search per k is O(n log n) total |
| Space | O(n) | storing the array |

Given n ≤ 1000 and k ≤ 10, this easily fits within limits. Even an O(n²) approach would pass, but sorting-based counting is cleaner and more direct.

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
            a.sort()
            ans = 0
            for i in range(1, n + 1):
                lo, hi = 0, n
                while lo < hi:
                    mid = (lo + hi) // 2
                    if a[mid] >= i:
                        hi = mid
                    else:
                        lo = mid + 1
                if n - lo >= i:
                    ans = i
            print(ans)

    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""4
5
4 3 1 4 5
4
4 4 4 4
3
1 1 1
5
5 5 1 1 5
""") == """3
4
1
3"""

# all equal
assert run("""1
5
2 2 2 2 2
""") == "2"

# single element
assert run("""1
1
10
""") == "1"

# skewed distribution
assert run("""1
5
5 1 1 1 1
""") == "1"

# tight boundary
assert run("""1
6
3 3 3 3 3 3
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal array | single value | uniform optimal square |
| single element | 1 | minimal boundary case |
| skewed distribution | 1 | insufficient width despite tall max |
| uniform mid values | 3 | correct scaling behavior |

## Edge Cases

A common edge case is when a single very large plank exists among many small ones. For example, `[100, 1, 1, 1, 1]` should return 1 because only one plank can support height 100.

Another edge case is when all planks are identical. For `[3, 3, 3]`, the answer is 3 because both height and count constraints align perfectly at every threshold up to 3.
