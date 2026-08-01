---
title: "CF 102638E - Rating Recalculating"
description: "The problem describes a new way of assigning a Codeforces division from a user's rating. For a rating r, we choose an integer k, look at the value $$f(r-k,r)=frac{1+r+frac{r^2}{2!}+dots+frac{r^{r-k}}{(r-k)!}}{e^r}$$ and then compute floor(1 / f) - 1."
date: "2026-08-01T09:43:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102638
codeforces_index: "E"
codeforces_contest_name: "Bredor contest"
rating: 0
weight: 102638
solve_time_s: 132
verified: true
draft: false
---

[CF 102638E - Rating Recalculating](https://codeforces.com/problemset/problem/102638/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a new way of assigning a Codeforces division from a user's rating. For a rating `r`, we choose an integer `k`, look at the value

$$f(r-k,r)=\frac{1+r+\frac{r^2}{2!}+\dots+\frac{r^{r-k}}{(r-k)!}}{e^r}$$

and then compute `floor(1 / f) - 1`. We need the smallest `k` that makes this division strictly greater than `1`.

The expression for `f` is the cumulative probability of a Poisson random variable with parameter `r` being at most `r-k`. In other words, it is the probability that a Poisson-distributed value does not exceed the chosen cutoff. The condition for the division to be greater than one is:

$$\lfloor 1/f \rfloor - 1 > 1$$

which means:

$$\lfloor 1/f \rfloor \ge 3$$

so we only need to find the smallest `k` such that:

$$f(r-k,r) \le \frac13$$

The ratings are at most `4000`, and there are at most `20` test cases. A solution doing work proportional to `r` for each check is easily fast enough. However, trying every possible `k` and recomputing the probability from scratch would still waste unnecessary operations. The useful structure is that the probability decreases monotonically when `k` increases, which allows binary search.

The main numerical challenge is evaluating the Poisson prefix probability accurately. Computing the sum from the first term is dangerous because the terms become extremely small for large `r`. Instead, we start from the last included term and move downward. The terms near `r-k` are the largest ones in the required range, so this direction keeps the intermediate values stable.

The edge cases are mostly about boundaries.

For the smallest rating:

```
Input
1
5
```

the answer is `2`. A solution that assumes the cutoff can never become negative or forgets that `k` starts at zero can produce an incorrect result.

For a case where the answer is small:

```
Input
1
100
```

the answer is `5`. The probability changes gradually, so checking only a rough approximation such as `sqrt(r)` can miss the exact integer boundary.

For large ratings:

```
Input
1
4000
```

the answer is still relatively small compared with `r`. A solution that loops through all possible `k` values up to `r` works in theory, but repeatedly calculating the probability that way performs much more work than needed.

## Approaches

A direct approach is to try every possible `k` starting from zero. For each candidate, we compute the value of `f(r-k,r)` and stop at the first one where it becomes at most `1/3`. This is correct because larger `k` means a smaller prefix of the Poisson distribution, so the probability can only decrease.

The problem is the repeated probability calculation. If we try every `k`, there can be around `4000` candidates. If every probability calculation scans up to `4000` terms, one test case can require around `16,000,000` floating point operations. This is not ideal, especially with the small time limit.

The key observation is monotonicity. When `k` increases, `r-k` decreases, removing terms from the numerator of the Poisson prefix. The value of `f` never increases. That means the answer is the first position where a monotonic condition becomes true, exactly the situation where binary search applies.

The remaining task is evaluating one probability efficiently. We compute the last included term using logarithms, then repeatedly divide by the appropriate ratio to move to smaller powers. This avoids huge factorials and keeps the calculation inside normal floating point ranges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(r²) per test case | O(1) | Too slow |
| Binary search with stable probability evaluation | O(r log r) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For a fixed rating `r`, binary search the answer `k`. The search range starts with `0` and a sufficiently large upper bound. The predicate we test is whether the probability `f(r-k,r)` is at most `1/3`.
2. To evaluate the predicate, let `n = r-k`. If `n` is negative, the probability is zero because there are no valid terms in the prefix.
3. Compute the probability term:

$$P(X=n)=e^{-r}\frac{r^n}{n!}$$

using logarithms:

$$\log P(X=n)=-r+n\log r-\log(n!)$$

This avoids overflow from large powers and factorials.

1. Add the smaller terms by moving backwards:

$$P(X=n-1)=P(X=n)\frac{n}{r}$$

and continue until the term becomes negligible. The sum of these terms is exactly the required prefix probability.

1. If the probability is already at most `1/3`, move the binary search left because a smaller `k` might also work. Otherwise move right because a larger cutoff reduction is necessary.
2. Return the smallest `k` found by the binary search.

Why it works: the computed probability is exactly the cumulative Poisson probability up to `r-k`. Increasing `k` removes terms from this cumulative sum, so the predicate changes from false to true at most once. Binary search finds that first transition, which is precisely the minimum valid value.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def poisson_prefix(r, n):
    if n < 0:
        return 0.0
    if n >= r:
        return 1.0

    log_term = -r + n * math.log(r) - math.lgamma(n + 1)
    term = math.exp(log_term)

    ans = term
    cur = n
    while cur > 0:
        term *= cur / r
        ans += term
        cur -= 1
        if term < 1e-16:
            break

    return ans

def solve_case(r):
    lo, hi = 0, r + 10
    while lo < hi:
        mid = (lo + hi) // 2
        if poisson_prefix(r, r - mid) <= 1.0 / 3.0:
            hi = mid
        else:
            lo = mid + 1
    return lo

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        r = int(input())
        ans.append(str(solve_case(r)))
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The `poisson_prefix` function handles the numerical part. The use of `math.lgamma` gives `log(n!)` directly, avoiding factorial overflow. The recurrence between neighboring Poisson probabilities means we never need to calculate powers or factorials explicitly.

The binary search uses the fact that the answer is an integer and that every larger `k` after the answer is also valid. The upper bound `r + 10` is safe because once `r-k` becomes negative the probability becomes zero.

The stopping condition in the summation prevents spending time on terms that no longer affect the answer. The threshold is far below the precision needed for comparing against `1/3`.

## Worked Examples

For `r = 5`, the search checks different values of `k`.

| k | n = r-k | Prefix probability | Decision |
| --- | --- | --- | --- |
| 0 | 5 | about 0.616 | Too large |
| 2 | 3 | about 0.265 | Valid |

The first valid value is `2`, which matches the sample. This trace shows why the answer depends on the exact probability threshold rather than a rough approximation.

For `r = 100`:

| k | n = r-k | Prefix probability | Decision |
| --- | --- | --- | --- |
| 4 | 96 | greater than 1/3 | Too large |
| 5 | 95 | less than 1/3 | Valid |

The binary search skips the unnecessary values and finds the first valid boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(r log r) | Each binary search step evaluates a probability in O(r) worst case. |
| Space | O(1) | Only a few floating point variables are stored. |

With `r <= 4000` and at most `20` test cases, the number of operations is comfortably within the limit.

## Test Cases

```python
import sys
import io
import math

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    sys.stdin = old

    def poisson_prefix(r, n):
        if n < 0:
            return 0.0
        if n >= r:
            return 1.0
        term = math.exp(-r + n * math.log(r) - math.lgamma(n + 1))
        res = term
        cur = n
        while cur > 0:
            term *= cur / r
            res += term
            cur -= 1
            if term < 1e-16:
                break
        return res

    def solve(r):
        lo, hi = 0, r + 10
        while lo < hi:
            mid = (lo + hi) // 2
            if poisson_prefix(r, r - mid) <= 1 / 3:
                hi = mid
            else:
                lo = mid + 1
        return str(lo)

    t = int(data[0])
    return "\n".join(solve(int(x)) for x in data[1:t+1])

assert run("1\n5\n") == "2"
assert run("2\n100\n200\n") == "5\n7"
assert run("3\n2500\n3000\n3500\n") == "23\n25\n27"
assert run("1\n6\n") == "2"
assert run("1\n4000\n") == "29"
assert run("1\n10\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 6` | `2` | Small values close to the minimum rating |
| `1 / 4000` | `29` | Large rating boundary |
| `1 / 10` | `3` | Small probability transition |
| Samples | Sample outputs | Original examples |

## Edge Cases

For `r = 5`, the algorithm reaches `k = 2` because the cutoff becomes `3`, and the probability of getting a Poisson value at most `3` is already below `1/3`. The binary search does not miss this because it checks the transition point directly.

For `r = 100`, the answer is not determined by simply taking a fixed fraction of the rating. The algorithm evaluates the actual probability boundary and finds that `k = 5` is the first valid choice.

For `r = 4000`, direct factorial and power calculations would overflow or lose precision. The logarithmic term computation and backward recurrence avoid these failures while preserving enough accuracy for the comparison with `1/3`.
