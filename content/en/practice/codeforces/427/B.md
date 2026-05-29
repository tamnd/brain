---
title: "CF 427B - Prison Transfer"
description: "We have a line of prisoners, and each prisoner has a crime severity value. We must choose exactly c consecutive prisoners for transfer. Every prisoner inside the chosen segment must have severity at most t."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 427
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 244 (Div. 2)"
rating: 1100
weight: 427
solve_time_s: 93
verified: true
draft: false
---

[CF 427B - Prison Transfer](https://codeforces.com/problemset/problem/427/B)

**Rating:** 1100  
**Tags:** data structures, implementation  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of prisoners, and each prisoner has a crime severity value. We must choose exactly `c` consecutive prisoners for transfer. Every prisoner inside the chosen segment must have severity at most `t`.

The task is simply to count how many contiguous segments of length `c` satisfy this restriction.

The input gives the number of prisoners, the maximum allowed severity, and the required segment length. Then we receive the array of severities. The output is a single integer, the number of valid contiguous segments.

The constraints immediately rule out expensive approaches. The number of prisoners can reach `2 * 10^5`, which means an `O(n^2)` algorithm would perform roughly `4 * 10^10` operations in the worst case, far beyond the limit for a 1 second problem. We need something linear or close to linear.

The values themselves can be as large as `10^9`, but that does not matter much because we never perform arithmetic on them beyond comparisons with `t`.

There are several easy-to-miss edge cases.

One common mistake is forgetting that segments must be contiguous. For example:

```
5 3 2
1 5 2 3 1
```

The valid segments are:

- `[2,3]`
- `[3,1]`

The answer is `2`, not `4`. A careless solution might count all prisoners with value at most `3` and try to form combinations from them, which ignores the contiguous requirement.

Another subtle case happens when a bad prisoner splits the array into independent regions.

```
7 2 3
1 2 1 5 1 1 1
```

The first three prisoners form one valid segment. The last three prisoners form another. Any segment crossing the `5` is invalid. The correct answer is `2`.

A frequent off-by-one bug appears when a valid block length equals exactly `c`.

```
4 3 4
1 2 3 1
```

The whole array is valid, so the answer is `1`. Some implementations incorrectly use `length - c` instead of `length - c + 1`.

Another important edge case is when no prisoner satisfies the limit.

```
5 1 2
3 4 5 6 7
```

No segment works, so the answer is `0`.

## Approaches

The brute-force approach is straightforward. We examine every contiguous segment of length `c`, then check whether all values inside that segment are at most `t`.

There are `n - c + 1` possible segments. Checking one segment takes `O(c)` time, so the total complexity becomes `O((n - c + 1) * c)`. In the worst case, both `n` and `c` can be about `2 * 10^5`, giving roughly `4 * 10^10` operations. That is far too slow.

The brute-force works because the condition for a segment is simple: every element inside it must satisfy a limit. The problem is that neighboring segments overlap heavily, yet the brute-force repeatedly rechecks the same elements.

The key observation is that invalid prisoners completely separate the array into independent valid regions. Suppose we scan the array and focus only on consecutive stretches where every value is at most `t`.

For example:

```
1 2 1 5 1 1 1
```

The value `5` breaks the array into:

```
[1 2 1]   and   [1 1 1]
```

Inside a valid block of length `L`, every contiguous subarray of length `c` is automatically valid. The number of such subarrays is:

```
L - c + 1
```

provided `L >= c`.

This transforms the problem into counting lengths of maximal valid blocks.

We scan once through the array while maintaining the current length of consecutive acceptable prisoners. When we encounter a value greater than `t`, the current block ends and we add its contribution.

This gives a linear `O(n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × c) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize an answer variable `ans = 0`.
2. Maintain a counter `length` representing the current consecutive block where all severities are at most `t`.
3. Traverse the array from left to right.
4. If the current severity is at most `t`, increment `length` because the valid block continues.
5. If the current severity is greater than `t`, the current valid block ends.

If `length >= c`, then this block contributes `length - c + 1` valid segments.

Add this value to the answer, then reset `length = 0`.
6. After finishing the traversal, process the final block as well.

This step is necessary because the array may end while still inside a valid block.
7. Print the accumulated answer.

### Why it works

The algorithm maintains the invariant that `length` always equals the size of the current maximal suffix consisting only of acceptable prisoners.

Whenever we encounter an invalid prisoner, no valid segment can cross that position. This means every valid segment must lie entirely inside one valid block. For a block of length `L`, every contiguous window of size `c` is valid, and the number of such windows is exactly `L - c + 1`.

Since the algorithm processes every valid block exactly once and counts all length-`c` windows inside it, every valid segment is counted once and only once.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, t, c = map(int, input().split())
a = list(map(int, input().split()))

ans = 0
length = 0

for x in a:
    if x <= t:
        length += 1
    else:
        if length >= c:
            ans += length - c + 1
        length = 0

if length >= c:
    ans += length - c + 1

print(ans)
```

The implementation directly follows the block-counting idea.

The variable `length` stores the size of the current consecutive valid region. Every time we read a value not exceeding `t`, we extend the region by one.

When a value exceeds `t`, we know the current region has ended. If its size is at least `c`, then it contains valid windows. The number of windows is `length - c + 1`.

The final `if` after the loop is easy to forget. Without it, any valid block ending at the last element would never be counted.

All computations fit comfortably inside Python integers. Even in the largest case, the answer is at most `n`.

## Worked Examples

### Example 1

Input:

```
4 3 3
2 3 1 1
```

| Position | Value | Valid (`<= t`) | Current `length` | Added to `ans` | Total `ans` |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | Yes | 1 | 0 | 0 |
| 1 | 3 | Yes | 2 | 0 | 0 |
| 2 | 1 | Yes | 3 | 0 | 0 |
| 3 | 1 | Yes | 4 | 0 | 0 |

After traversal:

```
length = 4
4 - 3 + 1 = 2
```

Final answer:

```
2
```

The valid segments are:

```
[2,3,1]
[3,1,1]
```

This example demonstrates that a single valid block can contain multiple overlapping valid segments.

### Example 2

Input:

```
7 2 3
1 2 1 5 1 1 1
```

| Position | Value | Valid (`<= t`) | Current `length` | Added to `ans` | Total `ans` |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | Yes | 1 | 0 | 0 |
| 1 | 2 | Yes | 2 | 0 | 0 |
| 2 | 1 | Yes | 3 | 0 | 0 |
| 3 | 5 | No | 0 | 1 | 1 |
| 4 | 1 | Yes | 1 | 0 | 1 |
| 5 | 1 | Yes | 2 | 0 | 1 |
| 6 | 1 | Yes | 3 | 0 | 1 |

After traversal:

```
length = 3
3 - 3 + 1 = 1
```

Final answer:

```
2
```

This trace shows how an invalid value splits the array into independent regions. No valid segment can cross the position containing `5`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each prisoner is processed exactly once |
| Space | O(1) | Only a few integer variables are used |

A linear scan over `2 * 10^5` elements is easily fast enough within the time limit. The memory usage is constant apart from storing the input array.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, t, c = map(int, input().split())
    a = list(map(int, input().split()))

    ans = 0
    length = 0

    for x in a:
        if x <= t:
            length += 1
        else:
            if length >= c:
                ans += length - c + 1
            length = 0

    if length >= c:
        ans += length - c + 1

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("4 3 3\n2 3 1 1\n") == "2", "sample 1"

# minimum size
assert run("1 5 1\n3\n") == "1", "single valid prisoner"

# no valid segment
assert run("5 1 2\n3 4 5 6 7\n") == "0", "all prisoners invalid"

# entire array valid
assert run("5 10 3\n1 2 3 4 5\n") == "3", "all windows valid"

# exact block size equals c
assert run("4 3 4\n1 2 3 1\n") == "1", "off-by-one check"

# multiple separated blocks
assert run("7 2 3\n1 2 1 5 1 1 1\n") == "2", "split by invalid prisoner"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 1 / 3` | `1` | Minimum input size |
| `5 1 2 / 3 4 5 6 7` | `0` | No valid segments |
| `5 10 3 / 1 2 3 4 5` | `3` | Entire array valid |
| `4 3 4 / 1 2 3 1` | `1` | Exact-length block handling |
| `7 2 3 / 1 2 1 5 1 1 1` | `2` | Splitting by invalid values |

## Edge Cases

Consider the case where a bad prisoner splits the array:

```
7 2 3
1 2 1 5 1 1 1
```

The scan builds a valid block of length `3`, then encounters `5`. Since `5 > 2`, the algorithm adds:

```
3 - 3 + 1 = 1
```

Then it resets the block length to zero and starts counting again. The final block also has length `3`, contributing another `1`. The total becomes `2`.

Now consider the exact-boundary case:

```
4 3 4
1 2 3 1
```

The entire array forms one valid block of length `4`. Since `length == c`, the formula gives:

```
4 - 4 + 1 = 1
```

This correctly counts the single valid segment consisting of the whole array.

Finally, consider a completely invalid array:

```
5 1 2
3 4 5 6 7
```

Every value exceeds `t`, so the algorithm repeatedly resets `length` to zero. No block ever reaches size `2`, so the answer remains `0`.
