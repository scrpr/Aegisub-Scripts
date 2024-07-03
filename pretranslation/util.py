from tokencost import count_message_tokens, count_string_tokens

def estimate_token_length(input: str) -> float:
    token_length = 0.0

    for char in input:
        char_code = ord(char)

        if char_code < 128:
            # ASCII character
            if 65 <= char_code <= 122:
                # a-Z
                token_length += 0.25
            else:
                token_length += 0.5
        else:
            # Unicode character
            token_length += 1.5

    return token_length

def calculate_token_cost(messages, model):
    token_cost = 0
    try:
        token_cost = count_message_tokens(messages, model)
    except Exception as e:
        print(f"Token counting failed: {e}, falling back to estimate_token_length.")
        token_cost = estimate_token_length(messages[1]['content'])
    return token_cost