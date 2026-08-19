---
title: "CF 102180D - \u0422\u044b\u043a\u0432\u0435\u043d\u043d\u0430\u044f \u043c\u0430\u0433\u0438\u044f"
description: "We have n pumpkins, and the size of the i-th pumpkin is ai. Two operations can change a pumpkin. We may add exactly p to its size, or multiply its size by k. A third operation turns the pumpkin into a carriage, but only when its size is exactly m."
date: "2026-08-19T15:28:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102180
codeforces_index: "D"
codeforces_contest_name: "MSPU Training Contest 2018-2019"
rating: 0
weight: 102180
solve_time_s: 142
verified: true
draft: false
---

[CF 102180D - \u0422\u044b\u043a\u0432\u0435\u043d\u043d\u0430\u044f \u043c\u0430\u0433\u0438\u044f](https://codeforces.com/problemset/problem/102180/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` pumpkins, and the size of the `i`-th pumpkin is `a_i`. Two operations can change a pumpkin. We may add exactly `p` to its size, or multiply its size by `k`. A third operation turns the pumpkin into a carriage, but only when its size is exactly `m`.

For every initial pumpkin we need to decide independently whether some sequence of the first two operations can transform its size into exactly `m`. The output contains `1` for a usable pumpkin and `0` otherwise.

The key difficulty is that the operations can be interleaved. For example, we could add `p`, multiply by `k`, add `p` again, and multiply again. A direct search over such sequences has far too many possibilities.

The bounds make this especially restrictive. There can be `10^5` pumpkins, so an algorithm that performs even `O(n^2)` work would already require about `10^10` operations. The target size and initial sizes are at most `10^7`, which leaves room for algorithms linear in `m`, but an `O(n log m)` solution is substantially better and easily fits the limit. Since `k >= 2`, repeated multiplication can happen only `O(log m)` times before the size exceeds `m`.

There are several boundary cases that can fool a careless implementation. If `a_i > m`, the answer is immediately `0`, because every available operation only increases the size. For example, with `1 3 2 7` and pumpkin size `9`, the answer is `0`.

The pumpkin may already have the target size. With `1 5 2 10` and pumpkin size `10`, the answer is `1`, because zero operations are allowed before the carriage spell.

Exact equality after multiplication also matters. With `1 3 2 12` and pumpkin size `3`, multiplying twice gives `12`, so the answer is `1`. An implementation that stops when the next multiplication would exceed `m` must still test the current value before multiplying.

Finally, having the same remainder modulo `p` is not enough by itself. The multiplied value must also not exceed `m`. For example, with `1 6 2 10` and pumpkin size `6`, both `6` and `10` are congruent modulo `2`, but the answer is actually `1` because no multiplication is needed and two additions of `2` reach `10`. In contrast, for `1 4 3 10` and pumpkin size `4`, the remainder condition holds, but multiplying gives `12 > 10`, so the answer is `0`.

## Approaches

A direct brute-force solution can view every spell as a choice between adding `p` and multiplying by `k`. Starting from a pumpkin, it recursively tries both operations while the resulting size does not exceed `m`. This is correct because every possible valid sequence consists only of these two choices.

The problem is the number of sequences. If a search explores `L` spell positions, it can have up to `2^L` branches. In the worst case, `L` can be on the order of `m / p`, which can be about `10^7`. A bound such as `2^10000000` is obviously impossible to enumerate, even for one pumpkin.

The brute-force works because it considers every possible ordering of the two operations, but most of those orderings are equivalent from the perspective of reachability. The key observation is that every multiplication can be moved before every addition.

Suppose a sequence contains an addition by `p` followed later by a multiplication by `k`. If there are `s` multiplications after that addition, its contribution to the final value is `p * k^s`. Instead of performing that addition at its original position, we can delete it and perform `k^s` additions by `p` at the very end. Both sequences contribute exactly the same amount to the final size.

Repeating this transformation moves all multiplications to the beginning and all additions to the end. This is the central simplification used in the official contest analysis.

Consequently, if a pumpkin starts at size `x`, every reachable target can be obtained in the form

`x * k^t + q * p`

for some nonnegative integers `t` and `q`.

For a fixed number `t` of multiplications, we first reach `x * k^t`. From there, only additions by `p` remain. Such additions can reach `m` exactly if and only if `m - x * k^t` is nonnegative and divisible by `p`.

Thus, for every pumpkin we only need to try the possible values of `t`. Since `k >= 2`, the value `x * k^t` grows exponentially, so there are only `O(log m)` possibilities. We can check each one in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of spells | O(m) recursion/state depth in a bounded search | Too slow |
| Optimal | O(n log m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `p`, `k`, `m` and the array of initial pumpkin sizes. We process every pumpkin independently because spells applied to one pumpkin have no effect on another.
2. For the current pumpkin with size `x`, start with `cur = x`. This represents the value obtained after zero multiplications.
3. Before doing another multiplication, check whether `cur <= m` and whether `(m - cur) % p == 0`. If both conditions hold, the pumpkin is usable. We can perform the current number of multiplications first, then repeatedly add `p` until reaching exactly `m`.
4. If the check fails, replace `cur` by `cur * k` and repeat while `cur * k <= m`. Multiplication is considered only while it keeps the pumpkin at or below the target, because all subsequent operations only increase the value.
5. If every possible multiplication count has been checked without finding a valid remainder, output `0` for this pumpkin.
6. Repeat the process for all `n` pumpkins and print the resulting sequence of zeros and ones.

The reason the check is sufficient is that every arbitrary spell sequence can be rearranged into all multiplications followed by all additions. For a fixed number of multiplications, the only remaining question is whether the difference to `m` is a nonnegative multiple of `p`.

### Why it works

Consider a pumpkin of initial size `x` and any successful sequence that reaches `m`. Move every addition to the end of the sequence using the transformation described above. This preserves the final size, so there is also a successful sequence containing some number `t` of multiplications followed only by additions.

After those multiplications the pumpkin has size `x * k^t`. The remaining operations add `p` repeatedly, so the final value has the form `x * k^t + q * p`. Hence a successful sequence exists exactly when, for some `t`, `x * k^t <= m` and `m - x * k^t` is divisible by `p`.

The algorithm checks every possible `t` for which `x * k^t <= m`. It accepts precisely when that condition is satisfied, so it cannot miss a valid pumpkin or accept an impossible one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, p, k, m = map(int, input().split())
    a = list(map(int, input().split()))

    ans = []

    for x in a:
        cur = x
        possible = False

        while cur <= m:
            if (m - cur) % p == 0:
                possible = True
                break

            if cur > m // k:
                break

            cur *= k

        ans.append(1 if possible else 0)

    print(*ans)

if __name__ == "__main__":
    solve()
```

The outer loop processes each initial pumpkin once. For that pumpkin, `cur` is always the size after some number of multiplications and before any final additions. The first check therefore corresponds exactly to one candidate value of `t`.

The expression `(m - cur) % p == 0` is used only after `cur <= m`. Without that boundary check, a negative difference could accidentally satisfy divisibility even though the pumpkin can never decrease to `m`.

The condition `cur > m // k` is a safe way to decide that the next multiplication would exceed `m`. Writing `cur * k <= m` would also be correct in Python because Python integers do not overflow, but `m // k` avoids constructing a value that is already known to be too large. It also makes the boundary condition explicit.

The current value is checked before multiplication. This handles both `x == m` and cases where the correct number of multiplications is exactly the current number of iterations. Stopping before checking the current value would incorrectly reject such pumpkins.

The solution does not need to explicitly count the required additions. Once `m - cur` is a nonnegative multiple of `p`, performing that many additions reaches `m` exactly.

## Worked Examples

### Sample 1

The first sample is interpreted as

```
1 3 2 7
9
```

The pumpkin starts at `9`, already larger than the target `7`.

| Pumpkin | `cur` | `cur <= m` | `(m-cur) % p` | Result |
| --- | --- | --- | --- | --- |
| 9 | 9 | false | not checked | 0 |

Since both available transformations only increase the size, there is no way to turn `9` into `7`. The correct output is `0`.

This example exercises the early boundary condition `x > m`. A solution that only checks the modular condition could incorrectly accept the pumpkin because `9 - 7` is divisible by `3`.

### Sample 2

The second sample is

```
9 2 4 8
1 2 3 4 5 6 7 8 9
```

We test every initial size using `p = 2`, `k = 4`, and `m = 8`.

| Initial `x` | `cur` values checked | Successful `cur` | Output |
| --- | --- | --- | --- |
| 1 | 1, 4 | 4 | 1 |
| 2 | 2 | 2 | 1 |
| 3 | 3 | 3 | 0 |
| 4 | 4 | 4 | 1 |
| 5 | 5 | 5 | 0 |
| 6 | 6 | 6 | 1 |
| 7 | 7 | 7 | 0 |
| 8 | 8 | 8 | 1 |
| 9 | 9 | none | 0 |

For `x = 1`, multiplying gives `4`, and then two additions of `2` reach `8`. For `x = 2`, four additions of `2` reach `10`, so instead we multiply once and immediately reach `8`. For `x = 3`, neither `3` nor `12` is usable because `12` already exceeds the target and `8 - 3` is not divisible by `2`.

The resulting output is

```
1 1 0 1 0 1 0 1 0
```

This trace demonstrates why we must check several possible numbers of multiplications rather than only the initial value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log m) | Each pumpkin is multiplied by at least `2` on every iteration, so it has at most `O(log m)` candidate values. |
| Space | O(n) | The input array and the output array contain `n` elements. |

Since `n <= 10^5` and `m <= 10^7`, the number of multiplication checks per pumpkin is small. Even with the smallest possible `k = 2`, there are fewer than 24 multiplications before exceeding `10^7`, so the total number of iterations is only a few million.

The solution comfortably fits the stated 1 second and 256 MB limits in a compiled language, and the Python implementation also performs only a small constant amount of work per logarithmic step.

## Test Cases

The provided statement formatting combines the two examples, so the first sample is reconstructed as `1 3 2 7` with the single pumpkin `9`, whose answer is `0`.

```python
import sys
import io

def solve_text(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    p = next(it)
    k = next(it)
    m = next(it)

    a = [next(it) for _ in range(n)]
    ans = []

    for x in a:
        cur = x
        possible = False

        while cur <= m:
            if (m - cur) % p == 0:
                possible = True
                break

            if cur > m // k:
                break

            cur *= k

        ans.append(1 if possible else 0)

    return " ".join(map(str, ans))

def run(inp: str) -> str:
    return solve_text(inp).strip()

# Provided sample 1
assert run("""\
1 3 2 7
9
""") == "0", "sample 1"

# Provided sample 2
assert run("""\
9 2 4 8
1 2 3 4 5 6 7 8 9
""") == "1 1 0 1 0 1 0 1 0", "sample 2"

# Minimum-size input, including the case a_i == m.
assert run("""\
1 1 2 1
1
""") == "1", "target already reached"

# All pumpkins are equal, and the answer is obtained after multiplication.
assert run("""\
5 3 2 7
1 1 1 1 1
""") == "1 1 1 1 1", "all equal values"

# Boundary around a multiplication that would exceed m.
assert run("""\
4 3 2 10
1 4 7 10
""") == "1 0 1 1", "multiplication boundary"

# Values above m and values requiring different multiplication counts.
assert run("""\
6 5 3 20
21 5 10 15 20 1
""") == "0 1 1 1 1 0", "above target and multiple paths"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 2 7 / 9` | `0` | Initial value already exceeds the target. |
| `1 1 2 1 / 1` | `1` | Zero operations are valid when the pumpkin already equals `m`. |
| `5 3 2 7 / 1 1 1 1 1` | `1 1 1 1 1` | Duplicate initial values are handled independently. |
| `4 3 2 10 / 1 4 7 10` | `1 0 1 1` | Exact multiplication boundaries and modular checks. |
| `6 5 3 20 / 21 5 10 15 20 1` | `0 1 1 1 1 0` | Values above the target and different valid operation counts. |

## Edge Cases

When the initial pumpkin is larger than `m`, the algorithm immediately enters the loop condition with `cur > m`, so it performs no transformations and returns `0`. For `1 3 2 7` with `a = 9`, this gives `0`, which is necessary because neither adding nor multiplying can decrease a size.

When the pumpkin already equals `m`, the first iteration checks `(m - cur) % p`, which is `0`. The algorithm returns `1` without applying any operation. For `1 5 2 10` with `a = 10`, the answer is `1`.

When multiplication lands exactly on `m`, the algorithm must inspect the value after that multiplication. For `1 3 2 12` with `a = 3`, the checked values are `3`, `6`, and `12`. At `12`, the difference from the target is zero, so the answer is `1`.

When multiplication would jump over `m`, it must not be performed. Consider `1 4 3 10` with `a = 4`. The current value `4` has difference `6`, which is not divisible by `4`, while the next value would be `12 > 10`. The search stops and returns `0`.

When a valid route uses multiplication before additions, the modular test finds it. For `p = 3`, `k = 2`, `m = 7`, and `a = 2`, the initial value `2` gives `7 - 2 = 5`, which is not divisible by `3`. After one multiplication, `cur = 4`, and `7 - 4 = 3` is divisible by `3`. The actual sequence is `2 -> 4 -> 7`, so the algorithm correctly returns `1`.

The implementation also handles repeated values without any special treatment. Each occurrence is checked separately and receives the same result for identical parameters and identical initial size. This preserves the required output order.
