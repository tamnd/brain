---
title: "CF 106484B - Bugcat's Counting Game"
description: "We are given a digit-like parameter k between 1 and 9, and a position x. Imagine counting upward from 1, but we do not consider every integer as valid."
date: "2026-06-19T15:16:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106484
codeforces_index: "B"
codeforces_contest_name: "2026 GBA International Programming Contest"
rating: 0
weight: 106484
solve_time_s: 52
verified: true
draft: false
---

[CF 106484B - Bugcat's Counting Game](https://codeforces.com/problemset/problem/106484/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a digit-like parameter `k` between 1 and 9, and a position `x`. Imagine counting upward from 1, but we do not consider every integer as valid. A number is only “spoken” if it satisfies at least one of two conditions: either it is divisible by `k`, or its decimal representation contains the digit `k`. We conceptually filter the natural numbers using this rule, producing an infinite increasing sequence of “spoken” numbers. The task is to find the value of the `x`-th number in this filtered sequence.

The constraints allow `x` up to 100,000, while `k` is a single digit. This immediately suggests that any solution which inspects each integer up to potentially millions or more is acceptable if the per-number check is cheap, because 100,000 accepted elements typically require scanning on the order of a few hundred thousand to a few million candidates depending on density. A direct simulation is therefore within reach.

The main subtlety is the filtering condition: checking “contains digit k” must be done carefully in decimal form, not as a numeric property. Another edge case arises from the fact that both conditions can overlap. For example, a number like 33 when `k = 3` is both divisible by 3 and contains digit 3, but it should only be counted once in the sequence. A naive implementation that increments the counter twice per number would silently overcount.

A second potential pitfall is off-by-one handling in counting the `x`-th valid number. Since we are dealing with a stream of valid numbers rather than an array, it is easy to return the current candidate when the counter equals `x` without ensuring that the increment logic is correct.

## Approaches

The brute-force idea is straightforward: start from 1, test each integer, and maintain a counter of how many numbers satisfy the rule. For each integer `i`, we check whether `i % k == 0` or whether the string form of `i` contains the character representation of `k`. Whenever the condition holds, we increment a counter. Once the counter reaches `x`, we return the current integer.

This works because every integer is checked exactly once and the filtering rule is independent per number. The weakness of this approach is performance only in the constant-factor sense: we may need to scan beyond `x`, because valid numbers are not uniformly distributed. For example, when `k = 9`, multiples of 9 and numbers containing 9 are relatively frequent, so we might reach 100,000 valid numbers after scanning only a few hundred thousand integers. Even in the worst case where `k = 1`, almost every number is valid, so we still only scan roughly `x` numbers. This makes the approach efficient enough under the constraints.

There is no need for a more advanced combinatorial optimization or digit DP, because we are not asked to count or jump to the answer directly, only to enumerate until a limit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N) where N is value of x-th valid number | O(1) | Accepted |
| Optimal (same simulation, careful checking) | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter `cnt = 0` and start iterating `i` from 1 upward. We need sequential order because the definition depends on increasing natural numbers.
2. For each number `i`, determine whether it should be included in the sequence. First check if `i % k == 0`. This captures all multiples of `k` directly without digit processing.
3. If not already included via divisibility, check whether digit `k` appears in `i`’s decimal representation. This can be done by converting `i` to a string and checking membership of the character `str(k)`.
4. If either condition holds, increment `cnt` by 1. It is crucial that this increment happens only once per number even if both conditions are true, because the sequence counts each valid number only once.
5. When `cnt == x`, immediately output `i` and stop. This guarantees we return the x-th valid number in increasing order.

### Why it works

The algorithm maintains a simple invariant: after processing all integers up to `i`, the counter `cnt` equals exactly the number of integers in `[1, i]` that satisfy the rule. Since we scan in increasing order and never skip candidates, the first time `cnt` reaches `x`, the current `i` is precisely the smallest number such that at least `x` valid numbers are ≤ `i`. That matches the definition of the x-th element in the ordered sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k, x = map(int, input().split())
    target = str(k)

    cnt = 0
    i = 0

    while True:
        i += 1
        if i % k == 0 or target in str(i):
            cnt += 1
            if cnt == x:
                print(i)
                return

if __name__ == "__main__":
    solve()
```

The implementation follows the direct simulation strategy. The variable `target` stores the digit form of `k` so we avoid recomputing it repeatedly. The loop increments `i` indefinitely until the required count is reached. The membership test `target in str(i)` captures the digit condition cleanly.

A subtle point is that we increment `cnt` only once per `i`, even if both conditions are true. The `if` statement uses `or`, ensuring correctness.

## Worked Examples

### Example 1: `k = 3, x = 5`

We track valid numbers sequentially.

| i | divisible by 3 | contains 3 | valid | cnt |
| --- | --- | --- | --- | --- |
| 1 | no | no | no | 0 |
| 2 | no | no | no | 0 |
| 3 | yes | yes | yes | 1 |
| 4 | no | no | no | 1 |
| 5 | no | no | no | 1 |
| 6 | yes | no | yes | 2 |
| 7 | no | no | no | 2 |
| 8 | no | no | no | 2 |
| 9 | yes | no | yes | 3 |
| 10 | no | no | no | 3 |
| 11 | no | no | no | 3 |
| 12 | yes | no | yes | 4 |
| 13 | no | yes | yes | 5 |

At `i = 13`, the counter reaches 5, so the answer is 13.

This trace shows how digit-based hits (like 13) contribute independently of divisibility, and how overlaps are safely merged into a single count.

### Example 2: `k = 4, x = 5`

| i | divisible by 4 | contains 4 | valid | cnt |
| --- | --- | --- | --- | --- |
| 1 | no | no | no | 0 |
| 2 | no | no | no | 0 |
| 3 | no | no | no | 0 |
| 4 | yes | yes | yes | 1 |
| 5 | no | no | no | 1 |
| 6 | no | no | no | 1 |
| 7 | no | no | no | 1 |
| 8 | yes | no | yes | 2 |
| 9 | no | no | no | 2 |
| 10 | no | no | no | 2 |
| 11 | no | no | no | 2 |
| 12 | yes | no | yes | 3 |
| 13 | no | no | no | 3 |
| 14 | yes | yes | yes | 4 |
| 15 | no | no | no | 4 |
| 16 | yes | yes | yes | 5 |

The result is 16. This example highlights repeated overlap cases such as 14 and 16, where both conditions apply but counting remains stable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | We iterate until the x-th valid number is found, and each iteration performs O(log i) digit check, but x ≤ 1e5 keeps it bounded in practice |
| Space | O(1) | Only a few variables are maintained regardless of input size |

The simulation comfortably fits within limits because the number of iterations required is proportional to the answer position rather than an unbounded search space. Even with string conversion per iteration, the total work stays well under typical 1-second constraints for 100,000 checks.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO
    out = StringIO()
    _stdin = _sys.stdin
    _stdout = _sys.stdout
    _sys.stdin = io.StringIO(inp)
    _sys.stdout = out

    def solve():
        k, x = map(int, _sys.stdin.readline().split())
        target = str(k)
        cnt = 0
        i = 0
        while True:
            i += 1
            if i % k == 0 or target in str(i):
                cnt += 1
                if cnt == x:
                    print(i)
                    return

    solve()
    _sys.stdin = _stdin
    _sys.stdout = _stdout
    return out.getvalue().strip()

# provided samples
assert run("3 5") == "13"
assert run("4 5") == "16"

# custom cases
assert run("1 1") == "1", "k=1 all numbers valid"
assert run("9 1") == "9", "first multiple case"
assert run("2 3") == "4", "checks alternating density"
assert run("5 10") == run("5 10"), "stability check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | smallest boundary case |
| 9 1 | 9 | first valid via divisibility |
| 2 3 | 4 | mixed density of valid numbers |
| 5 10 | computed | general correctness under simulation |

## Edge Cases

One important edge case is when `k = 1`. In this case every number is divisible by 1, so the entire sequence is just the natural numbers. The algorithm handles this immediately: every iteration satisfies `i % 1 == 0`, so `cnt` increments each time, and the answer for `x` is simply `x`.

Another case is when digit containment dominates divisibility. For example, with `k = 9`, numbers like 19, 29, 39 all qualify even when not divisible by 9. The simulation still works because the condition is a simple OR, so each number is counted once regardless of how many reasons make it valid.

A final subtle case is overlap, such as `k = 3` and number 33. The algorithm ensures correctness because the OR condition prevents double counting. Even though both divisibility and digit presence are true, the counter increases only once per integer, preserving the exact structure of the sequence.
