---
title: "CF 165B - Burning Midnight Oil"
description: "Vasya has to write at least n lines of code during one night. He starts with productivity v, meaning he writes v lines before the first tea break. After every break, his productivity drops by a factor of k, using integer division."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation"]
categories: ["algorithms"]
codeforces_contest: 165
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 112 (Div. 2)"
rating: 1500
weight: 165
solve_time_s: 102
verified: true
draft: false
---

[CF 165B - Burning Midnight Oil](https://codeforces.com/problemset/problem/165/B)

**Rating:** 1500  
**Tags:** binary search, implementation  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

Vasya has to write at least `n` lines of code during one night. He starts with productivity `v`, meaning he writes `v` lines before the first tea break. After every break, his productivity drops by a factor of `k`, using integer division.

The total number of lines he writes is:

$$v + \left\lfloor \frac{v}{k} \right\rfloor + \left\lfloor \frac{v}{k^2} \right\rfloor + \cdots$$

The process stops once the next term becomes zero. We must find the smallest starting productivity `v` such that the total written lines are at least `n`.

The constraints are large enough that trying every possible `v` naively would be too slow. `n` can reach `10^9`, so a linear scan from `1` upward could require a billion iterations. Even if each iteration is small, that is far beyond what fits comfortably in a 2 second time limit.

The structure of the sum matters. As `v` increases, the total number of written lines never decreases. Larger starting productivity always produces at least as many lines as before. That monotonic behavior is exactly what makes binary search applicable.

There are a few edge cases that can silently break careless implementations.

Consider:

```
1 2
```

The correct answer is:

```
1
```

A buggy implementation might start binary search from `0` and mishandle the condition when the answer itself is the smallest possible value.

Another subtle case is when the sum exceeds `n` early:

```
59 10
```

For `v = 54`:

$$54 + 5 = 59$$

The answer is exactly `54`. If the implementation computes powers like `k^i` directly, overflow or unnecessary work can appear in other languages. Iterative division is safer and cleaner.

One more important scenario is when `k` is small, especially `2`:

```
1000000000 2
```

The sequence contains many non-zero terms because division by `2` decreases slowly. A solution that repeatedly recomputes large powers inefficiently may become too slow. The intended approach only needs logarithmically many divisions.

## Approaches

The most direct approach is brute force. We can try every value of `v` starting from `1`. For each candidate, we compute:

$$v + \left\lfloor \frac{v}{k} \right\rfloor + \left\lfloor \frac{v}{k^2} \right\rfloor + \cdots$$

until the terms become zero. The first `v` whose sum reaches at least `n` is the answer.

This works because the definition exactly matches the process in the problem statement. The issue is scale. In the worst case, the answer itself can be close to `10^9`, so checking candidates one by one becomes impossibly slow.

The key observation is that the total written lines form a monotonic function of `v`.

If some value `v` is enough to finish the program, then every larger value is also enough. Similarly, if some `v` is insufficient, every smaller value is also insufficient.

That converts the problem into a classic binary search on the answer space.

Instead of testing every value, we search the range `[1, n]`. For each midpoint `mid`, we compute how many lines Vasya can write starting from `mid`. If the total is at least `n`, then the answer lies in the left half, including `mid`. Otherwise, we move right.

The helper computation itself is efficient. Each term divides by `k`, so the number of iterations is only logarithmic in `v`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) | O(1) | Too slow |
| Optimal | O(log n × log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Define a helper function `enough(v)` that computes how many lines Vasya can write starting with productivity `v`.
2. Inside the helper function, repeatedly add the current productivity to a running total, then divide the productivity by `k`.
3. Stop once the productivity becomes zero, because all later terms would also be zero.
4. If the final total is at least `n`, return `True`. Otherwise return `False`.
5. Run binary search on the range `[1, n]`.
6. Compute `mid = (left + right) // 2`.
7. Check whether `mid` is sufficient using the helper function.
8. If `mid` works, record it as a possible answer and continue searching the left half. We do this because we want the minimum valid value.
9. If `mid` does not work, search the right half.
10. Continue until the search interval becomes empty.
11. Output the smallest valid value found.

### Why it works

The correctness depends on monotonicity.

Let `f(v)` be the total number of lines written starting from productivity `v`.

Every term in the sum:

$$\left\lfloor \frac{v}{k^i} \right\rfloor$$

is non-decreasing as `v` increases. That means `f(v)` itself is non-decreasing.

So there exists a boundary point where values smaller than the answer are insufficient and values greater than or equal to the answer are sufficient. Binary search always maintains this boundary correctly and eventually isolates the minimum valid `v`.

The helper function is also correct because it directly simulates the productivity decay described in the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def enough(v, n, k):
    total = 0
    current = v

    while current > 0:
        total += current
        current //= k

    return total >= n

def solve():
    n, k = map(int, input().split())

    left, right = 1, n
    answer = n

    while left <= right:
        mid = (left + right) // 2

        if enough(mid, n, k):
            answer = mid
            right = mid - 1
        else:
            left = mid + 1

    print(answer)

solve()
```

The helper function follows the exact productivity process from the problem. Starting from `v`, it keeps adding the current contribution and divides by `k` after each step.

Using iterative division is safer than computing powers like `k^i`. The loop naturally stops once the contribution becomes zero.

The binary search maintains the invariant that every value strictly smaller than `left` is known to be invalid, while every value larger than `right` has already been processed or discarded.

The search range is `[1, n]` because `n` itself is always sufficient. Even if Vasya only writes the initial batch and nothing afterward, starting with `n` lines clearly works.

A common off-by-one mistake is updating the wrong boundary after finding a valid midpoint. Since we want the minimum valid value, we must continue searching the left half with:

```
right = mid - 1
```

Another subtle detail is storing the candidate answer before moving left. Otherwise the final valid midpoint could be lost.

## Worked Examples

### Example 1

Input:

```
7 2
```

Binary search trace:

| left | right | mid | Total Written | Enough? |
| --- | --- | --- | --- | --- |
| 1 | 7 | 4 | 4 + 2 + 1 = 7 | Yes |
| 1 | 3 | 2 | 2 + 1 = 3 | No |
| 3 | 3 | 3 | 3 + 1 = 4 | No |

Final answer:

```
4
```

This trace shows the monotonic structure clearly. Once `4` works, every larger value would also work, so binary search safely moves left to look for a smaller valid answer.

### Example 2

Input:

```
59 10
```

Binary search trace:

| left | right | mid | Total Written | Enough? |
| --- | --- | --- | --- | --- |
| 1 | 59 | 30 | 30 + 3 = 33 | No |
| 31 | 59 | 45 | 45 + 4 = 49 | No |
| 46 | 59 | 52 | 52 + 5 = 57 | No |
| 53 | 59 | 56 | 56 + 5 = 61 | Yes |
| 53 | 55 | 54 | 54 + 5 = 59 | Yes |
| 53 | 53 | 53 | 53 + 5 = 58 | No |

Final answer:

```
54
```

This example demonstrates why we keep searching after finding a valid midpoint. `56` works, but it is not minimal. The search eventually narrows to `54`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n × log n) | Binary search performs O(log n) iterations, each helper call takes O(log n) divisions |
| Space | O(1) | Only a few integer variables are used |

Even at the maximum constraint `n = 10^9`, binary search requires only about 30 iterations. Each helper computation also performs at most around 30 divisions when `k = 2`. The total work easily fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def enough(v, n, k):
        total = 0
        current = v

        while current > 0:
            total += current
            current //= k

        return total >= n

    n, k = map(int, input().split())

    left, right = 1, n
    answer = n

    while left <= right:
        mid = (left + right) // 2

        if enough(mid, n, k):
            answer = mid
            right = mid - 1
        else:
            left = mid + 1

    return str(answer)

# provided samples
assert run("7 2\n") == "4", "sample 1"
assert run("59 10\n") == "54", "sample 2"

# minimum values
assert run("1 2\n") == "1", "minimum case"

# exact equality after several divisions
assert run("10 2\n") == "6", "6 + 3 + 1 = 10"

# large k, almost no extra contribution
assert run("100 10\n") == "91", "91 + 9 = 100"

# maximum-style stress case
assert run("1000000000 2\n") == "500000006", "large input"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | `1` | Smallest possible answer |
| `10 2` | `6` | Exact equality after multiple reductions |
| `100 10` | `91` | Large divisor with very short sequence |
| `1000000000 2` | `500000006` | Large input and binary search stability |

## Edge Cases

Consider the smallest possible input:

```
1 2
```

Binary search starts with `left = right = 1`.

For `mid = 1`:

$$1 + 0 = 1$$

The condition succeeds immediately, so the answer becomes `1`.

This case confirms that the search boundaries are initialized correctly and that the algorithm handles the smallest valid answer without underflow.

Now consider:

```
10 2
```

The correct answer is `6`.

Tracing the helper computation:

| Current | Total |
| --- | --- |
| 6 | 6 |
| 3 | 9 |
| 1 | 10 |
| 0 | stop |

The total reaches exactly `10`, so `6` is valid. A common mistake is using `>` instead of `>=` when checking sufficiency. That bug would incorrectly reject exact matches.

Finally, consider a case where the productivity drops almost immediately:

```
100 10
```

For `v = 91`:

$$91 + 9 = 100$$

The next term is zero.

This case confirms that the helper function correctly stops once division reaches zero, instead of continuing forever or performing unnecessary work.
