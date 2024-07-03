import json
import copy
from prompts import PROMPT_CHINESE, SAKURA_SERIES_SYSTEM_PROMPT, PROMPT_USER_SAKURA
import util
import scheme
import clients

def pre_translation_sakura(input_lines, context, keywords, model):
    contexts = {
        "context": context,
        "keywords": keywords,
    }
    lines = []
    lines_stripped = []
    messages = [
            {
                "role": "system",
                "content": SAKURA_SERIES_SYSTEM_PROMPT
            }
    ]
    new_lines = [None] * len(input_lines)

    for i in range (len(input_lines)):
        temp_input = copy.deepcopy(input_lines[i])
        temp_input['index'] = i
        lines.append(temp_input)
        lines_stripped.append(input_lines[i])

        token_count = util.estimate_token_length(json.dumps(lines_stripped, ensure_ascii=False))
        if token_count >= 400:
            # if messages[-1]['role'] == "system":
            #     messages.append({
            #         "role": "user",
            #         "content": PROMPT_USER_SAKURA_V010_FIRST + context + PROMPT_USER_SAKURA_V010_SECOND + json.dumps(lines_stripped, ensure_ascii=False)
            #     })
            # else:
            #     messages.append({
            #         "role": "user",
            #         "content": json.dumps(lines_stripped, ensure_ascii=False)
            #     })
            messages.append({
                "role": "user",
                "content": PROMPT_USER_SAKURA + json.dumps(lines_stripped, ensure_ascii=False)
            })

            try:
                response_raw = clients.call_llm(messages=messages, model=model, frequency_penalty=0.1)

                response = json.loads(response_raw)

                if abs(len(response) - len(lines)) > 2:
                    raise Exception("Incorrect length!")

                for j in range(len(response)):
                    index = lines[j]['index']
                    new_lines[index] = {
                        "speaker": response[j]['speaker'],
                        "text": response[j]['text']
                    }
                
                messages.append({
                    "role": "assistant",
                    "content": response_raw
                })

                if len(messages) >= 5:
                    messages = [{
                        "role": "system",
                        "content": SAKURA_SERIES_SYSTEM_PROMPT
                    }] + messages[-4:] # 最长保存2轮
                lines = []
                lines_stripped = []
            except Exception as e:
                print(f"Exception: {e}.")
                for attempt in range(3):
                    print(f"Retrying ({attempt+1}/3)")
                    try:
                        temp_messages = [{"role": "system", "content": SAKURA_SERIES_SYSTEM_PROMPT}] + messages[-3:]
                        response_raw = clients.call_llm(messages=temp_messages, model=model, frequency_penalty=0.2)

                        response = json.loads(response_raw)
                        
                        if abs(len(response) - len(lines)) > 2:
                            raise Exception("Incorrect length!")

                        for j in range(len(response)):
                            index = lines[j]['index']
                            new_lines[index] = {
                                "speaker": response[j]['speaker'],
                                "text": response[j]['text']
                            }

                        messages.append({
                            "role": "assistant",
                            "content": response_raw
                        })

                        if len(messages) >= 5:
                            messages = [{
                                "role": "system",
                                "content": SAKURA_SERIES_SYSTEM_PROMPT
                            }] + messages[-4:] # 最长保存2轮
                        lines = []
                        lines_stripped = []
                        break
                    except Exception as e:
                        print(f"Exception: {e}.")
                        if attempt >= 2:
                            print("All retries failed. Skipping this batch.")
                            for j in range(len(lines)):
                                index = lines[j]['index']
                                new_lines[index] = {
                                    "speaker": "",
                                    "text": ""
                                }
                            lines = []
                            lines_stripped = []
                            break

            continue
            
    messages.append({
        "role": "user",
        "content": json.dumps(lines_stripped, ensure_ascii=False)
    })
    if len(messages) >= 5:
        messages = [{
            "role": "system",
            "content": SAKURA_SERIES_SYSTEM_PROMPT
        }] + messages[-4:] # 最长保存2轮

    try:
        response_raw = clients.call_llm(messages=messages, model=model, frequency_penalty=0.1)
        response = json.loads(response_raw)

        if abs(len(response) - len(lines)) > 2:
            raise Exception("Incorrect length!")

        for j in range(len(response)):
            index = lines[j]['index']
            new_lines[index] = {
                "speaker": response[j]['speaker'],
                "text": response[j]['text']
            }
    except Exception as e:
        print(f"Exception: {e}")
        for attempt in range(3):
            print(f"Retrying ({attempt+1}/3)")
            try:
                temp_messages = [{"role": "system", "content": SAKURA_SERIES_SYSTEM_PROMPT}] + messages[-3:]
                response_raw = clients.call_llm(messages=temp_messages, model=model, frequency_penalty=0.2)
                response = json.loads(response_raw)

                if abs(len(response) - len(lines)) > 2:
                    raise Exception("Incorrect length!")

                for j in range(len(response)):
                    index = lines[j]['index']
                    new_lines[index] = {
                        "speaker": response[j]['speaker'],
                        "text": response[j]['text']
                    }
                break
            except Exception as e:
                print(f"Exception: {e}")
                if attempt >= 2:
                    print("All retries failed. Skipping this batch.")
    
    for i in range(len(new_lines)):
        if new_lines[i] == None:
            new_lines[i] = {
                "speaker": "",
                "text": ""
            }
    return new_lines

# def pre_translation(input_lines, context, keywords, model):
#     user_content = {
#         "context": context,
#         "keywords": keywords,
#         "lines": [],
#     }
#     messages = [
#             {
#                 "role": "system",
#                 "content": PROMPT_CHINESE
#             },
#             {
#                 "role": "user",
#                 "content": ""
#             }
#     ]
#     new_lines = []

#     for i in range (len(input_lines)):
#         user_content['lines'].append(input_lines[i])
#         messages[1]['content'] = json.dumps(user_content, ensure_ascii=False)
#         token_count = num_tokens_from_messages(messages=messages, model=model) if model.startswith('gpt-') else estimate_token_length(messages[1]['content'])
#         if token_count >= 2000:
#             response = json.loads(call_llm(messages=messages, model=model))
#             for j in range (len(response['lines'])):
#                 new_lines.append(response['lines'][j])
#             user_content['lines'] = []
#             user_content['context'] = response['context']
#             user_content['keywords'] = response['keywords']
#             continue
            
#     response = json.loads(call_llm(messages=messages, model=model))
#     for i in range (len(response['lines'])):
#         new_lines.append(response['lines'][i])
    
#     return new_lines

def pre_translation(input_lines, context, keywords, model, maxtoken):
    base_messages = [
        {"role": "system", "content": PROMPT_CHINESE},
        {"role": "user", "content": ""}
    ]

    def process_lines(start, end, context, keywords):
        if start > end:
            return [], context, keywords
        
        local_lines = copy.deepcopy(input_lines[start:end+1])
        local_user_content = f"context: {context}\nkeywords: {keywords}\n"
        for i in range(len(local_lines)):
            local_lines[i]['id'] = i + start
            local_user_content += f"{local_lines[i]['speaker']}|{local_lines[i]['text']}|{local_lines[i]['id']}\n"
        
        
        local_messages = [
            {"role": "system", "content": PROMPT_CHINESE},
            {"role": "user", "content": local_user_content}
        ]
        token_count = util.calculate_token_cost(messages=local_messages, model=model)

        if token_count <= ( int(maxtoken) + 700 ): # system prompt token
            try:
                response = clients.call_llm_instructor(messages=local_messages, model=model)
            except Exception as e:
                print(f"Exception: {e}")
                print("All retries failed. Skipping this batch.")
                response = scheme.LinesModel(context=context, keywords=keywords, lines=[])
            new_context = response.context
            new_keywords = response.keywords
            return response.lines, new_context, new_keywords

        mid = (start + end) // 2
        first_half, first_context, first_keywords = process_lines(start, mid, context, keywords)
        second_half, second_context, second_keywords = process_lines(mid + 1, end, first_context, first_keywords)
        
        return first_half + second_half, second_context, second_keywords
    
    final_lines, _, _ = process_lines(0, len(input_lines) - 1, context, keywords)
    new_lines = [None] * len(input_lines)
    for line in final_lines:
        i = int(line.id)
        new_lines[i] = {
            "speaker": line.speaker,
            "text": line.text
        }
    for i in range(len(new_lines)):
        if new_lines[i] is None:
            new_lines[i] = {
                "speaker": "",
                "text": ""
            }
    return new_lines
