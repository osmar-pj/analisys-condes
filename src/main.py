import os
from dotenv import load_dotenv
# pip install wialon
from wialon.sdk import WialonSdk, WialonError, SdkException
"""
WialonSDK example usage
"""
# Initialize Wialon instance
load_dotenv()

def login():
    sdk = WialonSdk(
        is_development=True,
        scheme='https',
        host='hst-api.wialon.com'
    )

    try:
        # If you haven't a token, you should use our token generator
        token = os.getenv('TOKEN')
        # https://goldenmcorp.com/resources/token-generator
        sdk.login(token)
        return sdk
        # sdk.logout()
    except SdkException as e:
        print(f'Sdk related error: {e}')
    except WialonError as e:
        print(f'Wialon related error: {e}')
    except Exception as e:
        print(f'Python error: {e}')