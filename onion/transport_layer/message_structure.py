
def message_structure(addr, client, syn, ack, state, message, certificate, req=0):
    ip, server_port = addr
    data = '''
            {
                "certificate": "%s",
                "source_ip": "%s",
                "server_port": "%s",
                "card": "%s",
                "syn": "%s",
                "ack": "%s",
                "s" : "%s",
                "req" : "%s",
                "message" : "%s"
            }
            ''' % (str(certificate), str(ip), str(server_port),
                   str(client), str(syn), str(ack), str(state), str(req), str(message))

    return data
