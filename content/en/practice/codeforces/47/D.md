---
title: "CF 47D - Safe"
description: "We are trying to reconstruct a hidden binary string of length n. Every guess Vasya made is another binary string of the same length, together with a number saying how many positions matched the real code exactly."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 47
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 44 (Div. 2)"
rating: 2200
weight: 47
solve_time_s: 100
verified: true
draft: false
---

[CF 47D - Safe](https://codeforces.com/problemset/problem/47/D)

**Rating:** 2200  
**Tags:** brute force  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are trying to reconstruct a hidden binary string of length `n`. Every guess Vasya made is another binary string of the same length, together with a number saying how many positions matched the real code exactly.

For example, if the hidden code is `101011` and a guess is `111001`, the answer would be `3` because the strings agree at three positions.

We are given up to ten such guesses. Every answer is at most `5`, which turns out to be the crucial restriction. The task is to count how many binary strings are consistent with all answers simultaneously.

The most direct interpretation is this: among all `2^n` binary strings, how many satisfy

$$\text{matches}(x, s_i) = c_i$$

for every attempt `i`.

The constraints completely rule out enumerating every possible code. Since `n` can reach `35`, the search space contains

$$2^{35} \approx 3.4 \times 10^{10}$$

strings. Even checking one billion strings per second would still be too slow.

The number of attempts is tiny, only at most `10`. That suggests the solution must exploit relationships between the guesses rather than brute-forcing all candidates.

The unusual restriction `c_i ≤ 5` is the real opening. Each guess differs from the true answer in at least `n - 5` positions. That means the hidden code is very far from every given string, and the number of corrections needed relative to any one guess is tiny.

Several edge cases are easy to mishandle.

Suppose two guesses are identical but demand different match counts:

```
6 2
000000 2
000000 3
```

No binary string can satisfy both conditions, so the correct answer is `0`. A careless implementation that processes constraints independently may accidentally count impossible states.

Another subtle case appears when a constraint demands zero matches:

```
6 1
000000 0
```

The only valid code is `111111`. Any implementation that thinks in terms of “changing a few bits” must still allow flipping every position if necessary.

There is also the case where many different corrections produce the same final string. For example:

```
6 2
000000 1
111111 5
```

Both constraints describe exactly the same set of strings, namely all strings with exactly one zero. A naive recursive search may double-count unless it stores complete assignments rather than paths.

## Approaches

The brute-force idea is straightforward. Enumerate every binary string of length `n`, compare it against all `m` guesses, and count how many satisfy all match counts.

Checking one candidate costs `O(mn)` because we compare against every guess character by character. The total complexity becomes

$$O(2^n \cdot m \cdot n)$$

which is hopeless for `n = 35`.

The structure of the constraints suggests a different viewpoint. Pick one guess as a reference string, say the first one. Its required match count is `c`.

Since the hidden string has exactly `c` matching positions with this reference, it differs in exactly

$$n - c$$

positions.

At first this still looks large, because `n - c` may be around `30`. But flipping the perspective helps.

Instead of constructing the hidden string directly, consider which positions remain equal to the reference string. Since `c ≤ 5`, there are at most five such positions.

That changes the search space dramatically. We only need to choose up to five positions that stay unchanged relative to the first guess. Every other position becomes the opposite bit automatically.

The number of such subsets is

$$\sum_{k=0}^{5} \binom{35}{k}$$

which is under `400000`. For each subset we can reconstruct exactly one candidate string and verify all constraints.

This works because binary strings have only two possible values at each position. Once we decide whether a position matches the reference string, its value is fixed.

The brute-force succeeds because every valid code can be checked independently. The optimized solution succeeds because the first constraint compresses the candidate space from `2^35` down to all subsets of size at most five.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot m \cdot n)$ | $O(1)$ | Too slow |
| Optimal | $O\left(mn \sum_{k=0}^{5}\binom{n}{k}\right)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all guesses and their required match counts.
2. Choose the first guess as the reference string.
3. Suppose the first guess has match count `c`. The hidden code must differ from this string in exactly `n - c` positions.
4. Instead of choosing differing positions, choose the positions that remain equal to the reference string. Their count is exactly `c`, and since `c ≤ 5`, the number of possibilities is small.
5. Enumerate every subset of positions of size `c`.

These positions are declared equal to the first guess. Every other position is flipped.
6. Construct the candidate string implied by this subset.

For every index:

- if the index belongs to the chosen subset, copy the reference bit
- otherwise, invert it

Because the alphabet is binary, this uniquely determines the whole string.
7. Check the candidate against every guess.

Count how many positions match. If every count equals the required value, the candidate is valid.
8. Count all valid candidates and print the total.

### Why it works

The first constraint partitions all positions into two groups: positions where the hidden string equals the reference guess, and positions where it differs.

Since the strings are binary, “different” means the opposite bit, not an arbitrary third value. Once the equal positions are chosen, the hidden string becomes completely determined.

Every valid hidden string corresponds to exactly one subset of equal positions of size `c`, and every such subset generates exactly one candidate string. The algorithm enumerates all these subsets and filters out those violating other constraints, so every valid solution is counted exactly once.

## Python Solution

```python
import sys
from itertools import combinations

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    strings = []
    counts = []

    for _ in range(m):
        s, c = input().split()
        strings.append(s)
        counts.append(int(c))

    base = strings[0]
    keep = counts[0]

    ans = 0
    positions = list(range(n))

    for same_positions in combinations(positions, keep):
        same_set = set(same_positions)

        candidate = []

        for i in range(n):
            if i in same_set:
                candidate.append(base[i])
            else:
                candidate.append('1' if base[i] == '0' else '0')

        candidate = ''.join(candidate)

        ok = True

        for s, need in zip(strings, counts):
            match = 0

            for a, b in zip(candidate, s):
                if a == b:
                    match += 1

            if match != need:
                ok = False
                break

        if ok:
            ans += 1

    print(ans)

solve()
```

The implementation follows the mathematical reduction directly.

The first important observation appears in these lines:

```
base = strings[0]
keep = counts[0]
```

We use the first guess as the reference string. Any valid answer must match it in exactly `keep` positions.

The loop

```
for same_positions in combinations(positions, keep):
```

enumerates every possible set of positions where the hidden code equals the reference string. Since `keep ≤ 5`, this enumeration stays small enough.

The candidate construction is subtle. For positions outside the chosen subset, we must flip the bit:

```
'1' if base[i] == '0' else '0'
```

This works only because the alphabet is binary. In a larger alphabet, differing from the reference would not uniquely determine the value.

The verification step compares the candidate against every guess and counts exact matches. The loop exits immediately after finding a contradiction, which avoids unnecessary work.

A common mistake is trying to mutate the reference string incrementally while iterating subsets. Rebuilding the candidate from scratch is simpler and avoids stale state bugs.

Another subtle point is uniqueness. Different subsets always generate different candidate strings because the positions equal to the reference are uniquely determined.

## Worked Examples

### Example 1

Input:

```
6 2
000000 2
010100 4
```

The first guess requires exactly two matching positions.

We enumerate all subsets of size `2`.

| Chosen equal positions | Constructed candidate | Matches with `000000` | Matches with `010100` | Valid |
| --- | --- | --- | --- | --- |
| {0,1} | 001111 | 2 | 2 | No |
| {0,2} | 010111 | 2 | 4 | Yes |
| {0,3} | 011011 | 2 | 4 | Yes |
| {1,2} | 100111 | 2 | 2 | No |
| {2,4} | 110101 | 2 | 4 | Yes |

Continuing this process yields six valid strings.

This trace demonstrates the core invariant: once the equal positions relative to the first guess are fixed, the entire candidate string is fixed automatically.

### Example 2

Input:

```
6 2
000000 0
111111 6
```

The first constraint says the hidden string matches `000000` in zero positions.

| Chosen equal positions | Constructed candidate | Matches with `000000` | Matches with `111111` | Valid |
| --- | --- | --- | --- | --- |
| {} | 111111 | 0 | 6 | Yes |

There is only one subset of size zero, producing exactly one candidate.

This example exercises the boundary case where every bit must flip.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O\left(mn \sum_{k=0}^{5}\binom{n}{k}\right)$ | Enumerate all subsets of size `c ≤ 5`, build each candidate, and verify against all guesses |
| Space | $O(n)$ | Storage for the current candidate string |

For `n = 35`, the largest number of subsets occurs at `c = 5`:

$$\binom{35}{5} = 324632$$

Each candidate requires at most `35 × 10 = 350` character comparisons, which easily fits inside the time limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from itertools import combinations

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())

    strings = []
    counts = []

    for _ in range(m):
        s, c = input().split()
        strings.append(s)
        counts.append(int(c))

    base = strings[0]
    keep = counts[0]

    ans = 0

    for same_positions in combinations(range(n), keep):
        same_set = set(same_positions)

        candidate = []

        for i in range(n):
            if i in same_set:
                candidate.append(base[i])
            else:
                candidate.append('1' if base[i] == '0' else '0')

        candidate = ''.join(candidate)

        ok = True

        for s, need in zip(strings, counts):
            match = sum(a == b for a, b in zip(candidate, s))

            if match != need:
                ok = False
                break

        if ok:
            ans += 1

    return str(ans)

# provided sample
assert run(
"""6 2
000000 2
010100 4
"""
) == "6", "sample 1"

# contradiction
assert run(
"""6 2
000000 2
000000 3
"""
) == "0", "contradiction"

# all bits flipped
assert run(
"""6 1
000000 0
"""
) == "1", "unique complement"

# exact original string
assert run(
"""6 1
101010 6
"""
) == "1", "only base string works"

# maximum keep value
assert run(
"""6 1
111111 5
"""
) == "6", "choose one differing position"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two identical guesses with different counts | 0 | Contradiction detection |
| Single guess with count 0 | 1 | Full complement construction |
| Single guess with count 6 | 1 | No flips required |
| Single guess with count 5 | 6 | Enumeration of all one-bit differences |

## Edge Cases

Consider the contradictory constraints case:

```
6 2
000000 2
000000 3
```

The algorithm enumerates every candidate with exactly two matching positions relative to `000000`. Every such candidate automatically has exactly two matches with the second identical string as well.

During verification:

| Candidate | Matches with first | Matches with second |
| --- | --- | --- |
| 001111 | 2 | 2 |
| 010111 | 2 | 2 |
| 111100 | 2 | 2 |

None satisfy the required value `3`, so the answer remains `0`.

Now examine the zero-match case:

```
6 1
000000 0
```

The chosen subset size is zero, so only the empty subset exists.

| Equal positions | Candidate |
| --- | --- |
| {} | 111111 |

The algorithm flips every bit and correctly finds the unique valid code.

Finally, consider overlapping constraints:

```
6 2
000000 1
111111 5
```

The first constraint generates all strings with exactly one zero:

| Equal positions | Candidate |
| --- | --- |
| {0} | 011111 |
| {1} | 101111 |
| {2} | 110111 |

Each candidate automatically matches `111111` in five positions, so all six candidates are accepted exactly once.

This confirms that the subset representation avoids duplicate counting.
