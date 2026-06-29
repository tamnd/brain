---
title: "CF 104636A - Oath of the Night's Watch"
description: "We are given a list of steward strengths, and we need to decide which stewards Jon Snow will support. A steward is supported only if there exists at least one steward with strictly smaller strength and at least one steward with strictly larger strength."
date: "2026-06-29T17:04:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104636
codeforces_index: "A"
codeforces_contest_name: "\u041c\u0438\u0441\u0438\u0441 2023 \u043e\u0441\u0435\u043d\u044c - \u043c\u0430\u0441\u0441\u0438\u0432\u044b, \u0441\u0442\u0440\u043e\u043a\u0438"
rating: 0
weight: 104636
solve_time_s: 71
verified: false
draft: false
---

[CF 104636A - Oath of the Night's Watch](https://codeforces.com/problemset/problem/104636/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of steward strengths, and we need to decide which stewards Jon Snow will support. A steward is supported only if there exists at least one steward with strictly smaller strength and at least one steward with strictly larger strength.

This condition is applied independently for each position in the array. We are not selecting a subset or modifying values, we are simply checking, for each element, whether it is “sandwiched” between a smaller and a larger value somewhere in the full collection.

The input size can reach 100,000 elements, and each value can be as large as 10^9. This immediately rules out any solution that compares each element against all others. A quadratic approach would perform on the order of 10^10 comparisons in the worst case, which is far beyond what fits in a two second limit.

A subtle edge case appears when all values are identical. In that situation, no element has both a strictly smaller and a strictly larger neighbor. Even though there are many elements, none satisfy the condition. Another corner case is when only two distinct values exist. Then only the larger value has a smaller neighbor, and only the smaller value has a larger neighbor, but no element can satisfy both simultaneously.

## Approaches

A direct way to check the condition for each steward is to scan the entire array and search for a smaller value and a larger value. For each index, we would run two scans: one to detect whether any value is smaller, and another to detect whether any value is larger. This works correctly because it explicitly verifies the condition in the definition.

However, this leads to a total of O(n^2) checks. With n up to 100,000, this becomes roughly 10^10 comparisons, which is too slow.

The key observation is that the condition for a value depends only on global extremes in the array. A value can only have a strictly smaller element if it is greater than the global minimum. Similarly, it can only have a strictly larger element if it is smaller than the global maximum. This reduces the problem to identifying which elements lie strictly between the minimum and maximum values of the array.

Once the minimum and maximum are known, each element can be classified in constant time, reducing the entire solution to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We translate the condition “has at least one smaller and at least one larger element” into a global characterization using minimum and maximum values.

1. Compute the minimum value in the array. This represents the smallest possible strength, so any element equal to it cannot have a strictly smaller neighbor.
2. Compute the maximum value in the array. This represents the largest possible strength, so any element equal to it cannot have a strictly larger neighbor.
3. Iterate through all elements and count how many satisfy the condition value > minimum and value < maximum. This directly encodes the requirement that both a smaller and a larger element exist somewhere in the array.
4. Return the count as the answer.

The key idea is that existence of any smaller element is equivalent to being strictly greater than the global minimum, and existence of any larger element is equivalent to being strictly less than the global maximum. This eliminates any need for pairwise comparisons.

### Why it works

The correctness comes from how global extrema encode all possible comparisons. If an element equals the minimum value, then no strictly smaller element exists anywhere in the array. If it is larger than the minimum, the minimum itself guarantees the existence of a smaller element. The same reasoning applies symmetrically for the maximum. Therefore, satisfying both inequalities is exactly equivalent to satisfying the original condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    mn = min(a)
    mx = max(a)
    
    ans = 0
    for x in a:
        if mn < x < mx:
            ans += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by reading the array and computing its minimum and maximum in linear time. These two values are the only global information required to evaluate every element.

The loop then checks each element against the strict inequalities. The condition is written carefully as mn < x < mx to ensure that boundary elements are excluded. A common mistake is using non-strict comparisons, which would incorrectly include elements equal to the minimum or maximum.

The overall structure is intentionally simple: all heavy computation is pushed into a single pass, and classification is done in constant time per element.

## Worked Examples

### Example 1

Input:

```
2
1 5
```

| i | value | min | max | condition (min < x < max) | counted |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 5 | false | 0 |
| 2 | 5 | 1 | 5 | false | 0 |

The minimum is 1 and the maximum is 5. Neither endpoint can be supported because each lacks either a smaller or larger neighbor. The result is 0.

### Example 2

Input:

```
3
1 2 5
```

| i | value | min | max | condition (min < x < max) | counted |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 5 | false | 0 |
| 2 | 2 | 1 | 5 | true | 1 |
| 3 | 5 | 1 | 5 | false | 1 |

Here the value 2 lies strictly between 1 and 5, so it has both a smaller and a larger element somewhere in the array. The other two values sit on the extremes and fail one side of the requirement.

These traces show that only interior elements with respect to global extrema are valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute min and max, one pass to count valid elements |
| Space | O(1) | Only a few variables are used beyond the input array |

The linear scan is well within limits for n up to 100,000. Memory usage is minimal since no auxiliary data structures beyond the input list are required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio

    out = sysio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample cases
assert run("2\n1 5\n") == "0", "sample 1"
assert run("3\n1 2 5\n") == "1", "sample 2"

# all equal
assert run("4\n7 7 7 7\n") == "0", "all equal"

# strictly increasing
assert run("5\n1 2 3 4 5\n") == "3", "middle elements only"

# two distinct values
assert run("6\n1 1 1 2 2 2\n") == "0", "no interior values"

# single element
assert run("1\n10\n") == "0", "single element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 0 | no element can satisfy both sides |
| strictly increasing array | n-2 | only interior elements qualify |
| two-value array | 0 | extremes only, no valid interior |
| single element | 0 | boundary minimal case |

## Edge Cases

When all elements are identical, both minimum and maximum are the same value. In that situation, the condition mn < x < mx fails for every element because no number can lie strictly between equal bounds. The algorithm correctly returns zero because every element is excluded by both comparisons.

When there are only two distinct values, for example an array like [1, 1, 1, 5, 5], the minimum is 1 and the maximum is 5. Neither 1 nor 5 lies strictly between them, so again no element is counted. This matches the fact that any chosen element fails at least one side of the requirement.

When the array has exactly one element, both minimum and maximum are equal to that element, and the strict inequality eliminates it immediately. The algorithm naturally returns zero without any special handling.
