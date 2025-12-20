from pipeline import index_document , ask_question
# run once
index_document(
    pdf_path="E:\College study material\SEM-3\starting pages community service.pdf",
    user_id="user_001"
)

# run many times
while True:
    q = input("Ask: ")
    if q == "exit":
        break

    answer = ask_question(q, user_id="user_001")
    print(answer)
