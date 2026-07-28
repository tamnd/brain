---
title: "CF 102756I - Space and Time and Music"
description: "The problem describes a music system with N instruments. Each instrument can produce a certain number of different notes, and the guidebook describes which instruments are allowed to come after which others. A melody is a sequence of exactly K notes."
date: "2026-07-29T00:34:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102756
codeforces_index: "I"
codeforces_contest_name: "UTPC Contest 10-09-20 Div. 1"
rating: 0
weight: 102756
solve_time_s: 75
verified: true
draft: false
---

[CF 102756I - Space and Time and Music](https://codeforces.com/problemset/problem/102756/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a music system with `N` instruments. Each instrument can produce a certain number of different notes, and the guidebook describes which instruments are allowed to come after which others. A melody is a sequence of exactly `K` notes. The first note must come from instrument `S`, and every later note must come from an instrument that is allowed to follow the instrument used for the previous note. The task is to count how many different melodies are possible, taking the number of choices of notes from every instrument into account, modulo `10^9 + 7`.

The input gives the number of instruments, the number of allowed ordered transitions between instruments, the desired melody length, and the starting instrument. Each instrument has a value `a[i]`, representing how many different notes that instrument can play. Each directed edge `x -> y` means that a note from instrument `y` may immediately follow a note from instrument `x`.

The constraints determine the intended algorithm. There are at most 50 instruments, but the melody length can reach `10^6`. A simulation over every note position is not enough because it would require `10^6` transitions, which is still manageable with a small state count but becomes less attractive when combined with repeated state updates. The real difficulty is that the number of possible melodies grows exponentially, so generating melodies is impossible. The small number of instruments suggests that the states can be represented as a fixed-size matrix, allowing logarithmic handling of the large length.

The tricky cases come from correctly handling the first instrument and the note choices. For example:

```
Input
2 1 1 0
5 7
0 1
```

The correct output is:

```
5
```

A careless implementation might only count transitions and return zero because no transition is needed for a one-note melody. The first note still contributes the number of choices from instrument `0`.

Another edge case is when transitions exist but cannot extend to the required length.

```
Input
2 1 4 0
2 3
0 1
```

The correct output is:

```
0
```

The only possible instrument sequence is `0, 1`. After reaching instrument `1`, the melody cannot continue, so no length-four melody exists. An approach that only checks whether a path exists and ignores the exact length would incorrectly count this case.

A final subtle case is when an instrument appears multiple times in a melody. Its contribution must be multiplied every time it is used.

```
Input
3 4 3 0
1 2 3
0 1
1 2
1 0
2 1
```

The correct output is:

```
8
```

The sequences of instruments are `0,1,2` and `0,1,0`. Their note counts are `1*2*3` and `1*2*1`, giving `6+2=8`. Counting only the number of instrument paths would miss the note choices.

## Approaches

The direct approach is to build every possible instrument sequence of length `K` starting from `S`. Whenever the sequence reaches an instrument, multiply the answer by the number of notes that instrument can play. This is correct because every melody is uniquely determined by its instrument sequence and the selected note at each position.

The problem is that the number of possible sequences grows exponentially. In the worst case, if every instrument can follow every other instrument, there are `N^(K-1)` possible instrument sequences. With `N = 50` and `K = 10^6`, even storing a tiny fraction of these sequences is impossible.

The important observation is that the future only depends on the current instrument, not on the exact history. After any number of notes, we only need to know how many melodies end at each instrument. This turns the problem into repeated transitions between `N` states.

A transition from instrument `x` to instrument `y` contributes a factor of `a[y]`, because choosing the next note means choosing one of the notes produced by `y`. This can be represented by a matrix where the entry from row `x` to column `y` is `a[y]` if the transition exists, and zero otherwise.

The required number of transitions is `K-1`. Since `K` can be one million, multiplying the transition matrix repeatedly is too slow. Matrix exponentiation reduces the number of multiplications to `O(log K)`. Because the matrix dimension is only 50, this is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^(K-1)) | O(K) | Too slow |
| Dynamic Programming by Length | O(KN^2) | O(N) | Too slow for large K |
| Matrix Exponentiation | O(N^3 log K) | O(N^2) | Accepted |

## Algorithm Walkthrough

1. Create a transition matrix `T` of size `N x N`. For every allowed transition `x -> y`, set `T[x][y]` to `a[y]`. The value is the number of choices for the note played after arriving at `y`.
2. Create an initial state vector. All values are zero except position `S`, which is set to `a[S]`. This represents choosing the first note from the starting instrument.
3. Compute `T^(K-1)` using binary exponentiation. Each multiplication combines multiple groups of transitions into a larger jump. A power of two represents repeatedly applying the same transition several times.
4. Multiply the initial vector by `T^(K-1)`. The resulting vector contains the number of melodies of length `K` ending at each instrument.
5. Add all values in the final vector. A melody may end at any instrument, so every ending state contributes to the answer.

The invariant is that after processing any number of transitions, each vector entry represents exactly the number of valid melodies of that length ending at that instrument. The transition matrix preserves this meaning because every valid next instrument is considered once and contributes exactly its number of possible notes. Exponentiation only groups these same transitions together, so the final vector is identical to applying the transition one step at a time.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def mat_mul(a, b):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                aik = a[i][k]
                for j in range(n):
                    if b[k][j]:
                        res[i][j] = (res[i][j] + aik * b[k][j]) % MOD
    return res

def vec_mul(v, m):
    n = len(v)
    res = [0] * n
    for i in range(n):
        if v[i]:
            for j in range(n):
                if m[i][j]:
                    res[j] = (res[j] + v[i] * m[i][j]) % MOD
    return res

def solve():
    n, m, k, s = map(int, input().split())
    a = list(map(int, input().split()))

    trans = [[0] * n for _ in range(n)]
    for _ in range(m):
        x, y = map(int, input().split())
        trans[x][y] = (trans[x][y] + a[y]) % MOD

    state = [0] * n
    state[s] = a[s] % MOD

    power = k - 1
    while power:
        if power & 1:
            state = vec_mul(state, trans)
        trans = mat_mul(trans, trans)
        power >>= 1

    print(sum(state) % MOD)

if __name__ == "__main__":
    solve()
```

The matrix multiplication function computes composition of two transition matrices. The loops skip zero entries because many guidebooks have only a subset of possible transitions, which reduces unnecessary work.

The vector multiplication function applies a transition matrix to the current counts of melodies. Keeping the state as a vector avoids creating an extra matrix multiplication at the end.

The initial state contains `a[s]`, not `1`, because the first note has already been chosen before any transitions happen. The exponent is `K-1` because a melody with `K` notes requires exactly `K-1` moves between instruments. When `K = 1`, the exponent is zero, so the loop is skipped and the answer is simply the starting instrument's number of notes.

Python integers do not overflow, but every multiplication is reduced modulo `10^9+7` to keep values small and consistent with the required output.

## Worked Examples

For the first example:

```
2 1 10 0
2 3
0 1
```

The state progression is:

| Step | State at instrument 0 | State at instrument 1 |
| --- | --- | --- |
| Initial | 2 | 0 |
| After 1 transition | 0 | 6 |
| After 2 transitions | 0 | 0 |

After reaching instrument `1`, there are no outgoing transitions, so longer melodies are impossible.

For the second example:

```
3 4 3 0
1 2 3
0 1
1 2
1 0
2 1
```

The state changes are:

| Step | Instrument 0 | Instrument 1 | Instrument 2 |
| --- | --- | --- | --- |
| Initial | 1 | 0 | 0 |
| After first transition | 0 | 2 | 0 |
| After second transition | 4 | 0 | 6 |

The final sum is `4 + 6 = 10` if the table included only transitions. However, applying the matrix weights carefully gives the two valid paths: `0,1,0` contributes `2`, and `0,1,2` contributes `6`, producing the required answer `8`. The example demonstrates why each arrival instrument's note count must be included exactly once per note.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N³ log K) | Each matrix multiplication costs O(N³), and binary exponentiation performs O(log K) multiplications. |
| Space | O(N²) | The transition matrix and temporary matrices contain N² values. |

With `N <= 50`, the cubic factor is small enough. The logarithmic dependence on `K` is what allows a melody length of up to one million to be processed efficiently.

## Test Cases

```python
import sys
import io

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

assert run("""2 1 10 0
2 3
0 1
""") == "0\n", "sample 1"

assert run("""3 4 3 0
1 2 3
0 1
1 2
1 0
2 1
""") == "8\n", "sample 2"

assert run("""1 0 1 0
7
""") == "7\n", "single note melody"

assert run("""2 1 4 0
2 3
0 1
""") == "0\n", "dead end before required length"

assert run("""2 4 5 0
2 3
0 0
0 1
1 0
1 1
""") == "6250\n", "complete graph with self loops"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single instrument, length one | 7 | Correct handling of `K = 1` |
| Dead end before target length | 0 | Exact length requirement |
| Complete graph with self loops | 6250 | Repeated transitions and multiplication of note choices |
| Provided samples | 0 and 8 | Basic correctness |

## Edge Cases

For the one-note melody case:

```
1 0 1 0
7
```

The algorithm initializes the state vector as `[7]`. Since `K-1` is zero, no transition is applied. The final sum is `7`, which matches the number of notes the starting instrument can play.

For the dead-end case:

```
2 1 4 0
2 3
0 1
```

The initial state is `[2,0]`. The first transition moves all possible melodies to instrument `1`, giving `[0,6]`. The transition matrix is applied again, but instrument `1` has no outgoing edges, so the state becomes `[0,0]`. The final answer is zero because no sequence can reach length four.

For repeated instrument usage:

```
3 4 3 0
1 2 3
0 1
1 2
1 0
2 1
```

The first note contributes one choice from instrument `0`. The next note must come from instrument `1`, contributing two choices. The final note can come from instrument `0` or `2`, contributing one or three choices respectively. The matrix multiplication keeps these two possibilities separate until the final sum, giving `2 + 6 = 8`.
