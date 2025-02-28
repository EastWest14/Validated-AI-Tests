import asyncio
from validated_ai_tests import ValidatedCasesRunner, Case


async def chatbot_response_generator(conversation: str) -> str:
    # Static example response for now
    return "Please restart your app"


trouble_logging_in_case = Case(
    executor=chatbot_response_generator,
    input_args=[
        """
        User: I am having trouble logging in.
        Chatbot: Hi, I am here to help. What seems to be the problem?
        User: I can't log in. App spins forever when I press login.
"""
    ],
    input_kwargs={},
    case_pass_condition="Chatbot should ask user to restart app.",
    pass_cases=[
        "Chatbot: Please restart your app.",
        "Chatbot: This sounds frustrating. Please restart your app.",
        "Chatbot: As a first step, lets try restarting the app.",
    ],
    fail_cases=[
        "Chatbot: Please check your internet connection.",
        "Chatbot: Have you tried reinstalling the app?",
        "Chatbot: oh, that's a tough one",
    ],
)


cases = [trouble_logging_in_case]
runner = ValidatedCasesRunner(cases)
result = asyncio.run(runner.run())
print(result)
