---
title: "CF 949A - Zebras"
description: "We are given a binary string representing a chronological sequence of days, where each character is either 0 or 1."
date: "2026-06-17T02:22:09+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 949
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 469 (Div. 1)"
rating: 1600
weight: 949
solve_time_s: 92
verified: false
draft: false
---

[CF 949A - Zebras](https://codeforces.com/problemset/problem/949/A)

**Rating:** 1600  
**Tags:** greedy  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string representing a chronological sequence of days, where each character is either 0 or 1. We must split these positions into several groups such that every position belongs to exactly one group, but each group does not need to consist of consecutive indices.

Each group must form a “zebra sequence.” A valid zebra sequence has three properties. It is non-empty, it starts with 0, it ends with 0, and adjacent elements in the subsequence must alternate between 0 and 1.

This immediately implies that every valid subsequence must look like 0, 01, 010, 0101, and so on, but always ending on 0, so its length is odd and it contains one more zero than ones.

We are asked to decide whether such a partition is possible, and if it is, to output any valid partition.

The input size goes up to 200,000 characters, which rules out anything quadratic or even $O(n \log n)$ with heavy constants unless it is extremely well-structured. A linear or near-linear greedy construction is expected.

A key structural constraint hides inside the definition: every zebra starts and ends with 0, so every group must consume zeros in a way that they serve as both starts and ends. This already suggests that zeros will control feasibility.

A naive mistake is to try building subsequences greedily without tracking availability of alternating structure, or to assign zeros independently without pairing them with ones correctly. Another common failure is ignoring the fact that ones must always sit between two zeros in their subsequence; any 1 that cannot be paired in alternating fashion forces failure.

A small illustrative failure case is `111000`. There are enough zeros and ones overall, but any attempt to start multiple sequences fails because there are no alternating patterns possible starting from zeros in a way that consumes all ones correctly. The correct output is `-1`.

Another subtle case is `0101`. It looks alternating, but it ends in 1, so no subsequence can include it entirely; it is impossible to assign it into valid zebra sequences.

## Approaches

A brute-force approach would try to partition indices into groups and check each group for validity. This means assigning each index to one of possibly $O(n)$ subsequences and verifying alternation per group. Even if we restrict ourselves to greedy assignment, the number of ways to distribute elements grows exponentially, and verification itself is linear per candidate partition. This is completely infeasible at $n = 2 \cdot 10^5$.

The key observation is that the structure of each zebra is rigid. Since sequences must alternate and start with 0, every time we place a 1, it must continue a previously started sequence that currently ends in 0. Similarly, every 0 either starts a new sequence or closes an existing one that expects a 0 next.

This suggests maintaining two dynamic sets of “open subsequences”: those currently ending in 0 and those ending in 1. We always want to match characters greedily: a 1 must extend a sequence ending in 0, and a 0 must extend a sequence ending in 1 or start a new sequence.

The crucial insight is that we are not choosing partitions freely; instead, we are effectively threading sequences through the string. Each index attaches to exactly one chain, and chains evolve in a stack-like fashion based on the last expected character. This reduces the problem to a greedy construction with bookkeeping of active sequences.

At the end, all sequences must end in 0, meaning no sequence can be left expecting a 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Partitioning | Exponential | O(n) | Too slow |
| Greedy Chain Assignment | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two stacks (or lists): one for sequences that currently end in 0, and one for sequences that currently end in 1. Each sequence is represented by its collected indices.

1. Iterate through the string from left to right.
2. When we see a `0`, we must attach it to a sequence that currently ends in `1` if such a sequence exists, because that preserves alternation. If no such sequence exists, we start a new sequence with this index. Starting new sequences with 0 is valid because they begin correctly.
3. When we see a `1`, we must attach it to a sequence that currently ends in `0`. If none exists, the construction is impossible and we immediately fail.
4. After attaching, we move the sequence between stacks because its ending character flips.
5. After processing all characters, we verify that no sequence ends in `1`. Any such sequence would violate the requirement that all sequences end with 0.

The decision at each step is forced by the alternation rule. A 1 cannot start a zebra and cannot follow another 1, so it always consumes an available “open zero-ended chain.”

### Why it works

At every prefix of the string, each active sequence is uniquely characterized by its last element. The algorithm ensures that any sequence ending in 1 is always waiting for a 0 next, and any sequence ending in 0 is waiting for a 1 next. Since a valid zebra must alternate strictly, any deviation from greedy assignment would only delay consumption of a character and reduce future flexibility. Because 1 has only one valid predecessor state (0-ended sequences), and 0 has a choice that never reduces feasibility when a 1-ended sequence exists, the greedy choice preserves all future possibilities. If at any point a 1 cannot be assigned, no rearrangement could fix it because every sequence that could accept it is already structurally incompatible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    zero_end = []  # sequences ending with 0
    one_end = []   # sequences ending with 1
    res = []       # list of sequences

    # each sequence is a list of indices
    for i, ch in enumerate(s, 1):
        if ch == '0':
            if one_end:
                seq = one_end.pop()
                seq.append(i)
                zero_end.append(seq)
            else:
                seq = [i]
                zero_end.append(seq)
        else:  # ch == '1'
            if not zero_end:
                print(-1)
                return
            seq = zero_end.pop()
            seq.append(i)
            one_end.append(seq)

    # all sequences must end with 0
    if one_end:
        print(-1)
        return

    print(len(zero_end))
    for seq in zero_end:
        print(len(seq), *seq)

if __name__ == "__main__":
    solve()
```

The solution maintains explicit sequences and dynamically moves them between states depending on the last character appended. The critical implementation detail is that sequences are stored directly, so no reconstruction is needed at the end.

One subtlety is the handling of the final validation: any sequence left in the “ends with 1” pool is invalid, since a zebra must end in 0.

## Worked Examples

### Example 1

Input: `0010100`

We track how sequences evolve.

| Step | Char | Zero-end sequences | One-end sequences | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | [1] | [] | start new |
| 2 | 0 | [1], [2] | [] | start new |
| 3 | 1 | [1,3] | [2] | move seq 1→1 |
| 4 | 0 | [2,4] | [1] | extend seq 2 |
| 5 | 1 | [2,4,5] | [1] | extend |
| 6 | 0 | [1,6] | [2,4,5] | move seq 1 |
| 7 | 0 | [1,6], [2,4,5,7] | [] | move seq |

All sequences end in 0, so output is valid.

This trace shows that zeros either start new chains or fix existing ones, while ones strictly consume open zero-ended chains.

### Example 2

Input: `0101`

| Step | Char | Zero-end | One-end | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | [1] | [] | start |
| 2 | 1 | [] | [1,2] | extend |
| 3 | 0 | [1,3,2] | [] | extend |
| 4 | 1 | [] | [1,3,2,4] | extend |

Final sequences end in 1, so no valid partition exists.

This demonstrates the necessity that every chain must terminate on 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each index is pushed and popped at most once |
| Space | O(n) | storing all indices in sequences |

The linear scan and constant-time stack operations ensure the solution fits comfortably within limits for $n = 200{,}000$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    s = sys.stdin.readline().strip()
    zero_end = []
    one_end = []

    for i, ch in enumerate(s, 1):
        if ch == '0':
            if one_end:
                seq = one_end.pop()
                seq.append(i)
                zero_end.append(seq)
            else:
                zero_end.append([i])
        else:
            if not zero_end:
                return "-1"
            seq = zero_end.pop()
            seq.append(i)
            one_end.append(seq)

    if one_end:
        return "-1"

    out = [str(len(zero_end))]
    for seq in zero_end:
        out.append(str(len(seq)) + " " + " ".join(map(str, seq)))
    return "\n".join(out)

# provided sample
assert run("0010100\n") != "-1"

# custom cases
assert run("0\n") == "1\n1 1", "single zero"
assert run("1\n") == "-1", "single one invalid"
assert run("0101\n") == "-1", "alternation ends wrong"
assert run("001100\n") != "-1", "balanced structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1 / 1 1` | minimal valid case |
| `1` | `-1` | impossible start |
| `0101` | `-1` | ending constraint violation |
| `001100` | valid partition | multiple chains interaction |

## Edge Cases

A critical edge case is when the string starts with a long run of ones, such as `11100`. At the first character, there is no existing zero-ended sequence to attach to, so the algorithm immediately rejects the input. This is correct because no zebra can begin with 1.

Another edge case is a perfectly alternating prefix that ends in 1, such as `010`. The algorithm will successfully build a sequence ending in 1, but the final validation fails because a zebra must end in 0. This shows why final state checking is essential and cannot be replaced by local checks during construction.

A third case is multiple competing sequences, for example `000111000`. The algorithm creates multiple chains as needed, and each 1 consumes a different open zero-ended sequence. The correctness here comes from the fact that we never force two 1s into the same chain unless structure allows it.
