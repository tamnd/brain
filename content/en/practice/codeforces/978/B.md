---
title: "CF 978B - File Name"
description: "We are given a short string representing a file name. The only constraint that matters is that the substring \"xxx\" is forbidden anywhere inside the final string."
date: "2026-06-17T01:22:19+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 978
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 481 (Div. 3)"
rating: 800
weight: 978
solve_time_s: 73
verified: true
draft: false
---

[CF 978B - File Name](https://codeforces.com/problemset/problem/978/B)

**Rating:** 800  
**Tags:** greedy, strings  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short string representing a file name. The only constraint that matters is that the substring `"xxx"` is forbidden anywhere inside the final string. We are allowed to delete characters from arbitrary positions, and we want to remove as few characters as possible so that no three consecutive `'x'` characters remain in the resulting string.

The task is therefore a minimization problem on a single string: we must break every run of consecutive `'x'` characters so that no run has length 3 or more, while deleting as few characters as possible.

The input size is small, with the length of the string at most 100. This immediately suggests that any linear scan or even slightly more involved greedy logic will be sufficient. Even an $O(n^2)$ approach would pass comfortably, but the structure of the problem strongly indicates that a single pass greedy solution is enough.

A naive but important observation is that deletions outside runs of `'x'` are never helpful for this constraint. Only sequences of consecutive `'x'` characters matter, since any forbidden pattern must come entirely from them.

A few edge cases matter conceptually.

One case is a string like `"xx"` or `"axxa"`. No deletion is needed because there is no run of length 3. The correct answer is 0.

Another case is `"xxx"`. We must delete at least one character to break the run, so the answer is 1.

A slightly longer case like `"xxxx"` requires deleting at least one character to reduce any resulting run of `'x'` to at most 2. For example, removing one character yields `"xxx"`, but that is still invalid, so at least one more deletion is required, making the answer 2.

A careless approach often fails by only checking whether `"xxx"` exists and deleting a single character somewhere, without considering longer runs. That works for exactly length 3 but breaks immediately for length 4 or more.

## Approaches

A brute-force solution would try all subsets of positions to delete, reconstruct the resulting string, and check whether it contains `"xxx"`. This is correct but completely infeasible in general since there are $2^n$ subsets, which for $n = 100$ is astronomically large.

The structure of the constraint makes the problem local: only consecutive blocks of `'x'` matter. Instead of thinking about deletions globally, we can process the string left to right and handle each maximal segment of consecutive `'x'` independently.

Inside a block of $k$ consecutive `'x'` characters, we want to ensure that at most 2 remain. If $k \le 2$, nothing needs to be removed. If $k \ge 3$, we must delete exactly $k - 2$ characters, because keeping more than 2 would violate the condition, and keeping fewer than 2 would only increase deletions unnecessarily.

The key insight is that deletions in one block do not affect any other block. Therefore, the optimal strategy is simply to sum the excess over 2 for every run of `'x'`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We scan the string once while tracking consecutive `'x'` characters.

1. Initialize a counter for the answer and a variable to track the current run length of `'x'`. This run length represents how many consecutive `'x'` characters we have seen so far.
2. Iterate through the string character by character.
3. If the current character is `'x'`, increment the run length. This extends the current block.
4. If the current character is not `'x'`, we finalize the previous block. If the run length was at least 3, we add `run_length - 2` to the answer because only two `'x'` characters can remain without violating the rule. Then reset the run length to zero.
5. After finishing the loop, we must process the last block if the string ends with `'x'`. The same rule applies: any run longer than 2 contributes `run_length - 2` deletions.

Why it works is based on a structural invariant: at every point, we fully account for deletions needed in all completed runs of consecutive `'x'` characters, and no run interacts with another. Each block is independent because the forbidden pattern depends only on adjacency, and deletions inside one block cannot create or fix violations in another block. Therefore, summing local optimal fixes yields the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
s = input().strip()

ans = 0
run = 0

for ch in s:
    if ch == 'x':
        run += 1
    else:
        if run >= 3:
            ans += run - 2
        run = 0

# finalize last run
if run >= 3:
    ans += run - 2

print(ans)
```

The implementation keeps a single running counter `run` for consecutive `'x'` characters. The critical detail is the final flush after the loop, since a string ending in `'x'` would otherwise leave its last segment unprocessed.

A common mistake is forgetting this final step, which leads to undercounting when the string ends in a long sequence of `'x'`.

## Worked Examples

Consider the input `"xxxiii"`.

We track runs of `'x'`:

| Index | Char | Run length | Action | Answer |
| --- | --- | --- | --- | --- |
| 1 | x | 1 | continue | 0 |
| 2 | x | 2 | continue | 0 |
| 3 | x | 3 | still open | 0 |
| 4 | i | 0 | add 3-2=1 | 1 |
| 5 | i | 0 | continue | 1 |
| 6 | i | 0 | continue | 1 |

Final answer is 1.

This shows that only one deletion is needed to break the single run of three `'x'` characters.

Now consider `"xxxx"`.

| Index | Char | Run length | Action | Answer |
| --- | --- | --- | --- | --- |
| 1 | x | 1 | continue | 0 |
| 2 | x | 2 | continue | 0 |
| 3 | x | 3 | continue | 0 |
| 4 | x | 4 | end of string triggers flush | 4-2=2 |

Final answer is 2.

This confirms that longer runs require proportional reductions beyond just removing a single character.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each character is processed once in a single pass |
| Space | $O(1)$ | Only a constant number of counters are maintained |

The input size is at most 100, so the linear scan is trivially fast within limits, and even constant-factor overhead is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input().strip())
    s = input().strip()

    ans = 0
    run_len = 0

    for ch in s:
        if ch == 'x':
            run_len += 1
        else:
            if run_len >= 3:
                ans += run_len - 2
            run_len = 0

    if run_len >= 3:
        ans += run_len - 2

    return str(ans)

# provided samples
assert run("6\nxxxiii\n") == "1"

# custom cases
assert run("3\nxxx\n") == "1"
assert run("4\nxxxx\n") == "2"
assert run("5\naxxxa\n") == "1"
assert run("2\nxx\n") == "0"
assert run("7\nxxxxxxx\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"xxx"` | `1` | minimal forbidden case |
| `"xxxx"` | `2` | longer run handling |
| `"axxxa"` | `1` | internal block handling |
| `"xx"` | `0` | no deletion needed |
| `"xxxxxxx"` | `5` | large run correctness |

## Edge Cases

For a string like `"axxxxa"`, the algorithm isolates the internal run of four `'x'` characters. As it scans, it builds a run length of 4, then resets when it hits `'a'`, adding `4 - 2 = 2` to the answer. The surrounding `'a'` characters do not affect the computation.

For `"xxxxxxx"`, the run grows to 7 and is only processed at the end. The final flush adds `7 - 2 = 5`, correctly handling the worst-case continuous block.

Both cases confirm the invariant that each maximal `'x'` segment is independently reduced to length at most 2, with minimal deletions.
