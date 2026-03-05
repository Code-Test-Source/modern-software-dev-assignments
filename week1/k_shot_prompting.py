from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = """
Write the word backwards, letter by letter from end to beginning.

Examples:
hello: h-e-l-l-o -> o-l-l-e-h = olleh
world: w-o-r-l-d -> d-l-r-o-w = dlrow
python: p-y-t-h-o-n -> n-o-h-t-y-p = nohtyp
example: e-x-a-m-p-l-e -> e-l-p-m-a-x-e = elpmaxe
programming: p-r-o-g-r-a-m-m-i-n-g -> g-n-i-m-m-a-r-g-o-r-p = gnimmargorp
statistics: s-t-a-t-i-s-t-i-c-s -> s-c-i-t-s-i-t-a-t-s = scitsitats
teststring: t-e-s-t-s-t-r-i-n-g -> g-n-i-r-t-s-t-s-e-t = gnirtstset

Example with 10 letters ending in "status":
teststatus: t-e-s-t-s-t-a-t-u-s -> s-u-t-a-t-s-t-s-e-t = sutatstset

Example with 10 letters begining in "http":
httperror: h-t-t-p-e-r-r-o-r -> r-o-r-r-e-p-t-t-h = rorreptth

The input is ONE complete word.
Do not revert only part of the word, and do not change the order of letters other than fully reversing the entire word.
Reverse ALL letters from position 10 to position 1.
Output only the reversed word.
"""

USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"


def test_your_prompt(system_prompt: str) -> bool:
    """Run the prompt up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="codellama:7b-instruct-q4_0",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {output_text}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)
