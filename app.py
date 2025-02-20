import streamlit as st
from langchain_openai import ChatOpenAI
import elicitron


st.title("要件定義エージェントデモ")


user_request = st.text_area(
    label="作成したいアプリケーションについて記載",
    placeholder="スマホ向け健康管理アプリを開発したい",
)


with st.expander("詳細設定"):
    cols = st.columns(2)
    if cols[0].button("要件定義テンプレ"):
        pass
    if cols[1].button("マテ生ヒアリングテンプレ"):
        pass

    num_personas = st.number_input("生成するペルソナの人数", min_value=1, max_value=20, value=5)

    eval_system_msg = st.text_area(
        label="評価エージェント：システムメッセージ",
        value=elicitron.EVAL_SYSTEM_MSG,
    )
    eval_human_prefix_msg = st.text_area(
        label="評価エージェント：入力メッセージ先頭（後に「ユーザリクエスト」「インタビュー結果」が続く）",
        value=elicitron.EVAL_HUMAN_PREFIX_MSG,
    )
    doc_gen_system_msg = st.text_area(
        label="文書生成エージェント：システムメッセージ",
        value=elicitron.DOC_GEN_SYSTEM_MSG,
    )
    doc_gen_human_prefix_msg = st.text_area(
        label="文書生成エージェント：入力メッセージ先頭（後に「ユーザリクエスト」「インタビュー結果」が続く）",
        value=elicitron.DOC_GEN_HUMAN_PREFIX_MSG,
    )
    doc_gen_human_postfix_msg = st.text_area(
        label="文書生成エージェント：入力メッセージ末尾（出力形式の指定）",
        value=elicitron.DOC_GEN_HUMAN_POSTFIX_MSG,
    )


if st.button("実行"):
    # ChatOpenAIモデルを初期化
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
    # 要件定義書生成AIエージェントを初期化
    agent = elicitron.DocumentationAgent(
        llm=llm,
        k=num_personas,
        eval_system_msg=eval_system_msg,
        eval_human_prefix_msg=eval_human_prefix_msg,
        doc_gen_system_msg=doc_gen_system_msg,
        doc_gen_human_prefix_msg=doc_gen_human_prefix_msg,
        doc_gen_human_postfix_msg=doc_gen_human_postfix_msg,
    )
    # エージェントを実行して最終的な出力を取得
    final_output = agent.run(user_request=user_request) 

    # 最終的な出力を表示
    print(final_output)
