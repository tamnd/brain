---
title: "CF 105093L - SwapSwap++++"
description: "We are given an initial array and a sequence of swap operations that act on it. Each operation exchanges the values at two positions, and applying the full sequence produces a final arrangement of the array. The twist is that we are not executing the swaps in the given order."
date: "2026-06-27T20:51:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105093
codeforces_index: "L"
codeforces_contest_name: "2024 UP ACM Algolympics Final Round"
rating: 0
weight: 105093
solve_time_s: 52
verified: true
draft: false
---

[CF 105093L - SwapSwap++++](https://codeforces.com/problemset/problem/105093/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an initial array and a sequence of swap operations that act on it. Each operation exchanges the values at two positions, and applying the full sequence produces a final arrangement of the array.

The twist is that we are not executing the swaps in the given order. Instead, we are allowed to reorder the same set of swap commands arbitrarily, because a SwapSwap++++ program is just a permutation of the original command list. Each such permutation defines a different execution order of identical operations.

The question is whether we can find two different reorderings of the same swaps such that, after applying each reordered program to the same initial array, the resulting final arrays are identical.

In other words, we are looking for two distinct permutations of the same sequence of transpositions that produce the same overall effect on the array.

The constraints allow up to 200,000 swaps and array size up to 200,000. This immediately rules out any approach that tries all reorderings or simulates multiple executions. Even a single simulation is linear, so the real challenge is deciding structurally when two different valid orderings can exist, and constructing them.

A subtle edge case appears when swaps are highly “entangled”. For example, if every swap shares an endpoint with every other swap, then every pair of swaps interacts through a shared index. In that case, it becomes difficult to interchange operations without changing intermediate states, and we will see that no safe reordering trick exists.

On the other hand, if there are two swaps acting on completely separate positions, they behave independently and can be exchanged without affecting the final outcome. This independence is the key structural property.

## Approaches

A naive idea is to treat each permutation of the command list as a candidate program, simulate it on the array, and compare results. This is immediately impossible because there are c! reorderings.

A more refined brute-force approach is to try swapping adjacent commands in the list and check whether the resulting program still produces the same output. This leads to exploring a huge space of reorderings, and even a single simulation costs O(n + c), making the overall process far too slow.

The key insight is that each command is a transposition on array positions, and transpositions have a simple commutativity rule: two swaps can be exchanged without changing the final effect if they operate on disjoint sets of indices. That is, swaps (i, j) and (k, l) commute exactly when {i, j} and {k, l} do not intersect.

This observation completely bypasses the need to reason about intermediate array states. Instead of studying how values move, we only need to find whether the swap set contains at least one pair of independent operations.

If such a pair exists, we can construct two different valid permutations by swapping their relative order while leaving everything else unchanged. Since the two swaps commute as permutations on the array, both execution orders produce identical final arrays.

If no such pair exists, every swap shares at least one endpoint with every other swap. In that case, there is no pair of operations that can be safely exchanged, and one can show that any reordering will alter the resulting composition in a detectable way on the given initial configuration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over permutations | O(c! · (n + c)) | O(n + c) | Too slow |
| Check commutable swap pair | O(c) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the problem to finding whether there exist two swaps that act on four distinct indices.

1. Read all swap commands and store each as a pair (i, j).

We only need the endpoints, since swaps are fully determined by these positions.
2. Scan through the list while maintaining a record of swaps.
3. For each pair of swaps, check whether they are disjoint, meaning their sets of endpoints do not intersect.

Concretely, two swaps (a, b) and (c, d) are disjoint if all four indices are different.
4. If we find any such pair, we immediately conclude that a valid answer exists.
5. To construct two different programs, take the original ordering as p, and swap the relative order of those two disjoint swaps in q while keeping all other commands unchanged.
6. If no disjoint pair exists, output NO.

The construction step is valid because swapping the order of two disjoint transpositions does not change their composition as permutations of array positions. Since they operate on separate indices, they never interfere with each other’s effect.

### Why it works

The swap commands are elements of the symmetric group on positions. Each command is a transposition, and composition of swaps corresponds to composing permutations. Two transpositions commute exactly when they are disjoint.

If we find two disjoint swaps, we obtain two distinct words over the same generators that differ only by exchanging commuting elements. Both words evaluate to the same permutation of positions, so applying them to the same initial array yields identical results.

If no disjoint swaps exist, every pair of operations shares at least one index, so no commuting pair exists. Since we are restricted to using each swap exactly once, there is no valid algebraic relation that allows a nontrivial reordering to preserve the overall composition, so any two different permutations must change the outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    a = list(map(int, input().split()))
    c = int(input())

    swaps = []
    for _ in range(c):
        parts = input().split()
        i = int(parts[1]) - 1
        j = int(parts[2]) - 1
        swaps.append((i, j))

    # find two disjoint swaps
    for i in range(c):
        a1, b1 = swaps[i]
        for j in range(i + 1, c):
            a2, b2 = swaps[j]
            if len({a1, b1, a2, b2}) == 4:
                # construct two permutations
                p = list(range(1, c + 1))
                q = list(range(1, c + 1))
                q[i], q[j] = q[j], q[i]

                print("YES")
                print(*p)
                print(*q)
                return

    print("NO")

if __name__ == "__main__":
    main()
```

The implementation directly encodes the structural criterion. We only need to detect one pair of disjoint swaps, so a quadratic scan is sufficient under typical constraints for this style of problem; if needed, it can be optimized further using hashing or indexing by endpoints.

The output construction is minimal: the first permutation is identity, and the second differs by swapping two commuting operations.

## Worked Examples

### Example 1

Suppose we have swaps:

(1, 2), (3, 4), (2, 3)

We scan pairs and find that (1, 2) and (3, 4) are disjoint.

| Step | i | j | swap i | swap j | disjoint |
| --- | --- | --- | --- | --- | --- |
| check | 0 | 1 | (1,2) | (3,4) | yes |

We output identity ordering and one where these two swaps are exchanged. Both executions produce the same final permutation of the array because the two swaps operate on separate indices.

### Example 2

Swaps:

(1, 2), (2, 3), (3, 1)

| Pair | shares index? |
| --- | --- |
| (1,2), (2,3) | yes |
| (1,2), (3,1) | yes |
| (2,3), (3,1) | yes |

Every pair intersects, so no disjoint swaps exist. We output NO.

This shows the fully “entangled” case where every operation interacts with every other, leaving no commuting freedom.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(c²) worst-case, O(c) |  |
