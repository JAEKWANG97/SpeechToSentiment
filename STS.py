import speech_recognition as sr
import requests
import json

# Google Speech Recognition을 사용하여 음성을 텍스트로 변환하는 함수
def recognize_speech_from_mic(recognizer, microphone):
    """마이크로부터 음성을 텍스트로 변환합니다."""
    with microphone as source:
        print("말씀하세요!")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("시간 초과: 사용자가 말을 시작하지 않았습니다.")
            return None

    try:
        text = recognizer.recognize_google(audio, language='ko-KR')
        print("당신이 말한 내용: " + text)
        return text
    except sr.UnknownValueError:
        print("Google 음성 인식이 오디오를 이해하지 못했습니다.")
    except sr.RequestError as e:
        print(f"Google 음성 인식 서비스 요청에 실패했습니다; {e}")
    return None

# Naver Sentiment Analysis API를 사용하여 텍스트의 감정을 분석하는 함수
def analyze_sentiment(text, client_id, client_secret):
    """텍스트의 감정을 분석합니다."""
    url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/json"
    }
    data = {"content": text}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    rescode = response.status_code
    if rescode == 200:
        return response.text
    else:
        print("Error : " + response.text)
        return None

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    client_id = "제공받은API ID"
    client_secret = "제공받은API Secret"

    text = recognize_speech_from_mic(recognizer, microphone)
    if text:
        sentiment_result = analyze_sentiment(text, client_id, client_secret)
        if sentiment_result:
            print(json.dumps(json.loads(sentiment_result), indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
