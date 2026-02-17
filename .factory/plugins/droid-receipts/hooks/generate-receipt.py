#!/usr/bin/env python3
"""
Droid Receipts - Generate visual receipts for Droid sessions.

Triggered by SessionEnd hook. Reads session data from:
- Hook stdin (session_id, transcript_path, cwd)
- Session settings JSON (token counts, model)
- Transcript JSONL (session title, timestamps)

Generates an SVG receipt saved to ~/.factory/receipts/
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Pricing: $1 per 1 million tokens
PRICE_PER_MILLION = 1.0

# Output directory for receipts
RECEIPTS_DIR = Path.home() / ".factory" / "receipts"


def format_currency(tokens: int) -> str:
    """Calculate cost at $1/M tokens."""
    cost = tokens / 1_000_000 * PRICE_PER_MILLION
    return f"${cost:.2f}"


def format_number(n: int) -> str:
    """Format number with thousand separators."""
    return f"{n:,}"


def format_duration(ms: int) -> str:
    """Format duration from milliseconds."""
    seconds = ms // 1000
    minutes = seconds // 60
    hours = minutes // 60
    
    if hours > 0:
        return f"{hours}h {minutes % 60}m {seconds % 60}s"
    elif minutes > 0:
        return f"{minutes}m {seconds % 60}s"
    else:
        return f"{seconds}s"


def get_model_name(model: str) -> str:
    """Clean up model name for display."""
    model_map = {
        "claude-opus-4-6": "Claude Opus 4.6",
        "claude-opus-4-6-fast": "Claude Opus 4.6 Fast",
        "claude-opus-4-5-20251101": "Claude Opus 4.5",
        "claude-sonnet-4-5-20250929": "Claude Sonnet 4.5",
        "claude-haiku-4-5-20251001": "Claude Haiku 4.5",
        "gpt-5.1-codex-max": "GPT-5.1 Codex Max",
        "gpt-5.1-codex": "GPT-5.1 Codex",
        "gpt-5.1": "GPT-5.1",
        "gpt-5.2": "GPT-5.2",
        "gpt-5.2-codex": "GPT-5.2 Codex",
        "gpt-5.3-codex": "GPT-5.3 Codex",
        "gemini-3-pro-preview": "Gemini 3 Pro",
        "gemini-3-flash-preview": "Gemini 3 Flash",
        "glm-4.7": "Droid Core (GLM-4.7)",
        "glm-5": "Droid Core (GLM-5)",
        "kimi-k2.5": "Droid Core (Kimi K2.5)",
        "minimax-m2.5": "MiniMax M2.5",
    }
    return model_map.get(model, model)


def escape_xml(text: str) -> str:
    """Escape XML special characters."""
    return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;"))


def generate_svg(session_data: dict) -> str:
    """Generate SVG receipt from session data."""
    
    # Extract data
    session_id = session_data["session_id"]
    # Use short session ID (first 8 chars)
    session_short = session_id[:8] if len(session_id) >= 8 else session_id
    location = session_data.get("location", "The Cloud")[:30]
    model = session_data["model"]
    model_name = get_model_name(model)
    tokens = session_data["tokens"]
    end_time = session_data.get("end_time", datetime.now().isoformat())
    active_time = session_data.get("active_time_ms", 0)
    
    # Calculate totals - sum ALL tokens for total cost
    input_tokens = tokens.get("inputTokens", 0)
    output_tokens = tokens.get("outputTokens", 0)
    cache_write = tokens.get("cacheCreationTokens", 0)
    cache_read = tokens.get("cacheReadTokens", 0)
    total_tokens = input_tokens + output_tokens + cache_write + cache_read
    
    input_cost = format_currency(input_tokens)
    output_cost = format_currency(output_tokens)
    cache_write_cost = format_currency(cache_write)
    cache_read_cost = format_currency(cache_read)
    total_cost = format_currency(total_tokens)
    
    # Format date
    try:
        dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
        date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        date_str = end_time
    
    # Format duration
    duration_str = format_duration(active_time)
    
    # Escape text for XML
    location = escape_xml(location)
    model_name = escape_xml(model_name)
    session_short = escape_xml(session_short)
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="550" viewBox="0 0 400 550" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .receipt-bg {{ fill: #f8f8f8; }}
      .text {{ font-family: 'Courier New', Courier, monospace; font-size: 12px; fill: #333; }}
      .text-bold {{ font-family: 'Courier New', Courier, monospace; font-size: 12px; fill: #333; font-weight: bold; }}
      .text-large {{ font-family: 'Courier New', Courier, monospace; font-size: 16px; fill: #333; font-weight: bold; }}
      .text-small {{ font-family: 'Courier New', Courier, monospace; font-size: 10px; fill: #666; }}
      .text-tiny {{ font-family: 'Courier New', Courier, monospace; font-size: 9px; fill: #999; }}
      .separator {{ stroke: #333; stroke-width: 2; }}
      .light-separator {{ stroke: #ccc; stroke-width: 1; stroke-dasharray: 2,2; }}
      .logo-text {{ font-family: Arial, sans-serif; font-size: 24px; fill: #333; font-weight: bold; }}
    </style>
  </defs>
  
  <!-- Receipt background -->
  <rect class="receipt-bg" x="10" y="10" width="380" height="530" rx="4"/>
  
  <!-- Header -->
  <text x="200" y="55" class="logo-text" text-anchor="middle">FACTORY</text>
  <text x="200" y="78" class="text-small" text-anchor="middle">DROID RECEIPT</text>
  
  <!-- Separator -->
  <line x1="30" y1="95" x2="370" y2="95" class="separator"/>
  
  <!-- Session info -->
  <text x="30" y="120" class="text">Location</text>
  <text x="370" y="120" class="text" text-anchor="end">{location}</text>
  <line x1="105" y1="116" x2="285" y2="116" class="light-separator"/>
  
  <text x="30" y="140" class="text">Session</text>
  <text x="370" y="140" class="text" text-anchor="end">{session_short}</text>
  <line x1="105" y1="136" x2="285" y2="136" class="light-separator"/>
  
  <text x="30" y="160" class="text">Date</text>
  <text x="370" y="160" class="text" text-anchor="end">{date_str}</text>
  <line x1="105" y1="156" x2="285" y2="156" class="light-separator"/>
  
  <text x="30" y="180" class="text">Duration</text>
  <text x="370" y="180" class="text" text-anchor="end">{duration_str}</text>
  <line x1="105" y1="176" x2="285" y2="176" class="light-separator"/>
  
  <!-- Separator -->
  <line x1="30" y1="200" x2="370" y2="200" class="separator"/>
  
  <!-- Header -->
  <text x="30" y="225" class="text-bold">ITEM</text>
  <text x="200" y="225" class="text-bold" text-anchor="middle">QTY</text>
  <text x="370" y="225" class="text-bold" text-anchor="end">PRICE</text>
  
  <line x1="30" y1="235" x2="370" y2="235" class="light-separator"/>
  
  <!-- Model name -->
  <text x="30" y="260" class="text-bold">{model_name}</text>
  
  <!-- Line items -->
  <text x="45" y="285" class="text">Input tokens</text>
  <text x="200" y="285" class="text" text-anchor="middle">{format_number(input_tokens)}</text>
  <text x="370" y="285" class="text" text-anchor="end">{input_cost}</text>
  
  <text x="45" y="305" class="text">Output tokens</text>
  <text x="200" y="305" class="text" text-anchor="middle">{format_number(output_tokens)}</text>
  <text x="370" y="305" class="text" text-anchor="end">{output_cost}</text>'''
    
    # Add cache tokens if present
    if cache_write > 0:
        svg += f'''
  <text x="45" y="325" class="text">Cache write</text>
  <text x="200" y="325" class="text" text-anchor="middle">{format_number(cache_write)}</text>
  <text x="370" y="325" class="text" text-anchor="end">{cache_write_cost}</text>'''
    
    if cache_read > 0:
        y_pos = 345 if cache_write > 0 else 325
        svg += f'''
  <text x="45" y="{y_pos}" class="text">Cache read</text>
  <text x="200" y="{y_pos}" class="text" text-anchor="middle">{format_number(cache_read)}</text>
  <text x="370" y="{y_pos}" class="text" text-anchor="end">{cache_read_cost}</text>'''
    
    # Calculate total section position
    total_y = 345
    if cache_write > 0:
        total_y += 20
    if cache_read > 0:
        total_y += 20
    
    svg += f'''
  
  <!-- Total section -->
  <line x1="30" y1="{total_y + 15}" x2="370" y2="{total_y + 15}" class="separator"/>
  
  <text x="30" y="{total_y + 40}" class="text-bold" font-size="14">TOTAL</text>
  <text x="370" y="{total_y + 40}" class="text-bold" font-size="14" text-anchor="end">{total_cost}</text>
  
  <line x1="30" y1="{total_y + 55}" x2="370" y2="{total_y + 55}" class="separator"/>
  
  <!-- Footer -->
  <text x="200" y="{total_y + 85}" class="text" text-anchor="middle">CASHIER: {model_name}</text>
  
  <text x="200" y="{total_y + 115}" class="text" text-anchor="middle">Thank you for building!</text>
  
  <line x1="100" y1="{total_y + 135}" x2="300" y2="{total_y + 135}" class="light-separator"/>
  
  <text x="200" y="{total_y + 155}" class="text-small" text-anchor="middle">github.com/Factory-AI/factory</text>
</svg>'''
    
    return svg


def main():
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)
        
        session_id = hook_input.get("session_id", "")
        transcript_path = hook_input.get("transcript_path", "").replace("~", os.environ.get("HOME", "~"))
        cwd = hook_input.get("cwd", "")
        
        # Extract location from cwd
        location = Path(cwd).name if cwd else "The Cloud"
        
        # Read session settings
        settings_path = transcript_path.replace(".jsonl", ".settings.json")
        
        if not os.path.exists(settings_path):
            print(f"No session settings found at {settings_path}", file=sys.stderr)
            sys.exit(0)  # Non-blocking exit
        
        with open(settings_path, "r") as f:
            settings = json.load(f)
        
        tokens = settings.get("tokenUsage", {})
        model = settings.get("model", "unknown")
        active_time_ms = settings.get("assistantActiveTimeMs", 0)
        
        # Skip if no token data
        if not tokens:
            print("No token usage data available", file=sys.stderr)
            sys.exit(0)
        
        # Parse transcript for end time
        end_time = datetime.now().isoformat()
        
        if os.path.exists(transcript_path):
            with open(transcript_path, "r") as f:
                # Get last timestamp
                for line in reversed(list(f)):
                    line = line.strip()
                    if line:
                        try:
                            entry = json.loads(line)
                            if "timestamp" in entry:
                                end_time = entry["timestamp"]
                                break
                        except:
                            pass
        
        # Build session data
        session_data = {
            "session_id": session_id,
            "location": location,
            "model": model,
            "tokens": tokens,
            "end_time": end_time,
            "active_time_ms": active_time_ms,
        }
        
        # Create output directory
        RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generate SVG
        svg_content = generate_svg(session_data)
        
        # Save receipt
        output_path = RECEIPTS_DIR / f"{session_id}.svg"
        with open(output_path, "w") as f:
            f.write(svg_content)
        
        print(f"Receipt saved to {output_path}")
        
        # Optionally open in browser (macOS)
        if sys.platform == "darwin":
            os.system(f'open "{output_path}"')
        
    except Exception as e:
        print(f"Error generating receipt: {e}", file=sys.stderr)
        sys.exit(0)  # Non-blocking exit


if __name__ == "__main__":
    main()
