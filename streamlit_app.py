import openai
import streamlit as st

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
    interests = {"興味が強い": [], "どちらともいえない": [], "興味が低い": []}
    for question, response in responses.items():
        if response == "やりたい":
            interests["興味が強い"].append(question)
        elif response == "どちらともいえない":
            interests["どちらともいえない"].append(question)
        else:
            interests["興味が低い"].append(question)

    st.write("### あなたの興味の結果")
    for interest, questions in interests.items():
        st.write(f"**{interest}**")
        for question in questions:
            st.write(f"- {question}")

    # 回答結果を元にChatGPT APIを使用して文章を生成
    if interests["興味が強い"]:
        strong_interests = ", ".join(interests["興味が強い"])
        prompt = f"以下の項目に強い興味を示しています: {strong_interests}. これらの興味に基づいた職業に関するアドバイスを提供してください。"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        advice = response.choices[0].text.strip()
        st.write("### 職業に関するアドバイス")
        st.write(advice)
    else:
        st.write("特に強い興味を示す項目はありませんでした。")

# Streamlitの実行
if __name__ == "__main__":
    st.set_page_config(page_title="職業適性検査")
