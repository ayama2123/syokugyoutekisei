import streamlit as st
import openai
import os

# Streamlitのページ設定
st.set_page_config(page_title="職業適性検査")

# OpenAI APIキーの設定
openai.api_key = os.getenv('OPENAI_API_KEY')

# 質問リスト
questions = [
    "工事現場で、ブルドーザーやクレーンを運転する",
    "大学や研究所で、科学の研究をする",
    "雑誌やパンフレットなどにイラストをかく",
    "患者の体温や血圧を測ったり、入院患者の世話をする",
    "社長として、会社の経営の仕事にあたる",
    "文字や数字を、書類に正確に記入する",
    "自動車のエンジンやブレーキを調べて、修理する",
    "新しい薬を開発する",
    "テレビドラマや映画のシナリオを書く",
    "家庭を訪問して、お年寄りや体の不自由な人の世話をする",
    "店長として、商品の仕入れや販売方法を工夫し、売上を伸ばす",
    "帳簿や伝票に書かれた金額の計算をする",
    "木材を加工し、組み立てて、家を建てる",
    "新しい理論を考えて、調査や実験でそれを確かめる",
    "洋服やアクセサリーのデザインをする",
    "保育園で乳幼児の世話をしたり、いっしょに遊んだりする",
    "自分の店を経営する",
    "文字や数字を、コンピュータに入力する",
    "部品を組み立てて機械を作る",
    "環境をよくするために大気や水の汚れを測定し、分析する",
    "人物や風景、物の写真をとり、雑誌やポスターに発表する",
    "悩みをもつ子どもやその家族からの相談にのり、援助する",
    "流行しそうな商品を仕入れ、売り出しの方法を考える",
    "従業員の毎月の給料を計算する",
    "飛行機が安全に飛べるように、点検や整備をする",
    "農業試験場で、農作物の品種改良の研究をする",
    "家具や照明など、部屋のインテリアのデザインをする",
    "ホテルで、宿泊客の受付や、案内などのサービスをする",
    "客を集めるため、広告や催し物などを企画する",
    "会社で書類のコピーをとったり、電話の取次ぎをする",
    "船に乗って、魚や貝などの漁をする",
    "博物館などで、歴史・民俗などの資料を集め、研究する",
    "曲を作ったり、編曲したりする",
    "飛行機の中で、乗客にサービスをする",
    "テレビやラジオの番組を企画し、番組づくりを取り仕切る",
    "依頼に来た客に代わって、役所へ出す書類を作成する",
    "火事の現場に駆けつけ、逃げ遅れた人を助けたり、消火活動を行う",
    "古い地層から化石や骨を集め、恐竜や昔の生き物の生活を調べる",
    "インターネットのホームページのデザインをする",
    "ツアー旅行に同行し、宿や観光の手配など参加者の世話をする",
    "ニュースを読んだり、テレビやラジオの番組の司会をする",
    "銀行で現金を支払ったり、受け取ったりする"
]

# 回答選択肢
options = ["やりたい", "やりたくない", "どちらともいえない"]

# 回答を保存するための辞書
responses = {}

# ヘッダー
st.title("職業適性検査")

# 質問を表示し、回答を収集
for i, question in enumerate(questions):
    st.write(f"**{i+1}. {question}**")
    response = st.radio("", options, index=2, horizontal=True)
    responses[question] = response
    
# 結果を解析して表示
if st.button("分析を開始（少し時間がかかります）"):
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
        prompt = f"以下の項目に基づいて興味関心の傾向と適していると考えられる職業を提案してください。\n\n興味が強い項目: {strong_interests}\n興味が低い項目: {low_interests}\n"

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは回答結果に応じて職業興味と適職を診断するGPTです。"},
                {"role": "user", "content": prompt}
            ]
        )
        advice = response.choices[0].message.content
        st.write("### あなたに合う職業の提案")
        st.write(advice)
    else:
        st.write("特に強い興味を示す項目はありませんでした。")

