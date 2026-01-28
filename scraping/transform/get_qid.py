import hashlib

def get_qid(q, idx):
    text_hash = hashlib.md5(q['ENGLISH']['QUESTION_TEXT'].encode()).hexdigest()[:10]
    return f"q_{q['TEST_ID']}_{idx}_{text_hash}"
