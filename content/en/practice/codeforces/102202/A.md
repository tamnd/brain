---
title: "CF 102202A - Rainbow Beads"
description: "We have a string of length (N), where every jewel is one of R, B, or V. We may choose one contiguous substring and want its maximum possible length. A chosen substring must look diverse to three different observers."
date: "2026-08-24T05:07:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102202
codeforces_index: "A"
codeforces_contest_name: "2019 KAIST RUN Spring Contest"
rating: 0
weight: 102202
solve_time_s: 3406
verified: true
draft: false
---

[CF 102202A - Rainbow Beads](https://codeforces.com/problemset/problem/102202/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string of length (N), where every jewel is one of `R`, `B`, or `V`. We may choose one contiguous substring and want its maximum possible length.

A chosen substring must look diverse to three different observers. A normal observer distinguishes all three colors, a red-colorblind observer treats `V` as `R`, and a blue-colorblind observer treats `V` as `B`. For every observer, neighboring jewels must have different perceived colors.

The useful way to combine these three requirements is to examine every possible pair of neighboring original colors. Two equal colors are forbidden for the normal observer. The pair `R,V` is forbidden for the red-colorblind observer, because it becomes `R,R`. The pair `B,V` is forbidden for the blue-colorblind observer, because it becomes `B,B`. Consequently, among all possible distinct pairs, the only pair that survives is `R,B`.

That gives a much simpler restatement of the problem: a valid substring of length at least two can contain only `R` and `B`, and every neighboring pair must alternate. A `V` can only appear in a valid substring of length one.

The bound (N \le 250,000) rules out quadratic or worse algorithms in the intended solution. A single linear scan performs only a constant amount of work per jewel, which is comfortably within a 1 second limit in Python. An algorithm that examines every pair of positions would already perform about (31) billion pair checks at the maximum input size, so the structure of the valid substring needs to be exploited directly.

There are several small cases where an implementation based only on the original definition can go wrong. For input `1` followed by `V`, the answer is `1`, because a one-jewel substring has no adjacent pair to violate any condition. A careless implementation that looks only for alternating `R` and `B` might incorrectly return zero.

For input `3` with `RVB`, the answer is `1`. Although all three original colors are different, `RV` becomes `RR` for a red-colorblind observer and `VB` becomes `BB` for a blue-colorblind observer. Checking only whether neighboring original characters differ would incorrectly accept the whole string.

For input `4` with `RBRB`, the answer is `4`. Every adjacent pair is either `RB` or `BR`, so all three observers see different colors at every boundary. An implementation that treats the presence of multiple colors too loosely might miss that a fully alternating `R/B` string is valid.

## Approaches

A direct brute-force solution can enumerate every contiguous substring and test whether it satisfies all three observers. For a substring, checking every adjacent pair takes time proportional to its length, so the approach is correct because it explicitly verifies the definition before updating the best answer.

The problem is the number of substrings. There are (N(N+1)/2) of them, and if each one is checked from scratch, the total number of character inspections is

\frac{N(N+1)(N+2)}{6}.
]

For (N=250,000), this is approximately (2.6\times10^{15}) operations, far beyond the time limit. Even an improved brute-force implementation that extends each starting position until it encounters an invalid boundary still takes (O(N^2)) in the worst case, because an alternating string allows every extension to continue.

The key observation is that the three colorblindness conditions eliminate every adjacent pair except `R,B` and `B,R`. Once this is recognized, we no longer need to inspect arbitrary substrings. We only need the longest contiguous run in which every adjacent pair consists of different `R` and `B` characters.

This property can be maintained while scanning from left to right. If the current character is `R` or `B` and differs from the previous character, the current alternating run extends by one. Otherwise, the current run must restart at the current character. A `V` always starts a new run of length one, since no valid substring of length at least two can contain it.

The brute-force works because it tests every possible interval explicitly, but fails because there are too many intervals. The observation that the valid local transitions are exactly `R -> B` and `B -> R` turns the problem into finding one longest alternating run, which can be done in one pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^3)) when checking every substring from scratch | (O(1)) | Too slow |
| Brute Force with early stopping | (O(N^2)) | (O(1)) | Too slow |
| Optimal scan | (O(N)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the string and initialize the current valid run length to zero and the maximum answer to zero. A run represents a suffix ending at the current position whose every adjacent pair is valid.
2. Process the string from left to right. For the first character, start a run of length one. There is no previous character, so there is no boundary to check.
3. For every later character, check whether both the current character and the previous character belong to `{R, B}` and whether they are different. This is exactly the condition that the new adjacent pair is either `RB` or `BR`.
4. If that condition holds, increase the current run length by one. The newly added boundary is valid, and all earlier boundaries in the run were already valid.
5. Otherwise, start a new run of length one at the current character. This covers both a `V` and a repeated color such as `RR` or `BB`. Neither can extend the previous valid substring.
6. After determining the current run length, update the maximum answer. The longest run encountered during the scan is the longest valid substring.

### Why it works

The invariant is that after processing position (i), `current` is exactly the length of the longest valid substring that ends at position (i). If the new boundary is `RB` or `BR`, appending the current character preserves validity, so the previous run extends by one. For every other boundary, no valid substring of length at least two can cross that boundary, so the only valid substring ending at the current position has length one. Taking the maximum of these ending lengths considers every possible valid substring exactly where it ends, so the final maximum is the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    best = 1
    current = 1

    for i in range(1, n):
        if s[i] in "RB" and s[i - 1] in "RB" and s[i] != s[i - 1]:
            current += 1
        else:
            current = 1

        if current > best:
            best = current

    print(best)

if __name__ == "__main__":
    solve()
```

The input is read using `sys.stdin.readline`, which is sufficient for a string of length (250,000) and avoids unnecessary input overhead.

`current` stores the length of the valid alternating suffix ending at the current position. The condition

```
s[i] in "RB" and s[i - 1] in "RB" and s[i] != s[i - 1]
```

checks precisely whether the boundary between positions `i - 1` and `i` is allowed. Both characters must be non-`V`, and they must be different. Since the alphabet contains only `R`, `B`, and `V`, this is equivalent to saying that the pair is `RB` or `BR`.

When the condition fails, `current` becomes `1`, rather than `0`. The current jewel itself is always a valid one-jewel bead, even when it is `V`.

The answer is initialized to `1` because (N \ge 1). This also handles the all-`V` case without any special branch. No integer overflow is possible in Python, and the only stored input-sized object is the string itself.

## Worked Examples

### Sample 1

The input is `RBBB`. The only valid adjacent transition is between different `R` and `B` characters. After the first `B`, the next `B` breaks the alternating run, and the remaining `B` breaks it again.

| Position | Character | Previous | Valid transition | Current | Best |
| --- | --- | --- | --- | --- | --- |
| 0 | R | none | start | 1 | 1 |
| 1 | B | R | yes | 2 | 2 |
| 2 | B | B | no | 1 | 2 |
| 3 | B | B | no | 1 | 2 |

The substring `RB` has length two and satisfies every observer. No longer substring works because every substring containing two consecutive `B` jewels violates the normal observer's requirement. The answer is `2`.

### Sample 2

The input is `RBRBB`. The first four characters form an alternating `R/B` sequence. The final `B` is adjacent to another `B`, so it starts a new run.

| Position | Character | Previous | Valid transition | Current | Best |
| --- | --- | --- | --- | --- | --- |
| 0 | R | none | start | 1 | 1 |
| 1 | B | R | yes | 2 | 2 |
| 2 | R | B | yes | 3 | 3 |
| 3 | B | R | yes | 4 | 4 |
| 4 | B | B | no | 1 | 4 |

The substring `RBRB` has length four and every adjacent pair is either `RB` or `BR`. The final `BB` boundary prevents a length-five answer, so the result is `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | Every jewel is processed once with constant work. |
| Space | (O(N)) | The input string requires (O(N)) memory, while the algorithm itself uses (O(1)) additional space. |

With (N) at most (250,000), the scan performs only a few constant-time operations per character. This is easily compatible with the 1 second time limit, while the memory usage is far below the 1024 MB limit.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    best = 1
    current = 1

    for i in range(1, n):
        if s[i] in "RB" and s[i - 1] in "RB" and s[i] != s[i - 1]:
            current += 1
        else:
            current = 1

        best = max(best, current)

    print(best)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("4\nRBBB\n") == "2", "sample 1"
assert run("5\nRBRBB\n") == "4", "sample 2"

# Minimum-size input
assert run("1\nV\n") == "1", "single V"

# All equal values
assert run("5\nRRRRR\n") == "1", "all equal"

# V cannot participate in a valid substring of length > 1
assert run("3\nRVB\n") == "1", "V blocks both neighboring transitions"

# Maximum-size input
n = 250000
s = "".join("R" if i % 2 == 0 else "B" for i in range(n))
assert run(f"{n}\n{s}\n") == str(n), "maximum alternating string"

# Boundary and off-by-one case
assert run("6\nBRBBRB\n") == "3", "longest run is BRB"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / V` | 1 | Minimum size and the fact that a single `V` is valid |
| `5 / RRRRR` | 1 | Repeated colors cannot form a valid adjacent pair |
| `3 / RVB` | 1 | `V` cannot be adjacent to either `R` or `B` |
| `250000 / RBRB...` | 250000 | Maximum input size and a run reaching the full string |
| `6 / BRBBRB` | 3 | Restarting after an invalid boundary and avoiding off-by-one errors |

## Edge Cases

For a single jewel, consider the input

```
1
V
```

There is no adjacent pair at all, so every observer considers the bead valid. The algorithm starts `current` and `best` at `1` and never enters the loop, producing `1`.

For a substring containing `V`, consider

```
3
RVB
```

At position one, the pair `RV` is invalid because red-colorblind people perceive it as two red jewels. The algorithm resets the run to `1`. At position two, `VB` is invalid for the analogous blue-colorblind reason, so the run remains `1`. The result is `1`.

For repeated colors, consider

```
5
RRRRR
```

The first `R` creates a run of length one. Every subsequent `R` equals the previous character, so every transition is invalid and the run repeatedly resets to one. The answer is `1`.

For a fully alternating bead, consider

```
6
RBRBRB
```

Every boundary is either `RB` or `BR`, so `current` increases from `1` through `6`. The maximum becomes `6`, showing that the algorithm does not impose any unnecessary restriction on the length of an alternating `R/B` sequence.

The boundary case `BRBBRB` is useful for catching an off-by-one error. The scan produces run lengths `1, 2, 1, 1, 2, 3`, so the answer is `3`, represented by the final substring `BRB`. A careless implementation that updates the maximum before resetting or compares the wrong pair of indices can incorrectly report `2` or `4`.
