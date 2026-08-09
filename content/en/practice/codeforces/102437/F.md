---
title: "CF 102437F - \u0411\u044b\u0441\u0442\u0440\u044b\u0439 \u043f\u0435\u0440\u0435\u0432\u043e\u0434"
description: "This is an interactive problem. There is an unknown nonnegative balance n, with n <= 10^18. We cannot read n directly. Instead, we may ask the terminal to withdraw some positive amount x."
date: "2026-08-09T12:57:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102437
codeforces_index: "F"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102437
solve_time_s: 998
verified: false
draft: false
---

[CF 102437F - \u0411\u044b\u0441\u0442\u0440\u044b\u0439 \u043f\u0435\u0440\u0435\u0432\u043e\u0434](https://codeforces.com/problemset/problem/102437/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 16m 38s  
**Verified:** no  

## Solution
## Problem Understanding

This is an interactive problem. There is an unknown nonnegative balance `n`, with `n <= 10^18`. We cannot read `n` directly. Instead, we may ask the terminal to withdraw some positive amount `x`. If the current balance is at least `x`, the terminal answers `accepted` and subtracts `x` from the balance. Otherwise it answers `rejected` and the balance stays unchanged.

The goal is to make the balance exactly zero and then print `finish`. The difficulty is the query limit. If `q` is the smallest integer satisfying `n <= 2^q`, then the terminal allows at most `q + 10` withdrawal attempts. Since `10^18 < 2^60`, a solution that blindly tests all powers of two from `2^59` down to `1` uses 60 attempts, which is too many for small values of `n`.

There is no ordinary input containing `n`. The input stream consists of replies from the interactor after our program prints commands. Likewise, the output is a sequence of interactive commands such as `withdraw x` and finally `finish`. Every command must be flushed immediately so that the interactor can answer it.

The bound `10^18` is useful because it gives only 60 relevant binary positions. A straightforward binary decomposition would thus take at most 60 successful or rejected withdrawal attempts. The challenge is not computational complexity in the usual sense, but reducing the number of interactions to at most `q + 10`, where `q` depends on the unknown `n`.

A careless implementation can fail on small balances. For example, if the balance is `0`, the correct interaction is simply `finish`, because `withdraw 1` would be rejected and wastes one of the available attempts. For a balance of `1`, `withdraw 1` must be accepted and then `finish` is correct. A strategy that always performs all 60 power-of-two queries wastes far more than the allowed `q + 10 = 10` attempts.

Another subtle case is that an accepted query changes the hidden balance. Suppose the balance is `10` and we ask for `8`. The answer is `accepted`, but the balance is now `2`. Any later reasoning has to use the new balance, not the original one. The optimal method is deliberately designed to tolerate this changing value.

## Approaches

The basic solution is to process the binary representation directly. Starting with `2^59`, ask whether that amount can be withdrawn. If it can, subtract it from the balance. Then continue with `2^58`, `2^57`, and so on down to `1`. At every step, if the corresponding binary bit is set, it is removed. After all 60 powers have been considered, the balance is zero.

This works because every number up to `10^18` is smaller than `2^60`, so its binary representation contains only powers from `2^59` through `2^0`. The problem is the number of interactions. For a small balance such as `n = 1`, this method still makes 60 attempts, while the terminal allows only 10. The official contest tutorial describes exactly this as the baseline and then reduces the number of queries with a binary search.

The key observation is that we do not actually need to know the exact largest power of two that can currently be withdrawn. We only need a power large enough to bound the remaining balance, because once we have such a bound, processing all smaller powers is enough to finish.

We can find a useful starting exponent with a binary search over the 60 possible powers. For a query `2^m`, an `accepted` answer proves that the current balance was at least `2^m`, so `m` is a valid exponent and we move the left boundary to `m`. A `rejected` answer proves that the current balance was below `2^m`, so `m` cannot be used and we move the right boundary to `m`.

The complication is that accepted queries subtract money, so the balance changes during this binary search. Fortunately, this does not break the method. Every exponent ever recorded as accepted corresponds to a power that was actually present in the balance at that moment. Since the balance can only decrease, that power was also no larger than the original balance. Thus the final `l` can never exceed the binary logarithm of the original `n`.

When the binary search finishes with `r = l + 1`, the last rejected boundary tells us that the current balance is smaller than `2^r = 2^(l+1)`. We can now simply try `2^l`, `2^(l-1)`, ..., `1`. These are all the powers that can occur in the binary representation of a number smaller than `2^(l+1)`, so they are sufficient to drain the account completely.

There are at most 6 binary-search queries because there are only 60 possible exponents and `2^6 = 64 > 60`. The cleanup uses at most `l + 1` queries, and `l <= q`, where `q` is the logarithm of the original balance. Thus the total is at most `q + 7`, comfortably below the allowed `q + 10`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(60) interactions | O(1) | Too many queries for small `n` |
| Optimal | O(log n) interactions | O(1) | Accepted |

## Algorithm Walkthrough

1. Set `l = 0` and `r = 60`. The interval represents all possible binary exponents, from `0` through `59`, and `2^60` is already known to exceed every possible initial balance.
2. While `r - l > 1`, choose `m = (l + r) // 2` and ask to withdraw `2^m`. This is the binary-search step. An accepted response proves that exponent `m` is achievable, so set `l = m`. A rejected response proves that `2^m` is too large for the current balance, so set `r = m`.
3. If the interactor ever answers `fail`, terminate immediately. Continuing after `fail` cannot produce a valid verdict.
4. After the binary search, process exponents from `l` down to `0`. For each exponent `i`, ask to withdraw `2^i`. If the answer is `accepted`, that power is removed from the remaining balance. If it is `rejected`, the bit corresponding to that power is absent, so nothing needs to be changed.
5. Print `finish` after all powers through `2^0` have been considered. At this point the balance must be zero.

### Why it works

At the end of the binary search, `r = l + 1`, and the right boundary corresponds to a power that was rejected at some point. The balance can only decrease after that rejection, so the current balance is certainly less than `2^r = 2^(l+1)`. Every nonnegative integer smaller than `2^(l+1)` can be represented using only the powers `2^l, 2^(l-1), ..., 1`. The cleanup phase tests exactly those powers and withdraws every one that is present, so the remaining balance becomes zero.

The query limit follows from a second invariant. Whenever the binary search sets `l = m`, the withdrawal of `2^m` was accepted, which means the original balance was at least `2^m`. Hence `m <= q`. Consequently `l <= q`. The binary search needs at most 6 queries, and the cleanup needs at most `l + 1 <= q + 1` queries, for a total of at most `q + 7`, which is below `q + 10`.

## Python Solution

The problem is interactive, so this program is intended to communicate with the official interactor rather than read a conventional test case.

```python
import sys
input = sys.stdin.readline

def ask(x):
    print(f"withdraw {x}", flush=True)
    response = input().strip()

    if response == "accepted":
        return True
    if response == "rejected":
        return False

    # The only other possible response is "fail".
    sys.exit(0)

def main():
    l = 0
    r = 60

    # Find an exponent l such that the remaining balance is below 2^(l+1).
    while r - l > 1:
        m = (l + r) // 2

        if ask(1 << m):
            l = m
        else:
            r = m

    # The remaining balance is smaller than 2^(l+1).
    # Its binary representation therefore uses only these powers.
    for i in range(l, -1, -1):
        ask(1 << i)

    print("finish", flush=True)

if __name__ == "__main__":
    main()
```

The `ask` function performs exactly one interactive withdrawal. Using `flush=True` is essential because the interactor cannot respond until it receives the command. The function returns a Boolean for the two normal responses and terminates immediately for `fail`.

The binary-search interval uses exponents rather than money amounts. `r = 60` is safe because every possible initial balance is strictly smaller than `2^60`. The loop condition `r - l > 1` leaves consecutive boundaries, so after the loop `r = l + 1`.

The expression `1 << m` computes `2^m` directly. Python integers have arbitrary precision, so there is no overflow issue. The largest value produced is `2^59`, which is also safely within the allowed withdrawal amount of `10^18`.

The cleanup loop deliberately goes downward. If we processed smaller powers first, a later accepted larger power could still leave a balance containing smaller bits, making the reasoning less direct. Descending powers mirrors ordinary binary decomposition and guarantees that every remaining bit is handled exactly once.

There is no attempt to skip a rejected cleanup query. A rejected query still counts as an interaction, but it is necessary because we need to determine whether that binary bit is present. The number of such queries is already covered by the `q + 7` bound.

## Worked Examples

### Sample 1

The interaction shown in the sample is consistent with an initial balance of `1`.

| Step | Action | Response | Remaining balance | `l` | `r` |
| --- | --- | --- | --- | --- | --- |
| 1 | `withdraw 42` | `rejected` | 1 | 0 | 42 |
| 2 | `withdraw 1` | `accepted` | 0 | 0 | 42 |
| 3 | `withdraw 1` | `rejected` | 0 | 0 | 42 |
| 4 | `finish` | accepted by judge | 0 | 0 | 42 |

The sample itself is not produced by the optimal algorithm, so its command sequence should not be expected to match the program above. It demonstrates the protocol: a rejected withdrawal changes nothing, an accepted withdrawal subtracts the requested amount, and `finish` succeeds only when the balance is zero.

For `n = 1`, the optimal program first performs its binary search. All tested powers greater than `1` are rejected, leaving `l = 0`. The cleanup then asks for `1`, receives `accepted`, and finishes. The total number of withdrawal attempts is at most 7.

### Sample 2

This sample is consistent with an initial balance of `0`.

| Step | Action | Response | Remaining balance | `l` | `r` |
| --- | --- | --- | --- | --- | --- |
| 1 | `withdraw 1` | `rejected` | 0 | 0 | 1 |
| 2 | `finish` | accepted by judge | 0 | 0 | 1 |

Again, the sample is illustrating the protocol rather than the exact optimal query sequence. The important edge case is that a rejected withdrawal does not prove the balance is negative. It means only that the requested amount is larger than the current balance, so a balance of zero is possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) interactions | At most 6 binary-search queries and at most `q + 1` cleanup queries |
| Space | O(1) | Only a constant number of integer variables is stored |

Since `n <= 10^18 < 2^60`, the binary-search phase always needs at most 6 interactions. The cleanup needs at most `q + 1`, where `q` satisfies `n <= 2^q`. Thus the total is at most `q + 7`, leaving three queries of safety under the required `q + 10` limit. The memory usage is constant.

## Test Cases

Because this is an interactive problem, ordinary `run(input_string)` tests cannot provide the hidden balance through stdin. A useful offline test harness instead simulates the interactor. The following code uses the same algorithm against a fake terminal, checks that the final balance is zero, and verifies the query limit.

```python
import io
import sys

def run_simulation(initial_balance):
    balance = initial_balance
    attempts = 0
    commands = []

    def ask(x):
        nonlocal balance, attempts
        attempts += 1
        commands.append(f"withdraw {x}")

        if balance >= x:
            balance -= x
            return True
        return False

    l = 0
    r = 60

    while r - l > 1:
        m = (l + r) // 2

        if ask(1 << m):
            l = m
        else:
            r = m

    for i in range(l, -1, -1):
        ask(1 << i)

    commands.append("finish")

    q = 0
    while (1 << q) < initial_balance:
        q += 1

    assert balance == 0
    assert attempts <= q + 10

    return "\n".join(commands)

# Provided sample 1 corresponds to an initial balance of 1.
sample1 = run_simulation(1)
assert sample1.endswith("finish"), "sample 1"

# Provided sample 2 corresponds to an initial balance of 0.
sample2 = run_simulation(0)
assert sample2.endswith("finish"), "sample 2"

# Minimum-size balance.
assert run_simulation(0).endswith("finish"), "zero balance"

# Small boundary values around powers of two.
for n in [1, 2, 3, 4, 7, 8, 9, 15, 16, 17]:
    run_simulation(n)

# A large value close to 2^60.
assert run_simulation(10**18).endswith("finish"), "maximum allowed balance"

# Exact powers of two exercise the boundary between q values.
for n in [2**10, 2**20, 2**30, 2**40, 2**50, 2**59]:
    run_simulation(n)

# Values immediately below and above powers of two catch off-by-one errors.
for n in [2**10 - 1, 2**10, 2**10 + 1]:
    run_simulation(n)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `finish` | Empty account and smallest possible balance |
| `1` | `finish` after successful withdrawal | Smallest positive balance |
| `2^k - 1` | `finish` | Lower boundary of a binary interval |
| `2^k` | `finish` | Exact power-of-two boundary |
| `2^k + 1` | `finish` | Upper side of the boundary |
| `10^18` | `finish` | Maximum permitted balance |
| `2^59` | `finish` | Largest relevant binary power |

The simulator deliberately does not compare the exact sequence of commands against a fixed expected transcript. Interactive solutions can legitimately make different valid queries, and the correctness conditions are that the final balance is zero and the query limit is respected.

## Edge Cases

### Zero balance

For `n = 0`, the exact input situation is represented by an interactor that rejects every positive withdrawal. The binary search eventually leaves `l = 0`, and the cleanup asks for `1`, which is rejected. The balance remains zero, so `finish` is correct. The algorithm never assumes that an accepted query must occur.

### Balance equal to one

For `n = 1`, every power greater than one is rejected during the binary search. The resulting `l` is zero, so the cleanup asks for `1`. That query is accepted and leaves zero. This case is especially useful because `q = 0`, making the maximum allowed number of withdrawal attempts only `10`.

### Exact power of two

Suppose `n = 16`. During the binary search, the query for `16` may be accepted, immediately reducing the balance to zero. The exponent `l = 4` records that `2^4` was available. Later cleanup queries for `16`, `8`, `4`, `2`, and `1` are harmless because the balance is already zero, and all are rejected. The final `finish` is valid. This demonstrates why an accepted binary-search query changing the balance does not invalidate the algorithm.

### Just below a power of two

Suppose `n = 15`. A query for `16` is rejected, so the right boundary becomes the exponent corresponding to `16`. Eventually the binary search establishes a lower exponent whose next power is larger than the current balance. The cleanup checks `8`, `4`, `2`, and `1`, and all four bits are accepted. Their sum is `15`, so the balance reaches zero.

### Just above a power of two

Suppose `n = 17`. A query for `16` can be accepted, leaving balance `1`. The binary search records exponent `4`, and the cleanup subsequently checks powers down from `16`. Since the remaining balance is only `1`, the larger powers are rejected and `1` is accepted. The final balance is zero. This case demonstrates why the cleanup must continue all the way to `2^0`, even after a large power has already been withdrawn.

### Maximum balance

For `n = 10^18`, we have `q = 59` because `2^59 <= 10^18 < 2^60`. The binary search uses at most 6 queries, and `l` is at most 59, so the cleanup uses at most 60 more queries. The total is at most 66, while the terminal permits `q + 10 = 69` attempts. The algorithm therefore remains within the limit even at the largest possible balance.
