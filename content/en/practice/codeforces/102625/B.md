---
title: "CF 102625B - Amber Kand"
description: "We have two strings of equal length. The first string is the starting arrangement, and the second string is the target arrangement we want to reach."
date: "2026-08-03T15:17:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102625
codeforces_index: "B"
codeforces_contest_name: "IIT(ISM) Virtual Farewell"
rating: 0
weight: 102625
solve_time_s: 151
verified: true
draft: false
---

[CF 102625B - Amber Kand](https://codeforces.com/problemset/problem/102625/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two strings of equal length. The first string is the starting arrangement, and the second string is the target arrangement we want to reach. A move is allowed only when two neighboring characters belong to different groups: one group contains letters like `a`, `c`, `e`, where the position in the alphabet is odd, and the other contains letters like `b`, `d`, `f`, where the position in the alphabet is even. Such neighboring characters may be swapped.

The question is whether some sequence of valid swaps can transform the first string into the second one.

The length of each string can reach $10^5$. This immediately rules out approaches that try to simulate possible swap sequences or explore states, because even a linear number of choices at each position would create an enormous search space. A valid solution needs to inspect the strings a small number of times, which means an $O(n)$ or $O(n \log n)$ approach is suitable.

The main traps come from assuming that every permutation of characters is possible. For example:

```
Special:  ab
Elegant:  ba
```

The answer is `Yes`, because `a` and `b` are from different groups and can be swapped directly.

A more subtle case is:

```
Special:  abc
Elegant:  cba
```

The answer is `No`. The letters `a` and `c` belong to the same group, so they can never cross each other. A careless solution that only checks whether the two strings contain the same letters would incorrectly accept this case.

Another edge case is when the strings already have the same group order but different positions of groups:

```
Special:  abcde
Elegant:  baced
```

The answer is `Yes`. The relative order of odd-position alphabet letters is `ace` in both strings, and the relative order of even-position alphabet letters is `bd` in both strings. The allowed swaps can rearrange how these two groups are interleaved.

## Approaches

A brute-force solution would try to perform valid swaps and search through all possible strings that can be created. This is correct because every reachable state would eventually be explored, but the number of states grows extremely quickly. A string of length $10^5$ has far too many possible arrangements, so this approach is unusable.

A simpler but still inefficient idea is to repeatedly look for a character that is currently in the wrong place and move it toward its destination using adjacent swaps. Each movement can take $O(n)$ time, and doing this for many characters can lead to $O(n^2)$ operations. With $10^5$ characters, that would be around $10^{10}$ operations in the worst case.

The key observation is that the operation only swaps characters from different groups. Characters from the same group never pass each other. If we remove all even alphabet position letters from both strings, their remaining order must be identical. The same must be true after removing all odd alphabet position letters.

These two subsequences are the only information that cannot change. Once they match, the two strings are simply different interleavings of the same two sequences. Any such interleaving can be obtained by repeatedly swapping adjacent characters from different groups, because the operation is exactly moving one group element across elements of the other group.

The brute-force works because it follows every legal move, but it fails because there are too many possible moves. The observation about preserved subsequences reduces the whole problem to checking two linear scans.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Repeated adjacent movement | O(n²) | O(1) | Too slow |
| Preserved subsequences | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Separate both strings into two subsequences. The first subsequence contains letters with odd alphabet positions, and the second contains letters with even alphabet positions. Do this for both the starting string and the target string.
2. Compare the odd-position letter subsequence from the first string with the odd-position letter subsequence from the second string.

These characters can never change their relative order because valid swaps only move them around characters from the other group.
3. Compare the even-position letter subsequence in the same way.

The same reasoning applies: two even-position letters can never swap with each other.
4. If both pairs of subsequences are identical, print `Yes`. Otherwise, print `No`.

Matching subsequences mean that the two strings contain the same fixed order inside both groups. The remaining difference is only how these two groups are mixed together, and those changes are exactly what the allowed swaps can create.

Why it works:

Every valid swap exchanges one odd-position alphabet letter with one even-position alphabet letter. Because of this, neither group can change its internal order. Any reachable target must preserve both subsequences.

The reverse direction also holds. Suppose both subsequences match. Consider the odd and even letters as two queues that must be merged into the target order. Starting from the original string, an adjacent swap can move the next required letter from either queue across letters of the other queue until it reaches its desired position. Since all crossed letters belong to the opposite group, every such swap is valid. Repeating this process constructs the target string, so matching subsequences are also sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    t = input().strip()

    s_odd = []
    s_even = []
    t_odd = []
    t_even = []

    for c in s:
        if (ord(c) - ord('a') + 1) % 2 == 1:
            s_odd.append(c)
        else:
            s_even.append(c)

    for c in t:
        if (ord(c) - ord('a') + 1) % 2 == 1:
            t_odd.append(c)
        else:
            t_even.append(c)

    if s_odd == t_odd and s_even == t_even:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

The code builds four lists. The first two store the characters from the starting string separated by their group, and the other two do the same for the target string.

The alphabet position calculation uses `ord(c) - ord('a') + 1` because `ord` starts counting from zero for `a`, while the problem's grouping starts from one. A wrong parity calculation here would swap the two groups and make every answer incorrect.

The final comparison is enough because no other property of the string can affect reachability. The relative order inside each group is the only information that survives all valid operations.

## Worked Examples

For the first sample:

```
cheel
naara
```

The trace is:

| Character group | Starting string | Target string | Result |
| --- | --- | --- | --- |
| Odd alphabet positions | cee | aea | Different |
| Even alphabet positions | hl | nr | Different |

The odd group already differs, so these characters would need to cross each other. Since they belong to the same group, no sequence of allowed swaps can fix it. The answer is `No`.

For the second sample:

```
potha
opath
```

The trace is:

| Character group | Starting string | Target string | Result |
| --- | --- | --- | --- |
| Odd alphabet positions | oah | oah | Same |
| Even alphabet positions | pt | pt | Same |

Both groups keep their internal order. The strings only differ in how the two groups are interleaved, which can be changed using the allowed swaps. The answer is `Yes`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each string is scanned once and the subsequences are compared |
| Space | O(n) | The separated subsequences together contain all characters |

The maximum length is $10^5$, so a linear scan easily fits within the time limit. The memory usage is also well within the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve_case(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    s = sys.stdin.readline().strip()
    t = sys.stdin.readline().strip()

    s_odd = []
    s_even = []
    t_odd = []
    t_even = []

    for c in s:
        if (ord(c) - ord('a') + 1) % 2:
            s_odd.append(c)
        else:
            s_even.append(c)

    for c in t:
        if (ord(c) - ord('a') + 1) % 2:
            t_odd.append(c)
        else:
            t_even.append(c)

    ans = "Yes" if s_odd == t_odd and s_even == t_even else "No"

    sys.stdin = old_stdin
    return ans + "\n"

assert solve_case("cheel\nnaara\n") == "No\n", "sample 1"
assert solve_case("potha\nopath\n") == "Yes\n", "sample 2"

assert solve_case("a\na\n") == "Yes\n", "single character"
assert solve_case("ab\nba\n") == "Yes\n", "direct valid swap"
assert solve_case("abc\ncba\n") == "No\n", "same-group order cannot change"
assert solve_case("aaaaa\naaaaa\n") == "Yes\n", "all equal characters"
assert solve_case("aceg\ngeca\n") == "No\n", "large same-group reversal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` to `a` | Yes | Minimum size and no swaps |
| `ab` to `ba` | Yes | Direct swap between different groups |
| `abc` to `cba` | No | Same-group order preservation |
| `aaaaa` to `aaaaa` | Yes | All characters identical |
| `aceg` to `geca` | No | Boundary case where all letters are in one group |

## Edge Cases

For the case:

```
Special:
abc

Elegant:
cba
```

The algorithm separates both strings into odd and even groups. The odd subsequence of `abc` is `ac`, while the odd subsequence of `cba` is `ca`. Since these are different, the algorithm returns `No`. The failure comes from trying to reverse two letters that can never swap.

For the case:

```
Special:
ab

Elegant:
ba
```

The odd subsequences are both `a`, and the even subsequences are both `b`. The algorithm returns `Yes`. The characters can exchange places because they are from opposite groups.

For the case:

```
Special:
aaaa

Elegant:
aaaa
```

Both subsequences are identical because every character is the same group. The algorithm returns `Yes` immediately. This handles repeated characters without accidentally requiring unique positions.

For the case:

```
Special:
potha

Elegant:
opath
```

The odd group is `oah` in both strings, and the even group is `pt` in both strings. The algorithm accepts the transformation because the only changes needed are movements of one group through the other.
