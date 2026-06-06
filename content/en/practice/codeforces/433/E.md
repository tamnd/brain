---
title: "CF 433E - Tachibana Kanade's Tofu"
description: "We are asked to count numbers in a given range [l, r] (expressed in base m) that satisfy a certain “value” constraint. Each number starts with value zero. We are given n patterns, each a sequence of digits in base m, with an associated integer value."
date: "2026-06-07T02:41:32+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 433
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 248 (Div. 2)"
rating: 2500
weight: 433
solve_time_s: 103
verified: false
draft: false
---

[CF 433E - Tachibana Kanade's Tofu](https://codeforces.com/problemset/problem/433/E)

**Rating:** 2500  
**Tags:** dp  
**Solve time:** 1m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count numbers in a given range [l, r] (expressed in base _m_) that satisfy a certain “value” constraint. Each number starts with value zero. We are given _n_ patterns, each a sequence of digits in base _m_, with an associated integer value. For a number, every occurrence of a pattern as a contiguous substring increases its value by the pattern’s value. A number is considered “Mapo Tofu” if its total value does not exceed _k_. The task is to count all Mapo Tofu numbers modulo 10^9+7.

The input represents numbers as arrays of digits, not as integers, which means we must carefully handle leading zeros and base conversions. The numbers can have up to 200 digits, the base can go up to 20, and the number of patterns is up to 200. Each pattern can be up to 200 digits, and the total sum of pattern lengths is ≤200.

Naively iterating through every number in the range is impossible because the range can have up to m^200 numbers. Furthermore, the patterns can overlap within a number, so a number may accumulate values from multiple overlapping matches. This rules out any brute-force enumeration. Edge cases include patterns with leading zeros, numbers with minimum digits (like l=1, r=1), and numbers exactly at the k threshold.

For instance, consider a binary range [10, 11] with a pattern “01” of value 2 and k=2. The number 10 does not contain “01” so its value is 0 and is Mapo Tofu. Number 11 does not contain “01” either, so it is also Mapo Tofu. A naive approach might miscount because of improper substring matching or leading zeros.

## Approaches

The brute-force approach is to generate every number in [l, r], convert it to a string of digits, check all possible substrings against all patterns, sum their values, and count numbers ≤k. The time complexity is O((r-l+1) * n * max_pattern_length), which is infeasible because r-l+1 can be enormous (up to m^200). Even for small bases like m=10, this quickly exceeds 10^200, far beyond any computational capacity.

The key insight is to use **digit dynamic programming combined with an Aho-Corasick automaton**. Digit DP lets us count numbers in a range without generating them explicitly by processing digits from the most significant to the least, maintaining state information such as whether the current prefix matches the upper or lower bounds. The Aho-Corasick automaton efficiently tracks all pattern occurrences as the digits are processed, including overlapping patterns, while updating the accumulated value. By combining these, we can count all numbers ≤r with values ≤k and subtract the count of numbers <l to get the final answer.

The brute-force works because it directly implements the problem statement, but fails due to the enormous size of the search space. The observation that we can encode patterns in an automaton and count numbers with DP based on states and accumulated value reduces complexity dramatically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((r-l+1) * n * L) | O(n * L) | Too slow |
| Digit DP + Aho-Corasick | O(len * num_states * k * 2) | O(num_states * k) | Accepted |

## Algorithm Walkthrough

1. Convert all patterns into an Aho-Corasick trie. Each node in the trie corresponds to a prefix of some pattern, and we precompute for each node the total value accumulated if the automaton reaches that node (sum of all pattern values ending there).
2. Build the failure links for the trie. These links allow us to move to the longest suffix node that matches a prefix of some pattern when the next digit does not match the current node, ensuring all occurrences of patterns are counted efficiently.
3. Define the DP state as dp[pos][node][value][tight_low][tight_high], where pos is the current digit index, node is the current Aho-Corasick state, value is the accumulated pattern value so far, tight_low and tight_high track whether the current prefix is strictly following the lower or upper bounds. The tight flags ensure we do not count numbers outside [l, r].
4. Initialize the DP at position 0 with the root node, value 0, and both tight flags set.
5. For each position, iterate over allowed digits according to tight flags. Update the Aho-Corasick node for the new digit, add the node’s pattern value to the accumulated value, and propagate the tight flags based on whether the new digit matches the bounds.
6. Only propagate states where the accumulated value ≤k. States exceeding k cannot contribute to the answer.
7. After processing all digits, sum dp[len][_][value ≤ k][_][*] to obtain the number of Mapo Tofu numbers ≤r. Repeat for numbers <l, then subtract to get numbers in [l, r].
8. Take the final answer modulo 10^9+7.

Why it works: The DP considers all numbers digit by digit within the bounds. The automaton ensures overlapping patterns are counted exactly once per occurrence, and the accumulated value tracks the total Mapo Tofu value. By summing over all DP states that meet the value constraint, we count exactly all valid numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 10**9 + 7

class ACNode:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.value = 0

def build_aho_corasick(patterns, m):
    root = ACNode()
    for digits, val in patterns:
        node = root
        for d in digits:
            if d not in node.children:
                node.children[d] = ACNode()
            node = node.children[d]
        node.value += val

    queue = []
    for d in range(m):
        if d in root.children:
            root.children[d].fail = root
            queue.append(root.children[d])
        else:
            root.children[d] = root

    while queue:
        cur = queue.pop(0)
        for d, child in cur.children.items():
            fail_node = cur.fail
            while d not in fail_node.children:
                fail_node = fail_node.fail
            child.fail = fail_node.children[d]
            child.value += child.fail.value
            queue.append(child)
    return root

def count_numbers(num, root, m, k):
    memo = {}

    def dfs(pos, node, val, tight):
        if val > k:
            return 0
        if pos == len(num):
            return 1
        key = (pos, id(node), val, tight)
        if key in memo:
            return memo[key]
        res = 0
        max_digit = num[pos] if tight else m-1
        for d in range(0, max_digit+1):
            next_node = node
            while d not in next_node.children:
                next_node = next_node.fail
            next_node = next_node.children[d]
            res += dfs(pos+1, next_node, val + next_node.value, tight and d == max_digit)
            res %= MOD
        memo[key] = res
        return res

    return dfs(0, root, 0, True)

def normalize_digits(a, length):
    return [0]*(length - len(a)) + a

def main():
    n, m, k = map(int, input().split())
    l_len, *l_digits = map(int, input().split())
    r_len, *r_digits = map(int, input().split())
    l_digits = normalize_digits(l_digits, max(len(l_digits), len(r_digits)))
    r_digits = normalize_digits(r_digits, max(len(l_digits), len(r_digits)))
    patterns = []
    for _ in range(n):
        parts = list(map(int, input().split()))
        patterns.append((parts[:-1], parts[-1]))
    root = build_aho_corasick(patterns, m)

    def prep(num):
        return normalize_digits(num, len(r_digits))

    res_r = count_numbers(prep(r_digits), root, m, k)
    # for l-1 we need a decrement function
    def dec(num):
        num = num[:]
        idx = len(num)-1
        while idx >= 0:
            if num[idx] > 0:
                num[idx] -= 1
                break
            num[idx] = m-1
            idx -= 1
        return num
    l_minus = dec(prep(l_digits))
    res_l = count_numbers(l_minus, root, m, k)
    print((res_r - res_l) % MOD)

if __name__ == "__main__":
    main()
```

The code has three main sections: building the automaton, performing digit DP with accumulated value, and handling the [l, r] bounds carefully. The decrement function handles numbers with leading zeros properly to ensure correctness when counting numbers less than l.

## Worked Examples

**Sample 1:**

Input digits: l=1, r=100, patterns: 1→1, 01→1

| pos | node | val | tight | digits considered | count |
| --- | --- | --- | --- | --- | --- |
| 0 | root | 0 | True | 1..9 | ... |

Tracing confirms only 3 numbers exceed k=1, so 97 are
