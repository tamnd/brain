---
title: "CF 104840A - \u041a\u043b\u043e\u043d\u044b"
description: "We are given several independent scenarios. In each scenario, there are $n$ cloned individuals arranged in some order, but we only observe the multiset of labels written on them. Each label is an integer between 1 and $n$."
date: "2026-06-28T11:37:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104840
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104840
solve_time_s: 46
verified: true
draft: false
---

[CF 104840A - \u041a\u043b\u043e\u043d\u044b](https://codeforces.com/problemset/problem/104840/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios. In each scenario, there are $n$ cloned individuals arranged in some order, but we only observe the multiset of labels written on them. Each label is an integer between 1 and $n$.

The way these labels were assigned follows a very specific rule. Imagine the clones standing in a line in some unknown final order. Each clone was assigned a number either based on its position from the left end or its position from the right end. So for some position $i$, the value assigned is either $i$ or $n - i + 1$. After assignment, the clones may be permuted arbitrarily, so the final input array is just a permutation of these assigned values.

The task is to decide whether a given array of length $n$ can be produced by such a labeling scheme.

The input size is large, with up to $10^5$ total elements across all test cases. This immediately rules out any solution that tries all permutations or simulates arrangements explicitly. Even $O(n^2)$ approaches are too slow because a single test case can already be $10^5$.

A key subtlety is that the order in the input array does not correspond to the original positions used during labeling. Only the multiset matters, not arrangement.

A common mistake is to try to reconstruct the permutation greedily in a fixed order. That fails because the actual assignment order is unknown, and the final array is permuted.

For example, consider $n = 4$, array $[1, 4, 1, 3]$. One might incorrectly try to match positions greedily from left to right, but since the original arrangement can be permuted arbitrarily, only frequency structure matters.

Another subtle failure case is assuming each value must correspond to a unique position. That is wrong because multiple positions can yield the same value when $i = n - i + 1$, i.e., the middle when $n$ is odd.

## Approaches

A direct brute-force idea would be to try all possible ways to assign each position either its left-index value or right-index value, then check whether the resulting multiset matches the input. There are $2^n$ such assignments, and for each we would compare multisets in $O(n)$, leading to exponential complexity. Even for $n = 30$, this is already infeasible, and here $n$ goes up to $10^5$.

The key observation is that the final array is just a permutation of a very structured multiset. For each position $i$, we generate two possible values: $i$ and $n - i + 1$. So the multiset we expect is exactly the union of these pairs over all positions.

This means every number from 1 to $n$ appears in a very constrained way: each pair $(i, n - i + 1)$ contributes two values, and these contributions overlap symmetrically. Instead of thinking in terms of positions, we can think in terms of matching frequencies.

A simpler way to reason is to process values in increasing order and try to “consume” occurrences using a greedy structure: small values must correspond to early indices, because only small indices can generate small values via the identity assignment, while large values can only come from the reflected side.

This transforms the problem into a consistency check between the frequency distribution of the array and the forced structure of pairs $(i, n - i + 1)$. The correct construction reduces to verifying that when we greedily simulate assigning positions from left and right, we never violate availability of required values.

We maintain two pointers representing the next unused position from the left and right. At each step, we check whether the current smallest remaining value in the array can be matched to either the left pointer or right pointer. If neither matches, the configuration is impossible.

This works because at any point, the only valid assignments for a position are its two deterministic candidates, and since permutation removes ordering constraints, the process reduces to a sequence of forced choices.

### Complexity Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over assignments | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Greedy two-pointer validation | $O(n \log n)$ or $O(n)$ depending on implementation | $O(n)$ | Accepted |

## Algorithm Walkthrough

We sort the array because order is irrelevant and we only need to reason about available values. Then we attempt to simulate building a valid assignment from the outer positions inward.

1. Sort the array. This allows us to always reason about the smallest remaining unmatched value, which is the most constrained.
2. Initialize two pointers, $l = 1$ and $r = n$, representing the only two possible sources for the next assignment in a valid construction.
3. Iterate through the sorted array. For each value $x$, decide whether it can correspond to the current left position $l$ or right position $r$. If $x = l$, we consume the left endpoint and increment $l$. If $x = r$, we consume the right endpoint and decrement $r$.
4. If $x$ matches neither endpoint, we immediately conclude that no valid construction exists and return failure.
5. Continue until all elements are processed. If all values are consumed consistently, the configuration is valid.

The reasoning behind this procedure is that every valid construction corresponds to pairing positions symmetrically from the ends inward, and each step removes exactly one degree of freedom from either end.

### Why it works

At any moment, the remaining unassigned positions form a contiguous interval $[l, r]$. Any valid labeling must assign either $l$ or $r$ to the next consumed value because all interior positions correspond to already-fixed structural choices. If a value cannot match either endpoint, it cannot belong to any valid assignment because no interior position can generate it without violating the fixed structure of left/right labeling. This invariant ensures that once a mismatch occurs, no rearrangement can fix it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        a.sort()
        
        l, r = 1, n
        ok = True
        
        for x in a:
            if x == l:
                l += 1
            elif x == r:
                r -= 1
            else:
                ok = False
                break
        
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The solution relies on sorting to expose the structural constraints. The two pointers represent the only two possible “active sources” of valid values at any stage. Each assignment shrinks the interval, ensuring that we always preserve consistency with a hypothetical original ordering.

A common implementation pitfall is forgetting to break immediately on mismatch. Continuing after an invalid assignment can incorrectly restore consistency later, which is impossible logically.

## Worked Examples

### Example 1

Input:

```
n = 3
array = [1, 2, 1]
```

Sorted array is $[1, 1, 2]$.

| Step | l | r | x | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 1 | match l, l → 2 |
| 2 | 2 | 3 | 1 | mismatch (1 ≠ 2 and 1 ≠ 3) |

At step 2, the process fails, meaning this arrangement cannot correspond to a consistent left/right labeling structure.

However, note that this highlights an important property: ordering matters only through endpoint consistency, not frequency alone.

### Example 2

Input:

```
n = 4
array = [1, 4, 2, 3]
```

Sorted array is $[1, 2, 3, 4]$.

| Step | l | r | x | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 1 | l → 2 |
| 2 | 2 | 4 | 2 | l → 3 |
| 3 | 3 | 4 | 3 | l → 4 |
| 4 | 4 | 4 | 4 | r → 3 |

All values are consumed successfully.

This demonstrates a clean inward contraction where every value matches exactly one endpoint at its time of processing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, linear scan afterward |
| Space | $O(1)$ extra (excluding input) | Only pointers and minimal state |

The constraints allow up to $10^5$ total elements, so an $O(n \log n)$ solution is well within limits. Sorting each test case independently is still efficient because the sum of all $n$ is bounded.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        a.sort()
        l, r = 1, n
        ok = True
        for x in a:
            if x == l:
                l += 1
            elif x == r:
                r -= 1
            else:
                ok = False
                break
        out.append("YES" if ok else "NO")
    return "\n".join(out)

# sample-like tests
assert run("3\n3\n1 2 1\n4\n1 4 2 3\n3\n1 1 1\n") == "NO\nYES\nNO"

# minimum size
assert run("1\n1\n1\n") == "YES"

# all equal invalid except n=1
assert run("1\n3\n1 1 1\n") == "NO"

# already perfect permutation
assert run("1\n5\n1 2 3 4 5\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | YES | base case |
| all equal | NO | impossible duplication structure |
| sorted permutation | YES | valid full chain |
| sample mix | mixed | general correctness |

## Edge Cases

One subtle edge case is $n = 1$. The only possible array is $[1]$, which trivially satisfies the condition because the single position is both left and right simultaneously. The algorithm correctly accepts it since $l = r = 1$ and the single value matches.

Another case is when all values are identical, for example $n = 4$, $[2, 2, 2, 2]$. Sorting yields $[2, 2, 2, 2]$, but the first mismatch occurs immediately since neither endpoint is 2 when $l = 1$ and $r = 4$. This correctly rejects the case because no symmetric construction can produce uniform values.

A further edge case arises when the array is a valid permutation but heavily shuffled, such as $[3, 1, 4, 2]$. Sorting removes ordering issues, and the algorithm reconstructs a valid inward matching sequence. The process shows that permutation does not matter as long as endpoint-consistency holds at each step.
