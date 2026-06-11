---
title: "CF 1296A - Array with Odd Sum"
description: "We have an array of integers. An operation allows us to pick two different positions and copy the value from one position into the other. Since we may repeat this operation any number of times, values can be duplicated throughout the array."
date: "2026-06-11T18:32:25+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1296
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 617 (Div. 3)"
rating: 800
weight: 1296
solve_time_s: 108
verified: true
draft: false
---

[CF 1296A - Array with Odd Sum](https://codeforces.com/problemset/problem/1296/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of integers. An operation allows us to pick two different positions and copy the value from one position into the other. Since we may repeat this operation any number of times, values can be duplicated throughout the array.

For each test case, we need to determine whether it is possible to transform the array so that the final sum of all elements is odd.

The constraints are very small. The total number of elements across all test cases is at most 2000, so even relatively inefficient solutions would fit comfortably. The real challenge is understanding what the operation can and cannot change.

The key observation is that copying values does not create new numbers. The only thing that matters for the parity of the sum is whether elements are odd or even. Every operation replaces one element with another existing element, so the array always contains only values that originally appeared.

To get an odd sum, the final array must contain an odd number of odd elements. Since the parity of the sum is exactly the parity of the count of odd numbers, the problem becomes a question about odd and even values rather than the actual magnitudes.

A few edge cases are easy to miss.

Consider:

```
1
4
2 2 8 8
```

The answer is `NO`. Every value is even, and copying even values can never create an odd value. A careless solution that only checks whether operations are available would incorrectly answer `YES`.

Consider:

```
1
4
5 5 5 5
```

The answer is `NO`. All values are odd and there are four of them, so the sum is even. Since there is no even value in the array, every position will always remain odd after any sequence of operations. The number of odd elements stays equal to `n`, so the sum can never become odd.

Consider:

```
1
2
2 3
```

The answer is `YES`. The original sum is already odd, so no operation is needed. Any solution that assumes at least one operation must be performed would fail here.

## Approaches

A brute-force mindset starts by thinking about the operations directly. We could try generating reachable arrays and checking whether any of them has an odd sum. Since each operation chooses two indices and can be repeated indefinitely, the state space explodes very quickly. Even for modest values of `n`, the number of possible arrays becomes enormous. This approach is correct in principle because it explores all possibilities, but it is completely impractical.

The reason the brute-force idea feels difficult is that it focuses on exact values. The operation actually preserves much less information than it appears to. The only thing relevant to the final answer is parity.

An odd sum occurs exactly when the number of odd elements is odd.

Suppose the current sum is already odd. Then we can simply perform zero operations and answer `YES`.

Now suppose the current sum is even. Can we change its parity?

If the array contains both an odd value and an even value, then we can copy one parity onto positions of the other parity. This allows us to change the count of odd elements. In particular, we can always make the count of odd numbers become odd, which makes the total sum odd.

If all numbers are even, every value that can ever appear is even, so the sum always remains even.

If all numbers are odd, then every position always contains an odd number. The count of odd elements is permanently equal to `n`. The sum is odd only when `n` is odd. Since we are currently considering the case where the sum is even, this means `n` is even and the answer is `NO`.

This leads to a very simple criterion:

If the current sum is odd, answer `YES`.

Otherwise, answer `YES` only when the array contains at least one odd and at least one even number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the sum of all elements.
2. If the sum is odd, print `"YES"`.

No operation is required because the target condition is already satisfied.
3. Count whether the array contains at least one odd element.
4. Count whether the array contains at least one even element.
5. If both parities are present, print `"YES"`.

Having both parities means we can modify the number of odd elements through copying operations, making an odd total sum achievable.
6. Otherwise, print `"NO"`.

When all values have the same parity, every future value also has that parity, so an even sum cannot be turned into an odd one.

### Why it works

The parity of the sum depends only on the parity of the number of odd elements. If the initial sum is already odd, the goal is achieved immediately.

When both odd and even values exist, copying allows us to convert elements from one parity class to the other, changing the number of odd elements. This makes it possible to obtain an odd count of odd numbers and hence an odd sum.

When all values are even, every reachable array consists entirely of even numbers. When all values are odd, every reachable array consists entirely of odd numbers. In either case, the parity structure cannot change, so an even sum remains even forever. These are exactly the situations where the answer is `NO`.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    if sum(a) % 2 == 1:
        print("YES")
        continue

    has_odd = any(x % 2 for x in a)
    has_even = any(x % 2 == 0 for x in a)

    if has_odd and has_even:
        print("YES")
    else:
        print("NO")
```

The first check handles the easiest case. If the sum is already odd, we do not need to reason about operations at all.

The variables `has_odd` and `has_even` record whether each parity appears in the array. Their actual counts are unnecessary. Only the existence of both parities matters.

The final condition follows directly from the proof. An even sum can be changed into an odd one only when both odd and even values are available somewhere in the array.

No overflow concerns exist because the largest possible sum is only `2000 × 2000 = 4,000,000`, which easily fits in Python integers.

## Worked Examples

### Example 1

Input:

```
n = 2
a = [2, 3]
```

| Step | Sum | Has Odd | Has Even | Result |
| --- | --- | --- | --- | --- |
| Initial state | 5 | Yes | Yes | - |
| Check sum parity | 5 is odd | Yes | Yes | YES |

The sum is already odd. The algorithm immediately answers `YES` without considering any operations.

### Example 2

Input:

```
n = 4
a = [2, 2, 8, 8]
```

| Step | Sum | Has Odd | Has Even | Result |
| --- | --- | --- | --- | --- |
| Initial state | 20 | No | Yes | - |
| Check sum parity | Even | No | Yes | Continue |
| Parity presence | No odd values | No | Yes | NO |

This example shows why merely having operations available is not enough. Every value is even, so every future value is also even. An odd sum is impossible.

### Example 3

Input:

```
n = 3
a = [3, 3, 3]
```

| Step | Sum | Has Odd | Has Even | Result |
| --- | --- | --- | --- | --- |
| Initial state | 9 | Yes | No | - |
| Check sum parity | Odd | Yes | No | YES |

Even though all values share the same parity, the current sum is already odd, so the answer is `YES`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute the sum and parity information |
| Space | O(1) | Only a few variables are used besides the input array |

The total number of elements across all test cases is at most 2000, so an O(n) solution runs comfortably within the limits. Memory usage is constant apart from storing the input array.

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

        if sum(a) % 2 == 1:
            out.append("YES")
            continue

        has_odd = any(x % 2 for x in a)
        has_even = any(x % 2 == 0 for x in a)

        out.append("YES" if has_odd and has_even else "NO")

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""5
2
2 3
4
2 2 8 8
3
3 3 3
4
5 5 5 5
4
1 1 1 1
"""
) == """YES
NO
YES
NO
NO
"""

# minimum size, odd element
assert run(
"""1
1
1
"""
) == """YES
"""

# minimum size, even element
assert run(
"""1
1
2
"""
) == """NO
"""

# mixed parity with even initial sum
assert run(
"""1
2
1 2
"""
) == """YES
"""

# all odd, even count
assert run(
"""1
6
7 7 7 7 7 7
"""
) == """NO
"""

# large all-even case
assert run(
"""1
8
2 4 6 8 10 12 14 16
"""
) == """NO
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, [1]` | YES | Smallest array with odd sum |
| `n=1, [2]` | NO | Smallest array with even sum |
| `n=2, [1,2]` | YES | Mixed parity can create odd sum |
| `n=6, [7,7,7,7,7,7]` | NO | All odd with even count |
| `n=8, [2,4,6,8,10,12,14,16]` | NO | All-even array |

## Edge Cases

### Single Even Element

Input:

```
1
1
2
```

The sum is `2`, which is even. The array contains no odd value and one even value. The algorithm reaches the final condition and prints `NO`.

Since there is only one value and every operation copies an existing value, the array can never contain an odd number.

### All Odd Values With Even Length

Input:

```
1
4
5 5 5 5
```

The sum is `20`, which is even. The array contains odd values but no even values.

The algorithm prints `NO`.

Every position will always contain an odd value after any sequence of assignments. The count of odd elements remains `4`, so the sum remains even forever.

### Mixed Parities With Even Initial Sum

Input:

```
1
4
1 1 2 2
```

The sum is `6`, which is even. The array contains both odd and even values.

The algorithm prints `YES`.

For example, copy an odd value onto one of the even positions. The array can become `[1, 1, 1, 2]`, whose sum is `5`, an odd number.

### Already Odd Sum

Input:

```
1
3
1 2 4
```

The sum is `7`, which is odd.

The algorithm immediately prints `YES`.

This case confirms that performing operations is optional. The correct answer may already be achieved in the original array.
