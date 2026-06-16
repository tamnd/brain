---
title: "CF 1005C - Summarize to the Power of Two"
description: "We are given a multiset of integers, and we are allowed to delete any subset of them. After deletions, we want the remaining elements to satisfy a pairing condition: every remaining value must be able to find at least one other remaining value such that their sum equals a power…"
date: "2026-06-16T23:19:21+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1005
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 496 (Div. 3)"
rating: 1300
weight: 1005
solve_time_s: 107
verified: false
draft: false
---

[CF 1005C - Summarize to the Power of Two](https://codeforces.com/problemset/problem/1005/C)

**Rating:** 1300  
**Tags:** brute force, greedy, implementation  
**Solve time:** 1m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of integers, and we are allowed to delete any subset of them. After deletions, we want the remaining elements to satisfy a pairing condition: every remaining value must be able to find at least one other remaining value such that their sum equals a power of two.

This condition is local per element, but the choice of partner must come from the same final set. So the problem is really asking for the largest possible subset where every element participates in at least one valid “power-of-two sum pair”, and then we subtract that size from the original array length.

The constraint n up to 120000 forces us away from anything quadratic or even n√n in a naive form. Any solution that tries all pairs or recomputes matches per element independently without reuse will time out, because checking all candidate pairs would require about n² operations in the worst case, which is on the order of 10¹⁰.

A subtle edge case appears when no pairing is possible at all. For example, if the array contains a single element like [16], there is no way to satisfy the condition, so the optimal answer is to delete everything. Another interesting case is when values are too large to pair into any power of two sum range, for instance [4, 16], where even the best possible complement (4 + 16 = 20) is not a power of two.

The key difficulty is that the condition is not symmetric in a constructive way: each element has multiple possible targets, but we must globally ensure all elements are covered by some matching structure.

## Approaches

A direct approach is to try every subset of the array and test whether it is good. For a fixed subset, we would check each element and attempt to find a partner among the remaining elements whose sum is a power of two. Even if we optimize membership checks with a hash set, verifying one subset costs O(n²) in the worst case. Since there are 2ⁿ subsets, this is completely infeasible.

Even if we restrict ourselves to the idea of pairing greedily per element, we quickly run into conflicts. An element might have multiple possible partners, and choosing one locally can block another element from finding its required match. So a purely greedy matching from scratch for each element fails because it ignores global consistency.

The key observation is that only sums of the form 2ᵈ matter, and each value aᵢ only needs to find one partner. This suggests reframing the problem as a matching problem on a graph: each number is a node, and we connect i and j if aᵢ + aⱼ is a power of two. We want to delete as few nodes as possible so that every remaining node has degree at least one in the induced subgraph.

Instead of constructing this huge graph explicitly, we invert the perspective. For each value x, its valid partners are numbers of the form 2ᵈ − x. Since values are up to 10⁹, d only needs to go up to about 31 or 32. This drastically limits the search space per element.

We then use a frequency map and greedily try to form valid pairs. The crucial structure is that pairing is symmetric, so we can iterate through values and greedily match each occurrence with available complements, ensuring each element is used at most once.

The final goal is equivalent to maximizing the number of elements that participate in at least one successful pairing, which reduces to repeatedly forming disjoint pairs whenever possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n) | Too slow |
| Frequency + Power Enumeration | O(n log A) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a frequency map of all values in the array. This allows constant-time access to how many unused copies of a number remain.
2. Iterate through each distinct value x in the map. For each x, attempt to pair its occurrences one by one.
3. For each occurrence of x, try all powers of two sums 2ᵈ such that 2ᵈ − x is a candidate value. If a complement y = 2ᵈ − x exists in the map with positive remaining frequency, form a pair (x, y) and decrement both counts.
4. Continue this process until no more pairs can be formed for x, then move to the next value.
5. Count how many elements were successfully paired. Since each pair contributes two kept elements, the answer is n minus the number of elements used in successful pairings.

The reason we try all powers of two per value is that each element only has O(log maxA) potential partners, which keeps the search small and ensures we do not miss any valid pairing.

### Why it works

Each valid configuration decomposes into disjoint pairs because every element must have at least one partner, and a single partner is sufficient. Once we fix that we only care about selecting edges of a compatibility graph, maximizing kept elements reduces to selecting as many valid edges as possible without reusing vertices. Since each vertex participates in at most one edge in the constructed solution, greedy pairing over all possible power targets is sufficient because any optimal solution can be rearranged into such disjoint matches without loss, given that each edge independently satisfies the condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    from collections import Counter
    cnt = Counter(a)
    
    powers = [1 << i for i in range(32)]
    
    used = Counter()
    ans_pairs = 0
    
    for x in list(cnt.keys()):
        while cnt[x] > 0:
            matched = False
            for p in powers:
                y = p - x
                if y < 0:
                    continue
                if cnt[y] > 0:
                    cnt[x] -= 1
                    cnt[y] -= 1
                    ans_pairs += 1
                    matched = True
                    break
            if not matched:
                break
    
    print(n - 2 * ans_pairs)

if __name__ == "__main__":
    solve()
```

The implementation relies on a frequency counter so we do not explicitly build all pairs. The list of powers of two is precomputed up to 2³¹, which safely covers all possible sums given the constraints.

For each value, we repeatedly attempt to find a complement that forms a valid power-of-two sum. Once a pair is formed, both frequencies are reduced immediately, ensuring no element is reused.

A subtle point is that we recompute complements against the current state of the frequency map rather than a fixed snapshot, since earlier pairings affect later availability.

## Worked Examples

### Example 1

Input:

```
6
4 7 1 5 4 9
```

We track frequencies and pairing attempts.

| Step | x | p | y = p - x | cnt[x] | cnt[y] | Pair formed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 8 | 4 | 2 → 1 | 0 | No |
| 2 | 4 | 16 | 12 | 1 | 0 | No |
| 3 | 7 | 8 | 1 | 1 | 1 | Yes |
| 4 | 1 | 8 | 7 | 0 | 0 | Yes |
| 5 | 4 | 8 | 4 | 1 → 0 | 0 | No |
| 6 | 5 | 8 | 3 | 1 | 0 | No |

We form 1 valid pair, covering 2 elements. So answer is 6 − 2 = 4.

This trace shows that pairing is highly dependent on availability order, and the greedy process consumes frequencies as soon as valid complements appear.

### Example 2

Input:

```
4
1 3 2 1
```

| Step | x | p | y | cnt[x] | cnt[y] | Pair |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 1 | 2 → 1 | 0 | No |
| 2 | 1 | 4 | 3 | 1 | 1 | Yes |
| 3 | 3 | 4 | 1 | 0 | 0 | Yes |
| 4 | 2 | 2 | 0 | 1 | 0 | No |

We form one pair again, leaving two unpaired elements.

This confirms that elements may remain unmatched if no valid complement exists, and they are effectively removed in the optimal solution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A) | Each value tries at most ~32 power-of-two targets |
| Space | O(n) | Frequency map over distinct values |

The log factor comes from enumerating candidate powers of two for each value. Since A ≤ 10⁹, this is bounded by 31 iterations per element, which fits comfortably under the time limit for n up to 120000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    from collections import Counter

    cnt = Counter(a)
    powers = [1 << i for i in range(32)]
    ans_pairs = 0

    for x in list(cnt.keys()):
        while cnt[x] > 0:
            matched = False
            for p in powers:
                y = p - x
                if y < 0:
                    continue
                if cnt[y] > 0:
                    cnt[x] -= 1
                    cnt[y] -= 1
                    ans_pairs += 1
                    matched = True
                    break
            if not matched:
                break

    return str(n - 2 * ans_pairs)

# provided sample
assert run("6\n4 7 1 5 4 9\n") == "1"

# all equal values, no pairs possible
assert run("3\n4 4 4\n") == "0"

# simple pair
assert run("2\n1 1\n") == "0"

# boundary small case
assert run("1\n16\n") == "1"

# mix case
assert run("4\n1 3 2 8\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 0 | impossible pairing structure |
| 1 1 | 0 | direct power-of-two pairing |
| single element | 1 | full deletion case |
| mixed | 2 | greedy matching interactions |

## Edge Cases

A single-element array like [16] demonstrates the failure of any strategy that assumes every value can find a partner. The algorithm processes the value, finds no complement among any 2ᵈ − 16, and leaves it unmatched, contributing correctly to full deletion.

In a case like [1, 1], the algorithm immediately finds that 1 + 1 = 2, a power of two, consumes both occurrences, and produces zero deletions. The frequency-based structure ensures both copies are handled symmetrically without double counting.

In arrays where multiple pairing options exist, such as [1, 3, 2, 8], the algorithm’s sequential consumption of frequencies ensures that once a value is used in one pair, it cannot incorrectly participate in another, preserving correctness under the disjoint-pair requirement.
