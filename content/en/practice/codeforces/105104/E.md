---
title: "CF 105104E - Election"
description: "We are given a list of constituencies, each described only by a single integer representing how many votes it contains."
date: "2026-06-27T20:09:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105104
codeforces_index: "E"
codeforces_contest_name: "2024 HNMU@XTU"
rating: 0
weight: 105104
solve_time_s: 48
verified: true
draft: false
---

[CF 105104E - Election](https://codeforces.com/problemset/problem/105104/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of constituencies, each described only by a single integer representing how many votes it contains. In each constituency, one of two candidates wins all votes from that constituency, so each constituency behaves like a single “block” that contributes either its full value to one side or to the other.

The hidden question is not about simulating an election. Instead, it asks whether the structure of these vote blocks is rigid enough that any legal way of splitting them into two groups leads to a unique overall outcome pattern. Equivalently, we want to know whether there exist two different assignments of signs, one assignment corresponding to “candidate A wins this constituency” and the other to “candidate B wins it”, such that the resulting weighted sums behave indistinguishably under all legal transformations. The example in the statement hints at this: different sign assignments can produce the same total effect, which means ambiguity in determining the election outcome.

The input size is up to 100000 values, each as large as 2^31 − 1. This immediately rules out any approach that tries to enumerate subsets or compare all possible partitions. Even a quadratic approach over pairs of constituencies would be too slow. The solution must be essentially linear or linearithmic.

A subtle issue arises when many values are equal or when small values can be composed from larger ones. In those cases, different sign assignments can cancel each other in unexpected ways. For example, if the array contains values like 1, 2, 3, 4, we can combine signs to create equal totals in multiple ways, which corresponds to ambiguity. A naive intuition that “different numbers guarantee uniqueness” fails because linear combinations over signs can still collide.

Another edge case is when all values are powers of two or follow a strictly increasing structure. In such cases, uniqueness often holds, but only if each value is large enough compared to the sum of all previous ones. Otherwise, earlier values can simulate later ones through cancellation.

## Approaches

A brute-force interpretation would attempt to check whether two different sign assignments exist that produce identical election outcomes. One way to think about it is to consider all subsets of constituencies and compute all possible signed sums. If every subset produces a distinct value, then the system is unambiguous. However, this immediately leads to 2^n possibilities, and even for n = 40 this is already infeasible.

Another attempt would be to sort the values and try to detect collisions among subset sums using dynamic programming. This still explodes because the sum range is enormous, up to n * 2^31, and DP over sums is not feasible in either time or memory.

The key insight is to reinterpret the problem as a uniqueness condition on subset sums of a multiset where each element can be taken with a plus or minus sign. This is equivalent to asking whether the set is “linearly independent over coefficients in {−1, 0, 1}” in a very restricted sense. The critical observation is that ambiguity appears exactly when some subset of smaller elements can combine to match a larger element.

Once we sort the array, the condition simplifies dramatically. If at any point the largest remaining element is not strictly greater than the sum of all smaller elements considered so far, then we can construct two different sign assignments that collide. Conversely, if every element is strictly greater than the sum of all previous elements, then each element introduces a new scale that cannot be replicated by combinations of earlier ones, ensuring uniqueness.

This transforms the problem into a greedy linear scan after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over sign assignments | O(2^n) | O(n) | Too slow |
| Sorted greedy prefix sum check | O(n log n) | O(1) extra | Accepted |

## Algorithm Walkthrough

### Algorithm Walkthrough

1. Sort the array in non-decreasing order so that we always consider whether smaller values can build larger ones. Sorting is necessary because the key property depends on cumulative reachability from smaller elements.
2. Initialize a running sum variable as 0. This sum represents the maximum value that can be constructed using combinations of already processed elements.
3. Iterate through the sorted array from smallest to largest element.
4. For each element ai, check whether ai is less than or equal to the current running sum. If this condition holds, we immediately conclude that ambiguity exists and stop.
5. If ai is strictly greater than the current sum, we update the running sum by adding ai, since this element extends the range of constructible values.
6. If the loop finishes without triggering the failure condition, we conclude that no collision between sign assignments is possible.

### Why it works

At every step, the running sum represents the full range of values that can be generated using signed combinations of previously processed elements. If a new element is at most this sum, it means it can be expressed as a combination of earlier elements with appropriate signs, so it does not introduce a new independent direction. This implies that two different sign assignments can produce the same total effect, breaking uniqueness. If every new element exceeds the current reachable range, it cannot be replicated by earlier elements, so each element contributes a new independent scale, preventing any cancellation-based collisions across the entire set.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    s = 0
    for x in a:
        if x <= s:
            print("NO")
            return
        s += x

    print("YES")

if __name__ == "__main__":
    solve()
```

The implementation follows the greedy construction exactly. Sorting ensures we always test feasibility in increasing order of magnitude. The running sum `s` tracks what can already be formed by previous elements. The moment we encounter an element that does not exceed this boundary, we detect a potential collision in representability and terminate early.

A common implementation mistake is using `<` instead of `<=`. Equality must fail because an element equal to the current sum can be replicated exactly by signed combinations of earlier elements, producing ambiguity. Another subtlety is that we only maintain a single sum; there is no need for tracking positive and negative ranges separately because symmetry is implicit in the construction.

## Worked Examples

### Example 1

Input:

```
n = 4
a = [1, 2, 3, 4]
```

Sorted array is already `[1, 2, 3, 4]`.

| Step | x | running sum before | condition (x ≤ s) | action | running sum after |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | false | add | 1 |
| 2 | 2 | 1 | false | add | 3 |
| 3 | 3 | 3 | true | stop | - |

At step 3, the value 3 is equal to the sum of previous elements. This means 3 can be formed as 1 + 2, so it introduces ambiguity. The algorithm outputs NO.

### Example 2

Input:

```
n = 4
a = [1, 3, 6, 13]
```

| Step | x | running sum before | condition (x ≤ s) | action | running sum after |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | false | add | 1 |
| 2 | 3 | 1 | false | add | 4 |
| 3 | 6 | 4 | false | add | 10 |
| 4 | 13 | 10 | false | add | 23 |

No element is ever reachable by previous sums. Each value introduces a new independent scale, so the system remains unambiguous. The output is YES.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, linear scan afterward |
| Space | O(1) extra | Only a running sum is maintained |

The constraints allow up to 100000 elements, so an n log n solution easily fits within time limits. The memory usage is constant beyond the input array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        s = 0
        for x in a:
            if x <= s:
                print("NO")
                return
            s += x
        print("YES")

    from io import StringIO
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_stdout
    return out.getvalue().strip()

# provided samples (interpreted)
assert run("4\n1 2 3 4\n") == "NO"
assert run("4\n114 515 1919 810\n") == "YES"

# custom cases
assert run("1\n1\n") == "YES"
assert run("2\n1 1\n") == "NO"
assert run("3\n1 2 4\n") == "YES"
assert run("5\n1 2 3 8 16\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1` | YES | minimal case |
| `2\n1 1` | NO | equality failure case |
| `3\n1 2 4` | YES | power-of-two safe chain |
| `5\n1 2 3 8 16` | NO | early collision via 1+2+3 |

## Edge Cases

A minimal edge case is a single constituency. With input `1`, any value trivially forms a unique system since no comparison is possible. The algorithm initializes sum to zero and immediately accepts the first value if it is positive.

For input `2\n1 1`, sorting yields `[1, 1]`. The first element sets sum to 1. The second element equals the current sum, triggering the failure condition. This reflects the fact that two identical blocks can be swapped between sides without changing the overall outcome, producing ambiguity.

For input `3\n1 2 4`, the running sum evolves as 1, 3, 7. Each element is strictly larger than the sum before it, so no element is representable by earlier ones. The algorithm confirms uniqueness correctly.

For input `5\n1 2 3 8 16`, the prefix sum reaches 6 after processing 1, 2, 3. The next element 8 is still safe, but 16 eventually exceeds the total structure in a way that still preserves strict growth; however, if we modify slightly to include 6 instead of 8, the failure appears immediately since 6 equals 1+2+3, demonstrating how subset composability breaks uniqueness even when values are not equal.
