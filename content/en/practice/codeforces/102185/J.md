---
title: "CF 102185J - \u041a\u043e\u0440\u043c\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u043e\u043a\u043e\u0434\u0438\u043b\u043e\u0432"
description: "We have an even amount of meat, N, and two crocodiles. Vasya chooses two positive integer piece sizes A and B. The total meat must consist of the same number of pieces of each size, so if there are m pieces of size A and m pieces of size B, then N = m(A + B)."
date: "2026-08-19T06:38:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102185
codeforces_index: "J"
codeforces_contest_name: "Southern Russia Open Championship \u2013 ContestSFedU 2019, Team Final."
rating: 0
weight: 102185
solve_time_s: 86
verified: true
draft: false
---

[CF 102185J - \u041a\u043e\u0440\u043c\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u043e\u043a\u043e\u0434\u0438\u043b\u043e\u0432](https://codeforces.com/problemset/problem/102185/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an even amount of meat, `N`, and two crocodiles. Vasya chooses two positive integer piece sizes `A` and `B`. The total meat must consist of the same number of pieces of each size, so if there are `m` pieces of size `A` and `m` pieces of size `B`, then

`N = m(A + B)`.

The pieces are thrown every `K` seconds in the order `A, B, A, B, ...`. A crocodile can catch a new piece only when it has finished its previous one. If both crocodiles are free at the same moment, the stronger crocodile gets the piece. Each kilogram takes exactly one second to eat.

We need to output any positive integers `A` and `B` for which the difference between the total amounts eaten by the two crocodiles is as small as possible.

The bound `N <= 10^9` immediately rules out enumerating all possible pairs of piece sizes. There can be on the order of `N^2` positive pairs, which is far beyond what a one-second solution can inspect. The key is that the answer depends only on how `K` compares with `N/2` and `N-1`, so the final algorithm needs only constant time and constant memory.

There are three boundary situations that a careless solution can mishandle. For `N = 4, K = 1`, choosing `A = B = 2` is optimal. The first piece is caught by the strong crocodile at time zero, but that crocodile is still eating when the second piece arrives at time one, so the weak crocodile gets it. A simulation that checks whether the crocodile finishes strictly before the next throw instead of allowing simultaneous finishing to count as available can get this case wrong.

For `N = 4, K = 2`, choosing `A = B = 2` does not balance the food. The strong crocodile finishes exactly when the second piece is thrown, so it is immediately eligible and catches that piece too. The optimal construction is `A = 3, B = 1`, giving the strong crocodile 3 kilograms and the weak crocodile 1 kilogram. The equality at the boundary is the source of the common off-by-one error.

For `N = 4, K = 3`, no piece can keep the strong crocodile busy until the second throw, because even the largest possible first piece has size at most 3. The construction `A = 1, B = 3` is valid, but the strong crocodile catches both pieces and eats all 4 kilograms. A solution that assumes the weak crocodile must receive some meat will incorrectly search for an impossible balance.

## Approaches

A direct brute-force solution can enumerate every positive pair `(A, B)`, reject pairs for which `A + B` does not divide `N`, and simulate all throws for every remaining pair. The simulation is correct because the state of each crocodile is completely determined by the time at which it last caught a piece and the size of that piece.

The problem is the number of candidates. If we simply enumerate all positive `A` and `B` with `A + B <= N`, there are

`1 + 2 + ... + (N - 1) = N(N - 1)/2`

ordered pairs, which is about `5 * 10^17` when `N = 10^9`. Even rejecting invalid pairs before simulation cannot make that approach viable.

The structure becomes much simpler once we look at the number `m` of pairs of pieces. Since `N = m(A+B)`, if `m >= 2`, then

`A + B <= N/2`.

This single inequality is decisive. When `K >= N/2`, every piece in such a construction has size at most `K`, so after catching a piece the strong crocodile is free by the next throw. Since the strong crocodile wins whenever it is free, it catches every piece.

Thus, when `K >= N/2`, any useful attempt to give meat to the weak crocodile must use `m = 1`. There are then exactly two pieces, of sizes `A` and `B`, with `A+B=N`. The first piece goes to the strong crocodile. The second can go to the weak crocodile only if the first piece is still being eaten at time `K`, which means `A > K`.

This reduces the entire optimization to choosing the smallest possible `A` satisfying `A > K`. That is `A = K+1`, giving `B = N-K-1`, whenever `K <= N-2`.

When `K < N/2`, there is an even better possibility. We can take one piece of each size with `A = B = N/2`. Since `A > K`, the strong crocodile is still busy when the second piece arrives. The weak crocodile catches it, so both crocodiles receive exactly `N/2` kilograms and the optimal difference is zero.

When `K >= N-1`, even the largest possible first piece in the two-piece construction cannot satisfy `A > K`, because `A <= N-1`. The weak crocodile cannot receive anything, so the unavoidable difference is `N`. We can use `A = 1, B = N-1`, which makes the strong crocodile eat everything.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compare `K` with `N/2`. If `K < N/2`, choose `A = B = N/2`. The first piece keeps the strong crocodile busy for more than `K` seconds, so the second piece goes to the weak crocodile. Both receive the same amount, which is the absolute minimum possible difference, zero.
2. If `K >= N/2`, consider whether `K < N-1`. In this range, choose `A = K+1` and `B = N-K-1`. The first piece lasts longer than `K` seconds, so the strong crocodile is busy when the second piece arrives. The weak crocodile receives the second piece. Since `A` is the smallest possible first piece that lasts beyond the next throw, this minimizes the resulting difference `A-B`.
3. If `K >= N-1`, choose `A = 1` and `B = N-1`. The strong crocodile finishes the first piece before the second throw and catches the second one as well. It eats all `N` kilograms, and no construction can give any meat to the weak crocodile, so this is optimal.

### Why it works

The central invariant is that whenever `A+B <= N/2` and `K >= N/2`, both possible piece sizes are at most `K`, so the strong crocodile is always free at the next throw. Consequently, every construction with at least two copies of each size feeds everything to the strong crocodile.

When `K < N/2`, the construction `A=B=N/2` gives difference zero, which cannot be improved. When `K >= N/2`, any construction that can feed the weak crocodile must have exactly one piece of each size, because all constructions with at least two pairs feed everything to the strong crocodile. With two pieces, the weak crocodile receives the second one exactly when `A>K`, so the smallest possible valid `A` is `K+1`. This minimizes `A-B`, proving that each branch returns an optimal construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, K = map(int, input().split())

    if 2 * K < N:
        A = N // 2
        B = N // 2
    elif K < N - 1:
        A = K + 1
        B = N - K - 1
    else:
        A = 1
        B = N - 1

    print(A, B)

solve()
```

The first branch uses `2 * K < N` instead of `K < N / 2`, avoiding floating-point arithmetic. Since `N` is even, `N/2` is an integer, and the strict inequality is exactly the condition that a piece of size `N/2` is still being eaten when the next piece arrives.

In the second branch, `A = K+1` is deliberately one larger than `K`. If we used `A = K`, the strong crocodile would finish the first piece exactly at the second throw and would be eligible to catch it. The problem explicitly says that simultaneous finishing and throwing allows the crocodile to attempt the new piece.

The expression `B = N-K-1` is positive precisely while `K < N-1`. That is why the second branch stops at `K = N-1`. In the last branch, `A = 1` and `B = N-1` are both positive and sum to `N`, so there is exactly one piece of each size.

All values are at most `10^9`, so Python integers easily handle every calculation. No simulation is necessary.

## Worked Examples

### Sample 1

For `N = 4` and `K = 3`, we have `2K = 6 >= 4` and `K >= N-1`. The last branch applies.

| N | K | Condition | A | B | Result |
| --- | --- | --- | --- | --- | --- |
| 4 | 3 | `K >= N-1` | 1 | 3 | Strong eats both |

At time zero, the strong crocodile catches the 1-kilogram piece. It finishes at time 1, well before the second throw at time 3. Both crocodiles are free then, so the strong crocodile wins the tie and catches the 3-kilogram piece. The amounts are 4 and 0, giving difference 4, which is unavoidable for this `K`.

The official sample uses `1 3`, so this construction also reproduces the sample output.

### Sample 2

For `N = 4` and `K = 1`, we have `2K = 2 < 4`, so the first branch applies.

| N | K | Condition | A | B | Result |
| --- | --- | --- | --- | --- | --- |
| 4 | 1 | `2K < N` | 2 | 2 | Strong gets A, weak gets B |

The strong crocodile catches the first 2-kilogram piece at time zero and will finish at time 2. The second piece arrives at time 1, while the strong crocodile is still occupied. The weak crocodile is free, so it catches that piece.

Each crocodile receives 2 kilograms, so the difference is zero. Since zero is the smallest possible difference, this construction is optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations and comparisons are performed. |
| Space | O(1) | Only `N`, `K`, `A`, and `B` are stored. |

The algorithm does not depend on the magnitude of `N` except through integer arithmetic, so even `N = 10^9` and `K = 10^9` require the same amount of work as the smallest test. It easily fits within the one-second time limit and the 256 MB memory limit.

## Test Cases

```python
# The tested solution logic is kept here as a function so that
# each assertion can run independently.

import sys
import io

def solve_case(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        N, K = map(int, sys.stdin.readline().split())

        if 2 * K < N:
            A = N // 2
            B = N // 2
        elif K < N - 1:
            A = K + 1
            B = N - K - 1
        else:
            A = 1
            B = N - 1

        return f"{A} {B}"
    finally:
        sys.stdin = old_stdin

# Provided samples
assert solve_case("4 3\n") == "1 3", "sample 1"
assert solve_case("4 1\n") == "2 2", "sample 2"

# Minimum-size input
assert solve_case("2 1\n") == "1 1", "minimum N"

# Balanced construction
assert solve_case("10 1\n") == "5 5", "zero-difference case"

# Exact boundary K = N/2
assert solve_case("6 3\n") == "4 2", "K = N/2"

# Exact boundary K = N-1
assert solve_case("10 9\n") == "1 9", "K = N-1"

# Maximum-size values
assert solve_case("1000000000 1000000000\n") == "1 999999999", "maximum values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1` | `1 1` | Minimum possible `N`, including the branch where `K = N-1`. |
| `10 1` | `5 5` | A zero-difference construction when `K < N/2`. |
| `6 3` | `4 2` | The strict boundary `K = N/2`, where equal pieces no longer work. |
| `10 9` | `1 9` | The strict boundary `K = N-1`, where `K+1` would make `B` zero. |
| `1000000000 1000000000` | `1 999999999` | Maximum input values and large integer arithmetic. |

## Edge Cases

For `N = 4, K = 1`, the algorithm takes `A = B = 2`. The first piece is eaten from time 0 through time 2, while the second arrives at time 1. The strong crocodile is therefore busy and the weak crocodile gets the second piece. The result is `2 2`, giving equal totals.

For `N = 4, K = 2`, the equality at the eating boundary changes the result. With `A = B = 2`, the strong crocodile finishes exactly when the second piece is thrown, so it catches that piece too. The algorithm instead selects `A = 3, B = 1`. The strong crocodile remains busy until time 3, while the weak crocodile catches the 1-kilogram piece at time 2. The resulting difference is 2, and no smaller positive difference is possible because any two-piece construction giving the second piece to the weak crocodile requires `A > 2`.

For `N = 4, K = 3`, we are in the `K >= N-1` branch and output `1 3`. The strong crocodile finishes the first piece at time 1, so both crocodiles are free at time 3. The strong crocodile wins the simultaneous attempt and eats the second piece as well. Since every possible first piece has size at most `N-1 = 3`, no first piece can keep the strong crocodile busy until time 3. The weak crocodile consequently cannot receive any meat, making difference `N` unavoidable.
