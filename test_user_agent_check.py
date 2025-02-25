import requests
import pytest

class TestUserAgentCheck:
    user_agents_data = [
        (
            'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'Mobile', 'No', 'Android'
        ),
        (
            'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
            'Mobile', 'Chrome', 'iOS'
        ),
        (
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Googlebot', 'Unknown', 'Unknown'
        ),
        (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
            'Web', 'Chrome', 'No'
        ),
        (
            'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Mobile', 'No', 'iPhone'
        )
    ]

    @pytest.mark.parametrize("user_agent, expected_platform, expected_browser, expected_device", user_agents_data)
    def test_user_agent_check(self, user_agent, expected_platform, expected_browser, expected_device):
        print('\n---')
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        response = requests.get(url, headers={"User-Agent": user_agent})

        result = response.json()

        if result["platform"] == "Unknown" and expected_platform != "Unknown":
            print(f"Platform is not detected for User-Agent: {user_agent}, expected: {expected_platform}")
        elif result["platform"] != expected_platform:
            print(f"Wrong platform for User-Agent: {user_agent}, expected: {expected_platform}, got: {result['platform']}")
            assert False, f"Expected platform: {expected_platform}, but got: {result['platform']}"

        if result["browser"] == "Unknown" and expected_browser != "Unknown":
            print(f"Browser is not detected for User-Agent: {user_agent}, expected: {expected_browser}")
        elif result["browser"] != expected_browser:
            print(f"Wrong browser for User-Agent: {user_agent}, expected: {expected_browser}, got: {result['browser']}")
            assert False, f"Expected browser: {expected_browser}, but got: {result['browser']}"

        if result["device"] == "Unknown" and expected_device != "Unknown":
            print(f"Device is not detected for User-Agent: {user_agent}, expected: {expected_device}")
        elif result["device"] != expected_device:
            print(f"Wrong device for User-Agent: {user_agent}, expected: {expected_device}, got: {result['device']}")
            assert False, f"Expected device: {expected_device}, but got: {result['device']}"
