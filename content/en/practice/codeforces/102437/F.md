---
title: "CF 102437F - \u0411\u044b\u0441\u0442\u0440\u044b\u0439 \u043f\u0435\u0440\u0435\u0432\u043e\u0434"
description: "This is an interactive problem. There is no ordinary input containing the account balance. The interactor secretly chooses an initial balance (n), with (0 le n le 10^{18}), and our program has to discover enough information about it to transfer the entire balance away."
date: "2026-08-16T09:33:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102437
codeforces_index: "F"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102437
solve_time_s: 247
verified: false
draft: false
---

[CF 102437F - \u0411\u044b\u0441\u0442\u0440\u044b\u0439 \u043f\u0435\u0440\u0435\u0432\u043e\u0434](https://codeforces.com/problemset/problem/102437/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 7s  
**Verified:** no  

## Solution
## Problem Understanding

This is an interactive problem. There is no ordinary input containing the account balance. The interactor secretly chooses an initial balance (n), with (0 \le n \le 10^{18}), and our program has to discover enough information about it to transfer the entire balance away. The only query is `withdraw x`. If the current balance is at least (x), the interactor answers `accepted` and removes (x). Otherwise it answers `rejected` and leaves the balance unchanged. We may finish by printing `finish`, but that is accepted only when the hidden balance is actually zero. The official statement confirms this interactive protocol and the limit of (q+10) queries, where (q) is the smallest integer satisfying (n\le2^q).

The challenge is not merely to find (n), but to do it with very few destructive comparisons. Since (n) can be as large as (10^{18}), a strategy that performs one withdrawal per dollar can require (10^{18}) queries. Even an ordinary binary search over the whole interval ([0,10^{18}]) would use about 60 queries, which is already too many when (n) is small. For example, if (n=1), then (q=0), so at most 10 attempts are allowed.

There are two edge cases that deserve special attention. If (n=0), the correct interaction can be just `withdraw 1`, receiving `rejected`, followed by `finish`. A strategy that blindly starts testing large powers of two would waste many queries and exceed the limit for (q=0). If (n=1), the first `withdraw 1` is accepted, but that does not by itself prove that the account is empty. A second `withdraw 1` is necessary to distinguish (n=1) from (n\ge2). For example, the sample interaction

```
withdraw 42
withdraw 1
withdraw 1
finish
```

with replies

```
rejected
accepted
rejected
```

proves that the hidden balance was exactly 1. The first rejection gives (n<42), the first accepted withdrawal gives (n\ge1), and the second rejection proves that after removing one dollar nothing remained. The official samples contain exactly this interaction.

## Approaches

The direct approach is to repeatedly try `withdraw 1`. Every successful query removes exactly one dollar, so it is obviously correct, and eventually the account becomes empty. The problem is the number of operations. For (n=10^{18}), this requires exactly (10^{18}) attempts, while the interactor allows only (q+10), with (q=60). The approach is not remotely feasible.

A more promising idea is to use powers of two. If we somehow know that the balance lies between (2^k) and (2^{k+1}-1), then withdrawing (2^{k-1},2^{k-2},\ldots,1) extracts its remaining binary representation in at most (k) queries. The missing piece is how to discover (k) without spending (k) more queries just testing powers of two.

The key observation is that successful withdrawals can be treated as comparisons against the original balance. Suppose we have already withdrawn exactly (s) dollars, so the current account contains (n-s). To ask whether the original balance was at least some target (T), we can request `withdraw T-s`. If it is accepted, then (n-s\ge T-s), which is equivalent to (n\ge T). After that successful query, the total amount withdrawn becomes exactly (T). If it is rejected, the total withdrawn amount remains (s), and we have learned (n<T).

This lets us perform binary search on the exponent of the largest power of two not exceeding (n), while every successful comparison simply moves the amount already withdrawn to the tested power. Only about six queries are needed to locate that exponent because there are only 60 possible exponents. After that, the remaining balance is smaller than the largest known power of two, so its binary representation can be extracted directly.

The brute-force method spends one query per dollar, while the optimal method spends a constant number of queries to locate the magnitude and then one query per binary digit. The distinction is crucial because the query limit itself is logarithmic in (n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n)) queries | (O(1)) | Too slow |
| Optimal | (O(\log n)) queries | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Ask for one dollar. If the interactor rejects it, the hidden balance is zero, so print `finish`. This handles the (n=0) case within a single query.
2. If the first dollar was accepted, ask for one more dollar. If it is rejected, the original balance was exactly one, so print `finish`. After two accepted one-dollar withdrawals, we know that (n\ge2) and exactly two dollars have already been removed.
3. Maintain `paid`, the total amount already withdrawn. Initially `paid = 2`. We now find the largest exponent (f) such that (2^f\le n). Since (n\le10^{18}<2^{60}), it is enough to search exponents from 1 through 59.
4. Binary-search the exponent. For a candidate exponent (m), let `target = 2^m`. If `target <= paid`, then (n\ge paid\ge target) is already known, so no query is needed. Otherwise request `withdraw target - paid`. An accepted response proves (n\ge target), and we update `paid` to `target`. A rejected response proves (n<target), so the candidate exponent is too large.
5. After the exponent search, `paid = 2^f` and (2^f\le n<2^{f+1}). The remaining balance is consequently smaller than (2^f). Test the powers (2^{f-1},2^{f-2},\ldots,1) in descending order. Whenever a query is accepted, that binary digit is present and is removed from the account. A rejection means that digit is absent.
6. Once all these powers have been tested, every possible binary digit below (2^f) has been removed. The account is empty, so print `finish`.

### Why it works

The central invariant is that `paid` is always exactly the total amount removed from the original account. Thus the current balance is (n-\text{paid}). Whenever we want to test whether (n\ge T), and (T>\text{paid}), the query `withdraw T-paid` is accepted exactly when (n-\text{paid}\ge T-\text{paid}), which is exactly (n\ge T). A successful query also changes `paid` to (T), preserving the invariant.

The exponent search consequently finds the largest power of two not exceeding (n). Once that power has been withdrawn, the remaining amount is strictly smaller than it. Testing all smaller powers in descending order is exactly the greedy construction of the binary representation, so every remaining dollar is eventually transferred. No query can leave a nonzero balance after the final power of one has been tested.

The number of attempts is also within the special interactive bound. There are at most two initial queries, at most six exponent-search queries, and at most 59 binary-digit queries. Thus there are at most 67 attempts. For the largest possible balance, (q=60), so the limit is 70. For smaller balances the exponent search still costs only a constant number of queries, while the final binary extraction costs at most (q) queries, leaving the required slack of 10 queries.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ask(x):
    print(f"withdraw {x}", flush=True)
    response = input().strip()

    if response == "fail":
        sys.exit(0)

    return response == "accepted"

def finish():
    print("finish", flush=True)

# First distinguish n = 0 and n = 1.
if not ask(1):
    finish()
    sys.exit(0)

if not ask(1):
    finish()
    sys.exit(0)

# Two dollars have already been withdrawn.
paid = 2

# Find the largest f such that 2^f <= n.
lo = 1
hi = 59

while lo < hi:
    mid = (lo + hi + 1) // 2
    target = 1 << mid

    if target <= paid:
        lo = mid
    else:
        if ask(target - paid):
            paid = target
            lo = mid
        else:
            hi = mid - 1

f = lo

# Extract the remaining balance bit by bit.
power = 1 << (f - 1)

while power >= 1:
    if ask(power):
        pass
    power >>= 1

finish()
```

The `ask` function is the only place that communicates with the interactor. It prints the command, flushes immediately, and reads the reply. A `fail` response must terminate the program immediately, because continuing would violate the protocol.

The first two calls to `ask(1)` are special. The first distinguishes zero from a positive balance. The second distinguishes one from at least two. After both calls succeed, `paid` is exactly 2, which gives us a known amount already removed from the original balance.

During the exponent search, the expression `target - paid` is always positive because the query is performed only when `target > paid`. It is also at most (2^{59}), which is below the allowed maximum query amount of (10^{18}). Python integers have arbitrary precision, so there is no overflow issue.

The final loop does not need to maintain a separate variable for the current account balance. Each successful power withdrawal simply removes that binary digit. Because the powers are tested from largest to smallest, at every point the tested power is no larger than the remaining possible balance range.

The program has no ordinary input to parse because this is an interactive task. The required `input = sys.stdin.readline` declaration is still used for reading interactor responses, as required by the Python implementation convention.

## Worked Examples

### Sample 1

The sample interaction corresponds to an initial balance of exactly 1. Its transcript is:

```
withdraw 42
rejected
withdraw 1
accepted
withdraw 1
rejected
finish
```

Our implementation reaches the same conclusion through a slightly different transcript, because it starts by checking one dollar.

| Step | Query | Response for (n=1) | `paid` after step | Meaning |
| --- | --- | --- | --- | --- |
| 1 | `withdraw 1` | `accepted` | 1 | (n\ge1) |
| 2 | `withdraw 1` | `rejected` | 1 | (n<2), hence (n=1) |
| 3 | `finish` | `OK` | 1 | Account is empty |

The trace demonstrates why the second one-dollar query is necessary. A single accepted withdrawal cannot distinguish (n=1) from (n=2) or any larger positive balance.

### Sample 2

The second sample corresponds to an initial balance of zero:

```
withdraw 1
rejected
finish
```

| Step | Query | Response for (n=0) | `paid` after step | Meaning |
| --- | --- | --- | --- | --- |
| 1 | `withdraw 1` | `rejected` | 0 | (n<1), hence (n=0) |
| 2 | `finish` | `OK` | 0 | Account is empty |

This is the critical small-value case. A strategy that always performs a long power-of-two search would exceed the (q+10=10) query limit here, while the proposed algorithm stops after one withdrawal attempt.

### A larger example

Consider (n=13). The first two one-dollar withdrawals leave 11 dollars and set `paid=2`. During exponent search, the algorithm eventually proves that (2^3=8\le13) but (2^4=16>13). The successful comparison against 8 withdraws the remaining 6 dollars needed to make `paid=8`. The account now contains 5 dollars.

The final binary extraction tests 4, 2, and 1. The query for 4 succeeds, leaving 1 dollar; the query for 2 is rejected; the query for 1 succeeds. The total withdrawn amount is (8+4+1=13), so `finish` is safe.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\log n)) interactive queries | A constant-size exponent search is followed by one query per binary digit |
| Space | (O(1)) | Only a few integer variables and the current interactor response are stored |

The balance is bounded by (10^{18}), so there are at most 60 relevant binary positions. The worst-case number of withdrawal attempts is at most 67, below the allowed 70 attempts when (n) is near (10^{18}). For small (n), the number of final binary queries decreases with (q), while the exponent search remains bounded by six queries, so the (q+10) restriction is satisfied throughout the entire range.

## Test Cases

Because the original task is interactive, its samples are not ordinary stdin/stdout test cases. A useful offline test harness must simulate the hidden balance and verify that every generated withdrawal is legal, that the final balance is zero, and that the number of attempts does not exceed (q+10). The following tests mirror the submitted algorithm.

```python
import sys
import io

def offline_commands(n):
    balance = n
    commands = []

    def ask(x):
        nonlocal balance

        assert 1 <= x <= 10**18
        commands.append(("withdraw", x))

        if balance >= x:
            balance -= x
            return True
        return False

    if not ask(1):
        commands.append(("finish",))
        return commands, balance

    if not ask(1):
        commands.append(("finish",))
        return commands, balance

    paid = 2

    lo = 1
    hi = 59

    while lo < hi:
        mid = (lo + hi + 1) // 2
        target = 1 << mid

        if target <= paid:
            lo = mid
        else:
            if ask(target - paid):
                paid = target
                lo = mid
            else:
                hi = mid - 1

    f = lo
    power = 1 << (f - 1)

    while power >= 1:
        ask(power)
        power >>= 1

    commands.append(("finish",))
    return commands, balance

def run(n):
    commands, balance = offline_commands(n)

    q = 0 if n == 0 else (n - 1).bit_length()
    attempts = sum(1 for command in commands if command[0] == "withdraw")

    assert balance == 0
    assert commands[-1] == ("finish",)
    assert attempts <= q + 10

    return commands

def check_sample_1():
    balance = 1
    transcript = [
        ("withdraw", 42, False),
        ("withdraw", 1, True),
        ("withdraw", 1, False),
    ]

    for _, x, accepted in transcript:
        actual = balance >= x
        assert actual == accepted

        if actual:
            balance -= x

    assert balance == 0

def check_sample_2():
    balance = 0
    transcript = [
        ("withdraw", 1, False),
    ]

    for _, x, accepted in transcript:
        actual = balance >= x
        assert actual == accepted

        if actual:
            balance -= x

    assert balance == 0

check_sample_1()
check_sample_2()

# Minimum-size cases.
assert run(0)[-1] == ("finish",), "zero balance"
assert run(1)[-1] == ("finish",), "one dollar"

# Boundary between q = 1 and q = 2.
assert run(2)[-1] == ("finish",), "exact power of two"
assert run(3)[-1] == ("finish",), "just above a power of two"

# Large power of two, where the exponent reaches 59.
assert run(1 << 59)[-1] == ("finish",), "2^59"

# Maximum allowed initial balance.
assert run(10**18)[-1] == ("finish",), "maximum balance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (n=0) | `finish` after one rejected withdrawal | Minimum balance and the (q=0) query limit |
| (n=1) | `finish` after distinguishing the second withdrawal | Smallest positive balance and the off-by-one boundary |
| (n=2) | `finish` with the exact power of two fully withdrawn | Exact power-of-two handling |
| (n=3) | `finish` after extracting binary representation (11_2) | Value immediately above a power of two |
| (n=2^{59}) | `finish` | Highest relevant binary exponent |
| (n=10^{18}) | `finish` | Maximum allowed balance and query amount boundary |

## Edge Cases

For (n=0), the exact input state is a hidden balance of zero, so the first command is `withdraw 1`. The interactor rejects it because (0<1), and the program immediately prints `finish`. Only one attempt was made, while (q=0) permits ten.

For (n=1), the interaction begins with `withdraw 1`, which is accepted and leaves zero. The program cannot simply finish at this point because the same response would also occur for every (n\ge1). It sends `withdraw 1` again, receives `rejected`, and now knows that the original balance was less than two. Combined with the first accepted withdrawal, this proves (n=1). The program then finishes after two attempts, well below (q+10=10).

For (n=2), both initial one-dollar queries are accepted, so `paid=2` and the real account is empty. The exponent search knows that exponent 1 is already valid because `paid` itself equals (2^1). It does not issue a zero-valued query. The remaining power tests are empty of funds and all are rejected, after which `finish` is correct. This avoids a common boundary bug where an implementation accidentally tries `withdraw 0`.

For (n=3), the first two withdrawals again establish `paid=2`. The exponent search finds (f=1), since (2\le3<4). The remaining balance is one, so the final `withdraw 1` succeeds and removes it. The binary extraction has represented the original value as (2+1), exactly as required.

For (n=2^{59}), the exponent search reaches the largest allowed power (2^{59}). After that successful comparison, `paid` equals the entire balance. The final tests use powers from (2^{58}) down to 1, all of which are rejected. This case exercises the upper exponent boundary without ever querying (2^{60}), which would exceed the permitted withdrawal amount of (10^{18}).

For (n=10^{18}), the largest possible initial balance has (q=60). The algorithm first withdraws two dollars, uses at most six additional queries to locate the highest relevant power, and then uses at most 59 binary-digit queries. Even in the worst interaction this is at most 67 withdrawal attempts, below the allowed (q+10=70). The implementation also stays within the permitted (10^{18}) maximum for every individual withdrawal.
