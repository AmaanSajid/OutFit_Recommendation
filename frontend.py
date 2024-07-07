import streamlit as st
from PIL import Image
import io
from Upload_database import insert_clothing_item, get_all_clothing_items, get_clothing_item_by_id
from vision_llm import generate_outfit_combinations

def format_items_for_llm(items):
    formatted_items = []
    for item in items:
        item_id, item_type, color, style, image_path, _ = item
        formatted_items.append({
            "id": item_id,
            "type": item_type,
            "color": color,
            "style": style
        })
    return formatted_items

def main():
    st.title("Weekly Outfit Planner")

    # Sidebar for uploading new clothing item
    with st.sidebar:
        st.header("Add New Clothing Item")
        uploaded_file = st.file_uploader("Upload a clothing item image", type=["jpg", "png"])
        if uploaded_file is not None:
            # Preview the uploaded image
            image = Image.open(uploaded_file)
            # Resize image to a small, constant size
            image.thumbnail((100, 100))  # Resize image while maintaining aspect ratio
            st.image(image, caption="Preview", use_column_width=False, width=100)
            
            # Get item details
            item_type = st.selectbox("Item type", ["top", "bottom"])
            color = st.text_input("Color")
            style = st.text_input("Style")
            
            if st.button("Save Item"):
                # Reset the file pointer to the beginning of the file
                uploaded_file.seek(0)
                item_id = insert_clothing_item(item_type, color, style, uploaded_file)
                st.success(f"Item saved successfully with ID: {item_id}")

    # Main area for generating and displaying outfits
    st.header("Generate Weekly Outfits")
    if st.button("Generate Outfits"):
        items = get_all_clothing_items()
        formatted_items = format_items_for_llm(items)
        
        # Generate outfit combinations using LLM
        outfit_combinations = generate_outfit_combinations(formatted_items)
        for outfit in outfit_combinations:
            st.subheader(f"Day {outfit['day']}")
            col1, col2 = st.columns(2)
            
            # Display top
            top_item = get_clothing_item_by_id(outfit['top'])
            try:
                top_image = Image.open(top_item[4])
                top_image.thumbnail((150, 150))
                with col1:
                    st.image(top_image, caption=f"Top: {top_item[3]} ({top_item[2]})", use_column_width=False, width=150)
            except Exception as e:
                st.error(f"Error loading top image: {e}")
            
            # Display bottom
            bottom_item = get_clothing_item_by_id(outfit['bottom'])
            try:
                bottom_image = Image.open(bottom_item[4])
                bottom_image.thumbnail((150, 150))
                with col2:
                    st.image(bottom_image, caption=f"Bottom: {bottom_item[3]} ({bottom_item[2]})", use_column_width=False, width=150)
            except Exception as e:
                st.error(f"Error loading bottom image: {e}")
                
if __name__ == "__main__":
    main()