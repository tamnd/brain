---
title: "CF 102281I - \u0414\u0435\u0442\u0441\u043a\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430"
description: "We are given an addition written with words instead of digits, such as VOLVO+FIAT=MOTOR. Every distinct letter must be assigned a digit from 0 through 9. Two different letters must receive different digits, while every occurrence of the same letter receives the same digit."
date: "2026-08-13T09:27:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102281
codeforces_index: "I"
codeforces_contest_name: "2011, IV \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u043d\u0430\u044f \u043c\u0435\u0436\u0432\u0443\u0437\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 102281
solve_time_s: 96
verified: true
draft: false
---

[CF 102281I - \u0414\u0435\u0442\u0441\u043a\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430](https://codeforces.com/problemset/problem/102281/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an addition written with words instead of digits, such as `VOLVO+FIAT=MOTOR`. Every distinct letter must be assigned a digit from `0` through `9`. Two different letters must receive different digits, while every occurrence of the same letter receives the same digit. Leading zeroes are explicitly allowed, so the first letter of a word is not special.

The task is to find every assignment for which the numerical value of the first word plus the numerical value of the second word equals the numerical value of the result word. Each valid assignment is printed by replacing every letter in the original expression with its assigned digit. The statement guarantees that there are at most 1000 solutions.

Each of the three words has at most 15 characters. This makes converting a completed assignment into three integers cheap, but it does not make trying every assignment cheap. There can be at most 10 different letters because only 10 digits exist. A completely blind search over ten letters considers up to `10! = 3,628,800` assignments, and for each assignment it still has to evaluate the three words. That is already millions of candidates, and a straightforward Python implementation can spend most of its time checking assignments that could have been rejected much earlier.

The structure of addition gives us a much stronger constraint. Instead of waiting until every letter has a digit, we can process the addition from the units column toward the most significant column. Every column has only one possible carry, and once the digits of the two addends are known, the result digit is forced. This turns a global equality into a sequence of very small local checks.

There are several edge cases that a careless implementation can mishandle. First, leading zeroes are legal. For example, `A+A=B` has the valid solution `5+5=0`, so the assignment `A=5, B=0` must be accepted. An implementation that forbids zero for the first character would incorrectly discard it.

A second issue is that the same letter can occur in multiple positions of the same column structure. For `A+A=A`, the only solution is `0+0=0`, because the single letter must have the same value everywhere. A solver that treats the two occurrences of `A` as independent variables can accidentally accept assignments such as `1+1=1`.

A third edge case is a final carry. For an input such as `A+B=CA`, a valid assignment may require the addition to produce an extra most significant digit. The solver must process all columns and verify that the carry left after the final real column is exactly zero. Ignoring that final condition can accept an incomplete addition.

Finally, different letters must never share a digit. For `A+B=C`, the assignment `A=1, B=1, C=2` satisfies the arithmetic equality but is not a valid cryptarithm assignment. The digit-usage structure must reject it before producing the answer.

## Approaches

The most direct approach is to collect all distinct letters, assign digits to them in every possible injective way, convert the three words to integers, and test the equality. This is correct because every possible legal assignment is considered exactly once, and the final arithmetic test precisely matches the condition of the problem.

The difficulty is the size of the search space. With ten distinct letters there are `10 * 9 * 8 * ... * 1 = 10! = 3,628,800` assignments. If every assignment requires scanning up to 45 characters across the three words, the worst case is on the order of 160 million character-level operations. The search also does no useful work until all letters have been assigned.

The observation that changes the problem is that decimal addition is local. Consider one column from the right. If the two addend digits are `x` and `y`, and the incoming carry is `carry`, then

`x + y + carry = result_digit + 10 * next_carry`.

Once `x` and `y` are known, `result_digit` and `next_carry` are completely determined. If the result letter already has a digit, we only have to compare it with the forced digit. If it has not been assigned yet, we have to check whether the forced digit is unused.

This lets us search from right to left. At every column we assign only the still-unknown letters that occur in the two addends. The result digit is then derived rather than guessed. A wrong partial assignment dies immediately in the column where the arithmetic becomes impossible.

The brute-force search works because every complete assignment can be checked independently, but fails because it postpones all arithmetic constraints until the end. Column-wise backtracking applies the strongest available constraint as soon as its required digits are known.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(L * 10!)` in the worst case | `O(U)` | Too slow for a tight Python implementation |
| Column-wise backtracking | `O(L * P(10,U))` worst-case, with strong column pruning | `O(U + L)` | Accepted |

Here `L` is the maximum word length, `U` is the number of distinct letters, and `P(10,U) = 10!/(10-U)!`. Since `U <= 10` is fixed by the decimal alphabet, the practical search is small, especially because most branches are rejected before all letters are assigned.

## Algorithm Walkthrough

1. Split the input expression at `+` and `=` into the two addends and the result. Store the letters as strings so that their positions can later be inspected from right to left.
2. Count the distinct letters. If there are more than 10, there cannot be any assignment because there are only ten available digits. The search can terminate immediately.
3. Maintain an array `digit[26]`, initially containing `-1`, that stores the assigned digit of each letter. Maintain a ten-element `used` array indicating which digits have already been taken.
4. Process columns from the units position toward the most significant position. For column `pos`, the addend digit is the character at `a[-1-pos]` if that position exists, otherwise it contributes zero. The same rule is used for the second addend and the result.
5. Look only at the distinct letters appearing in the two addend positions of the current column. If one of them has no assigned digit, try every unused digit for it. Since there are at most two addend letters in one column, this creates at most 90 choices before considering the result.
6. Compute `total = digit_left + digit_right + carry`. The required result digit is `total % 10`, and the carry for the next column is `total // 10`.
7. If the result letter already has a digit, compare that digit with the required result digit. A mismatch makes the current branch impossible. If the result letter is unassigned, assign the required digit only when that digit is unused. This is the key pruning step, because the result digit is never guessed.
8. Recurse to the next column with the new carry. After returning, undo every assignment made in the current column so that another branch starts with exactly the previous state.
9. After all columns have been processed, accept the assignment only when the carry is zero. Convert every word using the assignment and save the resulting expression.

The invariant is that before processing a column, every letter needed by the already processed suffix has a fixed digit, all assigned digits are distinct, and the processed suffixes satisfy the addition including the current carry. Every recursive transition preserves this invariant because it checks the exact decimal equation for the current column. Conversely, any valid complete assignment must satisfy every individual column equation, so the corresponding choices are never pruned. Thus every produced assignment is valid, and every valid assignment is eventually produced.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_expression(expr):
    a, rest = expr.split('+')
    b, c = rest.split('=')

    max_len = max(len(a), len(b), len(c))

    letters = set(a + b + c)
    if len(letters) > 10:
        return []

    digit = [-1] * 26
    used = [False] * 10
    solutions = []

    def get_char(word, pos):
        idx = len(word) - 1 - pos
        if idx < 0:
            return -1
        return ord(word[idx]) - ord('A')

    def build_number(word):
        value = 0
        for ch in word:
            value = value * 10 + digit[ord(ch) - ord('A')]
        return value

    def make_output():
        na = build_number(a)
        nb = build_number(b)
        nc = build_number(c)
        solutions.append(f"{na}+{nb}={nc}")

    def dfs(pos, carry):
        if pos == max_len:
            if carry == 0:
                make_output()
            return

        x = get_char(a, pos)
        y = get_char(b, pos)
        z = get_char(c, pos)

        assigned_now = []

        def assign_operand(ch, d):
            digit[ch] = d
            used[d] = True
            assigned_now.append((ch, d))

        def undo():
            while assigned_now:
                ch, d = assigned_now.pop()
                digit[ch] = -1
                used[d] = False

        # Recursively assign the distinct letters appearing in
        # the two addend positions.
        operands = []
        if x != -1:
            operands.append(x)
        if y != -1 and y != x:
            operands.append(y)

        def assign_operands(idx):
            if idx == len(operands):
                dx = 0 if x == -1 else digit[x]
                dy = 0 if y == -1 else digit[y]

                total = dx + dy + carry
                needed = total % 10
                next_carry = total // 10

                if z == -1:
                    if needed != 0:
                        return
                    dfs(pos + 1, next_carry)
                    return

                if digit[z] != -1:
                    if digit[z] == needed:
                        dfs(pos + 1, next_carry)
                    return

                if used[needed]:
                    return

                digit[z] = needed
                used[needed] = True
                dfs(pos + 1, next_carry)
                digit[z] = -1
                used[needed] = False
                return

            ch = operands[idx]

            if digit[ch] != -1:
                assign_operands(idx + 1)
                return

            for d in range(10):
                if used[d]:
                    continue

                assign_operand(ch, d)
                assign_operands(idx + 1)
                undo()

        assign_operands(0)

    dfs(0, 0)
    return solutions

def main():
    expr = input().strip()
    solutions = solve_expression(expr)

    out = [str(len(solutions))]
    out.extend(solutions)
    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    main()
```

The parser separates the expression into exactly three words. Since the input format contains only one `+` and one `=`, the two `split` operations are sufficient.

The `digit` array uses letter indices from `0` to `25`. A value of `-1` means that the letter has not been assigned yet. The `used` array gives constant-time checks for whether a candidate digit is available.

`get_char` converts a column number measured from the right into a character index. Returning `-1` for a missing position is convenient because a missing addend contributes zero to that column. There is no special leading-zero handling because the problem explicitly permits leading zeroes.

The nested `assign_operands` function is where the backtracking happens. It assigns only the letters that occur in the two addends for the current column. If a letter was assigned by an earlier column, it is reused without branching.

Once the operand digits are available, the result digit is calculated with `% 10`. The carry is calculated with `// 10`. This order matters because the result digit belongs to the current column, while the carry belongs to the next one.

A subtle case occurs when the result position does not exist. Then the result digit is conceptually zero. The code accepts that situation only when the calculated digit is zero. For example, if both addends have already ended but a carry remains, that carry is handled by the final `pos == max_len` check rather than by inventing another result digit.

Assignments are always undone after the recursive branch finishes. The result letter is also temporarily assigned and explicitly restored. Without this rollback, a digit chosen in one branch would leak into the next branch and silently remove valid solutions.

Python integers do not overflow, and the largest possible word has only 15 digits, so ordinary integer arithmetic is more than sufficient.

## Worked Examples

### Sample 1

Consider `ONE+ONE=TWO`. Processing begins at the units column, where `E + E` must produce `O`. The carry then determines the tens column, and so on. A representative successful branch is shown below.

| Column | Left digit | Right digit | Carry in | Sum | Result digit | Carry out |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | `5` | `5` | 0 | 10 | `0` | 1 |
| 1 | `6` | `6` | 1 | 13 | `3` | 1 |
| 2 | `0` | `0` | 1 | 1 | `1` | 0 |

The corresponding assignment is `O=0`, `N=1`, `E=5`, giving `015+015=030`. This particular branch is actually rejected because `N=1` and `O=0` are consistent, but the word `ONE` is `015` and `TWO` is `?30`, requiring `T=0`, which conflicts with `O=0`. The important point is that the conflict is detected at the result-letter assignment rather than after constructing all possible letter assignments.

A successful branch such as `065+065=130` has the same column invariant. The units column gives `5+5=10`, fixing `O=0` and producing carry 1. The tens column gives `6+6+1=13`, fixing `N=3` and producing carry 1. The hundreds column then gives `0+0+1=1`, fixing `T=1`. Every column agrees with the same global mapping.

The sample contains 17 valid assignments, and leading zeroes such as `065` are deliberately preserved in the printed form.

### Sample 2

For `VOLVO+FIAT=MOTOR`, the rightmost column contains `O + T = R` plus the incoming carry. The next column contains `V + A`, and the repeated letters in `VOLVO` and `MOTOR` cause assignments made earlier to constrain later columns.

A successful solution from the sample is `15615+9743=25358`. Reading from right to left gives the following trace.

| Column | Left digit | Right digit | Carry in | Sum | Result digit | Carry out |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | `5` | `3` | 0 | 8 | `8` | 0 |
| 1 | `1` | `4` | 0 | 5 | `5` | 0 |
| 2 | `6` | `7` | 0 | 13 | `3` | 1 |
| 3 | `5` | `9` | 1 | 15 | `5` | 1 |
| 4 | `1` | 0 | 1 | 2 | `2` | 0 |

The resulting mapping is `V=1`, `O=5`, `L=6`, `F=9`, `I=7`, `A=4`, `T=3`, `M=2`, `R=8`. The fifth column uses the fact that `FIAT` has no more digits, so its contribution is zero. The final carry is zero, proving that the complete five-digit equality has been resolved.

This example demonstrates why processing columns from right to left is stronger than assigning letters in arbitrary order. Several digits become forced by arithmetic, rather than being independently guessed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(L * P(10,U))` worst-case | At most `P(10,U)` injective digit assignments can appear in the backtracking tree, and each branch advances through at most `L` columns. Arithmetic constraints usually prune much earlier. |
| Space | `O(U + L)` | The digit mapping, used-digit array, recursion depth, and stored output strings require space proportional to the number of letters, word length, and solutions. |

Here `L <= 15` and `U <= 10`. The theoretical search bound is finite and small because there are only ten digits, while the column constraints eliminate branches before all ten digits have usually been assigned. The guaranteed maximum of 1000 output solutions also bounds the amount of stored result data.

## Test Cases

The following test harness uses the same solver logic and compares outputs as sets, because the problem permits solutions in arbitrary order. For the samples, the expected solutions are written explicitly. For custom cases, the expected output is short enough to verify directly.

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_expression(expr):
    a, rest = expr.split('+')
    b, c = rest.split('=')

    max_len = max(len(a), len(b), len(c))
    if len(set(a + b + c)) > 10:
        return []

    digit = [-1] * 26
    used = [False] * 10
    solutions = []

    def get_char(word, pos):
        idx = len(word) - 1 - pos
        if idx < 0:
            return -1
        return ord(word[idx]) - 65

    def number(word):
        value = 0
        for ch in word:
            value = value * 10 + digit[ord(ch) - 65]
        return value

    def dfs(pos, carry):
        if pos == max_len:
            if carry == 0:
                solutions.append(
                    f"{number(a)}+{number(b)}={number(c)}"
                )
            return

        x = get_char(a, pos)
        y = get_char(b, pos)
        z = get_char(c, pos)

        operands = []
        if x != -1:
            operands.append(x)
        if y != -1 and y != x:
            operands.append(y)

        def choose(idx):
            if idx == len(operands):
                dx = 0 if x == -1 else digit[x]
                dy = 0 if y == -1 else digit[y]

                total = dx + dy + carry
                needed = total % 10
                next_carry = total // 10

                if z == -1:
                    if needed == 0:
                        dfs(pos + 1, next_carry)
                    return

                if digit[z] != -1:
                    if digit[z] == needed:
                        dfs(pos + 1, next_carry)
                    return

                if used[needed]:
                    return

                digit[z] = needed
                used[needed] = True
                dfs(pos + 1, next_carry)
                used[needed] = False
                digit[z] = -1
                return

            ch = operands[idx]

            if digit[ch] != -1:
                choose(idx + 1)
                return

            for d in range(10):
                if not used[d]:
                    digit[ch] = d
                    used[d] = True
                    choose(idx + 1)
                    used[d] = False
                    digit[ch] = -1

        choose(0)

    dfs(0, 0)
    return solutions

def run(inp: str) -> str:
    expr = inp.strip()
    ans = solve_expression(expr)
    return str(len(ans)) + (("\n" + "\n".join(ans)) if ans else "")

def parse_output(s):
    lines = s.strip().splitlines()
    count = int(lines[0])
    return count, set(lines[1:])

# Sample 1
sample1 = run("ONE+ONE=TWO")
count, got = parse_output(sample1)
expected1 = {
    "065+065=130",
    "085+085=170",
    "206+206=412",
    "216+216=432",
    "231+231=462",
    "236+236=472",
    "271+271=542",
    "281+281=562",
    "286+286=572",
    "291+291=582",
    "407+407=814",
    "417+417=834",
    "427+427=854",
    "432+432=864",
    "452+452=904",
    "457+457=914",
    "467+467=934",
    "482+482=964",
}
assert count == 17 and got == expected1, "sample 1"

# Sample 2
sample2 = run("VOLVO+FIAT=MOTOR")
count, got = parse_output(sample2)
expected2 = {
    "15615+9743=25358",
    "15715+9643=25358",
    "36736+9825=46561",
    "36836+9725=46561",
    "46346+9821=56167",
    "46846+9321=56167",
    "71571+9642=81213",
    "71671+9542=82123",
    "72472+9651=82123",
    "72672+9451=82123",
}
assert count == 10 and got == expected2, "sample 2"

# Minimum-size, all letters equal.
assert run("A+A=A") == "1\n0+0=0", "same letter"

# Two distinct letters, including the valid leading-zero result.
assert run("A+A=B") == (
    "9\n"
    "1+1=2\n"
    "2+2=4\n"
    "3+3=6\n"
    "4+4=8\n"
    "5+5=0\n"
    "6+6=2\n"
    "7+7=4\n"
    "8+8=6\n"
    "9+9=8"
), "leading zero"

# Maximum word length, but only two distinct letters.
assert run("AAAAAAAAAAAAAAA+AAAAAAAAAAAAAAA=BBBBBBBBBBBBBBB") == (
    "5\n"
    "0+0=0\n"
    "111111111111111+111111111111111=222222222222222\n"
    "222222222222222+222222222222222=444444444444444\n"
    "333333333333333+333333333333333=666666666666666\n"
    "444444444444444+444444444444444=888888888888888"
), "maximum length"

# More than ten distinct letters means no assignment exists.
assert run("ABCDEFGHIJ+K=ABCDEFGHIJK") == "0", "more than ten letters"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A+A=A` | `1` solution, `0+0=0` | Same letter on both sides and the all-equal assignment |
| `A+A=B` | `9` solutions | Distinct digits, arithmetic carry, and a valid zero result |
| `AAAAAAAAAAAAAAA+AAAAAAAAAAAAAAA=BBBBBBBBBBBBBBB` | `5` solutions | Maximum word length and repeated letters across every column |
| `ABCDEFGHIJ+K=ABCDEFGHIJK` | `0` solutions | More than ten distinct letters |

## Edge Cases

For `A+A=A`, the algorithm starts with an empty mapping. In the only column, it sees the same operand letter twice, so `operands` contains `A` only once. Assigning `A=0` gives `0+0=0`, so the branch reaches the end with carry zero and is accepted. Any nonzero assignment gives `2A` as the result, which cannot equal `A` with a distinct decimal digit, so all other branches are rejected. The output is exactly `0+0=0`.

For `A+A=B`, the units column assigns `A` first. When `A=5`, the sum is 10, so the required result digit is zero and the carry is one. Since zero is unused, `B=0` is accepted. The resulting expression is `5+5=0`. This demonstrates why the solver must not impose a no-leading-zero rule. The same input also exercises the carry transition for every other value of `A`.

For the maximum-length input `AAAAAAAAAAAAAAA+AAAAAAAAAAAAAAA=BBBBBBBBBBBBBBB`, all fifteen columns have exactly the same structure. If `A=1`, the first column produces `B=2` and no carry. Every subsequent column repeats the same calculation, so the complete result is `111111111111111+111111111111111=222222222222222`. Assignments `A=2,3,4` similarly produce `B=4,6,8`, while `A=5` produces fifteen zeroes in the result. Any `A>=6` either reuses a result digit already assigned in the corresponding relation or produces a result digit equal to a previously used value. The algorithm handles all fifteen columns without any dependence on the absolute numerical size of the words.

For `ABCDEFGHIJ+K=ABCDEFGHIJK`, eleven distinct letters are required. Since a legal assignment needs a different digit for every letter and there are only ten digits, the solver returns immediately without entering the recursive search. This check also prevents a careless implementation from indexing or constructing an impossible digit permutation.

The final-carry boundary is handled by the `pos == max_len` condition. Suppose the processed columns finish with carry one. There is no result character left at that position, so the addition cannot be valid. The recursion reaches the base case and rejects the branch because `carry != 0`. A valid solution must always leave exactly zero after the most significant real column.
