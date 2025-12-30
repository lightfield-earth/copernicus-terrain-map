# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "geopandas==1.0.1",
#     "leafmap[maplibre]==0.43.11",
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import marimo as mo
    import leafmap.maplibregl as leafmap
    from leafmap.maplibregl import Layer
    return json, leafmap, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Generating HTML for Map Deployment
    #### December 2025
    At present, when executing this notebook from within the Marimo interactive notebook experience, the HTML export does not function properly. The resulting HTML only includes the base map. To properly export the HTML for deployment, execute
    ```bash
    python map_notebook_marimo.py
    ```
    at the command line.
    """)
    return


@app.cell
def _(json, leafmap):
    with open('basemap_style_spec.json', 'r') as f:
        style_spec = json.load(f)

    m = leafmap.Map(
        center=(-98.5795,39.8283),  # Center of the US
        zoom=3,                     # Initial zoom level
        min_zoom=2,
        max_zoom=10,
        height='600px',                            
        style=style_spec,
        use_message_queue=True,     # Needed to export HTML for the full map
        hash=True,
        controls={
            "geolocate": "top-right",
            "navigation": "top-right",
            "fullscreen": "top-right", 
            "scale": "bottom-left"
        }
    )

    m.add_tile_layer(
        url="https://tiles.lightfield.ag/hillshade_tiles_planet_z11_webp/{z}/{x}/{y}.webp",
        before_id='Residential',
        paint={
            "raster-resampling": "nearest",  # Use nearest neighbor instead of linear
            "raster-opacity": 1.0
        }
    )

    image = "LightField Combination Mark.png"
    m.add_image(image=image, position="top-left", height='50px')

    m
    return (m,)


@app.cell
def _(m):
    m.to_html('index_stage.html',title='Copernicus GLO-30 Global Terrain Layer',overwrite=True)
    return


if __name__ == "__main__":
    app.run()
