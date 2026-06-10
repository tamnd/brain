---
title: "CF 1537D - Deleting Divisors"
description: "We start with a positive integer $n$. Two players alternate turns, with Alice moving first. On each turn, the current player chooses a proper divisor of the current number, meaning a divisor that is neither $1$ nor the number itself, and subtracts it from the number."
date: "2026-06-10T15:04:51+07:00"
tags: ["codeforces", "competitive-programming", "games", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1537
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 726 (Div. 2)"
rating: 1700
weight: 1537
solve_time_s: 150
verified: false
draft: false
---

[CF 1537D - Deleting Divisors](https://codeforces.com/problemset/problem/1537/D)

**Rating:** 1700  
**Tags:** games, math, number theory  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a positive integer $n$. Two players alternate turns, with Alice moving first. On each turn, the current player chooses a proper divisor of the current number, meaning a divisor that is neither $1$ nor the number itself, and subtracts it from the number.

The game continues on the updated value. If a player begins a turn and there is no valid divisor to subtract, that player loses.

For every test case, we must determine which player wins assuming both play perfectly.

The input consists of up to $10^4$ independent games. The starting value $n$ can be as large as $10^9$. Since there are many test cases, any solution that performs extensive game-state exploration for each value is immediately suspicious. A solution around $O(\sqrt n)$ per test case is completely safe because $\sqrt{10^9} \approx 31623$, while anything involving large dynamic programming tables up to $n$ is impossible.

Several edge cases are easy to mishandle.

When $n=1$, there are no divisors at all. Alice loses immediately.

Input:

```
1
1
```

Output:

```
Bob
```

A solution that assumes every positive number has at least one move would fail here.

Prime numbers are also terminal positions. For example:

Input:

```
1
13
```

Output:

```
Bob
```

The only divisors of a prime are $1$ and itself, both forbidden.

Powers of two behave differently from other even numbers. For example:

Input:

```
1
8
```

Output:

```
Bob
```

A naive rule such as "all even numbers are winning" gives the wrong answer.

The number $2$ is another special case:

Input:

```
1
2
```

Output:

```
Bob
```

Although it is even, it has no valid move because its only divisors are $1$ and $2$.

## Approaches

A natural first idea is to treat the game as a standard impartial game. For every value $x$, we can generate all legal moves $x \to x-d$, where $d$ is a proper divisor of $x$. A position is winning if at least one move leads to a losing position, and losing if every move leads to a winning position.

This brute-force definition is correct because it directly matches optimal play. Unfortunately, it is not practical. Since $n$ can reach $10^9$, we cannot build a DP table up to $n$. Even for much smaller limits, repeatedly enumerating game states becomes too expensive.

The key observation is that the game has a very rigid structure. Every move subtracts a proper divisor, so the number always decreases. This allows us to analyze winning and losing positions mathematically instead of computing them recursively.

Let us examine small values:

| n | Result |
| --- | --- |
| 1 | Lose |
| 2 | Lose |
| 3 | Lose |
| 4 | Win |
| 5 | Lose |
| 6 | Win |
| 7 | Lose |
| 8 | Lose |
| 9 | Lose |
| 10 | Win |

All odd numbers appear to be losing.

This is not a coincidence. If $n$ is odd, every divisor of $n$ is also odd. Subtracting an odd divisor from an odd number produces an even number. Thus every move from an odd position goes to an even position. If all even positions reachable from odd numbers are winning, then every odd number is losing.

Next, consider even numbers.

If an even number is not a power of two, it contains an odd factor. Let $d$ be that odd factor. Subtracting $d$ preserves evenness and produces an odd number. Since odd numbers are losing positions, such an even number is winning.

The only difficult case is powers of two.

Let $n=2^k$.

Every proper divisor is also a power of two. Any move looks like

$$2^k \to 2^k - 2^m$$

with $m<k$.

Factoring gives

$$2^k - 2^m = 2^m(2^{k-m}-1).$$

The second factor is odd and greater than $1$, so the result is an even number that is not a power of two.

We already established that every even number that is not a power of two is winning. Hence every move from $2^k$ leads to a winning position.

This means powers of two alternate between winning and losing according to the exponent parity:

$$2^1=2 \text{ is losing}$$

$$2^2=4 \text{ is winning}$$

$$2^3=8 \text{ is losing}$$

$$2^4=16 \text{ is winning}$$

and so on.

The final characterization is remarkably simple:

If $n$ is odd, Bob wins.

If $n$ is an even number that is not a power of two, Alice wins.

If $n=2^k$, Alice wins when $k$ is even and Bob wins when $k$ is odd.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of reachable states | Large DP/state storage | Too slow |
| Optimal | $O(\log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the current value $n$.
2. If $n$ is odd, output `"Bob"`.

Every move from an odd number goes to an even number, and odd positions are losing.
3. Check whether $n$ is a power of two.

Repeatedly divide by $2$ while it remains even and count how many divisions are performed.
4. If the remaining value is not $1$, then $n$ was not a power of two.

Such numbers are even and contain an odd factor, allowing a move to a losing odd position. Output `"Alice"`.
5. Otherwise $n=2^k$.
6. If $k$ is even, output `"Alice"`.
7. If $k$ is odd, output `"Bob"`.

### Why it works

The entire solution rests on classifying positions into three categories.

Every odd number is losing because all legal moves lead to even numbers.

Every even number that is not a power of two is winning because it contains an odd divisor. Subtracting that divisor produces an odd number, which is losing.

For powers of two, every move leads to an even number that is not a power of two. Those positions are winning, so powers of two themselves alternate between losing and winning according to the parity of the exponent. Since $2=2^1$ is losing, all odd exponents are losing and all even exponents are winning.

Every possible value belongs to exactly one of these categories, so the algorithm always returns the correct winner.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())

    if n % 2 == 1:
        print("Bob")
        continue

    x = n
    cnt = 0

    while x % 2 == 0:
        x //= 2
        cnt += 1

    if x != 1:
        print("Alice")
    else:
        print("Alice" if cnt % 2 == 0 else "Bob")
```

The first branch handles all odd numbers immediately because they are losing positions.

For even numbers, the code removes every factor of two and counts how many were removed. If the remaining value is greater than one, then the number had an odd factor and is not a pure power of two. Those positions are always winning.

If the remaining value is exactly one, the original number was $2^{\text{cnt}}$. The winner depends only on whether the exponent is even or odd.

No large arrays or recursion are needed. The loop runs at most about thirty times because $2^{30} > 10^9$.

## Worked Examples

### Example 1

Input:

```
4
1
4
12
69
```

| n | Odd? | Power of Two? | Exponent | Winner |
| --- | --- | --- | --- | --- |
| 1 | Yes | No | - | Bob |
| 4 | No | Yes | 2 | Alice |
| 12 | No | No | - | Alice |
| 69 | Yes | No | - | Bob |

Output:

```
Bob
Alice
Alice
Bob
```

This example shows all three categories: odd numbers, powers of two, and even numbers with odd factors.

### Example 2

Input:

```
3
2
8
16
```

| n | Odd? | Power of Two? | Exponent | Winner |
| --- | --- | --- | --- | --- |
| 2 | No | Yes | 1 | Bob |
| 8 | No | Yes | 3 | Bob |
| 16 | No | Yes | 4 | Alice |

Output:

```
Bob
Bob
Alice
```

This trace demonstrates the alternating behavior of powers of two. Odd exponents lose, even exponents win.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log n)$ | At most the number of factors of two in $n$ are removed |
| Space | $O(1)$ | Only a few integer variables are stored |

Since $n \le 10^9$, the loop performs at most about thirty iterations per test case. Even with $10^4$ test cases, the running time is easily within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())

        if n % 2:
            ans.append("Bob")
            continue

        x = n
        cnt = 0

        while x % 2 == 0:
            x //= 2
            cnt += 1

        if x != 1:
            ans.append("Alice")
        else:
            ans.append("Alice" if cnt % 2 == 0 else "Bob")

    print("\n".join(ans))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# provided sample
assert run("4\n1\n4\n12\n69\n") == "Bob\nAlice\nAlice\nBob\n", "sample 1"

# minimum value
assert run("1\n1\n") == "Bob\n", "n = 1"

# smallest power of two
assert run("1\n2\n") == "Bob\n", "2 is losing"

# even but not power of two
assert run("1\n6\n") == "Alice\n", "contains odd factor"

# largest power of two below 1e9
assert run("1\n536870912\n") == "Bob\n", "2^29"

# large odd value
assert run("1\n999999937\n") == "Bob\n", "large prime"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `Bob` | Empty game state |
| `2` | `Bob` | Smallest power of two |
| `6` | `Alice` | Even number with odd factor |
| `536870912` | `Bob` | Large power of two with odd exponent |
| `999999937` | `Bob` | Large odd prime |

## Edge Cases

Consider the input:

```
1
1
```

The algorithm immediately detects an odd number and outputs `"Bob"`. This matches the game because there are no legal moves from $1$.

Consider:

```
1
2
```

The factorization loop finds exactly one factor of two. The number is $2^1$, and the exponent is odd, so the algorithm outputs `"Bob"`. Indeed, $2$ has no proper divisors and is losing.

Consider:

```
1
8
```

The loop removes three factors of two, giving exponent $3$. Since the exponent is odd, the answer is `"Bob"`. Every move from $8$ leads to $6$ or another winning position, so the first player loses.

Consider:

```
1
18
```

Removing factors of two leaves $9$, which is not $1$. The number is an even non-power-of-two, so the algorithm outputs `"Alice"`. Alice can subtract the odd divisor $9$, reaching $9$, which is a losing position.

These cases cover the situations most likely to break an incomplete analysis: terminal positions, primes, powers of two, and even numbers containing odd factors.
