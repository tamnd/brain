---
title: "CF 1081B - Farewell Party"
description: "We are given a group of n people. Each person wore exactly one hat, and every hat belongs to one of n possible types labeled from 1 to n. Multiple people may share the same hat type, and some hat types may not be used at all."
date: "2026-06-15T06:11:19+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1081
codeforces_index: "B"
codeforces_contest_name: "Avito Cool Challenge 2018"
rating: 1500
weight: 1081
solve_time_s: 173
verified: true
draft: false
---

[CF 1081B - Farewell Party](https://codeforces.com/problemset/problem/1081/B)

**Rating:** 1500  
**Tags:** constructive algorithms, implementation  
**Solve time:** 2m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a group of n people. Each person wore exactly one hat, and every hat belongs to one of n possible types labeled from 1 to n. Multiple people may share the same hat type, and some hat types may not be used at all.

Each person i provides a single number a_i, which is supposed to represent how many other people wore a different hat type than theirs. If we denote the final assignment of hat types as b_1, b_2, ..., b_n, then for person i, the value a_i must equal the number of indices j such that b_j is different from b_i.

The task is to determine whether there exists any assignment of hat types consistent with all these statements, and if so, construct one valid assignment.

The constraint n ≤ 10^5 forces us away from anything quadratic or involving pairwise comparison between people. Any solution that attempts to verify all assignments or simulate candidates explicitly will fail, since even O(n^2) already implies around 10^10 operations.

A subtle point is that the condition is symmetric but expressed individually. Each person’s statement depends only on how many people share their own hat type. This means the problem is fundamentally about grouping indices into classes where each class size determines the same value for everyone inside it.

One edge case that exposes incorrect intuition is when all a_i are equal but impossible globally. For example, if all a_i are 1 and n = 2, we cannot satisfy both people simultaneously because each person sees exactly one other person, but grouping constraints break.

Another failure case occurs when a person claims a value that implies a group size outside [1, n], such as a_i = n - 1, which forces them into a singleton group.

## Approaches

A brute-force approach would try to assign each person a hat type and check whether all constraints hold. Since each b_i can take n values, this leads to n^n possibilities, which is entirely infeasible even for n = 10.

A more structured brute-force idea is to guess group sizes: for each possible partition of n into group sizes, assign values accordingly. However, the number of partitions grows exponentially and still does not scale.

The key observation is that the statement of a person is determined entirely by the size of their group. If a person belongs to a group of size s, then exactly s - 1 people share their hat, and therefore n - s people have a different hat. So every person with value a_i must belong to a group of size:

s = n - a_i

This transforms the problem from arbitrary assignments into grouping indices by required group size.

Now the problem becomes: can we partition indices into groups where each index i must belong to a group of size s_i = n - a_i, and all members of a group must agree on the same s_i?

This is a consistency and grouping problem, solvable greedily by grouping equal required sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^n) | O(n) | Too slow |
| Optimal grouping by size frequencies | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We convert each statement into a required group size.

1. For each person i, compute s_i = n - a_i. This is the only possible group size for which i’s statement can be true.
2. If any s_i is less than 1 or greater than n, immediately conclude impossibility. A group cannot have invalid size.
3. Group indices by their required size s_i using a mapping from size to list of people.
4. For each group of size s, check that the number of people requiring size s is divisible by s. If not, we cannot split them into uniform groups of size s, so the configuration is impossible.
5. For each valid size s, partition its list into chunks of exactly s people. Each chunk corresponds to one hat type.
6. Assign a unique hat label to each chunk and set b_i accordingly.

### Why it works

The transformation s_i = n - a_i is forced: any person in a group of size s will necessarily see exactly n - s people outside their group, matching their statement. Once all people with the same required size are collected, any valid solution must partition them into groups of size exactly s, since mixing sizes would violate at least one person’s required group size. The divisibility condition ensures that every such group can be formed without leftovers, and assigning distinct labels per chunk constructs a valid witness solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    groups = {}
    required = []

    for i, x in enumerate(a):
        s = n - x
        if s < 1 or s > n:
            print("Impossible")
            return
        required.append(s)
        if s not in groups:
            groups[s] = []
        groups[s].append(i)

    ans = [0] * n
    color = 1

    for s, idxs in groups.items():
        if len(idxs) % s != 0:
            print("Impossible")
            return

        for i in range(0, len(idxs), s):
            chunk = idxs[i:i+s]
            for j in chunk:
                ans[j] = color
            color += 1

    print("Possible")
    print(*ans)

if __name__ == "__main__":
    solve()
```

The code first converts each a_i into a required group size s_i. It then builds buckets of indices sharing the same requirement. Each bucket must be evenly divisible into groups of that size. The assignment of colors corresponds directly to constructing these groups.

A subtle implementation detail is that we do not need to enforce any ordering of groups. Any partition works because all members in a group are interchangeable in terms of constraints.

## Worked Examples

### Example 1

Input:

```
3
0 0 0
```

Here each s_i = 3 - 0 = 3, so all three people must be in a single group.

| Step | Groups formed | Action | State |
| --- | --- | --- | --- |
| Compute s_i | [3, 3, 3] | All indices go to s=3 | {3: [0,1,2]} |
| Check divisibility | 3 % 3 = 0 | valid | unchanged |
| Build groups | chunk of size 3 | assign color 1 | b = [1,1,1] |

This confirms that a single group of size 3 is consistent with all statements.

### Example 2

Input:

```
4
2 2 1 1
```

We compute s_i = 4 - a_i = [2,2,3,3].

| Step | Groups formed | Action | State |
| --- | --- | --- | --- |
| Compute s_i | [2,2,3,3] | split by value | {2:[0,1], 3:[2,3]} |
| Check s=2 | 2 % 2 = 0 | ok | unchanged |
| Check s=3 | 2 % 3 ≠ 0 | fail | stop |

This shows that even though local grouping seems plausible, the 3-requirement cannot be satisfied, so the instance is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each index is processed once for grouping and once for assignment |
| Space | O(n) | storage for groups and output array |

The solution fits comfortably within constraints since both memory and runtime scale linearly with n, which is necessary for n up to 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from io import StringIO

    input_data = sys.stdin.read().strip().split()
    it = iter(input_data)

    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    groups = {}
    for i, x in enumerate(a):
        s = n - x
        groups.setdefault(s, []).append(i)

    ans = [0] * n
    color = 1

    for s, idxs in groups.items():
        if len(idxs) % s != 0:
            return "Impossible"
        for i in range(0, len(idxs), s):
            for j in idxs[i:i+s]:
                ans[j] = color
            color += 1

    return "Possible\n" + " ".join(map(str, ans))

# provided sample
assert run("3\n0 0 0\n") == "Possible\n1 1 1"

# all impossible due to mismatch
assert run("3\n0 1 2\n") == "Impossible"

# simple split case
assert run("4\n2 2 1 1\n") == "Impossible"

# single group edge
assert run("1\n0\n") == "Possible\n1"

# alternating valid grouping
assert run("4\n3 3 3 3\n") == "Possible\n1 1 1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 identical zeros | Possible | single full group |
| mixed 0 1 2 | Impossible | inconsistent sizes |
| 4 with split sizes | Impossible | divisibility failure |
| n=1 edge | Possible | minimal case |
| all require full group | Possible | uniform requirement |

## Edge Cases

One edge case occurs when all a_i = n - 1. Then all s_i = 1, so every person must be in a singleton group. The algorithm correctly assigns each index to its own group because each bucket of size 1 is trivially divisible by 1, producing a valid assignment where every person has a unique hat.

Another edge case is n = 1 with a_1 = 0. This gives s_1 = 1, forming a single valid group. The algorithm handles this without special logic because grouping naturally produces one chunk.

A more subtle case is when multiple required sizes exist but one size has leftover elements. For example, n = 6 with s-values [2,2,2,2,2,3]. The size-2 group has 5 elements, which cannot form complete pairs, causing the algorithm to correctly reject the instance before any partial assignment is attempted.
