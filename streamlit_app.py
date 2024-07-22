import streamlit as st
import openai
import os

# Streamlitのページ設定
st.set_page_config(page_title="職業適性検査")

# OpenAI APIキーの設定
openai.api_key = os.getenv('OPENAI_API_KEY')

# 質問リスト
questions = [
    "人と話すことが好きですか？",
    "データの分析が得意ですか？",
    "創造的な作業が好きですか？",
    "新しい技術を学ぶことが好きですか？",
    "リーダーシップを発揮することが好きですか？",
    "細かい作業を集中して行うことが得意ですか？",
    "困難な問題を解決することが好きですか？",
    "チームで働くことが好きですか？",
    "自分のアイデアを発表することが得意ですか？",
    "計画を立てて実行することが得意ですか？"
]

# 回答選択肢
options = ["やりたい", "どちらともいえない", "やりたくない"]

# 回答を保存するための辞書
responses = {}

# ヘッダー
st.title("職業適性検査")

# 質問を表示し、回答を収集
for i, question in enumerate(questions):
    response = st.radio(question, options, key=i)
    responses[question] = response

# 結果を解析して表示
if st.button("結果を見る"):
    interests = {"興味が強い": [], "興味が低い": []}
    for question, response in responses.items():
        if response == "やりたい":
            interests["興味が強い"].append(question)
        elif response == "やりたくない":
            interests["興味が低い"].append(question)

    # ChatGPT APIを使用して職業を提案
    if interests["興味が強い"] or interests["興味が低い"]:
        strong_interests = ", ".join(interests["興味が強い"])
        low_interests = ", ".join(interests["興味が低い"])
        prompt = f"以下の項目に基づいて職業を提案してください。\n\n興味が強い項目: {strong_interests}\n興味が低い項目: {low_interests}\n"

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは回答結果に応じて職業興味と適職を診断するGPTです。"},
                {"role": "user", "content": prompt}
            ]
        )
        advice = response.choices[0].messages.content()
        st.write("### あなたに合う職業の提案")
        st.write(advice)
    else:
        st.write("特に強い興味を示す項目はありませんでした。")

