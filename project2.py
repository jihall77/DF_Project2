class Signature:
    sig = bytearray()
    foot = bytearray()
    last_pdf_foot_offset = 0

    headers = {
        #"BMP" : "BM",
        "MPG" : {
            b'\x00\x00\x01\xb0',
            b'\x00\x00\x01\xb1',
            b'\x00\x00\x01\xb2',
            b'\x00\x00\x01\xb3',
            b'\x00\x00\x01\xb4',
            b'\x00\x00\x01\xb5',
            b'\x00\x00\x01\xb6',
            #b'\x00\x00\x01\xb7',
            b'\x00\x00\x01\xb8',
            b'\x00\x00\x01\xb9',
            b'\x00\x00\x01\xba',
            b'\x00\x00\x01\xbb',
            b'\x00\x00\x01\xbc',
            b'\x00\x00\x01\xbd',
            b'\x00\x00\x01\xbe',
            b'\x00\x00\x01\xbf',
        },
        "GIF" : {
            b'GIF87a',
            b'GIF89a'
        },
        "ZIP" : b'PK\x03\04',
        "JPG" : {
            b'\xff\xd8\xff\xe0',
            b'\xff\xd8\xff\xe1',
            b'\xff\xd8\xff\xe2',
            b'\xff\xd8\xff\xe3',
            b'\xff\xd8\xff\xe4',
            b'\xff\xd8\xff\xe5',
            b'\xff\xd8\xff\xe6',
            b'\xff\xd8\xff\xe7',
            b'\xff\xd8\xff\xe8',
            b'\xff\xd8\xff\xe9',
            b'\xff\xd8\xff\xea',
            b'\xff\xd8\xff\xeb',
            b'\xff\xd8\xff\xec',
            b'\xff\xd8\xff\xed',
            b'\xff\xd8\xff\xee',
            b'\xff\xd8\xff\xef',
        },
        #"DOCX" : "bytearray(b'PK\\x03\\x04\\x14\\x00\\x06\\x00')",
        "PNG" : b'\x89PNG\x0d\x0a\x1a\x0a',
        "PDF" : b'%PDF'
        #"AVI" : "RIFF....AVI LIST"
    }

    footers = {
        "MPG" : b'\x00\x00\x01\xb7',
        "PDF_1" : "\\n\x25\x25EOF",
        "PDF_2" : "\\n\x25\x25EOF\\n",
        "PDF_3" : "\\r\\n\x25\x25EOF\\r\\n",
        "PDF_4" : "\\r\x25\x25EOF\\r",
        "GIF" : b'\x00\x3b',
        "ZIP" : b'PK\x05\06',
        "JPG" : b'\xff\xd9',
        "PNG" : b'IEND\xAE\x42\x60\x82',
    }

    footers_l = {
        "MPG" : 4,
        "GIF" : 2,
        "ZIP" : 4,
        "JPG" : 2,
        "PNG" : 8,
    }

    headers_l = {
        "MPG" : 4,
        "GIF" : 6,
        "ZIP" : 4,
        "JPG" : 4,
        "PNG" : 8,
        "AVI" : 16,
        "BMP" : 6,
        "PDF" : 4
    }

    greater_2s_h = ["b'\\x00\\x00'", "b'%P'", "b'GI'", "b'PK'", "b'\\x89P'", "b'RI'", "b'BM'", "b'\\xff\\xd8'"]
    greater_4s_h = ["b'GIF8'", "b'PK\\x03\\x04'", "b'\\x89PNG'", "b'RIFF'", "b'%PDF'"]
    greater_6s_h = ["b'\\x89PNG\\x0d\\x0a'", "b'GIF87a'", "b'GIF89a'"]
    greater_8s_h = "b'RIFF'"


    def bytearray_in(self, b_arr, b_list):
        for item in b_list:
            if (b_arr == item):
                return True
        
        return False

    def push_h(self, byte):
        self.sig += byte
<<<<<<< HEAD
=======
        if (len(self.sig) > 2):
            #print(str(self.sig[:2])[10:-1])
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
            #print(self.sig)
            ret = self.get_info("MPG")
            self.sig = bytearray()
            return ret
>>>>>>> 6838553e18dba9f4c7999cc615c3e85a67d1fc7f
        
        if (len(self.sig) < 16):
            return {"Type": "NULL", "len": 0}

        if ("RIFF" in str(self.sig) and "AVI LIST" in str(self.sig)):
            file_info = self.get_info("AVI")
            #print("AVI")
            self.sig = bytearray()
            return file_info

        if(self.sig[-6:-4] == b'BM'):
            #print("BMP")
            self.sig = self.sig[-6:]
            file_info = self.get_info("BMP")
            self.sig = bytearray()
            return file_info

        if (self.bytearray_in(self.sig[-4:], self.headers["MPG"])):
            #print("MPG")
            self.sig = self.sig[-4]
            file_info = self.get_info("MPG")
            self.sig = bytearray()
            return file_info

        if (self.bytearray_in(self.sig[-4:], self.headers["JPG"])):
            #print("JPG")
            self.sig = self.sig[-4]
            file_info = self.get_info("JPG")
            self.sig = bytearray()
            return file_info

        if (self.bytearray_in(self.sig[-6:], self.headers["GIF"])):
            #print("JPG")
            self.sig = self.sig[-6]
            file_info = self.get_info("GIF")
            self.sig = bytearray()
            return file_info

        if (self.sig[-4:] == self.headers["PDF"]):
            #print("PNG")
            self.sig = self.sig[-4:]
            file_info = self.get_info("PDF")
            self.sig = bytearray()
            return file_info

        if (self.sig[-4:] == self.headers["ZIP"]):
            #print("PNG")
            self.sig = self.sig[-4:]
            file_info = self.get_info("ZIP")
            self.sig = bytearray()
            return file_info

        if (self.sig[-8:] == self.headers["PNG"]):
            #print("PNG")
            self.sig = self.sig[-8:]
            file_info = self.get_info("PNG")
            self.sig = bytearray()
            return file_info

        del self.sig[0]

        return {"Type": "NULL", "len": 0}

    def get_info(self, htype=""):
        if (htype == ""):
            for head in self.headers.keys():
                if(self.headers[head] in str(self.sig)):
                    htype = head

        if (htype == "MPG"):
            #print("MPG")
            return {"Type": "MPG", "len": -1}
        elif (htype == "PDF"):
            return {"Type": "PDF", "len": -1}
        elif (htype == "BMP"):
            #print("BMP")
            file_len =  int.from_bytes(self.sig[2:6], 'little')
            return {"Type": "BMP", "len": file_len}
        elif (htype == "GIF"):
            return {"Type": "GIF", "len": -1}
        elif (htype == "ZIP"):
            return {"Type": "ZIP", "len": -1}
        elif (htype == "JPG"):
            #print("JPG")
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

        #print(self.foot)
        if ( self.foot == self.footers[file_data["Type"]] ):
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
file_stats = {
    "MPG": 0,
    "JPG": 0,
    "BMP": 0,
    "PDF": 0,
    "GIF": 0,
    "ZIP": 0,
    "PNG": 0,
    "AVI": 0
}
while byte:
    byte = disk.read(1)
    if(seek_header):
        file_data = signature.push_h(byte)

        if (file_data["len"] > 0):
            #print(file_data["Type"] + " " + str(file_data["len"]) + " " + str(hex(offset)) + "\n")
            file_data["offset"] = offset - signature.headers_l[file_data["Type"]]
            files.append(file_data)
            file_stats[file_data["Type"]] += 1
            if (file_data["Type"] != "BMP"):
                disk.seek(file_data["len"], 1)
                offset += file_data["len"]
        elif (file_data["len"] < 0):
            file_data["offset"] = offset - signature.headers_l[file_data["Type"]]
            seek_header = False
            print(file_data["Type"])
    else:
        file_len = signature.push_f(byte, file_data, offset)
        #print(seek_header)
        if (file_len > 0):
            file_data["len"] = file_len
            files.append(file_data)
            file_stats[file_data["Type"]] += 1
            print(file_data)
            seek_header = True
            

    offset += 1
    if (offset % 100000 == 0):
        print(str(offset/1000))

f_i = 0
f_j = 1
last_offset = 0
last_run_to = 0
this_offset = 0
bad_files = list()

print(file_stats)

print(len(files))
while f_i < len(files):
    if(files[f_i]["Type"] != "BMP"):
        f_i += 1
        continue
    last_offset = files[f_i]["offset"]
    last_run_to = last_offset + files[f_i]["len"]
    f_j = f_i + 1
    while f_j < len(files):
        
        if (files[f_j]["Type"] == "BMP"):
            f_j += 1
            continue

        this_offset = files[f_j]["offset"]
        #print(str(last_run_to) + " " + str(this_offset))
        if (last_run_to >= this_offset):
            bad_files.insert(0, f_i)
            file_stats["BMP"] -= 1
            break
        f_j += 1
    f_i += 1
    
print(len(bad_files))

for f in bad_files:
    del files[f]

f_i = 0

bad_files.clear()

while f_i < len(files):
    if(files[f_i]["Type"] != "BMP"):
        f_i += 1
        continue
    last_offset = files[f_i]["offset"]
    last_run_to = last_offset + files[f_i]["len"]

    f_j = f_i + 1
    while f_j < len(files):
        if(files[f_j]["Type"] != "BMP" or f_j in bad_files):
            f_j += 1
            continue
        this_offset = files[f_j]["offset"]
        if (last_run_to > this_offset):
            bad_files.insert(0, f_j)
            file_stats["BMP"] -= 1

        f_j += 1
    
    f_i += 1

print(len(bad_files))

for f in bad_files:
    del files[f]
    

print(file_stats)
    #if (offset % 1000000 == 0):
       # print(str(offset))


print(files)
byte = disk.read(-1)
i = 0
for data in files:
    subdata=byte[data["offset"]:data["offset"]+data["len"]]
    carve_file="CarvedFile_"+str(hex(data["offset"])) +"."+ data["Type"]
    carve_obj=open(carve_file, 'wb')
    carve_obj.write(subdata)
    carve_obj.close()
    i=i+1
    print("Found an image, carving to "+carve_file)
