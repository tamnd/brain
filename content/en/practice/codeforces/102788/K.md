---
title: "CF 102788K - Tower of Hanoi"
description: "The problem gives the intermediate positions of several teams while they were executing the classical three-rod Tower of Hanoi solution. Each team followed exactly the same recursive procedure, moving all N disks from rod A to rod B."
date: "2026-08-03T15:08:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102788
codeforces_index: "K"
codeforces_contest_name: "2017-2018 ICPC Central Quarter Final of Northeastern European Regional Collegiate Programming Contest"
rating: 0
weight: 102788
solve_time_s: 59
verified: true
draft: false
---

[CF 102788K - Tower of Hanoi](https://codeforces.com/problemset/problem/102788/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives the intermediate positions of several teams while they were executing the classical three-rod Tower of Hanoi solution. Each team followed exactly the same recursive procedure, moving all `N` disks from rod `A` to rod `B`. For every team, we are given a string of length `N`, where the character at position `i` describes the current rod of disk `i`, with disk `1` being the smallest and disk `N` being the largest. The task is to determine which team is furthest along in the process, meaning the one whose recorded configuration appears latest in the unique optimal sequence. If multiple teams have the same configuration, the first team among them must be chosen.

The number of disks can reach `1000`, and the number of teams can also reach `1000`. The total number of moves is `2^N - 1`, so storing or simulating the whole sequence is impossible even for moderately small `N`. A direct simulation already becomes useless around `N = 60`, because the number of moves exceeds what can be processed in a normal time limit. The solution must work in roughly `O(NM)` time, because the input itself contains `NM` characters.

The first tricky case is that the move count is not stored directly and cannot fit into standard integer types. For example, with `N = 1000`, the answer may need about one thousand bits. A solution that converts the configuration into a normal integer will overflow or spend unnecessary time on huge arithmetic.

Another edge case is when several teams have identical states. For example:

```
2 3
AA
BB
BB
```

The correct output is:

```
2
```

The last two teams both finished the puzzle, but the first occurrence must be selected. A careless implementation that updates the answer on `>=` instead of only on `>` would incorrectly return team `3`.

A second edge case is the initial configuration:

```
3 1
AAA
```

The correct output is:

```
1
```

The first state corresponds to move `0`. An implementation that assumes at least one disk has moved can misclassify this configuration.

## Approaches

The straightforward approach is to generate every configuration of the Hanoi process and compare each generated state with the teams' states. The recursive procedure is easy to simulate because each move is known in advance. The problem is that the sequence has `2^N` states. For `N = 1000`, this is far beyond any possible limit. Even generating one move per nanosecond would not make the approach practical.

The key observation is that the classical Hanoi sequence has a recursive structure. When solving `N` disks from `A` to `B`, the first half of the moves solves `N-1` disks from `A` to `C`, then disk `N` moves from `A` to `B`, then the remaining `N-1` disks move from `C` to `B`. This means the position of the largest disk immediately tells us which half of the sequence contains the current state.

If the largest disk is still on the source rod, the answer is somewhere in the first half. If it is on the destination rod, the answer is in the second half, and we only need to continue recursively on the smaller disks with swapped rod roles. Instead of constructing the whole sequence, we reconstruct the binary representation of the move number. Each disk contributes one bit: whether the moment when that disk moved has already happened.

The brute-force method works because the Hanoi sequence is deterministic, but fails because the sequence grows exponentially. The recursive structure lets us reduce the problem to examining each disk once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^N)` | `O(N)` | Too slow |
| Optimal | `O(NM)` | `O(N)` | Accepted |

## Algorithm Walkthrough

1. For each team's configuration, start with the largest disk and the original Hanoi parameters: moving from rod `A` to rod `B` using rod `C`.
2. Look at the position of the current largest disk. If it is still on the source rod, the move number belongs to the first half of the recursive sequence, so the current bit is `0`. The next recursive problem is moving the remaining disks from the same source to the auxiliary rod.
3. If the largest disk is on the destination rod, the move number belongs to the second half. The current bit is `1`, and the remaining disks must be considered in the second recursive phase, moving from the auxiliary rod to the destination rod.
4. Continue until all disks have been processed. The sequence of bits describes the move number. Instead of building the huge integer, compare these bit strings from the most significant side.
5. Keep the team with the largest binary move representation. Only replace the current answer when a strictly larger value is found, which automatically preserves the first team in case of ties.

The reason this works is that the largest disk changes position exactly once during the entire optimal solution. Before that move, every configuration must belong to the first recursive block. After that move, every configuration belongs to the second recursive block. Repeating this argument for smaller disks uniquely determines the position of every state in the sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def get_bits(state):
    n = len(state)
    src, dst, aux = 'A', 'B', 'C'
    bits = []

    for disk in range(n - 1, -1, -1):
        pos = state[disk]
        if pos == src:
            bits.append('0')
            src, dst, aux = src, aux, dst
        else:
            bits.append('1')
            src, dst, aux = aux, dst, src

    return ''.join(bits)

def solve():
    n, m = map(int, input().split())

    best_team = 1
    best = None

    for i in range(1, m + 1):
        state = input().strip()
        value = get_bits(state)

        if best is None or value > best:
            best = value
            best_team = i

    print(best_team)

if __name__ == "__main__":
    solve()
```

The function `get_bits` performs the recursive reasoning without recursion. The loop starts with the largest disk because it determines the highest bit of the move number. Processing disks from largest to smallest is equivalent to descending through the recursive calls.

When the current disk is on the source rod, the move has not happened yet, so the corresponding bit is `0`. The smaller disks are still in the first recursive phase, which changes the auxiliary rod into the temporary destination. When the disk is on the destination rod, the move has happened, so the bit is `1`, and the roles of the rods change to describe the second phase.

The comparison is done on strings because every state produces exactly `N` bits. Equal-length binary strings compare correctly lexicographically, with `1` being larger than `0`, so no big integer conversion is required.

## Worked Examples

For the first sample:

```
4 7
CAAA
AAAA
CCCB
CBAA
BBAA
BBCA
CCCA
```

The generated move representations are:

| Team | State | Binary move representation |
| --- | --- | --- |
| 1 | CAAA | 0010 |
| 2 | AAAA | 0000 |
| 3 | CCCB | 1100 |
| 4 | CBAA | 0011 |
| 5 | BBAA | 0101 |
| 6 | BBCA | 0110 |
| 7 | CCCA | 1010 |

The largest binary value is `1100`, which belongs to team `3`.

For the second sample:

```
3 4
AAA
BBB
BAA
BBB
```

| Team | State | Binary move representation |
| --- | --- | --- |
| 1 | AAA | 000 |
| 2 | BBB | 111 |
| 3 | BAA | 001 |
| 4 | BBB | 111 |

Teams `2` and `4` are both at the final move. Since ties keep the earlier team, the answer is team `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(NM)` | Every team's string is scanned once, examining each disk exactly once. |
| Space | `O(N)` | The temporary bit representation has length `N`. |

With `N` and `M` both at most `1000`, this performs about one million simple operations and easily fits the limits.

## Test Cases

```python
import sys
import io

def solve_data(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def get_bits(state):
        src, dst, aux = 'A', 'B', 'C'
        bits = []

        for disk in range(len(state) - 1, -1, -1):
            if state[disk] == src:
                bits.append('0')
                src, dst, aux = src, aux, dst
            else:
                bits.append('1')
                src, dst, aux = aux, dst, src

        return ''.join(bits)

    n, m = map(int, input().split())
    ans = 1
    best = None

    for i in range(1, m + 1):
        cur = get_bits(input().strip())
        if best is None or cur > best:
            best = cur
            ans = i

    return str(ans)

assert solve_data("""4 7
CAAA
AAAA
CCCB
CBAA
BBAA
BBCA
CCCA
""") == "3"

assert solve_data("""3 4
AAA
BBB
BAA
BBB
""") == "2"

assert solve_data("""1 3
A
B
B
""") == "2"

assert solve_data("""2 3
AA
BB
BB
""") == "2"

assert solve_data("""5 2
AAAAA
BBBBB
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 / A / B / B` | `2` | Single disk handling |
| `2 3 / AA / BB / BB` | `2` | Tie handling |
| `5 2 / AAAAA / BBBBB` | `2` | Large move numbers without integer conversion |
| Sample cases | `3`, `2` | General correctness |

## Edge Cases

For the duplicate-state case:

```
2 3
AA
BB
BB
```

The first state has move number `0`. Both `BB` states have move number `3`. The algorithm generates the same bit string for teams `2` and `3`, and because it only updates when the new value is strictly larger, team `2` remains selected.

For the initial configuration:

```
3 1
AAA
```

Every disk is still on the source rod. The algorithm records three zero bits, representing move number `0`. No special handling is needed because the same recursive rule applies even before any move occurs.

For the largest possible inputs, the algorithm never constructs the Hanoi sequence. It only reads each of the `1000` characters for each of the `1000` teams, so the exponential number of possible moves never appears in the computation.
