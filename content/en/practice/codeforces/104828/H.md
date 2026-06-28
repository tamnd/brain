---
title: "CF 104828H - \u56de\u6587\u4e32\u5206\u5272"
description: "We are given multiple independent strings, and for each one we need to decide whether it can be decomposed into a sequence of substrings where every piece is a palindrome."
date: "2026-06-28T12:28:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104828
codeforces_index: "H"
codeforces_contest_name: "The 11-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 104828
solve_time_s: 31
verified: true
draft: false
---

[CF 104828H - \u56de\u6587\u4e32\u5206\u5272](https://codeforces.com/problemset/problem/104828/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple independent strings, and for each one we need to decide whether it can be decomposed into a sequence of substrings where every piece is a palindrome. The cut points are arbitrary, and we are free to choose any number of pieces as long as each piece reads the same forward and backward.

A key constraint is the total length across all test cases, which is large, up to five million characters. This rules out any approach that tries to examine all substrings or all partitions explicitly. Anything quadratic per string will immediately fail because even a single 10^5 length string would already imply about 10^10 operations in the worst case for naive partition checking.

The output is simply a binary decision per string, so we are not asked to construct the partition, only to determine whether at least one valid partition exists.

A subtle edge case appears when thinking about very short strings. A single character is always valid because it is a palindrome itself. Two-character strings are also always valid because either both characters are equal, making the whole string a palindrome, or we can split it into two single-character palindromes. This already suggests that the answer might always be affirmative, but that must be justified carefully rather than assumed.

Another potential pitfall is trying to greedily take the longest palindromic prefix at each step. That approach can fail in problems where local optimal choices block future valid partitions, so any correct reasoning must avoid relying on greedy structure unless it is proven unnecessary.

## Approaches

The brute-force viewpoint is to consider all ways of cutting the string into segments and checking whether each segment is a palindrome. If a string has length n, there are 2^(n-1) ways to place cuts. Even if palindrome checking for a segment is O(1) amortized with preprocessing, enumerating partitions is still exponential. For n = 50, this is already infeasible, and here n can reach 10^6.

A more structured way to think about the problem is to ask what constraints actually exist on a valid decomposition. Every single character is a palindrome by definition. This immediately implies that any string can be decomposed into n single-character palindromes. Since the problem allows n ≥ 1 with no restriction on minimal segment length, the trivial partition always exists.

This observation removes the need for any algorithmic processing of the string content. There is no requirement that segments be maximal, disjoint in any special way, or fewer than n pieces. The condition is satisfied as long as we can partition into valid palindromes, and the singleton partition always works.

Thus, every string is automatically a “good” string under the given definition. The entire problem reduces to printing “Yes” for every test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Partitioning | O(2^n) | O(n) | Too slow |
| Observed Trivial Decomposition | O(1) per string | O(1) | Accepted |

## Algorithm Walkthrough

1. For each input string, read it and ignore its contents for decision purposes. The structure of the string does not influence the answer because every character forms a valid palindrome on its own.
2. Immediately output “Yes” for the string. This corresponds to choosing the partition where every character is its own segment.
3. Repeat this for all test cases.

### Why it works

The correctness rests on the existence of a universal decomposition strategy. For any string S = s1 s2 ... sn, we can define Ti = si for each i. Each Ti is a single character and therefore a palindrome. Concatenating all Ti reconstructs S exactly. Since the definition of a valid string only requires the existence of at least one such decomposition, every input string satisfies the condition. No counterexample can exist because the construction does not depend on any property of the characters.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        s = input().strip()
        out.append("Yes")
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads each string and deliberately avoids any analysis beyond consuming input. The only subtle implementation detail is using fast buffered output, since printing one line per test case up to one million times requires efficient aggregation.

There are no boundary checks needed on string content or length beyond stripping the newline.

## Worked Examples

Consider the input:

```
2
sosos
hahaha
```

We process each string independently.

For the first string “sosos”, we immediately output “Yes”. The implicit partition is ["s","o","s","o","s"], each of which is a palindrome.

| Step | String | Action | Output |
| --- | --- | --- | --- |
| 1 | sosos | accept trivial decomposition | Yes |

For the second string “hahaha”, we again output “Yes”. One valid decomposition is ["h","a","h","a","h","a"], and another valid decomposition could be ["hah","aha"].

| Step | String | Action | Output |
| --- | --- | --- | --- |
| 1 | hahaha | accept trivial decomposition | Yes |

These examples confirm that even when longer palindromic segments exist, the correctness does not depend on finding them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(∑n) | Each character is read once and ignored |
| Space | O(1) | Only output buffer is used |

The algorithm scales linearly with input size, which is optimal since reading the input itself already requires Ω(∑n) time. The memory usage stays constant aside from the output buffer.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        s = input().strip()
        res.append("Yes")
    return "\n".join(res)

# provided samples
assert run("2\nsosos\nhahaha\n") == "Yes\nYes"

# single character strings
assert run("3\na\nb\nc\n") == "Yes\nYes\nYes"

# mixed lengths
assert run("2\nab\naba\n") == "Yes\nYes"

# large repeated pattern
assert run("1\n" + "a"*1000 + "\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single characters | Yes lines | minimal valid decomposition |
| mixed short strings | all Yes | correctness regardless of palindromicity |
| long uniform string | Yes | stress on input size handling |

## Edge Cases

A minimal input like `"a"` confirms the base case. The algorithm reads one string and outputs “Yes”, corresponding to the single-piece decomposition.

For `"ab"`, a naive approach might incorrectly try to find a nontrivial palindrome partition and fail. The correct reasoning instead uses ["a","b"], both valid palindromes, so the algorithm outputs “Yes”.

For a long non-palindromic string such as `"abcde"`, there is no need to search for symmetric structure. The decomposition into five single-c
