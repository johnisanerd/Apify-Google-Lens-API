"""
Google Lens API: A Quick Start Example
See more at: https://apify.com/johnvc/google-lens-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/google-lens-api/input-schema?fpr=9n7kx3

This script shows how to call the Google Lens API on Apify from Python and
read its structured JSON output. The default run stays deliberately small so
your first call is inexpensive; the --example recipes mirror the API's main
use cases (see the README Recipes section).

Get your free Apify API key at: https://apify.com?fpr=9n7kx3

Examples:
  uv run python google-lens-api-example.py
  uv run python google-lens-api-example.py --example stolen_check
  uv run python google-lens-api-example.py --example upload --image path/to/photo.jpg
"""

from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path
from typing import Any

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR_ID = "johnvc/google-lens-api"


def _print_items(items: list[dict[str, Any]]) -> None:
    """Print a short summary of dataset items."""
    print(f"Returned {len(items)} item(s).\n")
    for item in items:
        print(item.get('title'), item.get('source'), item.get('url'))


def run_default(client: ApifyClient) -> None:
    """Cheap general quick-start. Inputs stay small on purpose."""
    run_input: dict[str, Any] = {
        "image_url": "https://i.imgur.com/HBrB8p0.png",
        "search_type": "visual_matches",
        "max_results": 3,  # small on purpose to keep the first run inexpensive
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_stolen_check(client: ApifyClient) -> None:
    """Check where one image is being reused (mirrors the stolen-photo use case).

    exact_matches returns up to 400 pages carrying the identical file. Coverage
    varies run to run at the source; an empty result is a real answer.
    """
    run_input: dict[str, Any] = {
        "image_url": "https://i.imgur.com/HBrB8p0.png",
        "search_type": "exact_matches",
        "max_results": 5,  # small on purpose; raise once you know your budget
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_product_match(client: ApifyClient) -> None:
    """Visual product search: photo in, shoppable listings out."""
    run_input: dict[str, Any] = {
        "image_url": "https://i.imgur.com/HBrB8p0.png",
        "search_type": "products",
        "max_results": 3,  # small on purpose; raise once you know your budget
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_upload(client: ApifyClient, image_path: str) -> None:
    """Search by a LOCAL image file, no public URL needed.

    The file's bytes are base64-encoded and sent as image_base64; the API
    stages them privately behind a signed link and runs the lookup. You can
    pass several entries to batch up to 10 images per run (about 6 MB of
    images total on this path, because the platform caps run input at 9 MB;
    bigger files go through the console's Upload images field instead).
    """
    path = Path(image_path)
    if not path.is_file():
        raise SystemExit(f"Image file not found: {path}")
    encoded = base64.b64encode(path.read_bytes()).decode()
    run_input: dict[str, Any] = {
        "image_base64": [encoded],  # add more entries to batch several images
        "search_type": "visual_matches",
        "max_results": 3,  # small on purpose to keep the first run inexpensive
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def main() -> None:
    """Dispatch a quick-start or use-case recipe."""
    parser = argparse.ArgumentParser(description="Google Lens API examples")
    parser.add_argument(
        "--example",
        default="default",
        choices=['default', 'stolen_check', 'product_match', 'upload'],
        help="Which recipe to run (see README Recipes).",
    )
    parser.add_argument(
        "--image",
        default="sample-image.jpg",
        help="Local image file for the upload recipe (defaults to the bundled sample).",
    )
    args = parser.parse_args()

    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        raise SystemExit("Set APIFY_API_TOKEN in .env or the environment.")

    client = ApifyClient(token)
    if args.example == "upload":
        run_upload(client, args.image)
        return
    dispatch = {
        "default": run_default,
        "stolen_check": run_stolen_check,
        "product_match": run_product_match,
    }
    dispatch[args.example](client)


if __name__ == "__main__":
    main()
