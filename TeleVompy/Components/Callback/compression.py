from ...Utils.base_class import BaseClass, dprint


class Compression(BaseClass):
    """ A class to handle data compression """

    def __init__(self, input_data: str = ''):
        """ Initialize a new Compression object """
        super().__init__()
        self.__symbols = ",:[](){}"
        self.__input_data = input_data
        self.__data = input_data

    @property
    def data(self) -> str:
        """ Returns the processed data """
        return self.__data

    def __replace_spaces(self) -> None:
        """ Replaces some characters in the data to make it smaller """
        self.__data = self.__data.replace('": "', '":"')
        self.__data = self.__data.replace('": ', '":')
        self.__data = self.__data.replace('", "', '","')
        self.__data = self.__data.replace(', "', ',"')
        self.__data = self.__data.replace(', ', ',')

    def __replace_curly_braces(self) -> None:
        """ Replaces curly braces in the data """
        self.__data = self.__data[1:-1]
    
    def __replace_double_quotes(self) -> None:
        """ Replaces double quotes in the data """
        self.__data = self.__data.replace('"', '')

    def __set_double_quotes(self) -> None:
        """ Set double quotes in the data around chars """
        temp, word = '', ''
        for char in self.__data:
            if char in self.__symbols:
                char = f'"{char}' if char == '{' else char
                char = f'{char}"' if char == '}' else char
                temp += self.__is_int(word) + char
                word = ''
            else:
                word += char
        temp += self.__is_int(word)
        self.__data = temp

    def __set_curly_braces(self) -> None:
        """ Sets curly braces in the data around chars """
        self.__data = '{' + self.__data + '}'

    def __is_int(self, word: str) -> str:
        """ Is word an integer? """
        if not word:
            return ''
        try:
            return str(int(word.replace('"', '')))
        except:
            return f'"{word}"'

    def compression_percentage(self, revers: bool = False) -> None:
        """ Calculates compression percentage """
        try:
            print(f'Input  data: {self.__input_data}\nOutput data: {self.__data}')
            if not revers:
                percent = round((1 - len(self.__data) / len(self.__input_data)) * 100, 3)
                print(f'Compression percentage: {percent}')
            else:
                percent = round((1 - len(self.__input_data) / len(self.__data)) * 100, 3)
                print(f'Decompression percentage (calculate with out spaces): {percent}')
        except Exception as e:
            dprint(self, f"calculating compression percentage error: {e}")

    def compress(self, show: bool = False) -> str:
        """
        Compresses data and returns compressed string

        Returns
        -------
        `str`: The compressed data
        """

        if not self.__data:
            return ''
        
        self.__replace_spaces()
        self.__replace_curly_braces()
        self.__replace_double_quotes()

        if show:
            self.compression_percentage()

        return self.__data

    def decompress(self, show: bool = False) -> str:
        """
        Decompresses compressed data and returns decompressed string

        Returns 
        -------
        `str`: The decompressed data
        """

        if not self.__data:
            return ''
        
        self.__set_double_quotes()
        self.__set_curly_braces()

        if show:
            self.compression_percentage(revers=True)

        return self.__data
