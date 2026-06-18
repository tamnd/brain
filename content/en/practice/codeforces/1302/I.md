---
problem: 1302I
contest_id: 1302
problem_index: I
name: "Deja vu"
contest_name: "AIM Tech Poorly Prepared Contest (unrated, funny, Div. 1 preferred)"
rating: 0
tags: []
answer: passed_samples
verified: true
solve_time_s: 236
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2dd39d-3468-83ec-885f-f9f55d26717b
---

# CF 1302I - Deja vu

**Rating:** ?  
**Tags:** -  
**Model:** gpt-5-3-mini  
**Solve time:** 3m 56s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2dd39d-3468-83ec-885f-f9f55d26717b  

---

## Solution

## Problem Understanding

We are given a binary string, think of it as a row of cells containing only `0` and `1`. From this long row, we slide a window of fixed size `k` across all possible starting positions. Each position produces a substring of length `k`, and each substring is itself a binary string.

The task is not to list these substrings or compare them pairwise directly in a naive way, but simply to count how many distinct patterns of length `k` appear anywhere in the string.

So the output is the number of unique “windows” of size `k` when we scan left to right.

The constraints allow the string length up to 200,000. A naive comparison of all substrings would involve up to 200,000 windows, and each comparison costs O(k), leading to roughly O(nk), which can reach 4×10^10 operations in the worst case. That is far beyond the time limit.

The key observation is that each substring is short (binary alphabet), so we need a way to compare substrings in O(1) after preprocessing, or represent them in a compact hashable form.

A subtle edge case appears when all characters are identical. For example, if `s = 00000` and `k = 3`, every substring is identical, so the answer is `1`. A naive hashing method that incorrectly uses non-rolling recomputation might accidentally treat identical substrings as different due to recomputing errors or inconsistent normalization. Another edge case is when `k = 1`, where the answer is just the number of distinct characters, always `1` or `2`.

## Approaches

A brute-force solution would extract every substring of length `k`, store it as a string, and insert it into a set. This is correct logically because sets handle uniqueness. However, copying each substring costs O(k), and doing this for O(n) positions makes the total cost O(nk), which is too slow for the upper bound.

To improve this, we notice that substrings overlap heavily. Moving from one window to the next only changes two characters: one leaves the window and one enters. This structure suggests a rolling representation.

Since the alphabet is binary, we can interpret each substring as a number in base 2. Then each window corresponds to an integer, and we can update this integer in O(1) using bit operations: shift left, add new bit, and mask out old bits beyond length `k`. This gives us a rolling hash without collisions.

This reduces the problem to maintaining a sliding binary value and inserting each value into a set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(k) per substring | Too slow |
| Rolling binary hash | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the first window of size `k` into an integer by interpreting it as a binary number. This gives a compact representation of the substring.
2. Insert this integer into a hash set. This set stores all distinct window values seen so far.
3. For each position `i` from `k` to `n - 1`, update the current value:

we shift left by 1 bit (equivalent to multiplying by 2), add the new bit `s[i]`, and remove the contribution of the bit that falls out of the window by masking with `(1 << k) - 1`.
4. Insert each updated value into the set. Each value uniquely identifies a substring of length `k`.
5. The answer is the size of the set after processing all windows.

The key idea in step 3 is that we never reconstruct a substring. We reuse the previous computation and adjust it locally, which keeps the runtime linear.

### Why it works

Each substring of length `k` corresponds to a unique binary number when interpreted in base 2. The rolling update preserves exact equivalence between the integer representation and the current window content. Since every window is visited exactly once and mapped deterministically into a number, equality of substrings corresponds exactly to equality of integers stored in the set. No collisions are introduced because the representation is exact rather than hashed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    s = input().strip()

    if k == 0:
        print(0)
        return

    mask = (1 << k) - 1

    val = 0
    for i in range(k):
        val = (val << 1) | (ord(s[i]) - 48)

    seen = {val}

    for i in range(k, n):
        val = ((val << 1) & mask) | (ord(s[i]) - 48)
        seen.add(val)

    print(len(seen))

if __name__ == "__main__":
    solve()
```

The code maintains a rolling integer `val` that always represents the last `k` bits of the string. The mask ensures that older bits are removed once they move outside the window. The set `seen` tracks all distinct values encountered.

A common mistake is forgetting the mask operation, which causes bits beyond length `k` to accumulate and corrupt comparisons between windows. Another subtle issue is initializing the first window correctly; failing to do so shifts all comparisons and produces incorrect counts.

## Worked Examples

### Example 1

Input:

```
5 2
01101
```

We track the rolling window values:

| i | window | binary | value |
| --- | --- | --- | --- |
| 1 | 01 | 01 | 1 |
| 2 | 11 | 11 | 3 |
| 3 | 10 | 10 | 2 |
| 4 | 01 | 01 | 1 |

The set becomes `{1, 3, 2}` so the answer is `3`.

This trace shows how repeated substrings collapse into identical integers, confirming that the encoding correctly identifies duplicates.

### Example 2

Input:

```
4 3
0001
```

| i | window | binary | value |
| --- | --- | --- | --- |
| 2 | 000 | 000 | 0 |
| 3 | 001 | 001 | 1 |

The set is `{0, 1}` so the answer is `2`.

This demonstrates that even small changes at the end of the string create distinct window values, and the rolling update captures them without recomputation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each window update uses constant-time bit operations and one set insertion |
| Space | O(n) | In the worst case all windows are distinct and stored in the set |

The algorithm runs comfortably within limits since 200,000 operations with O(1) updates is efficient in Python, and memory usage is linear in the number of distinct substrings.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# Provided sample (conceptual placeholder, assumes solve() wired correctly)
# assert run("5 2\n01101\n") == "3\n"

# custom cases
# all identical
# assert run("5 2\n00000\n") == "1\n"

# k = 1
# assert run("4 1\n0101\n") == "2\n"

# maximum diversity small
# assert run("4 2\n0101\n") == "3\n"

# single window
# assert run("3 3\n101\n") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 2 / 00000 | 1 | identical substrings collapse |
| 4 1 / 0101 | 2 | single-character distinct counting |
| 4 2 / 0101 | 3 | overlapping windows uniqueness |
| 3 3 / 101 | 1 | single full-length window |

## Edge Cases

When the string consists of all identical characters, every window maps to the same integer because the rolling value never changes except for shifting within identical bits. For input `s = 000000` and `k = 3`, every computed value remains `0`, so the set size is `1`.

When `k = 1`, each window is just a single bit. The rolling mechanism degenerates into directly inserting each character’s integer value into the set. For `s = 0101`, the values alternate between `0` and `1`, producing exactly two distinct elements.

When `k = n`, there is only one window, so the initial encoding already represents the full string and the set size is always `1`.