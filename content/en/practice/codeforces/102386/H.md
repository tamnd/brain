---
title: "CF 102386H - \u0421\u0432\u0435\u0442\u043e\u0444\u043e\u0440\u044b"
description: "At the intersection there are two countdowns, initially showing A and B. After every second, both values decrease by one simultaneously. We are interested only in the moments when both countdowns are still positive."
date: "2026-08-14T13:32:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102386
codeforces_index: "H"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b\u0430 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u043c\u0438\u0440\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2019"
rating: 0
weight: 102386
solve_time_s: 140
verified: false
draft: false
---

[CF 102386H - \u0421\u0432\u0435\u0442\u043e\u0444\u043e\u0440\u044b](https://codeforces.com/problemset/problem/102386/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 20s  
**Verified:** no  

## Solution
## Problem Understanding

At the intersection there are two countdowns, initially showing `A` and `B`. After every second, both values decrease by one simultaneously. We are interested only in the moments when both countdowns are still positive. At such a moment, the two displayed numbers are considered special if one is an integer multiple of the other.

We need to count every such moment before either countdown reaches zero. Since both counters decrease by exactly the same amount, after `t` seconds their values are `A - t` and `B - t`. The condition is that one of these positive values divides the other.

The bounds allow both `A` and `B` to be as large as `10^9`. A direct simulation can consequently require almost `10^9` iterations, which is far beyond what a competitive programming solution can afford. We need to replace the simulation with arithmetic that examines only about `sqrt(10^9)`, which is roughly `31623`, possibilities.

There are several boundary cases that can easily cause an off-by-one error. For example, with input `1 1`, the only state before a counter reaches zero is `(1, 1)`, so the answer is `1`. A loop that simulates until one value becomes zero and checks only after decrementing would incorrectly return `0`.

With input `3 30`, the positive states are `(3,30)`, `(2,29)`, and `(1,28)`. The first state has `30` divisible by `3`, and the last has `28` divisible by `1`, so the answer is `2`. The state `(0,27)` must not be considered, because the problem stops as soon as a counter reaches zero.

Another special case is equal counters. For input `5 5`, every positive state is `(5,5)`, `(4,4)`, `(3,3)`, `(2,2)`, `(1,1)`, and every one satisfies the condition. The answer is `5`. Treating the difference between the counters as a divisor target without handling a zero difference separately would fail here.

## Approaches

The most direct solution is to simulate every second. At time `t`, we compute `A - t` and `B - t`, check whether either divides the other, and increment the answer when it does. This is correct because every possible state before a light turns green occurs at exactly one integer time.

The problem is the number of states. If the smaller initial counter is close to `10^9`, the simulation performs almost `10^9` iterations. Even with constant work per iteration, that is much too slow.

The useful observation is that the difference between the counters never changes. Suppose without loss of generality that `A <= B`. After `t` seconds the counters are

`A - t` and `B - t`.

Their difference is always

`(B - t) - (A - t) = B - A`.

Call this fixed difference `d`. At every relevant moment the larger value is therefore the smaller value plus `d`.

Now let the smaller current value be `x`. The condition that the larger value is an integer multiple of the smaller one becomes

`x + d` is divisible by `x`.

Since `x` already divides itself, this is equivalent to

`x` divides `d`.

As the countdown progresses, `x` takes every integer value from `A` down to `1`. The original simulation has consequently been transformed into a much smaller number-theoretic problem: count the positive divisors of `d` that are at most `A`.

When `A = B`, the difference is zero. Every positive `x` divides zero, so every one of the `A` states is valid. That case is handled directly.

For a nonzero difference, divisors can be enumerated in pairs. If `i` divides `d`, then `d / i` is also a divisor. We only need to try `i` up to `sqrt(d)`, giving a time complexity of `O(sqrt(|A-B|))`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(min(A, B)) | O(1) | Too slow |
| Optimal | O(sqrt( | A-B | )) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two initial countdown values and let `m = min(A, B)`. The smaller counter is the one that reaches zero first, so its positive values are exactly `m, m-1, ..., 1`.
2. If `A == B`, return `A`. Both counters are equal at every moment before zero, so every one of the `A` positive states satisfies the required condition.
3. Otherwise compute `d = abs(A - B)`. The difference between the two counters stays equal to `d` throughout the countdown.
4. Enumerate integers `i` from `1` through `floor(sqrt(d))`. Whenever `i` divides `d`, both `i` and `d // i` are divisors of `d`.
5. Count a divisor only if it is at most `m`. Such a divisor corresponds to exactly one countdown state whose smaller displayed value equals that divisor. Divisors larger than `m` never occur before the first counter reaches zero.
6. If `i` and `d // i` are different, count them separately. When `i * i == d`, the two values are the same divisor and must be counted only once.
7. Output the resulting count.

### Why it works

Assume `A <= B`, with the other case being symmetric. At any valid time, let the smaller displayed value be `x`. The other value is `x + d`, where `d = B - A` is constant. The required condition is that one value divides the other. Since `x + d` is at least `x`, this means exactly that `x` divides `x + d`. Subtracting `x` gives the equivalent condition `x | d`.

During the countdown before either value reaches zero, `x` takes every integer from `A` down to `1` exactly once. Thus there is a one-to-one correspondence between valid moments and divisors of `d` that are at most `A`, which is `m` in the symmetric formulation. The algorithm enumerates exactly those divisors, so its count is exactly the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B = map(int, input().split())

    m = min(A, B)
    d = abs(A - B)

    if d == 0:
        print(m)
        return

    ans = 0
    i = 1

    while i * i <= d:
        if d % i == 0:
            if i <= m:
                ans += 1

            other = d // i
            if other != i and other <= m:
                ans += 1

        i += 1

    print(ans)

solve()
```

The first three assignments identify the smaller countdown and the invariant difference. Using `m = min(A, B)` means the rest of the algorithm does not need to distinguish which original counter was smaller.

The `d == 0` branch is necessary because divisor enumeration is based on the positive integer divisors of a nonzero difference. When the counters are equal, every positive state is valid, so the answer is simply the number of positive states, `m`.

For a nonzero difference, the loop checks only `i * i <= d`. Every divisor below the square root has a complementary divisor above it, so checking both members of each pair covers all divisors without scanning all values up to `d`.

The condition `other != i` prevents a perfect square from being counted twice. For example, if `d = 36`, the pair generated by `i = 6` is `(6, 6)`, which represents only one divisor.

The comparison with `m` is what enforces the time boundary. A divisor larger than the initial smaller countdown can never appear as the smaller positive countdown value, so it must not contribute to the answer.

Python integers do not overflow, and `i * i` is safe even at the largest possible `d`, which is below `10^9`. There is also no need for any array or other auxiliary structure.

## Worked Examples

For the first sample, `A = 3` and `B = 30`. The smaller initial value is `3`, and the fixed difference is `27`.

| `i` | `27 % i` | Divisors found | `<= m` | `ans` |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1, 27 | 1 | 1 |
| 2 | 1 | none | none | 1 |
| 3 | 0 | 3, 9 | 3, 9 only 3 | 2 |
| 4 | 3 | none | none | 2 |
| 5 | 2 | none | none | 2 |

The loop stops once `i * i > 27`. The divisors of `27` that do not exceed `3` are `1` and `3`, giving the answer `2`. They correspond to the states `(1,28)` and `(3,30)`.

For the second sample, `A = 16` and `B = 4`. Now `m = 4` and `d = 12`.

| `i` | `12 % i` | Divisors found | `<= m` | `ans` |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1, 12 | 1 | 1 |
| 2 | 0 | 2, 6 | 2 | 2 |
| 3 | 0 | 3, 4 | 3, 4 | 4 |

The smaller counter takes the values `4, 3, 2, 1`. All four are divisors of `12`, so all four moments satisfy the condition. The answer is `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt( | A-B | )) | The non-equal case checks divisors only up to the square root of the fixed difference. |
| Space | O(1) | Only a constant number of integer variables are stored. |

The largest possible nonzero difference is less than `10^9`, so the loop performs at most about `31623` iterations. That is tiny compared with the nearly `10^9` iterations required by direct simulation. The equal-counter case is even faster because it returns immediately.

## Test Cases

```python
import sys
import io

def solve():
    A, B = map(int, input().split())

    m = min(A, B)
    d = abs(A - B)

    if d == 0:
        print(m)
        return

    ans = 0
    i = 1

    while i * i <= d:
        if d % i == 0:
            if i <= m:
                ans += 1

            other = d // i
            if other != i and other <= m:
                ans += 1

        i += 1

    print(ans)

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = sys.stdin.readline

assert run("3 30\n") == "2", "sample 1"
assert run("16 4\n") == "4", "sample 2"

assert run("1 1\n") == "1", "minimum equal counters"
assert run("5 5\n") == "5", "all states valid when counters are equal"
assert run("1 1000000000\n") == "1", "only the smaller value 1 can be a divisor"
assert run("1000000000 1000000000\n") == "1000000000", "maximum equal counters"
assert run("2 4\n") == "2", "boundary state at value 1 must be counted"
assert run("6 10\n") == "2", "divisors 1 and 2 are the only valid smaller values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum input and immediate equal-counter case |
| `5 5` | `5` | Every positive state is valid when the counters are equal |
| `1 1000000000` | `1` | Very large difference and the fact that only the divisor `1` is reachable |
| `1000000000 1000000000` | `1000000000` | Maximum input values and the special `d = 0` case |
| `2 4` | `2` | The final positive state must be counted, while the zero state must not |
| `6 10` | `2` | Filtering divisors by the initial smaller counter |

## Edge Cases

For `1 1`, the algorithm sets `m = 1` and `d = 0`. It immediately returns `m`, producing `1`. This avoids trying to enumerate divisors of zero and correctly counts the only positive state, `(1,1)`.

For `3 30`, the algorithm gets `m = 3` and `d = 27`. The divisors encountered are `1`, `27`, `3`, and `9`. Only `1` and `3` are at most `m`, so the answer is `2`. These correspond to the positive states `(1,28)` and `(3,30)`. The state `(0,27)` never enters the counting logic.

For `5 5`, the difference is zero. Every positive smaller value from `5` down to `1` satisfies `x | x`, so returning `m = 5` counts all five valid moments. A generic divisor-of-difference formula without a separate zero case would not represent this situation correctly.

For `1 1000000000`, the difference is `999999999` and the smaller counter can only ever show `1` before reaching zero. Although the difference has many divisors, only the divisor `1` is reachable. The algorithm filters every larger divisor out with the `<= m` condition and returns `1`.

For `2 4`, the difference is `2`, and the reachable smaller values are `2` and `1`. Both divide `2`, so the answer is `2`. This confirms that the value `1`, which occurs immediately before the first counter reaches zero, is included, while the subsequent zero value is excluded.

For `1000000000 1000000000`, the algorithm does not attempt a billion-step simulation. It recognizes equal counters immediately and returns `1000000000`. This is both the correct answer and the reason the equal-counter branch is essential for performance as well as correctness.
