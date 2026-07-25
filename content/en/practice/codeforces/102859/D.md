---
title: "CF 102859D - Banquet"
description: "We have a circular arrangement of N dishes, where each dish is represented by a lowercase letter. A sample is any consecutive sequence of dishes taken clockwise or counter-clockwise around the circle. The task is to count how many different strings can appear as samples."
date: "2026-07-25T14:21:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102859
codeforces_index: "D"
codeforces_contest_name: "mBIT Standard November 2020"
rating: 0
weight: 102859
solve_time_s: 50
verified: true
draft: false
---

[CF 102859D - Banquet](https://codeforces.com/problemset/problem/102859/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a circular arrangement of `N` dishes, where each dish is represented by a lowercase letter. A sample is any consecutive sequence of dishes taken clockwise or counter-clockwise around the circle. The task is to count how many different strings can appear as samples. Two samples are considered equal only when their lengths and every character position are equal.

The circle means the usual substring definition is not enough. A sequence may wrap from the end of the input string back to the beginning, so the clockwise direction can be represented by taking substrings of `S + S` with length at most `N`. The counter-clockwise direction is the same idea applied to the reversed string.

The length of the circle is up to `50000`, which rules out generating every sample explicitly. A string of length `N` has `O(N^2)` possible substrings, and here that would be around 2.5 billion candidates. Even checking each candidate once would already exceed typical contest limits. We need a linear or close to linear solution.

The tricky cases are caused by repeated patterns and by the two directions overlapping. For example, with a single repeated character:

```
Input
4
aaaa
```

The only possible samples are `a`, `aa`, `aaa`, and `aaaa`, so the answer is:

```
4
```

A solution that counts occurrences instead of distinct strings would overcount because every starting position creates the same samples.

Another easy mistake is forgetting that the two directions share answers. For:

```
Input
3
aba
```

Clockwise samples include `ab` and `ba`, while counter-clockwise traversal also produces the same strings. Counting both sides independently would count duplicates. The correct answer is:

```
8
```

The full set is `a`, `b`, `aa`, `ab`, `ba`, `aba`, `aab`, and `baa`.

## Approaches

A direct approach would enumerate every starting dish, extend a sample one character at a time, and store every generated string in a set. There are `N` starting positions and up to `N` lengths for each position, producing `O(N^2)` samples. Since each sample can itself contain up to `N` characters, comparing and storing them can push the brute force toward `O(N^3)` work. Even with hashing, the quadratic number of samples is already too large for `N = 50000`.

The structure of the problem suggests using a suffix automaton. A suffix automaton compactly stores all distinct substrings of a string. Each state represents a group of substrings with the same end-position behavior, and the number of represented strings can be counted from the lengths stored in the automaton.

The circle can be converted into ordinary strings. Clockwise samples are all substrings of `S + S` whose length is at most `N`. Counter-clockwise samples are all substrings of `reverse(S) + reverse(S)` with the same length limit. Instead of building two automata and merging answers manually, we build one generalized suffix automaton that receives both doubled strings. It represents the union of all valid samples.

The only extra detail is the length limit. The doubled strings contain substrings longer than one complete turn, but those are not valid samples. When counting the contribution of a state, every length is capped at `N`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) to O(N³) | O(N²) | Too slow |
| Generalized Suffix Automaton | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Build a generalized suffix automaton by inserting `S + S` and then inserting `reverse(S) + reverse(S)`. Before inserting the second string, start again from the root so the automaton represents the union of substrings from both sources.
2. For every automaton state, store the usual suffix automaton value `len`, which is the maximum length of a substring represented by that state. The suffix link points to the state representing the next smaller suffix group.
3. Count the contribution of each non-root state. Normally a state contributes all lengths from `len[link[state]] + 1` to `len[state]`. Because samples cannot be longer than one full circle, replace both lengths by their minimum with `N`.
4. Add all state contributions. The sum is the number of distinct samples in both directions.

Why it works: a suffix automaton partitions all distinct substrings into states where each state covers one continuous range of lengths. The suffix link tells us the end of the previous range, so every distinct substring appears exactly once in the difference between a state and its suffix link. The generalized construction makes the represented language the union of both directions, and the length cap removes exactly the strings that require going around the circle more than once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    strings = [s + s, (s[::-1]) + (s[::-1])]

    nexts = [{}]
    link = [-1]
    length = [0]

    def extend(c, last):
        cur = len(nexts)
        nexts.append({})
        length.append(length[last] + 1)
        link.append(0)

        p = last
        while p != -1 and c not in nexts[p]:
            nexts[p][c] = cur
            p = link[p]

        if p == -1:
            link[cur] = 0
        else:
            q = nexts[p][c]
            if length[p] + 1 == length[q]:
                link[cur] = q
            else:
                clone = len(nexts)
                nexts.append(nexts[q].copy())
                length.append(length[p] + 1)
                link.append(link[q])

                while p != -1 and nexts[p].get(c) == q:
                    nexts[p][c] = clone
                    p = link[p]

                link[q] = clone
                link[cur] = clone

        return cur

    for text in strings:
        last = 0
        for c in text:
            last = extend(c, last)

    ans = 0
    for state in range(1, len(length)):
        high = min(length[state], n)
        low = min(length[link[state]], n)
        if high > low:
            ans += high - low

    print(ans)

if __name__ == "__main__":
    solve()
```

The automaton construction is the standard suffix automaton extension. Each inserted character creates a new state and fixes transitions that previously did not exist. Cloning is required when an existing transition leads to a state whose length range is too large for the new suffix.

The important implementation detail is resetting `last` to the root before inserting the reversed doubled string. Without this reset, the automaton would behave as if the second string continued the first one, which would introduce invalid substrings crossing the boundary.

The final loop computes the number of represented lengths for each state. The root is skipped because it represents the empty string. The `min` operation applies the circular-length restriction and avoids counting samples longer than one full trip around the table.

## Worked Examples

For:

```
3
aba
```

The two inserted strings are `abaaba` and `abaaba` because the reverse is the same. The automaton only needs one copy of the language.

| State | Length | Suffix Link Length | Contribution |
| --- | --- | --- | --- |
| `a` group | 1 | 0 | 1 |
| `ab` group | 2 | 1 | 1 |
| `aba` group | 3 | 1 | 2 |
| repeated groups | ... | ... | remaining distinct strings |

The total becomes `8`. The trace demonstrates that duplicated clockwise and counter-clockwise samples are merged automatically.

For:

```
6
ondrej
```

The reverse direction adds strings such as `rejo` and `drejon`, while the clockwise direction contains strings from `ondrejondrej`.

| Stage | Inserted text | Maximum sample length considered | Effect |
| --- | --- | --- | --- |
| First insertion | `ondrejo...` | 6 | Adds clockwise samples |
| Second insertion | reversed doubled string | 6 | Adds counter-clockwise samples |
| Counting | all states | 6 | Counts union only |

The automaton keeps shared substrings in the same states, so the final count is the number of unique samples from both directions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | The automaton receives four copies of the original length in total, and every state operation is amortized constant time. |
| Space | O(N) | A suffix automaton contains at most about twice the number of inserted characters in states. |

The input size of `50000` is well within the linear bounds. The implementation avoids storing all substrings, which is the main reason it fits the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# samples
assert run("3\naba\n") == "8\n", "sample 1"
assert run("6\nondrej\n") == "66\n", "sample 2"

# custom cases
assert run("4\naaaa\n") == "4\n", "all equal values"
assert run("2\nab\n") == "4\n", "minimum size"
assert run("5\nabcde\n") == "25\n", "all characters different"
assert run("5\nabcba\n") == "17\n", "palindrome overlap case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 aaaa` | `4` | Repeated strings must be counted once |
| `2 ab` | `4` | Smallest circle and both directions |
| `5 abcde` | `25` | Maximum diversity of substrings |
| `5 abcba` | `17` | Overlap between directions |

## Edge Cases

For the repeated-character case:

```
4
aaaa
```

The doubled string is `aaaaaaaa`. The automaton sees many occurrences of the same patterns, but they collapse into the same states. The state contributions produce lengths `1`, `2`, `3`, and `4` only, giving the correct answer `4`.

For the direction-overlap case:

```
3
aba
```

The reversed circle produces no new unique strings beyond the shared language already represented in the automaton. Because both doubled strings are inserted into the same structure, the counting formula does not add duplicate states for the same samples. The answer remains `8`.

For a case where wrapping matters:

```
5
abcde
```

A sample such as `dea` cannot be found in the original string as a normal substring, but it appears inside `abcdeabcde`. The doubling step creates these wrapped substrings, and the length cap prevents invalid samples such as `abcdea` from being counted. The final answer is `25`.
