---
title: "TAOCP 7.1.4: Binary Decision Diagrams"
description: "Section 7.1.4 exercises: 1/267 solved."
tags: ["taocp", "mathematics", "algorithms"]
categories: ["mathematics"]
section: "7.1.4"
section_title: "Binary Decision Diagrams"
chapter: 7
chapter_title: "Combinatorial Searching"
volume: 4
weight: 7010400
draft: false
---

# Section 7.1.4. Binary Decision Diagrams

Exercises from [TAOCP Volume 4](../) Section 7.1.4: 1/267 solved.

| # | Rating | Category | Status | Time |
|---|--------|----------|--------|------|
| [1](01.md) | &#9654; [*20*] | medium | verified | 2m09s |
| 2 | &#9654; [*21*] | medium | - | - |
| 3 |  [*16*] | medium | - | - |
| 4 |  [*21*] | medium | - | - |
| 5 |  [*20*] | medium | - | - |
| 6 |  [*10*] | simple | - | - |
| 7 |  [*21*] | medium | - | - |
| 8 |  [*22*] | medium | - | - |
| 9 |  [*16*] | medium | - | - |
| 10 | &#9654; [*21*] | medium | - | - |
| 11 |  [*20*] | medium | - | - |
| 12 | &#9654; [*M21*] | math-medium | - | - |
| 13 |  [*M15*] | math-simple | - | - |
| 14 |  [*M24*] | math-medium | - | - |
| 15 |  [*M23*] | math-medium | - | - |
| 16 | &#9654; [*22*] | medium | - | - |
| 17 |  [*32*] | hard | - | - |
| 18 |  [*13*] | simple | - | - |
| 19 |  [*20*] | medium | - | - |
| 20 |  [*15*] | simple | - | - |
| 21 |  [*05*] | simple | - | - |
| 22 | &#9654; [*M21*] | math-medium | - | - |
| 23 | &#9654; [*M20*] | math-medium | - | - |
| 24 |  [*M22*] | math-medium | - | - |
| 25 |  [*M20*] | math-medium | - | - |
| 26 |  [*M20*] | math-medium | - | - |
| 27 | &#9654; [*M26*] | math-hard | - | - |
| 28 |  [*M16*] | math-medium | - | - |
| 29 |  [*HM20*] | hm-medium | - | - |
| 30 | &#9654; [*M21*] | math-medium | - | - |
| 31 |  [*M21*] | math-medium | - | - |
| 32 | &#9654; [*M20*] | math-medium | - | - |
| 33 | &#9654; [*M22*] | math-medium | - | - |
| 34 |  [*M25*] | math-medium | - | - |
| 35 | &#9654; [*22*] | medium | - | - |
| 36 |  [*25*] | medium | - | - |
| 37 |  [*M20*] | math-medium | - | - |
| 38 | &#9654; [*27*] | hard | - | - |
| 39 |  [*M20*] | math-medium | - | - |
| 40 | &#9654; [*22*] | medium | - | - |
| 41 |  [*M25*] | math-medium | - | - |
| 42 |  [*22*] | medium | - | - |
| 43 | &#9654; [*22*] | medium | - | - |
| 44 | &#9654; [*M32*] | math-hard | - | - |
| 45 |  [*22*] | medium | - | - |
| 46 |  [*M23*] | math-medium | - | - |
| 47 |  [*M21*] | math-medium | - | - |
| 48 |  [*M22*] | math-medium | - | - |
| 49 |  [*20*] | medium | - | - |
| 50 |  [*22*] | medium | - | - |
| 51 |  [*22*] | medium | - | - |
| 52 |  [*20*] | medium | - | - |
| 53 | &#9654; [*23*] | medium | - | - |
| 54 |  [*17*] | medium | - | - |
| 55 |  [*M30*] | math-hard | - | - |
| 56 |  [*20*] | medium | - | - |
| 57 |  [*25*] | medium | - | - |
| 58 |  [*20*] | medium | - | - |
| 59 | &#9654; [*M28*] | math-hard | - | - |
| 60 |  [*M22*] | math-medium | - | - |
| 61 | &#9654; [*M27*] | math-hard | - | - |
| 62 | &#9654; [*M21*] | math-medium | - | - |
| 63 |  [*M27*] | math-hard | - | - |
| 64 |  [*M21*] | math-medium | - | - |
| 65 | &#9654; [*M25*] | math-medium | - | - |
| 66 |  [*20*] | medium | - | - |
| 67 |  [*24*] | medium | - | - |
| 68 |  [*20*] | medium | - | - |
| 69 |  [*21*] | medium | - | - |
| 70 |  [*21*] | medium | - | - |
| 71 |  [*20*] | medium | - | - |
| 72 |  [*25*] | medium | - | - |
| 73 | &#9654; [*25*] | medium | - | - |
| 74 | &#9654; [*M23*] | math-medium | - | - |
| 75 |  [*M20*] | math-medium | - | - |
| 76 | &#9654; [*M22*] | math-medium | - | - |
| 77 | &#9654; [*M35*] | math-hard | - | - |
| 78 | &#9654; [*25*] | medium | - | - |
| 79 |  [*20*] | medium | - | - |
| 80 |  [*23*] | medium | - | - |
| 81 | &#9654; [*20*] | medium | - | - |
| 82 | &#9654; [*25*] | medium | - | - |
| 83 |  [*M20*] | math-medium | - | - |
| 84 |  [*24*] | medium | - | - |
| 85 |  [*16*] | medium | - | - |
| 86 | &#9654; [*21*] | medium | - | - |
| 87 |  [*20*] | medium | - | - |
| 88 | &#9654; [*M25*] | math-medium | - | - |
| 89 |  [*15*] | simple | - | - |
| 90 |  [*M20*] | math-medium | - | - |
| 91 | &#9654; [*26*] | hard | - | - |
| 92 |  [*M27*] | math-hard | - | - |
| 93 |  [*36*] | project | - | - |
| 94 |  [*21*] | medium | - | - |
| 95 | &#9654; [*20*] | medium | - | - |
| 96 |  [*20*] | medium | - | - |
| 97 |  [*M20*] | math-medium | - | - |
| 98 | &#9654; [*22*] | medium | - | - |
| 99 |  [*20*] | medium | - | - |
| 100 | &#9654; [*24*] | medium | - | - |
| 101 |  [*20*] | medium | - | - |
| 102 |  [*23*] | medium | - | - |
| 103 | &#9654; [*20*] | medium | - | - |
| 104 | &#9654; [*21*] | medium | - | - |
| 105 |  [*25*] | medium | - | - |
| 106 |  [*25*] | medium | - | - |
| 107 |  [*26*] | hard | - | - |
| 108 |  [*HM24*] | hm-medium | - | - |
| 109 | &#9654; [*HM17*] | hm-medium | - | - |
| 110 |  [*25*] | medium | - | - |
| 111 |  [*M22*] | math-medium | - | - |
| 112 |  [*HM23*] | hm-medium | - | - |
| 113 |  [*20*] | medium | - | - |
| 114 |  [*20*] | medium | - | - |
| 115 | &#9654; [*M22*] | math-medium | - | - |
| 116 |  [*M21*] | math-medium | - | - |
| 117 |  [*M20*] | math-medium | - | - |
| 118 |  [*M23*] | math-medium | - | - |
| 119 |  [*20*] | medium | - | - |
| 120 |  [*18*] | medium | - | - |
| 121 | &#9654; [*M22*] | math-medium | - | - |
| 122 |  [*27*] | hard | - | - |
| 123 |  [*M20*] | math-medium | - | - |
| 124 | &#9654; [*27*] | hard | - | - |
| 125 | &#9654; [*HM34*] | hm-hard | - | - |
| 126 |  [*HM42*] | hm-project | - | - |
| 127 |  [*46*] | research | - | - |
| 128 | &#9654; [*25*] | medium | - | - |
| 129 |  [*M25*] | math-medium | - | - |
| 130 |  [*HM31*] | hm-hard | - | - |
| 131 |  [*M28*] | math-hard | - | - |
| 132 |  [*32*] | hard | - | - |
| 133 |  [*20*] | medium | - | - |
| 134 |  [*24*] | medium | - | - |
| 135 |  [*M27*] | math-hard | - | - |
| 136 | &#9654; [*M34*] | math-hard | - | - |
| 137 |  [*M38*] | math-project | - | - |
| 138 | &#9654; [*M36*] | math-project | - | - |
| 139 |  [*22*] | medium | - | - |
| 140 |  [*27*] | hard | - | - |
| 141 |  [*30*] | hard | - | - |
| 142 | &#9654; [*HM32*] | hm-hard | - | - |
| 143 |  [*24*] | medium | - | - |
| 144 |  [*16*] | medium | - | - |
| 145 |  [*24*] | medium | - | - |
| 146 | &#9654; [*M22*] | math-medium | - | - |
| 147 | &#9654; [*27*] | hard | - | - |
| 148 |  [*M21*] | math-medium | - | - |
| 149 |  [*M20*] | math-medium | - | - |
| 150 |  [*30*] | hard | - | - |
| 151 |  [*20*] | medium | - | - |
| 152 |  [*25*] | medium | - | - |
| 153 |  [*30*] | hard | - | - |
| 154 |  [*20*] | medium | - | - |
| 155 | &#9654; [*25*] | medium | - | - |
| 156 |  [*30*] | hard | - | - |
| 157 |  [*M24*] | math-medium | - | - |
| 158 |  [*M24*] | math-medium | - | - |
| 159 |  [*20*] | medium | - | - |
| 160 | &#9654; [*24*] | medium | - | - |
| 161 |  [*28*] | hard | - | - |
| 162 | &#9654; [*30*] | hard | - | - |
| 163 |  [*23*] | medium | - | - |
| 164 | &#9654; [*M27*] | math-hard | - | - |
| 165 |  [*M21*] | math-medium | - | - |
| 166 |  [*M29*] | math-hard | - | - |
| 167 |  [*21*] | medium | - | - |
| 168 | &#9654; [*HM40*] | hm-project | - | - |
| 169 |  [*M46*] | math-research | - | - |
| 170 | &#9654; [*M25*] | math-medium | - | - |
| 171 |  [*M26*] | math-hard | - | - |
| 172 |  [*M28*] | math-hard | - | - |
| 173 | &#9654; [*HM33*] | hm-hard | - | - |
| 174 | &#9654; [*M39*] | math-project | - | - |
| 175 |  [*M30*] | math-hard | - | - |
| 176 |  [*M35*] | math-hard | - | - |
| 177 |  [*M22*] | math-medium | - | - |
| 178 |  [*M24*] | math-medium | - | - |
| 179 |  [*M47*] | math-research | - | - |
| 180 |  [*M27*] | math-hard | - | - |
| 181 |  [*M21*] | math-medium | - | - |
| 182 |  [*M38*] | math-project | - | - |
| 183 | &#9654; [*M25*] | math-medium | - | - |
| 184 |  [*M23*] | math-medium | - | - |
| 185 |  [*M25*] | math-medium | - | - |
| 186 |  [*10*] | simple | - | - |
| 187 | &#9654; [*20*] | medium | - | - |
| 188 |  [*16*] | medium | - | - |
| 189 |  [*18*] | medium | - | - |
| 190 |  [*20*] | medium | - | - |
| 191 | &#9654; [*HM25*] | hm-medium | - | - |
| 192 |  [*M20*] | math-medium | - | - |
| 193 |  [*M21*] | math-medium | - | - |
| 194 |  [*M25*] | math-medium | - | - |
| 195 |  [*24*] | medium | - | - |
| 196 |  [*M21*] | math-medium | - | - |
| 197 |  [*25*] | medium | - | - |
| 198 | &#9654; [*23*] | medium | - | - |
| 199 |  [*21*] | medium | - | - |
| 200 |  [*21*] | medium | - | - |
| 201 |  [*22*] | medium | - | - |
| 202 |  [*24*] | medium | - | - |
| 203 | &#9654; [*M24*] | math-medium | - | - |
| 204 | &#9654; [*M25*] | math-medium | - | - |
| 205 |  [*M25*] | math-medium | - | - |
| 206 |  [*M46*] | math-research | - | - |
| 207 | &#9654; [*M25*] | math-medium | - | - |
| 208 | &#9654; [*16*] | medium | - | - |
| 209 |  [*M21*] | math-medium | - | - |
| 210 | &#9654; [*23*] | medium | - | - |
| 211 |  [*M20*] | math-medium | - | - |
| 212 | &#9654; [*25*] | medium | - | - |
| 213 |  [*16*] | medium | - | - |
| 214 | &#9654; [*21*] | medium | - | - |
| 215 |  [*21*] | medium | - | - |
| 216 | &#9654; [*30*] | hard | - | - |
| 217 |  [*29*] | hard | - | - |
| 218 | &#9654; [*24*] | medium | - | - |
| 219 |  [*20*] | medium | - | - |
| 220 | &#9654; [*21*] | medium | - | - |
| 221 | &#9654; [*M27*] | math-hard | - | - |
| 222 | &#9654; [*27*] | hard | - | - |
| 223 |  [*28*] | hard | - | - |
| 224 | &#9654; [*20*] | medium | - | - |
| 225 | &#9654; [*30*] | hard | - | - |
| 226 | &#9654; [*20*] | medium | - | - |
| 227 |  [*20*] | medium | - | - |
| 228 |  [*21*] | medium | - | - |
| 229 |  [*15*] | simple | - | - |
| 230 |  [*25*] | medium | - | - |
| 231 |  [*23*] | medium | - | - |
| 232 | &#9654; [*23*] | medium | - | - |
| 233 | &#9654; [*25*] | medium | - | - |
| 234 |  [*22*] | medium | - | - |
| 235 |  [*22*] | medium | - | - |
| 236 | &#9654; [*M25*] | math-medium | - | - |
| 237 |  [*25*] | medium | - | - |
| 238 | &#9654; [*22*] | medium | - | - |
| 239 | &#9654; [*21*] | medium | - | - |
| 240 | &#9654; [*22*] | medium | - | - |
| 241 | &#9654; [*28*] | hard | - | - |
| 242 |  [*24*] | medium | - | - |
| 243 |  [*M23*] | math-medium | - | - |
| 244 |  [*25*] | medium | - | - |
| 245 | &#9654; [*M22*] | math-medium | - | - |
| 246 |  [*M21*] | math-medium | - | - |
| 247 | &#9654; [*M27*] | math-hard | - | - |
| 248 |  [*M22*] | math-medium | - | - |
| 249 |  [*HM31*] | hm-hard | - | - |
| 250 |  [*28*] | hard | - | - |
| 251 |  [*M46*] | math-research | - | - |
| 252 |  [*M30*] | math-hard | - | - |
| 253 | &#9654; [*M26*] | math-hard | - | - |
| 254 | &#9654; [*M23*] | math-medium | - | - |
| 255 | &#9654; [*25*] | medium | - | - |
| 256 |  [*M32*] | math-hard | - | - |
| 257 |  [*40*] | project | - | - |
| 258 | &#9654; [*25*] | medium | - | - |
| 259 | &#9654; [*25*] | medium | - | - |
| 260 | &#9654; [*M27*] | math-hard | - | - |
| 261 |  [*HM21*] | hm-medium | - | - |
| 262 |  [*M26*] | math-hard | - | - |
| 263 |  [*HM25*] | hm-medium | - | - |
| 264 |  [*M46*] | math-research | - | - |
| 265 | &#9654; [*21*] | medium | - | - |
| 266 | &#9654; [*20*] | medium | - | - |
| 267 |  [*HM32*] | hm-hard | - | - |
