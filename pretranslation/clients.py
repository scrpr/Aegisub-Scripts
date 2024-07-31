import instructor
import scheme
import config
from openai import OpenAI

def call_llm(messages, model, frequency_penalty=0.0):
    if model == "sakura":
        client = OpenAI(base_url=config.SAKURA_URL, api_key=config.SAKURA_KEY)
    elif model.startswith("moonshot"):
        client = OpenAI(base_url="https://api.moonshot.cn/v1", api_key=config.MOONSHOT_KEY)
    else:
        client = OpenAI(base_url=config.OPENAI_URL, api_key=config.OPENAI_KEY)

    print(f"Calling {model} using:\n" + str(messages) + "\n")
    response = client.chat.completions.create(
        model=model,
        response_format={ "type": "json_object" },
        messages=messages,
        frequency_penalty=frequency_penalty,
    )
    
    print(f"{model} returned: \n" + response.choices[0].message.content + "\n")
    if response.choices[0].finish_reason != 'stop':
        raise Exception(f"""Message finished with reason: {response.choices[0].finish_reason}""")
    return response.choices[0].message.content

def call_llm_instructor(messages, model, frequency_penalty=0.0):
    instructor_mode = instructor.Mode.FUNCTIONS
    if model.startswith("claude") or model.startswith("deepseek") or model.startswith("gemini"):
        instructor_mode = instructor.Mode.JSON
    client = instructor.from_openai(OpenAI(base_url=config.OPENAI_URL, api_key=config.OPENAI_KEY), mode=instructor_mode)
    print(f"Calling {model} using:\n" + str(messages) + "\n")

    try:
        response = client.chat.completions.create(
            model=model,
            response_model=scheme.LinesModel,
            messages=messages,
            frequency_penalty=frequency_penalty
        )
    except Exception as e:
        print(f"Exception: {e}")

    print(f"{model} returned: \n" + str(response) + "\n")

    return response