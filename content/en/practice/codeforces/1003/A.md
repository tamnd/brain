---
title: "CF 1003A - Polycarp's Pockets"
description: "We are given a multiset of coin values, and we need to place every coin into a collection of “pockets” under a simple restriction: inside any single pocket, no value is allowed to repeat."
date: "2026-06-16T23:30:13+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1003
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 494 (Div. 3)"
rating: 800
weight: 1003
solve_time_s: 75
verified: true
draft: false
---

[CF 1003A - Polycarp's Pockets](https://codeforces.com/problemset/problem/1003/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of coin values, and we need to place every coin into a collection of “pockets” under a simple restriction: inside any single pocket, no value is allowed to repeat. Coins are indistinguishable except for their values, so the task is purely about how many copies of each value exist and how they can be separated across groups.

Each pocket behaves like a set of values, not a multiset. If a value appears multiple times in the input, those copies must be distributed across different pockets. The goal is to minimize how many such pockets are needed to accommodate all coins.

The constraint range is very small, with at most 100 coins and values also bounded by 100. This immediately tells us that any solution from quadratic time downwards is easily sufficient, and even direct counting approaches are safe without concern for performance.

The key edge behavior comes from duplicates. If all values are distinct, one pocket is enough. If all values are the same, each coin forces a separate pocket, since no pocket can contain two identical values. A subtle case is when several values repeat with different frequencies, because the limiting factor is not the total number of coins but the most frequent single value.

For example, if we had input like `1 1 2 2 3`, the value `1` appears twice and `2` also appears twice, forcing at least two pockets, even though the total size is larger than two. Any naive attempt that only considers total count or unique count would fail here.

## Approaches

A brute-force interpretation would try to actually simulate the packing process. One could repeatedly construct pockets by greedily placing coins while ensuring no duplicates within a pocket, removing used coins, and repeating until all coins are placed. This is correct because every step produces a valid grouping, and eventually all coins are assigned.

The issue is efficiency. Each time we build a pocket, we scan remaining coins and try to fit as many distinct values as possible. In the worst case, such as when all coins are identical or when many duplicates exist, we repeatedly process almost the full list. This leads to roughly O(n²) or worse behavior depending on implementation details, and although n is small here, this approach is conceptually unnecessary.

The key observation is that each distinct value with frequency f contributes exactly f “requirements” that must be placed into different pockets. Every pocket can accommodate at most one occurrence of each value, so if a value appears f times, we need at least f different pockets to place all its copies. This means the answer must be at least the maximum frequency of any value.

This bound is also sufficient. If we create as many pockets as the maximum frequency, we can distribute occurrences of each value across different pockets in a simple round-robin fashion. Since no value appears more times than the number of pockets, every occurrence can be placed without conflict.

This reduces the problem to a frequency counting task.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Packing | O(n²) | O(n) | Accepted but unnecessary |
| Frequency Count | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many times each coin value appears in the array. This captures all constraints in a compact form because only duplicates matter for conflicts.
2. Track the largest frequency among all values. This value represents the minimum number of pockets required so that even the most frequent value can be separated across different pockets.
3. Output this maximum frequency as the answer. Every other value automatically fits within these pockets because none of them appears more often than the chosen capacity.

### Why it works

Each pocket can contain at most one coin of a given value. Therefore, if some value appears f times, we need at least f distinct pockets to place all occurrences without repetition. Conversely, if we have k pockets where k equals the maximum frequency, we can assign the i-th occurrence of every value to pocket i. This guarantees no two identical values ever collide in the same pocket, and every coin is assigned exactly once.

The algorithm is correct because it transforms a packing constraint into a per-value capacity constraint and uses the tightest possible bound across all values.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

freq = [0] * 101

for x in a:
    freq[x] += 1

ans = max(freq)
print(ans)
```

The solution relies entirely on frequency counting. The array `freq` is sized to 101 because values are guaranteed to lie between 1 and 100. Each coin increments its corresponding bucket, and the final answer is simply the maximum bucket value.

There is no need for sorting or simulation. The logic hinges on the fact that constraints are independent across values except for sharing pockets, and the only shared limitation is that identical values must be separated.

## Worked Examples

### Example 1

Input:

```
6
1 2 4 3 3 2
```

Frequencies are:

| Value | Count |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 1 |

We only track the maximum count.

| Step | Value processed | freq state (partial) | max freq |
| --- | --- | --- | --- |
| 1 | 1 | 1:1 | 1 |
| 2 | 2 | 2:1 | 1 |
| 3 | 4 | 4:1 | 1 |
| 4 | 3 | 3:1 | 1 |
| 5 | 3 | 3:2 | 2 |
| 6 | 2 | 2:2 | 2 |

Final answer is 2.

This shows that duplicates determine the constraint, not total size.

### Example 2

Input:

```
5
5 5 5 5 1
```

| Value | Count |
| --- | --- |
| 5 | 4 |
| 1 | 1 |

| Step | Value processed | freq state | max freq |
| --- | --- | --- | --- |
| 1 | 5 | 5:1 | 1 |
| 2 | 5 | 5:2 | 2 |
| 3 | 5 | 5:3 | 3 |
| 4 | 5 | 5:4 | 4 |
| 5 | 1 | 1:1 | 4 |

Final answer is 4.

This demonstrates the worst-case behavior where a single value dictates the number of pockets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each coin is processed once to update frequency counts |
| Space | O(1) | Frequency array is fixed size (100 possible values) |

The solution comfortably fits within constraints since n is at most 100, and the operations are purely constant-time increments and a final scan over a fixed array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    freq = [0] * 101
    for x in a:
        freq[x] += 1
    return str(max(freq))

# provided sample
assert run("6\n1 2 4 3 3 2\n") == "2"

# all distinct
assert run("4\n1 2 3 4\n") == "1"

# all same
assert run("5\n7 7 7 7 7\n") == "5"

# mixed frequencies
assert run("7\n1 1 2 2 2 3 4\n") == "3"

# single element
assert run("1\n10\n") == "1"

# two high-frequency values
assert run("6\n5 5 6 6 6 5\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 4 | 1 | all distinct values |
| 7 7 7 7 7 | 5 | maximum repetition case |
| 1 1 2 2 2 3 4 | 3 | mixed frequency structure |
| 10 | 1 | minimum size input |

## Edge Cases

When all coins have unique values, every frequency is 1, so the maximum is 1 and only one pocket is required. The algorithm initializes all frequencies to zero and increments each once, leaving the maximum as 1, correctly producing a single pocket.

When all coins are identical, every increment hits the same bucket. For an input like `7 7 7 7`, the frequency of 7 becomes 4, and the algorithm outputs 4. This matches the fact that each identical coin must occupy a separate pocket due to the restriction.

When multiple values share the same maximum frequency, such as `1 1 2 2`, both values reach frequency 2. The maximum remains 2, and two pockets are sufficient. Each occurrence of 1 and 2 can be split across the two pockets without conflict, confirming that ties do not change the result beyond the maximum value itself.
