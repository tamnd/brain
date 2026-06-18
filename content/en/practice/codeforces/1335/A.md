---
problem: 1335A
contest_id: 1335
problem_index: A
name: "Candies and Two Sisters"
contest_name: "Codeforces Round 634 (Div. 3)"
rating: 800
tags: ["math"]
answer: passed_samples
verified: true
solve_time_s: 284
date: 2026-06-14
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e0db5-5080-83ec-a350-4bcdb1d55f19
---

# CF 1335A - Candies and Two Sisters

**Rating:** 800  
**Tags:** math  
**Model:** gpt-5-5  
**Solve time:** 4m 44s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e0db5-5080-83ec-a350-4bcdb1d55f19  

---

## Solution

## Problem Understanding

We are splitting a pile of identical candies into two positive parts. Each test case gives a number `n`, and we want to count how many different ordered pairs `(a, b)` exist such that both `a` and `b` are positive integers, they sum to `n`, and the first part is strictly larger than the second.

Although the candies are indistinguishable, the order matters because Alice and Betty are different people, and the constraint `a > b` removes symmetric duplicates automatically.

From a constraints perspective, the number of test cases can be as large as 10,000, and each `n` can be up to 2×10^9. That immediately rules out any solution that tries to enumerate all pairs `(a, b)` up to `n`, since that would be linear per test case and far too slow. The intended solution must compute the answer in constant time per test case.

A subtle failure case for naive reasoning comes from forgetting the strict inequality. For example, when `n = 4`, valid splits are `(3,1)` only. The pair `(2,2)` is invalid even though it sums correctly, and missing that condition would overcount. Another common mistake is treating `(a, b)` and `(b, a)` as two valid choices, which would double count and break the ordering condition entirely.

## Approaches

A brute-force strategy would try every possible value of `a` from `1` to `n - 1`, compute `b = n - a`, and count it if `a > b`. This is correct, but it checks roughly `n` candidates per test case, which becomes about 2×10^9 operations in the worst case for a single input, and up to 10^13 operations overall. That is completely infeasible.

The key observation is that once `a + b = n`, choosing `a` automatically fixes `b`, so the problem reduces to counting how many integers `a` satisfy both `a > n - a` and `a > 0`. The inequality simplifies to `2a > n`, so `a > n/2`.

At the same time, we must also ensure `b = n - a > 0`, which implies `a < n`. So valid values of `a` are integers strictly greater than `n/2` and strictly less than `n`.

This turns the problem into counting integers in a contiguous interval, which can be computed directly with arithmetic rather than iteration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per test case | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Observe that any valid distribution is fully determined by choosing `a`, since `b = n - a`. This reduces the problem to counting valid values of `a`.
2. Translate the constraint `a > b` into an inequality using substitution: `a > n - a`.
3. Rearrange the inequality to isolate `a`, giving `2a > n`, which implies `a > n/2`.
4. Combine this with positivity constraints. Since `b > 0`, we must have `a < n`, and since `a > 0` is already guaranteed by `a > n/2` for `n ≥ 1`, the effective range is `a ∈ (n/2, n)`.
5. Count integers in this range. The smallest valid integer is `floor(n/2) + 1`, and the largest is `n - 1`. The count is therefore `(n - 1) - (floor(n/2) + 1) + 1`, which simplifies to `n//2 - 1 + 1 = (n - 1) // 2`.
6. Return this value for each test case.

### Why it works

Every valid split corresponds to exactly one integer `a` in the range `(n/2, n)`, and every such integer produces a valid `b = n - a` that is positive and strictly smaller than `a`. The mapping between valid splits and valid `a` values is one-to-one, so counting valid `a` values is equivalent to counting valid distributions. No invalid pair is included because the inequality ensures both positivity and strict ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    print((n - 1) // 2)
```

The solution reads each test case and applies the derived formula directly. The expression `(n - 1) // 2` captures exactly the number of integers strictly greater than `n/2` and less than `n`. Integer division ensures correct flooring behavior without floating-point operations.

A common pitfall would be using `n // 2` instead, which is off by one for even values of `n`, since it incorrectly includes the midpoint case where `a = b`.

## Worked Examples

### Example 1

Input:

```
n = 7
```

Valid `a` values are those strictly greater than 3.5 and less than 7, so `a ∈ {4, 5, 6}`.

| Step | Expression | Value |
| --- | --- | --- |
| n | input | 7 |
| lower bound | floor(n/2)+1 | 4 |
| upper bound | n-1 | 6 |
| count | 6 - 4 + 1 | 3 |

This confirms 3 valid splits: `(6,1), (5,2), (4,3)`.

### Example 2

Input:

```
n = 6
```

Valid `a` values satisfy `a > 3` and `a < 6`, so `a ∈ {4, 5}`.

| Step | Expression | Value |
| --- | --- | --- |
| n | input | 6 |
| lower bound | floor(n/2)+1 | 4 |
| upper bound | n-1 | 5 |
| count | 5 - 4 + 1 | 2 |

This matches the two valid splits `(5,1)` and `(4,2)`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed in constant time using a closed-form formula |
| Space | O(1) | No auxiliary structures are used |

The solution easily fits within constraints since even for 10,000 test cases, the work is just simple arithmetic operations.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        print((n - 1) // 2)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.strip()

# provided samples
assert run("6\n7\n1\n2\n3\n2000000000\n763243547\n") == "3\n0\n0\n1\n999999999\n381621773"

# custom cases
assert run("1\n1\n") == "0", "minimum edge"
assert run("1\n2\n") == "0", "smallest even"
assert run("1\n4\n") == "1", "first non-trivial even"
assert run("1\n5\n") == "2", "odd case check"
assert run("1\n8\n") == "3", "larger even case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | smallest invalid case |
| 2 | 0 | smallest even edge |
| 4 | 1 | first valid split appears |
| 5 | 2 | odd behavior correctness |
| 8 | 3 | growth pattern correctness |

## Edge Cases

For `n = 1`, there is no way to split into two positive parts, since the minimum sum of two positive integers is 2. The formula gives `(1 - 1) // 2 = 0`, which matches the empty set of valid pairs.

For `n = 2`, the only possible split is `(1,1)`, but it violates `a > b`, so the correct answer is 0. The formula gives `(2 - 1) // 2 = 0`, correctly excluding the symmetric midpoint case.

For even `n`, such as `n = 10`, the pair `(5,5)` is not allowed, so the count only includes values strictly above half. The formula naturally excludes the midpoint because of the strict inequality embedded in the derivation.

For large `n` like `2 × 10^9`, no overflow issues arise in Python, and the computation remains a single integer operation per test case, preserving correctness and efficiency.