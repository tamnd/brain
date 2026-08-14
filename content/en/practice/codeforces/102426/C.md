---
title: "CF 102426C - LytchenLovesJSON"
description: "The task is essentially to implement a small JSON interpreter. The input begins with one valid JSON document whose root is always an object. The document may contain nested objects, arrays, strings, numbers, booleans, and null."
date: "2026-08-14T15:23:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102426
codeforces_index: "C"
codeforces_contest_name: "The 7-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 102426
solve_time_s: 175
verified: true
draft: false
---

[CF 102426C - LytchenLovesJSON](https://codeforces.com/problemset/problem/102426/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is essentially to implement a small JSON interpreter.

The input begins with one valid JSON document whose root is always an object. The document may contain nested objects, arrays, strings, numbers, booleans, and `null`. Its formatting is arbitrary, so whitespace and line breaks cannot be used to determine where individual values end.

After the JSON document, every remaining line is a query. A query describes a path through the object graph. A name such as `birthday.year` means looking up `birthday` in the current object and then `year` in the resulting object. A suffix such as `[3]` means taking an array element or a character from a string. Several index operations may be chained, as in `a[0][2]`.

For every query we either reach a value and print it in the special format required by the statement, or report the first kind of error encountered. A missing object attribute produces `Error: no such attribute`. An index applied to anything other than a string or array produces `Error: invalid type`. A valid string or array index outside its range produces `Error: index overflow`.

The document contains at most 100 lines of at most 100 characters, so its textual size is at most about 10,000 characters. There are at most 100 queries, each at most 100 characters. These bounds are small enough that even reparsing the entire document for every query would still scan only about one million input characters in the worst case. The useful engineering choice is still to parse once, because the parsed object can then be reused by every query and the implementation becomes conceptually cleaner.

The JSON grammar also means a general string tokenizer is necessary. A JSON value can cross several physical lines, and whitespace can appear between any structural tokens. A parser based on `split`, regular expressions over individual lines, or assumptions about indentation can silently fail.

Strings need special treatment because their escape sequences are part of the problem's observable behavior. For example, consider:

```
{"s":"a\\nb"}
s
s[1]
```

The string contains the two characters backslash and `n` in its middle, rather than an actual newline. The required output for `s` is `a\nb`, with the escape sequence preserved. A parser that blindly uses Python's normal JSON decoder would turn `\n` into a newline and would produce the wrong representation.

A second subtle case is an escaped quote:

```
{"s":"a\"b"}
s
s[1]
```

The value is `a"b`, so the output is `a"b` and the indexed character is `"`. Treating the quote as the end of the string would corrupt the parse.

An index can also be applied to a string rather than an array:

```
{"s":"abc"}
s[0]
s[3]
```

The correct output is:

```
a
Error: index overflow
```

A careless implementation using `if index > len(s)` instead of `if index >= len(s)` would incorrectly accept `s[3]`.

Finally, an attribute lookup can follow an indexed primitive:

```
{"a":[10]}
a[0].x
```

The result is:

```
Error: no such attribute
```

After `a[0]` the current value is the number `10`, which has no object attributes. This is different from applying an index to the number itself, which would be an `invalid type` error.

## Approaches

The most direct solution is to parse the JSON document and immediately answer each query. A naive implementation can even parse the entire JSON document independently for every query. Since the document has at most 10,000 characters and there are at most 100 queries, that approach performs at most about 1,000,000 character-level parsing operations, plus query processing. Under these constraints, it is actually fast enough.

The weakness of that approach is repeated work. Every query starts from exactly the same root object, so rebuilding the same object graph up to 100 times has no algorithmic benefit.

The useful observation is that the JSON document is immutable throughout the input. Once it has been converted into a tree of objects, arrays, and primitive values, every query is simply a walk through that same tree. We can parse the document exactly once, keep each object as a dictionary and each array as a list, and then interpret each query against the stored structure.

The parser itself is a recursive descent parser. JSON has a particularly convenient recursive structure: an object contains key-value pairs, an array contains values, and a value can recursively be another object or array. Each parser function consumes characters from a shared position and returns both the parsed value and the new position.

The only nonstandard part is string handling. Instead of asking Python's JSON library to decode strings, the parser handles escapes itself. The escapes `\t`, `\\`, `\/`, and `\"` are converted to their corresponding characters, while other escape sequences remain literal because the output specification requires them to be preserved. This also gives string indexing the exact representation expected by the problem.

The two approaches can be compared as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Reparse the JSON for every query | O(QS + QL) | O(S) | Accepted under these constraints |
| Parse once, answer queries on the tree | O(S + QL) | O(S) | Accepted, preferred |

Here `S` is the JSON document length, `Q` is the number of queries, and `L` is the maximum query length.

## Algorithm Walkthrough

1. Read all input lines and concatenate them into one character stream. We cannot decide where the JSON document ends by looking at lines because the document may contain arbitrary formatting and line breaks.
2. Parse the root value with a recursive descent JSON parser. The parser skips JSON whitespace before every value, then dispatches according to the first character. A `{` starts an object, `[` starts an array, `"` starts a string, `t` or `f` starts a boolean, `n` starts `null`, and a sign or digit starts a number.
3. Represent every parsed value as a pair containing its type and its data. Objects store a dictionary from keys to values, arrays store a list of values, strings store their processed character representation, numbers store floating-point values, and primitive booleans and `null` are stored directly.
4. After parsing the root object, use the parser's current character position to find the remaining query lines. This is safer than trying to identify the last JSON line using braces or indentation because the parser already knows exactly where the root value ended.
5. Split each query at `.` to obtain its attribute-access segments. Within each segment, first read the alphabetic attribute name and then read every `[index]` suffix attached to it.
6. Start every query with the root object. For each attribute name, check whether the current value is an object and whether the requested key exists. If either condition fails, print `Error: no such attribute` and stop processing that query.
7. After successfully obtaining the attribute value, process its index operations from left to right. An index is valid only when the current value is a string or an array. Otherwise print `Error: invalid type`.
8. For a valid string or array, compare the requested index against its length. An index is legal exactly when `0 <= index < length`. If it is outside that range, print `Error: index overflow`; otherwise replace the current value with the selected element.
9. Once the complete query has been consumed, serialize the resulting value according to its type. Numbers use fixed-point notation with two digits after the decimal point. Arrays and objects are serialized recursively, and object keys are sorted lexicographically before their key-value pairs are printed.

The invariant throughout query evaluation is that `current` is exactly the JSON value reached by the prefix of the query processed so far. Attribute processing changes it to the corresponding child of the current object, while index processing changes it to the corresponding element or character. Since each operation is performed only after checking the current type and bounds, every successful transition is a valid edge in the JSON object graph. If an operation cannot be performed, the reported error corresponds exactly to the first invalid operation.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Parser:
    def __init__(self, text):
        self.s = text
        self.n = len(text)
        self.i = 0

    def skip_ws(self):
        while self.i < self.n and self.s[self.i] in " \t\r\n":
            self.i += 1

    def parse(self):
        self.skip_ws()
        c = self.s[self.i]

        if c == '{':
            return self.parse_object()
        if c == '[':
            return self.parse_array()
        if c == '"':
            return ("string", self.parse_string())
        if c == 't':
            self.i += 4
            return ("bool", True)
        if c == 'f':
            self.i += 5
            return ("bool", False)
        if c == 'n':
            self.i += 4
            return ("null", None)

        return self.parse_number()

    def parse_string(self):
        self.i += 1
        result = []

        while True:
            c = self.s[self.i]
            self.i += 1

            if c == '"':
                return ''.join(result)

            if c != '\\':
                result.append(c)
                continue

            esc = self.s[self.i]
            self.i += 1

            if esc == 't':
                result.append('\t')
            elif esc == '\\':
                result.append('\\')
            elif esc == '/':
                result.append('/')
            elif esc == '"':
                result.append('"')
            else:
                # The statement requires other escape sequences
                # to be kept as written.
                result.append('\\')
                result.append(esc)

    def parse_number(self):
        start = self.i

        if self.s[self.i] == '-':
            self.i += 1

        while self.i < self.n and self.s[self.i].isdigit():
            self.i += 1

        if self.i < self.n and self.s[self.i] == '.':
            self.i += 1
            while self.i < self.n and self.s[self.i].isdigit():
                self.i += 1

        if self.i < self.n and self.s[self.i] in 'eE':
            self.i += 1
            if self.s[self.i] in '+-':
                self.i += 1
            while self.i < self.n and self.s[self.i].isdigit():
                self.i += 1

        return ("number", float(self.s[start:self.i]))

    def parse_object(self):
        self.i += 1
        obj = {}
        self.skip_ws()

        if self.s[self.i] == '}':
            self.i += 1
            return ("object", obj)

        while True:
            self.skip_ws()
            key = self.parse_string()

            self.skip_ws()
            self.i += 1  # ':'

            value = self.parse()
            obj[key] = value

            self.skip_ws()
            if self.s[self.i] == '}':
                self.i += 1
                return ("object", obj)

            self.i += 1  # ','

    def parse_array(self):
        self.i += 1
        arr = []
        self.skip_ws()

        if self.s[self.i] == ']':
            self.i += 1
            return ("array", arr)

        while True:
            arr.append(self.parse())
            self.skip_ws()

            if self.s[self.i] == ']':
                self.i += 1
                return ("array", arr)

            self.i += 1  # ','

def format_value(value):
    typ, data = value

    if typ == "bool":
        return "true" if data else "false"

    if typ == "number":
        return f"{data:.2f}"

    if typ == "string":
        return data

    if typ == "null":
        return "null"

    if typ == "array":
        return "[ " + ", ".join(format_value(x) for x in data) + " ]"

    # object
    items = []
    for key in sorted(data):
        items.append(f'"{key}": {format_value(data[key])}')
    return "{ " + ", ".join(items) + " }"

def answer_query(root, query):
    current = root

    for part in query.split('.'):
        p = 0

        while p < len(part) and part[p].isalpha():
            p += 1

        key = part[:p]

        if current[0] != "object" or key not in current[1]:
            return "Error: no such attribute"

        current = current[1][key]

        while p < len(part):
            # part[p] must be '[' because the input is guaranteed valid.
            p += 1
            start = p

            while p < len(part) and part[p].isdigit():
                p += 1

            index = int(part[start:p])
            p += 1  # ']'

            if current[0] not in ("string", "array"):
                return "Error: invalid type"

            if index >= len(current[1]):
                return "Error: index overflow"

            if current[0] == "string":
                current = ("string", current[1][index])
            else:
                current = current[1][index]

    return format_value(current)

def main():
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    text = ''.join(lines)

    parser = Parser(text)
    root = parser.parse()

    # The parser stops exactly after the JSON document.
    rest = text[parser.i:]

    queries = rest.splitlines()
    out = []

    for query in queries:
        query = query.strip()
        if query:
            out.append(answer_query(root, query))

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    main()
```

The `Parser` class maintains one cursor, `self.i`, into the complete input stream. Every parsing function consumes exactly the characters belonging to its value. Recursive calls are what naturally handle nesting, so an object containing an array containing another object requires no special-case depth logic.

`parse_string` deserves particular attention. The four escape forms that the output rules explicitly care about are converted into their actual characters. Other escapes are retained with their leading backslash. In particular, `\u25A0` stays as the six-character sequence `\u25A0`, matching the required output behavior rather than Python's Unicode decoding behavior.

`parse_number` consumes the optional sign, integer part, fractional part, and exponent independently. The input is guaranteed to contain valid JSON, so the parser does not need to validate every malformed-number case.

The query evaluator deliberately checks the attribute before processing its brackets. A query such as `missing[0]` must report a missing attribute rather than an invalid index type, because there is no value on which the index could operate.

The index boundary check uses `index >= len(current[1])`. Since indices are guaranteed nonnegative, there is no separate lower-bound case. Python itself has negative indexing, so explicitly rejecting negative indices would be necessary in a less restricted input format, but here every query index is already nonnegative.

The serializer recursively formats arrays and objects. Object keys are sorted at output time, because the input order is not necessarily the required output order. Numeric values are formatted with `:.2f`, which provides exactly two digits after the decimal point.

## Worked Examples

The supplied statement contains one large sample. The excerpt in the prompt appears to have lost or corrupted part of the sample around the final `teammates` queries, so the following trace uses the unambiguous portion of that sample.

For the query `grades[4][1]`, the relevant part of the document is:

```
"grades": [90, 80, 88, 100, [55, 80]]
```

The evaluation proceeds as follows.

| Step | Operation | Current value |
| --- | --- | --- |
| 1 | Start at root | object |
| 2 | Access `grades` | `[90, 80, 88, 100, [55, 80]]` |
| 3 | Apply `[4]` | `[55, 80]` |
| 4 | Apply `[1]` | `80` |
| 5 | Format number | `80.00` |

The key invariant is visible here: after every operation, `current` is precisely the value described by the processed prefix of the query. The second index operates on the array obtained from the first index, not on the original `grades` array.

For a second example, consider:

```
{
"a": {
"z": 1,
"x": [10, 20]
},
"s": "abc"
}
a.x[1]
s[2]
a.x[2]
a.x[0].missing
```

The first query follows an object edge, another object edge, an array edge, and finally reaches the number `20`.

| Step | Operation | Current value |
| --- | --- | --- |
| 1 | Start at root | object |
| 2 | Access `a` | object |
| 3 | Access `x` | `[10, 20]` |
| 4 | Apply `[1]` | `20` |
| 5 | Format | `20.00` |

For `s[2]`, the string is indexed directly and produces `c`. For `a.x[2]`, the array has length two, so index `2` is outside the legal range `0` through `1`, producing `Error: index overflow`. For `a.x[0].missing`, the index succeeds and leaves the current value as the number `10`; the following attribute lookup cannot find an object attribute and produces `Error: no such attribute`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S + QL + S log S) | Parsing costs O(S), queries cost O(QL), and sorting object keys during serialization costs at most O(S log S) across the stored objects |
| Space | O(S) | The parsed JSON tree stores the document's values, keys, arrays, and nested objects |

Here `S` is at most about 10,000 characters, `Q` is at most 100, and `L` is at most 100. Even the repeated-parsing approach would only scan roughly one million document characters, while the chosen implementation parses once and reuses the resulting tree. The memory usage is comfortably below 128 MB.

## Test Cases

The test harness below assumes the submitted solution is saved as `solution.py` and exposes the `main` entry point. The helper invokes that exact program, which makes the assertions test the same parser, query evaluator, and serializer used for submission.

```python
import subprocess
import sys

def run(inp: str) -> str:
    result = subprocess.run(
        [sys.executable, "solution.py"],
        input=inp,
        text=True,
        capture_output=True,
        check=True
    )
    return result.stdout

# Provided sample core
sample1 = r'''{
"name": "Lchen",
"gender": false,
"height": 1.60e+2,
"birthday": {
"year": 2000,
"month": 1,
"day": 1,
"aggregate": [2000, 1, 1]
},
"grades": [90, 80, 88, 100, [55, 80]],
"laboratory": null
}
name
name[0]
name.gender
gender
gender[1]
height
birthday.year
grades[2]
grades[4]
grades[4][1]
laboratory
grades[5]
'''

assert run(sample1) == (
    "Lchen\n"
    "L\n"
    "Error: no such attribute\n"
    "false\n"
    "Error: invalid type\n"
    "160.00\n"
    "2000.00\n"
    "88.00\n"
    "[ 55.00, 80.00 ]\n"
    "80.00\n"
    "null\n"
    "Error: index overflow"
), "provided sample core"

# Custom 1: minimum-size object, missing attribute, invalid index type.
case1 = '''{"a":0}
a
b
a[0]
'''
assert run(case1) == (
    "0.00\n"
    "Error: no such attribute\n"
    "Error: invalid type"
), "minimum object and error types"

# Custom 2: nested arrays and string escape handling.
case2 = r'''{
"a": [[1, 2], []],
"s": "A\\B"
}
a[0][1]
a[1][0]
s[1]
'''
assert run(case2) == (
    "2.00\n"
    "Error: index overflow\n"
    "\\"
), "nested indexing and backslash"

# Custom 3: boundary index, object key sorting, exponent and negative number.
case3 = '''{
"z": 3,
"a": {
"y": 2,
"x": [-12.5e0, 3]
}
}
a
a.x[0]
a.x[2]
z
'''
assert run(case3) == (
    '{ "x": [ -12.50, 3.00 ], "y": 2.00 }\n'
    "-12.50\n"
    "Error: index overflow\n"
    "3.00"
), "sorting, exponent and upper-bound index"

# Custom 4: maximum number of JSON lines and maximum number of queries.
keys = [chr(ord('a') + i) for i in range(26)]
keys += ['a' + chr(ord('a') + i) for i in range(26)]
keys += ['b' + chr(ord('a') + i) for i in range(26)]
keys += ['c' + chr(ord('a') + i) for i in range(20)]

json_lines = ['{']
for i, key in enumerate(keys):
    json_lines.append(f'"{key}": 7' + (',' if i + 1 < len(keys) else ''))
json_lines.append('}')

# Add enough repeated queries to reach the 100-query limit.
queries = [keys[i % len(keys)] for i in range(100)]
max_case = '\n'.join(json_lines + queries) + '\n'

expected = ''.join("7.00\n" for _ in range(100)).rstrip('\n')
assert run(max_case) == expected, "maximum query count and large document"
```

The custom cases exercise different failure modes and structural properties.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `{"a":0}` with `a`, `b`, `a[0]` | `0.00`, missing attribute, invalid type | Minimum-size object and error precedence |
| Nested arrays with `"A\\B"` | `2.00`, overflow, `\` | Multiple indices and string escape handling |
| Nested object with `[-12.5e0,3]` | Sorted object, `-12.50`, overflow, `3.00` | Numeric parsing, serialization, key sorting, upper boundary |
| 100-line document with 100 queries | 100 lines of `7.00` | Maximum query count and large-document handling |

## Edge Cases

For an escaped string, consider:

```
{"s":"a\"b"}
s
s[1]
```

The parser enters the string after the first quote. When it sees `\"`, it consumes both characters and appends a literal quote rather than terminating the string. The stored value is `a"b`, so the first query prints `a"b` and the second prints `"`. A parser that searches for the next raw quote would terminate the string too early.

For an escape sequence that should remain textual, consider:

```
{"s":"x\u25A0y"}
s
```

The parser sees `\u`, recognizes that it is not one of the four escape forms that should be decoded, and stores both the backslash and `u`, followed by the remaining digits as ordinary characters. The resulting output is `x\u25A0y`. Using `json.loads` directly would instead create a Unicode black-square character and would violate the specified output behavior.

For string indexing, consider:

```
{"s":"abc"}
s[0]
s[2]
s[3]
```

The first two queries select `a` and `c`. The third sees `index == len(s)`, so it reports `Error: index overflow`. The same condition applies to arrays. The legal interval is half-open, `[0, length)`.

For invalid index types, consider:

```
{"x":false,"y":null,"z":{"a":1}}
x[0]
y[0]
z[0]
```

All three queries produce `Error: invalid type`. Boolean, `null`, and object values are not indexable. The parser does not try to interpret Python-specific operations such as indexing a dictionary or a boolean.

For a missing attribute after a successful index, consider:

```
{"a":[10]}
a[0].x
```

`a` resolves to an array, `[0]` resolves to the number `10`, and `.x` then asks for an attribute of that number. Since only objects have attributes, the correct result is `Error: no such attribute`. The implementation checks the current value's type before looking in its dictionary.

For nested arrays, consider:

```
{"a":[[[7]]]}
a[0][0][0]
```

The first index changes the current value from the outer array to the middle array, the second changes it to the inner array, and the third reaches `7`, which is printed as `7.00`. Processing brackets sequentially is what makes an arbitrary number of chained indices work without special cases.

For object formatting, consider:

```
{"z":1,"a":2}
a
```

The output is:

```
{ "a": 2.00, "z": 1.00 }
```

The input order is irrelevant. The serializer sorts the dictionary keys before constructing the output, which is necessary because JSON object order in the input is not guaranteed to match the required lexicographic order.
