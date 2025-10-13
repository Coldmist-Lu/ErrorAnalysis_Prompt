# generate messages on identifying errors
python GenerateMessages.py -m gpt-3.5-turbo -l zhen -q error -o ./test/messages_error.json --src ./test/src_zhen.txt --tgt ./test/tgt_zhen.txt --ref ./test/ref_zhen.txt
# get responses
python CallChatgpt.py -m gpt-3.5-turbo -p ./test/messages_error.json -t 0 -o ./test/responses_error.json -k API-KEY # replace with your API key
# generate messages on scoring
python GenerateMessages.py -m gpt-3.5-turbo -q score -o ./test/messages_score.json --err ./test/responses_error.json
# get responses
python CallChatgpt.py -m gpt-3.5-turbo -p ./test/messages_score.json -t 0 -o ./test/responses_score.json -k API-KEY # replace with your API key