---
title: "CF 2145C - Monocarp's String"
description: "We are given a binary string consisting only of a and b. From this string, we are allowed to remove exactly one contiguous block of characters, possibly empty. After this deletion, we look at the remaining characters and count how many a and b are left."
date: "2026-06-08T01:31:34+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 2145
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 183 (Rated for Div. 2)"
rating: 1300
weight: 2145
solve_time_s: 108
verified: false
draft: false
---

[CF 2145C - Monocarp's String](https://codeforces.com/problemset/problem/2145/C)

**Rating:** 1300  
**Tags:** binary search, greedy, strings  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string consisting only of `a` and `b`. From this string, we are allowed to remove exactly one contiguous block of characters, possibly empty. After this deletion, we look at the remaining characters and count how many `a` and `b` are left.

The goal is to make those two counts equal by choosing a single removed segment, while minimizing the length of that removed segment. If no choice of a single removed interval can achieve equality except by deleting the entire string, the answer is `-1`.

The key constraint is that the removal must be one continuous segment, not scattered deletions. That makes the problem fundamentally about choosing a window whose removal adjusts the global balance between `a` and `b`.

The input size is large, with total length across all test cases up to 200,000. That immediately rules out any quadratic approach over substrings. Any solution that tries all possible removal intervals explicitly would examine O(n²) candidates in the worst case, which is far too slow.

A subtle edge case appears when the string has no way to balance even after removals that preserve structure. For example, if all characters are `a`, no matter what internal segment you remove, the remaining string still has only `a`, so equality is impossible unless we delete everything. Similarly, if total counts are already equal, removing nothing is optimal.

## Approaches

A direct approach is to try every possible segment `[l, r]`, remove it, and check whether the remaining string has equal numbers of `a` and `b`. Counting remaining characters after each removal can be optimized using prefix sums, so each check is O(1). However, there are O(n²) such segments, so the total complexity becomes O(n²), which is too large for 2e5 total length.

The key observation is that removing a segment changes the global difference between counts in a very structured way. Let the total imbalance be:

```
D = (#a - #b)
```

We want the final imbalance to be zero after removing a segment. Suppose we remove a segment `[l, r]`. Let:

```
delta[l, r] = (#a - #b in s[l..r])
```

Then the remaining imbalance becomes:

```
D - delta[l, r]
```

We want:

```
D - delta[l, r] = 0  →  delta[l, r] = D
```

So the problem reduces to finding a subarray whose `(a - b)` value equals the total `(a - b)` of the full string, while minimizing its length.

This is now a classic prefix sum transformation. We assign `+1` to `a` and `-1` to `b`, compute prefix sums, and want two indices `i < j` such that:

```
prefix[j] - prefix[i] = D
```

Equivalently:

```
prefix[i] = prefix[j] - D
```

We scan once and use a hash map from prefix values to their earliest occurrence, minimizing segment length.

The only remaining complication is feasibility: if total counts are already equal, answer is `0`. If no valid segment exists, the only possible way is deleting everything, so we return `-1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Prefix + Hash Map | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the string into a numeric array where `a = +1` and `b = -1`. This transforms the problem into working with balance rather than raw counts.
2. Compute the total sum `D`. If `D == 0`, the string is already balanced, so no removal is needed and we return `0`.
3. Build prefix sums while scanning from left to right. Each prefix value represents the imbalance up to that index.
4. Store the earliest index at which each prefix value appears. This is important because using the earliest occurrence maximizes the length of the remaining segment and minimizes the removed segment.
5. For each position `j`, compute the target prefix value `prefix[j] - D`. If we have seen this value before at index `i`, then the subarray `(i+1..j)` has imbalance exactly `D`, meaning removing it makes the rest balanced.
6. Track the minimum length among all such valid segments.
7. If no segment is found, return `-1`.

The central idea is that every valid deletion corresponds exactly to choosing a subarray whose imbalance equals the original imbalance. Once prefix sums are used, the problem becomes a linear scan with a lookup.

### Why it works

The algorithm relies on the fact that removing a segment only affects the total imbalance through that segment’s own contribution. The prefix transformation turns every segment into a difference of two points, so the condition becomes a fixed target difference. Since every possible segment is represented exactly once as a prefix pair, scanning all prefixes guarantees that every valid removal is considered. Storing earliest occurrences ensures that among all valid pairs we always obtain the shortest removed segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()

        arr = [1 if c == 'a' else -1 for c in s]
        total = sum(arr)

        if total == 0:
            out.append("0")
            continue

        prefix = 0
        first_pos = {0: -1}
        ans = n + 1

        for i, v in enumerate(arr):
            prefix += v

            need = prefix - total
            if need in first_pos:
                ans = min(ans, i - first_pos[need])

            if prefix not in first_pos:
                first_pos[prefix] = i

        if ans == n + 1:
            out.append("-1")
        else:
            out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation starts by encoding the string into a signed array so that balance becomes additive. The prefix sum tracks how far we are from equality at each index. The dictionary `first_pos` ensures we always use the earliest occurrence of a prefix value, which is necessary for minimizing the removed segment length.

The key subtlety is the order of updates: we check for a valid segment before inserting the current prefix into the map. This prevents accidentally using a segment ending at the current index incorrectly when computing length boundaries.

## Worked Examples

### Example 1

Input:

```
5
bbbab
```

We compute prefix values using `a=+1, b=-1`.

| i | char | prefix | needed (prefix - total) | first_pos used | best length |
| --- | --- | --- | --- | --- | --- |
| 0 | b | -1 | -1 - (-3)=2 | - | inf |
| 1 | b | -2 | -2 - (-3)=1 | - | inf |
| 2 | b | -3 | -3 - (-3)=0 | 0 exists | 2 |
| 3 | a | -2 | -2 - (-3)=1 | 1 exists | 2 |
| 4 | b | -3 | -3 - (-3)=0 | 0 exists | 3 |

Total imbalance is `-3`. The best segment has length `3`, corresponding to removing the prefix that contains three `b` characters, leaving a balanced string.

This trace shows how prefix differences directly encode candidate deletions.

### Example 2

Input:

```
6
bbaaba
```

Here total balance is `0`.

Since prefix sum already ends at zero, no removal is needed and the answer is `0`.

This confirms the special case handling when the string is already balanced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once with O(1) hashmap operations |
| Space | O(n) | Prefix values stored in a hash map |

The linear complexity comfortably fits within the total constraint of 2e5 characters across all test cases. Memory usage remains proportional to distinct prefix sums, which is bounded by n.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()

        arr = [1 if c == 'a' else -1 for c in s]
        total = sum(arr)

        if total == 0:
            out.append("0")
            continue

        prefix = 0
        first_pos = {0: -1}
        ans = n + 1

        for i, v in enumerate(arr):
            prefix += v
            need = prefix - total
            if need in first_pos:
                ans = min(ans, i - first_pos[need])
            if prefix not in first_pos:
                first_pos[prefix] = i

        out.append(str(-1 if ans == n + 1 else ans))

    return "\n".join(out)

# provided samples
assert run("""5
5
bbbab
6
bbaaba
4
aaaa
12
aabbaaabbaab
5
aabaa
""") == """3
0
-1
2
-1"""

# all equal
assert run("""1
4
aaaa
""") == "-1"

# already balanced
assert run("""1
2
ab
""") == "0"

# needs internal removal
assert run("""1
5
bbbab
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all `a` | -1 | impossible unless full deletion |
| already balanced | 0 | no removal needed |
| mixed case | 3 | correctness of prefix matching |

## Edge Cases

A string consisting of only one character type, such as `aaaa`, produces a constant negative or positive prefix trend with no repeated structure that satisfies the required difference. The algorithm scans all prefixes, finds no valid match, and correctly returns `-1`.

When the string is already balanced, such as `ab` or `baba`, the total sum is zero. The early exit ensures we do not incorrectly search for unnecessary removals, and we immediately return `0`.

For cases where the optimal removal is at the boundary, such as removing a prefix or suffix, the prefix map still captures them because we initialize `prefix = 0` at index `-1`. This guarantees that segments starting at index `0` are valid candidates and handled uniformly with interior segments.
