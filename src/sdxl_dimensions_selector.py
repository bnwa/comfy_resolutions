from typing import cast

import torch
from comfy_api.latest import io
from typing_extensions import override

_DIMENSIONS: dict[str, tuple[int, int]] = {
    "1024 × 1024  (1:1)": (1024, 1024),
    "1152 × 896   (9:7)": (1152, 896),
    "896  × 1152  (7:9)": (896, 1152),
    "1216 × 832  (19:13)": (1216, 832),
    "832  × 1216 (13:19)": (832, 1216),
    "1344 × 768   (7:4)": (1344, 768),
    "768  × 1344  (4:7)": (768, 1344),
    "1536 × 640  (12:5)": (1536, 640),
    "640  × 1536  (5:12)": (640, 1536),
}


class SDXLDimensionsSelector(io.ComfyNode):
    @override
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="comfy_combos_SDXLDimensionsSelector",
            display_name="Select SDXL Dimensions",
            category="Comfy Combos",
            description="Select width and height from common SDXL-compatible dimension presets",
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
        latent = {"samples": torch.zeros(batch_size, 4, height // 8, width // 8)}  # pyright: ignore[reportPrivateImportUsage]
        return io.NodeOutput(
            width,
            height,
            latent,
            upscale_factor,
            round(width * upscale_factor),
            round(height * upscale_factor),
        )
