---
title: "CF 1119B - Alyona and a Narrow Fridge"
description: "The fridge has height h and exactly two columns. Shelves can be inserted at any heights, which means we are free to divide the fridge into horizontal compartments of arbitrary heights. Each bottle occupies one column and has height a[i]."
date: "2026-06-12T04:28:46+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "flows", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1119
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 2"
rating: 1300
weight: 1119
solve_time_s: 114
verified: true
draft: false
---

[CF 1119B - Alyona and a Narrow Fridge](https://codeforces.com/problemset/problem/1119/B)

**Rating:** 1300  
**Tags:** binary search, flows, greedy, sortings  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The fridge has height `h` and exactly two columns. Shelves can be inserted at any heights, which means we are free to divide the fridge into horizontal compartments of arbitrary heights. Each bottle occupies one column and has height `a[i]`.

The task is not to choose any subset of bottles. We must consider bottles in order and find the largest `k` such that bottles `1..k` can all be placed inside the fridge simultaneously.

The key observation is that every compartment created by shelves has width 2. At most two bottles can occupy the same vertical level because the fridge has only two columns. If two bottles share a compartment, the compartment height must be at least the taller of the two bottles. Since shelves can be placed anywhere, only the required heights matter.

The number of bottles is at most `1000`. This is small enough that even an `O(n² log n)` solution is perfectly acceptable. The fridge height can be as large as `10^9`, but height values are only used in arithmetic comparisons, so the large bound does not create any difficulty.

A common mistake is to add the heights of all bottles. For example:

```
3 7
2 3 5
```

The answer is `3`, even though `2 + 3 + 5 = 10 > 7`.

The reason is that bottles can stand side by side. Pairing heights `(5,3)` uses only `5` units of vertical space, and bottle `2` uses another `2`, for a total of `7`.

Another easy mistake is pairing bottles arbitrarily instead of optimally.

```
4 8
1 4 4 4
```

After sorting we get `[1,4,4,4]`.

Pairing `(1,4)` and `(4,4)` requires `4 + 4 = 8`, which fits.

A careless arrangement such as `(1)` + `(4)` + `(4,4)` requires `1 + 4 + 4 = 9`, which does not fit.

The feasibility check must always use the best possible pairing strategy.

A third subtle case occurs when the number of bottles is odd.

```
3 6
1 2 4
```

Sorted heights are `[1,2,4]`.

The optimal arrangement uses the largest bottle alone and pairs the remaining two. Required height is `4 + 1 = 5`, not `4 + 2 = 6`. Handling odd counts incorrectly often produces wrong answers.

## Approaches

A brute-force solution would try every `k` from `1` to `n` and determine whether bottles `1..k` fit. To check feasibility, we could enumerate all possible pairings of bottles into two-column compartments and compute the minimum required height. This is clearly correct because it examines every arrangement, but the number of pairings grows exponentially and becomes completely impractical.

The structure of the fridge gives a much stronger observation. Since each level has width 2, every compartment contributes the maximum height among the bottles placed in it. To minimize total used height, we should place the tallest bottles in separate compartments whenever necessary and pair smaller bottles with them.

Suppose we want to test whether the first `k` bottles fit. Take their heights and sort them.

For an even number of bottles:

```
b0 ≤ b1 ≤ b2 ≤ b3 ≤ ... ≤ b(k-1)
```

The optimal arrangement pairs neighboring bottles from the top:

```
(b(k-2), b(k-1))
(b(k-4), b(k-3))
...
```

The required height becomes:

```
b(k-1) + b(k-3) + ...
```

For an odd number of bottles, the smallest bottle occupies a compartment alone, and the remaining bottles are paired similarly. The required height is again obtained by summing every second element from the end of the sorted array.

This gives an efficient feasibility test.

If the first `k` bottles fit, then any smaller prefix also fits because removing bottles cannot make placement harder. That monotonicity allows binary search on `k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log² n) | O(n) | Accepted |

## Approaches

The feasibility condition is monotonic. If bottles `1..k` fit, then bottles `1..(k-1)` also fit.

That immediately suggests binary search on the answer.

For a candidate `k`, we extract the first `k` heights, sort them, and compute the minimum fridge height required.

After sorting, the optimal strategy is to pair bottles so that the largest bottle in each pair contributes to the total. The largest bottle must contribute its full height no matter what it is paired with. The second-largest contributor should be as small as possible, which is achieved by pairing large bottles together.

As a result, the required height is simply the sum of elements at positions:

```
last, last-2, last-4, ...
```

in the sorted array.

If this sum does not exceed `h`, the prefix is feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log² n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Binary search the answer `k` in the range `[1, n]`.
2. For a candidate value `k`, take the first `k` bottle heights.
3. Sort these heights in nondecreasing order.
4. Starting from the largest element, move left by two positions each time and add those heights to a running sum.
5. This sum equals the minimum fridge height required for these `k` bottles.
6. If the sum is at most `h`, mark `k` as feasible and continue searching to the right.
7. Otherwise search to the left.
8. The largest feasible value found during binary search is the answer.

### Why it works

After sorting, every compartment contributes the height of its tallest bottle. To minimize the total contribution, the largest bottles should be paired together. Then the set of compartment heights becomes exactly the elements at positions `last, last-2, last-4, ...`.

Any other pairing would force some larger bottle to become the maximum of an additional compartment and could not reduce the total required height. Thus the feasibility test computes the true minimum height needed for the chosen prefix.

Because feasibility is monotonic with respect to `k`, binary search correctly finds the largest valid prefix.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_fit(k, a, h):
    b = sorted(a[:k])

    need = 0
    i = k - 1

    while i >= 0:
        need += b[i]
        i -= 2

    return need <= h

def solve():
    n, h = map(int, input().split())
    a = list(map(int, input().split()))

    lo, hi = 1, n
    ans = 1

    while lo <= hi:
        mid = (lo + hi) // 2

        if can_fit(mid, a, h):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The helper function performs the feasibility check. It sorts the first `k` bottles and computes the minimum required height by summing every second element from the end.

The binary search maintains the invariant that all feasible answers lie on the left side of the first infeasible value. When a candidate works, we record it and search for a larger prefix. When it fails, we search among smaller prefixes.

A common implementation mistake is summing adjacent pairs explicitly. That works but introduces extra indexing logic. Summing elements at positions `k-1, k-3, k-5, ...` directly is simpler and corresponds exactly to the compartment heights.

Another subtle point is that `ans` can safely start at `1`. The statement guarantees that at least one bottle always fits because every bottle height is at most `h`.

## Worked Examples

### Example 1

Input:

```
5 7
2 3 5 4 1
```

Binary search checks:

| k | Sorted prefix | Heights summed | Required height | Feasible |
| --- | --- | --- | --- | --- |
| 3 | [2,3,5] | 5 + 2 | 7 | Yes |
| 4 | [2,3,4,5] | 5 + 3 | 8 | No |

The largest feasible value is `3`.

This trace shows the odd-sized case. The largest bottle contributes `5`, and the remaining two bottles together contribute only `2`.

### Example 2

Input:

```
4 8
1 4 4 4
```

| k | Sorted prefix | Heights summed | Required height | Feasible |
| --- | --- | --- | --- | --- |
| 2 | [1,4] | 4 | Yes |  |
| 3 | [1,4,4] | 4 + 1 = 5 | Yes |  |
| 4 | [1,4,4,4] | 4 + 4 = 8 | Yes |  |

Answer:

```
4
```

This example demonstrates why pairing large bottles together is optimal. The required height becomes exactly `8`, which fits the fridge.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log² n) | Binary search performs O(log n) checks, each sorting up to n elements |
| Space | O(n) | Temporary sorted array for feasibility testing |

With `n ≤ 1000`, the worst-case work is roughly `1000 × log²(1000)`, which is far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    n, h = map(int, input().split())
    a = list(map(int, input().split())

    def can_fit(k):
        b = sorted(a[:k])
        need = 0
        i = k - 1
        while i >= 0:
            need += b[i]
            i -= 2
        return need <= h

    lo, hi = 1, n
    ans = 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if can_fit(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

def run(inp: str) -> str:
    global input
    input = io.StringIO(inp).readline

    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old
    return out.getvalue().strip()

# provided sample
assert run("5 7\n2 3 5 4 1\n") == "3", "sample 1"

# minimum size
assert run("1 5\n5\n") == "1", "single bottle"

# all equal
assert run("4 6\n3 3 3 3\n") == "4", "all equal heights"

# odd count boundary
assert run("3 6\n1 2 4\n") == "3", "odd number of bottles"

# answer not equal to n
assert run("5 5\n5 5 5 5 5\n") == "2", "largest valid prefix"

# larger prefix barely fits
assert run("4 8\n1 4 4 4\n") == "4", "exact height match"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 / 5` | `1` | Minimum input size |
| `4 6 / 3 3 3 3` | `4` | All heights equal |
| `3 6 / 1 2 4` | `3` | Odd-sized prefix handling |
| `5 5 / 5 5 5 5 5` | `2` | Binary search boundary |
| `4 8 / 1 4 4 4` | `4` | Exact fit at fridge height |

## Edge Cases

### Odd number of bottles

Input:

```
3 6
1 2 4
```

Sorted prefix:

```
[1, 2, 4]
```

The algorithm sums positions `2` and `0`, giving:

```
4 + 1 = 5
```

Since `5 ≤ 6`, all three bottles fit. An incorrect implementation might sum `4 + 2 = 6` by pairing incorrectly, which still works here but fails on similar inputs.

### Exact height match

Input:

```
4 8
1 4 4 4
```

Sorted:

```
[1, 4, 4, 4]
```

Required height:

```
4 + 4 = 8
```

The algorithm accepts equality because the condition is `need <= h`. Using a strict inequality would incorrectly reject this case.

### Many tall bottles

Input:

```
5 5
5 5 5 5 5
```

For `k = 2`:

```
need = 5
```

Feasible.

For `k = 3`:

```
need = 5 + 5 = 10
```

Not feasible.

Binary search correctly returns `2`. This case verifies that the monotonic property holds and that the search stops at the largest feasible prefix.

### Small bottle paired with a large bottle

Input:

```
4 7
1 1 1 7
```

Sorted:

```
[1, 1, 1, 7]
```

Required height:

```
7 + 1 = 8
```

The answer is not automatically `4` just because three bottles are tiny. The tallest bottle dominates its compartment, and the algorithm captures that by summing every second element from the end.
