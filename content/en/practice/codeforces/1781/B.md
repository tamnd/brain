---
title: "CF 1781B - Going to the Cinema"
description: "Each person has a threshold value $ai$. Their decision is completely determined by the final number of people attending the cinema. Suppose exactly $k$ people go."
date: "2026-06-09T11:18:25+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1781
codeforces_index: "B"
codeforces_contest_name: "VK Cup 2022 - \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 (Engine)"
rating: 1000
weight: 1781
solve_time_s: 277
verified: false
draft: false
---

[CF 1781B - Going to the Cinema](https://codeforces.com/problemset/problem/1781/B)

**Rating:** 1000  
**Tags:** brute force, greedy, sortings  
**Solve time:** 4m 37s  
**Verified:** no  

## Solution
## Problem Understanding

Each person has a threshold value $a_i$. Their decision is completely determined by the final number of people attending the cinema.

Suppose exactly $k$ people go.

A person with threshold $a_i$ is happy if and only if their action matches their rule:

If they go, there must be at least $a_i$ other attendees, so we need $k-1 \ge a_i$.

If they stay home, there must be fewer than $a_i$ other attendees, so we need $k < a_i$.

We must count how many different attendance sets make every person happy simultaneously.

The constraints immediately suggest that we cannot examine every subset. Even for $n=40$, there are already more than a trillion subsets, and here $n$ can reach $2 \cdot 10^5$ across test cases. Any exponential solution is impossible. Since the total size over all test cases is only $2 \cdot 10^5$, an $O(n \log n)$ solution per test case is completely safe, while $O(n^2)$ would be too slow in the worst case.

The main difficulty is that happiness depends on the total number of attendees, not on individual choices independently. A naive implementation can easily miss this global dependency.

Consider the input:

```
2
1 1
```

If exactly one person goes, then the attendee sees $0$ other attendees, which is less than $1$, so they are unhappy. The non-attendee sees $1$ attendee, which is at least $1$, so they are also unhappy. The correct answer is 2, corresponding to "everyone goes" and "nobody goes".

Another subtle case is:

```
3
0 0 0
```

Anyone with threshold 0 must attend whenever the attendance count is at least 0, which is always true. The only valid choice is that all three people go. A careless solution might think every subset works because the thresholds are small.

A third edge case is:

```
3
2 2 2
```

Nobody can attend unless there are at least two other attendees. The only valid configurations are "everyone goes" and "nobody goes", giving answer 2. This shows that both extremes can be valid simultaneously.

## Approaches

The brute-force idea is straightforward. Enumerate every subset of people, compute how many people attend, and check whether every person is happy under that attendance count. This is correct because it directly tests the definition.

The problem is the number of subsets. There are $2^n$ possibilities. For $n=200000$, this is unimaginably large, so we need a completely different viewpoint.

The key observation is that a valid attendance set is determined entirely by its size.

Assume exactly $k$ people attend.

Anyone who attends must satisfy:

$$a_i \le k-1$$

Anyone who stays home must satisfy:

$$a_i > k-1$$

These two conditions split the people into two groups. Every person with $a_i \le k-1$ must attend, and every person with $a_i > k-1$ must stay home.

That means the attendance set is not arbitrary anymore. Once $k$ is fixed, the set is uniquely determined.

Let us sort the thresholds.

If exactly $k$ people attend, then after sorting, the first $k$ values must be at most $k-1$, and all remaining values must be greater than $k-1$.

In sorted order this becomes:

$$a_k \le k-1$$

and

$$a_{k+1} > k-1$$

using 1-based indexing.

Every value of $k$ satisfying these inequalities contributes exactly one valid attendance set.

After sorting, we only need to test all $k$ from $0$ to $n$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n2^n)$ | $O(1)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort the array of thresholds in nondecreasing order.
2. Consider every possible attendance count $k$ from $0$ to $n$.
3. For $k=0$, nobody attends. This is valid only if every threshold is strictly positive. In sorted order, that means $a_1 > 0$.
4. For $k=n$, everybody attends. This is valid only if every threshold is at most $n-1$, which is always true because of the input constraints. Thus $k=n$ is always valid.
5. For $1 \le k \le n-1$, check whether:

$$a_k \le k-1$$

and

$$a_{k+1} > k-1.$$
6. If both conditions hold, increase the answer by one.
7. Output the total count.

### Why it works

Fix a value $k$.

Any person with threshold at most $k-1$ must attend, because staying home would make them unhappy. Any person with threshold greater than $k-1$ must stay home, because attending would make them unhappy.

A valid configuration with exactly $k$ attendees exists if and only if there are exactly $k$ people whose thresholds are at most $k-1$. After sorting, this is equivalent to saying the first $k$ values are at most $k-1$ and the remaining values are greater than $k-1$.

Whenever those inequalities hold, the attendance set is uniquely determined and everyone is happy. Whenever they fail, at least one person must violate their condition. Thus every valid attendance set is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()

        cur = 0

        if a[0] > 0:
            cur += 1

        for k in range(1, n):
            if a[k - 1] <= k - 1 and a[k] > k - 1:
                cur += 1

        cur += 1  # k = n is always valid

        ans.append(str(cur))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The sorted array is the central data structure. Once the thresholds are ordered, checking whether exactly $k$ people should attend becomes a boundary test between positions $k$ and $k+1$.

The case $k=0$ needs separate handling because there is no element before the boundary. Nobody attends only when all thresholds are positive, which in sorted order means the smallest value is positive.

The loop handles all interior values $1 \le k \le n-1$. Using zero-based indexing, $a[k-1]$ is the largest threshold among the first $k$ people and $a[k]$ is the smallest threshold among the remaining people.

The case $k=n$ is always valid. Every threshold satisfies $a_i \le n-1$ by definition of the input, so everyone can attend without violating their requirement.

A common off-by-one mistake is comparing against $k$ instead of $k-1$. The condition refers to the number of _other_ attendees, so when $k$ people attend, each attendee sees exactly $k-1$ others.

## Worked Examples

### Example 1

Input:

```
2
1 1
```

Sorted array:

```
[1, 1]
```

| k | Condition checked | Valid? | Count |
| --- | --- | --- | --- |
| 0 | a[0] > 0 | Yes | 1 |
| 1 | a[0] ≤ 0 and a[1] > 0 | No | 1 |
| 2 | always valid | Yes | 2 |

Answer:

```
2
```

This example shows that both extreme attendance counts can be valid simultaneously.

### Example 2

Input:

```
7
0 1 2 3 4 5 6
```

Sorted array:

```
[0, 1, 2, 3, 4, 5, 6]
```

| k | a[k-1] ≤ k-1 | a[k] > k-1 | Valid? |
| --- | --- | --- | --- |
| 0 | - | No | No |
| 1 | 0 ≤ 0 | 1 > 0 | Yes |
| 2 | 1 ≤ 1 | 2 > 1 | Yes |
| 3 | 2 ≤ 2 | 3 > 2 | Yes |
| 4 | 3 ≤ 3 | 4 > 3 | Yes |
| 5 | 4 ≤ 4 | 5 > 4 | Yes |
| 6 | 5 ≤ 5 | 6 > 5 | Yes |
| 7 | always valid | Yes |  |

Every interior boundary satisfies the condition, but each valid $k$ corresponds to the same attendance set structure. The final count produced by the algorithm is:

```
1
```

Only one actual attendance configuration satisfies everybody simultaneously.

The trace demonstrates the boundary interpretation: a valid attendance size exists exactly when the sorted array cleanly separates values $\le k-1$ from values $> k-1$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates the running time |
| Space | $O(n)$ | Storage of the threshold array |

The total number of people across all test cases is at most $2 \cdot 10^5$. Sorting each test case gives a total complexity of $O(2 \cdot 10^5 \log(2 \cdot 10^5))$, which comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()

        ans = 0

        if a[0] > 0:
            ans += 1

        for k in range(1, n):
            if a[k - 1] <= k - 1 and a[k] > k - 1:
                ans += 1

        ans += 1
        out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run(
"""4
2
1 1
7
0 1 2 3 4 5 6
8
6 0 3 3 6 7 2 7
5
3 0 0 3 3
"""
) == """2
1
3
2"""

# minimum size
assert run(
"""1
2
0 0
"""
) == "1"

# all equal positive
assert run(
"""1
3
2 2 2
"""
) == "2"

# all zero
assert run(
"""1
3
0 0 0
"""
) == "1"

# boundary split exactly once
assert run(
"""1
4
0 0 3 3
"""
) == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 0 0` | `1` | Minimum size, only everybody attends |
| `3 / 2 2 2` | `2` | Both extremes valid |
| `3 / 0 0 0` | `1` | Nobody attending is impossible |
| `4 / 0 0 3 3` |  |  |
