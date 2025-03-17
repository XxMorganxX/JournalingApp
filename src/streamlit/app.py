import streamlit as st



# Option 2: Using audio_recorder_streamlit
from audio_recorder_streamlit import audio_recorder as audio_recorder_alt

st.title("Sit down and Yap!")

# A slider widget
number = st.slider("Select a number", 0, 100, 50)
st.write("The selected number is", number)

selected_date = st.date_input("Pick a date")
st.write("You selected:", selected_date)

st.title("Audio Recording Options")


# Option 2: audio_recorder_streamlit
st.subheader("Recording Option 2")
audio_bytes_alt = audio_recorder_alt("Click to record", "Recording...")
if audio_bytes_alt:
    st.audio(audio_bytes_alt, format="audio/wav")
    st.download_button(
        label="Download Recording",
        data=audio_bytes_alt,
        file_name="recording.wav",
        mime="audio/wav"
    )

# A button widget
if st.button("Click me"):
    st.write("Button clicked!")
    