def handle_uploaded_file(f):  
    with open('OJ/codeFiles'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  