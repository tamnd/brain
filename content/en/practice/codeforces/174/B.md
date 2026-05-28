---
title: "CF 174B - File List"
description: "We are given one long string that originally consisted of several file names written back to back with no separators. Every valid file name must look like name.ext. The rules are strict. The part before the dot contains only lowercase letters and has length from 1 to 8."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 174
codeforces_index: "B"
codeforces_contest_name: "VK Cup 2012 Round 3 (Unofficial Div. 2 Edition)"
rating: 1400
weight: 174
solve_time_s: 220
verified: true
draft: false
---

[CF 174B - File List](https://codeforces.com/problemset/problem/174/B)

**Rating:** 1400  
**Tags:** dp, greedy, implementation  
**Solve time:** 3m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given one long string that originally consisted of several file names written back to back with no separators. Every valid file name must look like `name.ext`.

The rules are strict. The part before the dot contains only lowercase letters and has length from 1 to 8. The extension after the dot also contains only lowercase letters and has length from 1 to 3. Each file name must contain exactly one dot.

Our task is to split the entire string into consecutive substrings so that every substring is a valid file name. If such a partition exists, we print any one of them. Otherwise we print `NO`.

The input length can reach `4 * 10^5`, which completely changes how we must think about the problem. Any solution that tries all partitions recursively will explode exponentially. Even an `O(n^2)` dynamic programming solution is risky at this scale because it would require around `1.6 * 10^11` operations in the worst case.

The key observation is that a valid file name has very small bounded length. The name contributes at most 8 characters, the extension contributes at most 3, and there is exactly one dot. So every valid segment has total length between 3 and 12. That means from any position we only need to check a constant number of possible next cuts.

Several edge cases are easy to mishandle.

A string without any dot can never work.

For example:

```
abcdef
```

There is no way to create a valid file name because every segment requires exactly one dot.

A segment containing multiple dots is also invalid.

For example:

```
a..b
```

A careless parser might split it as `a.` and `.b`, but neither side satisfies the rules because both the name and extension must contain letters.

Another tricky case is when the dot is too close to one end.

For example:

```
abcdefghij.k
```

The name part has length 10, which exceeds the maximum of 8.

Similarly:

```
a.abcd
```

The extension length is 4, which exceeds the maximum of 3.

One more subtle issue appears when a locally valid choice blocks the future.

Consider:

```
ab.cdex.f
```

The substring `ab.c` is valid, but the remaining `dex.f` is not because the name length is 3 and valid, actually this one works. A better example is:

```
a.bcdefghi.j
```

If we greedily take `a.b`, the remaining `cdefghi.j` is valid. But other greedy strategies can fail on different inputs. The problem requires checking whether the suffix can also be partitioned correctly.

This naturally leads to dynamic programming.

## Approaches

The brute-force idea is straightforward. Starting from the beginning of the string, try every possible next substring that could represent a file name. Then recursively solve the remaining suffix.

This works because every valid partition is eventually explored. The problem is the number of partitions. Even though each segment length is bounded, the branching factor is still large enough to create exponential behavior. A string of length `4 * 10^5` would be impossible to process this way.

Memoization improves things dramatically.

The important observation is that the validity of the remaining work depends only on the current index. Once we know whether the suffix starting at position `i` can be partitioned, we never need to recompute it again.

Even better, each state has only constant transitions. A valid file name length ranges from 3 to 12, so from each position we try at most 10 candidate substrings. Checking whether one substring is valid also costs constant time because the maximum length is tiny.

This transforms the exponential search into linear dynamic programming.

We define `dp[i]` as whether the suffix starting at index `i` can be partitioned into valid file names. The answer is `dp[0]`.

To transition from `i`, we try every endpoint `j` such that `s[i:j]` could be a valid file name. If the substring is valid and `dp[j]` is true, then `dp[i]` is also true.

We process states from right to left so that future values are already known.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) recursion | Too slow |
| Optimal DP | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Define a helper function that checks whether a substring is a valid file name.

The substring must contain exactly one dot. The part before the dot must have length from 1 to 8 and contain only lowercase letters. The part after the dot must have length from 1 to 3 and also contain only lowercase letters.
2. Create a DP array `dp` of size `n + 1`.

`dp[i]` means that the suffix starting at index `i` can be partitioned successfully. We set `dp[n] = True` because the empty suffix is already valid.
3. Create another array `nxt` to reconstruct the answer.

If we choose a valid segment from `i` to `j`, we store `nxt[i] = j`.
4. Process indices from right to left.

At each position `i`, try every substring length from 3 to 12, because those are the only possible file name lengths.
5. For each candidate substring `s[i:j]`, check two conditions.

First, the substring itself must be a valid file name.

Second, `dp[j]` must already be true, meaning the remaining suffix can also be partitioned.
6. If both conditions hold, mark `dp[i] = True` and store `nxt[i] = j`.

We can stop checking more candidates because any valid partition is acceptable.
7. After filling the DP table, check `dp[0]`.

If it is false, print `NO`.

Otherwise reconstruct the answer by repeatedly taking substrings `s[pos:nxt[pos]]`.

### Why it works

The DP invariant is simple.

`dp[i]` is true exactly when the suffix starting at `i` can be partitioned into valid file names.

The transition is complete because every valid partition must begin with some valid file name `s[i:j]`. After removing that first segment, the remaining suffix starts at `j`, so it must also be solvable.

The transition is sound because whenever we mark `dp[i] = True`, we have explicitly found a valid first segment and a valid partition of the remaining suffix.

Since we process from right to left, every needed future state is already known when we compute `dp[i]`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def valid_file(t: str) -> bool:
    if t.count('.') != 1:
        return False

    name, ext = t.split('.')

    if not (1 <= len(name) <= 8):
        return False

    if not (1 <= len(ext) <= 3):
        return False

    return name.islower() and ext.islower()

def solve():
    s = input().strip()
    n = len(s)

    dp = [False] * (n + 1)
    nxt = [-1] * (n + 1)

    dp[n] = True

    for i in range(n - 1, -1, -1):
        for length in range(3, 13):
            j = i + length

            if j > n:
                break

            if valid_file(s[i:j]) and dp[j]:
                dp[i] = True
                nxt[i] = j
                break

    if not dp[0]:
        print("NO")
        return

    print("YES")

    pos = 0
    while pos < n:
        print(s[pos:nxt[pos]])
        pos = nxt[pos]

solve()
```

The helper function directly encodes the file name rules. Since the maximum substring length is only 12, using operations like `count('.')` and `split('.')` is completely safe and still constant time.

The DP array is filled from right to left because each state depends on future positions. The empty suffix is marked reachable with `dp[n] = True`, which acts as the base case.

The inner loop tries only lengths from 3 to 12. The minimum possible valid file name is `"a.b"` with length 3. The maximum is `"abcdefgh.abc"` with length 12.

The reconstruction array `nxt` stores where the next segment begins. Without it, we would know only whether a solution exists, not how to print one.

One subtle implementation detail is the early `break` after finding a valid transition. The problem accepts any valid partition, so continuing the search is unnecessary.

Another important detail is using `j > n` as the stopping condition. This prevents out-of-range slicing logic and avoids checking impossible substrings.

## Worked Examples

### Example 1

Input:

```
read.meexample.txtb.cpp
```

| i | Candidate | Valid filename | dp[next] | dp[i] |
| --- | --- | --- | --- | --- |
| 18 | cpp | No | - | False |
| 15 | b.cpp | Yes | True | True |
| 9 | eexample.t | Yes | True | True |
| 0 | read.m | Yes | True | True |

Reconstructed partition:

```
read.m
eexample.t
xtb.cpp
```

This trace shows that the algorithm does not try to recover the original partition. It only needs any valid partition. Each chosen substring satisfies the file name constraints independently.

### Example 2

Input:

```
abcdef
```

| i | Candidate | Valid filename | dp[next] | dp[i] |
| --- | --- | --- | --- | --- |
| 5 | none | - | - | False |
| 4 | none | - | - | False |
| 3 | def | No | - | False |
| 0 | abcdef | No | - | False |

Since no substring contains a valid dot structure, every DP state remains false.

Output:

```
NO
```

This demonstrates that the algorithm correctly rejects strings with no possible valid segmentation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position checks at most 10 substring lengths |
| Space | O(n) | DP and reconstruction arrays |

The input size reaches `4 * 10^5`, so linear complexity is exactly what we need. The constant factor is also very small because each substring length is bounded by 12. The memory usage easily fits within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve_io(inp: str) -> str:
    input_data = io.StringIO(inp)
    output_data = io.StringIO()

    input = input_data.readline

    def valid_file(t: str) -> bool:
        if t.count('.') != 1:
            return False

        name, ext = t.split('.')

        if not (1 <= len(name) <= 8):
            return False

        if not (1 <= len(ext) <= 3):
            return False

        return name.islower() and ext.islower()

    s = input().strip()
    n = len(s)

    dp = [False] * (n + 1)
    nxt = [-1] * (n + 1)

    dp[n] = True

    for i in range(n - 1, -1, -1):
        for length in range(3, 13):
            j = i + length

            if j > n:
                break

            if valid_file(s[i:j]) and dp[j]:
                dp[i] = True
                nxt[i] = j
                break

    if not dp[0]:
        print("NO", file=output_data)
    else:
        print("YES", file=output_data)

        pos = 0
        while pos < n:
            print(s[pos:nxt[pos]], file=output_data)
            pos = nxt[pos]

    return output_data.getvalue()

# provided sample
out = solve_io("read.meexample.txtb.cpp\n")
assert out.startswith("YES")

# minimum valid case
assert solve_io("a.b\n") == "YES\na.b\n"

# no dot
assert solve_io("abcdef\n") == "NO\n"

# extension too long
assert solve_io("a.abcd\n") == "NO\n"

# maximum allowed lengths
assert solve_io("abcdefgh.abc\n") == "YES\nabcdefgh.abc\n"

# multiple valid partitions
out = solve_io("ab.cd.ef\n")
assert out.startswith("YES")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a.b` | `YES` | Smallest possible valid filename |
| `abcdef` | `NO` | Strings without dots |
| `a.abcd` | `NO` | Extension length limit |
| `abcdefgh.abc` | `YES` | Maximum allowed lengths |
| `ab.cd.ef` | `YES` | Multiple possible partitions |

## Edge Cases

Consider the input:

```
a..b
```

The substring contains two dots. During validation, `count('.') != 1` immediately rejects it. No DP transition becomes valid, so the algorithm prints:

```
NO
```

This prevents malformed names from slipping through.

Now consider:

```
abcdefghij.k
```

The only possible filename split is:

```
abcdefghij.k
```

The name length is 10, which exceeds the limit of 8. The validator rejects it, so `dp[0]` remains false.

The output is:

```
NO
```

Next examine:

```
a.abcd
```

The extension length is 4. The validator checks `1 <= len(ext) <= 3`, which fails. Again no valid transition exists.

Finally consider:

```
a.ba.bc
```

There are multiple possible local cuts. The algorithm checks all feasible substring lengths from each position and only accepts a segment if the remaining suffix is also solvable.

One valid partition is:

```
a.ba
.bc
```

Actually `.bc` is invalid because names cannot be empty. The DP correctly avoids this path. Instead it may choose:

```
a.b
a.bc
```

Both segments satisfy the constraints, so the algorithm prints a valid answer. This demonstrates why suffix feasibility must be part of the transition instead of making purely greedy choices.
