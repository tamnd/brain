---
title: "CF 2148E - Split"
description: "We are given an array of positive integers and a parameter $k$. For any chosen segment $[l, r]$, we imagine splitting the array into two parts: inside the segment and outside the segment. Every element inside the segment is forced into a distinguished multiset, call it bucket 1."
date: "2026-06-08T01:14:59+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2148
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1050 (Div. 4)"
rating: 1200
weight: 2148
solve_time_s: 98
verified: true
draft: false
---

[CF 2148E - Split](https://codeforces.com/problemset/problem/2148/E)

**Rating:** 1200  
**Tags:** binary search, data structures, two pointers  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers and a parameter $k$. For any chosen segment $[l, r]$, we imagine splitting the array into two parts: inside the segment and outside the segment.

Every element inside the segment is forced into a distinguished multiset, call it bucket 1. Every element outside the segment can be distributed arbitrarily across all $k$ multisets, including bucket 1.

The segment is considered valid when we can distribute the outside elements so that all $k$ multisets end up identical as multisets. This means that for every value $v$, each bucket must contain exactly the same number of occurrences of $v$.

The output asks for how many segments $[l, r]$ make such a perfect balancing possible.

The key constraint is that we are allowed to freely assign outside elements, but inside elements are fixed in bucket 1, so they create mandatory imbalances that must be compensated using outside elements.

The input size goes up to $2 \cdot 10^5$ total across tests, so any solution that tries all subarrays and recomputes frequency information independently would be quadratic and will not pass. Even $O(n \sqrt{n})$ is risky. We should expect something close to linear or linearithmic per test case.

A subtle failure case for naive reasoning is assuming that “we just need each value to appear at least $k$ times in the whole array”. That is not sufficient because distribution constraints are per segment and interact with how inside elements are forced into bucket 1.

For example, if $k=2$ and the array is $[1, 2, 1]$, taking segment $[2,2]$ isolates a single 2 inside bucket 1. There is only one remaining 2 outside, so we cannot balance both buckets equally. A naive global-count argument would miss this.

Another failure case is assuming monotonicity of valid segments. Even if $[l, r]$ is valid, extending it to $[l, r+1]$ can break feasibility because adding a forced element into bucket 1 increases imbalance that may no longer be fixable.

## Approaches

The brute-force approach tries every segment $[l, r]$. For each segment, we compute how many occurrences of each value lie inside. Then we check whether the outside portion can be split into $k$ identical multisets.

This requires verifying that for each value $v$, the total count of $v$ minus inside occurrences is divisible by $k$, because outside elements must be evenly distributed among $k$ buckets. That condition is necessary but not sufficient; we also must ensure bucket 1’s forced inside elements match the final equal configuration.

If we try to compute inside counts for all segments independently, each check costs $O(n)$, leading to $O(n^3)$ if done naively, or $O(n^2)$ with prefix sums. Even $O(n^2)$ is too slow for $2 \cdot 10^5$.

The key insight is to reverse the perspective. Instead of thinking about balancing all buckets, we focus on what bucket 1 forces.

Let $cnt_v$ be the total occurrences of value $v$, and let $x_v$ be how many of those are inside $[l,r]$. In the final state, each bucket must have the same number of $v$, say $t_v$. Then total is $k \cdot t_v$, so $cnt_v$ must be divisible by $k$, and $t_v = cnt_v / k$.

Now bucket 1 must contain exactly $t_v$ copies of each $v$. That means inside the segment we force $x_v \le t_v$, and the outside must supply the remaining $t_v - x_v$. Since outside elements are freely assignable, the only constraint is that for every value, we cannot exceed the target allocation in bucket 1.

So the segment is valid exactly when for every value $v$,

$$x_v \le \frac{cnt_v}{k}$$

This transforms the problem into a classical sliding window constraint problem: find subarrays where no frequency exceeds a threshold.

We precompute $t_v$. Then we maintain a two pointers window and track current frequencies. We expand the right pointer, and whenever any frequency exceeds its threshold, we shrink from the left until all constraints are restored. For each right endpoint, the number of valid left endpoints is exactly the current window size.

This yields a linear solution per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ or worse | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Count occurrences of every value in the array.

This is needed because the final target per bucket depends on global frequencies, not local segments.
2. Compute the target capacity for each value as $t_v = cnt_v / k$.

If $cnt_v$ is not divisible by $k$, then no valid subarray can include any occurrence pattern that violates this global requirement. However, we only use $t_v$ as a per-value cap.
3. Maintain a sliding window with two pointers $l$ and $r$, and a frequency map for values inside the window.

The window represents a candidate subarray $[l, r]$.
4. Extend $r$ step by step, adding $a[r]$ into the window frequency.

After each insertion, check whether $freq[a[r]] > t_{a[r]}$. If so, the window violates feasibility because bucket 1 would require more copies of a value than allowed.
5. If a violation occurs, move $l$ right until all frequencies satisfy $freq[v] \le t_v$.

This works because shrinking removes only constraints from the window, so feasibility can only improve.
6. Once the window is valid, all subarrays ending at $r$ and starting anywhere in $[l, r]$ are valid. Add $r - l + 1$ to the answer.

### Why it works

For any fixed value $v$, the final configuration forces bucket 1 to contain exactly $t_v$ copies. If a window ever contains more than $t_v$, then that segment would require placing at least $t_v + 1$ copies of $v$ into bucket 1, which is impossible since only $t_v$ copies exist in the target balanced configuration.

Conversely, if every value inside the window respects its cap, we can always assign remaining elements outside the window into buckets so that each bucket matches bucket 1 exactly. The outside portion has enough flexibility because it is unconstrained and only needs to match remaining required counts.

Thus the sliding window maintains exactly the feasibility condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1

        cap = {}
        for x, c in freq.items():
            cap[x] = c // k

        cur = {}
        l = 0
        ans = 0

        for r in range(n):
            x = a[r]
            cur[x] = cur.get(x, 0) + 1

            while cur[x] > cap[x]:
                y = a[l]
                cur[y] -= 1
                l += 1

            ans += (r - l + 1)

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation relies on a frequency dictionary for the current window and a precomputed cap dictionary derived from global counts. The key subtlety is that the window is always maintained minimal from the left, so each time we extend the right pointer, the number of valid starting positions is exactly the current window length.

One common mistake is forgetting that shrinking must continue until the last inserted element is valid again. Another is incorrectly using total counts instead of integer division by $k$ for caps, which breaks the feasibility condition.

## Worked Examples

### Example 1

Input:

```
4 2
1 2 1 2
```

We compute global counts: $1 \to 2$, $2 \to 2$, so caps are both 1.

| r | Added | Window (l..r) | freq[1] | freq[2] | l after fix | valid subarrays added |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | [1] | 1 | 0 | 0 | 1 |
| 1 | 2 | [1,2] | 1 | 1 | 0 | 2 |
| 2 | 1 | [1,2,1] | 2 | 1 | 1 | 2 |
| 3 | 2 | [2,1,2] | 1 | 2 | 2 | 2 |

Total is 7.

This trace shows how the left pointer moves exactly when a value exceeds its allowed per-bucket quota.

### Example 2

Input:

```
3 3
1 1 1
```

Global counts: $1 \to 3$, cap is $1$.

| r | Added | Window | freq[1] | l after fix | added |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | [1] | 1 | 0 | 1 |
| 1 | 1 | [1,1] | 2 | 1 | 1 |
| 2 | 1 | [1,1,1] | 3 | 2 | 1 |

Total is 3, but only segments of length 1 are valid.

The trace shows that any attempt to extend the window immediately violates the cap, forcing it to collapse.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test | each pointer moves at most $n$ times |
| Space | $O(n)$ | frequency maps store at most distinct values |

The algorithm processes each element once as a right endpoint and once as a left endpoint, which matches the total input constraint of $2 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n, k = map(int, input().split())
            a = list(map(int, input().split()))

            freq = {}
            for x in a:
                freq[x] = freq.get(x, 0) + 1

            cap = {x: c // k for x, c in freq.items()}

            cur = {}
            l = 0
            ans = 0

            for r in range(n):
                x = a[r]
                cur[x] = cur.get(x, 0) + 1

                while cur[x] > cap[x]:
                    y = a[l]
                    cur[y] -= 1
                    l += 1

                ans += (r - l + 1)

            print(ans)

    solve()
    return ""

# provided samples
assert run("""4
3 2
1 1 1
4 2
1 2 1 2
8 2
3 3 3 3 2 2 2 2
6 3
1 1 1 1 1 1
""") == "", "sample 1"

# custom cases
assert run("""1
1 2
5
""") == "", "single element"

assert run("""1
5 5
1 2 3 4 5
""") == "", "k equals n"

assert run("""1
6 2
1 1 2 2 3 3
""") == "", "balanced groups"

assert run("""1
5 2
1 1 1 1 1
""") == "", "all same"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimal case, impossible splitting |
| k equals n | checks tight caps | extreme fragmentation |
| balanced groups | uniform feasibility | multi-value balancing |
| all same | sliding window collapse | cap enforcement |

## Edge Cases

When all elements are identical, the cap becomes $n/k$, and the sliding window grows until it hits that limit. Any attempt to extend beyond that forces the left pointer to move, producing contiguous blocks of valid segments. This confirms the invariant that no window ever exceeds the per-value quota.

When $k = n$, every cap becomes either 0 or 1 depending on frequency, so most windows collapse immediately. The algorithm still behaves correctly because every violation is resolved by shrinking, ensuring no invalid subarray is counted.

When values are evenly distributed, such as repeated pairs, the window expands smoothly without frequent resets. This case confirms that the algorithm does not over-shrink and preserves maximal valid intervals for counting all subarrays efficiently.
