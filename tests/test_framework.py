import pytest
from validated_ai_tests import Case

from unittest.mock import MagicMock


@pytest.fixture
def sync_case():
    return Case(
        executor=lambda _, __: "Affirmative",
        input_args=[1, "2"],
        input_kwargs={},
        case_pass_condition="Pass, if response signals yes",
        pass_cases=[
            "Affirmative",
            "yes",
            "yep",
            "positive",
        ],
        fail_cases=["No", "negative", ""],
    )


@pytest.fixture
def pass_llm_response():
    mock_llm_response = MagicMock()
    dummy_choice = MagicMock()
    dummy_choice.message.content = '{"result": "PASS", "explanation": "..."}'
    mock_llm_response.choices = [dummy_choice]
    return mock_llm_response


@pytest.fixture
def pass_responding_llm_client(pass_llm_response):
    client = MagicMock()
    client.chat.completions.create.return_value = pass_llm_response
    return client


@pytest.mark.asyncio
async def test_case_run_sync(sync_case, pass_responding_llm_client):
    result, explanation = await sync_case.run_case(pass_responding_llm_client)
    pass_responding_llm_client.chat.completions.create.assert_called_once_with(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": sync_case._full_prompt + "Affirmative"}
        ],
        response_format={"type": "json_object"},
    )
    assert result is True
    assert explanation is not None
