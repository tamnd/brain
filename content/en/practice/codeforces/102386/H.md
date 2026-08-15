---
title: "CF 102386H - \u0421\u0432\u0435\u0442\u043e\u0444\u043e\u0440\u044b"
description: "At the intersection there are two countdowns, initially showing (A) and (B). Every second, both values decrease by one. We only consider moments while both lights are still red, so neither counter has reached zero yet."
date: "2026-08-15T07:41:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102386
codeforces_index: "H"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b\u0430 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u043c\u0438\u0440\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2019"
rating: 0
weight: 102386
solve_time_s: 161
verified: false
draft: false
---

[CF 102386H - \u0421\u0432\u0435\u0442\u043e\u0444\u043e\u0440\u044b](https://codeforces.com/problemset/problem/102386/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 41s  
**Verified:** no  

## Solution
## Problem Understanding

At the intersection there are two countdowns, initially showing (A) and (B). Every second, both values decrease by one. We only consider moments while both lights are still red, so neither counter has reached zero yet.

At a particular moment (t), the counters show

[
A-t,\qquad B-t.
]

We need to count how many such moments have the property that one displayed number is an integer multiple of the other. The initial moment (t=0) is included.

Since (A,B\le 10^9), simulating every second can require up to (10^9) iterations. That is far beyond what a typical competitive-programming time limit allows. We need to exploit the fact that both counters decrease by exactly the same amount, so their difference never changes.

There are several small cases where a direct implementation can go wrong. For (A=B=1), the only red moment is ((1,1)), so the answer is (1). A solution that starts checking only after the first decrement would incorrectly return (0). For (A=1,B=2), the only valid moment is ((1,2)), so the answer is also (1). The moment when the smaller counter becomes zero must not be included. Finally, for (A=B=5), every state ((5,5),(4,4),\ldots,(1,1)) qualifies, giving (5), so equality needs to be handled separately rather than trying to find divisors of a zero difference.

## Approaches

The straightforward approach is to simulate the countdown. At every second, let the current values be (x) and (y), check whether (x) divides (y) or (y) divides (x), then decrement both counters. This is correct because it examines every possible red state exactly once. However, if one counter starts at (10^9), the simulation performs almost (10^9) iterations, which is too slow.

The useful structure appears when we write the state after (t) seconds as (A-t) and (B-t). Their difference is always

[
(B-t)-(A-t)=B-A.
]

Assume for the moment that (A\le B). Put (x=A-t). The other counter is then (x+(B-A)). The condition that the two numbers differ by an integer factor is equivalent to

[
x+(B-A)\equiv 0\pmod{x}.
]

Since (x\equiv0\pmod{x}), this reduces to

[
B-A\equiv0\pmod{x}.
]

So every valid moment corresponds exactly to a positive divisor (x) of the fixed difference (B-A). During the red period, (x) takes every integer value from (A) down to (1). Consequently, we only need to count divisors of (|A-B|) that are at most (\min(A,B)).

If (A=B), the difference is zero and every state has equal counters, so the answer is simply (A). Otherwise, we can enumerate the divisors of (|A-B|) in (O(\sqrt{|A-B|})) time. Whenever (i) divides the difference, both (i) and (|A-B|/i) are divisors, and we count each one if it is at most (\min(A,B)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(\min(A,B))) | (O(1)) | Too slow |
| Optimal | (O(\sqrt{ | A-B | })) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Let (m=\min(A,B)) and (d=|A-B|). The smaller counter starts at (m) and decreases through every value (m,m-1,\ldots,1) while both lights remain red.
2. If (d=0), return (m). The counters are equal at every red moment, and equal positive numbers are integer multiples of each other with ratio (1).
3. Otherwise, enumerate integers (i) from (1) through (\lfloor\sqrt d\rfloor). Whenever (i) divides (d), (i) is one divisor and (d/i) is its paired divisor.
4. Count (i) when (i\le m). Also count (d/i) when (d/i\le m), provided the two divisors are different.
5. Output the accumulated count. Every counted divisor represents exactly one value of the smaller counter, hence exactly one valid moment.

The key invariant is that the smaller counter takes each positive value from (m) down to (1) exactly once. For such a value (x), the larger counter is (x+d), and (x) divides (x+d) exactly when (x) divides (d). Thus the algorithm counts precisely the valid states and no others.

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
            j = d // i

            if i <= m:
                ans += 1

            if j != i and j <= m:
                ans += 1

        i += 1

    print(ans)

solve()
```

The first three variables reduce the original countdown to the two quantities that matter: the largest possible value of the smaller counter, (m), and the fixed difference (d).

The (d=0) branch is necessary because zero does not have a finite set of positive divisors. More importantly, when the counters are equal, every red state is valid, so handling equality directly is both simpler and mathematically correct.

For (d>0), the loop only reaches (\sqrt d). When (i) divides (d), the paired divisor (j=d/i) is obtained immediately, so there is no need to scan all possible counter values.

The condition `j != i` prevents a square number from being counted twice. For example, if (d=16) and (i=4), both divisor expressions produce (4), but it represents only one possible counter value.

Python integers do not overflow, and (i*i) is at most roughly (10^9) inside the loop, so the arithmetic is safe. The upper boundary is also correct: if the smaller counter is (m), that initial state is still red and must be considered, while the state after (m) seconds has a zero counter and must not be considered.

## Worked Examples

For (A=3,B=30), the fixed difference is (27), and the smaller counter ranges from (3) to (1).

| (i) | (d/i) | Divisor (i\le m) | Divisor (d/i\le m) | Answer |
| --- | --- | --- | --- | --- |
| 1 | 27 | Yes | No | 1 |
| 2 | not a divisor | No | No | 1 |
| 3 | 9 | Yes | No | 2 |
| 4 | loop ends |  |  | 2 |

The relevant divisors of (27) are (1,3,9,27), but only (1) and (3) are at most (m=3). They correspond to the states ((1,28)) and ((3,30)). The answer is (2).

For (A=16,B=4), the fixed difference is (12), and the smaller counter ranges from (4) down to (1).

| (i) | (d/i) | Divisor (i\le m) | Divisor (d/i\le m) | Answer |
| --- | --- | --- | --- | --- |
| 1 | 12 | Yes | No | 1 |
| 2 | 6 | Yes | No | 2 |
| 3 | 4 | Yes | Yes | 4 |

The divisors of (12) not exceeding (4) are (1,2,3,4). They correspond to the four valid states where the smaller counter is (1,2,3,) or (4). The answer is (4).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\sqrt{ | A-B | })) | We test divisibility only up to the square root of the nonzero difference. |
| Space | (O(1)) | Only a constant number of integer variables are stored. |

With (A,B\le10^9), the loop executes at most about (31623) iterations. That replaces a possible billion-step simulation with a few tens of thousands of constant-time operations, while using constant memory.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    A, B = map(int, input().split())

    m = min(A, B)
    d = abs(A - B)

    if d == 0:
        print(m)
    else:
        ans = 0
        i = 1

        while i * i <= d:
            if d % i == 0:
                j = d // i

                if i <= m:
                    ans += 1

                if j != i and j <= m:
                    ans += 1

            i += 1

        print(ans)

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

def run(inp: str) -> str:
    return solve_data(inp)

assert run("3 30\n") == "2\n", "sample 1"
assert run("16 4\n") == "4\n", "sample 2"

assert run("1 1\n") == "1\n", "minimum equal values"
assert run("1 2\n") == "1\n", "only initial state is valid"
assert run("5 5\n") == "5\n", "all states are equal"
assert run("4 7\n") == "2\n", "divisor boundary"
assert run("2 1000000000\n") == "2\n", "large difference"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum values and the zero-difference branch |
| `1 2` | `1` | Initial state is included, zero state is excluded |
| `5 5` | `5` | Every state is valid when the counters are equal |
| `4 7` | `2` | Divisors at the boundary (x\le\min(A,B)) |
| `2 1000000000` | `2` | Large values without linear simulation |

## Edge Cases

For `1 1`, we have (m=1) and (d=0). The equality branch immediately returns (m=1). The only red state is `(1, 1)`, so the result is correct.

For `1 2`, we have (m=1) and (d=1). The only divisor of (d) is (1), and it satisfies (1\le m), so the answer is (1). The state after one second would contain a zero and is outside the red period, so no additional state is counted.

For `5 5`, (d=0), so the algorithm returns (5). The five red states are `(5,5)`, `(4,4)`, `(3,3)`, `(2,2)`, and `(1,1)`. Treating zero as an ordinary divisor would be mathematically invalid and would also miss the fact that every state qualifies.

For `4 7`, (m=4) and (d=3). The positive divisors of (3) are (1) and (3), both at most (4), so the answer is (2). They correspond to the states `(4,7)` and `(1,4)`. The divisor (3) is paired with (1), and both must be counted because both values occur among the possible smaller-counter states.

For `2 1000000000`, the difference is (999999998), but the smaller counter can only be (2) or (1). The divisors relevant to those states are (1) and (2), and both divide the difference, giving answer (2). The algorithm finds this without attempting anything close to (10^9) countdown steps.
