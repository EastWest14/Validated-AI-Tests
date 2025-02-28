import json
from openai import OpenAI

import inspect


def get_llm_json_response(client, prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


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
        self,
        executor,
        input_args,
        input_kwargs,
        case_pass_condition,
        pass_cases,
        fail_cases,
    ):
        self.executor = executor
        self.input_args = input_args
        self.input_kwargs = input_kwargs
        self.case_pass_condition = case_pass_condition
        self.pass_cases = pass_cases
        self.fail_cases = fail_cases

    async def validate(self, client):
        validator_result = {
            "cases": [],
            "has_failure": False,
        }
        has_failure = False

        for p_case in self.pass_cases:
            resp = get_llm_json_response(client, self._full_prompt + p_case)
            result = resp.get("result")
            if result.upper() == "PASS":
                validator_result["cases"].append({"case": p_case, "result": "PASS"})
            else:
                validator_result["cases"].append({"case": p_case, "result": "FAIL"})
                has_failure = True
        for f_case in self.fail_cases:
            resp = get_llm_json_response(client, self._full_prompt + f_case)
            result = resp.get("result")
            if result.upper() == "FAIL":
                validator_result["cases"].append({"case": f_case, "result": "PASS"})
            else:
                validator_result["cases"].append({"case": f_case, "result": "FAIL"})
                has_failure = True

        validator_result["has_failure"] = has_failure
        return validator_result

    async def run_case(self, client):
        if callable(self.executor):
            value = self.executor(*self.input_args, **self.input_kwargs)
            if inspect.isawaitable(value):
                value = await value
        elif inspect.isawaitable(self.executor):
            value = await self.executor(*self.input_args, **self.input_kwargs)
        else:
            raise TypeError(
                "Expected a callable or an awaitable for the executor input."
            )
        resp = get_llm_json_response(client, self._full_prompt + value)
        result = resp.get("result")
        if result.upper() == "PASS":
            return True
        else:
            return False

    @property
    def _full_prompt(self):
        return self._COMMON_VALIDATOR_PROMPT.format(
            description=self.case_pass_condition
        )


class ValidatedCasesRunner:
    def __init__(self, cases, client=None):
        self.cases = cases
        if not client:
            client = OpenAI()
        self.client = client

    async def run(self):
        results = []
        for case in self.cases:
            validator_results = await case.validate(self.client)
            test_passes = await case.run_case(self.client)
            results.append(
                {
                    "validator_results": validator_results,
                    "test_passes": test_passes,
                }
            )
        return results
