from openai_llm import ask_openai
from gemini_llm import ask_gemini  # keep for later, safe import

def get_llm_responses(question, context):

    results = {}

    # OpenAI response (primary)
    try:
        results["OpenAI"] = ask_openai(question, context)
    except Exception as e:
        results["OpenAI"] = f"OpenAI Error: {str(e)}"

    # Gemini response (optional fallback)
    try:
        results["Gemini"] = ask_gemini(question, context)
    except Exception as e:
        results["Gemini"] = f"Gemini Error / Disabled: {str(e)}"

    return results


def get_selected_response(selected_llm, question, context):

    if selected_llm == "OpenAI":
        return ask_openai(question, context)

    elif selected_llm == "Gemini":
        return ask_gemini(question, context)

    else:
        return "Invalid LLM selection"