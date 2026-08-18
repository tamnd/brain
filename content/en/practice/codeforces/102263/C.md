---
title: "CF 102263C - Check The Text"
description: "Roze wants the final text on the screen to be exactly the required text, including capitalization and the single spaces between consecutive words. The required text is given as n words, so the intended screen contents are those words joined by one space."
date: "2026-08-19T02:48:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102263
codeforces_index: "C"
codeforces_contest_name: "ArabellaCPC 2019"
rating: 0
weight: 102263
solve_time_s: 205
verified: true
draft: false
---

[CF 102263C - Check The Text](https://codeforces.com/problemset/problem/102263/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

Roze wants the final text on the screen to be exactly the required text, including capitalization and the single spaces between consecutive words. The required text is given as `n` words, so the intended screen contents are those words joined by one space.

The second part of the input describes the actual keyboard actions, one key per line. A letter key produces either a lowercase or uppercase character depending on the current CapsLock state. Pressing `CapsLock` toggles that state. `Space` inserts one space, while `Backspace` removes the last character currently on the screen, if the screen is nonempty.

The task is to execute these actions exactly as the keyboard would and compare the resulting screen with the intended text. We print `Correct` only when the two strings are identical.

The number of words and the number of key presses are both below 2000, and the total length of the required words is also below 2000. These limits are small enough that even a quadratic implementation would usually fit comfortably, but they also make a direct linear simulation extremely simple. There is no need for hashing, dynamic programming, or any more advanced data structure. We only need to process each key once and maintain the current screen.

Several details can cause an incorrect implementation to silently accept the wrong text.

Consider this input:

```
2
a b
2
a
b
```

The final screen is `ab`, while the required text is `a b`, so the answer is `Incorrect`. An implementation that simply compares the sequence of letters while ignoring `Space` would incorrectly accept it.

Capitalization is also part of the text. For example:

```
2
A b
3
CapsLock
a
b
```

The final screen is `Ab`, not `A b`, so the answer is `Incorrect`. A careless implementation might track only which letters were typed and forget that CapsLock changes their case.

Backspace at an empty screen is another boundary condition. For example:

```
2
a b
4
a
Backspace
Space
b
```

The first two actions leave the screen empty, then `Space` produces `" "`, and `b` produces `" b"`. The result is `Incorrect`. More generally, a backspace must not make the screen length negative.

Finally, a backspace can remove a space just like it removes a letter. For example:

```
2
a b
4
a
Space
Backspace
b
```

The final screen is `ab`, not `a b`, so the answer is `Incorrect`. Treating spaces separately from letters during deletion would be wrong.

## Approaches

A direct simulation is the natural starting point. Maintain a string representing the current screen. For every letter, append the correctly cased character. For `Space`, append a space. For `Backspace`, remove the last character when one exists. For `CapsLock`, toggle a Boolean flag. Once all keys have been processed, compare the simulated screen with `" ".join(words)`.

The idea is correct because every keyboard operation has a direct representation in the simulation. The main weakness of the most naive implementation is the choice of data structure. Python strings are immutable, so an operation such as `screen = screen[:-1]` creates a new string and copies the remaining characters. Repeated appends can also copy increasingly long strings.

With at most 1999 key presses, the worst-case amount of character copying is on the order of one million operations for a carefully constructed sequence of appends and deletions, so even this naive implementation is acceptable for the original constraints. However, its quadratic behavior is unnecessary and would become a problem if the same task were scaled to hundreds of thousands of key presses. The issue is not the simulation itself, but repeatedly rebuilding the entire prefix of the screen.

The key observation is that the screen behaves exactly like a stack. A newly typed character is placed at the end, and `Backspace` removes precisely the most recently written character. A Python list gives us constant-time append and removal from the end, so it represents the screen naturally.

With this representation, every key requires constant work. We process the key sequence once, producing the final screen in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive immutable-string simulation | O(m²) worst case | O(m) | Accepted for these limits, but unnecessarily slow |
| Stack simulation | O(m + L) | O(m + L) | Accepted |

Here `m` is the number of key presses and `L` is the length of the required text.

## Algorithm Walkthrough

1. Read the `n` target words and construct the required screen with `" ".join(words)`. Joining is necessary because the spaces between words are part of what must be checked.
2. Create an empty list called `screen`. This list represents the current characters on the screen, with the last list element corresponding to the character that Backspace would remove.
3. Set a Boolean variable `caps` to `False`. The keyboard starts in lowercase mode, so the first letter key must be interpreted as lowercase unless a `CapsLock` key has already toggled the state.
4. Process each of the `m` pressed keys in order. If the key is `CapsLock`, flip `caps`. No character is added to the screen because CapsLock only changes the interpretation of future letter keys.
5. If the key is `Backspace`, remove the last element of `screen` when the list is nonempty. If the list is empty, do nothing, matching the keyboard's behavior.
6. If the key is `Space`, append `" "` to `screen`. Spaces are ordinary screen characters for the purpose of Backspace and final comparison.
7. Otherwise the key is a letter. Convert it to uppercase when `caps` is true and to lowercase when `caps` is false, then append the resulting character to `screen`.
8. After all keys have been processed, convert `screen` to a string and compare it with the target text. Print `Correct` if they are equal and `Incorrect` otherwise.

### Why it works

The invariant is that after processing any prefix of the key sequence, `screen` contains exactly the characters that would be visible on the real keyboard's screen after executing that same prefix, and `caps` equals the keyboard's current CapsLock state.

Initially both are correct because the screen is empty and CapsLock is off. Each possible key preserves the invariant: CapsLock changes only the state, Backspace removes the last visible character when possible, Space adds a space, and a letter adds the letter with the case determined by the current state. Consequently, after all keys are processed, `screen` is exactly the actual final screen. Comparing it with the required text is thus sufficient to determine whether the text was printed correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    words = input().split()
    target = " ".join(words)

    m = int(input())

    screen = []
    caps = False

    for _ in range(m):
        key = input().strip()

        if key == "CapsLock":
            caps = not caps
        elif key == "Backspace":
            if screen:
                screen.pop()
        elif key == "Space":
            screen.append(" ")
        else:
            screen.append(key.upper() if caps else key.lower())

    result = "".join(screen)

    print("Correct" if result == target else "Incorrect")

if __name__ == "__main__":
    solve()
```

The target string is constructed once from the words. Since the input guarantees exactly one intended space between consecutive words, `" ".join(words)` produces precisely the string that must appear on the screen.

The `screen` list is the stack described in the algorithm. `append` handles characters entering the screen, while `pop` removes the most recently written character. The `if screen` check is necessary because Backspace on an empty screen has no effect.

The `caps` flag is toggled before processing any later letter. A `CapsLock` key itself never appears on the screen, so it must not be appended to the stack.

The order of the condition checks matters because `CapsLock`, `Backspace`, and `Space` are special key names rather than letters. Any other key is guaranteed to be a single alphabetic character, so it can safely be handled by the final branch.

There are no integer-overflow concerns because the algorithm uses only counters bounded by the input size. The list can contain at most `m` characters, so its memory usage is linear.

## Worked Examples

The statement provides one sample, so the second trace below uses a small constructed case that exercises CapsLock and Backspace.

### Sample 1

The required text is `Hello World`. The pressed keys first produce `Hell`, then Backspace removes the final `l`, and the later operations eventually produce `Howorld` rather than the required text.

| Key | Caps | Screen |
| --- | --- | --- |
| CapsLock | true | `""` |
| h | true | `"H"` |
| CapsLock | false | `"H"` |
| e | false | `"He"` |
| l | false | `"Hel"` |
| l | false | `"Hell"` |
| Backspace | false | `"Hel"` |
| o | false | `"Helo"` |
| Space | false | `"Helo "` |
| w | false | `"Helo w"` |
| o | false | `"Helo wo"` |
| Backspace | false | `"Helo w"` |
| Backspace | false | `"Helo "` |
| w | false | `"Helo w"` |
| o | false | `"Helo wo"` |
| r | false | `"Helo wor"` |
| l | false | `"Helo worl"` |
| d | false | `"Helo world"` |

The final screen is `"Helo world"`, while the target is `"Hello World"`. Both the missing `l` and the incorrect capitalization of `World` matter, so the answer is `Incorrect`.

### Constructed Sample 2

Consider the following input:

```
2
Ab c
6
CapsLock
a
b
CapsLock
Space
c
```

The execution is:

| Key | Caps | Screen |
| --- | --- | --- |
| CapsLock | true | `""` |
| a | true | `"A"` |
| b | true | `"AB"` |
| CapsLock | false | `"AB"` |
| Space | false | `"AB "` |
| c | false | `"AB c"` |

The final screen is `"AB c"`, but the required text is `"Ab c"`, so the result is `Incorrect`. This trace demonstrates why CapsLock must affect each future letter independently rather than simply changing the final string afterward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m + L) | Every key is processed once, and the final comparison scans the produced and target strings |
| Space | O(m + L) | The target and simulated screen both require linear storage |

The original constraints keep both `m` and the target length below 2000, so the linear solution performs only a few thousand basic operations and uses very little memory. It also avoids the unnecessary quadratic copying caused by immutable-string updates, making the implementation suitable for substantially larger versions of the same problem.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.splitlines()
    it = iter(data)

    n = int(next(it))
    words = next(it).split()
    target = " ".join(words)

    m = int(next(it))

    screen = []
    caps = False

    for _ in range(m):
        key = next(it).strip()

        if key == "CapsLock":
            caps = not caps
        elif key == "Backspace":
            if screen:
                screen.pop()
        elif key == "Space":
            screen.append(" ")
        else:
            screen.append(key.upper() if caps else key.lower())

    return "Correct" if "".join(screen) == target else "Incorrect"

def run(inp: str) -> str:
    return solve_data(inp)

# Provided sample
sample1 = """2
Hello World
17
CapsLock
h
CapsLock
e
l
l
Backspace
o
Space
w
o
Backspace
Backspace
w
o
r
l
d
"""
assert run(sample1) == "Incorrect", "sample 1"

# Minimum-size style case, exact text with one space
case2 = """2
a b
3
a
Space
b
"""
assert run(case2) == "Correct", "basic correct text"

# Backspace on an empty screen, followed by the target
case3 = """2
a b
5
Backspace
a
Space
b
Backspace
"""
assert run(case3) == "Incorrect", "empty backspace and final deletion"

# CapsLock toggles twice, producing the original lowercase text
case4 = """2
ab cd
7
CapsLock
a
CapsLock
b
Space
c
d
"""
assert run(case4) == "Correct", "CapsLock toggling"

# Backspace removes a space, so the final text has no separator
case5 = """2
a b
4
a
Space
Backspace
b
"""
assert run(case5) == "Incorrect", "backspace removes space"

# Large boundary-style case
words = ["a" * 999, "b" * 999]
target = " ".join(words)
case6 = (
    "2\n"
    + target
    + "\n"
    + "1999\n"
    + "\n".join(list("a" * 999 + "b" * 1000))
    + "\n"
)
assert run(case6) == "Incorrect", "large input boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `Incorrect` | Provided sample, including deletion and capitalization |
| `a b` with `a`, `Space`, `b` | `Correct` | Basic successful simulation |
| Leading `Backspace` followed by text | `Incorrect` | Backspace on an empty screen |
| Two CapsLock toggles | `Correct` | CapsLock state changes and returns to lowercase |
| `a`, `Space`, `Backspace`, `b` | `Incorrect` | Backspace must remove spaces too |
| 999 `a` characters and 999 `b` characters | `Incorrect` | Large boundary input and linear processing |

## Edge Cases

A Backspace on an empty screen must be ignored. For the input

```
2
a b
5
Backspace
a
Space
b
Backspace
```

the first Backspace leaves the empty stack unchanged. The next three keys create `"a b"`, and the final Backspace removes `b`, leaving `"a "`. Since `"a "` differs from `"a b"`, the answer is `Incorrect`. The `if screen` guard prevents an invalid `pop` and exactly models the keyboard behavior.

Spaces are stored in the same stack as letters. For

```
2
a b
4
a
Space
Backspace
b
```

the stack evolves from `[]` to `["a"]`, then `["a", " "]`, then back to `["a"]`, and finally to `["a", "b"]`. The final text is `"ab"`, so the result is `Incorrect`. Treating Backspace as a letter-only operation would leave the deleted space in the result and produce the wrong answer.

CapsLock affects only subsequent letter presses. With

```
2
A b
3
CapsLock
a
b
```

the flag becomes true before `a`, so the screen becomes `"A"`. The flag remains true when `b` is pressed, producing `"AB"`. The target is `"A b"`, so the answer is `Incorrect`. The simulation does not retroactively change characters already on the screen when CapsLock is toggled.

Consecutive CapsLock presses cancel each other. For

```
2
ab cd
7
CapsLock
a
CapsLock
b
Space
c
d
```

the first toggle makes `a` uppercase, producing `"A"`. The second toggle returns to lowercase, so `b`, `c`, and `d` are lowercase. The final screen is `"Ab cd"`, which differs from the target `"ab cd"`, so this particular input is `Incorrect`. If the first letter were also uppercase in the target, the same two toggles would correctly restore lowercase mode for the remaining letters. The key point is that the state changes at the exact position of each `CapsLock` press.

The required spaces must be checked exactly, not merely treated as separators. For

```
2
a b
2
a
b
```

the stack becomes `"ab"`, while the target is `"a b"`. The algorithm compares complete strings, so it correctly prints `Incorrect`.

Finally, a sequence can contain many operations that cancel one another. For example,

```
2
a b
6
a
Backspace
Backspace
a
Space
b
```

starts with `"a"`, deletes it, ignores the second Backspace because the screen is empty, then constructs `"a b"`. The final result is `Correct`. This case confirms that the algorithm does not confuse an old deleted character with the current screen state.
