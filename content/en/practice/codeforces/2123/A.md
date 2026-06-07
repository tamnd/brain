---
title: "CF 2123A - Blackboard Game"
description: "The blackboard initially contains every integer from 0 to n - 1. A round always has two moves. First Alice removes some number a. Then Bob must remove a different number b such that $$a+b equiv 3 pmod 4.$$ If Bob cannot find such a number, the game ends immediately and Bob loses."
date: "2026-06-08T03:36:36+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 2123
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1034 (Div. 3)"
rating: 800
weight: 2123
solve_time_s: 97
verified: true
draft: false
---

[CF 2123A - Blackboard Game](https://codeforces.com/problemset/problem/2123/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The blackboard initially contains every integer from `0` to `n - 1`.

A round always has two moves. First Alice removes some number `a`. Then Bob must remove a different number `b` such that

$$a+b \equiv 3 \pmod 4.$$

If Bob cannot find such a number, the game ends immediately and Bob loses. After Bob removes his number, the next round starts. The players continue until someone cannot make the required move.

We are given several values of `n`, and for each one we must determine which player wins assuming both play perfectly.

The constraint is tiny. There are at most 100 test cases and `n ≤ 100`. A brute-force game search would already be feasible, but the real goal is to discover the mathematical structure behind the game. Once that structure is understood, the answer for each test case can be computed in constant time.

The subtle part is that Bob does not choose an arbitrary number. His choice is completely determined by the residue class of Alice's number modulo 4.

The valid pairings are:

$$0 \leftrightarrow 3$$

and

$$1 \leftrightarrow 2.$$

Any number congruent to `0 (mod 4)` must be matched with a number congruent to `3 (mod 4)`, and any number congruent to `1 (mod 4)` must be matched with a number congruent to `2 (mod 4)`.

A common mistake is to focus on the exact values instead of their residues modulo 4. For example, when `n = 5`, the numbers are:

$$0,1,2,3,4.$$

The number `4` behaves exactly like `0` because both are congruent to `0 (mod 4)`.

Another easy mistake is to assume that an even number of total integers automatically favors Bob. For `n = 2`, there are two numbers, but the set is `{0,1}`. No valid partner exists for either choice, so Alice wins immediately.

Input:

```
1
2
```

Output:

```
Alice
```

Bob loses on his first move.

## Approaches

A brute-force approach would model the current set of remaining numbers and recursively try every legal move. Alice would try to reach a winning state, while Bob would try to avoid losing.

This works because the state space is small when `n ≤ 100`, but it completely ignores the structure of the game. Even for moderate `n`, the number of possible game states grows exponentially.

The key observation is that only residues modulo 4 matter.

Every number belongs to one of four groups:

$$0,\ 1,\ 2,\ 3 \pmod 4.$$

Bob's response must come from a specific complementary group:

| Alice chooses | Bob must choose |
| --- | --- |
| 0 mod 4 | 3 mod 4 |
| 3 mod 4 | 0 mod 4 |
| 1 mod 4 | 2 mod 4 |
| 2 mod 4 | 1 mod 4 |

This means the game splits into two completely independent pools:

1. Residues `0` and `3`.
2. Residues `1` and `2`.

Let

$$c_0,c_1,c_2,c_3$$

be the counts of numbers having each residue.

A move in the first pool always removes one element from `c_0` and one from `c_3`.

A move in the second pool always removes one element from `c_1` and one from `c_2`.

Bob can continue responding as long as both counts in the chosen pool remain positive.

For the numbers `0` through `n-1`, the residue counts differ by at most one. Checking the first few values reveals the pattern:

| n | Winner |
| --- | --- |
| 1 | Alice |
| 2 | Alice |
| 3 | Alice |
| 4 | Bob |
| 5 | Alice |
| 6 | Alice |
| 7 | Alice |
| 8 | Bob |

Every block of four numbers contributes exactly one complete `(0,3)` pair and one complete `(1,2)` pair.

When `n` is a multiple of 4, every residue class appears equally often. All numbers can be partitioned into valid pairs. No matter what Alice does, Bob always has a response. After all numbers are removed, Alice is the first player unable to move, so Bob wins.

When `n` is not a multiple of 4, one or more residue classes has an extra element. Alice can eventually choose from an unmatched residue and leave Bob without a legal response. Bob cannot prevent this because the imbalance already exists in the initial position.

The winner is simply:

- Bob if `n % 4 == 0`
- Alice otherwise

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow conceptually |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`.
2. Compute `n % 4`.
3. If the remainder is `0`, output `"Bob"`.

In this case every residue class appears equally often, so every number belongs to some valid matching pair.
4. Otherwise output `"Alice"`.

At least one residue class is unmatched. Alice can exploit this imbalance and eventually force Bob into a position with no legal response.

### Why it works

The game is entirely determined by the counts of residues modulo 4. Valid moves always consume one number from a complementary pair of residue classes, either `(0,3)` or `(1,2)`.

When `n` is divisible by 4, the counts of all four residue classes are equal. Every element can be matched, so Bob always has a response to Alice's move until the board becomes empty. Alice then faces the first position with no legal move and loses.

When `n` is not divisible by 4, at least one residue class has more elements than its complementary class. Those extra elements can never be matched. Alice can force play until only unmatched elements remain, at which point Bob cannot respond. Hence Alice wins.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    print("Bob" if n % 4 == 0 else "Alice")
```

The implementation follows the mathematical characterization directly.

The only value that matters is `n % 4`. If the remainder is zero, the residue classes are perfectly balanced and Bob wins. Every other remainder creates an imbalance that favors Alice.

No simulation is needed. No game states need to be stored. Each test case is handled independently in constant time.

## Worked Examples

### Example 1

Input:

```
4
```

Residue counts:

| Residue | Count |
| --- | --- |
| 0 | 1 |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |

All classes are balanced.

| Step | Value |
| --- | --- |
| n | 4 |
| n % 4 | 0 |
| Winner | Bob |

Every number belongs to a valid pair. Bob can always answer Alice's move until the board becomes empty.

### Example 2

Input:

```
5
```

Numbers are:

```
0 1 2 3 4
```

Residue counts:

| Residue | Count |
| --- | --- |
| 0 | 2 |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |

The extra residue-0 element has no permanent matching partner.

| Step | Value |
| --- | --- |
| n | 5 |
| n % 4 | 1 |
| Winner | Alice |

This trace demonstrates the key imbalance. One element cannot be paired, which eventually leaves Bob without a legal response.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | One modulus operation per test case |
| Space | O(1) | No auxiliary storage |

The constraints are extremely small, but the solution is even simpler. Each test case requires constant work and uses constant memory, easily fitting within the limits.

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
        ans.append("Bob" if n % 4 == 0 else "Alice")
    sys.stdout.write("\n".join(ans))

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
assert run("5\n2\n4\n5\n7\n100\n") == \
       "Alice\nBob\nAlice\nAlice\nBob"

# minimum n
assert run("1\n1\n") == "Alice"

# first Bob position
assert run("1\n4\n") == "Bob"

# just above multiple of 4
assert run("1\n9\n") == "Alice"

# maximum constraint
assert run("1\n100\n") == "Bob"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n = 1` | Alice | Smallest possible board |
| `n = 4` | Bob | First balanced configuration |
| `n = 9` | Alice | Multiple of 4 plus one |
| `n = 100` | Bob | Maximum constraint value |

## Edge Cases

For `n = 1`, the board contains only `{0}`.

Input:

```
1
1
```

Alice removes `0`. No numbers remain. Bob has no legal response.

The algorithm computes:

| Variable | Value |
| --- | --- |
| n | 1 |
| n % 4 | 1 |

Output:

```
Alice
```

For `n = 2`, the board contains `{0,1}`.

Input:

```
1
2
```

Neither number has a complementary residue available. Whatever Alice removes, Bob immediately loses.

The algorithm computes:

| Variable | Value |
| --- | --- |
| n | 2 |
| n % 4 | 2 |

Output:

```
Alice
```

For `n = 8`, the residue counts are perfectly balanced:

| Residue | Count |
| --- | --- |
| 0 | 2 |
| 1 | 2 |
| 2 | 2 |
| 3 | 2 |

Input:

```
1
8
```

Every element can be matched. Bob always has a response until the board is empty.

The algorithm computes:

| Variable | Value |
| --- | --- |
| n | 8 |
| n % 4 | 0 |

Output:

```
Bob
```

These cases cover the smallest board, an immediate Bob loss, and a fully balanced position where Bob wins. The rule `n % 4 == 0` correctly handles all of them.
