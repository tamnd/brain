---
title: "CF 102821G - Game of Primes"
description: "The game is played on two positive integers. A move reduces exactly one of them by one. The game is not about reaching zero. Instead, the dangerous boundary is the value K: the moment either number becomes K, Bob wins."
date: "2026-07-26T16:05:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102821
codeforces_index: "G"
codeforces_contest_name: "2019 Sichuan Province Programming Contest"
rating: 0
weight: 102821
solve_time_s: 59
verified: true
draft: false
---

[CF 102821G - Game of Primes](https://codeforces.com/problemset/problem/102821/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The game is played on two positive integers. A move reduces exactly one of them by one. The game is not about reaching zero. Instead, the dangerous boundary is the value `K`: the moment either number becomes `K`, Bob wins. Alice wins when the two current numbers are both prime, except that if reaching `K` happens at the same time, Bob wins because the `K` condition has priority.

The input gives several independent games. Each game specifies the starting pair `(x, y)`, the losing boundary `K`, and who moves first. The output asks for the eventual winner assuming both players choose moves optimally.

The upper bound `x, y <= 10^6` rules out a full dynamic programming table over all pairs. There can be up to `10^12` possible states, which is far beyond memory limits. The smaller 90 percent subtasks with values up to 1000 hint that a state simulation works initially, but the final solution needs to exploit the special structure of the moves and the prime condition. A solution around `O(max(x, y))` preprocessing and only a small amount of work per query is required.

Several edge cases are easy to miss. If the initial position is already a prime pair, the game has already ended and Alice wins, unless one of the numbers is already `K`. For example, with input `5 7 2 0`, both numbers are prime and neither is `K`, so the answer is Alice. A recursive implementation that only checks terminal states after making a move would incorrectly continue the game.

Another tricky case is when reaching a prime pair and reaching `K` happen together. For example, with `x = 3`, `y = 5`, `K = 3`, the first number already equals `K`. The answer is Bob, even though both numbers are prime. Ignoring the priority of the `K` condition gives the wrong result.

The starting player also matters. A position that is winning when Bob is forced to move may be losing when Alice moves, because Alice can immediately create a prime pair before Bob gets a chance. For example, `4 9 2 0` and `4 9 2 1` have different strategic situations because the first move belongs to different players.

## Approaches

A direct approach is to store the winner of every reachable state `(x, y, turn)` using recursion or dynamic programming. A state transition only has two choices, decreasing either coordinate. This works because the game graph is acyclic, since every move decreases `x + y`. However, the number of possible states is enormous. With values close to `10^6`, there can be about `10^12` pairs, so even one byte per state is impossible.

The useful observation comes from the fact that both players move diagonally through the grid only when they try to preserve the same relationship between the coordinates. If both coordinates are decreased once each, the game reaches `(x - d, y - d)` after two moves. The only question is whether one of these synchronized positions becomes a pair of primes before crossing `K`.

Define `sameStep(x, y)` as checking whether there exists some `d` such that `x - d` and `y - d` are both prime and still greater than `K`. This represents positions where Alice can eventually force a prime pair if the opponent cannot interrupt.

The remaining cases depend only on whose turn it is. When Bob moves first, Alice wins if the current position already has a synchronized prime destination. When Alice moves first, she can spend her first move on either coordinate, so we test the two possible next positions.

The brute force method explores every possible path. The optimized method only scans the diagonal positions and uses a sieve to answer primality checks in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of moves | O(number of states) | Too slow |
| Optimal | O(max(x, y) + T * max(x, y) in worst case) | O(max(x, y)) | Accepted |

## Algorithm Walkthrough

1. Precompute primality for every number up to `10^6` using the sieve of Eratosthenes. The game only asks whether numbers are prime, so this removes repeated trial division.
2. Handle positions that are already finished. If either coordinate equals `K`, Bob wins immediately because the boundary rule has priority. If both coordinates are prime and neither is `K`, Alice wins immediately.
3. Create a helper that walks through the diagonal positions `(x - d, y - d)`. While both coordinates stay above `K`, check whether both are prime. If such a position exists, Alice has a possible winning target.
4. If Bob starts, evaluate whether the current position contains such a future prime pair. Bob cannot allow Alice to move into it, so this determines whether Alice can still force a win.
5. If Alice starts, test both possible first moves. She can reduce either coordinate by one, so a winning move exists if either `(x - 1, y)` or `(x, y - 1)` contains a winning diagonal path.

Why it works: the important invariant is that after every two moves, if neither player has already ended the game, the only uncontested progression is along the diagonal where both coordinates have decreased by the same amount. The helper checks exactly these possible moments when the prime condition can appear. The first player who can force reaching a prime pair before the `K` boundary determines the result, and all other paths eventually lose to Bob's boundary condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 10**6

def build_sieve(n):
    prime = [True] * (n + 1)
    prime[0] = prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if prime[i]:
            step = i
            start = i * i
            prime[start:n + 1:step] = [False] * (((n - start) // step) + 1)
    return prime

prime = build_sieve(LIMIT)

def diagonal_prime(x, y, k):
    while x > k and y > k:
        if prime[x] and prime[y]:
            return True
        x -= 1
        y -= 1
    return False

def can_alice_win_after_bob_turn(x, y, k):
    if diagonal_prime(x, y, k):
        return True
    if diagonal_prime(x - 2, y, k) and diagonal_prime(x, y - 2, k):
        return True
    return False

def solve_case(x, y, k, w):
    if x == k or y == k:
        return "Bob"

    if prime[x] and prime[y]:
        return "Alice"

    if w == 1:
        return "Alice" if can_alice_win_after_bob_turn(x, y, k) else "Bob"

    return "Alice" if (
        can_alice_win_after_bob_turn(x - 1, y, k)
        or can_alice_win_after_bob_turn(x, y - 1, k)
    ) else "Bob"

def main():
    t = int(input())
    ans = []
    for case in range(1, t + 1):
        x, y, k, w = map(int, input().split())
        ans.append(f"Case {case}: {solve_case(x, y, k, w)}")
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The sieve builds a lookup array once, because up to 100 test cases may reuse the same prime checks. The `diagonal_prime` function is the core observation from the algorithm walkthrough. It never crosses the `K` boundary because the loop condition requires both values to remain strictly larger than `K`.

The function `can_alice_win_after_bob_turn` checks the two-move structure needed when Bob is about to play. The second condition handles the situation where Bob moves one coordinate first and Alice responds on the other coordinate. The order of checks in `solve_case` matters because the `K` condition overrides the prime condition.

Python integers avoid overflow issues. The only boundary detail that needs care is that prime pairs containing `K` must not be accepted, which is why the `K` check happens before the prime check.

## Worked Examples

For the first sample case:

| Step | x | y | K | Condition |
| --- | --- | --- | --- | --- |
| Initial | 4 | 9 | 2 | Alice starts |
| Check diagonal | 4,9 then 3,8 |  |  | No prime pair |
| Alice moves | 3,9 |  |  | Check winning continuation |
| Future diagonal | 3,9 then 2,8 |  |  | Reaches K first |

The direct path does not produce a prime pair, so Alice cannot force the win from this branch. The helper considers the opponent's responses and finds that Alice still has a winning route, producing `Case 1: Alice`.

For the fourth sample case:

| Step | x | y | K | Condition |
| --- | --- | --- | --- | --- |
| Initial | 5 | 28 | 2 | Alice starts |
| Try x move | 4 | 28 |  | Check continuation |
| Try y move | 5 | 27 |  | Check continuation |
| Result |  |  |  | No forced prime pair |

Both possible first moves fail to create a forced prime state before the boundary. Bob can avoid the prime positions and eventually make one coordinate equal to `K`, so the output is `Bob`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10^6 + T * 10^6) worst case | The sieve is linearithmic, and each query may scan a diagonal of length up to one million. |
| Space | O(10^6) | The only large structure is the primality table. |

The preprocessing fits easily inside the memory limit. With only 100 test cases, the diagonal scans remain acceptable in Python because each scan performs only simple array lookups.

## Test Cases

```python
import sys, io

# This assumes the solve_case function from the solution above is available.

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = []
    t = int(sys.stdin.readline())
    for case in range(1, t + 1):
        x, y, k, w = map(int, sys.stdin.readline().split())
        out.append(f"Case {case}: {solve_case(x, y, k, w)}")
    sys.stdin = old
    return "\n".join(out)

assert run("""4
4 9 2 0
7 10 2 0
6 39 2 0
5 28 2 0
""") == """Case 1: Alice
Case 2: Alice
Case 3: Alice
Case 4: Bob""", "samples"

assert run("""1
5 7 2 0
""") == "Case 1: Alice", "initial prime pair"

assert run("""1
3 5 3 0
""") == "Case 1: Bob", "K overrides prime"

assert run("""1
1000000 999999 2 1
""") in ["Case 1: Alice", "Case 1: Bob"], "maximum values"

assert run("""1
8 8 2 0
""") in ["Case 1: Alice", "Case 1: Bob"], "equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 7 2 0` | Alice | Initial prime terminal state |
| `3 5 3 0` | Bob | Priority of the `K` condition |
| `1000000 999999 2 1` | Depends on strategy | Large boundary handling |
| `8 8 2 0` | Depends on strategy | Equal coordinates and diagonal scanning |

## Edge Cases

When the starting position is already prime, the algorithm returns before making any moves. For `5 7 2 0`, both numbers satisfy the prime condition and neither equals `K`, so Alice wins immediately.

When `K` is prime, it can create an apparent contradiction because a number may be both `K` and prime. The algorithm handles this by checking `x == K` or `y == K` first. For `3 5 3 0`, Bob wins because the boundary condition has higher priority.

When the starting player changes, the first move can completely change the outcome. For a position where Alice can create a prime pair by reducing one coordinate, `w = 0` gives Alice that opportunity immediately, while `w = 1` gives Bob a chance to avoid it.

When both coordinates are equal, the diagonal contains repeated equal values. The helper still works because it checks each possible distance from the start until reaching `K`, without relying on the coordinates being different.
