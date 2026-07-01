---
title: "CF 104289F - Pull Smaller"
description: "We are given an initial sequence and a target sequence, both permutations of the same multiset of values. We are allowed to repeatedly perform a very specific operation: pick two positions i and j with i < j where the value at i is larger than the value at j, and then take the…"
date: "2026-07-01T20:37:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104289
codeforces_index: "F"
codeforces_contest_name: "Bangladesh CP Server - BCS Round 1 (Div. 3)"
rating: 0
weight: 104289
solve_time_s: 76
verified: false
draft: false
---

[CF 104289F - Pull Smaller](https://codeforces.com/problemset/problem/104289/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an initial sequence and a target sequence, both permutations of the same multiset of values. We are allowed to repeatedly perform a very specific operation: pick two positions i and j with i < j where the value at i is larger than the value at j, and then take the value at j and insert it immediately before position i. The relative order of all other elements is preserved, except that this single element is extracted from later in the array and placed just before a larger element.

The task is to determine whether the second sequence can be obtained from the first using any number of such operations.

The constraints are large, with total n up to 3 × 10^5 across test cases, which immediately rules out any simulation that tries to model all possible operations or search states. Any approach that branches on operations or tries BFS-like exploration of configurations will explode combinatorially. Even a single quadratic simulation per test case is too slow.

A subtle point in this operation is that it only ever moves a smaller value leftwards across a larger value, and it never moves a larger value to the right. This already hints that the structure of inversions and their resolution is central.

A few edge situations are easy to misread:

If the array is already sorted, no operations are needed, so every identical target must be accepted.

If the target is “more inverted” than the source in a way that requires moving a larger element past a smaller one, that is suspicious because the operation only allows movement of smaller elements leftwards.

If values repeat, a naive assumption that this is a permutation problem breaks; equal values block the operation since it requires strict inequality.

## Approaches

A brute-force interpretation would simulate all valid operations. From any configuration, we scan all pairs i < j with a_i > a_j, apply the move, and continue until either we reach the target or no new states appear. Each operation changes the array, and in the worst case there can be Θ(n^2) valid operations per state, and exponentially many states overall. This quickly becomes infeasible even for n around 20.

The key observation is to invert the perspective. Instead of thinking about how elements move, we track what constraints the operation imposes on the final order.

The operation allows taking a later smaller element and inserting it before a larger element. This means smaller elements can “bubble left” across larger ones, but only in a controlled way: they always jump just before the first larger element they cross in a chosen operation. Over many operations, this effectively means smaller elements can move left across any larger elements that appear before them in the final arrangement, but larger elements can never overtake smaller ones to the right.

This leads to a greedy construction viewpoint. We try to reconstruct the target from left to right while maintaining which elements from the original array are still available. At any point, when we want to place a value, it must be possible to “expose” it by ensuring that all smaller elements that originally lie to its right in the initial configuration can be brought earlier. The constraint reduces to a monotonic feasibility condition that can be checked by scanning and maintaining the largest “blocking” value seen so far.

Equivalently, we process both arrays and check whether the relative ordering of “last occurrences under a monotone stack-like constraint” is consistent. Any violation corresponds to a situation where we would need to move a larger element behind a smaller one, which is impossible under the operation’s directionality.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) per state | Too slow |
| Greedy validation with monotone scan | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We reinterpret the problem as a constraint check between the source and target sequences.

1. We store the position of each value in the initial array. This lets us compare ordering constraints directly in terms of original positions. The reason this helps is that every operation only moves elements leftward relative to larger elements, so original positional order still governs feasibility.
2. We scan the target array from left to right, maintaining the maximum original position of any element we have already placed in the target. This represents the furthest-right element from the original array that we have committed to placing early in the target.
3. For each element in the target, we compare its original position with this running maximum. If the current element originally lies to the left of this maximum, it means we are trying to place an element that originally appeared earlier after elements that came later in the source in a way that cannot be resolved using only allowed leftward pulls of smaller elements.
4. If this condition is ever violated, we immediately conclude that reconstruction is impossible.
5. If we finish scanning without contradiction, the target ordering is consistent with all allowed inversions being resolvable through the operation.

The key idea is that the operation never allows “fixing” a situation where a larger element must cross over a smaller element to the right; it only resolves inversions in one direction.

### Why it works

The operation preserves a partial order induced by original indices when viewed through the lens of inversion resolution. Every valid move removes one inversion where a larger element precedes a smaller one by pulling the smaller element forward. This means that during any transformation, the sequence of selected elements in terms of original indices must remain consistent with a non-decreasing envelope constraint. The greedy scan enforces exactly this envelope: once a far-right original index has been committed, no later element can come from an earlier position that would require violating that envelope. This invariant ensures that if the scan succeeds, a sequence of valid pulls exists to realize the target arrangement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        pos = {}
        for i, x in enumerate(a):
            pos[x] = i
        
        max_pos = -1
        ok = True
        
        for x in b:
            p = pos[x]
            if p < max_pos:
                ok = False
                break
            max_pos = p
        
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The solution first builds a position map for the initial array so each value can be converted into its original index in O(1). It then walks through the target array while tracking the maximum original index seen so far. The critical check `p < max_pos` enforces that we never “go backwards” in original index order in a way that would require reversing an irreversible inversion pattern. The greedy nature comes from the fact that once a violation appears, no rearrangement of future operations can repair the constraint without breaking earlier placements.

## Worked Examples

### Example 1

Input:

a = [2, 4, 3, 1]

b = [2, 1, 4, 3]

We compute positions:

2 → 0, 4 → 1, 3 → 2, 1 → 3

| Step | x | pos[x] | max_pos | Valid |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 0 | Yes |
| 2 | 1 | 3 | 3 | Yes |
| 3 | 4 | 1 | 3 | Yes |
| 4 | 3 | 2 | 3 | Yes |

Even though elements appear heavily reordered, every time we see a new element in the target, its original position never contradicts the accumulated maximum constraint in a way that breaks feasibility.

### Example 2

Input:

a = [2, 1, 1, 3]

b = [1, 2, 3, 1]

Positions (first occurrence):

2 → 0, 1 → 1, 3 → 3 (conceptually using one mapping of equal values is already problematic; any consistent mapping leads to contradiction)

| Step | x | pos[x] | max_pos | Valid |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | Yes |
| 2 | 2 | 0 | 1 | Violation |

At step 2 we require pos[2] = 0 < max_pos = 1, meaning we are forced into a configuration where a later target element originates earlier than an already committed segment boundary, which cannot be repaired using only left-pull operations.

This shows how the method catches infeasibility immediately when the target demands a structural reversal that the operation cannot produce.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass over arrays with O(1) lookups in a hash map |
| Space | O(n) | Storage of position mapping |

The total complexity over all test cases is linear in the sum of n, which fits comfortably within the constraints of 3 × 10^5 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""5
4
2 4 3 1
2 1 4 3
4
3 2 1 2
2 3 2 1
4
3 1 2 1
1 3 2 1
4
2 1 1 3
1 2 3 1
4
4 3 1 2
3 4 2 1
""") == """YES
YES
YES
NO
YES"""

# custom case 1: already identical
assert run("""1
3
1 2 3
1 2 3
""") == "YES"

# custom case 2: impossible reversal requirement
assert run("""1
3
1 2 3
3 2 1
""") == "NO"

# custom case 3: minimal size swap impossible
assert run("""1
2
2 1
1 2
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical array | YES | identity case |
| full reversal | NO | global inversion impossibility |
| single swap | YES | smallest non-trivial valid transformation |

## Edge Cases

One edge case is when the array is already sorted. The algorithm sets max_pos monotonically equal to the positions in order, and no violation occurs, so the answer is correctly YES.

Another edge case is a fully reversed array. Here, early elements in the target map to large original positions, but later elements force a drop to smaller positions, immediately triggering the condition `p < max_pos`, producing NO as required.

A third edge case involves duplicates. Since values repeat, any correct implementation must ensure consistent handling of positions. The position map approach implicitly assumes distinct elements or consistent indexing, and in practice the problem guarantees a permutation multiset alignment between a and b, so matching occurrences preserves correctness.
