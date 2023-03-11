# generate messages on identifying errors
python GenerateMessages.py -l zhen -q error -o ./test/messages_error.json --src ./test/src_zhen.txt --tgt ./test/tgt_zhen.txt --ref ./test/ref_zhen.txt
# get responses
python CallChatGPT.py -m ./test/messages_error.json -t 0 -o ./test/responses_error.json -k api_key # replace with your API key
# generate messages on scoring
python GenerateMessages.py -q score -o ./test/messages_score.json --err ./test/responses_error.json
# get responses
python CallChatGPT.py -m ./test/messages_score.json -t 0 -o ./test/responses_score.json -k api_key # replace with your API key