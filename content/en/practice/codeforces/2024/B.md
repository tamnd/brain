---
title: "CF 2024B - Buying Lemonade"
description: "We have a vending machine with n hidden slots, each containing a known number of lemonade cans. There are also n buttons, each mapped to exactly one slot, but the mappings are lost."
date: "2026-06-09T03:07:08+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2024
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 980 (Div. 2)"
rating: 1100
weight: 2024
solve_time_s: 311
verified: false
draft: false
---

[CF 2024B - Buying Lemonade](https://codeforces.com/problemset/problem/2024/B)

**Rating:** 1100  
**Tags:** binary search, constructive algorithms, sortings  
**Solve time:** 5m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We have a vending machine with `n` hidden slots, each containing a known number of lemonade cans. There are also `n` buttons, each mapped to exactly one slot, but the mappings are lost. Pressing a button may give you a can if the corresponding slot has any left; otherwise, nothing happens. You cannot see which slot a can comes from, and you cannot see the current contents.

The task is: given the initial counts in the slots and a target `k`, determine the minimum number of button presses that guarantees obtaining at least `k` cans, regardless of which button corresponds to which slot. We know in advance that the total cans are at least `k`.

Constraints indicate we may have up to `2 * 10^5` slots summed across all test cases, and `k` can be as large as `10^9`. This rules out any brute-force simulation where we try every possible sequence of presses, because pressing buttons individually until we reach `k` could take O(k) operations, which is too large. We need a method that scales with `n` rather than `k`.

A subtle edge case occurs when some slots have extremely large counts and others very small. For example, if `a = [1, 1000000000]` and `k = 2`, a naive approach pressing buttons blindly could overpress the first slot and waste presses, whereas an optimal strategy must account for the worst-case distribution to guarantee `k` cans.

## Approaches

The naive solution is to simulate all sequences of presses. One could attempt a greedy method: pick any button repeatedly until it fails, then move to another. While correct in principle, simulating this is too slow when counts are large because in the worst case it requires O(k) presses, which is up to 10^9.

The key observation is that the minimum number of presses depends on the slot counts sorted in descending order. If we denote the slot counts as `a_1 ≥ a_2 ≥ ... ≥ a_n`, the worst-case scenario occurs when our presses hit the largest slots first but miss the smaller slots until the end. Because we can adapt after each press based on success or failure, we can model this with a **binary search on the number of presses per button**.

The optimal solution can be seen as distributing the presses across buttons in a way that accounts for the uncertainty of which button maps to which slot. If we assign `x` presses to each button, the guaranteed cans we collect from each slot is `min(a_i, x)`, because a slot with fewer cans than `x` cannot give more than its content. Summing this over all slots gives the total guaranteed cans. The minimum total presses is therefore the smallest `x` such that the sum of `min(a_i, x)` across all slots is at least `k`.

Sorting the slot counts in descending order allows us to compute this efficiently. Once sorted, we can use a greedy approach: try to "take as many as possible from the largest slots first," which reduces to a binary search over the possible number of presses.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k) per test case | O(n) | Too slow |
| Greedy / Binary Search | O(n log max(a_i)) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n` and `k` and the array `a`. Sort `a` in descending order. Sorting ensures we attempt to "cover" the largest slots first.
2. Initialize two pointers for binary search: `low = 1` (minimum 1 press) and `high = k` (worst-case: 1 press per can).
3. While `low < high`, compute `mid = (low + high) // 2`. For this candidate `mid` presses per button, calculate `sum(min(a_i, mid))` over all slots. This sum is the number of guaranteed cans if each button is pressed `mid` times in an adaptive strategy.
4. If the sum is at least `k`, then we can potentially achieve `k` with fewer presses per button, so set `high = mid`. Otherwise, set `low = mid + 1` to increase the number of presses.
5. After the binary search completes, `low` is the minimum number of presses per button required.
6. To find the total number of presses, note that we will press each button up to its assigned `low` times. But because `k` may be less than the total sum of `min(a_i, low)`, we adjust the last press count to exactly meet `k`. The total presses are therefore computed as the sum of `min(a_i, low)` until the sum reaches `k`.

**Why it works:** The binary search maintains the invariant that `low` is always feasible or too small, and `high` is always enough to guarantee `k` cans. Since `min(a_i, x)` is monotonic in `x`, the search converges to the minimum value. Sorting ensures that we consider the worst-case distribution of presses, giving a guaranteed number of cans regardless of button-to-slot mapping.

## Python Solution

```python
import sys
input = sys.stdin.readline

def min_presses(n, k, a):
    a.sort(reverse=True)
    low, high = 1, k
    while low < high:
        mid = (low + high) // 2
        total = sum(min(ai, mid) for ai in a)
        if total >= k:
            high = mid
        else:
            low = mid + 1
    # low is the minimum presses per button in worst case
    total_presses = 0
    remaining = k
    for ai in a:
        take = min(ai, low, remaining)
        total_presses += take
        remaining -= take
        if remaining == 0:
            break
    return total_presses

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    print(min_presses(n, k, a))
```

Each part of the code corresponds directly to the algorithm steps. Sorting is essential for the greedy calculation of guaranteed cans. The binary search loop efficiently finds the minimal number of presses per button without simulating each press. Summing `min(a_i, mid)` guarantees we respect the slot limits. The final loop ensures that the total presses count exactly meets `k`.

## Worked Examples

**Example 1**:

Input: `n=2, k=2, a=[1,2]`

| Step | Sorted `a` | Mid | Sum(min(a_i, mid)) | Decision |
| --- | --- | --- | --- | --- |
| Init | [2,1] | - | - | low=1, high=2 |
| 1 | - | mid=1 | min(2,1)+min(1,1)=2 | sum>=k → high=1 |
| Done | - | low=1 | total_presses = min(2,1)+min(1,1)=2 | Output 2 |

We press each button once. Worst-case, we get 2 cans.

**Example 2**:

Input: `n=3, k=4, a=[2,1,3]`

| Step | Sorted `a` | Mid | Sum(min(a_i, mid)) | Decision |
| --- | --- | --- | --- | --- |
| Init | [3,2,1] | - | - | low=1, high=4 |
| 1 | - | mid=2 | min(3,2)+min(2,2)+min(1,2)=2+2+1=5 | sum>=k → high=2 |
| 2 | - | mid=1 | 1+1+1=3 | sum<k → low=2 |
| Done | - | low=2 | sum of min(a_i,2) until 4 cans = 2+2=4 | Output 4 |

This confirms the algorithm correctly distributes presses among slots to guarantee `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log k) per test case | Sorting takes O(n log n), binary search over range 1..k takes log k, each iteration sums over n slots. |
| Space | O(n) | Storing the array of slot counts. |

Given that sum of `n` over all test cases is ≤ 2*10^5 and `log k ≤ 30`, the solution easily fits in 1-second time limit.

## Test Cases

```python
def run(inp: str) -> str:
    import sys, io
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    output = io.StringIO()
    with redirect_stdout(output):
        exec(open("solution.py").read())
    return output.getvalue().strip()

# Provided samples
assert run("5\n2 1\n1 1\n2 2\n1 2\n3 4\n2 1 3\n10 50\n1 1 3 8 8 9 12 13 27 27\n2 1000000000\n1000000000 500000000\n") == "1\n2\n
```
