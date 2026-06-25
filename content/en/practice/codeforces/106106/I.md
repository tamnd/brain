---
title: "CF 106106I - \u041d\u0435\u043c\u043d\u043e\u0436\u043a\u043e \u043c\u0430\u0442\u0435\u043c\u0430\u0442\u0438\u043a\u0438"
description: "The task asks for a simple mathematical observation. We are given a number k and need to find the largest positive integer n such that n is not greater than k and the value of n is exactly equal to its factorial."
date: "2026-06-25T11:41:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106106
codeforces_index: "I"
codeforces_contest_name: "\u0423\u0440\u0430\u043b\u044c\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u042e\u043d\u0438\u043e\u0440\u044b 2024"
rating: 0
weight: 106106
solve_time_s: 26
verified: true
draft: false
---

[CF 106106I - \u041d\u0435\u043c\u043d\u043e\u0436\u043a\u043e \u043c\u0430\u0442\u0435\u043c\u0430\u0442\u0438\u043a\u0438](https://codeforces.com/problemset/problem/106106/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 26s  
**Verified:** yes  

## Solution
## Problem Understanding

The task asks for a simple mathematical observation. We are given a number `k` and need to find the largest positive integer `n` such that `n` is not greater than `k` and the value of `n` is exactly equal to its factorial. The factorial of a number is the product of all positive integers up to that number. The original problem is from Codeforces Gym 106106, problem I, "Немножко математики".

The input contains only one integer `k`, with `1 ≤ k ≤ 10^5`. Since the upper bound is small, a direct simulation is already possible, but the more useful observation is that factorials grow extremely quickly. After the first few values, `n!` becomes much larger than `n`, so there cannot be many candidates to check.

The only positive integers that satisfy `n = n!` are `1` and `2`. For `n = 1`, the factorial is `1! = 1`. For `n = 2`, the factorial is `2! = 2`. For every `n ≥ 3`, the factorial contains a multiplication by at least `2`, and the result is strictly larger than `n`.

The main edge cases are when `k` is exactly one of these valid values or when it lies between them.

For input:

```
1
```

the correct output is:

```
1
```

A careless solution that only checks whether `k` itself satisfies the condition might fail if it assumes there is always a smaller answer.

For input:

```
3
```

the correct output is:

```
2
```

The value `3` is not valid because `3! = 6`, so the answer must move down to the previous valid number.

For input:

```
100000
```

the correct output is:

```
2
```

A brute-force factorial calculation may overflow in languages with fixed-size integers if it keeps multiplying unnecessarily, even though the answer is already known.

## Approaches

The straightforward approach is to iterate through every number from `1` to `k`, calculate its factorial, and remember the largest number whose factorial equals itself. This is correct because it directly checks the definition of a valid answer. However, even though `k` is only `100000`, repeatedly calculating factorials is unnecessary. The factorial value becomes enormous very quickly, and storing or computing these values adds complexity without providing useful information.

The key observation is that the equation `n = n!` is extremely restrictive. Once `n` reaches `3`, the factorial immediately becomes larger:

```
3! = 6 > 3
```

For every larger number the gap only increases. This leaves exactly two possible answers: `1` and `2`.

The problem then becomes a simple comparison. If `k` is at least `2`, the largest valid value available is `2`. Otherwise, the only possible answer is `1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k * k) in a naive factorial simulation | O(1) | Unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the value `k`.
2. Check whether `k` is at least `2`. The value `2` is valid because `2! = 2`, and no larger positive integer can satisfy the equation.
3. If `k` is smaller than `2`, output `1`, because `1! = 1` is the only remaining valid value.

Why it works: the factorial function has a fixed point only at `1` and `2` among positive integers. Once the number reaches `3`, multiplying by all previous positive integers makes the factorial larger than the original number forever.

## Why it works

The algorithm relies on the fact that there are only two positive integers where the number and its factorial are equal. The values `1` and `2` can be verified directly. For every `n ≥ 3`, we have:

```
n! = 1 * 2 * 3 * ... * n
```

The product contains the factors `1 * 2 * ... * (n - 1)`, which is already at least `2` for these values, and multiplying by `n` makes the factorial strictly greater than `n`. Therefore no value larger than `2` can be an answer. The algorithm only chooses between the two possible valid numbers, so it always returns the maximum one not exceeding `k`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input())
    if k >= 2:
        print(2)
    else:
        print(1)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the mathematical observation. The condition `k >= 2` covers every case where the answer can be `2`. Otherwise, `k` must be `1`, and the answer is also `1`.

There is no factorial calculation in the code. This avoids unnecessary multiplication and removes any risk of integer overflow in languages with smaller integer types.

## Worked Examples

### Example 1

Input:

```
4
```

| Step | k | Condition | Answer |
| --- | --- | --- | --- |
| 1 | 4 | `4 >= 2` is true | 2 |

The value `2` is valid and is the largest possible answer not exceeding `4`.

### Example 2

Input:

```
2
```

| Step | k | Condition | Answer |
| --- | --- | --- | --- |
| 1 | 2 | `2 >= 2` is true | 2 |

This checks the boundary where the largest valid number is exactly equal to the input.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only one comparison is performed |
| Space | O(1) | No additional data structures are used |

The solution easily fits the limits because it performs a constant amount of work regardless of the input value.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    k = int(input())
    if k >= 2:
        return "2\n"
    return "1\n"

# provided samples
assert solution("4\n") == "2\n", "sample 1"
assert solution("2\n") == "2\n", "sample 2"
assert solution("10\n") == "2\n", "sample 3"

# custom cases
assert solution("1\n") == "1\n", "minimum value"
assert solution("3\n") == "2\n", "first invalid factorial value"
assert solution("100000\n") == "2\n", "maximum input"
assert solution("2\n") == "2\n", "boundary value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Handles the smallest possible input |
| `3` | `2` | Confirms that values after `2` are rejected |
| `100000` | `2` | Handles the largest allowed input |
| `2` | `2` | Checks the exact boundary of the two valid answers |

## Edge Cases

For `k = 1`, the algorithm checks `k >= 2`, which is false, and returns `1`. This is correct because `1! = 1`, and there is no smaller positive integer candidate.

For `k = 3`, the algorithm returns `2` immediately. Although `3` is large enough to be considered, it cannot be used because `3! = 6`. The comparison with `2` captures the largest valid value below it.

For `k = 100000`, the algorithm does not attempt to compute any factorial. It returns `2` after a single comparison, avoiding the unnecessary growth of factorial values while still producing the correct result.
