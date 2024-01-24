def get_message_size(message):
    return len(message.encode("utf-8"))


def restricted_message_size(message_size):
    """the message size restricted to 134217728 bytes"""
    if message_size >= 134217728:
        return False
    else:
        return True
