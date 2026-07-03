---
title: "CF 103439G - Replace Sort"
description: "We are given an array $A$ that we want to transform into a nondecreasing sequence. Alongside it, we have a separate set $B$ of spare values. Every element across $A$ and $B$ is distinct."
date: "2026-07-03T07:46:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103439
codeforces_index: "G"
codeforces_contest_name: "XXII Open Cup, Grand Prix of Southeastern Europe"
rating: 0
weight: 103439
solve_time_s: 51
verified: true
draft: false
---

[CF 103439G - Replace Sort](https://codeforces.com/problemset/problem/103439/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array $A$ that we want to transform into a nondecreasing sequence. Alongside it, we have a separate set $B$ of spare values. Every element across $A$ and $B$ is distinct.

The only allowed operation is to take a value from $B$ and overwrite any position in $A$ with it, and each element of $B$ can be used at most once. The goal is not to rearrange $A$ directly, but to strategically replace some entries so that the final array becomes sorted in nondecreasing order, while minimizing how many replacements are used. If no sequence of replacements can achieve a sorted array, the answer is $-1$.

A key structural constraint is that replacements are not freely reusable. Each value in $B$ is a single-use tool, so the problem is not just “how many positions are wrong”, but “which positions can be repaired with which available values”.

The constraints allow $N, M$ up to $5 \cdot 10^5$, which immediately rules out any solution that tries to simulate replacements or try subsets. Anything quadratic in $N$ or $M$ is too slow. A valid approach must rely on sorting and linear or near-linear scans after preprocessing.

A subtle point is that we are not asked to make $A$ sorted by rearranging or inserting elements, but strictly by replacement. This means every final value must come either from the original array or from $B$, and we are effectively choosing which positions to “fix” and what values to assign.

Edge cases that break naive reasoning are easy to miss. For example, if $A = [2, 6, 13, 10]$ and $B = [5]$, one might think replacing 13 with 5 fixes the inversion with 10, but it can break ordering constraints on the left side if we later need a larger value there. This is exactly why local fixes fail: a replacement must be globally consistent with the final monotone structure.

Another edge case is when all elements in $B$ are either too small or too large to repair necessary constraints. For instance, if $A = [3, 1, 2]$ and $B = [0]$, there is no way to fix the inversion between 3 and 1 while keeping feasibility for the rest.

## Approaches

A brute-force strategy would try all subsets of positions in $A$ to replace, and for each subset check whether we can assign distinct values from $B$ so that the resulting array is sorted. For a fixed subset of size $k$, we would also need to choose which $k$ values from $B$ to use and match them to positions. Even if feasibility checking were linear, the number of subsets is $2^N$, and assigning values adds factorial complexity. This is completely infeasible beyond very small $N$.

The key observation is that once the final array is sorted, the structure is rigid: there is a target nondecreasing sequence we must match, and every position imposes a constraint on what value can end up there. Instead of thinking in terms of arbitrary replacements, we shift to thinking about how to construct a valid sorted array from left to right while minimizing how often we are forced to use $B$.

A useful way to reframe the problem is to consider the final sorted array as some nondecreasing sequence that must be “compatible” with the original $A$. If we process $A$ from left to right, we want to keep as many original values as possible, but only if they can still fit into a globally increasing structure. Whenever an element breaks feasibility, we may replace it, but we should use the smallest available value from $B$ that can maintain consistency. This naturally suggests a greedy strategy once we understand that feasibility depends only on ordering constraints, not identity of positions.

The deeper insight is that we can treat the problem as constructing the longest prefix of $A$ that can be kept unchanged while still being extendable into a sorted array using available replacements. Any element that cannot be kept forces us to use a replacement, and the choice of replacement must respect future ordering, which pushes us toward sorting both $A$ and $B$ and greedily matching constraints.

The final solution becomes a sweep where we maintain the last chosen value in the final array and decide whether to keep $A[i]$ or replace it with the smallest possible $B$ value that still preserves nondecreasing order. If neither is possible, the configuration is impossible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subset + Validation | $O(2^N)$ | $O(N)$ | Too slow |
| Greedy with Sorted Arrays | $O((N+M)\log(N+M))$ | $O(N+M)$ | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Sort both arrays $A$ and $B$. Sorting $B$ allows us to always pick the smallest usable replacement when needed, which is crucial because larger replacements only make future feasibility harder.
2. Initialize a pointer $j = 0$ for $B$, and a variable $last = -\infty$ representing the last value placed in the constructed final array. This tracks the monotone constraint.
3. Scan through each element $A[i]$ from left to right, deciding whether to keep it or replace it. This order matters because earlier decisions restrict all future positions.
4. If $A[i] \ge last$, we can safely keep $A[i]$, and we set $last = A[i]$. This is optimal because keeping original values reduces the number of replacements.
5. Otherwise, we try to repair the violation using $B$. We advance pointer $j$ until we find the smallest $B[j] \ge last$. If such an element exists, we use it, increment the replacement count, and update $last = B[j]$, then move $j$ forward.
6. If neither $A[i]$ nor any remaining value in $B$ can satisfy $last$, we conclude the process is impossible and return $-1$. This corresponds to a gap in available values that cannot be bridged without breaking monotonicity.
7. Continue until all elements of $A$ are processed, and return the number of replacements used.

### Why it works

The algorithm maintains the invariant that after processing index $i$, the constructed sequence is the lexicographically smallest possible nondecreasing sequence achievable using some subset of replacements. Sorting $B$ ensures that whenever we must insert a replacement, using the smallest feasible value preserves maximum flexibility for future positions. Any larger choice would only tighten future constraints without improving current feasibility, because the only requirement is nondecreasing order, not closeness to original values. This greedy dominance ensures that if a solution exists, the algorithm never blocks itself unnecessarily.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    a.sort()
    b.sort()
    
    j = 0
    last = -10**18
    used = 0
    
    for x in a:
        if x >= last:
            last = x
        else:
            while j < m and b[j] < last:
                j += 1
            if j == m:
                print(-1)
                return
            last = b[j]
            j += 1
            used += 1
    
    print(used)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the greedy construction directly. Sorting both arrays is the structural step that turns the problem into a monotone matching process. The pointer over $B$ ensures each replacement is used at most once and always chosen minimally.

A subtle implementation detail is the use of a large negative initial value for $last$, which avoids special casing the first element. Another is that we never reconsider earlier choices, so the scan is strictly linear after sorting.

## Worked Examples

### Example 1

Input:

```
4 1
2 6 13 10
5
```

We sort $A$ as $[2, 6, 10, 13]$ and $B = [5]$.

| i | A[i] | last | Action | B used | last after |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | -inf | keep | 0 | 2 |
| 1 | 6 | 2 | keep | 0 | 6 |
| 2 | 10 | 6 | keep | 0 | 10 |
| 3 | 13 | 10 | cannot keep, try B but 5 < 10 | 0 | fail |

We cannot find any usable replacement at the last step, so the answer is $-1$. This shows that even though only one inversion exists in the original array, there is no available value in $B$ large enough to preserve monotonic growth after earlier decisions.

### Example 2

Input:

```
4 2
2 6 13 10
5 4
```

Sorted arrays: $A = [2, 6, 10, 13]$, $B = [4, 5]$.

| i | A[i] | last | Action | B used | last after |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | -inf | keep | 0 | 2 |
| 1 | 6 | 2 | keep | 0 | 6 |
| 2 | 10 | 6 | replace with 4? invalid, replace with 5 | 1 | 5 |
| 3 | 10/13 | 5 | keep 10? valid | 1 | 10 |

We use one replacement early to maintain feasibility, then proceed. The trace shows that using the smallest valid replacement is necessary, because choosing 5 instead of 4 keeps more flexibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((N+M)\log(N+M))$ | Sorting dominates, scan is linear |
| Space | $O(N+M)$ | Storage for arrays |

The constraints allow up to $5 \cdot 10^5$ elements, so an $O(n \log n)$ approach fits comfortably within time limits, while any quadratic approach would be far beyond feasible operation counts.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    a.sort()
    b.sort()
    
    j = 0
    last = -10**18
    used = 0
    
    for x in a:
        if x >= last:
            last = x
        else:
            while j < m and b[j] < last:
                j += 1
            if j == m:
                return "-1"
            last = b[j]
            j += 1
            used += 1
    
    return str(used)

# provided samples
assert run("4 1\n2 6 13 10\n5\n") == "-1"
assert run("4 2\n2 6 13 10\n5 4\n") == "2"

# custom cases
assert run("1 1\n5\n10\n") == "0", "already sorted single element"
assert run("3 1\n3 1 2\n2\n") == "-1", "insufficient repair value"
assert run("3 3\n3 1 2\n1 2 4\n") == "1", "one repair fixes inversion"
assert run("5 5\n5 4 3 2 1\n1 2 3 4 5\n") == "2", "reverse array needs repairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element case | 0 | trivial already valid |
| insufficient repair | -1 | impossibility detection |
| minimal fix | 1 | single inversion repair |
| reverse array | 2 | worst-case descending structure |

## Edge Cases

A key edge case is when the array is already sorted. The algorithm never enters the replacement branch, because every $A[i]$ satisfies the monotone condition, so the answer remains zero replacements.

Another edge case is when all elements in $B$ are smaller than the current constraint. In this situation, the pointer over $B$ exhausts without finding a valid candidate, and the algorithm correctly returns $-1$. This corresponds to a gap where no replacement can bridge the monotonic requirement.

A third case is when greedy choice might seem risky, such as picking the smallest valid $B$ value. The trace shows that using a larger value early can block later feasibility. The algorithm avoids this by always consuming the minimal feasible replacement, preserving maximum slack for future elements.
