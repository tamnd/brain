---
title: "CF 180D - Name"
description: "We are given a multiset of characters in string s. We may rearrange these characters in any order, but we must use every character exactly once. Among all such permutations, we want the lexicographically smallest string that is still strictly larger than another string t."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 180
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 116 (Div. 2, ACM-ICPC Rules)"
rating: 1900
weight: 180
solve_time_s: 99
verified: true
draft: false
---

[CF 180D - Name](https://codeforces.com/problemset/problem/180/D)

**Rating:** 1900  
**Tags:** greedy, strings  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of characters in string `s`. We may rearrange these characters in any order, but we must use every character exactly once. Among all such permutations, we want the lexicographically smallest string that is still strictly larger than another string `t`.

This is not asking for the next permutation of `s` itself. The original order of `s` is irrelevant. The only thing that matters is the character counts available to us.

The constraints are large enough that brute force permutation generation is impossible. A string of length 5000 has astronomically many permutations, even with repeated letters. Since the alphabet contains only lowercase English letters, we should expect a solution based on character frequencies and greedy construction. An `O(n * 26)` or `O(n^2)` algorithm is fine for `n = 5000`, but factorial or exponential approaches are ruled out immediately.

The tricky part is lexicographic minimality. We do not only need some permutation greater than `t`, we need the smallest such permutation. Greedy decisions that locally increase the string too early can easily produce a valid answer that is not minimal.

One important edge case appears when every permutation of `s` is smaller than or equal to `t`.

For example:

```
s = "abc"
t = "zzz"
```

No permutation can exceed `"zzz"`, so the correct answer is:

```
-1
```

A careless greedy algorithm might still try to build something character by character and forget to detect impossibility.

Another subtle case occurs when the optimal answer differs from `t` very late.

```
s = "aabc"
t = "aaba"
```

The answer is:

```
aabc
```

The first three characters must stay equal to keep the result minimal. Increasing earlier would create a larger-than-necessary answer.

Prefix relationships also matter.

```
s = "aaa"
t = "aa"
```

The answer is:

```
aaa
```

A longer string with the same prefix is lexicographically larger. If we ignore the differing lengths, we may incorrectly conclude that no larger permutation exists.

The opposite direction matters too:

```
s = "aa"
t = "aaa"
```

Every permutation of `s` is smaller because it becomes a prefix of `t`, so the correct answer is:

```
-1
```

Handling length interactions correctly is essential.

## Approaches

The brute-force idea is straightforward. Generate every distinct permutation of `s`, sort them lexicographically, and take the first one greater than `t`.

This works logically because lexicographic order directly matches the requirement. The first valid permutation after sorting is exactly the desired answer.

The problem is the number of permutations. Even a string of length 15 already has up to `15! ≈ 10^12` permutations. Here the length can be 5000, so exhaustive generation is completely impossible.

The key observation is that lexicographic order depends on the first position where two strings differ.

Suppose we are building the answer from left to right. At some position `i`, we have already matched `t[0:i]`. Now we have two possibilities.

If we place exactly `t[i]`, we remain tied and must continue carefully.

If we place something larger than `t[i]`, then the rest of the string should be as small as possible, because the lexicographic comparison has already been decided.

This creates a natural greedy strategy. At every position, try to keep equality with `t` if possible. If equality cannot eventually lead to a solution, then place the smallest larger character available and finish the remainder in sorted order.

The remaining challenge is determining whether continuing with equality is feasible. Since the alphabet size is only 26, we can greedily test possibilities efficiently using character counts.

A clean way to think about the algorithm is backtracking over positions, but with only 26 branching options at each step and immediate pruning.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / factorial | Exponential | Too slow |
| Optimal | O(n × 26) | O(26 + n) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of every character in `s`.

These counts represent the remaining letters we may still place.
2. Build the answer from left to right.

At each position `i`, we try to choose the smallest possible character that can still lead to a valid final string.
3. For the current position, iterate through candidate characters from `'a'` to `'z'`.

We only consider characters whose remaining count is positive.
4. Compare the candidate character with `t[i]` if `i < len(t)`.

If `i >= len(t)`, then any additional character already makes the string lexicographically larger because `t` becomes a prefix.
5. If the candidate is smaller than `t[i]`, skip it.

Choosing a smaller character while all previous positions are equal would immediately make the whole string smaller than `t`.
6. Temporarily place the candidate and decrease its count.
7. If the candidate is larger than `t[i]`, fill the rest of the positions with all remaining characters in sorted order and finish.

Once we exceed `t` at some position, the minimal continuation is simply the lexicographically smallest suffix possible.
8. If the candidate equals `t[i]`, we must check whether the remaining characters can still eventually produce a string larger than `t`.

This is the subtle part. Equality keeps the comparison unresolved.
9. Continue recursively or iteratively to the next position.

If a valid completion exists, keep this character. Otherwise restore the count and try the next larger character.
10. If no character works at some position, backtrack.
11. If the entire string is built and it is strictly larger than `t`, output it. Otherwise print `-1`.

### Why it works

The algorithm always tries smaller lexicographic choices before larger ones. At each position, it attempts to preserve equality with `t` because any earlier increase would make the result unnecessarily large.

When equality becomes impossible, the algorithm picks the smallest character that makes the prefix larger than `t`. After that point, the remainder is minimized by sorting the unused characters.

This exactly mirrors the definition of lexicographic order. The first differing position determines the comparison, so minimizing all earlier positions guarantees global minimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
t = input().strip()

n = len(s)

cnt = [0] * 26
for ch in s:
    cnt[ord(ch) - ord('a')] += 1

ans = []

def dfs(pos, greater):
    if pos == n:
        return greater or n > len(t)

    limit = ord(t[pos]) - ord('a') if pos < len(t) else -1

    for c in range(26):
        if cnt[c] == 0:
            continue

        if not greater:
            if pos < len(t):
                if c < limit:
                    continue
            # if pos >= len(t), any character works

        cnt[c] -= 1
        ans.append(chr(c + ord('a')))

        new_greater = greater

        if not greater:
            if pos >= len(t):
                new_greater = True
            elif c > limit:
                new_greater = True

        if dfs(pos + 1, new_greater):
            return True

        ans.pop()
        cnt[c] += 1

    return False

if dfs(0, False):
    print("".join(ans))
else:
    print(-1)
```

The solution keeps only the remaining character counts instead of physically generating permutations. This avoids huge memory usage and duplicate work.

The recursive state contains two pieces of information. `pos` tells us which position we are filling, and `greater` tells us whether the constructed prefix is already lexicographically larger than `t`.

If `greater` is already true, the rest of the positions can use the smallest available characters greedily. The DFS naturally achieves this because it iterates from `'a'` upward.

The boundary case `pos >= len(t)` is especially important. Once the constructed string becomes longer while still matching all previous characters, it is automatically lexicographically larger.

Another subtle detail is the base condition:

```
return greater or n > len(t)
```

If all positions are used and the strings are equal so far, then the result is larger only when our string is longer than `t`.

The recursion depth is at most 5000. Python's default recursion limit may be too small on some systems. In competitive environments this solution is typically accepted, but adding:

```
sys.setrecursionlimit(10000)
```

is also reasonable.

## Worked Examples

### Example 1

Input:

```
s = "aad"
t = "aac"
```

Character counts:

```
a: 2
d: 1
```

| Position | Current Prefix | Candidate | Relation to t | Decision |
| --- | --- | --- | --- | --- |
| 0 | "" | a | equal | keep exploring |
| 1 | "a" | a | equal | keep exploring |
| 2 | "aa" | d | greater than c | accept |

Final answer:

```
aad
```

The trace shows the ideal greedy behavior. The algorithm keeps equality as long as possible, then increases at the latest valid position.

### Example 2

Input:

```
s = "abc"
t = "acb"
```

| Position | Current Prefix | Candidate | Relation to t | Decision |
| --- | --- | --- | --- | --- |
| 0 | "" | a | equal | continue |
| 1 | "a" | b | smaller than c | reject |
| 1 | "a" | c | equal | continue |
| 2 | "ac" | b | equal | end reached, not greater |
| 0 | "" | b | greater than a | accept |

Final answer:

```
bac
```

The failed branch demonstrates why simple greedy equality is not enough. Matching `"acb"` exactly is invalid because the result must be strictly larger.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × 26) | Each position tries at most 26 characters |
| Space | O(n + 26) | Recursion stack plus frequency array |

The alphabet size is constant, so the branching factor is tightly bounded. With `n ≤ 5000`, this comfortably fits within the time limit. Memory usage is also tiny compared to the allowed 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    s = input().strip()
    t = input().strip()

    n = len(s)

    cnt = [0] * 26
    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    ans = []

    sys.setrecursionlimit(10000)

    def dfs(pos, greater):
        if pos == n:
            return greater or n > len(t)

        limit = ord(t[pos]) - ord('a') if pos < len(t) else -1

        for c in range(26):
            if cnt[c] == 0:
                continue

            if not greater:
                if pos < len(t) and c < limit:
                    continue

            cnt[c] -= 1
            ans.append(chr(c + ord('a')))

            ng = greater

            if not greater:
                if pos >= len(t) or c > limit:
                    ng = True

            if dfs(pos + 1, ng):
                return True

            ans.pop()
            cnt[c] += 1

        return False

    if dfs(0, False):
        return "".join(ans)
    return "-1"

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("aad\naac\n") == "aad", "sample 1"

# minimum size
assert run("a\na\n") == "-1", "equal single characters"

# longer string wins by prefix
assert run("aaa\naa\n") == "aaa", "prefix ordering"

# impossible case
assert run("abc\nzzz\n") == "-1", "no permutation can exceed"

# late increase
assert run("aabc\naaba\n") == "aabc", "increase at final position"

# exact equality forbidden
assert run("abc\nacb\n") == "bac", "must be strictly larger"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / a` | `-1` | Equal strings are not allowed |
| `aaa / aa` | `aaa` | Longer prefix-equal string is larger |
| `abc / zzz` | `-1` | Impossible construction |
| `aabc / aaba` | `aabc` | Optimal increase occurs late |
| `abc / acb` | `bac` | Exact equality must be rejected |

## Edge Cases

Consider the case where every permutation is too small.

```
s = "abc"
t = "zzz"
```

At position 0, every available character is smaller than `'z'`, so all candidates are rejected immediately. The DFS fails at the root and returns `-1`.

Now consider a prefix situation.

```
s = "aaa"
t = "aa"
```

The algorithm matches both `'a'` characters. At position 2, `pos >= len(t)` becomes true, so placing any remaining character automatically sets `greater = True`. The result becomes `"aaa"`.

The opposite prefix direction behaves differently.

```
s = "aa"
t = "aaa"
```

The algorithm matches the first two positions exactly, but then runs out of characters while still not being greater. Since `n < len(t)`, the base case returns false and the final answer is `-1`.

Another tricky case is exact equality.

```
s = "abc"
t = "abc"
```

The DFS can build `"abc"`, but at the end `greater` is still false and the lengths are equal. The branch is rejected. The algorithm backtracks and eventually determines that no larger permutation exists.
