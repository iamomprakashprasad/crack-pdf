import multiprocessing

from constants import SPECIAL_CHARS_LIST, ALPHABETS, NUMBERS, SPECIAL_CHARS

class MultiProcess:
    def __init__(self, first_password:str) -> None:
        self.cpu_count = multiprocessing.cpu_count()
        self.first_password = first_password
        self.chunks = self.__get_chunks(self.__chunk_creation_type()) if self.cpu_count else {}

    def __create_alphabets_chunks(self):
        lower_case = [chr(each_word) for each_word in range(97, 123) ]
        upper_case = list(map(lambda x: x.upper(), lower_case))
        alphabets = lower_case+upper_case
        del lower_case, upper_case
        return self.__create_chunks(data=alphabets)

    def __create_nums_chunks(self):
        numbers = list(range(10))
        chunkked_nums = list()
        return self.__create_chunks(data=numbers)
            
    def __create_spl_chrs_chunks(self):
        return self.__create_chunks(data=SPECIAL_CHARS_LIST)

    def __chunk_creation_type(self):
        alphabets, numbers, spl_chrs = (0,)*3
        for each_word in self.first_password:
            if each_word.isalpha():
                alphabets+=1
            elif each_word.isnumeric():
                numbers+=1
            else:
                spl_chrs+=1
        if alphabets>=numbers>=spl_chrs or alphabets>=spl_chrs>=numbers:
            max_type = ALPHABETS
        elif numbers>=alphabets>=spl_chrs or numbers>=spl_chrs>=alphabets:
            max_type = NUMBERS
        else:
            max_type = SPECIAL_CHARS
        print(f"{max_type=}")
        return max_type

    def __get_chunks(self, max_type:str):
        if max_type == ALPHABETS:
            return {f"{ALPHABETS}": self.__create_alphabets_chunks()}
        elif max_type == NUMBERS:
            return {f"{NUMBERS}": self.__create_nums_chunks()}
        else:
            return {f"{SPECIAL_CHARS}": self.__create_spl_chrs_chunks()}
    
        
    def __create_chunks(self, data:list, chunkked_data:list=[]) -> list:
        each_chunk_size, remanings = divmod(len(data), self.cpu_count)
        if not each_chunk_size: return data
        for each_word in range(0, len(data)-remanings, each_chunk_size):
            chunkked_data.append(data[each_word:each_word+each_chunk_size])
        if remanings<= len(chunkked_data):
            chunkked_data = self.__merrge_remainings(remanings, chunkked_data, data)
        else:
            chunkked_data = self.__create_chunks_execute(data[-remanings:], chunkked_data)
        return chunkked_data

    def __merrge_remainings(self, remanings:int, chunkked_data:list, data:list) -> list:
            while remanings:
                chunkked_data[remanings-1].append(data[-remanings])
                remanings-=1
            return chunkked_data

if __name__ == "__main__":
    mp = MultiProcess(first_password='{'*8+'a')
    print(mp.chunks)


