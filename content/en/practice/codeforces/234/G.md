---
title: "CF 234G - Practice"
description: "We have n football players, numbered from 1 to n. Each practice consists of splitting all players into two non-empty teams."
date: "2026-06-04T10:00:19+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "divide-and-conquer", "implementation"]
categories: ["algorithms"]
codeforces_contest: 234
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 145 (Div. 2, ACM-ICPC Rules)"
rating: 1600
weight: 234
solve_time_s: 98
verified: true
draft: false
---

[CF 234G - Practice](https://codeforces.com/problemset/problem/234/G)

**Rating:** 1600  
**Tags:** constructive algorithms, divide and conquer, implementation  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` football players, numbered from `1` to `n`.

Each practice consists of splitting all players into two non-empty teams. After several practices, we want every pair of players to have been separated at least once, meaning that there exists some practice where the two players were placed on opposite teams.

The task is not only to construct such a schedule, but to use the minimum possible number of practices.

The input contains only one integer `n`. The output must first print the minimum number of practices, then describe each practice by listing one of the two teams. Any optimal construction is accepted.

The constraint `n ≤ 1000` is small enough that we can explicitly output all teams. The challenge is not computational complexity but discovering the minimum number of practices and constructing them.

A useful way to think about the problem is to assign each player a binary code. Every practice corresponds to one bit position. During a practice, players with bit `0` go to one team and players with bit `1` go to the other team. Two players are separated whenever their codes differ in some bit.

Since there are at most 1000 players, binary representations up to 10 bits are sufficient because `2^10 = 1024`.

There are a few subtle edge cases.

For `n = 2`, only one pair exists. A single practice placing player 1 against player 2 is enough.

Input:

```
2
```

One valid output is:

```
1
1 1
```

A careless implementation that always outputs `⌈log2 n⌉` practices without considering small values could accidentally create an empty team in some practice.

Another edge case occurs when `n` is not a power of two.

Input:

```
5
```

We need three practices because `2^2 = 4 < 5 ≤ 8 = 2^3`. Some bit positions may contain very uneven splits, but every practice must still have both teams non-empty. An implementation that blindly prints all bit positions without checking would be incorrect if a bit position contains only zeros among existing players.

A final subtlety is that player numbering starts at 1. Using numbers `1..n` directly as binary codes can increase the required number of bits by one. The clean construction uses codes `0..n-1`.

## Approaches

A brute-force viewpoint is to think directly about pairs of players. There are `n(n-1)/2` pairs. We could repeatedly design practices and check which pairs have already been separated. Such a search quickly becomes combinatorial because every practice is a partition of the players into two non-empty groups. Even for moderate `n`, the number of possible partitions is enormous.

The real structure appears when we ask what information a practice provides. A practice only tells us on which side of the partition each player lies. If we perform `m` practices, every player receives an `m`-bit signature describing its team assignment across all practices.

Two players are separated at least once exactly when their signatures are different. If two players have identical signatures, they always appear on the same side and are never separated.

This transforms the problem into a coding problem. We need `n` distinct signatures. With `m` bits, there are at most `2^m` different signatures, so:

$$2^m \ge n$$

Hence:

$$m \ge \lceil \log_2 n \rceil$$

This gives a lower bound on the answer.

The same observation immediately gives a construction. Assign player `i` the binary representation of `i-1`. Since the values `0,1,\dots,n-1` are distinct, all signatures are distinct. For each bit position, create one practice that separates players according to that bit.

Every pair of players has different binary representations, so they differ in some bit. During the corresponding practice they are placed on opposite teams, satisfying the requirement.

The lower bound and construction match, proving optimality.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Compute the smallest integer `m` such that `2^m ≥ n`.
2. Number the players from `0` to `n-1` internally. These values serve as unique binary codes.
3. For each bit position `b` from `0` to `m-1`, create one practice.
4. In practice `b`, place every player whose code has bit `b` equal to `1` into the first team.
5. All remaining players automatically belong to the second team.
6. Output the players in the first team for each practice.

Why is it safe to output only the players with bit `1`? Since `2^m ≥ n`, the highest bit position used is necessary. For every bit position `b < m`, there exists at least one code with bit `b = 1` and at least one code with bit `b = 0` among `0..n-1`. Thus both teams are non-empty.

### Why it works

Each player receives the binary representation of a unique integer from `0` to `n-1`.

Consider any two different players. Their assigned integers differ, so their binary representations differ in at least one bit position. During the practice corresponding to that bit, one player belongs to the first team and the other belongs to the second team. Thus every pair is separated at least once.

Now consider the minimum number of practices. After `m` practices, every player can be described only by an `m`-bit signature. There are at most `2^m` distinct signatures. Since all `n` players must have different signatures, we need `2^m ≥ n`. Hence at least `⌈log₂ n⌉` practices are necessary.

Our construction uses exactly `⌈log₂ n⌉` practices, so it is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    m = 0
    while (1 << m) < n:
        m += 1

    print(m)

    for b in range(m):
        team = []
        for i in range(n):
            if (i >> b) & 1:
                team.append(str(i + 1))

        print(len(team), *team)

solve()
```

The first loop computes the minimum number of bits required to represent `n` distinct codes.

The player with number `i + 1` receives internal code `i`. Using `0..n-1` is important because exactly `n` distinct codes are needed and this avoids wasting one code value.

For each bit position, the solution gathers all players whose code contains a `1` in that bit. Those players form the first team. Everyone else implicitly belongs to the second team.

One subtle point is that the output format requires only one team to be listed. The remaining players automatically form the other team.

Another subtle point is proving that the listed team is never empty. Since `m` is the smallest value with `2^m ≥ n`, every bit position below `m` appears as `1` for at least one number among `0..n-1`. Thus every printed practice contains at least one player.

## Worked Examples

### Example 1

Input:

```
2
```

We need the smallest `m` with `2^m ≥ 2`, so `m = 1`.

| Bit position | Codes | Players with bit = 1 | Output line |
| --- | --- | --- | --- |
| 0 | 0,1 | {2} | `1 2` |

Output:

```
1
1 2
```

Player 1 and player 2 are on opposite teams in the only practice, so the unique pair is separated.

### Example 2

Input:

```
5
```

We need `m = 3` because `2^2 < 5 ≤ 2^3`.

Internal codes are:

| Player | Code |
| --- | --- |
| 1 | 000 |
| 2 | 001 |
| 3 | 010 |
| 4 | 011 |
| 5 | 100 |

Practice construction:

| Bit position | Players with bit = 1 |
| --- | --- |
| 0 | 2, 4 |
| 1 | 3, 4 |
| 2 | 5 |

Possible output:

```
3
2 2 4
2 3 4
1 5
```

Consider players 3 and 5. Their codes are `010` and `100`. They differ in bits 1 and 2, so they are separated in multiple practices. The same argument works for every pair because all codes are distinct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | We inspect every player for every bit position |
| Space | O(n) | One team list is stored at a time |

Since `n ≤ 1000`, we have at most `⌈log₂ 1000⌉ = 10` practices. The algorithm performs roughly `1000 × 10 = 10000` checks, which is trivial within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())

    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]

    for b in range(m):
        team = []
        for i in range(n):
            if (i >> b) & 1:
                team.append(str(i + 1))
        out.append(f"{len(team)}" + ("" if not team else " " + " ".join(team)))

    return "\n".join(out)

# provided sample
assert run("2\n") == "1\n1 2"

# minimum size
assert run("2\n").splitlines()[0] == "1"

# first non-power of two
assert run("3\n").splitlines()[0] == "2"

# power of two
assert run("8\n").splitlines()[0] == "3"

# maximum size
assert run("1000\n").splitlines()[0] == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | one practice | Smallest valid instance |
| `3` | two practices | Non-power-of-two transition |
| `8` | three practices | Exact power of two |
| `1000` | ten practices | Maximum constraint |

## Edge Cases

Consider:

```
2
```

The algorithm computes `m = 1`. Player 1 receives code `0`, player 2 receives code `1`. The single practice places player 2 in the listed team and player 1 in the other team. The only pair is separated immediately.

Consider:

```
5
```

The algorithm computes `m = 3`. The third practice contains only player 5 because only code `100` has the highest bit set. This is still valid because both teams remain non-empty. A careless implementation might incorrectly reject such highly unbalanced partitions.

Consider:

```
8
```

Here `m = 3` exactly. Every player receives a distinct 3-bit code from `000` to `111`. The construction achieves the lower bound exactly, showing that no fourth practice is needed. The pairwise separation property follows directly from the uniqueness of binary representations.
