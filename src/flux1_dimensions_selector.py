from typing import cast

import torch
from comfy_api.latest import io
from typing_extensions import override

# Flux.1 Dev recommended dimension presets.
#
# Derived from target aspect ratio × megapixel budget, rounded to 64 for
# GPU tensor-core alignment (or to 16 where 64-rounding would distort the
# ratio, e.g. 4:3 and 16:9).  All dimensions are at least multiples of 16,
# matching the BFL reference implementation (VAE 8× downsample × 2×2 patch
# embedding).
#
# The ~1 MP set is the community-standard Flux resolution table (ControlAltAI
# calculator, default divisor 64).  The ~2 MP set covers the community-
# validated high-quality sweet spot; quality degrades above ~2 MP without a
# hires-fix / upscale second pass.
_DIMENSIONS: dict[str, tuple[int, int]] = {
    # ── ~1 MP: community-standard Flux.1 Dev resolutions ────────────
    # Key format: {w:<4} × {h:<4}  {ratio:<7} — {label}
    # Columns: × at 5 · ( at 13 · — at 21 · label at 23
    "1024 × 1024  (1:1)   — Square": (1024, 1024),  # 1.05 MP
    "1152 × 896   (9:7)   — Landscape": (1152, 896),  # 1.03 MP
    "896  × 1152  (7:9)   — Portrait": (896, 1152),  # 1.03 MP
    "1152 × 864   (4:3)   — Classic Landscape": (1152, 864),  # 1.00 MP
    "864  × 1152  (3:4)   — Classic Portrait": (864, 1152),  # 1.00 MP
    "1216 × 832   (3:2)   — Photo Landscape": (1216, 832),  # 1.01 MP
    "832  × 1216  (2:3)   — Photo Portrait": (832, 1216),  # 1.01 MP
    "1344 × 768   (7:4)   — Wide Landscape": (1344, 768),  # 1.03 MP
    "768  × 1344  (4:7)   — Tall Portrait": (768, 1344),  # 1.03 MP
    "1280 × 720   (16:9)  — Widescreen": (1280, 720),  # 0.92 MP
    "720  × 1280  (9:16)  — Vertical": (720, 1280),  # 0.92 MP
    "1536 × 640   (12:5)  — Ultrawide": (1536, 640),  # 0.98 MP
    "640  × 1536  (5:12)  — Ultra-Tall": (640, 1536),  # 0.98 MP
    # ── ~2 MP: high quality, community sweet spot ───────────────────
    "1408 × 1408  (1:1)   — HD Square": (1408, 1408),  # 1.98 MP
    "1728 × 1152  (3:2)   — HD Landscape": (1728, 1152),  # 1.99 MP
    "1152 × 1728  (2:3)   — HD Portrait": (1152, 1728),  # 1.99 MP
    "1920 × 1088  (~16:9) — Full HD Widescreen": (1920, 1088),  # 2.09 MP
    "1088 × 1920  (~9:16) — Full HD Vertical": (1088, 1920),  # 2.09 MP
}


class Flux1DimensionsSelector(io.ComfyNode):
    @override
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="comfy_resolutions_Flux1DimensionsSelector"
            display_name="Select Flux.1 Dimensions",
            category="Comfy Resolutions"
            description="Select width and height from common Flux.1-compatible dimension presets. Uses 16-channel Flux VAE latent space.",
            inputs=[
                io.Combo.Input(
                    "dimensions",
                    display_name="Dimensions",
                    options=list(_DIMENSIONS.keys()),
                ),
                io.Float.Input(
                    "upscale_factor",
                    display_name="Upscale Factor",
                    default=2.0,
                    min=1.0,
                    max=8.0,
                    step=0.25,
                ),
                io.Int.Input(
                    "batch_size",
                    display_name="Batch Size",
                    default=1,
                    min=1,
                    step=1,
                ),
            ],
            outputs=[
                io.Int.Output("WIDTH", display_name="width"),
                io.Int.Output("HEIGHT", display_name="height"),
                io.Latent.Output("LATENT", display_name="latent"),
                io.Float.Output("UPSCALE_FACTOR", display_name="upscale factor"),
                io.Int.Output("UPSCALED_WIDTH", display_name="upscaled width"),
                io.Int.Output("UPSCALED_HEIGHT", display_name="upscaled height"),
            ],
        )

    @override
    @classmethod
    def execute(cls, **inputs) -> io.NodeOutput:  # type: ignore[no-untyped-def]  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        batch_size = cast(int, inputs["batch_size"])
        width, height = _DIMENSIONS[inputs["dimensions"]]
        upscale_factor = cast(float, inputs["upscale_factor"])
        latent = {"samples": torch.zeros(batch_size, 16, height // 8, width // 8)}  # pyright: ignore[reportPrivateImportUsage]
        return io.NodeOutput(
            width,
            height,
            latent,
            upscale_factor,
            round(width * upscale_factor),
            round(height * upscale_factor),
        )
