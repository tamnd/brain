---
title: "CF 102318B - Simplified Keyboard"
description: "The problem uses a small custom keyboard containing all 26 lowercase letters. The letters are arranged in three rows: Two words are given for each test case. We must classify the pair into one of three categories."
date: "2026-08-13T23:53:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102318
codeforces_index: "B"
codeforces_contest_name: "UCF Locals 2017"
rating: 0
weight: 102318
solve_time_s: 76
verified: true
draft: false
---

[CF 102318B - Simplified Keyboard](https://codeforces.com/problemset/problem/102318/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem uses a small custom keyboard containing all 26 lowercase letters. The letters are arranged in three rows:

```
a b c d e f g h i
j k l m n o p q r
s t u v w x y z
```

Two words are given for each test case. We must classify the pair into one of three categories. They are **identical** if they have the same length and every corresponding character is equal. They are **similar** if they have the same length, are not identical, and every corresponding pair of characters is either equal or occupies neighboring positions on the keyboard. If neither condition holds, they are **different**.

The original contest statement gives words of length from 1 through 20, and the first input value specifies how many word pairs follow.

The small word length means there is no need for advanced data structures or asymptotically complicated algorithms. Even a linear scan through every character is tiny, at most 20 character comparisons for one test case. The only meaningful design choice is how efficiently we determine whether two letters are keyboard neighbors. Since the keyboard has only 26 fixed letters, we can encode every letter's row and column directly and answer that question in constant time.

There are several cases where a careless implementation can give the wrong classification. Different lengths must immediately produce `3`. For example:

```
1
ab abc
```

The correct output is:

```
3
```

A program that only checks the overlapping characters would see `a` versus `a` and `b` versus `b` and might incorrectly call the words similar.

Two words with the same length but identical characters must produce `1`, not `2`. For example:

```
1
cool cool
```

The correct output is:

```
1
```

A program that checks whether every pair is equal or neighboring and returns `2` without first checking whether the whole words are identical would misclassify this case.

Adjacency is based on the keyboard geometry, including diagonal neighbors. For example:

```
1
knq bxz
```

The correct output is:

```
2
```

Here `k` is next to `b`, `n` is next to `x`, and `q` is next to `z`. Treating only horizontally and vertically touching keys as neighbors would incorrectly reject this pair.

## Approaches

A straightforward brute-force solution can process each position independently. For every pair of corresponding letters, we can scan all 26 keyboard letters to find whether the second letter belongs to the neighborhood of the first. Since a word contains at most 20 characters, this performs at most (20 \times 26 = 520) letter checks for one test case. Across (n) test cases, the worst case is (520n) such checks, in addition to the normal input processing. The approach is correct because it directly tests the definition of similarity, but repeatedly searching the fixed 26-letter keyboard is unnecessary work.

The key observation is that the keyboard never changes. Every letter has a fixed row and column, so we can map a character to its coordinates using its alphabet index. For a character with alphabet index `p`, its row is `p // 9` and its column is `p % 9`. The first two rows contain nine letters each, while the final row contains eight.

Two letters are neighbors exactly when their row difference is at most one and their column difference is at most one. Equality also satisfies that condition, so the algorithm can first determine whether the entire words are identical. If they are not identical, we only need to verify the neighbor condition at every position.

This reduces the work for each test case to a single scan of the words. The brute-force solution works because the keyboard is tiny, but fails to exploit the fact that its geometry is fixed. Replacing repeated searches with direct coordinate arithmetic turns the classification into a simple linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26L) per test case | O(1) | Correct, but unnecessary repeated work |
| Optimal | O(L) per test case | O(1) | Accepted |

Here (L) is the word length, with (L \le 20).

## Algorithm Walkthrough

1. Read the number of test cases, then read the two words belonging to the current test case. The classification is independent for each pair, so every case can be processed separately.
2. If the two words have different lengths, output `3`. Similarity requires a character-to-character correspondence across the entire words, so different lengths make both identity and similarity impossible.
3. If the two words are exactly equal, output `1`. This check has to happen before the similarity test because identical words also satisfy the weaker condition that corresponding letters are equal or neighboring.
4. Otherwise, scan the two words at the same positions. Convert each character to its zero-based alphabet index with `ord(ch) - ord('a')`. From this index, compute its keyboard row and column.
5. For every corresponding pair, check whether the absolute row difference is at most one and the absolute column difference is at most one. If either difference exceeds one, the pair contains a non-neighboring position, so output `3` immediately.
6. If the entire scan finishes without finding a bad position, output `2`. The words are already known to be different, and every corresponding pair is equal or neighboring, which is exactly the definition of similarity.

### Why it works

The invariant during the character scan is that every position processed so far contains either equal letters or two neighboring keyboard keys. If a position violates this property, the words cannot be similar, so returning `3` is correct. If every position satisfies the property, the words have equal length and pass the complete similarity condition. Since the words were checked for equality first, they are not identical, so the correct result is `2`. The three possible outputs are consequently distinguished without overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline

def position(ch):
    p = ord(ch) - ord('a')
    return p // 9, p % 9

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        a, b = input().split()

        if len(a) != len(b):
            ans.append("3")
            continue

        if a == b:
            ans.append("1")
            continue

        similar = True

        for x, y in zip(a, b):
            rx, cx = position(x)
            ry, cy = position(y)

            if abs(rx - ry) > 1 or abs(cx - cy) > 1:
                similar = False
                break

        ans.append("2" if similar else "3")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `position` function converts the alphabet index into the keyboard coordinates. The division by `9` is correct because the first two rows each contain nine letters: `a` through `i`, then `j` through `r`. The remaining letters `s` through `z` form the final row.

The length check comes first because `zip(a, b)` would otherwise stop at the shorter word and silently ignore extra characters. That would be incorrect for inputs such as `ab` and `abc`.

The equality check comes before the neighbor scan because equality is the stronger classification. Without it, a pair such as `cool` and `cool` would satisfy the neighbor condition and could incorrectly receive output `2`.

The neighbor test uses `abs(row_difference) <= 1` and `abs(column_difference) <= 1`. This includes horizontal, vertical, and diagonal neighbors. It also includes the same key, although the equality case has already been handled separately.

There is no integer overflow concern because all coordinates are between zero and eight, and Python integers are unbounded anyway. The early `break` is also useful because one invalid position is enough to prove that the words are different rather than similar.

## Worked Examples

Since the current Codeforces page does not expose formal sample blocks, the following traces use examples from the original contest statement and additional small cases. The original statement explicitly gives `aaaaa` versus `abkja`, `moon` versus `done`, and `knq` versus `bxz` as similar examples.

### Example 1

Input:

```
1
moon done
```

The two words have equal length and are not identical. Their corresponding letters are checked as follows.

| Position | First | Second | First coordinates | Second coordinates | Neighbor? |
| --- | --- | --- | --- | --- | --- |
| 0 | m | d | (1,3) | (0,3) | yes |
| 1 | o | o | (1,5) | (1,5) | yes |
| 2 | o | n | (1,5) | (1,4) | yes |
| 3 | n | e | (1,4) | (0,4) | yes |

Every position satisfies the neighbor condition, so the final output is:

```
2
```

This trace demonstrates why vertical and horizontal adjacency are both accepted. It also exercises the fact that the same letter counts as acceptable during the similarity check.

### Example 2

Input:

```
1
ab abc
```

The first word has length 2 and the second has length 3.

| Step | First word | Second word | Condition | Output |
| --- | --- | --- | --- | --- |
| 1 | `ab` | `abc` | lengths differ | `3` |

The algorithm stops before comparing characters because no words of different lengths can be identical or similar.

This example demonstrates why the length check must happen before using `zip`, otherwise the unmatched `c` would disappear from the comparison.

### Example 3

Input:

```
1
knq bxz
```

The coordinate checks are:

| Position | First | Second | First coordinates | Second coordinates | Neighbor? |
| --- | --- | --- | --- | --- | --- |
| 0 | k | b | (1,1) | (0,1) | yes |
| 1 | n | x | (1,4) | (2,5) | yes |
| 2 | q | z | (1,7) | (2,7) | yes |

Every pair is neighboring, so the result is:

```
2
```

This trace specifically confirms that diagonal movement is allowed. The pair `n` and `x` differs by one row and one column, so it is a valid neighboring pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nL) | Each of the (n) test cases scans at most (L \le 20) character pairs |
| Space | O(n) | The implementation stores all output strings before printing |

The input words are extremely short, with a maximum length of 20 characters. The algorithm performs only a constant amount of arithmetic per character, so even a large number of test cases is handled comfortably within the 1 second and 256 MB limits specified for the contest problem.

The output list uses O(n) memory. It could be printed immediately to reduce that to O(1) auxiliary space, but buffering the tiny output strings is simpler and still well within the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def position(ch):
    p = ord(ch) - ord('a')
    return p // 9, p % 9

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        a, b = input().split()

        if len(a) != len(b):
            ans.append("3")
            continue

        if a == b:
            ans.append("1")
            continue

        similar = True

        for x, y in zip(a, b):
            rx, cx = position(x)
            ry, cy = position(y)

            if abs(rx - ry) > 1 or abs(cx - cy) > 1:
                similar = False
                break

        ans.append("2" if similar else "3")

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Examples from the original statement
assert run("1\ncool cool\n") == "1", "identical words"
assert run("1\nmoon done\n") == "2", "similar words"

# Minimum-size input
assert run("3\na a\na b\na c\n") == "1\n2\n3", "single-character cases"

# Maximum word length, identical
assert run("1\n" + "a" * 20 + " " + "a" * 20 + "\n") == "1", \
    "maximum length identical words"

# Diagonal and vertical neighbors
assert run("2\nknq bxz\naaa bkk\n") == "2\n2", \
    "diagonal and multi-position adjacency"

# Different lengths and a non-neighboring pair
assert run("3\nab abc\nab cb\naz za\n") == "3\n3\n3", \
    "length and boundary failures"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a a`, `a b`, `a c` | `1`, `2`, `3` | Minimum-size words and immediate adjacency boundaries |
| Two identical 20-character words | `1` | Maximum allowed word length and equality handling |
| `knq bxz`, `aaa bkk` | `2`, `2` | Vertical and diagonal keyboard neighbors |
| `ab abc`, `ab cb`, `az za` | `3`, `3`, `3` | Different lengths, non-neighboring letters, and reversed positions |

## Edge Cases

The first edge case is different word lengths. Consider:

```
1
ab abc
```

The algorithm compares the lengths first and sees `2 != 3`. It immediately produces `3`. No character scan is performed, so the extra `c` cannot be accidentally ignored.

The second edge case is identical words:

```
1
cool cool
```

The lengths match, and the equality test succeeds, so the algorithm produces `1` immediately. It never reaches the similarity test. This ordering matters because every identical pair also satisfies the weaker requirement that corresponding characters are equal or neighboring.

The third edge case is a diagonal neighbor:

```
1
knq bxz
```

The first pair is `k` at `(1,1)` and `b` at `(0,1)`, which are vertically adjacent. The second pair is `n` at `(1,4)` and `x` at `(2,5)`, which are diagonally adjacent. The third pair is `q` at `(1,7)` and `z` at `(2,7)`, which are vertically adjacent. Every pair passes, so the answer is `2`.

The final edge case is a pair that looks close alphabetically but is not adjacent geometrically:

```
1
ab cb
```

The first position compares `a` at `(0,0)` with `c` at `(0,2)`. Their row difference is zero, but their column difference is two, so they are not neighbors. The algorithm breaks immediately and outputs `3`. This is why comparing alphabet indices, such as checking whether their numeric difference is at most one, would be an incorrect interpretation of the keyboard layout.
