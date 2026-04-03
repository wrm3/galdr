# Vision-First Guardrail (C-007)

This rule fires on EVERY response when working on Hieroglyphics experiments.

## The Rule

If any proposed language model architecture uses `nn.Embedding(vocab_size, embed_dim)` on
integer glyph IDs as its PRIMARY input pathway, **STOP immediately** and flag this as off-track.

The language model MUST consume one of:
1. Pre-computed 512-dim embeddings from the vision encoder (GlyphResNet18)
2. Glyph images processed through the vision encoder in the forward pass

## Why This Rule Exists

POC020 drifted into training a standard next-token predictor on integer glyph ID sequences.
This was architecturally identical to GPT-2 with a different vocabulary mapping. The glyph
images, metadata bars, and vision encoder were completely bypassed. Task 802 proved this
approach provides no compression advantage over BPE (ratio ~1.03-1.10).

The visual representation IS the compression mechanism. If the LM doesn't see it,
the experiment is testing nothing unique to Hieroglyphics.

## How to Check

Before implementing or reviewing any LM code, verify:

1. Where does the LM get its input embeddings?
   - GOOD: `embeddings = vision_encoder(glyph_images)` or loading pre-computed vision embeddings
   - BAD: `embeddings = self.embedding(glyph_ids)` where glyph_ids are integers

2. Are glyph images rendered with metadata bars during training data preparation?
   - GOOD: Glyphs include top/left/bottom metadata bars (37 bits of information)
   - BAD: Only semantic core patterns, or no images at all

3. Does the training pipeline include the vision encoder?
   - GOOD: Vision encoder produces embeddings that feed into the LM
   - BAD: Vision encoder is only used for a separate embedding store, not LM training

## Exception

A baseline/control model using nn.Embedding on integer IDs is EXPECTED as part of the
A/B comparison (Task 502/504). This is the control, not the experiment. Both must exist.

## Reference

- `PROJECT_VISION.md` — full rationale
- `.galdr/CONSTRAINTS.md` — C-007 definition
- `.galdr/experiments/HYPOTHESIS.md` — HYP-001 (vision embeddings carry more information)
