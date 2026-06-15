---
title: "CF 1208B - Uniqueness"
description: "We are given a sequence of numbers and we are allowed to remove one continuous block from it, or remove nothing at all. After this single deletion, the remaining elements must all be different from each other."
date: "2026-06-15T17:52:58+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1208
codeforces_index: "B"
codeforces_contest_name: "Manthan, Codefest 19 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 1500
weight: 1208
solve_time_s: 229
verified: true
draft: false
---

[CF 1208B - Uniqueness](https://codeforces.com/problemset/problem/1208/B)

**Rating:** 1500  
**Tags:** binary search, brute force, implementation, two pointers  
**Solve time:** 3m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of numbers and we are allowed to remove one continuous block from it, or remove nothing at all. After this single deletion, the remaining elements must all be different from each other.

The task is to choose a subarray to remove so that the final array has no repeated values, and among all valid choices we want the shortest possible removed segment. If the array is already free of duplicates, the answer is zero because we do not need to delete anything.

The key constraint here is that the array length is at most 2000. This immediately suggests that quadratic or even cubic solutions are acceptable if implemented carefully, while anything worse than $O(n^2)$ risks becoming borderline but still potentially acceptable. However, the structure of the problem strongly hints that we should try to avoid checking all possible subarrays in a fully recomputed way.

A naive interpretation would be: try every pair $(l, r)$, delete that segment, then check if the remaining elements are all distinct. That check alone costs $O(n)$, and there are $O(n^2)$ subarrays, giving $O(n^3)$, which is unnecessary but might still pass in optimized Python under 2000. Still, we can do better.

A subtle edge case appears when duplicates are already separated far apart. For example, in an array like $[1, 2, 3, 1]$, the only valid removal must eliminate at least one occurrence of the duplicated value. A careless approach that only checks prefix or suffix might miss optimal solutions where the removal lies strictly in the middle.

Another important edge case is when all elements are identical. For example $[5, 5, 5, 5]$, the best we can do is keep at most one element, so we must remove $n-1$ elements, and the optimal segment can be anywhere except leaving a single element.

## Approaches

The brute-force idea starts by choosing the segment $[l, r]$ to remove. After deletion, we concatenate the prefix $[1, l-1]$ and suffix $[r+1, n]$, then check whether this combined array has all distinct values.

This works because it directly follows the definition of the problem. However, recomputing uniqueness from scratch for every $(l, r)$ pair requires scanning up to $n$ elements, leading to $O(n^3)$ total operations in the worst case. With $n = 2000$, this is too slow if implemented straightforwardly.

The key observation is that once we fix the left boundary of the kept prefix, we can greedily extend the right boundary of the suffix while ensuring no duplicates are introduced. Instead of recomputing validity from scratch for every removed segment, we treat the solution as choosing a split of the array into a kept prefix and kept suffix. The removed segment is exactly what lies between them.

So we iterate over how many elements we keep from the left side, maintain which values appear there, and then find the maximum valid suffix starting from the right that does not introduce duplicates with the prefix. This turns the problem into a two-pointer style interaction between prefix and suffix validity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Two-pointer prefix-suffix scan | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

We want to choose a prefix we keep and a suffix we keep, and remove everything in between. The goal is to maximize the size of the kept elements while ensuring all kept values are distinct. Minimizing removed segment is equivalent to maximizing kept prefix plus suffix.

1. Fix a left boundary $i$, meaning we keep the prefix $a_1 \dots a_i$. We ensure this prefix has no duplicates by tracking seen values. If a duplicate appears, we stop because extending further is invalid.
2. For this fixed prefix, we try to choose a suffix starting from the end of the array. We maintain a set of values already used in the prefix and extend a pointer $j$ from $n$ backward, only including elements that are not present in the prefix set and not duplicated in the suffix itself.
3. As we move $j$ leftwards, we maintain a set for suffix elements. If a value conflicts with the prefix or repeats in the suffix, we stop extending.
4. For each valid prefix, we compute the best possible suffix and derive the total kept length. The removed segment is the gap between them, so we update the minimum removed size.
5. We repeat this for all valid prefix endpoints.

The subtle idea is that once the prefix is fixed, the suffix is greedily maximized from the right, because taking any later suffix element only reduces freedom and never helps future validity.

### Why it works

The algorithm relies on the fact that any valid final array can be represented as a prefix and suffix that are disjoint and individually distinct, and also mutually disjoint in values. For any optimal solution, the prefix portion must correspond to some prefix of the original array (after choosing where the removal starts), and similarly the suffix corresponds to a suffix of the original array. By enumerating all prefix endpoints and greedily extending suffixes, we ensure that every optimal split is considered in one of the iterations. The greedy suffix extension is safe because once a suffix element is excluded due to duplication, including more elements earlier in the suffix cannot restore validity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    ans = n

    # try all prefix ends
    for i in range(n + 1):
        seen = set()
        ok = True

        # build prefix [0..i-1]
        for k in range(i):
            if a[k] in seen:
                ok = False
                break
            seen.add(a[k])

        if not ok:
            break

        # now greedily take suffix from right
        used_suffix = set()
        j = n

        while j > i:
            if a[j - 1] in seen or a[j - 1] in used_suffix:
                break
            used_suffix.add(a[j - 1])
            j -= 1

        kept = i + (n - j)
        ans = min(ans, n - kept)

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first tries every prefix length. For each prefix, it explicitly checks that the prefix itself contains no duplicates. This is necessary because once a prefix becomes invalid, extending it further only worsens the situation, so we can stop early.

After fixing a valid prefix, we compute the longest possible suffix that does not conflict with it. The suffix is built from the end backwards, and we stop as soon as a conflict appears, since any further inclusion would only reduce validity.

The kept size is the sum of prefix length and suffix length. Since we are effectively splitting the array into three parts, prefix, removed segment, suffix, the removed size is derived by subtraction.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

| i | Prefix valid | Suffix j | Kept prefix | Kept suffix | Total kept |
| --- | --- | --- | --- | --- | --- |
| 0 | yes | 0 | 0 | 3 | 3 |
| 1 | yes | 0 | 1 | 2 | 3 |
| 2 | yes | 0 | 2 | 1 | 3 |
| 3 | yes | 3 | 3 | 0 | 3 |

All values are already distinct, so the best configuration keeps all elements, giving answer 0.

This confirms that when no conflicts exist, the suffix expansion always consumes the whole array, yielding zero removal.

### Example 2

Input:

```
4
1 2 1 3
```

| i | Prefix valid | Suffix j | Kept prefix | Kept suffix | Total kept |
| --- | --- | --- | --- | --- | --- |
| 0 | yes | 2 | 0 | 2 | 2 |
| 1 | yes | 3 | 1 | 1 | 2 |
| 2 | no | - | - | - | - |

Best solution keeps `[1,2]` and `[3]`, removing middle segment `[1]`, so answer is 1.

This demonstrates how duplicates force a middle deletion, and how suffix selection must avoid conflicting values from the prefix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each prefix is checked once, and suffix is scanned from the right at most n times total across iterations |
| Space | O(n) | Sets for prefix and suffix tracking |

The quadratic behavior fits comfortably within $n \le 2000$, since about 4 million operations are manageable in Python under typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else solve_capture(inp)

def solve_capture(inp: str) -> str:
    import sys
    input = sys.stdin.readline
    it = inp.strip().split()
    n = int(it[0])
    a = list(map(int, it[1:]))

    ans = n
    for i in range(n + 1):
        seen = set()
        ok = True
        for k in range(i):
            if a[k] in seen:
                ok = False
                break
            seen.add(a[k])
        if not ok:
            break

        used_suffix = set()
        j = n
        while j > i:
            if a[j - 1] in seen or a[j - 1] in used_suffix:
                break
            used_suffix.add(a[j - 1])
            j -= 1

        kept = i + (n - j)
        ans = min(ans, n - kept)

    return str(ans)

# samples
assert solve_capture("3\n1 2 3\n") == "0"

# all equal
assert solve_capture("4\n5 5 5 5\n") == "3"

# single duplicate pair
assert solve_capture("4\n1 2 1 3\n") == "1"

# already distinct larger
assert solve_capture("5\n1 2 3 4 5\n") == "0"

# prefix conflict early
assert solve_capture("5\n1 2 1 2 3\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 3 | worst-case deletion |
| single duplicate pair | 1 | middle removal correctness |
| already distinct | 0 | no-op case |
| repeated pattern | 2 | prefix-suffix interaction |

## Edge Cases

For an array like $[5, 5, 5, 5]$, the algorithm tries prefix lengths. At $i = 1$, the prefix is valid. The suffix scan immediately stops after adding one element, since the next element conflicts with the suffix set. This yields a kept size of 2, meaning removal size is 2, but better prefixes give the optimal removal of 3. The algorithm correctly evaluates all prefix choices and finds the minimum.

For a case like $[1, 2, 1, 2]$, the prefix at $i = 2$ is valid, but the suffix cannot include either 1 or 2, so suffix size becomes zero. The result corresponds to removing a middle segment of size 2, which is correctly captured by the split logic.
