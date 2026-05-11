# Comfy Combos

Dropdown selector nodes for ComfyUI. Each node replaces a free-text or
disconnected widget with a single combo input that passes a typed value
downstream.

> [!IMPORTANT]
> This extension uses the `comfy_api.latest` v3 node API. It requires a
> recent ComfyUI build (0.3.x or later). Older installations will not load
> these nodes.

---

## Installation

**Via ComfyUI-Manager** — use the GitHub address to directly add the extension since it is not currently registered.

**Manual**

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/bnwa/comfy_combos
```

No additional Python dependencies are required beyond ComfyUI itself.

---

## Nodes

All nodes appear under the **Comfy Combos** category.

### Select Sampler

Outputs the chosen KSampler sampler name as a `SAMPLER_NAME` string.

| | Name | Type | Notes |
|---|---|---|---|
| **Input** | `sampler_name` | Combo | All samplers registered with `KSampler` |
| **Output** | `Sampler` | `SAMPLER_NAME` | |

---

### Select Scheduler

Outputs the chosen KSampler scheduler name as a `SCHEDULER_NAME` string.

| | Name | Type | Notes |
|---|---|---|---|
| **Input** | `scheduler_name` | Combo | All schedulers registered with `KSampler` |
| **Output** | `Scheduler` | `SCHEDULER_NAME` | |

---

### Select SDXL Dimensions

Picks from nine community-standard SDXL dimension presets and emits a
pre-allocated empty latent alongside scaled output dimensions.

| | Name | Type | Default | Range |
|---|---|---|---|---|
| **Input** | `dimensions` | Combo | — | 9 presets (see below) |
| **Input** | `upscale_factor` | Float | `2.0` | 1.0 – 8.0, step 0.25 |
| **Input** | `batch` | Int | `1` | ≥ 1 |

| | Name | Type |
|---|---|---|
| **Output** | `width` | Int |
| **Output** | `height` | Int |
| **Output** | `latent` | Latent (4-channel) |
| **Output** | `upscale factor` | Float |
| **Output** | `upscaled width` | Int |
| **Output** | `upscaled height` | Int |

**Presets**

| Label | Width | Height | Ratio |
|---|---|---|---|
| 1024 × 1024 | 1024 | 1024 | 1:1 |
| 1152 × 896 | 1152 | 896 | 9:7 |
| 896 × 1152 | 896 | 1152 | 7:9 |
| 1216 × 832 | 1216 | 832 | 19:13 |
| 832 × 1216 | 832 | 1216 | 13:19 |
| 1344 × 768 | 1344 | 768 | 7:4 |
| 768 × 1344 | 768 | 1344 | 4:7 |
| 1536 × 640 | 1536 | 640 | 12:5 |
| 640 × 1536 | 640 | 1536 | 5:12 |

---

### Select Flux.1 Dimensions

Picks from 18 Flux.1 Dev dimension presets across two megapixel budgets and
emits a pre-allocated empty latent using the 16-channel Flux VAE latent space.

| | Name | Type | Default | Range |
|---|---|---|---|---|
| **Input** | `dimensions` | Combo | — | 18 presets (see below) |
| **Input** | `upscale_factor` | Float | `2.0` | 1.0 – 8.0, step 0.25 |
| **Input** | `batch` | Int | `1` | ≥ 1 |

| | Name | Type |
|---|---|---|
| **Output** | `width` | Int |
| **Output** | `height` | Int |
| **Output** | `latent` | Latent (16-channel) |
| **Output** | `upscale factor` | Float |
| **Output** | `upscaled width` | Int |
| **Output** | `upscaled height` | Int |

**Presets — ~1 MP (community-standard)**

| Label | Width | Height |
|---|---|---|
| Square | 1024 | 1024 |
| Landscape | 1152 | 896 |
| Portrait | 896 | 1152 |
| Classic Landscape | 1152 | 864 |
| Classic Portrait | 864 | 1152 |
| Photo Landscape | 1216 | 832 |
| Photo Portrait | 832 | 1216 |
| Wide Landscape | 1344 | 768 |
| Tall Portrait | 768 | 1344 |
| Widescreen | 1280 | 720 |
| Vertical | 720 | 1280 |
| Ultrawide | 1536 | 640 |
| Ultra-Tall | 640 | 1536 |

**Presets — ~2 MP (community sweet spot)**

| Label | Width | Height |
|---|---|---|
| HD Square | 1408 | 1408 |
| HD Landscape | 1728 | 1152 |
| HD Portrait | 1152 | 1728 |
| Full HD Widescreen | 1920 | 1088 |
| Full HD Vertical | 1088 | 1920 |

---

### Select Z-Image Dimensions

Picks from 33 official Z-Image dimension presets across three resolution tiers
and emits a pre-allocated empty latent using the 16-channel VAE latent space
(8× spatial compression).

| | Name | Type | Default | Range |
|---|---|---|---|---|
| **Input** | `dimensions` | Combo | — | 33 presets across three tiers |
| **Input** | `upscale_factor` | Float | `2.0` | 1.0 – 8.0, step 0.25 |
| **Input** | `batch` | Int | `1` | ≥ 1 |

| | Name | Type |
|---|---|---|
| **Output** | `width` | Int |
| **Output** | `height` | Int |
| **Output** | `latent` | Latent (16-channel) |
| **Output** | `upscale factor` | Float |
| **Output** | `upscaled width` | Int |
| **Output** | `upscaled height` | Int |

**Tiers:** 1024 (~1 MP, 11 presets) · 1280 (~1.6 MP, 11 presets) · 1536 (~2.4 MP, 11 presets).
Each tier covers Square, Landscape/Portrait, Classic 4:3/3:4, Photo 3:2/2:3,
16:9/9:16 Widescreen/Vertical, and 21:9/9:21 Ultrawide/Ultra-Tall.

---

## Development

Install with dev dependencies:

```bash
cd comfy_combos
pip install -e ".[dev]"
pre-commit install
```
