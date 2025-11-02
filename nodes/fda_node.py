from state.chat_state import ChatState
from services.mcp_client import query_fda

async def fda_node(state) -> dict:
    """
    Retrieve FDA info for all listed medicines.
    Returns a formatted plain-text result.
    Works with both ChatState and dict state objects.
    """

    # ✅ Safely extract medicine_text (list)
    medi_text = (
        state.get("medicine_text")
        if isinstance(state, dict)
        else getattr(state, "medicine_text", [])
    )

    if not medi_text:
        # nothing to query
        return state

    formatted_results = []

    # ✅ Loop through all medicines and collect formatted info
    for medicine in medi_text:
        fda_info = await query_fda(medicine)
        formatted_results.append(f"💊 Medicine: {medicine}\n📄 FDA Info: {fda_info}\n")

    # ✅ Join all medicine info with line breaks
    all_fda_info = "\n" + "\n".join(formatted_results)

    # ✅ Convert medicine list to a readable string
    medi_text_str = ", ".join(medi_text)

    # ✅ Return values in expected format (string-based)
    return {
        "medicine_query": medi_text_str,
        "fda_info": all_fda_info
    }





# from state.chat_state import ChatState
# from services.mcp_client import query_fda

# async def fda_node(state) -> dict:
#     """
#     Retrieve FDA info for the first listed medicine.
#     Works with both ChatState and dict state objects.
#     """

#         # ✅ Safely extract medicine_text (list)
#     medi_text = (
#         state.get("medicine_text")
#         if isinstance(state, dict)
#         else getattr(state, "medicine_text", [])
#     )

#     if not medi_text:
#         # nothing to query
#         return state

#     first_medicine = medi_text[0]


#     # ✅ Call your MCP client
#     fda_infor = await query_fda(first_medicine)

#     return {"medicine_query": first_medicine, "fda_info": fda_infor}

