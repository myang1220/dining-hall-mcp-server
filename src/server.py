#!/usr/bin/env python3
import os
from typing import Optional
from fastmcp import FastMCP
from src.tools.menus import get_menus_tool, summarize_menus_tool, refresh_cache_tool

mcp = FastMCP("dining-hall-mcp")

@mcp.tool(description="Get dining hall menus for a specific date range and location")
def get_menus(date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, locationId: Optional[str] = None):
    return get_menus_tool(date=date, start_date=start_date, end_date=end_date, location_id=locationId)

@mcp.tool(description="Get summarized dining hall menu information with highlights and dietary information")
def summarize_menus(date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, locationId: Optional[str] = None, topN: int = 5):
    return summarize_menus_tool(date=date, start_date=start_date, end_date=end_date, location_id=locationId, top_n=topN)

@mcp.tool(description="Refresh the dining hall menu cache with fresh data from the API")
def refresh_cache(start_date: Optional[str] = None, end_date: Optional[str] = None):
    return refresh_cache_tool(start_date=start_date, end_date=end_date)

@mcp.tool(description="Get information about the dining hall MCP server including name, version, environment, and Python version")
def get_server_info() -> dict:
    return {
        "server_name": "Dining Hall MCP Server",
        "version": "1.0.0",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": os.sys.version.split()[0]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting FastMCP server on {host}:{port}")
    
    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )