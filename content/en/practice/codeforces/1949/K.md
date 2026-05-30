---
title: "CF 1949K - Make Triangle"
description: "We are given a multiset of positive integers and three required group sizes. Every number must belong to exactly one of the three groups, and each group must contain exactly the requested number of elements. After splitting the numbers, we look only at the three group sums."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1949
codeforces_index: "K"
codeforces_contest_name: "European Championship 2024 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2800
weight: 1949
solve_time_s: 149
verified: true
draft: false
---

[CF 1949K - Make Triangle](https://codeforces.com/problemset/problem/1949/K)

**Rating:** 2800  
**Tags:** constructive algorithms, math  
**Solve time:** 2m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of positive integers and three required group sizes. Every number must belong to exactly one of the three groups, and each group must contain exactly the requested number of elements.

After splitting the numbers, we look only at the three group sums. If those sums are $s_a$, $s_b$, and $s_c$, they must form a non-degenerate triangle. Since all values are positive, the triangle condition reduces to a single inequality:

$$\max(s_a,s_b,s_c) < s_a+s_b+s_c-\max(s_a,s_b,s_c)$$

In other words, no side may be at least half of the total perimeter.

The total number of elements across all test cases is at most $200\,000$. That immediately rules out anything exponential, any subset DP, and even $O(n^2)$ per test case. We need something close to $O(n \log n)$, which strongly suggests sorting plus a greedy construction.

The tricky part is that the group sizes are fixed. We are not free to move elements arbitrarily once a group becomes full.

One easy mistake is to think that only the largest element matters.

Consider:

```
n = 6
sizes = (2,2,2)
values = [3,1,1,1,1,1]
```

The total sum is $8$, so every group sum must be strictly smaller than $4$. The largest element is only $3$, which looks harmless.

But every group must contain two numbers. The only possible group containing the $3$ has sum $4$, and the remaining groups have sums $2$ and $2$. The resulting sides are $(4,2,2)$, which is degenerate. The correct answer is `NO`.

Another dangerous case is when a solution exists but the largest numbers cannot simply be packed together.

```
sizes = (1,2,2)
values = [2,2,2,1,1]
```

Putting the two largest numbers into the same group gives sums $(2,4,2)$, which fails.

A valid partition is:

```
2
2 1
2 1
```

with sums $(2,3,3)$.

The algorithm has to reason about future placements, not only the current sums.

## Approaches

A brute-force solution would try all ways to choose the first group, then all ways to choose the second group, and place the remaining numbers into the third group.

For example, if the sizes are $n_a,n_b,n_c$, the number of partitions is

$$\binom{n}{n_a}\binom{n-n_a}{n_b}.$$

Even for $n=40$, this is already astronomically large. With $n$ up to $200\,000$, brute force is completely impossible.

The key observation is that triangle validity depends only on the final group sums.

Let

$$T = \sum x_i.$$

The triangle condition is equivalent to requiring every group sum to be strictly smaller than $T/2$.

Now imagine processing the numbers from largest to smallest.

Suppose a group currently has sum $S$ and still needs $k$ more elements. Even in the most optimistic scenario, those future elements must contribute at least the sum of the $k$ smallest remaining numbers.

That gives a lower bound on the eventual group sum.

If even that lower bound already reaches $T/2$, this group can never become valid.

This transforms the problem into a greedy feasibility check. While assigning the largest remaining number, we only place it into a group whose best possible future still keeps the final sum below $T/2$.

Because there are only three groups, checking all candidate groups for every element is constant work after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Greedy Construction | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Compute the total sum $T$.
2. Sort all numbers in ascending order.
3. Precompute prefix sums of the sorted array.

The prefix sums let us quickly obtain the sum of the smallest $k$ numbers.
4. For each group, store:

- its current sum,
- how many slots are still empty,
- the actual numbers assigned to it.
5. Process the numbers from largest to smallest.
6. Let the current number be $x$.
7. Try each of the three groups.

Suppose a group currently has sum $S$ and still needs $r$ elements including $x$.

After placing $x$, the group will still need $r-1$ more elements.

The smallest possible additional contribution is the sum of the smallest $r-1$ numbers among all numbers that are still unprocessed.

Since we process from largest to smallest, those future numbers are exactly the smaller values. Using the global smallest $r-1$ values gives a lower bound that is always safe.
8. Define

$$\text{best\_possible}
=
S + x + \text{sumSmallest}(r-1).$$

If

$$2 \cdot \text{best\_possible} < T,$$

then even under the most optimistic completion this group can remain a valid triangle side.

1. Place $x$ into the first group satisfying that condition.
2. If no group can accept $x$, output `NO`.
3. If all numbers are assigned successfully, output `YES` and the three groups.

### Why it works

The invariant is:

For every group, there remains at least one way to complete its remaining slots while keeping its final sum strictly below $T/2$.

When we place a number $x$, we only allow assignments that preserve this invariant.

The quantity

$$S + x + \text{sumSmallest}(r-1)$$

is the minimum final sum that group could ever achieve after taking $x$. If even that minimum is already at least $T/2$, then placing $x$ there makes success impossible.

Conversely, if the inequality holds, the group still has room to stay below $T/2$.

Processing numbers from largest to smallest is crucial. Large numbers are the hardest to place. If a large number cannot fit into any group without violating the invariant, then no later smaller number can repair the situation.

When the algorithm finishes, every group still satisfies the invariant with zero remaining slots. The lower bound becomes the exact final sum, so every group sum is strictly below $T/2$. That is exactly the triangle condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n, na, nb, nc = map(int, input().split())
        a = list(map(int, input().split()))

        total = sum(a)

        a.sort()

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]

        groups = [[], [], []]
        sums = [0, 0, 0]
        rem = [na, nb, nc]

        ok = True

        for i in range(n - 1, -1, -1):
            x = a[i]

            placed = False

            for g in range(3):
                if rem[g] == 0:
                    continue

                need_after = rem[g] - 1

                min_final_sum = sums[g] + x + pref[need_after]

                if 2 * min_final_sum < total:
                    groups[g].append(x)
                    sums[g] += x
                    rem[g] -= 1
                    placed = True
                    break

            if not placed:
                ok = False
                break

        if not ok:
            out.append("NO")
            continue

        out.append("YES")
        out.append(" ".join(map(str, groups[0])))
        out.append(" ".join(map(str, groups[1])))
        out.append(" ".join(map(str, groups[2])))

    sys.stdout.write("\n".join(out))

solve()
```

The first step is sorting the values. Every future feasibility check depends on knowing which numbers are still smaller than the current one.

The prefix sum array is the implementation detail that makes the greedy check fast. Instead of repeatedly summing the smallest $k$ values, we obtain that quantity in $O(1)$.

The expression

```
min_final_sum = sums[g] + x + pref[need_after]
```

is the core of the algorithm. It represents the smallest final sum this group could ever have if we place $x$ into it right now.

The strict inequality

```
2 * min_final_sum < total
```

must stay strict. Replacing it with `<=` would allow degenerate triangles where one side equals the sum of the other two.

Another subtle point is that we store the actual values directly in the groups. The statement asks for the numbers, not their indices.

## Worked Examples

### Example 1

Input:

```
6 2 2 2
1 1 1 1 1 1
```

Total sum $T=6$.

| Current x | Group sums before | Remaining slots before | Chosen group |
| --- | --- | --- | --- |
| 1 | (0,0,0) | (2,2,2) | A |
| 1 | (1,0,0) | (1,2,2) | A |
| 1 | (2,0,0) | (0,2,2) | B |
| 1 | (2,1,0) | (0,1,2) | B |
| 1 | (2,2,0) | (0,0,2) | C |
| 1 | (2,2,1) | (0,0,1) | C |

Final sums are $(2,2,2)$.

Every side is smaller than $3=T/2$, so the triangle is valid.

This example shows the simplest balanced case where all groups end with identical sums.

### Example 2

Input:

```
6 2 2 2
1 1 1 1 1 3
```

Total sum $T=8$.

| Current x | Candidate group | Minimum possible final sum |
| --- | --- | --- |
| 3 | Any group | 4 |
| 3 | Check condition | $2 \cdot 4 = 8$ |

The inequality must be strict:

```
2 * 4 < 8
```

which is false.

The first element already cannot be placed anywhere.

The algorithm immediately outputs `NO`.

This trace demonstrates why the sample is impossible. Any group containing the $3$ must eventually reach sum $4$, which equals half of the perimeter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates the runtime |
| Space | $O(n)$ | Stored groups and prefix sums |

The total number of elements across all test cases is at most $200\,000$. Sorting all elements costs roughly $200\,000 \log_2 200\,000$, which easily fits within the time limit. The memory usage is linear and comfortably below the $256$ MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, na, nb, nc = map(int, input().split())
        a = list(map(int, input().split()))

        total = sum(a)

        a.sort()

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]

        groups = [[], [], []]
        sums = [0, 0, 0]
        rem = [na, nb, nc]

        ok = True

        for i in range(n - 1, -1, -1):
            x = a[i]

            placed = False

            for g in range(3):
                if rem[g] == 0:
                    continue

                need_after = rem[g] - 1

                min_final_sum = sums[g] + x + pref[need_after]

                if 2 * min_final_sum < total:
                    groups[g].append(x)
                    sums[g] += x
                    rem[g] -= 1
                    placed = True
                    break

            if not placed:
                ok = False
                break

        if not ok:
            out.append("NO")
        else:
            out.append("YES")

    return "\n".join(out) + "\n"

# provided samples
assert run(
"""4
6 2 2 2
1 1 1 1 1 1
5 3 1 1
1 1 1 1 1
6 2 2 2
1 1 1 1 1 3
8 1 2 5
16 1 1 1 1 1 1 12
"""
) == "YES\nNO\nNO\nYES\n"

# minimum size
assert run(
"""1
3 1 1 1
1 1 1
"""
) == "YES\n"

# all equal values
assert run(
"""1
9 3 3 3
5 5 5 5 5 5 5 5 5
"""
) == "YES\n"

# degenerate boundary
assert run(
"""1
6 2 2 2
1 1 1 1 1 3
"""
) == "NO\n"

# uneven sizes but valid
assert run(
"""1
5 1 2 2
2 2 2 1 1
"""
) == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1 1 1 / 1 1 1` | YES | Smallest legal instance |
| Nine equal values | YES | Symmetric balanced construction |
| `1 1 1 1 1 3` with sizes `(2,2,2)` | NO | Degenerate triangle boundary |
| `2 2 2 1 1` with sizes `(1,2,2)` | YES | Large values must be separated |

## Edge Cases

Consider:

```
6 2 2 2
1 1 1 1 1 3
```

The total sum is $8$. Any group containing the $3$ must also contain one more element because every group size is $2$. Its smallest possible final sum is $4$.

The algorithm computes:

```
min_final_sum = 3 + 1 = 4
```

and checks:

```
2 * 4 < 8
```

which fails.

No group can accept the $3$, so the answer is correctly `NO`.

Now consider:

```
5 1 2 2
2 2 2 1 1
```

The total sum is $8$.

The first $2$ can go into the size-$1$ group because its final sum remains $2$, safely below $4$.

The remaining two $2$ values cannot be merged into the same group, because that would force a future sum of $4$. The feasibility check rejects that placement and distributes them into different groups.

The final sums become:

```
2, 3, 3
```

which satisfy the triangle inequality.

This is exactly the kind of case where a naive greedy based only on current sums fails, while the feasibility-based greedy succeeds.

The solution relies on looking ahead through the minimum possible future contribution, which is why it handles these boundary cases correctly.
