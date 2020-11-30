class Signature:
    sig = bytearray()
    foot = bytearray()
    last_pdf_foot_offset = 0

    headers = {
        "BMP" : "bytearray(b'BM')",
        "MPG" : "bytearray(b'\\x00\\x00\\x01')",
        "PDF" : "bytearray(b'%PDF')",
        "GIF_1" : "bytearray(b'GIF87a')",
        "GIF_2" : "bytearray(b'GIF89a')",
        "GIF" : "bytearray(b'GIF8Xa')",
        "ZIP" : "bytearray(b'PK\\x03\\04')",
        "JPG" : "bytearray(b'\\xff\\xd8')",
        #"DOCX" : "bytearray(b'PK\\x03\\x04\\x14\\x00\\x06\\x00')",
        "PNG" : "bytearray(b'\\x89PNG\\x0d\\x0a\\x1a\\x0a')",
        "AVI" : "bytearray(b'RIFF....AVI LIST')"
    }

    footers = {
        "MPG" : "bytearray(b'\\x00\\x00\\x01\xb7')",
        "PDF_1" : "\\n\x25\x25EOF",
        "PDF_2" : "\\n\x25\x25EOF\\n",
        "PDF_3" : "\\r\\n\x25\x25EOF\\r\\n",
        "PDF_4" : "\\r\x25\x25EOF\\r",
        "GIF" : "bytearray(b'\\x00\x3b')",
        "ZIP" : "bytearray(b'PK\\x05\\06')",
        "JPG" : "bytearray(b'\\xff\\xd9')",
        "PNG" : "bytearray(b'IEND\\xAE\x42\x62\\x82')",
    }

    footers_l = {
        "MPG" : 4,
        "GIF" : 2,
        "ZIP" : 4,
        "JPG" : 2,
        "PNG" : 8,
    }

    greater_2s_h = ["b'\\x00\\x00'", "b'%P'", "b'GI'", "b'PK'", "b'\\x89P'", "b'RI'", "b'BM'"]
    greater_4s_h = ["b'GIF8'", "b'PK\\x03\\x04'", "b'\\x89PNG'", "b'RIFF'", "b'%PDF'"]
    greater_6s_h = ["b'\\x89PNG\\x0d\\x0a'", "b'GIF87a'", "b'GIF89a'"]
    greater_8s_h = "b'RIFF'"


    def push_h(self, byte):
        self.sig += byte
        if (len(self.sig) > 2):
            #print(str(self.sig[:2])[10:-1]
            if( str(self.sig[:2])[10:-1] in self.greater_2s_h):
                pass
            else:
                del self.sig[0]
        if (len(self.sig) == 4):
            if (not( str(self.sig[:4])[10:-1] in self.greater_4s_h or str(self.sig[:3])[10:-1] == self.headers["MPG"])):
                del self.sig[0]
                del self.sig[0]
        if (len(self.sig) > 4):
            if( str(self.sig[:4])[10:-1] in self.greater_4s_h or str(self.sig[:2]) == self.headers["BMP"]):
                pass
            else:
                del self.sig[0]
        if (len(self.sig) == 6):
            if (not( str(self.sig[:6])[10:-1] in self.greater_6s_h or str(self.sig[:4])[10:-1] == self.greater_8s_h) ):
                del self.sig[0]
                del self.sig[0]
                del self.sig[0]
                del self.sig[0]
        if (len(self.sig) > 6):
            if( str(self.sig[:6])[10:-1] in self.greater_6s_h or str(self.sig[:4])[10:-1] == self.greater_8s_h):
                pass
            else:
                del self.sig[0]

        if (len(self.sig) == 8):
            if (not(str(self.sig[:4])[10:-1] == self.greater_8s_h or str(self.sig) == self.headers["PNG"])):
                del self.sig[0]
                del self.sig[0]
                del self.sig[0]
                del self.sig[0]
                del self.sig[0]
                del self.sig[0]

        if( len(self.sig) > 8):
            if( str(self.sig[:4])[10:-1] == self.greater_8s_h):
                pass
            else:
                del self.sig[0]

        if( str(self.sig) in self.headers.values() and str(self.sig) != self.headers["BMP"] and str(self.sig) != self.headers["MPG"]):
            #print(self.sig)
            ret = self.get_info()
            self.sig = bytearray()
            #print(ret["Type"])
            return ret

        if (str(self.sig[:-1]) == self.headers["MPG"] and int(self.sig[3]) >= 176 and int(self.sig[3]) < 192):
            print(self.sig)
            ret = self.get_info("MPG")
            self.sig = bytearray()
            return ret
        
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
            for head in self.headers.keys():
                if(self.headers[head] == str(self.sig)):
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
            return {"Type": "NULL", "len": 0}

    def push_f(self, byte, file_data, offset):
        self.foot += byte

        if(file_data["Type"] == "PDF"):
            
            if( len(self.foot) < 9 ):
                return -1
            
            #print(str(self.foot) + " " + str(len(self.foot)))
            if (self.footers["PDF_1"] in str(self.foot) or self.footers["PDF_2"] in str(self.foot) or self.footers["PDF_3"] in str(self.foot) or self.footers["PDF_4"] in str(self.foot)):
                #print(str(self.foot) + " " + str(len(self.foot)))
                self.last_pdf_foot_offset = offset
            
            del self.foot[0]

            head = self.push_h(byte)
            if (head["len"] != 0 and self.last_pdf_foot_offset > 0):
                file_len = self.last_pdf_foot_offset - file_data["offset"]
                self.last_pdf_foot_offset = 0
                self.foot = bytearray()
                return file_len
            
            return -1

        if ( len(self.foot) > self.footers_l[file_data["Type"]] ):
            #print(str(self.foot) + " " + str(self.footers_l[file_data["Type"]]))
            del self.foot[0]


        if ( str(self.foot) == self.footers[file_data["Type"]] ):
            self.foot = bytearray()
            return offset - file_data["offset"]

        return -1
                                

        




disk = open("Project2Updated.dd", "rb")
byte = "0"
offset = 0
signature = Signature()
seek_header = True
files = list()
file_data = ""
while byte:
    byte = disk.read(1)
    if(seek_header):
        file_data = signature.push_h(byte)
        if (file_data["len"] > 0):
            #print(file_data["Type"] + " " + str(file_data["len"]) + " " + str(hex(offset)) + "\n")
            file_data["offset"] = offset - len(signature.headers[file_data["Type"]][12:-2])
            files.append(file_data)
            disk.seek(file_data["len"], 1)
        elif (file_data["len"] < 0):
            file_data["offset"] = offset - len(signature.headers[file_data["Type"]][12:-2])
            seek_header = False
            #print(file_data["Type"])
    else:
        file_len = signature.push_f(byte, file_data, offset)
        #print(seek_header)
        if (file_len > 0):
            file_data["len"] = file_len
            files.append(file_data)
            #print(file_data)
            seek_header = True

    offset += 1
    if (offset % 1000000 == 0):
        print(str(offset))

print(files)