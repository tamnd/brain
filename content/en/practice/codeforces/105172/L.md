---
title: "CF 105172L - Nanami, Nanami, Nanami..."
description: "We are given several independent test cases. In each test case, there is a list of integers. We are allowed to remove exactly one element from this list."
date: "2026-06-27T08:27:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105172
codeforces_index: "L"
codeforces_contest_name: "The 20th Southeast University Programming Contest (Summer)"
rating: 0
weight: 105172
solve_time_s: 75
verified: true
draft: false
---

[CF 105172L - Nanami, Nanami, Nanami...](https://codeforces.com/problemset/problem/105172/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, there is a list of integers. We are allowed to remove exactly one element from this list. After doing so, we look at the remaining numbers and try to pick a value $d$ that still appears in the list and is strictly smaller than the removed value $c$. Our goal is to choose the removal and the resulting value $d$ so that $d$ is as large as possible.

In simpler terms, we pick one element as a “threshold” $c$, delete one occurrence of it, and then look for the largest number in the remaining array that is still smaller than $c$. We want to maximize that best possible $d$ over all choices of $c$.

The constraints are small: each array has at most 100 elements and values are at most 100. This immediately suggests that even cubic or quadratic solutions would be acceptable, but we should still aim for a structure that makes the logic transparent rather than simulating every removal explicitly.

A subtle point is that removing an element only affects the availability of that exact value. If we pick $d \neq c$, then removing $c$ never removes all occurrences of $d$. This means most of the “remove and recompute” idea is unnecessary overhead.

Edge cases worth thinking about come from arrays where the maximum value appears multiple times, or where there are many duplicates:

If all values are equal, such as `3 3`, there is no valid pair $d < c$, because no matter what you remove, there is no strictly smaller value. The problem guarantees this situation will not happen in a degenerate way, since it ensures at least two distinct values exist.

If the array is `1 2 2`, removing one `2` still leaves `1 2`, and the best $d$ is still `1`. A naive simulation might incorrectly think removing the only maximum changes the answer, but it does not.

## Approaches

The brute-force idea is straightforward. For every index $i$, treat $a[i]$ as the removed value $c$. After removing it, scan the remaining array and check every value $a[j]$ that is smaller than $c$, taking the maximum among them. This requires $O(n)$ work per removal, and since there are $O(n)$ choices, the total complexity is $O(n^2)$ per test case. With $n \le 100$, this is already safe.

However, this approach recomputes the same structure repeatedly. The key observation is that the removal operation is almost irrelevant: removing one occurrence of a value does not change whether another value exists in the array. So the only question that matters is whether there exists any value strictly greater than $d$. If such a value exists, we can always choose it as $c$, and removing one occurrence of it will not affect $d$.

So the problem reduces to finding the largest value $d$ such that there exists at least one strictly larger value in the array. That is exactly the second largest distinct value in the set of numbers.

We can therefore ignore multiplicities entirely and just work with unique values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Accepted |
| Optimal (distinct scan) | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the array and extract all distinct values.

This removes duplicates because duplicates do not change ordering between values, only frequency.
2. Sort the distinct values in descending order.

Sorting gives us a clean ranking from largest to smallest, which directly encodes the condition $d < c$.
3. Take the second element in this sorted distinct list.

This value is the largest number that still has at least one strictly greater value above it.
4. Output this value for the test case.

The reasoning behind step 3 is the core of the solution. Any candidate $d$ must have some $c > d$. That immediately means $d$ cannot be the maximum distinct value. Among all remaining candidates, the best possible choice is the largest one still below the maximum, which is the second largest distinct value.

### Why it works

Let $M$ be the maximum value in the array. Any valid $d$ must satisfy $d < M$, because if $d = M$, there is no strictly larger value to serve as $c$. For any value $d < M$, we can always choose $c = M$ (or any occurrence of $M$) and remove it. Since removing one element does not eliminate all occurrences of $d$, $d$ remains in the array. Therefore every value except the maximum is feasible, and we maximize by picking the largest among them, which is the second largest distinct value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        vals = sorted(set(a), reverse=True)
        print(vals[1])

if __name__ == "__main__":
    solve()
```

The solution reads each test case independently, converts the array into a set to remove duplicates, sorts it in descending order, and outputs the second element. The only subtle requirement is ensuring that the array has at least two distinct values, which is guaranteed by the problem statement.

## Worked Examples

We trace two cases to see how the transformation to “second maximum distinct value” emerges.

### Example 1

Input: `1 4 2`

Distinct values: `[4, 2, 1]`

| Step | Distinct Set | Sorted Desc | Chosen Value |
| --- | --- | --- | --- |
| Start | {1, 2, 4} | - | - |
| Sort | - | [4, 2, 1] | - |
| Output | - | - | 2 |

Here, `4` is the only value that cannot serve as $d$, so the best possible valid value is `2`.

### Example 2

Input: `5 2 1 1 3 1 4`

Distinct values: `[5, 4, 3, 2, 1]`

| Step | Distinct Set | Sorted Desc | Chosen Value |
| --- | --- | --- | --- |
| Start | {1, 2, 3, 4, 5} | - | - |
| Sort | - | [5, 4, 3, 2, 1] | - |
| Output | - | - | 4 |

The value `5` is unusable as $d$, and `4` becomes the largest value that still has a strictly greater element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ per test case | Sorting the distinct elements dominates the work |
| Space | $O(n)$ | Storage for the distinct set |

Given $n \le 100$ and $t \le 100$, this runs comfortably within limits even with repeated sorting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        vals = sorted(set(a), reverse=True)
        out.append(str(vals[1]))
    return "\n".join(out)

# provided samples
assert run("""5
2
1 2
3
1 2 3
3
1 4 2
5
1 2 9 4 3
7
5 2 1 1 3 1 4
""") == """1
2
2
4
4"""

# minimum size with two distinct values
assert run("""1
2
1 100
""") == "1"

# duplicates everywhere except one max
assert run("""1
5
7 7 7 7 1
""") == "1"

# already sorted descending
assert run("""1
4
10 9 8 7
""") == "9"

# mixed duplicates
assert run("""1
6
2 2 3 3 3 1
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 100 / 1 100` | `1` | simplest two-element case |
| all 7s + 1 | `1` | duplicates do not affect result |
| `10 9 8 7` | `9` | already ordered input |
| mixed duplicates | `2` | handling repeated values |

## Edge Cases

When the maximum value appears many times, removing one occurrence still leaves it present in the array. This means it is always valid to choose the maximum as $c$, ensuring that every smaller distinct value remains reachable as a candidate $d$. The algorithm handles this naturally because duplicates are removed before sorting, so frequency never affects ordering.

When values are tightly packed, such as consecutive integers, the second largest distinct value is still well-defined. For example, in `[1, 2]`, the answer is `1`, and removing either element does not change the fact that only one value can serve as a valid $d$.

When there are multiple duplicates of intermediate values, such as `[1, 2, 2, 3]`, the presence of extra `2`s does not change the ordering of distinct values, and the algorithm still correctly returns `2`.
