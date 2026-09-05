# Use Smart Input Pattern Recognition Instead of Explicit Subcommands

We decided to route user intent dynamically based on input format rather than requiring explicit subcommands like `ld add` or `ld tag`. Queries starting with `http://` or `https://` are treated as bookmark creation workflows, queries prefixed with `#` navigate tags, and all other text acts as a title/description search phrase. This minimizes keystrokes and cognitive overhead in a launcher environment, trading away explicit namespace separation for immediate intent recognition.

## Considered Options

- **Explicit subcommands (`ld search ...`, `ld add ...`, `ld tag ...`)**: Standard CLI style, unambiguous routing, but slower to type and adds redundant prefixes in a quick-launcher context.
- **Smart pattern recognition**: Automatically distinguishes URL addition and tag exploration by regex / prefix checks while falling back to bookmark search.
