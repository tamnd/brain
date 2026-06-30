---
title: "CF 104435B - Cult of Wah!"
description: "Each test case contains two collections of lowercase words. The first collection is the Wah-List, which contains every word that must appear after the encrypted message has been decoded. The second collection is the encrypted message itself."
date: "2026-06-30T18:41:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104435
codeforces_index: "B"
codeforces_contest_name: "2023 UP ACM Algolympics Final Round"
rating: 0
weight: 104435
solve_time_s: 59
verified: true
draft: false
---

[CF 104435B - Cult of Wah!](https://codeforces.com/problemset/problem/104435/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case contains two collections of lowercase words.

The first collection is the Wah-List, which contains every word that must appear after the encrypted message has been decoded.

The second collection is the encrypted message itself. Every word was encrypted with the same Caesar cipher shift. During encryption, every letter was moved forward by `k` positions in the alphabet, wrapping around after `z`. To decode, we must shift every letter backward by the same amount.

Our task is to find the smallest **positive** shift value `k` such that, after decoding the entire message, every word from the Wah-List appears somewhere in the decoded message. If no positive shift satisfies this condition, we output `-1`.

The alphabet contains only 26 letters, so there are only 26 distinct Caesar shifts. Since the problem only allows positive values of `k`, we only need to test shifts from `1` through `25`. A shift of `26` would produce the original message again and is equivalent to `0`, so it can never be the smallest positive answer.

The message length is at most 1500 characters, and the Wah-List contains at most 20 words of length at most 50. Even decoding the entire message for every possible shift requires only about `25 × 1500 = 37500` character operations per test case, which is comfortably small.

One subtle case is when several shifts produce valid decoded messages. For example,

```
Wah-List:
aaa

Message:
bbb ccc ddd
```

Shifts `1`, `2`, and `3` all produce a message containing `aaa`. The correct answer is `1` because we must return the smallest positive shift, not just any valid one.

Another easy mistake is forgetting that the shift wraps around the alphabet.

```
Wah-List:
xyz

Message:
abc
```

Decoding with `k = 3` turns `abc` into `xyz`. Simply subtracting three from each character without wrapping would produce invalid letters.

A third pitfall is treating duplicate message words incorrectly. Consider

```
Wah-List:
cat dog

Message:
fdw fdw grj
```

After decoding with the correct shift, the message becomes

```
cat cat dog
```

The duplicates do not matter. We only need to know whether each required word appears at least once, so storing decoded words in a set is sufficient.

## Approaches

The most direct solution is to try every possible positive shift. For each shift, decode every word in the message, collect the decoded words into a set, and check whether every Wah-List word belongs to that set. Since there are only 25 candidate shifts, this approach is already extremely efficient.

Suppose we ignored the fact that the alphabet has only 26 letters and instead searched over arbitrarily large values of `k`. That would clearly be impossible because infinitely many shifts exist. The crucial observation is that Caesar cipher shifts repeat every 26 positions. Shifting by 27 is exactly the same as shifting by 1, shifting by 52 is the same as shifting by 0, and so on. This periodicity reduces the search space to only 25 meaningful candidates.

Once we recognize this, there is no need for more sophisticated algorithms such as hashing, tries, or string matching. Decoding every candidate message is already well within the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over arbitrary shifts | Unbounded | O(1) | Impossible |
| Try all 25 Caesar shifts | O(25 × L) | O(M) | Accepted |

Here, `L` is the total number of characters in the encrypted message and `M` is the number of words in the message.

## Algorithm Walkthrough

1. Read the Wah-List and store its words in a set. Using a set makes later membership checks constant time.
2. Read the encrypted message as a list of words.
3. For every shift `k` from `1` to `25`, decode every message word by shifting each character backward by `k` positions with modulo 26 arithmetic.
4. Insert every decoded word into a set. Duplicate decoded words are irrelevant because we only care whether a required word appears at least once.
5. Check whether every Wah-List word belongs to the decoded-word set.
6. As soon as one shift satisfies the condition, output that shift and stop searching. Since shifts are tested in increasing order, the first valid one is automatically the smallest positive answer.
7. If none of the 25 shifts succeeds, output `-1`.

### Why it works

Every possible Caesar cipher is uniquely determined by its shift modulo 26. Testing shifts from `1` through `25` covers every distinct positive cipher exactly once. For a fixed shift, decoding reconstructs exactly the message that would have existed before encryption with that shift. The algorithm accepts precisely when every required word appears in that decoded message. Since shifts are checked in increasing order, the first successful one is guaranteed to be the smallest valid answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def decode_word(word, shift):
    res = []
    for c in word:
        x = (ord(c) - ord('a') - shift) % 26
        res.append(chr(ord('a') + x))
    return "".join(res)

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        wah = set(input().split())

        m = int(input())
        message = input().split()

        answer = -1

        for shift in range(1, 26):
            decoded = set()

            for word in message:
                decoded.add(decode_word(word, shift))

            if wah.issubset(decoded):
                answer = shift
                break

        print(answer)

if __name__ == "__main__":
    solve()
```

The solution begins by storing the Wah-List in a set because membership testing is the only operation we need. Every candidate shift is processed independently.

The helper function performs the Caesar decoding. Each letter is converted to a value from `0` to `25`, the shift is subtracted, modulo arithmetic handles wrap-around automatically, and the result is converted back into a character.

For each shift, every message word is decoded exactly once and inserted into a set. Using a set naturally ignores duplicates while providing constant-time lookups. The subset test directly answers whether every required word is present.

The loop stops immediately after finding the first valid shift. Since the shifts are examined in ascending order, this guarantees the minimum positive answer.

## Worked Examples

### Example 1

Suppose the input is

```
1
2
wah umu
3
zhv zdk xpx
```

The correct shift is `3`.

| Shift | Decoded words | Contains wah? | Contains umu? | Valid |
| --- | --- | --- | --- | --- |
| 1 | different words | No | No | No |
| 2 | different words | No | No | No |
| 3 | yes wah umu | Yes | Yes | Yes |

The search stops immediately after shift `3`, demonstrating why checking shifts in increasing order automatically gives the smallest valid answer.

### Example 2

```
1
1
aaa
3
bbb ccc ddd
```

| Shift | Decoded words | Contains aaa? | Valid |
| --- | --- | --- | --- |
| 1 | aaa bbb ccc | Yes | Yes |

Although larger shifts also work, the algorithm never reaches them because shift `1` is already the smallest valid answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(25 × L) | The message is decoded once for each of the 25 possible positive shifts. |
| Space | O(M) | The decoded-word set stores at most one copy of each decoded message word. |

Since the total message length is at most 1500 characters, decoding the message 25 times requires only a few tens of thousands of character operations. This easily fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    from contextlib import redirect_stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    def decode_word(word, shift):
        return "".join(chr((ord(c) - 97 - shift) % 26 + 97) for c in word)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        for _ in range(t):
            n = int(input())
            wah = set(input().split())
            m = int(input())
            msg = input().split()

            ans = -1
            for k in range(1, 26):
                dec = {decode_word(w, k) for w in msg}
                if wah.issubset(dec):
                    ans = k
                    break
            print(ans)

    with redirect_stdout(out):
        solve()

    return out.getvalue()

assert run("""1
1
aaa
3
bbb ccc ddd
""") == "1\n"

assert run("""1
1
xyz
1
abc
""") == "3\n"

assert run("""1
1
abc
1
abc
""") == "-1\n"

assert run("""1
2
cat dog
3
fdw fdw grj
""") == "3\n"

assert run("""1
1
a
1
b
""") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `aaa` with `bbb ccc ddd` | `1` | Smallest valid shift is chosen. |
| `xyz` with `abc` | `3` | Alphabet wrap-around is handled correctly. |
| `abc` with `abc` | `-1` | Shift `0` is not allowed. |
| Duplicate decoded words | `3` | Message duplicates do not affect correctness. |
| Single-character words | `1` | Minimum-size input works correctly. |

## Edge Cases

Consider

```
1
1
abc
1
abc
```

The only shift that leaves the message unchanged is `0`, but only positive shifts are allowed. The algorithm checks shifts `1` through `25`, finds no valid decoding, and correctly outputs `-1`.

Now consider

```
1
1
xyz
1
abc
```

When the algorithm reaches shift `3`, each character is decoded using modulo 26 arithmetic. The word `abc` becomes `xyz`, satisfying the Wah-List. This confirms that wrap-around is implemented correctly.

Finally, consider

```
1
2
cat dog
3
fdw fdw grj
```

With shift `3`, the decoded message is `cat cat dog`. The decoded-word set becomes `{cat, dog}` despite the duplicate occurrence of `cat`. The subset test succeeds, showing that duplicates in the message never interfere with correctness.
