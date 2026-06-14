---
title: "CF 1582C - Grandma Capa Knits a Scarf"
description: "We are given a string made of lowercase letters. We are allowed to pick exactly one letter of the alphabet, and then delete any occurrences of that chosen letter from the string, possibly none or all of them."
date: "2026-06-14T22:58:57+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "greedy", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1582
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 750 (Div. 2)"
rating: 1200
weight: 1582
solve_time_s: 267
verified: true
draft: false
---

[CF 1582C - Grandma Capa Knits a Scarf](https://codeforces.com/problemset/problem/1582/C)

**Rating:** 1200  
**Tags:** brute force, data structures, greedy, strings, two pointers  
**Solve time:** 4m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made of lowercase letters. We are allowed to pick exactly one letter of the alphabet, and then delete any occurrences of that chosen letter from the string, possibly none or all of them. After these deletions, we want the resulting string to become a palindrome, and we want to minimize how many characters we removed. If no single letter choice can make the string a palindrome, we must report that it is impossible.

A key constraint is that deletions are extremely restricted. We are not allowed to freely remove mismatched characters; we can only delete occurrences of one fixed character. This restriction turns the problem into checking whether the string can be turned into a palindrome by "filtering out" one character type.

The input size reaches up to 100,000 characters per test case with up to 200,000 total characters. This immediately rules out any solution that tries to simulate deletion choices and palindrome checks independently for every letter and every deletion combination. A naive approach that rebuilds strings repeatedly would reach O(n * 26 * n), which is far beyond acceptable limits.

A subtle edge case appears when the string is already a palindrome. In that case, the answer is zero regardless of which letter we choose. Another tricky situation arises when mismatches exist at symmetric positions but cannot all be resolved by removing a single character type. For example, if mismatched pairs require removing two different letters, no valid solution exists even if the string "almost" looks symmetric.

## Approaches

The brute-force idea is straightforward: try each of the 26 possible letters as the chosen deletion character. For each choice, build the resulting string by skipping that letter, then check whether the remaining string is a palindrome. If it is, count how many deletions were performed and keep the minimum.

This works because it directly simulates the allowed operation. However, each palindrome check is O(n), and building filtered strings is also O(n). Since we repeat this for 26 letters, the complexity becomes O(26 · n²) if implemented carelessly with repeated string construction, or O(26 · n) per check leading to O(26 · n²) across all checks in worst implementation patterns. With n up to 10⁵, this is infeasible.

The key observation is that we do not actually need to rebuild strings for every candidate letter. Instead, we can treat the problem as a two-pointer palindrome check with a constraint: when we see a mismatch, we are forced to "fix" it by deleting one of the two letters involved, and that deletion choice must be consistent across all mismatches. This means the only meaningful candidates are the two letters appearing at the first mismatch from the outside. Any valid solution must remove one of those letters entirely from the conflicting pairs, otherwise symmetry cannot be restored.

So we reduce the problem to checking at most two candidate letters derived from the first mismatch, and simulate a constrained palindrome check where we skip occurrences of that letter.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26 · n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We use a two-pointer scan from both ends of the string.

1. Initialize two pointers, left at 0 and right at n − 1. Move them inward as long as characters match. This verifies the prefix-suffix symmetry that already holds.
2. If the pointers cross, the string is already a palindrome, so no deletions are needed.
3. If we find the first mismatch at positions left and right, we have two candidate letters: s[left] and s[right]. Any valid solution must remove all occurrences of one of these two letters to resolve this mismatch.
4. For each candidate letter, simulate a palindrome check where we ignore all occurrences of that letter. We again use two pointers, skipping characters equal to the chosen letter.
5. If after skipping one letter the string becomes a palindrome, we compute the number of removed characters as the total count of that letter in the original string minus the number of occurrences that remain in the valid palindrome formation.
6. Take the minimum result across the two candidates. If neither candidate produces a valid palindrome, return −1.

The reasoning behind restricting candidates to the mismatch pair is that the first position where symmetry fails already forces one side of the mismatch to be entirely eliminated in any valid solution.

### Why it works

The algorithm relies on the fact that a palindrome mismatch at positions l and r cannot be fixed by deleting unrelated characters. Since we can only delete one letter globally, at least one of s[l] or s[r] must be removed from all relevant positions. Once that letter is removed, the rest of the string must already be structurally consistent under two-pointer pairing. This guarantees that any successful configuration must correspond to one of the two candidate deletions, so checking only those is sufficient and complete.

## Python Solution

```python
import sys
input = sys.stdin.readline

def check(s, ch):
    l, r = 0, len(s) - 1
    removed = 0
    while l < r:
        while l < r and s[l] == ch:
            l += 1
            removed += 1
        while l < r and s[r] == ch:
            r -= 1
            removed += 1
        if l >= r:
            break
        if s[l] != s[r]:
            return float('inf')
        l += 1
        r -= 1
    return removed

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()

        l, r = 0, n - 1
        while l < r and s[l] == s[r]:
            l += 1
            r -= 1

        if l >= r:
            print(0)
            continue

        c1, c2 = s[l], s[r]

        ans = min(check(s, c1), check(s, c2))
        print(-1 if ans == float('inf') else ans)

if __name__ == "__main__":
    solve()
```

The solution starts by locating the first mismatch, which identifies the only two relevant characters worth considering. The helper function `check` simulates removing all occurrences of a chosen character while maintaining a palindrome check using two pointers. The `removed` counter tracks how many deletions are needed, and invalid configurations immediately return infinity.

The main logic relies on the fact that once we commit to removing one of the two mismatch characters, the rest of the string must already be consistent under palindrome constraints.

## Worked Examples

Consider the string `abcaacab`.

We first compare from both ends until a mismatch:

| left | right | s[left] | s[right] | action |
| --- | --- | --- | --- | --- |
| 0 | 7 | a | b | mismatch stops |

The candidates are `a` and `b`.

For `a`, removing all `a` characters yields `bcaacb`, which is a palindrome. The number of deletions is 4.

For `b`, removing all `b` characters yields `acaaca`, which is also a palindrome. The deletions required are 2.

The minimum is 2.

Now consider `khyyhhyhky`.

Mismatch occurs at the outermost mismatch that forces candidates `k` and `y`.

Checking `k` removal leads to a consistent palindrome after skipping all `k` characters, while removing `y` requires more deletions but still yields a valid palindrome structure. The algorithm selects the minimum feasible deletion count.

These traces show that the algorithm never explores unnecessary letters, only those that directly resolve the first structural conflict.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One two-pointer scan plus up to two filtered scans per test case |
| Space | O(1) | Only pointers and counters are used |

The total input size across test cases is bounded by 2 × 10⁵, so a linear scan per test case fits comfortably within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    input = sys.stdin.readline

    def check(s, ch):
        l, r = 0, len(s) - 1
        removed = 0
        while l < r:
            while l < r and s[l] == ch:
                l += 1
                removed += 1
            while l < r and s[r] == ch:
                r -= 1
                removed += 1
            if l >= r:
                break
            if s[l] != s[r]:
                return float('inf')
            l += 1
            r -= 1
        return removed

    def solve():
        t = int(input())
        for _ in range(t):
            n = int(input())
            s = input().strip()

            l, r = 0, n - 1
            while l < r and s[l] == s[r]:
                l += 1
                r -= 1

            if l >= r:
                print(0)
                continue

            c1, c2 = s[l], s[r]
            ans = min(check(s, c1), check(s, c2))
            print(-1 if ans == float('inf') else ans)

    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("""5
8
abcaacab
6
xyzxyz
4
abba
8
rprarlap
10
khyyhhyhky""") == """2
-1
0
3
2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single palindrome | 0 | already valid, no deletions needed |
| impossible mismatch | -1 | no single-letter removal can fix structure |
| all same letters | 0 | trivial palindrome |
| alternating pattern | minimal deletion choice | forces correct candidate selection |

## Edge Cases

When the string is already symmetric, the two-pointer scan finishes without encountering a mismatch. The algorithm immediately returns zero, which is correct because no deletions are required and any chosen letter would only increase cost.

When the mismatch occurs at the very ends of the string, such as `ab`, the candidate letters are `a` and `b`. Each removal attempt produces a single-character string, which is trivially a palindrome. The algorithm correctly returns the smaller deletion cost, which is one in both cases.

When multiple mismatches exist deeper in the string, the first mismatch still determines the only viable deletion candidates. Even if later mismatches involve other characters, any valid solution must already resolve the first conflict, so restricting attention to those two letters remains sufficient and the algorithm correctly rejects impossible cases.
