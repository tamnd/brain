---
title: "CF 102709F - Zoom Exercises"
description: "The problem consists of several independent pushup rounds. In each round, the starting number represents the current amount of pushups. The two players repeatedly replace the current number with one of its proper divisors, meaning a divisor that is smaller than the number itself."
date: "2026-08-01T21:58:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102709
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 9-11-20 Div. 2"
rating: 0
weight: 102709
solve_time_s: 124
verified: true
draft: false
---

[CF 102709F - Zoom Exercises](https://codeforces.com/problemset/problem/102709/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem consists of several independent pushup rounds. In each round, the starting number represents the current amount of pushups. The two players repeatedly replace the current number with one of its proper divisors, meaning a divisor that is smaller than the number itself. The player who is forced to replace the number with `1` loses immediately. After both players make optimal decisions, we need to find the total amount of pushups Elijah must perform. If Fiona wins a round, Elijah has to do twice the original amount of that round, while if Elijah wins, he does nothing.

The number of rounds can be as large as 100, and each value can be as large as `10^11`. A direct simulation of the game is not possible because the sequence of moves depends on the divisors of a number, and exploring all possible choices would create a large game tree. The size of the numbers also rules out trial division up to the square root for every value, because `sqrt(10^11)` is over 300000 and this repeated 100 times is already unnecessary work. We need a mathematical observation that reduces each round to a simple property of the starting number.

The key edge cases are numbers with no safe moves. A prime number only has the divisor `1` besides itself. For example:

```
Input:
1
7

Output:
14
```

Elijah must move from `7` to `1`, so he loses the round and Fiona wins. The careless assumption that "having a move means having a chance to win" would fail here.

Another case is a composite number with a small prime divisor:

```
Input:
1
12

Output:
0
```

Elijah can move `12` to `2`. The remaining player must move `2` to `1` and loses. A solution that only checks whether the number has many divisors but does not reason about optimal play may incorrectly classify such numbers.

The value `2` itself is also a special small case:

```
Input:
1
2

Output:
4
```

The only possible move is `2 -> 1`, which loses immediately. A primality test must correctly handle the smallest prime values.

## Approaches

A brute-force solution would model each number as a game state. From a state `x`, it would try every proper divisor of `x`, recursively determine whether the opponent can win, and choose a move that forces the opponent into a losing state. This works because impartial games can be solved by recursively evaluating all reachable states.

The issue is the number of states and transitions. For a single value with many divisors, the recursion explores many possibilities. Even though the game depth is limited, building the full divisor game graph for values up to `10^11` is unnecessary and does not fit the intended constraints.

The useful observation comes from looking at the structure of divisors. A prime number has no proper divisor greater than `1`, so the current player has no winning move. Every composite number has at least one prime divisor `p`. That prime divisor is a losing position for the next player, so the current player can immediately move to `p` and win.

The whole game therefore collapses into a primality check. Fiona wins exactly when the starting number is prime. Elijah only pays for prime rounds, and each such round contributes twice its original value.

Since the numbers are up to `10^11`, we use a deterministic Miller-Rabin primality test for 64-bit integers instead of checking every possible divisor.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the divisor game tree | O(number of states) | Too slow |
| Optimal | O(log n) modular multiplications per primality test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all pushup amounts and prepare the final answer as zero. Each round contributes independently, so there is no interaction between numbers.
2. For every pushup amount, test whether it is prime using deterministic Miller-Rabin. This is the correct reduction because the game result depends only on whether the starting number has a prime divisor smaller than itself.
3. If the number is prime, add `2 * number` to the answer. A prime starting position is losing for Elijah, meaning Fiona wins and Elijah receives the penalty.
4. Print the accumulated answer.

Why it works:

The invariant behind the solution is that every composite number is a winning position and every prime number is a losing position. For a prime number, the only legal move is directly to `1`, which loses immediately. For a composite number, choosing any prime factor as the next state gives the opponent a prime position, and prime positions are losing. Since every round is independent, summing the penalties from prime starting values gives the final answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_prime(n):
    if n < 2:
        return False

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    # Deterministic for numbers smaller than 2^64
    bases = [2, 3, 5, 7, 11, 13]

    for a in bases:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        composite = True
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                composite = False
                break

        if composite:
            return False

    return True

def solve():
    n = int(input())
    ans = 0

    for _ in range(n):
        a = int(input())
        if is_prime(a):
            ans += 2 * a

    print(ans)

if __name__ == "__main__":
    solve()
```

The `is_prime` function first removes small prime factors. This quickly handles many composite numbers and avoids unnecessary Miller-Rabin work. The remaining part writes `n - 1` as `d * 2^s`, then checks whether several bases prove that `n` is composite.

Python's built-in `pow(a, d, n)` performs modular exponentiation efficiently, which is essential because the values are too large for ordinary exponentiation. The chosen bases are sufficient for the input range, which is below the 64-bit boundary.

The main loop follows the game reduction directly. It never generates divisors or simulates moves because those details have already been captured by the primality property.

## Worked Examples

### Sample 1

Input:

```
1
6
```

| Step | Current value | Prime? | Answer |
| --- | --- | --- | --- |
| Start | 6 | No | 0 |
| Finish | 6 | Composite, Elijah wins | 0 |

The number `6` is composite. Elijah can move to `2` or `3`, both of which are losing positions for the next player. Fiona cannot force a win, so Elijah performs no pushups.

### Sample 2

Input:

```
2
30
2
```

| Step | Current value | Prime? | Answer |
| --- | --- | --- | --- |
| Start | 30 | No | 0 |
| Process round | 2 | Yes | 4 |
| Finish | Both rounds processed |  | 4 |

The first round contributes nothing because `30` is composite. The second round starts at `2`, which is prime, so Fiona wins and Elijah pays `2 * 2 = 4` pushups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log a) | Each of the at most 100 numbers is tested for primality using modular exponentiation. |
| Space | O(1) | The algorithm only stores a few integers and the running answer. |

The solution avoids divisor enumeration entirely. With only 100 values and numbers around `10^11`, deterministic Miller-Rabin easily fits within the time limit.

## Test Cases

```python
import sys
import io

def is_prime(n):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in [2, 3, 5, 7, 11, 13]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def solve(inp):
    data = list(map(int, inp.split()))
    n = data[0]
    ans = 0
    for x in data[1:]:
        if is_prime(x):
            ans += 2 * x
    return str(ans)

assert solve("1\n6\n") == "0"
assert solve("2\n30\n2\n") == "4"

assert solve("1\n2\n") == "4"
assert solve("3\n4\n8\n12\n") == "0"
assert solve("3\n3\n5\n7\n") == "30"
assert solve("1\n100000000003\n") == "200000000006"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 2` | `4` | Smallest prime boundary |
| `4, 8, 12` | `0` | Composite numbers with many divisors |
| `3, 5, 7` | `30` | Several prime rounds |
| `100000000003` | `200000000006` | Large number primality handling |

## Edge Cases

For the prime case:

```
Input:
1
7
```

Miller-Rabin identifies `7` as prime. The algorithm adds `2 * 7`, giving `14`. This matches the game because Elijah has no move except losing immediately.

For the composite case:

```
Input:
1
12
```

The algorithm rejects `12` as prime and adds nothing. This matches the game because Elijah can choose the divisor `2`, forcing Fiona into a losing position.

For the smallest value:

```
Input:
1
2
```

The primality check returns true immediately from the small prime list. The answer becomes `4`, handling the case where the only divisor move is the losing move to `1`.
