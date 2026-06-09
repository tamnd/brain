---
title: "CF 1896C - Matching Arrays"
description: "We have two arrays of equal length. Array a is fixed, while array b may be rearranged arbitrarily. After choosing a permutation of b, we compare the arrays position by position. The beauty of the resulting pair of arrays is the number of indices where a[i] b[i]."
date: "2026-06-08T21:37:56+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1896
codeforces_index: "C"
codeforces_contest_name: "CodeTON Round 7 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1400
weight: 1896
solve_time_s: 158
verified: false
draft: false
---

[CF 1896C - Matching Arrays](https://codeforces.com/problemset/problem/1896/C)

**Rating:** 1400  
**Tags:** binary search, constructive algorithms, greedy, sortings  
**Solve time:** 2m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We have two arrays of equal length. Array `a` is fixed, while array `b` may be rearranged arbitrarily. After choosing a permutation of `b`, we compare the arrays position by position.

The beauty of the resulting pair of arrays is the number of indices where `a[i] > b[i]`.

For each test case, we are given a target value `x`. The task is to determine whether there exists a permutation of `b` whose beauty is exactly `x`. If such a permutation exists, we must output one valid arrangement.

The total size of all test cases is at most `2 · 10^5`. That immediately rules out anything that examines many permutations. Even an `O(n²)` algorithm would perform around `4 · 10^10` operations in the worst case, which is far beyond the limit. Since sorting `2 · 10^5` numbers is easily affordable, a solution around `O(n log n)` per test file is the natural target.

The tricky part is that we are not maximizing or minimizing the beauty. We need an arrangement producing exactly a given number of winning positions.

One easy mistake is to greedily assign small values of `b` wherever possible and stop once `x` wins have been created.

Consider:

```
n = 3, x = 1
a = [2, 4, 3]
b = [4, 1, 2]
```

A careless greedy may place `1` against `4`, creating one win, and then assign the remaining values arbitrarily. It could accidentally create a second win. The correct answer exists:

```
b = [2, 4, 1]
```

which produces exactly one winning position.

Another subtle case occurs when the requested beauty is impossible.

```
n = 1, x = 1
a = [1]
b = [2]
```

No rearrangement exists. Since `1 > 2` is false, the beauty is always zero.

A third source of bugs comes from equal values.

```
n = 3, x = 0
a = [2, 2, 2]
b = [2, 2, 2]
```

Beauty counts only strict inequalities. Equal values do not contribute. Any logic that treats `>=` as a win will produce the wrong answer.

## Approaches

The brute-force approach is straightforward. Generate every permutation of `b`, compute the beauty of each arrangement, and check whether any beauty equals `x`.

The beauty computation takes `O(n)` time. There are `n!` permutations. Even for `n = 10`, this is already about `3.6 million` permutations. For `n = 20`, it becomes completely infeasible. Since the actual limit is `2 · 10^5`, brute force is useful only for understanding the structure of the problem.

The key observation is that only the relative ordering of values matters. Suppose we sort the positions of `a` by value. If we want exactly `x` positions where `a[i] > b[i]`, then the smallest `x` values of `b` should be used to create those wins, because small values are easiest to beat.

Let us sort the indices of `a` by increasing `a[i]`. Let those indices be:

```
p[0], p[1], ..., p[n-1]
```

Also sort the values of `b`.

To create exactly `x` wins, assign the smallest `x` elements of sorted `b` to the largest `x` elements of `a`.

Why? Those largest elements of `a` are the easiest places to guarantee `a[i] > b[i]`.

After that assignment, the remaining `n - x` values of `b` are assigned to the remaining positions of `a`.

A very elegant construction appears. If sorted `b` is:

```
b0 ≤ b1 ≤ ... ≤ b(n-1)
```

then after sorting positions of `a`, we place:

```
b0 ... b(x-1)
```

onto the largest `x` positions of `a`, and

```
bx ... b(n-1)
```

onto the smallest `n-x` positions.

This is equivalent to rotating the sorted `b` array by `x` positions relative to sorted `a`.

The resulting arrangement either gives exactly `x` wins or proves that no solution exists. We simply count the actual beauty afterward. If the count equals `x`, we output the arrangement. Otherwise, no valid arrangement exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · n!) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the indices of `a` by increasing value.
2. Sort all values of `b`.
3. Create an answer array of length `n`.
4. For the smallest `n - x` positions in sorted order of `a`, assign the largest `n - x` values of sorted `b`.

More precisely, for `i = 0 ... n-x-1`:

```
ans[pos[i]] = sorted_b[x + i]
```

These positions should avoid creating wins whenever possible.
5. For the largest `x` positions in sorted order of `a`, assign the smallest `x` values of sorted `b`.

For `i = 0 ... x-1`:

```
ans[pos[n-x+i]] = sorted_b[i]
```

These are the positions intended to become wins.
6. Compute the beauty of the constructed arrangement.
7. If the beauty equals `x`, print `"YES"` and the arrangement.
8. Otherwise print `"NO"`.

### Why it works

After sorting both arrays, the construction pairs the smallest `x` elements of `b` with the largest elements of `a`. If any arrangement can create `x` winning positions, those are the most favorable positions for the wins.

The remaining larger elements of `b` are matched against the smaller elements of `a`, minimizing the chance of creating additional wins.

This arrangement is the standard cyclic-shift construction used in the official solution. If the desired beauty is achievable, the construction realizes it. If the beauty produced by the construction is not exactly `x`, then the required number of wins cannot be obtained by any permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        pos = sorted(range(n), key=lambda i: a[i])
        b.sort()

        ans = [0] * n

        for i in range(n - x):
            ans[pos[i]] = b[x + i]

        for i in range(x):
            ans[pos[n - x + i]] = b[i]

        beauty = sum(a[i] > ans[i] for i in range(n))

        if beauty == x:
            print("YES")
            print(*ans)
        else:
            print("NO")

solve()
```

The first step sorts the indices of `a` instead of sorting `a` itself. We eventually need to output the permutation in the original order, so keeping track of positions is essential.

The two assignment loops implement the cyclic shift. The first loop fills the smaller elements of `a` with the larger portion of sorted `b`. The second loop places the smallest values of `b` onto the largest values of `a`.

After constructing the candidate arrangement, the code performs a direct verification. This final check is important because the presence of equal values can prevent some intended winning positions from actually satisfying `a[i] > b[i]`.

The verification step is only `O(n)`, so it does not affect the overall complexity.

## Worked Examples

### Example 1

Input:

```
n = 3, x = 1
a = [2, 4, 3]
b = [4, 1, 2]
```

Sorted information:

```
pos = [0, 2, 1]
sorted_b = [1, 2, 4]
```

| Step | Position Used | Value Assigned | ans |
| --- | --- | --- | --- |
| Initial | - | - | [0,0,0] |
| i=0 in first loop | pos[0]=0 | 2 | [2,0,0] |
| i=1 in first loop | pos[1]=2 | 4 | [2,0,4] |
| i=0 in second loop | pos[2]=1 | 1 | [2,1,4] |

Beauty calculation:

| Index | a[i] | ans[i] | a[i] > ans[i] |
| --- | --- | --- | --- |
| 0 | 2 | 2 | No |
| 1 | 4 | 1 | Yes |
| 2 | 3 | 4 | No |

Beauty equals `1`, so the answer is accepted.

This example shows how the smallest value of `b` is deliberately placed against the largest value of `a` to create exactly one winning position.

### Example 2

Input:

```
n = 3, x = 3
a = [2, 4, 3]
b = [4, 1, 2]
```

Sorted information:

```
pos = [0, 2, 1]
sorted_b = [1, 2, 4]
```

| Step | Position Used | Value Assigned | ans |
| --- | --- | --- | --- |
| i=0 second loop | pos[0]=0 | 1 | [1,0,0] |
| i=1 second loop | pos[1]=2 | 2 | [1,0,2] |
| i=2 second loop | pos[2]=1 | 4 | [1,4,2] |

Beauty calculation:

| Index | a[i] | ans[i] | a[i] > ans[i] |
| --- | --- | --- | --- |
| 0 | 2 | 1 | Yes |
| 1 | 4 | 4 | No |
| 2 | 3 | 2 | Yes |

Beauty is only `2`.

Since the constructed arrangement fails to achieve `3`, the correct output is `"NO"`.

This example illustrates the effect of equal values. Even though we try to create three wins, the value `4` cannot be beaten by another `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the work |
| Space | O(n) | Arrays for indices and answer |

The total size of all test cases is at most `2 · 10^5`. Sorting each test case gives a total complexity of `O(N log N)` across the entire input, which comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    out = []

    t = int(input())

    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        pos = sorted(range(n), key=lambda i: a[i])
        b.sort()

        ans = [0] * n

        for i in range(n - x):
            ans[pos[i]] = b[x + i]

        for i in range(x):
            ans[pos[n - x + i]] = b[i]

        beauty = sum(a[i] > ans[i] for i in range(n))

        if beauty == x:
            out.append("YES")
            out.append(" ".join(map(str, ans)))
        else:
            out.append("NO")

    return "\n".join(out)

# minimum size, beauty 0
assert run(
"""1
1 0
1
2
"""
) == "YES\n2"

# minimum size, impossible beauty 1
assert run(
"""1
1 1
1
2
"""
) == "NO"

# all values equal
assert run(
"""1
3 0
2 2 2
2 2 2
"""
) == "YES\n2 2 2"

# boundary x = n, impossible because of equality
assert run(
"""1
3 3
2 4 3
4 1 2
"""
) == "NO"

# off-by-one style case
assert run(
"""1
3 2
2 4 3
4 1 2
"""
).startswith("YES")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, x=0` | YES | Smallest valid instance |
| `n=1, x=1` | NO | Impossible target beauty |
| All values equal | YES | Strict inequality handling |
| `x=n` example | NO | Equality prevents full beauty |
| `n=3, x=2` | YES | Rotation boundaries are correct |

## Edge Cases

Consider:

```
1
1 1
1
2
```

Sorted arrays remain unchanged. The construction produces:

```
ans = [2]
```

Beauty is:

```
1 > 2 = false
```

The beauty is `0`, not `1`, so the algorithm prints `"NO"`.

Now consider equal values:

```
1
3 0
2 2 2
2 2 2
```

After sorting, every assignment still places `2` against `2`.

Beauty becomes:

```
0
```

because equality does not count as a win. The verification step correctly accepts the arrangement.

Finally consider:

```
1
3 3
2 4 3
4 1 2
```

The construction places the smallest values of `b` against the largest values of `a`, attempting to create three wins. The resulting arrangement contains one position with:

```
4 vs 4
```

which is not a win. Beauty becomes `2`. The final verification detects the mismatch and outputs `"NO"`.

These examples show why the verification step is necessary. The construction identifies the only candidate arrangement that could realize the target beauty, and the final count confirms whether it actually does.
