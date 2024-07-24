from extract import extract_text_from_word
from split import split_text_into_clips
from embedding import embed_text
from store import store_clips_to_file
from similarity import find_relevant_clips, identify_exact_words
from format_mapping import format_maps, parse_nested_list

# Qwen API key
api_key = 'sk-1fc2f2739d444a1690d390e9cfdd8b0c'

# File paths
word_file = 'old.docx'
revenue_number = " 10,811,255 " 
new_excel_value = " 10,911,255 " 
clips_file = 'clips.txt'

extracted_text = extract_text_from_word(word_file)
clips = split_text_into_clips(extracted_text)
store_clips_to_file(clips, clips_file)

query_embedding = embed_text(revenue_number)

relevant_clips = find_relevant_clips(clips, query_embedding, embed_text)

exact_words = identify_exact_words(relevant_clips, revenue_number, api_key)

# print("Relevant clips found in the Word file:")
# for clip, similarity in relevant_clips:
#     print(f"Clip: {clip}\nSimilarity: {similarity}\n")

# print("revenue_number:"+revenue_number)
# print("Exact words related to the revenue number:")
# print(exact_words)
# print(type(exact_words))

exact_words_list = parse_nested_list(exact_words)
task = []
for i in exact_words_list:
    temp = []
    i = i.strip()
    temp.append(i[1:-1])
    new_value = format_maps(revenue_number, i[1:-1], new_excel_value).strip().replace("'", '')
    print(new_value)
    temp.append(new_value)
    task.append(temp)
print(task)
    