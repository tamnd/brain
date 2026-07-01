---
title: "CF 104246F - Find Rewards from RAPL"
description: "We are given a collection of coders, each starting with some initial reward value. Over time, a sequence of updates arrives, and each update targets exactly one coder and increases that coder’s reward by some integer, which may be positive or negative."
date: "2026-07-01T23:01:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104246
codeforces_index: "F"
codeforces_contest_name: "CodeSmash 2021 by RAPL"
rating: 0
weight: 104246
solve_time_s: 80
verified: false
draft: false
---

[CF 104246F - Find Rewards from RAPL](https://codeforces.com/problemset/problem/104246/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of coders, each starting with some initial reward value. Over time, a sequence of updates arrives, and each update targets exactly one coder and increases that coder’s reward by some integer, which may be positive or negative.

After each update, we are asked to report how many distinct reward values exist among all coders at that moment. In other words, after processing the first k updates, we conceptually have an updated array of size n, and we want the number of unique values inside it.

The input structure is multiple independent test cases. Each test case gives an initial array, then a stream of point modifications, and we must output one answer per update step.

The constraints matter because both n and m can be as large as 100000 per test case, and the total over all test cases is at most 200000. This immediately rules out any approach that recomputes the number of distinct values from scratch after each update, since that would cost O(n) per query and lead to roughly 10^10 operations in the worst case.

A subtle issue is that values can repeat heavily after updates. A naive intuition might try to maintain a frequency map of values, but blindly updating frequencies without tracking how many elements share a value leads to incorrect distinct counts.

Another edge case appears when multiple coders converge to the same value after different update paths. For example, starting with [1, 2], then adding +1 to index 1 and -1 to index 2 yields [2, 1], which still has two distinct values even though individual values changed identity. Any solution must track global value multiplicity, not just per-index history.

## Approaches

A direct brute force solution recomputes the number of distinct values after every update. After applying the k-th operation, we scan the entire array and insert all values into a set to count uniques. This is correct because a set naturally deduplicates values.

However, each scan costs O(n), and we do it m times, so the complexity per test case becomes O(nm). With n and m up to 100000, this is far beyond feasible limits.

The key observation is that only one element changes per operation. This means the entire array does not need to be recomputed; we only need to adjust the contribution of a single old value and a single new value.

If we maintain a frequency map of values across all coders, then each update only affects two frequencies: the old value of the updated coder decreases by one occurrence, and the new value increases by one occurrence. The number of distinct values is exactly the number of keys in this frequency map with positive count.

So instead of rebuilding the set, we maintain counts incrementally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Frequency Map Maintenance | O((n + m) log n) or O(n + m) average | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two structures: an array storing current values for each coder, and a hashmap storing how many times each value appears globally.

### Steps

1. Initialize an array `a` with the initial rewards of all coders.
2. Build a frequency map `freq` where `freq[x]` is how many coders currently have value `x`.
3. Compute initial number of distinct values as the number of keys in `freq` with nonzero frequency.
4. For each update `(p, r)`, identify the current value `old = a[p]`.
5. Decrease `freq[old]` by one because coder `p` will no longer have this value.
6. If `freq[old]` becomes zero, remove it from the map or treat it as absent, since it no longer contributes to distinct values.
7. Compute the new value `new = old + r` and assign it to coder `p`.
8. Increase `freq[new]` by one, creating the entry if necessary.
9. After each update, output the current number of keys in `freq`.

Each step is driven by the fact that only one element changes per operation, so global structure updates reduce to two counter adjustments.

### Why it works

The key invariant is that after processing each update, the frequency map exactly represents the multiset of current reward values across all coders. Since distinct values correspond precisely to values with frequency greater than zero, counting active keys in the map yields the correct answer. Because every update only changes one array position, adjusting two counts preserves this invariant without needing any full recomputation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out_lines = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        freq = {}
        distinct = 0

        for x in a:
            if x not in freq:
                freq[x] = 0
            if freq[x] == 0:
                distinct += 1
            freq[x] += 1

        for _ in range(m):
            p, r = map(int, input().split())
            p -= 1

            old = a[p]

            freq[old] -= 1
            if freq[old] == 0:
                distinct -= 1

            new = old + r
            a[p] = new

            if new not in freq:
                freq[new] = 0
            if freq[new] == 0:
                distinct += 1
            freq[new] += 1

            out_lines.append(str(distinct))

    print("\n".join(out_lines))

if __name__ == "__main__":
    solve()
```

The implementation mirrors the invariant directly. The array `a` stores current values so that each update can access the old value in O(1). The dictionary `freq` tracks multiplicities. The variable `distinct` avoids recomputing the number of active keys by maintaining it incrementally when counts cross zero in either direction.

Care must be taken when handling transitions. When decrementing a value, the distinct counter only decreases when its count becomes exactly zero. When incrementing a value, the distinct counter increases only when it transitions from zero to one. This avoids double counting values that already exist.

Indexing is adjusted by subtracting one from `p` because input uses 1-based indexing.

## Worked Examples

### Example 1

Input:

```
n = 5, m = 3
a = [20, 10, 25, 5, 3]
updates = (5,2), (2,-5), (4,20)
```

We track `(freq, distinct)`.

| Step | Operation | Array state | freq changes | distinct |
| --- | --- | --- | --- | --- |
| 0 | init | [20,10,25,5,3] | all 1 | 5 |
| 1 | +2 at 5 | [20,10,25,5,5] | 3:1→0, 5:1→2 | 4 |
| 2 | -5 at 2 | [20,5,25,5,5] | 10:1→0, 5:2→3 | 3 |
| 3 | +20 at 4 | [20,5,25,25,5] | 5:3→2, 25:1→2 | 3 |

This trace shows how duplicates reduce distinct count only when a value fully disappears, not when it merely changes frequency.

### Example 2

Input:

```
n = 1, m = 3
a = [100]
updates: (1,400), (1,1), (1,-100)
```

| Step | Value | freq | distinct |
| --- | --- | --- | --- |
| 0 | [100] | {100:1} | 1 |
| 1 | 500 | {500:1} | 1 |
| 2 | 501 | {501:1} | 1 |
| 3 | 401 | {401:1} | 1 |

Even though the value changes each time, there is always exactly one element, so the number of distinct values never changes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) average per test case | Each update performs constant-time hash map operations |
| Space | O(n + m) | Frequency map stores at most n + m distinct values over time |

The total sum of n and m across all test cases is bounded by 200000, so the solution comfortably fits within both time and memory limits. Each update is handled in O(1) amortized time using hashing, making the full input linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys

    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, m = map(int, input().split())
            a = list(map(int, input().split()))
            freq = {}
            distinct = 0
            for x in a:
                if freq.get(x, 0) == 0:
                    distinct += 1
                freq[x] = freq.get(x, 0) + 1

            for _ in range(m):
                p, r = map(int, input().split())
                p -= 1
                old = a[p]
                freq[old] -= 1
                if freq[old] == 0:
                    distinct -= 1
                new = old + r
                a[p] = new
                if freq.get(new, 0) == 0:
                    distinct += 1
                freq[new] = freq.get(new, 0) + 1
                out.append(str(distinct))

        return "\n".join(out)

    return solve()

# provided sample (trimmed formatting assumed)
assert run("""1
5 3
20 10 25 5 3
5 2
2 -5
4 20
""") == "4\n3\n3"

# all equal updates
assert run("""1
3 2
7 7 7
1 1
2 -1
""") == "2\n2"

# single element
assert run("""1
1 3
10
1 5
1 -2
1 -3
""") == "1\n1\n1"

# create and destroy distinct values
assert run("""1
2 4
1 2
1 1
2 -1
1 -2
2 3
""") == "2\n2\n1\n2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single array, repeated updates | constant 1 | stability of single element case |
| all equal values | correct distinct transitions | handling zero-to-one transitions |
| alternating merges | dynamic creation/removal | correctness of freq boundary updates |

## Edge Cases

One important edge case is when a value disappears completely. Suppose all coders currently have value 5 except one, and that last one is updated away. The frequency of 5 drops to zero and must reduce the distinct counter by exactly one. The algorithm handles this because the decrement step checks for `freq[old] == 0` after subtraction and reduces `distinct` only at that moment.

Another case is introducing a value that already exists. If a coder changes from 3 to 7, but 7 already appears elsewhere, then the distinct count must not increase. The check `if freq[new] == 0` ensures that we only increment distinct when the value was previously absent.

A third case is repeated updates on the same index. The array `a[p]` always stores the current value, so each update correctly subtracts the previous state before applying the next one. This avoids accumulating stale contributions from earlier updates.
