# visualize_zarr_ng

A lightweight utility for serving local **Zarr** volumes into [Neuroglancer Demo](https://neuroglancer-demo.appspot.com) with zero dependencies.
This tool spins up a **CORS-enabled HTTP server** that makes your `.zarr` datasets accessible to Neuroglancer, allowing quick visualization directly in your browser.

---
# Contributors

* Gabriele Amorosino
* Taylor Grafft
* Vasilis Karlaftis 
* Yael Balbastre
---

## Features

* No external dependencies (uses only Python standard library).
* Simple local HTTP server with **CORS support** for Neuroglancer.
* Generates a ready-to-use **Neuroglancer Demo URL**.
* Auto-opens your dataset in the browser (optional).
* Customizable host, port, and layer name.
* Supports different file types (default: `.zarr`).

---

## Installation

Requires **Python 3.8+**.
Clone this repository:

```bash
git clone https://github.com/gamorosino/visualize_zarr_ng.git
cd visualize_zarr_ng
```

No additional packages are needed.

---

## Usage

```bash
python visualize_zarr.py </path/to/volume1.zarr /path/to/volume2.zarr ...> [--port 5000] [--host 127.0.0.1] [--name <mylayer1 mylayer2 ...>]
```

### Arguments

* `file_path` (**required**) → Path to your `.zarr` directories.
* `--host` → Host to bind server (default: `127.0.0.1`).
* `--port` → Port for local server (default: `5000`).
* `--name` → Custom layer names (default: `.zarr` basename).
* `--file_type` → File type prefix (default: `zarr`).
* `--no-open` → Prevent auto-opening Neuroglancer in browser.

---

## Example

```bash
python visualize_zarr.py ./data/brain_volume.zarr --port 8080 --name "BrainVolume"
```

This will:

1. Start a local CORS-enabled HTTP server at `http://127.0.0.1:8080/`.
2. Generate a Neuroglancer Demo link pointing to your dataset.
3. Automatically open it in your default web browser.

Example output:

```
Neuroglancer Demo URL (encoded):
https://neuroglancer-demo.appspot.com/#!{"layers":[{"type":"image","source":"zarr://http://127.0.0.1:8080/brain_volume.zarr/","name":"BrainVolume"}]}
```

---

##  How It Works

1. The script serves the **parent directory** of your `.zarr` store over HTTP.
2. Adds **CORS headers** required by the Neuroglancer demo site.
3. Builds a minimal Neuroglancer state JSON with your dataset as an image layer.
4. Encodes the state into a shareable Neuroglancer demo URL.

---

##  Stopping the Server

Press `CTRL+C` in the terminal where the server is running.

---

##  License

MIT License – feel free to use and adapt.
