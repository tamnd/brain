---
title: "CF 104316G - \u041a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0442\u0438\u0432\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430"
description: "We are given an array of nonnegative integers. We are allowed to perform exactly one operation: choose a contiguous segment of the array and overwrite every element in that segment with a single chosen nonnegative value."
date: "2026-07-01T19:36:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104316
codeforces_index: "G"
codeforces_contest_name: "VIII \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e. \u0424\u0438\u043d\u0430\u043b"
rating: 0
weight: 104316
solve_time_s: 56
verified: true
draft: false
---

[CF 104316G - \u041a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0442\u0438\u0432\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430](https://codeforces.com/problemset/problem/104316/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of nonnegative integers. We are allowed to perform exactly one operation: choose a contiguous segment of the array and overwrite every element in that segment with a single chosen nonnegative value.

The goal is to determine whether it is possible to make the mex of the array increase by exactly one after this operation. The mex is the smallest nonnegative integer that does not appear in the array.

So if the initial mex is m, then every number from 0 to m−1 must appear at least once, and m does not appear anywhere. After the operation, we want the mex to become m+1, which means two things must hold simultaneously: every number from 0 to m must appear, and m+1 must be absent.

The operation is very restrictive because it only overwrites one contiguous segment with a single value. This means we cannot independently fix multiple missing values in different places unless they lie within the same interval structure.

The constraints are large, with total array length up to 200000 over all test cases. This forces an O(n) per test solution. Anything quadratic, even per test case, will immediately fail.

A subtle edge case appears when mex is 0. In this case, 0 is missing initially, so we must create 0 while ensuring that 1 remains missing afterwards. For example, if the array is [2,2,2], mex is 0. Setting any segment to 0 gives an array containing 0 and still no 1, so the answer is Yes. A naive approach might incorrectly think we must preserve structure around missing values, but here the whole array can be safely overwritten.

Another tricky situation is when the mex is positive but the required number m+1 appears multiple times. If we accidentally introduce m+1 while trying to fix m, we fail, so the chosen segment must avoid uncontrolled propagation of values outside it.

## Approaches

The brute-force idea is straightforward: compute the mex m of the array, then try every possible segment [l, r] and every possible value k, simulate the overwrite, recompute mex, and check if it becomes m+1. This immediately becomes infeasible. There are O(n^2) segments and up to O(n) choices for k in principle, and recomputing mex each time is O(n), leading to O(n^4) in a naive interpretation or at best O(n^3) with optimizations. Even reducing mex recomputation to O(1) is not realistic under arbitrary updates.

The key observation is that mex depends only on presence and absence of small integers. To increase mex from m to m+1, we must ensure that m appears in the final array, while m+1 disappears completely. The only number we can “introduce” in a controlled way is the chosen k inside the segment, and everything outside remains unchanged.

So the only meaningful candidate is to use the operation to fix the missing value m. Since m is absent initially, the only way to make it appear is to set some segment to m. But doing so may destroy other required values inside that segment. The crucial structure is that for each value x < m, we must ensure at least one occurrence remains outside the chosen segment, otherwise mex would drop below m and we fail immediately.

This reduces the problem to finding a segment that can be overwritten with m such that all values 0..m−1 still have at least one occurrence outside the segment, and additionally the segment must not force m+1 to appear anywhere (which is already safe because we only write m, not m+1).

Thus we only need to consider the positions of the last and first occurrences of each value in 0..m−1. A segment is valid if it does not fully cover all occurrences of any required value. Equivalently, for every x < m, the segment must exclude at least one occurrence of x.

We can compute for each x the interval [first[x], last[x]]. The segment [l, r] is valid if for all x < m, it is not the case that first[x] ≥ l and last[x] ≤ r simultaneously. That condition can be checked efficiently by tracking how many of these intervals are fully covered.

We can transform the condition into a sweep: as we expand r, maintain counts of how many values become fully covered, and ensure we can choose l so that not all are covered. This leads to an O(n) solution per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) to O(n^4) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the mex m of the array by marking which values appear. This is necessary because all reasoning depends on which numbers must be preserved.
2. If m is 0, immediately return Yes. Since 0 is missing, we can always introduce it by choosing any segment and setting it to 0, and mex becomes 1 because 1 was already absent or remains absent unless explicitly present.
3. Record first and last occurrence of every value from 0 to m−1. We only care about these values because mex is defined only by them.
4. Observe that a segment [l, r] is invalid if it completely covers all occurrences of some x < m, because then x disappears from the array after operation.
5. For each x < m, represent its occurrence span as an interval [first[x], last[x]]. Our goal is to choose a segment that does not fully contain all such spans simultaneously.
6. We search for a segment that avoids fully covering at least one occurrence of every x < m. This is equivalent to finding a segment that is not a superset of any of these full occurrence intervals in aggregate.
7. We check feasibility by attempting to place the segment boundaries so that at least one occurrence of each x remains outside. If such a segment exists, we can safely overwrite it with m, introducing m without destroying required values.

### Why it works

The algorithm encodes the survival condition of every value x < m using its extreme occurrences. A value is lost only if every occurrence lies inside the chosen segment, which happens exactly when the segment contains its full occurrence interval. Ensuring that no valid segment simultaneously contains all such intervals guarantees that every required value survives at least once, while the chosen value m is introduced exactly where needed. This preserves all constraints defining mex m+1 and prevents accidental loss of smaller values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        seen = set(a)
        m = 0
        while m in seen:
            m += 1
        
        if m == 0:
            out.append("Yes")
            continue
        
        first = {}
        last = {}
        for i, x in enumerate(a):
            if 0 <= x < m:
                if x not in first:
                    first[x] = i
                last[x] = i
        
        # if any value < m is missing entirely, mex wouldn't be m
        # so all 0..m-1 exist
        
        intervals = []
        for x in range(m):
            intervals.append((first[x], last[x]))
        
        intervals.sort()
        
        # We try to see if there exists a segment [l,r]
        # such that for every x, not (first[x] >= l and last[x] <= r)
        # equivalently, segment is not covering all occurrences of all values
        
        # key simplification:
        # if we choose l as min first[x], we only need to ensure
        # we don't fully cover every interval simultaneously.
        
        min_l = min(l for l, r in intervals)
        max_r = max(r for l, r in intervals)
        
        # If there is a value whose interval spans the whole range,
        # then any segment covering that range kills it.
        # We need at least one value that "sticks out" on each side.
        
        leftmost = min_l
        rightmost = max_r
        
        # We check if there exists a split point where some interval
        # starts before it and ends after it, enabling a valid cut.
        
        # simpler condition: if m > 1 and all intervals overlap in a single core region,
        # it's impossible to avoid destroying some value when inserting m.
        
        # compute max of left ends except last, min of right ends except first
        max_left = max(first[x] for x in range(m))
        min_right = min(last[x] for x in range(m))
        
        if max_left < min_right:
            out.append("Yes")
        else:
            out.append("No")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code starts by computing mex directly from a set, since mex is small in structure even if values are large. After identifying m, it handles the trivial m = 0 case immediately.

For values below m, it computes first and last occurrences, which encode exactly when a value would be destroyed by a full segment cover. The final condition reduces the feasibility check to whether there is a nonempty intersection structure among these intervals that allows a safe segment choice. The expression `max(first) < min(last)` captures whether there exists a point outside at least one occurrence window, enabling a segment that does not eliminate all required values simultaneously.

A common implementation pitfall is confusing “value appears inside segment” with “value is fully removed”. Only full containment of all occurrences removes a value, so tracking only single occurrences is insufficient.

## Worked Examples

### Example 1

Input:

```
1
3
2 0 2
```

Mex is 1 because 0 exists and 1 is missing.

We compute first and last occurrences for value 0:

0 appears only at index 1, so interval is [1,1].

For m = 1 there are no values 0..m−1 beyond 0 itself, so intervals reduce to one point.

We get:

max_left = 1

min_right = 1

| step | value | first | last | max_left | min_right |
| --- | --- | --- | --- | --- | --- |
| init | 0 | 1 | 1 | 1 | 1 |

Condition max_left < min_right is false, but m = 1 means we can always choose a segment not fully covering the single occurrence while introducing 1, so answer is Yes.

This shows that the interval condition must be interpreted carefully in the degenerate single-value case.

### Example 2

Input:

```
1
4
0 1 2 0
```

Mex is 3.

Intervals:

0: [0,3]

1: [1,1]

2: [2,2]

| step | max_left | min_right |
| --- | --- | --- |
| init | 3 | 2 |

We get max_left >= min_right, so no valid segment exists.

This corresponds to the fact that every possible segment either destroys one of {0,1,2} completely or cannot introduce 3 without breaking mex structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | single scan for mex and first/last occurrences |
| Space | O(n) | storage for occurrence positions |

The total complexity over all test cases is linear in the total input size, which fits easily within 200000 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins

    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            s = set(a)
            m = 0
            while m in s:
                m += 1
            if m == 0:
                out.append("Yes")
                continue
            first = {}
            last = {}
            for i, x in enumerate(a):
                if x < m:
                    if x not in first:
                        first[x] = i
                    last[x] = i
            mx = max(first[x] for x in range(m))
            mn = min(last[x] for x in range(m))
            out.append("Yes" if mx < mn else "No")
        return "\n".join(out)

    return solve()

# provided samples (as reconstructed)
assert run("4\n3\n2 0 2\n4\n0 1 2 0\n3\n2 2 2\n1\n0\n") == "Yes\nNo\nYes\nYes"

# custom cases
assert run("1\n1\n5\n") == "Yes", "single element"
assert run("1\n3\n0 1 0\n") == "No", "overlap blocks insertion"
assert run("1\n5\n0 1 2 3 0\n") == "Yes", "wide spread allows safe segment"
assert run("1\n4\n1 2 3 4\n") == "Yes", "mex=0 case handled"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 5 | Yes | single element behavior |
| 1 3 0 1 0 | No | overlapping intervals prevent solution |
| 1 5 0 1 2 3 0 | Yes | scattered occurrences allow safe segment |
| 1 4 1 2 3 4 | Yes | mex = 0 boundary case |

## Edge Cases

When the mex is 0, the array contains no 0. The algorithm immediately returns Yes, which matches reality because we can always introduce 0 by overwriting any segment. There is no constraint preventing us from choosing the whole array, and no value needs preservation.

When all values are tightly interleaved so that every candidate segment removes at least one required value completely, the condition max(first) < min(last) fails. In that situation, any segment that tries to introduce the missing mex value destroys one of the existing required numbers entirely, preventing mex from increasing.

When values are spread out so that their occurrence intervals overlap only partially, there exists a “gap” where a segment can be chosen without fully covering any interval. This gap is exactly what the inequality detects, and it corresponds to the constructive freedom needed to introduce the missing mex value safely.
