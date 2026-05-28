---
title: "CF 158B - Taxi"
description: "We have a collection of schoolchildren organized into groups, and each group wants to travel together in a taxi. Each group has between one and four children, and each taxi can carry at most four children."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 158
codeforces_index: "B"
codeforces_contest_name: "VK Cup 2012 Qualification Round 1"
rating: 1100
weight: 158
solve_time_s: 81
verified: true
draft: false
---

[CF 158B - Taxi](https://codeforces.com/problemset/problem/158/B)

**Rating:** 1100  
**Tags:** *special, greedy, implementation  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of schoolchildren organized into groups, and each group wants to travel together in a taxi. Each group has between one and four children, and each taxi can carry at most four children. The goal is to determine the minimum number of taxis required to transport all groups while respecting that groups cannot be split across taxis, though multiple groups can share a taxi if their combined size does not exceed four.

The input consists of the number of groups, followed by the size of each group. The output is a single integer representing the minimum number of taxis needed.

The key constraints are that there can be up to 100,000 groups, and the time limit is three seconds. This implies we cannot afford anything worse than linear time with respect to the number of groups. Quadratic or naive approaches that attempt all combinations of groupings will be too slow, because the number of possible combinations grows exponentially with the number of groups.

Edge cases to consider include scenarios where all groups are of size four, which will force one taxi per group, and scenarios where all groups are of size one, which allows perfect packing into taxis of four. Another subtle case is a mix of group sizes such that greedy packing is non-trivial-for example, a group of three and a group of two cannot fit together, so order of combination matters.

## Approaches

A brute-force approach would attempt to try all permutations of the groups and try to pack them into taxis in all possible orders. This is correct because it explores every configuration, but it is computationally infeasible for n up to 100,000. Even if each permutation check were linear, the factorial growth of permutations makes it impossible.

The key insight is that the groups have only four possible sizes. This limited range allows a frequency-based approach. We can count how many groups there are of each size and combine them optimally. Groups of size four always occupy a taxi on their own. Groups of size three can be paired with groups of size one if available. Groups of size two can be paired with another group of size two or with up to two groups of size one. Finally, leftover groups of size one can be combined in fours. The structure of the problem allows a greedy strategy: handle the largest groups first and fill remaining space with smaller groups. This guarantees minimal taxis because larger groups are the limiting factor and smaller groups can be used to fill gaps without violating constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal (frequency + greedy) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many groups there are of each size from 1 to 4. This gives us a small frequency table we can use for greedy decisions.
2. Each group of size four requires a separate taxi. Increment the taxi counter by the number of size-four groups.
3. Pair each group of size three with a group of size one if possible. For each pair, increment the taxi counter and decrement the count of size-one groups accordingly. If there are not enough size-one groups, the groups of size three still occupy a taxi individually.
4. Pair groups of size two together. Each pair of size-two groups fits exactly in a taxi. If an odd group of size two remains, it can be paired with up to two groups of size one. Increment the taxi counter and decrement size-one groups accordingly. If no size-one groups remain, the single group of size two occupies a taxi alone.
5. Finally, handle remaining size-one groups. They can share taxis four per taxi. Compute the number of taxis as the ceiling of the count of leftover ones divided by four.
6. The sum of all taxis calculated in these steps gives the minimum number of taxis required.

Why it works: the invariant is that at each step, we are maximally filling taxis with the largest remaining groups and only then using smaller groups to fill gaps. Because the group sizes are constrained to 1 through 4, there is no configuration where combining differently would reduce the total number of taxis, making this greedy approach optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
sizes = list(map(int, input().split()))

count = [0] * 5  # index 0 unused
for s in sizes:
    count[s] += 1

taxis = 0

# size 4 groups
taxis += count[4]

# size 3 groups + size 1 groups
pair_3_1 = min(count[3], count[1])
taxis += pair_3_1
count[3] -= pair_3_1
count[1] -= pair_3_1

# remaining size 3 groups
taxis += count[3]

# size 2 groups
taxis += count[2] // 2
if count[2] % 2:
    taxis += 1
    count[1] -= min(2, count[1])

# size 1 groups
if count[1] > 0:
    taxis += (count[1] + 3) // 4  # ceil division

print(taxis)
```

The code initializes a frequency array for groups of each size. It counts taxis needed for groups of four directly, then pairs threes with ones to optimize space usage. Remaining threes and twos are processed carefully, with leftover ones filling taxis last. Ceiling division handles leftover ones efficiently, and all operations are constant-time except for the initial counting, giving linear time complexity.

## Worked Examples

### Example 1

Input: `5 1 2 4 3 3`

| Step | count[1] | count[2] | count[3] | count[4] | taxis | Explanation |
| --- | --- | --- | --- | --- | --- | --- |
| initial | 1 | 1 | 2 | 1 | 0 | count sizes |
| size 4 | 1 | 1 | 2 | 1 | 1 | group of 4 takes taxi |
| pair 3&1 | 0 | 1 | 1 | 1 | 2 | pair one group of 3 with one group of 1 |
| remaining 3 | 0 | 1 | 1 | 1 | 3 | remaining 3 occupies taxi |
| pair 2&2 | 0 | 1 | 1 | 1 | 3 | only one 2, will handle next |
| leftover 2 + ones | 0 | 1 | 1 | 1 | 4 | remaining 2 takes taxi; no ones to pair |
| leftover 1 | 0 | 1 | 1 | 1 | 4 | no ones left |

The output is 4, matching the sample.

### Example 2

Input: `8 1 1 1 1 2 2 3 4`

| Step | count[1] | count[2] | count[3] | count[4] | taxis | Explanation |
| --- | --- | --- | --- | --- | --- | --- |
| initial | 4 | 2 | 1 | 1 | 0 | count sizes |
| size 4 | 4 | 2 | 1 | 1 | 1 | taxi for 4 |
| pair 3&1 | 3 | 2 | 0 | 1 | 2 | 3 paired with 1 |
| remaining 2 | 3 | 2 | 0 | 1 | 3 | two 2's form a taxi |
| leftover 1 | 3 | 0 | 0 | 1 | 4 | remaining 3 ones need one taxi |

Output: 4. The trace demonstrates the algorithm correctly handles multiple pairings and leftover ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to count sizes, then constant-time operations to compute taxis |
| Space | O(1) | Frequency array of size 5 independent of n |

Linear time is acceptable for n up to 100,000, and constant space ensures memory limits are satisfied.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    sizes = list(map(int, input().split()))
    count = [0] * 5
    for s in sizes:
        count[s] += 1
    taxis = 0
    taxis += count[4]
    pair_3_1 = min(count[3], count[1])
    taxis += pair_3_1
    count[3] -= pair_3_1
    count[1] -= pair_3_1
    taxis += count[3]
    taxis += count[2] // 2
    if count[2] % 2:
        taxis += 1
        count[1] -= min(2, count[1])
    if count[1] > 0:
        taxis += (count[1] + 3) // 4
    return str(taxis)

# Provided sample
assert run("5\n1 2 4 3 3\n") == "4", "sample 1"

# Custom cases
assert run("4\n4 4 4 4\n") == "4", "all size 4"
assert run("8\n1 1 1 1 2 2 3 4\n") == "4", "mixed sizes"
assert run("5\n1 1 1
```
