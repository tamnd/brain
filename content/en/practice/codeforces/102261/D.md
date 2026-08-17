---
title: "CF 102261D - \u0420\u0430\u0441\u043a\u043e\u0434\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435"
description: "We have a string of characters. A decoding round looks for every occurrence of three consecutive characters of the form ~XY, where X and Y are hexadecimal digits, and replaces each such triple by the single character whose ASCII code is the hexadecimal number XY."
date: "2026-08-17T20:39:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102261
codeforces_index: "D"
codeforces_contest_name: "\u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e - \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f (\u042f\u043d\u0434\u0435\u043a\u0441)"
rating: 0
weight: 102261
solve_time_s: 163
verified: true
draft: false
---

[CF 102261D - \u0420\u0430\u0441\u043a\u043e\u0434\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435](https://codeforces.com/problemset/problem/102261/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string of characters. A decoding round looks for every occurrence of three consecutive characters of the form `~XY`, where `X` and `Y` are hexadecimal digits, and replaces each such triple by the single character whose ASCII code is the hexadecimal number `XY`. All replacements in one round happen simultaneously.

We are not asked to reconstruct the final decoded string. We only need the maximum number of consecutive nontrivial rounds, meaning rounds in which at least one such triple exists.

The interesting part is that a replacement can create another tilde. In particular, `~7e` becomes the character with ASCII code `0x7e`, which is another `~`. That new tilde can participate in a pattern during the next round. A replacement can also create a hexadecimal digit, which may later be consumed by a tilde to its left.

The input length is at most 300,000, so an algorithm that scans the whole string once is appropriate. An algorithm taking quadratic time is too slow. This matters because the number of decoding rounds itself can be linear. For example, the string `~7e7e7e` is reduced as `~7e7e7e`, then `~7e7e`, then `~7e`, then `~`, so the number of rounds is proportional to the input length.

A naive implementation that explicitly constructs the string after every round can consequently perform on the order of 300,000 full scans. Since every nontrivial round reduces the length by at least two, the worst case contains about 150,000 rounds, and the total number of examined characters can reach Θ(n²), roughly n²/4 in a chain where only one pattern is reduced per round.

There are several edge cases that are easy to miss.

For `~7e7e`, the first round changes `~7e` into `~`, leaving `~7e`. The second round changes that into `~`, so the answer is 2. An implementation that only searches the original string finds one pattern and misses the newly created tilde.

For `~~37~45~fF`, the three patterns `~37`, `~45`, and `~fF` all exist in the initial state and must be decoded in the same round. After that round the string contains `~7E` followed by the decoded `0xFF` character, so another round is possible. The correct answer is 2. A sequential implementation that treats each replacement as a separate round can count these operations incorrectly.

For `~00`, the replacement produces ASCII code 0, which is not printable and is outside the input alphabet. It still has to be represented internally as a character value. The correct answer is 1, and the resulting character cannot start another encoding.

For `~7g`, the triple is not valid because `g` is not a hexadecimal digit. Nothing happens, so the answer is 0. Checking only whether the two characters are alphabetic would incorrectly accept this case.

Uppercase and lowercase hexadecimal digits are both valid. Thus `~7E` is a valid pattern and has answer 1.

## Approaches

The direct approach is to simulate the decoding process exactly. During one round, scan the current string from left to right. Whenever `~XY` is found, append the decoded character to the next string and skip three positions. Otherwise append the current character unchanged. After the scan, replace the current string with the newly constructed one and repeat until no pattern was found.

This simulation is correct because it follows precisely the simultaneous definition of a round. Patterns cannot overlap: after the leading `~`, the next two characters must be hexadecimal digits, so another pattern cannot begin at either of those positions. The problem is its running time. A nontrivial round decreases the string length by at least two, so there can be Θ(n) rounds. If only one pattern disappears per round, the scans have lengths approximately `n, n-2, n-4, ...`, which gives Θ(n²) character processing. For n = 300,000, this is tens of billions of operations.

The key observation is that we do not actually need to materialize every intermediate string. Each replacement creates one new character, and that character has a well-defined round number in which it appears.

Imagine that every current character is an object containing two values: its ASCII code and the round in which that character was created. Original characters have round 0. Suppose three adjacent objects form `~XY`. The replacement can happen only after all three objects already exist, so the new character appears in round

`1 + max(depth of the three objects)`.

This turns the whole process into a reduction tree. Instead of simulating rounds globally, we can construct these reductions locally while scanning the original string.

A stack is sufficient because every encoded triple consumes three adjacent current characters and produces one character. When a new character is appended, the only newly possible pattern is one ending at that character or one created by a reduction immediately before it. We can repeatedly reduce such patterns on the top of the stack. The depth stored with each resulting character is exactly the round in which it would appear.

The crucial reason this works with simultaneous rounds is that two valid patterns can never overlap. If a pattern is currently available, reducing it cannot invalidate another currently available pattern. A later pattern that uses the new character simply receives a larger depth, which corresponds exactly to waiting for the next decoding round.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal stack | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute the hexadecimal value of every possible byte. For characters `0` through `9`, `A` through `F`, and `a` through `f`, store values from 0 through 15. Every other character receives an invalid marker. This avoids repeated string searches and handles both cases of hexadecimal notation directly.
2. Scan the input from left to right. For every original character, push its ASCII code onto the stack together with depth 0. Original characters already exist before the first decoding round.
3. After pushing a character, check whether the last three stack entries have the form `~XY`. The entries represent adjacent characters of the current reduced string, because every previous reduction replaced a consecutive block by one stack entry.
4. If the last three entries form a valid pattern, remove them and calculate the decoded ASCII code as `16 * value(X) + value(Y)`. Its depth is one greater than the maximum depth of the three removed entries.
5. Push the resulting character and its calculated depth back onto the stack. The new character represents a whole reduced block of the original input.
6. Repeat the reduction check while the top of the stack contains a valid pattern. A newly created character can make a pattern with two characters immediately before it, so checking only once would miss chains of reductions.
7. Keep the maximum depth ever produced. That depth is the maximum number of consecutive nontrivial decoding rounds.

### Why it works

Maintain the invariant that every stack entry represents one contiguous block of the original string after all reductions internal to that block have been performed, and that its stored depth is exactly the round in which its current character appears.

When three adjacent entries form `~XY`, the corresponding characters exist simultaneously after their stored depths have elapsed. The earliest possible round in which all three are present is one greater than their maximum depth, so replacing them produces exactly the character that the real process creates in that round. Because valid patterns cannot overlap, performing this reduction locally cannot interfere with another reduction that should happen in the same round.

Every reduction made by the stack corresponds to a real decoding operation, and every real decoding operation eventually becomes visible as a valid triple on the stack. The largest stored depth is consequently exactly the last nontrivial round.

## Python Solution

```python
import sys
input = sys.stdin.readline

def decode_rounds(s: str) -> int:
    hex_value = [-1] * 256

    for i in range(10):
        hex_value[ord('0') + i] = i

    for i in range(6):
        hex_value[ord('A') + i] = 10 + i
        hex_value[ord('a') + i] = 10 + i

    stack_char = []
    stack_depth = []

    answer = 0

    for ch in s:
        stack_char.append(ord(ch))
        stack_depth.append(0)

        while len(stack_char) >= 3:
            c0 = stack_char[-3]
            c1 = stack_char[-2]
            c2 = stack_char[-1]

            if c0 != 126:
                break

            v1 = hex_value[c1]
            v2 = hex_value[c2]

            if v1 == -1 or v2 == -1:
                break

            d = max(
                stack_depth[-3],
                stack_depth[-2],
                stack_depth[-1]
            ) + 1

            value = 16 * v1 + v2

            stack_char.pop()
            stack_char.pop()
            stack_char.pop()

            stack_depth.pop()
            stack_depth.pop()
            stack_depth.pop()

            stack_char.append(value)
            stack_depth.append(d)

            if d > answer:
                answer = d

    return answer

def main() -> None:
    s = input().rstrip('\n')
    print(decode_rounds(s))

if __name__ == "__main__":
    main()
```

The hexadecimal lookup table is built once. Using an array indexed by the ASCII code makes checking a character constant time, and it naturally handles decoded values from 0 through 255.

The two stacks are kept in parallel. `stack_char` stores the current character of each reduced block, while `stack_depth` stores the round in which that character exists. Keeping the arrays separate avoids allocating a tuple every time a character is pushed or reduced.

Every input character is pushed exactly once. A successful reduction removes three entries and adds one, so every reduction decreases the stack size by two. There can be at most `floor(n / 2)` reductions. The inner `while` loop is consequently executed only O(n) times in total, even though it is nested inside the scan.

The boundary check `len(stack_char) >= 3` is necessary before reading the last three elements. The hexadecimal table also handles decoded characters below 33 and above 126 without any special case, since all internal characters are represented simply by their integer ASCII values.

Python integers have arbitrary precision, so the depth calculation does not have an overflow issue. In practice the maximum depth is at most `floor((n - 1) / 2)`.

## Worked Examples

Consider the sample `~7eFf`. The first three characters form `~7e`, which decodes to another tilde. That new tilde is immediately followed by `Ff`, so a second reduction is possible.

| Input character | Stack characters after reductions | Maximum depth |
| --- | --- | --- |
| `~` | `~` | 0 |
| `7` | `~7` | 0 |
| `e` | `~` | 1 |
| `F` | `~F` | 1 |
| `f` | `ÿ` | 2 |

After processing `e`, the stack contains a tilde with depth 1. Processing `F` and `f` completes another valid triple, so the decoded character has depth 2. No later reduction is possible, giving answer 2. This demonstrates the central idea that a character generated in one round can participate in a later round.

Now consider the sample `~~37~45~fF`.

| Input character | Stack characters after reductions | Maximum depth |
| --- | --- | --- |
| `~` | `~` | 0 |
| `~` | `~~` | 0 |
| `3` | `~~3` | 0 |
| `7` | `~7` | 1 |
| `~` | `~7~` | 1 |
| `4` | `~7~4` | 1 |
| `5` | `~` | 2 |
| `~` | `~~` | 2 |
| `f` | `~~f` | 2 |
| `F` | `~ÿ` | 2 |

After reading `7`, the substring `~37` becomes the character `7`, giving depth 1. After reading `5`, the stack temporarily forms `~7E`, which is itself a valid encoding and therefore reduces to `~` at depth 2. The final `~fF` becomes `0xFF` at depth 1 and does not create another tilde. The maximum depth is 2.

The table also shows why the stack can perform reductions that were not present in the original string. When `~7E` appears, it represents the state of the string after one real decoding round, so reducing it immediately while constructing the reduction tree is equivalent to simulating the second round.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each input character is pushed once, and every reduction removes three entries and creates one. |
| Space | O(n) | The stack can contain one entry for every original character. |

With `n <= 300000`, the linear solution performs only a constant amount of work per input character and per reduction. The memory consumption is also linear and stays comfortably within the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def decode_rounds(s: str) -> int:
    hex_value = [-1] * 256

    for i in range(10):
        hex_value[ord('0') + i] = i

    for i in range(6):
        hex_value[ord('A') + i] = 10 + i
        hex_value[ord('a') + i] = 10 + i

    stack_char = []
    stack_depth = []
    answer = 0

    for ch in s:
        stack_char.append(ord(ch))
        stack_depth.append(0)

        while len(stack_char) >= 3:
            c0 = stack_char[-3]
            c1 = stack_char[-2]
            c2 = stack_char[-1]

            if c0 != ord('~'):
                break

            v1 = hex_value[c1]
            v2 = hex_value[c2]

            if v1 == -1 or v2 == -1:
                break

            depth = max(
                stack_depth[-3],
                stack_depth[-2],
                stack_depth[-1]
            ) + 1

            value = 16 * v1 + v2

            stack_char.pop()
            stack_char.pop()
            stack_char.pop()

            stack_depth.pop()
            stack_depth.pop()
            stack_depth.pop()

            stack_char.append(value)
            stack_depth.append(depth)

            answer = max(answer, depth)

    return answer

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return str(decode_rounds(inp.rstrip('\n')))

# Provided samples
assert run("~7e") == "1", "sample 1"
assert run("~~37~45~fF") == "2", "sample 2"
assert run("~~30~30~7e7E") == "2", "sample 3"
assert run("~7eFf") == "2", "sample 4"
assert run("~hello") == "0", "sample 5"

# Minimum-size input
assert run("a") == "0", "minimum length"

# No valid hexadecimal pair
assert run("~7g") == "0", "invalid hexadecimal digit"

# A decoded non-printable character must still be handled
assert run("~00") == "1", "decoded character below input alphabet"

# Newly created tilde enables another round
assert run("~7e7e") == "2", "new tilde creates another round"

# Maximum-size input, with the maximum possible number of rounds.
# Length is exactly 300000.
max_input = "~" + "7e" * 149999 + "!"
assert len(max_input) == 300000
assert run(max_input) == "149999", "maximum length and maximum depth"

# All characters equal
assert run("~" * 300000) == "0", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | 0 | Minimum input size and absence of a pattern |
| `~7g` | 0 | Invalid hexadecimal character |
| `~00` | 1 | Decoded value outside the printable input alphabet |
| `~7e7e` | 2 | A generated tilde participating in the next round |
| `~` + `7e` repeated 149999 times + `!` | 149999 | Maximum input size and maximum possible depth |
| `~` repeated 300000 times | 0 | Large input with no reductions |

## Edge Cases

For the chain `~7e7e`, the stack first reads `~7e` and replaces it by a tilde of depth 1. The remaining `7e` are now immediately after that generated tilde, so the stack forms another valid triple and replaces it by a tilde of depth 2. The final stack contains only that tilde, and the answer is 2. This catches implementations that inspect only the original input patterns.

For `~~37~45~fF`, the initial patterns are simultaneous. The stack reduces `~37` to `7` with depth 1, then `~45` to `E` with depth 1. Those two reductions expose `~7E`, which becomes a tilde with depth 2. The final `~fF` becomes `0xFF` with depth 1. The answer is 2. This catches implementations that confuse individual replacements with decoding rounds.

For `~00`, the stack recognizes both digits as valid hexadecimal digits and produces integer value 0. The depth becomes 1, and the resulting zero byte cannot form a new pattern because it is not a tilde. The answer is 1. The algorithm never assumes that intermediate characters are printable, which is necessary because decoded values can occupy the entire byte range.

For `~7g`, the first character is a tilde and `7` is a valid hexadecimal digit, but `g` has lookup value `-1`. The stack leaves all three characters unchanged, so no reduction is counted and the answer is 0. This demonstrates why hexadecimal validation must accept exactly `0` through `9`, `A` through `F`, and `a` through `f`.

For the maximum-size chain `~` followed by 149999 copies of `7e` and then `!`, the length is exactly 300000. Each round removes the first `7e` from the active chain and leaves another `~7e` pattern, so there are exactly 149999 nontrivial rounds. The final `!` prevents any additional round. This is the worst structural case for the answer and also demonstrates why a round-by-round simulation can require quadratic time.

For the string consisting of 300000 tildes, no tilde is followed by two hexadecimal digits, so the stack never performs a reduction. Every entry has depth 0 and the answer remains 0. This confirms that the algorithm does not accidentally treat a tilde by itself as an encoding.
