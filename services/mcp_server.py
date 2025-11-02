# server.py
from fastmcp import FastMCP
import httpx

mcp = FastMCP("FDA_DrugInfo")

@mcp.tool()
async def get_drug_info(drug_name: str) -> str:
    """
    Get drug info from FDA API
    """
    try:
        url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug_name}&limit=1"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            return f"Error: FDA API returned {response.status_code}"

        data = response.json()
        results = data.get("results", [])
        if not results:
            return f"No drug information found for: {drug_name}"

        drug_info = results[0]

        # Extract specific fields safely
        # brand_name = drug_info.get("openfda", {}).get("brand_name", ["N/A"])[0]
        # generic_name = drug_info.get("openfda", {}).get("generic_name", ["N/A"])[0]
        indications = " ".join(drug_info.get("indications_and_usage", ["N/A"]))
        dosage = " ".join(drug_info.get("dosage_and_administration", ["N/A"]))
        # warnings = " ".join(drug_info.get("warnings", ["N/A"]))
        side_effects = " ".join(drug_info.get("adverse_reactions", ["N/A"]))

        # Format neatly
        result = (
            f"=== Drug Information ===\n"
            # f"Brand Name   : {brand_name}\n"
            # f"Generic Name : {generic_name}\n"
            f"Indications  : {indications[:500]}...\n"
            f"Dosage       : {dosage[:500]}...\n"
            # f"Warnings     : {warnings[:500]}...\n"
            f"Side Effects : {side_effects[:500]}...\n"
        )
        return result

    except Exception as e:
        return f"Error fetching drug info: {str(e)}"



def run_server():
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8002)

if __name__ == "__main__":
    run_server()

