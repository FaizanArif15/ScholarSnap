# summarize_agent.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from arxiv import search_arxiv_paper
from gmail_service import email_summary

# Load environment variables
load_dotenv()

def summarize_paper(paper_text: str, paper_title: str, paper_url: str) -> str:
    """
    Summarize an academic paper text using GPT-4o-small.
    The summary should be short, simple, and suitable for beginners.
    """
    # Initialize the OpenAI model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

    # Create a good prompt template
    prompt_template = PromptTemplate(
        input_variables=["paper_text", "paper_title", "paper_url"],
        template=(
            "You are a research assistant helping summarize academic papers clearly and concisely.\n\n"
            "Paper title: {paper_title}\n"
            "Paper URL: {paper_url}\n\n"
            "Below is the paper content:\n"
            "{paper_text}\n\n"
            "Write a friendly and informative summary that:\n"
            "1. Explains the main idea and motivation in simple language.\n"
            "2. Highlights the key methods or approach.\n"
            "3. Lists the main results or findings.\n"
            "4. Ends with a short note on why this research matters.\n\n"
            "Include a final section called '🔗 Paper Link' with the paper URL.\n\n"
            "Format your response like this:\n"
            "✏️ Paper Title\n"
            "{paper_title}\n"
            "🧠 Summary\n"
            "<your short, clear summary (150-200 words)>\n\n"
            "🔑 Key Insights\n"
            "- Insight 1\n"
            "- Insight 2\n"
            "- Insight 3\n\n"
            "🔗 Paper Link\n"
            "{paper_url}"
        ),
    )

    # Format the prompt
    prompt = prompt_template.format(
        # paper_text=paper_text[:7000],  # limit to ~7000 characters for cost/speed
        paper_text=paper_text,
        paper_title=paper_title,
        paper_url=paper_url,
    )
    
    # Generate summary
    response = llm.invoke(prompt)
    return response.content



def run_agent():
    """Run the full fetch -> summarize -> email pipeline once."""
    try:
        print("📥 Fetching and extracting paper...")
        text, paper_title, paper_url = search_arxiv_paper()

        print("\n🤖 Generating summary")
        summary = summarize_paper(text, paper_title, paper_url)
        
        notify_emails = os.getenv("NOTIFY_EMAIL", "")
        recipients = [email.strip() for email in notify_emails.split(",") if email.strip()]

        # Send email (ensure email_summary signature matches below)
        email_summary(summary, paper_title, recipients)

        print("\n🧾 Summary generated and emailed.")
        return True
    except Exception as e:
        print(f"❌ run_agent failed: {e}")
        return False


if __name__ == "__main__":
    
    run_agent()
