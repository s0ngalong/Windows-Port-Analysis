#define function for the IPv4 address input
def ValidIP(IP_Address):
    Check = IP_Address.count(".")
    if Check != 3:
        #exits the program with message
        return ('Please input a properly formatted IP Address. \n4 Octets separated by 3 Periods.')
    #split the input by a period.
    Address = IP_Address.split('.')
    OctetNum = ['First','Second','Thirt','Fourth']
    #begin loop to check for type errors
    for I in range(4):
        #try to convert string to intiger
        try:
            int(Address[I])
            #if fails, handle the valueError
        except ValueError:
            return ('The '+str(OctetNum[I])+' Octet has a letter or symbol that is not allowed.')
        #Validate valid numbers
        if int(Address[I]) not in range(256):
            return ('The '+OctetNum[I]+' octet is not within the range of 0 to 255')
    print ('IPv4 Address sucessfully validated.')
    #The return will apply address list after validation runs.
    return IP_Address