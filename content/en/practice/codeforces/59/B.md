---
title: "CF 59B - Fortune Telling"
description: "Marina can pick any subset of flowers from the field. Each flower has a certain number of petals, and she will pluck all petals from all chosen flowers one by one. The phrases alternate between \"Loves\" and \"Doesn't love\", starting from \"Loves\" on the first petal."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 59
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 55 (Div. 2)"
rating: 1200
weight: 59
solve_time_s: 117
verified: false
draft: false
---

[CF 59B - Fortune Telling](https://codeforces.com/problemset/problem/59/B)

**Rating:** 1200  
**Tags:** implementation, number theory  
**Solve time:** 1m 57s  
**Verified:** no  

## Solution
## Problem Understanding

Marina can pick any subset of flowers from the field. Each flower has a certain number of petals, and she will pluck all petals from all chosen flowers one by one. The phrases alternate between `"Loves"` and `"Doesn't love"`, starting from `"Loves"` on the first petal.

The final phrase depends only on the total number of petals in the bouquet. If the total is odd, the last spoken phrase is `"Loves"`. If the total is even, the last phrase is `"Doesn't love"`.

The task becomes much simpler after this observation. We are not simulating the fortune telling process at all. We only need to choose a subset whose sum is odd, while making that sum as large as possible.

The number of flowers is at most 100, and each flower has at most 100 petals. Even a brute-force solution over all subsets would involve checking $2^{100}$ possibilities, which is completely impossible. A million operations is usually fine in competitive programming, but $2^{100}$ is astronomically larger.

The small value bounds on petal counts hint that the solution probably depends on parity rather than complicated optimization. Once we reduce the problem to "find the maximum odd sum", the structure becomes very direct.

There are a few edge cases that can easily break a careless implementation.

Suppose every flower has an even number of petals:

```
3
2 4 6
```

The total sum is even, and removing any even number still leaves an even sum. No odd bouquet exists, so the correct answer is:

```
0
```

A naive approach that always prints the total sum when possible would fail here.

Another tricky case is when the total sum is even, but there are odd flowers available:

```
4
1 2 4 8
```

The total sum is 15, which is already odd, so the answer is 15. Some implementations mistakenly remove an odd flower whenever they see one, even when the total is already correct.

A different failure mode appears when the total sum is even and there are multiple odd flowers:

```
5
1 3 5 2 2
```

The total sum is 13, already odd, so we keep everything. But if the total had been even, the correct strategy would be to remove the smallest odd flower, not just any odd flower. Removing a larger odd flower would reduce the answer unnecessarily.

For example:

```
3
3 5 8
```

The total is 16. Removing 5 gives 11, while removing 3 gives 13. The optimal answer is 13.

## Approaches

The brute-force idea is straightforward. Enumerate every possible subset of flowers, compute the total number of petals in that subset, and keep the largest odd sum.

This works because every bouquet corresponds to exactly one subset. If we check all subsets, we are guaranteed to find the best valid one.

The problem is the number of subsets. With $n = 100$, the total number of subsets is:

$$2^{100}$$

That is far beyond what any program can process within the time limit.

The key observation is that only parity matters.

An odd total produces `"Loves"`, and an even total produces `"Doesn't love"`. So we want the largest possible odd sum.

Start with the sum of all flowers. There are only two cases.

If the total sum is already odd, we should obviously keep every flower because removing any positive number only decreases the sum.

If the total sum is even, then we must change its parity. Removing an even flower keeps the sum even, so that does not help. Removing an odd flower flips the parity to odd.

Among all odd flowers, we should remove the smallest one because we want the remaining sum to stay as large as possible.

If there are no odd flowers at all, then every possible subset sum is even, and the answer is 0.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of flowers and the petal counts.
2. Compute the total sum of all petals.

Keeping all flowers gives the largest possible sum, so this is the best starting point.
3. Check whether the total sum is odd.

If it is odd, print the total immediately because no smaller subset can improve the answer.
4. If the total sum is even, search for the smallest flower with an odd number of petals.

Removing one odd number changes an even sum into an odd sum.
5. If such a flower exists, print:

$$\text{total sum} - \text{smallest odd flower}$$

This produces the maximum possible odd sum because we remove the minimum amount necessary to fix the parity.

1. If no odd flower exists, print 0.

In this situation every flower is even, so every subset sum is also even.

### Why it works

The algorithm relies on parity properties.

The sum of numbers changes parity only when an odd number is added or removed. Starting from the maximum possible sum, there are only two possibilities.

If the total sum is already odd, any removal would decrease the answer, so keeping everything is optimal.

If the total sum is even, we must remove an odd value to make it odd. Removing the smallest odd value minimizes the loss, which guarantees the resulting odd sum is as large as possible.

No other operation can produce a better answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

total = sum(a)

if total % 2 == 1:
    print(total)
else:
    smallest_odd = float('inf')

    for x in a:
        if x % 2 == 1:
            smallest_odd = min(smallest_odd, x)

    if smallest_odd == float('inf'):
        print(0)
    else:
        print(total - smallest_odd)
```

The program begins by reading the flower petal counts and computing their total sum.

The first branch handles the easiest case. If the total is already odd, we print it directly because keeping all flowers always maximizes the bouquet size.

The second branch searches for the minimum odd flower. The variable `smallest_odd` starts at infinity so we can safely minimize against real values during the loop.

The parity check uses `x % 2 == 1`. Any odd flower can flip the parity of the total when removed.

The condition:

```
smallest_odd == float('inf')
```

means that no odd flower was found. In that case every flower is even, and no odd subset sum exists.

There are no overflow concerns because the maximum possible total is only:

$$100 \times 100 = 10000$$

Still, Python integers handle much larger values automatically.

## Worked Examples

### Example 1

Input:

```
1
1
```

| Step | Value |
| --- | --- |
| Total sum | 1 |
| Total parity | Odd |
| Output | 1 |

The total is already odd, so taking the only flower is optimal.

### Example 2

Input:

```
3
3 5 8
```

| Step | Value |
| --- | --- |
| Total sum | 16 |
| Total parity | Even |
| Odd flowers | 3, 5 |
| Smallest odd | 3 |
| Final answer | 16 - 3 = 13 |

The trace shows why removing the smallest odd flower matters. Removing 5 would produce only 11, which is worse.

### Example 3

Input:

```
4
2 4 6 8
```

| Step | Value |
| --- | --- |
| Total sum | 20 |
| Total parity | Even |
| Odd flowers found | None |
| Output | 0 |

Every flower is even, so every subset sum remains even. No valid bouquet exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass to compute the sum and one pass to find the smallest odd flower |
| Space | $O(1)$ | Only a few variables are used |

With at most 100 flowers, the solution runs instantly. The algorithm is linear and uses constant extra memory, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    total = sum(a)

    if total % 2 == 1:
        print(total)
    else:
        smallest_odd = float('inf')

        for x in a:
            if x % 2 == 1:
                smallest_odd = min(smallest_odd, x)

        if smallest_odd == float('inf'):
            print(0)
        else:
            print(total - smallest_odd)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("1\n1\n") == "1", "sample 1"

# all even values
assert run("4\n2 4 6 8\n") == "0", "all sums are even"

# total already odd
assert run("4\n1 2 4 8\n") == "15", "keep all flowers"

# remove smallest odd
assert run("3\n3 5 8\n") == "13", "must remove minimum odd"

# minimum size with even flower
assert run("1\n2\n") == "0", "single even flower"

# maximum size style case
assert run("5\n100 100 100 100 99\n") == "499", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 / 2 4 6 8` | `0` | No odd subset exists |
| `4 / 1 2 4 8` | `15` | Keep all flowers when total is already odd |
| `3 / 3 5 8` | `13` | Must remove the smallest odd flower |
| `1 / 2` | `0` | Single even flower edge case |
| `5 / 100 100 100 100 99` | `499` | Works correctly with larger values |

## Edge Cases

Consider the input:

```
3
2 4 6
```

The algorithm computes the total sum as 12. Since 12 is even, it searches for the smallest odd flower. None exist because every value is even.

The variable `smallest_odd` never changes from infinity, so the algorithm prints 0.

This is correct because every subset of even numbers also has an even sum.

Now consider:

```
3
3 5 8
```

The total sum is 16, which is even. The algorithm scans the array and finds odd flowers 3 and 5. The minimum is 3.

Removing 3 produces:

```
16 - 3 = 13
```

which is odd and maximal.

If we removed 5 instead, the answer would be 11, so choosing the smallest odd flower is essential.

Finally, examine:

```
4
1 2 4 8
```

The total sum is 15, already odd.

The algorithm immediately prints 15 without removing anything.

This avoids a common mistake where implementations unnecessarily remove an odd flower even though the parity is already correct.
