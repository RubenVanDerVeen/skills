# Hedging: three-way classification

Regex cannot tell these apart. When a `focsi-cautious` finding fires, classify the word in context:

| Class | Signals | Verdict |
|---|---|---|
| Hedge | suggest, indicate, appear to, may, might, likely, tend to, generally | Fine in a claim context; info note at most outside one |
| Non-hedge | can (ability), must (requirement), should (recommendation), cannot | Fine as-is; never flag |
| Context-dependent | proves, clearly, obviously, undoubtedly, always, never, demonstrates | Flag only when the sentence asserts a result claim; suppress in math, definitions, and universal-quantifier statements |

Examples:

- "The valve must close within 10 ms." Non-hedge (requirement). Keep.
- "This proves the model is correct." Context-dependent result claim. Suggest "These results indicate..." unless the proof is formal.
- "Always, the pressure drops." Universal quantifier in a math claim. Suppress.

Rule of thumb: hedge strength should match evidence strength. One experiment rarely proves anything; it suggests or demonstrates.