
def message_structure(addr, syn, ack, message):
    ip, server_port = addr
    data = '''
            {
                "source_ip": "%s",
                "server_port": "%s",
                "syn": "%s",
                "ack": "%s",
                "message" : "%s"
            }
            ''' % (str(ip), str(server_port), str(syn), str(ack), str(message))

    return data
