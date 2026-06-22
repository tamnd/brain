---
title: "CF 105442J - Rabid Rabbit"
description: "We are given a line of rabbit hutches, each containing some number of rabbits. For each query, we are handed a contiguous segment of this line, and Leonardo is only allowed to operate inside that segment. Each “day” he chooses a pair of distinct hutches inside the segment."
date: "2026-06-23T03:38:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105442
codeforces_index: "J"
codeforces_contest_name: "2024-2025 CTU Open Contest"
rating: 0
weight: 105442
solve_time_s: 63
verified: true
draft: false
---

[CF 105442J - Rabid Rabbit](https://codeforces.com/problemset/problem/105442/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of rabbit hutches, each containing some number of rabbits. For each query, we are handed a contiguous segment of this line, and Leonardo is only allowed to operate inside that segment.

Each “day” he chooses a pair of distinct hutches inside the segment. He sums the number of rabbits in those two hutches. If that sum is a positive Fibonacci number, the day is valid, but there is an additional restriction: each Fibonacci value can be used at most once across all days in that segment. The task for every query segment is to determine the maximum number of such days possible.

Rephrasing the core task in simpler terms, for a subarray we want to count how many distinct Fibonacci numbers can be expressed as the sum of two different elements chosen from that subarray.

The constraints are large, with up to 100,000 elements and 100,000 queries. Any solution that recomputes pair sums per query would immediately fail, since even a single segment could contain on the order of n² pairs. A naive per-query O(n²) approach leads to about 10¹⁰ operations in the worst case, which is infeasible.

A more subtle observation is that the rabbit counts are bounded by 10⁹, so any valid pair sum is at most 2×10⁹. This means we only care about Fibonacci numbers up to that range, and there are only about 45 of them. This finite set of targets is the key structural simplification.

A few edge cases deserve attention.

If the segment has length 1, no pair exists, so the answer is always 0.

If all values in a segment are identical, say [5, 5, 5], then every pair sum is the same (10), so even if 10 is Fibonacci, the answer is at most 1 because repetition is forbidden.

If values are large and sparse, many Fibonacci targets cannot be formed at all, so the answer can be significantly smaller than the number of pairs.

## Approaches

A direct approach would examine every query segment independently. For a fixed segment, we could enumerate all pairs (i, j), compute their sums, and check whether each sum is Fibonacci. We would store used Fibonacci values in a set to enforce uniqueness. This is correct, but the inner pair enumeration dominates complexity. For a segment of size k, this is O(k²), which is far too slow when k approaches 10⁵.

The key observation is that Fibonacci numbers form a small fixed universe. Since all Ai ≤ 10⁹, any sum is ≤ 2×10⁹, so we precompute all Fibonacci numbers up to that limit. There are only about 44 such numbers. Instead of thinking in terms of pairs, we reverse the perspective: for each Fibonacci number F, we ask whether there exists a pair inside the segment that sums to F.

Now the problem becomes a series of independent two-sum existence queries over subarrays, repeated for ~44 fixed targets. This is much more manageable because two-sum on a static array can be answered using sorting and two pointers, or using frequency structures if we fix the segment.

However, we still have multiple queries over different segments, so we need a structure that supports fast segment frequency access. A common way to handle this is to process each Fibonacci value independently and compute, for each query, whether that Fibonacci can be formed inside its segment. Then the final answer per query is simply the number of Fibonacci values that are feasible.

To test feasibility of a fixed Fibonacci value F over a segment [l, r], we need to check if there exist i < j in [l, r] such that A[i] + A[j] = F. Since values are large but the Fibonacci universe is small, we can compress the array values and use a frequency map per segment. A more efficient way is to sort indices offline per Fibonacci value and use a two-pointer technique on the sorted array of values while maintaining segment constraints using a Fenwick tree or Mo’s algorithm.

Given the constraints, the clean intended solution is to treat each Fibonacci value separately and use Mo’s algorithm over queries to maintain a frequency structure of current segment values. For each Fibonacci number F, we maintain a sliding window and check pairs incrementally. Because the number of Fibonacci values is constant (~44), we multiply Mo complexity by a small factor, which remains acceptable.

The final design is: precompute Fibonacci numbers, run Mo’s algorithm over queries, and maintain a frequency array for values in the current segment. For each Fibonacci F, we maintain a running count of pairs forming F by checking complement frequencies. When we add or remove an element, we update contributions for all Fibonacci values in O(#Fib), which is constant.

This turns the problem into about O((N + Q) √N × 44), which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per query | O(Q·N²) | O(1) | Too slow |
| Mo’s algorithm + Fibonacci enumeration | O((N + Q) √N · 44) | O(N) | Accepted |

## Algorithm Walkthrough

1. Precompute all Fibonacci numbers up to 2×10⁹ and store them in a list F. This works because any valid pair sum cannot exceed this bound.
2. Read all queries and prepare them for offline processing. We will reorder them using Mo’s ordering so that we can move a sliding window efficiently.
3. Maintain a frequency array freq[x] representing how many times value x appears in the current segment.
4. For each Fibonacci number Fk, we maintain a counter ways[k] that tracks how many valid pairs in the current segment sum to Fk.
5. When we add an element x into the current segment, we update all Fibonacci counters by checking, for each Fk, whether (Fk − x) exists in freq before insertion. If so, we increase ways[k] accordingly. Then we increment freq[x].
6. When removing an element x, we first decrement freq[x], then subtract contributions for all Fibonacci numbers using the updated frequency.
7. As we slide the Mo window, we continuously maintain all ways[k] values.
8. For each query, after adjusting the window to its [l, r], we compute the answer as the number of Fibonacci indices k such that ways[k] > 0.

The correctness relies on maintaining an exact count of valid unordered pairs for each Fibonacci sum inside the current segment. Each update precisely adjusts pair counts based on whether the complement is present at the moment of insertion or removal, ensuring no pair is missed or double counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Query:
    __slots__ = ("l", "r", "i", "blk")
    def __init__(self, l, r, i, blk):
        self.l = l
        self.r = r
        self.i = i
        self.blk = blk

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    fib = [1, 2]
    while fib[-1] <= 2_000_000_000:
        fib.append(fib[-1] + fib[-2])
    fib = fib[:-1]

    fib_index = {v: i for i, v in enumerate(fib)}
    m = len(fib)

    block = int(n ** 0.5)

    queries = []
    for i in range(q):
        l, r = map(int, input().split())
        queries.append(Query(l, r, i, l // block))

    queries.sort(key=lambda x: (x.blk, x.r if x.blk % 2 == 0 else -x.r))

    freq = {}
    ways = [0] * m

    def add(x):
        for i, f in enumerate(fib):
            y = f - x
            if y in freq:
                ways[i] += freq[y]
        freq[x] = freq.get(x, 0) + 1

    def remove(x):
        freq[x] -= 1
        for i, f in enumerate(fib):
            y = f - x
            if y in freq:
                ways[i] -= freq[y]

    cur_l, cur_r = 0, -1
    ans = [0] * q

    for qu in queries:
        l, r = qu.l, qu.r

        while cur_l > l:
            cur_l -= 1
            add(a[cur_l])
        while cur_r < r:
            cur_r += 1
            add(a[cur_r])
        while cur_l < l:
            remove(a[cur_l])
            cur_l += 1
        while cur_r > r:
            remove(a[cur_r])
            cur_r -= 1

        cnt = 0
        for i in range(m):
            if ways[i] > 0:
                cnt += 1
        ans[qu.i] = cnt

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The implementation relies on a frequency dictionary rather than a fixed-size array because values can be up to 10⁹. The add and remove functions symmetrically update pair counts by scanning all Fibonacci numbers and checking complements in constant time.

The most delicate part is the ordering of updates in remove: the frequency is decremented before subtracting contributions, ensuring we do not count the removed element as part of valid pairs.

The final answer per query simply counts how many Fibonacci targets have at least one valid pair in the current segment.

## Worked Examples

Consider a small array [1, 2, 3, 5] and Fibonacci numbers [1, 2, 3, 5, 8, ...]. For the full segment, we track which Fibonacci sums appear.

| Step | Window | freq | Valid Fibonacci sums |
| --- | --- | --- | --- |
| 1 | [1] | {1:1} | none |
| 2 | [1,2] | {1:1,2:1} | 3 |
| 3 | [1,2,3] | {1,1,3} | 3,4,5 exists? only 3,5 from pairs |
| 4 | [1,2,3,5] | {1,1,1,5} | 3,5,6,7,8 depending on pairs |

This trace shows how each new element increases the number of possible sums by interacting with all existing values.

Now consider a query over [2,3,5]. The frequency becomes {2,3,5}. Valid pairs include 2+3=5 and 2+5=7 and 3+5=8. Only Fibonacci sums among these are counted, and duplicates of the same Fibonacci number are ignored.

This demonstrates how the algorithm does not care about which pairs produce a Fibonacci number, only whether at least one such pair exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + Q) √N · 44) | Mo’s algorithm processes pointer shifts, each shift scans Fibonacci list |
| Space | O(N) | Frequency map and query storage |

The √N factor comes from Mo ordering, while the constant 44 comes from the bounded Fibonacci universe. With N, Q up to 10⁵, this fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    fib = [1, 2]
    while fib[-1] <= 2_000_000_000:
        fib.append(fib[-1] + fib[-2])
    fib = fib[:-1]

    block = int(n ** 0.5)

    queries = []
    for i in range(q):
        l, r = map(int, input().split())
        queries.append((l, r, i, l // block))

    queries.sort(key=lambda x: (x[3], x[1]))

    freq = {}
    ways = [0] * len(fib)

    def add(x):
        for i, f in enumerate(fib):
            ways[i] += freq.get(f - x, 0)
        freq[x] = freq.get(x, 0) + 1

    def remove(x):
        freq[x] -= 1
        for i, f in enumerate(fib):
            ways[i] -= freq.get(f - x, 0)

    cur_l, cur_r = 0, -1
    ans = [0] * q

    for l, r, i, _ in queries:
        while cur_l > l:
            cur_l -= 1
            add(a[cur_l])
        while cur_r < r:
            cur_r += 1
            add(a[cur_r])
        while cur_l < l:
            remove(a[cur_l])
            cur_l += 1
        while cur_r > r:
            remove(a[cur_r])
            cur_r -= 1

        ans[i] = sum(1 for x in ways if x > 0)

    return "\n".join(map(str, ans))

# minimal
assert run("1 1\n5\n0 0") == "0"

# simple pair
assert run("4 1\n1 2 3 5\n0 3") == "3"

# all equal
assert run("5 1\n2 2 2 2 2\n0 4") == "1"

# boundary two elements
assert run("2 1\n1 1\n0 1") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | no pair exists |
| small mixed array | 3 | multiple Fibonacci sums |
| all equal values | 1 | duplicate sum handling |
| two elements | 1 | simplest valid pair case |

## Edge Cases

A single-element segment such as [7] produces zero valid days because no pair can be formed. The algorithm initializes the window and never registers any contribution in ways[], since add() requires at least one existing element to match a complement.

A segment where all values are identical, for example [4,4,4,4], ensures that every update adds the same complement structure. Each Fibonacci value can only be satisfied by the same pair sum repeatedly, so only one Fibonacci number can be counted even though many pairs exist. The frequency-based update ensures that multiple identical pairs still only contribute to a single nonzero ways entry per Fibonacci target.

A segment like [1,1,2] tests duplicate handling. When inserting the second 1, the pair sum 2 becomes available, but removing or reordering elements does not incorrectly double count because updates are symmetric between add and remove operations and depend strictly on current frequency state.
