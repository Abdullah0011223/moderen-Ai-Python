import streamlit as st
import json
import os

LIBRARY_FILE = "library.json"

# Load library
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# UI: Book Display
def display_book(book):
    st.markdown(f"**📖 Title:** {book['title']}")
    st.markdown(f"**👤 Author:** {book['author']}")
    st.markdown(f"**📅 Year:** {book['year']}")
    st.markdown(f"**📚 Genre:** {book['genre']}")
    st.markdown(f"**✅ Read:** {'Yes' if book['read'] else 'No'}")
    st.markdown("---")

# Main UI
st.set_page_config(page_title="📚 Personal Library", page_icon="📖")
st.title("📚 Personal Library Manager")

library = load_library()

menu = st.sidebar.selectbox("📌 Menu", [
    "Add Book", "Remove Book", "Search Book", "Display All Books", "Statistics"
])

# 1. Add Book
if menu == "Add Book":
    st.header("➕ Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, format="%d")
        genre = st.text_input("Genre")
        read = st.selectbox("Have you read it?", ["Yes", "No"]) == "Yes"
        submitted = st.form_submit_button("Add Book")
        if submitted:
            new_book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read
            }
            library.append(new_book)
            save_library(library)
            st.success("✅ Book added successfully!")

# 2. Remove Book
elif menu == "Remove Book":
    st.header("❌ Remove a Book")
    titles = [book["title"] for book in library]
    if titles:
        selected = st.selectbox("Select a book to remove", titles)
        if st.button("Remove"):
            library = [book for book in library if book["title"] != selected]
            save_library(library)
            st.success(f"🗑️ '{selected}' removed from library.")
    else:
        st.info("Library is empty.")

# 3. Search Book
elif menu == "Search Book":
    st.header("🔍 Search Book by Title or Author")
    query = st.text_input("Enter title or author")
    if query:
        results = [
            book for book in library
            if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()
        ]
        if results:
            st.success(f"Found {len(results)} result(s):")
            for book in results:
                display_book(book)
        else:
            st.warning("No matching books found.")

# 4. Display All Books
elif menu == "Display All Books":
    st.header("📖 All Books in Your Library")
    if library:
        for book in library:
            display_book(book)
    else:
        st.info("Library is empty.")

# 5. Statistics
elif menu == "Statistics":
    st.header("📊 Library Statistics")
    total = len(library)
    read = sum(1 for book in library if book['read'])
    unread = total - read
    st.markdown(f"📚 **Total Books:** {total}")
    st.markdown(f"✅ **Books Read:** {read}")
    st.markdown(f"📘 **Unread Books:** {unread}")
    if total > 0:
        st.progress(read / total)

