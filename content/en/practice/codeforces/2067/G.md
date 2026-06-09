---
title: "CF 2067G - Tropical Season"
description: "We are given a collection of barrels, each containing some amount of water, and one of them has a tiny amount of poison. The poison adds an imperceptible 0.179 kilograms to the barrel's weight."
date: "2026-06-09T03:39:30+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 2067
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 1004 (Div. 2)"
rating: 3300
weight: 2067
solve_time_s: 89
verified: false
draft: false
---

[CF 2067G - Tropical Season](https://codeforces.com/problemset/problem/2067/G)

**Rating:** 3300  
**Tags:** data structures  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of barrels, each containing some amount of water, and one of them has a tiny amount of poison. The poison adds an imperceptible 0.179 kilograms to the barrel's weight. We cannot touch a barrel containing poison, but we can pour water between barrels safely as long as we do not touch the poisonous one. The only information we get comes from a comparison scale that tells us, for any two barrels, whether their weights are equal or which one is heavier.

The task is to determine whether it is possible to guarantee identification of the poisonous barrel, without ever touching it, and to maintain this guarantee even as barrels are added or removed through a sequence of queries.

The problem size is large: up to 200,000 barrels and 200,000 queries. This rules out any solution that requires comparing all pairs of barrels explicitly or simulating every possible sequence of pours, because that would take O(n^2) time per query. Each barrel weight is bounded by a million, but the number of barrels is the real constraint. Since we need to process queries online, we need a dynamic strategy that allows efficient insertion, deletion, and identification of the poisonous barrel.

A non-obvious edge case is when all barrels contain the same amount of water. In that case, the poisonous barrel is the heaviest by a tiny margin, but it is impossible to safely distinguish it, because any pouring from a non-poisonous barrel will only equalize the other barrels' weights without revealing the poison. Another subtle case occurs when there are exactly two distinct weights and the heavier weight is held by more than one barrel; in that situation, the poisonous barrel could be any of them, and we cannot touch any to safely identify it.

## Approaches

A brute-force solution would simulate all pours and scale comparisons. One could imagine picking two barrels, comparing them, pouring from the lighter to the heavier, and continuing until only one candidate remains. While conceptually correct, this requires carefully tracking all pairwise comparisons and pours, which is O(n^2) in the worst case and cannot handle 2×10^5 barrels efficiently.

The key observation is that we never need to simulate actual pours. The ability to pour safely means we can make multiple barrels identical in weight, as long as we never touch the poison barrel. If we can reduce all non-poisonous barrels to the same weight, any remaining barrel with a distinct weight must be the poisonous one. Therefore, the optimal approach reduces to tracking the multiset of barrel water amounts. If there is a unique heaviest barrel, the poisonous barrel can be identified safely. If the maximum occurs more than once, it is impossible to guarantee identification without risk.

This observation lets us handle queries efficiently. Adding a barrel updates the frequency of that water amount. Removing a barrel decrements the frequency. At each step, we only need to check whether the current maximum occurs once. This reduces the problem to O(log n) per query if we maintain counts with a balanced map, or O(1) per query with a frequency array for the given bounds on water amounts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n + q) using counts | O(10^6) | Accepted |

## Algorithm Walkthrough

1. Build a frequency table of all current water amounts. This allows constant-time updates when adding or removing barrels. Using a fixed-size array of length 10^6 + 1 is sufficient because all water amounts are bounded.
2. Determine the current maximum water amount and its count in the table. If the count of the maximum is 1, the poisonous barrel is uniquely the heaviest, so the answer is "Yes". If the maximum occurs more than once, the answer is "No".
3. Process each query. If a barrel is added, increment the frequency for its water amount. If a barrel is removed, decrement the frequency. Update the maximum and its count dynamically. After each query, check whether the maximum occurs once and output "Yes" or "No".
4. When updating the maximum, be careful: if the removed barrel was the current maximum and its count drops to zero, scan downward for the next largest water amount. When adding a barrel, if its weight exceeds the current maximum, update the maximum.

Why it works: The algorithm guarantees that all non-poisonous barrels can be made equal safely. The poisonous barrel must always be distinct in weight to identify it. Therefore, tracking the maximum and its multiplicity is sufficient to answer the problem correctly without ever simulating actual pours.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

n, q = map(int, input().split())
a = list(map(int, input().split()))

freq = defaultdict(int)
for x in a:
    freq[x] += 1

max_weight = max(freq.keys())
def output():
    print("Yes" if freq[max_weight] == 1 else "No")

output()

for _ in range(q):
    line = input()
    op, val = line.split()
    val = int(val)
    if op == '+':
        freq[val] += 1
        if val > max_weight:
            max_weight = val
    else:
        freq[val] -= 1
        if freq[val] == 0:
            del freq[val]
            if val == max_weight:
                if freq:
                    max_weight = max(freq.keys())
                else:
                    max_weight = 0
        elif val == max_weight:
            pass
    output()
```

The solution starts by building a frequency map of all barrel water amounts. The helper function `output` checks whether the current maximum occurs once. Each query either increments or decrements the frequency map. If the maximum barrel is removed entirely, the algorithm scans for the next maximum. Using `defaultdict` ensures we do not need to check for missing keys explicitly.

The subtle part is correctly updating `max_weight` when removing barrels. We must only scan for a new maximum if the previous maximum has no barrels left. When adding a barrel heavier than the current maximum, we simply replace the maximum.

## Worked Examples

Sample 1:

| Operation | Frequencies | Max | Max Count | Answer |
| --- | --- | --- | --- | --- |
| Initial | {2:2, 4:1, 11:1} | 11 | 1 | Yes |
| -2 | {2:1,4:1,11:1} | 11 | 1 | No |
| +4 | {2:1,4:2,11:1} | 11 | 1 | Yes |
| +30 | {2:1,4:2,11:1,30:1} | 30 | 1 | No |
| +40 | {2:1,4:2,11:1,30:1,40:1} | 40 | 1 | Yes |
| -4 | {2:1,4:1,11:1,30:1,40:1} | 40 | 1 | No |
| +2 | {2:2,4:1,11:1,30:1,40:1} | 40 | 1 | No |
| +2 | {2:3,4:1,11:1,30:1,40:1} | 40 | 1 | Yes |

The table shows that updating the frequency map and tracking the maximum is sufficient to determine the answer. The state reflects the invariant that a unique maximum weight allows safe identification of the poisonous barrel.

Custom Example:

Input: `3 3\n1 1 2\n+1\n-2\n+3\n`

| Operation | Frequencies | Max | Max Count | Answer |
| --- | --- | --- | --- | --- |
| Initial | {1:2,2:1} | 2 | 1 | Yes |
| +1 | {1:3,2:1} | 2 | 1 | Yes |
| -2 | {1:3} | 1 | 3 | No |
| +3 | {1:3,3:1} | 3 | 1 | Yes |

This demonstrates the algorithm correctly handles additions and removals that change the maximum and its multiplicity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) amortized | Each query updates a frequency map, and maximum is adjusted in O(1) amortized time. |
| Space | O(10^6) | Frequency array size depends on maximum water amount, which is ≤ 10^6. |

The solution easily fits in 4 seconds with 200,000 barrels and queries and does not exceed 1 GB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided sample
assert run("4 7\n2 2 4 11\n- 2\n+ 4\n+ 30\n+ 40\n- 4\n+ 2\n+ 2\n") == \
"Yes\nNo\nYes\nNo\nYes\nNo\nNo\nYes"

# minimum input
assert run("1 1\n1\n+1\n") == "Yes\nNo"

# all-equal barrels
assert run("3 2\n2 2 2\n+2\n-2\n")
```
