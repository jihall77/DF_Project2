class Signature:
    sig = bytearray()

    headers = {
        "BMP" : "bytearray(b'BM')",
        "MPG" : "bytearray(b'\\x00\\x00\\x01')",
        "PDF" : "bytearray(b'%PDF')",
        "GIF_1" : "bytearray(b'GIF87a')",
        "GIF_2" : "bytearray(b'GIF89a')",
        "ZIP" : "bytearray(b'PZ\\x03\\04')",
        "JPG" : "bytearray(b'\\xff\\xd8')",
        "DOCX" : "bytearray(b'PK\\x03\\x04\\x14\\x00\\x06\\x00')",
        "PNG" : "bytearray(b'\\x89PNG\\x0d\\x0a\\x1a\\x0a')",
        "AVI" : "bytearray(b'RIFF....AVI LIST')"
    }

    greater_2s = ["b'\\x00\\x00'", "b'%P'", "b'GI'", "b'PZ'", "b'PK'", "b'\\x89P'", "b'RI'", "b'BM'"]
    greater_4s = ["b'GIF8'", "b'PK\\x03\\x04'", "b'\\x89PNG'", "b'RIFF'"]
    greater_6s = ["b'PK\\x03\\x04'", "b'\\x89PNG'", "b'RIFF'"]
    greater_8s = "b'RIFF'"

    def push_h(self, byte):
        self.sig += byte
        if (len(self.sig) > 2):
            #print(str(self.sig[:2])[10:-1]
            if( str(self.sig[:2])[10:-1] in self.greater_2s):
                pass
            else:
                del self.sig[0]

        if (len(self.sig) > 4):
            if( str(self.sig[:4])[10:-1] in self.greater_4s or str(self.sig[:2]) == self.headers["BMP"]):
                pass
            else:
                del self.sig[0]
                        
        if (len(self.sig) > 6):
            if( str(self.sig[:4])[10:-1] in self.greater_6s):
                pass
            else:
                del self.sig[0]
                                
        if( len(self.sig) > 8):
            if( str(self.sig[:4])[10:-1] == self.greater_8s):
                pass
            else:
                del self.sig[0]


        if( str(self.sig) in self.headers.values() and str(self.sig) != self.headers["BMP"]):
            print(self.sig)
            self.sig = bytearray()
            return 1

        if (str(self.sig[:-1]) == self.headers["MPG"] and int(self.sig[3]) >= 176 and int(self.sig[3]) < 192):
            print(self.sig)
            self.sig = bytearray()
            return 1
        
        if ("RIFF" in str(self.sig) and "AVI LIST" in str(self.sig)):
            file_info = self.get_info("AVI")
            self.sig = bytearray()
            return file_info

        if (str(self.sig[:2]) == self.headers["BMP"] and len(self.sig) == 6):
            file_info = self.get_info("BMP")
            self.sig = bytearray()
            return file_info

        return {"Type": "none", "len": 0}

    def get_info(self, htype=""):
        if (htype == ""):
            for head in self.headers.values():
                if(self.headers[self.sig] == head):
                    htype = head

        if (htype == "MPG"):
            return {"Type": "MPG", "len": -1}
        elif (htype == "PDF"):
            return {"Type": "PDF", "len": -1}
        elif (htype == "BMP"):
            file_len =  int.from_bytes(self.sig[2:6], 'little')
            return {"Type": "BMP", "len": file_len}
        elif (htype == "GIF_1" or htype == "GIF_2"):
            return {"Type": "GIF", "len": -1}
        elif (htype == "ZIP"):
            return {"Type": "ZIP", "len": -1}
        elif (htype == "JPG"):
            return {"Type": "JPG", "len": -1}
        elif (htype == "DOCX"):
            return {"Type": "DOCX", "len": -1}
        elif (htype == "PNG"):
            return {"Type": "PNG", "len": -1}
        elif (htype == "AVI"):
            file_len = int.from_bytes(self.sig[4:8], 'little')
            return {"Type": "AVI", "len": file_len}
        else:
            return

        




disk = open("Project2Updated.dd", "rb")
byte = "0"
offset = 0
signature = Signature()
seek_header = True
files = list()
file_data = ""
while (byte != "" ):
    byte = disk.read(1)
    if(seek_header):
        file_data = signature.push_h(byte)
        if (file_data["len"] > 0):
            print(file_data["Type"] + " " + str(file_data["len"]) + " " + str(hex(offset)) + "\n")
            file_data.["offset"] = offset - len(signature.headers[file_data["Type"]][12:-2])
            files.append(file_data)
        elif (file_data["len"] < 0):
            file_data.["offset"] = offset - len(signature.headers[file_data["Type"]][12:-2])
            seek_header = False
    else:
        file_len = signature.push_f(byte, file_data)
        if (file_len > 0):
            file_data["len"] = file_len
            files.append(file_data)
            seek_header = True

    offset += 1
