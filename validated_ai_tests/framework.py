import json
from openai import OpenAI

# from validated_llm_tests.core import sample_function


class Case:
    _COMMON_VALIDATOR_PROMPT = """
        You are given an input and a description that may describe this input.
        Your goal is to determine if the input matches the description.
        
        Always return a JSON. If yes, return {{"result": "PASS", "Explanation": "..."}}.
        If no, return {{"result": "FAIL", "Explanation": "..."}}.

        Description: {description}
        Input: 
    """

    def __init__(
        self, executor, input_args, input_kwargs, case_pass_condition, pass_cases, fail_cases,
    ):
        self.executor = executor
        self.input_args = input_args
        self.input_kwargs = input_kwargs
        self.case_pass_condition = case_pass_condition
        self.pass_cases = pass_cases
        self.fail_cases = fail_cases
    
    def validate(self, client):
        # Check all the pass and fail cases against prompt.
        pass  
        
    def run_case(self, client):
        # Execute executor and check result against prompt.
        pass
    
    @property
    def _full_prompt(self):
        return self._COMMON_VALIDATOR_PROMPT.format(
            description=self.case_pass_condition
        )


def chatbot_response_generator(conversation: str) -> str:
    # Static example response for now
    return 'Please restart your app'


trouble_logging_in_case = Case(
    executor=chatbot_response_generator,
    input_args=["""
        User: I am having trouble logging in.
        Chatbot: Hi, I am here to help. What seems to be the problem?
        User: I can't log in. App spins forever when I press login.
"""],
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



class ValidatedCasesRunner:
    def __init__(self, cases, client=None):
        self.cases = cases
        if not client:
            client = OpenAI()
        self.client = client

    def run(self):
        results = []
        for case in self.cases:
            validator_results = case.validate(self.client)
            test_results = case.run_case(self.client)
            results.append({
                'validator_results': validator_results,
                'test_results': test_results,
            })
        return results
    

cases = [trouble_logging_in_case]
runner = ValidatedCasesRunner(cases)
result = runner.run()
print(result)