from pipeline import index_document, ask_question

# Run once to index a document
# Use forward slashes or raw string for Windows paths
index_document(
    pdf_path=r"E:\College study material\SEM-1\Biology\Module 4 - Enzymes.pdf",  # Note the 'r' prefix
    user_id="user_002"
)

# Run many times to ask questions
while True:
    q = input("Ask: ")
    if q.lower() == "exit":
        break
  
    answer = ask_question(q, user_id="user_002")
    print(f"\n📝 Answer: {answer}\n")