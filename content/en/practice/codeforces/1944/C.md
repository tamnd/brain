---
title: "CF 1944C - MEX Game 1"
description: "Alice and Bob play on a multiset of numbers. Alice and Bob alternately remove elements from the array, with Alice moving first. The difference is that whenever Alice removes a value, she also keeps it in her personal array c, while Bob simply deletes a value."
date: "2026-06-09T01:54:26+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "games", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1944
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 934 (Div. 2)"
rating: 1300
weight: 1944
solve_time_s: 209
verified: true
draft: false
---

[CF 1944C - MEX Game 1](https://codeforces.com/problemset/problem/1944/C)

**Rating:** 1300  
**Tags:** constructive algorithms, games, greedy  
**Solve time:** 3m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

Alice and Bob play on a multiset of numbers. Alice and Bob alternately remove elements from the array, with Alice moving first. The difference is that whenever Alice removes a value, she also keeps it in her personal array `c`, while Bob simply deletes a value.

When all elements have been removed, the score of the game is the MEX of `c`, meaning the smallest non-negative integer that does not appear among the values Alice collected.

Alice wants this MEX to be as large as possible. Bob wants it to be as small as possible. We must determine the final score assuming both players play perfectly.

The array values are always between `0` and `n-1`, and the total number of elements across all test cases is at most `2 · 10^5`. This immediately suggests that anything quadratic is too expensive. A solution that performs work proportional to the number of elements, or perhaps `n log n`, is easily fast enough.

The tricky part is that this is a game. A naive implementation might try to simulate optimal play move by move, but the number of possible game states grows exponentially. The real task is to understand which values Alice can force into her collection and which values Bob can prevent.

Several edge cases are easy to misjudge.

Consider:

```
2
1 1
```

There is no `0` at all. Alice can never obtain a `0`, so the answer is `0`.

Consider:

```
4
0 1 2 3
```

Every required value appears exactly once. Alice takes one of them, Bob immediately deletes another. Bob can destroy one missing ingredient of the future MEX, so the answer is only `1`, not `4`.

Consider:

```
4
0 0 1 1
```

Each important value appears twice. Alice can take one copy while Bob removes the other. Both `0` and `1` survive, so the answer becomes `2`.

A common mistake is to compute the ordinary MEX of the original array. The game is about which values Alice can guarantee to collect, not which values merely exist.

## Approaches

The brute force view is to treat the game as a minimax search. From every state, Alice chooses an element to maximize the eventual MEX, while Bob chooses an element to minimize it. This is correct because it directly models optimal play.

Unfortunately, even for modest `n`, the number of states becomes enormous. Every move branches into many possibilities, making the complexity essentially exponential. With `n` up to `2 · 10^5`, this is completely infeasible.

The key observation is that only the frequencies of the values matter.

Suppose we focus on some number `x`.

If `x` does not exist at all, Alice can never obtain it.

If `x` appears exactly once, then whichever player gets that unique copy determines whether `x` will belong to Alice's collection. Bob can always target such vulnerable values.

If `x` appears at least twice, Alice has much more protection. Even if Bob deletes one copy, another remains available.

To make the final MEX at least `k`, Alice must obtain every value from `0` through `k-1`.

Bob's best strategy is to create a missing value as early as possible. Values with frequency `1` are the only places where he can permanently destroy a number by taking its unique copy.

This leads to a remarkably simple characterization.

Scan values from `0` upward.

If a value never appears, that value becomes the answer immediately.

Among values that do appear, count how many have frequency exactly `1`.

The first value where this count reaches `2` is also the answer.

Why? Alice moves first, so among all singleton values she can secure at most one of them before Bob destroys another singleton. The second singleton becomes the first unavoidable gap in Alice's collection.

This transforms a game problem into a frequency-counting problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of every value in the array.
2. Initialize a counter `single = 0`. This will track how many values seen so far occur exactly once.
3. Scan values from `0` upward.
4. If the current value has frequency `0`, return this value immediately.

A missing value cannot be collected by Alice, so it is automatically the MEX.
5. If the current value has frequency `1`, increment `single`.
6. If `single` becomes `2`, return the current value.

Alice can guarantee possession of at most one singleton value. The second singleton creates the first value that Bob can force to be absent from Alice's collection.
7. The scan always terminates because values are restricted to the range `[0, n-1]`, and eventually some value beyond the existing frequencies will have count `0`.

### Why it works

For every value with frequency at least two, Bob cannot completely remove that value before Alice has a chance to obtain one copy. Such values are safe.

Values with frequency exactly one are fragile. Bob can permanently eliminate a singleton by taking its only copy. Since Alice moves first, she can protect at most one singleton value among the increasing sequence of values that matter for the MEX. Once two singleton values have appeared, Bob can always prevent one of them from entering Alice's collection. The smallest value where this becomes unavoidable is exactly the final MEX.

The first absent value also immediately determines the MEX because Alice cannot collect something that does not exist.

These two conditions completely characterize optimal play.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    answers = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = [0] * (n + 1)
        for x in a:
            freq[x] += 1

        single = 0

        for mex in range(n + 1):
            if freq[mex] == 0:
                answers.append(str(mex))
                break

            if freq[mex] == 1:
                single += 1

            if single == 2:
                answers.append(str(mex))
                break

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The frequency array is the core data structure. Since every value satisfies `0 ≤ a[i] < n`, an array of size `n + 1` is sufficient.

The scan proceeds in increasing order because MEX depends on the first problematic value. The moment we encounter a missing value, the answer is fixed and we stop.

The `single` counter tracks how many vulnerable values have appeared. The first singleton can be secured by Alice. The second singleton is where Bob can force a gap, so we return immediately.

One subtle detail is scanning through `n`. Even though input values are strictly less than `n`, the answer can be `n`. For example:

```
0 1 2 3
```

has ordinary MEX `4`. Using a frequency array of size only `n` would miss this possibility.

## Worked Examples

### Example 1

Input:

```
4
0 0 1 1
```

Frequency table:

| Value | Frequency | Single Count | Action |
| --- | --- | --- | --- |
| 0 | 2 | 0 | continue |
| 1 | 2 | 0 | continue |
| 2 | 0 | 0 | answer = 2 |

Output:

```
2
```

Both important values appear twice, so Bob cannot completely block either one. The first absent value is `2`, which becomes the final MEX.

### Example 2

Input:

```
4
0 1 2 3
```

Frequency table:

| Value | Frequency | Single Count | Action |
| --- | --- | --- | --- |
| 0 | 1 | 1 | continue |
| 1 | 1 | 2 | answer = 1 |

Output:

```
1
```

Every value is a singleton. Alice can secure only one of them. As soon as the second singleton appears, Bob can force a missing value among `{0,1}`, making the MEX equal to `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is counted once and each value is scanned once |
| Space | O(n) | Frequency array of size `n + 1` |

The total sum of `n` across all test cases is at most `2 · 10^5`. An `O(n)` solution processes only a few hundred thousand operations overall, which is comfortably within the time limit. The memory usage is also well below the available limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = [0] * (n + 1)
        for x in a:
            freq[x] += 1

        single = 0

        for mex in range(n + 1):
            if freq[mex] == 0:
                ans.append(str(mex))
                break

            if freq[mex] == 1:
                single += 1

            if single == 2:
                ans.append(str(mex))
                break

    return "\n".join(ans) + "\n"

# provided samples
assert run(
"""3
4
0 0 1 1
4
0 1 2 3
2
1 1
"""
) == "2\n1\n0\n", "sample 1"

# minimum size
assert run(
"""1
1
0
"""
) == "1\n", "single element 0"

# all equal values
assert run(
"""1
5
0 0 0 0 0
"""
) == "1\n", "all zeros"

# missing zero
assert run(
"""1
4
1 1 2 2
"""
) == "0\n", "mex starts at zero"

# two singleton values
assert run(
"""1
5
0 1 2 2 2
"""
) == "1\n", "second singleton determines answer"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 0` | `1` | Smallest valid input |
| `5 / 0 0 0 0 0` | `1` | All values identical |
| `4 / 1 1 2 2` | `0` | Missing zero handling |
| `5 / 0 1 2 2 2` | `1` | Second singleton rule |

## Edge Cases

Consider:

```
1
2
1 1
```

Frequency of `0` is already zero. During the scan, the algorithm immediately stops at value `0` and returns `0`. Alice cannot collect a value that does not exist, so the MEX must be `0`.

Consider:

```
1
4
0 1 2 3
```

The scan sees frequency `1` for value `0`, making `single = 1`. It then sees frequency `1` for value `1`, making `single = 2`, and returns `1`. This captures the fact that Bob can destroy one of the singleton values before Alice collects them all.

Consider:

```
1
6
0 0 1 1 2 2
```

All frequencies up to `2` are at least two. The singleton counter never increases. The scan reaches value `3`, whose frequency is zero, and returns `3`. Multiple copies protect every required value from Bob's interference.

Consider:

```
1
5
0 0 1 2 2
```

The scan processes:

| Value | Frequency | Single Count |
| --- | --- | --- |
| 0 | 2 | 0 |
| 1 | 1 | 1 |
| 2 | 2 | 1 |
| 3 | 0 | 1 |

The first missing value is `3`, so the answer is `3`. There is only one singleton, which Alice can secure, so Bob cannot force an earlier gap.
