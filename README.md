# 🔍 Google Lens API: reverse image search from Python and MCP

Actor: [johnvc/google-lens-api](https://apify.com/johnvc/google-lens-api?fpr=9n7kx3) · [Input schema](https://apify.com/johnvc/google-lens-api/input-schema?fpr=9n7kx3)

This repo shows two ways to use the [Google Lens API](https://apify.com/johnvc/google-lens-api?fpr=9n7kx3) on Apify: a Python quick start and MCP installs for five AI clients. Send an image straight from your computer, base64 from code, or any public image URL, and get back visually similar results, shoppable product matches with prices, or every page carrying the exact same image, which is the bulk reverse image search photographers use for attribution checks. Most reverse image tools demand a public URL; this one does not.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

### Text walkthrough

The google lens api takes an image (a local file via image_base64 or the console upload field, or a public image_url) plus a search_type. visual_matches is the general reverse image search and returns about 59 rows per lookup with title, source, url, thumbnail and the full image link. products returns shoppable listings with price, currency and inStock. exact_matches returns up to 400 pages carrying the identical file, which powers the stolen-photo check recipe in this repo. Exact-match coverage varies run to run at the source, so an empty result finishes clean rather than erroring; retry or switch type.

## Quick Start

You need Python 3.11+ and a free Apify API key: sign up at [apify.com](https://apify.com?fpr=9n7kx3), then copy your token from Console Settings.

```bash
git clone https://github.com/johnisanerd/Apify-Google-Lens-API.git
cd Apify-Google-Lens-API
uv sync
cp .env.example .env   # then paste your APIFY_API_TOKEN
uv run python google-lens-api-example.py
```

Run a specific recipe:

```bash
uv run python google-lens-api-example.py --example stolen_check
```

### Search by a local file, no public URL needed

The repo bundles `sample-image.jpg`, so this works out of the box:

```bash
uv run python google-lens-api-example.py --example upload
uv run python google-lens-api-example.py --example upload --image path/to/your/photo.jpg
```

Under the hood the file is base64-encoded and sent as `image_base64`; the API stages it privately behind a signed link and runs the lookup. Batch up to 10 images per run by passing more entries (about 6 MB of images per run on the base64 path; the console's Upload images field takes files up to 20 MB each, 30 MB per run).

```python
import base64
from pathlib import Path

encoded = base64.b64encode(Path("photo.jpg").read_bytes()).decode()
run_input = {"image_base64": [encoded], "search_type": "visual_matches", "max_results": 3}
```

## Why use this API

- Upload local files or send base64, no public URL needed, up to 10 images per run
- Three search types behind one input: visual matches, products, exact matches
- Real destination URLs with source site names for every match
- Product matches carry price, currency and stock where the retailer publishes them
- Up to 400 exact-match rows per lookup for attribution and licensing sweeps
- Country and language targeting when you need regional results

## Recipes

The example script ships ready-made recipes that mirror this API's main use cases:

- **Search by a local file** (`--example upload`): Base64-encodes an image from your disk and looks it up, no public URL needed.
- **Check if a photo is being reused** (`--example stolen_check`): Runs exact matches over one image and lists every page carrying it.
- **Visual product search** (`--example product_match`): Turns a product photo into shoppable listings with prices.

**Schedule tip:** save any of these inputs as a task in the [Apify Console](https://apify.com/johnvc/google-lens-api?fpr=9n7kx3) and attach a schedule. A daily or weekly run turns a one-off pull into a pipeline with zero manual work.

## Usage Examples

Basic input:

```json
{
  "image_url": "https://i.imgur.com/HBrB8p0.png",
  "search_type": "visual_matches",
  "max_results": 10
}
```

Advanced input:

```json
{
  "image_url": "https://i.imgur.com/HBrB8p0.png",
  "search_type": "exact_matches",
  "max_results": 200,
  "country": "us"
}
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `image_url` | string | yes | none | REQUIRED. |
| `search_type` | string | no | `"visual_matches"` | What kind of matches to return. |
| `query` | string | no | none | Optional. |
| `max_results` | integer | no | `50` | How many matches to return. |
| `country` | string | no | none | Optional two letter country code such as us, gb or de. |
| `language` | string | no | none | Optional two letter language code such as en, es or fr. |

## Output Format

One row from a real run:

```json
{
  "resultType": "match",
  "searchType": "visual_matches",
  "position": 1,
  "title": "File:Danny DeVito by Gage Skidmore.jpg - Wikimedia Commons",
  "source": "Wikimedia Commons",
  "url": "https://commons.wikimedia.org/wiki/File:Danny_DeVito_by_Gage_Skidmore.jpg",
  "thumbnail": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcR0rTF6u7bB7aTW",
  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Danny_DeVito.jpg",
  "imageWidth": 1280,
  "imageHeight": 1024
}
```

## n8n integration

Available as an n8n community node, **[n8n-nodes-google-lens-api](https://www.npmjs.com/package/n8n-nodes-google-lens-api)**. In n8n: Settings, Community Nodes, install `n8n-nodes-google-lens-api`, then use it in any workflow (it also works as an AI Agent tool).

## People also search for

### Is this a reverse image search API with a free tier?

Yes: pay per result on Apify, and an Apify free account includes monthly platform credit, so small lookups cost nothing out of pocket.

### How do I reverse image search in Python?

Run the quick start here: uv sync, set your token, pass an image URL. Three lines of client code, JSON back.

### Can I do a bulk reverse image search?

Loop the client over a URL list, or point an AI agent at the MCP server below and hand it the list. Each image is one lookup.

### Why is the image field empty on exact matches?

The source returns only a thumbnail plus pixel dimensions for exact matches. Visual and product matches carry the full image link.

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Google Lens API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings -> Connectors** (or **Settings -> Developer -> Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/google-lens-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Google Lens API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/google-lens-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/google-lens-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Google Lens API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings -> Connectors -> Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/google-lens-api`.
3. In any chat, open **+ -> Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/google-lens-api`, using OAuth when prompted.
5. Ask Claude to run the Google Lens API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/google-lens-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/google-lens-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor -> Settings -> MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Google Lens API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/google-lens-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp


---

Made with care by [johnvc on Apify](https://apify.com/johnvc?fpr=9n7kx3). This example repo is part of [Alpha OSINT](https://www.alphaosint.com), toolset of financial and operations data sources and APIs.

Last Updated: 2026.08.16
