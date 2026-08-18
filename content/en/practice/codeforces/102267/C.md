---
title: "CF 102267C - Matryoshka Dolls"
description: "We have a largest Matryoshka doll of integer size S. If one doll is placed inside another, the inner doll must be at most 1/X of the outer doll's size."
date: "2026-08-19T03:14:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102267
codeforces_index: "C"
codeforces_contest_name: "The 2019 University of Jordan Collegiate Programming Contest"
rating: 0
weight: 102267
solve_time_s: 350
verified: false
draft: false
---

[CF 102267C - Matryoshka Dolls](https://codeforces.com/problemset/problem/102267/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We have a largest Matryoshka doll of integer size `S`. If one doll is placed inside another, the inner doll must be at most `1/X` of the outer doll's size. We want the longest possible nesting chain, so the question is how many dolls can appear from the original size `S` down to the smallest positive integer size.

Suppose the current doll has size `A`. The largest possible size for the next doll is `floor(A / X)`. Choosing anything smaller can never help, because a larger next doll leaves at least as much room for every later doll. Repeating this choice gives the longest possible chain.

The constraints are small enough for logarithmic arithmetic to be the natural target. Since `X >= 2`, every nesting step reduces the size by at least a factor of two. Starting from at most `10^9`, there can be fewer than 31 reductions before the size becomes zero. A linear scan over all sizes up to `10^9` would be far too expensive for a one second limit, while an `O(log S)` solution performs only a few dozen iterations.

There are several boundary cases where an implementation can make an off-by-one error. For `S = 1, X = 2`, the answer is `1`, because the original doll itself counts, but no positive integer size can fit inside it. A careless loop that only counts successful divisions could output `0`.

For `S = 10, X = 2`, the optimal chain is `10 -> 5 -> 2 -> 1`, giving `4`. An implementation that uses ordinary division without taking the floor explicitly is safe in Python because integer division already floors, but using floating-point division and converting later can introduce unnecessary precision risks.

For `S = 9, X = 2`, the chain is `9 -> 4 -> 2 -> 1`, again giving `4`. The second size is `4`, not `4.5`, because doll sizes must be integers. Any approach that treats the sizes as real numbers can produce an incorrect chain length.

When `S = X = 10^9`, the chain is `10^9 -> 1`, so the answer is `2`. A common mistake is to require the next doll to have size strictly smaller than `S / X`, but the condition allows equality, so size `1` is valid.

## Approaches

A direct brute-force method could search through every possible integer size for the next doll. For a current size `A`, it could inspect all candidates from `1` through `floor(A / X)` and determine which one is largest and valid. This is correct because every possible choice for the next doll is examined, and taking the largest valid choice produces the best continuation.

The problem is the amount of unnecessary work. With `S = 10^9` and `X = 2`, such a search examines roughly

`floor(10^9 / 2) + floor(10^9 / 4) + floor(10^9 / 8) + ...`

candidates over the whole chain. This sum is `10^9 - popcount(10^9) = 999,999,987`, so the worst case is essentially one billion iterations. That cannot fit comfortably within a one second limit.

The brute-force method works because it is searching a space where the best next size is obvious once all candidates have been considered. The key observation is that we do not actually need to search that space. For a current size `A`, every valid next size is at most `floor(A / X)`, and choosing exactly that maximum gives the largest possible starting point for the remaining dolls. The problem therefore reduces to repeatedly applying integer division by `X`.

Starting with `S`, we count the current doll, replace its size by `S // X`, and continue while the new size is positive. Since `X` is at least `2`, the number of iterations is logarithmic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(S)` in the worst case | `O(1)` | Too slow |
| Optimal | `O(log_X S)` | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Read `S` and `X`. The current doll size is initially `S`, and the answer starts at `1` because the largest doll itself is already part of the nesting chain.
2. While the current size is at least `X`, replace it with `current // X` and increment the answer.

Dividing only while `current >= X` is equivalent to checking whether another positive integer doll can fit inside. If `current < X`, then `floor(current / X) = 0`, and size `0` is not a doll, so the chain must stop.
3. Print the accumulated answer.

The correctness follows from the invariant that before every iteration, `current` is the largest possible size of the doll at that depth among all optimal chains. From a doll of size `current`, no valid inner doll can exceed `floor(current / X)`, and that exact size is valid whenever it is positive. Choosing the maximum possible next size cannot reduce the maximum achievable number of later dolls, because every later constraint is monotonic with respect to the current size. Thus every division produces the best possible next doll, and the loop stops exactly when no positive inner doll exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    S, X = map(int, input().split())

    ans = 1
    while S >= X:
        S //= X
        ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The variable `ans` starts at `1` because the original doll is counted even when no smaller doll can be placed inside it. This handles `S = 1` correctly.

The condition `S >= X` is the clean boundary check. If it holds, `S // X` is at least `1`, so another positive-sized doll exists. If it does not hold, the quotient would be zero and nesting must stop.

The update uses integer division directly. Since the sizes are integers, `S // X` is exactly the largest valid integer size for the next doll. No floating-point arithmetic is necessary.

Python integers also remove any overflow concern, although the input values are already small enough that 32-bit signed integers would be sufficient for the stored values.

The input contains only one test case, so there is no outer test-case loop. The required `sys.stdin.readline` setup is still used for fast and conventional competitive-programming input.

## Worked Examples

### Sample 1: `S = 10, X = 2`

The current doll can repeatedly be replaced by the largest integer size that fits inside it.

| Step | Current size | New size | Answer |
| --- | --- | --- | --- |
| Start | 10 | 5 | 2 |
| 2 | 5 | 2 | 3 |
| 3 | 2 | 1 | 4 |
| Stop | 1 | Not possible | 4 |

The resulting chain is `10 -> 5 -> 2 -> 1`. When the current size reaches `1`, it is smaller than `X = 2`, so another positive integer doll cannot fit. The answer is `4`.

### Custom Example: `S = 9, X = 2`

| Step | Current size | New size | Answer |
| --- | --- | --- | --- |
| Start | 9 | 4 | 2 |
| 2 | 4 | 2 | 3 |
| 3 | 2 | 1 | 4 |
| Stop | 1 | Not possible | 4 |

This example exercises the integer boundary. The first inner doll has size `9 // 2 = 4`, not `5`, because the requirement is `2 * inner <= outer`. The chain is `9 -> 4 -> 2 -> 1`, giving `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(log_X S)` | Every iteration divides the current size by `X`, and `X >= 2`. |
| Space | `O(1)` | Only the current size, divisor, and answer are stored. |

With `S <= 10^9` and `X >= 2`, there are at most 30 divisions before the value reaches `1`. The algorithm therefore performs only a few dozen iterations even in the worst case, easily fitting within the one second time limit and using negligible memory.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.split()
    S, X = map(int, data)

    ans = 1
    while S >= X:
        S //= X
        ans += 1

    return str(ans)

def run(inp: str) -> str:
    return solve_data(inp).strip()

# Provided sample
assert run("10 2\n") == "4", "sample 1"

# Minimum possible S
assert run("1 2\n") == "1", "minimum size"

# Exact powers of X
assert run("8 2\n") == "4", "exact divisibility"

# Non-divisible boundary, catches incorrect rounding
assert run("9 2\n") == "4", "floor division boundary"

# Equal maximum values
assert run("1000000000 1000000000\n") == "2", "maximum equal values"

# Maximum S with minimum X
assert run("1000000000 2\n") == "30", "maximum chain length"

# X larger than S
assert run("5 10\n") == "1", "no inner doll"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | `1` | Minimum size and the fact that the original doll counts |
| `8 2` | `4` | Exact powers and equality at every division boundary |
| `9 2` | `4` | Integer floor division rather than real-number division |
| `1000000000 1000000000` | `2` | Maximum values and the allowed equality boundary |
| `1000000000 2` | `30` | Maximum number of iterations under the constraints |
| `5 10` | `1` | Case where no inner doll can be placed |

## Edge Cases

For `S = 1, X = 2`, the algorithm starts with `ans = 1` and `S = 1`. The condition `1 >= 2` is false, so the loop does not execute and the output is `1`. This prevents the common mistake of counting only inner dolls rather than counting the original largest doll.

For `S = 9, X = 2`, the first update is `9 // 2 = 4`. The following updates are `4 // 2 = 2` and `2 // 2 = 1`. The algorithm stops at `1` and returns `4`. This demonstrates why the quotient must be taken as an integer, since a hypothetical real-valued chain involving `4.5` is not allowed.

For `S = X = 10^9`, the initial condition `10^9 >= 10^9` is true, so the algorithm accepts an inner doll of size `10^9 // 10^9 = 1` and increments the answer to `2`. The next condition fails because `1 < 10^9`. The output is consequently `2`, confirming that the boundary condition permits an inner doll exactly equal to `S / X`.

For `S = 5, X = 10`, the initial condition `5 >= 10` is false. The algorithm immediately returns `1`, which is correct because any positive inner integer size would have to be at most `floor(5 / 10) = 0`.

For the largest possible chain, `S = 10^9, X = 2`, the algorithm performs 29 successful divisions before reaching `1`, so the original doll plus those 29 inner dolls gives `30`. Even this extreme case requires only logarithmically many operations, which is the central reason the solution comfortably meets the constraints.
