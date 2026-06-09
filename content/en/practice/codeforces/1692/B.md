---
title: "CF 1692B - All Distinct"
description: "We are given an array of integers. In one operation, we must remove exactly two elements from the array. The two removed elements can be any values, as long as they come from different positions."
date: "2026-06-09T23:01:11+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1692
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 799 (Div. 4)"
rating: 800
weight: 1692
solve_time_s: 139
verified: true
draft: false
---

[CF 1692B - All Distinct](https://codeforces.com/problemset/problem/1692/B)

**Rating:** 800  
**Tags:** greedy, sortings  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers. In one operation, we must remove exactly two elements from the array. The two removed elements can be any values, as long as they come from different positions.

Our goal is to perform zero or more such operations so that the remaining array contains only distinct values. Among all ways to achieve that, we want the remaining array to be as long as possible.

For each test case, we must output the maximum possible length of a final array whose elements are all different.

The constraints are very small. Each array contains at most 50 elements, and there are at most 1000 test cases. Even relatively inefficient approaches would fit comfortably within the limits. The challenge is not performance but recognizing the structure of the problem.

The key observation is that duplicates are the only obstacle. If an array contains $k$ distinct values, then any valid final array can contain at most one copy of each value, so its length can never exceed $k$.

The subtle part is the operation itself. We cannot remove a single element. Every removal deletes exactly two elements. That means the number of removed elements must always be even.

Consider the array:

```
1 1 2
```

There are $k=2$ distinct values. Keeping one copy of each value would leave length $2$, which seems ideal. However, reaching length $2$ would require removing exactly one element, and that is impossible because removals happen in pairs. We must remove two elements, leaving length $1$.

The correct answer is therefore:

```
1
```

Another easy-to-miss case is:

```
1 1 2 2
```

There are $k=2$ distinct values and $n-k=2$ duplicate elements. Since the number of duplicates is already even, we can delete exactly those duplicates and keep:

```
1 2
```

The answer is:

```
2
```

A careless solution that only counts distinct values would fail on cases where the number of duplicates is odd.

## Approaches

A brute-force approach would try all possible sequences of pair removals and check which final arrays contain distinct values. Even for small arrays, the number of possible removal sequences grows explosively. Every operation chooses two indices, then the next operation works on a different array state. This quickly becomes infeasible.

To find a better solution, we should think about what the final array must look like.

Suppose the array contains $k$ distinct values. Any valid final array can contain at most one occurrence of each value, so the longest possible distinct array would ideally have length $k$.

To obtain such an array, we would remove exactly:

$$n-k$$

elements.

These are precisely the extra copies beyond the first occurrence of each value.

If $n-k$ is even, then we can remove exactly those duplicates. The remaining array has length $k$, and all elements are distinct.

If $n-k$ is odd, then removing only duplicates is impossible because every operation removes two elements. We must remove one additional element as part of some pair. That reduces the final length by one more, giving length $k-1$.

The entire problem reduces to counting distinct values and checking the parity of the number of duplicates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array.
2. Compute the number of distinct values, denoted by `k`.
3. Compute the number of duplicate elements:

$$d = n - k$$

These are the elements that must be removed if we want to keep one copy of every value.
4. Check whether `d` is even.

If `d` is even, we can remove exactly those duplicates using pair removals, so the answer is `k`.
5. If `d` is odd, one extra element must also disappear because the total number of removed elements must be even.

In that case the answer is `k - 1`.
6. Output the result.

### Why it works

Every valid final array can contain at most one copy of each distinct value, so its length cannot exceed the number of distinct values $k$.

Removing all duplicate copies requires deleting exactly $n-k$ elements. When this number is even, it matches the operation requirement and we can keep all $k$ distinct values.

When $n-k$ is odd, deleting only duplicates would require an odd number of removed elements, which cannot be achieved because every operation removes two elements. At least one additional element must be removed, decreasing the maximum achievable length by one. Thus the best possible length becomes $k-1$.

Since these are the only two possibilities, the algorithm is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    distinct = len(set(a))
    duplicates = n - distinct

    if duplicates % 2 == 0:
        print(distinct)
    else:
        print(distinct - 1)
```

The implementation follows the mathematical observation directly.

The set stores one copy of each value, so `len(set(a))` gives the number of distinct elements. The difference `n - distinct` equals the number of duplicate elements that must be removed to leave only unique values.

The parity of this quantity determines whether we can stop after removing duplicates or whether one extra element must also be removed.

There are no tricky boundary conditions. When all values are distinct, `duplicates = 0`, which is even, so the answer remains `n`. When all values are equal, `distinct = 1`, and the formula still produces the correct result.

## Worked Examples

### Example 1

Input:

```
6
2 2 2 3 3 3
```

| n | distinct (k) | duplicates (d) | d % 2 | answer |
| --- | --- | --- | --- | --- |
| 6 | 2 | 4 | 0 | 2 |

The array contains only the values 2 and 3. We can keep one copy of each and remove the other four elements. Since four is even, pair removals work perfectly and the final length is 2.

### Example 2

Input:

```
5
9 1 9 9 1
```

| n | distinct (k) | duplicates (d) | d % 2 | answer |
| --- | --- | --- | --- | --- |
| 5 | 2 | 3 | 1 | 1 |

There are two distinct values. Keeping one copy of each would require removing three elements, which is impossible because removals occur in pairs. One more element must disappear, so the maximum final length becomes 1.

This example demonstrates the crucial parity observation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Building the set and counting distinct values |
| Space | O(n) | The set may contain all array elements if they are distinct |

With $n \le 50$, this solution is far below the limits. Even across all test cases, the total amount of work is tiny.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        distinct = len(set(a))
        duplicates = n - distinct

        if duplicates % 2 == 0:
            ans.append(str(distinct))
        else:
            ans.append(str(distinct - 1))

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue()

# provided sample
assert run(
"""4
6
2 2 2 3 3 3
5
9 1 9 9 1
4
15 16 16 15
4
10 100 1000 10000
"""
) == "2\n1\n2\n4"

# minimum size
assert run(
"""1
1
7
"""
) == "1"

# all equal values
assert run(
"""1
5
3 3 3 3 3
"""
) == "1"

# odd number of duplicates
assert run(
"""1
3
1 1 2
"""
) == "1"

# even number of duplicates
assert run(
"""1
4
1 1 2 2
"""
) == "2"

# maximum-size style case
assert run(
"""1
50
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
"""
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `1` | Minimum array size |
| `3 3 3 3 3` | `1` | All values equal |
| `1 1 2` | `1` | Odd duplicate count |
| `1 1 2 2` | `2` | Even duplicate count |
| Fifty identical values | `0` | Large duplicate count and parity handling |

## Edge Cases

Consider:

```
1
3
1 1 2
```

We have:

```
distinct = 2
duplicates = 1
```

The duplicate count is odd. Keeping one copy of each value would require removing exactly one element, but operations remove two elements at a time. The algorithm returns:

```
2 - 1 = 1
```

which is correct.

Now consider:

```
1
4
1 1 2 2
```

We have:

```
distinct = 2
duplicates = 2
```

The duplicate count is even. We can delete one extra `1` and one extra `2`, removing exactly two elements. The algorithm returns:

```
2
```

which is optimal.

Finally, consider:

```
1
5
7 7 7 7 7
```

We have:

```
distinct = 1
duplicates = 4
```

Since four is even, we can remove four elements and keep one `7`. The algorithm outputs:

```
1
```

which is the longest possible distinct array.

These examples cover the parity cases that determine the entire solution.
