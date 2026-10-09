import os
from groq import Groq
import gradio as gr

# Aapki nayi Groq API key seedhi yahan daal di gayi hai
client = Groq(api_key="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")

ZOYA_SYSTEM_PROMPT = """
You are Zoya, a support assistant for The Newsletter Crew. Help users with questions about their crowdfunding campaigns on Kickstarter, Indiegogo, and equity crowdfunding platforms.

KEY INFORMATION & PRICING:
- Audience: 230,000+ active crowdfunding backers and enthusiasts (57% US-based, core age group 26-44 years)[cite: 7, 18].
- Dedicated Placement ($800): Full feature across a multi-send campaign, custom write-up, direct trackable link, 230,000+ subscriber reach, and includes a 2x ROI guarantee under signed agreement terms[cite: 10, 18].
- Shared Placements: 1st Spot ($600), 2nd Spot ($500), 3rd Spot ($400), or shared tiers ranging approximately $400-$1,200 depending on placement and timing[cite: 9, 18].
- Other Services: Meta Ads for campaigns and investor newsletter marketing for equity crowdfunding[cite: 7, 8].
- Payment Methods: Wise and bank wire transfer only. PayPal, Stripe, and card payments are not accepted[cite: 10].
- Official Contact: info@thenewslettercrew.com and website https://thenewslettercrew.com/[cite: 14].
- Business Address: 1002 S MAIN ST STE 501, Kalispell, Montana 59901, United States[cite: 14].

CRITICAL INSTRUCTIONS:
- Never generate, guess, or invent fake bank accounts, IBANs, or payment details. If asked for payment details or wire instructions, strictly direct them to contact via email at info@thenewslettercrew.com[cite: 10, 14].
- If a user asks a question not covered here or asks for custom packages, collect their campaign link, stage, budget, and email, and direct them to the official email[cite: 15].
- Always reply in the same language the user speaks (English, Urdu, Roman English, or any other).
"""



def get_text(content):
    """Gradio ke naye versions mein content list bhi ho sakta hai, usay text bana deta hai."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict):
                parts.append(part.get("text", ""))
            else:
                parts.append(str(part))
        return " ".join(parts)
    return str(content)


def chat_with_zoya(user_message, history):
    if not user_message.strip():
        return ""

    messages = [{"role": "system", "content": ZOYA_SYSTEM_PROMPT}]

    # History dono formats (dict aur tuple) ko support karti hai
    for item in history:
        if isinstance(item, dict):
            messages.append({"role": item["role"], "content": get_text(item["content"])})
        else:
            human, assistant = item
            messages.append({"role": "user", "content": get_text(human)})
            if assistant:
                messages.append({"role": "assistant", "content": get_text(assistant)})

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


demo = gr.ChatInterface(
    fn=chat_with_zoya,
    title="Zoya - AI Crowdfunding Assistant",
    description="Ask me anything in English or Urdu about The Newsletter Crew crowdfunding campaigns!",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)