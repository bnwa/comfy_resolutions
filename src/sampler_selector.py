import comfy.samplers
from comfy_api.latest import io
from typing_extensions import override


class SamplerSelector(io.ComfyNode):
    @override
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            category="Comfy Combos",
            description="Select a sampler from a dropdown",
            display_name="Select Sampler",
            node_id="comfy_combos_SamplerSelector",
            inputs=[
                io.Combo.Input(
                    "sampler_name",
                    options=comfy.samplers.KSampler.SAMPLERS,
                )
            ],
            outputs=[io.Custom("SAMPLER_NAME").Output(display_name="Sampler")],
        )

    @override
    @classmethod
    def execute(cls, **inputs) -> io.NodeOutput:  # type: ignore[no-untyped-def]  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        return io.NodeOutput(inputs["sampler_name"])
