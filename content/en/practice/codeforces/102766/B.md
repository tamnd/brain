---
title: "CF 102766B - Singhal and Equality"
description: "The string contains lowercase letters, and the goal is to modify it until every letter that appears has exactly the same frequency. One operation changes one existing character into any other lowercase character. The task is to find the smallest number of such changes needed."
date: "2026-07-30T04:17:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102766
codeforces_index: "B"
codeforces_contest_name: "Codedigger Training Contest -String"
rating: 0
weight: 102766
solve_time_s: 78
verified: true
draft: false
---

[CF 102766B - Singhal and Equality](https://codeforces.com/problemset/problem/102766/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The string contains lowercase letters, and the goal is to modify it until every letter that appears has exactly the same frequency. One operation changes one existing character into any other lowercase character. The task is to find the smallest number of such changes needed.

For example, if a string has counts `a = 5`, `b = 2`, and `c = 1`, we are allowed to either remove some letters by converting them into other existing letters, or create new letters. The final string can contain any number of distinct characters, but every character that remains must have the same count.

The input contains several independent strings. The number of test cases can be as large as `10^5`, and the sum of all string lengths is also at most `10^5`. This means the solution must be close to linear in the total input size. A solution that tries many modifications or scans all possible transformed strings would be impossible, while an approach doing a small amount of work per character will fit easily.

A few cases require care. If all characters already have equal frequency, no operation is needed. For input:

```
1
aabb
```

the answer is `0`, because both letters already appear twice. A method that always tries to merge everything into one character would incorrectly return `2`.

A string with one character is another boundary case:

```
1
aaaa
```

The answer is `0`. The string already has exactly one distinct character, and the condition is satisfied because all distinct characters, meaning only `a`, have the same frequency.

A less obvious case is when the best answer introduces a different number of distinct characters than the original string. For:

```
1
aba
```

the answer is `1`. We can change `b` into `a` and get `aaa`, or change one `a` into `c` and get `abc`. A solution that only tries to balance the letters currently present would miss the possibility of adding or removing distinct characters.

## Approaches

A direct approach would be to guess the final number of distinct characters, the letters that will remain, and their target frequency. For each guess, we could count how many characters already match the desired final arrangement and change the rest. This is correct because every possible final state is considered, but the number of possible states is far too large.

The key observation comes from the fact that there are only 26 possible lowercase letters. The final number of distinct characters must be some divisor of the string length, because if there are `k` characters and each appears `x` times, then `k * x = |S|`. Since `k` cannot exceed 26, we only need to check a very small number of possibilities.

Suppose we choose `k` final characters. Their required frequency is `|S| / k`. A chosen character with current frequency `c` can contribute at most `min(c, |S| / k)` characters that remain unchanged. If we keep a character that has more than the target frequency, the extra copies must be changed. If it has fewer copies, we must create additional copies using changes from other characters.

For a fixed `k`, the best choice is to select the `k` letters with the largest possible contributions. After calculating the maximum number of positions that can stay unchanged, the remaining positions are exactly the operations we need.

The brute-force works because it examines the possible final configurations, but it fails because it treats the 26 letters as if they create a huge search space. The observation that only the final number of distinct letters matters reduces the problem to checking at most 26 cases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of possible final states | O(26) | Too slow |
| Optimal | O(26 × 26) per string | O(26) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of every lowercase letter in the string. Only 26 counters are needed because the alphabet size is fixed.
2. Try every possible number of final distinct characters `k` from `1` to `26`. Ignore values of `k` that do not divide the string length, because equal frequencies cannot sum to the total length otherwise.
3. For a valid `k`, compute the target frequency `need = length / k`. For every letter, calculate how many of its current occurrences could remain unchanged if this letter is one of the final `k` letters. This value is `min(current_frequency, need)`.
4. Sort these 26 contribution values and take the largest `k` of them. These represent the best `k` letters to keep in the final string.
5. The number of unchanged positions is the sum of these chosen contributions. The required operations for this choice are `length - unchanged_positions`. Keep the minimum value among all valid `k`.

Why it works: for any chosen final number of characters, every final character must have exactly `need` occurrences. A character cannot preserve more than `need` of its old occurrences, and preserving fewer would never be beneficial because another character could use those preserved positions. Selecting the largest `k` contributions gives the maximum number of positions that can survive unchanged for that target. Since every possible valid final number of characters is checked, the minimum found answer is the true optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        s = input().strip()
        n = len(s)

        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1

        best = n

        for k in range(1, 27):
            if n % k != 0:
                continue

            need = n // k
            keep = []

            for c in cnt:
                keep.append(min(c, need))

            keep.sort(reverse=True)
            unchanged = sum(keep[:k])

            best = min(best, n - unchanged)

        ans.append(str(best))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The frequency array stores the complete state of the input because only letter counts affect the answer. The loop over `k` checks every possible size of the final alphabet. Values that cannot divide the string length are skipped because they cannot form equal groups.

For each valid `k`, the code builds the amount each letter can contribute without modification. Sorting puts the most useful letters first, so taking the first `k` values gives the best set of characters to keep. The answer is the total length minus these preserved positions.

There are no indexing issues because every character is converted into a value from `0` to `25`. Python integers also remove any concern about overflow, although the actual values are small.

## Worked Examples

For the string `aba`:

| k | target frequency | contributions | unchanged | operations |
| --- | --- | --- | --- | --- |
| 1 | 3 | 2, 1, 0, ... | 2 | 1 |
| 3 | 1 | 1, 1, 0, ... | 2 | 1 |

The best answer is `1`. The trace shows that the optimal result does not need to keep the same number of distinct characters as the original string.

For the string `abbbc`:

| k | target frequency | contributions | unchanged | operations |
| --- | --- | --- | --- | --- |
| 1 | 5 | 3, 1, 1, 0, ... | 3 | 2 |
| 5 | 1 | 1, 1, 1, 0, ... | 3 | 2 |

The answer is `2`. Keeping one character requires changing the other two letters, while keeping three different characters requires reducing the frequency of `b` and creating missing copies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 × 26) per test case | There are at most 26 choices for `k`, and sorting 26 values is constant work. |
| Space | O(26) | Only the alphabet frequency array and temporary contribution values are stored. |

The total input size is limited to `10^5` characters, so the constant amount of work done for each string easily fits within the time limit.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        s = input().strip()
        n = len(s)

        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        best = n

        for k in range(1, 27):
            if n % k == 0:
                need = n // k
                values = [min(x, need) for x in cnt]
                values.sort(reverse=True)
                best = min(best, n - sum(values[:k]))

        ans.append(str(best))

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out.getvalue()

assert solve("""6
aba
abba
abbc
abbbc
codedigger
codealittle
""") == """1
0
1
2
2
3
"""

assert solve("""1
a
""") == """0
"""

assert solve("""1
aaaa
""") == """0
"""

assert solve("""1
abcde
""") == """0
"""

assert solve("""1
aaaaab
""") == """1
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `0` | Minimum string size and single distinct character |
| `aaaa` | `0` | Already equal frequencies |
| `abcde` | `0` | Every character already has frequency one |
| `aaaaab` | `1` | Removing an overrepresented character count |

## Edge Cases

For `aabb`, the algorithm checks `k = 1` and `k = 2`. When `k = 2`, the target frequency is `2`, both letters contribute `2`, and all four positions remain unchanged. The answer is `0`, avoiding the mistake of forcing the string into one character.

For `aaaa`, only one letter exists, but `k = 1` is valid because the length is divisible by one. The target frequency is `4`, and the letter contributes all four positions. The algorithm returns `0`.

For `aba`, the algorithm considers both `k = 1` and `k = 3`. With `k = 1`, the best contribution is two unchanged `a` characters. With `k = 3`, the best contributions are one `a` and one `b`, leaving one missing character to create. Both choices require one operation, so the final answer is `1`.

For `abbbc`, the valid choices are `k = 1` and `k = 5`. The first choice keeps three `b` characters and changes the remaining two. The second choice keeps one copy of each available character and changes two positions to create the missing letters. Both lead to two operations, which confirms that the algorithm handles cases where removing characters and adding characters are equally good.
