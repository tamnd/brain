---
title: "CF 102875J - Just Multiplicative Inverse"
description: "The function in this problem is a recursive way to compute a modular inverse, but the requested value is not the inverse itself."
date: "2026-07-25T13:01:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102875
codeforces_index: "J"
codeforces_contest_name: "2020 Jiangsu Collegiate Programming Contest"
rating: 0
weight: 102875
solve_time_s: 69
verified: true
draft: false
---

[CF 102875J - Just Multiplicative Inverse](https://codeforces.com/problemset/problem/102875/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

The function in this problem is a recursive way to compute a modular inverse, but the requested value is not the inverse itself. The question asks for the average number of function calls when the function is started with every possible starting value from `1` to `p - 1`, where `p` is a prime number.

The recursive function stops immediately when its argument becomes `1`. Otherwise, it moves from the current value `x` to `p mod x` and makes one more call. The multiplication and modulo operations used to build the inverse are irrelevant here because only the number of calls matters. For example, when `p = 7`, the chain for `x = 5` is `5 -> 2 -> 1`, so it contributes `3` calls to the average.

The input contains up to 100 prime values, and every prime is at most `10^6`. This bound is the main algorithmic clue. A solution that tries to follow every recursive chain independently can repeat the same subproblems many times, and a direct simulation of every chain would approach quadratic behavior. For a value around `10^6`, a quadratic method would require around `10^12` operations, which is far beyond what a normal time limit allows. We need to exploit the fact that every state depends only on a smaller remainder.

The subtle cases are mostly around the boundaries. When `p = 2`, there is only one possible starting value, `x = 1`. The answer is `1`, and an implementation that assumes the loop always contains values from `2` to `p - 1` can accidentally divide by zero because the number of starting values is `p - 1`.

For input:

```
1
2
```

the correct output is:

```
1.0000000000
```

There is no recursive transition because the only call is `F(1, 2)`.

Another easy mistake is treating the returned modular value as the answer. For example, with `p = 7` and `x = 5`, the function returns the modular inverse value, but the contribution is the number of calls:

```
F(5, 7) -> F(2, 7) -> F(1, 7)
```

The contribution is `3`, not the inverse of `5` modulo `7`.

## Approaches

A straightforward approach is to simulate the recursive function for every possible starting value. For each `x` from `1` to `p - 1`, we repeatedly replace `x` with `p mod x` until reaching `1`, counting the number of calls. This gives the correct result because the recursion exactly describes the process we need to measure.

The problem is that many different starting values visit the same intermediate values. If we compute every chain separately, the same remainder can be evaluated again and again. In the worst case, doing this independently for all starting values can become quadratic. With `p` close to `10^6`, that would mean about one trillion transitions.

The key observation is that the dependency graph is already ordered. For any `x > 1`, the next value is `p mod x`, and this value is always smaller than `x`. That means if we calculate answers in increasing order of `x`, the answer for every transition is already known.

Let `dp[x]` be the number of calls made by the function starting at `x`. The base case is `dp[1] = 1`. For every other value:

$$dp[x] = 1 + dp[p \bmod x]$$

The extra `1` represents the current call, and the remaining calls are exactly the calls from the recursive child.

The final answer is the average of all `dp[x]` values from `1` to `p - 1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(p²) | O(1) | Too slow |
| Optimal | O(p) | O(p) | Accepted |

## Algorithm Walkthrough

1. Create an array `dp` where `dp[x]` stores the number of calls needed when the function starts from `x`. Set `dp[1] = 1` because the function returns immediately for this state. This gives us the only stopping condition directly.
2. Iterate through `x` from `2` to `p - 1`. For each value, calculate the next recursive state `p mod x`. Since this value is smaller than `x`, its answer has already been computed.
3. Set `dp[x] = 1 + dp[p mod x]`. The current call contributes one, and the rest of the chain is already stored in the dynamic programming table.
4. Add every `dp[x]` value and divide the total by `p - 1`. Every starting value from `1` to `p - 1` has equal probability, so the required expectation is the arithmetic mean.

Why it works: the important invariant is that after processing every value up to `x`, `dp[i]` is correct for every `i <= x`. The recursive transition from `x` always moves to a smaller number, so the needed subproblem is already covered by the invariant. Because every possible starting value is included exactly once in the final sum, the computed average matches the expected number of calls.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(p):
    if p == 2:
        return 1.0

    dp = [0] * p
    dp[1] = 1

    total = 1
    for x in range(2, p):
        dp[x] = 1 + dp[p % x]
        total += dp[x]

    return total / (p - 1)

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        p = int(input())
        ans.append(f"{solve_case(p):.10f}")
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The special case `p = 2` avoids creating an invalid average calculation. There is only one possible starting value, so the answer is directly `1`.

For larger primes, `dp` has size `p` because every possible starting value is smaller than `p`. The increasing loop order is the central implementation detail. When calculating `dp[x]`, the index `p % x` is guaranteed to be smaller than `x`, so no recursion or additional ordering is required.

The variable `total` is kept as an integer while building the sum. The conversion to floating point happens only during the final division, which avoids unnecessary precision loss during accumulation.

## Worked Examples

For `p = 7`, the computed values are:

| x | p mod x | dp[x] | Running sum |
| --- | --- | --- | --- |
| 1 | - | 1 | 1 |
| 2 | 1 | 2 | 3 |
| 3 | 1 | 2 | 5 |
| 4 | 3 | 3 | 8 |
| 5 | 2 | 3 | 11 |
| 6 | 1 | 2 | 13 |

The average is:

$$13 / 6 = 2.1666666667$$

This example shows how repeated subproblems are reused. The chains for `4` and `5` do not need to independently recompute the paths through `3` and `2`.

For `p = 5`:

| x | p mod x | dp[x] | Running sum |
| --- | --- | --- | --- |
| 1 | - | 1 | 1 |
| 2 | 1 | 2 | 3 |
| 3 | 2 | 3 | 6 |
| 4 | 1 | 2 | 8 |

The final result is:

$$8 / 4 = 2.0$$

This case demonstrates that a state can depend on another non-immediate previous value. `dp[3]` depends on `dp[2]`, which was already available because the iteration follows increasing order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(p) | Every value from `1` to `p - 1` is processed once. |
| Space | O(p) | The dynamic programming array stores one value for every possible state. |

The largest possible prime is `10^6`, so the algorithm performs about one million simple operations per test case. This fits comfortably because the repeated work from recursive simulations has been removed.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve_case(p):
        if p == 2:
            return 1.0
        dp = [0] * p
        dp[1] = 1
        total = 1
        for x in range(2, p):
            dp[x] = 1 + dp[p % x]
            total += dp[x]
        return total / (p - 1)

    t = int(input())
    out = []
    for _ in range(t):
        out.append(f"{solve_case(int(input())):.10f}")
    return "\n".join(out)

assert solution("""5
2
3
5
7
999983
""") == """1.0000000000
1.5000000000
2.0000000000
2.1666666667
15.9864347558""", "samples"

assert solution("""1
2
""") == "1.0000000000", "minimum prime"

assert solution("""1
3
""") == "1.5000000000", "small recursive case"

assert solution("""1
5
""") == "2.0000000000", "small chain reuse"

assert solution("""1
7
""") == "2.1666666667", "branching chains"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | `1.0000000000` | Handles the smallest possible prime and avoids division mistakes. |
| `3` | `1.5000000000` | Checks the first non-trivial recursive transitions. |
| `5` | `2.0000000000` | Validates dependency ordering in the DP array. |
| `7` | `2.1666666667` | Exercises multiple chains sharing intermediate states. |

## Edge Cases

For `p = 2`, the algorithm immediately returns `1.0`. The loop from `2` to `p - 1` is empty, but this is correct because the only starting point is `x = 1`.

For input:

```
1
2
```

the execution is:

| Step | State |
| --- | --- |
| Start | Only value is `x = 1` |
| Function calls | One call |
| Average | `1 / 1 = 1` |

For cases where a starting value reaches another computed state, the DP ordering handles it naturally. With `p = 7`, when calculating `dp[5]`, the transition is:

```
5 -> 2
```

The value `dp[2]` is already known:

```
dp[2] = 1 + dp[1] = 2
```

so:

```
dp[5] = 1 + dp[2] = 3
```

The algorithm never recomputes the chain `2 -> 1`, which is the main reason the linear solution works.
