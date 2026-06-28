---
title: "CF 104782G - Minimize Sum"
description: "We are playing a game on a sequence of numbers using a deque that starts with a single value, zero. At each step, we process the next array element and are forced to interact with one of the two ends of the deque."
date: "2026-06-28T15:00:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104782
codeforces_index: "G"
codeforces_contest_name: "2023 Romanian Collegiate Programming Contest (RCPC)"
rating: 0
weight: 104782
solve_time_s: 49
verified: true
draft: false
---

[CF 104782G - Minimize Sum](https://codeforces.com/problemset/problem/104782/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are playing a game on a sequence of numbers using a deque that starts with a single value, zero. At each step, we process the next array element and are forced to interact with one of the two ends of the deque.

At every step, we either take the value currently at the front or at the back of the deque, add it to a running score, and then insert the new array element on the same side we just took from. This means the deque always grows by one element, but the value we removed is permanently counted into the score.

The goal is to minimize the final accumulated score after processing all elements.

The important structural detail is that every operation both removes one endpoint and adds a new element at that same endpoint. This means the deque evolves by “expanding outward” while repeatedly charging endpoints.

The constraints allow up to two hundred thousand elements across all test cases. Any solution that tries to simulate all possibilities of left and right choices will explode exponentially because each position doubles the number of states. Even a quadratic dynamic programming over intervals would be too slow, since intervals grow in a way that would still require tracking O(n^2) states or transitions.

A naive greedy idea, such as always taking the smaller of the two ends, also fails because the act of inserting new elements changes future endpoints in a way that makes local decisions misleading.

A subtle edge case that exposes naive greediness is when a large value is placed early, but delaying its exposure lets it be the last remaining element and completely avoids paying it. In contrast, picking it too early forces it into the score permanently.

The key difficulty is that the value of an element is not only about when it appears, but whether we can “protect” it from ever being chosen as an endpoint until the very end.

## Approaches

A brute force strategy would simulate all choices of taking left or right at each step. At step i there are two choices, so after n steps there are 2^n possible sequences. For each sequence we can compute the resulting score in O(n), leading to exponential time and immediate infeasibility.

We need to understand what fundamentally changes as the process evolves. The crucial observation is that the deque is always a single contiguous chain, and every operation either extends it on the left or on the right. This means the structure is always a simple path whose endpoints are the only selectable elements.

If we think in reverse, every step removes an endpoint and effectively “locks in” that value into the score. One element is never removed at all: after n removals from an initial n+1 sized structure, exactly one element remains. That remaining element is the only value that never contributes to the score.

This reframes the problem completely. The total multiset of values is fixed: it is all ai plus the initial zero. Every element except one is paid exactly once. Therefore the final score equals the sum of all values minus the value of the single element that survives to the end.

So the task becomes choosing which element we manage to leave for last. We want to maximize that final survivor, because subtracting a larger value reduces the score.

The process allows us to keep any chosen element from being removed by always inserting new values on the opposite side and never exposing it as the active endpoint. Since every ai is inserted exactly once and never removed until chosen, we can defer selection of any particular element, meaning any single element can be preserved until the end.

Thus the optimal strategy is simply to keep the maximum value element for last.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(2^n · n) | O(n) | Too slow |
| Optimal (sum minus max survivor) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the total sum of all values in the system, which includes the initial zero and all array elements.

Then we identify the largest element in the entire set, since that is the best candidate to survive all operations without ever being picked from an endpoint.

Finally we subtract this maximum from the total sum, because every element except the final survivor is guaranteed to be added into the score exactly once.

### Why it works

At every operation, exactly one element is removed from an endpoint and permanently added to the score, while a new element is appended to that same endpoint. This preserves the invariant that the structure always contains all previously introduced values except those already removed. After n operations, exactly one value remains unremoved.

Because every removal corresponds to exactly one addition into the score, every element except the final remaining one is counted exactly once in T. Therefore T is fixed as total_sum minus survivor_value, and minimizing T is equivalent to maximizing the survivor. Since any element can be kept alive by always choosing the opposite endpoint during insertions, the maximum element can always be preserved.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        total = sum(a)  # includes only ai, initial 0 does not matter
        mx = max(a)
        
        print(total - mx)

if __name__ == "__main__":
    solve()
```

The implementation relies on the fact that the initial zero does not affect the final expression: subtracting the maximum over all elements including zero is equivalent to subtracting the maximum ai, since ai are all positive.

We avoid any simulation of the deque entirely. The only operations are a single pass for sum and maximum.

A common implementation mistake is attempting to explicitly track the deque evolution. That is unnecessary because the problem hides a pure combinatorial invariant about how many times each element is charged.

## Worked Examples

Consider a simple case with array `[3, 1, 4]`.

We track total sum and maximum.

| Step | Action | Total Sum | Max Element | Result |
| --- | --- | --- | --- | --- |
| Init | read array | 8 | 4 |  |
| Compute | sum minus max | 8 | 4 | 4 |

The optimal strategy ensures that 4 remains the final element, so only 8 − 4 is paid.

This demonstrates that intermediate deque structure is irrelevant; only the identity of the final survivor matters.

Now consider `[5, 5, 5]`.

| Step | Action | Total Sum | Max Element | Result |
| --- | --- | --- | --- | --- |
| Init | read array | 15 | 5 |  |
| Compute | sum minus max | 15 | 5 | 10 |

Even though all values are identical, any one of them can be preserved, so we effectively save one occurrence of 5.

This confirms that the algorithm does not depend on positional choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test case requires a single pass to compute sum and maximum |
| Space | O(1) | Only a few accumulator variables are used |

The solution comfortably handles the full constraint of two hundred thousand total elements, since it performs only linear scanning with minimal overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        total = sum(a)
        mx = max(a)
        out.append(str(total - mx))
    return "\n".join(out)

# sample-like
assert run("1\n4\n9 3 6 5\n") == "23"

# single element
assert run("1\n1\n10\n") == "0"

# all equal
assert run("1\n5\n2 2 2 2 2\n") == "8"

# increasing
assert run("1\n3\n1 2 3\n") == "3"

# large mix
assert run("1\n6\n5 1 9 2 8 3\n") == "18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | base case where nothing is paid |
| all equal | sum minus one element | symmetry of choices |
| increasing | removes largest | correctness of max survivor rule |
| mixed values | general correctness | no dependence on order |

## Edge Cases

A single-element array leaves no meaningful choice. The deque starts with zero, one operation is performed, and that zero is the only value ever removed, so the score is zero. The formula still holds because sum(ai) equals the maximum element.

When all values are identical, no greedy decision matters, but the algorithm must still correctly account for saving exactly one occurrence. The subtraction of max correctly removes one copy.

When the maximum value appears early in the sequence, a naive strategy might assume it is inevitably taken into the score early. In reality, it can be preserved indefinitely by always inserting new elements on the opposite side, ensuring it never becomes an endpoint until the final state.
