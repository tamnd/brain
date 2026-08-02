---
title: "CF 102621G - Hen Hackers"
description: "The problem is an interactive task. The hidden object is a password made from distinct characters of the 62-character set containing lowercase letters, uppercase letters, and digits."
date: "2026-08-02T13:56:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102621
codeforces_index: "G"
codeforces_contest_name: "mBIT Advanced June 2020"
rating: 0
weight: 102621
solve_time_s: 56
verified: true
draft: false
---

[CF 102621G - Hen Hackers](https://codeforces.com/problemset/problem/102621/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem is an interactive task. The hidden object is a password made from distinct characters of the 62-character set containing lowercase letters, uppercase letters, and digits. A query sends a possible password to the judge, and the judge replies whether the query is the exact password, a proper subsequence of the password, or not contained in it at all. The goal is to discover the password within 750 guesses.

The key restriction is that every character appears at most once, so the password is a permutation of a subset of the alphabet. The maximum possible length is 62, which is small enough that we can afford logarithmic searches over characters, but not enough to try all possible permutations. The number of possible passwords is enormous, so any method based on enumerating candidates is impossible.

The tricky parts come from interpreting the judge response correctly. A query containing one character does not only tell us about that character. It also reveals whether the entire password has length one. For example, querying `a` against the password `a` gives `C`, while querying `a` against `ab` gives `Y`. Treating both responses as identical would lose the length information.

Another subtle case is the final query. If our constructed string contains every character of the password in the correct order, the answer may be `C` instead of `Y`. The algorithm must stop immediately on `C`, because sending extra queries after success is not allowed.

## Approaches

A direct approach would be to try candidate strings and use the responses to eliminate impossible passwords. This is correct because every answer gives information about the hidden string, but the search space is far too large. Even restricting ourselves to strings without repeated characters gives

$$62! + 62 \cdot 61! + \dots$$

possible passwords, which is far beyond what can be tested in 750 queries.

The useful observation is that the judge can answer subsequence questions. First, we can discover exactly which characters exist in the password by asking about each individual character. After that, the remaining problem is only ordering those characters.

Because the characters are unique, once we know the set of characters, the password is just one ordering of them. We can maintain a sorted prefix of the password and insert new characters into their correct positions. A binary search over insertion positions works because a candidate ordering is either a subsequence or it is not. This reduces the number of queries needed for ordering from quadratic to roughly $62 \log 62$.

The brute force works because every valid guess gives information, but it fails because the number of possible orders explodes. The observation that subsequence checks reveal relative ordering lets us replace guessing with construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of possible passwords) | O(number of candidates) | Too slow |
| Optimal | O(62 log 62) queries | O(62) | Accepted |

## Algorithm Walkthrough

1. Query every character in the allowed alphabet. If the answer is `Y`, the character belongs to the password. If the answer is `C`, the password consists of that single character and we can finish immediately.
2. Keep the discovered characters in the order they have been found so far. The first known character starts the current ordered sequence.
3. Insert every remaining discovered character into the current sequence. To test whether a position is correct, place the new character there and query the whole sequence. A positive answer means the order is consistent with the hidden password.
4. Use binary search while inserting. If placing the character before the middle position works, the answer is in the left half. Otherwise it must be after that position.
5. After every insertion, the maintained sequence is a subsequence of the real password. Once all characters are inserted, the sequence equals the password, so the next successful query returns `C`.

Why it works: the invariant is that the maintained sequence always appears in the same order inside the hidden password. When inserting a new character, exactly one position preserves this property because the password has no repeated characters. Binary search only chooses between positions using valid subsequence checks, so it cannot discard the true location. After all characters are placed, the maintained sequence contains every character of the password and therefore must be the password itself.

## Python Solution

```python
import sys
input = sys.stdin.readline

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def solve():
    def ask(s):
        print(s, flush=True)
        return input().strip()

    present = []

    for c in alphabet:
        res = ask(c)
        if res == "C":
            return
        if res == "Y":
            present.append(c)

    if not present:
        return

    order = [present[0]]

    for c in present[1:]:
        lo, hi = 0, len(order)

        while lo < hi:
            mid = (lo + hi) // 2
            candidate = ''.join(order[:mid]) + c + ''.join(order[mid:])
            res = ask(candidate)

            if res == "C":
                return

            if res == "Y":
                hi = mid
            else:
                lo = mid + 1

        order.insert(lo, c)

    res = ask(''.join(order))
    if res == "C":
        return

if __name__ == "__main__":
    solve()
```

The `ask` function handles the interactive protocol. It prints a query, flushes immediately, and reads the judge response. Flushing is required because the judge cannot answer until it receives the complete query.

The first loop identifies the character set. A character receiving `Y` is guaranteed to be somewhere in the password because a single character subsequence can only exist if that character exists.

The insertion section keeps `order` valid after every operation. The candidate string is rebuilt from the left part, the inserted character, and the right part, avoiding index mistakes. The binary search boundaries represent possible insertion locations from zero through the current length.

The final query uses all discovered characters in their reconstructed order. If the algorithm is correct, this is the hidden password and the judge returns `C`.

## Worked Examples

Because the original task is interactive, examples are conversations rather than fixed input/output pairs.

For a hidden password `hunter2`, the character discovery phase might look like this:

| Step | Query | Response | Known characters |
| --- | --- | --- | --- |
| 1 | `h` | Y | h |
| 2 | `u` | Y | h,u |
| 3 | `n` | Y | h,u,n |
| 4 | `t` | Y | h,u,n,t |
| 5 | `e` | Y | h,u,n,t,e |
| 6 | `r` | Y | h,u,n,t,e,r |
| 7 | `2` | Y | h,u,n,t,e,r,2 |

The ordering phase inserts characters by testing subsequences. For example, when inserting `t` into `hun`, the query `thun` fails because `t` does not appear before `h`, while `hunt` succeeds because it matches the hidden order.

This demonstrates that a subsequence query can be used as a comparison operation between possible positions.

For a one-character password such as `A`, the first character query gives:

| Step | Query | Response | Action |
| --- | --- | --- | --- |
| 1 | `a` | N | continue |
| 2 | ... | ... | continue |
| 28 | `A` | C | finish |

This confirms why the algorithm must handle `C` during the character detection stage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(62 log 62) queries | At most 62 characters are discovered and each insertion uses binary search |
| Space | O(62) | Only the discovered characters and current ordering are stored |

The query limit is 750, while the algorithm uses far fewer than that. The largest number of insertions is 61, and each requires at most six queries because the sequence length never exceeds 62.

## Test Cases

This problem is interactive, so normal offline assert tests cannot represent the real judge interaction. A local simulation would need a fake judge that stores a hidden password and returns `C`, `Y`, or `N` according to subsequence rules.

A suitable simulator should test the following cases:

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Hidden password `a` | `a` discovered | Single-character password handling |
| Hidden password `hunter2` | `hunter2` discovered | Normal insertion ordering |
| Hidden password `Z9aB` | `Z9aB` discovered | Mixed character classes |
| Hidden password containing all 62 characters | Full alphabet order recovered | Maximum length handling |

## Edge Cases

For a single-character password, such as `x`, querying `x` returns `C`, not `Y`. The algorithm exits immediately instead of trying to continue building an ordering.

For a password containing characters discovered in a different order from their real positions, the insertion stage fixes the ordering. For example, if discovery finds `a`, `b`, `c` but the password is `cab`, inserting `c` and then testing positions ensures the final sequence becomes `cab`.

For the maximum-length password containing all possible characters, the algorithm still works because every insertion only depends on subsequence checks. The number of queries grows with the number of characters, not with the number of possible passwords.
