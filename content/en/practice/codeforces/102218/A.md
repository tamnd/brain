---
title: "CF 102218A - Alan's Birthday"
description: "We are given a string of (N) lowercase English letters. We may freely change the positions of its characters, but we must keep exactly the same multiset of letters. Among all possible rearrangements, we need the one that appears earliest in lexicographic order."
date: "2026-08-18T12:31:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "A"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 620
verified: false
draft: false
---

[CF 102218A - Alan's Birthday](https://codeforces.com/problemset/problem/102218/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of (N) lowercase English letters. We may freely change the positions of its characters, but we must keep exactly the same multiset of letters. Among all possible rearrangements, we need the one that appears earliest in lexicographic order.

The dictionary is searched from the lexicographically smallest word toward larger words, so giving Alan a lexicographically smaller rearrangement makes him find the word sooner. The task is consequently to construct the smallest permutation of the characters of (S).

The constraint (N \le 10^7) is the main signal about the intended complexity. Ten million characters already require linear work just to read the input, so an (O(N^2)) algorithm is completely out of range. Even (O(N\log N)), while asymptotically reasonable for many sorting problems, performs substantially more work than necessary here and can also create extra memory pressure under the 64 MB limit. The alphabet contains only 26 possible characters, which gives us a way to process the entire string in linear time without performing a general-purpose sort.

A careless implementation can also fail on repeated characters. For example, with

```
4
bbaa
```

the correct output is

```
aabb
```

because both copies of `a` must appear before both copies of `b`. Treating the characters as distinct objects and trying to reason about permutations can accidentally count identical arrangements multiple times, although the final answer is still determined entirely by their frequencies.

The smallest possible input is another simple boundary case. With

```
1
z
```

the only possible rearrangement is

```
z
```

An implementation that assumes there are at least two characters could incorrectly access another position or perform unnecessary swapping.

The alphabet boundaries can also expose mistakes in counting or output order. For

```
2
za
```

the answer is

```
az
```

The fact that `z` occurs before `a` in the input is irrelevant. The output must follow the fixed alphabet order, not the order in which characters first appear.

Finally, a string such as

```
5
aaaaa
```

must remain exactly the same. A counting implementation has to output every occurrence, not just one copy of each distinct character.

## Approaches

The most direct solution is to consider every possible rearrangement of the string, compare them lexicographically, and keep the smallest one. This is correct because the desired answer is defined as the minimum among precisely those rearrangements. The problem is the number of candidates. With (N) characters, there can be (N!) permutations when all characters are distinct, and comparing a candidate with the current best can take (O(N)) time in the worst case. The resulting worst-case operation count is (O(N\cdot N!)), which becomes impossible even for very small values of (N), let alone (10^7).

A more practical first idea is to use a standard sorting algorithm. Sorting the characters places the smallest character first, then the next smallest, and so on, producing the lexicographically smallest permutation. This takes (O(N\log N)) time in general.

The brute-force approach works because it explicitly examines every possible ordering, but fails because the number of orderings grows factorially. The observation that unlocks the problem is that characters come from an alphabet of only 26 letters. We do not need to sort arbitrary values. We only need to know how many `a` characters exist, how many `b` characters exist, and so on through `z`.

Once those frequencies are known, the smallest rearrangement is forced. Every `a` must come first, followed by every `b`, followed by every `c`, and so forth. Counting the letters takes (O(N)), and traversing the 26-letter alphabet takes (O(26)), which is effectively constant. The complete algorithm is therefore (O(N)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N\cdot N!)) | (O(N)) | Too slow |
| Standard Sorting | (O(N\log N)) | (O(N)) | Correct, but unnecessary work |
| Frequency Counting | (O(N+26)) | (O(26)) besides the input/output | Accepted |

## Algorithm Walkthrough

1. Read (N) and the string (S). The value of (N) tells us how many characters should occur, while (S) contains the actual characters whose order we are allowed to change.
2. Create an array `count` of size 26, initially filled with zeroes. Position 0 represents `a`, position 1 represents `b`, and position 25 represents `z`. A fixed-size frequency array is sufficient because the alphabet never contains more than 26 different characters.
3. Scan every character of (S`and increment its corresponding frequency. For a character`c`, its position in the array is `ord(c) - ord('a')`. After this scan, `count[i]` exactly equals the number of copies of the corresponding letter in the input.
4. Traverse the alphabet from `a` through `z`. For each letter, append it exactly `count[i]` times to the answer. We process letters in increasing alphabetic order because any occurrence of a smaller character must precede every occurrence of a larger character in the lexicographically smallest permutation.
5. Print the resulting string. Since the frequencies sum to (N), the output contains exactly the same characters as the input, only arranged in increasing order.

### Why it works

After the counting phase, the algorithm knows exactly how many copies of every letter must appear in the answer. Consider any two different letters (x < y). If an occurrence of (y) appears before an occurrence of (x), swapping those two positions makes the string lexicographically smaller at the first position where the two strings differ. Consequently, no lexicographically smallest arrangement can place a larger letter before a smaller one. Applying this argument to every pair of letters forces all `a` characters to come first, then all `b` characters, continuing through `z`. The algorithm constructs exactly that arrangement, so no other valid rearrangement can be lexicographically smaller.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()

count = [0] * 26

for ch in s:
    count[ord(ch) - 97] += 1

answer = ''.join(chr(97 + i) * count[i] for i in range(26))
sys.stdout.write(answer + '\n')
```

The first line reads the declared length, although the length does not otherwise need to be used. The string itself contains all information required to construct the answer.

The frequency array has exactly 26 positions. For each character, `ord(ch) - 97` converts `a` to 0, `b` to 1, and `z` to 25. No sorting is performed, so processing the ten million characters remains linear.

The expression `chr(97 + i) * count[i]` creates the required run of one letter. Joining the 26 runs produces the complete sorted string. There is no off-by-one issue because the loop covers exactly indices 0 through 25.

The input contains only lowercase English letters, so `strip()` does not remove any meaningful character. It only removes the line ending, along with any accidental surrounding whitespace.

Python integers do not overflow, and every frequency is at most (10^7). The output itself necessarily contains (N) characters, so creating a string of that size is unavoidable. The algorithm does not create an additional sorted copy or any data structure proportional to (N) beyond the input and final output strings.

## Worked Examples

### Sample 1

For the input `mac`, the frequency array has one `a`, one `c`, one `m`, and zero copies of every other letter.

| Letter | Count | Output after processing |
| --- | --- | --- |
| `a` | 1 | `a` |
| `b` | 0 | `a` |
| `c` | 1 | `ac` |
| `d` through `l` | 0 | `ac` |
| `m` | 1 | `acm` |
| `n` through `z` | 0 | `acm` |

The final result is `acm`. The trace demonstrates why the original positions of the characters do not matter. The `a` is emitted first even though it appeared in the middle of the input.

### Sample 2

For `geso`, every character occurs once.

| Letter | Count | Output after processing |
| --- | --- | --- |
| `a` through `d` | 0 | `` |
| `e` | 1 | `e` |
| `f` through `g` | 0, 1 | `eg` |
| `h` through `n` | 0 | `eg` |
| `o` | 1 | `ego` |
| `p` through `r` | 0 | `ego` |
| `s` | 1 | `egos` |
| `t` through `z` | 0 | `egos` |

The final result is `egos`. Since `e < g < o < s`, emitting the letters in alphabetic order produces the earliest possible dictionary position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N+26)=O(N)) | Every input character is counted once, then the fixed 26-letter alphabet is traversed. |
| Space | (O(26)) auxiliary | The frequency array always contains only 26 integers. The input and output strings themselves require (O(N)) memory. |

With (N) as large as (10^7), linear time is the appropriate target because simply reading the input already costs (O(N)). The algorithm performs only one pass over the characters and a constant amount of additional work. It also avoids the extra structures and comparisons associated with general-purpose sorting, which is especially useful under the 64 MB memory limit.

## Test Cases

```python
import sys
import io

input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    count = [0] * 26

    for ch in s:
        count[ord(ch) - 97] += 1

    answer = ''.join(chr(97 + i) * count[i] for i in range(26))
    sys.stdout.write(answer + '\n')

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue().rstrip('\n')
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = sys.stdin.readline

# Provided samples
assert run("3\nmac\n") == "acm", "sample 1"
assert run("4\ngeso\n") == "egos", "sample 2"

# Minimum-size input
assert run("1\nz\n") == "z", "single character"

# All characters are equal
assert run("5\naaaaa\n") == "aaaaa", "all equal"

# Reverse alphabetic order with duplicates
assert run("6\nzzbaaa\n") == "aaabzz", "duplicates and reverse order"

# Characters from both alphabet boundaries
assert run("5\nzayzx\n") == "axyzz", "alphabet boundaries"

# Maximum-size input
s = "z" * 10_000_000
out = run("10000000\n" + s + "\n")
assert out == s, "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / z` | `z` | Minimum size and single-character handling |
| `5 / aaaaa` | `aaaaa` | All characters identical |
| `6 / zzbaaa` | `aaabzz` | Duplicate frequencies and reordering |
| `5 / zayzx` | `axyzz` | Correct handling of `a` and `z` boundaries |
| `10000000 / z...z` | Same 10,000,000 `z` characters | Maximum input size and linear processing |

The maximum-size test deliberately uses one repeated character. That makes the expected result easy to construct while still exercising the full input bound. The assertion compares the produced string with the already-created input string, avoiding the need to construct another separate ten-million-character expected value.

## Edge Cases

For the single-character case

```
1
z
```

the counting pass increments the frequency of `z` to one. The alphabet traversal reaches `z` and emits it once, producing `z`. Nothing in the algorithm assumes that multiple positions exist.

For repeated characters,

```
4
bbaa
```

the counts become `a = 2` and `b = 2`. The traversal emits `aa` before `bb`, giving `aabb`. The original order `bbaa` has no influence because the algorithm stores frequencies rather than positions.

For the alphabet boundary case,

```
2
za
```

the counts are `a = 1` and `z = 1`. Since the output loop starts at `a` and ends at `z`, it emits `a` first and `z` last, producing `az`. This catches implementations that accidentally preserve input order or use an incorrect character comparison.

For an already sorted string,

```
3
abc
```

the counts are already consistent with the required output order. The algorithm produces `abc` unchanged. This confirms that the procedure is not merely reversing or otherwise applying a fixed permutation.

For an input containing every character equally,

```
26
abcdefghijklmnopqrstuvwxyz
```

each frequency is one, so the output is exactly `abcdefghijklmnopqrstuvwxyz`. The frequency array covers every valid index from 0 through 25, confirming that neither endpoint of the alphabet is skipped.
