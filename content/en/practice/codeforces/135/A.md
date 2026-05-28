---
title: "CF 135A - Replacement"
description: "We start with an array of positive integers. We must change exactly one element to a different value, still between 1 and 10^9. After that single replacement, we sort the array in non-decreasing order."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 135
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 97 (Div. 1)"
rating: 1300
weight: 135
solve_time_s: 94
verified: true
draft: false
---

[CF 135A - Replacement](https://codeforces.com/problemset/problem/135/A)

**Rating:** 1300  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array of positive integers. We must change exactly one element to a different value, still between `1` and `10^9`. After that single replacement, we sort the array in non-decreasing order.

The task is to produce the lexicographically smallest possible sorted array after performing exactly one replacement.

The wording in the original statement about “minimum possible values for each position” is another way of describing the lexicographically minimum sorted array. We want the first position as small as possible, then the second, and so on.

The constraint `n ≤ 10^5` immediately rules out anything quadratic. Even a simple `O(n^2)` algorithm would require around `10^10` operations in the worst case, which is far beyond the limit. Sorting is cheap enough here because `O(n log n)` for `10^5` elements is easily manageable in Python.

The tricky part is understanding what replacement actually produces the smallest final sorted array.

Suppose the array is already sorted:

```
1 2 3 4 5
```

If we replace the largest value `5` with `1`, we get:

```
1 1 2 3 4
```

This is clearly optimal because making a number smaller helps the sorted order as early as possible.

Now consider an array where every element is already `1`:

```
1 1 1
```

We are forced to change one element to something different. We cannot replace a `1` with another `1`. The best option is increasing one element minimally:

```
1 1 2
```

A careless implementation might still try to replace something with `1`, producing the unchanged array, which is illegal.

Another subtle case is when the array contains multiple minimum values but also larger numbers:

```
1 1 5
```

The correct answer is:

```
1 1 1
```

We replace `5` with `1`. A naive “always increase one value” strategy would miss that we can still make the array smaller overall.

The real distinction is whether the array already consists entirely of `1`s`.

## Approaches

The brute-force idea is straightforward. For every position, try replacing that element with every candidate value that could matter, sort the resulting array, and keep the lexicographically smallest answer.

This works conceptually because the problem asks directly for the smallest possible final sorted array. If we enumerate every valid replacement, one of them must be optimal.

The problem is the number of possibilities. Even if we only tried a small set of candidate replacement values, sorting an array of size `n` for every position already costs `O(n^2 log n)`. With `n = 10^5`, this is completely infeasible.

The key observation is that only the smallest possible replacement value matters.

If the array contains any value larger than `1`, then replacing one such value with `1` strictly improves the sorted array. Among all choices, replacing the largest element is best because it removes the biggest number while adding the smallest allowed number.

For example:

```
1 2 3 4 5
```

becomes:

```
1 1 2 3 4
```

after replacing `5` with `1`.

The only time this strategy fails is when every element already equals `1`. Then we cannot replace anything with `1`, because the value must actually change. The smallest valid modification is replacing one `1` with `2`.

So the optimal strategy becomes very small:

1. Sort the array.
2. If all elements are `1`, change the last one to `2`.
3. Otherwise, change the largest element to `1`.
4. Sort again if necessary.

Because the array is already sorted, the final arrangement is immediate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n) or worse | O(n) | Too slow |
| Optimal | O(n log n) | O(1) extra, excluding sort | Accepted |

## Algorithm Walkthrough

1. Read the array and sort it in non-decreasing order.

Sorting lets us reason directly about lexicographic order. The smallest elements appear first, so improving earlier positions becomes obvious.
2. Check whether the largest element equals `1`.

Since the array is sorted, this condition means every element is `1`.
3. If all elements are `1`, replace the last element with `2`.

We must modify exactly one value, and `2` is the smallest valid number different from `1`.
4. Otherwise, replace the last element, which is currently the maximum, with `1`.

This removes the largest value and inserts the smallest possible value, producing the lexicographically smallest sorted array.
5. Sort the array again if needed, or simply print the modified sorted order.

After replacing the largest element with `1`, the new `1` belongs at the front. Performing another sort is simple and still efficient enough.

### Why it works

The lexicographic order is determined by the earliest differing position. To minimize the final sorted array, we want as many small values as possible at the beginning.

If the array contains some value greater than `1`, replacing one such value with `1` increases the count of minimum elements and removes a larger number. Replacing the largest value is always at least as good as replacing any smaller value, because the prefix after sorting remains identical while later positions become smaller.

If every element is already `1`, decreasing any value is impossible. The smallest legal change is increasing exactly one element to `2`, giving the smallest possible sorted result among all valid modifications.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

a.sort()

if a[-1] == 1:
    a[-1] = 2
else:
    a[-1] = 1

a.sort()

print(*a)
```

The solution begins by sorting the array. This makes the maximum element easy to access at `a[-1]`.

The condition `a[-1] == 1` is enough to determine whether all elements are `1`, because the array is sorted. If the maximum is `1`, then every value must also be `1`.

When all elements are `1`, we replace the last element with `2`. Choosing any larger number would produce a lexicographically worse array.

Otherwise, we replace the maximum element with `1`. This introduces one more minimum value while removing the largest existing number.

The final sort restores non-decreasing order. Its cost is still acceptable because sorting `10^5` integers twice is easily within the limit.

A common mistake is forgetting that the replacement must actually change the value. For an all-ones array, replacing a `1` with another `1` is invalid.

Another easy bug is replacing the smallest non-one element instead of the largest one. That leaves a larger number in the array and produces a worse lexicographic result.

## Worked Examples

### Example 1

Input:

```
5
1 2 3 4 5
```

| Step | Array State |
| --- | --- |
| Initial array | 1 2 3 4 5 |
| After sorting | 1 2 3 4 5 |
| Largest element is not 1 | replace 5 with 1 |
| Modified array | 1 2 3 4 1 |
| After final sort | 1 1 2 3 4 |

Final output:

```
1 1 2 3 4
```

This trace shows the main greedy idea. Removing the largest number while adding `1` produces the smallest possible prefix after sorting.

### Example 2

Input:

```
3
1 1 1
```

| Step | Array State |
| --- | --- |
| Initial array | 1 1 1 |
| After sorting | 1 1 1 |
| Largest element is 1 | replace last 1 with 2 |
| Modified array | 1 1 2 |
| After final sort | 1 1 2 |

Final output:

```
1 1 2
```

This example demonstrates the special case where decreasing any value is impossible. The algorithm makes the smallest legal increase instead.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Dominated by sorting |
| Space | O(1) extra, excluding sort | Only a few variables are used |

With `n = 10^5`, an `O(n log n)` solution easily fits within the time limit. Python’s built-in sort is highly optimized and handles this input size comfortably.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    if a[-1] == 1:
        a[-1] = 2
    else:
        a[-1] = 1

    a.sort()

    print(*a)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("5\n1 2 3 4 5\n") == "1 1 2 3 4\n", "sample 1"

# minimum size
assert run("1\n1\n") == "2\n", "single element equal to 1"

# single non-one element
assert run("1\n7\n") == "1\n", "replace maximum with 1"

# all equal values
assert run("4\n1 1 1 1\n") == "1 1 1 2\n", "all ones case"

# mixed values
assert run("5\n1 1 5 7 9\n") == "1 1 1 5 7\n", "replace largest value"

# already sorted but with duplicates
assert run("6\n2 2 2 2 2 2\n") == "1 2 2 2 2 2\n", "duplicate non-one values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `2` | Minimum-size all-ones case |
| `1 / 7` | `1` | Single-element non-one array |
| `1 1 1 1` | `1 1 1 2` | Forced increase when every value is 1 |
| `1 1 5 7 9` | `1 1 1 5 7` | Replacing the maximum is optimal |
| `2 2 2 2 2 2` | `1 2 2 2 2 2` | Handling repeated large values |

## Edge Cases

Consider the input:

```
1
1
```

The sorted array is still `[1]`. Since every element equals `1`, replacing with `1` is illegal because the value must change. The algorithm changes the only element to `2`, producing:

```
2
```

Now consider:

```
3
1 1 5
```

After sorting, the array is:

```
1 1 5
```

The largest value is not `1`, so the algorithm replaces `5` with `1`:

```
1 1 1
```

This is optimal because the first differing position compared to any other valid answer becomes as small as possible.

Another tricky case is:

```
4
2 2 2 2
```

The algorithm replaces the largest `2` with `1`:

```
1 2 2 2
```

Replacing any other element gives the same multiset after sorting, so choosing the last element is sufficient.

Finally, consider:

```
5
1 1 1 1 1000000000
```

The algorithm replaces the huge value with `1`, producing:

```
1 1 1 1 1
```

This confirms that the actual magnitude of the removed value does not matter. Any value larger than `1` should become `1`, and removing the maximum gives the best lexicographic result.
