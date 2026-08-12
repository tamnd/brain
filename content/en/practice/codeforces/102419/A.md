---
title: "CF 102419A - Two Strings"
description: "We have two strings a and b of the same length. We must choose two different positions and swap those positions in both strings simultaneously. The goal is to make the resulting a lexicographically larger than the resulting b."
date: "2026-08-12T20:05:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102419
codeforces_index: "A"
codeforces_contest_name: "SPC 2019"
rating: 0
weight: 102419
solve_time_s: 629
verified: true
draft: false
---

[CF 102419A - Two Strings](https://codeforces.com/problemset/problem/102419/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two strings `a` and `b` of the same length. We must choose two different positions and swap those positions in both strings simultaneously. The goal is to make the resulting `a` lexicographically larger than the resulting `b`.

The crucial detail is that a swap moves an entire pair `(a[i], b[i])`. We do not independently choose characters from the two strings. If position `i` is moved to position `j`, both of its characters move together.

Lexicographic comparison is decided by the first position where the two strings differ. At such a position, `a` wins exactly when `a[i] > b[i]`. So for every position, only the relation between its two characters matters:

`a[i] > b[i]` means this position is favorable to `a`.

`a[i] = b[i]` means this position is neutral.

`a[i] < b[i]` means this position is unfavorable to `a`.

The length can reach `10^5`, so an algorithm that examines every pair of positions and then compares the resulting strings is far too expensive. There are about `n^2 / 2` possible swaps, and comparing two strings can take `O(n)`, giving `O(n^3)` character work in the worst case. With `n = 10^5`, we need a linear or near-linear solution.

There are several small cases that can fool a naive strategy. For example,

```
2
ba
ab
```

Here the original first position has `b > a`, but the only possible swap moves the unfavorable second pair to the front. The result is `ab` versus `ba`, so the answer is `NO`. Merely finding one position where `a[i] > b[i]` is not enough when that position is already first and `n = 2`.

Another case is

```
3
abc
abc
```

Every position is neutral, so no swap can ever create a position where `a` has a larger character. The answer is `NO`. A solution that assumes any swap can change the comparison would incorrectly accept this case.

At the other extreme,

```
3
zzz
aaa
```

already has `a[0] > b[0]`. We are required to swap, but we can swap positions `2` and `3`, leaving the first position untouched. The answer is `YES`.

## Approaches

The direct brute-force approach is to try every pair `(x, y)`, perform the swap in copies of the two strings, and compare the resulting strings lexicographically. There are `n(n-1)/2` pairs, which is `O(n^2)`, and each comparison can inspect `O(n)` characters. The worst case is thus `O(n^3)`. For `n = 100000`, this is roughly `10^15` character-level operations, far beyond the time limit.

The useful observation is that we do not actually care about the exact characters at every position. For lexicographic comparison, a position only needs to be classified as favorable, neutral, or unfavorable according to the comparison of `a[i]` and `b[i]`.

Suppose we find a position `p` where `a[p] > b[p]`. If `p` is not the first position, swapping positions `0` and `p` immediately solves the problem. After the swap, position `0` contains the old pair from `p`, so the new strings satisfy `a[0] > b[0]`. The strings are consequently ordered correctly regardless of what happens later.

If the favorable position is already position `0`, we cannot use it as the destination of another swap without moving it away. When `n >= 3`, we can simply swap positions `1` and `2`. Position `0` remains unchanged, so it still gives `a[0] > b[0]`. This also satisfies the requirement that exactly one swap is performed.

Only `n = 2` needs special handling when the favorable position is already first. There is only one possible swap, so after swapping, the old second position becomes the first position. The swap succeeds exactly when `a[1] >= b[1]`. If the second position is neutral, the new first position is equal and the favorable pair moves to the second position. If the second position is also favorable, the first position remains favorable. If it is unfavorable, the resulting first position makes `a < b`.

The observation reduces the whole problem to one scan for a position with `a[i] > b[i]`, plus a constant amount of work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the strings from left to right and find any index `p` such that `a[p] > b[p]`. If no such index exists, output `NO`. A swap only moves existing pairs between positions, so it can never create a favorable pair if none exists initially.
2. If `p > 0`, output positions `1` and `p + 1`. After swapping them, the pair originally at `p` moves to the first position, giving `a[0] > b[0]`. The resulting strings are immediately ordered with `a` larger than `b`.
3. If `p = 0` and `n >= 3`, output positions `2` and `3`. The first position is not touched, so the strict inequality `a[0] > b[0]` remains the first decisive comparison. The swap is still performed because the problem requires exactly one operation.
4. If `p = 0` and `n = 2`, the only possible swap is positions `1` and `2`. After this swap, the old second position becomes the first position. Accept the swap exactly when `a[1] >= b[1]`; otherwise output `NO`.

The invariant behind the solution is that a position's comparison relation moves together with its pair `(a[i], b[i])`. Whenever we move a known favorable pair to the first position, it becomes the first decisive comparison and proves `a > b`. When the favorable pair is already first, we can preserve it by swapping two later positions, provided two such positions exist. The only situation where that is impossible is `n = 2`, where the sole alternative must be checked directly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = input().strip()
    b = input().strip()

    pos = -1

    for i in range(n):
        if a[i] > b[i]:
            pos = i
            break

    if pos == -1:
        print("NO")
        return

    if pos > 0:
        print("YES")
        print(1, pos + 1)
        return

    if n >= 3:
        print("YES")
        print(2, 3)
        return

    # n == 2 and the favorable position is already position 1.
    if a[1] >= b[1]:
        print("YES")
        print(1, 2)
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The scan stores the first position where `a[i] > b[i]`. Any such position is sufficient, because if it is not already first, moving it to the first position settles the lexicographic comparison immediately.

The `pos > 0` branch uses zero-based Python indices but prints one-based positions. Thus position `0` becomes `1`, while `pos` becomes `pos + 1`.

When `pos == 0` and `n >= 3`, positions `1` and `2` in zero-based indexing correspond to output positions `2` and `3`. They are guaranteed to exist because `n >= 3`, and neither affects the favorable first position.

The final branch is only reached for `n == 2`. There is exactly one legal swap, so checking `a[1] >= b[1]` is sufficient. Equality is accepted because after the swap the first characters may be equal, allowing the favorable pair from the original first position to decide the comparison at the second character.

No string copying or mutation is necessary. The algorithm only determines a valid pair of indices, so the extra memory usage is constant.

## Worked Examples

### Sample 1

The input is

```
3
abc
abc
```

The scan proceeds as follows.

| index | `a[index]` | `b[index]` | relation | `pos` |
| --- | --- | --- | --- | --- |
| 0 | a | a | equal | -1 |
| 1 | b | b | equal | -1 |
| 2 | c | c | equal | -1 |

No position satisfies `a[i] > b[i]`, so `pos` remains `-1`.

The algorithm prints:

```
NO
```

This demonstrates that swapping positions cannot manufacture a favorable pair. All pairs are neutral, so every possible permutation leaves the two strings identical.

### Sample 2

The input is

```
3
zzz
aaa
```

The scan stops immediately.

| index | `a[index]` | `b[index]` | relation | `pos` |
| --- | --- | --- | --- | --- |
| 0 | z | a | `a > b` | 0 |

The favorable position is already first, and `n = 3`, so the algorithm swaps positions `2` and `3`.

| Operation | First position after swap | Resulting comparison |
| --- | --- | --- |
| swap positions 2 and 3 | `z` vs `a` | `z > a` |

The resulting strings are still `zzz` and `aaa`, but the required swap has been performed. The output is

```
YES
2 3
```

The example demonstrates why the operation being mandatory does not cause a problem when there are at least two positions after an already favorable first position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The strings are scanned once to find a position with `a[i] > b[i]`. |
| Space | O(1) | Only the input strings and a constant number of indices are stored; no additional structure depends on `n`. |

With `n <= 10^5`, a linear scan performs only about one hundred thousand character comparisons, which is easily within the 1 second limit. The algorithm also uses constant auxiliary space, far below the 256 MB memory limit.

## Test Cases

```python
import sys
import io
from contextlib import redirect_stdout

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = input().strip()
    b = input().strip()

    pos = -1

    for i in range(n):
        if a[i] > b[i]:
            pos = i
            break

    if pos == -1:
        print("NO")
        return

    if pos > 0:
        print("YES")
        print(1, pos + 1)
        return

    if n >= 3:
        print("YES")
        print(2, 3)
        return

    if a[1] >= b[1]:
        print("YES")
        print(1, 2)
    else:
        print("NO")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    output = io.StringIO()

    try:
        sys.stdin = io.StringIO(inp)
        with redirect_stdout(output):
            solve()
    finally:
        sys.stdin = old_stdin

    return output.getvalue()

# Provided samples
assert run("""3
abc
abc
""") == "NO\n", "sample 1"

assert run("""3
zzz
aaa
""") == "YES\n2 3\n", "sample 2"

# Minimum size, favorable position is second.
assert run("""2
ab
aa
""") == "YES\n1 2\n", "minimum size with favorable second position"

# Minimum size, favorable position is first but the second position is unfavorable.
assert run("""2
ba
ab
""") == "NO\n", "minimum size impossible case"

# All positions equal.
assert run("""4
abcd
abcd
""") == "NO\n", "all-equal strings"

# Maximum size, favorable position is the final character.
n = 100000
a = "a" * (n - 1) + "b"
b = "a" * n
assert run(f"{n}\n{a}\n{b}\n") == f"YES\n1 {n}\n", "maximum size and last position"

# Favorable position is first, with exactly three positions.
assert run("""3
baa
abb
""") == "YES\n2 3\n", "favorable first position"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / ab / aa` | `YES / 1 2` | Minimum length with the favorable pair at the second position. |
| `2 / ba / ab` | `NO` | The special `n = 2` case where the only swap makes `a < b`. |
| `4 / abcd / abcd` | `NO` | No favorable position exists anywhere. |
| `100000 / a...ab / a...a` | `YES / 1 100000` | Maximum length and a favorable position at the last index, catching indexing mistakes. |
| `3 / baa / abb` | `YES / 2 3` | Favorable first position while exactly one swap must still be performed. |

## Edge Cases

### No favorable position

Consider

```
3
abc
abd
```

Every position satisfies `a[i] <= b[i]`. The scan reaches the end without finding a favorable pair, so `pos = -1` and the algorithm prints `NO`. Since swapping only relocates existing pairs, no operation can make a larger character appear in `a` than in `b` at a position where it was previously impossible.

### Favorable position is already first with three or more positions

Consider

```
3
baa
abb
```

At position `1`, `b > a`, so the scan finds `pos = 0`. Since there are at least three positions, the algorithm chooses positions `2` and `3`. The first pair remains `(b, a)`, so the resulting strings still satisfy `a > b` immediately at their first character. The required swap changes only later positions.

### Favorable position is first with two positions

Consider

```
2
ba
ab
```

The first position has `b > a`, but the second has `a < b`. Since `n = 2`, the only legal operation swaps the two positions. The result becomes `ab` and `ba`, whose first characters satisfy `a < b`. The algorithm checks `a[1] >= b[1]`, finds `a < b`, and correctly prints `NO`.

The contrasting case

```
2
ba
aa
```

has `b > a` at the first position and `a = a` at the second. After swapping, the strings become `ab` and `aa`. The first characters are equal, and the second comparison is `b > a`, so the result is valid. The algorithm accepts because `a[1] >= b[1]`.

### Favorable position at the final index

Consider

```
4
aaab
aaaa
```

The only favorable position is index `4`, where `b > a` in the notation of the strings, specifically `b > a`. The zero-based scan finds `pos = 3`. Swapping positions `1` and `4` moves that favorable pair to the front, producing a first-character comparison of `b > a`. The algorithm outputs `YES 1 4`.

This case exercises the `pos + 1` conversion and shows why any favorable position away from the front can be moved directly to the front.
