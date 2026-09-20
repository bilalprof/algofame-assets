
## Gold text rule

Gradient-filled text (`background-clip: text; color: transparent`) must never carry a `text-shadow`: the shadow paints through the transparent glyphs and muddies the gold. Use a glyph-shaped `filter: drop-shadow(...)` on the element instead.
