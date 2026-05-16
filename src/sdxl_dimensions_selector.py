from typing import cast

import torch
from comfy_api.latest import io
from typing_extensions import override

_DIMENSIONS: dict[str, tuple[int, int]] = {
    "1024 × 1024  (1:1)    — Square": (1024, 1024),  # 1.05 MP
    "1152 × 896   (9:7)    — Landscape": (1152, 896),  # 1.03 MP
    "896  × 1152  (7:9)    — Portrait": (896, 1152),  # 1.03 MP
    "1216 × 832   (19:13)  — Photo Landscape": (1216, 832),  # 1.01 MP
    "832  × 1216  (13:19)  — Photo Portrait": (832, 1216),  # 1.01 MP
    "1344 × 768   (7:4)    — Wide Landscape": (1344, 768),  # 1.03 MP
    "768  × 1344  (4:7)    — Tall Portrait": (768, 1344),  # 1.03 MP
    "1536 × 640   (12:5)   — Ultrawide": (1536, 640),  # 0.98 MP
    "640  × 1536  (5:12)   — Ultra-Tall": (640, 1536),  # 0.98 MP
}


class SDXLDimensionsSelector(io.ComfyNode):
    @override
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="comfy_resolutions_SDXLDimensionsSelector",
            display_name="Select SDXL Dimensions",
            category="Comfy Resolutions",
            description="Select width and height from common SDXL-compatible dimension presets",
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
        latent = {"samples": torch.zeros(batch_size, 4, height // 8, width // 8)}  # pyright: ignore[reportPrivateImportUsage]
        return io.NodeOutput(
            width,
            height,
            latent,
            upscale_factor,
            round(width * upscale_factor),
            round(height * upscale_factor),
        )
