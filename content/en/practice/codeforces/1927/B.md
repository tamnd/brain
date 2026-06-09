---
title: "CF 1927B - Following the String"
description: "We are given an array a that describes how a hidden string was built. For each position i, the value a[i] tells us how many times the character at position i has already appeared earlier in the string. If a[i] = 0, this character has never appeared before."
date: "2026-06-08T18:53:28+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1927
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 923 (Div. 3)"
rating: 900
weight: 1927
solve_time_s: 142
verified: false
draft: false
---

[CF 1927B - Following the String](https://codeforces.com/problemset/problem/1927/B)

**Rating:** 900  
**Tags:** constructive algorithms, greedy, strings  
**Solve time:** 2m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array `a` that describes how a hidden string was built.

For each position `i`, the value `a[i]` tells us how many times the character at position `i` has already appeared earlier in the string. If `a[i] = 0`, this character has never appeared before. If `a[i] = 2`, the same character has already appeared exactly twice before position `i`.

Our task is to reconstruct any lowercase string whose trace matches the given array.

The key observation is that the trace does not care about which specific letter is used. It only cares about how many previous occurrences that letter already had when it was placed.

The total length across all test cases is at most `2 · 10^5`, so the solution must be close to linear time. An `O(n²)` approach would perform roughly `4 · 10^10` operations in the worst case, which is far beyond the limit. A linear or near-linear solution is required.

Several situations can cause mistakes if the reconstruction logic is not chosen carefully.

Consider:

```
a = [0, 1, 2, 3]
```

The only valid construction repeatedly uses the same character:

```
aaaa
```

At position 3, we need a character that has already appeared three times. Choosing a new letter would immediately violate the trace.

Another example is:

```
a = [0, 0, 0, 0]
```

A valid answer is:

```
abcd
```

Using the same character repeatedly would produce trace values `[0,1,2,3]` instead.

A more subtle case is:

```
a = [0, 0, 1]
```

The third character must match the second character, not the first one. The trace requires exactly one previous occurrence. If we pick the first character, its occurrence count would already be one, but after using it the trace would correspond to a different construction history. We must track the current frequency of every letter carefully.

The statement guarantees that at least one valid answer exists, so we never need to detect impossibility.

## Approaches

A direct brute-force reconstruction is easy to imagine.

Process the string from left to right. For position `i`, try every letter from `'a'` to `'z'`. For each candidate letter, count how many times it has appeared earlier in the partially constructed string. If that count equals `a[i]`, place the letter and continue.

This works because the definition of the trace can be checked directly. The problem is efficiency. Counting previous occurrences by scanning the already-built prefix costs `O(n)` per letter. With up to 26 letters tested at each position, the complexity becomes `O(26·n²)`, which is too slow for `n = 2 · 10^5`.

The structure of the trace gives a much simpler solution.

Suppose we know the current frequency of every letter. If a letter has appeared `k` times so far, then placing it now would produce trace value `k`, because exactly `k` previous occurrences already exist.

That means position `i` only needs a letter whose current frequency equals `a[i]`.

Since there are only 26 lowercase letters, we can maintain the frequency of each letter and search for one whose count matches `a[i]`. After choosing it, we increase that frequency by one.

The statement guarantees that a valid answer exists, so such a letter will always be available.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(26·n) = O(n) | O(26) | Accepted |

## Algorithm Walkthrough

1. Create an array `cnt` of size 26, initialized with zeros. `cnt[j]` stores how many times letter `j` has already been used.
2. Process the trace from left to right.
3. For the current value `a[i]`, find any letter whose current frequency equals `a[i]`.
4. Append that letter to the answer string.
5. Increase that letter's frequency by one, because it has now appeared once more.
6. Continue until all positions are processed.
7. Output the constructed string.

The search in step 3 checks at most 26 letters, which is effectively constant time.

### Why it works

At every moment, `cnt[c]` equals the number of occurrences of character `c` already placed in the prefix.

When we place a character whose current frequency is `k`, exactly `k` copies of that character exist before the current position. By definition, the trace value produced at this position is `k`.

The algorithm always chooses a character whose frequency equals the required value `a[i]`, so the generated trace at position `i` is exactly correct.

After placing the character, its frequency increases by one, preserving the invariant for future positions. Since the input is guaranteed to come from some valid string, a suitable character always exists. Thus every position is constructed correctly, and the final string has exactly the required trace.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        cnt = [0] * 26
        ans = []

        for x in a:
            for j in range(26):
                if cnt[j] == x:
                    ans.append(chr(ord('a') + j))
                    cnt[j] += 1
                    break

        print("".join(ans))

solve()
```

The array `cnt` stores the current occurrence count of every lowercase letter. For each trace value `x`, we search for a letter whose frequency is exactly `x`.

Once such a letter is found, we append it to the answer and increment its frequency. The invariant is that before processing a position, `cnt[j]` equals the number of occurrences of letter `j` already present in the constructed prefix.

A common mistake is trying to track only the last used character or only characters that have appeared before. The trace depends on exact occurrence counts, so all 26 frequencies must be maintained.

Another subtle point is the order of operations. We must compare `cnt[j]` with `x` before incrementing it. Incrementing first would shift every trace value by one and produce incorrect results.

## Worked Examples

### Example 1

Input trace:

```
0 0 0 1 0 2 0 3 1 1 4
```

| Position | Trace Value | Chosen Letter | Frequency Before | Frequency After |
| --- | --- | --- | --- | --- |
| 1 | 0 | a | 0 | 1 |
| 2 | 0 | b | 0 | 1 |
| 3 | 0 | c | 0 | 1 |
| 4 | 1 | a | 1 | 2 |
| 5 | 0 | d | 0 | 1 |
| 6 | 2 | a | 2 | 3 |
| 7 | 0 | e | 0 | 1 |
| 8 | 3 | a | 3 | 4 |
| 9 | 1 | b | 1 | 2 |
| 10 | 1 | c | 1 | 2 |
| 11 | 4 | a | 4 | 5 |

Constructed string:

```
abcadaeabca
```

This is different from the sample output, but it generates the same trace and is completely valid. The example shows that many answers can exist.

### Example 2

Input trace:

```
0 1 2 3 4 5 6 7
```

| Position | Trace Value | Chosen Letter | Frequency Before | Frequency After |
| --- | --- | --- | --- | --- |
| 1 | 0 | a | 0 | 1 |
| 2 | 1 | a | 1 | 2 |
| 3 | 2 | a | 2 | 3 |
| 4 | 3 | a | 3 | 4 |
| 5 | 4 | a | 4 | 5 |
| 6 | 5 | a | 5 | 6 |
| 7 | 6 | a | 6 | 7 |
| 8 | 7 | a | 7 | 8 |

Constructed string:

```
aaaaaaaa
```

This example demonstrates that a single character can satisfy every position when the trace values continually increase.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26·n) = O(n) | For each position we scan at most 26 letters |
| Space | O(26) | Frequency array for lowercase letters |

The total input size across all test cases is at most `2 · 10^5`. The algorithm performs at most `26 × 2 · 10^5 = 5.2 · 10^6` frequency checks, which easily fits within the time limit. Memory usage is constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        cnt = [0] * 26
        ans = []

        for x in a:
            for j in range(26):
                if cnt[j] == x:
                    ans.append(chr(ord('a') + j))
                    cnt[j] += 1
                    break

        out.append("".join(ans))

    return "\n".join(out)

# provided sample structure
assert run("1\n1\n0\n") == "a"

# minimum size
assert run("1\n1\n0\n") == "a"

# all positions use same letter
assert run("1\n4\n0 1 2 3\n") == "aaaa"

# all positions introduce new letters
assert run("1\n5\n0 0 0 0 0\n") == "abcde"

# mixed frequencies
assert run("1\n3\n0 0 1\n") == "abb"

# boundary case with repeated reuse
assert run("1\n8\n0 1 2 3 4 5 6 7\n") == "aaaaaaaa"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `a` | Smallest possible instance |
| `0 1 2 3` | `aaaa` | Repeated reuse of the same character |
| `0 0 0 0 0` | `abcde` | Continuous introduction of new characters |
| `0 0 1` | `abb` | Correct handling of equal frequencies |
| `0 1 2 3 4 5 6 7` | `aaaaaaaa` | Large occurrence counts for one letter |

## Edge Cases

Consider:

```
n = 1
a = [0]
```

Initially every letter has frequency 0. The algorithm chooses `'a'`, increases its count to 1, and outputs:

```
a
```

The trace is `[0]`, which is correct.

Now consider:

```
n = 4
a = [0, 0, 0, 0]
```

The frequencies start as:

```
a:0 b:0 c:0 d:0 ...
```

The algorithm repeatedly chooses the first letter whose count is 0. After using `'a'`, its count becomes 1, so the next available count-0 letter is `'b'`, then `'c'`, then `'d'`.

The result is:

```
abcd
```

Every position corresponds to a first occurrence, matching the trace exactly.

Finally consider:

```
n = 3
a = [0, 0, 1]
```

After processing the first two positions:

```
string = "ab"
counts = {a:1, b:1}
```

The required trace value is now 1. The first letter with frequency 1 is `'a'`, so the algorithm outputs:

```
aba
```

The trace becomes:

```
[0, 0, 1]
```

which matches the input. The example shows why tracking exact frequencies is necessary. The decision depends on current occurrence counts, not on whether a letter has appeared before.
