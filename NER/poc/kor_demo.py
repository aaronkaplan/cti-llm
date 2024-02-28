from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from kor import create_extraction_chain, Object, Text

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    max_tokens=2000,
    model_kwargs={
        'frequency_penalty': 0,
        'presence_penalty': 0,
        'top_p': 1.0
    }
)

schema = Object(
    id="entity_extraction",
    description="Extract various types of entities from text.",
    attributes=[
        Text(id="MALWARE", description="Malware names", examples=[("LockBit, DarkSide, WannaCry", "LockBit, DarkSide, WannaCry")], many=True),
        Text(id="THREAT_ACTOR", description="Names of threat actors", examples=[("BlueCharlie, APT28, Lazarus Group", "BlueCharlie, APT28, Lazarus Group")], many=True),
        Text(id="SOFTWARE", description="Software names", examples=[("LockBit 2.0, Windows 10, OpenSSH", "LockBit 2.0, Windows 10, OpenSSH")], many=True),
        Text(id="TTP", description="Tactics, Techniques, and Procedures", examples=[("spear-phishing, drive-by download, credential stuffing", "spear-phishing, drive-by download, credential stuffing")], many=True),
        Text(id="OS", description="Operating System names", examples=[("Windows, Linux, macOS", "Windows, Linux, macOS")], many=True),
        Text(id="HARDWARE", description="Hardware names", examples=[("iPhone, Netgate Firewall, Raspberry Pi", "iPhone, Netgate Firewall, Raspberry Pi")], many=True),
        Text(id="USERNAME", description="Usernames", examples=[("john_doe, admin, guest", "john_doe, admin, guest")], many=True),
        Text(id="ORGANIZATION", description="Organization names", examples=[("Insikt Group, OpenAI, Microsoft", "Insikt Group, OpenAI, Microsoft")], many=True),
        Text(id="SECTOR", description="Industry sectors", examples=[("finance, healthcare, energy", "finance, healthcare, energy")], many=True),
        Text(id="GEO_LOCATION", description="Geographical locations", examples=[("Russia, New York, Silicon Valley", "Russia, New York, Silicon Valley")], many=True),
        Text(id="EXPLOIT_NAME", description="Exploit names", examples=[("EternalBlue, Heartbleed, Shellshock", "EternalBlue, Heartbleed, Shellshock")], many=True),
        Text(id="DATE", description="Dates", examples=[("March 2023, September 2022, Q2 2021", "March 2023, September 2022, Q2 2021")], many=True),
        Text(id="TIME", description="Times", examples=[("10:00 AM, 23:45, midnight", "10:00 AM, 23:45, midnight")], many=True),
    ],
    many=False,
)

chain = create_extraction_chain(llm, schema, encoder_or_encoder_class='json')

# DEBUG
print(chain.prompt.format_prompt(text="[user input]").to_string())

# Example usage:

with get_openai_callback() as cb:
    result = chain.invoke("LockBit, BlueCharlie, and Windows 10 were mentioned")
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Successful Requests: {cb.successful_requests}")
    print(f"Total Cost (USD): ${cb.total_cost}")
    print("/////////")
    print(result['text']['data'])