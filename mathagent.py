import math
import streamlit as st

# =========================
# 1. "Tools" (atomic skills)
# =========================

def add_numbers(a: int, b: int) -> int:
    """Return a + b."""
    return a + b

def subtract_numbers(a: int, b: int) -> int:
    """Return a - b."""
    return a - b

def multiply_numbers(a: int, b: int) -> int:
    """Return a * b."""
    return a * b

def is_prime(n: int) -> bool:
    """Return True if n is prime, else False."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    # check divisors of form 6k ± 1 up to sqrt(n)
    i = 5
    while i * i <= n:
        if (n % i == 0) or (n % (i + 2) == 0):
            return False
        i += 6
    return True


# =======================================
# 2. Agent logic (business orchestration)
# =======================================

def math_agent(a: int, b: int) -> dict:
    """
    This is the 'agent controller'.
    It uses the tools above to produce a structured answer.
    """
    result_add = add_numbers(a, b)
    result_sub = subtract_numbers(a, b)
    result_mul = multiply_numbers(a, b)
    prime_a = is_prime(a)
    prime_b = is_prime(b)

    # Friendly summary text for normal users
    summary_lines = []
    summary_lines.append(f"The sum of {a} and {b} is {result_add}.")
    summary_lines.append(f"{a} minus {b} is {result_sub}.")
    summary_lines.append(f"The product of {a} and {b} is {result_mul}.")
    summary_lines.append(f"{a} is {'a prime' if prime_a else 'not a prime'} number.")
    summary_lines.append(f"{b} is {'a prime' if prime_b else 'not a prime'} number.")
    summary_text = " ".join(summary_lines)

    # Structured response (could be returned as JSON if you later expose an API)
    return {
        "inputs": {"a": a, "b": b},
        "operations": {
            "addition": {
                "expression": f"{a} + {b}",
                "value": result_add,
            },
            "subtraction": {
                "expression": f"{a} - {b}",
                "value": result_sub,
            },
            "multiplication": {
                "expression": f"{a} * {b}",
                "value": result_mul,
            },
        },
        "prime_analysis": {
            "a_is_prime": prime_a,
            "b_is_prime": prime_b,
        },
        "summary_text": summary_text,
    }


# ==========================
# 3. Streamlit UI (frontend)
# ==========================

st.set_page_config(
    page_title="AI Math Agent Demo",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 AI Math Agent Demo")
st.write(
    "Public demo agent. Enter two whole numbers. "
    "The agent will calculate add / subtract / multiply "
    "and tell you if each number is prime."
)

# Input area
col1, col2 = st.columns(2)
with col1:
    a = st.number_input("Number A", value=7, step=1)
with col2:
    b = st.number_input("Number B", value=10, step=1)

# Run button
if st.button("Run Agent"):
    # run core logic
    agent_result = math_agent(int(a), int(b))

    # ---- Results section ----
    st.subheader("Results")

    st.markdown("#### ➕ Addition")
    st.code(
        f"{agent_result['operations']['addition']['expression']} = "
        f"{agent_result['operations']['addition']['value']}"
    )

    st.markdown("#### ➖ Subtraction")
    st.code(
        f"{agent_result['operations']['subtraction']['expression']} = "
        f"{agent_result['operations']['subtraction']['value']}"
    )

    st.markdown("#### ✖ Multiplication")
    st.code(
        f"{agent_result['operations']['multiplication']['expression']} = "
        f"{agent_result['operations']['multiplication']['value']}"
    )

    # Prime checks
    st.markdown("#### 🔍 Prime Check")
    a_prime_flag = agent_result["prime_analysis"]["a_is_prime"]
    b_prime_flag = agent_result["prime_analysis"]["b_is_prime"]

    st.write(
        f"Is **{agent_result['inputs']['a']}** prime? "
        + ("✅ Yes" if a_prime_flag else "❌ No")
    )
    st.write(
        f"Is **{agent_result['inputs']['b']}** prime? "
        + ("✅ Yes" if b_prime_flag else "❌ No")
    )

    # Summary
    st.markdown("---")
    st.markdown("#### 🗒 Summary (ready to copy/paste)")
    st.success(agent_result["summary_text"])

    # Optional: raw JSON for devs
    with st.expander("Developer View (JSON output)"):
        st.json(agent_result)


# ==========================
# 4. Footer / guidance
# ==========================
st.markdown("---")
st.caption(
    "This is a public-safe agent example. "
    "No personal data, no API keys, no company secrets. "
    "In real HR / Finance agents, you'd secure this behind login."
)
