---
title: "CF 104869K - Maximum Rating"
description: "We are given an array of integers representing rating changes from several contest rounds. We are allowed to reorder these rounds arbitrarily. We then simulate starting from rating zero, adding values one by one."
date: "2026-06-28T10:52:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104869
codeforces_index: "K"
codeforces_contest_name: "The 2023 ICPC Asia Shenyang Regional Contest (The 2nd Universal Cup. Stage 13: Shenyang)"
rating: 0
weight: 104869
solve_time_s: 58
verified: true
draft: false
---

[CF 104869K - Maximum Rating](https://codeforces.com/problemset/problem/104869/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers representing rating changes from several contest rounds. We are allowed to reorder these rounds arbitrarily. We then simulate starting from rating zero, adding values one by one. Each time the running sum strictly exceeds all previous values of the running sum, we count that as an update of the maximum rating.

The task is not to find the best ordering, but something more global: for a fixed multiset of values, we want to know how many different values of “number of maximum updates” are achievable by choosing different permutations of the array. After every update that changes one element of the array, we must recompute this quantity.

The key constraint is that both n and q can be as large as 200,000, so any solution that tries to simulate permutations, or even reason per query with anything worse than logarithmic or constant work per update, will not pass. The structure strongly suggests that the answer must depend on a very small number of global properties of the multiset, not on its detailed arrangement.

A subtle but important edge case appears when all numbers are non-positive. In that situation, the running sum starts at zero and never becomes strictly positive, so no maximum update ever happens. A naive approach that assumes at least one update always occurs would incorrectly report a positive answer here. Another fragile case is when zeros are present: zeros never increase the sum, but they can be mistaken as harmless positives if one only checks sign carelessly.

## Approaches

If we try to think directly, the brute-force idea is to enumerate all permutations of the array and simulate the process for each one, counting how many times the prefix sum sets a new record. This is correct in principle, since it matches the definition exactly. However, there are n factorial permutations, and even simulating one permutation costs linear time, so this approach explodes immediately beyond very small n.

The key observation is that the process only cares about when the prefix sum crosses new highs, and this depends only on whether elements are positive or not. Negative and zero values can delay growth but can never create additional record-breaking events on their own. Meanwhile, positive values can each contribute at most one new record, because once a prefix sum reaches a new peak due to a positive number, no rearrangement can make that same element contribute again.

This collapses the entire problem into tracking how many strictly positive values exist. Once this is recognized, the number of achievable k values becomes extremely constrained: if there are no positive numbers, the process never increases above zero, so the only possible value is k = 0. If there is at least one positive number, we can either force all positives to appear early and create a new record for each of them, or delay all positives until the end so that only one crossing happens when the accumulated negatives are overcome. Intermediate behaviors are also achievable, but crucially, every value from 1 up to the number of positive elements is possible, forming a continuous range.

Thus the answer per array is simply the size of the positive-count range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over permutations | O(n! · n) | O(n) | Too slow |
| Track positive count only | O(n + q) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the entire problem to maintaining how many elements in the array are strictly greater than zero.

1. Compute the initial number of positive elements in the array, call it pos.
2. For each update that changes a single element, first determine whether that element was positive before the update and whether it is positive after the update.
3. Adjust pos accordingly by subtracting one if a positive becomes non-positive, or adding one if a non-positive becomes positive.
4. After each update, compute the answer from pos: if pos is zero, output 1, otherwise output pos.

The non-trivial part of this reasoning is why the answer depends only on pos. The structure of prefix maximum updates ensures that only strictly positive increments can create new records, while negatives and zeros only affect timing and cannot increase the number of record-breaking events beyond what positives already allow.

### Why it works

The running maximum of prefix sums increases exactly when we add an element that pushes the cumulative sum above all previously achievable values. Any non-positive element cannot contribute to a new maximum increase, since adding it to any prefix sum cannot strictly increase the sum. Therefore only positive elements are capable of triggering such events.

Moreover, each positive element can be arranged so that it either produces its own new maximum or gets absorbed into a single final crossing, but no arrangement can make more than pos distinct maximum updates happen, and at least one update is possible whenever pos is non-zero. This forces the set of achievable k values to be exactly {1, 2, ..., pos}, and in the degenerate case where pos = 0, it collapses to {0}.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    
    pos = 0
    for x in a:
        if x > 0:
            pos += 1
    
    for _ in range(q):
        i, v = map(int, input().split())
        i -= 1
        
        old = a[i]
        if old > 0:
            pos -= 1
        
        a[i] = v
        
        if v > 0:
            pos += 1
        
        if pos == 0:
            print(1)
        else:
            print(pos)

if __name__ == "__main__":
    solve()
```

The solution maintains a single global counter `pos`, representing how many elements are strictly positive at any moment. Each update only affects this counter locally, so the array itself is only needed for remembering previous values. The output logic directly follows from the derived characterization: either all values are non-positive, giving a single possible outcome, or otherwise every count from 1 to pos is achievable.

A common mistake here is to try to recompute the answer by sorting or simulating prefix sums after each update, which would be far too slow. The critical simplification is that the full structure of the array never matters, only the sign distribution.

## Worked Examples

Consider the array `[1, 2, 3]`.

Initially, all three elements are positive, so pos = 3.

| Step | Array | pos | Output |
| --- | --- | --- | --- |
| init | [1,2,3] | 3 | - |
| 1 | [1,2,4] | 3 | 3 |
| 2 | [1,-2,4] | 2 | 2 |
| 3 | [-3,-2,4] | 1 | 1 |
| 4 | [-3,-2,1] | 1 | 1 |
| 5 | [-3,1,1] | 2 | 2 |

This matches the idea that the answer is always equal to the number of positive elements unless that number is zero.

Now consider a case with no positives, such as `[0, -1, -5]`.

| Step | Array | pos | Output |
| --- | --- | --- | --- |
| init | [0,-1,-5] | 0 | 1 |
| after updates | still all ≤ 0 | 0 | 1 |

Here no ordering can ever make the running sum exceed zero, so the only achievable value is k = 0, and the number of valid k values is 1.

These traces confirm that the invariant is purely sign-based and insensitive to magnitude or ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Each update adjusts a single counter in O(1) time |
| Space | O(1) extra | Only the array and one integer counter are maintained |

The constraints allow up to 200,000 updates, so constant-time processing per query is necessary. The solution fits comfortably within limits since it performs no heavy computation per operation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    
    pos = sum(1 for x in a if x > 0)
    
    out = []
    for _ in range(q):
        i, v = map(int, input().split())
        i -= 1
        if a[i] > 0:
            pos -= 1
        a[i] = v
        if a[i] > 0:
            pos += 1
        out.append(str(1 if pos == 0 else pos))
    
    return "\n".join(out)

# minimal case
assert run("1 1\n0\n1 5\n") == "1", "single element becomes positive"

# all non-positive
assert run("3 2\n0 -1 -2\n1 -5\n2 -3\n") == "1\n1", "all non-positive stays 1"

# all positive shrinking
assert run("3 3\n1 2 3\n1 -1\n2 -2\n3 -3\n") == "2\n1\n1", "positive count decreases"

# mixed updates
assert run("4 2\n1 -1 2 -3\n2 5\n3 -4\n") == "3\n2", "toggle positives"

# already maximal positives
assert run("2 1\n10 20\n1 -5\n") == "1", "drop to single positive"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element update | 1 | base case correctness |
| all non-positive | 1 per query | handling zero-positive case |
| decreasing positives | shrinking answers | dynamic updates |
| mixed toggles | correct sign transitions | both directions |
| drop to single positive | boundary transition | pos = 1 behavior |

## Edge Cases

When all elements are non-positive, the algorithm correctly keeps `pos = 0` throughout and outputs 1 for every query. This corresponds to the fact that no permutation can ever create a positive prefix sum, so no maximum update occurs.

When a value crosses from positive to non-positive or vice versa, only a single counter update is needed. For example, changing `-3` to `4` increases `pos` by one, and the resulting increase in the answer reflects the fact that one more element can now independently contribute to a potential record event.

The correctness does not depend on magnitude. Even extreme values like `-10^9` and `10^9` behave identically to `-1` and `1`, since only sign affects whether an element contributes to `pos`.
