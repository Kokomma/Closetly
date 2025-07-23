# closet_app.py

import streamlit as st
from PIL import Image
import os
import uuid

# Setup
st.set_page_config(page_title="My Closet App", layout="wide")
st.title("👗🧥 My Digital Closet")

# Image folder
CLOSET_DIR = "closet_images"
if not os.path.exists(CLOSET_DIR):
    os.makedirs(CLOSET_DIR)

# Upload section
st.header("📤 Upload a New Clothing Item")
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    unique_name = f"{uuid.uuid4().hex}_{uploaded_file.name}"
    image_path = os.path.join(CLOSET_DIR, unique_name)

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Image uploaded!")

    # Metadata
    st.subheader("🏷️ Add Tags")
    tag_type = st.text_input("Type (e.g. top, jeans, dress)")
    color = st.text_input("Color (e.g. red, black, blue)")
    occasion = st.text_input("Occasion (e.g. casual, work, party)")

    if st.button("Save Item"):
        with open(image_path.replace(".png", ".txt").replace(".jpg", ".txt"), "w") as f:
            f.write(f"{tag_type},{color},{occasion}")
        st.success("✅ Item saved with tags!")

# Display closet
st.header("🧾 My Closet")
cols = st.columns(4)
images = [f for f in os.listdir(CLOSET_DIR) if f.endswith((".jpg", ".png", ".jpeg"))]

for idx, image_file in enumerate(images):
    path = os.path.join(CLOSET_DIR, image_file)
    with cols[idx % 4]:
        st.image(path, width=150)
        tag_file = path.replace(".png", ".txt").replace(".jpg", ".txt")
        if os.path.exists(tag_file):
            tags = open(tag_file).read().split(",")
            st.caption(f"Type: {tags[0]}\nColor: {tags[1]}\nOccasion: {tags[2]}")
        else:
            st.caption("No tags")

# Outfit preview
st.header("🪞 Outfit Preview")
selected_images = st.multiselect("Choose items to create an outfit", images)

if selected_images:
    for img in selected_images:
        st.image(os.path.join(CLOSET_DIR, img), width=200)
