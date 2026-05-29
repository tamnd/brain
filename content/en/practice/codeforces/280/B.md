---
title: "CF 280B - Maximum Xor Secondary"
description: "We are given an array of distinct positive integers. For every subarray, we look at its largest value and its second largest value, then compute their XOR. Among all possible subarrays, we need the maximum such XOR value."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 280
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 172 (Div. 1)"
rating: 1800
weight: 280
solve_time_s: 95
verified: true
draft: false
---

[CF 280B - Maximum Xor Secondary](https://codeforces.com/problemset/problem/280/B)

**Rating:** 1800  
**Tags:** data structures, implementation, two pointers  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of distinct positive integers. For every subarray, we look at its largest value and its second largest value, then compute their XOR. Among all possible subarrays, we need the maximum such XOR value.

The direct interpretation is simple: every subarray contributes exactly one pair, its largest and second largest elements. The difficulty comes from the number of subarrays. An array of size $10^5$ has roughly $5 \times 10^9$ subarrays, far too many to examine individually.

The constraints force us to think about structure instead of enumeration. With $n = 10^5$ and a 1 second limit, quadratic algorithms are already risky in Python, and cubic algorithms are completely impossible. A realistic target is $O(n \log n)$ or $O(n)$.

The tricky part is identifying which pairs of elements can ever become the maximum and second maximum of some subarray.

Consider this example:

```
5 2 1 4 3
```

The subarray `[4, 3]` has maximum `4` and second maximum `3`, giving `7`.

A naive thought is to try every pair `(a[i], a[j])`, but most pairs are invalid because there may be a larger element between them. For example:

```
1 10 2
```

The pair `(1, 2)` can never become the top two elements of any subarray containing both, because `10` is larger than both and lies between them.

Another subtle case is strictly increasing arrays:

```
1 2 3 4 5
```

Every valid pair is adjacent in value order within some prefix. A careless solution that only checks neighboring indices would miss possibilities if it does not maintain the correct monotonic structure.

A decreasing array behaves symmetrically:

```
5 4 3 2 1
```

The answer comes from neighboring elements again, but discovered from the opposite direction.

The distinctness guarantee matters heavily. If duplicates existed, defining the second maximum would become ambiguous. The problem avoids that complication entirely.

## Approaches

The brute force approach is straightforward. Enumerate every subarray, find its maximum and second maximum, compute their XOR, and track the largest result.

For a subarray of length $k$, finding the top two values takes $O(k)$. Since there are $O(n^2)$ subarrays, the total complexity becomes $O(n^3)$. Even optimizing maximum tracking only reduces this to roughly $O(n^2)$, which is still too slow for $10^5$.

The key observation is that we do not actually care about subarrays themselves. We only care about pairs of numbers that can become the largest and second largest elements of some subarray.

Suppose we look at two positions $i < j$. They form a valid pair if one of them is the maximum of the interval and the other is the second maximum. That means every element between them must be smaller than the larger of the two.

Assume $a[i] < a[j]$. Then $a[i]$ can become the second maximum only if every element between $i$ and $j$ is smaller than $a[i]$. Otherwise some middle value would replace it as second maximum.

This condition is exactly what a monotonic stack captures.

When processing the array left to right with a decreasing stack, every popped or neighboring element represents the closest larger value relationship. Those are precisely the pairs that can become the top two elements of some subarray.

The beautiful part is that each element enters and leaves the stack once, giving linear complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ or $O(n^2)$ with optimizations | $O(1)$ | Too slow |
| Optimal Monotonic Stack | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Initialize an empty decreasing stack and a variable `ans = 0`.
2. Process the array from left to right.
3. For the current value `x`, repeatedly pop elements from the stack while the top of the stack is smaller than `x`.

Each popped value `y` forms a valid candidate pair with `x`, so update:

$$ans = \max(ans, x \oplus y)$$

This works because `x` is the first larger element to the right of `y`. Every element between them is smaller than `y`, so they can become the largest and second largest elements of a subarray.
4. After all smaller elements are removed, if the stack is not empty, then the current top `y` is larger than `x`.

Update:

$$ans = \max(ans, x \oplus y)$$

Here, `y` and `x` also form a valid pair because all elements between them are smaller than `x`.
5. Push `x` onto the stack.
6. Continue until the entire array is processed.

### Why it works

The stack always remains strictly decreasing.

For every element, we discover exactly the nearest larger element relationships that matter. Any pair capable of becoming the maximum and second maximum of some subarray must have no larger obstruction between them. The monotonic stack enumerates precisely these pairs.

If a pair is skipped by the algorithm, then some larger element lies between them, making it impossible for them to be the top two elements of any subarray together.

Since every valid pair is checked once, the maximum XOR found is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    stack = []
    ans = 0

    for x in a:
        while stack and stack[-1] < x:
            ans = max(ans, stack[-1] ^ x)
            stack.pop()

        if stack:
            ans = max(ans, stack[-1] ^ x)

        stack.append(x)

    print(ans)

solve()
```

The stack stores values in strictly decreasing order. Whenever a new value `x` arrives, all smaller elements on top are popped because they can never help future elements anymore.

Before removing each smaller value, we evaluate its XOR with `x`. That pair corresponds to a valid subarray relationship where one becomes maximum and the other second maximum.

After popping finishes, the remaining top element, if it exists, is the nearest larger value to the left. This pair is also valid and must be checked.

Each element is pushed once and popped once, which guarantees linear complexity.

One subtle implementation detail is the order of operations. The XOR must be computed before popping. Another is that we only compare against the current stack top after all smaller values are removed. At that point the stack top is guaranteed to be larger than the current value.

Python integers safely handle the XOR range since values are at most $10^9$.

## Worked Examples

### Example 1

Input:

```
5
5 2 1 4 3
```

| Current x | Stack Before | Action | XOR Checked | Best Answer |
| --- | --- | --- | --- | --- |
| 5 | [] | push 5 | none | 0 |
| 2 | [5] | compare with 5 | 5 ^ 2 = 7 | 7 |
| 1 | [5, 2] | compare with 2 | 2 ^ 1 = 3 | 7 |
| 4 | [5, 2, 1] | pop 1 | 1 ^ 4 = 5 | 7 |
| 4 | [5, 2] | pop 2 | 2 ^ 4 = 6 | 7 |
| 4 | [5] | compare with 5 | 5 ^ 4 = 1 | 7 |
| 3 | [5, 4] | compare with 4 | 4 ^ 3 = 7 | 7 |

Final answer:

```
7
```

This trace shows both types of valid pairs. Some arise during popping, such as `(2, 4)`, while others come from the remaining stack top, such as `(4, 3)`.

### Example 2

Input:

```
5
9 8 3 5 7
```

| Current x | Stack Before | Action | XOR Checked | Best Answer |
| --- | --- | --- | --- | --- |
| 9 | [] | push 9 | none | 0 |
| 8 | [9] | compare with 9 | 9 ^ 8 = 1 | 1 |
| 3 | [9, 8] | compare with 8 | 8 ^ 3 = 11 | 11 |
| 5 | [9, 8, 3] | pop 3 | 3 ^ 5 = 6 | 11 |
| 5 | [9, 8] | compare with 8 | 8 ^ 5 = 13 | 13 |
| 7 | [9, 8, 5] | pop 5 | 5 ^ 7 = 2 | 13 |
| 7 | [9, 8] | compare with 8 | 8 ^ 7 = 15 | 15 |

Final answer:

```
15
```

This example demonstrates how the stack identifies the relevant neighboring larger relationships without examining all subarrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each element is pushed and popped at most once |
| Space | $O(n)$ | The stack may contain all elements in decreasing order |

With $10^5$ elements, linear time is easily fast enough. The memory usage is also comfortably within limits since the stack stores at most the entire array once.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    stack = []
    ans = 0

    for x in a:
        while stack and stack[-1] < x:
            ans = max(ans, stack[-1] ^ x)
            stack.pop()

        if stack:
            ans = max(ans, stack[-1] ^ x)

        stack.append(x)

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run("5\n5 2 1 4 3\n") == "7", "sample 1"

# minimum valid size
assert run("2\n1 2\n") == "3", "minimum size"

# strictly increasing
assert run("5\n1 2 3 4 5\n") == "7", "increasing array"

# strictly decreasing
assert run("5\n5 4 3 2 1\n") == "7", "decreasing array"

# middle obstruction
assert run("3\n1 10 2\n") == "11", "large middle element blocks pair"

# random structure
assert run("5\n9 8 3 5 7\n") == "15", "mixed structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2` | `3` | Smallest legal input |
| `1 2 3 4 5` | `7` | Increasing monotonic behavior |
| `5 4 3 2 1` | `7` | Decreasing monotonic behavior |
| `1 10 2` | `11` | Invalid distant pairs blocked by larger middle value |
| `9 8 3 5 7` | `15` | General mixed configuration |

## Edge Cases

Consider the array:

```
3
1 10 2
```

The pair `(1, 2)` looks tempting because `1 ^ 2 = 3`, but they can never become the largest and second largest values of the same subarray. The value `10` lies between them and dominates both.

The algorithm handles this naturally.

Processing steps:

```
stack = []
push 1

x = 10
1 < 10, check 1 ^ 10 = 11
pop 1
push 10

x = 2
check 10 ^ 2 = 8
```

The pair `(1, 2)` is never considered because the monotonic structure recognizes that `10` blocks it.

Now consider a strictly increasing array:

```
5
1 2 3 4 5
```

Every new element pops the previous one immediately.

The checks become:

```
1 ^ 2 = 3
2 ^ 3 = 1
3 ^ 4 = 7
4 ^ 5 = 1
```

The maximum answer is correctly found as `7`.

Finally, consider a strictly decreasing array:

```
5
5 4 3 2 1
```

Nothing is ever popped. Every element compares only with the nearest larger value on the left:

```
5 ^ 4 = 1
4 ^ 3 = 7
3 ^ 2 = 1
2 ^ 1 = 3
```

The algorithm still explores all valid pairs because the stack preserves the decreasing structure exactly.
