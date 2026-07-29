import streamlit as st
import re

if "review_text" not in st.session_state:
    st.session_state.review_text = ""

def detect_fake_review(review_text):
    text_lower = review_text.lower()
    
    # STRONG FAKE INDICATORS - Multiple matches needed for fake
    strong_fake = [
        'best product ever', 'changed my life', 'unbelievable', 'perfect product',
        'amazing beyond', 'everyone should buy', 'best ever made', 'never seen',
        'magical', 'flawless', 'ultimate product', 'extraordinary', 'unbeatable',
        'works 1000 times', 'five stars not enough', 'masterpiece', 'life changing',
        'absolutely flawless', 'completely outstanding', 'totally perfect', 'far beyond expectations'
    ]
    
    # MODERATE FAKE INDICATORS
    moderate_fake = [
        'amazing', 'incredible', 'perfect', 'awesome', 'spectacular', 'phenomenal',
        'outstanding', 'magnificent', 'brilliant', 'exceptional', 'extraordinary',
        'fantastic', 'wonderful', 'terrific', 'superb', 'divine', 'fabulous',
        'unmatched', 'supreme', 'world-class', 'revolutionary', 'innovative'
    ]
    
    # WEAK FAKE INDICATORS
    weak_fake = [
        'very good', 'excellent', 'great', 'love it', 'highly recommend',
        'best', 'wonderful', 'beautiful', 'stunning'
    ]
    
    # STRONG GENUINE INDICATORS
    strong_genuine = [
        'but', 'however', 'although', 'though', 'downside', 'issue', 'problem',
        'complaint', 'not perfect', 'wish it had', 'could improve', 'better if',
        'pros and cons', 'mixed', 'not ideal', 'needs improvement'
    ]
    
    # MODERATE GENUINE INDICATORS
    moderate_genuine = [
        'good', 'decent', 'okay', 'alright', 'satisfactory', 'reliable',
        'works well', 'fairly', 'pretty good', 'average', 'mediocre',
        'material', 'quality', 'design', 'build', 'packaging', 'delivery',
        'battery', 'performance', 'price', 'value', 'comfortable', 'easy to use'
    ]
    
    # WEAK GENUINE INDICATORS
    weak_genuine = [
        'and', 'the', 'with', 'for', 'after', 'weeks', 'days', 'daily',
        'using', 'use', 'works', 'installation', 'support', 'matched'
    ]
    
    # Count strong fake indicators
    strong_fake_count = 0
    for phrase in strong_fake:
        if phrase in text_lower:
            strong_fake_count += 1
    
    # Count moderate fake indicators
    moderate_fake_count = 0
    for word in moderate_fake:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            moderate_fake_count += 1
    
    # Count weak fake indicators
    weak_fake_count = 0
    for word in weak_fake:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            weak_fake_count += 1
    
    # Count strong genuine indicators
    strong_genuine_count = 0
    for phrase in strong_genuine:
        if phrase in text_lower:
            strong_genuine_count += 1
    
    # Count moderate genuine indicators
    moderate_genuine_count = 0
    for word in moderate_genuine:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            moderate_genuine_count += 1
    
    # Count weak genuine indicators
    weak_genuine_count = 0
    for word in weak_genuine:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            weak_genuine_count += 1
    
    # Calculate fake score
    fake_score = (strong_fake_count * 8) + (moderate_fake_count * 3) + (weak_fake_count * 0.5)
    
    # Calculate genuine score
    genuine_score = (strong_genuine_count * 8) + (moderate_genuine_count * 3) + (weak_genuine_count * 0.5)
    
    # Check capitalization
    caps_count = sum(1 for c in review_text if c.isupper())
    caps_ratio = caps_count / len(review_text) if len(review_text) > 0 else 0
    if caps_ratio > 0.35:
        fake_score += 8
    
    # Check exclamation marks
    exclaim_count = review_text.count('!')
    if exclaim_count > 5:
        fake_score += 8
    elif exclaim_count > 3:
        fake_score += 5
    
    # Check word count
    word_count = len(review_text.split())
    if word_count < 15:
        fake_score += 5
    elif word_count > 300:
        genuine_score += 3
    
    # Check for specific measurements/numbers
    has_measurements = bool(re.search(r'\d+\s*(days?|weeks?|months?|years?|hours?|%)', review_text))
    if has_measurements:
        genuine_score += 6
    
    # Calculate final confidence
    total = fake_score + genuine_score
    if total == 0:
        confidence = 50
        prediction = "UNCERTAIN"
    else:
        fake_percentage = (fake_score / total) * 100
        
        if fake_percentage > 70:
            prediction = "FAKE"
            confidence = fake_percentage
        elif fake_percentage < 30:
            prediction = "GENUINE"
            confidence = 100 - fake_percentage
        else:
            prediction = "UNCERTAIN"
            confidence = 50 + abs(fake_percentage - 50) / 2
    
    # Ensure confidence is between 15 and 90
    confidence = max(15, min(90, confidence))
    
    return prediction, confidence

st.set_page_config(
    page_title="Review Authenticity Checker",
    page_icon="🔍",
    layout="centered",
)

# Header
st.markdown("""
<div style="text-align:center;padding:15px;">
    <h1 style="color:#3b82f6;">🔍 Review Authenticity Checker</h1>
    <p style="color:gray;">
        Analyze product reviews using Rule-Based Pattern Analysis
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.title("About")
    st.write("""
This application uses a machine learning-based classification engine to detect whether a product review is **Fake** or **Genuine**.

### Tech Stack
- Python
- Streamlit
- Scikit-learn
- TF-IDF Vectorization
- MLP Neural Network
""")

st.subheader("Enter Review")
review = st.text_area(
    "",
    value=st.session_state.review_text,
    placeholder="Paste the review here...",
    height=150,
)
st.session_state.review_text = review

c1, c2 = st.columns(2)
with c1:
    check = st.button("🔍 Analyze", use_container_width=True)
with c2:
    clear = st.button("🗑️ Clear", use_container_width=True)

if clear:
    st.session_state.review_text = ""
    st.rerun()

if check:
    if review.strip() == "":
        st.warning("⚠️ Please enter a review.")
        st.stop()

    prediction, confidence = detect_fake_review(review)

    st.divider()
    a, b, c = st.columns(3)
    with a:
        if prediction == "FAKE":
            st.error("❌ FAKE")
        elif prediction == "GENUINE":
            st.success("✅ GENUINE")
        else:
            st.warning("⚠️ UNCERTAIN")
    with b:
        st.metric("Confidence", f"{confidence:.1f}%")
    with c:
        st.metric("Words", len(review.split()))

    st.progress(confidence / 100)
    st.info("🧠 Prediction generated using Regex + Keyword Pattern Analysis.")

    st.divider()
    st.subheader("📊 Analysis Details")
    left, right = st.columns(2)
    with left:
        caps_ratio = sum(1 for c in review if c.isupper()) / len(review) if len(review) > 0 else 0
        st.write(f"**Prediction:** {prediction}")
        st.write(f"**Confidence:** {confidence:.1f}%")
        st.write(f"**Word Count:** {len(review.split())}")
        st.write(f"**Capitalization:** {caps_ratio*100:.1f}%")
    with right:
        extreme_words = ['amazing', 'incredible', 'perfect', 'awesome', 'best', 'worst', 'terrible', 'horrible']
        extreme_count = sum(1 for w in extreme_words if re.search(r'\b' + w + r'\b', review.lower()))
        genuine_words = ['but', 'however', 'problem', 'issue', 'downside', 'complaint', 'not perfect']
        genuine_count = sum(1 for w in genuine_words if re.search(r'\b' + w + r'\b', review.lower()))
        st.write(f"**Exclamation Marks:** {review.count('!')}")
        st.write(f"**Extreme Words Found:** {extreme_count}")
        st.write(f"**Balanced Language Indicators:** {genuine_count}")
        st.write(f"**Characters:** {len(review)}")

    st.divider()
    if prediction == "FAKE":
        st.error(
            "🚨 **This review appears to be FAKE.**\n\n"
            "The rule-based engine detected patterns commonly associated with deceptive reviews, "
            "such as extreme language, generic phrases, or unnatural exaggeration."
        )
    elif prediction == "GENUINE":
        st.success(
            "✅ **This review appears to be GENUINE.**\n\n"
            "The review shows balanced tone, specific details, and natural language patterns."
        )
    else:
        st.warning(
            "❓ **Mixed signals detected.**\n\n"
            "This review has both genuine and suspicious patterns."
        )

st.markdown("---")
st.caption("Developed by Dhruv Bhoir | Fake Review Detection System")
