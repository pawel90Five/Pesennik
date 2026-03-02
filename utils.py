from math import ceil
from pymupdf import Document, Font, Page

class Song:
    """ class for song with chord, text and coordinates """
    __font_tiro = Font("tiro")
    __font_tibo = Font("tibo")

    def __init__(self, header:str, 
                 header_coords:tuple, 
                 text:list[tuple]) -> None:
        self.header = header
        self.header_coords = header_coords
        self.text = self.__prepare_text(text) # 
        self.anchor_point = self.__find_anchor_point(header_coords, self.text)
        self.max_length_line = self.__find_max_length(self.text)

    def __prepare_text(self, text:list[tuple]) -> list[tuple]:
        """ returns list of tuples (coords, text) """
        new_text = []
        try:
            new_text.append(text[0])
        except IndexError:
            print(text)
        for i in range(len(text) - 1):
            c1 = text[i][0][0][1]
            c2 = text[i + 1][0][0][1]

            if c2 <= c1:
                anchor = c1
                for j in range(i+1, len(text)):
                    new_text.append(
                        (
                            (
                                (
                                    text[j][0][0][0],
                                    text[j][0][0][1] + anchor
                                ),
                                text[j][0][1]
                            ),
                            text[j][1]
                        )
                    )
                        
                break
            else:
                new_text.append(text[i+1])
        return new_text
    def __find_anchor_point(self, header_coords:tuple, text:dict) -> tuple:
        """ returns anchor point of song """
        x = min([x[0][0][0] for x in text] + [header_coords[0]])
        y = min([y[0][0][1] for y in text] + [header_coords[1]])
        return (x, y)

    def __find_max_length(self, text:list[tuple], fontsize:int=12) -> int:
        """ returns max length of text in song """
        lengths = []
        lengths.append(self.__font_tibo.text_length(self.header, 
                                              fontsize+4))

        for line in text:
            if line[0][1] == 'bold':
                lengths.append(
                    self.__font_tibo.text_length(line[1], 
                                              fontsize)
                )
            else:
                lengths.append(
                    self.__font_tiro.text_length(line[1], 
                                              fontsize)
                )

        return max(lengths)

    def insert_to_doc(self, doc:Document) -> None:
        pass

    def insert_to_page(self, page:Page, point:tuple[int], fs:int=12) -> None:
        """ insert song to page """
        page.insert_font(fontname="timesroman", fontbuffer=self.__font_tiro.buffer)
        page.insert_font(fontname="timesbold", fontbuffer=self.__font_tibo.buffer)
        
        diff = (
            self.anchor_point[0] - point[0],
            self.anchor_point[1] - point[1]
        )
        page.insert_text((self.header_coords[0]-diff[0], 
                          self.header_coords[1]-diff[1]), 
                         text=self.header, fontsize=fs+4, fontname="timesbold") 
        for i in self.text:
            page.insert_text(
                (i[0][0][0]-diff[0], 
                 i[0][0][1]-diff[1]),
                text=i[1],
                fontsize=fs,
                fontname="timesbold" if i[0][1] == 'bold' else "timesroman",
                encoding=2,
            )
           
 
def is_header_line(spans:dict, fs:int=12) -> bool:
    """ returns True if line is header """
    start_words = [
        "предприпев",
        "пред припев",
        "пред. припев",
        "припев",
        "пиан:",
        "купл",
        "кон",
        "в кон",
        "куп.",
        "пр:",
        "пр."
        "п :",
        "п:",
        "проиг",
        "пов:",
        "запев",
        "вст.",
        "вст:",
        "мост",
        "мостик",
        "бридж",
        "бас",
        ":", "a", "b", "c", "d", "e", "f", "g", "h", "m", "#", "1", "2", "3",
        "е ", "а ", "с ", "н "
    ]
    if not all(["bold" in s["font"].lower() for s in spans]) or \
       not all([s["size"] >= fs for s in spans]):
        return False
    
    txt:str = "".join([span["text"] for span in spans]).strip().lower()

    if any([txt.startswith(w) for w in start_words]):
        return False
    
    return True

def less_spaces(s:str, n:int=2) -> str:
    """ returns string with less spaces by n times"""
    spaces = 0
    res = []
    for i in range(len(s)):
        if s[i] == ' ':
            spaces += 1
        else:
            res.append(" " * ceil(spaces / n))
            res.append(s[i])
            spaces = 0
    return ''.join(res)



if __name__ == '__main__':
    text = "   F     G"
    print(less_spaces(text, 2))