---
title: "CF 1916A - 2023"
description: "We start with an unknown array a whose product of all elements is exactly 2023. Some k elements were removed, leaving the array b of length n. The task is to determine whether such an original array could exist. If it can, we must output any valid set of k removed numbers."
date: "2026-06-08T19:51:12+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1916
codeforces_index: "A"
codeforces_contest_name: "Good Bye 2023"
rating: 800
weight: 1916
solve_time_s: 155
verified: true
draft: false
---

[CF 1916A - 2023](https://codeforces.com/problemset/problem/1916/A)

**Rating:** 800  
**Tags:** constructive algorithms, implementation, math, number theory  
**Solve time:** 2m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an unknown array `a` whose product of all elements is exactly `2023`. Some `k` elements were removed, leaving the array `b` of length `n`.

The task is to determine whether such an original array could exist. If it can, we must output any valid set of `k` removed numbers. After multiplying all numbers in `b` and all numbers we output, the result must be exactly `2023`.

The key observation is that the order of elements does not matter. Only the product matters. If the product of the remaining numbers is already too large or is not a divisor of `2023`, there is no way to complete the array. Otherwise, we can choose removed numbers whose product fills the missing factor.

The constraints are extremely small. Both `n` and `k` are at most `5`, and there are at most `100` test cases. Even an exhaustive search over many possibilities would fit comfortably within the limits. Still, the problem has a simple mathematical solution that runs in constant time per test case.

There are several easy-to-miss cases.

Suppose the remaining product does not divide `2023`.

Input:

```
1
2 1
5 2
```

The product of `b` is `10`. Since `2023` is not divisible by `10`, no collection of additional integers can make the final product exactly `2023`. The correct answer is:

```
NO
```

A careless solution that only checks whether the product is less than `2023` would incorrectly accept this case.

Another important case occurs when the remaining product already equals `2023`.

Input:

```
1
1 1
2023
```

The missing product is `1`. Since we must output exactly one removed number, we can output:

```
YES
1
```

The value `1` preserves the total product. A solution that insists on finding a factor greater than `1` would fail.

A third edge case is when multiple removed numbers are required.

Input:

```
1
1 3
1
```

The remaining product is `1`, so the removed numbers must multiply to `2023`. One valid answer is:

```
YES
2023 1 1
```

We only need any valid collection of exactly `k` numbers. Forgetting the requirement to output exactly `k` values would produce an invalid answer.

## Approaches

A brute-force idea is to try all possible collections of `k` removed numbers and check whether their product, multiplied by the product of `b`, equals `2023`.

This works because the target product is fixed and very small. However, even with small constraints, the search space grows rapidly if we allow arbitrary candidate values. The approach depends on guessing factors and exploring combinations, which is unnecessary.

The structure of the problem suggests a much simpler direction. The original product is known in advance:

```
2023 = 7 × 17 × 17
```

Let

```
P = product of all elements in b
```

If an original array exists, then

```
P × (product of removed numbers) = 2023
```

This immediately implies that `P` must divide `2023`.

If `2023 % P != 0`, no solution exists.

Otherwise the missing product is

```
M = 2023 / P
```

Now we need exactly `k` removed numbers whose product is `M`.

The easiest construction is to place `M` as the first removed number and fill the remaining `k - 1` positions with `1`. Their product remains `M`, so the condition is satisfied.

This reduces the entire problem to one divisibility check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of candidate factors | O(k) | Unnecessary |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the product `P` of all elements in the given array `b`.
2. Check whether `2023` is divisible by `P`.

If `2023 % P != 0`, output `"NO"` because no collection of removed numbers can make the total product exactly `2023`.
3. Otherwise compute the missing factor:

```
M = 2023 / P
```
4. Output `"YES"`.
5. Construct the removed numbers as:

```
[M, 1, 1, ..., 1]
```

with exactly `k` numbers.
6. Output this list.

### Why it works

Let `P` be the product of the remaining array.

If `P` does not divide `2023`, then any product of removed numbers would have to equal `2023 / P`, which is not an integer. Since all array elements are integers, no valid original array can exist.

If `P` divides `2023`, define `M = 2023 / P`. The constructed removed numbers have product

```
M × 1 × 1 × ... × 1 = M
```

Hence the product of all elements of the reconstructed array is

```
P × M = P × (2023 / P) = 2023.
```

The construction always produces exactly `k` numbers, so every accepted case yields a valid answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, k = map(int, input().split())
    b = list(map(int, input().split()))

    prod = 1
    for x in b:
        prod *= x

    if 2023 % prod != 0:
        print("NO")
    else:
        print("YES")
        missing = 2023 // prod
        ans = [missing] + [1] * (k - 1)
        print(*ans)
```

The first part computes the product of the remaining elements. Since `n ≤ 5` and every value is at most `2023`, the product easily fits within Python's integer arithmetic.

The divisibility test is the entire feasibility check. If the remaining product is not a divisor of `2023`, reconstruction is impossible.

When reconstruction is possible, the code computes the missing factor `2023 // prod`. That value becomes the first removed element. The remaining positions are filled with `1`, which does not change the product and guarantees that exactly `k` numbers are printed.

The order of multiplication is irrelevant because only the final product matters.

## Worked Examples

### Example 1

Input:

```
1
4 2
1 289 1 1
```

| Step | Value |
| --- | --- |
| Product of `b` | 289 |
| Check `2023 % 289` | 0 |
| Missing factor | 7 |
| Output numbers | 7, 1 |

Verification:

```
289 × 7 × 1 = 2023
```

The trace shows the typical successful case. The remaining product already contains most of the factorization of `2023`, and only one factor is missing.

### Example 2

Input:

```
1
2 2
5 2
```

| Step | Value |
| --- | --- |
| Product of `b` | 10 |
| Check `2023 % 10` | 3 |
| Divisible? | No |
| Result | NO |

Since `10` is not a divisor of `2023`, no integer product can fill the gap. The algorithm immediately rejects the test case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Multiply all elements of `b` once |
| Space | O(1) | Only a few variables are stored |

With `n ≤ 5` and at most `100` test cases, the running time is effectively constant. The solution easily satisfies the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = []
    t = int(input())

    for _ in range(t):
        n, k = map(int, input().split())
        b = list(map(int, input().split()))

        prod = 1
        for x in b:
            prod *= x

        if 2023 % prod != 0:
            out.append("NO")
        else:
            out.append("YES")
            missing = 2023 // prod
            ans = [missing] + [1] * (k - 1)
            out.append(" ".join(map(str, ans)))

    return "\n".join(out) + "\n"

# sample-style checks
assert run(
"""1
4 2
1 289 1 1
"""
) == "YES\n7 1\n"

assert run(
"""1
2 2
5 2
"""
) == "NO\n"

# minimum size
assert run(
"""1
1 1
2023
"""
) == "YES\n1\n"

# product already 1, multiple removed values
assert run(
"""1
1 3
1
"""
) == "YES\n2023 1 1\n"

# exact factorization present
assert run(
"""1
3 1
7 17 17
"""
) == "YES\n1\n"

# non-divisor larger than a factor
assert run(
"""1
1 1
289
"""
) == "YES\n7\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2023` with `k=1` | `YES 1` | Product already complete |
| `1` with `k=3` | `YES 2023 1 1` | Exact number of removed elements |
| `7 17 17` | `YES 1` | Missing factor equals 1 |
| `5 2` | `NO` | Non-divisor rejection |
| `289` | `YES 7` | Missing factor greater than 1 |

## Edge Cases

Consider:

```
1
2 1
5 2
```

The product of `b` is `10`. The algorithm checks:

```
2023 % 10 = 3
```

Since the remainder is nonzero, it outputs:

```
NO
```

No integer factor can transform `10` into `2023`.

Consider:

```
1
1 1
2023
```

The product of `b` is already `2023`.

```
M = 2023 / 2023 = 1
```

The algorithm outputs:

```
YES
1
```

Multiplying by `1` keeps the total product unchanged.

Consider:

```
1
1 3
1
```

The product of `b` is `1`, so

```
M = 2023
```

The constructed removed numbers are:

```
2023 1 1
```

Their product is still `2023`, and exactly three numbers are produced as required.

Consider:

```
1
3 1
7 17 7
```

The product of `b` is

```
833
```

Since

```
2023 % 833 != 0
```

the algorithm outputs:

```
NO
```

This demonstrates that even when every element individually divides `2023`, their combined product may not, and the divisibility check correctly catches the failure.
