import comfy.samplers
from comfy_api.latest import io
from typing_extensions import override


class SchedulerSelector(io.ComfyNode):
    @override
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            category="Comfy Combos",
            description="Select a scheduler from a dropdown",
            display_name="Select Scheduler",
            node_id="comfy_combos_SchedulerSelector",
            inputs=[
                io.Combo.Input(
                    "scheduler_name",
                    options=comfy.samplers.KSampler.SCHEDULERS,
                )
            ],
            outputs=[io.Custom("SCHEDULER_NAME").Output(display_name="Scheduler")],
        )

    @override
    @classmethod
    def execute(cls, **inputs) -> io.NodeOutput:  # type: ignore[no-untyped-def]  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        return io.NodeOutput(inputs["scheduler_name"])
