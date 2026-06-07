---
title: "CF 447A - DZY Loves Hash"
description: "We are tasked with simulating insertions into a hash table with a fixed number of buckets. Each bucket can hold at most one element. The hash function is simple: for a number $x$, the target bucket is $x mod p$. We receive a sequence of numbers and must insert them in order."
date: "2026-06-07T17:05:14+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 447
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round #FF (Div. 2)"
rating: 800
weight: 447
solve_time_s: 78
verified: true
draft: false
---

[CF 447A - DZY Loves Hash](https://codeforces.com/problemset/problem/447/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tasked with simulating insertions into a hash table with a fixed number of buckets. Each bucket can hold at most one element. The hash function is simple: for a number $x$, the target bucket is $x \mod p$. We receive a sequence of numbers and must insert them in order. If a number is destined for a bucket that is already occupied, a conflict occurs. The goal is to report the index of the insertion that causes the first conflict, or -1 if no conflict occurs.

The input gives $p$, the number of buckets, and $n$, the number of numbers to insert, followed by $n$ numbers. Both $p$ and $n$ are at most 300, and each number can be as large as $10^9$. This ensures that even a simple O(n) or O(n²) simulation is feasible, but we should avoid unnecessary nested loops.

Non-obvious edge cases include inserting the same number multiple times or numbers that collide under modulo arithmetic but are distinct. For example, if $p=3$ and the input sequence is 1, 4, 7, the modulo results are all 1. The first two insertions occupy the bucket successfully, but the third triggers a conflict. A careless implementation that does not check previous insertions under modulo would incorrectly allow multiple insertions into the same bucket.

## Approaches

The brute-force approach is to maintain an array of size $p$ representing the buckets. Each insertion checks if the target bucket is occupied. If it is, return the index. This approach is correct because it faithfully simulates the hash table behavior. The operation count is at most 300 insertions × 1 check per insertion, which is trivial for the given limits. There is no need for nested loops or fancy data structures.

The key insight for a slightly more elegant solution is realizing that the modulo operation guarantees the bucket index is in the range 0 to $p-1$. This allows using a fixed-size array to store occupancy flags, eliminating the need for dynamic data structures. Because the array index directly corresponds to the bucket number, every lookup and update is O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(p) | Accepted |
| Optimal | O(n) | O(p) | Accepted |

For this problem, brute force is essentially optimal because the input size is small and no asymptotic improvement is possible.

## Algorithm Walkthrough

1. Read $p$ and $n$ from input. Initialize an array `occupied` of size $p$ with all elements set to False. This array will track which buckets are already filled.
2. Iterate over the sequence of numbers with their 1-based index $i$. For each number $x$, compute the target bucket as `bucket = x % p`.
3. Check if `occupied[bucket]` is True. If so, a conflict has occurred, so immediately print $i$ and exit.
4. If the bucket is free, set `occupied[bucket]` to True and continue to the next number.
5. If all numbers are processed without encountering a conflict, print -1.

This algorithm works because the `occupied` array always accurately reflects which buckets are in use. Each insertion either marks a bucket as occupied or detects a conflict. Since each number is checked exactly once, there is no chance of missing a conflict. The invariants are that `occupied[bucket]` is True if and only if some previous number was inserted into that bucket, and the index $i$ returned is guaranteed to be the first conflict.

## Python Solution

```python
import sys
input = sys.stdin.readline

p, n = map(int, input().split())
occupied = [False] * p

for i in range(1, n + 1):
    x = int(input())
    bucket = x % p
    if occupied[bucket]:
        print(i)
        break
    occupied[bucket] = True
else:
    print(-1)
```

The first line reads the number of buckets and numbers. The `occupied` array is initialized to track bucket usage. The loop iterates with 1-based indexing to directly match the problem's requirement for the insertion index. The modulo operation computes the correct bucket. The `else` on the for-loop executes only if the loop completes without breaking, handling the "no conflict" case cleanly.

A subtle implementation point is using 1-based indexing for the result. Off-by-one errors are common here if you accidentally return `i-1` or start the loop at zero.

## Worked Examples

**Sample 1**: `p=10`, numbers=[0, 21, 53, 41, 53]

| Step | Number | Bucket (x % p) | occupied before | occupied after | Conflict? |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | [F]*10 | [T, F, F,...] | No |
| 2 | 21 | 1 | [T, F,...] | [T, T, F,...] | No |
| 3 | 53 | 3 | [T, T, F, F,...] | [T, T, F, T,...] | No |
| 4 | 41 | 1 | [T, T, F, T,...] | - | Yes |

The fourth insertion hits bucket 1, which is already occupied by 21. The algorithm correctly returns 4.

**Custom Input**: `p=5`, numbers=[0, 5, 10]

| Step | Number | Bucket | occupied before | occupied after | Conflict? |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | [F]*5 | [T, F, F, F, F] | No |
| 2 | 5 | 0 | [T, F, F, F, F] | - | Yes |

The conflict occurs on the second insertion. The algorithm handles repeated modulo results correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each number is processed once, with constant-time modulo and lookup. |
| Space | O(p) | We maintain an array of size equal to the number of buckets. |

Given $p, n \le 300$, this runs in milliseconds and uses negligible memory relative to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    exec(open("solution.py").read())
    return sys.stdout.getvalue().strip()

# provided sample
assert run("10 5\n0\n21\n53\n41\n53\n") == "4", "sample 1"

# minimum input, no conflict
assert run("2 1\n1\n") == "-1", "min input"

# conflict on first repeat
assert run("5 3\n0\n5\n10\n") == "2", "modulo repeat conflict"

# all numbers distinct modulo p
assert run("3 3\n1\n2\n0\n") == "-1", "distinct modulo"

# maximum n, simple conflict at the end
inp = "300 300\n" + "\n".join(str(i) for i in range(300)) + "\n0\n"
assert run(inp) == "301", "max n conflict"

# single conflict late
assert run("3 5\n1\n2\n4\n5\n7\n") == "4", "late conflict"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 1 | -1 | minimum-size input, no conflict |
| 5 3 0 5 10 | 2 | repeated modulo triggers conflict |
| 3 3 1 2 0 | -1 | all distinct modulo, no conflict |
| 300 300 sequence + 0 | 301 | maximum-size input with conflict |
| 3 5 1 2 4 5 7 | 4 | late conflict, correctness on small p |

## Edge Cases

The algorithm handles numbers larger than $p$ because modulo reduces them to valid bucket indices. Repeated numbers are correctly identified as conflicts on the first repeat. For minimum-size input, the loop completes without breaking, triggering the `else` clause and returning -1. All traces confirm that `occupied` faithfully records bucket usage and that the returned index always corresponds to the first conflict.
