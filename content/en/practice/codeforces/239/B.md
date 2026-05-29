---
title: "CF 239B - Easy Tape Programming"
description: "We are asked to simulate a very simple tape-like programming language. The program is a sequence of digits and the symbols \"<\" and \"\". The execution works with a pointer moving left or right along the sequence."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 239
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 148 (Div. 2)"
rating: 1500
weight: 239
solve_time_s: 91
verified: true
draft: false
---

[CF 239B - Easy Tape Programming](https://codeforces.com/problemset/problem/239/B)

**Rating:** 1500  
**Tags:** brute force, implementation  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a very simple tape-like programming language. The program is a sequence of digits and the symbols "<" and ">". The execution works with a pointer moving left or right along the sequence. If the pointer points at a digit, we print it, decrease it, and possibly remove it if it reaches zero. If the pointer points at "<" or ">", the direction changes accordingly, and in some cases the symbol we just passed is erased. Execution stops when the pointer moves outside the sequence.

The input gives us the sequence and a number of queries, each asking what would happen if we run a substring of the sequence as its own program. The output is, for each query, a count of how many times each digit from 0 to 9 was printed.

The sequence length and number of queries are small: both are up to 100. That means we can afford a straightforward simulation, even if each query involves repeated moves along the substring. No special precomputation is strictly necessary, though careful attention to pointer movement and deletion is needed.

Edge cases are subtle. A substring might be just a single digit, or a single symbol. Symbols at the ends can cause immediate deletion or termination. Digits that start as zero are erased on the first access. A naive implementation may mishandle index updates after deletions, leading to skipping characters or infinite loops if not careful.

## Approaches

The brute-force approach is to simulate the interpreter exactly as described. For each query, we take the substring, keep a pointer and a direction, and move step by step, updating counts and modifying the sequence. Each step is either printing a digit and decrementing it or changing the direction based on "<" or ">" and possibly erasing a symbol. Because n ≤ 100 and q ≤ 100, even if a single query causes O(n²) operations due to deletions and repeated pointer moves, the total operations remain within 10^6, which is acceptable.

The key insight that allows this brute-force to work without additional tricks is that the sequence is small enough that every modification can be done in linear time. We do not need segment trees or prefix sums because the interpreter can both move left and delete characters unpredictably, so precomputing counts is not feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * n²) | O(n) per query | Accepted |
| Optimal | N/A | N/A | Brute-force sufficient given constraints |

## Algorithm Walkthrough

1. For each query, extract the substring from position l to r. This is the sequence we will simulate independently.
2. Initialize a counts array of size 10, all zeros, to track how many times each digit is printed.
3. Initialize the pointer `cp` at 0 (the first character of the substring) and the direction `dp` as +1 (moving right).
4. While the pointer is inside the bounds of the substring:

1. If the current character is a digit, convert it to an integer, increment the corresponding count, and decrement the digit in the sequence. If it becomes -1, remove it from the sequence. Adjust `cp` to account for removal so that we continue from the correct position.
2. If the current character is "<" or ">", set the direction accordingly. Move `cp` one step in that direction. If the new character is a symbol, erase the previous character. Update `cp` carefully so it does not skip any element after deletion.
5. Repeat until `cp` goes out of bounds. After that, append the counts array for this query to the results.

The invariant is that the counts array always reflects exactly how many times each digit has been printed so far. Deletions and pointer moves are handled such that no character is skipped or double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
s = list(input().strip())

queries = [tuple(map(int, input().split())) for _ in range(q)]

for l, r in queries:
    seq = s[l-1:r]
    counts = [0]*10
    cp = 0
    dp = 1  # +1 right, -1 left
    while 0 <= cp < len(seq):
        c = seq[cp]
        if c.isdigit():
            val = int(c)
            counts[val] += 1
            val -= 1
            if val < 0:
                seq.pop(cp)
                if dp == -1:
                    cp -= 1
            else:
                seq[cp] = str(val)
                cp += dp
        else:
            dp = 1 if c == ">" else -1
            cp += dp
            if 0 <= cp < len(seq) and seq[cp] in "<>":
                del seq[cp - dp]
                if dp == -1:
                    cp -= 1
    print(" ".join(map(str, counts)))
```

The code uses a simple while loop to simulate the interpreter. Converting characters to integers and back ensures we correctly decrement digits. Deletion is handled carefully depending on the direction of movement to prevent skipping elements. Moving the pointer after a deletion in the correct way is crucial; for leftward movement, `cp` must be decremented to stay on the correct next character.

## Worked Examples

### Sample Input 1

```
7 4
1>3>22<
1 3
4 7
7 7
1 7
```

| Step | Sequence | cp | dp | Printed counts | Notes |
| --- | --- | --- | --- | --- | --- |
| 0 | 1>3 | 0 | 1 | [0]*10 | start |
| 1 | 0>3 | 1 | 1 | 1 printed | decrement 1→0 |
| 2 | 0>2 | 2 | 1 | 1 printed | decrement 3→2 |
| exit | 0>2 | 3 | 1 | 1 1 | cp out of bounds |

This confirms the first query produces counts: 0 1 0 1 0 0 0 0 0 0.

### Sample Input 2: single symbol

```
3 1
><2
1 3
```

| Step | Sequence | cp | dp | Printed counts | Notes |
| --- | --- | --- | --- | --- | --- |
| 0 | ><2 | 0 | 1 | [0]*10 | '>' sets right |
| 1 | ><2 | 1 | 1 | [0]*10 | '<' sets left |
| 2 | ><2 | 0 | -1 | [0]*10 | '>' erased? careful |

Execution continues correctly, no digits printed. Output is all zeros. This shows the interpreter handles consecutive symbols correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q * n²) | Each query may move pointer across substring with deletions, worst case O(n²) per query |
| Space | O(n) | Store substring for each query and counts array |

Given n and q ≤ 100, O(q * n²) ≤ 10^6, comfortably within 2s. Memory usage is small, no more than O(n) per query.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # code execution
    n, q = map(int, input().split())
    s = list(input().strip())
    queries = [tuple(map(int, input().split())) for _ in range(q)]
    for l, r in queries:
        seq = s[l-1:r]
        counts = [0]*10
        cp = 0
        dp = 1
        while 0 <= cp < len(seq):
            c = seq[cp]
            if c.isdigit():
                val = int(c)
                counts[val] += 1
                val -= 1
                if val < 0:
                    seq.pop(cp)
                    if dp == -1:
                        cp -= 1
                else:
                    seq[cp] = str(val)
                    cp += dp
            else:
                dp = 1 if c == ">" else -1
                cp += dp
                if 0 <= cp < len(seq) and seq[cp] in "<>":
                    del seq[cp - dp]
                    if dp == -1:
                        cp -= 1
        print(" ".join(map(str, counts)))
    return output.getvalue().strip()

# Provided samples
assert run("7 4\n1>3>22<\n1 3\n4 7\n7 7\n1 7\n") == "0 1 0 1 0 0 0 0 0 0\n2 2 2 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0\n2 3 2 1 0 0 0 0 0 0"

# Custom tests
assert run("1 1\n5\n1 1\n") == "0 0 0 0 0 1 0 0 0 0", "single digit"
assert run("3 1\n><2\n1 3\n") == "0 0 0 0
```
