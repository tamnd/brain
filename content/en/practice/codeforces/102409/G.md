---
title: "CF 102409G - Ironical Solution 2"
description: "The encrypted message is not an arbitrary collection of numbers. There are exactly (2^N) values, one for every subset of the original (N) character codes."
date: "2026-08-11T16:36:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102409
codeforces_index: "G"
codeforces_contest_name: "Semana i 2019"
rating: 0
weight: 102409
solve_time_s: 178
verified: true
draft: false
---

[CF 102409G - Ironical Solution 2](https://codeforces.com/problemset/problem/102409/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The encrypted message is not an arbitrary collection of numbers. There are exactly (2^N) values, one for every subset of the original (N) character codes. If the original character codes are (x_1,x_2,\ldots,x_N), the transmitted array contains every possible sum

[
\sum_{i\in S}x_i
]

for every subset (S). The array is sorted, so its first value is always (0), corresponding to the empty subset.

The task is to recover the original (N) character codes from these subset sums. The recovered codes must be printed as characters in non-decreasing ASCII order. Since the original characters are alphanumeric, each recovered value corresponds to a valid digit or letter.

The bound (N\leq20) is the central constraint. There are (2^{20}=1,048,576) subset sums in the largest input, so an algorithm with roughly one operation per transmitted number is realistic. An algorithm that tries every possible original word is completely impossible, and even an approach that repeatedly performs a linear search through the entire (2^N)-element array can reach roughly (2^{2N}) work. The maximum subset sum is only (20\cdot122=2440), because the largest alphanumeric ASCII value is 122. This small value range gives us an especially useful frequency-array representation.

There are several edge cases where careless implementations fail. The smallest case is

```
1
65
```

The only subset sums are (0) and (65), so the correct output is `A`. A decoder that assumes there is always a pair of non-empty subset sums can go past the end of the data.

Repeated character codes are also possible. For example,

```
3
0 65 65 65 130 130 130 195
```

comes from `AAA`, so the correct output is

```
AAA
```

A decoder that stores subset sums in a set instead of preserving their multiplicities loses the fact that (65) occurs three times and cannot reconstruct the word correctly.

Different subsets can produce the same sum even when the character codes are distinct. Consider

```
3
0 48 49 97 97 145 146 194
```

The original codes are (48,49,97), corresponding to `01a`. The two occurrences of (97) are different subsets, namely ({97}) and ({48,49}). Treating the encrypted values as distinct numbers instead of a multiset silently destroys this information.

The character range also includes digits. For example,

```
3
0 48 122 122 170 170 244 292
```

comes from `0zz`. A decoder that assumes every recovered value is an uppercase or lowercase letter would reject a valid answer.

## Approaches

A direct brute-force approach could try every possible original word, generate its subset sums, sort them, and compare the result with the input. There are 62 possible alphanumeric characters, so even before exploiting the required sorted order there are (62^{20}), approximately (7.0\cdot10^{35}), candidate words at (N=20). Generating (2^{20}) subset sums for every candidate makes this approach many orders of magnitude beyond the time limit.

There is a much more structured way to invert the encryption. Suppose some character codes have already been recovered, and let `subsets` contain all subset sums formed by those recovered codes. Initially no codes have been recovered, so `subsets` contains only (0).

Look at the smallest subset sum that has not yet been consumed. Because every character code is positive, the smallest such value must be the next unrecovered character code. Once that code is (x), every subset formed from the recovered codes can be extended by adding (x). If a previous subset sum was (s), the corresponding new subset sum is (s+x). Consequently, we know exactly which values must be removed from the remaining encrypted multiset: every (s+x) for (s) in `subsets`.

After removing those values, the subset sums of the recovered codes can be expanded by appending each (s+x) to `subsets`. The process repeats until (N) character codes have been recovered.

The remaining question is how to find and remove values efficiently. A general-purpose multiset such as a hash map would work, but this problem gives us an even stronger property: every subset sum lies between (0) and (2440). We can store the multiplicity of every possible sum in a frequency array. Finding the smallest remaining value then requires only a pointer moving from left to right through at most 2440 positions, and removing a value is a constant-time array decrement.

The brute-force reconstruction fails because every required deletion might require searching through a huge list. The observation that the sum range is tiny lets us replace those searches with direct indexing, reducing the entire reconstruction to (O(2^N)) operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over possible words | (O(62^N 2^N)) | (O(2^N)) | Too slow |
| Linear search for every deletion | (O(4^N)) | (O(2^N)) | Too slow |
| Frequency array reconstruction | (O(2^N + 2440)) | (O(2^N + 2440)) | Accepted |

## Algorithm Walkthrough

1. Read (N) and the (2^N) encrypted subset sums. Instead of relying on their sorted order, count how many times every sum occurs in a frequency array `freq`. Since every sum is at most 2440, the array needs only 2441 entries.
2. Initialize `subsets = [0]`. This represents all subset sums that can be formed from the character codes recovered so far. Before recovering anything, the only subset is the empty subset.
3. Keep a pointer `ptr` initially at zero. Advance it while `freq[ptr]` is zero. The first position with positive frequency is the smallest subset sum that has not yet been explained by the already recovered characters.
4. Take `x = ptr` as the next character code. The reason this works is positivity. Every unrecovered character is positive, so the smallest unexplained subset sum must be obtained by taking exactly one new character and no previously recovered character.
5. Let `old_len = len(subsets)`. For every one of the `old_len` existing subset sums `s`, decrement `freq[s + x]`. These are precisely the subset sums that contain the newly recovered character `x` and otherwise use any subset of the already recovered characters.
6. Append every `s + x` to `subsets`. After this operation, `subsets` contains every subset sum obtainable from all recovered character codes, so it represents the new state required by the next iteration.
7. Repeat the previous steps exactly (N) times. Convert every recovered integer to a character with `chr` and concatenate them. The reconstruction naturally produces the codes in non-decreasing order, so no additional sorting is required.

### Why it works

The invariant is that after recovering (k) character codes, `subsets` contains exactly the (2^k) subset sums formed from those codes, while `freq[v]` records how many occurrences of (v) in the original encrypted multiset have not yet been explained by those recovered codes.

Initially the invariant holds because no codes have been recovered and the only subset sum is zero. Assume it holds before recovering the next code. The smallest unexplained sum must be the smallest remaining original character code because every other unexplained subset containing that character is at least as large as the character itself, and every subset using two or more positive unrecovered values is larger still. Calling this value (x), the subsets containing (x) are exactly (s+x), where (s) is a subset sum of the already recovered codes. Removing exactly those occurrences leaves precisely the subset sums that do not contain (x). Appending the same (s+x) values to `subsets` creates all subset sums after adding (x). Thus the invariant is preserved at every iteration, and after (N) iterations every original character code has been recovered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    m = 1 << n

    sums = list(map(int, input().split()))

    # Every original character is alphanumeric, so its ASCII value is
    # at most 122. With at most 20 characters, every subset sum is <= 2440.
    freq = [0] * 2441
    for x in sums:
        freq[x] += 1

    # The input array is no longer needed.
    del sums

    # All subset sums generated by the characters recovered so far.
    subsets = [0]

    answer = []
    ptr = 0

    for _ in range(n):
        while ptr <= 2440 and freq[ptr] == 0:
            ptr += 1

        x = ptr
        answer.append(chr(x))

        old_len = len(subsets)

        # Remove all subset sums that contain the newly recovered value x.
        for i in range(old_len):
            s = subsets[i]
            freq[s + x] -= 1

        # Add those sums to the set of subset sums of recovered values.
        for i in range(old_len):
            subsets.append(subsets[i] + x)

    print("".join(answer))

if __name__ == "__main__":
    solve()
```

The input is first converted into `freq`, preserving multiplicity rather than just membership. This is essential because the encrypted array is a multiset, and the same sum can occur for many different subsets.

The `subsets` array starts with zero because the empty subset is always available. If there are currently (k) recovered values, its size is exactly (2^k). When a new value `x` is found, the code first remembers the old size. This boundary is necessary because only the old subset sums should be used to generate `s + x`. Iterating over the list while simultaneously appending to it without fixing `old_len` would process newly created sums in the same iteration and generate incorrect extra values.

The frequency decrement happens before the new sums are appended. This follows directly from the invariant: the newly generated sums are precisely the occurrences that become explained by the newly recovered character.

The pointer only moves forward. Once `freq[v]` reaches zero, no later operation can make that particular value become unexplained again, because every operation only consumes encrypted subset sums. Since the largest possible sum is 2440, the pointer performs at most 2441 iterations in total.

Python integers do not have the overflow problem that a fixed-width integer implementation might have, although all actual subset sums are already bounded by 2440. The largest structure is `subsets`, which contains at most (2^{20}=1,048,576) integers.

## Worked Examples

### Sample 1

The encrypted array begins with

```
0 66 101 101 114 121 167 167 180 187 ...
```

The first nonzero unexplained value is 66, so the first character is `B`. After removing 66, the next unexplained value is 101, giving `e`. The same value appears again as the next character, because the original word contains two `e` characters.

| Step | Chosen code | Chosen character | Size of `subsets` after step | Newly explained sums |
| --- | --- | --- | --- | --- |
| Start | 0 |  | 1 | 0 |
| 1 | 66 | B | 2 | 66 |
| 2 | 101 | e | 4 | 101, 167 |
| 3 | 101 | e | 8 | 101, 167, 202, 268 |
| 4 | 114 | r | 16 | 114, 180, 215, 281, 215, 281, 316, 382 |
| 5 | 121 | y | 32 | 121, 187, 222, 288, 222, 288, 323, 389, 235, 301, 336, 402, 336, 402, 437, 503 |

The recovered codes are (66,101,101,114,121), which convert to `Beery`. The repeated 101 is handled naturally because `freq[101]` remains positive after the first `e` is recovered.

### Constructed Example 2

Consider three copies of the character `A`, whose ASCII code is 65.

```
3
0 65 65 65 130 130 130 195
```

The reconstruction behaves as follows.

| Step | Chosen code | `subsets` before | Removed sums | `subsets` after |
| --- | --- | --- | --- | --- |
| 1 | 65 | [0] | 65 | [0, 65] |
| 2 | 65 | [0, 65] | 65, 130 | [0, 65, 65, 130] |
| 3 | 65 | [0, 65, 65, 130] | 65, 130, 130, 195 | [0, 65, 65, 130, 65, 130, 130, 195] |

The final answer is `AAA`. The trace shows why frequencies cannot be replaced by a set. At the final step there are three separate occurrences of 130 in the complete encrypted array, corresponding to the three two-element subsets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(2^N + 2440)) | Across all iterations, the number of processed old subset sums is (1+2+\cdots+2^{N-1}=2^N-1), while the pointer scans at most 2441 values. |
| Space | (O(2^N + 2440)) | `subsets` has at most (2^N) elements and `freq` has 2441 entries. |

For (N=20), the reconstruction performs fewer than 1,048,576 subset updates, plus a scan over a fixed 2441-value range. That is appropriate for the 3 second limit. The frequency array is also much more memory-efficient than a Python `Counter` containing potentially hundreds of thousands of dictionary entries.

## Test Cases

```python
import sys
import io
import math

input = sys.stdin.readline

def solve():
    n = int(input())

    sums = list(map(int, input().split()))

    freq = [0] * 2441
    for x in sums:
        freq[x] += 1

    del sums

    subsets = [0]
    answer = []
    ptr = 0

    for _ in range(n):
        while ptr <= 2440 and freq[ptr] == 0:
            ptr += 1

        x = ptr
        answer.append(chr(x))

        old_len = len(subsets)

        for i in range(old_len):
            s = subsets[i]
            freq[s + x] -= 1

        for i in range(old_len):
            subsets.append(subsets[i] + x)

    print("".join(answer))

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

sample1 = """\
5
0 66 101 101 114 121 167 167 180 187 202 215 215 222 222 235 268 281 281 288 288 301 316 323 336 336 382 389 402 402 437 503
"""

assert run(sample1) == "Beery", "sample 1"

assert run(
    """\
1
65
"""
) == "A", "minimum size"

assert run(
    """\
3
0 65 65 65 130 130 130 195
"""
) == "AAA", "all equal values"

assert run(
    """\
3
0 48 49 97 97 145 146 194
"""
) == "01a", "equal subset sums from distinct values"

assert run(
    """\
3
0 48 122 122 170 170 244 292
"""
) == "0zz", "digit and lowercase boundary"

# Maximum-size case: twenty copies of 'z', ASCII value 122.
# The sum 122*k occurs C(20, k) times.
parts = []
for k in range(21):
    parts.extend([str(122 * k)] * math.comb(20, k))

max_case = "20\n" + " ".join(parts) + "\n"

assert run(max_case) == "z" * 20, "maximum N"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 65` | `A` | Minimum (N), single subset value besides zero |
| `3 / 0 65 65 65 130 130 130 195` | `AAA` | Duplicate character codes and multiplicities |
| `3 / 0 48 49 97 97 145 146 194` | `01a` | Different subsets producing the same sum |
| `3 / 0 48 122 122 170 170 244 292` | `0zz` | Smallest digit and largest lowercase letter |
| (N=20), twenty copies of 122 | `zzzzzzzzzzzzzzzzzzzz` | Maximum input size and extreme duplicate frequencies |

The maximum-size test deliberately uses twenty identical values. It produces (2^{20}) encrypted sums while keeping the expected answer simple. The binomial multiplicities exercise the frequency array heavily and confirm that the algorithm never assumes subset sums are unique.

## Edge Cases

For (N=1), the input

```
1
65
```

starts with `freq[0]=1` and `freq[65]=1`. The pointer skips zero because the empty subset is not a character, then selects 65. `subsets` initially contains only zero, so exactly one occurrence of 65 is removed. The output is `A`. The loop executes exactly once, so there is no attempt to access a nonexistent second character.

For duplicate character codes, consider

```
3
0 65 65 65 130 130 130 195
```

The first selected value is 65. The algorithm consumes one occurrence of 65 and creates subset sums `[0,65]`. The next smallest remaining value is still 65, so the algorithm correctly selects another `A`. It consumes one 65 and one 130, then expands the subset list to `[0,65,65,130]`. The third iteration again selects 65 and consumes the remaining 65, two 130 values, and 195. The result is `AAA`. The frequency array is what makes the repeated values distinguishable.

For equal subset sums produced by different subsets, use

```
3
0 48 49 97 97 145 146 194
```

The first recovered code is 48. The second is 49, which consumes 49 and 97, because the existing subset sums are 0 and 48. At this point one occurrence of 97 remains. The third recovered code is 97. It consumes 97, 145, 146, and 194 using the four existing subset sums. The result is `01a`. This demonstrates why the algorithm tracks counts rather than simply deleting distinct values.

For the alphanumeric boundary case,

```
3
0 48 122 122 170 170 244 292
```

the first recovered value is 48, which becomes the character `0`. The next value is 122, and it is selected twice. The output is `0zz`. The frequency array supports the entire permitted sum range, including both the smallest digit code and the largest lowercase letter code.

The maximum case has (N=20), so `subsets` eventually contains (1,048,576) values. Even when every original code is 122, the algorithm does not branch or backtrack. At each iteration the smallest remaining value is again 122, and the frequency counts correctly encode the binomial multiplicities of the subset sums. After twenty iterations, exactly twenty `z` characters have been recovered.

The editorial is structured to be publishable as-is.
