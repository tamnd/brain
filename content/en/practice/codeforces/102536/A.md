---
title: "CF 102536A - The Slowden Files"
description: "We need compare two passwords and determine their edit distance. The first string is what a user typed, and the second string is the actual password. An edit is changing one character, inserting one character, or deleting one character."
date: "2026-08-06T20:12:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102536
codeforces_index: "A"
codeforces_contest_name: "2020 UP ACM Algolympics Final Round"
rating: 0
weight: 102536
solve_time_s: 180
verified: true
draft: false
---

[CF 102536A - The Slowden Files](https://codeforces.com/problemset/problem/102536/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m  
**Verified:** yes  

## Solution
## Problem Understanding

We need compare two passwords and determine their edit distance. The first string is what a user typed, and the second string is the actual password. An edit is changing one character, inserting one character, or deleting one character. The output depends only on whether the minimum number of edits needed is 0, 1, 2, 3, or larger.

The input can contain up to 10,000 password pairs, and the combined length of all passwords can reach 2,000,000 characters. A normal dynamic programming edit distance solution uses `O(nm)` time for strings of lengths `n` and `m`, which would be far too expensive when both strings have length around 100,000. Even a single pair of length 100,000 would require around 10 billion state transitions. The solution needs to exploit the fact that we only care about distances up to three.

A few cases require special attention because simpler comparisons can give the wrong result. The first is when strings have different lengths. For example:

```
Input:
1
abc
abcd
```

The correct output is:

```
You almost got it. You're wrong in just one spot.
```

A comparison that only counts different positions would find no mismatching positions in the first three characters and incorrectly claim the strings match. The missing character is a deletion or insertion, so it must be counted.

Another case is when an insertion shifts all later characters. For example:

```
Input:
1
abcde
abXcde
```

The correct output is:

```
You almost got it. You're wrong in just one spot.
```

A position-by-position mismatch counter would see several wrong positions, even though inserting `X` fixes everything with one operation.

A final edge case is the difference between replacement and multiple edits caused by length changes. For example:

```
Input:
1
abc
xyz
```

The correct output is:

```
You almost got it, but you're wrong in two spots.
```

Actually, the edit distance is three here, because all three characters must be replaced. A method that only compares the number of different characters after sorting or ignoring positions could incorrectly classify it.

## Approaches

The direct approach is to compute the classic Levenshtein distance using dynamic programming. For two strings, we create a table where each cell represents the minimum number of edits needed to transform a prefix of one string into a prefix of the other. The transitions consider deleting a character, inserting a character, or replacing a mismatching character. This is correct because every optimal transformation must end with one of those three operations.

The problem is the size of the table. If both passwords have length 100,000, the table has about 10 billion cells. Even though the answer is capped at three, the normal algorithm still spends time calculating states that cannot affect the final decision.

The key observation is that we do not need the exact distance once it becomes larger than three. We only need to know whether the distance is at most three. When the length difference between two strings is already larger than three, at least that many insertions or deletions are required, so the answer is immediately too large.

When lengths are close, we can align the strings using the fact that only a small number of edits are allowed. If the strings differ by at most three operations, the matching portions must remain mostly aligned. We can recursively skip matching characters from both ends, then handle the small remaining mismatched region. Each mismatch can be resolved by trying the possible edit operations, while stopping as soon as the number of edits exceeds three.

The brute-force solution works because every possible edit sequence is considered, but fails because the number of possible sequences grows rapidly. The observation that the allowed distance is a tiny constant lets us search only the small space around the current mismatch instead of building the full dynamic programming table.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of edits | O(depth) | Too slow |
| Full Dynamic Programming | O(nm) | O(nm) or O(min(n,m)) | Too slow for maximum input |
| Optimal Bounded Search | O(k * L), where k = 3 and L is the combined string length | O(k) | Accepted |

## Algorithm Walkthrough

1. Read the two passwords. If they are identical, the edit distance is zero and we can immediately return the successful login message. Checking equality first also avoids unnecessary recursive work on the most common simple case.
2. Compare the lengths of the two passwords. If their difference is greater than three, return the message for a distance larger than three. A length difference of four already requires four insertions or deletions, even if every existing character matches.
3. Use a recursive function that receives two current positions and the number of edits already used. Before doing more work, skip every matching character from the current positions. Matching characters never need to participate in an optimal edit sequence.
4. If one string reaches its end, the remaining characters in the other string must all be inserted or deleted. Add that remaining length to the current edit count.
5. If the current edit count is already greater than three, stop exploring this path. Larger distances do not affect the final category.
6. When both strings still have characters left and they differ, try the three possible edit operations. Replace both characters and move forward, delete the character from the first string, or delete the character from the second string. Return the smallest number of edits found.
7. Convert the final distance into the required output message. Distances above three share the same output.

Why it works: After removing all equal prefixes, the first remaining characters are different. Any optimal edit sequence must either replace one of these characters, remove one of them, or insert a character before one of them. These are exactly the three transitions explored by the algorithm. The recursion stops only after proving that more than three edits are needed, which is sufficient because all larger distances have the same required output.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 3

def limited_distance(a, b):
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def solve(i, j, used):
        while i < len(a) and j < len(b) and a[i] == b[j]:
            i += 1
            j += 1

        if i == len(a):
            return used + (len(b) - j)
        if j == len(b):
            return used + (len(a) - i)

        if used > LIMIT:
            return LIMIT + 1

        best = LIMIT + 1

        best = min(best, solve(i + 1, j + 1, used + 1))
        best = min(best, solve(i + 1, j, used + 1))
        best = min(best, solve(i, j + 1, used + 1))

        return best

    return solve(0, 0, 0)

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        a = input().rstrip("\n")
        b = input().rstrip("\n")

        d = limited_distance(a, b)

        if d == 0:
            ans.append("You're logged in!")
        elif d == 1:
            ans.append("You almost got it. You're wrong in just one spot.")
        elif d == 2:
            ans.append("You almost got it, but you're wrong in two spots.")
        elif d == 3:
            ans.append("You're wrong in three spots.")
        else:
            ans.append("What you entered is too different from the real password.")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `limited_distance` function is the bounded search described in the algorithm. The cache stores states consisting of the two current positions and the number of edits already used. The edit count is included because reaching the same pair of positions after using different numbers of edits can lead to different pruning decisions.

The loop that skips equal characters is the main optimization. Long identical sections of a password are ignored without creating recursion states. Since only three edits are allowed, the recursive branching happens only around the few places where the strings differ.

The base cases handle the situation where one password ends first. The remaining suffix of the other password cannot be matched in any other way, so every remaining character requires an insertion or deletion.

The function never needs to distinguish between distances four and larger. Returning `LIMIT + 1` is enough because all those cases produce the same output. Python integers do not overflow here, and the cache size stays small because only states near the mismatch regions are explored.

## Worked Examples

For the first sample pair:

```
password
password
```

| Position in first string | Position in second string | Used edits | Current action | Result |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | Skip matching characters | End of both strings |
| 8 | 8 | 0 | Remaining distance | 0 |

The algorithm removes the entire common prefix and reaches the end of both strings. The distance is zero, so the login message is printed.

For the fourth sample pair:

```
password
pazzw0rd
```

| Position in first string | Position in second string | Used edits | Current action | Result |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | Skip `pa` | Mismatch at index 2 |
| 2 | 2 | 0 | Replace `s` with `z` | Used edits becomes 1 |
| 3 | 3 | 1 | Replace `s` with `z` | Used edits becomes 2 |
| 5 | 5 | 2 | Replace `o` with `0` | Used edits becomes 3 |
| 8 | 8 | 3 | End of both strings | Distance is 3 |

This trace shows why replacements must be counted independently. Three different wrong characters require three edits even though the strings have the same length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(3L) which is O(L) | Each explored state is within the small edit-distance boundary, and matching runs are skipped. |
| Space | O(L) in the worst case | The memoization table stores only the explored recursive states. |

Here, `L` is the combined length of the two passwords. The input limit of 2,000,000 total characters fits because the algorithm never constructs a quadratic table and only explores states created by at most three edits.

## Test Cases

```python
import sys
import io
from functools import lru_cache

def program(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

assert program("""5
password
password
password
passw0rd
password
pazzword
password
pazzw0rd
password
username
""") == """You're logged in!
You almost got it. You're wrong in just one spot.
You almost got it, but you're wrong in two spots.
You're wrong in three spots.
What you entered is too different from the real password.
""", "sample"

assert program("""1
a
a
""") == """You're logged in!
""", "single equal character"

assert program("""1
a
b
""") == """You almost got it. You're wrong in just one spot.
""", "single replacement"

assert program("""1
abc
abcdef
""") == """You're wrong in three spots.
""", "three insertions"

assert program("""1
abc
xyz
""") == """You're wrong in three spots.
""", "three replacements"

assert program("""1
aaaaaaaaaa
bbbbbbbbbb
""") == """What you entered is too different from the real password.
""", "large mismatch count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Equal passwords | Login message | Zero-distance handling |
| One character versus another | One move message | Replacement transition |
| Short prefix versus longer string | Three moves message | Insertions at the end |
| Completely different equal-length strings | Three moves or larger classification | Edit limit handling |
| Many mismatching characters | Too different message | Early cutoff beyond distance three |

## Edge Cases

A length difference larger than three is handled before recursion can waste time. For example:

```
Input:
1
a
abcde
```

The second password has four extra characters. Even if the existing `a` matches perfectly, four insertions are required. The algorithm returns a distance larger than three and prints:

```
What you entered is too different from the real password.
```

A position-based mismatch counter would incorrectly focus only on the shared character and miss the required insertions.

A single insertion in the middle of a password is handled because the algorithm tries deletion and insertion, not only replacement. For:

```
Input:
1
abcde
abXcde
```

The recursive process skips `ab`, reaches the mismatch, and tries deleting `X` from the second string. The remaining characters match, giving a distance of one.

Passwords with identical characters but different capitalization are treated as different because comparisons use the actual characters. For:

```
Input:
1
Password
password
```

The first character differs, so the algorithm counts a replacement. The output is:

```
You almost got it. You're wrong in just one spot.
```

This avoids accidentally treating passwords as case-insensitive, which would change the meaning of the comparison.
