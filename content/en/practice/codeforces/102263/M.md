---
title: "CF 102263M - Two Operations"
description: "We have a string of lowercase letters. We may freely swap any two positions, so the order of the characters is never a real restriction. The second operation takes two equal adjacent letters and replaces them with the next letter."
date: "2026-08-17T20:11:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102263
codeforces_index: "M"
codeforces_contest_name: "ArabellaCPC 2019"
rating: 0
weight: 102263
solve_time_s: 72
verified: true
draft: false
---

[CF 102263M - Two Operations](https://codeforces.com/problemset/problem/102263/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string of lowercase letters. We may freely swap any two positions, so the order of the characters is never a real restriction. The second operation takes two equal adjacent letters and replaces them with the next letter. For example, two `c` characters can become one `d`, while two `z` characters cannot be merged because there is no character after `z`.

The goal is to perform any sequence of operations and obtain the lexicographically largest possible string. Since arbitrary swaps are available, once we know how many copies of every letter remain, we can always arrange them in descending order. The real problem is consequently to determine the best final multiset of letters.

The length can be as large as `10^5`. That is large enough to rule out algorithms that repeatedly explore many possible operation sequences or scan the whole string after every operation. A linear or near-linear solution is appropriate. The alphabet has only 26 characters, which gives us a particularly useful constant-sized dimension for carrying information from one letter to the next.

There are several edge cases where a careless implementation can go wrong. For the input `aa`, the correct output is `b`. Simply sorting the original string would produce `aa`, missing the operation that strictly improves the first character. For `zz`, the correct output is `zz`, because `z` has no successor. An implementation that blindly increments every pair would incorrectly produce a character outside the alphabet. For `yyy`, the correct output is `zy`: one pair of `y` becomes `z`, while the remaining `y` cannot participate in another operation. Finally, for `aaaa`, the answer is `c`, not `bb`. After the first two merges we obtain `bb`, and those two `b` characters can merge again into `c`. A solution that processes each letter only once without carrying newly created pairs upward would miss this cascade.

## Approaches

A direct simulation can repeatedly search for two equal letters, swap characters when necessary to bring such a pair together, replace the pair by its successor, and continue until no useful pair remains. This is correct if every available pair is eventually processed, because every operation reduces the string length by one and the swaps allow any two equal characters to become adjacent.

The problem is the cost of performing that simulation efficiently. There can be as many as `n - 1` operations. This maximum is achieved, for example, when the string consists of a power-of-two number of `a` characters. With `n = 100000`, a naive implementation that scans the current string to find a merge after every operation can perform about

`100000 + 99999 + ... + 1 = 5,000,050,000`

character inspections in the worst case. Exploring different possible operation orders is even worse, since it can create a large search tree.

The key observation is that swaps completely remove the importance of positions. We only need the count of each letter. Suppose there are `cnt[c]` copies of some letter `c`. Every pair of them can be replaced by one `c + 1`. If there are `cnt[c] // 2` pairs, they can all be converted, leaving `cnt[c] % 2` copies of `c` and adding `cnt[c] // 2` copies to the next letter.

This operation is always beneficial for lexicographic maximization. Two copies of `c` are replaced by one copy of the strictly larger character `c + 1`. Since all remaining characters can be sorted in descending order, moving one character upward in the alphabet gives the largest possible leading contribution from those characters. There is also no reason to preserve a pair at a lower letter, because it can always be converted and any newly produced pair at the next letter can itself be converted again.

Thus the entire process becomes a small carry operation. We process the alphabet from `a` through `y`. The parity of each count stays at its current character, while half of the count is carried to the next character. The `z` count is never changed, because `zz` cannot be converted. Finally, we output every remaining character from `z` down to `a`.

The brute-force process works because each merge represents a valid operation, but it fails when the number of merges becomes linear and each merge requires another scan. The observation that only character counts matter lets us replace all of those operations with 25 constant-time count transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count how many times each of the 26 lowercase letters occurs in the input string. Positions do not need to be preserved because arbitrary swaps let us rearrange the string whenever necessary.
2. Process letters from `a` to `y`. For the current letter with count `cnt[i]`, keep `cnt[i] % 2` copies at this letter and add `cnt[i] // 2` copies to `cnt[i + 1]`. This exactly represents performing all possible merges of the current character.
3. Continue processing the next letter using its updated count. This step is what handles cascades such as `aaaa -> bb -> c`. The copies created at one level are treated exactly like copies that were present in the original input.
4. Leave the count of `z` unchanged. There is no character after `z`, so a pair of `z` characters cannot be converted.
5. Construct the answer by iterating from `z` down to `a` and appending each character according to its final count. This ordering is lexicographically maximal because, for a fixed multiset, placing larger characters earlier always produces the largest string.

Why it works: after processing letter `i`, its final count is exactly the parity of the number of copies that reached it, while every possible pair has been converted into the next character. The discarded pairs are not lost, because each one contributes exactly one copy to `i + 1`. Hence the invariant is that the processed prefix of the alphabet has been reduced as far upward as possible, with every remaining pair represented in the next position. Since no lower character can be improved further once its pairs have been carried upward, and since descending order is optimal for the resulting multiset, the final string is lexicographically maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(s: str) -> str:
    cnt = [0] * 26

    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    for i in range(25):
        cnt[i + 1] += cnt[i] // 2
        cnt[i] %= 2

    ans = []

    for i in range(25, -1, -1):
        if cnt[i]:
            ans.append(chr(ord('a') + i) * cnt[i])

    return ''.join(ans)

def main():
    s = input().strip()
    print(solve(s))

if __name__ == "__main__":
    main()
```

The `cnt` array stores the current multiplicity of every letter. Counting the input takes one pass over the string, and each character maps directly to an index using its ASCII value.

The loop from index `0` through `24` performs the carry operation from each letter to its successor. The order is essential. When processing `b`, its count may already contain pairs produced from `a`, so processing the alphabet from low to high automatically handles arbitrarily long chains of operations.

The expression `cnt[i] // 2` is the number of pairs that can be merged, while `cnt[i] % 2` is the only number that must remain at the current character. Python integers do not have an overflow issue here, and every count is at most the original string length.

The construction loop runs backwards so that larger letters appear first. Repeating each character according to its final count preserves the exact final multiset produced by the carry process.

There is no need to explicitly simulate swaps. Their only purpose in the original operations is to make equal characters adjacent, and counting the characters already gives us the same freedom without constructing intermediate strings.

## Worked Examples

For the first sample, `abbx`, the initial counts are one `a`, two `b` characters, and one `x`.

| Letter processed | Count before | Pairs carried | Count kept | Next count |
| --- | --- | --- | --- | --- |
| `a` | 1 | 0 | 1 | `b` remains 2 |
| `b` | 2 | 1 | 0 | `c` becomes 1 |
| `c` | 1 | 0 | 1 | `d` remains 0 |
| `d` through `w` | 0 | 0 | 0 | unchanged |
| `x` | 1 | 0 | 1 | unchanged |
| `y` | 0 | 0 | 0 | unchanged |
| `z` | 0 | cannot merge | 0 | unchanged |

The final multiset is `{x, c, a}`, so descending order gives `xca`. This is exactly the sample result. The trace demonstrates that the pair of `b` characters becomes `c`, and that the newly created `c` is considered as part of the same carry process.

For the second sample, `zyayz`, the counts are one `a`, one `y`, one `z`, one `a`, and one `y`.

| Letter processed | Count before | Pairs carried | Count kept | Effect |
| --- | --- | --- | --- | --- |
| `a` | 2 | 1 | 0 | one `b` created |
| `b` | 1 | 0 | 1 | remains `b` |
| `c` through `x` | 0 | 0 | 0 | unchanged |
| `y` | 2 | 1 | 0 | one `z` created |
| `z` | 2 | cannot merge | 2 | remains `zz` |

The final counts are two `z` characters and one `b`, giving `zzb`. The sample output is `zzza`, so this direct trace exposes an important correction: the input in the supplied statement is actually `zyayz`, whose counts are `z = 2`, `y = 2`, `a = 1`, not `a = 2`. Thus the actual trace is:

| Letter processed | Count before | Pairs carried | Count kept | Effect |
| --- | --- | --- | --- | --- |
| `a` | 1 | 0 | 1 | `a` remains |
| `b` through `x` | 0 | 0 | 0 | unchanged |
| `y` | 2 | 1 | 0 | one `z` created |
| `z` | 3 | cannot merge | 3 | remains `zzz` |

The final string is `zzza`, matching the sample. This demonstrates the special handling of `z`: the `y` pair can become another `z`, but the resulting three `z` characters cannot be reduced further.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting scans the string once, and processing the 26 letters takes constant time. |
| Space | O(n) | The output itself can contain O(n) characters; the auxiliary count array uses O(1) space. |

With `n <= 10^5`, the algorithm performs one pass over the input and a fixed 26-letter pass afterward. It avoids constructing every intermediate string and avoids repeated scans, so its running time is easily suitable for the stated input bound.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve(s: str) -> str:
    cnt = [0] * 26

    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    for i in range(25):
        cnt[i + 1] += cnt[i] // 2
        cnt[i] %= 2

    ans = []
    for i in range(25, -1, -1):
        ans.append(chr(ord('a') + i) * cnt[i])

    return ''.join(ans)

def run(inp: str) -> str:
    return solve(inp.strip())

# Provided samples
assert run("abbx") == "xca", "sample 1"
assert run("zyayz") == "zzza", "sample 2"

# Minimum-size input
assert run("a") == "a", "single character"

# z is a terminal character and can never be merged
assert run("zz") == "zz", "z boundary"

# Complete cascade: aaaa -> bb -> c
assert run("aaaa") == "c", "multi-level carry"

# y reaches z, but z cannot be carried further
assert run("yy") == "z", "y to z boundary"

# Odd count must leave one character behind
assert run("yyy") == "zy", "odd y count"

# A higher existing character must remain ahead of the carried result
assert run("aaz") == "zb", "existing z and generated b"

# Maximum-size input
assert run("z" * 100000) == "z" * 100000, "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `a` | Minimum input size and no possible operation |
| `zz` | `zz` | Upper alphabet boundary |
| `aaaa` | `c` | Multiple consecutive carry levels |
| `yy` | `z` | Conversion into `z` without attempting a nonexistent next character |
| `yyy` | `zy` | Correct handling of an odd count |
| `aaz` | `zb` | Interaction between generated characters and an existing high character |
| `z` repeated 100000 times | Same string | Maximum input size and linear performance |

## Edge Cases

For the input `aa`, the algorithm starts with `cnt[a] = 2`. Processing `a` carries one pair to `b` and leaves zero `a` characters, so the final count of `b` is one. The output is `b`. A solution that merely sorts the original characters would incorrectly return `aa`, because it would never consider that merging two lower characters produces a lexicographically larger character.

For the input `zz`, the algorithm never processes `z` as a source of a carry. Its count stays equal to two, and the descending construction produces `zz`. The boundary is handled by stopping the carry loop at `y`. Attempting to access the successor of `z` would either create an invalid character or cause an indexing error.

For `yyy`, the count of `y` is three. One pair is carried to `z`, leaving one `y`. The final counts are `z = 1` and `y = 1`, so the result is `zy`. The algorithm keeps the odd copy instead of discarding it, which is the key boundary condition for every character.

For `aaaa`, the first carry changes four `a` characters into two `b` characters. When the algorithm reaches `b`, those two newly generated characters form another pair and are carried to `c`. The result is a single `c`. This demonstrates why the alphabet must be processed from left to right: processing each original count independently would miss operations enabled by characters created earlier.

For `aaz`, the two `a` characters become one `b`, while the original `z` remains untouched. The final multiset is `{z, b}`, and descending order produces `zb`. This confirms that the operation does not need to be performed on the highest existing character first. All lower-level carries can be computed independently and then merged into the final ordering.

For an input containing only `z`, such as `z`, there are no possible operations at all. The count array remains unchanged and the output is exactly `z`, which also confirms that the algorithm handles the smallest possible input without relying on any pair existing.
