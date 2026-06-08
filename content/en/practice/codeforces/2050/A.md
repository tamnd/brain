---
title: "CF 2050A - Line Breaks"
description: "We are given a list of words and a fixed-length strip that can hold a certain number of characters. The task is to decide how many words we can consecutively place on this first strip without exceeding its length, while the remaining words go on a second strip that has…"
date: "2026-06-08T08:46:56+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2050
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 991 (Div. 3)"
rating: 800
weight: 2050
solve_time_s: 95
verified: true
draft: false
---

[CF 2050A - Line Breaks](https://codeforces.com/problemset/problem/2050/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of words and a fixed-length strip that can hold a certain number of characters. The task is to decide how many words we can consecutively place on this first strip without exceeding its length, while the remaining words go on a second strip that has effectively unlimited space. Words must be written contiguously, without spaces, and no word can be split between strips. The output is the maximum number of words that fit on the first strip.

Looking at the constraints, we see that each test case has at most 50 words, each up to 10 characters long, and the strip can hold up to 500 characters. This is small enough to consider a simple iterative solution where we sum word lengths one by one, since even in the worst case, we would do at most 50 additions per test case and there are at most 1000 test cases. So a straightforward solution will be fast enough.

Edge cases to consider include scenarios where the first word itself is longer than the strip, meaning zero words can fit. Another subtle case is when the sum of the lengths of all words is exactly equal to the strip length. A careless implementation might stop before adding the last word, producing an off-by-one error.

## Approaches

The brute-force approach iterates over the words, keeping a running sum of their lengths. For each word, we check if adding it would exceed the strip length. If it does, we stop and return the count of words added so far. This approach is correct because it respects the order of words and stops exactly when we cannot fit the next word. Its complexity is O(n) per test case, or at most 50 operations, which is acceptable for our constraints.

The optimal approach is effectively the same in this case because the problem is small and there is no faster method needed. The key insight is recognizing that we only need a single pass over the words with a running total. There is no need for dynamic programming or binary search because the problem size is small, and the sum calculation is straightforward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per test case | O(1) | Accepted |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and `m`, representing the number of words and the strip length.
3. Initialize `current_length` to 0 and `count` to 0.
4. Iterate over each word in the list:

1. Measure the word's length.
2. Check if adding this length to `current_length` exceeds `m`.
3. If it does not, add the length to `current_length` and increment `count`.
4. If it does, break the loop, as no further words can be added.
5. After iterating over the words, `count` contains the maximum number of words that fit.
6. Print the result for this test case.

Why it works: The running total guarantees we never exceed the strip length. Because we check each word in order, we ensure that all selected words are consecutive from the start. The invariant is that `current_length` always equals the sum of lengths of the words currently counted, and it never exceeds `m`.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    words = [input().strip() for _ in range(n)]
    current_length = 0
    count = 0
    for word in words:
        length = len(word)
        if current_length + length <= m:
            current_length += length
            count += 1
        else:
            break
    print(count)
```

The code first reads the number of test cases. For each test case, it reads the number of words and the strip length, then the words themselves. We maintain a running sum of word lengths and a counter. The condition `current_length + length <= m` ensures that we do not exceed the strip length. The loop breaks as soon as a word would overflow the strip, guaranteeing correctness and avoiding off-by-one errors. Using `input().strip()` removes newline characters from words.

## Worked Examples

**Sample Input 1:**

```
3 1
a
b
c
```

| Word | Current Length | Count | Action |
| --- | --- | --- | --- |
| a | 0 + 1 = 1 | 1 | fits, continue |
| b | 1 + 1 = 2 | - | exceeds 1, stop |

Output: `1`

The first word fits, but adding the second exceeds the strip length, so only one word is counted.

**Sample Input 2:**

```
2 9
alpha
beta
```

| Word | Current Length | Count | Action |
| --- | --- | --- | --- |
| alpha | 0 + 5 = 5 | 1 | fits, continue |
| beta | 5 + 4 = 9 | 2 | fits exactly, continue |

Output: `2`

All words exactly fit the strip, demonstrating the edge case where total length equals `m`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * t) | Each test case iterates over all `n` words, t test cases in total |
| Space | O(n) | Storing words for each test case |

Given the constraints (n ≤ 50, t ≤ 1000), the solution performs at most 50,000 operations, well within 1-second time limit. Memory usage is minimal, comfortably under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        words = [input().strip() for _ in range(n)]
        current_length = 0
        count = 0
        for word in words:
            length = len(word)
            if current_length + length <= m:
                current_length += length
                count += 1
            else:
                break
        print(count)
    return output.getvalue().strip()

# Provided samples
assert run("5\n3 1\na\nb\nc\n2 9\nalpha\nbeta\n4 12\nhello\nworld\nand\ncodeforces\n3 2\nab\nc\nd\n3 2\nabc\nab\na\n") == "1\n2\n2\n1\n0", "sample 1"

# Custom cases
assert run("1\n1 1\na\n") == "1", "single word fits"
assert run("1\n1 1\nab\n") == "0", "single word too long"
assert run("1\n3 5\na\nb\nc\n") == "3", "all words fit"
assert run("1\n3 2\na\nb\nc\n") == "2", "exact fit before last word"
assert run("1\n2 5\nabc\nde\n") == "2", "sum equals m"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 word fits | 1 | Minimum input where the word fits |
| 1 word too long | 0 | Minimum input where the word cannot fit |
| Multiple small words | 3 | All words fit easily |
| Multiple words, last too big | 2 | Check stopping at last word |
| Sum equals strip | 2 | Exact fit edge case |

## Edge Cases

If the first word itself exceeds `m`, the algorithm returns `0`. For example, input `1 2\nabc` produces `0` because `len("abc") = 3 > 2`. If multiple words sum exactly to `m`, all are counted correctly. The running sum ensures we never exceed `m`, and the break statement prevents any overcount. The algorithm handles single-word and empty strips gracefully.
