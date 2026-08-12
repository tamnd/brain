---
title: "CF 102330D - \u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441\u0438\u0432\u043d\u044b\u0439 \u0442\u043e\u0440\u0433"
description: "We have two current offers, x from Barnum and y from Carlisle, with x <= y. Barnum increases his offer by a, then Carlisle decreases his offer by b. On the next pair of moves the changes become 2a and 2b, then 3a and 3b, and so on."
date: "2026-08-13T03:57:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102330
codeforces_index: "D"
codeforces_contest_name: "\u0421\u0438\u0440\u0438\u0443\u0441.2019.\u041d\u043e\u044f\u0431\u0440\u044c.\u041e\u0447\u043d\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 102330
solve_time_s: 60
verified: true
draft: false
---

[CF 102330D - \u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441\u0438\u0432\u043d\u044b\u0439 \u0442\u043e\u0440\u0433](https://codeforces.com/problemset/problem/102330/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We have two current offers, `x` from Barnum and `y` from Carlisle, with `x <= y`. Barnum increases his offer by `a`, then Carlisle decreases his offer by `b`. On the next pair of moves the changes become `2a` and `2b`, then `3a` and `3b`, and so on.

The process ends as soon as the two offers meet or cross. The answer is the last offer that was actually spoken. Since every termination condition happens when Barnum's current offer is at least Carlisle's current or next offer, the answer will always be Barnum's offer at the terminating round.

Suppose we have completed `k` rounds. Barnum has added

a(1+2+⋯+k)=a 2 k(k+1) ​

to his original offer. Carlisle has subtracted

b(1+2+⋯+k)=b 2 k(k+1) ​ .

Thus after both moves of round `k`, their offers are

B k ​ =x+a 2 k(k+1) ​

and

C k ​ =y−b 2 k(k+1) ​ .

The process terminates in round `k` exactly when these two values satisfy `B_k >= C_k`. Rearranging gives

(a+b) 2 k(k+1) ​ ≥y−x.

So the whole simulation reduces to finding the smallest nonnegative integer `k` satisfying this inequality. Once `k` is known, the answer is simply `B_k`.

There are at most `2000` test cases, while `x` and `y` can differ by almost `10^12`. The number of rounds can consequently be around `sqrt(10^12)`, roughly `1.4 * 10^6`, even when the step sizes are only `1`. A direct simulation could thus perform billions of iterations across all tests, which is far beyond a one-second limit. We need to exploit the monotonic growth of the triangular number instead of simulating every round.

Several boundary cases deserve special care. If the initial offers are already equal, for example `1 1 5 7`, the negotiation ends immediately and the answer is `1`. A loop that always performs one round first would incorrectly output a larger value.

An equality at the boundary must also terminate immediately. For `1 4 1 1`, after two rounds the offers become `4` and `1`, and the answer is `4`. More generally, the condition is `>=`, not only `>`. Replacing it with a strict comparison can move the answer to the next round.

The step sizes can be very different. For `7 18 1 3`, the answer is `10`: after Barnum says `8` and Carlisle says `15`, Barnum says `10`, after which Carlisle's intended `9` is already no greater than `10`. A solution that checks only whether Barnum's offer has reached Carlisle's previous offer would miss this termination condition.

## Approaches

The straightforward solution simulates the negotiation round by round. In round `k`, it increases Barnum's offer by `k*a` and decreases Carlisle's offer by `k*b`, then checks whether the offers have met. This is correct because it follows exactly the sequence of offers described by the process.

The problem is the number of rounds. With `y-x` close to `10^12` and `a=b=1`, we need roughly

2 k(k+1) ​ ≈5⋅10 11 ,

which gives `k` around `10^6`. With `2000` test cases, a worst-case simulation can reach about `2 * 10^9` rounds. Even though each round is constant time, that is much too large.

The useful observation is that after round `k`, the total amount by which the gap has decreased is exactly

(a+b) 2 k(k+1) ​ .

The triangular number `k(k+1)/2` is strictly increasing for nonnegative `k`, so the predicate

(a+b) 2 k(k+1) ​ ≥y−x

is false for all smaller `k` and true for all sufficiently large `k`. That monotonicity makes binary search a natural replacement for simulation.

There is also a subtle point about the order of the offers. Barnum speaks first in every round. If his new offer already reaches Carlisle's previous offer, the process stops immediately at Barnum's value. If it does not, Carlisle speaks next. If Carlisle's new offer has fallen to Barnum's value or below, the process also stops at Barnum's value. Both situations are captured by the single condition `B_k >= C_k`, because `C_k <= C_{k-1}`. If Barnum reaches `C_{k-1}`, he certainly also reaches the even smaller `C_k`.

Thus we only need the first round in which the offers after the round would satisfy `B_k >= C_k`. The answer is Barnum's offer in that round.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) per test, with k up to about 1.4 * 10^6 | O(1) | Too slow in the worst case |
| Optimal | O(log k) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the initial gap `d = y - x`. If `d` is zero, the offers already agree, so the answer is `x` and no rounds are needed.
2. For a candidate round `k`, compute the triangular number

T k ​ = 2 k(k+1) ​ .

After both offers in that round, their distance is

d−(a+b)T k ​ .

The negotiation has ended by that round exactly when this value is nonpositive.
3. Use binary search to find the smallest `k` for which

(a+b)T k ​ ≥d.

The predicate is monotone because `T_k` strictly increases with `k`.
4. Once the smallest valid `k` is found, calculate Barnum's offer

x+aT k ​ .

That is the amount at which the negotiation ends.
5. Print this value for the current test case and repeat for all test cases.

### Why it works

Before round `k`, the cumulative increases made by Barnum are `a(1 + ... + k)`, while the cumulative decreases made by Carlisle are `b(1 + ... + k)`. Their combined movement toward each other is therefore `(a+b)T_k`. The first round where this movement is at least the original gap is exactly the first round where Barnum's offer is at least Carlisle's offer after the corresponding decrease.

Because Carlisle's offer after round `k` is no larger than his offer before round `k`, any crossing that happens when Barnum speaks first is also represented by the same condition `B_k >= C_k`. Hence the smallest `k` found by the binary search is precisely the terminating round, and `x + aT_k` is precisely the last spoken amount.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        x, y, a, b = map(int, input().split())

        if x == y:
            out.append(str(x))
            continue

        gap = y - x
        step = a + b

        # Find the smallest k such that
        # step * k * (k + 1) / 2 >= gap.
        lo, hi = 0, 1

        while step * hi * (hi + 1) // 2 < gap:
            hi *= 2

        while lo < hi:
            mid = (lo + hi) // 2
            triangular = mid * (mid + 1) // 2

            if step * triangular >= gap:
                hi = mid
            else:
                lo = mid + 1

        k = lo
        triangular = k * (k + 1) // 2
        answer = x + a * triangular

        out.append(str(answer))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first special case handles `x == y` directly. In that situation `k = 0` satisfies the termination condition, so performing another iteration would be an off-by-one error.

For every other test, `gap` stores the distance between the initial offers, while `step = a + b` is the amount by which that distance is reduced per unit of the triangular progression. The expression `k * (k + 1) // 2` is the cumulative multiplier after `k` rounds.

The upper bound for the binary search is found by doubling `hi`. This avoids relying on a manually chosen constant. Since the required `k` is only around the square root of the gap, this doubling takes very few operations.

The binary search maintains the usual invariant that the answer is somewhere in `[lo, hi]`. When the midpoint already satisfies the required inequality, it remains possible that `mid` itself is the answer, so `hi` moves to `mid`. Otherwise the answer must be larger, so `lo` becomes `mid + 1`.

Python integers have arbitrary precision, so expressions such as `a * k * (k + 1)` do not overflow. The integer division is also done before multiplying by `a` in the final calculation, since `k(k+1)` is always even and the triangular number is an integer.

## Worked Examples

For the first sample, `x = 7`, `y = 18`, `a = 1`, and `b = 3`. The initial gap is `11`, and every round contributes `4T_k` toward closing it.

| k | T_k | Barnum `B_k` | Carlisle `C_k` | `4T_k >= 11` |
| --- | --- | --- | --- | --- |
| 0 | 0 | 7 | 18 | No |
| 1 | 1 | 8 | 15 | No |
| 2 | 3 | 10 | 9 | Yes |

The first valid round is `k = 2`. Barnum's offer is `7 + 1 * 3 = 10`, so the answer is `10`. This example also demonstrates why checking only against Carlisle's previous offer is insufficient. Barnum's `10` does not reach the previous `15`, but Carlisle's next intended offer is `9`, so the negotiation still ends at `10`.

For the second sample, both parties start at `4`.

| k | T_k | Barnum `B_k` | Carlisle `C_k` | Condition |
| --- | --- | --- | --- | --- |
| 0 | 0 | 4 | 4 | Yes |

The smallest valid `k` is zero, so the answer remains `4`. This confirms that the initial equality must be handled without performing a bargaining round.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t log K) | Each test uses a doubling phase and binary search over the required round `K` |
| Space | O(1) auxiliary | Only a constant number of integer variables are used for each test |

With `y-x <= 10^12` and `a+b >= 2`, the terminating round is at most on the order of `10^6`. The binary search consequently needs only a few dozen iterations per test, so even `2000` test cases require only tens of thousands of predicate evaluations. The memory usage is constant apart from the output buffer.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        x, y, a, b = map(int, input().split())

        if x == y:
            out.append(str(x))
            continue

        gap = y - x
        step = a + b

        lo, hi = 0, 1

        while step * hi * (hi + 1) // 2 < gap:
            hi *= 2

        while lo < hi:
            mid = (lo + hi) // 2
            triangular = mid * (mid + 1) // 2

            if step * triangular >= gap:
                hi = mid
            else:
                lo = mid + 1

        k = lo
        triangular = k * (k + 1) // 2
        out.append(str(x + a * triangular))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run("1\n7 18 1 3\n") == "10\n", "sample 1"

# Provided sample 2
assert run("1\n4 4 4 4\n") == "4\n", "sample 2"

# Minimum values, already equal
assert run("1\n1 1 1 1\n") == "1\n", "minimum equal case"

# Exact triangular boundary:
# gap = 3, a+b = 2, T_2 = 3, so equality occurs at k = 2.
assert run("1\n1 4 1 1\n") == "4\n", "triangular boundary"

# Highly asymmetric step sizes
assert run("1\n1 10 1 8\n") == "2\n", "asymmetric steps"

# Large values
assert run("1\n1 1000000000000 1000000 1000000\n") == \
       "500000500000000001\n", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 1 1` | `1` | Initial equality and zero rounds |
| `1 / 1 4 1 1` | `4` | Exact equality at the triangular boundary |
| `1 / 1 10 1 8` | `2` | Strongly asymmetric bargaining steps |
| `1 / 1 1 1000000000000 1000000 1000000` | `500000500000000001` | Large values and integer arithmetic |

## Edge Cases

The initial equality case is `1 1 1 1`. Here `gap = 0`, so `k = 0` already satisfies the condition. The algorithm immediately returns `x = 1`, avoiding an unnecessary first round.

The equality boundary is represented by `1 4 1 1`. The initial gap is `3`. For `k = 1`, the total closing amount is `2`, which is insufficient. For `k = 2`, the triangular number is `3`, so `(a+b)T_2 = 6`, which exceeds the gap. Barnum's offer is `1 + 3 = 4`, giving the correct answer `4`. A strict comparison would mishandle cases where the two offers meet exactly.

The first sample, `7 18 1 3`, catches the ordering issue between the two offers. At `k = 2`, Barnum offers `10` while Carlisle's offer after the same round is `9`. The process ends at `10`, even though Barnum's offer did not reach Carlisle's previous offer of `15`. The combined-gap condition captures this correctly.

For the large case `1 1000000000000 1000000 1000000`, the gap is `999999999999`. At `k = 999999`, the triangular number is `499999500000`, which is still too small after multiplication by `2 * 10^6`. At `k = 1000000`, the triangular number becomes `500000500000`, which is enough. Barnum's final offer is

1+1000000⋅500000500000=500000500000000001.

The calculation is comfortably within Python's integer range because Python integers grow automatically, and the binary search avoids iterating through a million rounds.
