---
title: "CF 102465A - City of Lights"
description: "We have N lights numbered from 1 through N. Initially every light is on. Each of the k commands contains a positive integer x, and that command toggles every light whose number is a multiple of x. A toggled light changes from on to off or from off to on."
date: "2026-08-09T03:35:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102465
codeforces_index: "A"
codeforces_contest_name: "2018-2019 ICPC Southwestern European Regional Programming Contest (SWERC 2018)"
rating: 0
weight: 102465
solve_time_s: 361
verified: true
draft: false
---

[CF 102465A - City of Lights](https://codeforces.com/problemset/problem/102465/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have N lights numbered from 1 through N. Initially every light is on. Each of the k commands contains a positive integer x, and that command toggles every light whose number is a multiple of x. A toggled light changes from on to off or from off to on.

The commands arrive in a fixed order, and we need the largest number of lights that are off immediately after any command. The initial state, before the first command, has zero lights off.

The constraints are small in terms of the number of commands, with k≤100, but N can reach 10 6. A direct simulation needs to touch every multiple of every command. If all 100 commands are 1, every command touches all 10 6 lights, giving 10 8 individual light updates. That is too much for a 1 second limit, especially in Python. We need to represent a whole group of lights more compactly.

The natural representation is a bitset. One bit represents one light, with bit 0 corresponding to light 1, bit 1 to light 2, and so on. The set of lights toggled by a command is then one large integer. Toggling the entire group becomes a single XOR operation, and counting the off lights becomes a population count with `int.bit_count()`. Python implements these operations on packed machine words internally, so the work is performed in optimized native code rather than one Python operation per light. Python's `int.bit_count()` directly returns the number of set bits.

There are several edge cases that are easy to mishandle. With `N=1`, a command `1` toggles the only light, so the answer is 1.

```
1
1
1
```

The output is `1`. A solution that only checks the final state and accidentally ignores the state after the command would still happen to work here, but the more general lesson is that the maximum can occur at an intermediate moment.

Repeated commands are another trap.

```
10
2
2
2
```

After the first command, lights 2, 4, 6, 8, and 10 are off, so the answer is 5. The second command turns all of them back on, but the answer remains 5. A solution that only examines the final configuration would incorrectly output 0.

The largest possible command value also needs correct boundary handling.

```
5
2
5
1
```

After command `5`, only light 5 is off. Command `1` toggles every light, giving four lights off and light 5 on. The correct output is 4. A loop that accidentally stops at `N - 1` would miss light 5.

## Approaches

The straightforward solution stores the state of every light and processes each command by walking through its multiples. For command x, we visit x,2x,3x,…, toggle each corresponding light, maintain the current number of off lights, and update the answer. This is correct because every affected light is visited exactly once for that command, and maintaining the count incrementally avoids scanning all N lights after every operation.

The problem is the worst case. If every command is `1`, each command visits N lights. With N=10 6 and k=100, that is 100⋅10 6 =10 8 light updates. The C++ reference approach can handle this simple simulation in optimized native code, but the same loop in Python is not appropriate for a 1 second limit. The official problem constraints are indeed N≤10 6, k≤100, with a 1 second time limit.

The key observation is that a command does not need to be represented as 1,000,000 separate Boolean values. It is naturally a set of positions, and set toggling is exactly XOR. We can encode the whole state of the city as one Python integer. If bit j−1 is 1, light j is off. The mask for command x has bit j−1 set exactly when x divides j. Applying the command is then simply `state ^= mask`.

There is one additional detail because constructing a million-bit mask by repeatedly doing `mask |= 1 << position` would itself perform a huge number of Python-level operations. The mask has a very regular binary pattern, so we construct it algebraically.

For m=⌊N/x⌋, the first mx bits of the desired pattern contain one set bit every x positions. The value

2 x −1 2 mx −1 ​

has binary representation consisting of m copies of the pattern `1` separated by exactly x−1 zeroes. Shifting it by x−1 positions moves those set bits to positions x−1,2x−1,…,mx−1, which correspond exactly to lights x,2x,…,mx.

The brute-force approach works because it explicitly maintains every light, but fails because the same million positions may be traversed one hundred times. The bitset observation lets us perform each entire toggle as an XOR on packed bits and count the result with a native population-count operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(kN) worst case | O(N) | Too slow in Python |
| Bitset | O(kN/w) packed-word operations | O(kN/w) | Accepted |

Here w is the machine-word width used internally by Python's arbitrary-precision integers. The actual implementation stores each command mask as a single Python integer.

## Algorithm Walkthrough

1. Read N, k, and the sequence of commands. The command order must be preserved because the question asks for the maximum during the process, not merely the final state.
2. For every distinct command value x, construct a bitmask whose set bits correspond exactly to the multiples of x not exceeding N. Let m=N//x. The expression

( 2 x −1 2 mx −1 ​ )2 x−1

produces set bits at exactly positions x−1,2x−1,…,mx−1.
3. Store the constructed masks in a dictionary. If the same command appears several times, its mask is reused instead of being constructed again.
4. Start with `state = 0`. A zero bit means the corresponding light is on, so initially every light is represented correctly.
5. Process the commands in their original order. XOR the current state with the mask of the command. XOR is the correct operation because a 1 in the command mask means that light must be toggled. XOR changes 0 to 1 and 1 to 0.
6. After each command, calculate `state.bit_count()` and update the maximum. This checks every possible moment at which the maximum can occur.

### Why it works

After processing any prefix of the commands, bit j−1 of `state` is 1 exactly when light j has been toggled an odd number of times. Every command whose value divides j contributes one XOR with that bit. An even number of toggles returns the light to its original on state, while an odd number leaves it off. Thus the set bits of `state` are exactly the currently off lights. Taking `bit_count()` therefore gives the exact number of off lights after that prefix, and taking the maximum over all prefixes gives the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    k = int(input())

    commands = [int(input()) for _ in range(k)]

    masks = {}

    def build_mask(x):
        if x in masks:
            return masks[x]

        m = n // x

        # (2^(m*x) - 1) / (2^x - 1)
        # has one bit set every x positions, starting at bit 0.
        pattern = ((1 << (m * x)) - 1) // ((1 << x) - 1)

        # Shift the set bits from positions 0, x, 2x, ...
        # to positions x-1, 2x-1, 3x-1, ...
        mask = pattern << (x - 1)

        masks[x] = mask
        return mask

    state = 0
    answer = 0

    for x in commands:
        state ^= build_mask(x)
        answer = max(answer, state.bit_count())

    print(answer)

if __name__ == "__main__":
    solve()
```

The input is read with `sys.stdin.readline`, as required for competitive programming. There is only one test case in the problem, so no outer test-case loop is needed.

`m = n // x` is the number of multiples of `x` that are valid light numbers. When `x = n`, we get `m = 1`, and the resulting mask contains only bit `n-1`, corresponding to light n. When `x = 1`, the mask contains every bit from 0 through `n-1`, so the command correctly toggles every light.

The mask construction uses only integer arithmetic. The denominator `(1 << x) - 1` represents a block of x binary ones. Dividing the all-ones integer `(1 << (m * x)) - 1` by that block produces the repeated pattern needed for the multiples. The final shift aligns the first set bit with light x, rather than light 1.

`state ^= mask` is deliberately done in the original command order. Commands commute as operations on the final state, but the maximum is taken after each prefix, so reordering commands would change the answer.

Python integers have arbitrary precision, so there is no integer overflow when the state reaches one million bits. The built-in `bit_count()` counts those set bits directly.

## Worked Examples

The provided sample is:

```
10
4
6
2
1
3
```

The relevant state is the set of lights currently off.

| Command | Mask affects | Off lights after command | Off count | Maximum |
| --- | --- | --- | --- | --- |
| 6 | 6 | {6} | 1 | 1 |
| 2 | 2, 4, 6, 8, 10 | {2, 4, 8, 10} | 4 | 4 |
| 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | {1, 3, 5, 6, 7, 9} | 6 | 6 |
| 3 | 3, 6, 9 | {1, 5, 6, 7} | 4 | 6 |

The answer is `6`. The trace shows why we must check the state after every command rather than only looking at the final state.

A second example exercises repeated commands:

```
10
2
2
2
```

| Command | Mask affects | Off lights after command | Off count | Maximum |
| --- | --- | --- | --- | --- |
| 2 | 2, 4, 6, 8, 10 | {2, 4, 6, 8, 10} | 5 | 5 |
| 2 | 2, 4, 6, 8, 10 | {} | 0 | 5 |

The same mask is reused for both commands. XORing it twice cancels the first toggle, but the intermediate state with five lights off is still considered, giving the answer `5`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(kN/w) packed-word work | Each command performs a large-integer XOR and population count over roughly N bits |
| Space | O(kN/w) | At most k masks, each containing N bits |

The largest state contains 10 6 bits, roughly 125 KB. Even keeping 100 distinct masks requires only about 12.5 MB of raw bit storage, comfortably below the 256 MB memory limit. The packed representation also avoids the 10 8 Python-level light updates that the direct simulation could require.

The mask construction uses Python's native arbitrary-precision integer operations rather than a Python loop over all multiples. This is the key implementation detail that makes the bitset approach practical under the original 1 second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    k = int(input())
    commands = [int(input()) for _ in range(k)]

    masks = {}

    def build_mask(x):
        if x in masks:
            return masks[x]

        m = n // x
        pattern = ((1 << (m * x)) - 1) // ((1 << x) - 1)
        mask = pattern << (x - 1)

        masks[x] = mask
        return mask

    state = 0
    answer = 0

    for x in commands:
        state ^= build_mask(x)
        answer = max(answer, state.bit_count())

    return answer

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        return str(solve()) + "\n"
    finally:
        sys.stdin = old_stdin

# Provided sample
assert run("""10
4
6
2
1
3
""") == "6\n", "sample 1"

# Minimum size
assert run("""1
1
1
""") == "1\n", "single light"

# Repeated commands
assert run("""10
2
2
2
""") == "5\n", "repeated command"

# Boundary command N, followed by command 1
assert run("""5
2
5
1
""") == "4\n", "boundary multiple"

# Maximum-size input, all commands equal
assert run("1000000\n100\n" + "1\n" * 100) == "1000000\n", \
    "maximum N and repeated command"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `10 / 4 / 6 2 1 3` | 6 | Provided sample and intermediate maximum |
| `1 / 1 / 1` | 1 | Minimum N and single-bit mask |
| `10 / 2 / 2 2` | 5 | Repeated toggles and intermediate state |
| `5 / 2 / 5 1` | 4 | Multiples at exactly the upper boundary |
| `1000000 / 100 / 1 ... 1` | 1000000 | Maximum N, maximum k, and repeated mask reuse |

## Edge Cases

For the minimum case,

```
1
1
1
```

we have `x = 1`, `m = 1`, and the constructed mask is `1`. XORing the initial state `0` with `1` gives `state = 1`, whose population count is 1. The algorithm returns `1`, which is the only possible maximum.

For repeated commands,

```
10
2
2
2
```

the mask for `2` represents lights 2, 4, 6, 8, and 10. The first XOR creates five set bits, so the answer becomes 5. The second XOR clears exactly those same five bits. The final state is zero, but the recorded maximum remains 5. This is why the algorithm evaluates `bit_count()` after every command.

For a command equal to N,

```
5
2
5
1
```

the first mask has only bit 4 set, representing light 5. The state therefore has one set bit. The second command has every one of the five bits set, so XOR changes the state from `10000` to `01111`. Four bits are set, giving the correct answer of 4. The construction's use of `n // x` handles the endpoint exactly.

For the maximum-size repeated case,

```
1000000
100
1
1
...
1
```

the mask for `1` is reused for all 100 commands. After every odd-numbered command all one million lights are off, while after every even-numbered command all are on. The maximum is consequently 1,000,000. The algorithm does not rebuild the million-bit mask 100 times, and the state changes are just repeated XOR operations on the same packed integer.
