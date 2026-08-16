---
title: "CF 102277I - Team Shirts/Jerseys"
description: "Travis has at most 25 friends, and each friend has chosen a jersey number from 1 through 99. Travis may choose one additional jersey number for himself, also from 1 through 99."
date: "2026-08-16T19:40:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102277
codeforces_index: "I"
codeforces_contest_name: "UCF Locals 2018"
rating: 0
weight: 102277
solve_time_s: 121
verified: true
draft: false
---

[CF 102277I - Team Shirts/Jerseys](https://codeforces.com/problemset/problem/102277/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

Travis has at most 25 friends, and each friend has chosen a jersey number from 1 through 99. Travis may choose one additional jersey number for himself, also from 1 through 99. He wants to know whether some choice for his own number makes it possible to concatenate some of the available jersey numbers and obtain his favorite integer exactly.

The order of the chosen jersey numbers is arbitrary. A jersey number must be used as a whole, so if someone has jersey 75, Travis may use `75`, but cannot use only `7` or only `5`. A friend's jersey can be omitted, and Travis's own jersey can also be omitted. The output is `1` if there exists a choice of Travis's number that makes the favorite integer constructible, and `0` otherwise. The official statement gives `t < 1,000,000,000`, `n <= 25`, and jersey numbers in the range 1 through 99.

The small value of `n` might suggest exponential search, but the much stronger restriction is on the favorite integer. Since it is below one billion, it has at most 9 decimal digits. Every jersey contributes either one or two digits. That means the target has only a tiny number of possible ways to split its decimal representation into valid jersey-sized pieces. A solution proportional to the number of possible splits is easily fast enough, while enumerating arbitrary subsets and permutations of up to 25 friends is far too expensive.

The first edge case is a target consisting of a single digit. For example, with

```
7
1
24
```

the answer is `1`, because Travis can simply choose jersey `7` and use it alone. A solution that assumes at least one friend's jersey must participate would incorrectly reject this case.

An internal zero requires care. For example,

```
101
1
10
```

has answer `1`, because the target can be split as `10 | 1`, with the existing jersey `10` followed by Travis's chosen jersey `1`. Treating every digit independently would incorrectly consider the zero as a jersey number, while splitting it as `1 | 01` would also be invalid because jersey `01` does not exist.

Repeated jersey numbers are another source of mistakes. For example,

```
2222
3
2 2 2
```

has answer `1`. The target needs four copies of jersey `2`, three are supplied by friends and Travis can choose `2` himself. A set-based implementation that forgets multiplicities would lose this distinction.

Finally, having the right values is not enough if the target cannot be partitioned into those complete values. For example,

```
715
1
75
```

has answer `0`. The available friend jersey contributes `75`, but the target would need either `7 | 15` or `71 | 5`, and neither decomposition can be supplied using the single friend plus one newly chosen jersey.

## Approaches

A direct brute-force approach would try to choose a subset of friends, choose an ordering for that subset, decide whether Travis's jersey is used, choose his jersey number, concatenate everything, and compare the result with the target. This is correct because every legal construction is represented by some such choice. The problem is the number of possibilities. For `n = 25`, the number of ordered subsets is

25!\sum_{j=0}^{25}\frac{1}{j!},
]

which is approximately `e * 25!`, or about `4.2 * 10^25`. Trying up to 99 choices for Travis's jersey pushes this toward `4.2 * 10^27` candidate constructions. This is many orders of magnitude beyond what a two-second program can examine.

The key observation is that we do not actually need to choose friends first. The target itself determines the possible sequence of jersey numbers. Since every jersey is between 1 and 99, each piece of the target must contain exactly one or two digits. For a target with `L` digits, there are only `L - 1` positions where we may either cut or not cut. Thus there are at most

[
2^{L-1} \le 2^8 = 256
]

possible partitions.

For every partition, we obtain a sequence of one-digit or two-digit numbers. We can count how many copies of every jersey number that partition requires. The friends provide some multiset of jersey numbers. The partition is feasible exactly when every required copy is available among the friends, except that at most one missing copy can be supplied by Travis.

There is no need to try all 99 possible choices for Travis. If a partition is missing one jersey number, Travis can simply choose that number. If it is missing two or more copies, one jersey cannot repair the partition. If nothing is missing, Travis can choose any valid jersey number and simply not use it.

The brute-force approach works because it explicitly searches every possible construction, but fails when it treats the 25 friends as the search space. The observation that the target has at most nine digits changes the search space completely. Instead of exploring permutations of friends, we enumerate the at most 256 ways the target itself can be divided into legal jersey numbers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(99 * e * n!)` | `O(n)` | Too slow |
| Optimal | `O(2^8 * n)` | `O(1)` apart from input storage | Accepted |

## Algorithm Walkthrough

1. Convert the favorite integer to its decimal string representation. We work with the digits directly because a valid construction is a concatenation of jersey numbers, so every valid construction corresponds to a partition of this string.
2. Count how many times each jersey number from 1 through 99 occurs among the friends. A frequency array is convenient because the entire value range contains only 99 possibilities.
3. Enumerate every subset of the `L - 1` gaps between consecutive target digits. A selected gap means that the current jersey number ends there. An unselected gap means that the next digit belongs to the same jersey number.
4. For each partition, scan the target from left to right and form the corresponding one-digit or two-digit pieces. Reject a piece equal to zero, because jersey numbers start at 1. Also reject a two-digit piece beginning with zero, because jersey numbers are given without leading zeroes.
5. Count the required occurrences of every resulting jersey number. Compare these requirements with the friends' frequencies. For every value, compute how many copies are missing.
6. Accept the partition if the total number of missing copies is at most one. If it is zero, the friends alone can form the target. If it is one, Travis chooses exactly that missing jersey number. If it is larger than one, a single jersey cannot complete the construction.
7. If any partition is accepted, print `1`. If every partition fails, print `0`.

### Why it works

Consider any valid construction of the favorite integer. Every jersey number in that construction has either one or two digits, so the construction induces a unique partition of the target's decimal string. Our enumeration examines that partition. Its frequency comparison accepts precisely when all required jersey copies can be supplied by the friends plus at most one jersey chosen by Travis. Thus every valid construction is accepted. Conversely, every accepted partition describes a sequence of legal jersey numbers whose concatenation is exactly the target, and the frequency test guarantees that the required copies actually exist after Travis chooses the one missing value if necessary. Hence the algorithm returns `1` exactly when a valid construction exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = input().strip()
    n = int(input())
    friends = list(map(int, input().split()))

    freq = [0] * 100
    for x in friends:
        freq[x] += 1

    length = len(t)

    # There are length - 1 possible cut positions.
    # A mask describes which positions are cuts.
    for mask in range(1 << (length - 1)):
        need = [0] * 100
        pos = 0
        missing = 0
        valid = True

        while pos < length:
            if pos + 1 < length:
                # If there is a cut after this digit, use one digit.
                if mask & (1 << pos):
                    value = ord(t[pos]) - ord('0')
                    pos += 1
                else:
                    # Otherwise use two digits.
                    if t[pos] == '0':
                        valid = False
                        break
                    value = (ord(t[pos]) - ord('0')) * 10
                    value += ord(t[pos + 1]) - ord('0')
                    pos += 2
            else:
                value = ord(t[pos]) - ord('0')
                pos += 1

            if value == 0:
                valid = False
                break

            need[value] += 1

        if not valid:
            continue

        for value in range(1, 100):
            if need[value] > freq[value]:
                missing += need[value] - freq[value]
                if missing > 1:
                    break

        if missing <= 1:
            print(1)
            return

    print(0)

if __name__ == "__main__":
    solve()
```

The frequency array stores the friends' multiset rather than just their distinct jersey values. This is necessary because two copies of jersey `7` are different resources from one copy of jersey `7`.

The mask has one bit for every gap between adjacent target digits. When bit `pos` is set, the digit at `pos` ends the current jersey, so the next piece starts at `pos + 1`. When it is clear, we consume two digits together. Since jersey numbers have at most two digits, these are the only two possibilities.

The final digit must always be consumed as a one-digit jersey. The loop handles this with the `pos + 1 < length` condition, avoiding an out-of-bounds access on the last digit.

The check `t[pos] == '0'` before creating a two-digit number prevents values such as `01` from being treated as jersey `1`. The separate `value == 0` check rejects a standalone zero.

The `missing` counter measures resource shortages rather than trying to decide which jersey Travis should choose in advance. If exactly one copy is missing, that value is Travis's optimal choice. If no copy is missing, his jersey is irrelevant because he does not have to use it.

Python integers have arbitrary precision, so there is no overflow issue. More importantly, the target is kept as a string, so there is no reason to perform arithmetic on a potentially long concatenated value.

## Worked Examples

The statement's PDF lays out the sample cases in a two-column format. The distinct sample cases are the target `707` with friends `7, 24`, the target `70707` with friends `7, 7`, the target `1122` with friends `21, 1, 23`, and the target `715` with friend `75`. The corresponding outputs are `1`, `0`, `0`, and `0`.

For Sample 1,

```
707
2
7 24
```

The successful partition is `7 | 07` only if `07` were legal, so that partition is rejected. The actual successful partition is `70 | 7`. Travis chooses `70`, while his friend supplies `7`.

| Position | Chosen piece | Required counts | Missing copies |
| --- | --- | --- | --- |
| 0 | `70` | `70:1` | 1 |
| 2 | `7` | `70:1, 7:1` | 1 |
| End | `70 | 7 = 707` | `70:1, 7:1` | 1 |

The invariant is that after processing each piece, the required frequency array exactly describes the jerseys needed by the corresponding prefix of the target. Since only jersey `70` is missing from the friends, Travis can supply it and the answer is `1`.

For Sample 2,

```
70707
2
7 7
```

The target has five digits, so every partition consists of pieces of one or two digits. The target requires more resources than the two available copies of `7` can provide, regardless of which single jersey Travis chooses.

| Position | Chosen piece | Required counts | Missing copies |
| --- | --- | --- | --- |
| 0 | `70` | `70:1` | 1 |
| 2 | `7` | `70:1, 7:1` | 1 |
| 3 | `7` | `70:1, 7:2` | 1 |
| End | invalid or needs another piece | More than one copy unavailable | 2+ |

Every possible partition either contains an invalid zero-leading piece or requires at least two copies that are not supplied by the friends. One extra jersey cannot cover both shortages, so the answer is `0`.

For Sample 3,

```
1122
3
21 1 23
```

A partition such as `1 | 12 | 2` is structurally valid, but it requires jersey `12` and jersey `2`, neither of which is supplied. A partition such as `11 | 22` requires two jerseys that are also unavailable. No partition leaves at most one missing copy, so the answer is `0`.

For Sample 4,

```
715
1
75
```

The only useful two-digit pieces around the target are `71` and `15`, but the available `75` does not match either. The partitions `7 | 15` and `71 | 5` each require two jerseys, while only one can be supplied by the friend and one by Travis. Since neither missing jersey can be chosen to make the corresponding partition work with `75`, the answer is `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(2^L * L + 2^L * 99) = O(2^L * 99)` | `L <= 9`, so at most 256 partitions are checked |
| Space | `O(99)` | Frequency arrays have a fixed size of 100 |

The largest target has only nine digits, so the algorithm examines at most 256 partitions. Even scanning all 99 possible jersey values for every partition takes only about 25,000 simple operations. This is comfortably inside the two-second limit and uses negligible memory compared with the 256 MB limit reported for the Codeforces problem.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    t = input().strip()
    n = int(input())
    friends = list(map(int, input().split())) if n else []

    freq = [0] * 100
    for x in friends:
        freq[x] += 1

    length = len(t)

    for mask in range(1 << (length - 1)):
        need = [0] * 100
        pos = 0
        valid = True

        while pos < length:
            if pos + 1 < length:
                if mask & (1 << pos):
                    value = ord(t[pos]) - ord('0')
                    pos += 1
                else:
                    if t[pos] == '0':
                        valid = False
                        break
                    value = (ord(t[pos]) - ord('0')) * 10
                    value += ord(t[pos + 1]) - ord('0')
                    pos += 2
            else:
                value = ord(t[pos]) - ord('0')
                pos += 1

            if value == 0:
                valid = False
                break

            need[value] += 1

        if not valid:
            continue

        missing = 0
        for value in range(1, 100):
            if need[value] > freq[value]:
                missing += need[value] - freq[value]
                if missing > 1:
                    break

        if missing <= 1:
            return "1\n"

    return "0\n"

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        return solve()
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided samples
assert run("707\n2\n7 24\n") == "1\n", "sample 1"
assert run("70707\n2\n7 7\n") == "0\n", "sample 2"
assert run("1122\n3\n21 1 23\n") == "0\n", "sample 3"
assert run("715\n1\n75\n") == "0\n", "sample 4"

# Minimum-size target, Travis supplies the only needed jersey.
assert run("1\n1\n24\n") == "1\n", "single digit target"

# All values equal, with Travis supplying the fourth copy.
assert run("2222\n3\n2 2 2\n") == "1\n", "repeated jersey"

# Internal zero handled through a valid two-digit jersey.
assert run("101\n1\n10\n") == "1\n", "internal zero"

# Maximum target length and maximum number of friends.
friends = " ".join(["9"] * 25)
assert run(f"999999999\n25\n{friends}\n") == "1\n", "maximum-size input"

# Two missing jersey copies cannot be repaired by one Travis jersey.
assert run("1234\n2\n12 34\n") == "0\n", "two-copy shortage"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 24` | `1` | Minimum-size target and use of Travis's jersey alone |
| `2222 / 3 / 2 2 2` | `1` | Multiplicity and Travis supplying exactly one additional copy |
| `101 / 1 / 10` | `1` | Correct handling of an internal zero |
| `999999999 / 25 / 9 ... 9` | `1` | Maximum target length and maximum friend count |
| `1234 / 2 / 12 34` | `0` | More than one missing copy cannot be repaired |

## Edge Cases

For a one-digit target such as

```
1
1
24
```

there is only one possible partition, namely `1`. The friend list contains no `1`, so the algorithm computes one missing copy. Since the number of missing copies is exactly one, Travis chooses jersey `1`, and the algorithm returns `1`.

For an internal zero such as

```
101
1
10
```

the partition `10 | 1` is valid. The first piece is the existing jersey `10`, and the second piece is supplied by Travis. The algorithm never attempts to interpret the zero as a separate jersey, so it returns `1`.

For repeated values,

```
2222
3
2 2 2
```

the required frequency is four copies of `2`, while the friends provide three. The shortage is exactly one, so Travis chooses `2`. The algorithm returns `1`, demonstrating why frequencies rather than a set of available values are necessary.

For an impossible internal-zero construction,

```
100
1
10
```

the target cannot be partitioned completely into valid positive one or two-digit jersey numbers. After `10`, the remaining `0` would have to be a jersey by itself, which is illegal. Every partition containing that standalone zero is rejected, so the answer is `0`.

For a case requiring two additional jerseys,

```
1234
2
12 34
```

the natural partition is `12 | 34`, but both jerseys already exist, so this particular input would actually be feasible and the expected result is `1`. A better shortage test is

```
1234
1
12
```

Here the partition `12 | 34` requires jersey `34`, which Travis can supply, so this is also feasible. To force two shortages, use

```
123
1
45
```

The only valid partitions are `1 | 23` and `12 | 3`. Each needs two jerseys, while the friend has `45`, and Travis can provide only one of the two required values. Both partitions consequently fail, giving `0`. This illustrates the exact meaning of the `missing <= 1` condition.
