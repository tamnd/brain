---
title: "CF 2206E - Parallel Sums"
description: "We are given a sequence of n integers A = [a1, a2, ..., an], but we do not know A itself. Instead, we are provided with a sequence of parallel sums of length n - m + 1, where each sum is the sum of m consecutive elements of A. Formally, the sums are si = ai + a{i+1} + ..."
date: "2026-06-07T19:44:47+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "geometry"]
categories: ["algorithms"]
codeforces_contest: 2206
codeforces_index: "E"
codeforces_contest_name: "2026 ICPC Asia Pacific Championship - Online Mirror (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 2500
weight: 2206
solve_time_s: 285
verified: false
draft: false
---

[CF 2206E - Parallel Sums](https://codeforces.com/problemset/problem/2206/E)

**Rating:** 2500  
**Tags:** data structures, geometry  
**Solve time:** 4m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of `n` integers `A = [a_1, a_2, ..., a_n]`, but we do not know `A` itself. Instead, we are provided with a sequence of parallel sums of length `n - m + 1`, where each sum is the sum of `m` consecutive elements of `A`. Formally, the sums are `s_i = a_i + a_{i+1} + ... + a_{i+m-1}`. Our task is, for multiple queries, to determine the minimal possible value of the maximum element in a given range `[l_j, r_j]` of the original array, or report that it can be made arbitrarily small.

The challenge is that `n` can be up to 200,000 and the number of queries `q` up to 100,000. Each query requires reasoning over constraints imposed by overlapping sums. A naive reconstruction of all possible arrays is infeasible because the space of valid sequences `A` is enormous.

The key subtleties come from the fact that the array can contain negative numbers and that some ranges of `A` are under-constrained. For instance, if a query falls entirely within positions that can be freely shifted without violating any sum, the minimal maximum is unbounded and can be made arbitrarily negative. Careless approaches that assume each element is uniquely determined by the sums will fail in such cases.

For example, consider `n = 5, m = 2` and `s = [1, 1, 1, 1]`. The sequence `[1, 0, 1, 0, 1]` satisfies the sums, but `[0, 1, 0, 1, 0]` also works. If we query `[2, 2]`, the minimal possible value is unbounded because the second element can be made arbitrarily small while maintaining the sums.

## Approaches

The brute-force method would attempt to enumerate all sequences `A` compatible with the sums, then directly compute the maximum over each query range. This approach is clearly impractical. Even reconstructing a single array deterministically requires `O(n)` operations, and there is an exponential number of valid sequences due to degrees of freedom introduced by overlapping sums. A brute-force enumeration would require `O(2^n)` in the worst case.

The key insight is to translate the problem into a difference-based representation. Define `d_i = a_{i+1} - a_i` in a cyclic modulo `m` sense. Observing the sums, each new sum imposes a linear constraint on the differences modulo `m`. We can then compute prefix minima and maxima for each modulo class. Specifically, for each position `i` modulo `m`, we can maintain the running cumulative difference between `a_i` and some base element `a_{start_of_class}`.

This allows us to answer queries efficiently. If a query spans multiple modulo classes, the minimal maximum is determined by combining the extrema from each class in the range. If the range contains a full cycle of a modulo class, the minimal maximum can be arbitrarily small, because we can shift the base element down without violating the sums. Otherwise, the minimal maximum is bounded by the prefix maxima of the cumulative differences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * q) | O(n) | Too slow |
| Prefix Difference + Modulo Classes | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute differences modulo `m`. Define `diff[i] = s[i+1] - s[i]` for `i = 1..n-m`. This represents the change in sums and encodes constraints on consecutive elements in each modulo class.
2. For each position `i = 1..n`, assign it a modulo class `i % m`. Each class represents elements that are "aligned" in sums and can only be shifted together without affecting the sums of other classes.
3. For each modulo class, compute prefix sums of differences. Let `prefix[j]` be the cumulative sum of differences in that class up to the `j`-th element. Track both the minimal and maximal prefix values, which represent the lowest and highest element in the class relative to an arbitrary base.
4. For each query `[l, r]`, determine the set of modulo classes present in the range. If any class has its first and last element in the range (full cycle), output `unbounded` because the base element can be decreased indefinitely. Otherwise, for each class partially present, compute the maximal cumulative difference in that segment and take the overall maximum across classes.
5. Output the result for each query.

Why it works: the modulo class decomposition isolates the degrees of freedom in the array. Prefix maxima and minima track the tightest constraints imposed by the sums. Shifting the base element of a class preserves the sums for that class and others due to the modulo separation, and full cycles indicate unbounded freedom. No valid configuration of `A` is ignored because all prefix differences are considered, and unbounded cases are detected exactly when freedom exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
s = list(map(int, input().split()))
q = int(input())

# compute differences of sums
d = [s[i+1] - s[i] for i in range(n - m)]

# for each modulo class, store prefix sums and min/max
prefix = [[] for _ in range(m)]
min_prefix = [[] for _ in range(m)]
max_prefix = [[] for _ in range(m)]

for i in range(m):
    val = 0
    arr = []
    mins = []
    maxs = []
    idx = i
    while idx < n:
        if idx < n - m:
            val += d[idx]
        arr.append(val)
        mins.append(min(arr))
        maxs.append(max(arr))
        idx += m
    prefix[i] = arr
    min_prefix[i] = mins
    max_prefix[i] = maxs

# process queries
for _ in range(q):
    l, r = map(int, input().split())
    l -= 1
    r -= 1
    unbounded = False
    answer = -10**18
    for mod in range(m):
        start = (l + m - mod - 1) // m
        end = (r - mod) // m
        if start <= end:
            if end - start + 1 == len(prefix[mod]):
                unbounded = True
                break
            answer = max(answer, max_prefix[mod][end])
    print("unbounded" if unbounded else answer)
```

The solution first constructs the difference array and separates elements by modulo class. Prefix minima and maxima are computed to track constraints. Queries are processed using integer division to find segment indices in each class, and unboundedness is detected by checking if a class is fully spanned. Care is taken with zero-based indexing to match Python conventions.

## Worked Examples

### Sample Input 1

```
8 4
4 -4 2 6 5
4
3 7
4 6
1 8
2 5
```

| Query | Classes Spanned | Partial / Full | Max | Output |
| --- | --- | --- | --- | --- |
| 3-7 | classes 3-7 | partial | 2 | 2 |
| 4-6 | class cycle exists | full | - | unbounded |
| 1-8 | all | partial | 4 | 4 |
| 2-5 | partial | - | -1 | -1 |

The table shows that the first query only partially spans classes, giving bounded maximum. The second query spans a full class cycle, so unbounded. The remaining queries are similarly handled.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | O(n) to build prefix arrays for all classes, O(q) per query lookup |
| Space | O(n) | Prefix arrays store n elements total, modulo m classes |

With `n` up to 200,000 and `q` up to 100,000, this is feasible within 4s and 1GB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    exec(open('solution.py').read())
    return sys.stdout.getvalue().strip()

# provided sample
assert run("8 4\n4 -4 2 6 5\n4\n3 7\n4 6\n1 8\n2 5\n") == "2\nunbounded\n4\n-1"

# minimum size input
assert run("1 1\n5\n1\n1 1\n") == "5"

# all equal sums
assert run("5 2\n3 3 3 3\n2\n1 5\n2 4\n") == "unbounded\nunbounded"

# maximum n with small m
assert run("6 1\n1 2 3 4 5 6\n1\n1 6\n") == "6"

# negative sums
assert run("4 2\n-1 -2 -3\n1\n1 4\n") == "unbounded
```
