from .localize_html import localize_html
from .get_qid import get_qid

def process_question(q, idx, test_obj):
    q_english = q['ENGLISH']
    q_text = localize_html(q_english['QUESTION_TEXT'])
    
    options_html = ""
    has_options = False
    for i in range(1, 11):
        opt_key = f'OPT{i}'
        if opt_key in q_english and q_english[opt_key]:
            has_options = True
            opt_test = localize_html(q_english[opt_key])
            options_html += f'<li>{opt_test}</li>'
    
    if has_options:
        q_text += f'<ol style="list-style-type:upper-alpha">{options_html}</ol>'

    transformed_q = {
        "global_idx": idx + 1,
        "local_idx": len(test_obj['sections'][0]['questions']) + 1,
        "post_id": get_qid(q, idx),
        "text": q_text,
        "answer": q.get('READABLE_ANSWER', 'Not Answered'),
        "award": float(q.get('RIGHT_MARKS', 0)),
        "penalty": q.get('WRONG_MARKS', "0")
    }
    
    return transformed_q
