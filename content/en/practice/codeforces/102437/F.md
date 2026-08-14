---
title: "CF 102437F - \u0411\u044b\u0441\u0442\u0440\u044b\u0439 \u043f\u0435\u0440\u0435\u0432\u043e\u0434"
description: "This is an interactive problem. There is a hidden nonnegative balance (n), with (n le 10^{18}), and the program does not receive (n) as ordinary input. Instead, it can ask the terminal whether at least (x) dollars remain by issuing withdraw x."
date: "2026-08-14T15:41:08+07:00"
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

This is an interactive problem. There is a hidden nonnegative balance (n), with (n \le 10^{18}), and the program does not receive (n) as ordinary input. Instead, it can ask the terminal whether at least (x) dollars remain by issuing `withdraw x`. An `accepted` answer means (x) dollars are removed from the current balance, while `rejected` means the balance was smaller than (x) and remains unchanged. Once the program believes the balance is zero, it prints `finish`.

The query limit depends on the unknown (n). Let (q) be the smallest integer satisfying (n \le 2^q). The terminal allows at most (q+10) withdrawal attempts. This makes the number of queries the real complexity measure. Since (10^{18}<2^{60}), a fixed strategy using all 60 powers of two is correct, but it can make 60 queries even when (n) is tiny. For example, when (n=0), the limit is only 10 queries, so an unconditional 60-query scan is invalid.

The straightforward solution is also sensitive to the distinction between an accepted query and knowing that the balance is zero. If (n=5), querying `withdraw 4` returns `accepted`, but the remaining balance is 1. Printing `finish` immediately would be wrong. A successful withdrawal only tells us that the requested amount was available.

The zero balance is another boundary case. If (n=0), `withdraw 1` must return `rejected`, after which `finish` is correct. If (n=1), the same query returns `accepted`, and `finish` becomes correct only after that withdrawal.

Exact powers of two are also useful for checking off-by-one errors. For (n=2^k), the query `withdraw 2^k` succeeds and leaves exactly zero. The algorithm must still be able to continue safely because it cannot generally assume that an accepted query exhausted the account. The largest possible value (10^{18}) is below (2^{60}) but above (2^{59}), so exponent 59 is the largest power of two that can ever be requested. The value (2^{60}) would exceed the allowed withdrawal amount and is unnecessary.

There is one more subtlety. During the optimization phase, the balance changes after every accepted query, so the answers do not form an ordinary monotone predicate about the original (n). For example, with (n=100), a query for 8 can be accepted and reduce the balance to 92, after which a query for 64 can be rejected even though the original balance was 100. The binary search therefore needs a different correctness argument from ordinary binary search.

## Approaches

The brute-force approach is to try every power of two from (2^{59}) down to (2^0). Whenever a withdrawal is accepted, that bit is removed from the current balance. This works because every nonnegative integer has a unique binary representation. At the end, every possible bit has been attempted, so nothing remains.

The problem is the number of attempts. There are exactly 60 powers of two from (2^0) through (2^{59}), so the worst case is 60 queries. For (n=0), however, (q=0), and the terminal permits only 10 attempts. The brute-force algorithm can already fail on the smallest possible balance.

The key observation is that we do not actually need to identify the highest set bit exactly. We only need to find an exponent (l) small enough that, after a short search, the remaining balance is less than (2^{l+1}). Then the usual descending binary decomposition can start at (l) instead of 59.

We can obtain such an (l) with binary search over the 60 possible exponents. For a midpoint (m), we try to withdraw (2^m). If it succeeds, we set (l=m). If it fails, we set (r=m). The balance may change during this process, so (l) is not necessarily the highest bit of either the original or current balance. What matters is that when the search finishes with (r=l+1), the final rejected query gives a bound on the current balance. If the last useful accepted query established (l), then every later exponent larger than (l) was rejected, and in particular the boundary exponent (l+1) is too large for the current balance. Thus the current balance is below (2^{l+1}).

The search has at most six queries because there are only 60 candidate exponents and (60<2^6). Afterward, at most (l+1) more queries are needed, and (l) never exceeds the logarithmic scale of the original balance. Hence the total is at most (q+7), comfortably below the allowed (q+10). This is the intended optimization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(60)) queries | (O(1)) | Too many queries for small (n) |
| Optimal | (O(q)) queries, at most (q+7) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Start with the exponent interval ([l,r)=[0,60)). We use 60 because every allowed balance is below (2^{60}), so every relevant power is (2^0,\ldots,2^{59}).
2. While (r-l>1), choose (m=(l+r)//2) and issue `withdraw \(2^m\)`. If the terminal answers `accepted`, set (l=m). The withdrawal has actually reduced the balance, but (l) still records a useful exponent that was affordable at that moment. If the answer is `rejected`, set (r=m), because the current balance is certainly below (2^m).
3. After the binary search, process exponents from (l) down to zero. For every (i), issue `withdraw \(2^i\)`. An accepted response removes that binary bit from the remaining balance. A rejected response simply means that bit is absent.
4. After all exponents from (l) through zero have been tried, print `finish`. The binary search has guaranteed that the remaining balance was below (2^{l+1}), so every possible remaining bit has now been considered.

The central invariant is that the balance never increases, and every accepted query removes exactly the amount that was requested. At the end of the binary search, either the search reached (l=59) after successfully withdrawing (2^{59}), in which case the remaining balance is below (2^{59}), or the search has a boundary (r=l+1) created by a rejected query for (2^r). In the latter case the current balance is below (2^{l+1}). Consequently, the final descending scan from (l) to zero is sufficient to remove every remaining dollar.

The query bound follows from the same construction. The binary search uses at most six attempts. The final scan uses at most (l+1) attempts. Since accepted withdrawals only decrease the balance, (l) cannot exceed the logarithmic scale of the original balance. Thus the total is at most (q+7), leaving three attempts of the required (q+10) allowance unused.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    def ask(x):
        print(f"withdraw {x}", flush=True)
        response = input().strip()
        if response == "fail":
            sys.exit(0)
        return response

    l, r = 0, 60

    while r - l > 1:
        m = (l + r) // 2
        response = ask(1 << m)

        if response == "accepted":
            l = m
        else:
            r = m

    for i in range(l, -1, -1):
        ask(1 << i)

    print("finish", flush=True)

if __name__ == "__main__":
    solve()
```

The `ask` function is the only place where communication with the interactor happens. It prints a withdrawal command, flushes immediately as required by the protocol, and reads the response. The `fail` response causes immediate termination because continuing after the terminal has locked is explicitly forbidden.

The binary search uses exponents rather than the monetary values themselves. The interval contains the integers from 0 through 59, so every requested amount is at most (2^{59}<10^{18}). Python integers do not overflow, but the same implementation in C++ would also fit comfortably in a signed 64-bit integer for every actual query.

The final loop deliberately starts at `l`, not `l + 1` or 59. Some powers may already have been withdrawn during the binary search, so they can be rejected when queried again. That is harmless. Since the balance only decreases, a previously successful withdrawal can never become successful a second time.

The program does not try to detect zero from an `accepted` response. There is no way to distinguish between an account containing exactly (x) and one containing more than (x) after an accepted `withdraw x`. Continuing with the predetermined strategy avoids that ambiguity.

## Worked Examples

The interactive samples are transcripts rather than ordinary input files. Sample 1 is consistent with an initial balance of 1: `withdraw 42` is rejected, `withdraw 1` is accepted, and the second `withdraw 1` is rejected because the balance is already zero. Sample 2 is consistent with an initial balance of 0.

For Sample 1, the optimal algorithm does not have to reproduce the sample transcript. Its six queries for (n=1) are shown below.

| Step | Exponent | Withdrawal | Response | Remaining balance |
| --- | --- | --- | --- | --- |
| 1 | 30 | (2^{30}) | rejected | 1 |
| 2 | 15 | (2^{15}) | rejected | 1 |
| 3 | 7 | (2^7) | rejected | 1 |
| 4 | 3 | (2^3) | rejected | 1 |
| 5 | 1 | (2^1) | rejected | 1 |
| 6 | 0 | (2^0) | accepted | 0 |

The binary search ends with (l=0), and the final scan removes the single dollar. The algorithm then prints `finish`. The sample's shorter transcript is simply another valid interaction for the same hidden balance.

For Sample 2, the initial balance is zero.

| Step | Exponent | Withdrawal | Response | Remaining balance |
| --- | --- | --- | --- | --- |
| 1 | 30 | (2^{30}) | rejected | 0 |
| 2 | 15 | (2^{15}) | rejected | 0 |
| 3 | 7 | (2^7) | rejected | 0 |
| 4 | 3 | (2^3) | rejected | 0 |
| 5 | 1 | (2^1) | rejected | 0 |
| 6 | 0 | (2^0) | rejected | 0 |

The search again finishes with (l=0). The final query confirms that no dollar can be withdrawn, and `finish` is correct. Only six attempts are used, below the (q+10=10) limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(q)) interactive queries | At most 6 binary-search queries plus at most (q+1) final queries |
| Space | (O(1)) | Only a constant number of integer variables is stored |

Since (n\le10^{18}<2^{60}), we always have (q\le60). The algorithm therefore uses at most 67 withdrawal attempts, while the protocol allows (q+10), which is at least 10 and reaches 70 for the largest possible logarithmic range. The implementation uses constant memory.

## Test Cases

Because this is interactive, the ordinary Codeforces input cannot be reproduced by a conventional offline `run(input_string)` helper. The useful way to test the logic locally is to replace the interactor with a simulator holding a hidden balance. The same `strategy` function is then used both by the real solution and by the test harness.

```python
import sys

def strategy(ask, finish):
    l, r = 0, 60

    while r - l > 1:
        m = (l + r) // 2
        response = ask(1 << m)

        if response == "accepted":
            l = m
        elif response == "rejected":
            r = m
        else:
            raise RuntimeError("unexpected interactor response")

    for i in range(l, -1, -1):
        ask(1 << i)

    finish()

def run_hidden(n):
    balance = n
    commands = []

    def ask(x):
        nonlocal balance
        assert 1 <= x <= 10**18

        commands.append(f"withdraw {x}")

        if balance >= x:
            balance -= x
            return "accepted"
        return "rejected"

    def finish():
        commands.append("finish")
        assert balance == 0

    strategy(ask, finish)
    return commands, balance

def check_sample_transcript(n, commands, replies):
    balance = n

    assert len(commands) == len(replies)

    for command, reply in zip(commands, replies):
        parts = command.split()

        if parts[0] == "withdraw":
            x = int(parts[1])
            expected = "accepted" if balance >= x else "rejected"

            assert reply == expected

            if expected == "accepted":
                balance -= x

        elif command == "finish":
            assert balance == 0
        else:
            raise AssertionError("invalid command")

    assert balance == 0

# Provided Sample 1.
sample1_commands = [
    "withdraw 42",
    "withdraw 1",
    "withdraw 1",
]
sample1_replies = [
    "rejected",
    "accepted",
    "rejected",
]
check_sample_transcript(1, sample1_commands, sample1_replies)

# Provided Sample 2.
sample2_commands = [
    "withdraw 1",
]
sample2_replies = [
    "rejected",
]
check_sample_transcript(0, sample2_commands, sample2_replies)

# Minimum balance.
commands, balance = run_hidden(0)
assert balance == 0
assert commands[-1] == "finish"
assert len(commands) <= 10

# Small boundary values.
commands, balance = run_hidden(1)
assert balance == 0
assert commands[-1] == "finish"

commands, balance = run_hidden(2)
assert balance == 0
assert commands[-1] == "finish"

commands, balance = run_hidden(3)
assert balance == 0
assert commands[-1] == "finish"

# Exact power of two near the upper range.
commands, balance = run_hidden(1 << 59)
assert balance == 0
assert commands[-1] == "finish"
assert len(commands) <= 59 + 10

# Maximum allowed balance.
commands, balance = run_hidden(10**18)
assert balance == 0
assert commands[-1] == "finish"
assert len(commands) <= 60 + 10

# Repeated equal hidden balances catch accidental state leakage.
results = [run_hidden(42) for _ in range(3)]
assert all(balance == 0 for _, balance in results)
assert results[0][0] == results[1][0] == results[2][0]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 transcript, hidden (n=1) | `finish`, balance 0 | Successful withdrawal followed by a redundant rejected query |
| Sample 2 transcript, hidden (n=0) | `finish`, balance 0 | Minimum balance and immediate zero state |
| (n=0) | `finish`, balance 0 | Smallest possible (q) and strict query budget |
| (n=1,2,3) | `finish`, balance 0 | Lowest nonzero balances and bit-boundary behavior |
| (n=2^{59}) | `finish`, balance 0 | Highest relevant power of two |
| (n=10^{18}) | `finish`, balance 0 | Maximum allowed balance and (q=60) |
| (n=42) repeated three times | `finish`, balance 0 each time | State isolation and deterministic interaction |

## Edge Cases

The zero balance is handled by the search naturally. For `withdraw 1` with (n=0), the answer is `rejected`, and every later withdrawal is also rejected. The binary search eventually reaches (l=0), the final scan performs one more `withdraw 1`, and `finish` is valid. The complete interaction uses only six attempts, while the protocol allows ten.

For (n=1), the binary search rejects every tested power above one. The final scan starts at exponent zero, so `withdraw 1` succeeds and leaves zero. The algorithm then finishes. The crucial boundary is that exponent zero is included in the final loop. Starting from one would miss the only dollar.

For an exact power such as (n=2^5=32), a binary-search query can successfully withdraw 32 and leave zero. Later queries are all rejected. The final scan remains safe because rejected withdrawals do nothing. This demonstrates why the solution must not assume that an `accepted` response means the balance is now zero.

For the maximum balance (n=10^{18}), we have (2^{59}<10^{18}<2^{60}), so (q=60). Every query uses an exponent below 60, and the binary search needs at most six attempts. Even if (l=59), the final scan needs only 60 more attempts, giving at most 66 or 67 total depending on the exact search path, below the allowed 70.

The most subtle case is when accepted queries alter the balance during binary search. Suppose (n=100). A query for 8 can succeed, reducing the balance to 92. A later query for 32 can also succeed, reducing it to 60, while a query for 64 is then rejected. The responses cannot be interpreted as comparisons with the original 100. What remains valid is the weaker statement needed by the algorithm: the final rejected boundary proves that the current balance is smaller than the next power above (l). The final descending scan then removes the remaining binary representation without relying on the original balance being unchanged.
