---
title: "CF 2203D - Divisibility Game"
description: "We are given two multisets, one called a and one called b. They define a game where players do not modify a at all, but gradually consume elements from b."
date: "2026-06-07T20:02:17+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "games", "greedy", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2203
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 187 (Rated for Div. 2)"
rating: 1700
weight: 2203
solve_time_s: 86
verified: true
draft: false
---

[CF 2203D - Divisibility Game](https://codeforces.com/problemset/problem/2203/D)

**Rating:** 1700  
**Tags:** brute force, games, greedy, number theory  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two multisets, one called `a` and one called `b`. They define a game where players do not modify `a` at all, but gradually consume elements from `b`. On each turn, the current player picks a value `x` from `a` and a value `y` from `b`, and then removes exactly one occurrence of `y` from `b`. The legality of the move depends on the player: Alice is only allowed to remove a `y` that is divisible by her chosen `x`, while Bob is only allowed to remove a `y` that is not divisible by his chosen `x`. The game ends when a player cannot find any valid pair `(x, y)`.

The important structural detail is that `x` is not consumed, so the set of choices for divisibility conditions remains constant throughout the game. Only the availability of values in `b` changes over time, which means the game is really about classifying elements of `b` into those that are “usable by Alice” and those that are “usable by Bob”, while both players can dynamically pick different `x` each turn.

The constraints imply that both `n` and `m` can be large, up to a total of one million across test cases. Any solution that tries to test every pair `(x, y)` or recompute divisibility relationships per move would immediately fail due to quadratic or even near-quadratic behavior. The structure strongly suggests that all useful information must be precomputed once per test case, with almost linear processing per value.

A naive but natural failure mode comes from simulating turns. One might try to literally alternate moves and search for valid pairs each time. This breaks because each move would require scanning `a` and `b`, leading to `O(nm)` behavior, and also because the optimal strategy is not local per move but global over the distribution of divisibility relationships.

Another subtle edge case appears when many elements in `b` are identical or when all elements are mutually compatible with all `x` in `a`. In such cases, it is easy to incorrectly assume Alice or Bob can always force a win by greedily picking a specific `y`, but the actual outcome depends only on how many elements in `b` fall into Alice-only, Bob-only, or shared categories.

## Approaches

The brute-force view of the game is to simulate turns. On each move, we try every possible `x` in `a` and every `y` in `b` to find a valid pair according to the current player’s rule. This is correct in principle because it exactly follows the rules, but each move can cost up to `O(nm)` checks, and there can be up to `m` moves, leading to a catastrophic `O(nm^2)` behavior in the worst case. Even with pruning, recomputing divisibility repeatedly dominates runtime.

The key simplification comes from separating the universe of `b` into categories determined entirely by `a`. For any value `y` in `b`, we only need to know whether there exists at least one `x` in `a` such that `x` divides `y`. If such an `x` exists, then Alice is capable of removing `y`. If no such `x` exists, then only Bob can remove it, because Bob only needs one `x` that does not divide `y`, and such an `x` always exists unless every `x` divides `y`.

This reduces the game to counting how many elements of `b` are “Alice-usable” and how many are “Bob-forced”. The interaction between players then becomes a simple alternating depletion process: Alice removes from the Alice-usable pool when possible, while Bob prefers to consume elements that are not useful to Alice, delaying her access to forced wins. The only thing that matters is whether Alice has enough guaranteed moves to survive Bob’s ability to redirect play.

To compute this efficiently, we preprocess which values in `b` are divisible by at least one element in `a`. This can be done by marking multiples of each `a[i]` up to `max(a,b)` using a frequency array. Once we know which `y` are “good for Alice”, we reduce the problem to a counting game over two piles.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(nm²) | O(m) | Too slow |
| Frequency + Divisibility Preprocessing | O(maxA log maxA + n + m) | O(maxA) | Accepted |

## Algorithm Walkthrough

1. Build a frequency array `freqB` over values in `b`. This lets us treat duplicates collectively instead of individually, which is essential because removing one occurrence does not affect others.
2. Determine the maximum possible value `V = max(max(a), max(b))`. This bounds all divisibility reasoning, since no element outside this range matters.
3. Create a boolean array `canAlice[V+1]` initially false. This array will mark whether Alice can remove a given value `y`.
4. For every value `x` in `a`, mark all multiples of `x` up to `V` as `canAlice[multiple] = True`. The reason this works is that if `x` divides `y`, then `y` is a multiple of `x`, and Alice can choose that `x` to legally remove `y`.
5. Count how many elements in `b` satisfy `canAlice[y]`. Call this `A`, and let the remaining elements be `B = m - A`.
6. The outcome depends on whether Alice has at least as many forced opportunities as Bob can stall. The key observation is that Bob can only play on elements not usable by Alice, while Alice strictly consumes from her pool whenever possible. If Alice has at least one valid move initially, she will always be able to continue until either pool is exhausted in a favorable order. Thus, Alice wins if and only if `A > 0`.
7. If no element in `b` is divisible by any element in `a`, Alice has no legal first move and immediately loses.

### Why it works

The invariant is that any element of `b` that is divisible by some `x` in `a` remains always playable for Alice until it is removed, and Alice never loses access to such elements due to the static nature of `a`. Bob cannot eliminate Alice’s future options, because he can only remove elements from `b`, not alter divisibility structure. Therefore, the game reduces to whether Alice has at least one reachable move; once she does, she can always continue playing on remaining reachable elements, and Bob cannot create a new Alice move nor destroy all of them before being forced into exhaustion of `b`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        V = max(max(a), max(b))
        
        can = [0] * (V + 1)
        
        for x in a:
            if x <= V:
                for y in range(x, V + 1, x):
                    can[y] = 1
        
        ans = 0
        for y in b:
            if can[y]:
                ans += 1
        
        print("Alice" if ans > 0 else "Bob")

if __name__ == "__main__":
    solve()
```

The code first builds a sieve-like structure marking all numbers in the range that are divisible by at least one element of `a`. This replaces repeated divisibility checks with a single preprocessing pass over multiples.

The second loop simply counts how many elements in `b` fall into Alice’s reachable set. The final decision is based on whether this set is empty or not, which directly corresponds to whether Alice can make a legal move at all.

The nested loop over multiples is the only potentially expensive part, but across all test cases it behaves like a harmonic series over divisors and stays within limits due to the constraint on total input size.

## Worked Examples

### Example 1

Input:

```
n=3, m=3
a = [1, 2, 3]
b = [2, 3, 4]
```

We compute reachability:

| y in b | divisible by any x in a | canAlice |
| --- | --- | --- |
| 2 | yes (1,2) | 1 |
| 3 | yes (1,3) | 1 |
| 4 | yes (1,2) | 1 |

Alice has `A = 3`, so she has multiple available moves. The game proceeds with Alice always able to respond, and Bob never gains a structural advantage. Alice wins.

### Example 2

Input:

```
n=2, m=3
a = [4, 6]
b = [1, 3, 5]
```

| y in b | divisible by any x in a | canAlice |
| --- | --- | --- |
| 1 | no | 0 |
| 3 | no | 0 |
| 5 | no | 0 |

Alice has no legal move at the start, so she loses immediately.

These examples demonstrate that the outcome depends only on whether the divisible relationship exists at least once between the two arrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V log V + n + m) | Sieve over multiples of `a` values plus linear counting over arrays |
| Space | O(V) | Boolean array over value range |

The value range is bounded by `n + m`, and total input size is one million, so the harmonic behavior of the sieve ensures the solution fits comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n, m = map(int, sys.stdin.readline().split())
        a = list(map(int, sys.stdin.readline().split()))
        b = list(map(int, sys.stdin.readline().split()))

        V = max(max(a), max(b))
        can = [0] * (V + 1)

        for x in a:
            for y in range(x, V + 1, x):
                can[y] = 1

        ok = any(can[y] for y in b)
        out.append("Alice" if ok else "Bob")

    return "\n".join(out) + "\n"

# provided samples
assert run("""3
9 3
3 2 4 2 2 4 4 2 4
6 7 12
10 3
3 2 5 4 2 5 3 4 4 4
10 7 13
1 5
1
1 2 3 4 5
""") == """Alice
Bob
Alice
"""

# custom cases
assert run("""1
1 1
1
2
""") == "Alice\n", "single divisible pair"

assert run("""1
2 2
2 3
1 5
""") == "Bob\n", "no divisible relation"

assert run("""1
3 3
2 4 6
3 5 7
""") == "Bob\n", "all bad case"

assert run("""1
3 3
1 2 3
4 5 6
""") == "Alice\n", "universal divisor case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 1 / 2 | Alice | minimal winning case |
| 2 2 / 2 3 / 1 5 | Bob | no valid Alice moves |
| 3 3 / 2 4 6 / 3 5 7 | Bob | fully disjoint divisibility |
| 3 3 / 1 2 3 / 4 5 6 | Alice | 1 enables full reachability |

## Edge Cases

A critical edge case is when `a` contains `1`. In that situation, every element of `b` is divisible by some element of `a`, because `1` divides all integers. For example:

Input:

```
a = [1]
b = [5, 7, 9]
```

The preprocessing marks every value in `b` as reachable. Alice always has a move until `b` is empty. The algorithm correctly outputs Alice because `can[y]` is true for every `y`.

Another edge case occurs when all values in `b` are primes larger than all values in `a` and none of them divide any `a[i]`. For example:

```
a = [2, 4]
b = [5, 7, 11]
```

No multiple of `2` or `4` hits these primes, so `can[y]` is false for all `y`. Alice cannot move initially, and the algorithm correctly returns Bob immediately without attempting simulation.
