from pipeline import index_document , ask_question
#run once
index_document(
    pdf_path="E:\College study material\SEM-1\Biology\Module 4 - Enzymes.pdf",
    user_id="user_002"
)

#run many times
while True:
    q = input("Ask: ")
    if q.lower() == "exit":
        break

    answer = ask_question(q, user_id="user_002")
    print(answer)

