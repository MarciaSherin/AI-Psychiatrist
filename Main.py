import streamlit as st
import re
from datetime import datetime
import pandas as pd
import plotly.express as px
import numpy as np

class EmotionAnalyzer:
    def __init__(self):
        self.emotion_patterns = {
            'Depression': [
                r'\b(sad|depress|hopeless|tired|exhausted|lonely|worthless)\b',
                r'\b(don\'t feel|no point|cant go on|give up)\b'
            ],
            'Anxiety': [
                r'\b(anxious|worried|nervous|stress|panic|fear)\b',
                r'\b(what if|might|could happen|scared of)\b'
            ],
            'Anger': [
                r'\b(angry|mad|furious|rage|hate|frustrated)\b',
                r'\b(can\'t stand|fed up|sick of)\b'
            ],
            'Positive': [
                r'\b(happy|good|great|better|wonderful|excited)\b',
                r'\b(looking forward|proud|grateful|thankful)\b'
            ]
        }

    def analyze_text(self, text):
        text = text.lower()
        emotions = {}
        matched_patterns = {}
        
        # Analyze each emotion
        for emotion, patterns in self.emotion_patterns.items():
            matches = []
            for pattern in patterns:
                found_matches = re.findall(pattern, text)
                if found_matches:
                    matches.extend(found_matches)
            emotions[emotion] = len(matches)
            matched_patterns[emotion] = list(set(matches))
        
        return emotions, matched_patterns

def create_emotion_chart(emotions):
    df = pd.DataFrame(list(emotions.items()), columns=['Emotion', 'Score'])
    fig = px.bar(df, x='Emotion', y='Score',
                 title='Emotion Analysis Scores',
                 color='Emotion',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(
        xaxis_title="Emotion Category",
        yaxis_title="Detection Score",
        showlegend=False
    )
    return fig

def main():
    st.set_page_config(
        page_title="AI Psychiatrist Analysis",
        page_icon="🧠",
        layout="wide"
    )

    # Initialize the analyzer
    analyzer = EmotionAnalyzer()

    # Header
    st.title("AI Psychiatrist Text Analysis")
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
        <p style='color: #666666; margin: 0;'>
            <strong>Note:</strong> This is a demonstration tool. For real mental health support,
            please consult a licensed professional.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Create two columns for input and history
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Text Analysis")
        # Text input
        text_input = st.text_area(
            "Enter text for analysis:",
            height=150,
            placeholder="Type or paste text here..."
        )

        if st.button("Analyze Text", type="primary"):
            if text_input.strip():
                # Perform analysis
                emotions, patterns = analyzer.analyze_text(text_input)
                
                # Store results in session state
                if 'analysis_history' not in st.session_state:
                    st.session_state.analysis_history = []
                
                analysis_result = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'text': text_input,
                    'emotions': emotions,
                    'patterns': patterns
                }
                st.session_state.analysis_history.append(analysis_result)

                # Display results
                st.subheader("Analysis Results")
                
                # Emotion scores visualization
                st.plotly_chart(create_emotion_chart(emotions), use_container_width=True)
                
                # Detailed results in expandable sections
                with st.expander("View Detailed Analysis", expanded=True):
                    # Dominant emotion
                    dominant_emotion = max(emotions.items(), key=lambda x: x[1])
                    if dominant_emotion[1] > 0:
                        st.markdown(f"**Dominant Emotion:** {dominant_emotion[0]}")
                    else:
                        st.markdown("**Dominant Emotion:** Neutral")
                    
                    # Matched keywords
                    st.markdown("**Matched Keywords:**")
                    for emotion, matches in patterns.items():
                        if matches:
                            st.markdown(f"- {emotion}: {', '.join(matches)}")
                    
                    # Raw scores
                    st.markdown("**Raw Emotion Scores:**")
                    score_df = pd.DataFrame(list(emotions.items()), 
                                         columns=['Emotion', 'Score'])
                    st.dataframe(score_df, use_container_width=True)

    with col2:
        st.subheader("Analysis History")
        if 'analysis_history' in st.session_state and st.session_state.analysis_history:
            for i, analysis in enumerate(reversed(st.session_state.analysis_history)):
                with st.expander(f"Analysis {analysis['timestamp']}", expanded=i==0):
                    st.markdown(f"**Input Text:**")
                    st.text(analysis['text'][:100] + "..." if len(analysis['text']) > 100 else analysis['text'])
                    
                    st.markdown("**Results:**")
                    dominant = max(analysis['emotions'].items(), key=lambda x: x[1])
                    st.markdown(f"Dominant Emotion: {dominant[0]}")
                    
                    # Mini bar chart
                    mini_df = pd.DataFrame(list(analysis['emotions'].items()), 
                                         columns=['Emotion', 'Score'])
                    st.bar_chart(mini_df.set_index('Emotion'), use_container_width=True)

    # Add CSS for better styling
    st.markdown("""
        <style>
        .stTextArea textarea {
            font-size: 16px;
        }
        .streamlit-expanderHeader {
            font-size: 14px;
        }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
