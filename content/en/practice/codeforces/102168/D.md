---
title: "CF 102168D - \u0411\u0435\u0437 \u043e\u0434\u043d\u043e\u0433\u043e \u0441\u0438\u043c\u0432\u043e\u043b\u0430"
description: "We have a string s of length n. For every position i, Vasya writes the string obtained by removing exactly the character at position i. All resulting strings have length n - 1, and the task is to count how many of these n strings are actually different."
date: "2026-08-19T07:19:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102168
codeforces_index: "D"
codeforces_contest_name: "\u041b\u0438\u0447\u043d\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u043e\u0433\u043e \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442\u0430 \u0441\u0440\u0435\u0434\u0438 \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432 2018-2019"
rating: 0
weight: 102168
solve_time_s: 85
verified: true
draft: false
---

[CF 102168D - \u0411\u0435\u0437 \u043e\u0434\u043d\u043e\u0433\u043e \u0441\u0438\u043c\u0432\u043e\u043b\u0430](https://codeforces.com/problemset/problem/102168/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string `s` of length `n`. For every position `i`, Vasya writes the string obtained by removing exactly the character at position `i`. All resulting strings have length `n - 1`, and the task is to count how many of these `n` strings are actually different.

The input contains one lowercase Latin string. Its length is between 2 and 200,000, so an algorithm that performs work proportional to `n^2` is far too expensive. With 200,000 positions, even a simple quadratic loop would require about 40 billion iterations in the worst case, which cannot fit into a 2-second limit. We need a linear or near-linear solution.

The subtle part is that two different removed positions can produce exactly the same string. For example, for `aaa`, deleting any of the three characters gives `aa`, so the answer is 1 rather than 3. A careless solution that simply counts deletion positions would fail on this case.

Another boundary case is `ab`. Removing the first character gives `b`, while removing the second gives `a`, so the answer is 2. An implementation that accidentally treats every pair of adjacent positions as equivalent would incorrectly return 1.

A longer example is `aabb`. Removing either character from the first `aa` gives `abb`, while removing either character from the final `bb` gives `aab`. The answer is 2. The equality of the characters matters across the entire interval between two deletion positions, not just at the two endpoints.

## Approaches

The direct approach is to construct the resulting string for every possible deleted position and put all resulting strings into a set. This is correct because every generated string represents exactly one of Vasya's days, and the set removes duplicates. However, constructing one result costs `O(n)`, and there are `n` possible deletions, giving `O(n^2)` time. For `n = 200000`, that is roughly 40 billion character operations before accounting for string and set overhead.

The useful observation is that we do not actually need to construct any of those strings. Consider two deletion positions `i < j`. Before position `i`, both resulting strings contain exactly the same prefix. After position `j`, both contain exactly the same suffix. The only potentially different part is the interval from `i` through `j`.

Deleting `i` leaves

```
s[i+1] s[i+2] ... s[j]
```

from that interval, while deleting `j` leaves

```
s[i] s[i+1] ... s[j-1]
```

For these two strings to be equal, every character in the interval `s[i..j]` must be the same. If even one character differs, the two resulting strings differ at the corresponding position.

This gives a very simple equivalence rule: deleting positions `i` and `j` produces the same string exactly when every character between them is equal. In other words, all positions belonging to one maximal run of equal characters produce the same result when one character from that run is deleted.

For `aabb`, the runs are `aa` and `bb`, so there are two distinct resulting strings. For `abca`, every character forms its own run, so there are four distinct results. For `zzz`, there is only one run, so every deletion produces the same string.

Thus the answer is simply the number of maximal consecutive runs of equal characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) in the worst case | Too slow |
| Count equal-character runs | O(n) | O(1) auxiliary space | Accepted |

## Algorithm Walkthrough

1. Read the string `s` and start the answer at 1. Since `n >= 2`, at least one deletion result exists, and the first character starts the first run.
2. Scan the string from the second character to the end. Whenever `s[i]` differs from `s[i - 1]`, a new maximal run begins, so increment the answer.
3. Ignore positions where `s[i] == s[i - 1]`. They belong to the same run, and deleting any one character from that run gives the same resulting string.
4. Print the number of runs.

### Why it works

Partition the string into maximal runs of equal characters. Suppose two deletion positions belong to the same run. Every character between them is identical, so shifting the deletion from one position to the other changes nothing in the resulting string. Hence all positions inside one run correspond to one distinct result.

Now suppose two positions belong to different runs. Between them there is a boundary where two consecutive characters differ. The two deletion results differ at that boundary because one result shifts the characters on one side of the boundary while the other does not. Hence positions from different runs cannot produce the same string.

So there is exactly one distinct resulting string for every maximal equal-character run, and counting those runs gives the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_string(s: str) -> int:
    answer = 1

    for i in range(1, len(s)):
        if s[i] != s[i - 1]:
            answer += 1

    return answer

def main() -> None:
    s = input().strip()
    print(solve_string(s))

if __name__ == "__main__":
    main()
```

The `solve_string` function implements the run-counting algorithm directly. The initial value `answer = 1` is valid because the input length is at least 2, so the string always has at least one run.

The loop starts at index 1 because index 0 has no previous character to compare with. Every change from `s[i - 1]` to `s[i]` starts a new run and contributes exactly one new distinct deletion result.

There is no need to construct the strings obtained after deletion, and no set is required. Python integers are also more than sufficient for this answer because it is at most `n`, which is only 200,000.

The `strip()` call removes the newline supplied by standard input. Since the string contains only lowercase Latin letters, there are no meaningful spaces that could be accidentally removed.

## Worked Examples

For the first sample, `abca`, every neighboring pair is different.

| Index `i` | Character | Previous character | New run? | Answer |
| --- | --- | --- | --- | --- |
| 0 | `a` | none | yes, initial run | 1 |
| 1 | `b` | `a` | yes | 2 |
| 2 | `c` | `b` | yes | 3 |
| 3 | `a` | `c` | yes | 4 |

The four runs are `a`, `b`, `c`, and `a`. Deleting each position gives a different result, so the answer is 4.

For the second sample, `zzz`, all characters belong to one run.

| Index `i` | Character | Previous character | New run? | Answer |
| --- | --- | --- | --- | --- |
| 0 | `z` | none | yes, initial run | 1 |
| 1 | `z` | `z` | no | 1 |
| 2 | `z` | `z` | no | 1 |

Deleting any one `z` leaves `zz`, so there is only one distinct string. The algorithm correctly returns 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character is inspected exactly once. |
| Space | O(1) | Only the answer and loop variables are stored apart from the input string. |

With `n <= 200000`, the algorithm performs only about 200,000 character comparisons. This is comfortably within the stated 2-second time limit and uses negligible auxiliary memory.

## Test Cases

```
# helper: run solution on input string, return output string
def run(inp: str) -> str:
    s = inp.strip()
    return str(solve_string(s))

# Provided samples
assert run("abca") == "4", "sample 1"
assert run("zzz") == "1", "sample 2"

# Minimum-size inputs
assert run("aa") == "1", "two equal characters form one run"
assert run("ab") == "2", "two different characters form two runs"

# All characters equal
assert run("aaaaaaaaaa") == "1", "all deletions produce the same string"

# Every character starts a new run
assert run("abababab") == "8", "alternating characters produce eight runs"

# Several runs with different lengths
assert run("aabbbaa") == "3", "runs are aa, bbb, aa"

# Maximum-size input, all equal
maximum_equal = "a" * 200000
assert run(maximum_equal) == "1", "maximum length with one run"

# Maximum-size input, alternating characters
maximum_alternating = "ab" * 100000
assert run(maximum_alternating) == "200000", "maximum length with every position in its own run"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `aa` | 1 | Minimum length and duplicate deletion results |
| `ab` | 2 | Minimum length with two distinct runs |
| `aaaaaaaaaa` | 1 | All deletion positions are equivalent |
| `abababab` | 8 | Every position forms a separate run |
| `aabbbaa` | 3 | Multiple runs with different lengths |
| `a * 200000` | 1 | Maximum input size and constant-size scan state |
| `(ab) * 100000` | 200000 | Maximum number of runs and boundary handling |

## Edge Cases

For `aa`, the algorithm starts with `answer = 1`. At index 1, the current character is also `a`, so the answer remains 1. The two possible deletions both produce `a`, which confirms the handling of the minimum-size equal-character case.

For `ab`, the initial answer is 1, and the comparison at index 1 finds `b != a`, increasing the answer to 2. The two deletion results are `b` and `a`, so they are genuinely different.

For `aaaa`, the scan never sees a character different from its predecessor. The answer remains 1, matching the fact that deleting any of the four positions produces `aaa`.

For `aabbbaa`, the scan sees the transitions `a -> b` and `b -> a`. Starting from 1, these two transitions produce an answer of 3. The runs are `aa`, `bbb`, and `aa`, and each run corresponds to exactly one distinct string.

For the maximum-length alternating string `abab...ab`, every neighboring pair differs. The answer is incremented at every position after the first, producing 200,000. This checks both the upper bound on the answer and the absence of an off-by-one error in the loop.

The key edge case behind the entire solution is a pair of deletion positions inside the same equal-character run. For `aabb`, deleting either character from the first `aa` produces `abb`. The algorithm counts that entire run only once. When moving from the first run to the second run, the character changes from `a` to `b`, so the answer increases to 2, exactly matching the two distinct resulting strings.
