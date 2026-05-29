---
title: "CF 296A - Yaroslav and Permutations"
description: "We are given a sequence of integers, and we are allowed to repeatedly swap adjacent elements. Because adjacent swaps can generate any permutation of the array, the real freedom we have is complete reordering of the elements."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 296
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 179 (Div. 2)"
rating: 1100
weight: 296
solve_time_s: 57
verified: true
draft: false
---

[CF 296A - Yaroslav and Permutations](https://codeforces.com/problemset/problem/296/A)

**Rating:** 1100  
**Tags:** greedy, math  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and we are allowed to repeatedly swap adjacent elements. Because adjacent swaps can generate any permutation of the array, the real freedom we have is complete reordering of the elements.

The target condition is not about a specific arrangement, but about whether we can reorder the elements so that no two equal values end up next to each other. In other words, we want to know if there exists any permutation of the multiset of values where adjacent duplicates never occur.

The constraint n ≤ 100 means even cubic or factorial solutions would pass comfortably if they were ever needed, but the structure of the problem suggests we should be looking for a direct characterization rather than construction. Even if we tried to simulate all permutations, the search space grows as n!, which becomes irrelevant even for moderate n like 20. This is a hint that the answer depends on a simple property of frequencies rather than ordering details.

A few edge cases are worth isolating early. When n = 1, the array is trivially valid since there are no adjacent pairs at all. When all elements are identical and n > 1, no rearrangement can prevent adjacency, so the answer must be NO. A more subtle situation appears when one value dominates but not completely, for example [1, 1, 1, 2, 2]. This can sometimes be rearranged successfully or fail depending on whether the dominant value is too frequent to be separated.

## Approaches

A brute force approach would generate every possible permutation of the array and check whether any permutation satisfies the condition that all adjacent elements differ. This is conceptually straightforward because adjacency is easy to verify in linear time per permutation. However, the number of permutations is n!, and even for n = 10 this is already about 3.6 million configurations, each requiring O(n) validation. The total cost grows far beyond feasible limits.

The key observation is that adjacency constraints are governed entirely by how often the most frequent value appears. If a value appears too many times, there is no way to interleave it with other values sufficiently to separate all occurrences. Each occurrence of the most frequent element needs a “gap” filled by other elements, and the number of available gaps is limited by the rest of the array.

This reduces the problem from a global arrangement question to a simple frequency check. If the maximum frequency of any value is at most (n + 1) // 2, we can always construct a valid arrangement by spacing occurrences apart. If it exceeds this threshold, at least two occurrences must end up adjacent in any permutation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We solve the problem by focusing entirely on frequency distribution.

1. Count how many times each value appears in the array.

This gives a complete summary of how “crowded” each number is without caring about positions.
2. Find the maximum frequency among all values.

The most frequent element is the only one that can potentially force unavoidable adjacency.
3. Compute the threshold (n + 1) // 2.

This represents the maximum number of occurrences a value can have while still being separable by other elements.
4. Compare the maximum frequency with the threshold.

If it is greater, output NO. Otherwise, output YES.

The reason this comparison is sufficient is that any valid arrangement can be viewed as distributing the most frequent element into slots between other elements. If there are too many occurrences, the number of available slots is insufficient, forcing at least one adjacent collision.

### Why it works

Any arrangement of the array can be seen as placing the most frequent value first, then trying to interleave all other values around it. Between k occurrences of the same value, there are only k − 1 mandatory gaps. To avoid adjacency, each gap must contain at least one different element. If the remaining elements are not enough to fill these gaps, two identical values must become adjacent in every possible permutation. The condition max frequency ≤ (n + 1) // 2 is exactly the boundary where the available elements are just sufficient to separate all occurrences.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
a = list(map(int, input().split()))

freq = {}
for x in a:
    freq[x] = freq.get(x, 0) + 1

mx = max(freq.values()) if freq else 0

if mx <= (n + 1) // 2:
    print("YES")
else:
    print("NO")
```

The solution relies on a straightforward frequency dictionary. Each element is counted once, and then the maximum frequency is extracted. The final decision compares this value to the derived threshold.

A common mistake is attempting to simulate swaps or construct the permutation explicitly. That is unnecessary because the existence condition depends only on counts, not arrangement strategy. Another subtle point is using (n + 1) // 2 rather than n // 2, since odd lengths allow one extra occurrence of the majority element.

## Worked Examples

Consider an array of size 1, such as [7].

| Step | Value |
| --- | --- |
| n | 1 |
| frequencies | {7: 1} |
| max frequency | 1 |
| threshold | 1 |
| decision | YES |

This confirms the trivial case where no adjacency constraints exist.

Now consider [1, 1, 1, 2, 2].

| Step | Value |
| --- | --- |
| n | 5 |
| frequencies | {1: 3, 2: 2} |
| max frequency | 3 |
| threshold | 3 |
| decision | YES |

Even though one value is dominant, it can still be interleaved as 1, 2, 1, 2, 1.

Finally consider [5, 5, 5, 5, 1].

| Step | Value |
| --- | --- |
| n | 5 |
| frequencies | {5: 4, 1: 1} |
| max frequency | 4 |
| threshold | 3 |
| decision | NO |

The four occurrences of 5 cannot be separated by a single different element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once to compute frequencies, then scanned once to find the maximum |
| Space | O(k) | Frequency map stores counts for distinct values |

The constraints n ≤ 100 make this solution trivially fast, but the linear structure also scales well beyond the limits of the problem.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose

    input = _sys.stdin.readline
    n = int(input().strip())
    a = list(map(int, input().split()))

    freq = {}
    for x in a:
        freq[x] = freq.get(x, 0) + 1

    mx = max(freq.values()) if freq else 0
    return "YES\n" if mx <= (n + 1) // 2 else "NO\n"

# provided sample
assert run("1\n1\n") == "YES\n", "sample 1"

# single element edge case
assert run("1\n7\n") == "YES\n"

# all equal, impossible when n > 1
assert run("4\n2 2 2 2\n") == "NO\n"

# alternating possible
assert run("5\n1 2 1 2 3\n") == "YES\n"

# dominant element barely valid
assert run("5\n1 1 2 2 3\n") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | YES | trivial base case |
| all equal n>1 | NO | impossibility under dominance |
| alternating mix | YES | separable frequencies |
| borderline distribution | YES | threshold correctness |

## Edge Cases

A single-element array like [9] immediately satisfies the condition since there are no adjacent pairs to violate. The algorithm counts one occurrence, finds max frequency 1, and compares it to threshold 1, producing YES without any ambiguity.

An array such as [3, 3, 3, 3] produces a maximum frequency equal to n. The threshold for n = 4 is 2, so the condition fails. The frequency check correctly identifies that no rearrangement can prevent adjacency because every position is occupied by the same value.

A more subtle case like [1, 1, 2, 2, 3] passes because the most frequent value appears only twice, which fits within the allowed separation capacity. The computed threshold is 3, and the algorithm correctly allows YES even though naive intuition might expect instability due to repeated values.
