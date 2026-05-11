from comfy_api.latest import ComfyExtension, io
from typing_extensions import override

from .src.flux1_dimensions_selector import Flux1DimensionsSelector
from .src.sampler_selector import SamplerSelector
from .src.scheduler_selector import SchedulerSelector
from .src.sdxl_dimensions_selector import SDXLDimensionsSelector
from .src.zimage_dimensions_selector import ZImageDimensionsSelector


class ComfyCombos(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            Flux1DimensionsSelector,
            SamplerSelector,
            SchedulerSelector,
            SDXLDimensionsSelector,
            ZImageDimensionsSelector,
        ]


async def comfy_entrypoint() -> ComfyExtension:
    return ComfyCombos()
