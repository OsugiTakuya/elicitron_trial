import streamlit as st
from langchain_openai import ChatOpenAI
import elicitron
import uuid
import os


st.title("要件定義エージェントデモ")

with st.expander("技術説明"):
    st.write("TBD")


st.divider()


# セッション初期化
session_init_dict = {
    "user_request_value": "",
    "eval_system_msg": elicitron.EVAL_SYSTEM_MSG,
    "eval_human_prefix_msg": elicitron.EVAL_HUMAN_PREFIX_MSG,
    "doc_gen_system_msg": elicitron.DOC_GEN_SYSTEM_MSG,
    "doc_gen_human_prefix_msg": elicitron.DOC_GEN_HUMAN_PREFIX_MSG,
    "doc_gen_human_postfix_msg": elicitron.DOC_GEN_HUMAN_POSTFIX_MSG,
}
for session_name, init_value in session_init_dict.items():
    if session_name not in st.session_state:
        st.session_state[session_name] = init_value


with st.expander("詳細設定"):
    cols = st.columns(2)
    if cols[0].button("要件定義テンプレ"):
        st.session_state["user_request_value"] = ""
        st.session_state["eval_system_msg"] = elicitron.EVAL_SYSTEM_MSG
        st.session_state["eval_human_prefix_msg"] = elicitron.EVAL_HUMAN_PREFIX_MSG
        st.session_state["doc_gen_system_msg"] = elicitron.DOC_GEN_SYSTEM_MSG
        st.session_state["doc_gen_human_prefix_msg"] = elicitron.DOC_GEN_HUMAN_PREFIX_MSG
        st.session_state["doc_gen_human_postfix_msg"] = elicitron.DOC_GEN_HUMAN_POSTFIX_MSG
    if cols[1].button("マテ生ヒアリングテンプレ"):
        st.session_state["user_request_value"] = "xxx"
        st.session_state["eval_system_msg"] = "xxx"
        st.session_state["eval_human_prefix_msg"] = "xxx"
        st.session_state["doc_gen_system_msg"] = "xxx"
        st.session_state["doc_gen_human_prefix_msg"] = "xxx"
        st.session_state["doc_gen_human_postfix_msg"] = "xxx"

    num_personas = st.number_input("生成するペルソナの人数（上限10）", min_value=1, max_value=30, value=5)

    eval_system_msg = st.text_area(
        label="評価エージェント：システムメッセージ",
        value=st.session_state["eval_system_msg"],
    )
    eval_human_prefix_msg = st.text_area(
        label="評価エージェント：入力メッセージ先頭（後に「ユーザリクエスト」「インタビュー結果」が続く）",
        value=st.session_state["eval_human_prefix_msg"],
    )
    doc_gen_system_msg = st.text_area(
        label="文書生成エージェント：システムメッセージ",
        value=st.session_state["doc_gen_system_msg"],
    )
    doc_gen_human_prefix_msg = st.text_area(
        label="文書生成エージェント：入力メッセージ先頭（後に「ユーザリクエスト」「インタビュー結果」が続く）",
        value=st.session_state["doc_gen_human_prefix_msg"],
    )
    doc_gen_human_postfix_msg = st.text_area(
        label="文書生成エージェント：入力メッセージ末尾（出力形式の指定）",
        value=st.session_state["doc_gen_human_postfix_msg"],
    )

    password = st.text_input(
        label="管理者パスワード",
    )


user_request = st.text_area(
    label="エージェントへの要求",
    placeholder="スマホ向け健康管理アプリを開発したい",
    value=st.session_state["user_request_value"],
)

if st.button("実行"):
    if password != "xxxxxxxxxx" and num_personas > 10:
        raise ValueError("ペルソナ数の設定が上限を超えています")
    
    session_id = str(uuid.uuid1())
    result_dir = os.path.join("results", session_id)
    logpath = os.path.join(result_dir, "agents.log")
    os.mkdir(result_dir)
    
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
    final_output = agent.run(user_request=user_request, logpath=logpath) 

    # 最終的な出力を表示
    with st.expander("結果", expanded=True):
        st.markdown(final_output)
