from typing import cast

import torch
from comfy_api.latest import io
from typing_extensions import override

_DIMENSIONS: dict[str, tuple[int, int]] = {
    # ── 1024 tier (~1 MP) ──────────────────────
    "1024 × 1024  (1:1)   — Square": (1024, 1024),  # 1.05 MP
    "1152 × 896   (9:7)   — Landscape": (1152, 896),  # 1.03 MP
    "896  × 1152  (7:9)   — Portrait": (896, 1152),  # 1.03 MP
    "1152 × 864   (4:3)   — Classic Landscape": (1152, 864),  # 1.00 MP
    "864  × 1152  (3:4)   — Classic Portrait": (864, 1152),  # 1.00 MP
    "1248 × 832   (3:2)   — Photo Landscape": (1248, 832),  # 1.04 MP
    "832  × 1248  (2:3)   — Photo Portrait": (832, 1248),  # 1.04 MP
    "1280 × 720   (16:9)  — Widescreen": (1280, 720),  # 0.92 MP
    "720  × 1280  (9:16)  — Vertical": (720, 1280),  # 0.92 MP
    "1344 × 576   (21:9)  — Ultrawide": (1344, 576),  # 0.77 MP
    "576  × 1344  (9:21)  — Ultra-Tall": (576, 1344),  # 0.77 MP
    # ── 1280 tier (~1.6 MP) ────────────────────
    "1280 × 1280  (1:1)   — HD Square": (1280, 1280),  # 1.64 MP
    "1440 × 1120  (9:7)   — HD Landscape": (1440, 1120),  # 1.61 MP
    "1120 × 1440  (7:9)   — HD Portrait": (1120, 1440),  # 1.61 MP
    "1472 × 1104  (4:3)   — HD Classic Landscape": (1472, 1104),  # 1.63 MP
    "1104 × 1472  (3:4)   — HD Classic Portrait": (1104, 1472),  # 1.63 MP
    "1536 × 1024  (3:2)   — HD Photo Landscape": (1536, 1024),  # 1.57 MP
    "1024 × 1536  (2:3)   — HD Photo Portrait": (1024, 1536),  # 1.57 MP
    "1536 × 864   (16:9)  — HD Widescreen": (1536, 864),  # 1.33 MP
    "864  × 1536  (9:16)  — HD Vertical": (864, 1536),  # 1.33 MP
    "1680 × 720   (21:9)  — HD Ultrawide": (1680, 720),  # 1.21 MP
    "720  × 1680  (9:21)  — HD Ultra-Tall": (720, 1680),  # 1.21 MP
    # ── 1536 tier (~2.4 MP) ────────────────────
    "1536 × 1536  (1:1)   — 2K Square": (1536, 1536),  # 2.36 MP
    "1728 × 1344  (9:7)   — 2K Landscape": (1728, 1344),  # 2.32 MP
    "1344 × 1728  (7:9)   — 2K Portrait": (1344, 1728),  # 2.32 MP
    "1728 × 1296  (4:3)   — 2K Classic Landscape": (1728, 1296),  # 2.24 MP
    "1296 × 1728  (3:4)   — 2K Classic Portrait": (1296, 1728),  # 2.24 MP
    "1872 × 1248  (3:2)   — 2K Photo Landscape": (1872, 1248),  # 2.34 MP
    "1248 × 1872  (2:3)   — 2K Photo Portrait": (1248, 1872),  # 2.34 MP
    "2048 × 1152  (16:9)  — 2K Widescreen": (2048, 1152),  # 2.36 MP
    "1152 × 2048  (9:16)  — 2K Vertical": (1152, 2048),  # 2.36 MP
    "2016 × 864   (21:9)  — 2K Ultrawide": (2016, 864),  # 1.74 MP
    "864  × 2016  (9:21)  — 2K Ultra-Tall": (864, 2016),  # 1.74 MP
}


class ZImageDimensionsSelector(io.ComfyNode):
    @override
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="comfy_combos_ZImageDimensionsSelector",
            display_name="Select Z-Image Dimensions",
            category="Comfy Combos",
            description="Select width and height from official Z-Image dimension presets across 1024, 1280, and 1536 tiers (covers base and Turbo variants). Uses 16-channel VAE latent space with 8× spatial compression.",
            inputs=[
                io.Combo.Input(
                    "dimensions",
                    options=list(_DIMENSIONS.keys()),
                ),
                io.Float.Input(
                    "upscale_factor",
                    default=2.0,
                    min=1.0,
                    max=8.0,
                    step=0.25,
                ),
                io.Int.Input(
                    "batch_size",
                    display_name="Batch",
                    default=1,
                    min=1,
                    step=1,
                ),
            ],
            outputs=[
                io.Int.Output(display_name="width"),
                io.Int.Output(display_name="height"),
                io.Latent.Output("latent"),
                io.Float.Output(display_name="upscale factor"),
                io.Int.Output(display_name="upscaled width"),
                io.Int.Output(display_name="upscaled height"),
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
