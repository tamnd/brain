---
title: "CF 149A - Business trip"
description: "Petya can decide in which months he waters the flower. Each month contributes a fixed amount of growth, and skipping a month contributes nothing. The goal is to reach at least k centimeters of total growth while using as few months as possible."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 149
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 106 (Div. 2)"
rating: 900
weight: 149
solve_time_s: 93
verified: true
draft: false
---

[CF 149A - Business trip](https://codeforces.com/problemset/problem/149/A)

**Rating:** 900  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

Petya can decide in which months he waters the flower. Each month contributes a fixed amount of growth, and skipping a month contributes nothing. The goal is to reach at least `k` centimeters of total growth while using as few months as possible.

The input gives the required growth `k`, followed by 12 integers. The `i`-th integer tells us how much the flower grows if Petya waters it during month `i`.

The output is the minimum number of months needed to reach at least `k` total growth. If even watering during all 12 months is not enough, the answer is `-1`.

The constraints are tiny. There are always exactly 12 months, so even exponential approaches are technically possible. A brute-force solution over all subsets would check `2^12 = 4096` combinations, which is still completely fine within 2 seconds. Still, the problem is designed to teach a greedy observation, and the cleanest solution runs in essentially constant time.

The tricky cases are not about performance, they are about handling special situations correctly.

One important edge case is when `k = 0`.

Input:

```
0
0 0 0 0 0 0 0 0 0 0 0 0
```

Correct output:

```
0
```

Petya already satisfies the requirement without watering at all. A careless implementation might still pick months unnecessarily.

Another edge case is when the total yearly growth is insufficient.

Input:

```
15
1 1 1 1 1 1 1 1 1 1 1 1
```

Correct output:

```
-1
```

Even using every month only gives total growth `12`. Forgetting this check can produce an incorrect positive answer.

A more subtle case happens when several months have zero growth.

Input:

```
5
5 0 0 0 0 0 0 0 0 0 0 0
```

Correct output:

```
1
```

If the implementation processes months in arbitrary order instead of prioritizing the largest gains first, it may count useless zero-growth months before reaching the target.

## Approaches

A direct brute-force approach would try every subset of the 12 months. For each subset, we compute the total growth and count how many selected months it uses. Among all subsets whose total growth is at least `k`, we choose the minimum count.

This works because there are only 12 months. The total number of subsets is `2^12 = 4096`, and for each subset we may inspect all 12 months, giving roughly 50,000 operations.

The weakness of brute force is that it ignores the structure of the problem. We do not actually care which specific months are chosen. We only care about the growth values contributed by those months.

The key observation is simple: if we want to minimize the number of selected months, we should always take the largest available growth values first.

Suppose we picked a smaller month while leaving a larger month unused. Replacing the smaller one with the larger one can only increase the total growth without increasing the number of months. Because of that, any optimal solution can be transformed into one that uses the largest available months first.

That immediately suggests a greedy strategy:

1. Sort the monthly growth values in descending order.
2. Keep taking the next largest month until the accumulated growth reaches at least `k`.
3. If all months are used and the target is still unreachable, print `-1`.

With only 12 numbers, sorting is trivial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^12 × 12) | O(1) | Accepted |
| Optimal | O(12 log 12) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the target growth `k` and the 12 monthly growth values.
2. Handle the special case `k = 0`.

If no growth is required, Petya does not need to water the flower at all, so the answer is `0`.
3. Sort the 12 growth values in descending order.

The largest growth months should be considered first because they help us reach the target using the fewest selections.
4. Initialize two variables:

`total = 0` for accumulated growth.

`months = 0` for the number of selected months.
5. Iterate through the sorted list.

Add the current month's growth to `total` and increment `months`.
6. After each addition, check whether `total >= k`.

As soon as this becomes true, print `months` and stop. Since we processed months from largest to smallest, this is the minimum possible number of months.
7. If the loop finishes and the target was never reached, print `-1`.

Even using every month was insufficient.

### Why it works

The greedy choice is always safe because larger monthly growth values dominate smaller ones. If a solution uses a smaller value while excluding a larger one, swapping them cannot hurt and may improve the total growth. Repeating this argument transforms any optimal solution into one that consists of the largest available months in descending order.

Because of that property, once we sort the values descendingly, the first prefix whose sum reaches `k` is guaranteed to use the minimum number of months.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input())
    months = list(map(int, input().split()))

    if k == 0:
        print(0)
        return

    months.sort(reverse=True)

    total = 0

    for i in range(12):
        total += months[i]

        if total >= k:
            print(i + 1)
            return

    print(-1)

solve()
```

The first special case checks whether `k` is already zero. This avoids accidentally selecting months when no growth is needed.

The list is sorted in descending order because the greedy strategy depends on always taking the largest remaining growth first.

The loop accumulates growth one month at a time. The answer is `i + 1` because `i` is zero-indexed while the number of selected months starts from one.

The final `-1` is only reached if all 12 months were used and the accumulated growth is still too small.

No extra data structures are needed. The implementation stays short because the greedy logic directly matches the proof.

## Worked Examples

### Sample 1

Input:

```
5
1 1 1 1 2 2 3 2 2 1 1 1
```

After sorting:

```
3 2 2 2 2 1 1 1 1 1 1 1
```

| Step | Selected Growth | Total Growth | Months Used |
| --- | --- | --- | --- |
| 1 | 3 | 3 | 1 |
| 2 | 2 | 5 | 2 |

At step 2, the total growth reaches `5`, so the answer is `2`.

This trace demonstrates the greedy invariant. After selecting the two largest available months, no other pair of months can produce a larger total growth.

### Sample 2

Input:

```
0
1 2 3 4 5 6 7 8 9 10 11 12
```

| Step | Action | Result |
| --- | --- | --- |
| 1 | Check `k == 0` | True |
| 2 | Print answer | 0 |

The algorithm exits immediately without sorting or selecting months.

This example confirms that the special case is necessary. Watering any month would be unnecessary work.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(12 log 12) | Sorting 12 integers dominates the runtime |
| Space | O(1) | Only a few variables are used |

The input size is fixed at 12 months, so the solution runs effectively in constant time. Both the runtime and memory usage are far below the problem limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        k = int(input())
        months = list(map(int, input().split()))

        if k == 0:
            return "0"

        months.sort(reverse=True)

        total = 0

        for i in range(12):
            total += months[i]

            if total >= k:
                return str(i + 1)

        return "-1"

    return solve()

# provided sample
assert run(
    "5\n1 1 1 1 2 2 3 2 2 1 1 1\n"
) == "2", "sample 1"

# k = 0
assert run(
    "0\n0 0 0 0 0 0 0 0 0 0 0 0\n"
) == "0", "no growth needed"

# impossible case
assert run(
    "15\n1 1 1 1 1 1 1 1 1 1 1 1\n"
) == "-1", "total yearly growth insufficient"

# single month enough
assert run(
    "5\n5 0 0 0 0 0 0 0 0 0 0 0\n"
) == "1", "largest month alone works"

# all equal values
assert run(
    "6\n1 1 1 1 1 1 1 1 1 1 1 1\n"
) == "6", "needs exact number of equal months"

# maximum useful boundary
assert run(
    "100\n100 0 0 0 0 0 0 0 0 0 0 0\n"
) == "1", "largest possible single contribution"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `k = 0` | `0` | No months are needed |
| Total sum smaller than `k` | `-1` | Impossible scenario |
| One large month and many zeros | `1` | Greedy picks largest first |
| All values equal | Exact count | Correct accumulation logic |
| Single month with value 100 | `1` | Boundary growth values |

## Edge Cases

Consider the case where no growth is required.

Input:

```
0
3 4 5 6 7 8 9 1 2 3 4 5
```

The algorithm immediately checks `k == 0` and prints `0`. No sorting or accumulation happens. This is correct because Petya already satisfies the requirement without watering at all.

Now consider an impossible case.

Input:

```
20
1 1 1 1 1 1 1 1 1 1 1 1
```

After sorting, the array remains unchanged. The algorithm accumulates values:

```
1, 2, 3, ..., 12
```

Even after all 12 months, the total is only `12`, which is still below `20`. The loop finishes and the algorithm prints `-1`.

Finally, consider many zero-growth months.

Input:

```
5
5 0 0 0 0 0 0 0 0 0 0 0
```

After sorting:

```
5 0 0 0 0 0 0 0 0 0 0 0
```

The first selected month already reaches the target:

```
total = 5
```

The algorithm prints `1`.

This confirms why sorting descendingly matters. Selecting months in arbitrary order could waste choices on zero-growth months before reaching the target.
