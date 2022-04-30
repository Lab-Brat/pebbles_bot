import subprocess

def test_response(input_text):
    user_message = str(input_text).lower()

    if user_message == 'hi':
        return 'im here to help with Linux and chew bubblegum'

    if user_message == 'ram':
        ram = subprocess.check_output(['free', '-h'])
        return ram.decode('ascii')

