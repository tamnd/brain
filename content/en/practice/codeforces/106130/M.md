---
title: "CF 106130M - \u5b57\u7b26\u6d88\u6d88\u4e50"
description: "We are given a lowercase string. Before the game starts, we may rearrange its characters in any order we like. A single elimination operation chooses a contiguous block consisting of the same character, and that block must have length at least 3."
date: "2026-06-19T19:52:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106130
codeforces_index: "M"
codeforces_contest_name: "GDUT 2025 Monthly competition"
rating: 0
weight: 106130
solve_time_s: 66
verified: true
draft: false
---

[CF 106130M - \u5b57\u7b26\u6d88\u6d88\u4e50](https://codeforces.com/problemset/problem/106130/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a lowercase string. Before the game starts, we may rearrange its characters in any order we like.

A single elimination operation chooses a contiguous block consisting of the same character, and that block must have length at least 3. The entire block disappears, and the remaining parts of the string are concatenated. We may perform at most `k` such operations.

The task is to find the minimum possible final length of the string.

The crucial detail is the freedom to rearrange the string before any eliminations happen. Once the order is no longer fixed, the problem is no longer about positions inside the original string. The only thing that matters is how many times each character appears.

The string length can be as large as `10^5`, so any algorithm that tries to simulate rearrangements or elimination sequences on the string itself is unnecessary. The alphabet contains only 26 lowercase letters, which strongly suggests that the solution should be based on character frequencies rather than on the string structure.

A few edge cases are easy to misjudge.

Consider:

```
n = 2, k = 100
s = aa
```

The count of `'a'` is only 2. No block of length at least 3 can ever be formed, so the answer is `2`, not `0`.

Consider:

```
n = 6, k = 1
s = aaabbb
```

A careless approach might think that only one of the two groups can be removed after rearrangement, which is correct. We remove either `"aaa"` or `"bbb"`, leaving length `3`.

Consider:

```
n = 7, k = 5
s = aaaaabc
```

Although `k` is large, the character `'a'` can be eliminated completely in a single operation because all five copies can be placed into one block `"aaaaa"`. The answer is `2`, not something requiring multiple operations.

## Approaches

A brute-force mindset would be to think about all possible rearrangements and all possible elimination orders. Even for a moderate string length, the number of permutations is astronomical, and after every elimination the string changes again. This is completely infeasible.

The key observation is that rearrangement removes all positional constraints.

Suppose a character appears `c` times.

If `c < 3`, that character can never form a removable block. No matter how we rearrange the string, at least those `c` characters must remain.

If `c ≥ 3`, we can place all copies together into one contiguous block and remove the entire block in a single operation. There is never any benefit in spending more than one operation on the same character, because one operation already deletes every occurrence of that character.

This transforms the problem into a simple resource allocation problem.

Each character with frequency at least 3 becomes an item:

- Cost: 1 operation.
- Gain: its frequency.

We have a budget of at most `k` operations and want to maximize the number of deleted characters. The optimal strategy is to remove the characters with the largest frequencies first.

Since there are only 26 lowercase letters, we only need to count frequencies, collect all frequencies at least 3, sort them in descending order, and take the largest `k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n + 26 log 26) | O(26) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of every lowercase letter.
2. For every frequency `c`, check whether `c ≥ 3`.

A frequency smaller than 3 can never be eliminated, so it contributes nothing to the removable pool.
3. Store every removable frequency in a list.

Each such frequency represents a character that can be completely deleted using exactly one operation.
4. Sort the list in descending order.

Since every removable character costs the same number of operations, namely one, we should spend operations on the largest frequencies first.
5. Take the first `min(k, len(list))` frequencies and sum them.

This is the maximum number of characters that can be removed.
6. Output:

```
n - removed_characters
```

### Why it works

After rearrangement, occurrences of the same character can always be grouped together.

For a character appearing `c ≥ 3` times, placing all copies consecutively creates a removable block of length `c`, so the entire character class can be deleted in one operation. For a character appearing fewer than 3 times, no removable block can be formed at all.

Thus every character independently falls into one of two categories: completely removable with cost 1, or not removable. The problem becomes selecting at most `k` removable characters whose total frequencies are as large as possible. Since all costs are equal, choosing the largest frequencies is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    s = input().strip()

    freq = [0] * 26
    for ch in s:
        freq[ord(ch) - ord('a')] += 1

    removable = [c for c in freq if c >= 3]
    removable.sort(reverse=True)

    removed = sum(removable[:k])
    print(n - removed)

solve()
```

The first part counts character frequencies.

The list `removable` contains exactly those characters whose entire occurrence set can be deleted in one operation. Frequencies below 3 are ignored because they can never participate in a valid elimination.

After sorting in descending order, the first `k` entries correspond to the most profitable operations. Summing them gives the maximum number of deleted characters.

The final answer is the original length minus the number of removed characters.

A subtle point is that `k` may be much larger than the number of removable characters. Python slicing handles this naturally, so `removable[:k]` is safe even when `k` exceeds the list length.

## Worked Examples

### Sample 1

Input:

```
9 3
aaccbbbba
```

Character frequencies:

| Character | Frequency |
| --- | --- |
| a | 3 |
| b | 4 |
| c | 2 |

Removable frequencies:

| Step | Removable List |
| --- | --- |
| Before sorting | [3, 4] |
| After sorting | [4, 3] |

Selection:

| k | Chosen Frequencies | Removed |
| --- | --- | --- |
| 3 | [4, 3] | 7 |

Final answer:

| n | Removed | Result |
| --- | --- | --- |
| 9 | 7 | 2 |

This example shows that once rearrangement is allowed, we simply remove the whole `'b'` group and the whole `'a'` group.

### Sample 2

Input:

```
5 1
aaaaa
```

Character frequencies:

| Character | Frequency |
| --- | --- |
| a | 5 |

Removable frequencies:

| Step | Removable List |
| --- | --- |
| Before sorting | [5] |
| After sorting | [5] |

Selection:

| k | Chosen Frequencies | Removed |
| --- | --- | --- |
| 1 | [5] | 5 |

Final answer:

| n | Removed | Result |
| --- | --- | --- |
| 5 | 5 | 0 |

This demonstrates that all copies of a character can be deleted in a single operation when its frequency is at least 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + 26 log 26) | Count frequencies, then sort at most 26 values |
| Space | O(26) | Frequency array and removable list |

Since the alphabet size is fixed, the sorting cost is effectively constant. The running time is dominated by the single scan of the string, which easily fits within the constraints for `n = 10^5`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, k = map(int, input().split())
    s = input().strip()

    freq = [0] * 26
    for ch in s:
        freq[ord(ch) - ord('a')] += 1

    removable = [c for c in freq if c >= 3]
    removable.sort(reverse=True)

    return str(n - sum(removable[:k]))

# provided samples
assert run("9 3\naaccbbbba\n") == "2", "sample 1"
assert run("5 1\naaaaa\n") == "0", "sample 2"

# custom cases
assert run("1 0\na\n") == "1", "minimum size"
assert run("2 100\naa\n") == "2", "cannot remove length 2 block"
assert run("6 1\naaabbb\n") == "3", "only one group removable"
assert run("8 4\nabacadae\n") == "4", "one removable character"

# large all-equal case
assert run(f"100000 1\n{'a'*100000}\n") == "0", "maximum size style test"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / a` | `1` | Smallest possible input |
| `2 100 / aa` | `2` | Frequency below 3 is never removable |
| `6 1 / aaabbb` | `3` | Operation budget limits removals |
| `8 4 / abacadae` | `4` | Only one character qualifies for removal |
| `100000 1 / a...a` | `0` | Large frequency handled correctly |

## Edge Cases

Consider:

```
2 100
aa
```

The frequency of `'a'` is 2. The removable list is empty because 2 is smaller than 3.

```
removable = []
removed = 0
answer = 2
```

Even an unlimited operation budget cannot help because no valid block can ever be created.

Consider:

```
6 1
aaabbb
```

The frequencies are `[3, 3]`.

After sorting:

```
[3, 3]
```

Only one operation is available, so we take the first frequency:

```
removed = 3
answer = 6 - 3 = 3
```

This confirms that the operation count, not just removability, matters.

Consider:

```
7 5
aaaaabc
```

The frequencies are:

```
a -> 5
b -> 1
c -> 1
```

The removable list is:

```
[5]
```

Even though five operations are available, there is only one removable character type.

```
removed = 5
answer = 2
```

The algorithm correctly treats a frequency of 5 as a single removable block rather than requiring multiple operations.
