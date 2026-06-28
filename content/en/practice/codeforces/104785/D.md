---
title: "CF 104785D - Delivery Forces"
description: "We are given a company with $n$ couriers, where $n$ is guaranteed to be divisible by three. Each courier has a strength value, and we must partition all couriers into exactly $k = n/3$ groups, each group containing exactly three people."
date: "2026-06-28T14:38:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104785
codeforces_index: "D"
codeforces_contest_name: "2023 United Kingdom and Ireland Programming Contest (UKIEPC 2023)"
rating: 0
weight: 104785
solve_time_s: 53
verified: true
draft: false
---

[CF 104785D - Delivery Forces](https://codeforces.com/problemset/problem/104785/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a company with $n$ couriers, where $n$ is guaranteed to be divisible by three. Each courier has a strength value, and we must partition all couriers into exactly $k = n/3$ groups, each group containing exactly three people.

For each group, its effectiveness is defined not by the maximum or minimum strength inside it, but by the median strength, meaning the second largest value among the three. The goal is to assign couriers into triples so that the sum of all group medians is as large as possible.

So the task is not about balancing teams or making them equal, but about carefully deciding which values become the “middle” contributors of each triple.

The constraints go up to $n \le 10^6$, which immediately forces a linearithmic or linear solution after sorting. Any approach that tries to enumerate or simulate group formation directly will be too slow because even a single combinatorial construction over triples would explode to $O(n^3)$ or worse. Sorting at $O(n \log n)$ is acceptable, and anything beyond a few passes over the array must be linear.

A common subtle failure case comes from greedily grouping local triples without global ordering. For example, with values like:

Input:

```
6
1 2 3 100 101 102
```

A naive grouping might form `(100, 101, 102)` and `(1, 2, 3)`, giving medians `101 + 2 = 103`. That looks plausible, but it is not optimal grouping logic in general, and such greedy local decisions fail when values are interleaved in more adversarial distributions.

The real difficulty is that each element participates in exactly one triple, so choosing who becomes a median globally interacts with all other choices. We need a structure that guarantees that the selected “middle” elements are as large as possible while still being valid medians inside triples.

## Approaches

The brute-force idea is straightforward: try all possible ways to partition the array into triples, compute the median of each triple, and take the maximum sum. This is correct in principle because it checks every valid configuration. However, the number of ways to partition $n$ elements into groups of three is astronomically large, growing faster than exponential. Even for $n = 30$, this becomes infeasible, and at $n = 10^6$, it is completely impossible.

The key observation is that we do not actually need to construct triples explicitly. We only care about the middle element of each triple. If we sort the array, the structure of optimal grouping becomes constrained: large values should act as “support” elements for medians, small values should be sacrificed as the low ends of triples, and the remaining elements naturally become medians.

After sorting, imagine walking inward from both ends of the array. Each triple needs one large helper element and one small filler element around a chosen median. This means that for every median we select, we can “spend” one large element and one small element to complete its group. Since we want medians to be as large as possible, we avoid wasting large values as medians’ companions too early.

This leads to a clean greedy structure: sort the array and ignore the smallest third as forced fillers, and the largest third as forced supporters. The remaining middle third contains the best possible candidates for medians, but not all of them are used directly. Instead, the correct medians appear at regular intervals in the sorted order.

Concretely, after sorting in ascending order, the optimal solution picks elements starting from index $k$, then skips one, takes one, and repeats. This works because the first $k$ smallest elements are best used as the “low sides” of triples, while the largest $k$ elements serve as the “high sides”, leaving exactly $k$ elements in positions where they can be maximized as medians.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal (sorting + greedy selection) | $O(n \log n)$ | O(n) | Accepted |

## Algorithm Walkthrough

We first sort the array so that we can reason about structure instead of individual assignments. Sorting transforms the problem from combinatorial grouping into positional selection.

After sorting in ascending order, we treat the array as three conceptual segments: the smallest elements, the largest elements, and the middle region where medians are drawn from. Since each group consumes exactly one small and one large helper, we reserve the smallest $k$ elements as low partners and the largest $k$ elements as high partners.

What remains in the middle region is $k$ elements that will contribute to the answer. However, we do not take them consecutively; instead, we pick every second element starting from index $k$, because between consecutive medians we must account for the allocation of helper elements in valid triples.

1. Sort the array in ascending order.
2. Let $k = n/3$.
3. Initialize a variable `answer = 0`.
4. Starting from index $k$, iterate over the array and pick every second element until $k$ elements are chosen.
5. Add each selected element to `answer`.
6. Output `answer`.

The reason for skipping every other element is that each chosen median implicitly reserves space for one smaller and one larger element in its triple formation, and the sorted structure ensures that these roles can always be filled without interfering with other chosen medians.

### Why it works

Once the array is sorted, any valid grouping can be rearranged so that smaller elements never appear as medians unless necessary. Each median must have at least one element smaller than it and one larger than it. By reserving the smallest $k$ elements as guaranteed small companions and the largest $k$ as guaranteed large companions, we isolate exactly $k$ positions where medians can be taken.

The alternating selection guarantees that no two medians compete for the same helper elements, because between every two chosen medians there is a structural separation that corresponds to consumed support elements. This ensures feasibility while maximizing the sum because we always choose the largest available candidates from the allowable median region.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    a.sort()
    k = n // 3
    
    ans = 0
    
    # pick medians: indices k, k+2, ..., k+2*(k-1)
    for i in range(k):
        idx = k + 2 * i
        ans += a[idx]
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution starts by sorting the array, which is essential because all structural reasoning depends on relative order. The variable $k$ represents how many triples we will form, so we expect exactly $k$ medians to contribute to the final sum.

The loop carefully selects indices starting at $k$ and jumping by two each time. The starting offset $k$ avoids the smallest elements, which are reserved as mandatory low companions in each triple. The step of two ensures that each selected median is separated by one element that serves as structural spacing for valid grouping.

## Worked Examples

### Example 1

Input:

```
6
1 2 3 4 5 6
```

Sorted array is `[1, 2, 3, 4, 5, 6]`, and $k = 2$.

| Step | Chosen index | Value | Running sum |
| --- | --- | --- | --- |
| 1 | 2 | 3 | 3 |
| 2 | 4 | 5 | 8 |

The selected medians are 3 and 5, giving total 8.

This shows how the smallest two elements (1, 2) and largest two elements (5, 6) are effectively used as structural supports, leaving the correct middle choices for medians.

### Example 2

Input:

```
9
9 1 8 2 7 3 6 4 5
```

Sorted array is `[1,2,3,4,5,6,7,8,9]`, $k = 3$.

| Step | Chosen index | Value | Running sum |
| --- | --- | --- | --- |
| 1 | 3 | 4 | 4 |
| 2 | 5 | 6 | 10 |
| 3 | 7 | 8 | 18 |

The medians are 4, 6, and 8.

This confirms that even in a fully interleaved permutation, sorting fully restores structure and the greedy index selection remains stable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; single linear scan afterwards |
| Space | $O(n)$ | Array storage and sorting overhead |

The constraints allow up to one million elements, so a single sort followed by a linear pass is comfortably within limits. No additional data structures are required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    backup = _sys.stdout
    _sys.stdout = io.StringIO()
    solve()
    out = _sys.stdout.getvalue()
    _sys.stdout = backup
    return out.strip()

# provided-style small case
assert run("6\n1 2 3 4 5 6\n") == "8"

# all equal
assert run("6\n5 5 5 5 5 5\n") == "10"

# already sorted descending
assert run("6\n6 5 4 3 2 1\n") == "8"

# minimal n = 3
assert run("3\n1 100 50\n") == "50"

# larger structured case
assert run("9\n9 8 7 6 5 4 3 2 1\n") == "18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | consistent sum | stability under symmetry |
| descending input | correct handling of order | sorting necessity |
| minimal case | single triple correctness | base case correctness |
| structured 9 elements | multi-group correctness | general pattern validity |

## Edge Cases

One edge case is when all values are identical. For input:

```
6
5 5 5 5 5 5
```

sorting does not change the array, and $k = 2$. The algorithm selects indices 2 and 4, both equal to 5, giving result 10. Any grouping yields the same result, and the algorithm remains consistent because every element is interchangeable, so the median selection pattern does not matter.

Another edge case is the smallest valid input:

```
3
1 2 3
```

Here $k = 1$, and after sorting we pick index 1 (0-based), which is value 2. This is exactly the median of the only possible triple, confirming that the indexing logic aligns with the definition even at boundary size.
