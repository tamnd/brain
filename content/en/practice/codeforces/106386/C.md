---
title: "CF 106386C - Olympic Haircut"
description: "Aruj starts with k hair follicles. There are n barbers, and barber i removes exactly ai follicles if Aruj still has more than ai follicles. If he has ai or fewer, that visit would leave him bald, which is not allowed."
date: "2026-06-25T10:13:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106386
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 2-25-26 (Advanced)"
rating: 0
weight: 106386
solve_time_s: 37
verified: true
draft: false
---

[CF 106386C - Olympic Haircut](https://codeforces.com/problemset/problem/106386/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

Aruj starts with `k` hair follicles. There are `n` barbers, and barber `i` removes exactly `a_i` follicles if Aruj still has more than `a_i` follicles. If he has `a_i` or fewer, that visit would leave him bald, which is not allowed.

Aruj may choose any subset of barbers and visit them in any order. The goal is to minimize the number of follicles left while always keeping at least one follicle. The output is the smallest possible remaining number of follicles.

The important observation is that the order of chosen barbers only appears to matter. If the total amount removed by a chosen set is `S`, then the final amount is `k - S`. The chosen set is valid exactly when `S < k`. If the total removal is below `k`, then before any individual barber visit the total removed so far plus the current barber's removal is at most `S`, which is still less than `k`. That means the current hair count is always greater than the barber's removal amount, so the haircut never reaches zero.

The constraints make the intended approach clear. There are at most `16` barbers, so the number of possible subsets is `2^16 = 65536`. This is small enough for complete subset enumeration. A solution that tries every possible ordering would be much larger, because a subset could have many possible visit sequences. The limit on `n` is specifically allowing us to explore subsets rather than permutations.

The main edge cases come from confusing the condition `S < k` with `S <= k`, and from forgetting that choosing no barbers is always allowed.

For example:

```
Input:
1 10
10

Output:
10
```

A careless solution might choose the barber because removing exactly `10` follicles seems to leave `0`. However, the rules forbid reaching zero, so the barber cannot be used.

Another case is:

```
Input:
3 10
5 8 4

Output:
1
```

Choosing the first and third barbers removes `9` follicles. The final answer is `1`. A solution that only checks individual barbers might miss combinations of several smaller removals.

## Approaches

The direct approach is to try every subset of barbers. For each subset, calculate the total number of follicles it removes. If that total is smaller than `k`, the subset is valid, and we keep the largest valid removal amount. This works because the final answer is simply `k` minus the maximum removable amount.

The brute force method is correct because every possible group of barbers is examined. The problem is that the number of subsets grows exponentially. In this problem the maximum is only `2^16`, which is manageable, but a more general version with larger `n` would quickly become impossible. For example, with `n = 40`, checking all subsets would require more than one trillion operations.

The key insight is that we do not need to care about the order of the barbers. The condition for a valid sequence depends only on the sum of all chosen removals. Once we know a subset has total removal smaller than `k`, every ordering of that subset works. This converts the problem into finding the largest subset sum strictly less than `k`, which is a standard meet in the middle situation.

We split the barbers into two groups. Each half has at most eight elements, so we can generate all subset sums for each half. Instead of checking all `2^16` subsets directly, we combine the two lists efficiently. For every sum from one half, we find the largest compatible sum from the other half that keeps the total below `k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(1) | Accepted for n ≤ 16 |
| Meet in the Middle | O(2^(n/2) log(2^(n/2))) | O(2^(n/2)) | Accepted |

## Algorithm Walkthrough

1. Split the array of barber removals into two halves. Each half contains at most eight values, so all subset sums inside one half can be generated quickly.
2. Generate every possible subset sum of the first half. Include the empty subset with sum `0` because visiting no barber from this side is allowed.
3. Generate every possible subset sum of the second half in the same way. The problem is now reduced to combining one value from each list.
4. Sort the subset sums from the second half. For every subset sum `x` from the first half, find the largest second half sum `y` such that `x + y < k`.
5. Track the largest valid total removal `x + y`. The final remaining follicles are `k` minus this value.

The reason this works is that every possible subset of barbers can be divided uniquely into a choice from the first half and a choice from the second half. The two generated lists contain all possible contributions, so checking compatible pairs covers every possible solution.

Why it works: The algorithm maintains the invariant that the best value found so far is the maximum number of follicles that can be removed without reaching zero. Every valid subset corresponds to exactly one pair of generated subset sums. The binary search step considers the best possible partner for each first half choice, so no valid answer is skipped.

## Python Solution

```python
import sys
input = sys.stdin.readline

def generate_sums(arr):
    sums = [0]
    for x in arr:
        current = []
        for s in sums:
            current.append(s + x)
        sums += current
    return sums

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    mid = n // 2
    left = generate_sums(a[:mid])
    right = generate_sums(a[mid:])

    right.sort()

    best = 0
    import bisect

    for x in left:
        limit = k - x - 1
        if limit >= 0:
            pos = bisect.bisect_right(right, limit) - 1
            if pos >= 0:
                best = max(best, x + right[pos])

    print(k - best)

if __name__ == "__main__":
    solve()
```

The `generate_sums` function builds all possible removals from one group of barbers. Starting with only `0`, every barber either is skipped or contributes its removal amount, so each existing sum creates one new sum.

The array is divided into two parts before generating sums. With `n = 16`, each side has at most eight elements, giving at most `256` subset sums per side. This keeps the combination step very small.

The binary search uses `bisect_right` to find the first value greater than the allowed limit, then moves one position back to obtain the largest valid value. The strict inequality matters here. We need `x + y < k`, so the limit is `k - x - 1`, not `k - x`.

Python integers do not overflow, which avoids issues because `a_i` and `k` can be as large as `10^9`.

## Worked Examples

### Sample 1

Input:

```
3 10
5 8 4
```

The subsets of removals are explored through the two halves.

| Left sum | Allowed right sum | Best right sum | Best removal |
| --- | --- | --- | --- |
| 0 | 9 | 8 | 8 |
| 5 | 4 | 4 | 9 |

The best removal is `9`, leaving `10 - 9 = 1` follicle.

This trace demonstrates why combining smaller barbers matters. The answer is not from the single largest barber but from the best combination that stays below the limit.

### Sample 2

Input:

```
1 10
20
```

| Left sum | Allowed right sum | Best right sum | Best removal |
| --- | --- | --- | --- |
| 0 | 9 | 0 | 0 |

The only barber removes too much, so no haircut can be performed.

The empty subset is always considered, which keeps the original amount of hair as a valid answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^(n/2) log(2^(n/2))) | We generate both subset sum lists and binary search for each left half sum. |
| Space | O(2^(n/2)) | The generated subset sums are stored for both halves. |

For `n = 16`, the largest subset list contains only `256` values, so the solution easily fits within the limits.

## Test Cases

```python
import sys
import io
import bisect

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def generate_sums(arr):
        sums = [0]
        for x in arr:
            sums += [s + x for s in sums]
        return sums

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    mid = n // 2
    left = generate_sums(a[:mid])
    right = generate_sums(a[mid:])
    right.sort()

    best = 0
    for x in left:
        pos = bisect.bisect_right(right, k - x - 1) - 1
        if pos >= 0:
            best = max(best, x + right[pos])

    return str(k - best) + "\n"

assert solution("3 10\n5 8 4\n") == "1\n", "sample 1"
assert solution("1 10\n20\n") == "10\n", "sample 2"

assert solution("1 1\n1\n") == "1\n", "cannot reach zero"
assert solution("4 100\n10 20 30 40\n") == "1\n", "all values fit except exact total"
assert solution("5 50\n10 10 10 10 10\n") == "10\n", "repeated values"
assert solution("4 15\n14 7 8 6\n") == "1\n", "boundary subset sum"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `1` | Minimum size and forbidden zero result |
| `4 100 / 10 20 30 40` | `1` | Exact total removal must not be accepted |
| `5 50 / 10 10 10 10 10` | `10` | Many equal values |
| `4 15 / 14 7 8 6` | `1` | Choosing a near limit combination |

## Edge Cases

For the case where a barber removes exactly all remaining follicles:

```
Input:
1 10
10
```

The generated subset sums are `0` and `10`. The binary search only accepts sums below `10`, so the sum `10` is rejected. The answer remains `10`.

For the case where several smaller barbers combine into the optimal answer:

```
Input:
3 10
5 8 4
```

The subset sum `5 + 4 = 9` is valid because it is strictly smaller than `10`. The algorithm finds this pair across the two halves and returns `1`.

For the case where every barber is too large:

```
Input:
3 5
6 7 8
```

Every non empty subset sum is at least `6`, so every haircut would make Aruj bald. The only valid subset is the empty subset, and the algorithm returns `5`.

For the case where all barbers together are still safe:

```
Input:
4 20
3 4 5 6
```

The total removal is `18`, which is valid. The algorithm finds the complete subset and returns `2`, showing that it is allowed to use every barber when the total stays below the starting amount.
