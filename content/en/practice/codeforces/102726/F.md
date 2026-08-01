---
title: "CF 102726F - Zoom Exercises"
description: "The game is played independently on several pushup rounds. Each round starts with a number of pushups. On a turn, a player replaces the current number with one of its proper divisors. Choosing 1 immediately loses the round for the player who made that move."
date: "2026-08-01T22:13:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102726
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 9-11-20 Div. 1"
rating: 0
weight: 102726
solve_time_s: 80
verified: true
draft: false
---

[CF 102726F - Zoom Exercises](https://codeforces.com/problemset/problem/102726/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
# Problem Understanding

The game is played independently on several pushup rounds. Each round starts with a number of pushups. On a turn, a player replaces the current number with one of its proper divisors. Choosing 1 immediately loses the round for the player who made that move. Both players choose moves optimally. If Fiona wins a round, Elijah pays twice the original number of pushups, while if Elijah wins, he pays nothing. The task is to compute Elijah's total number of pushups after all rounds.

The input contains the number of rounds followed by the starting value for each round. The output is the total penalty Elijah receives after every optimal game is finished.

The important constraint is that each starting number can be as large as $10^{11}$, while there can be up to 100 rounds. Trial division up to the square root would require about $10^6$ checks per number in the worst case, which is already around $10^8$ operations for all rounds. In Python this is close to the limit and leaves little room for overhead. A faster primality test is needed.

The game structure is much simpler than it first appears. The only mathematical property we need is whether a number is prime. A careless solution might try to simulate every possible divisor move, but numbers can have many divisors and the game tree is not the right object to explore.

A first edge case is a prime starting value. For example:

```
1
7
```

The correct output is:

```
14
```

The only divisor smaller than 7 is 1. Fiona, moving first, must choose 1 and immediately loses. Since Elijah wins, he pays 0? Wait, the game rule says the player who replaces the number with 1 loses, so the first player losing means Fiona loses only if Fiona starts. However, Elijah starts every round, so a prime number is a losing position for Elijah. The correct output is 14 because Fiona wins and Elijah pays twice 7.

A second edge case is a composite number:

```
1
12
```

The correct output is:

```
0
```

A careless approach may think the many divisors make the game complicated, but Elijah can always move to a prime divisor such as 3. That leaves Fiona with a prime number, where she has no winning move. Every composite number gives the first player this option.

A third edge case is the smallest possible value:

```
1
2
```

The correct output is:

```
4
```

The number 2 is prime, so Elijah loses immediately by the reasoning above. Implementations that treat 2 as a special composite-like case will produce the wrong answer.

## Approaches

The direct approach would be to generate every divisor of each number and recursively determine whether a position is winning. This works because the game is finite. Every move reduces the current value, so eventually someone reaches a forced move to 1. A recursive game search would correctly classify every position.

The problem is that the values can reach $10^{11}$. Even finding all divisors repeatedly is unnecessary work, and the recursive state space becomes difficult to manage. The worst-case divisor enumeration already becomes too expensive when repeated across all test cases.

The key observation is that every composite number has a prime divisor smaller than itself. If the current number is composite, the first player can replace it with that prime divisor. The opponent is then forced into a losing prime position. On the other hand, if the current number is prime, the only legal replacement is 1, which immediately loses.

The entire game therefore collapses to one question: is the starting number prime? Prime numbers contribute $2a_i$ pushups, while composite numbers contribute zero.

To handle values up to $10^{11}$, deterministic Miller-Rabin primality testing is enough. With a small fixed set of bases, it gives an exact answer for this range without checking every possible divisor.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Too dependent on number of divisors and game states | O(number of states) | Too slow |
| Optimal | O(n log^3(max(a))) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each pushup amount, determine whether it is prime using Miller-Rabin primality testing. The only information the game needs is whether the starting position is winning or losing, and that is completely determined by primality.
2. If the number is prime, add twice its value to the answer. A prime number is a losing position for the first player, so Fiona wins that round.
3. If the number is composite, add nothing. Elijah can move to a prime divisor and force Fiona into the losing situation.

Why it works:

A prime number has no divisor other than itself and 1. Since replacing the number with 1 loses instantly, the first player has no safe move and loses. A composite number has a prime divisor smaller than itself. The first player chooses that divisor, leaving the opponent with a prime number. The opponent then loses. These two cases cover every integer greater than 1, so the algorithm always assigns the correct winner.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_prime(n):
    if n < 2:
        return False

    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for a in [2, 3, 5, 7, 11]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        ok = False
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                ok = True
                break

        if not ok:
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

The `is_prime` function first removes small prime factors. This quickly handles many composite values and avoids unnecessary Miller-Rabin work.

For the remaining values, the number is written as $d \times 2^s$. Miller-Rabin checks whether a number behaves like a prime under several modular exponentiation tests. The chosen bases are deterministic for the input range, so no probabilistic error remains.

The main loop only needs to classify each starting number. It adds `2 * a` only for losing positions. Python integers already support values larger than the maximum possible answer, so no overflow handling is needed.

## Worked Examples

For the first example:

```
1
6
```

| Round | Value | Prime? | Added Pushups | Total |
| --- | --- | --- | --- | --- |
| 1 | 6 | No | 0 | 0 |

The number 6 is composite, so Elijah moves to a prime divisor such as 2 or 3 and wins.

For the second example:

```
2
30
2
```

| Round | Value | Prime? | Added Pushups | Total |
| --- | --- | --- | --- | --- |
| 1 | 30 | No | 0 | 0 |
| 2 | 2 | Yes | 4 | 4 |

The first round is won by Elijah. The second round is a prime position, so Fiona wins and Elijah receives a penalty of $2 \times 2$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log^3(max(a))) | Each Miller-Rabin test uses a constant number of modular exponentiations. |
| Space | O(1) | Only a few variables are stored while processing each number. |

With only 100 numbers and values up to $10^{11}$, the deterministic Miller-Rabin approach easily fits the time limit.

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

    for a in [2, 3, 5, 7, 11]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def solve(inp):
    data = inp.strip().split()
    n = int(data[0])
    ans = 0
    for i in range(1, n + 1):
        x = int(data[i])
        if is_prime(x):
            ans += 2 * x
    return str(ans)

assert solve("1\n6\n") == "0", "sample 1"
assert solve("2\n30\n2\n") == "4", "sample 2"

assert solve("1\n2\n") == "4", "smallest prime"
assert solve("3\n3\n5\n9\n") == "16", "multiple primes and composite"
assert solve("2\n1000000007\n100000000000\n") == "2000000014", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 2` | `4` | Smallest possible prime case |
| `3 / 3 5 9` | `16` | Prime classification mixed with composite values |
| `2 / 1000000007 100000000000` | `2000000014` | Large-number primality handling |

## Edge Cases

For a prime value such as:

```
1
7
```

Miller-Rabin identifies 7 as prime, so the algorithm adds `2 * 7`. This matches the game because Elijah has no safe first move.

For a composite value such as:

```
1
12
```

The primality test returns false, so the answer remains unchanged. This matches the strategy where Elijah moves to a prime divisor and wins.

For the smallest input:

```
1
2
```

The primality test treats 2 correctly as prime. The answer becomes 4, which catches implementations that incorrectly assume all even numbers are composite.
