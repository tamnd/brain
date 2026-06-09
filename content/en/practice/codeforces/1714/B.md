---
title: "CF 1714B - Remove Prefix"
description: "We are given a sequence of integers a of length n, where each integer lies between 1 and n. The goal is to make the sequence contain only distinct values by repeatedly removing elements from the beginning."
date: "2026-06-09T20:04:36+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1714
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 811 (Div. 3)"
rating: 800
weight: 1714
solve_time_s: 99
verified: true
draft: false
---

[CF 1714B - Remove Prefix](https://codeforces.com/problemset/problem/1714/B)

**Rating:** 800  
**Tags:** data structures, greedy, implementation  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers `a` of length `n`, where each integer lies between `1` and `n`. The goal is to make the sequence contain only distinct values by repeatedly removing elements from the beginning. For each test case, we must determine the minimum number of elements to remove from the left so that the remaining sequence contains no duplicates.

The input consists of multiple test cases, up to 10^4, and the sum of all sequence lengths does not exceed 2×10^5. This implies that any solution that is linear in the length of the sequence per test case will fit comfortably in a 2-second time limit, while solutions with O(n^2) per test case would be too slow.

An important edge case occurs when the duplicates appear at the very start of the array, for example `[1,1,1,1]`. A naive approach that checks duplicates only from the beginning of the sequence might incorrectly remove too few elements. Another edge case is when the sequence is already unique, such as `[1,2,3]`. In that case, the answer must be zero. A sequence with all elements distinct but in decreasing order, like `[6,5,4,3,2,1]`, is another case that could trip up an algorithm that does not properly track duplicates from the end.

## Approaches

The brute-force approach would simulate the removal of prefixes. Start from removing zero elements and check whether the remaining sequence is unique. If not, remove one more element, check again, and repeat until the sequence is unique. This works because checking uniqueness in a subsequence can be done with a set, but in the worst case this is O(n^2) since we might check all prefixes and each check is O(n). For `n` up to 2×10^5, this is far too slow.

The key insight is that removing elements from the start only affects duplicates at the left. Once a duplicate occurs for the first time from the right, we can remove everything before its earliest occurrence. This leads naturally to a reverse traversal: start from the right end of the array and insert elements into a set. Once we encounter an element already in the set, we stop. The number of elements before this stopping point is exactly the minimum prefix we must remove to achieve uniqueness in the remaining sequence. This reduces the problem to a linear scan from the end, with O(n) time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a set `seen` to track the numbers that have already appeared.
2. Start scanning the sequence from the rightmost element towards the leftmost element.
3. For each element, check if it is in `seen`.
4. If the element is already in `seen`, stop scanning. This is the first duplicate encountered from the right.
5. If the element is not in `seen`, add it to `seen` and continue moving left.
6. After stopping, the position of the leftmost element we scanned corresponds to the minimum prefix to remove. The number of elements to remove is exactly the index of this element (0-based indexing).
7. Print the number of elements to remove for each test case.

**Why it works:** The invariant is that `seen` always contains all elements in the suffix of the array starting from the rightmost element scanned so far. The first element that would duplicate an element in this suffix must be removed because it violates uniqueness. By scanning from the right, we are guaranteed that we are keeping the longest unique suffix, and any element to the left that duplicates an element in this suffix must belong to the prefix that is removed. This guarantees minimal prefix removal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    seen = set()
    remove_count = 0
    # traverse from right to left
    for i in range(n-1, -1, -1):
        if a[i] in seen:
            break
        seen.add(a[i])
        remove_count += 1
    # the minimal prefix to remove
    print(n - remove_count)
```

This solution initializes a `set` for tracking duplicates. It counts the number of elements in the longest unique suffix. Subtracting this count from `n` gives the minimal prefix length to remove. The traversal from right to left ensures we capture the longest unique suffix efficiently. We break immediately when a duplicate is encountered, avoiding unnecessary work.

## Worked Examples

**Example 1: `[3, 1, 4, 3]`**

| i | a[i] | seen | remove_count |
| --- | --- | --- | --- |
| 3 | 3 | {} | 1 |
| 2 | 4 | {3} | 2 |
| 1 | 1 | {3,4} | 3 |
| 0 | 3 | {1,4,3} | stop |

Remaining suffix `[1,4,3]`, removed prefix length = 4 - 3 = 1.

**Example 2: `[1,2,1,7,1,2,1]`**

| i | a[i] | seen | remove_count |
| --- | --- | --- | --- |
| 6 | 1 | {} | 1 |
| 5 | 2 | {1} | 2 |
| 4 | 1 | {1,2} | stop |

Remaining suffix `[2,1]`, removed prefix length = 7 - 2 = 5.

These traces show that scanning from right to left captures the longest unique suffix and yields the minimal prefix length to remove.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is added to `seen` at most once. Right-to-left scan stops immediately at first duplicate. |
| Space | O(n) per test case | The `seen` set can store all distinct numbers in the sequence. |

Given that the sum of `n` across all test cases does not exceed 2×10^5, the solution fits well within the 2-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        seen = set()
        remove_count = 0
        for i in range(n-1, -1, -1):
            if a[i] in seen:
                break
            seen.add(a[i])
            remove_count += 1
        print(n - remove_count)
    return output.getvalue().strip()

# Provided samples
assert run("5\n4\n3 1 4 3\n5\n1 1 1 1 1\n1\n1\n6\n6 5 4 3 2 1\n7\n1 2 1 7 1 2 1\n") == "1\n4\n0\n0\n5"

# Custom test cases
assert run("2\n3\n1 1 1\n3\n1 2 3\n") == "2\n0", "all-equal vs all-distinct"
assert run("1\n5\n5 4 3 2 1\n") == "0", "reverse-order unique"
assert run("1\n1\n1\n") == "0", "single element"
assert run("1\n6\n1 2 3 3 2 1\n") == "3", "multiple duplicates"
assert run("1\n7\n1 2 3 4 5 6 7\n") == "0", "already unique"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | 2 | Correct handling of repeated elements at start |
| `1 2 3` | 0 | Sequence already unique |
| `5 4 3 2 1` | 0 | Longest suffix is entire array |
| `1 2 3 3 2 1` | 3 | Correct prefix removal for internal duplicates |
| `1 2 3 4 5 6 7` | 0 | Already unique, no removal |

## Edge Cases

For `[1,1,1,1,1]`, scanning from right, we see the last `1` first, then stop at the previous `1`. The suffix is `[1]`, prefix length removed = 5-1 = 4. The algorithm correctly identifies the minimal removal.

For `[6,5,4,3,2,1]`, scanning from right, each element is unique until the leftmost element. The suffix is the entire array, so the minimal prefix removal is 0.

For `[1]`, single-element sequences are always unique. The algorithm scans from right, adds `1` to `seen`,
