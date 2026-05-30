---
title: "CF 467B - Fedor and New Game"
description: "We are given a game with several players, each controlling an army composed of different types of soldiers. Each army is represented as a non-negative integer where the binary representation encodes the presence of soldier types: a bit set to 1 means the army includes that type."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 467
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 267 (Div. 2)"
rating: 1100
weight: 467
solve_time_s: 79
verified: true
draft: false
---

[CF 467B - Fedor and New Game](https://codeforces.com/problemset/problem/467/B)

**Rating:** 1100  
**Tags:** bitmasks, brute force, constructive algorithms, implementation  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a game with several players, each controlling an army composed of different types of soldiers. Each army is represented as a non-negative integer where the binary representation encodes the presence of soldier types: a bit set to 1 means the army includes that type. Fedor is the last player, and we are asked to determine how many other players have armies that differ from his in at most _k_ types of soldiers. In other words, the Hamming distance between Fedor’s army and another player’s army must be at most _k_.

The input consists of _n_, the total number of soldier types, _m_, the number of other players, and _k_, the friendship threshold in terms of differing soldier types. Each army is then listed as a number, including Fedor's at the end. The output is a single integer, counting Fedor’s potential friends.

The constraints give us _n_ up to 20, _m_ up to 1000, and _k_ up to _n_. With _n_ ≤ 20, every army can be represented as a 20-bit number, so operations on individual bits are fast. The upper bound on _m_ means we can examine each of the other players individually. A naive approach that compares each player to Fedor using bitwise operations will perform at most 20 × 1000 = 20,000 bit checks, which is well within the time limit. Edge cases include when _k_ = 0, where only armies identical to Fedor’s count, and when _k_ = _n_, where every player is a friend regardless of differences.

A careless implementation might try to compare decimal numbers directly instead of their binary representations or use string-based binary comparisons. For example, if Fedor's army is 15 (1111 in binary) and another player has 14 (1110 in binary), the naive decimal comparison would miss that they differ in exactly one type, which is allowed if _k_ ≥ 1.

## Approaches

The most straightforward solution is brute-force: for each of the first _m_ players, compute the number of differing bits between their army and Fedor’s army. This is equivalent to taking the bitwise XOR of the two numbers and counting the number of 1s in the result. Each 1 corresponds to a type of soldier where the armies differ. If the count is at most _k_, increment the friendship counter.

This brute-force works because the maximum bit length _n_ is small, so counting differing bits for each player is cheap. There is no need for more advanced techniques like precomputation or combinatorial optimizations. The key insight that simplifies the implementation is using the XOR operation, which converts the problem of counting differing soldier types into counting 1s in a single integer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m × n) | O(1) | Accepted |
| Optimal | O(m × n) | O(1) | Accepted |

The “optimal” here is essentially the same as brute-force, but the insight is recognizing the XOR operation and bit counting as a clean, efficient way to implement it.

## Algorithm Walkthrough

1. Read the integers _n_, _m_, and _k_ from input. These define the number of soldier types, the number of other players, and the maximum allowed differences for friendship.
2. Read the next _m + 1_ lines into an array of integers representing the armies. The last entry in this array is Fedor’s army.
3. Initialize a counter `friends = 0` to keep track of potential friends.
4. For each of the first _m_ armies, compute the bitwise XOR with Fedor’s army. This produces an integer where each bit set to 1 represents a type of soldier that differs between the two armies.
5. Count the number of 1s in the XOR result. This can be done using the built-in `bin(x ^ y).count('1')` in Python. If this count is less than or equal to _k_, increment the `friends` counter.
6. After iterating through all other players, print the `friends` counter.

Why it works: XOR isolates exactly the soldier types where armies differ. Counting 1s in the XOR result gives the Hamming distance. Since friendship is defined by having at most _k_ differences, comparing this count to _k_ correctly identifies potential friends. Every player is considered independently, and no approximation is involved, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())
armies = [int(input()) for _ in range(m + 1)]
fedor = armies[-1]

friends = 0
for i in range(m):
    diff = bin(armies[i] ^ fedor).count('1')
    if diff <= k:
        friends += 1

print(friends)
```

The solution first reads input efficiently using `sys.stdin.readline` to handle larger _m_. The army values are stored in a list for easy access, and Fedor’s army is accessed as the last element. The loop iterates only over the first _m_ players, ensuring we do not compare Fedor to himself. The XOR operation provides a concise way to capture differences, and counting bits via `bin(...).count('1')` leverages Python’s built-in binary representation.

## Worked Examples

**Sample 1**

Input:

```
7 3 1
8
5
111
17
```

| Player | Army | XOR with Fedor | Count of 1s | Friend? |
| --- | --- | --- | --- | --- |
| 1 | 8 | 8 ^ 17 = 25 | 3 | No |
| 2 | 5 | 5 ^ 17 = 20 | 2 | No |
| 3 | 111 | 111 ^ 17 = 126 | 6 | No |

`friends = 0`, which matches the expected output.

**Custom Sample 2**

Input:

```
4 3 2
3
5
6
7
```

| Player | Army | XOR with Fedor | Count of 1s | Friend? |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 ^ 7 = 4 | 1 | Yes |
| 2 | 5 | 5 ^ 7 = 2 | 1 | Yes |
| 3 | 6 | 6 ^ 7 = 1 | 1 | Yes |

All three are friends, `friends = 3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m × n) | Each of the m players is compared to Fedor using XOR and counting up to n bits. |
| Space | O(m) | Storing the army list of m + 1 players. |

With _m_ ≤ 1000 and _n_ ≤ 20, at most 20,000 bit comparisons are done, which is well within a 1-second time limit. Memory usage is trivial for these input sizes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, k = map(int, input().split())
    armies = [int(input()) for _ in range(m + 1)]
    fedor = armies[-1]
    friends = 0
    for i in range(m):
        if bin(armies[i] ^ fedor).count('1') <= k:
            friends += 1
    return str(friends)

# provided sample
assert run("7 3 1\n8\n5\n111\n17\n") == "0", "sample 1"

# minimum input
assert run("1 1 1\n1\n1\n") == "1", "minimum input"

# all equal armies
assert run("5 3 5\n31\n31\n31\n31\n") == "3", "all equal"

# maximum difference allowed
assert run("4 2 4\n1\n2\n15\n") == "2", "maximum difference"

# no friends
assert run("3 2 0\n1\n2\n3\n") == "0", "no friends"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 7 3 1 … | 0 | Provided sample |
| 1 1 1 … | 1 | Minimum input size |
| 5 3 5 … | 3 | All armies identical, k = n |
| 4 2 4 … | 2 | Maximum difference allowed by k |
| 3 2 0 … | 0 | k = 0, only identical armies count |

## Edge Cases

When _k_ = 0, only armies identical to Fedor’s are friends. For input:

```
3 2 0
5
6
5
```

XOR results: 5^5 = 0, 6^5 = 3. Count of 1s: 0 and 2. Only the first player is a friend, so the output is 1. The algorithm correctly captures this by comparing the bit count to _k_.

When _k_ = n, every player is a friend. For example:

```
3 2
```
