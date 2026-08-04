---
title: "CF 102606I - Idiotic Suffix Array"
description: "A direct approach would try to build a candidate string, generate all of its suffixes, sort them, and check whether the original suffix has the required rank. This is correct because it exactly follows the definition of the suffix array."
date: "2026-08-04T17:07:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102606
codeforces_index: "I"
codeforces_contest_name: "2020 ECNU Campus Online Invitational Contest"
rating: 0
weight: 102606
solve_time_s: 73
verified: true
draft: false
---

[CF 102606I - Idiotic Suffix Array](https://codeforces.com/problemset/problem/102606/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Approaches

A direct approach would try to build a candidate string, generate all of its suffixes, sort them, and check whether the original suffix has the required rank. This is correct because it exactly follows the definition of the suffix array. However, it gives no useful way to search through the enormous space of possible strings. There are `n` suffixes, and generating them can already require `O(n^2)` memory because their total length is quadratic. For `n = 100000`, the worst case would involve about five billion character positions just to store all suffixes.

The key observation is that we do not need to build a suffix array. We only need to force the comparisons between suffixes.

Suppose the first character of the answer is `'b'`. Any suffix starting with `'a'` will automatically be smaller, while any suffix starting with a character greater than `'b'` will automatically be larger. This gives a simple way to decide the rank.

We can put exactly `k - 1` suffixes after the first position that begin with `'a'`. Those suffixes will all come before the whole string. Then we make every remaining suffix begin with `'c'`, so they all come after the whole string.

The string becomes:

```
b + (k-1 times 'a') + (n-k times 'c')
```

The suffixes starting inside the `a` block are smaller because their first character is `'a'`. The suffixes starting inside the `c` block are larger because their first character is `'c'`. The whole string is the only suffix beginning with `'b'`, so it sits exactly after the `k-1` smaller suffixes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n²) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `k`. The first character of the answer will be `'b'`, because we want to separate smaller suffixes from larger suffixes using lexicographical order.
2. Append `k - 1` copies of `'a'`. Each suffix beginning inside this block starts with `'a'`, so it is smaller than the full string, whose first character is `'b'`. These are exactly the suffixes that should appear before the answer.
3. Append `n - k` copies of `'c'`. Every suffix beginning inside this block starts with `'c'`, so it is larger than the full string. These suffixes will appear after the answer.
4. Output the constructed string.

Why it works: the suffixes are divided into three groups. The first group consists of the `k - 1` suffixes starting in the `a` block, and every one of them is smaller than the full string. The second group is the suffix starting at index `0`, beginning with `b`. The third group consists of suffixes starting in the `c` block, and all of them are larger. Since no other suffix begins with `b`, the full string has exactly `k - 1` suffixes before it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    ans = ['b']
    ans.append('a' * (k - 1))
    ans.append('c' * (n - k))
    print(''.join(ans))

if __name__ == "__main__":
    solve()
```

The first append creates the suffix that we want to rank. The next append adds exactly the number of smaller suffixes required by the input. The final append fills the remaining positions with characters that are guaranteed to make their suffixes larger.

The calculation `k - 1` is the important boundary detail. The full string itself is not counted among the suffixes before it, so only the suffixes after position zero can contribute to the smaller count.

When `k = 1`, the middle block has length zero and the answer is a `b` followed by `c` characters. When `k = n`, the final block disappears and all later suffixes begin with `a`, making the full string the largest suffix.

## Worked Examples

For sample 1, `n = 4`, `k = 2`.

| Step | Constructed part | Current string |
| --- | --- | --- |
| Start | first character | `b` |
| Add `k-1 = 1` copies of `a` | add smaller suffix source | `ba` |
| Add `n-k = 2` copies of `c` | add larger suffix source | `bacc` |

The suffixes are:

| Suffix position | Suffix | Comparison |
| --- | --- | --- |
| 0 | `bacc` | target suffix |
| 1 | `acc` | smaller |
| 2 | `cc` | larger |
| 3 | `c` | larger |

Only one suffix is smaller, so the full string has rank `2`.

For sample 2, `n = 8`, `k = 3`.

| Step | Constructed part | Current string |
| --- | --- | --- |
| Start | first character | `b` |
| Add `k-1 = 2` copies of `a` | add smaller suffix source | `baa` |
| Add `n-k = 5` copies of `c` | add larger suffix source | `baaccccc` |

The suffixes beginning at positions `1` and `2` are `aaccccc` and `accccc`, both smaller than the full string. All later suffixes begin with `c`, so they are larger. The full string has exactly two suffixes before it, giving rank `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The algorithm creates exactly `n` characters. |
| Space | O(n) | The output string requires linear storage. |

The largest possible input has `100000` characters, so a linear construction easily fits within the limits. No suffixes are stored or compared.

## Test Cases

```python
import sys
import io

def make_solution(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    n, k = map(int, sys.stdin.readline().split())
    ans = ['b']
    ans.append('a' * (k - 1))
    ans.append('c' * (n - k))
    print(''.join(ans))

    result = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

def rank_of_string(s):
    suffixes = sorted(s[i:] for i in range(len(s)))
    return suffixes.index(s) + 1

assert rank_of_string(make_solution("4 2")) == 2, "sample 1"
assert rank_of_string(make_solution("8 3")) == 3, "sample 2"

assert rank_of_string(make_solution("1 1")) == 1, "minimum size"
assert rank_of_string(make_solution("5 5")) == 5, "largest rank"
assert rank_of_string(make_solution("10 1")) == 1, "smallest rank"
assert rank_of_string(make_solution("100000 50000")) == 50000, "large input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | any one-character string | Handles the single suffix case |
| `5 5` | a string with four smaller suffixes | Checks the largest possible rank |
| `10 1` | a string with no smaller suffixes | Checks the smallest possible rank |
| `100000 50000` | rank `50000` | Confirms the linear construction scales |

## Edge Cases

For `n = 5, k = 5`, the algorithm creates `baaaa`. The suffixes after the first position are `aaaa`, `aaa`, `aa`, and `a`. They are all smaller because they begin with `a`. There are four smaller suffixes, so the full string is fifth.

For `n = 4, k = 1`, the algorithm creates `bccc`. The suffixes are `bccc`, `ccc`, `cc`, and `c`. Every suffix after the first starts with `c`, which is greater than `b`, so the full string is first.

For `n = 1, k = 1`, the algorithm creates `b`. There are no other suffixes, so the only suffix has rank one. The construction naturally handles this because both repeated blocks have length zero.
