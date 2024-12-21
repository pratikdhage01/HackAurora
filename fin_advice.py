from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
from phi.tools.yfinance import YFinanceTools

# Load environment variables
load_dotenv()

# Configure the agent with the Groq model and YFinanceTools
agent = Agent(
    model=Groq(id='llama-3.3-70b-specdec'),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
    show_tools=True,
    markdown=True,
    instructions=["Use Summarized way, i will be sending this output as voice to the user"]
)

# Generate and print response for mutual funds guidance
agent.print_response("Provide guidance on which indian mutual funds should I invest and compare top indian mutual funds based on their performance and risk factors.")
