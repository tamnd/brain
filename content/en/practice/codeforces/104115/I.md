---
title: "CF 104115I - \u0414\u0435\u043b\u0435\u043d\u0438\u0435 \u0441\u0442\u0440\u043e\u043a\u0438"
description: "We are given a string consisting of lowercase English letters and asked whether it can be split into exactly k contiguous non-empty pieces such that every piece contains the same number of consonant letters. A consonant here means any letter except a, e, i, o, u, y."
date: "2026-07-02T01:57:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104115
codeforces_index: "I"
codeforces_contest_name: "Voronezh State University - Sitronics contest, 2022"
rating: 0
weight: 104115
solve_time_s: 28
verified: true
draft: false
---

[CF 104115I - \u0414\u0435\u043b\u0435\u043d\u0438\u0435 \u0441\u0442\u0440\u043e\u043a\u0438](https://codeforces.com/problemset/problem/104115/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting of lowercase English letters and asked whether it can be split into exactly k contiguous non-empty pieces such that every piece contains the same number of consonant letters. A consonant here means any letter except a, e, i, o, u, y.

The key constraint is that the split must be by cutting the string into consecutive segments, so we are not rearranging characters. We only choose k cut positions, and the resulting k substrings must all have equal counts of consonants.

The input size can be as large as 200,000 characters, so any solution that tries all possible partitions or checks all cut combinations is immediately infeasible. A quadratic or exponential approach over split positions or segment choices would exceed time limits by a large margin, so the solution must be linear or near-linear in n.

A first subtle edge case appears when k is larger than n. Even if the string contains many vowels, every segment must be non-empty, so we cannot have more segments than characters. For example, n = 3, k = 4 always fails regardless of the string.

Another important edge case is when the total number of consonants is not divisible by k. Since each segment must have the same number of consonants, if the total consonant count is C, then each part must have exactly C / k consonants. If C is not divisible by k, no partition can work. For example, if the string has 5 consonants and k = 2, we cannot split 5 equally into two integer parts.

Finally, even when divisibility holds, we must ensure that the segmentation is possible in a contiguous way. This requires that when we scan left to right and accumulate consonants, we can place cuts exactly at multiples of the target per-segment consonant count.

## Approaches

A brute-force strategy would attempt to place k − 1 cuts among n − 1 possible positions and verify each partition. For each candidate partition, we would recompute consonant counts in each segment. Even with prefix sums, the number of cut combinations is on the order of choosing k positions out of n, which becomes combinatorially large when n is 200,000 and k is up to 200,000. This approach is completely infeasible.

The key observation is that only consonant counts matter, not exact letter composition. Once we know the total number of consonants C, every valid partition must split C into k equal integer parts, each equal to C / k. This transforms the problem into a single linear scan: we count consonants and then greedily assign them to segments in order. Whenever we accumulate exactly C / k consonants, we end one segment and start the next.

The greedy nature works because the string order is fixed. There is no benefit in delaying a cut or moving it earlier once the required quota for a segment is reached, since consonant counts only increase as we move right.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force cuts enumeration | Exponential | O(n) | Too slow |
| Prefix + greedy scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count the total number of consonants in the string by scanning each character once. If the count is zero, we treat it as a special case because all segments must still have equal counts, which forces every segment to have zero consonants.
2. If k is greater than n, immediately return “No” since we cannot form k non-empty segments.
3. If total consonants C is zero, every segment must have zero consonants, which is always possible as long as we can split the string into k non-empty parts. Since any cut does not affect consonant equality, the answer is “Yes” when k ≤ n.
4. If C is not divisible by k, return “No” because equal distribution of integer counts is impossible.
5. Compute target = C / k, which is the required number of consonants in each segment.
6. Traverse the string from left to right, maintaining a running counter of consonants in the current segment.
7. Each time we encounter a consonant, increment the running counter.
8. Whenever the running counter reaches target, we reset it to zero and conceptually finish one segment. We also count how many segments we have completed.
9. After processing the full string, check whether we formed exactly k segments and consumed all consonants evenly. If yes, return “Yes”, otherwise return “No”.

### Why it works

The correctness rests on the monotonic structure of the problem. Consonant counts only increase as we scan the string, so segment boundaries are forced: a segment must end exactly when its required quota is reached. Any earlier cut would leave insufficient consonants for the segment, and any later cut would exceed the quota. Therefore, if a valid partition exists, it must coincide with this greedy construction. The divisibility condition ensures that the quotas are consistent globally, and the scan guarantees local feasibility at every step.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_vowel(c):
    return c in "aeiouy"

def solve():
    n, k = map(int, input().split())
    s = input().strip()

    consonants = 0
    for ch in s:
        if not is_vowel(ch):
            consonants += 1

    if k > n:
        print("No")
        return

    if consonants == 0:
        print("Yes")
        return

    if consonants % k != 0:
        print("No")
        return

    target = consonants // k

    cnt = 0
    segments = 0

    for ch in s:
        if not is_vowel(ch):
            cnt += 1
        if cnt == target:
            segments += 1
            cnt = 0

    print("Yes" if segments == k and cnt == 0 else "No")

if __name__ == "__main__":
    solve()
```

The implementation mirrors the greedy construction directly. The vowel check is isolated for clarity. The only subtle condition is the final verification: we ensure that exactly k full segments were formed and that no leftover consonants remain, which would indicate an incomplete final segment.

## Worked Examples

### Example 1

Input:

```
9 2
polnareff
```

Consonants are p, l, n, r, f, f, so total is 6. Target per segment is 3.

| Step | Character | Consonant Count | Segments Formed |

|
