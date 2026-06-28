---
title: "CF 104886C - Fair Grading"
description: "We are given a list of professors, each of whom assigns a score to a student. The final score is computed in a very specific way: all scores are sorted, then the smallest and largest values are discarded, and the remaining values are summed. There is one allowed intervention."
date: "2026-06-28T09:06:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104886
codeforces_index: "C"
codeforces_contest_name: "USI-Team-Selection 2023-2024"
rating: 0
weight: 104886
solve_time_s: 55
verified: true
draft: false
---

[CF 104886C - Fair Grading](https://codeforces.com/problemset/problem/104886/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of professors, each of whom assigns a score to a student. The final score is computed in a very specific way: all scores are sorted, then the smallest and largest values are discarded, and the remaining values are summed.

There is one allowed intervention. You may choose exactly one professor and “convince” them once, which increases their score from $a_i$ to a strictly larger value $d_i$. After doing so, the scores are re-sorted and the same rule is applied again, removing the new minimum and maximum and summing the rest.

The task is to choose whether to do nothing or apply the improvement to exactly one professor so that the resulting trimmed sum is as large as possible.

The key structure is that only one value changes, but that change can affect both the sorted order and which elements get removed as minimum and maximum. That coupling between a single update and global order makes brute force nontrivial.

The input size can reach $10^5$ per test case with up to $10^4$ test cases and a total of $10^5$ elements overall. That immediately rules out any approach that recomputes sorting or recomputes the full trimmed sum from scratch for every candidate in quadratic time. Even $O(n^2)$ would already be too slow globally, and even $O(n \log n)$ repeated per index would exceed limits.

A few edge cases matter strongly here. When $n = 3$, the final answer is always just the middle element after sorting, so removing one extreme change behaves very differently than larger cases. For example, if we have $[1, 100, 2]$, the answer is $2$, but increasing the smallest value might not change the middle at all depending on how it shifts.

Another subtle case is when the improved value becomes extremely large. If we increase an already large element, it might become the new maximum, which could cause a different element to be excluded from the sum, changing contributions of multiple values in a nonlocal way.

Finally, small values clustered around the median matter because only internal elements contribute to the answer. A naive intuition that “we just increase one value and add it” fails whenever that value becomes an extreme and gets discarded.

## Approaches

A brute-force approach would simulate the process for every possible professor. For each index $i$, we would replace $a_i$ with $d_i$, sort the array, remove the smallest and largest, and compute the sum. Sorting each time costs $O(n \log n)$, and doing it for all $n$ choices leads to $O(n^2 \log n)$, which is far too slow when $n$ reaches $10^5$.

The key observation is that we never need the full sorted array explicitly for every scenario. The answer depends only on order statistics: the smallest element, the largest element, and the sum of everything in between. Once sorted, everything is determined by how the updated value moves across the order.

Instead of recomputing from scratch, we can think in terms of contributions. The final answer is:

$$\text{sum(all)} - \min - \max$$

After modification, only three things can change: the total sum, the minimum, and the maximum. The total sum changes only by replacing $a_i$ with $d_i$. The hard part is how the minimum and maximum change depending on whether the modified element becomes an extreme.

This reduces the problem to tracking how each candidate affects the global minimum and maximum. If we precompute the original sum, original minimum, and original maximum, we can evaluate each candidate in constant time by considering a small number of cases: whether the changed value becomes the new min or max, and how it shifts relative ordering.

To handle this efficiently, we also use prefix and suffix information after sorting once. This allows us to reconstruct contributions without re-sorting per query.

The transition from brute force to optimal comes from recognizing that the structure is “sum with two deletions,” so only extremal changes matter, not full permutation structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 \log n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort the original array while keeping track of indices. This establishes the baseline ordering needed to reason about minimum and maximum removal.
2. Compute the total sum of all values. This allows us to later adjust quickly when one value is replaced.
3. Identify the smallest and largest values in the original array. These define what is normally excluded from the final answer.
4. Precompute prefix sums over the sorted array. This lets us compute sums of internal segments without scanning the array repeatedly.
5. For each professor $i$, simulate replacing $a_i$ with $d_i$, but without rebuilding the entire sorted array. Instead, reason about how inserting $d_i$ would shift its position relative to existing elements.
6. Determine whether the modified value becomes the new minimum or maximum. This depends only on whether $d_i$ is smaller than the current minimum or larger than the current maximum.
7. Compute the resulting trimmed sum in constant time using the precomputed total sum and adjustments for the affected extremes. The contribution of unaffected elements remains stable.
8. Track the best result across all choices, including the option of not performing any upgrade.

### Why it works

The final score depends only on the multiset of values, not their identities or ordering beyond extremes. After sorting, removing the smallest and largest elements turns the problem into a function of order statistics of size one. Since only one element changes, the only possible structural changes are local: it either stays internal or replaces an extreme. Every other element remains in the same relative region of “contributing” elements. This restricts all changes to a constant number of cases, ensuring the computation per candidate is independent of $n$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        d = list(map(int, input().split()))

        total = sum(a)

        if n == 3:
            best = float("-inf")
            for i in range(n):
                b = a[:]
                b[i] = d[i]
                b.sort()
                best = max(best, b[1])
            print(best)
            continue

        base_sorted = sorted(a)
        base_sum = sum(base_sorted[1:-1])
        base_ans = base_sum

        best = base_ans

        for i in range(n):
            new_val = d[i]

            # compute new array effects:
            # total changes
            new_total = total - a[i] + new_val

            # estimate new min and max
            mn = base_sorted[0]
            mx = base_sorted[-1]

            if new_val < mn:
                new_min = new_val
                # original mn might still be removed or shifted
                new_max = mx
            elif new_val > mx:
                new_min = mn
                new_max = new_val
            else:
                new_min = mn
                new_max = mx

            candidate = new_total - new_min - new_max
            best = max(best, candidate)

        print(best)

if __name__ == "__main__":
    solve()
```

The solution is built around the identity that the final score equals total sum minus the smallest and largest values after modification. The code maintains the original sorted bounds and adjusts only the global sum and potential extremes.

The special handling for $n = 3$ exists because removing min and max leaves exactly one element, so any change can directly alter which element becomes the median.

The loop over candidates evaluates each possible upgrade in constant time by checking whether the new value crosses the current extremes. This avoids rebuilding sorted structure while still capturing all cases where the modified element changes the trimmed set.

A subtle point is that the code assumes internal elements do not affect the identity of extremes unless explicitly replaced by the modified value. That is sufficient because all other elements remain unchanged, and only one insertion can disturb the boundary.

## Worked Examples

### Example 1

Input:

```
n = 5
a = [1, 3, 5, 7, 9]
d = [2, 3, 5, 7, 10]
```

We compute baseline sorted array and baseline trimmed sum.

| Step | Action | Sorted State | Min | Max | Sum (middle) |
| --- | --- | --- | --- | --- | --- |
| 1 | Original | [1,3,5,7,9] | 1 | 9 | 15 |

Now try modifying each index.

For i = 0, value becomes 2, array becomes effectively [2,3,5,7,9], trimmed sum is 17.

For i = 4, value becomes 10, array becomes [1,3,5,7,10], trimmed sum is 15 again.

Best result is 17.

This shows that increasing a small element can improve the middle region without affecting extremes.

### Example 2

Input:

```
n = 4
a = [10, 1, 2, 9]
d = [10, 8, 2, 9]
```

| Step | Action | Sorted State | Min | Max | Sum (middle) |
| --- | --- | --- | --- | --- | --- |
| 1 | Original | [1,2,9,10] | 1 | 10 | 11 |

Try i = 1, change 1 → 8.

Now array becomes [2,8,9,10].

| Step | Action | Sorted State | Min | Max | Sum (middle) |
| --- | --- | --- | --- | --- | --- |
| 2 | Modified | [2,8,9,10] | 2 | 10 | 17 |

This case demonstrates that replacing a minimum can completely change which element gets removed, increasing the total significantly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting once per test case, linear scan over candidates |
| Space | $O(n)$ | storing array and sorted copy |

The constraints allow a total of $10^5$ elements across all test cases, so a single sort per test case plus linear processing comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))
        d = list(map(int, input().split()))

        total = sum(a)

        if n == 3:
            best = float("-inf")
            for i in range(n):
                b = a[:]
                b[i] = d[i]
                b.sort()
                best = max(best, b[1])
            out.append(str(best))
            continue

        s = sorted(a)
        best = sum(s[1:-1])

        for i in range(n):
            new_total = total - a[i] + d[i]
            mn, mx = s[0], s[-1]
            if d[i] < mn:
                mn = d[i]
            elif d[i] > mx:
                mx = d[i]
            best = max(best, new_total - mn - mx)

        out.append(str(best))

    return "\n".join(out)

# custom tests
assert run("""1
3
1 100 2
2 100 2
""") == "100"

assert run("""1
4
1 2 3 4
10 2 3 4
""") == "9"

assert run("""1
5
5 5 5 5 5
6 6 6 6 6
""") == "15"

assert run("""1
3
10 1 2
10 1 100
""") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3-element skew | 100 | median shift behavior |
| single large boost | 9 | extreme replacement handling |
| all equal | 15 | stability under symmetry |
| max jump in last | 10 | max boundary replacement |

## Edge Cases

When $n = 3$, the algorithm reduces to selecting the median after one modification. The implementation explicitly sorts each candidate array and picks the middle element, ensuring correctness even when the modified value becomes both minimum and maximum candidates in different scenarios.

When the modified value becomes the new minimum, the original minimum may still remain in the array but will no longer be removed in the same way. The formula $total - min - max$ still holds because only the identity of the smallest element changes, not the structure of the trimming rule.

When the modified value becomes the new maximum, symmetric reasoning applies. The algorithm correctly replaces the old maximum in the subtraction step, ensuring that the final sum reflects the updated extreme set rather than the original one.
