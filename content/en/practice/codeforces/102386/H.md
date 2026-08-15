---
title: "CF 102386H - \u0421\u0432\u0435\u0442\u043e\u0444\u043e\u0440\u044b"
description: "There are two traffic-light countdowns, initially showing (A) and (B). After every second, both values decrease by one. We are interested only in moments when both counters are still positive, because as soon as one reaches zero, the red-light period ends."
date: "2026-08-15T18:48:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102386
codeforces_index: "H"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b\u0430 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u043c\u0438\u0440\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2019"
rating: 0
weight: 102386
solve_time_s: 730
verified: false
draft: false
---

[CF 102386H - \u0421\u0432\u0435\u0442\u043e\u0444\u043e\u0440\u044b](https://codeforces.com/problemset/problem/102386/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 12m 10s  
**Verified:** no  

## Solution
## Problem Understanding

There are two traffic-light countdowns, initially showing (A) and (B). After every second, both values decrease by one. We are interested only in moments when both counters are still positive, because as soon as one reaches zero, the red-light period ends.

At such a moment, the two current values are considered good if one is an integer multiple of the other. We need to count all good moments before either counter reaches zero.

Suppose (A \le B). After (t) seconds, the counters are

[
A-t,\qquad B-t.
]

The process is valid for (t=0,1,\ldots,A-1), so there can be as many as (10^9) moments. A direct simulation would consequently require up to (10^9) iterations, which is far beyond what a competitive programming solution can afford. The values themselves also fit comfortably in a 32-bit signed integer, but intermediate products are unnecessary, and Python's arbitrary-precision integers remove any overflow concern anyway.

The main edge cases are caused by equality and by the fact that the moment when a counter becomes zero must not be counted. For example, with input `1 1`, the only red-light moment is the initial state `(1, 1)`, so the answer is `1`. A loop that starts after the first second would incorrectly return zero. With input `2 3`, the states are `(2,3)` and then `(1,2)`. Only `(1,2)` qualifies, so the answer is `1`. A careless implementation that also examines the state `(0,1)` would incorrectly count a state after the red period has ended.

Equality is another special case. For `5 5`, both counters are equal at every valid moment: `(5,5)`, `(4,4)`, `(3,3)`, `(2,2)`, `(1,1)`. Every one qualifies, so the answer is `5`. Treating the difference (B-A=0) like an ordinary divisor-counting problem would fail because every positive integer divides zero, and the answer is bounded by the shorter countdown instead.

## Approaches

A straightforward solution simulates every second. At time (t), it computes the two remaining values and checks whether either divides the other. This is correct because every possible red-light moment is visited exactly once, and the divisibility test is exactly the condition from the problem.

The problem is the number of moments. If one countdown starts at (1) and the other at (10^9), only one moment needs to be checked, but if both start near (10^9), almost (10^9) states may need to be examined. In the worst case, such as `1000000000 1000000000`, the simulation performs (10^9) iterations, which is too slow.

The key observation is that subtracting the same amount from both counters preserves their difference. Assume (A \le B), and define

[
d=B-A.
]

After (t) seconds the counters are

[
x=A-t,\qquad x+d=B-t.
]

The smaller counter is (x), and the larger one is (x+d). If (d>0), the larger value can never divide the smaller positive value. Thus the only possible condition is

[
x \mid (x+d).
]

Since (x\mid x), this is equivalent to

[
x\mid d.
]

This changes the problem completely. Instead of checking every second, we only need to count positive divisors of (d) that are at most the smaller initial countdown.

The difference (d) is at most (10^9-1), so all of its divisors can be counted by checking possible divisor pairs up to (\sqrt d). There are at most about (31623) such candidates, which is tiny compared with (10^9).

When (A=B), the difference is zero and the previous reduction becomes degenerate. In that case the counters are equal at every valid moment, so every moment qualifies and the answer is simply (A).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(\min(A,B))) | (O(1)) | Too slow |
| Optimal | (O(\sqrt{ | A-B | })) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Let (m=\min(A,B)) and (M=\max(A,B)). The smaller counter determines how many positive states remain before one light turns green.
2. If (A=B), return (A). The two counters stay equal throughout the entire red-light period, so every one of the (A) states is valid.
3. Otherwise compute the positive difference (d=M-m). At any valid moment, write the smaller current counter as (x). The other counter is then (x+d).
4. A valid state requires one counter to divide the other. Since (x<x+d), only (x\mid x+d) can hold. Subtracting (x) from the larger number gives the equivalent condition (x\mid d).
5. The smaller current counter takes every integer value from (m) down to (1). Consequently, the answer is exactly the number of positive divisors of (d) that do not exceed (m).
6. Enumerate integers (i) from (1) through (\lfloor\sqrt d\rfloor). Whenever (i) divides (d), both (i) and (d/i) are divisors. Count each one if it is at most (m), taking care not to count the same divisor twice when (i^2=d).
7. Print the accumulated count.

### Why it works

At every valid moment with (A\ne B), let (x) be the smaller remaining counter. The other counter is exactly (x+d), where (d=|A-B|) never changes. Because (x<x+d), the divisibility condition can only be (x\mid x+d), which is equivalent to (x\mid d). During the red-light period, (x) takes every positive integer from (\min(A,B)) down to (1), exactly once. Thus there is a one-to-one correspondence between valid moments and divisors of (d) that are at most (\min(A,B)). The divisor enumeration counts exactly those values, so the result is correct.

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

if __name__ == "__main__":
    solve()
```

The first three variables reduce the input to the smaller countdown (m) and the fixed difference (d). Using `abs(A - B)` makes the code independent of which original counter is larger.

The equality case is handled before divisor enumeration. When `d == 0`, every positive state has equal counters, so returning `m` directly avoids treating zero as though it had an ordinary finite set of divisors.

For the non-equal case, the loop only goes while `i * i <= d`. Every divisor below the square root has a complementary divisor above it, so checking one side finds both. The condition `other != i` prevents a square divisor from being counted twice.

The comparison with `m` is necessary because not every divisor of the difference corresponds to a state that actually occurs. The smaller current counter never exceeds its initial value, so only divisors at most `m` can represent valid moments.

There is no off-by-one issue involving zero because the current smaller counter ranges from `m` down to `1`. The state with value zero is never represented by the divisor enumeration.

## Worked Examples

For Sample 1, the input is `3 30`. Here (m=3) and (d=27). The possible smaller counter values are (3,2,1). Only those dividing (27) correspond to valid moments.

| (i) | (i^2 \le d) | (i\mid d) | Divisor pair | Count after pair |
| --- | --- | --- | --- | --- |
| 1 | Yes | Yes | (1,27) | 1 |
| 2 | Yes | No | None | 1 |
| 3 | Yes | Yes | (3,9) | 2 |
| 4 | No | Not checked | Not checked | 2 |

The divisors no larger than (3) are (1) and (3), giving answer `2`. In terms of actual countdown states, these are `(1,28)` and `(3,30)`. The state `(2,29)` does not qualify.

For Sample 2, the input is `16 4`. Here (m=4) and (d=12). The smaller counter takes the values (4,3,2,1), and all four divide (12).

| (i) | (i^2 \le d) | (i\mid d) | Divisor pair | Count after pair |
| --- | --- | --- | --- | --- |
| 1 | Yes | Yes | (1,12) | 2 |
| 2 | Yes | Yes | (2,6) | 4 |
| 3 | Yes | Yes | (3,4) | 6 |
| 4 | No | Not checked | Not checked | 6 |

The pair enumeration finds six divisors in total, but only (1,2,3,4) are at most (m=4). Thus the answer is `4`. The corresponding valid states are `(16,4)`, `(15,3)`, `(14,2)`, and `(13,1)`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\sqrt{ | A-B | })) | At most (\lfloor\sqrt{ | A-B | }\rfloor) divisor candidates are examined. |
| Space | (O(1)) | Only a constant number of integer variables are stored. |

With (A,B\le10^9), the loop performs fewer than (31623) iterations in the worst non-equal case. That is comfortably small, while the brute-force method could require close to (10^9) iterations.

## Test Cases

```python
# helper: run the core solution on an input string
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        A, B = map(int, input().split())

        m = min(A, B)
        d = abs(A - B)

        if d == 0:
            print(m)
            return sys.stdout.getvalue()

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
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def run(inp: str) -> str:
    return solve_data(inp).strip()

# Provided samples
assert run("3 30\n") == "2", "sample 1"
assert run("16 4\n") == "4", "sample 2"

# Minimum-size input
assert run("1 1\n") == "1", "both counters start at the minimum"

# Equal values
assert run("5 5\n") == "5", "every equal state is valid"

# Difference is 1, so only divisor 1 can contribute
assert run("2 3\n") == "1", "off-by-one boundary around zero"

# A square difference, checking the i*i == d case
assert run("5 14\n") == "2", "difference 9 has divisors 1, 3, 9, only 1 and 3 fit"

# Maximum-size equal input
assert run("1000000000 1000000000\n") == "1000000000", "maximum equal values"

# Large asymmetric input, only divisor 1 is within the smaller countdown
assert run("1 1000000000\n") == "1", "only the initial state can qualify"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum values and the equal-counter special case |
| `5 5` | `5` | Every valid moment qualifies when the counters are equal |
| `2 3` | `1` | Difference (1) and exclusion of the zero state |
| `5 14` | `2` | Square divisor handling and the upper bound (x\le m) |
| `1000000000 1000000000` | `1000000000` | Maximum input values without simulation |
| `1 1000000000` | `1` | Large difference with only one usable divisor |

## Edge Cases

For `1 1`, the algorithm computes (m=1) and (d=0). It immediately returns (m=1), matching the single valid state `(1,1)`. This handles both the minimum input size and the special meaning of zero difference.

For `2 3`, we have (m=2) and (d=1). The only positive divisor of (1) is `1`, and it is at most `2`, so the answer is `1`. The actual states are `(2,3)` and `(1,2)`, and only the second state has one counter dividing the other. The following state would be `(0,1)`, but it is outside the red-light period and is never considered.

For `5 5`, the difference is zero, so the algorithm returns `5` immediately. The five states `(5,5)`, `(4,4)`, `(3,3)`, `(2,2)`, and `(1,1)` are all valid. This is why the equal case cannot be passed through the ordinary divisor-counting formula.

For `5 14`, the difference is (9), whose divisors are (1,3,9). The smaller counter can only be (5,4,3,2,1), so only `1` and `3` correspond to actual moments. The answer is `2`. This case also checks the divisor-pair logic because (9) is a perfect square and the divisor `3` must be counted exactly once.

For `1000000000 1000000000`, the difference is zero and the answer is exactly `1000000000`. The algorithm produces this immediately instead of attempting a billion-step simulation, which demonstrates why the equal case needs to be handled directly.
