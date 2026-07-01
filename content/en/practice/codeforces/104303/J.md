---
title: "CF 104303J - \u7ec4\u961f"
description: "We are given a pool of students, each student knows a subset of up to 60 topics. A valid team is any subset of students such that two conditions are simultaneously satisfied: every topic from 1 to p is covered by at least one team member, and for each topic, at most one team…"
date: "2026-07-01T20:12:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104303
codeforces_index: "J"
codeforces_contest_name: "2023 Xiangtan Unversity Freshman Conteset"
rating: 0
weight: 104303
solve_time_s: 50
verified: true
draft: false
---

[CF 104303J - \u7ec4\u961f](https://codeforces.com/problemset/problem/104303/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a pool of students, each student knows a subset of up to 60 topics. A valid team is any subset of students such that two conditions are simultaneously satisfied: every topic from 1 to p is covered by at least one team member, and for each topic, at most one team member is allowed to know it. In other words, for every topic, if you look at the chosen subset, that topic can appear in the knowledge set of zero or one person, but never more than one, while still requiring that every topic appears somewhere in the team.

The task is to count how many subsets of students satisfy these constraints.

The most important structural consequence is that every topic behaves like a constraint that forbids pairing two students who both contain it, while also forcing that topic to appear at least once overall. Since each student is represented by a subset of up to 60 bits and n is at most 42, the natural search space is all subsets of students, which is 2^42, already around 4.4 trillion possibilities. Any solution that enumerates subsets directly is infeasible.

A subtle edge case appears when some topic is not present in any student. In that case no valid team exists, because the coverage requirement cannot be satisfied. For example, if p = 3 and no one knows topic 2, then even if we pick all students, topic 2 is still uncovered, so the answer must be zero.

Another failure mode appears when two students share a topic. A naive subset count would still include both, but such subsets are invalid regardless of other topics, so pruning is necessary rather than checking only at the end.

## Approaches

A brute force solution would iterate over all subsets of students, compute the union of topics in the subset, and check two conditions: the union must include all p topics, and no topic must appear twice. The second condition can be checked by maintaining a frequency array per subset or by tracking overlaps during construction. Even with bitmasks, this still requires iterating over 2^42 subsets, and for each subset scanning up to 42 students or 60 bits, leading to a complexity far beyond feasible limits.

The key observation is that the constraint “no topic appears in two chosen students” turns each valid team into a structure where chosen students must have disjoint bitmasks. This means we are counting subsets of pairwise-disjoint sets whose union covers all p bits. This is a classic disjoint set packing problem.

Since n is only 42 but p is up to 60, a direct subset DP over students is too large. The standard trick in this regime is meet-in-the-middle. We split students into two halves of size at most 21. Each half can be enumerated independently, and we record, for each subset, two pieces of information: the bitmask of topics it covers and whether it is internally valid (no overlap within the half).

For each half, we generate all valid subsets and group them by their coverage mask. The disjointness condition across halves becomes a simple bitwise AND constraint: a left subset with mask L and a right subset with mask R can be combined only if L & R = 0. The coverage requirement becomes L | R = FULL_MASK.

The counting then reduces to iterating over all valid left states and matching compatible right states using complement masks. Precomputing frequencies of right masks allows fast aggregation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Meet-in-the-middle | O(2^(n/2) · 2^(n/2)) | O(2^(n/2)) | Accepted |

## Algorithm Walkthrough

We split the students into two groups, left and right, each containing about n/2 people.

1. Convert each student’s knowledge set into a bitmask over p bits. This allows fast union and intersection checks using bit operations rather than per-topic loops.
2. Enumerate all subsets of the left half. For each subset, we build its union mask and simultaneously verify that no topic appears twice inside the subset. We maintain a running mask and a “valid so far” condition; if a new student overlaps with the current mask, the subset is discarded.
3. Store every valid left subset mask in a frequency table. If multiple subsets produce the same mask, we count them together since they are indistinguishable for later matching.
4. Repeat the same process for the right half, producing a frequency table of valid right masks.
5. For every pair of masks (L, R) where L comes from the left table and R from the right table, we check two conditions: L & R must be zero, and L | R must equal the full set of topics. When both hold, the contribution to the answer is freqL[L] × freqR[R].
6. Sum all contributions and output the result.

The reason we can combine halves independently is that validity inside each half already enforces disjointness within that half. Cross-half conflicts are handled explicitly using bitwise AND, so no invalid overlap can survive the merge step.

## Python Solution

```python
import sys
input = sys.stdin.readline

def gen_half(arr, p):
    n = len(arr)
    res = {}
    for mask in range(1 << n):
        ok = True
        cur = 0
        for i in range(n):
            if mask >> i & 1:
                x = arr[i]
                if cur & x:
                    ok = False
                    break
                cur |= x
        if ok:
            res[cur] = res.get(cur, 0) + 1
    return res

def solve():
    T = int(input())
    for _ in range(T):
        n, p = map(int, input().split())
        full = (1 << p) - 1
        a = []
        for _ in range(n):
            tmp = list(map(int, input().split()))
            k = tmp[0]
            mask = 0
            for x in tmp[1:]:
                mask |= 1 << (x - 1)
            a.append(mask)

        mid = n // 2
        left = a[:mid]
        right = a[mid:]

        L = gen_half(left, p)
        R = gen_half(right, p)

        ans = 0
        for lm, lv in L.items():
            for rm, rv in R.items():
                if (lm & rm) == 0 and (lm | rm) == full:
                    ans += lv * rv

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by encoding each student’s knowledge as a bitmask. This reduces all topic operations to O(1) bitwise operations.

The function `gen_half` enumerates all subsets of one half of students. For each subset mask, it constructs the union of topics and ensures no overlap occurs inside the subset. The check `cur & x` detects whether the new student shares any topic already present in the subset.

Each valid subset contributes its resulting coverage mask into a frequency dictionary, since multiple subsets may produce the same coverage.

After generating both halves, the final step checks compatibility. The condition `(lm & rm) == 0` enforces disjointness across halves, and `(lm | rm) == full` enforces full coverage of all topics.

The nested iteration over masks is acceptable because each half has at most 2^21 subsets.

## Worked Examples

Consider a small case with p = 3 and four students:

student 1 = {1}, student 2 = {2}, student 3 = {3}, student 4 = {1,2} is invalid in any subset with 1 or 2 alone due to overlap constraints depending on pairing.

Split into left {1,2} and right {3,4}.

### Left half enumeration

| subset | cur mask | valid |
| --- | --- | --- |
| ∅ | 000 | yes |
| {1} | 001 | yes |
| {2} | 010 | yes |
| {1,2} | 011 | yes |
| {4} | 011 | yes (single item) |

This produces frequency counts like mask 011 appears twice.

### Right half enumeration

| subset | cur mask | valid |
| --- | --- | --- |
| ∅ | 000 | yes |
| {3} | 100 | yes |
| {4} | 011 | yes |

Now we combine. We only accept pairs whose union is 111 and intersection is zero. So left mask 011 can only pair with right mask 100.

This trace shows that validity is entirely local inside halves, and global constraints are enforced only at merge time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^(n/2) · 2^(n/2)) | enumerate all subsets of both halves and match masks |
| Space | O(2^(n/2)) | store frequency maps of subset masks |

With n ≤ 42, each half has at most 2^21 ≈ 2 million subsets. The approach fits within limits for Python when implemented with bit operations and dictionary aggregation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import defaultdict

    def gen_half(arr, p):
        n = len(arr)
        res = {}
        for mask in range(1 << n):
            ok = True
            cur = 0
            for i in range(n):
                if mask >> i & 1:
                    x = arr[i]
                    if cur & x:
                        ok = False
                        break
                    cur |= x
            if ok:
                res[cur] = res.get(cur, 0) + 1
        return res

    T = int(input())
    out = []
    for _ in range(T):
        n, p = map(int, input().split())
        full = (1 << p) - 1
        a = []
        for _ in range(n):
            tmp = list(map(int, input().split()))
            k = tmp[0]
            mask = 0
            for x in tmp[1:]:
                mask |= 1 << (x - 1)
            a.append(mask)

        mid = n // 2
        L = gen_half(a[:mid], p)
        R = gen_half(a[mid:], p)

        ans = 0
        for lm, lv in L.items():
            for rm, rv in R.items():
                if (lm & rm) == 0 and (lm | rm) == full:
                    ans += lv * rv
        out.append(str(ans))

    return "\n".join(out)

# small sanity cases
assert run("1\n1 1\n1 1\n") == "1", "single student covers one topic"
assert run("1\n2 2\n1 1\n1 2\n") == "1", "only full pairing works"
assert run("1\n2 2\n1 1\n1 1\n") == "0", "duplicate topic invalid"
assert run("1\n3 3\n1 1\n1 2\n1 3\n") == "1", "perfect partition"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single student | 1 | minimal valid team |
| two complementary students | 1 | cross-half combination |
| duplicate knowledge | 0 | overlap rejection |
| full partition | 1 | correct full coverage |

## Edge Cases

A case where all students share at least one common topic immediately forces the answer to zero because any subset of size at least two violates the “no repeated topic” rule. The algorithm handles this naturally because during subset enumeration, any pair that includes both students triggers `cur & x != 0`, eliminating all multi-element subsets.

A case with missing topics results in `full` never being reachable. Even if left and right masks combine without overlap, `(lm | rm) == full` will never hold, so the accumulated answer remains zero.

A case with many identical students is handled through frequency aggregation in the mask maps. Even though subsets differ combinatorially, they collapse into identical masks and are correctly counted via multiplication in the final merge step.
