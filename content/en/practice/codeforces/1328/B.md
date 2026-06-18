---
problem: 1328B
contest_id: 1328
problem_index: B
name: "K-th Beautiful String"
contest_name: "Codeforces Round 629 (Div. 3)"
rating: 1300
tags: ["binary search", "brute force", "combinatorics", "implementation", "math"]
answer: passed_samples
verified: false
solve_time_s: 231
date: 2026-06-14
model: gpt-5-5
samples_passed: 0
samples_total: 0
share_url: https://chatgpt.com/share/6a2dfc6a-d998-83ec-acae-ab74293c87ce
---

# CF 1328B - K-th Beautiful String

**Rating:** 1300  
**Tags:** binary search, brute force, combinatorics, implementation, math  
**Model:** gpt-5-5  
**Solve time:** 3m 51s  
**Verified:** no (0/0 samples)  
**Share:** https://chatgpt.com/share/6a2dfc6a-d998-83ec-acae-ab74293c87ce  

---

## Solution

## Problem Understanding

We are looking at all binary strings of length `n` that contain exactly two occurrences of the letter `b`, while every other position is filled with `a`. Since the alphabet is ordered with `a < b`, strings starting with more leading `a`s come earlier in lexicographic order, and placing a `b` earlier pushes a string later.

The task is to imagine all such strings sorted like words in a dictionary and return the one at position `k`.

The input gives multiple queries. Each query provides a length `n` and a rank `k`, and we must directly construct the k-th string without generating all candidates.

The constraints force us into an O(n) per test or better solution in total. Since the sum of all `n` is up to `10^5`, any approach that is quadratic in `n` or enumerates all pairs of `b` positions per test case is infeasible.

A naive attempt would generate all pairs of positions `(i, j)` with `i < j`, build the string, and sort them. That already produces `O(n^2)` strings per test case, and even constructing them explicitly leads to TLE.

A subtler failure case comes from trying to simulate lexicographic ordering greedily without understanding the combinatorial structure. For example, incorrectly assuming the first `b` position is determined independently from the second leads to wrong ranking because the number of completions depends on both choices.

## Approaches

The brute-force view is straightforward: choose two indices for the `b` characters, build the string, and sort all results. This works conceptually because every valid string corresponds uniquely to a pair `(i, j)` with `i < j`. However, the number of such pairs is `n(n-1)/2`, so even listing them becomes quadratic, and sorting them adds another logarithmic factor on top of heavy string construction.

The key observation is that lexicographic order aligns perfectly with the first position of `b`. If we fix the first `b` at position `i`, then the second `b` can be placed anywhere strictly after `i`. All such strings form a contiguous block in lexicographic order.

For a fixed `i`, the number of choices for the second `b` is `n - i`. That means the block size for position `i` is `n - i`. We can scan these blocks in order of increasing `i` and subtract block sizes from `k` until we find the correct first `b` position. After that, the remaining offset directly tells us where the second `b` goes.

This reduces the problem to a single linear scan per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n) | O(n²) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We treat every valid string as determined by two indices `i < j` where both positions contain `b`.

1. We iterate `i` from 1 to `n-1`, treating `i` as the position of the first `b`.
2. For each `i`, we compute how many strings start with `b` at `i`. This equals `n - i` because the second `b` can be at any position after `i`.
3. If `k` is larger than this block size, we subtract it and move to the next `i`. This means the k-th string is not in this block.
4. Once we find an `i` such that `k <= n - i`, we fix the first `b` at `i`.
5. The second `b` is then at position `i + k`. This works because within this block, lexicographic order corresponds exactly to increasing position of the second `b`.
6. We construct the final string with `a` everywhere