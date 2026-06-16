---
title: "CF 1382A - Common Subsequence"
description: "We are given two integer arrays, and we want to construct a third array that can be obtained by deleting elements from both of them. In other words, we are looking for a sequence of values that appears in both arrays while preserving order in each."
date: "2026-06-16T13:58:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1382
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 658 (Div. 2)"
rating: 800
weight: 1382
solve_time_s: 401
verified: false
draft: false
---

[CF 1382A - Common Subsequence](https://codeforces.com/problemset/problem/1382/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 6m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two integer arrays, and we want to construct a third array that can be obtained by deleting elements from both of them. In other words, we are looking for a sequence of values that appears in both arrays while preserving order in each.

The goal is to output any such common subsequence, but with the strongest priority on minimizing its length. If no common subsequence exists, we must report that fact.

The key observation from the definition of subsequence is that any valid answer must consist only of values that appear in both arrays. However, this is not sufficient by itself because order matters. A value appearing in both arrays does not automatically guarantee it can form a subsequence of length greater than one with other values.

The constraints are small enough that both arrays together contain at most about two thousand elements across all tests. This immediately suggests that an $O(nm)$ comparison between arrays is safe, since even in the worst case we perform about one million operations per test suite in total, which is comfortably within limits.

The most subtle edge case arises from duplicates and ordering. A naive approach that simply collects all intersecting values without checking subsequence feasibility can easily fail. For example, consider:

```
a = [1, 2]
b = [2, 1]
```

The intersection is {1, 2}, but neither `[1, 2]` nor `[2, 1]` appears as a subsequence in both arrays. The correct answer must have length 1, and either `[1]` or `[2]` is valid. This shows that we cannot treat the problem as a set intersection.

Another failure mode is assuming we need to construct the longest common subsequence. That is unnecessary and far more complex; the problem only asks for the shortest non-empty common subsequence, which changes the structure completely.

## Approaches

A brute-force idea would be to enumerate all subsequences of the first array and check whether each appears in the second array. This is correct because it explicitly explores the search space of valid candidates. However, the number of subsequences is exponential, specifically $2^n$, so even for $n = 1000$ this becomes completely infeasible.

A more focused observation changes everything. The shortest possible common subsequence can only have length 1 or 2 in any meaningful situation, because if there exists any common element between the arrays, a single-element sequence is already optimal. There is no need to consider longer sequences unless forced by constraints, but here a length-1 solution is always better whenever possible.

So the real task becomes checking whether any value appears in both arrays. If such a value exists, we immediately output it. If not, there is no common subsequence at all.

This reduces the problem from combinatorial search to a simple frequency or membership test.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all subsequences) | $O(2^n \cdot m)$ | $O(1)$ | Too slow |
| Frequency / intersection check | $O(n + m)$ | $O(1000)$ | Accepted |

## Algorithm Walkthrough

We proceed test case by test case.

1. Build a frequency array or hash set for elements in the first array. This allows constant-time membership checks later.
2. Scan through the second array and check whether any element exists in the first array’s set. The first such element found immediately forms a valid answer of length 1.
3. If we find such an element, we output it and stop processing that test case. The reason we can stop immediately is that length 1 is the minimum possible for any non-empty sequence.
4. If we finish scanning without finding any common element, we output that no solution exists.

Why it works comes down to a minimality argument. Any valid common subsequence must contain at least one value that appears in both arrays. If such a value exists, the sequence consisting of only that value is already a valid subsequence of both arrays. Therefore, any longer sequence cannot improve optimality. If no value is shared, no non-empty common subsequence can exist at all.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    s = set(a)
    ans = None
    
    for x in b:
        if x in s:
            ans = x
            break
    
    if ans is None:
        print("NO")
    else:
        print("YES")
        print(1, ans)
```

The solution builds a set from the first array to support constant-time membership queries. It then scans the second array once and stops at the first shared value, ensuring minimal-length output.

A subtle point is that we do not need to consider ordering beyond membership. Since a single element has no ordering constraints, any occurrence in both arrays is sufficient. The early exit is also important for efficiency but not required for correctness.

## Worked Examples

### Example 1

```
a = [10, 8, 6, 4]
b = [1, 2, 3, 4, 5]
```

| Step | Current b element | In set(a)? | Answer |
| --- | --- | --- | --- |
| 1 | 1 | No | None |
| 2 | 2 | No | None |
| 3 | 3 | No | None |
| 4 | 4 | Yes | 4 |

We stop immediately when we encounter 4 in the second array because it is present in the first array. This confirms that a length-1 solution is always preferred when available.

### Example 2

```
a = [3]
b = [2]
```

| Step | Current b element | In set(a)? | Answer |
| --- | --- | --- | --- |
| 1 | 2 | No | None |

We finish scanning without finding any match, so no common subsequence exists. This demonstrates the case where the answer must be “NO”.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Each array is processed once, with constant-time set lookups |
| Space | $O(n)$ | Storage of elements of the first array in a hash set |

The total size across all test cases is small, so this linear solution easily fits within both time and memory limits even under worst-case input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        s = set(a)
        ans = None
        for x in b:
            if x in s:
                ans = x
                break
        
        if ans is None:
            out.append("NO")
        else:
            out.append("YES")
            out.append(f"1 {ans}")
    
    return "\n".join(out)

# sample 1
assert run("""5
4 5
10 8 6 4
1 2 3 4 5
1 1
3
3
1 1
3
2
5 3
1000 2 2 2 3
3 1 5
5 5
1 2 3 4 5
1 2 3 4 5
""") == """YES
1 4
YES
1 3
NO
YES
1 3
YES
1 2"""

# all disjoint
assert run("""1
3 3
1 2 3
4 5 6
""") == "NO"

# single overlap
assert run("""1
3 3
1 2 3
3 4 5
""") == "YES\n1 3"

# all same
assert run("""1
4 4
7 7 7 7
7 7 7 7
""") == "YES\n1 7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| disjoint arrays | NO | no common element case |
| single overlap | YES 1 x | basic positive case |
| identical arrays | YES 1 x | duplicates do not matter |

## Edge Cases

A critical edge case is when arrays contain repeated values but no shared distinct structure is needed.

For example:

```
a = [5, 5, 5]
b = [5]
```

The algorithm inserts 5 into the set from the first array. While scanning the second array, it immediately finds 5 and returns `[5]`. Even though multiplicity differs, subsequence validity only depends on existence, not frequency.

Another case is reversed ordering:

```
a = [1, 2]
b = [2, 1]
```

The scan finds either 2 or 1 depending on traversal order of `b`, but both are valid answers. This confirms that the algorithm does not rely on alignment or positional matching, only membership, which is sufficient because the output is constrained to length 1.
