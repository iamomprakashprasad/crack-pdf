import constants
from multi_process import MultiProcess
import multiprocessing

class PasswordsGenerator:
    def __init__(self, *, dummy_password:str=DUMMY_PASSWORD) -> None:
        if not dummy_password:
            dummy_password = ''
        self.dummy_password = dummy_password
        self.current_password = ''
        self.pointer = -1

    def gemerate_next_password(self) -> str:
        shift_pointer = False
        while True:
            current_word = self.current_password[self.pointer]
            # print(f"{current_word=}")
            if current_word in ('9', 'Z', '#'):
                if current_word == '9':
                    # print("ghj")
                    current_word = '0'
                elif current_word == 'Z':
                    current_word = 'a'
                else:
                    current_word = '['
                shift_pointer = True
            elif current_word == 'z':
                current_word = 'A'
            else:
                current_word = self.increment_word(word=current_word)
            self.current_password = self.current_password[:self.pointer]+current_word+self.current_password[self.pointer+1:]
            # print(f"{self.current_password=}")
            if not shift_pointer:
                # print(len(self.current_password))
                self.pointer = len(self.current_password)-1
                return self.current_password
            if not self.pointer:
                raise ValueError("Pattern is wrong", self.dummy_password) 
            self.pointer -= 1
            shift_pointer = False
            
    def increment_word(self, *, word:str) -> str:
        if word.isalpha():
            return chr(ord(word)+1)
        if word.isnumeric():
            return str(int(word)+1)
        else:
            return SPECIAL_CHARS[SPECIAL_CHARS.index(word)+1]

    def get_first_password(self) -> str:
        if self.current_password:
            raise ValueError("password format or first password is already genrated", f"{self.current_password=}")
        for each_word in self.dummy_password:
            if each_word.isnumeric():
                self.current_password+= "0"
            elif each_word.isalpha():
                self.current_password+= 'a'
            else:
                self.current_password+= SPECIAL_CHARS[0]
        print("Password generator is successfully setup and current password trying is --> ", self.current_password)
        self.pointer = len(self.current_password)-1
        return self.current_password
    

class PasswordsGeneratorCPU(MultiProcess):
    def __init__(self, dummy_password: str) -> None:
        self.dummy_password = dummy_password
        self.first_password = self.__get_first_password()
        super().__init__(first_password=self.first_password)
        self.chunk_type = self.get_chunk_type()
        self.chunks_list = self.chunks.get(self.chunk_type)

    def __get_first_password(self) -> str:
        for each_word in self.dummy_password:
            if each_word.isnumeric():
                self.first_password+= "0"
            elif each_word.isalpha():
                self.first_password+= 'a'
            else:
                self.first_password+= SPECIAL_CHARS[0]
        print("Password generator is successfully setup and current password trying is --> ", self.first_password)
        self.pointer = len(self.first_password)-1
        return self.first_password
    
    def get_chunk_type(self):
        if self.chunks.get(constants.ALPHABETS):
            return constants.ALPHABETS
        elif self.chunks.get(constants.NUMBERS):
            return constants.NUMBERS
        else:
            return constants.SPECIAL_CHARS


    def generate_processor_first_password(self, chunks):
        first_password = self.first_password
        self.first_password = {}
        def update_first_password(chunk:list):
            first_chunk_word = chunk[0]
            first_updated_password = ""
            for each_word in first_password:
                if (each_word.isalpha() and self.chunk_type == constants.ALPHABETS) or \
                    (each_word.isnumeric() and self.chunk_type == constants.NUMBERS) or \
                    (each_word in constants.SPECIAL_CHARS_LIST and self.chunk_type == constants.SPECIAL_CHARS):
                    first_updated_password+=first_chunk_word
                else:
                    first_updated_password+=each_word
            return first_updated_password, chunk
        pool = multiprocessing.Pool(processes=self.cpu_count)
        new_passwords = pool.map_async(update_first_password, chunks)
        return list(new_passwords)


        
    
