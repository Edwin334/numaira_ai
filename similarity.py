import numpy as np
from scipy.spatial.distance import cosine
from dashscope import Generation
#These two functions should run sequentially.
def find_relevant_clips(clips, query_embedding, embed_text, threshold=0.4):
    relevant_clips = []
    for clip in clips:
        clip_embedding = embed_text(clip)
        similarity = 1 - cosine(query_embedding, clip_embedding)
        if similarity >= threshold:
            relevant_clips.append((clip, similarity))
    return sorted(relevant_clips, key=lambda x: x[1], reverse=True)

def identify_exact_words(relevant_clips, revenue_number, api_key):
    clips_text = "\n".join([clip for clip, _ in relevant_clips])
    prompt = (
        f"给定以下文字片段：\n{clips_text}\n\n"
        f"请找出其中与这个数字 {revenue_number} 在意义上相等的文字片段，并从这些文字片段中提取出相关的数字，不论它们是用整数还是百万的形式表示。如果没有意义相等的文字片段，请忽略它们。"
        f"只需回答相关的数字，并使用嵌套列表格式，如 [[123456], [123百万]]。不要包含多余的推理信息。"
    )

    messages = [
        {'role': 'system', 'content': '只回答相关的数字，用嵌套列表装起来，不要包含多余信息'},
        {'role': 'user', 'content': prompt}
    ]


    response = Generation.call(
        model="qwen-max",
        messages=messages,
        result_format='message',
        api_key=api_key
    )

    exact_words = None
    if isinstance(response, dict) and 'output' in response:
        output = response['output']
        if 'choices' in output:
            for choice in output['choices']:
                if 'message' in choice and 'content' in choice['message']:
                    exact_words = choice['message']['content']
                    break
    return exact_words
