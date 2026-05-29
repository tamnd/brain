---
title: "CF 315A - Sereja and Bottles"
description: "We are given a set of soda bottles, each labeled with a brand and a \"can open\" brand. Each bottle can be used to open other bottles of the brand it can open. A bottle can be used to open itself or others."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 315
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 187 (Div. 2)"
rating: 1400
weight: 315
solve_time_s: 85
verified: true
draft: false
---

[CF 315A - Sereja and Bottles](https://codeforces.com/problemset/problem/315/A)

**Rating:** 1400  
**Tags:** brute force  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of soda bottles, each labeled with a brand and a "can open" brand. Each bottle can be used to open other bottles of the brand it can open. A bottle can be used to open itself or others. Our task is to count how many bottles are completely unopenable by any other bottle.

The input consists of an integer `n` representing the number of bottles, followed by `n` lines each containing two integers: `a[i]` (the brand of the bottle) and `b[i]` (the brand it can open). The output is a single integer: the count of bottles that cannot be opened by any other bottle in the collection.

The constraints are small: `n` is up to 100, and brands are integers up to 1000. This allows algorithms with time complexity up to roughly O(n²), because `100² = 10,000` operations is acceptable for a 2-second time limit.

Non-obvious edge cases include situations where all bottles can only open themselves. For example, if every bottle has `a[i] = b[i]`, no bottle can open another, so the answer should be `n`. Another edge case is when one bottle can open all others but no other bottle can open it; this should reduce the count of unopenable bottles to 0 for the bottles it can open, except for itself if nothing else opens it.

## Approaches

The brute-force approach is straightforward: for each bottle, check if there exists any other bottle that can open it. We iterate through all `n` bottles, and for each, iterate through all other `n-1` bottles, comparing the "can open" brand to the current bottle's brand. This is correct, because it explicitly checks every possible opener. The worst-case number of operations is O(n²), which is acceptable here since `n ≤ 100`.

The optimal approach is essentially the same as brute-force for this problem because the input size is small. There is no advanced data structure or graph technique required; the problem does not demand transitive closures or reachability. The insight is simply to recognize that "any bottle can open itself or others" reduces to checking whether there exists a different bottle that can open the current one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, the number of bottles.
2. Initialize two lists: `a` for bottle brands and `b` for the brands they can open.
3. For each bottle `i`, check all other bottles `j ≠ i`. If there exists a `j` such that `b[j] == a[i]`, mark bottle `i` as openable by some other bottle.
4. Count the bottles that were never marked as openable. This is the answer.
5. Print the count.

Why it works: The invariant is that for each bottle, we explicitly check all other bottles to see if it is openable. Because we consider all possible "other" bottles, no bottle is mistakenly classified as unopenable. Self-opening is ignored in the check, which aligns with the problem requirement that a bottle must be opened by a different one to be considered "openable by others."

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = []
b = []

for _ in range(n):
    x, y = map(int, input().split())
    a.append(x)
    b.append(y)

unopenable_count = 0

for i in range(n):
    can_be_opened = False
    for j in range(n):
        if i != j and b[j] == a[i]:
            can_be_opened = True
            break
    if not can_be_opened:
        unopenable_count += 1

print(unopenable_count)
```

The solution reads the bottle data, stores the brands and the brands they can open in two lists, and then iterates through each bottle checking if it is openable by any other bottle. The inner loop stops as soon as a match is found, optimizing slightly for the average case. The `i != j` condition ensures that a bottle is not considered as opened by itself.

## Worked Examples

**Sample 1**:

Input:

```
4
1 1
2 2
3 3
4 4
```

| i | a[i] | b[j] matches a[i]? | can_be_opened | unopenable_count |
| --- | --- | --- | --- | --- |
| 0 | 1 | no | False | 1 |
| 1 | 2 | no | False | 2 |
| 2 | 3 | no | False | 3 |
| 3 | 4 | no | False | 4 |

Output: `4`

All bottles can only open themselves, so none is openable by another bottle.

**Custom Example**:

Input:

```
3
1 2
2 3
3 1
```

| i | a[i] | b[j] matches a[i]? | can_be_opened | unopenable_count |
| --- | --- | --- | --- | --- |
| 0 | 1 | j=2, b[2]=1 | True | 0 |
| 1 | 2 | j=0, b[0]=2 | True | 0 |
| 2 | 3 | j=1, b[1]=3 | True | 0 |

Output: `0`

Here, each bottle is openable by another, so the count of unopenable bottles is zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each bottle is checked against all other bottles for a match, giving n*(n-1) comparisons. |
| Space | O(n) | Two lists of length n store the brands and openable brands. |

The solution fits comfortably within the constraints, since n² ≤ 10,000 operations and the memory required for two arrays of length 100 is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = []
    b = []
    for _ in range(n):
        x, y = map(int, input().split())
        a.append(x)
        b.append(y)
    unopenable_count = 0
    for i in range(n):
        can_be_opened = False
        for j in range(n):
            if i != j and b[j] == a[i]:
                can_be_opened = True
                break
        if not can_be_opened:
            unopenable_count += 1
    return str(unopenable_count)

# Provided sample
assert run("4\n1 1\n2 2\n3 3\n4 4\n") == "4", "sample 1"

# Custom cases
assert run("3\n1 2\n2 3\n3 1\n") == "0", "all bottles can open each other"
assert run("1\n1 1\n") == "1", "single bottle only opens itself"
assert run("2\n1 2\n2 1\n") == "0", "two bottles open each other"
assert run("5\n1 2\n2 2\n3 1\n4 5\n5 4\n") == "1", "one bottle cannot be opened by any other"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 bottles in cycle | 0 | All bottles can open another, no unopenable bottles |
| Single bottle | 1 | Smallest input, self-opening does not count |
| Two bottles open each other | 0 | Symmetric openable scenario |
| Mix with one isolated | 1 | Correctly identifies the bottle nobody can open |

## Edge Cases

A scenario where all bottles open only themselves:

```
3
1 1
2 2
3 3
```

Each bottle is checked against the others. None of the bottles has `b[j] == a[i]` for `i != j`, so all are unopenable. The output is `3`.

A scenario with one bottle that can open everyone else but no one can open it:

```
3
1 2
2 3
3 1
```

Bottle 0 is opened by bottle 2, bottle 1 by bottle 0, bottle 2 by bottle 1. The algorithm correctly identifies `can_be_opened = True` for all bottles, producing output `0`.

This confirms the algorithm handles self-opening correctly and does not count it as "openable by others."
