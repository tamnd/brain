---
problem: 1278A
contest_id: 1278
problem_index: A
name: "Shuffle Hashing"
contest_name: "Educational Codeforces Round 78 (Rated for Div. 2)"
rating: 1000
tags: ["brute force", "implementation", "strings"]
answer: passed_samples
verified: true
solve_time_s: 178
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2d9d8e-a568-83ec-a4e1-c0bcb751518e
---

# CF 1278A - Shuffle Hashing

**Rating:** 1000  
**Tags:** brute force, implementation, strings  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 58s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2d9d8e-a568-83ec-a4e1-c0bcb751518e  

---

## Solution

## Problem Understanding

We are given a base string that represents a password, and another string that is claimed to be a “hash” of that password. The hash is not a cryptographic hash in the usual sense. Instead, it is constructed by taking all characters of the password, permuting them in any order, and then embedding that permutation somewhere inside a larger string that also contains arbitrary extra lowercase letters before and after.

The question is whether the second string could have been produced in this way. In other words, we are checking if we can find a substring of the hash whose multiset of characters matches exactly the multiset of characters of the password. The rest of the hash outside this chosen substring can be anything.

Each test case is independent, so we repeat this check for multiple pairs of strings.

The constraints are small: both strings have length at most 100 and there are at most 100 test cases. This immediately rules out anything more complex than a few million simple operations in total. Even an O(n³) approach would still be safe, but anything exponential or involving permutations is unnecessary.

A common incorrect approach is to try generating all permutations of the password and searching for them inside the hash. That fails immediately because even a 10-letter password has 10! permutations, which is already far too large.

Another subtle mistake is to only check whether the password appears as a subsequence of the hash. That is incorrect because the password characters must appear contiguously after rearrangement, not scattered. The shuffle only affects order inside the chosen block, not positions across the entire string.

A small example that breaks naive logic:

Input:

```
p = "ab"
h = "axb"
```

Here, `"ab"` does appear as a subsequence, but there is no contiguous substring of length 2 in `h` that has both `'a'` and `'b'` together. So the answer is actually “NO”.

The correct condition depends on matching character counts inside a sliding window.

## Approaches

The brute-force idea is to consider every possible substring of `h`, extract its length equal to `len(p)`, and check whether the substring has the same character frequency as `p`. For each substring, we recompute counts from scratch, which costs O(26) or O(n) per check. Since there are O(n) substrings, this leads to O(n²) checks and O(n) work each time, giving O(n³) in the worst case.

This works easily for n ≤ 100 but is still more than needed.

The key observation is that we only care whether any substring of `h` has exactly the same multiset of characters as `p`. That is a classic fixed-length anagram matching problem. Instead of recomputing frequencies for every substring, we maintain a sliding window of size |p| over `h`, updating character counts in O(1) per step.

We compare the frequency array of the window with that of `p`. Since the alphabet size is constant (26 lowercase letters), comparison is O(26), which is effectively constant.

This reduces the problem to a linear scan over `h`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force substrings + full counting | O(n³) | O(1) | Accepted (but slow) |
| Sliding window frequency comparison | O(26·n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Compute the frequency array of the password string `p`. This array stores how many times each letter `'a'` to `'z'` appears. This is the pattern we must match exactly in some substring of `h`.
2. If `h` is shorter than `p`, we immediately return “NO” because no substring of `h` can contain all characters of `p`.
3. Build a frequency array for the first window of `h` of length equal to `p`. This window represents a candidate substring.
4. Compare the window frequency with the password frequency. If they match, we return “YES” immediately.
5. Slide the window one character at a time across `h`. At each step:

- Remove the contribution of the outgoing character (left side of window).
- Add the incoming character (right side of window).

This keeps the window frequency updated in O(1).
6. After each update, compare the updated window frequency with the password frequency. If at any point they match, we return “YES”.
7. If we finish scanning all windows without a match, we return “NO”.

The reason this procedure is correct is that every possible contiguous segment of `h` of length `|p|` is examined exactly once as a candidate, and every candidate is checked for being a permutation of `p`.

### Why it works

The key invariant is that at every step of the sliding window, the frequency array of the window exactly reflects the character multiset of the current substring of `h` of length `|p|`. Since every possible placement of a length-|p| substring is visited once, we never miss a valid candidate. Conversely, any matching substring must appear as one of these windows, so if none match, no valid construction exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_one(p, h):
    n, m = len(p), len(h)
    if m < n:
        return "NO"
    
    def freq(s):
        f = [0] * 26
        for c in s:
            f[ord(c) - 97] += 1
        return f
    
    fp = freq(p)
    window = freq(h[:n])
    
    if window == fp:
        return "YES"
    
    for i in range(n, m):
        window[ord(h[i]) - 97] += 1
        window[ord(h[i - n]) - 97] -= 1
        if window == fp:
            return "YES"
    
    return "NO"

def main():
    t = int(input())
    out = []
    for _ in range(t):
        p = input().strip()
        h = input().strip()
        out.append(solve_one(p, h))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The solution is structured around a helper that checks a single test case. The frequency arrays are simple fixed-size lists of length 26, which avoids any overhead from dictionaries. The sliding update is done in-place, which ensures constant-time transitions between windows.

A common implementation mistake is forgetting to handle the initial window separately. Another is incorrectly updating the frequency array, especially mixing up the outgoing and incoming indices. Since both operations are symmetric decrements and increments, swapping them silently breaks correctness.

## Worked Examples

### Example 1

Input:

```
p = "ab"
h = "aab"
```

Window size is 2.

| Step | Window | freq(window) | match with p |
| --- | --- | --- | --- |
| init | "aa" | a=2,b=0 | no |
| move | "ab" | a=1,b=1 | yes |

At the second window, the frequency matches the password exactly, so the answer is YES. This demonstrates how the correct substring may appear shifted inside a larger string with extra characters around it.

### Example 2

Input:

```
p = "abc"
h = "abac"
```

Window size is 3.

| Step | Window | freq(window) | match with p |
| --- | --- | --- | --- |
| init | "aba" | a=2,b=1,c=0 | no |
| move | "bac" | a=1,b=1,c=1 | yes |

Here the valid permutation of `"abc"` appears even though the original order is not preserved. This confirms that the algorithm correctly handles arbitrary permutations of the password.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 · | h |
| Space | O(1) | Only fixed-size frequency arrays are used |

Given that both strings are at most length 100 and there are at most 100 test cases, the total number of operations is negligible. Even in the worst case, we perform only a few hundred thousand constant-time updates.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    output = sio.StringIO()
    with redirect_stdout(output):
        main()
    return output.getvalue().strip()

# provided samples
assert run("""5
abacaba
zyxaabcaabkjh
onetwothree
threetwoone
one
zzonneyy
one
none
twenty
ten
""") == """YES
YES
NO
YES
NO"""

# minimal match
assert run("""1
a
a
""") == "YES"

# simple negative
assert run("""1
ab
cdabx
""") == "NO"

# permutation inside long string
assert run("""1
abc
zzcbaqq
""") == "YES"

# repeated characters edge case
assert run("""1
aab
ababa
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / a` | YES | minimal equality case |
| `ab / cdabx` | NO | no valid permutation window |
| `abc / zzcbaqq` | YES | embedded permutation detection |
| `aab / ababa` | YES | repeated character handling |

## Edge Cases

A key edge case is when the password contains repeated characters. In such cases, permutations are not unique, and naive substring checks based on order fail. For example:

Input:

```
p = "aab"
h = "ababa"
```

The correct answer is YES because substring `"aba"` or `"baa"` both match the required frequency.

The sliding window correctly handles this because it only tracks counts, not order. Each window is compared purely on multiset equality, so duplicates are naturally supported.

Another edge case is when `h` is shorter than `p`. For example:

```
p = "abc"
h = "ab"
```

The algorithm immediately rejects this before any processing, since no valid window exists. This avoids unnecessary computation and prevents out-of-bounds sliding logic.

A final subtle case is when the valid substring appears at the very end of `h`. The initialization plus full sliding loop ensures the last window is checked explicitly, so no boundary case is missed.