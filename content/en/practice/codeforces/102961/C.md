---
title: "CF 102961C - Ferris Wheel"
description: "We are given a line of people, each with a weight, and a Ferris wheel where each cabin can hold at most two people as long as their combined weight does not exceed a fixed limit."
date: "2026-07-04T06:50:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102961
codeforces_index: "C"
codeforces_contest_name: "CSES Problem Set: Sorting and Searching"
rating: 0
weight: 102961
solve_time_s: 44
verified: true
draft: false
---

[CF 102961C - Ferris Wheel](https://codeforces.com/problemset/problem/102961/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of people, each with a weight, and a Ferris wheel where each cabin can hold at most two people as long as their combined weight does not exceed a fixed limit. Every person must be placed into exactly one cabin, and the goal is to minimize how many cabins are used.

The input describes the number of people, the weight limit per cabin, and a list of individual weights. The output is a single number: the smallest number of cabins needed to seat everyone under the constraint that each cabin holds one or two people whose total weight does not exceed the limit.

The key constraint that drives the solution is that the number of people can be large, typically up to the order of 200,000. That immediately rules out any quadratic pairing strategy where we try all combinations of people. A solution that checks every pair would require on the order of n² operations, which would not complete within the time limit. Even an O(n log n) solution must be carefully designed so that sorting does not get dominated by repeated scanning.

A common failure case appears when a greedy strategy is applied without ordering. For example, pairing each person with the next available person in input order can fail badly.

Consider an input like:

```
n = 4, x = 10
weights = [9, 1, 8, 2]
```

If we greedily pair adjacent elements, we get (9,1) and (8,2), which uses 2 cabins and is optimal here. But on a slightly different ordering:

```
weights = [9, 8, 1, 2]
```

Adjacent pairing gives (9,8) invalid, so a naive repair might isolate 9, then pair 8 with 1, and leave 2 alone, resulting in 3 cabins. The optimal solution is (9,1) and (8,2), only 2 cabins. This shows that without sorting or a global strategy, local decisions can block better pairings.

Another subtle issue is forgetting that pairing is optional. Even if two small weights fit together, forcing them to pair can prevent a larger weight from being paired later, increasing total cabins.

## Approaches

The brute-force idea is to try assigning people into cabins in all possible ways, either placing each person alone or pairing them with someone else whose combined weight is valid. This corresponds to exploring all matchings in a compatibility graph where an edge exists if two weights sum to at most the limit. While correct in principle, the number of states grows exponentially, because each person can be paired or unpaired in many configurations, and choices interact globally. In the worst case, this becomes combinatorial explosion on the order of roughly 2ⁿ states.

The key structural observation is that once we sort the weights, we gain a monotonic ordering that lets us make safe greedy decisions. The heaviest remaining person is the hardest to place. If that person can be paired with anyone, the best candidate is the lightest remaining person. If even that does not fit, then the heaviest must go alone. This removes the need to explore multiple pairings because any other pairing for the heaviest would only use a heavier partner and is therefore never better.

This reduces the problem to a two-pointer process over a sorted array, where we repeatedly attempt to match the smallest and largest remaining elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal Greedy (Sorting + Two Pointers) | O(n log n) | O(1) extra / O(n) total | Accepted |

## Algorithm Walkthrough

### Optimal Strategy

1. Sort all weights in non-decreasing order. This creates a structure where the lightest and heaviest remaining elements are always easy to identify.
2. Initialize two pointers, one at the start of the array and one at the end. These represent the lightest and heaviest unassigned people.
3. Maintain a counter for the number of cabins used.
4. While the left pointer does not pass the right pointer, consider the current heaviest person at the right pointer.
5. If the lightest and heaviest together do not exceed the limit, assign them to the same cabin and move both pointers inward. This is justified because pairing the heaviest with the smallest possible partner maximizes the chance of future pairings.
6. If they exceed the limit, assign the heaviest person alone and move only the right pointer inward. This is necessary because no valid pairing exists for this heaviest person under the current constraint.
7. Increment the cabin counter for every assignment.
8. Continue until all people are assigned.

### Why it works

The algorithm maintains the invariant that all people outside the current pointers have already been assigned to cabins optimally under the same greedy rule. At each step, the decision focuses on the heaviest remaining person. Any feasible pairing for that person must involve someone no heavier than the current lightest candidate, so checking the smallest remaining weight is sufficient to determine whether pairing is possible. Since choosing the smallest possible partner never worsens future feasibility for remaining elements, the greedy choice preserves optimality throughout the process.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    
    l, r = 0, n - 1
    ans = 0
    
    while l <= r:
        ans += 1
        if l == r:
            break
        if a[l] + a[r] <= x:
            l += 1
            r -= 1
        else:
            r -= 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the array so that we can reason about extremes. The two-pointer loop always assigns exactly one cabin per iteration, either to a pair or a single heavy individual. The special case `l == r` handles the last remaining person cleanly, preventing double counting or invalid pairing attempts.

A common implementation pitfall is forgetting to increment the answer in both the paired and unpaired cases. Another is mishandling the termination condition, especially when only one element remains.

## Worked Examples

### Example 1

Input:

```
n = 4, x = 10
weights = [9, 1, 8, 2]
```

After sorting:

```
[1, 2, 8, 9]
```

| Step | Left | Right | Pair Attempt | Action | Cabins |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 9 | 1 + 9 = 10 | Pair | 1 |
| 2 | 2 | 8 | 2 + 8 = 10 | Pair | 2 |

The process finishes with all people assigned in two cabins. This shows how sorting transforms an apparently unstructured pairing problem into a clean boundary process.

### Example 2

Input:

```
n = 5, x = 6
weights = [3, 5, 2, 1, 4]
```

Sorted:

```
[1, 2, 3, 4, 5]
```

| Step | Left | Right | Pair Attempt | Action | Cabins |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 1 + 5 = 6 | Pair | 1 |
| 2 | 2 | 4 | 2 + 4 = 6 | Pair | 2 |
| 3 | 3 | 3 | single | Alone | 3 |

This trace highlights the odd-length case where one person remains unpaired at the end, forcing a single occupancy cabin.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, two-pointer scan is linear |
| Space | O(1) extra | Only pointers and counters used beyond input storage |

The solution easily fits within constraints for large inputs since sorting 200,000 elements is well within typical limits, and the linear scan is negligible compared to it.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from types import SimpleNamespace

    # re-run solution inline
    input = sys.stdin.readline

    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    l, r = 0, n - 1
    ans = 0

    while l <= r:
        ans += 1
        if l == r:
            break
        if a[l] + a[r] <= x:
            l += 1
            r -= 1
        else:
            r -= 1

    return str(ans)

# provided sample-style tests
assert run("4 10\n9 1 8 2\n") == "2"

# all fit individually
assert run("3 5\n4 4 4\n") == "3"

# all pairable
assert run("4 10\n1 2 3 4\n") == "2"

# alternating tight case
assert run("5 6\n3 5 2 1 4\n") == "3"

# single element
assert run("1 100\n42\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 10 / 9 1 8 2 | 2 | basic greedy pairing |
| 3 5 / 4 4 4 | 3 | no pairing possible |
| 4 10 / 1 2 3 4 | 2 | full pairing possible |
| 5 6 / 3 5 2 1 4 | 3 | mixed pairing + leftover |
| 1 100 / 42 | 1 | single element edge case |

## Edge Cases

One edge case is when only one person exists. After sorting, both pointers start at the same index. The algorithm immediately increments the cabin count once and exits when `l == r`, correctly returning 1.

Another case is when all weights exceed half the limit, making all pairing impossible. The algorithm always fails the sum check and repeatedly decrements the right pointer, assigning each person alone. The result is exactly n cabins, which is correct because no valid pairs exist.

A final case is when all weights are very small, allowing full pairing. The algorithm always succeeds in pairing left and right pointers until they meet or cross, producing exactly ⌈n/2⌉ cabins.
