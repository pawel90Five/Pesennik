import docx


def print_paragraphs(doc):
    for paragraph in doc.paragraphs:
        print(paragraph.text)
        
if __name__ == '__main__':
    doc = docx.Document('src/кусок.docx')

    print_paragraphs(doc)

