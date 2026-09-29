import streamlit as st
import httpx

st.title("Firm Intelligence")

question = st.text_input("Ask a question")

if st.button("Ask"):
    try:
        response = httpx.post(
            "http://127.0.0.1:8000/agent/ask",
            json={"question": question},
            timeout=30.0,
        )

        response.raise_for_status()
        data = response.json()

        st.write(data["answer"])
        st.write("Tool calls:", data["tool_calls_made"])
        st.write("Input tokens:", data["input_tokens"])
        st.write("Output tokens:", data["output_tokens"])

    except Exception as e:
        st.error(f"Request failed: {e}")

st.subheader("Search knowledge base")

search_query = st.text_input("Search documents")

if st.button("Search"):
    try:
        response = httpx.post(
            "http://127.0.0.1:8000/knowledge/search",
            json={"question": search_query, "top_k": 3},
            timeout=30.0,
        )

        if response.status_code == 409:
            st.warning("Knowledge index has not been built yet.")
        else:
            response.raise_for_status()
            data = response.json()

            for result in data:
                st.write(result["title"])
                st.write("Score:", result["score"])

    except httpx.HTTPError as e:
        st.error(f"Search failed: {e}")

st.subheader("Streaming firm summary")

firm_id = st.number_input("Firm ID", min_value=1, step=1)

if st.button("Get summary"):
    try:
        with httpx.stream(
            "GET",
            f"http://127.0.0.1:8000/firms/{firm_id}/summary/stream",
            timeout=30.0,
        ) as response:
            response.raise_for_status()

            placeholder = st.empty()
            full_text = ""

            for chunk in response.iter_text():
                full_text += chunk
                placeholder.write(full_text)

    except httpx.HTTPError as e:
        st.error(f"Summary failed: {e}")
