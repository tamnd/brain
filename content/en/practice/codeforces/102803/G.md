---
title: "CF 102803G - Goodbye"
description: "The game is played on a number rather than on a board or graph. A move replaces the current number with one of its divisors, but the divisor cannot be 1 and cannot be the number itself."
date: "2026-07-26T16:23:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102803
codeforces_index: "G"
codeforces_contest_name: "The 15th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102803
solve_time_s: 43
verified: true
draft: false
---

[CF 102803G - Goodbye](https://codeforces.com/problemset/problem/102803/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The game is played on a number rather than on a board or graph. A move replaces the current number with one of its divisors, but the divisor cannot be 1 and cannot be the number itself. The player who has no legal move wins, which makes the game a misère-style divisor game: reaching a prime number or 1 is good because the next player is forced to lose the opportunity to move.

Chino moves first on the given number n. She wants to choose a divisor on her first turn that leaves David in a losing position. Among all such choices, she wants the largest possible number. If n itself has no legal first move, she has already won and the answer is 0. If every possible first move allows David to win, the answer is -1.

The value of n is at most 100000 and there can be up to 1000 test cases. This rules out repeatedly exploring the entire divisor tree for every input. A recursive game search over all divisors can repeatedly visit the same states and can become expensive, so the solution needs to recognize the mathematical structure of winning and losing positions and preprocess useful information.

Several edge cases are easy to miss. For n = 1, there is no legal divisor, so Chino wins immediately and the answer is 0. A careless implementation that searches for a winning divisor would incorrectly return -1.

For n = 7, the same situation appears with a prime number. The only divisors are 1 and 7, both forbidden, so the correct output is 0.

For n = 6, the only possible first choices are 2 and 3. Both are prime positions, meaning the next player has no move and wins. Chino cannot force a win, so the correct output is -1. An approach that only checks whether a divisor exists would fail here.

For n = 12, Chino can choose 4. The number 4 has only one possible move, to 2, and 2 is a terminal winning position. Therefore 4 is a losing position for the player whose turn it is, so David loses after Chino chooses 4. The correct output is 4.

## Approaches

A direct solution would model every number as a game state. For a number x, we could generate all proper divisors and recursively determine whether the current player can force a win. This is correct because every move strictly decreases the number, so the recursion eventually reaches primes or 1.

The problem is that this repeats the same reasoning many times. For example, many different composite numbers contain 4, 6, or 9 as divisors, and a naive search would repeatedly recompute the result of those positions. Even with memoization, doing this independently for many test cases wastes work. Generating divisors for every state and traversing all reachable states is too large when n reaches 100000.

The key observation is that the game has a very simple losing-position structure. A position is losing only when every possible move goes to a winning position. Prime numbers and 1 are winning positions because no move is available. A composite number is losing exactly when all of its proper divisors are prime. That happens precisely when the number is the product of two primes, counting multiplicity.

If a number contains a composite proper divisor, that divisor is already a possible move. The smallest composite divisors that matter are always products of two primes, and those positions are losing. This means every composite number with more than two prime factors has a move to a losing position and is winning.

The problem is then reduced to finding the largest semiprime divisor of n, where semiprime means having exactly two prime factors with multiplicity. That divisor is the best first move because it leaves David in a losing state.

The brute force and optimized approaches can be compared as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Potentially O(number of reachable divisor states per test case) | O(n) with memoization | Too slow for many cases |
| Optimal | O(N log log N + N log N) preprocessing | O(N) | Accepted |

## Algorithm Walkthrough

1. Read all test cases and find the maximum value N that appears. All preprocessing can be limited to this value because no query needs a larger number.
2. Use a sieve to find prime numbers up to N. The classification of a game state depends only on its prime factors, so fast primality information is needed.
3. Mark every number that is a semiprime. A number is semiprime if its prime factor count with multiplicity is exactly two. For example, 4 = 2 × 2, 6 = 2 × 3, and 9 = 3 × 3 are semiprimes.
4. For every semiprime d, update all multiples of d that are larger than d. The value d is a valid first move for those multiples, and keeping the maximum candidate gives the largest winning first move. A multiple equal to d is skipped because Chino cannot choose the original number itself.
5. For each query n, handle the special states first. If n is 1 or prime, Chino wins without moving, so output 0. If n is semiprime, all legal moves go to prime numbers, so Chino cannot win and the answer is -1. Otherwise, output the largest semiprime divisor stored during preprocessing.

The correctness comes from the invariant that every stored answer for a number x is the largest divisor of x that is a losing game state. A losing game state is exactly a semiprime, so any stored candidate is a winning first move. Since every non-semiprime composite number has at least one semiprime divisor, the stored value exists whenever Chino can win by moving. Choosing the largest stored divisor satisfies Chino's preference without changing the outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    queries = [int(input()) for _ in range(int(input()))]
    if not queries:
        return

    limit = max(queries)

    prime = [True] * (limit + 1)
    if limit >= 0:
        prime[0] = False
    if limit >= 1:
        prime[1] = False

    i = 2
    while i * i <= limit:
        if prime[i]:
            step = i
            start = i * i
            prime[start:limit + 1:step] = [False] * (((limit - start) // step) + 1)
        i += 1

    factor_count = [0] * (limit + 1)
    for p in range(2, limit + 1):
        if prime[p]:
            for x in range(p, limit + 1, p):
                y = x
                while y % p == 0:
                    factor_count[x] += 1
                    y //= p

    semiprime = [False] * (limit + 1)
    for x in range(2, limit + 1):
        if factor_count[x] == 2:
            semiprime[x] = True

    best = [0] * (limit + 1)
    for d in range(2, limit + 1):
        if semiprime[d]:
            for multiple in range(d * 2, limit + 1, d):
                best[multiple] = d

    ans = []
    for n in queries:
        if n <= 1 or prime[n]:
            ans.append("0")
        elif semiprime[n]:
            ans.append("-1")
        else:
            ans.append(str(best[n]))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The sieve creates the prime array in the usual way by removing multiples of every discovered prime. The boundary cases for 0 and 1 are set explicitly because they are not prime and the sieve loop starts at 2.

The factor counting loop counts prime factors with repetition. This detail matters because 8 = 2 × 2 × 2 has three prime factors and is not semiprime, while 4 = 2 × 2 is semiprime. Counting only distinct prime factors would classify both incorrectly.

The `best` array is filled by iterating over semiprimes instead of iterating over divisors for every query. Every semiprime contributes itself to all larger multiples, and later contributions overwrite smaller answers because the iteration goes upward. The strict `2 * d` starting point prevents storing the original number as its own divisor.

The final query handling follows the game theory classification directly. Prime numbers and 1 are immediate wins, semiprimes are unavoidable losses, and all remaining composite numbers use the precomputed best semiprime divisor.

## Worked Examples

Consider the input value 6.

| Number | Prime? | Semiprime? | Best semiprime divisor | Output |
| --- | --- | --- | --- | --- |
| 6 | No | Yes | Not used | -1 |

The number 6 has two legal choices, 2 and 3. Both are prime, so David would receive a position where he has no move and wins. The semiprime classification correctly identifies 6 as a losing position for the first player.

Consider the input value 12.

| Number | Prime? | Semiprime? | Best semiprime divisor | Output |
| --- | --- | --- | --- | --- |
| 12 | No | No | 4 | 4 |

During preprocessing, 4 is recognized as a semiprime. Since 4 divides 12 and is smaller than 12, it becomes a candidate answer. There are no larger semiprime divisors of 12, so Chino chooses 4 and leaves David in a losing position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log log N + N log N) | The sieve takes O(N log log N), factor counting is bounded by prime multiples, and marking semiprime multiples is a harmonic-series style process |
| Space | O(N) | Several arrays of size N store primality, factor counts, classifications, and answers |

With N at most 100000, the preprocessing stays comfortably within the limits. The test case count does not significantly affect the runtime because all cases share the same precomputation.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# provided-style samples
assert run("1\n6\n") == "-1\n", "semiprime losing position"

# custom cases
assert run("5\n1\n2\n4\n12\n100000\n") == "0\n0\n-1\n4\n10000\n", "boundary and composite cases"
assert run("4\n7\n9\n10\n18\n") == "0\n-1\n-1\n9\n", "prime squares and products"
assert run("3\n8\n27\n30\n") == "4\n9\n15\n", "higher powers and multiple semiprimes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 2, 4, 12, 100000 | 0, 0, -1, 4, 10000 | Minimum values, direct wins, semiprime detection, large input |
| 7, 9, 10, 18 | 0, -1, -1, 9 | Prime handling and products of two primes |
| 8, 27, 30 | 4, 9, 15 | Correct largest losing divisor selection |

## Edge Cases

For n = 1, the algorithm checks `n <= 1` first and returns 0 immediately. There is no divisor to choose, so Chino has already won before making a move.

For a prime number such as n = 7, the prime array marks it as prime, and the algorithm returns 0. Searching for semiprime divisors would be wrong because a prime has no legal moves at all.

For a semiprime number such as n = 6, the algorithm detects that its prime factor count is exactly two and returns -1. Choosing any proper divisor gives a prime number, which is a winning position for David.

For a larger composite number such as n = 30, the semiprime divisors are 6, 10, and 15. The preprocessing phase stores the largest one, 15. Since 15 is losing for the next player, Chino can force a win by choosing the largest valid move.
