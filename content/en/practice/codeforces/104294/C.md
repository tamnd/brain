---
title: "CF 104294C - Attack on Titans"
description: "We are given three separate sequences, each representing the section heights of a wall. Every wall has the same number of sections, but the ordering is irrelevant for the task. What matters is only which heights appear in each wall at least once."
date: "2026-07-01T20:23:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104294
codeforces_index: "C"
codeforces_contest_name: "UTPC Spring 2023 Open Contest"
rating: 0
weight: 104294
solve_time_s: 70
verified: true
draft: false
---

[CF 104294C - Attack on Titans](https://codeforces.com/problemset/problem/104294/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three separate sequences, each representing the section heights of a wall. Every wall has the same number of sections, but the ordering is irrelevant for the task. What matters is only which heights appear in each wall at least once.

The goal is to find the largest height value that appears in all three walls simultaneously. In other words, we are searching for a value that exists somewhere in the first array, somewhere in the second array, and somewhere in the third array, and among all such values we want the maximum one. If no such value exists, the answer is defined to be -1.

The constraints allow up to 100000 elements per wall, and each height is at most 100000. This immediately rules out any approach that compares every pair or triple of elements directly. A cubic or even quadratic strategy would involve up to 10^10 operations in the worst case, which is far beyond what fits in 2 seconds in Python. Even sorting each array is fine, but repeated scanning or nested membership checks against Python lists would become too slow if done repeatedly.

The main subtlety is that duplicates do not matter beyond existence. If a height appears multiple times in a wall, it still contributes only one logical presence. Another edge case is when the intersection is empty. For example, if the three arrays are disjoint like [1], [2], [3], the correct output is -1, and any implementation that initializes a candidate answer to 0 would incorrectly return 0 if not careful.

## Approaches

A direct approach is to treat this as a membership intersection problem. For every value in the first wall, we could check whether it appears in the second and third walls. This is correct because it explicitly tests the condition of existence in all three sets. However, naive membership checks in lists cost O(n), so for each of up to n elements in the first array, we might scan two additional arrays. This leads to O(n^2) behavior per test case, which would be around 10^10 operations in the worst case, which is too slow.

The key observation is that we do not need positional information or multiplicity, only whether a value exists. This allows us to convert each array into a set of distinct values. Once we do that, checking membership becomes O(1) average time. The problem then reduces to computing the intersection of three sets and selecting the maximum element from the result. Since the values are bounded by 100000, we can also directly mark presence using boolean arrays, but set intersection is simpler and sufficiently fast.

The brute-force approach works conceptually because it directly tests all candidates, but fails under time constraints due to repeated linear scans. The set-based approach reduces each membership check to constant time, turning the problem into a linear scan over at most n values per set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Using sets | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the three arrays representing the wall sections. The ordering of values is irrelevant, so we focus only on presence.
2. Convert each array into a set. This removes duplicates and prepares fast membership checks. This step ensures that future lookups for existence in a wall are O(1) on average.
3. Iterate over the smallest of the three sets, since any valid common height must appear there as well. For each candidate value, check whether it exists in the other two sets.
4. Maintain a variable that tracks the maximum valid height found so far. Each time we find a value present in all three sets, we compare it with the current maximum and update it if it is larger.
5. After checking all candidates, output the maximum value found. If no value was ever valid, output -1.

Why it works: the algorithm relies on the fact that every valid answer must belong to the intersection of the three sets. By restricting the search space to one set and verifying membership in the others, we ensure completeness without missing any candidate. The invariant maintained is that at any point, the current best value is the maximum among all intersection elements seen so far.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
m = list(map(int, input().split()))
r = list(map(int, input().split()))
s = list(map(int, input().split()))

set_m = set(m)
set_r = set(r)
set_s = set(s)

ans = -1

for x in set_m:
    if x in set_r and x in set_s:
        if x > ans:
            ans = x

print(ans)
```

The solution reads the three arrays and immediately converts them into sets, since only presence matters. The loop over `set_m` ensures we only consider distinct candidate heights once. Each membership test against `set_r` and `set_s` runs in average constant time, which keeps the solution linear overall. The answer variable starts at -1 to correctly handle the case where no intersection exists.

A common mistake would be iterating over the original arrays instead of sets, which can lead to redundant checks. Another subtle issue is initializing `ans` to 0, which would be incorrect if all values are negative in a variant problem, but here it is safe only because the problem guarantees positive heights; still, -1 is the correct sentinel for “no intersection”.

## Worked Examples

### Example 1

Input:

```
n = 5
m = [1, 2, 3, 8, 5]
r = [5, 6, 7, 8, 9]
s = [8, 12, 14, 19, 12]
```

After converting to sets:

```
set_m = {1, 2, 3, 5, 8}
set_r = {5, 6, 7, 8, 9}
set_s = {8, 12, 14, 19}
```

We iterate over `set_m`:

| x | in set_r | in set_s | candidate |
| --- | --- | --- | --- |
| 1 | no | no | skip |
| 2 | no | no | skip |
| 3 | no | no | skip |
| 5 | yes | no | skip |
| 8 | yes | yes | 8 |

Final answer is 8.

This confirms that the algorithm correctly identifies only values present in all three sets and selects the maximum among them.

### Example 2

Input:

```
m = [4, 4, 2]
r = [1, 2, 3]
s = [2, 9, 10]
```

Sets:

```
set_m = {2, 4}
set_r = {1, 2, 3}
set_s = {2, 9, 10}
```

| x | in set_r | in set_s | candidate |
| --- | --- | --- | --- |
| 2 | yes | yes | 2 |
| 4 | no | no | skip |

Answer is 2.

This demonstrates that duplicates in input arrays do not affect correctness, since set conversion removes repetition automatically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each array is scanned once to build sets, then we iterate over one set with O(1) membership checks |
| Space | O(n) | we store up to n distinct values across three sets |

The constraints allow up to 100000 elements per array, so linear time and linear memory comfortably fit within limits in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    m = list(map(int, input().split()))
    r = list(map(int, input().split()))
    s = list(map(int, input().split()))

    set_m = set(m)
    set_r = set(r)
    set_s = set(s)

    ans = -1
    for x in set_m:
        if x in set_r and x in set_s:
            ans = max(ans, x)

    return str(ans)

# provided sample
assert run("""5
1 2 3 8 5
5 6 7 8 9
8 12 14 19 12
""") == "8"

# all disjoint
assert run("""3
1 2 3
4 5 6
7 8 9
""") == "-1"

# single common value
assert run("""4
10 20 30 40
5 10 6 7
10 8 9 1
""") == "10"

# duplicates everywhere
assert run("""5
1 1 2 2 3
3 3 2 2 1
2 2 2 2 2
""") == "2"

# all same
assert run("""3
7 7 7
7 7 7
7 7 7
""") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Disjoint sets | -1 | no intersection case |
| Mixed overlap | 10 | correct max intersection |
| Heavy duplicates | 2 | deduplication correctness |
| Uniform values | 7 | full intersection case |

## Edge Cases

One edge case is when there is no common value at all. For example:

```
3
1 2 3
4 5 6
7 8 9
```

After conversion to sets, none of the elements of `set_m` appear in both `set_r` and `set_s`. The loop never updates `ans`, so it remains -1, which is correct.

Another case is when all arrays consist of the same repeated value:

```
3
5 5 5
5 5 5
5 5 5
```

All sets become `{5}`. The loop checks 5, confirms it exists in both other sets, and updates `ans` to 5. No other values exist, so the output remains 5.

A final subtle case is when duplicates are mixed with a single valid intersection value, such as:

```
5
1 1 1 2 2
3 2 2 2 4
2 5 6 2 7
```

Here, only 2 is common. Even though it appears multiple times, set conversion ensures it is evaluated once, and the algorithm correctly returns 2.
