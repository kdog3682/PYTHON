import jieba
from pypinyin import lazy_pinyin, Style

def text_to_pinyin(text):
    words = jieba.cut(text)
    segmented_parts = []

    for word in words:
        part = {}
        part['text'] = word  # Original segment text

        # Check if the word is punctuation
        if word in "，。":
            part['type'] = 'punctuation'
            part['pinyin'] = word  # Punctuation remains the same in Pinyin
        else:
            part['type'] = 'word'
            part['pinyin'] = ''.join(lazy_pinyin(word, style=Style.TONE))  # Convert word to Pinyin

        segmented_parts.append(part)

    # Create a Pinyin sentence from the Pinyin parts
    pinyin_sentence = ' '.join([part['pinyin'] for part in segmented_parts])

    # Create a dictionary object with original text, its Pinyin, and the segmented parts
    result = {
        'text': text,
        'pinyin': pinyin_sentence,
        'parts': segmented_parts
    }

    return result

# Example usage:
# text = "我爱自然语言处理，它非常有趣。"
# pinyin_object = text_to_pinyin(text)
# print(pinyin_object)

