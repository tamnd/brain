---
title: "CF 102168L - \u041f\u0435\u0440\u0435\u0432\u043e\u0440\u043e\u0442\u044b"
description: "We have two non-empty lowercase strings, s and t. In one operation we may choose any two positions in s and reverse the entire substring between them. We may perform the operation any number of times, including zero times."
date: "2026-08-19T07:30:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102168
codeforces_index: "L"
codeforces_contest_name: "\u041b\u0438\u0447\u043d\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u043e\u0433\u043e \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442\u0430 \u0441\u0440\u0435\u0434\u0438 \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432 2018-2019"
rating: 0
weight: 102168
solve_time_s: 93
verified: true
draft: false
---

[CF 102168L - \u041f\u0435\u0440\u0435\u0432\u043e\u0440\u043e\u0442\u044b](https://codeforces.com/problemset/problem/102168/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two non-empty lowercase strings, `s` and `t`. In one operation we may choose any two positions in `s` and reverse the entire substring between them. We may perform the operation any number of times, including zero times. The task is to determine whether `s` can be transformed into exactly `t`.

The key question is not which individual reversals to perform, but which rearrangements of the characters can be produced by repeated reversals. Since both strings contain at most 200,000 characters, an algorithm that examines many possible reversal sequences cannot work. With a two-second limit, the intended solution needs to be essentially linear in the string length. Quadratic algorithms already require around 40 billion elementary iterations at the maximum size, which is far beyond what is practical.

The first edge case is different lengths. For example, `s = "abcd"` and `t = "abc"` must produce `NO`. A reversal never changes the number of characters, so any approach that only compares character frequencies without first considering length would need to handle this explicitly.

The second edge case is repeated characters. For `s = "xxx"` and `t = "yyy"`, the answer is `NO`, even though both strings have the same length. A careless solution that checks only the lengths would accept it. Character multiplicities matter.

The third edge case is that the strings do not have to be equal or obtainable with a single reversal. For `s = "abac"` and `t = "acba"`, the answer is `YES`. The transformation can be achieved through several reversals, so testing whether `t` is exactly one reversed substring away from `s` is insufficient.

The fourth edge case is a string that is already equal to the target. For example, `s = "abc"` and `t = "abc"` must produce `YES`, because performing zero operations is allowed. An implementation that assumes at least one reversal is required can reject this valid case.

## Approaches

A direct brute-force approach would treat every possible arrangement of the characters as a candidate reachable state. For each state, we could try every possible reversal and continue exploring until either `t` is found or every reachable arrangement has been exhausted. This is correct because every legal operation is explicitly represented, but it quickly becomes unusable. With `n` distinct characters there can be `n!` different permutations, and even checking one permutation against `t` costs `O(n)`. A complete permutation-based search therefore needs at least `O(n · n!)` work, with an additional `O(n^2)` factor if every state explicitly examines all possible reversal intervals.

The useful observation comes from considering the smallest possible reversal. If we reverse a substring of length two, positions `i` and `i + 1` simply exchange their characters. In other words, the allowed operation includes an adjacent swap.

Adjacent swaps are enough to produce every permutation of a string. We can move any desired character one position at a time until it reaches its target position, repeating this process for every position. Consequently, repeated substring reversals can rearrange the characters in `s` in completely arbitrary ways.

Once arbitrary permutations are possible, the exact order of the original characters no longer matters. The only invariant is how many times each character occurs. A transformation from `s` to `t` exists exactly when the two strings have the same length and the same frequency for every lowercase letter.

Because the alphabet contains only 26 lowercase letters, we do not even need a general-purpose dictionary. We can keep two arrays of 26 counters and compare them. This gives a simple linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n · n!)` at minimum | `O(n)` to store a state, potentially exponential for visited states | Too slow |
| Optimal | `O(n)` | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Read `s` and `t` and compare their lengths. If the lengths differ, print `NO` immediately because reversal never changes the number of positions.
2. Create an array of 26 counters for `s` and another array of 26 counters for `t`. The index `0` represents `'a'`, index `1` represents `'b'`, and so on.
3. Scan `s` and increment the counter corresponding to each character. Do the same for `t`. This records exactly which multiset of characters each string contains.
4. Compare the two frequency arrays. If every count is equal, print `YES`; otherwise print `NO`.

The reason this frequency test is sufficient is that a length-two reversal gives us an adjacent swap. Since arbitrary adjacent swaps generate every permutation, any ordering with the same character multiset can be reached.

### Why it works

Every operation preserves the multiset of characters, so different frequencies can never be transformed into each other. Conversely, suppose `s` and `t` have identical character frequencies. Since adjacent swaps are allowed, we can rearrange `s` into any permutation of its characters. We can construct `t` from left to right by moving an occurrence of the required character into each target position using adjacent swaps. Repeated substring reversals can perform those swaps, so `t` is reachable. Thus the frequency condition is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    t = input().strip()

    if len(s) != len(t):
        print("NO")
        return

    cnt_s = [0] * 26
    cnt_t = [0] * 26

    for ch in s:
        cnt_s[ord(ch) - ord('a')] += 1

    for ch in t:
        cnt_t[ord(ch) - ord('a')] += 1

    print("YES" if cnt_s == cnt_t else "NO")

if __name__ == "__main__":
    solve()
```

The first check handles the length boundary before any character processing. This is both logically necessary and slightly cheaper for impossible inputs.

The two arrays have exactly 26 entries because the input alphabet is restricted to lowercase English letters. The expression `ord(ch) - ord('a')` maps each character to an integer from 0 through 25.

The comparison `cnt_s == cnt_t` checks all character multiplicities simultaneously. There is no need to compare positions because reversals can change the order arbitrarily.

No integer overflow is possible in Python, and the largest counter is only 200,000. The strings themselves also fit comfortably in memory.

## Worked Examples

### Sample 1

For `s = "abac"` and `t = "acba"`, both strings have four characters. Their frequency vectors are identical.

| Character | Count in `s` | Count in `t` |
| --- | --- | --- |
| `a` | 2 | 2 |
| `b` | 1 | 1 |
| `c` | 1 | 1 |
| other letters | 0 | 0 |

The algorithm therefore prints `YES`.

The example also demonstrates why checking only whether one reversal works would be the wrong abstraction. The operation set is powerful enough to realize arbitrary permutations, so the final order itself does not impose an additional restriction.

### Sample 2

For `s = "xxx"` and `t = "yyy"`, the lengths agree, so the algorithm proceeds to the frequency comparison.

| Character | Count in `s` | Count in `t` |
| --- | --- | --- |
| `x` | 3 | 0 |
| `y` | 0 | 3 |
| other letters | 0 | 0 |

The frequency arrays differ, so the algorithm prints `NO`.

This confirms that equal length alone is not enough. Reversals only rearrange existing characters, and cannot turn one character into another.

### Sample 3

For `s = "abcd"` and `t = "abc"`, the lengths are different.

| Variable | Value |
| --- | --- |
| `len(s)` | 4 |
| `len(t)` | 3 |
| Decision | `NO` |

The algorithm returns immediately without constructing frequency arrays. No sequence of reversals can remove the fourth character.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Each input string is scanned once, and the final frequency comparison examines only 26 entries. |
| Space | `O(1)` | Two arrays of 26 integers are used, independent of `n`. |

For `n <= 200000`, the algorithm performs only a few hundred thousand character operations. This is comfortably within the given two-second limit, while the brute-force permutation space grows factorially and becomes impossible even for very small strings.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    s = input().strip()
    t = input().strip()

    if len(s) != len(t):
        print("NO")
        return

    cnt_s = [0] * 26
    cnt_t = [0] * 26

    for ch in s:
        cnt_s[ord(ch) - ord('a')] += 1

    for ch in t:
        cnt_t[ord(ch) - ord('a')] += 1

    print("YES" if cnt_s == cnt_t else "NO")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("abac\nacba\n") == "YES\n", "sample 1"
assert run("xxx\nyyy\n") == "NO\n", "sample 2"
assert run("abcd\nabc\n") == "NO\n", "sample 3"

# Minimum-size input
assert run("a\na\n") == "YES\n", "single equal character"

# Minimum-size mismatch
assert run("a\nb\n") == "NO\n", "single different character"

# All characters equal
assert run("aaaaaa\naaaaaa\n") == "YES\n", "all equal characters"

# Same multiset, very different order
assert run("abcabc\nccbbaa\n") == "YES\n", "same frequencies"

# Same length, but one character count differs
assert run("aabb\nabac\n") == "NO\n", "different multiplicities"

# Maximum-size input
n = 200000
assert run("a" * n + "\n" + "a" * n + "\n") == "YES\n", "maximum length"

# Maximum-size mismatch at the boundary
assert run("a" * (n - 1) + "b\n" + "a" * n + "\n") == "NO\n", "maximum length mismatch"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / a` | `YES` | Minimum string length and zero operations |
| `a / b` | `NO` | Minimum-size character mismatch |
| `aaaaaa / aaaaaa` | `YES` | All characters identical |
| `abcabc / ccbbaa` | `YES` | Same multiset with substantially different order |
| `aabb / abac` | `NO` | Different character multiplicities |
| `200000 × 'a' / 200000 × 'a'` | `YES` | Maximum input size and linear performance |
| `199999 × 'a' + 'b' / 200000 × 'a'` | `NO` | Large boundary case with a single frequency mismatch |

## Edge Cases

For different lengths, consider `s = "abcd"` and `t = "abc"`. The algorithm compares `4` and `3`, immediately prints `NO`, and never tries to compare their character frequencies. This is correct because every reversal preserves the length exactly.

For repeated characters with different multiplicities, consider `s = "aabb"` and `t = "abac"`. Both strings have length four, so the length test passes. The frequency of `a` is two in both strings, but `s` contains two `b` characters while `t` contains one `b` and one `c`. The arrays differ at those positions, so the result is `NO`.

For transformations requiring more than one reversal, consider `s = "abcabc"` and `t = "ccbbaa"`. The frequency of `a`, `b`, and `c` is two in both strings. The algorithm returns `YES` without attempting to find a particular sequence of reversals. The proof above guarantees that such a sequence exists because adjacent swaps can realize any permutation.

For already equal strings, consider `s = "abc"` and `t = "abc"`. The lengths match and all three character counts match, so the result is `YES`. This corresponds to using zero operations, which is allowed.

For the smallest possible strings, `s = "a"` and `t = "b"` cannot be changed at all because there is no pair of distinct positions on which to perform a meaningful reversal. Their frequencies differ, so the algorithm returns `NO`. For `s = "a"` and `t = "a"`, the frequencies match and the algorithm returns `YES`.

The maximum-size case contains 200,000 characters. The algorithm still performs one pass over each string and keeps only 52 counters, so its resource usage does not depend on the number of possible permutations. This is exactly the property needed to make the solution practical under the given constraints.
