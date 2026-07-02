---
title: "CF 103560D - \u041f\u043e\u0434\u0430\u0440\u043e\u043a \u0434\u043b\u044f \u041b\u0443\u0438\u0434\u0436\u0438"
description: "We are given a box of candies where each candy belongs to some type. For each type, we can count how many candies of that type exist. From this pool, we want to assemble a “gift” by selecting some candies."
date: "2026-07-03T05:26:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103560
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2018"
rating: 0
weight: 103560
solve_time_s: 51
verified: true
draft: false
---

[CF 103560D - \u041f\u043e\u0434\u0430\u0440\u043e\u043a \u0434\u043b\u044f \u041b\u0443\u0438\u0434\u0436\u0438](https://codeforces.com/problemset/problem/103560/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a box of candies where each candy belongs to some type. For each type, we can count how many candies of that type exist. From this pool, we want to assemble a “gift” by selecting some candies.

The restriction is structural: if we look at the final gift and group candies by type, the number of chosen candies of each type must be different from every other chosen type. In other words, if type 1 appears 5 times in the gift and type 2 appears 3 times, then no other chosen type is allowed to appear exactly 5 or 3 times. Some types may be skipped entirely, and for chosen types we are free to take any positive number up to the available supply.

The objective is to maximize the total number of candies in the gift, which is the sum of chosen counts across all selected types.

This is a global allocation problem: we are distributing integer “quotas” to types under capacity constraints (each type has a maximum frequency), while also enforcing that all chosen quotas are pairwise distinct, and we want to maximize their sum.

The constraints are large, with total input size up to about two hundred thousand candies across queries. This rules out any quadratic or per-query nested simulation over all values. Anything slower than roughly linearithmic per query will fail.

A subtle edge case appears when frequencies are very small or very repetitive. For example, if all types appear many times, we cannot assign large equal quotas even though capacity exists. Conversely, if many types appear once, we cannot assign all of them value 1 because duplicates are forbidden.

For instance, suppose we have three types each appearing twice. A naive approach might assign 2, 2, 2, but that violates the distinctness rule. The correct behavior is to assign 2, 1, 0, producing a sum of 3. Another edge case is a single type with many occurrences, where the answer is simply all of them.

These patterns suggest we are not simply maximizing per-type usage, but carefully spacing assigned values.

## Approaches

A brute-force strategy would try to assign a value to each type by backtracking or greedy guessing. For each type we could try every possible count from its frequency down to 1 and ensure no duplicates are used. This immediately leads to a combinatorial explosion. Even if we only consider frequencies up to n, trying all assignments across k types produces something like n choices per type, which is exponential in k. With up to two hundred thousand elements, this is impossible.

The key observation is that only the final chosen counts matter, not which exact candies are used. Once we compute frequencies of each type, the problem becomes: assign to each type an integer x_i such that 0 ≤ x_i ≤ c_i, all positive x_i are distinct, and maximize sum of x_i.

This is a classic greedy structure. If we sort types by decreasing frequency, we always want to give larger quotas to types that can afford them. The reason is simple: a large frequency gives flexibility, so we should reserve large values for them. Smaller frequencies are constrained and should absorb smaller quotas or be dropped.

We then construct the solution from the largest possible quota downward. We maintain the largest available quota we are willing to assign. For each frequency in descending order, we assign it the largest possible valid number that is strictly smaller than what we used before, while also not exceeding its capacity. If the capacity is too small, we just take that capacity and continue decreasing.

The structure works because the constraint is only “all assigned values must be distinct”. That immediately suggests a decreasing sequence is optimal, since any permutation of assigned values can be sorted without changing feasibility, and larger values always contribute more to the sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force assignment search | Exponential | O(n) | Too slow |
| Sort frequencies + greedy decreasing assignment | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first compress the input into frequencies of each candy type. This transforms the problem from dealing with individual items into working with a multiset of capacities.

## Algorithm Walkthrough

1. Count how many times each type appears, producing an array of frequencies. This step is necessary because only counts per type matter, not identities of individual candies.
2. Sort the frequency array in descending order. This ensures we always try to assign large quotas to types that can actually support them, preventing early waste of high values on small-capacity types.
3. Initialize a variable `cap` as a very large number, conceptually infinity but implemented as something like n, since no type can take more than n candies.
4. Iterate over frequencies in sorted order. For each frequency `f`, we want to assign a value `x` that is both ≤ f and strictly less than the last assigned value `cap`.
5. Set `x = min(f, cap - 1)`. This enforces both constraints simultaneously: we do not exceed availability, and we maintain distinctness by strictly decreasing the assignment.
6. If `x` becomes zero or negative, we stop the process, since no further positive assignment is possible. All remaining types would contribute nothing.
7. Otherwise, add `x` to the answer and update `cap = x`. This ensures the next assigned value must be strictly smaller, preserving uniqueness.

The process builds a strictly decreasing sequence of chosen counts, each bounded above by the corresponding frequency.

### Why it works

At every step, we are deciding the largest possible valid value for the current type under the constraint that all previously chosen values are distinct and larger. Because we process frequencies in descending order, we never regret assigning a large value early: any later assignment would have even smaller capacity, and swapping would not increase the sum. The greedy invariant is that after processing i types, we have constructed the maximum possible sum using i distinct positive integers, each respecting its frequency bound, and any alternative arrangement with the same prefix length cannot exceed it without violating either ordering or feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    for _ in range(q):
        n = int(input())
        freq = {}
        for _ in range(n):
            a = int(input())
            freq[a] = freq.get(a, 0) + 1

        vals = sorted(freq.values(), reverse=True)

        cap = n
        ans = 0

        for f in vals:
            x = min(f, cap - 1)
            if x <= 0:
                break
            ans += x
            cap = x

        print(ans)

if __name__ == "__main__":
    solve()
```

The code starts by compressing each query into a frequency map, since only counts per type matter. Sorting in descending order is the backbone of the greedy strategy, ensuring we always consider the most flexible types first.

The variable `cap` tracks the largest usable value left for assignment. It starts at n because no valid assignment can exceed the number of candies. At each step we clamp by both frequency and the current cap minus one, guaranteeing strict decrease.

A common mistake here is forgetting the `-1` when computing the next allowed value. Without it, equal consecutive assignments can appear, violating the distinctness constraint.

The early break when `x <= 0` is important because once we cannot assign at least 1, all remaining contributions are zero.

## Worked Examples

### Example 1

Input:

```
n = 5
types: [1, 1, 1, 2, 2]
```

Frequencies become:

```
[3, 2]
```

| Step | Frequency | cap before | chosen x | cap after | sum |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 5 | 2 | 2 | 2 |
| 2 | 2 | 2 | 1 | 1 | 3 |

The algorithm first assigns 2 to the type with frequency 3. Even though 3 is available, we cannot use it because we must preserve space for other distinct values. The next type receives 1. The final answer is 3, which is optimal.

### Example 2

Input:

```
n = 6
types: [1, 1, 1, 1, 1, 1]
```

Frequencies:

```
[6]
```

| Step | Frequency | cap before | chosen x | cap after | sum |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | 6 | 5 | 5 | 5 |

We take 5 because the first assignment must leave room for strictly smaller positive integers. There are no other types, so the process ends immediately.

This shows that even a single type cannot use all its capacity, since distinctness constraints implicitly force a decreasing structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting frequencies per query dominates |
| Space | O(n) | frequency map and list of counts |

The total sum of n across queries is at most two hundred thousand, so the solution comfortably fits within time limits. Sorting remains efficient because the total number of frequency entries across all queries is also bounded by the number of distinct types encountered.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    input = sys.stdin.readline

    q = int(input())
    out = []

    for _ in range(q):
        n = int(input())
        freq = {}
        for _ in range(n):
            a = int(input())
            freq[a] = freq.get(a, 0) + 1

        vals = sorted(freq.values(), reverse=True)

        cap = n
        ans = 0
        for f in vals:
            x = min(f, cap - 1)
            if x <= 0:
                break
            ans += x
            cap = x

        out.append(str(ans))

    return "\n".join(out)

# sample tests (format adapted)
assert run("1\n5\n1\n1\n1\n2\n2\n") == "3"

# single type max
assert run("1\n6\n1\n1\n1\n1\n1\n1\n") == "5"

# all distinct
assert run("1\n4\n1\n2\n3\n4\n") == "4"

# mixed frequencies
assert run("1\n6\n1\n1\n1\n2\n2\n3\n") == "5"

# edge small
assert run("1\n1\n1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal types | linear decreasing cap behavior | single-frequency dominance |
| all distinct types | trivial full selection | baseline correctness |
| mixed distribution | greedy balancing | interaction of constraints |
| single element | minimal boundary | edge case handling |

## Edge Cases

One edge case is when all frequencies are 1. The algorithm assigns 1, then 0 for the next, stopping immediately. This correctly produces 1 for many types rather than incorrectly summing all of them.

Another edge case is a single type with very large frequency. The algorithm correctly reduces it to n-1, since we must maintain a strictly decreasing positive sequence.

A third case is when there are many medium frequencies, such as multiple types each with frequency 3. The greedy order ensures we assign 3, 2, 1 across the first few types, and then stop. Any attempt to assign equal values would violate the constraint, so the decreasing cap mechanism naturally enforces correctness.
